#!/usr/bin/env python3
"""Focused zero-execution validation of P2-I2 I04-R2 machine invariants."""

from __future__ import annotations

import argparse
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
GRAPH = Path("/home/uros/Documents/RC-github/graph-reflexive-coherence")
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402
from p2_i2_i04r2_analysis import validate_machine_policy  # noqa: E402
from p2_i2_i04r2_calibration import validate_calibration_policy  # noqa: E402


EXPECTED = {
    "input": "1919cf9d99c3741363c2097a37fcfabcf0f76022e623ef9d110fa29d3a114114",
    "machine_policy": "277dfc22c9e98268e950cb634ed1174b9ad4f0f654a72984b365655815c3a9ce",
    "calibration_policy": "57dc32d02b828bb21caf069c5690bf4fcfc240848faefcd8412a6505bba849fe",
    "analysis_module": "2abc4c2040d4fff3467931feeedb0e2423a5fca71a3bc3a921aa4ca3e9b22a24",
    "calibration_entrypoint": "8a0ef5569705ea0619a628b3b5a25d9dc80448a273a68a92d131ce775793b61a",
    "test": "75de8f69c2e1433618303a8338d4899be272527c3af9b4c7c7476448f5ccfaf2",
    "preregistration": "dee89df45b4a5ece93d1d7ce461d2c0cb8f028ff44aa32b3f4e45e88a1b09e9b",
}
PATHS = {
    "input": EXPERIMENT / "contracts/p2-i2/i04r2-conditional-machine-verification-input.json",
    "machine_policy": EXPERIMENT / "configs/p2_i2_i04r2_machine_policy.json",
    "calibration_policy": EXPERIMENT / "configs/p2_i2_i04r2_calibration_policy.json",
    "analysis_module": EXPERIMENT / "scripts/p2_i2_i04r2_analysis.py",
    "calibration_entrypoint": EXPERIMENT / "scripts/p2_i2_i04r2_calibration.py",
    "test": EXPERIMENT / "implementation/tests/test_p2_i2_i04r2_analysis.py",
    "preregistration": EXPERIMENT / "contracts/p2-i2/i04r2-machine-verification-preregistration.json",
}
PARENT_ANALYSIS = EXPERIMENT / "configs/p2_i2_i04r1_analysis_policy.json"
EXPECTED_BASELINE_COMMIT = "6d0fdf8e7405b45cb509c5a0e323fa10149d2cf2"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(repository), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _result(check_id: str, name: str, condition: bool, finding: str, evidence: Any) -> dict[str, Any]:
    if not condition:
        raise AssertionError(f"{check_id} failed: {finding}")
    return {
        "check_id": check_id,
        "name": name,
        "status": "passed",
        "finding": finding,
        "evidence": evidence,
    }


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def _call_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            names.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            names.append(node.func.attr)
    return names


def _numeric_values(value: Any) -> set[int | float]:
    found: set[int | float] = set()
    if isinstance(value, bool) or value is None:
        return found
    if isinstance(value, (int, float)):
        found.add(value)
    elif isinstance(value, Mapping):
        for nested in value.values():
            found.update(_numeric_values(nested))
    elif isinstance(value, list):
        for nested in value:
            found.update(_numeric_values(nested))
    return found


def validate() -> dict[str, Any]:
    for name, path in PATHS.items():
        actual = _sha256(path)
        if actual != EXPECTED[name]:
            raise AssertionError(f"I04-R2 {name} identity drifted: {actual}")
    freeze = _load(PATHS["input"])
    machine = _load(PATHS["machine_policy"])
    calibration = _load(PATHS["calibration_policy"])
    parent_analysis = _load(PARENT_ANALYSIS)
    prereg = _load(PATHS["preregistration"])
    validate_machine_policy(machine, parent_analysis)
    validate_calibration_policy(calibration, machine, parent_analysis)
    checks: list[dict[str, Any]] = []

    checks.append(
        _result(
            "I04R2V-01",
            "frozen_identity",
            prereg["input_freeze"]["sha256"] == EXPECTED["input"]
            and prereg["machine_identity"]["policy_sha256"] == EXPECTED["machine_policy"]
            and prereg["machine_identity"]["analysis_module_sha256"]
            == EXPECTED["analysis_module"]
            and prereg["machine_identity"]["test_sha256"] == EXPECTED["test"]
            and prereg["future_calibration_identity"]["policy_sha256"]
            == EXPECTED["calibration_policy"]
            and prereg["future_calibration_identity"]["entrypoint_sha256"]
            == EXPECTED["calibration_entrypoint"],
            "Every I04-R2 input, machine, future-calibration, code, test, and preregistration identity matches.",
            EXPECTED,
        )
    )

    history = freeze["retained_I04R1_history"]
    checks.append(
        _result(
            "I04R2V-02",
            "conditional_review_and_parent_history",
            freeze["owner_review"]["sha256"]
            == "78a49384609cdc4198a2dbce359c21d03694822fb7da96d1c2ff5f3333741d5d"
            and len(history) == 10
            and all(_sha256(ROOT / row["path"]) == row["sha256"] for row in history),
            "The conditional owner review and complete I04-R1 package remain exact historical inputs.",
            {"review": freeze["owner_review"], "history_count": len(history)},
        )
    )

    evaluator = machine["complete_two_arm_evaluability"]
    analysis_source = PATHS["analysis_module"].read_text(encoding="utf-8")
    checks.append(
        _result(
            "I04R2V-03",
            "complete_two_arm_all_or_none",
            evaluator["required_scientific_records"] == 3
            and evaluator["cross_seed_order_or_mode_max_forbidden"] is True
            and "operationally invalid arm was silently removed before max" in analysis_source
            and "nonevaluable_record_ids" in analysis_source,
            "Candidate and both leave-one arms are mandatory; one invalid arm nulls comparator/margin within the exact tuple.",
            evaluator,
        )
    )

    calls = _call_names(PATHS["calibration_entrypoint"])
    calibration_source = PATHS["calibration_entrypoint"].read_text(encoding="utf-8")
    checks.append(
        _result(
            "I04R2V-04",
            "future_I05_exact_primary_estimator_route",
            calls.count("build_synthetic_response_envelope") == 3
            and "primary_margin" in calls
            and "normalized_paired_difference" not in calibration_source
            and calls.count("pretty_json_dumps") >= 2
            and "read_text" in calls
            and "loads" in calls
            and "reconstructed_serialized != retained_text" in calibration_source
            and calibration["matched_null_generator"]["precollapsed_comparator_supplied"]
            is False,
            "Future I05 builds three raw envelopes, invokes primary_margin, and byte-reconstructs retained serialization; no precollapsed/direct-margin route remains.",
            {
                "raw_builder_call_count": calls.count("build_synthetic_response_envelope"),
                "primary_margin_call_count": calls.count("primary_margin"),
                "retained_output_readback_call_count": calls.count("read_text"),
                "json_reconstruction_call_count": calls.count("loads"),
                "serialization_call_count": calls.count("pretty_json_dumps"),
                "generator_kind": calibration["matched_null_generator"]["kind"],
            },
        )
    )

    diversion = machine["I06_diversion_admissibility"]
    checks.append(
        _result(
            "I04R2V-05",
            "I06_diversion_noninterference",
            len(diversion["must_match"]) == 10
            and len(diversion["inert_sink_must_not_influence"]) == 8
            and len(diversion["required_registration_receipts"]) == 5
            and "cannot register" in diversion["failure_effect"]
            and "substitution is forbidden" in diversion["failure_effect"],
            "I06 must match all source/activity/physics/opportunity consequences and prove inert-sink noninterference or fail the mode registration.",
            diversion,
        )
    )

    source_rows = prereg["public_source_identity"]
    packet_source = Path(source_rows[0]["path"]).read_text(encoding="utf-8")
    sources_exact = all(_sha256(Path(row["path"])) == row["sha256"] for row in source_rows)
    checks.append(
        _result(
            "I04R2V-06",
            "native_arrival_identity_semantics",
            sources_exact
            and "state.nodes[packet.target_node_id].coherence = target_coherence + packet.amount"
            in packet_source
            and machine["I06_arrival_gain_admissibility"]["current_arrival_transform_id"]
            == "identity_packet_amount_addition",
            "Exact admitted source adds packet.amount to target coherence with no arrival transform; a semantic change reopens I04.",
            source_rows,
        )
    )

    arrival = machine["I06_arrival_gain_admissibility"]
    checks.append(
        _result(
            "I04R2V-07",
            "measured_gain_domain_and_adjustment_guards",
            "expected_native_arrival_gain" in analysis_source
            and "native_coherence_domain_lower" in analysis_source
            and "arrival_adjustment_event_ids" in analysis_source
            and len(arrival["forbidden_adjustment_event_kinds"]) == 5
            and "separately registered runtime_tolerance" in arrival["measured_gain_rule"],
            "Observed response must equal expected native gain within separate tolerance, stay inside the registered domain, and carry no adjustment event.",
            arrival,
        )
    )

    window = machine["window_before_scientific_zero"]
    checks.append(
        _result(
            "I04R2V-08",
            "window_validity_before_zero",
            len(window["required_receipt_fields"]) == 8
            and "step_processed_event_ids" in analysis_source
            and "window_contamination_event_ids" in analysis_source
            and window["failure_effect"].startswith("operational null"),
            "Evaluation, producer, queue, exact step-event, and contamination receipts are checked before observed response or scientific zero.",
            window,
        )
    )

    scope = machine["non_gating_scope_diagnostic"]
    parent_scope = parent_analysis["quantity_matched_scope_diagnostic"]
    checks.append(
        _result(
            "I04R2V-09",
            "quantity_matched_non_gating",
            len(scope["forbidden_effects"]) == 5
            and parent_scope["not_primary_metric"] is True
            and "equivalence alone has none" in parent_scope["R03_effect"],
            "Repeated-S1/S2 equivalence remains scope-only with no primary, top-signature, R03, or lowering effect.",
            {"overlay": scope, "parent": parent_scope},
        )
    )

    order = machine["order_conditioned_classification"]
    parent_classifier = parent_analysis["relation_classifier"]
    checks.append(
        _result(
            "I04R2V-10",
            "order_conditioned_not_failure",
            "not automatic" in order["not_top_effect"]
            and len(order["order_conditioned_inputs"]) == 5
            and "never by itself" in parent_classifier["causal_failure_separation"],
            "Not-top remains a metric disposition; raw orders, OP-08, interventions, controls, and causal validity govern history/hybrid interpretation.",
            {"overlay": order, "parent": parent_classifier},
        )
    )

    causal = machine["causal_receipt_authority"]
    parent_causal = parent_analysis["causal_chain_evidence"]
    checks.append(
        _result(
            "I04R2V-11",
            "receipt_derived_causal_status",
            len(causal["required_sources"]) == 8
            and causal["authored_summary_booleans_authoritative"] is False
            and causal["output_difference_sufficient"] is False
            and parent_causal["authored_summary_booleans_authoritative"] is False,
            "Candidate/private/controller status remains derived from retained masks, arrivals, calls, lineage, guards, configuration, and receipts.",
            causal,
        )
    )

    panels = calibration["matched_null_generator"]["panels"]
    exact_strings = [panel[order_id] for panel in panels for order_id in ("q1_then_q2", "q2_then_q1")]
    registry = _load(EXPERIMENT / "contracts/p2-i2/i03cr1-hybrid-closeout-registry.json")[
        "fixture_quarantine_registry"
    ]
    source_values: set[int | float] = set()
    source_texts: list[str] = []
    for row in registry["source_artifacts"]:
        document = _load(ROOT / row["path"])
        source_values.update(_numeric_values(document))
        source_texts.append((ROOT / row["path"]).read_text(encoding="utf-8"))
    checks.append(
        _result(
            "I04R2V-12",
            "fixture_quarantine_retained",
            len(registry["source_artifacts"]) == 7
            and not {float(Fraction(value)) for value in exact_strings} & source_values
            and all(value not in source for value in exact_strings for source in source_texts),
            "The unchanged exact-rational arithmetic panels remain absent from all seven registered I03 conformance sources.",
            {"source_count": 7, "exact_rationals": exact_strings},
        )
    )

    imports = {
        "analysis": sorted(_imported_modules(PATHS["analysis_module"])),
        "calibration": sorted(_imported_modules(PATHS["calibration_entrypoint"])),
    }
    checks.append(
        _result(
            "I04R2V-13",
            "code_and_graph_boundary",
            "pygrc" not in imports["analysis"]
            and "pygrc" not in imports["calibration"]
            and _git(ROOT, "rev-parse", "HEAD") == EXPECTED_BASELINE_COMMIT
            and _git(GRAPH, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION
            and _git(GRAPH, "status", "--short") == "",
            "I04-R2 code imports no PyGRC; accepted RCAE/graph revisions are exact and the graph checkout remains clean.",
            {"imports": imports, "graph_revision": EXPECTED_GRAPH_REVISION},
        )
    )

    test_run = subprocess.run(
        (
            str(ROOT / ".venv/bin/python"),
            "-m",
            "unittest",
            str(PATHS["test"].relative_to(ROOT)),
        ),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    test_text = test_run.stdout + test_run.stderr
    checks.append(
        _result(
            "I04R2V-14",
            "focused_pure_machine_tests",
            "Ran 7 tests" in test_text and "OK" in test_text,
            "Seven focused pure tests pass without replaying the accepted I03/I04R1 reviews.",
            {
                "command": ".venv/bin/python -m unittest "
                "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
                "implementation/tests/test_p2_i2_i04r2_analysis.py",
                "tests_run": 7,
                "status": "OK",
            },
        )
    )

    boundary = prereg["execution_boundary"]
    output_absent = not (
        EXPERIMENT / "outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json"
    ).exists()
    auth_absent = not (EXPERIMENT / "contracts/p2-i2/i05-calibration-execution-freeze.json").exists()
    checks.append(
        _result(
            "I04R2V-15",
            "zero_execution_and_I05_gate",
            output_absent
            and auth_absent
            and boundary["matched_null_invocations_in_I04R2"] == 0
            and boundary["PyGRC_model_instantiations_in_I04R2"] == 0
            and boundary["candidate_or_control_invocations_in_I04R2"] == 0
            and boundary["candidate_execution_authorized"] is False,
            "No null, model, candidate/control, authorization, output, or graph mutation occurred in I04-R2.",
            boundary,
        )
    )

    gate = prereg["gate_boundary"]
    checks.append(
        _result(
            "I04R2V-16",
            "conditional_acceptance_boundary",
            gate["owner_acceptance_required"] is True
            and gate["validation_target"] == "I04R2_acceptance_readiness"
            and len(gate["does_not_authorize"]) == 5,
            "Focused validation can establish readiness only; explicit owner acceptance is still required before CAL-PRE or I05 authorization construction.",
            gate,
        )
    )

    return {
        "artifact_id": "P2-I2-I04R2-MACHINE-VERIFICATION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I04R2",
        "lane_id": "AE01-L02",
        "validated_at": "2026-07-14",
        "status": "passed",
        "evidence_effect": "candidate_free_machine_integrity_only",
        "validated_identities": EXPECTED,
        "validator_sha256": _sha256(Path(__file__)),
        "summary": {
            "checks_passed": len(checks),
            "checks_failed": 0,
            "focused_pure_tests_passed": 7,
            "matched_null_invocations": 0,
            "PyGRC_model_instantiations": 0,
            "candidate_or_control_invocations": 0,
            "graph_mutations": 0,
            "CAL_PRE_gate_passed": False,
        },
        "checks": checks,
        "disposition": "P2-I2-I04R2-ACCEPTANCE-READY_pending_explicit_owner_acceptance",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise AssertionError("refusing to overwrite an existing validation record")
    result = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(pretty_json_dumps(result), encoding="utf-8")
    sys.stdout.write(pretty_json_dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
