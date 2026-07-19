"""Narrow RCAE-owned B-R interfaces for P2-I3 bounded conformance.

This module deliberately has no PyGRC import.  It owns only the serialized
export-policy lifecycle, a field-blind structural encounter adapter, composite
manifest coordination, and evidence-neutral constructor identities.  Native
coherence, packet transport, admission, refusal, save/load, and reset remain
owned by the exact LGRC9V3 runtime bound by the conformance harness.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Mapping


class BRContractError(ValueError):
    """Raised when a B-R producer or composite contract fails closed."""


POLICY_SCHEMA = "p2_i3_br_export_policy_state_v1"
RECEIPT_SCHEMA = "p2_i3_br_lifecycle_receipt_v1"
COMPOSITE_SCHEMA = "p2_i3_br_composite_manifest_v1"
BRANCH_SCHEMA = "p2_i3_br_branch_state_v1"
RESET_SCHEMA = "p2_i3_br_reset_state_v1"
AUDIT_SCHEMA = "p2_i3_br_audit_state_v1"

Q13_CONTRAST_IDS = (
    "P2-I3-BR-Q13-FORMATION-QUANTITY-MATCH-001",
    "P2-I3-BR-Q13-EXPORT-MASS-MATCH-001",
    "P2-I3-BR-Q13-COMPLETE-STATE-HISTORY-MATCH-001",
)

CONTROL_INTERFACE_IDS = (
    "P2-I3-BR-CTRL-CURRENT-STATE-RELOCATION-001",
    "P2-I3-BR-CTRL-ROLE-RAW-ID-PERMUTATION-001",
    "P2-I3-BR-CTRL-SOURCE-CLAMP-001",
    "P2-I3-BR-CTRL-RESERVOIR-CLAMP-001",
    "P2-I3-BR-CTRL-PRODUCER-OMISSION-001",
    "P2-I3-BR-CTRL-FALSE-INSTALLATION-001",
    "P2-I3-BR-CTRL-MATCHED-MASS-001",
    "P2-I3-BR-CTRL-NO-FIELD-001",
    "P2-I3-BR-CTRL-WITHDRAWAL-SHUFFLE-001",
)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest_data(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")
    ).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise BRContractError(f"{context} must be an object")
    return deepcopy(dict(value))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise BRContractError(message)


def _write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_bytes(value))


def initial_policy_state(binding: Mapping[str, Any]) -> dict[str, Any]:
    """Construct one immutable-binding, serialized export-policy baseline."""

    required = {
        "policy_id",
        "route_id",
        "source_node_id",
        "destination_node_id",
        "edge_id",
        "export_floor",
        "export_cap",
        "absolute_tolerance",
        "schedule_by_sequence",
    }
    _require(set(binding) == required, "export-policy binding fields drifted")
    schedules = _mapping(binding["schedule_by_sequence"], "schedule_by_sequence")
    _require(schedules, "export-policy schedule must not be empty")
    for sequence, schedule in schedules.items():
        _require(str(int(sequence)) == str(sequence), "schedule key must be an integer string")
        row = _mapping(schedule, f"schedule[{sequence}]")
        _require(
            set(row)
            == {
                "departure_event_time_key",
                "arrival_event_time_key",
                "scheduler_event_index",
                "packet_index",
                "source_lineage_id",
                "target_lineage_id",
            },
            f"schedule[{sequence}] fields drifted",
        )
    floor = float(binding["export_floor"])
    cap = float(binding["export_cap"])
    tolerance = float(binding["absolute_tolerance"])
    _require(floor >= 0.0 and cap >= 0.0 and tolerance >= 0.0, "invalid policy values")
    return {
        "schema": POLICY_SCHEMA,
        "policy_id": str(binding["policy_id"]),
        "route_id": str(binding["route_id"]),
        "source_node_id": int(binding["source_node_id"]),
        "destination_node_id": int(binding["destination_node_id"]),
        "edge_id": int(binding["edge_id"]),
        "export_floor": floor,
        "export_cap": cap,
        "absolute_tolerance": tolerance,
        "schedule_by_sequence": schedules,
        "next_sequence_index": 0,
        "consumed_receipt_ids": [],
        "settled_export_receipt_ids": [],
        "pending_export": None,
    }


def _unchanged_transition(
    state: Mapping[str, Any], *, receipt_id: str | None, disposition: str, reason: str
) -> dict[str, Any]:
    before = deepcopy(dict(state))
    return {
        "disposition": disposition,
        "reason": reason,
        "receipt_id": receipt_id,
        "policy_state": before,
        "native_request": None,
        "policy_state_changed": False,
        "native_mutation_authored": False,
    }


def evaluate_export_policy(
    *,
    carrier_coherence: float,
    receipt: Mapping[str, Any],
    predecessor_composite_identity: str,
    policy_state: Mapping[str, Any],
) -> dict[str, Any]:
    """Evaluate one receipt using only one declared route-local carrier value.

    The function returns a native request description but never receives or
    mutates a model.  Invalid, pending-conflicting, and duplicate receipts are
    exact policy no-ops.
    """

    state = _mapping(policy_state, "policy_state")
    _require(state.get("schema") == POLICY_SCHEMA, "wrong policy-state schema")
    row = _mapping(receipt, "receipt")
    receipt_id = None if "receipt_id" not in row else str(row["receipt_id"])
    expected_fields = {
        "schema",
        "receipt_id",
        "route_id",
        "sequence_index",
        "qualifying_native_event_identity",
        "predecessor_composite_identity",
        "policy_id",
        "source_node_id",
        "destination_node_id",
        "edge_id",
        "prior_settlement_status",
        "eligible",
    }
    if set(row) != expected_fields or row.get("schema") != RECEIPT_SCHEMA:
        return _unchanged_transition(
            state,
            receipt_id=receipt_id,
            disposition="invalid",
            reason="receipt_shape_or_schema_mismatch",
        )
    if receipt_id in state["consumed_receipt_ids"]:
        return _unchanged_transition(
            state,
            receipt_id=receipt_id,
            disposition="duplicate_consumed",
            reason="receipt_already_consumed",
        )
    if state["pending_export"] is not None:
        return _unchanged_transition(
            state,
            receipt_id=receipt_id,
            disposition="invalid",
            reason="prior_export_not_settled",
        )
    sequence = int(row["sequence_index"])
    exact = (
        row["route_id"] == state["route_id"]
        and sequence == int(state["next_sequence_index"])
        and bool(row["qualifying_native_event_identity"])
        and row["predecessor_composite_identity"]
        == predecessor_composite_identity
        and row["policy_id"] == state["policy_id"]
        and int(row["source_node_id"]) == int(state["source_node_id"])
        and int(row["destination_node_id"])
        == int(state["destination_node_id"])
        and int(row["edge_id"]) == int(state["edge_id"])
        and row["prior_settlement_status"] == "settled"
        and row["eligible"] is True
    )
    if not exact:
        return _unchanged_transition(
            state,
            receipt_id=receipt_id,
            disposition="invalid",
            reason="receipt_binding_or_predecessor_mismatch",
        )

    carrier = float(carrier_coherence)
    _require(carrier >= 0.0, "carrier coherence must be nonnegative")
    amount = min(
        float(state["export_cap"]),
        max(0.0, carrier - float(state["export_floor"])),
    )
    updated = deepcopy(state)
    updated["consumed_receipt_ids"].append(receipt_id)
    updated["next_sequence_index"] = sequence + 1
    tolerance = float(state["absolute_tolerance"])
    if amount <= tolerance:
        return {
            "disposition": "eligible_zero",
            "reason": "carrier_at_or_below_export_floor",
            "receipt_id": receipt_id,
            "reserved_amount": 0.0,
            "policy_state": updated,
            "native_request": None,
            "policy_state_changed": True,
            "native_mutation_authored": False,
        }

    schedule = _mapping(
        state["schedule_by_sequence"].get(str(sequence)),
        f"missing frozen schedule for sequence {sequence}",
    )
    request = {
        "source_node_id": int(state["source_node_id"]),
        "target_node_id": int(state["destination_node_id"]),
        "edge_id": int(state["edge_id"]),
        "amount": amount,
        **schedule,
    }
    updated["pending_export"] = {
        "receipt_id": receipt_id,
        "sequence_index": sequence,
        "amount": amount,
        "native_request_digest": digest_data(request),
        "predecessor_composite_identity": predecessor_composite_identity,
    }
    return {
        "disposition": "eligible_positive",
        "reason": "bounded_export_reserved",
        "receipt_id": receipt_id,
        "reserved_amount": amount,
        "policy_state": updated,
        "native_request": request,
        "policy_state_changed": True,
        "native_mutation_authored": False,
    }


def settle_export_policy(
    policy_state: Mapping[str, Any],
    *,
    receipt_id: str,
    native_settlement_identity: str,
) -> dict[str, Any]:
    """Advance policy state only after the native export has settled."""

    state = _mapping(policy_state, "policy_state")
    pending = state.get("pending_export")
    _require(isinstance(pending, Mapping), "no export is pending settlement")
    _require(pending.get("receipt_id") == receipt_id, "pending receipt mismatch")
    _require(bool(native_settlement_identity), "native settlement identity missing")
    updated = deepcopy(state)
    updated["pending_export"] = None
    updated["settled_export_receipt_ids"].append(receipt_id)
    return updated


def build_blind_encounter_request(
    *,
    opportunity: Mapping[str, Any],
    parent_composite_identity: str,
) -> dict[str, Any]:
    """Return one structural native request without receiving field state."""

    row = _mapping(opportunity, "opportunity")
    required = {
        "opportunity_id",
        "parent_composite_identity",
        "source_node_id",
        "target_node_id",
        "edge_id",
        "amount",
        "departure_event_time_key",
        "arrival_event_time_key",
        "scheduler_event_index",
        "packet_index",
        "source_lineage_id",
        "target_lineage_id",
    }
    _require(set(row) == required, "encounter opportunity fields drifted")
    _require(
        row["parent_composite_identity"] == parent_composite_identity,
        "encounter parent identity mismatch",
    )
    _require(float(row["amount"]) > 0.0, "encounter amount must be positive")
    return {
        key: deepcopy(row[key])
        for key in (
            "source_node_id",
            "target_node_id",
            "edge_id",
            "amount",
            "departure_event_time_key",
            "arrival_event_time_key",
            "scheduler_event_index",
            "packet_index",
            "source_lineage_id",
            "target_lineage_id",
        )
    }


def make_branch_state(
    *, branch_id: str, parent_composite_identity: str, opportunity_id: str
) -> dict[str, Any]:
    return {
        "schema": BRANCH_SCHEMA,
        "branch_id": branch_id,
        "parent_composite_identity": parent_composite_identity,
        "opportunity_id": opportunity_id,
    }


def make_reset_state(*, reset_id: str, baseline_composite_identity: str) -> dict[str, Any]:
    return {
        "schema": RESET_SCHEMA,
        "reset_id": reset_id,
        "baseline_composite_identity": baseline_composite_identity,
    }


def make_audit_state(*, lineage: list[str]) -> dict[str, Any]:
    return {"schema": AUDIT_SCHEMA, "lineage": list(lineage)}


def reset_rcae_components(
    *,
    baseline_policy_state: Mapping[str, Any],
    baseline_branch_state: Mapping[str, Any],
    baseline_reset_state: Mapping[str, Any],
    baseline_audit_state: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """Restore the declared RCAE half of a paired native-plus-RCAE reset."""

    policy = _mapping(baseline_policy_state, "baseline_policy_state")
    branch = _mapping(baseline_branch_state, "baseline_branch_state")
    reset = _mapping(baseline_reset_state, "baseline_reset_state")
    audit = _mapping(baseline_audit_state, "baseline_audit_state")
    _require(policy.get("schema") == POLICY_SCHEMA, "wrong baseline policy schema")
    _require(branch.get("schema") == BRANCH_SCHEMA, "wrong baseline branch schema")
    _require(reset.get("schema") == RESET_SCHEMA, "wrong baseline reset schema")
    _require(audit.get("schema") == AUDIT_SCHEMA, "wrong baseline audit schema")
    return {
        "policy": policy,
        "branch": branch,
        "reset": reset,
        "audit": audit,
    }


def causal_continuation_projection(
    *,
    native_restoration_digest: str,
    policy_state: Mapping[str, Any],
    branch_state: Mapping[str, Any],
    reset_state: Mapping[str, Any],
) -> dict[str, Any]:
    """Project declared causal state while excluding separate audit lineage."""

    return {
        "identity_id": "P2-I3-BR-Q15-CAUSAL-CONTINUATION-PROJECTION-001",
        "native_restoration_digest": native_restoration_digest,
        "policy_state": deepcopy(dict(policy_state)),
        "branch_state": deepcopy(dict(branch_state)),
        "reset_state": deepcopy(dict(reset_state)),
    }


def composite_identity(
    *,
    native_restoration_digest: str,
    policy_state: Mapping[str, Any],
    branch_state: Mapping[str, Any],
    reset_state: Mapping[str, Any],
    audit_state: Mapping[str, Any],
) -> str:
    return digest_data(
        {
            "identity_id": "P2-I3-BR-Q15-EXACT-COMPOSITE-RESTORATION-001",
            "native_restoration_digest": native_restoration_digest,
            "policy_state": dict(policy_state),
            "branch_state": dict(branch_state),
            "reset_state": dict(reset_state),
            "audit_state": dict(audit_state),
        }
    )


def save_composite(
    directory: Path,
    *,
    model: Any,
    native_digest: Callable[[Any], str],
    policy_state: Mapping[str, Any],
    branch_state: Mapping[str, Any],
    reset_state: Mapping[str, Any],
    audit_state: Mapping[str, Any],
) -> dict[str, Any]:
    """Write one complete temporary composite and its fail-closed manifest."""

    _require(not directory.exists(), "composite directory already exists")
    directory.mkdir(parents=True)
    values = {
        "policy": _mapping(policy_state, "policy_state"),
        "branch": _mapping(branch_state, "branch_state"),
        "reset": _mapping(reset_state, "reset_state"),
        "audit": _mapping(audit_state, "audit_state"),
    }
    _require(values["policy"].get("schema") == POLICY_SCHEMA, "wrong policy schema")
    _require(values["branch"].get("schema") == BRANCH_SCHEMA, "wrong branch schema")
    _require(values["reset"].get("schema") == RESET_SCHEMA, "wrong reset schema")
    _require(values["audit"].get("schema") == AUDIT_SCHEMA, "wrong audit schema")

    native_path = directory / "native.json"
    model.save(str(native_path))
    for name, value in values.items():
        _write_json(directory / f"{name}.json", value)
    native_restoration_digest = native_digest(model)
    component_paths = {
        "native": "native.json",
        "policy": "policy.json",
        "branch": "branch.json",
        "reset": "reset.json",
        "audit": "audit.json",
    }
    component_sha256 = {
        name: sha256_file(directory / relative)
        for name, relative in component_paths.items()
    }
    exact_identity = composite_identity(
        native_restoration_digest=native_restoration_digest,
        policy_state=values["policy"],
        branch_state=values["branch"],
        reset_state=values["reset"],
        audit_state=values["audit"],
    )
    manifest = {
        "schema": COMPOSITE_SCHEMA,
        "identity_id": "P2-I3-BR-Q15-EXACT-COMPOSITE-RESTORATION-001",
        "exact_composite_identity": exact_identity,
        "native_restoration_digest": native_restoration_digest,
        "component_paths": component_paths,
        "component_sha256": component_sha256,
        "bindings": {
            "route_id": values["policy"]["route_id"],
            "policy_id": values["policy"]["policy_id"],
            "opportunity_id": values["branch"]["opportunity_id"],
            "branch_id": values["branch"]["branch_id"],
            "reset_id": values["reset"]["reset_id"],
        },
    }
    _write_json(directory / "manifest.json", manifest)
    return manifest


def load_composite(
    directory: Path,
    *,
    native_loader: Callable[[str], Any],
    native_digest: Callable[[Any], str],
    expected_bindings: Mapping[str, str],
) -> dict[str, Any]:
    """Validate every component and binding before invoking the native loader."""

    manifest_path = directory / "manifest.json"
    _require(manifest_path.is_file() and not manifest_path.is_symlink(), "manifest missing")
    manifest = _mapping(json.loads(manifest_path.read_text(encoding="utf-8")), "manifest")
    _require(manifest.get("schema") == COMPOSITE_SCHEMA, "wrong composite schema")
    expected_components = {
        "native": "native.json",
        "policy": "policy.json",
        "branch": "branch.json",
        "reset": "reset.json",
        "audit": "audit.json",
    }
    _require(manifest.get("component_paths") == expected_components, "component set drifted")
    values: dict[str, dict[str, Any]] = {}
    for name, relative in expected_components.items():
        path = directory / relative
        _require(path.is_file() and not path.is_symlink(), f"component missing: {name}")
        _require(
            sha256_file(path) == manifest["component_sha256"].get(name),
            f"component digest mismatch: {name}",
        )
        if name != "native":
            values[name] = _mapping(
                json.loads(path.read_text(encoding="utf-8")), name
            )
    _require(
        manifest.get("bindings") == dict(expected_bindings),
        "composite binding mismatch",
    )
    recalculated = composite_identity(
        native_restoration_digest=str(manifest["native_restoration_digest"]),
        policy_state=values["policy"],
        branch_state=values["branch"],
        reset_state=values["reset"],
        audit_state=values["audit"],
    )
    _require(
        recalculated == manifest.get("exact_composite_identity"),
        "exact composite identity mismatch",
    )

    model = native_loader(str(directory / "native.json"))
    _require(
        native_digest(model) == manifest["native_restoration_digest"],
        "loaded native restoration identity mismatch",
    )
    return {"model": model, "manifest": manifest, **values}


def build_q13_constructor_records() -> list[dict[str, Any]]:
    """Expose three non-substitutable constructor identities without outcomes."""

    return [
        {
            "contrast_id": Q13_CONTRAST_IDS[0],
            "constructors": ["repeated_formation", "one_equal_total_pulse"],
            "meaning": "formation_quantity_only",
        },
        {
            "contrast_id": Q13_CONTRAST_IDS[1],
            "constructors": ["candidate_export", "equal_mass_zero_contrast_debit"],
            "meaning": "export_mass_separate_from_route_contrast",
        },
        {
            "contrast_id": Q13_CONTRAST_IDS[2],
            "constructors": ["history_arm_a", "history_arm_b"],
            "meaning": "equal_causal_projection_distinct_audit_history",
        },
    ]


def build_control_interface_records(*, carrier_value: float) -> list[dict[str, Any]]:
    """Expose distinct future control requests without assigning dispositions."""

    rows = [
        {
            "control_id": CONTROL_INTERFACE_IDS[0],
            "operation": "relocate_registered_carrier_state",
            "payload": {
                "source_binding": 1,
                "target_binding": 6,
                "carrier_coherence": float(carrier_value),
            },
            "excluded_payload_fields": ["route_label", "participant", "preference"],
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[1],
            "operation": "role_preserving_raw_id_permutation",
            "payload": {"node_permutation": {"0": 5, "1": 6, "5": 0, "6": 1}},
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[2],
            "operation": "source_coherence_clamp_request",
            "payload": {"binding": 1},
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[3],
            "operation": "reservoir_coherence_clamp_request",
            "payload": {"binding": 2},
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[4],
            "operation": "omit_export_policy",
            "payload": {"expected_native_request_count": 0},
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[5],
            "operation": "false_installation_request",
            "payload": {
                "depositor_history_required": False,
                "outcome_writing_allowed": False,
                "exact_native_operation_deferred_to": "P2-I3-I06",
            },
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[6],
            "operation": "matched_mass_conservative_request",
            "payload": {"equal_source_and_carrier_debit": True},
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[7],
            "operation": "no_field_request",
            "payload": {"formation_request_count": 0, "export_policy_invoked": False},
        },
        {
            "control_id": CONTROL_INTERFACE_IDS[8],
            "operation": "withdrawal_or_shuffle_request",
            "payload": {"subtypes": ["withdrawal", "shuffle"]},
        },
    ]
    _require(
        tuple(row["control_id"] for row in rows) == CONTROL_INTERFACE_IDS,
        "control interface order drifted",
    )
    return rows


__all__ = [
    "AUDIT_SCHEMA",
    "BRANCH_SCHEMA",
    "BRContractError",
    "COMPOSITE_SCHEMA",
    "CONTROL_INTERFACE_IDS",
    "POLICY_SCHEMA",
    "Q13_CONTRAST_IDS",
    "RECEIPT_SCHEMA",
    "RESET_SCHEMA",
    "build_blind_encounter_request",
    "build_control_interface_records",
    "build_q13_constructor_records",
    "canonical_bytes",
    "causal_continuation_projection",
    "composite_identity",
    "digest_data",
    "evaluate_export_policy",
    "initial_policy_state",
    "load_composite",
    "make_audit_state",
    "make_branch_state",
    "make_reset_state",
    "reset_rcae_components",
    "save_composite",
    "settle_export_policy",
    "sha256_file",
]
