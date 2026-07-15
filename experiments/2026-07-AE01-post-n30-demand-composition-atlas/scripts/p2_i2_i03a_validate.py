"""Static validator for the P2-I2-I03A state-carried freeze.

This script validates retained authority and admitted source dataflow only. It
does not construct or execute a P2-I2 candidate, cell, control, response, or
calibration operation.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


RCAE_ENTRY_REVISION = "26811d395c0662473629d5710983e3c1fdb4f58f"
GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
EXPECTED_FREEZE_SHA256 = "34d0903c746fb67abff5a1c12bb252b5cb15933d2de75e56f1232fbe7dfd0845"
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


def function_node(source: str, name: str) -> ast.FunctionDef:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"function not found: {name}")


def function_source(source: str, node: ast.FunctionDef) -> str:
    segment = ast.get_source_segment(source, node)
    if segment is None:
        raise AssertionError(f"source segment unavailable: {node.name}")
    return segment


def validate(args: argparse.Namespace) -> dict[str, Any]:
    rcae = args.rcae_root.resolve()
    graph = args.graph_root.resolve()
    experiment = rcae / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
    contract_dir = experiment / "contracts/p2-i2"

    freeze_path = contract_dir / "i03a-state-carried-realization-freeze-input.json"
    contract_path = (
        contract_dir / "i03a-state-carried-realization-and-discriminator-contract.json"
    )
    manifest_path = contract_dir / "i02r2-admitted-source-and-reset-provider-manifest.json"
    hypothesis_path = experiment / "hypotheses/p2-i2-operational-hypotheses.md"
    brief_path = experiment / "implementation/P2-I2-shared-pool-co-conditioning-brief.md"
    checklist_path = experiment / "implementation/P2-I2-shared-pool-co-conditioning-checklist.md"
    decision_path = experiment / "implementation/P2-I2-decision-record.md"
    report_path = experiment / "reports/P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md"

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

    entry_checks: list[dict[str, Any]] = []
    for item in freeze["frozen_inputs"]:
        content = subprocess.run(
            ["git", "-C", str(rcae), "show", f"{RCAE_ENTRY_REVISION}:{item['path']}"],
            check=True,
            capture_output=True,
        ).stdout
        actual = sha256_bytes(content)
        match = actual == item["sha256"]
        assert match, item["path"]
        entry_checks.append(
            {
                "path": item["path"],
                "expected_sha256": item["sha256"],
                "entry_revision_sha256": actual,
                "match": match,
            }
        )

    assert freeze["iteration_id"] == "P2-I2-I03A"
    assert sha256_path(freeze_path) == EXPECTED_FREEZE_SHA256
    assert freeze["mode_scope"]["active_mode"] == "state_carried"
    assert freeze["mode_scope"]["later_modes_authorized"] is False
    assert freeze["mode_scope"]["later_mode_work_prohibited_in_i03a"] is True
    assert len(freeze["review_questions"]) == 12

    assert contract["iteration_id"] == "P2-I2-I03A"
    assert contract["status"] == "review_ready"
    assert contract["mode_scope"]["pool_dependence_mode"] == "state_carried"
    assert contract["mode_scope"]["ordered_contribution_history_is_causal"] is False
    assert contract["mode_scope"]["audit_lineage_is_causal"] is False
    assert contract["realization_selection"]["realization_class"] == (
        "pygrc_native_candidate"
    )
    assert contract["realization_selection"]["rcae_causal_producer_selected"] is False
    assert contract["realization_selection"]["rcae_constructed_pool_state_selected"] is False
    assert contract["causal_factorization"]["V"]["state_carried_guard"].startswith(
        "expected_source_surface_digest remains null"
    )
    assert contract["review_stop"]["i03b_authorized"] is False
    assert contract["review_stop"]["i03c_authorized"] is False
    assert contract["review_stop"]["i04_authorized"] is False
    assert contract["review_stop"]["calibration_authorized"] is False
    assert contract["review_stop"]["candidate_execution_authorized"] is False
    assert contract["review_stop"]["scientific_evidence_assigned"] is False

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

    assert contract["restoration_profile_proposal"]["provider"] == (
        "pygrc.models.lgrc9v3_restoration_identity_v2"
    )
    assert contract["restoration_profile_proposal"]["selection_status"] == (
        "proposed_by_I03A_not_frozen_until_I06"
    )
    required_i04_deferred = {
        "one exact raw later-response field or family",
        "response orientation transform",
        "one closest insufficient-repetition primary comparator",
        "equality and measurement-resolution rule",
        "candidate-blind matched-null generator and seeds",
        "machine pass, ambiguous, and fail evaluation",
    }
    assert required_i04_deferred.issubset(set(contract["deferred_to_i04"]))

    manifest_symbols = {item["symbol"] for item in manifest["callable_entries"]}
    missing_symbols = sorted(set(SELECTED_CALLABLES) - manifest_symbols)
    assert not missing_symbols, missing_symbols

    source_checks: list[dict[str, Any]] = []
    for item in manifest["source_entries"]:
        relative = item["source_id"].removeprefix("grc:")
        revision_content = subprocess.run(
            ["git", "-C", str(graph), "show", f"{GRAPH_REVISION}:{relative}"],
            check=True,
            capture_output=True,
        ).stdout
        revision_sha = sha256_bytes(revision_content)
        worktree_sha = sha256_path(graph / relative)
        match = revision_sha == worktree_sha == item["sha256"]
        assert match, item["source_id"]
        source_checks.append(
            {
                "source_id": item["source_id"],
                "manifest_sha256": item["sha256"],
                "revision_sha256": revision_sha,
                "worktree_sha256": worktree_sha,
                "match": match,
            }
        )

    packets_path = graph / "src/pygrc/models/lgrc_9_v3_packets.py"
    runtime_path = graph / "src/pygrc/models/lgrc_9_v3_runtime.py"
    packets_source = packets_path.read_text(encoding="utf-8")
    runtime_source = runtime_path.read_text(encoding="utf-8")

    packet_id_node = function_node(packets_source, "build_lgrc9v3_packet_id")
    packet_id_args = [arg.arg for arg in packet_id_node.args.kwonlyargs]
    assert "source_lineage_id" not in packet_id_args
    assert "target_lineage_id" not in packet_id_args

    arrival_segment = function_source(
        packets_source,
        function_node(packets_source, "process_lgrc9v3_packet_arrival"),
    )
    assert "target_coherence + packet.amount" in arrival_segment
    assert "source_lineage_id=packet.source_lineage_id" in arrival_segment

    feedback_segment = function_source(
        runtime_source,
        function_node(runtime_source, "emit_feedback_eligibility_surface_row"),
    )
    assert "front_mass = sum" in feedback_segment
    assert "rear_mass = sum" in feedback_segment
    assert "boundary_polarity_score" in feedback_segment
    assert "source_lineage_id" not in feedback_segment
    assert "target_lineage_id" not in feedback_segment

    producer_segment = function_source(
        runtime_source,
        function_node(runtime_source, "_produce_packet_departure_from_feedback_eligibility"),
    )
    assert 'row.surface_values_after["boundary_polarity_score"]' in producer_segment
    assert "source_lineage_id" not in producer_segment
    assert "target_lineage_id" not in producer_segment

    for op_id in EXPECTED_OPS:
        assert op_id in hypothesis
    assert "P2-I2-I03A-REVIEW-READY" in hypothesis
    assert "I03B history-carried and I03C hybrid profiles remain" in hypothesis
    assert "all three profiles continue" in hypothesis
    assert "They are not alternatives in" in hypothesis
    assert "P2-I2-DEC-011" in brief
    assert "no later iteration" in brief
    assert "chooses one of the three modes as a winner" in brief
    assert "P2-I2-CHG-008" in checklist
    assert "No later iteration selects one of those modes as the winner" in checklist
    assert "P2-I2-DEC-011" in decision
    assert "P2-I2 retains and tests all three dependence modes" in decision
    assert "Post-freeze owner scope clarification" in report

    graph_after = {
        "revision": run_git(graph, "rev-parse", "HEAD"),
        "status_short": run_git(graph, "status", "--short"),
    }
    assert graph_after == graph_before

    invariants = {
        "entry_authority_digests_match": all(item["match"] for item in entry_checks),
        "original_i03a_freeze_preserved": sha256_path(freeze_path) == EXPECTED_FREEZE_SHA256,
        "state_carried_only_scope": True,
        "later_modes_unauthorized": True,
        "three_modes_retained_downstream": True,
        "realization_selection_occurs_within_modes": True,
        "native_candidate_without_rcae_causal_producer": True,
        "seven_cells_complete": cells == EXPECTED_CELLS,
        "five_controls_complete": controls == EXPECTED_CONTROLS,
        "nine_operational_projections_complete": ops == EXPECTED_OPS,
        "eleven_capability_dispositions_complete": caps == EXPECTED_CAPS,
        "selected_public_callables_admitted": not missing_symbols,
        "all_admitted_source_digests_match": all(
            item["match"] for item in source_checks
        ),
        "lineage_excluded_from_packet_identity": True,
        "arrival_mutates_common_state_additively": True,
        "feedback_reads_node_state_without_lineage": True,
        "native_producer_reads_state_derived_score_without_lineage": True,
        "i04_measurement_choices_deferred": True,
        "v2_provider_proposed_not_frozen": True,
        "no_candidate_or_calibration_execution": True,
        "graph_repository_unchanged": graph_after == graph_before,
    }
    assert all(invariants.values())

    return {
        "artifact_id": "P2-I2-I03A-STATE-CARRIED-REALIZATION-VALIDATION",
        "artifact_version": "1.1.0",
        "lane_id": "AE01-L02",
        "iteration_id": "P2-I2-I03A",
        "status": "passed",
        "validated_at": "2026-07-14",
        "validation_kind": "static_authority_source_dataflow_cross_artifact_and_scope_transition_only",
        "candidate_or_calibration_execution": False,
        "input_identity": {
            "freeze_sha256": sha256_path(freeze_path),
            "contract_sha256": sha256_path(contract_path),
            "hypothesis_sha256": sha256_path(hypothesis_path),
            "brief_sha256": sha256_path(brief_path),
            "checklist_sha256": sha256_path(checklist_path),
            "decision_record_sha256": sha256_path(decision_path),
            "manifest_sha256": sha256_path(manifest_path),
        },
        "entry_authority": {
            "rcae_revision": RCAE_ENTRY_REVISION,
            "artifact_count": len(entry_checks),
            "checks": entry_checks,
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
            "packet_id_keyword_arguments": packet_id_args,
            "lineage_absent_from_packet_id": True,
            "arrival_adds_packet_amount_to_target_coherence": True,
            "arrival_retains_lineage_in_audit_record": True,
            "feedback_sums_declared_node_coherence_masks": True,
            "feedback_has_no_lineage_read": True,
            "producer_reads_boundary_polarity_score": True,
            "producer_has_no_lineage_read": True,
        },
        "coverage": {
            "cells": cells,
            "controls": controls,
            "operational_projections": ops,
            "capability_dispositions": caps,
        },
        "invariants": invariants,
        "claim_boundary": {
            "i03a_review_ready": True,
            "all_three_modes_retained_through_execution": True,
            "inter_mode_winner_selection_allowed": False,
            "umbrella_discriminator_gate_passed": False,
            "i03b_authorized": False,
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
