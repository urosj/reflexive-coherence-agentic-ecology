#!/usr/bin/env python3
"""Frozen P2-I2-I03C hybrid implementation-conformance harness.

The harness reuses only deterministic construction/scheduling helpers from the
already retained I03B harness and the exact active-history adapter. It owns the
I03C hybrid masks, assertions, branch logic, and composite identity. Its output
is quarantined implementation evidence and cannot enter I04-I08 or an L02
scientific conclusion.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any, Mapping, Sequence

import pygrc
from pygrc.models import (
    LGRC9V3,
    LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY,
    LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED,
    digest_lgrc9v3_restoration_identity_v2,
    lgrc9v3_restoration_identity_v2,
)

import p2_i2_i03b_conform as base
from p2_i2_i03b_history_adapter import (
    RCAEActiveHistoryAdapterV1,
    TOKEN_FIELDS,
    digest_canonical,
)


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = Path("/home/uros/Documents/RC-github/graph-reflexive-coherence")
GRAPH_SOURCE_ROOT = GRAPH_ROOT / "src"
SCRIPT_RELATIVE_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i03c_conform.py"
)
BASE_HARNESS_RELATIVE_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i03b_conform.py"
)
ADAPTER_RELATIVE_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i03b_history_adapter.py"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def _git(*args: str) -> str:
    result = subprocess.run(
        ("git", "-C", str(GRAPH_ROOT), *args),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _graph_guard() -> dict[str, Any]:
    return {
        "revision": _git("rev-parse", "HEAD"),
        "status_porcelain": _git("status", "--porcelain=v1", "--untracked-files=all"),
    }


def _close(observed: float, expected: float, freeze: Mapping[str, Any]) -> bool:
    comparator = freeze["assertions"]["float_comparator"]
    return math.isclose(
        float(observed),
        float(expected),
        rel_tol=float(comparator["relative_tolerance"]),
        abs_tol=float(comparator["absolute_tolerance"]),
    )


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def add(self, check_id: str, condition: bool, observed: Any, expected: Any) -> None:
        row = {
            "check_id": check_id,
            "passed": bool(condition),
            "observed": observed,
            "expected": expected,
        }
        self.rows.append(row)
        _require(condition, f"{check_id} failed: {observed!r} != {expected!r}")


def _validate_freeze(freeze: Mapping[str, Any], freeze_path: Path) -> dict[str, Any]:
    _require(
        freeze.get("artifact_id")
        == "P2-I2-I03C-HYBRID-RUNTIME-CONFORMANCE-INPUT-FREEZE",
        "wrong freeze artifact_id",
    )
    _require(freeze.get("iteration_id") == "P2-I2-I03C", "wrong iteration_id")
    _require(freeze.get("pool_dependence_mode") == "hybrid", "wrong mode")
    _require(freeze.get("realization_class") == "minimally_producer_assisted", "wrong realization")
    _require(freeze.get("runtime_authorized") is True, "runtime not authorized")
    policy = freeze["run_policy"]
    _require(policy["evidence_invocations"] == 1, "one evidence invocation required")
    _require(policy["reconstruction_invocations"] == 1, "one reconstruction required")
    _require(policy["retry_limit"] == 0, "retry limit must be zero")
    _require(policy["parameter_search_allowed"] is False, "search prohibited")
    _require(policy["rescue_variants_allowed"] is False, "rescue prohibited")
    _require(policy["branch_scenarios_per_invocation"] == 12, "wrong branch count")
    quarantine = freeze["quarantine"]
    _require(not any(
        quarantine[key]
        for key in (
            "may_support_or_falsify_AE01_H_L02",
            "may_enter_I04_or_I05_calibration",
            "may_supply_I06_or_I07_registered_values",
            "may_replace_I08_scientific_execution",
            "may_rank_dependence_modes",
            "observed_values_may_be_reused_scientifically",
        )
    ), "quarantine must be fail-closed")

    authority = freeze["authority"]
    for item in authority["bound_rcae_artifacts"]:
        path = ROOT / item["path"]
        _require(path.is_file(), f"missing bound artifact: {path}")
        _require(_sha256(path) == item["sha256"], f"artifact digest mismatch: {path}")
    for key, expected_path in (
        ("harness", SCRIPT_RELATIVE_PATH),
        ("base_construction_harness", BASE_HARNESS_RELATIVE_PATH),
        ("adapter", ADAPTER_RELATIVE_PATH),
    ):
        item = authority[key]
        path = ROOT / item["path"]
        _require(item["path"] == expected_path, f"wrong {key} path")
        _require(_sha256(path) == item["sha256"], f"{key} digest mismatch")
    _require(
        Path(authority["harness"]["path"]).name == Path(__file__).name,
        "wrong executing harness",
    )

    graph_before = _graph_guard()
    _require(graph_before["revision"] == authority["graph_revision"], "graph mismatch")
    _require(graph_before["status_porcelain"] == "", "graph checkout not clean")
    source_digests: dict[str, str] = {}
    for item in authority["bound_graph_sources"]:
        path = GRAPH_ROOT / item["path"]
        actual = _sha256(path)
        _require(actual == item["sha256"], f"graph source mismatch: {path}")
        source_digests[item["path"]] = actual

    expected_import = (GRAPH_SOURCE_ROOT / "pygrc" / "__init__.py").resolve()
    actual_import = Path(pygrc.__file__).resolve()
    _require(actual_import == expected_import, "PyGRC imported outside admitted checkout")
    environment = freeze["environment"]
    _require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "RCAE .venv inactive")
    versions = {
        name: importlib.metadata.version(name)
        for name in environment["direct_dependencies"]
    }
    _require(versions == environment["direct_dependencies"], "dependency mismatch")
    _require(platform.python_version() == environment["python_version"], "Python mismatch")
    _require(
        any(Path(item).resolve() == GRAPH_SOURCE_ROOT.resolve() for item in sys.path if item),
        "admitted graph source root missing from sys.path",
    )

    fixture = freeze["fixture"]
    prior_forbidden = freeze["mechanical_cross_mode_rejection"]
    serialized_fixture = json.dumps(fixture, sort_keys=True)
    for item in prior_forbidden["forbidden_exact_serialized_values"]:
        _require(str(item) not in serialized_fixture, f"prior fixture value reused: {item}")
    _require(
        fixture["response"]["front_mask"] == ["P", "M_H"],
        "hybrid front mask must contain P and M_H",
    )
    _require(fixture["response"]["expected_source_surface_digest"] is None, "digest must be null")
    _require(
        fixture["joint_intervention_relation"]["canonical_scheduled"] is True
        and fixture["joint_intervention_relation"]["state_only_scheduled"] is False
        and fixture["joint_intervention_relation"]["history_only_scheduled"] is False,
        "both component interventions must change the frozen joint branch",
    )

    return {
        "freeze_path": str(freeze_path.relative_to(ROOT)),
        "freeze_sha256": _sha256(freeze_path),
        "harness_path": SCRIPT_RELATIVE_PATH,
        "harness_sha256": _sha256(Path(__file__)),
        "base_construction_harness_path": BASE_HARNESS_RELATIVE_PATH,
        "base_construction_harness_sha256": _sha256(ROOT / BASE_HARNESS_RELATIVE_PATH),
        "adapter_path": ADAPTER_RELATIVE_PATH,
        "adapter_sha256": _sha256(ROOT / ADAPTER_RELATIVE_PATH),
        "graph_before": graph_before,
        "graph_source_digests": source_digests,
        "pygrc_import_file": str(actual_import),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "sys_executable": sys.executable,
        "sys_prefix": sys.prefix,
        "direct_dependency_versions": versions,
        "model_instantiated_during_freeze_validation": False,
    }


def _tokens(adapter: RCAEActiveHistoryAdapterV1) -> list[float]:
    return [float(token["contact_amount"]) for token in adapter.tokens]


def _token_schema_ok(adapter: RCAEActiveHistoryAdapterV1) -> bool:
    return all(set(token) == set(TOKEN_FIELDS) for token in adapter.tokens)


def _coherences(model: LGRC9V3, role_ids: Mapping[str, int]) -> dict[str, float]:
    nodes = model.get_state().base_state.nodes
    return {role: float(nodes[node_id].coherence) for role, node_id in sorted(role_ids.items())}


def _packet_records(model: LGRC9V3) -> list[dict[str, Any]]:
    return [row.to_record() for row in model.get_state().packet_ledger.packet_records]


def _surface_rows(model: LGRC9V3) -> list[dict[str, Any]]:
    return [row.to_artifact() for row in model.get_state().causal_pulse_substrate_surface_log]


def _source_lineages(model: LGRC9V3, source_ids: set[int]) -> list[list[Any]]:
    return [
        [row["source_node_id"], row["source_lineage_id"]]
        for row in _packet_records(model)
        if row["source_node_id"] in source_ids
    ]


def _neutral_contact(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    cursor: base.ScheduleCursor,
    freeze: Mapping[str, Any],
) -> str:
    spec = freeze["fixture"]["neutral_contact"]
    base._schedule_and_drain(
        model,
        role_ids,
        edge_ids,
        cursor,
        source=str(spec["source"]),
        target=str(spec["target"]),
        edge_role=str(spec["edge_role"]),
        amount=float(spec["amount"]),
        source_lineage_id=str(spec["source_lineage_id"]),
        target_lineage_id=str(spec["target_lineage_id"]),
    )
    rows = model.get_state().causal_pulse_substrate_surface_log
    _require(bool(rows), "neutral contact produced no surface row")
    return str(rows[-1].surface_digest)


def _prepare_feedback(
    model: LGRC9V3,
    role_ids: Mapping[str, int],
    edge_ids: Mapping[str, int],
    cursor: base.ScheduleCursor,
    freeze: Mapping[str, Any],
    *,
    front_roles: Sequence[str] = ("P", "M_H"),
    response_source: str = "A",
    response_target: str = "B",
    response_edge: str = "A_to_B",
    expected_trigger_digest: str,
) -> dict[str, Any]:
    config = freeze["fixture"]["response"]
    row = model.emit_feedback_eligibility_surface_row(
        front_node_ids=tuple(role_ids[role] for role in front_roles),
        rear_node_ids=(role_ids["B_ref"],),
        reference_delta=float(config["reference_delta"]),
        feedback_threshold=float(config["threshold"]),
    )
    response_slot = cursor.take()
    model.set_feedback_coupled_pulse_producer(
        source_node_id=role_ids[response_source],
        target_node_id=role_ids[response_target],
        edge_id=edge_ids[response_edge],
        threshold=float(config["threshold"]),
        packet_amount=float(config["packet_amount"]),
        expected_polarity=str(config["expected_polarity"]),
        expected_source_surface_digest=None,
        arrival_event_time_key=float(response_slot["arrival_event_time_key"]),
    )
    source_digest = str(row.surface_values_after["source_surface_digest"])
    _require(source_digest == expected_trigger_digest, "feedback did not use final neutral contact")
    return {
        "surface_digest": row.surface_digest,
        "source_surface_digest": source_digest,
        "neutral_trigger_digest": expected_trigger_digest,
        "front_node_ids": list(row.surface_update_policy["declared_front_node_ids"]),
        "rear_node_ids": list(row.surface_update_policy["declared_rear_node_ids"]),
        "front_mass": float(row.surface_values_after["front_mass"]),
        "rear_mass": float(row.surface_values_after["rear_mass"]),
        "boundary_polarity_score": float(row.surface_values_after["boundary_polarity_score"]),
        "expected_source_surface_digest": None,
        "response_slot": response_slot,
    }


def _composite_artifact(
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV1,
    freeze: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "artifact_kind": "p2_i2_i03c_hybrid_composite_restoration_identity",
        "artifact_schema_version": "p2_i2_i03c_hybrid_composite_restoration_identity_v1",
        "fixture_id": freeze["fixture"]["fixture_id"],
        "native_restoration_identity_v2": lgrc9v3_restoration_identity_v2(model),
        "adapter_restoration_identity": adapter.restoration_identity_artifact(),
        "joint_binding": freeze["fixture"]["composite_identity_binding"],
    }


def _composite_summary(
    model: LGRC9V3,
    adapter: RCAEActiveHistoryAdapterV1,
    freeze: Mapping[str, Any],
) -> dict[str, str]:
    artifact = _composite_artifact(model, adapter, freeze)
    return {
        "composite_digest": digest_canonical(artifact),
        "native_v2_digest": digest_lgrc9v3_restoration_identity_v2(model),
        "adapter_restoration_digest": adapter.restoration_identity_digest(),
        "binding_digest": digest_canonical(freeze["fixture"]["composite_identity_binding"]),
    }


def _execute_branch(
    branch_id: str,
    freeze: Mapping[str, Any],
    checks: Checks,
    *,
    contribution_key: str,
    state_debit: bool = False,
    history_clamp: bool = False,
    response_source: str = "A",
    response_target: str = "B",
    response_edge: str = "A_to_B",
) -> dict[str, Any]:
    model, role_ids, edge_ids = base._build_model(freeze)
    adapter = base._adapter(freeze, role_ids, edge_ids, profile="common")
    cursor = base.ScheduleCursor()
    specs = freeze["fixture"]["contribution_sequences"][contribution_key]
    base._schedule_contributions(model, role_ids, edge_ids, cursor, specs)
    appended = adapter.ingest_new_rows(model)
    first_materialization = base._materialize(adapter, model, cursor)
    intervention = None
    if history_clamp:
        intervention = adapter.replace_history(
            (),
            intervention_id="i03c-conformance-history-clamp-to-empty",
            reason="fresh fixture-only H_P intervention with native P and audit preserved",
        )
        materialization = base._materialize(adapter, model, cursor)
    else:
        materialization = first_materialization
    debit_record = None
    if state_debit:
        debit = freeze["fixture"]["state_only_debit"]
        slot = base._schedule_and_drain(
            model,
            role_ids,
            edge_ids,
            cursor,
            source=str(debit["source"]),
            target=str(debit["target"]),
            edge_role=str(debit["edge_role"]),
            amount=float(debit["amount"]),
            source_lineage_id=str(debit["source_lineage_id"]),
            target_lineage_id=str(debit["target_lineage_id"]),
        )
        debit_record = {**debit, **slot}
    trigger = _neutral_contact(model, role_ids, edge_ids, cursor, freeze)
    feedback = _prepare_feedback(
        model,
        role_ids,
        edge_ids,
        cursor,
        freeze,
        response_source=response_source,
        response_target=response_target,
        response_edge=response_edge,
        expected_trigger_digest=trigger,
    )
    response = base._execute_feedback(model, role_ids, response_target=response_target)
    expected = freeze["assertions"]["branches"][branch_id]
    coherences = _coherences(model, role_ids)
    amounts = _tokens(adapter)
    expected_mask = [role_ids["P"], role_ids["M_H"]]
    checks.add(f"{branch_id}.tokens", amounts == expected["token_amounts"], amounts, expected["token_amounts"])
    checks.add(f"{branch_id}.token_schema", _token_schema_ok(adapter), [sorted(token) for token in adapter.tokens], sorted(TOKEN_FIELDS))
    checks.add(f"{branch_id}.readout", _close(adapter.readout(), expected["readout"], freeze), adapter.readout(), expected["readout"])
    checks.add(f"{branch_id}.materialized", _close(materialization["readout_after"], expected["readout"], freeze), materialization["readout_after"], expected["readout"])
    checks.add(f"{branch_id}.adapter_boundary", materialization["success_or_response_computed"] is False and materialization["later_response_scheduled"] is False and materialization["direct_native_state_mutation"] is False, materialization, "no success/response/direct mutation")
    checks.add(f"{branch_id}.joint_mask", feedback["front_node_ids"] == expected_mask, feedback["front_node_ids"], expected_mask)
    checks.add(f"{branch_id}.mask_exact_once", feedback["front_node_ids"].count(role_ids["P"]) == 1 and feedback["front_node_ids"].count(role_ids["M_H"]) == 1, feedback["front_node_ids"], "P and M_H once each")
    checks.add(f"{branch_id}.rear_mask", feedback["rear_node_ids"] == [role_ids["B_ref"]], feedback["rear_node_ids"], [role_ids["B_ref"]])
    checks.add(f"{branch_id}.neutral_latest", feedback["source_surface_digest"] == feedback["neutral_trigger_digest"], feedback["source_surface_digest"], feedback["neutral_trigger_digest"])
    checks.add(f"{branch_id}.expected_digest_null", feedback["expected_source_surface_digest"] is None, feedback["expected_source_surface_digest"], None)
    checks.add(f"{branch_id}.front_mass", _close(feedback["front_mass"], expected["front_mass"], freeze), feedback["front_mass"], expected["front_mass"])
    checks.add(f"{branch_id}.score", _close(feedback["boundary_polarity_score"], expected["score"], freeze), feedback["boundary_polarity_score"], expected["score"])
    checks.add(f"{branch_id}.reason", response["reason_code"] == expected["reason_code"], response["reason_code"], expected["reason_code"])
    checks.add(f"{branch_id}.scheduled", response["scheduled"] is expected["scheduled"], response["scheduled"], expected["scheduled"])
    checks.add(f"{branch_id}.response_delta", _close(response["response_delta"], expected["response_delta"], freeze), response["response_delta"], expected["response_delta"])
    checks.add(f"{branch_id}.native_no_direct_write", response["producer_mutated_coherence"] is False and response["direct_claim_write"] is False, response, "native packet transition and no claim")
    for role, value in expected["coherences"].items():
        checks.add(f"{branch_id}.coherence.{role}", _close(coherences[role], value, freeze), coherences[role], value)
    checks.add(f"{branch_id}.queue_drained", not model.get_state().packet_ledger.event_queue_records, len(model.get_state().packet_ledger.event_queue_records), 0)
    if history_clamp:
        checks.add("history_only.P_preserved", _close(coherences["P"], expected["coherences"]["P"], freeze), coherences["P"], expected["coherences"]["P"])
        checks.add("history_only.intervention_explicit", intervention is not None and intervention["native_audit_rewritten"] is False and intervention["success_or_response_written"] is False, intervention, "external H-only intervention")
    if state_debit:
        checks.add("state_only.history_preserved", amounts == freeze["assertions"]["branches"]["combined_q1_q2"]["token_amounts"], amounts, freeze["assertions"]["branches"]["combined_q1_q2"]["token_amounts"])
        checks.add("state_only.M_H_preserved", _close(coherences["M_H"], freeze["assertions"]["branches"]["combined_q1_q2"]["readout"], freeze), coherences["M_H"], freeze["assertions"]["branches"]["combined_q1_q2"]["readout"])
    return {
        "branch_id": branch_id,
        "tokens": list(adapter.tokens),
        "appended_tokens": list(appended),
        "first_materialization": first_materialization,
        "final_materialization": materialization,
        "history_intervention": intervention,
        "state_debit": debit_record,
        "coherences": coherences,
        "feedback": feedback,
        "response": response,
        "packet_records": _packet_records(model),
        "surface_rows": _surface_rows(model),
        "source_lineages": _source_lineages(model, {role_ids["S1"], role_ids["S2"]}),
        "composite_identity": _composite_summary(model, adapter, freeze),
    }


def _run_private_partition(freeze: Mapping[str, Any], checks: Checks) -> dict[str, Any]:
    model, role_ids, edge_ids = base._build_model(freeze)
    h1 = base._adapter(freeze, role_ids, edge_ids, profile="private_one")
    h2 = base._adapter(freeze, role_ids, edge_ids, profile="private_two")
    cursor = base.ScheduleCursor()
    specs = freeze["fixture"]["contribution_sequences"]["private_combined"]
    base._schedule_contributions(model, role_ids, edge_ids, cursor, specs)
    a1 = h1.ingest_new_rows(model)
    a2 = h2.ingest_new_rows(model)
    m1 = base._materialize(h1, model, cursor)
    m2 = base._materialize(h2, model, cursor)
    trigger = _neutral_contact(model, role_ids, edge_ids, cursor, freeze)
    f1 = _prepare_feedback(model, role_ids, edge_ids, cursor, freeze, front_roles=("P1", "M_H1"), expected_trigger_digest=trigger)
    r1 = base._execute_feedback(model, role_ids)
    f2 = _prepare_feedback(model, role_ids, edge_ids, cursor, freeze, front_roles=("P2", "M_H2"), response_source="A_alt", response_target="B_alt", response_edge="A_alt_to_B_alt", expected_trigger_digest=trigger)
    r2 = base._execute_feedback(model, role_ids, response_target="B_alt")
    expected = freeze["assertions"]["branches"]["private_partition"]
    masks = [f1["front_node_ids"], f2["front_node_ids"]]
    scores = [f1["boundary_polarity_score"], f2["boundary_polarity_score"]]
    checks.add("private.tokens", [_tokens(h1), _tokens(h2)] == expected["token_amounts"], [_tokens(h1), _tokens(h2)], expected["token_amounts"])
    checks.add("private.separate_joint_masks", masks == [[role_ids["P1"], role_ids["M_H1"]], [role_ids["P2"], role_ids["M_H2"]]], masks, "two separate private pairs")
    checks.add("private.no_common_or_cross_pair", all(len(mask) == 2 for mask in masks) and not any(role_ids["P"] in mask or role_ids["M_H"] in mask for mask in masks) and not any(set(mask) == {role_ids["P1"], role_ids["M_H1"], role_ids["P2"], role_ids["M_H2"]} for mask in masks), masks, "no common/cross-pair read")
    checks.add("private.scores", all(_close(value, target, freeze) for value, target in zip(scores, expected["scores"], strict=True)), scores, expected["scores"])
    checks.add("private.responses", [r1["scheduled"], r2["scheduled"]] == [False, False], [r1["scheduled"], r2["scheduled"]], [False, False])
    checks.add("private.adapter_boundary", all(not item["success_or_response_computed"] and not item["later_response_scheduled"] for item in (m1, m2)), [m1, m2], "no adapter success")
    return {
        "branch_id": "private_partition",
        "private_histories": [
            {"carrier_id": h1.carrier_id, "tokens": list(h1.tokens), "appended_tokens": list(a1), "materialization": m1, "feedback": f1, "response": r1},
            {"carrier_id": h2.carrier_id, "tokens": list(h2.tokens), "appended_tokens": list(a2), "materialization": m2, "feedback": f2, "response": r2},
        ],
        "aggregation_performed": False,
        "coherences": _coherences(model, role_ids),
        "packet_records": _packet_records(model),
        "surface_rows": _surface_rows(model),
    }


def _continuation_signature(model: LGRC9V3, adapter: RCAEActiveHistoryAdapterV1, role_ids: Mapping[str, int], freeze: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "coherences": _coherences(model, role_ids),
        "tokens": list(adapter.tokens),
        "packet_records": _packet_records(model),
        "surface_rows": _surface_rows(model),
        "queue_length": len(model.get_state().packet_ledger.event_queue_records),
        "composite_identity": _composite_summary(model, adapter, freeze),
    }


def _prepare_restoration(model: LGRC9V3, adapter: RCAEActiveHistoryAdapterV1, role_ids: Mapping[str, int], edge_ids: Mapping[str, int], cursor: base.ScheduleCursor, freeze: Mapping[str, Any]) -> dict[str, Any]:
    specs = freeze["fixture"]["contribution_sequences"]["combined_q1_q2"]
    base._schedule_contributions(model, role_ids, edge_ids, cursor, specs)
    adapter.ingest_new_rows(model)
    materialization = base._materialize(adapter, model, cursor)
    trigger = _neutral_contact(model, role_ids, edge_ids, cursor, freeze)
    feedback = _prepare_feedback(model, role_ids, edge_ids, cursor, freeze, expected_trigger_digest=trigger)
    return {"materialization": materialization, "feedback": feedback}


def _run_restoration(freeze: Mapping[str, Any], checks: Checks) -> dict[str, Any]:
    model, role_ids, edge_ids = base._build_model(freeze)
    adapter = base._adapter(freeze, role_ids, edge_ids)
    initial = _composite_summary(model, adapter, freeze)
    cursor = base.ScheduleCursor()
    prepared = _prepare_restoration(model, adapter, role_ids, edge_ids, cursor, freeze)
    pre_save = _composite_summary(model, adapter, freeze)
    with tempfile.TemporaryDirectory(prefix="p2-i2-i03c-") as directory:
        root = Path(directory)
        native_path = root / "native.json"
        adapter_path = root / "adapter.json"
        manifest_path = root / "manifest.json"
        model.save(str(native_path))
        adapter.save(adapter_path)
        manifest = {
            "artifact_kind": "p2_i2_i03c_paired_save_manifest",
            "artifact_schema_version": "p2_i2_i03c_paired_save_manifest_v1",
            "native_snapshot_sha256": _sha256(native_path),
            "adapter_snapshot_sha256": _sha256(adapter_path),
            "composite_identity_before_save": pre_save,
            "fixture_manifest_hash_validated_before_continuation": True,
        }
        manifest_path.write_bytes(_canonical_json_bytes(manifest))
        loaded_model = LGRC9V3.load(str(native_path))
        loaded_adapter = RCAEActiveHistoryAdapterV1.load(adapter_path)
        retained_manifest = _load_json(manifest_path)
    loaded = _composite_summary(loaded_model, loaded_adapter, freeze)
    checks.add("restoration.paired_load_identity", loaded == pre_save, loaded, pre_save)
    checks.add("restoration.manifest_validated", retained_manifest["composite_identity_before_save"] == pre_save and retained_manifest["fixture_manifest_hash_validated_before_continuation"] is True, retained_manifest, "complete paired manifest")

    original_response = base._execute_feedback(model, role_ids)
    loaded_response = base._execute_feedback(loaded_model, role_ids)
    original_after = _continuation_signature(model, adapter, role_ids, freeze)
    loaded_after = _continuation_signature(loaded_model, loaded_adapter, role_ids, freeze)
    checks.add("restoration.equal_saved_response", loaded_response == original_response, loaded_response, original_response)
    checks.add("restoration.equal_saved_continuation", loaded_after == original_after, loaded_after, original_after)

    model.reset()
    adapter.reset()
    loaded_model.reset()
    loaded_adapter.reset()
    original_reset = _continuation_signature(model, adapter, role_ids, freeze)
    loaded_reset = _continuation_signature(loaded_model, loaded_adapter, role_ids, freeze)
    checks.add("restoration.paired_reset_equal", loaded_reset == original_reset, loaded_reset, original_reset)
    checks.add("restoration.reset_initial_identity", original_reset["composite_identity"] == initial, original_reset["composite_identity"], initial)
    checks.add("restoration.reset_history_empty", original_reset["tokens"] == [], original_reset["tokens"], [])

    cursor_a = base.ScheduleCursor()
    cursor_b = base.ScheduleCursor()
    specs = freeze["fixture"]["contribution_sequences"]["q1_only"]
    base._schedule_contributions(model, role_ids, edge_ids, cursor_a, specs)
    base._schedule_contributions(loaded_model, role_ids, edge_ids, cursor_b, specs)
    adapter.ingest_new_rows(model)
    loaded_adapter.ingest_new_rows(loaded_model)
    base._materialize(adapter, model, cursor_a)
    base._materialize(loaded_adapter, loaded_model, cursor_b)
    trigger_a = _neutral_contact(model, role_ids, edge_ids, cursor_a, freeze)
    trigger_b = _neutral_contact(loaded_model, role_ids, edge_ids, cursor_b, freeze)
    feedback_a = _prepare_feedback(model, role_ids, edge_ids, cursor_a, freeze, expected_trigger_digest=trigger_a)
    feedback_b = _prepare_feedback(loaded_model, role_ids, edge_ids, cursor_b, freeze, expected_trigger_digest=trigger_b)
    response_a = base._execute_feedback(model, role_ids)
    response_b = base._execute_feedback(loaded_model, role_ids)
    continuation_a = _continuation_signature(model, adapter, role_ids, freeze)
    continuation_b = _continuation_signature(loaded_model, loaded_adapter, role_ids, freeze)
    checks.add("restoration.equal_reset_feedback", feedback_b == feedback_a, feedback_b, feedback_a)
    checks.add("restoration.equal_reset_response", response_b == response_a, response_b, response_a)
    checks.add("restoration.equal_reset_continuation", continuation_b == continuation_a, continuation_b, continuation_a)
    return {
        "branch_id": "restoration_continuation",
        "initial_composite_identity": initial,
        "prepared_before_save": prepared,
        "pre_save_composite_identity": pre_save,
        "paired_save_manifest": retained_manifest,
        "loaded_composite_identity": loaded,
        "original_response": original_response,
        "loaded_response": loaded_response,
        "original_after_response": original_after,
        "loaded_after_response": loaded_after,
        "original_reset": original_reset,
        "loaded_reset": loaded_reset,
        "original_reset_continuation": continuation_a,
        "loaded_reset_continuation": continuation_b,
    }


def _signature(branch: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "token_amounts": [token["contact_amount"] for token in branch["tokens"]],
        "readout": branch["final_materialization"]["readout_after"],
        "P": branch["coherences"]["P"],
        "M_H": branch["coherences"]["M_H"],
        "front_mass": branch["feedback"]["front_mass"],
        "score": branch["feedback"]["boundary_polarity_score"],
        "reason_code": branch["response"]["reason_code"],
        "scheduled": branch["response"]["scheduled"],
        "response_delta": branch["response"]["response_delta"],
    }


def _run_conformance(freeze: Mapping[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    checks = Checks()
    branches: dict[str, Any] = {}
    for branch_id, contribution_key in (
        ("reference", "reference"),
        ("q1_only", "q1_only"),
        ("q2_only", "q2_only"),
        ("combined_q1_q2", "combined_q1_q2"),
        ("combined_q2_q1", "combined_q2_q1"),
        ("lineage_permuted", "lineage_permuted"),
        ("write_diversion", "write_diversion"),
    ):
        branches[branch_id] = _execute_branch(branch_id, freeze, checks, contribution_key=contribution_key)
    branches["history_only_clamp"] = _execute_branch("history_only_clamp", freeze, checks, contribution_key="combined_q1_q2", history_clamp=True)
    branches["state_only_debit"] = _execute_branch("state_only_debit", freeze, checks, contribution_key="combined_q1_q2", state_debit=True)
    branches["private_partition"] = _run_private_partition(freeze, checks)
    branches["alternate_responder"] = _execute_branch("alternate_responder", freeze, checks, contribution_key="combined_q1_q2", response_source="A_alt", response_target="B_alt", response_edge="A_alt_to_B_alt")
    branches["restoration_continuation"] = _run_restoration(freeze, checks)

    canonical = branches["combined_q1_q2"]
    reverse = branches["combined_q2_q1"]
    permuted = branches["lineage_permuted"]
    diversion = branches["write_diversion"]
    history_only = branches["history_only_clamp"]
    state_only = branches["state_only_debit"]
    alternate = branches["alternate_responder"]
    checks.add("cross.order_equal_marginals", sorted(_tokens_from_branch(canonical)) == sorted(_tokens_from_branch(reverse)), _tokens_from_branch(reverse), _tokens_from_branch(canonical))
    checks.add("cross.order_equal_P", _close(canonical["coherences"]["P"], reverse["coherences"]["P"], freeze), reverse["coherences"]["P"], canonical["coherences"]["P"])
    checks.add("cross.order_history_response_differs", canonical["tokens"] != reverse["tokens"] and canonical["response"]["scheduled"] is True and reverse["response"]["scheduled"] is False, {"canonical": _signature(canonical), "reverse": _signature(reverse)}, "same P/marginals, different H/readout/response")
    checks.add("cross.label_causal_invariance", _signature(permuted) == _signature(canonical), _signature(permuted), _signature(canonical))
    checks.add("cross.label_audit_changes", permuted["source_lineages"] != canonical["source_lineages"], permuted["source_lineages"], "different audit assignment")
    checks.add("cross.diversion_preserves_source_debits", [diversion["coherences"]["S1"], diversion["coherences"]["S2"]] == [canonical["coherences"]["S1"], canonical["coherences"]["S2"]], [diversion["coherences"]["S1"], diversion["coherences"]["S2"]], [canonical["coherences"]["S1"], canonical["coherences"]["S2"]])
    checks.add("cross.history_only_preserves_P", _close(history_only["coherences"]["P"], canonical["coherences"]["P"], freeze), history_only["coherences"]["P"], canonical["coherences"]["P"])
    checks.add("cross.history_only_changes_joint_response", history_only["tokens"] == [] and history_only["response"]["scheduled"] is False and canonical["response"]["scheduled"] is True, _signature(history_only), "H-only clamp removes joint response")
    checks.add("cross.state_only_preserves_H_M", state_only["tokens"] == canonical["tokens"] and _close(state_only["coherences"]["M_H"], canonical["coherences"]["M_H"], freeze), _signature(state_only), "same H/M_H")
    checks.add("cross.state_only_changes_joint_response", not _close(state_only["coherences"]["P"], canonical["coherences"]["P"], freeze) and state_only["response"]["scheduled"] is False and canonical["response"]["scheduled"] is True, _signature(state_only), "P-only debit removes joint response")
    checks.add("cross.both_components_required_same_joint_path", canonical["response"]["scheduled"] is True and state_only["response"]["scheduled"] is False and history_only["response"]["scheduled"] is False and canonical["feedback"]["front_node_ids"] == state_only["feedback"]["front_node_ids"] == history_only["feedback"]["front_node_ids"], [canonical["response"]["scheduled"], state_only["response"]["scheduled"], history_only["response"]["scheduled"]], [True, False, False])
    checks.add("cross.alternate_same_common_mask", alternate["feedback"]["front_node_ids"] == canonical["feedback"]["front_node_ids"] and alternate["feedback"]["rear_node_ids"] == canonical["feedback"]["rear_node_ids"], alternate["feedback"], canonical["feedback"])
    checks.add("cross.alternate_same_relation", _signature(alternate) == _signature(canonical), _signature(alternate), _signature(canonical))

    graph_after = _graph_guard()
    checks.add("guard.graph_revision_unchanged", graph_after["revision"] == receipt["graph_before"]["revision"], graph_after["revision"], receipt["graph_before"]["revision"])
    checks.add("guard.graph_clean_after", graph_after["status_porcelain"] == "", graph_after["status_porcelain"], "")
    for path, digest in receipt["graph_source_digests"].items():
        checks.add(f"guard.source_unchanged:{path}", _sha256(GRAPH_ROOT / path) == digest, _sha256(GRAPH_ROOT / path), digest)
    receipt["graph_after"] = graph_after

    return {
        "artifact_id": "P2-I2-I03C-HYBRID-RUNTIME-CONFORMANCE",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I03C",
        "pool_dependence_mode": "hybrid",
        "realization_class": "minimally_producer_assisted",
        "status": "runtime_conformant",
        "evidence_class": "quarantined_realization_implementation_conformance",
        "scientific_evidence_assigned": False,
        "runtime_receipt": receipt,
        "run_policy": freeze["run_policy"],
        "quarantine": freeze["quarantine"],
        "fixture_id": freeze["fixture"]["fixture_id"],
        "branches": branches,
        "assertions": checks.rows,
        "assertion_summary": {
            "total": len(checks.rows),
            "passed": sum(row["passed"] for row in checks.rows),
            "failed": sum(not row["passed"] for row in checks.rows),
        },
        "producer_boundary": {
            "rcae_component": "RCAEActiveHistoryAdapterV1",
            "rcae_computes_joint_score_or_success": False,
            "rcae_schedules_later_response": False,
            "native_feedback_reads_P_and_M_H": True,
            "native_feedback_producer_owns_later_transition": True,
        },
        "disposition": "hybrid_minimally_producer_assisted_runtime_conformant_pending_owner_review",
        "next_iteration_authorized": False,
    }


def _tokens_from_branch(branch: Mapping[str, Any]) -> list[float]:
    return [float(token["contact_amount"]) for token in branch["tokens"]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-freeze-only", action="store_true")
    args = parser.parse_args()
    freeze_path = args.freeze.resolve()
    freeze = _load_json(freeze_path)
    receipt = _validate_freeze(freeze, freeze_path)
    if args.validate_freeze_only:
        print(json.dumps({"status": "freeze_valid", "runtime_operation_performed": False, "runtime_receipt": receipt}, indent=2, sort_keys=True))
        return 0
    _require(args.output is not None, "--output required")
    record = _run_conformance(freeze, receipt)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(_canonical_json_bytes(record))
    print(json.dumps({"status": record["status"], "assertion_summary": record["assertion_summary"], "output": str(output), "sha256": _sha256(output)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
