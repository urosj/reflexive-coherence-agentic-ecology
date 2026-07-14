"""Validate P2-I2 I05J arithmetic-resolution and metric-sheet closeout."""

from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
from importlib import metadata
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import (  # noqa: E402
    freeze_metric_resolution,
    load_json,
    pretty_json_dumps,
    validate_record,
)


POLICY = EXPERIMENT / "configs/p2_i2_i05j_metric_closeout_policy.json"
FREEZE = EXPERIMENT / "contracts/p2-i2/i05j-metric-closeout-input-freeze.json"
CORRECTION_FREEZE = (
    EXPERIMENT
    / "contracts/p2-i2/i05ja-native-dependency-correction-freeze.json"
)
DEPENDENCY_FAILURE = (
    EXPERIMENT / "contracts/p2-i2/i05ja-native-dependency-failure.json"
)
PROJECTION = EXPERIMENT / "contracts/p2-i2/i05j-analysis-arithmetic-resolution-input.json"
BASE_SHEET = EXPERIMENT / "contracts/metric-sheets/AE01-L02.json"
GOVERNED_OUTPUT = (
    EXPERIMENT
    / "outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json"
)
FINAL_RECEIPT = EXPERIMENT / "outputs/p2-i2/i05/i05b-final-receipt.json"
I05E_LINEAGE = EXPERIMENT / "contracts/p2-i2/i05e-portable-projection-lineage.json"
I05I_VALIDATION = EXPERIMENT / "contracts/p2-i2/i05i-portability-correction-validation.json"
CALIBRATION = EXPERIMENT / "contracts/p2-i2/metric-calibration.json"
FROZEN_SHEET = EXPERIMENT / "contracts/p2-i2/frozen-metric-sheet.json"
SCHEMA = EXPERIMENT / "contracts/schemas/ae01-contract.schema.json"
REPORT = EXPERIMENT / "reports/P2-I2-I05J-metric-closeout.md"
PARENT_COMMIT = "b5d0acbac6de34b0cbd40b3d16a05f6356d5b709"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_object(path: Path) -> dict[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise AssertionError(f"expected object: {path.relative_to(ROOT).as_posix()}")
    return value


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _check(
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
        "evidence": evidence,
        "finding": finding,
        "name": name,
        "status": "passed",
    }


def _diff_paths(left: Any, right: Any, prefix: tuple[str, ...] = ()) -> set[str]:
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        differences: set[str] = set()
        for key in set(left) | set(right):
            if key not in left or key not in right:
                differences.add("/".join((*prefix, str(key))))
            else:
                differences |= _diff_paths(left[key], right[key], (*prefix, str(key)))
        return differences
    if isinstance(left, list) and isinstance(right, list):
        differences = set()
        if len(left) != len(right):
            differences.add("/".join((*prefix, "length")))
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences |= _diff_paths(
                left_item,
                right_item,
                (*prefix, str(index)),
            )
        return differences
    return set() if left == right else {"/".join(prefix)}


def _expected_seed_margins(
    governed: Mapping[str, Any],
    base_sheet: Mapping[str, Any],
    required_orders: set[str],
) -> tuple[list[dict[str, int | float]], dict[int, list[dict[str, Any]]]]:
    rows = governed["per_seed_order_three_arm_margins"]
    by_seed: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_seed[int(row["seed"])].append(row)
    seed_profile = base_sheet["record"]["resolution_policy"][
        "calibration_seed_profile"
    ]
    if set(by_seed) != set(seed_profile):
        raise AssertionError("governed seed profile differs from base metric sheet")
    expected: list[dict[str, int | float]] = []
    for seed in seed_profile:
        seed_rows = by_seed[seed]
        if len(seed_rows) != 2:
            raise AssertionError(f"expected two physical-order rows for seed {seed}")
        if {row["physical_order_id"] for row in seed_rows} != required_orders:
            raise AssertionError(f"physical-order coverage differs for seed {seed}")
        margins = [float(row["normalized_margin"]) for row in seed_rows]
        if not all(math.isfinite(value) for value in margins):
            raise AssertionError(f"non-finite governed margin for seed {seed}")
        expected.append(
            {
                "matched_null_margin": max(abs(value) for value in margins),
                "seed": seed,
            }
        )
    return expected, by_seed


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load_object(POLICY)
    freeze = _load_object(FREEZE)
    correction_freeze = _load_object(CORRECTION_FREEZE)
    dependency_failure = _load_object(DEPENDENCY_FAILURE)
    projection = _load_object(PROJECTION)
    base_sheet = _load_object(BASE_SHEET)
    governed = _load_object(GOVERNED_OUTPUT)
    final_receipt = _load_object(FINAL_RECEIPT)
    lineage = _load_object(I05E_LINEAGE)
    i05i_validation = _load_object(I05I_VALIDATION)
    calibration = _load_object(CALIBRATION)
    frozen_sheet = _load_object(FROZEN_SHEET)
    schema = _load_object(SCHEMA)

    if Path(sys.executable).resolve() != (ROOT / ".venv/bin/python").resolve():
        raise AssertionError("I05J validator must run through repository .venv")

    frozen_paths = {
        item["path"]: item["sha256"] for item in policy["frozen_inputs"]
    }
    current_frozen_hashes = {
        relative: _sha256(ROOT / relative) for relative in frozen_paths
    }
    checks.append(
        _check(
            "I05J-01",
            "committed authority and frozen identities",
            _git("rev-parse", "HEAD") == PARENT_COMMIT
            and policy["authority"]["parent_commit"] == PARENT_COMMIT
            and freeze["authority"]["parent_commit"] == PARENT_COMMIT
            and correction_freeze["authority"]["parent_commit"] == PARENT_COMMIT
            and _sha256(POLICY) == freeze["policy_sha256"]
            and _sha256(PROJECTION)
            == freeze["calibration_input_projection"]["sha256"]
            and current_frozen_hashes == frozen_paths,
            "I05J binds the committed I05I parent and every accepted input/tool byte",
            {
                "frozen_input_count": len(frozen_paths),
                "parent_commit": PARENT_COMMIT,
                "policy_sha256": _sha256(POLICY),
            },
        )
    )

    correction_identities = correction_freeze["frozen_pre_correction_identities"]
    failure_counts = dependency_failure["process_counts"]
    checks.append(
        _check(
            "I05JA-01",
            "failed-start and exact dependency correction authority",
            correction_identities["original_I05J_freeze_sha256"]
            == _sha256(FREEZE)
            and correction_identities["failure_record_sha256"]
            == _sha256(DEPENDENCY_FAILURE)
            and correction_identities["policy_sha256"] == _sha256(POLICY)
            and dependency_failure["attempt"]["failed_closed_pre_output"] is True
            and dependency_failure["outputs"]["metric_calibration_exists"] is False
            and dependency_failure["outputs"]["frozen_metric_sheet_exists"] is False
            and failure_counts["native_freeze_resolution_entrypoint_starts"] == 1
            and metadata.version("jsonschema") == "4.26.0",
            "I05JA preserves the failed first start and installs only the pinned native dependency",
            {
                "correction_freeze_sha256": _sha256(CORRECTION_FREEZE),
                "failed_closed_pre_output_starts": 1,
                "installed_jsonschema_version": metadata.version("jsonschema"),
            },
        )
    )

    resolution = base_sheet["record"]["resolution_policy"]
    checks.append(
        _check(
            "I05J-02",
            "unchanged pending base metric sheet",
            base_sheet["record_type"] == "metric_sheet"
            and base_sheet["record"]["lane_id"] == "AE01-L02"
            and base_sheet["record"]["metric_sheet_id"]
            == "ae01-l02-primary-metric-v1"
            and resolution["status"] == "pending_candidate_blind_calibration"
            and resolution["delta"]["status"] == "pending"
            and resolution["measurement_resolution"] == 1e-12,
            "the base AE01-L02 sheet remains pending and byte-identical",
            {"base_metric_sheet_sha256": _sha256(BASE_SHEET)},
        )
    )

    output_projection = next(
        row
        for row in lineage["projections"]
        if row["path"] == GOVERNED_OUTPUT.relative_to(ROOT).as_posix()
    )
    immutable = lineage["immutable_execution_facts"]
    checks.append(
        _check(
            "I05J-03",
            "consumed one-shot and portable output authority",
            output_projection["current_sha256"] == _sha256(GOVERNED_OUTPUT)
            and immutable["analysis_arithmetic_delta"] == 1e-12
            and immutable["governed_attempt_count"] == 1
            and immutable["null_invocation_count"] == 1
            and immutable["infrastructure_retries"] == 0
            and immutable["second_invocation_refused"] is True
            and final_receipt["authorization_consumed"] is True
            and final_receipt["builder_invocation_count"] == 1
            and i05i_validation["result_status"]
            == "P2-I2-I05I-TERMINAL-GROUP-REVIEW-READY"
            and i05i_validation["complete_current_scope_violation_count"] == 0,
            "retained portable evidence authorizes closeout without another null invocation",
            {
                "builder_invocation_count": 1,
                "governed_attempt_count": 1,
                "infrastructure_retries": 0,
                "second_invocation_refused": True,
            },
        )
    )

    required_orders = set(
        policy["calibration_input_projection"]["required_physical_orders"]
    )
    expected_margins, by_seed = _expected_seed_margins(
        governed,
        base_sheet,
        required_orders,
    )
    checks.append(
        _check(
            "I05J-04",
            "exact ten-row to five-seed projection",
            len(governed["per_seed_order_three_arm_margins"]) == 10
            and len(by_seed) == 5
            and projection["candidate_blind"] is True
            and projection["seed_margins"] == expected_margins
            and projection["derivation"]["source_sha256"]
            == _sha256(GOVERNED_OUTPUT),
            "both required physical orders project to one maximum-absolute envelope per seed",
            {
                "projected_seed_count": len(expected_margins),
                "required_orders": sorted(required_orders),
                "source_row_count": 10,
            },
        )
    )

    all_margins = [
        abs(float(row["normalized_margin"]))
        for row in governed["per_seed_order_three_arm_margins"]
    ]
    seed_envelopes = [
        abs(float(row["matched_null_margin"])) for row in expected_margins
    ]
    floor = float(governed["analysis_arithmetic_floor"])
    raw_delta = max([floor, *all_margins])
    projected_delta = max([resolution["measurement_resolution"], *seed_envelopes])
    checks.append(
        _check(
            "I05J-05",
            "registered estimator preservation",
            max(all_margins) == max(seed_envelopes) == 0.0
            and raw_delta == projected_delta == 1e-12
            and governed["analysis_arithmetic_delta"] == projected_delta,
            "the seed-envelope projection preserves the complete registered maximum exactly",
            {
                "analysis_arithmetic_delta": projected_delta,
                "maximum_absolute_matched_null_margin": max(all_margins),
            },
        )
    )

    expected_calibration, expected_frozen_sheet = freeze_metric_resolution(
        deepcopy(base_sheet),
        projection,
    )
    checks.append(
        _check(
            "I05J-06",
            "byte-exact native generation reconstruction",
            calibration == expected_calibration
            and frozen_sheet == expected_frozen_sheet
            and CALIBRATION.read_text(encoding="utf-8")
            == pretty_json_dumps(expected_calibration)
            and FROZEN_SHEET.read_text(encoding="utf-8")
            == pretty_json_dumps(expected_frozen_sheet),
            "both retained artifacts reconstruct exactly through the native freeze implementation",
            {
                "frozen_metric_sheet_sha256": _sha256(FROZEN_SHEET),
                "metric_calibration_sha256": _sha256(CALIBRATION),
            },
        )
    )

    validate_record(calibration, schema)
    validate_record(frozen_sheet, schema)
    allowed_changes = {
        "record/resolution_policy/delta/calibration_artifact_ref",
        "record/resolution_policy/delta/rationale",
        "record/resolution_policy/delta/status",
        "record/resolution_policy/delta/value",
        "record/resolution_policy/status",
    }
    actual_changes = _diff_paths(base_sheet, frozen_sheet)
    checks.append(
        _check(
            "I05J-07",
            "schema and designated-field boundary",
            actual_changes == allowed_changes
            and frozen_sheet["record"]["resolution_policy"]["status"] == "frozen"
            and frozen_sheet["record"]["resolution_policy"]["delta"]["value"]
            == 1e-12
            and calibration["record"]["metric_sheet_ref"]
            == base_sheet["record"]["metric_sheet_id"]
            and calibration["record"]["delta"] == 1e-12,
            "native outputs are schema-valid and only the five designated resolution paths changed",
            {"changed_paths": sorted(actual_changes)},
        )
    )

    report_text = REPORT.read_text(encoding="utf-8")
    checks.append(
        _check(
            "I05J-08",
            "resolution-only interpretation boundary",
            calibration["record"]["evidence_effect"]
            == "resolution_only_no_candidate_evidence"
            and governed["runtime_tolerance_authority"] == "none"
            and "Narrow and robust are future relations to the frozen resolution" in report_text
            and "not a runtime or measurement tolerance" in report_text
            and "not a terminal scientific verdict" in report_text,
            "narrow/robust language remains relational and calibration assigns no scientific verdict",
            {
                "candidate_evidence_effect": "none",
                "runtime_tolerance_authority": "none",
                "scientific_result": False,
            },
        )
    )

    checks.append(
        _check(
            "I05J-09",
            "candidate and runtime quarantine",
            governed["candidate_blind"] is True
            and governed["candidate_evidence_effect"] == "none"
            and governed["runtime_execution"] is False
            and governed["pygrc_imported"] is False
            and set(governed["per_seed_order_three_arm_margins"]
                    [index]["seed"]
                    for index in range(10)).isdisjoint({101, 211, 307})
            and policy["gate_effect"]["CAL_GATE_passed"] is False
            and policy["gate_effect"]["I06_opened"] is False,
            "metric closeout consumes no candidate/runtime evidence and opens no later gate",
            {
                "CAL_GATE_passed": False,
                "I06_opened": False,
                "pygrc_imports_or_model_instantiations": 0,
            },
        )
    )

    ceiling = policy["invocation_ceiling_after_freeze"]
    corrected_ceiling = correction_freeze["invocation_ceiling_after_correction"]
    checks.append(
        _check(
            "I05J-10",
            "bounded invocation and review stop",
            ceiling == freeze["invocation_ceiling_after_freeze"]
            and ceiling["native_freeze_resolution_entrypoint_starts"] == 1
            and ceiling["I05J_validator_entrypoint_starts"] == 2
            and corrected_ceiling["native_freeze_resolution_entrypoint_starts_total"]
            == 2
            and corrected_ceiling["native_retry_starts"] == 1
            and corrected_ceiling["dependency_install_starts"] == 1
            and corrected_ceiling["I05J_validator_entrypoint_starts"] == 2
            and ceiling["null_builder_or_wrapper_invocations"] == 0
            and ceiling["other_python_process_starts"] == 0
            and ceiling["pygrc_imports_or_model_instantiations"] == 0
            and freeze["later_iteration_authorized"] is False
            and freeze["scientific_change_authorized"] is False,
            "I05J/I05JA retain one failed start, one native generation, and static reconstruction before owner review",
            {
                "failed_closed_pre_output_starts": 1,
                "native_freeze_resolution_entrypoint_starts": 2,
                "native_successful_generation_starts": 1,
                "null_builder_or_wrapper_invocations": 0,
                "owner_review_required": True,
                "validator_entrypoint_starts": 2,
            },
        )
    )

    return {
        "activity_id": policy["activity_id"],
        "analysis_arithmetic_delta": calibration["record"]["delta"],
        "artifact_id": "P2-I2-I05J-METRIC-CLOSEOUT-VALIDATION",
        "artifact_version": "1.0.0",
        "base_metric_sheet_sha256": _sha256(BASE_SHEET),
        "candidate_or_control_invocations": 0,
        "checks": checks,
        "conformance_or_scientific_invocations": 0,
        "frozen_metric_sheet_sha256": _sha256(FROZEN_SHEET),
        "I05JA_correction_freeze_sha256": _sha256(CORRECTION_FREEZE),
        "I05JA_dependency_failure_sha256": _sha256(DEPENDENCY_FAILURE),
        "installed_jsonschema_version": metadata.version("jsonschema"),
        "interpreter_identity": ".venv/bin/python",
        "iteration_id": "P2-I2-I05J",
        "lane_id": "AE01-L02",
        "metric_calibration_sha256": _sha256(CALIBRATION),
        "failed_closed_pre_output_starts": 1,
        "failed_closed_validator_starts": 1,
        "native_freeze_resolution_entrypoint_starts": 2,
        "native_successful_generation_starts": 1,
        "null_builder_or_wrapper_invocations": 0,
        "other_python_process_starts": 0,
        "passed_checks": len(checks),
        "policy_sha256": _sha256(POLICY),
        "projection_sha256": _sha256(PROJECTION),
        "pygrc_imports_or_model_instantiations": 0,
        "result_status": "P2-I2-I05J-METRIC-CLOSEOUT-REVIEW-READY",
        "scientific_result": False,
        "total_checks": len(checks),
        "validator": {
            "path": Path(__file__).relative_to(ROOT).as_posix(),
            "sha256": _sha256(Path(__file__)),
        },
        "validator_entrypoint_starts": 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise AssertionError(f"refusing to overwrite validation result: {args.output.name}")
    result = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(pretty_json_dumps(result), encoding="utf-8")
    print(
        "P2-I2 I05J metric closeout: "
        f"{result['passed_checks']}/{result['total_checks']}; "
        f"delta={result['analysis_arithmetic_delta']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
