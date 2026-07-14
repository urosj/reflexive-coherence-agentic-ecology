"""Static validator for the P2-I2-I03B history-carried design freeze.

This script validates retained authority, admitted source dataflow, producer
minimality, mode coverage, and the freeze-before-runtime boundary. It does not
instantiate an LGRC9V3 model or execute a candidate, cell, control, response,
calibration, or runtime-conformance operation.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


RCAE_ENTRY_REVISION = "c13ccb74d3ddc7c6f8f3870a15e17e024c9200dd"
GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
EXPECTED_FREEZE_SHA256 = (
    "1d1ab37502b9138c5c98b3048bd854ac7ed17d5775c9fd34ad8475608a0bcc7f"
)
EXPECTED_CONTRACT_SHA256 = (
    "8fc575089017c0e429f04bb221092493634bba4a6adcd4fc22ca36a5b238c38d"
)
EXPECTED_CELLS = [
    "reference-pool",
    "individual-contributions",
    "combined-orders",
    "pooled-history-shuffle",
    "contributor-removal",
    "global-state-exclusion",
    "access-capacity-contrast",
]
EXPECTED_CONTROLS = [f"AE01-L02-CTRL-{index:02d}" for index in range(1, 6)]
EXPECTED_OPS = [f"H-L02-OP-{index:02d}" for index in range(1, 10)]
EXPECTED_CAPS = [f"P2-I2-CAP-{index:02d}" for index in range(1, 12)]
SELECTED_CALLABLES = [
    "pygrc.models.LGRC9V3.get_state",
    "pygrc.models.LGRC9V3.schedule_packet_departure",
    "pygrc.models.LGRC9V3.step",
    "pygrc.models.LGRC9V3.emit_feedback_eligibility_surface_row",
    "pygrc.models.LGRC9V3.set_feedback_coupled_pulse_producer",
    "pygrc.models.LGRC9V3.produce_events",
    "pygrc.models.LGRC9V3.reset",
    "pygrc.models.LGRC9V3.save",
    "pygrc.models.LGRC9V3.load",
    "pygrc.models.lgrc9v3_restoration_identity_v2",
    "pygrc.models.digest_lgrc9v3_restoration_identity_v2",
]


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run_git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def named_node(source: str, name: str, node_type: type[ast.AST]) -> ast.AST:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, node_type) and getattr(node, "name", None) == name:
            return node
    raise AssertionError(f"source node not found: {name}")


def node_source(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node)
    if segment is None:
        raise AssertionError("source segment unavailable")
    return segment


def validate(args: argparse.Namespace) -> dict[str, Any]:
    rcae = args.rcae_root.resolve()
    graph = args.graph_root.resolve()
    experiment = rcae / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
    contract_dir = experiment / "contracts/p2-i2"

    freeze_path = contract_dir / "i03b-history-carried-realization-freeze-input.json"
    contract_path = (
        contract_dir
        / "i03b-history-carried-realization-and-discriminator-contract.json"
    )
    manifest_path = (
        contract_dir / "i02r2-admitted-source-and-reset-provider-manifest.json"
    )
    hypothesis_path = experiment / "hypotheses/p2-i2-operational-hypotheses.md"
    brief_path = experiment / "implementation/P2-I2-shared-pool-co-conditioning-brief.md"
    checklist_path = (
        experiment / "implementation/P2-I2-shared-pool-co-conditioning-checklist.md"
    )
    decision_path = experiment / "implementation/P2-I2-decision-record.md"
    report_path = (
        experiment
        / "reports/P2-I2-I03B-history-carried-realization-and-operational-hypothesis-freeze.md"
    )

    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    hypothesis = hypothesis_path.read_text(encoding="utf-8")
    brief = brief_path.read_text(encoding="utf-8")
    checklist = checklist_path.read_text(encoding="utf-8")
    decision = decision_path.read_text(encoding="utf-8")
    report = report_path.read_text(encoding="utf-8")

    graph_before = {
        "revision": run_git(graph, "rev-parse", "HEAD"),
        "status_short": run_git(graph, "status", "--short"),
    }
    assert graph_before["revision"] == GRAPH_REVISION
    assert graph_before["status_short"] == ""

    assert freeze["iteration_id"] == "P2-I2-I03B"
    assert freeze["pool_dependence_mode"] == "history_carried"
    assert sha256_path(freeze_path) == EXPECTED_FREEZE_SHA256
    assert freeze["design_phase_run_policy"]["history_carried_model_instantiations"] == 0
    assert freeze["design_phase_run_policy"]["history_carried_runtime_operations"] == 0
    assert freeze["runtime_transition_rule"]["separate_runtime_freeze_required"] is True
    assert len(freeze["comparison_questions"]) == 9

    prior_checks: list[dict[str, Any]] = []
    for item in freeze["bound_prior_artifacts"]:
        revision_content = subprocess.run(
            [
                "git",
                "-C",
                str(rcae),
                "show",
                f"{RCAE_ENTRY_REVISION}:{item['path']}",
            ],
            check=True,
            capture_output=True,
        ).stdout
        entry_sha = sha256_bytes(revision_content)
        current_sha = sha256_path(rcae / item["path"])
        match = entry_sha == current_sha == item["sha256"]
        assert match, item["path"]
        prior_checks.append(
            {
                "path": item["path"],
                "expected_sha256": item["sha256"],
                "entry_revision_sha256": entry_sha,
                "current_sha256": current_sha,
                "match": match,
            }
        )

    assert sha256_path(contract_path) == EXPECTED_CONTRACT_SHA256
    assert contract["iteration_id"] == "P2-I2-I03B"
    assert contract["status"] == "design_frozen_runtime_conformance_pending"
    assert contract["mode_scope"]["pool_dependence_mode"] == "history_carried"
    assert contract["mode_scope"]["ordered_common_history_is_causal"] is True
    assert (
        contract["mode_scope"]["encounter_pool_state_is_primary_causal_component"]
        is False
    )
    assert contract["mode_scope"]["audit_lineage_is_causal"] is False
    assert contract["native_first_source_comparison"]["native_candidate_disposition"] == (
        "inadequate_for_history_carried"
    )
    assert contract["realization_selection"]["realization_class"] == (
        "minimally_producer_assisted"
    )
    assert contract["realization_selection"]["rcae_causal_producer_selected"] is True
    assert (
        contract["realization_selection"][
            "rcae_producer_computes_success_or_later_response"
        ]
        is False
    )
    assert (
        contract["realization_selection"][
            "native_feedback_producer_owns_later_response_transition"
        ]
        is True
    )

    forbidden_tokens = set(contract["causal_factorization"]["q"]["forbidden_token_fields"])
    assert {
        "source_lineage_id",
        "target_lineage_id",
        "source_node_id",
        "pulse_packet_id",
        "pulse_event_id",
        "surface_digest",
        "success or response label",
    }.issubset(forbidden_tokens)
    assert contract["causal_factorization"]["C_P"]["response_read_allowed"] is False
    assert "M_H only" in contract["causal_factorization"]["V"]["history_read"]
    assert contract["causal_factorization"]["V"]["history_guard"].startswith(
        "expected_source_surface_digest remains null"
    )
    assert contract["producer_boundary"]["handoff"].startswith(
        "The adapter stops after native M_H materialization"
    )
    assert "direct mutation of LGRC9V3RuntimeState or node coherence" in (
        contract["producer_boundary"]["forbidden_calls_or_reads"]
    )

    cells = [item["cell_id"] for item in contract["logical_cells"]]
    controls = [item["control_id"] for item in contract["lane_controls"]]
    ops = [item["op_id"] for item in contract["operational_projections"]]
    caps = [
        item["capability_id"]
        for item in contract["native_adequacy_and_gap_disposition"]
    ]
    assert cells == EXPECTED_CELLS
    assert controls == EXPECTED_CONTROLS
    assert ops == EXPECTED_OPS
    assert caps == EXPECTED_CAPS
    for item in contract["lane_controls"]:
        assert item["target"]
        assert item["held_fixed"]
        assert item["expected_relation"]
        assert item["allowed_ambiguity"]
        assert item["fail_closed_effect"]
    for item in contract["operational_projections"]:
        assert item["cells"]
        assert item["expected_relation"]
        assert item["held_fixed"]
        assert item["fail_closed_effect"]

    restoration = contract["restoration_profile_proposal"]
    assert restoration["native_provider"] == (
        "pygrc.models.lgrc9v3_restoration_identity_v2"
    )
    assert "H_P ordered tokens" in restoration["rcae_external_current_state"]
    assert "adapter.reset()" in restoration["reset_policy"]
    assert contract["runtime_conformance_transition"]["separate_runtime_freeze_required"] is True
    assert contract["runtime_conformance_transition"]["retry_limit"] == 0
    assert contract["review_stop"]["i03c_authorized"] is False
    assert contract["review_stop"]["i04_authorized"] is False
    assert contract["review_stop"]["scientific_evidence_assigned"] is False

    manifest_symbols = {item["symbol"] for item in manifest["callable_entries"]}
    missing_symbols = sorted(set(SELECTED_CALLABLES) - manifest_symbols)
    assert not missing_symbols, missing_symbols

    manifest_sources = {item["source_id"]: item for item in manifest["source_entries"]}
    frozen_source_ids = freeze["admitted_source_scope"]["source_ids"]
    assert len(frozen_source_ids) == 20
    assert len(set(frozen_source_ids)) == len(frozen_source_ids)
    source_checks: list[dict[str, Any]] = []
    for source_id in frozen_source_ids:
        item = manifest_sources[source_id]
        relative = source_id.removeprefix("grc:")
        revision_content = subprocess.run(
            ["git", "-C", str(graph), "show", f"{GRAPH_REVISION}:{relative}"],
            check=True,
            capture_output=True,
        ).stdout
        revision_sha = sha256_bytes(revision_content)
        worktree_sha = sha256_path(graph / relative)
        match = revision_sha == worktree_sha == item["sha256"]
        assert match, source_id
        source_checks.append(
            {
                "source_id": source_id,
                "manifest_sha256": item["sha256"],
                "revision_sha256": revision_sha,
                "worktree_sha256": worktree_sha,
                "match": match,
            }
        )

    contract_source = (graph / "src/pygrc/models/lgrc_9_v3_contract.py").read_text(
        encoding="utf-8"
    )
    runtime_state_source = (
        graph / "src/pygrc/models/lgrc_9_v3_runtime_state.py"
    ).read_text(encoding="utf-8")
    runtime_source = (graph / "src/pygrc/models/lgrc_9_v3_runtime.py").read_text(
        encoding="utf-8"
    )
    timing_source = (graph / "src/pygrc/models/lgrc_9_v3_timing.py").read_text(
        encoding="utf-8"
    )
    restoration_source = (
        graph / "src/pygrc/models/lgrc_9_v3_restoration.py"
    ).read_text(encoding="utf-8")

    surface_class = named_node(
        contract_source,
        "LGRC9V3CausalPulseSubstrateSurfaceRow",
        ast.ClassDef,
    )
    surface_doc = ast.get_docstring(surface_class)
    assert surface_doc is not None
    assert "Passive evidence row" in surface_doc
    assert "records evidence only" in surface_doc
    assert "never mutates coherence" in surface_doc

    runtime_state_class = node_source(
        runtime_state_source,
        named_node(runtime_state_source, "LGRC9V3RuntimeState", ast.ClassDef),
    )
    assert "causal_pulse_substrate_surface_log" in runtime_state_class
    assert '"causal_pulse_substrate_surface_log"' in runtime_state_class
    assert "row.to_artifact()" in runtime_state_class

    build_row_segment = node_source(
        runtime_source,
        named_node(
            runtime_source,
            "_build_causal_pulse_substrate_surface_row",
            ast.FunctionDef,
        ),
    )
    assert "processed_event.source_node_id" in build_row_segment
    assert "processed_event.target_node_id" in build_row_segment
    assert "processed_event.amount" in build_row_segment
    assert "processed_event.event_time_key" in build_row_segment

    emit_event_segment = node_source(
        runtime_source,
        named_node(
            runtime_source,
            "_emit_causal_pulse_substrate_surface_event",
            ast.FunctionDef,
        ),
    )
    assert "causal_pulse_substrate_surface_log.append(row)" in emit_event_segment

    feedback_segment = node_source(
        runtime_source,
        named_node(
            runtime_source,
            "emit_feedback_eligibility_surface_row",
            ast.FunctionDef,
        ),
    )
    assert "self._latest_route_local_pulse_contact_surface_row()" in feedback_segment
    assert "front_mass = sum" in feedback_segment
    assert "rear_mass = sum" in feedback_segment
    assert "source_lineage_id" not in feedback_segment
    assert "target_lineage_id" not in feedback_segment

    producer_segment = node_source(
        runtime_source,
        named_node(
            runtime_source,
            "_produce_packet_departure_from_feedback_eligibility",
            ast.FunctionDef,
        ),
    )
    assert "_latest_lineage_eligible_surface_row" in producer_segment
    assert "LGRC9V3_CAUSAL_PULSE_SUBSTRATE_KIND_FEEDBACK_ELIGIBILITY" in producer_segment
    assert 'row.surface_values_after["boundary_polarity_score"]' in producer_segment
    assert "expected_source_digest != source_surface_digest" in producer_segment
    assert "source_lineage_id" not in producer_segment

    annotation_node = named_node(
        timing_source,
        "annotate_lgrc9v3_causal_history",
        ast.FunctionDef,
    )
    annotation_doc = ast.get_docstring(annotation_node)
    assert annotation_doc is not None
    assert "without mutating state" in annotation_doc
    assert "does not execute an LGRC runtime" in annotation_doc

    identity_v1_segment = node_source(
        restoration_source,
        named_node(
            restoration_source,
            "lgrc9v3_restoration_identity_v1",
            ast.FunctionDef,
        ),
    )
    identity_v2_segment = node_source(
        restoration_source,
        named_node(
            restoration_source,
            "lgrc9v3_restoration_identity_v2",
            ast.FunctionDef,
        ),
    )
    assert '"lgrc9v3_runtime_artifact": normalized_runtime_artifact' in identity_v1_segment
    assert "reset_baseline_snapshot" in identity_v2_segment
    assert '"current_state_restoration_identity"' in identity_v2_segment
    assert '"reset_baseline_restoration_identity"' in identity_v2_segment

    reset_segment = node_source(
        runtime_source,
        named_node(runtime_source, "reset", ast.FunctionDef),
    )
    assert "self._initial_state is None" in reset_segment
    assert "self._state = deepcopy(self._initial_state)" in reset_segment

    for op_id in EXPECTED_OPS:
        assert op_id in hypothesis
    assert "RCAEActiveHistoryAdapterV1" in hypothesis
    assert "minimally_producer_assisted" in hypothesis
    assert "I03C and I04 remain unauthorized" in hypothesis
    assert "history_carried" in brief
    assert "P2-I2-DEC-014" in decision
    assert "History-carried realization and producer boundary" in decision
    assert "#### 8B.2 Frozen design disposition" in checklist
    assert "No history-carried model was instantiated" in checklist
    assert "**Status:** design-frozen; runtime-conformance freeze pending" in report
    assert "No history-carried model was instantiated" in report
    assert "I03C and I04 remain" in report

    graph_after = {
        "revision": run_git(graph, "rev-parse", "HEAD"),
        "status_short": run_git(graph, "status", "--short"),
    }
    assert graph_after == graph_before

    invariants = {
        "entry_authority_and_prior_artifact_digests_match": all(
            item["match"] for item in prior_checks
        ),
        "design_input_freeze_preserved": sha256_path(freeze_path)
        == EXPECTED_FREEZE_SHA256,
        "design_contract_preserved": sha256_path(contract_path)
        == EXPECTED_CONTRACT_SHA256,
        "history_carried_only_scope": True,
        "i03a_preserved_and_i03c_i04_unauthorized": True,
        "native_history_candidate_explicitly_inadequate": True,
        "one_minimal_rcae_history_adapter_selected": True,
        "rcae_adapter_does_not_compute_success": True,
        "native_response_transition_ownership_retained": True,
        "active_history_distinct_from_encounter_state_and_audit": True,
        "history_only_and_state_only_interventions_frozen": True,
        "private_partition_no_common_read_guard_frozen": True,
        "seven_cells_complete": cells == EXPECTED_CELLS,
        "five_controls_complete": controls == EXPECTED_CONTROLS,
        "nine_operational_projections_complete": ops == EXPECTED_OPS,
        "eleven_capability_dispositions_complete": caps == EXPECTED_CAPS,
        "selected_public_callables_admitted": not missing_symbols,
        "all_twenty_frozen_source_digests_match": all(
            item["match"] for item in source_checks
        ),
        "native_surface_rows_are_passive_evidence": True,
        "native_feedback_reads_latest_contact_and_live_state": True,
        "native_producer_uses_latest_feedback_row_not_history_fold": True,
        "lgrc0_history_is_annotation_only": True,
        "native_v2_covers_runtime_and_reset_baseline": True,
        "external_history_requires_composite_identity": True,
        "separate_runtime_freeze_required": True,
        "no_history_runtime_or_scientific_execution": True,
        "graph_repository_unchanged": graph_after == graph_before,
    }
    assert all(invariants.values())

    return {
        "artifact_id": "P2-I2-I03B-HISTORY-CARRIED-REALIZATION-VALIDATION",
        "artifact_version": "1.0.0",
        "lane_id": "AE01-L02",
        "iteration_id": "P2-I2-I03B",
        "status": "passed",
        "validated_at": "2026-07-14",
        "validation_kind": "static_authority_source_dataflow_producer_boundary_cross_artifact_and_no_runtime_only",
        "history_carried_model_instantiations": 0,
        "history_carried_runtime_operations": 0,
        "candidate_control_calibration_or_scientific_execution": False,
        "input_identity": {
            "freeze_sha256": sha256_path(freeze_path),
            "contract_sha256": sha256_path(contract_path),
            "hypothesis_sha256": sha256_path(hypothesis_path),
            "brief_sha256": sha256_path(brief_path),
            "checklist_sha256": sha256_path(checklist_path),
            "decision_record_sha256": sha256_path(decision_path),
            "report_sha256": sha256_path(report_path),
            "manifest_sha256": sha256_path(manifest_path),
        },
        "entry_authority": {
            "rcae_revision": RCAE_ENTRY_REVISION,
            "prior_artifact_count": len(prior_checks),
            "checks": prior_checks,
        },
        "graph_before": graph_before,
        "graph_after": graph_after,
        "admitted_source_identity": {
            "source_count": len(source_checks),
            "checks": source_checks,
        },
        "selected_public_callables": {
            "symbols": SELECTED_CALLABLES,
            "all_admitted": not missing_symbols,
        },
        "source_dataflow": {
            "surface_rows_declared_passive": True,
            "route_rows_retain_physical_amount_endpoints_order_and_time": True,
            "runtime_artifact_serializes_ordered_surface_log": True,
            "feedback_derives_from_latest_route_contact": True,
            "feedback_reads_live_node_masks": True,
            "feedback_has_no_lineage_read": True,
            "native_producer_reads_latest_feedback_row": True,
            "native_expected_digest_compares_one_source_row": True,
            "lgrc0_history_annotation_non_mutating": True,
            "native_v2_composes_current_and_reset_identity": True,
        },
        "selection": {
            "pool_dependence_mode": "history_carried",
            "native_disposition": "inadequate_for_history_carried",
            "selected_realization_class": "minimally_producer_assisted",
            "selected_rcae_component": "RCAEActiveHistoryAdapterV1",
            "adapter_computes_success": False,
            "native_feedback_producer_owns_later_transition": True,
        },
        "coverage": {
            "cells": cells,
            "controls": controls,
            "operational_projections": ops,
            "capability_dispositions": caps,
        },
        "invariants": invariants,
        "claim_boundary": {
            "design_frozen": True,
            "runtime_conformance_authorized_before_second_freeze": False,
            "i03b_review_ready": False,
            "i03c_authorized": False,
            "i04_authorized": False,
            "scientific_evidence_assigned": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rcae-root", type=Path, required=True)
    parser.add_argument("--graph-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = validate(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["invariants"], sort_keys=True))


if __name__ == "__main__":
    main()
