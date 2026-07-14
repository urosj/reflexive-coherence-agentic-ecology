"""Registration-ready active-history adapter for P2-I2-I06.

This revision preserves the accepted I03B/I03C active-history semantics while
making native readout-materialization tolerance an explicit registered identity
field. It never reads response state or schedules the later response.
"""

from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
from typing import Any, Mapping

from p2_i2_i03b_history_adapter import (
    RCAEActiveHistoryAdapterV1,
    TOKEN_FIELDS,
    digest_canonical,
)


ADAPTER_ARTIFACT_KIND = "p2_i2_i06_active_history_adapter"
ADAPTER_SCHEMA_VERSION = "p2_i2_i06_active_history_adapter_v2"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


class RCAEActiveHistoryAdapterV2(RCAEActiveHistoryAdapterV1):
    """I03-compatible history carrier with registered numeric tolerance."""

    def __init__(self, *, materialization_tolerance: float, **kwargs: Any) -> None:
        tolerance = float(materialization_tolerance)
        if not math.isfinite(tolerance) or tolerance < 0.0:
            raise ValueError("materialization_tolerance must be finite and nonnegative")
        super().__init__(**kwargs)
        self._config["materialization_tolerance"] = tolerance

    @property
    def materialization_tolerance(self) -> float:
        return float(self._config["materialization_tolerance"])

    def materialize_readout(
        self,
        model: Any,
        *,
        departure_event_time_key: float,
        arrival_event_time_key: float,
        scheduler_event_index: int,
        packet_index: int,
    ) -> dict[str, Any]:
        """Materialize R_H through native packets under registered tolerance."""

        target = self.readout()
        node_id = int(self._config["readout_node_id"])
        before = float(model.get_state().base_state.nodes[node_id].coherence)
        delta = target - before
        tolerance = self.materialization_tolerance
        packet_scheduled = not math.isclose(
            delta,
            0.0,
            rel_tol=0.0,
            abs_tol=tolerance,
        )
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
            math.isclose(after, target, rel_tol=0.0, abs_tol=tolerance),
            "native readout materialization does not match active history",
        )
        record = {
            "carrier_id": self.carrier_id,
            "history_current_identity_digest": self.current_identity_digest(),
            "history_token_digest": digest_canonical(self._state["tokens"]),
            "readout_before": before,
            "readout_target": target,
            "readout_after": after,
            "materialization_tolerance": tolerance,
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

    def current_identity_artifact(self) -> dict[str, Any]:
        artifact = super().current_identity_artifact()
        artifact["artifact_kind"] = ADAPTER_ARTIFACT_KIND
        artifact["artifact_schema_version"] = ADAPTER_SCHEMA_VERSION
        return artifact

    def restoration_identity_artifact(self) -> dict[str, Any]:
        artifact = super().restoration_identity_artifact()
        artifact["artifact_kind"] = ADAPTER_ARTIFACT_KIND
        artifact["artifact_schema_version"] = ADAPTER_SCHEMA_VERSION
        return artifact

    @classmethod
    def load(cls, path: Path) -> "RCAEActiveHistoryAdapterV2":
        payload = json.loads(path.read_text(encoding="utf-8"))
        _require(payload["artifact_kind"] == ADAPTER_ARTIFACT_KIND, "wrong adapter kind")
        _require(
            payload["artifact_schema_version"] == ADAPTER_SCHEMA_VERSION,
            "wrong adapter schema",
        )
        without_digest = {
            key: deepcopy(value)
            for key, value in payload.items()
            if key != "restoration_identity_digest"
        }
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
            materialization_tolerance=config["materialization_tolerance"],
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


__all__ = [
    "ADAPTER_ARTIFACT_KIND",
    "ADAPTER_SCHEMA_VERSION",
    "RCAEActiveHistoryAdapterV2",
    "TOKEN_FIELDS",
    "digest_canonical",
]
