"""Focused static validation for the P2-I2 I04-R1 correction.

The validator checks only the owner-review correction surfaces.  It does not
repeat I03 mode reviews, import PyGRC, invoke the matched null, or instantiate
a candidate/control runtime.
"""

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
GRAPH_REPOSITORY_ID = "graph-reflexive-coherence"
GRAPH = ROOT.parent / GRAPH_REPOSITORY_ID
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402
from p2_i2_i04r1_analysis import (  # noqa: E402
    FORBIDDEN_RESPONSE_PHASE_CALLS,
    MODES,
    PHYSICAL_ORDERS,
    validate_analysis_policy,
)
from p2_i2_i04r1_calibration import validate_calibration_policy  # noqa: E402


EXPECTED = {
    "input": "8060d0476c02869ca5954be01b4e80ee9ca4e27f6438bbf22ea5d5a14be02c31",
    "analysis_policy": "91b8bd50633a19333935ec115bdd005697abdef5381ef59f4ceab21db08c090d",
    "calibration_policy": "5eb921eeb49c0fb336b5176a98bfd615482b991293afbd579263a5275a8717ad",
    "analysis_module": "1b4b8ccd3bea10e79ad17fdd9646d92c747ce5c3da20da96d72834ad300dbb4c",
    "calibration_entrypoint": "8228dc8a483a9c5b01cbb1c0f499797b35b8eb3bf17cf6781c112b289d8826bd",
    "test": "a96a12654f90a1837fd3f0958d4d521870bd8f30ab2f5966c1735c7fd0429b0c",
    "preregistration": "ddce7076c7170e38900197ca7bb0643d92305784daa523099041c9fc5a15d3a4",
}
EXPECTED_BASELINE_COMMIT = "6d0fdf8e7405b45cb509c5a0e323fa10149d2cf2"
EXPECTED_BASELINE_TREE = "16aef10e5329124a5155a2ae3c4cf1ea93b7469a"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
PATHS = {
    "input": EXPERIMENT / "contracts/p2-i2/i04r1-critical-review-correction-input.json",
    "analysis_policy": EXPERIMENT / "configs/p2_i2_i04r1_analysis_policy.json",
    "calibration_policy": EXPERIMENT / "configs/p2_i2_i04r1_calibration_policy.json",
    "analysis_module": EXPERIMENT / "scripts/p2_i2_i04r1_analysis.py",
    "calibration_entrypoint": EXPERIMENT / "scripts/p2_i2_i04r1_calibration.py",
    "test": EXPERIMENT / "implementation/tests/test_p2_i2_i04r1_analysis.py",
    "preregistration": EXPERIMENT / "contracts/p2-i2/i04r1-calibration-preregistration.json",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _external_source_path(row: Mapping[str, Any]) -> Path:
    if row.get("repository_id") != GRAPH_REPOSITORY_ID:
        raise AssertionError("external source repository identity drifted")
    relative = Path(str(row["path"]))
    if relative.is_absolute() or ".." in relative.parts:
        raise AssertionError("external source path is not source-relative")
    return GRAPH / relative


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


def _result(
    check_id: str,
    name: str,
    condition: bool,
    finding: str,
    evidence: Any,
) -> dict[str, Any]:
    if not condition:
        raise AssertionError(f"{check_id} failed: {finding}")
    return {
        "check_id": check_id,
        "name": name,
        "status": "passed",
        "finding": finding,
        "evidence": evidence,
    }


def _leaf_strings(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, str):
        found.add(value)
    elif isinstance(value, Mapping):
        for inner in value.values():
            found.update(_leaf_strings(inner))
    elif isinstance(value, list):
        for inner in value:
            found.update(_leaf_strings(inner))
    return found


def _numeric_values(value: Any) -> set[int | float]:
    found: set[int | float] = set()
    if isinstance(value, bool) or value is None:
        return found
    if isinstance(value, (int, float)):
        found.add(value)
    elif isinstance(value, Mapping):
        for inner in value.values():
            found.update(_numeric_values(inner))
    elif isinstance(value, list):
        for inner in value:
            found.update(_numeric_values(inner))
    return found


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def validate() -> dict[str, Any]:
    for name, path in PATHS.items():
        actual = _sha256(path)
        if actual != EXPECTED[name]:
            raise AssertionError(f"I04-R1 {name} identity drifted: {actual}")

    correction = _load(PATHS["input"])
    analysis = _load(PATHS["analysis_policy"])
    calibration = _load(PATHS["calibration_policy"])
    prereg = _load(PATHS["preregistration"])
    validate_analysis_policy(analysis)
    validate_calibration_policy(calibration, analysis)
    checks: list[dict[str, Any]] = []

    checks.append(
        _result(
            "I04R1V-01",
            "corrected_artifact_identity",
            prereg["correction_input_freeze"]["sha256"] == EXPECTED["input"]
            and prereg["analysis_identity"]["policy_sha256"] == EXPECTED["analysis_policy"]
            and prereg["analysis_identity"]["module_sha256"] == EXPECTED["analysis_module"]
            and prereg["analysis_identity"]["test_sha256"] == EXPECTED["test"]
            and prereg["calibration_identity"]["policy_sha256"]
            == EXPECTED["calibration_policy"]
            and prereg["calibration_identity"]["entrypoint_sha256"]
            == EXPECTED["calibration_entrypoint"],
            "Every corrected freeze, policy, code, test, and preregistration identity matches.",
            EXPECTED,
        )
    )

    historical_rows = correction["retained_I04_history"]
    historical_exact = all(_sha256(ROOT / row["path"]) == row["sha256"] for row in historical_rows)
    checks.append(
        _result(
            "I04R1V-02",
            "historical_I04_retention",
            len(historical_rows) == 10
            and historical_exact
            and prereg["historical_I04_disposition"]["status"]
            == "retained_historical_but_superseded_for_progression",
            "The original ten-artifact I04 package remains byte-exact history and cannot govern progression.",
            historical_rows,
        )
    )

    baseline_ok = (
        _git(ROOT, "rev-parse", "HEAD") == EXPECTED_BASELINE_COMMIT
        and _git(ROOT, "rev-parse", "HEAD^{tree}") == EXPECTED_BASELINE_TREE
        and _git(GRAPH, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION
        and _git(GRAPH, "status", "--short") == ""
    )
    modes_ok = (
        tuple(analysis["required_modes"]) == MODES
        and [row["mode"] for row in prereg["mode_registry"]] == list(MODES)
        and all(row["retained"] for row in prereg["mode_registry"])
    )
    checks.append(
        _result(
            "I04R1V-03",
            "accepted_baseline_and_three_modes",
            baseline_ok and modes_ok,
            "The accepted RCAE/PyGRC baselines are exact and all three unranked modes remain retained.",
            {
                "rcae_commit": EXPECTED_BASELINE_COMMIT,
                "rcae_tree": EXPECTED_BASELINE_TREE,
                "graph_revision": EXPECTED_GRAPH_REVISION,
                "modes": list(MODES),
            },
        )
    )

    pairing = analysis["primary_pairing"]
    checks.append(
        _result(
            "I04R1V-04",
            "carrier_changing_symmetric_primary",
            pairing["comparator_id"]
            == "strongest_symmetric_leave_one_common_carrier_admission"
            and [row["branch_id"] for row in pairing["leave_one_branches"]]
            == ["q1_admitted_q2_diverted", "q2_admitted_q1_diverted"]
            and pairing["derived_comparator"].startswith("maximum oriented response")
            and "not selected from observed effect size" in pairing["reason"],
            "The primary contrast changes the carrier, retains both symmetric leave-one arms, and uses a frozen strongest-marginal rule.",
            pairing,
        )
    )

    diagnostic = analysis["quantity_matched_scope_diagnostic"]
    checks.append(
        _result(
            "I04R1V-05",
            "symmetric_nonfailing_scope_diagnostic",
            diagnostic["repeating_sources"] == ["S1", "S2"]
            and tuple(diagnostic["physical_order_strata"]) == PHYSICAL_ORDERS
            and diagnostic["not_primary_metric"] is True
            and diagnostic["equivalence_relation"].startswith("allowed")
            and "equivalence alone has none" in diagnostic["R03_effect"],
            "Repeated-S1 and repeated-S2 remain physical-order-indexed scope diagnostics; equivalence cannot fail R03.",
            diagnostic,
        )
    )

    classifier = analysis["relation_classifier"]
    checks.append(
        _result(
            "I04R1V-06",
            "order_conditioned_metric_separation",
            classifier["top_aligned_signature"] == "both per-order panels are robust_aligned"
            and "OP-08 passes" in classifier["order_conditioned_or_mixed"]
            and "never by itself" in classifier["causal_failure_separation"],
            "A nonaligned history/hybrid order can retain an order-conditioned or mixed metric relation without automatic causal failure.",
            classifier,
        )
    )

    checks.append(
        _result(
            "I04R1V-07",
            "analysis_only_null_scope",
            calibration["delta_field"] == "analysis_arithmetic_delta"
            and len(calibration["calibrates"]) == 4
            and len(calibration["does_not_calibrate"]) == 6
            and calibration["runtime_execution"] is False
            and calibration["pygrc_imported"] is False,
            "The future I05 null calibrates only pure analysis arithmetic/serialization and explicitly excludes runtime/measurement tolerance.",
            {
                "calibrates": calibration["calibrates"],
                "does_not_calibrate": calibration["does_not_calibrate"],
            },
        )
    )

    numeric = analysis["I06_numeric_admissibility"]
    checks.append(
        _result(
            "I04R1V-08",
            "I06_numeric_domain",
            numeric["raw_floor"] == 1e-12
            and numeric["binary_safety_factor"] == 1024
            and "ulp(B_before)" in numeric["packet_amount_rule"]
            and "less than r/1024" in numeric["runtime_tolerance_rule"],
            "I06 must reject response configurations outside the floor/ULP/roundtrip/separate-tolerance domain.",
            numeric,
        )
    )

    window = analysis["measurement"]["window_protocol"]
    public_sources_exact = all(
        _sha256(_external_source_path(row)) == row["sha256"]
        for row in correction["public_source_semantics"]
    )
    checks.append(
        _result(
            "I04R1V-09",
            "outcome_independent_native_window",
            public_sources_exact
            and len(window["operation_slots"]) == 6
            and window["feedback_surface_calls"] == 1
            and window["producer_calls"] == 1
            and window["step_calls"] == 2
            and tuple(window["scheduled_step_kinds"]) == ("packet_departure", "packet_arrival")
            and tuple(window["unscheduled_or_native_block_step_kinds"])
            == ("event_queue_empty", "event_queue_empty")
            and window["outcome_independent_endpoint"] is True,
            "Exact admitted public-source semantics support one producer evaluation plus two fixed steps for every outcome.",
            {
                "window": window,
                "public_sources": correction["public_source_semantics"],
            },
        )
    )

    measurement = analysis["measurement"]
    checks.append(
        _result(
            "I04R1V-10",
            "B_purity_and_binary_response",
            len(measurement["purity_preconditions"]) == 5
            and len(measurement["purity_postconditions"]) == 4
            and measurement["scientific_no_response_value"] == 0.0
            and measurement["value_semantics"].startswith("0 or one fixed")
            and "reopens I04/I05" in measurement["purity_failure"],
            "B gain is a binary-like response occurrence measure and can register only when the response arrival is B's sole possible change.",
            measurement,
        )
    )

    isolation = analysis["mode_isolation"]
    checks.append(
        _result(
            "I04R1V-11",
            "per_mode_evidence_isolation",
            isolation["cross_mode_pooling_averaging_compensation_or_drop"] is False
            and isolation["analysis_entrypoint_accepts_exactly_one_mode"] is True
            and prereg["aggregation_and_decision_boundary"][
                "cross_mode_pooling_averaging_compensation_or_drop"
            ]
            is False,
            "Shared extraction identity does not pool, average, compensate, drop, or jointly verdict the three modes.",
            isolation,
        )
    )

    causal = analysis["causal_chain_evidence"]
    analysis_source = PATHS["analysis_module"].read_text(encoding="utf-8")
    checks.append(
        _result(
            "I04R1V-12",
            "evidence_derived_causal_controls",
            causal["authored_summary_booleans_authoritative"] is False
            and tuple(causal["forbidden_response_phase_calls"])
            == FORBIDDEN_RESPONSE_PHASE_CALLS
            and "derive_causal_chain_status" in analysis_source
            and '"used_common_pool"' not in analysis_source
            and '"controller_bypass"' not in analysis_source,
            "Candidate/private/controller status is derived from masks, arrivals, calls, packet lineage, configuration, and receipts—not authored success booleans or output inequality.",
            causal,
        )
    )

    common_rules = analysis["common_control_rules"]
    mode_rules = analysis["mode_control_rules"]
    checks.append(
        _result(
            "I04R1V-13",
            "complete_machine_control_registry",
            len(common_rules) == 9
            and [len(mode_rules[mode]) for mode in MODES] == [3, 3, 5]
            and any(
                row["control_id"] == "symmetric_leave_one_common_carrier_admission"
                and row["rule"] == "primary_relation"
                for row in common_rules
            )
            and any(
                row["control_id"] == "quantity_matched_single_source_repetition"
                and row["rule"] == "scope_diagnostic"
                for row in common_rules
            )
            and any(
                row["control_id"] == "interaction_or_synergy"
                and "no nonlinearity" in row["relation"]
                for row in mode_rules["hybrid"]
            ),
            "All nine common and 3/3/5 mode-specific controls retain exact machine rules; the two corrected common roles changed without losing any imported control.",
            {"common": common_rules, "mode_specific": mode_rules},
        )
    )

    authority_exact = all(
        _sha256(ROOT / row["path"]) == row["sha256"]
        for row in prereg["choice_rationale_quarantine"]["authorities"]
    )
    rationale = correction["quarantine"]["rationale_reconstruction"]
    checks.append(
        _result(
            "I04R1V-14",
            "pre_runtime_choice_rationale",
            authority_exact
            and prereg["choice_rationale_quarantine"]["rationale_reconstructs_without_conformance"]
            is True
            and set(rationale)
            == {"B_response", "fixed_window", "primary_comparator", "physical_orders", "control_derivation"},
            "Every corrected choice reconstructs from accepted theory, pre-runtime causal contracts, and admitted public-source semantics.",
            rationale,
        )
    )

    registry = _load(EXPERIMENT / "contracts/p2-i2/i03cr1-hybrid-closeout-registry.json")[
        "fixture_quarantine_registry"
    ]
    source_values: set[int | float] = set()
    source_texts: list[str] = []
    for row in registry["source_artifacts"]:
        path = ROOT / row["path"]
        document = _load(path)
        source_values.update(_numeric_values(document))
        source_texts.append(path.read_text(encoding="utf-8"))
    exact_strings = [
        panel[order]
        for panel in calibration["matched_null_generator"]["panels"]
        for order in PHYSICAL_ORDERS
    ]
    null_values = {float(Fraction(value)) for value in exact_strings}
    scientific_leaves = _leaf_strings(analysis) | _leaf_strings(calibration)
    quarantine_ok = (
        len(registry["source_artifacts"]) == 7
        and not null_values & source_values
        and all(value not in text for value in exact_strings for text in source_texts)
        and not set(registry["i03c_exact_branch_ids"]) & scientific_leaves
        and not set(registry["i03c_hashes"]) & scientific_leaves
    )
    checks.append(
        _result(
            "I04R1V-15",
            "I03_fixture_quarantine",
            quarantine_ok,
            "All seven registered I03 sources reject exact null values, branch identities, conformance hashes, and observed outcomes as I04-R1 inputs.",
            {"source_count": 7, "null_exact_rationals": exact_strings},
        )
    )

    module_imports = _imported_modules(PATHS["analysis_module"])
    calibration_imports = _imported_modules(PATHS["calibration_entrypoint"])
    code_text = analysis_source + PATHS["calibration_entrypoint"].read_text(encoding="utf-8")
    checks.append(
        _result(
            "I04R1V-16",
            "candidate_and_runtime_code_exclusion",
            "pygrc" not in module_imports
            and "pygrc" not in calibration_imports
            and "LGRC9V3(" not in code_text
            and "build_calibration_record(" in code_text,
            "Corrected code has no PyGRC import/model and only defines—not invokes during validation—the future governed null builder.",
            {"analysis_imports": sorted(module_imports), "calibration_imports": sorted(calibration_imports)},
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
            "I04R1V-17",
            "focused_pure_analysis_tests",
            "Ran 15 tests" in test_text and "OK" in test_text,
            "Fifteen candidate-free unit tests pass across comparator, diagnostic, window, isolation, control-rule, numeric-domain, and causal-chain corrections.",
            test_text.strip(),
        )
    )

    boundary = prereg["candidate_absence_and_execution_boundary"]
    output_absent = not (
        EXPERIMENT / "outputs/p2-i2/i05/matched-null-analysis-arithmetic-calibration.json"
    ).exists()
    auth_absent = not (
        EXPERIMENT / "contracts/p2-i2/i05-calibration-execution-freeze.json"
    ).exists()
    checks.append(
        _result(
            "I04R1V-18",
            "zero_execution_and_mechanical_I05_gate",
            output_absent
            and auth_absent
            and boundary["matched_null_invocations_in_I04R1"] == 0
            and boundary["candidate_or_control_invocations_in_I04R1"] == 0
            and boundary["PyGRC_model_instantiations_in_I04R1"] == 0
            and boundary["candidate_execution_authorized"] is False
            and calibration["authorization_requirement"]["required_CAL_PRE_gate"]
            == "passed_after_owner_acceptance_of_I04R1",
            "No null/runtime/candidate artifact exists; the future entry point remains mechanically closed until owner-accepted I04-R1 authority.",
            boundary,
        )
    )

    gate = prereg["gate_boundary"]
    checks.append(
        _result(
            "I04R1V-19",
            "review_ready_gate_boundary",
            gate["validation_target"] == "P2-I2-CAL-PRE-GATE"
            and gate["owner_review_required"] is True
            and len(gate["does_not_authorize"]) == 6
            and prereg["aggregation_and_decision_boundary"]["terminal_classification_deferred"]
            is True,
            "Validation can return only a corrected review-ready package; CAL-PRE, I05, registration, candidate execution, and scientific interpretation remain owner-gated.",
            gate,
        )
    )

    return {
        "artifact_id": "P2-I2-I04R1-CALIBRATION-PREREGISTRATION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I04R1",
        "lane_id": "AE01-L02",
        "validated_at": "2026-07-14",
        "status": "passed",
        "evidence_effect": "candidate_free_correction_integrity_only",
        "validated_identities": EXPECTED,
        "validator_sha256": _sha256(Path(__file__)),
        "summary": {
            "checks_passed": len(checks),
            "checks_failed": 0,
            "pure_tests_passed": 15,
            "PyGRC_model_instantiations": 0,
            "matched_null_invocations": 0,
            "candidate_or_control_invocations": 0,
            "graph_mutations": 0,
            "owner_gate_passed": False,
        },
        "checks": checks,
        "disposition": "P2-I2-I04-REVIEW-READY_pending_owner_acceptance",
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
