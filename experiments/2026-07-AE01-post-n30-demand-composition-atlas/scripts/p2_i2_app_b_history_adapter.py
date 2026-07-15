"""Source-label-free G/E/P history projection for P2-I2 Appendix B.

The adapter extends the already accepted I06 active-history role only at its
physical-route admission boundary.  It does not write success, select a
branch, or schedule the response.  Coherence changes remain native packets.
"""

from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

from p2_i2_i06_history_adapter import RCAEActiveHistoryAdapterV2, digest_canonical


ADAPTER_ARTIFACT_KIND = "p2_i2_app_b_active_history_adapter"
ADAPTER_SCHEMA_VERSION = "p2_i2_app_b_active_history_adapter_v1"
ROUTE_LOCAL_CONTACT = "route_local_pulse_contact"
PACKET_ARRIVAL = "lgrc9v3_packet_arrival"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _canonical_registry(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for row in rows:
        _require(
            set(row) == {"operation", "source_node_id", "target_node_id", "edge_id", "amount"},
            "operation registry fields drifted",
        )
        operation = str(row["operation"])
        _require(operation in {"G", "E", "P"}, "unsupported physical operation")
        amount = float(row["amount"])
        _require(math.isfinite(amount) and amount > 0.0, "operation amount must be positive")
        result.append(
            {
                "operation": operation,
                "source_node_id": int(row["source_node_id"]),
                "target_node_id": int(row["target_node_id"]),
                "edge_id": int(row["edge_id"]),
                "amount": amount,
            }
        )
    _require([row["operation"] for row in result] == ["G", "E", "P"], "operation registry order drifted")
    return result


class RCAEAppendixBHistoryAdapter(RCAEActiveHistoryAdapterV2):
    """Accepted active-history realization with exact physical route admission."""

    def __init__(self, *, operation_registry: Sequence[Mapping[str, Any]], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._config["operation_registry"] = _canonical_registry(operation_registry)
        self._config["admission_rule"] = "exact_native_arrival_route_edge_and_amount"
        self._config["operation_identity_retained_in_receipt_only"] = True

    def ingest_new_rows(self, model: Any) -> tuple[dict[str, Any], ...]:
        """Append generic amount tokens from exactly registered physical arrivals."""

        rows = model.get_state().causal_pulse_substrate_surface_log
        start = int(self._state["scan_index"])
        _require(start <= len(rows), "native surface log moved behind adapter cursor")
        consumed = set(self._state["consumed_surface_digests"])
        registry = self._config["operation_registry"]
        appended: list[dict[str, Any]] = []
        for row in rows[start:]:
            if row.surface_kind != ROUTE_LOCAL_CONTACT or row.pulse_event_kind != PACKET_ARRIVAL:
                continue
            matches = [
                item
                for item in registry
                if int(row.source_node_id) == item["source_node_id"]
                and int(row.target_node_id) == item["target_node_id"]
                and str(row.pulse_channel_id) == f"edge:{item['edge_id']}"
                and math.isclose(float(row.contact_amount), item["amount"], rel_tol=0.0, abs_tol=0.0)
            ]
            if not matches:
                continue
            _require(len(matches) == 1, "physical arrival matched multiple operations")
            digest = str(row.surface_digest)
            _require(digest not in consumed, "native operation row consumed twice")
            event_time = float(row.event_time_key)
            _require(math.isfinite(event_time), "operation event time must be finite")
            previous = self._state["last_arrival_event_time"]
            interval = 0.0 if previous is None else event_time - float(previous)
            _require(interval >= 0.0, "admitted operation history is not time ordered")
            token = {
                "sequence_index": len(self._state["tokens"]),
                "contact_amount": float(row.contact_amount),
                "operation_kind": "native_arrival_contact_amount",
                "inter_arrival_interval": interval,
            }
            self._state["tokens"].append(token)
            self._state["consumed_surface_digests"].append(digest)
            self._state["last_arrival_event_time"] = event_time
            consumed.add(digest)
            appended.append(
                {
                    "token": deepcopy(token),
                    "physical_operation": matches[0]["operation"],
                    "physical_surface_digest": digest,
                    "source_label_retained": False,
                    "actor_identity_retained": False,
                }
            )
        self._state["scan_index"] = len(rows)
        self._state["ingest_call_count"] += 1
        return tuple(appended)

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
    def load(cls, path: Path) -> "RCAEAppendixBHistoryAdapter":
        payload = json.loads(path.read_text(encoding="utf-8"))
        _require(payload["artifact_kind"] == ADAPTER_ARTIFACT_KIND, "wrong adapter kind")
        _require(payload["artifact_schema_version"] == ADAPTER_SCHEMA_VERSION, "wrong adapter schema")
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
            operation_registry=config["operation_registry"],
        )
        _require(adapter._config == config, "adapter configuration did not round-trip")
        adapter._state = adapter._validate_state(payload["current_state"])
        adapter._reset_baseline = adapter._validate_state(payload["reset_baseline_state"])
        _require(
            adapter.restoration_identity_digest() == payload["restoration_identity_digest"],
            "restored adapter identity mismatch",
        )
        return adapter


__all__ = [
    "ADAPTER_ARTIFACT_KIND",
    "ADAPTER_SCHEMA_VERSION",
    "RCAEAppendixBHistoryAdapter",
]
