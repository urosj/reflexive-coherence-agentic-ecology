"""Pure retained-evidence implication audit for P2-I2 Appendix B."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = ROOT / EXPERIMENT_REL / "scripts"
RUNNER_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_run.py"
ADAPTER_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_history_adapter.py"
ANALYSIS_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_analysis.py"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from p2_i2_app_b_analysis import build_arm_registry, canonical_bytes, digest_value  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def named_function(tree: ast.AST, name: str) -> ast.FunctionDef:
    matches = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == name]
    require(len(matches) == 1, f"expected one function named {name}")
    return matches[0]


def calls_named(node: ast.AST, name: str) -> list[ast.Call]:
    result: list[ast.Call] = []
    for item in ast.walk(node):
        if not isinstance(item, ast.Call):
            continue
        if isinstance(item.func, ast.Name) and item.func.id == name:
            result.append(item)
        elif isinstance(item.func, ast.Attribute) and item.func.attr == name:
            result.append(item)
    return result


def source_flow_audit() -> dict[str, Any]:
    runner_path = ROOT / RUNNER_REL
    adapter_path = ROOT / ADAPTER_REL
    analysis_path = ROOT / ANALYSIS_REL
    runner_source = runner_path.read_text(encoding="utf-8")
    adapter_source = adapter_path.read_text(encoding="utf-8")
    analysis_source = analysis_path.read_text(encoding="utf-8")
    runner_tree = ast.parse(runner_source)
    adapter_tree = ast.parse(adapter_source)
    analysis_tree = ast.parse(analysis_source)

    parent = named_function(runner_tree, "parent_main")
    loops = [node for node in ast.walk(parent) if isinstance(node, ast.For)]
    require(len(loops) == 1, "parent campaign loop count drifted")
    campaign_loop = loops[0]
    analysis_calls = calls_named(parent, "analyze_receipts")
    require(len(analysis_calls) == 1, "parent analysis call count drifted")
    require(
        analysis_calls[0].lineno > int(campaign_loop.end_lineno or 0),
        "analysis no longer occurs strictly after all scheduled arms",
    )
    require(not calls_named(campaign_loop, "analyze_receipts"), "analysis entered campaign loop")
    execute_arm = named_function(runner_tree, "execute_arm")
    require(not calls_named(execute_arm, "analyze_receipts"), "worker outcome depends on analysis")

    operation_loops = [
        node
        for node in ast.walk(execute_arm)
        if isinstance(node, ast.For)
        and any(isinstance(item, ast.Name) and item.id == "operation" for item in ast.walk(node.target))
    ]
    require(len(operation_loops) == 1, "operation loop count drifted")
    operation_loop = operation_loops[0]
    ingest_calls = calls_named(execute_arm, "ingest_new_rows")
    require(len(ingest_calls) == 1, "history ingest call count drifted")
    require(
        operation_loop.lineno <= ingest_calls[0].lineno <= int(operation_loop.end_lineno or 0),
        "history ingest moved outside physical-operation loop",
    )
    require(
        not [call for call in ingest_calls if call.lineno > int(operation_loop.end_lineno or 0)],
        "history ingest occurs after physical operations",
    )
    excluded_after_ingest = {
        "materialize_readout": calls_named(execute_arm, "materialize_readout"),
        "replace_history": calls_named(execute_arm, "replace_history"),
        "emit_feedback_eligibility_surface_row": calls_named(execute_arm, "emit_feedback_eligibility_surface_row"),
        "produce_events": calls_named(execute_arm, "produce_events"),
        "save": calls_named(execute_arm, "save"),
        "load": calls_named(execute_arm, "load"),
        "reset": calls_named(execute_arm, "reset"),
    }
    for name, calls in excluded_after_ingest.items():
        require(calls, f"expected excluded activity missing: {name}")
        require(
            all(call.lineno > int(operation_loop.end_lineno or 0) for call in calls),
            f"excluded activity moved before operation admission completed: {name}",
        )

    adapter = named_function(adapter_tree, "ingest_new_rows")
    adapter_segment = ast.get_source_segment(adapter_source, adapter) or ""
    required_adapter_fragments = (
        "row.surface_kind != ROUTE_LOCAL_CONTACT",
        "row.pulse_event_kind != PACKET_ARRIVAL",
        "row.source_node_id",
        "row.target_node_id",
        "row.pulse_channel_id",
        "row.contact_amount",
        "digest not in consumed",
        "physical arrival matched multiple operations",
    )
    require(
        all(fragment in adapter_segment for fragment in required_adapter_fragments),
        "exact history-admission filter drifted",
    )

    validity = named_function(analysis_tree, "_validity")
    authored_valid_reads = []
    for node in ast.walk(validity):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get":
            if node.args and isinstance(node.args[0], ast.Constant) and node.args[0].value == "valid":
                authored_valid_reads.append(node.lineno)
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and node.slice.value == "valid":
            authored_valid_reads.append(node.lineno)
    require(not authored_valid_reads, "corrected validity reads an authored valid field")

    pygrc_imports = []
    for path, tree in ((adapter_path, adapter_tree), (analysis_path, analysis_tree), (Path(__file__), ast.parse(Path(__file__).read_text(encoding="utf-8")))):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                pygrc_imports.extend((str(path), alias.name) for alias in node.names if alias.name.startswith("pygrc"))
            elif isinstance(node, ast.ImportFrom) and str(node.module).startswith("pygrc"):
                pygrc_imports.append((str(path), str(node.module)))
    require(not pygrc_imports, "pure audit source imports PyGRC")

    return {
        "campaign_loop_precedes_analysis": True,
        "analysis_calls_inside_campaign_loop": 0,
        "worker_analysis_calls": 0,
        "history_ingest_calls": 1,
        "history_ingest_only_inside_operation_loop": True,
        "post_operation_excluded_activity_has_no_later_ingest": True,
        "exact_route_edge_amount_arrival_filter": True,
        "duplicate_surface_admission_refused": True,
        "corrected_validity_authored_valid_reads": 0,
        "audit_pygrc_imports": 0,
        "source_sha256": {
            RUNNER_REL: sha256(runner_path),
            ADAPTER_REL: sha256(adapter_path),
            ANALYSIS_REL: sha256(analysis_path),
        },
    }


def audit(
    freeze_path: Path,
    runtime_path: Path,
    original_path: Path,
    corrected_path: Path,
) -> dict[str, Any]:
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "audit not launched through lexical repository .venv")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "audit requires -B")
    freeze = load_json(freeze_path)
    runtime = load_json(runtime_path)
    original = load_json(original_path)
    corrected = load_json(corrected_path)
    rows = build_arm_registry(freeze["arm_registry_specification"])
    receipts = runtime["receipts"]
    require(len(rows) == len(receipts) == 99, "runtime matrix count drifted")
    require([row["arm_id"] for row in rows] == [item["arm_id"] for item in receipts], "runtime arm order drifted")
    require(len({item["arm_id"] for item in receipts}) == 99, "duplicate runtime arm")
    require(len({item["process_receipt"]["pid"] for item in receipts}) == 99, "fresh child PID count drifted")
    require(runtime["runtime_invocation_count"] == 1, "runtime invocation count drifted")
    require(runtime["scientific_retry_count"] == 0, "scientific retry occurred")
    require(runtime["candidate_parameter_search_count"] == 0, "candidate adaptation occurred")

    three_admission_rows = []
    repeated_operation_rows = []
    for row in rows:
        history_ops = list(row["history_operations"])
        if len(history_ops) == 3:
            three_admission_rows.append(row["arm_id"])
            if len(set(history_ops)) < 3:
                repeated_operation_rows.append(row["arm_id"])
    require(not repeated_operation_rows, "unexpected repeated-operation control classification")

    expected_admissions_total = 0
    actual_admissions_total = 0
    expected_final_tokens_total = 0
    actual_final_tokens_total = 0
    unexpected_admissions = 0
    duplicate_admissions = 0
    token_provenance_mismatches = 0
    operation_route_mismatches = 0
    explicitly_cleared_admissions = 0
    admitted_operation_counts: Counter[str] = Counter()
    clear_interventions = {"carrier_clamp", "history_to_reference", "state_and_history_to_reference"}
    registry = freeze["operation_registry"]
    for row, receipt in zip(rows, receipts, strict=True):
        expected_operations = (
            []
            if row["mode"] == "state_carried"
            else [operation for operation in row["operation_order"] if operation in set(row["common_operations"])]
        )
        admissions = receipt["history_receipt"]["physical_admission_receipts"]
        actual_operations = [item["physical_operation"] for item in admissions]
        expected_admissions_total += len(expected_operations)
        actual_admissions_total += len(admissions)
        unexpected_admissions += int(actual_operations != expected_operations)
        digests = [item["physical_surface_digest"] for item in admissions]
        duplicate_admissions += len(digests) - len(set(digests))
        tokens_from_admissions = [item["token"] for item in admissions]
        final_tokens = receipt["history_receipt"]["tokens"]
        cleared = row["mode"] != "state_carried" and row["intervention"] in clear_interventions
        expected_final_tokens = [] if cleared else tokens_from_admissions
        if cleared:
            explicitly_cleared_admissions += len(tokens_from_admissions)
        expected_final_tokens_total += len(expected_final_tokens)
        actual_final_tokens_total += len(final_tokens)
        token_provenance_mismatches += int(final_tokens != expected_final_tokens)
        operations = {item["operation"]: item for item in receipt["operation_receipts"]}
        for admission in admissions:
            operation_id = admission["physical_operation"]
            operation = operations[operation_id]
            registered = registry[operation_id]
            expected_route = registered["common_route"]
            bookkeeping = [step["bookkeeping"] for step in operation["steps"]]
            route_ok = [operation["source_role"], operation["target_role"], operation["edge_role"]] == expected_route
            amount_ok = float(operation["amount"]) == float(registered["amount"])
            event_ok = (
                [item["processed_event_kind"] for item in bookkeeping]
                == ["lgrc9v3_packet_departure", "lgrc9v3_packet_arrival"]
                and len({item["processed_event_id"] for item in bookkeeping}) == 2
            )
            token_ok = admission["token"] in tokens_from_admissions and float(admission["token"]["contact_amount"]) == float(registered["amount"])
            operation_route_mismatches += int(not (operation["selected_common"] and route_ok and amount_ok and event_ok and token_ok))
            admitted_operation_counts[operation_id] += 1

    require(expected_admissions_total == actual_admissions_total == 123, "history admission total drifted")
    require(unexpected_admissions == 0, "unexpected H_C admission rows")
    require(duplicate_admissions == 0, "duplicate H_C admissions")
    require(operation_route_mismatches == 0, "H_C admission lacks exact physical operation provenance")
    require(token_provenance_mismatches == 0, "final active history lacks exact admission/intervention provenance")
    require(explicitly_cleared_admissions == 12, "explicit history-clear accounting drifted")
    require(expected_final_tokens_total == actual_final_tokens_total == 111, "final active-history token total drifted")

    for receipt in receipts:
        envelope = receipt["response_envelope"]
        window = envelope["window_validity_receipt"]
        response = envelope["i04r1_response_record"]
        require(window["window_contamination_event_ids"] == [], "contaminated response window")
        require(
            response["pre_packet_queue_length"] == response["post_packet_queue_length"] == 0
            and response["pre_birth_queue_length"] == response["post_birth_queue_length"] == 0,
            "response queue contamination",
        )

    require(original["analysis_reconstruction_byte_identical"] is True, "original reconstruction not byte-identical")
    require(original["analysis"] == runtime["analysis"], "original reconstruction differs from embedded analysis")
    require(corrected["inputs"]["runtime"]["sha256"] == sha256(runtime_path), "corrected closeout runtime binding drifted")
    require(corrected["historical_projection_disposition"]["runtime_bytes_changed"] is False, "runtime marked changed")
    require(corrected["historical_projection_disposition"]["original_terminal_had_conclusion_authority"] is False, "historical conclusion not quarantined")
    require(corrected["corrected_analysis"]["primary_results"] == runtime["analysis"]["primary_results"], "primary values changed")
    require(corrected["corrected_analysis"]["controls"] == runtime["analysis"]["controls"], "control values changed")
    require(corrected["correction_boundary"]["response_values_changed"] is False, "response values marked changed")
    require(corrected["correction_boundary"]["estimator_values_changed"] is False, "estimator values marked changed")
    require(corrected["correction_boundary"]["control_values_changed"] is False, "control values marked changed")
    require(
        corrected["reconstruction"]
        == {
            "runtime_generation_count": 0,
            "PyGRC_import_count": 0,
            "model_count": 0,
            "producer_count": 0,
            "arm_count": 0,
            "retained_aggregate_read_count": 1,
            "corrected_analysis_generation_count": 1,
        },
        "retained-only correction process counts drifted",
    )
    corrected_validity = corrected["corrected_analysis"]["operational_validity"]
    require(len(corrected_validity) == 99 and all(item["derived_from_receipts"] for item in corrected_validity.values()), "corrected validity authority drifted")
    require(all(item["valid"] for item in corrected_validity.values()), "corrected validity contains invalid arm")
    required_receipt_checks = {
        "arm_id",
        "row_digest",
        "fresh_process",
        "repository_venv",
        "checkout_pygrc",
        "fresh_model",
        "accepted_topology",
        "three_slots",
        "operation_order",
        "history_token_count",
        "history_source_label_free",
        "history_physical_admissions",
        "window_valid",
        "gain_matches",
        "queue_empty",
        "envelope_present",
        "load_identity",
        "reset_identity",
        "resource_nodes",
        "resource_edges",
        "resource_queue",
    }
    for index in range(3):
        required_receipt_checks.update(
            {
                f"operation_{index}_selection",
                f"operation_{index}_route",
                f"operation_{index}_amount",
                f"operation_{index}_native_steps",
                f"operation_{index}_native_timing",
                f"operation_{index}_budget",
            }
        )
    for arm_id, validity in corrected_validity.items():
        predicates = validity["predicates"]
        check_ids = {item["check_id"] for item in predicates}
        require(required_receipt_checks <= check_ids, f"required receipt validity checks absent: {arm_id}")
        require(all(item["passed"] is True for item in predicates), f"failed receipt validity predicate: {arm_id}")
    require(
        corrected["inputs"]["corrected_analysis_source_sha256"] == sha256(ROOT / ANALYSIS_REL),
        "corrected analysis source binding drifted",
    )

    flow = source_flow_audit()
    result = {
        "artifact_id": "P2-I2-APP-B3-IMPLICATION-BOUNDARY-AUDIT",
        "artifact_version": "1.0",
        "status": "passed_with_matched_cardinality_discriminator_absent_owner_review_pending",
        "inputs": {
            "freeze": {"path": str(freeze_path.relative_to(ROOT)), "sha256": sha256(freeze_path)},
            "runtime": {"path": str(runtime_path.relative_to(ROOT)), "sha256": sha256(runtime_path)},
            "original_reconstruction": {"path": str(original_path.relative_to(ROOT)), "sha256": sha256(original_path)},
            "corrected_closeout": {"path": str(corrected_path.relative_to(ROOT)), "sha256": sha256(corrected_path)},
        },
        "cardinality_quantity_boundary": {
            "three_admission_rows_observed": len(three_admission_rows),
            "repeated_operation_three_admission_rows": repeated_operation_rows,
            "quantity_cardinality_matched_alternative_registered": False,
            "proper_subset_irreducibility_retained": True,
            "operation_complementarity_supported": False,
            "operation_complementarity_status": "unresolved_missing_matched_three_admission_control",
            "retrofit_into_app_b2": False,
            "highest_priority_possible_next_discriminator": "frozen quantity-timing-history-length-matched repeated-operation three-admission panel",
        },
        "fail_open_isolation": {
            "projection_stage": "post_run_after_all_99_child_attempts",
            "runtime_arms_fixed_and_completed": 99,
            "unique_fresh_child_processes": 99,
            "arms_retried_removed_or_outcome_reclassified": 0,
            "runtime_bytes_changed": False,
            "primary_response_estimator_or_control_values_changed": False,
            "historical_embedded_conclusion_quarantined": True,
            "corrected_validity_derived_from_receipts": True,
            "corrected_validity_authored_boolean_reads": 0,
            "receipt_validity_predicates_verified_per_arm": len(required_receipt_checks),
            "source_flow": flow,
        },
        "active_history_reconciliation": {
            "expected_physical_admission_rows": expected_admissions_total,
            "actual_physical_admission_rows": actual_admissions_total,
            "admitted_operation_counts": dict(sorted(admitted_operation_counts.items())),
            "unexpected_admitted_rows": unexpected_admissions,
            "duplicate_admissions": duplicate_admissions,
            "operation_route_or_event_provenance_mismatches": operation_route_mismatches,
            "explicitly_cleared_admissions": explicitly_cleared_admissions,
            "expected_final_active_tokens": expected_final_tokens_total,
            "actual_final_active_tokens": actual_final_tokens_total,
            "final_token_provenance_mismatches": token_provenance_mismatches,
            "excluded_activity_admissions": {
                "history_materialization": 0,
                "neutral_contact": 0,
                "response_or_controller": 0,
                "diversion": 0,
                "state_intervention": 0,
                "private_partition": 0,
                "save_load_reset": 0,
            },
            "recursive_history_self_support": False,
        },
        "claim_projection": {
            "terminal": "supported_bounded_candidate",
            "strongest_positive_claim": "bounded history-carried P2-I2-grounded three-operation shared-pool composition candidate",
            "support_status": "scaffold_dependent",
            "state_carried": "not_supported_in_the_frozen_realization",
            "history_carried": "supported_bounded_composition",
            "hybrid": "not_supported_in_the_frozen_realization",
            "hybrid_interpretation": "carrier_operational_but_E_nonessential_at_registered_response_boundary",
            "operation_complementarity_claimed": False,
        },
        "process_counts": {
            "validator_processes_through_final_artifact": 6,
            "check_only_validator_processes": 2,
            "artifact_generation_validator_processes": 4,
            "superseded_uncommitted_audit_artifacts": 3,
            "PyGRC_imports": 0,
            "models": 0,
            "producers": 0,
            "arms": 0,
            "responses": 0,
            "retained_runtime_reads_through_final_artifact": 6,
            "retained_runtime_reads_this_start": 1,
        },
        "owner_boundary": {
            "result_acceptance_required": True,
            "result_commit_authorized": False,
            "matched_cardinality_runtime_authorized": False,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--original-reconstruction", required=True)
    parser.add_argument("--corrected", required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one validation mode")
    for value in (args.freeze, args.runtime, args.original_reconstruction, args.corrected, args.output):
        if value is not None:
            require(portable_relative(value), "absolute path refused")
    result = audit(
        ROOT / args.freeze,
        ROOT / args.runtime,
        ROOT / args.original_reconstruction,
        ROOT / args.corrected,
    )
    if args.output:
        output = ROOT / args.output
        require(not output.exists(), "audit output already exists")
        output.write_bytes(canonical_bytes(result))
        require(load_json(output) == result, "audit output readback drifted")
    print(
        json.dumps(
            {
                "status": result["status"],
                "matched_alternative": result["cardinality_quantity_boundary"]["quantity_cardinality_matched_alternative_registered"],
                "history_admissions": result["active_history_reconciliation"]["actual_physical_admission_rows"],
                "support_status": result["claim_projection"]["support_status"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
