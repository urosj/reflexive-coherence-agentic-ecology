"""Validate the candidate-free P2-I2 I04 calibration preregistration.

This validator performs static identity, semantic, quarantine, and pure unit
checks only. It never invokes the matched-null entry point, imports PyGRC, or
instantiates a candidate/runtime model.
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
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402
from p2_i2_analysis import MODES, ORDERS, validate_analysis_policy  # noqa: E402
from p2_i2_calibration import validate_calibration_policy  # noqa: E402


EXPECTED = {
    "input": "931bd8428a6e6fcda5ef97be04049f12aeb0dcbaddd331a5821562f81efdc5f4",
    "analysis_policy": "9ab75a6f1bc7beef14165978789353b69d1ed38503f7a131fe60a6452114ecd5",
    "calibration_policy": "e885837ced3b8818fe363381ec7b4d1968fcc6b0ec73946058663a787bd9424c",
    "analysis_module": "bf2674af59dbfa05074aff28b99125e9bb1c333ecd199ee3e5d9c9ebdf766428",
    "calibration_entrypoint": "05a62b434fcd54a208124feff4d8b9690fc771cd949063367a83b8db65f99a46",
    "test": "76ef526e133d9ae3a035ecca090d329eece9cd509c6d133b2134053596c63a04",
    "preregistration": "a12fc6899c45cc2568b82f6b69bc86f0df97963d2a8d636c8e65a68770ba3221",
}
EXPECTED_BASELINE_COMMIT = "6d0fdf8e7405b45cb509c5a0e323fa10149d2cf2"
EXPECTED_BASELINE_TREE = "16aef10e5329124a5155a2ae3c4cf1ea93b7469a"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"

PATHS = {
    "input": EXPERIMENT / "contracts/p2-i2/i04-choice-resolution-input.json",
    "analysis_policy": EXPERIMENT / "configs/p2_i2_analysis_policy.json",
    "calibration_policy": EXPERIMENT / "configs/p2_i2_calibration_policy.json",
    "analysis_module": EXPERIMENT / "scripts/p2_i2_analysis.py",
    "calibration_entrypoint": EXPERIMENT / "scripts/p2_i2_calibration.py",
    "test": EXPERIMENT / "implementation/tests/test_p2_i2_analysis.py",
    "preregistration": EXPERIMENT / "contracts/p2-i2/i04-calibration-preregistration.json",
}


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
            raise AssertionError(f"I04 {name} identity drifted: {actual}")

    choice = _load(PATHS["input"])
    analysis = _load(PATHS["analysis_policy"])
    calibration = _load(PATHS["calibration_policy"])
    prereg = _load(PATHS["preregistration"])
    validate_analysis_policy(analysis)
    validate_calibration_policy(calibration, analysis)

    checks: list[dict[str, Any]] = []
    checks.append(
        _result(
            "I04V-01",
            "frozen_artifact_identity",
            prereg["input_freeze"]["sha256"] == EXPECTED["input"]
            and prereg["analysis_identity"]["policy_sha256"] == EXPECTED["analysis_policy"]
            and prereg["analysis_identity"]["module_sha256"] == EXPECTED["analysis_module"]
            and prereg["calibration_identity"]["policy_sha256"] == EXPECTED["calibration_policy"]
            and prereg["calibration_identity"]["entrypoint_sha256"] == EXPECTED["calibration_entrypoint"],
            "All frozen I04 input, policy, code, test, and preregistration identities match.",
            {name: EXPECTED[name] for name in EXPECTED},
        )
    )

    authority_rows = []
    for row in choice["frozen_authorities"]:
        path = ROOT / row["path"]
        actual = _sha256(path)
        if actual != row["sha256"]:
            raise AssertionError(f"frozen authority drifted: {row['path']}")
        authority_rows.append({"path": row["path"], "sha256": actual})
    baseline_ok = (
        choice["entry_authority"]["accepted_rcae_commit"] == EXPECTED_BASELINE_COMMIT
        and choice["entry_authority"]["accepted_rcae_tree"] == EXPECTED_BASELINE_TREE
        and _git(ROOT, "rev-parse", EXPECTED_BASELINE_COMMIT) == EXPECTED_BASELINE_COMMIT
        and _git(ROOT, "rev-parse", f"{EXPECTED_BASELINE_COMMIT}^{{tree}}") == EXPECTED_BASELINE_TREE
    )
    checks.append(
        _result(
            "I04V-02",
            "accepted_authority_and_baseline",
            baseline_ok and len(authority_rows) == 10,
            "The accepted I03F baseline and all ten semantic/input authorities remain exact.",
            {"baseline_commit": EXPECTED_BASELINE_COMMIT, "authorities": authority_rows},
        )
    )

    modes_exact = (
        tuple(choice["required_modes"]) == MODES
        and tuple(analysis["required_modes"]) == MODES
        and [row["mode"] for row in prereg["mode_registry"]] == list(MODES)
        and all(row["retained"] for row in prereg["mode_registry"])
        and prereg["candidate_absence_and_execution_boundary"]["candidate_execution_authorized"] is False
    )
    checks.append(
        _result(
            "I04V-03",
            "owner_gate_and_three_mode_retention",
            modes_exact,
            "Owner acceptance opens I04 only; all three unranked modes remain present and candidate execution stays closed.",
            prereg["mode_registry"],
        )
    )

    measurement = analysis["measurement"]
    response_ok = (
        prereg["decision"]["raw_response"] == "native_B_target_coherence_gain"
        and measurement["orientation_transform"] == "identity"
        and measurement["direction"] == "higher_is_aligned"
        and measurement["window"]["producer_evaluations"] == 1
        and measurement["window"]["registered_later_opportunities_per_cell_seed_subconfiguration_order"] == 1
        and "B coherence gain is primary" in measurement["primary_field_rule"]
    )
    checks.append(
        _result(
            "I04V-04",
            "downstream_substrate_response",
            response_ok,
            "The primary field is one bounded native receiving-substrate consequence, not an intermediate score or success label.",
            measurement,
        )
    )

    pairing = analysis["primary_pairing"]
    pairing_ok = (
        pairing["comparator_subconfiguration"] == "quantity_and_timing_matched_single_source_repetition"
        and tuple(row["order_id"] for row in pairing["order_strata"]) == ORDERS
        and "do not choose a canonical order" in pairing["order_policy"]
        and prereg["aggregation_and_decision_boundary"]["primary_margin_count_per_mode"] == 6
        and prereg["aggregation_and_decision_boundary"]["primary_signature_requires_every_margin_aligned"] is True
    )
    checks.append(
        _result(
            "I04V-05",
            "closest_comparator_and_distribution",
            pairing_ok,
            "The closest repeated-single-source comparator is paired separately in both orders; six raw per-mode margins remain required.",
            pairing,
        )
    )

    aggregation = analysis["aggregation_and_missingness"]
    aggregation_ok = (
        aggregation["candidate_seeds"] == [101, 211, 307]
        and aggregation["opportunity_count_per_registered_stratum"] == 1
        and "complete two-order" in aggregation["operational_missingness_policy"]
        and "forbidden" in aggregation["scalar_collapse"]
        and analysis["paired_margin"]["retain_per_seed_margins"] is True
    )
    checks.append(
        _result(
            "I04V-06",
            "aggregation_pairing_and_missingness",
            aggregation_ok,
            "Fixed-denominator one-opportunity strata, scientific zero, operational null, full mode-seed invalidation, and raw retention are exact.",
            aggregation,
        )
    )

    equivalence = analysis["cross_mode_semantic_equivalence"]
    equivalence_ok = (
        all(
            equivalence[key] is True
            for key in ("shared_response_definition", "shared_analysis_identity", "shared_calibration_identity")
        )
        and len(equivalence["proof"]) == 7
        and "distinct mode-specific causes" in equivalence["upstream_non_equivalence_retained"]
    )
    checks.append(
        _result(
            "I04V-07",
            "shared_identity_semantic_equivalence",
            equivalence_ok,
            "Shared downstream analysis/calibration is justified across all seven required equivalence fields without merging upstream carriers.",
            equivalence,
        )
    )

    classifier = analysis["relation_classifier"]
    classifier_ok = (
        analysis["paired_margin"]["measurement_resolution"] == 1e-12
        and "both order strata" in classifier["top_primary_signature"]
        and classifier["delta_source"].endswith("pending")
        and set(classifier) >= {
            "robust_aligned",
            "narrow_aligned",
            "resolution_limited",
            "mixed_direction",
            "narrow_counter",
            "robust_counter",
            "resolution_unknown",
            "not_applicable",
        }
    )
    checks.append(
        _result(
            "I04V-08",
            "margin_and_relation_classifier",
            classifier_ok,
            "The frozen L02 denominator, unresolved I05 delta, complete relation vocabulary, and all-order top signature are coherent.",
            {"paired_margin": analysis["paired_margin"], "classifier": classifier},
        )
    )

    mode_rules = analysis["mode_control_rules"]
    logical_cells = set(analysis["terminal_input_boundary"]["required_cell_ids"])
    control_cells = {
        row["cell"] for row in analysis["common_control_rules"]
    } | {
        row["cell"] for mode in MODES for row in mode_rules[mode]
    }
    controls_ok = (
        len(analysis["common_control_rules"]) == 9
        and [len(mode_rules[mode]) for mode in MODES] == [3, 3, 5]
        and control_cells <= logical_cells
        and any(row["control_id"] == "equal_P_order_and_shuffle" for row in mode_rules["state_carried"])
        and any(row["control_id"] == "active_history_order_reversal" for row in mode_rules["history_carried"])
        and any(row["control_id"] == "complete_P_by_H_P_component_factorial" for row in mode_rules["hybrid"])
        and any(row["control_id"] == "interaction_or_synergy" and "no nonlinearity" in row["relation"] for row in mode_rules["hybrid"])
    )
    checks.append(
        _result(
            "I04V-09",
            "signed_controls_and_hybrid_factorial",
            controls_ok,
            "Every common and mode-specific qualitative expectation has a machine rule; the complete hybrid four-cell factorial is retained without a synergy requirement.",
            {
                "common": analysis["common_control_rules"],
                "mode_specific": mode_rules,
                "logical_cell_coverage": sorted(control_cells),
            },
        )
    )

    generator = calibration["matched_null_generator"]
    exact_strings = [panel[order] for panel in generator["panels"] for order in ORDERS]
    null_ok = (
        calibration["shared_across_modes"] is True
        and calibration["calibration_seeds"] == [19, 43, 71, 109, 163]
        and not set(calibration["calibration_seeds"]) & set(calibration["candidate_seeds_excluded"])
        and exact_strings == [f"{value}/23" for value in range(1, 11)]
        and calibration["delta_status"] == "pending_I05_execution"
        and all(value is False for value in calibration["I04_execution_boundary"].values())
        and calibration["authorization_requirement"]["must_be_absent_in_I04"] is True
        and "--authorization" in calibration["execution_policy"]["command"]
        and "--preregistration" in calibration["execution_policy"]["command"]
    )
    checks.append(
        _result(
            "I04V-10",
            "candidate_blind_null_preregistration",
            null_ok,
            "A shared ten-pair exact-rational null, disjoint seeds, estimator, resource envelope, command, and I04 non-execution boundary are frozen.",
            calibration,
        )
    )

    registry = _load(EXPERIMENT / "contracts/p2-i2/i03cr1-hybrid-closeout-registry.json")["fixture_quarantine_registry"]
    source_values: set[int | float] = set()
    source_leaf_strings: set[str] = set()
    source_texts: list[str] = []
    for row in registry["source_artifacts"]:
        path = ROOT / row["path"]
        document = _load(path)
        source_values.update(_numeric_values(document))
        source_leaf_strings.update(_leaf_strings(document))
        source_texts.append(path.read_text(encoding="utf-8"))
    null_values = {float(Fraction(value)) for value in exact_strings}
    branch_ids = set(registry["i03c_exact_branch_ids"])
    scientific_leaves = _leaf_strings(analysis) | _leaf_strings(calibration)
    quarantine_ok = (
        len(registry["source_artifacts"]) == 7
        and not null_values & source_values
        and all(value not in text for value in exact_strings for text in source_texts)
        and not branch_ids & scientific_leaves
        and not set(registry["i03c_hashes"]) & scientific_leaves
        and prereg["fixture_quarantine_disposition"]["scientific_contribution_topology_threshold_and_response_amounts_selected_in_I04"] is False
        and calibration["measurement_resolution"] == 1e-12
        and choice["fixture_quarantine"]["independent_prior_authority_exception"]["source"] == "AE01-L02 metric sheet"
    )
    checks.append(
        _result(
            "I04V-11",
            "complete_I03_fixture_quarantine",
            quarantine_ok,
            "All seven registered I03 sources are rejected; null values/strings, branch IDs, and conformance hashes are absent, with only the independently authoritative metric resolution retained.",
            {
                "source_count": len(registry["source_artifacts"]),
                "null_values": exact_strings,
                "numeric_intersection": sorted(null_values & source_values),
                "branch_intersection": sorted(branch_ids & scientific_leaves),
                "allowed_resolution": 1e-12,
            },
        )
    )

    imported = {
        name: sorted(_imported_modules(PATHS[name]))
        for name in ("analysis_module", "calibration_entrypoint")
    }
    source_code = PATHS["analysis_module"].read_text() + PATHS["calibration_entrypoint"].read_text()
    code_boundary_ok = (
        all("pygrc" not in modules for modules in imported.values())
        and "i03ar1" not in source_code.casefold()
        and "i03b-history" not in source_code.casefold()
        and "i03c-hybrid" not in source_code.casefold()
    )
    checks.append(
        _result(
            "I04V-12",
            "analysis_and_null_code_boundary",
            code_boundary_ok,
            "The analysis and future I05 entry point import no PyGRC and load no I03 source or candidate/runtime artifact.",
            imported,
        )
    )

    candidate_paths = []
    for pattern in ("i05*", "i06*", "i07*", "i08*"):
        candidate_paths.extend((EXPERIMENT / "contracts/p2-i2").glob(pattern))
    matched_null_output = EXPERIMENT / "outputs/p2-i2/i05/matched-null-calibration.json"
    authorization_path = ROOT / calibration["authorization_requirement"]["path"]
    absence_ok = (
        not candidate_paths
        and not matched_null_output.exists()
        and not authorization_path.exists()
        and prereg["candidate_absence_and_execution_boundary"]["matched_null_executed_in_I04"] is False
        and prereg["candidate_absence_and_execution_boundary"]["I05_calibration_execution_freeze_present_at_freeze"] is False
        and prereg["candidate_absence_and_execution_boundary"]["PyGRC_model_instantiations_in_I04"] == 0
    )
    checks.append(
        _result(
            "I04V-13",
            "candidate_calibration_and_runtime_absence",
            absence_ok,
            "No I05-I08 artifact, matched-null output, candidate outcome, or PyGRC model invocation exists in I04.",
            {
                "downstream_paths": [str(path) for path in candidate_paths],
                "matched_null_output_exists": matched_null_output.exists(),
                "I05_authorization_exists": authorization_path.exists(),
            },
        )
    )

    test_run = subprocess.run(
        (
            str(ROOT / ".venv/bin/python"),
            "-m",
            "unittest",
            "experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests/test_p2_i2_analysis.py",
        ),
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    test_ok = test_run.returncode == 0 and "Ran 10 tests" in test_run.stderr and "OK" in test_run.stderr
    checks.append(
        _result(
            "I04V-14",
            "candidate_free_analysis_unit_tests",
            test_ok,
            "Ten pure analysis tests pass without generating the registered null or executing a runtime.",
            {"command": prereg["analysis_identity"]["test_command"], "stderr": test_run.stderr.strip()},
        )
    )

    graph_repository_id = choice["entry_authority"].get(
        "graph_repository_id", "graph-reflexive-coherence"
    )
    if graph_repository_id != "graph-reflexive-coherence":
        raise AssertionError("graph repository identity drifted")
    graph_root = ROOT.parent / graph_repository_id
    graph_state = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "status": _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"),
    }
    checks.append(
        _result(
            "I04V-15",
            "graph_read_only_identity",
            graph_state == {"revision": EXPECTED_GRAPH_REVISION, "status": ""},
            "The admitted PyGRC checkout remains exact, clean, and unmodified.",
            graph_state,
        )
    )

    gate = prereg["gate_boundary"]
    gate_ok = (
        gate["validation_target"] == "P2-I2-CAL-PRE-GATE"
        and gate["owner_review_required"] is True
        and gate["on_owner_acceptance"] == "authorize I05 matched-null execution only"
        and len(gate["does_not_authorize"]) == 6
    )
    checks.append(
        _result(
            "I04V-16",
            "gate_and_change_control_boundary",
            bool(gate_ok) and len(prereg["change_control"]["requires_new_I04_and_I05_cycle"]) == 5,
            "I04 is review-ready only; owner acceptance may open I05 alone, and every scientific/analysis change restarts I04/I05.",
            {"gate": gate, "change_control": prereg["change_control"]},
        )
    )

    if len(checks) != 16:
        raise AssertionError("I04 validation check count drifted")
    return {
        "artifact_id": "P2-I2-I04-CALIBRATION-PREREGISTRATION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I04",
        "lane_id": "AE01-L02",
        "validated_at": "2026-07-14",
        "status": "passed_pending_owner_review",
        "evidence_effect": "static_candidate_free_preregistration_validation_only",
        "preregistration": {
            "path": str(PATHS["preregistration"].relative_to(ROOT)),
            "sha256": EXPECTED["preregistration"],
        },
        "validator": {
            "path": str(Path(__file__).resolve().relative_to(ROOT)),
            "sha256": _sha256(Path(__file__).resolve()),
        },
        "summary": {
            "checks_total": len(checks),
            "checks_passed": sum(row["status"] == "passed" for row in checks),
            "checks_failed": 0,
            "unit_tests_passed": 10,
            "model_instantiations": 0,
            "matched_null_invocations": 0,
            "candidate_invocations": 0,
            "graph_mutations": 0,
            "retained_modes": list(MODES),
        },
        "checks": checks,
        "gate_disposition": {
            "disposition": "P2-I2-I04-REVIEW-READY",
            "P2-I2-CAL-PRE-GATE": "pending_owner_review",
            "I05_authorized": False,
            "candidate_execution_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate()
    rendered = pretty_json_dumps(result)
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        sys.stdout.write(
            f"P2-I2 I04 validation passed: {result['summary']['checks_passed']}/{result['summary']['checks_total']} checks; 10/10 unit tests; no matched-null or candidate execution\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
