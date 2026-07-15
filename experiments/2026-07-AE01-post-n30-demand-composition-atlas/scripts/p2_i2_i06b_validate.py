#!/usr/bin/env python3
"""Candidate-free validation for the P2-I2-I06B additive registration overlay."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
CONTRACTS = EXPERIMENT / "contracts" / "p2-i2"
INPUT_FREEZE = CONTRACTS / "i06b-execution-readiness-correction-input-freeze.json"
OVERLAY = CONTRACTS / "i06b-execution-readiness-overlay.json"
MANIFEST = CONTRACTS / "i06b-execution-readiness-manifest.json"
BASE_REGISTRATION = CONTRACTS / "i06-three-mode-registration.json"
VALIDATOR = EXPERIMENT / "scripts" / "p2_i2_i06b_validate.py"


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _method(tree: ast.Module, class_name: str, method_name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == method_name:
                    return child
    raise AssertionError(f"missing {class_name}.{method_name}")


def _keyword_only_names(method: ast.FunctionDef) -> list[str]:
    return [argument.arg for argument in method.args.kwonlyargs]


def _strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            yield str(key)
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _portable_json(value: Any) -> bool:
    drive = re.compile(r"^[A-Za-z]:[\\/]")
    old_graph_root = "OLD_" + "GRAPH_ROOT"
    old_rcae_root = "OLD_" + "RCAE_ROOT"
    for token in _strings(value):
        if token.startswith("/") or token.startswith("file:") or drive.match(token):
            return False
        if old_graph_root in token or old_rcae_root in token:
            return False
    return True


def _git(graph_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(graph_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _check(checks: list[dict[str, Any]], check_id: str, name: str, passed: bool, details: Any) -> None:
    checks.append({"check_id": check_id, "name": name, "passed": bool(passed), "details": details})
    _require(passed, f"{check_id} failed: {name}")


def validate(repo: Path, graph_root: Path, output: Path) -> dict[str, Any]:
    freeze = _load(repo / INPUT_FREEZE)
    overlay = _load(repo / OVERLAY)
    manifest = _load(repo / MANIFEST)
    base = _load(repo / BASE_REGISTRATION)
    checks: list[dict[str, Any]] = []

    authority = freeze["entry_authority"]
    ceiling = freeze["correction_ceiling"]
    _check(
        checks,
        "I06B-01",
        "owner authority and three-primitive ceiling",
        authority["decision_id"] == "P2-I2-DEC-043"
        and authority["change_id"] == "P2-I2-CHG-037"
        and authority["meaning"].startswith("authorize")
        and not authority["package_acceptance"]
        and not authority["commit_authorized"]
        and not authority["candidate_execution_authorized"]
        and ceiling["primitive_count"] == 3
        and len(ceiling["primitives"]) == 3
        and ceiling["accepted_I06_I06A_file_mutations"] == 0
        and not ceiling["I07_source_construction"],
        {"decision_id": authority["decision_id"], "primitive_count": ceiling["primitive_count"]},
    )

    immutable_results = []
    for item in freeze["accepted_immutable_inputs"]:
        actual = _sha256(repo / item["path"])
        immutable_results.append({"path": item["path"], "expected": item["sha256"], "actual": actual})
    _check(
        checks,
        "I06B-02",
        "accepted I06 and I06A bytes remain exact",
        all(row["expected"] == row["actual"] for row in immutable_results),
        {"files": len(immutable_results), "all_exact": all(row["expected"] == row["actual"] for row in immutable_results)},
    )

    blocked_results = []
    for item in freeze["blocked_I07_inputs"]:
        actual = _sha256(repo / item["path"])
        blocked_results.append({"path": item["path"], "expected": item["sha256"], "actual": actual})
    blocked_policy = _load(repo / freeze["blocked_I07_inputs"][1]["path"])
    _check(
        checks,
        "I06B-03",
        "blocked I07 drafts remain exact and non-authoritative",
        all(row["expected"] == row["actual"] for row in blocked_results)
        and "blocked" in str(blocked_policy.get("status", ""))
        and blocked_policy.get("candidate_execution_authorized") is not True,
        {"files": len(blocked_results), "policy_status": blocked_policy.get("status")},
    )

    source_identity = freeze["source_runtime_identity"]
    runtime_source = graph_root / "src" / "pygrc" / "models" / "lgrc_9_v3_runtime.py"
    graph_head = _git(graph_root, "rev-parse", "HEAD")
    graph_status = _git(graph_root, "status", "--porcelain")
    source_text = runtime_source.read_text(encoding="utf-8")
    tree = ast.parse(source_text)
    signatures = {
        "emit_feedback_eligibility_surface_row": _keyword_only_names(
            _method(tree, "LGRC9V3", "emit_feedback_eligibility_surface_row")
        ),
        "set_feedback_coupled_pulse_producer": _keyword_only_names(
            _method(tree, "LGRC9V3", "set_feedback_coupled_pulse_producer")
        ),
        "schedule_packet_departure": _keyword_only_names(
            _method(tree, "LGRC9V3", "schedule_packet_departure")
        ),
    }
    expected_signatures = {
        "emit_feedback_eligibility_surface_row": [
            "front_node_ids", "rear_node_ids", "reference_delta", "feedback_threshold",
            "expected_next_route_id", "expected_next_channel_id",
        ],
        "set_feedback_coupled_pulse_producer": [
            "source_node_id", "target_node_id", "edge_id", "threshold", "packet_amount",
            "expected_polarity", "expected_source_surface_digest", "expected_next_route_id",
            "expected_next_channel_id", "arrival_event_time_key", "enabled",
        ],
        "schedule_packet_departure": [
            "source_node_id", "target_node_id", "edge_id", "amount",
            "departure_event_time_key", "arrival_event_time_key", "scheduler_event_index",
            "packet_index", "source_lineage_id", "target_lineage_id",
        ],
    }
    _check(
        checks,
        "I06B-04",
        "source-current public calls and graph identity are exact without importing PyGRC",
        graph_head == source_identity["graph_revision"]
        and graph_status == ""
        and _sha256(runtime_source) == source_identity["runtime_source_sha256"]
        and signatures == expected_signatures
        and "pygrc" not in sys.modules,
        {"graph_revision": graph_head, "graph_clean": graph_status == "", "signatures": signatures, "pygrc_imported": "pygrc" in sys.modules},
    )

    manifest_entries = manifest["files"]
    manifest_results = []
    for item in manifest_entries:
        actual = _sha256(repo / item["path"])
        manifest_results.append({"path": item["path"], "expected": item["sha256"], "actual": actual})
    _check(
        checks,
        "I06B-05",
        "I06B input, overlay, and validator manifest reconstruct exactly",
        manifest["artifact_version"] == "1.0.0"
        and len(manifest_results) == 3
        and all(row["expected"] == row["actual"] for row in manifest_results),
        {"files": len(manifest_results), "all_exact": all(row["expected"] == row["actual"] for row in manifest_results)},
    )

    precedence = overlay["overlay_precedence"]
    _check(
        checks,
        "I06B-06",
        "overlay precedence is additive and exactly bounded",
        overlay["input_freeze"]["sha256"] == _sha256(repo / INPUT_FREEZE)
        and overlay["base_registration"]["sha256"] == _sha256(repo / BASE_REGISTRATION)
        and precedence["historical_I06_I06A_bytes_changed"] is False
        and precedence["historical_I06_I06A_validation_reinterpreted"] is False
        and precedence["fourth_primitive_allowed"] is False
        and precedence["future_progression_scope"] == ["P2-I2-I07", "P2-I2-I08"],
        {"superseded_fields": len(precedence["supersedes_only"]), "fourth_primitive_allowed": precedence["fourth_primitive_allowed"]},
    )

    schedule = overlay["matched_event_schedule"]
    slots = schedule["slots"]
    schedule_exact = True
    for slot in slots:
        index = slot["slot_index"]
        schedule_exact &= slot["departure_event_time_key"] == 10.25 + 1.25 * index
        schedule_exact &= slot["arrival_event_time_key"] == slot["departure_event_time_key"] + 0.625
        schedule_exact &= slot["departure_scheduler_event_index"] == 10 + 2 * index
        schedule_exact &= slot["arrival_scheduler_event_index"] == 11 + 2 * index
        schedule_exact &= slot["packet_index_if_used"] == 10 + index
    response = schedule["response"]
    schedule_exact &= [slot["slot_index"] for slot in slots] == [0, 1, 2, 3, 4]
    schedule_exact &= slots[3]["purpose"] == "native_P_intervention_or_explicit_no_op"
    schedule_exact &= slots[4]["purpose"] == "matched_neutral_contact"
    schedule_exact &= response["arrival_event_time_key"] - slots[4]["arrival_event_time_key"] == 1.0
    schedule_exact &= response["native_or_direct_address_departure_event_time_key"] == slots[4]["arrival_event_time_key"]
    schedule_exact &= response["controller_matched_departure_event_time_key"] == slots[4]["arrival_event_time_key"]
    schedule_exact &= response["feedback_surface_scheduler_event_index"] == slots[4]["arrival_scheduler_event_index"] + 1
    schedule_exact &= response["native_producer_scheduler_event_index"] == slots[4]["arrival_scheduler_event_index"] + 2
    schedule_exact &= response["packet_departure_scheduler_event_index"] == slots[4]["arrival_scheduler_event_index"] + 3
    schedule_exact &= response["packet_arrival_scheduler_event_index"] == slots[4]["arrival_scheduler_event_index"] + 4
    _check(
        checks,
        "I06B-07",
        "matched five-slot schedule and native response path are exact",
        schedule_exact and "explicit no-op" in schedule["slot_policy"],
        {"slots": len(slots), "neutral_arrival": slots[4]["arrival_event_time_key"], "response_arrival": response["arrival_event_time_key"]},
    )

    intervention = overlay["native_P_intervention"]
    amounts = {(row["mode"], row["subconfiguration_id"]): row["amount"] for row in intervention["branch_amounts"]}
    expected_amounts = {
        ("state_carried", "post_write_native_P_debit"): 0.4375,
        ("hybrid", "post_write_native_P_debit"): 0.4375,
        ("history_carried", "history_mode_P_only_debit"): 0.4375,
        ("hybrid", "hybrid_reference_P_candidate_H"): 1.5,
        ("hybrid", "hybrid_reference_components"): 1.5,
    }
    reference_identity = intervention["full_reference_P_identity"]
    _check(
        checks,
        "I06B-08",
        "diagnostic and full reference-P debit identities are exact and distinct",
        intervention["method"] == "LGRC9V3.schedule_packet_departure"
        and intervention["source_role"] == "P"
        and intervention["target_role"] == "K_P"
        and intervention["edge_role"] == "P_TO_K_P"
        and intervention["slot_index"] == 3
        and amounts == expected_amounts
        and float.hex(0.625 + 0.875) == reference_identity["amount_hex"]
        and reference_identity["candidate_P_before_debit"] - reference_identity["amount"] == reference_identity["reference_P_after_debit"]
        and reference_identity["runtime_tolerance_not_used_to_choose_amount"],
        {"branch_amounts": len(amounts), "diagnostic_amount": 0.4375, "full_reference_amount": reference_identity["amount"]},
    )

    cells = {
        sub["id"]: set(sub["modes"])
        for cell in base["cell_registry"]
        for sub in cell["subconfigurations"]
    }
    topology_roles = {row["role"] for row in base["topology"]["nodes"]}
    edge_roles = {row["edge_role"] for row in base["topology"]["edges"]}
    branch_compatibility = all(mode in cells[subconfiguration] for mode, subconfiguration in amounts)
    _check(
        checks,
        "I06B-09",
        "native intervention branch applicability and topology are registered",
        branch_compatibility
        and {"P", "K_P"}.issubset(topology_roles)
        and "P_TO_K_P" in edge_roles
        and base["pool_economy_and_capacity"]["state_carried"]["depletion"] == "explicit native P-to-K_P debit"
        and base["pool_economy_and_capacity"]["hybrid"]["depletion"] == "separate explicit P debit and H_P replacement",
        {"applicable_pairs": len(amounts), "new_topology_roles_or_edges": 0},
    )

    direct = overlay["direct_address_bypass"]
    direct_surface = direct["feedback_surface_call"]
    direct_producer = direct["native_producer_call"]
    _check(
        checks,
        "I06B-10",
        "direct-address bypass has exact contributor-addressed native calls",
        direct["subconfiguration_id"] in cells
        and cells[direct["subconfiguration_id"]] == {"state_carried", "history_carried", "hybrid"}
        and direct_surface["method"] == "LGRC9V3.emit_feedback_eligibility_surface_row"
        and direct_surface["front_node_ids"] == ["role_ids[S1]", "role_ids[S2]"]
        and direct_surface["rear_node_ids"] == ["role_ids[B_REF]"]
        and direct_surface["reference_delta"] == base["response_registration"]["reference_delta"]
        and direct_producer["method"] == "LGRC9V3.set_feedback_coupled_pulse_producer"
        and direct_producer["packet_amount"] == base["response_registration"]["response_packet_amount"]
        and direct_producer["arrival_event_time_key"] == response["arrival_event_time_key"]
        and set(direct["forbidden_reads"]) == {"P", "M_H", "active_history_carrier"}
        and "outside_candidate_chain" in direct["classification"],
        {"front_mask": direct_surface["front_node_ids"], "arrival": direct_producer["arrival_event_time_key"]},
    )

    controller = overlay["controller_assembled_bypass"]
    controller_call = controller["direct_native_packet_call_if_true"]
    output_match = controller["output_matching"]
    _check(
        checks,
        "I06B-11",
        "controller bypass is receipt-derived, carrier-blind, and output-matched",
        controller["subconfiguration_id"] in cells
        and cells[controller["subconfiguration_id"]] == {"state_carried", "history_carried", "hybrid"}
        and controller["controller_predicate"]["common_carrier_reads"] == []
        and controller["controller_predicate"]["active_history_reads"] == []
        and controller["controller_predicate"]["native_feedback_surface_reads"] == []
        and controller_call["method"] == "LGRC9V3.schedule_packet_departure"
        and controller_call["source_node_id"] == "role_ids[A_PRIMARY]"
        and controller_call["target_node_id"] == "role_ids[B]"
        and controller_call["edge_id"] == "edge_ids[A_PRIMARY_TO_B]"
        and controller_call["amount"] == output_match["candidate_response_amount"]
        and controller_call["departure_event_time_key"] == output_match["candidate_response_departure_event_time_key"]
        and controller_call["arrival_event_time_key"] == output_match["candidate_response_arrival_event_time_key"]
        and controller_call["scheduler_event_index"] == response["packet_departure_scheduler_event_index"]
        and "outside_candidate_chain" in controller["classification"],
        {"predicate": controller["controller_predicate"]["expression"], "departure": controller_call["departure_event_time_key"], "arrival": controller_call["arrival_event_time_key"]},
    )

    thresholds = {mode: row["feedback_threshold"] for mode, row in base["mode_registry"].items()}
    _check(
        checks,
        "I06B-12",
        "all three unranked modes inherit unchanged thresholds, response, cells, controls, and seeds",
        list(base["mode_registry"]) == ["state_carried", "history_carried", "hybrid"]
        and thresholds == {"state_carried": 1.625, "history_carried": 0.71875, "hybrid": 2.96875}
        and len(base["cell_registry"]) == 7
        and sum(len(cell["subconfigurations"]) for cell in base["cell_registry"]) == 26
        and len(base["lane_control_materialization"]) == 5
        and base["execution_registration"]["candidate_seeds"] == [101, 211, 307]
        and not overlay["evidence_and_gate_boundary"]["mode_selection_or_ranking"],
        {"modes": list(base["mode_registry"]), "thresholds": thresholds, "subconfigurations": 26},
    )

    bounds = overlay["bounds_and_restoration"]
    base_bounds = base["pool_economy_and_capacity"]["bounds"]
    _check(
        checks,
        "I06B-13",
        "packet/event bounds and composite restoration duties remain adequate",
        bounds["maximum_packets_in_any_branch"] <= base_bounds["max_scheduled_packets_per_branch"]
        and bounds["maximum_processed_packet_events_in_any_branch"] <= base_bounds["max_processed_packet_events_per_branch"]
        and bounds["new_topology_roles_or_edges"] == 0
        and bounds["new_restoration_components"] == 0
        and bounds["intervention_and_bypass_receipts_are_continuation_identity_inputs"]
        and not bounds["one_sided_or_implicit_rebase_allowed"],
        {"max_packets": bounds["maximum_packets_in_any_branch"], "max_events": bounds["maximum_processed_packet_events_in_any_branch"]},
    )

    validator_text = (repo / VALIDATOR).read_text(encoding="utf-8")
    machine_root_fragment = ("/" + "home" + "/")
    portability = _portable_json(freeze) and _portable_json(overlay) and _portable_json(manifest)
    portability &= machine_root_fragment not in validator_text
    portability &= "OLD_" + "GRAPH_ROOT" not in validator_text
    portability &= "OLD_" + "RCAE_ROOT" not in validator_text
    _check(
        checks,
        "I06B-14",
        "new authority artifacts and validator contain no machine-local paths",
        portability,
        {"json_artifacts": 3, "validator_scanned": True, "portable": portability},
    )

    gate = overlay["evidence_and_gate_boundary"]
    source_ast = ast.parse(validator_text)
    imported_roots = {
        alias.name.split(".")[0]
        for node in source_ast.body
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    _check(
        checks,
        "I06B-15",
        "validation is candidate-free and all progression gates remain closed",
        "pygrc" not in imported_roots
        and gate["candidate_or_control_execution"] is False
        and gate["scientific_evidence"] is False
        and gate["R01_through_R05"] == "unassigned"
        and gate["REG_GATE"].startswith("reopened_pending")
        and gate["I07"] == "paused"
        and gate["EXEC_FREEZE"] == "closed"
        and gate["I08"] == "unauthorized"
        and gate["commit_authorized"] is False,
        {"pygrc_imported": False, "REG_GATE": gate["REG_GATE"], "EXEC_FREEZE": gate["EXEC_FREEZE"], "I08": gate["I08"]},
    )

    result: dict[str, Any] = {
        "artifact_id": "P2-I2-I06B-EXECUTION-READINESS-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I06B",
        "status": "passed_candidate_free_pending_explicit_owner_review",
        "validation_summary": {
            "checks_passed": len(checks),
            "checks_total": len(checks),
            "blockers": 0,
            "accepted_input_files_reconstructed": len(immutable_results),
            "blocked_I07_files_reconstructed": len(blocked_results),
            "I06B_manifest_files_reconstructed": len(manifest_results),
        },
        "checks": checks,
        "process_accounting": {
            "output_producing_validation_starts": 1,
            "validation_start_ceiling": freeze["validation_boundary"]["output_producing_validation_start_ceiling"],
            "infrastructure_retries": 0,
            "read_only_source_control_subprocesses": 2,
            "pygrc_imports": 0,
            "models_constructed": 0,
            "packets_scheduled_or_processed": 0,
            "candidate_operations": 0,
            "control_operations": 0,
            "response_evaluations": 0,
            "comparator_or_scientific_windows": 0,
        },
        "identities": {
            "input_freeze_sha256": _sha256(repo / INPUT_FREEZE),
            "overlay_sha256": _sha256(repo / OVERLAY),
            "manifest_sha256": _sha256(repo / MANIFEST),
            "validator_sha256": _sha256(repo / VALIDATOR),
            "base_registration_sha256": _sha256(repo / BASE_REGISTRATION),
            "graph_revision": graph_head,
            "runtime_source_sha256": _sha256(runtime_source),
            "interpreter_command": ".venv/bin/python",
            "python_version": sys.version.split()[0],
        },
        "reconstruction": {
            "canonical_JSON_roundtrip": True,
            "retained_output_readback_byte_identical": True,
            "output_regeneration_count": 0,
        },
        "evidence_effect": "implementation_registration_readiness_only_no_scientific_evidence",
        "gate_effect": {
            "REG_GATE": "reopened_pending_explicit_owner_acceptance_of_I06B",
            "I07": "paused",
            "EXEC_FREEZE": "closed",
            "I08": "unauthorized",
            "commit_authorized": False,
        },
    }
    encoded = _canonical_bytes(result)
    _require(_canonical_bytes(json.loads(encoded)) == encoded, "canonical reconstruction failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded)
    _require(output.read_bytes() == encoded, "retained output readback differs")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate"])
    parser.add_argument("--graph-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    repo = _repo_root()
    graph_root = (repo / args.graph_root).resolve()
    output = repo / args.output
    result = validate(repo, graph_root, output)
    print(json.dumps(result["validation_summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
