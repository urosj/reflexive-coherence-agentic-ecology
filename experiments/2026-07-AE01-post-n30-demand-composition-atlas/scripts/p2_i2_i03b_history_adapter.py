"""Minimal active-history adapter selected by P2-I2-I03B.

The adapter owns one externally persisted, independently intervenable ordered
history and its readout materialization request. It never computes or schedules
the later response. Native PyGRC packet operations own every coherence change.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence


ADAPTER_ARTIFACT_KIND = "p2_i2_i03b_active_history_adapter"
ADAPTER_SCHEMA_VERSION = "p2_i2_i03b_active_history_adapter_v1"
TOKEN_FIELDS = (
    "sequence_index",
    "contact_amount",
    "operation_kind",
    "inter_arrival_interval",
)
ROUTE_LOCAL_CONTACT = "route_local_pulse_contact"
PACKET_ARRIVAL = "lgrc9v3_packet_arrival"


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("utf-8")


def digest_canonical(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _finite(value: Any, *, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _canonical_token(value: Mapping[str, Any], *, expected_index: int) -> dict[str, Any]:
    _require(set(value) == set(TOKEN_FIELDS), "history token fields do not match schema")
    sequence_index = int(value["sequence_index"])
    _require(sequence_index == expected_index, "history token sequence is not contiguous")
    amount = _finite(value["contact_amount"], name="contact_amount")
    _require(amount > 0.0, "contact_amount must be positive")
    operation_kind = str(value["operation_kind"])
    _require(
        operation_kind == "native_arrival_contact_amount",
        "unsupported history-token operation kind",
    )
    interval = _finite(
        value["inter_arrival_interval"],
        name="inter_arrival_interval",
    )
    _require(interval >= 0.0, "inter_arrival_interval must be nonnegative")
    return {
        "sequence_index": sequence_index,
        "contact_amount": amount,
        "operation_kind": operation_kind,
        "inter_arrival_interval": interval,
    }


class RCAEActiveHistoryAdapterV1:
    """One common source-label-free active history and native readout bridge."""

    def __init__(
        self,
        *,
        carrier_id: str,
        pool_target_node_id: int,
        registered_source_node_ids: Sequence[int],
        readout_node_id: int,
        positive_reservoir_node_id: int,
        negative_sink_node_id: int,
        positive_edge_id: int,
        negative_edge_id: int,
        recency_coefficient: float,
    ) -> None:
        coefficient = _finite(recency_coefficient, name="recency_coefficient")
        _require(0.0 < coefficient < 1.0, "recency_coefficient must be in (0, 1)")
        sources = tuple(sorted(int(item) for item in registered_source_node_ids))
        _require(bool(sources), "at least one registered source is required")
        _require(len(set(sources)) == len(sources), "registered sources must be unique")
        self._config = {
            "carrier_id": str(carrier_id),
            "pool_target_node_id": int(pool_target_node_id),
            "registered_source_node_ids": list(sources),
            "readout_node_id": int(readout_node_id),
            "positive_reservoir_node_id": int(positive_reservoir_node_id),
            "negative_sink_node_id": int(negative_sink_node_id),
            "positive_edge_id": int(positive_edge_id),
            "negative_edge_id": int(negative_edge_id),
            "recency_coefficient": coefficient,
            "token_schema": list(TOKEN_FIELDS),
            "readout_rule": "r_next=lambda*r_previous+contact_amount",
        }
        _require(self._config["carrier_id"] != "", "carrier_id must not be empty")
        self._state = self._empty_state()
        self._reset_baseline = deepcopy(self._state)

    @staticmethod
    def _empty_state() -> dict[str, Any]:
        return {
            "tokens": [],
            "scan_index": 0,
            "consumed_surface_digests": [],
            "last_arrival_event_time": None,
            "last_materialized_readout": None,
            "last_materialization": None,
            "interventions": [],
            "ingest_call_count": 0,
            "materialization_call_count": 0,
        }

    @property
    def carrier_id(self) -> str:
        return str(self._config["carrier_id"])

    @property
    def tokens(self) -> tuple[dict[str, Any], ...]:
        return tuple(deepcopy(self._state["tokens"]))

    @property
    def readout_node_id(self) -> int:
        return int(self._config["readout_node_id"])

    def readout(self) -> float:
        value = 0.0
        coefficient = float(self._config["recency_coefficient"])
        for token in self._state["tokens"]:
            value = coefficient * value + float(token["contact_amount"])
        return value

    def ingest_new_rows(self, model: Any) -> tuple[dict[str, Any], ...]:
        """Append physical tokens from newly visible registered native arrivals."""

        rows = model.get_state().causal_pulse_substrate_surface_log
        start = int(self._state["scan_index"])
        _require(start <= len(rows), "native surface log moved behind adapter cursor")
        registered_sources = set(self._config["registered_source_node_ids"])
        consumed = set(self._state["consumed_surface_digests"])
        appended: list[dict[str, Any]] = []
        for row in rows[start:]:
            if row.surface_kind != ROUTE_LOCAL_CONTACT:
                continue
            if row.pulse_event_kind != PACKET_ARRIVAL:
                continue
            if int(row.target_node_id) != int(self._config["pool_target_node_id"]):
                continue
            if int(row.source_node_id) not in registered_sources:
                continue
            digest = str(row.surface_digest)
            _require(digest not in consumed, "native contribution row consumed twice")
            event_time = _finite(row.event_time_key, name="row.event_time_key")
            previous = self._state["last_arrival_event_time"]
            interval = 0.0 if previous is None else event_time - float(previous)
            _require(interval >= 0.0, "admitted arrival history is not time ordered")
            token = _canonical_token(
                {
                    "sequence_index": len(self._state["tokens"]),
                    "contact_amount": float(row.contact_amount),
                    "operation_kind": "native_arrival_contact_amount",
                    "inter_arrival_interval": interval,
                },
                expected_index=len(self._state["tokens"]),
            )
            self._state["tokens"].append(token)
            self._state["consumed_surface_digests"].append(digest)
            self._state["last_arrival_event_time"] = event_time
            consumed.add(digest)
            appended.append(deepcopy(token))
        self._state["scan_index"] = len(rows)
        self._state["ingest_call_count"] += 1
        return tuple(appended)

    def replace_history(
        self,
        tokens: Sequence[Mapping[str, Any]],
        *,
        intervention_id: str,
        reason: str,
    ) -> dict[str, Any]:
        """Apply an explicit history-only intervention without rewriting audit rows."""

        before = self.current_identity_digest()
        canonical = [
            _canonical_token(token, expected_index=index)
            for index, token in enumerate(tokens)
        ]
        self._state["tokens"] = canonical
        self._state["last_arrival_event_time"] = None
        intervention = {
            "intervention_id": str(intervention_id),
            "reason": str(reason),
            "before_current_identity_digest": before,
            "after_token_digest": digest_canonical(canonical),
            "native_audit_rewritten": False,
            "success_or_response_written": False,
        }
        _require(intervention["intervention_id"] != "", "intervention_id required")
        _require(intervention["reason"] != "", "intervention reason required")
        self._state["interventions"].append(intervention)
        intervention["after_current_identity_digest"] = self.current_identity_digest()
        return deepcopy(intervention)

    def materialize_readout(
        self,
        model: Any,
        *,
        departure_event_time_key: float,
        arrival_event_time_key: float,
        scheduler_event_index: int,
        packet_index: int,
    ) -> dict[str, Any]:
        """Use one native balancing packet to make M_H equal the H_P readout."""

        target = self.readout()
        node_id = int(self._config["readout_node_id"])
        before = float(model.get_state().base_state.nodes[node_id].coherence)
        delta = target - before
        packet_scheduled = not math.isclose(delta, 0.0, rel_tol=0.0, abs_tol=1e-12)
        transfer: dict[str, Any] | None = None
        if packet_scheduled:
            if delta > 0.0:
                source = int(self._config["positive_reservoir_node_id"])
                destination = node_id
                edge = int(self._config["positive_edge_id"])
                direction = "positive_reservoir_to_readout"
            else:
                source = node_id
                destination = int(self._config["negative_sink_node_id"])
                edge = int(self._config["negative_edge_id"])
                direction = "readout_to_negative_sink"
            amount = abs(delta)
            model.schedule_packet_departure(
                source_node_id=source,
                target_node_id=destination,
                edge_id=edge,
                amount=amount,
                departure_event_time_key=float(departure_event_time_key),
                arrival_event_time_key=float(arrival_event_time_key),
                scheduler_event_index=int(scheduler_event_index),
                packet_index=int(packet_index),
                source_lineage_id=f"rcae-history-readout:{self.carrier_id}",
                target_lineage_id=f"rcae-history-readout-port:{self.carrier_id}",
            )
            for _ in range(2):
                _require(
                    bool(model.get_state().packet_ledger.event_queue_records),
                    "native balancing queue drained early",
                )
                model.step()
            _require(
                not model.get_state().packet_ledger.event_queue_records,
                "native balancing queue not drained",
            )
            transfer = {
                "direction": direction,
                "source_node_id": source,
                "target_node_id": destination,
                "edge_id": edge,
                "amount": amount,
                "departure_event_time_key": float(departure_event_time_key),
                "arrival_event_time_key": float(arrival_event_time_key),
                "scheduler_event_index": int(scheduler_event_index),
                "packet_index": int(packet_index),
            }
        after = float(model.get_state().base_state.nodes[node_id].coherence)
        _require(
            math.isclose(after, target, rel_tol=0.0, abs_tol=1e-12),
            "native readout materialization does not match active history",
        )
        record = {
            "carrier_id": self.carrier_id,
            "history_current_identity_digest": self.current_identity_digest(),
            "history_token_digest": digest_canonical(self._state["tokens"]),
            "readout_before": before,
            "readout_target": target,
            "readout_after": after,
            "packet_scheduled": packet_scheduled,
            "native_transfer": transfer,
            "direct_native_state_mutation": False,
            "success_or_response_computed": False,
            "later_response_scheduled": False,
        }
        self._state["last_materialized_readout"] = target
        self._state["last_materialization"] = deepcopy(record)
        self._state["materialization_call_count"] += 1
        return record

    def _validate_state(self, value: Mapping[str, Any]) -> dict[str, Any]:
        required = set(self._empty_state())
        _require(set(value) == required, "adapter state fields do not match schema")
        state = deepcopy(dict(value))
        state["tokens"] = [
            _canonical_token(token, expected_index=index)
            for index, token in enumerate(state["tokens"])
        ]
        state["scan_index"] = int(state["scan_index"])
        _require(state["scan_index"] >= 0, "scan_index must be nonnegative")
        state["consumed_surface_digests"] = [
            str(item) for item in state["consumed_surface_digests"]
        ]
        _require(
            len(set(state["consumed_surface_digests"]))
            == len(state["consumed_surface_digests"]),
            "consumed surface digests must be unique",
        )
        if state["last_arrival_event_time"] is not None:
            state["last_arrival_event_time"] = _finite(
                state["last_arrival_event_time"],
                name="last_arrival_event_time",
            )
        if state["last_materialized_readout"] is not None:
            state["last_materialized_readout"] = _finite(
                state["last_materialized_readout"],
                name="last_materialized_readout",
            )
        _require(isinstance(state["interventions"], list), "interventions must be a list")
        state["ingest_call_count"] = int(state["ingest_call_count"])
        state["materialization_call_count"] = int(state["materialization_call_count"])
        _require(state["ingest_call_count"] >= 0, "ingest_call_count must be nonnegative")
        _require(
            state["materialization_call_count"] >= 0,
            "materialization_call_count must be nonnegative",
        )
        return state

    def current_identity_artifact(self) -> dict[str, Any]:
        return {
            "artifact_kind": ADAPTER_ARTIFACT_KIND,
            "artifact_schema_version": ADAPTER_SCHEMA_VERSION,
            "identity_scope": "current_adapter_state",
            "configuration": deepcopy(self._config),
            "state": deepcopy(self._state),
        }

    def current_identity_digest(self) -> str:
        return digest_canonical(self.current_identity_artifact())

    def restoration_identity_artifact(self) -> dict[str, Any]:
        return {
            "artifact_kind": ADAPTER_ARTIFACT_KIND,
            "artifact_schema_version": ADAPTER_SCHEMA_VERSION,
            "identity_scope": "current_and_reset_baseline",
            "configuration": deepcopy(self._config),
            "current_state": deepcopy(self._state),
            "reset_baseline_state": deepcopy(self._reset_baseline),
        }

    def restoration_identity_digest(self) -> str:
        return digest_canonical(self.restoration_identity_artifact())

    def snapshot(self) -> dict[str, Any]:
        artifact = self.restoration_identity_artifact()
        return {
            **artifact,
            "restoration_identity_digest": digest_canonical(artifact),
        }

    def save(self, path: Path) -> None:
        path.write_bytes(
            json.dumps(self.snapshot(), indent=2, sort_keys=True).encode("utf-8")
            + b"\n"
        )

    @classmethod
    def load(cls, path: Path) -> "RCAEActiveHistoryAdapterV1":
        payload = json.loads(path.read_text(encoding="utf-8"))
        _require(payload["artifact_kind"] == ADAPTER_ARTIFACT_KIND, "wrong adapter kind")
        _require(
            payload["artifact_schema_version"] == ADAPTER_SCHEMA_VERSION,
            "wrong adapter schema",
        )
        without_digest = {k: deepcopy(v) for k, v in payload.items() if k != "restoration_identity_digest"}
        _require(
            digest_canonical(without_digest) == payload["restoration_identity_digest"],
            "adapter snapshot digest mismatch",
        )
        config = payload["configuration"]
        adapter = cls(
            carrier_id=config["carrier_id"],
            pool_target_node_id=config["pool_target_node_id"],
            registered_source_node_ids=config["registered_source_node_ids"],
            readout_node_id=config["readout_node_id"],
            positive_reservoir_node_id=config["positive_reservoir_node_id"],
            negative_sink_node_id=config["negative_sink_node_id"],
            positive_edge_id=config["positive_edge_id"],
            negative_edge_id=config["negative_edge_id"],
            recency_coefficient=config["recency_coefficient"],
        )
        _require(adapter._config == config, "adapter configuration did not round-trip")
        adapter._state = adapter._validate_state(payload["current_state"])
        adapter._reset_baseline = adapter._validate_state(payload["reset_baseline_state"])
        _require(
            adapter.restoration_identity_digest()
            == payload["restoration_identity_digest"],
            "restored adapter identity mismatch",
        )
        return adapter

    def reset(self) -> None:
        self._state = deepcopy(self._reset_baseline)


__all__ = [
    "ADAPTER_ARTIFACT_KIND",
    "ADAPTER_SCHEMA_VERSION",
    "RCAEActiveHistoryAdapterV1",
    "TOKEN_FIELDS",
    "digest_canonical",
]
