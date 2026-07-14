"""Static validator for the P2-I2-I03C hybrid design freeze.

This validator checks authority, admitted-source identity, native joint-read
dataflow, active-history producer minimality, discriminator coverage, and the
freeze-before-runtime boundary. It never imports PyGRC, instantiates a model,
or executes a hybrid candidate, cell, control, response, or conformance run.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


RCAE_ENTRY_REVISION = "9332a67558764043d6f6adf67dc82a19187871db"
GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
EXPECTED_FREEZE_SHA256 = (
    "1d69dedf481aba2ad996388d35e03e65e7a7e5cc39276feaf8d92b730208c353"
)
EXPECTED_CONTRACT_SHA256 = (
    "eed0a4a84fbcf3da35c222347d3dd913d6dd5bc8bc8e4906e0fb8eea5d1e3fc8"
)
EXPECTED_ADAPTER_SHA256 = (
    "b1040726aaa524538911c6022f16a820091ac6a5c6ec006860d2b321faab2d2c"
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
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def named_node(source: str, name: str, node_type: type[ast.AST]) -> ast.AST:
    for node in ast.walk(ast.parse(source)):
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

    freeze_path = contract_dir / "i03c-hybrid-realization-freeze-input.json"
    contract_path = (
        contract_dir / "i03c-hybrid-realization-and-discriminator-contract.json"
    )
    output_path = contract_dir / "i03c-hybrid-realization-validation.json"
    manifest_path = (
        contract_dir / "i02r2-admitted-source-and-reset-provider-manifest.json"
    )
    adapter_path = experiment / "scripts/p2_i2_i03b_history_adapter.py"
    hypothesis_path = experiment / "hypotheses/p2-i2-operational-hypotheses.md"
    brief_path = experiment / "implementation/P2-I2-shared-pool-co-conditioning-brief.md"
    checklist_path = (
        experiment / "implementation/P2-I2-shared-pool-co-conditioning-checklist.md"
    )
    decision_path = experiment / "implementation/P2-I2-decision-record.md"
    report_path = (
        experiment
        / "reports/P2-I2-I03C-hybrid-realization-and-operational-hypothesis-freeze.md"
    )

    assert args.output.resolve() == output_path.resolve()
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    adapter_source = adapter_path.read_text(encoding="utf-8")
    hypothesis = hypothesis_path.read_text(encoding="utf-8")
    brief = brief_path.read_text(encoding="utf-8")
    checklist = checklist_path.read_text(encoding="utf-8")
    decision = decision_path.read_text(encoding="utf-8")
    report = report_path.read_text(encoding="utf-8")

    graph_before = {
        "revision": run_git(graph, "rev-parse", "HEAD"),
        "status_short": run_git(graph, "status", "--short"),
    }
    assert graph_before == {"revision": GRAPH_REVISION, "status_short": ""}

    assert freeze["iteration_id"] == "P2-I2-I03C"
    assert freeze["pool_dependence_mode"] == "hybrid"
    assert sha256_path(freeze_path) == EXPECTED_FREEZE_SHA256
    assert freeze["entry_authority"]["rcae_entry_revision"] == RCAE_ENTRY_REVISION
    assert freeze["entry_authority"]["graph_revision"] == GRAPH_REVISION
    assert freeze["entry_authority"]["graph_repository_read_only"] is True
    assert freeze["design_phase_run_policy"]["hybrid_model_instantiations"] == 0
    assert freeze["design_phase_run_policy"]["hybrid_runtime_operations"] == 0
    assert freeze["design_phase_run_policy"]["candidate_or_control_executions"] == 0
    assert freeze["runtime_transition_rule"]["separate_runtime_freeze_required"] is True
    assert freeze["runtime_transition_rule"]["retry_limit"] == 0
    assert len(freeze["comparison_questions"]) == 10
    assert freeze["selection_order"] == [
        "pygrc_native_candidate",
        "minimally_producer_assisted",
        "missing_prerequisite",
    ]
    minimum = freeze["hybrid_minimum_contract"]
    assert minimum["native_state_component_is_causal"] is True
    assert minimum["ordered_or_structured_common_history_is_causal"] is True
    assert minimum["state_only_intervention_required"] is True
    assert minimum["history_only_intervention_required"] is True
    assert minimum["joint_functional_dependence_required"] is True
    assert minimum["nonlinearity_required"] is False

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
    assert len(prior_checks) == 9

    guards = freeze["cross_mode_contamination_guards"]
    assert all(value is False for value in guards.values())
    assert len(freeze["carried_i03br1_obligations"]) == 6

    assert sha256_path(contract_path) == EXPECTED_CONTRACT_SHA256
    assert contract["iteration_id"] == "P2-I2-I03C"
    assert contract["status"] == "design_frozen_runtime_conformance_freeze_pending"
    assert contract["mode_scope"]["pool_dependence_mode"] == "hybrid"
    assert contract["mode_scope"]["native_encounter_state_is_causal"] is True
    assert contract["mode_scope"]["ordered_common_history_is_causal"] is True
    assert contract["mode_scope"]["audit_lineage_is_causal"] is False
    assert contract["mode_scope"]["nonlinearity_required"] is False
    assert contract["mode_scope"]["joint_functional_dependence_required"] is True
    assert contract["native_first_source_comparison"]["native_candidate_disposition"] == (
        "inadequate_for_complete_hybrid"
    )
    assert contract["native_first_source_comparison"]["selected_disposition"] == (
        "minimally_producer_assisted"
    )
    selection = contract["realization_selection"]
    assert selection["realization_class"] == "minimally_producer_assisted"
    assert selection["selected_rcae_component"] == "RCAEActiveHistoryAdapterV1"
    assert selection["selected_component_sha256"] == EXPECTED_ADAPTER_SHA256
    assert selection["rcae_producer_computes_joint_score_success_or_later_response"] is False
    assert selection["native_feedback_producer_owns_joint_evaluation_and_later_transition"] is True
    assert sha256_path(adapter_path) == EXPECTED_ADAPTER_SHA256

    factorization = contract["causal_factorization"]
    assert factorization["U_S"]["owner"].startswith("PyGRC")
    assert factorization["U_H"]["owner"] == "RCAEActiveHistoryAdapterV1"
    assert factorization["M_H"]["native_ownership"].startswith(
        "all reservoir/sink transport"
    )
    assert factorization["L"]["response_read_allowed"] is False
    assert factorization["V"]["joint_family"].startswith("J(C_P,R_H) = C_P + R_H")
    assert factorization["V"]["history_guard"].startswith(
        "expected_source_surface_digest is null"
    )
    assert "P and M_H exactly once each" in factorization["V"]["joint_read"]
    forbidden = factorization["forbidden_G"]["prohibited_inputs_or_actions"]
    assert "one controller calculating P plus H_P plus success" in forbidden
    assert "using expected_source_surface_digest as authorization" in forbidden

    producer = contract["producer_boundary"]
    assert producer["component"] == "RCAEActiveHistoryAdapterV1"
    assert producer["single_missing_operation"].startswith(
        "maintain/intervene on one active ordered common history"
    )
    assert producer["handoff"].startswith("The adapter stops after M_H materialization")
    assert "read P as a joint-success input" in producer["forbidden_calls_or_reads"]
    assert "compute P plus M_H or apply the response threshold" in producer[
        "forbidden_calls_or_reads"
    ]
    assert "schedule the later A-to-B packet" in producer["forbidden_calls_or_reads"]

    cells = [item["cell_id"] for item in contract["logical_cells"]]
    controls = [item["control_id"] for item in contract["lane_controls"]]
    ops = [item["op_id"] for item in contract["operational_projections"]]
    assert cells == EXPECTED_CELLS
    assert controls == EXPECTED_CONTROLS
    assert ops == EXPECTED_OPS
    for item in contract["lane_controls"]:
        assert item["target"]
        assert item["held_fixed"]
        assert item["expected_relation"]
        assert item["allowed_ambiguity"]
        assert item["fail_closed_effect"]

    discriminators = contract["hybrid_discriminators"]
    assert "P coherence" in discriminators["state_only_intervention"]["allowed_difference"]
    assert "H_P/R_H/M_H" in discriminators["history_only_intervention"]["allowed_difference"]
    assert discriminators["joint_contrast"]["nonlinearity_required"] is False
    assert "both one-component interventions affect" in discriminators[
        "joint_contrast"
    ]["required_relation"]
    assert contract["common_access_witness"]["source_address_or_lineage_input"] is False
    assert len(contract["private_partition_competitor"]["required_guards"]) == 6

    restoration = contract["restoration_profile_proposal"]
    assert restoration["native_provider"] == (
        "pygrc.models.lgrc9v3_restoration_identity_v2"
    )
    assert "H_P token sequence" in restoration["external_current_state"]
    assert "complete adapter baseline" in restoration["external_reset_baseline"]
    assert "one registered paired procedure" in restoration["reset_policy"]
    assert "original/load/reset branches" in restoration[
        "equal_input_continuation_requirement"
    ]
    transition = contract["runtime_conformance_transition"]
    assert transition["separate_runtime_freeze_required"] is True
    assert transition[
        "runtime_fixture_values_must_be_new_fixture_only_and_not_imported_from_i03a_or_i03b"
    ] is True
    assert transition["one_evidence_invocation"] is True
    assert transition["one_reconstruction_invocation"] is True
    assert transition["retry_limit"] == 0
    assert transition["parameter_search_allowed"] is False
    assert contract["review_stop"]["I04_authorized"] is False
    assert contract["review_stop"]["discriminator_gate_passed"] is False
    assert contract["review_stop"]["scientific_evidence_assigned"] is False

    manifest_symbols = {item["symbol"] for item in manifest["callable_entries"]}
    missing_symbols = sorted(set(SELECTED_CALLABLES) - manifest_symbols)
    assert not missing_symbols, missing_symbols

    manifest_sources = {item["source_id"]: item for item in manifest["source_entries"]}
    frozen_source_ids = freeze["admitted_source_scope"]["source_ids"]
    assert len(frozen_source_ids) == 20
    assert len(set(frozen_source_ids)) == 20
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
    runtime_source = (graph / "src/pygrc/models/lgrc_9_v3_runtime.py").read_text(
        encoding="utf-8"
    )
    timing_source = (graph / "src/pygrc/models/lgrc_9_v3_timing.py").read_text(
        encoding="utf-8"
    )
    restoration_source = (
        graph / "src/pygrc/models/lgrc_9_v3_restoration.py"
    ).read_text(encoding="utf-8")

    surface = named_node(
        contract_source, "LGRC9V3CausalPulseSubstrateSurfaceRow", ast.ClassDef
    )
    surface_doc = ast.get_docstring(surface)
    assert surface_doc is not None
    assert "Passive evidence row" in surface_doc
    assert "records evidence only" in surface_doc
    assert "never mutates coherence" in surface_doc

    feedback_segment = node_source(
        runtime_source,
        named_node(runtime_source, "emit_feedback_eligibility_surface_row", ast.FunctionDef),
    )
    assert "self._latest_route_local_pulse_contact_surface_row()" in feedback_segment
    assert "front_mass = sum" in feedback_segment
    assert "rear_mass = sum" in feedback_segment
    assert "for node_id in front_nodes" in feedback_segment
    assert "for node_id in rear_nodes" in feedback_segment
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
    assert 'row.surface_values_after["boundary_polarity_score"]' in producer_segment
    assert "expected_source_digest != source_surface_digest" in producer_segment
    assert "source_lineage_id" not in producer_segment

    annotation = named_node(
        timing_source, "annotate_lgrc9v3_causal_history", ast.FunctionDef
    )
    annotation_doc = ast.get_docstring(annotation)
    assert annotation_doc is not None
    assert "without mutating state" in annotation_doc
    assert "does not execute an LGRC runtime" in annotation_doc

    identity_v2_segment = node_source(
        restoration_source,
        named_node(
            restoration_source, "lgrc9v3_restoration_identity_v2", ast.FunctionDef
        ),
    )
    assert "reset_baseline_snapshot" in identity_v2_segment
    assert '"current_state_restoration_identity"' in identity_v2_segment
    assert '"reset_baseline_restoration_identity"' in identity_v2_segment
    reset_segment = node_source(
        runtime_source, named_node(runtime_source, "reset", ast.FunctionDef)
    )
    assert "self._state = deepcopy(self._initial_state)" in reset_segment

    adapter_class = node_source(
        adapter_source,
        named_node(adapter_source, "RCAEActiveHistoryAdapterV1", ast.ClassDef),
    )
    for required in (
        "def ingest_new_rows",
        "def replace_history",
        "def readout",
        "def materialize_readout",
        "def restoration_identity_artifact",
        "def save",
        "def load",
        "def reset",
        "model.schedule_packet_departure",
        "model.step",
    ):
        assert required in adapter_class
    for forbidden_call in (
        "emit_feedback_eligibility_surface_row",
        "set_feedback_coupled_pulse_producer",
        "produce_events",
    ):
        assert forbidden_call not in adapter_class
    materialize_segment = node_source(
        adapter_source,
        named_node(adapter_source, "materialize_readout", ast.FunctionDef),
    )
    assert '"success_or_response_computed": False' in materialize_segment
    assert '"later_response_scheduled": False' in materialize_segment
    assert '"direct_native_state_mutation": False' in materialize_segment
    assert "model.get_state().base_state.nodes[node_id].coherence" in materialize_segment
    ingest_segment = node_source(
        adapter_source, named_node(adapter_source, "ingest_new_rows", ast.FunctionDef)
    )
    assert "row.contact_amount" in ingest_segment
    assert "row.source_lineage_id" not in ingest_segment
    assert "row.target_lineage_id" not in ingest_segment
    assert "row.surface_digest" in ingest_segment

    for op_id in EXPECTED_OPS:
        assert op_id in hypothesis
    assert "[P,M_H]" in hypothesis or "[P, M_H]" in hypothesis
    assert "minimally_producer_assisted" in hypothesis
    assert "P2-I2-DEC-016" in decision
    assert "Hybrid realization and producer boundary" in decision
    assert "### 8C." in checklist
    assert "No hybrid model has been instantiated" in checklist
    assert "minimally producer-assisted" in checklist
    assert "**Status:** design-frozen" in report
    assert "No hybrid model was instantiated" in report
    assert "I04 remains blocked" in report
    assert "hybrid" in brief

    graph_after = {
        "revision": run_git(graph, "rev-parse", "HEAD"),
        "status_short": run_git(graph, "status", "--short"),
    }
    assert graph_after == graph_before

    invariants = {
        "entry_authority_and_nine_prior_artifact_digests_match": all(
            item["match"] for item in prior_checks
        ),
        "design_input_freeze_preserved": sha256_path(freeze_path)
        == EXPECTED_FREEZE_SHA256,
        "design_contract_preserved": sha256_path(contract_path)
        == EXPECTED_CONTRACT_SHA256,
        "hybrid_only_scope_and_cross_mode_guards_preserved": True,
        "native_complete_hybrid_explicitly_inadequate": True,
        "minimal_active_history_adapter_selected": True,
        "adapter_does_not_compute_joint_success_or_response": True,
        "native_joint_evaluation_and_later_transition_retained": True,
        "state_and_active_history_components_separately_causal": True,
        "state_only_and_history_only_interventions_frozen": True,
        "joint_contrast_and_nonrequired_nonlinearity_frozen": True,
        "private_partition_and_alternate_access_guards_frozen": True,
        "seven_cells_complete": cells == EXPECTED_CELLS,
        "five_controls_complete": controls == EXPECTED_CONTROLS,
        "nine_operational_projections_complete": ops == EXPECTED_OPS,
        "six_i03br1_obligations_carried": len(
            freeze["carried_i03br1_obligations"]
        )
        == 6,
        "selected_public_callables_admitted": not missing_symbols,
        "all_twenty_frozen_source_digests_match": all(
            item["match"] for item in source_checks
        ),
        "native_feedback_sums_multi_node_live_masks": True,
        "native_surface_rows_are_passive_not_active_history": True,
        "native_producer_uses_native_score_threshold_and_packet_path": True,
        "lgrc0_history_is_annotation_only": True,
        "native_v2_covers_current_and_reset_identity": True,
        "external_history_requires_composite_paired_identity": True,
        "separate_new_value_runtime_freeze_required": True,
        "no_hybrid_runtime_or_scientific_execution": True,
        "graph_repository_unchanged": graph_after == graph_before,
    }
    assert all(invariants.values())

    return {
        "artifact_id": "P2-I2-I03C-HYBRID-REALIZATION-VALIDATION",
        "artifact_version": "1.0.0",
        "lane_id": "AE01-L02",
        "iteration_id": "P2-I2-I03C",
        "status": "passed",
        "validated_at": "2026-07-14",
        "validation_kind": "static_authority_source_dataflow_producer_boundary_cross_mode_restoration_and_no_runtime_only",
        "hybrid_model_instantiations": 0,
        "hybrid_runtime_operations": 0,
        "candidate_control_calibration_or_scientific_execution": False,
        "input_identity": {
            "freeze_sha256": sha256_path(freeze_path),
            "contract_sha256": sha256_path(contract_path),
            "adapter_sha256": sha256_path(adapter_path),
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
            "native_front_mask_accepts_and_sums_multiple_live_nodes": True,
            "native_joint_mask_has_no_lineage_read": True,
            "native_latest_contact_is_trigger_audit_not_joint_score_input": True,
            "native_producer_reads_native_feedback_score_and_threshold": True,
            "surface_rows_declared_passive": True,
            "lgrc0_history_annotation_non_mutating": True,
            "adapter_ingests_physical_amount_without_lineage_token": True,
            "adapter_materializes_only_through_public_native_packets": True,
            "adapter_has_no_feedback_or_later_response_call": True,
            "native_v2_composes_current_and_reset_identity": True,
        },
        "selection": {
            "pool_dependence_mode": "hybrid",
            "native_disposition": "inadequate_for_complete_hybrid",
            "selected_realization_class": "minimally_producer_assisted",
            "state_component": "native_P_coherence",
            "history_component": "RCAEActiveHistoryAdapterV1.H_P",
            "history_output_port": "native_M_H_coherence",
            "joint_native_front_mask": ["P", "M_H"],
            "adapter_computes_joint_success": False,
            "native_feedback_producer_owns_later_transition": True,
        },
        "coverage": {
            "cells": cells,
            "controls": controls,
            "operational_projections": ops,
            "carried_i03br1_obligations": freeze["carried_i03br1_obligations"],
        },
        "invariants": invariants,
        "claim_boundary": {
            "design_frozen": True,
            "runtime_conformance_authorized_before_second_freeze": False,
            "i03c_review_ready": False,
            "discriminator_gate_passed": False,
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
