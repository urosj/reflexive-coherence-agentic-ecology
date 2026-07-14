"""Future I05 entry point for the corrected P2-I2 analysis-arithmetic null.

I04-R1 freezes and validates this file but never invokes ``main`` or
``build_calibration_record``.  The entry point imports no PyGRC code and
accepts no runtime or candidate input.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Mapping

from ae01_tooling import ContractError, pretty_json_dumps
from p2_i2_i04r1_analysis import (
    PHYSICAL_ORDERS,
    normalized_paired_difference,
    validate_analysis_policy,
)


EXPECTED_CALIBRATION_ID = "rcae-p2-i2-shared-analysis-arithmetic-null-v2"
ROOT = Path(__file__).resolve().parents[3]


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _repository_relative_identity(path: Path) -> str:
    """Return a stable RCAE-relative identity without persisting checkout roots."""

    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError(f"input path is outside the RCAE repository: {path.name}") from exc


def validate_calibration_policy(
    calibration: Mapping[str, Any],
    analysis: Mapping[str, Any],
) -> None:
    """Validate the future pure null without executing it."""

    validate_analysis_policy(analysis)
    if calibration.get("calibration_id") != EXPECTED_CALIBRATION_ID:
        raise ContractError("calibration identity drifted")
    if calibration.get("schema_version") != "1.0.0":
        raise ContractError("calibration schema drifted")
    if (
        calibration.get("candidate_blind") is not True
        or calibration.get("runtime_execution") is not False
        or calibration.get("pygrc_imported") is not False
        or calibration.get("shared_across_modes") is not True
    ):
        raise ContractError("candidate/runtime exclusion or shared pure identity drifted")
    if calibration.get("analysis_policy_ref") != "configs/p2_i2_i04r1_analysis_policy.json":
        raise ContractError("corrected analysis-policy reference drifted")
    if calibration.get("analysis_arithmetic_floor") != 1e-12:
        raise ContractError("analysis-arithmetic floor drifted")
    if calibration.get("delta_field") != "analysis_arithmetic_delta":
        raise ContractError("analytic delta field drifted")
    if calibration.get("calibrates") != [
        "deterministic exact-rational parsing and float conversion",
        "normalized-margin arithmetic",
        "calibration-record serialization",
        "byte reconstruction through the same pure entry point",
    ]:
        raise ContractError("analysis-only calibrated surface drifted")
    if set(calibration.get("does_not_calibrate", ())) != {
        "PyGRC floating-point execution",
        "queue ordering or packet transport",
        "B-coherence measurement noise",
        "save/load/reset continuation",
        "mode-specific arithmetic depth",
        "runtime, restoration, or continuation equality tolerance",
    }:
        raise ContractError("runtime/measurement exclusions drifted")
    if calibration.get("calibration_seeds") != [19, 43, 71, 109, 163]:
        raise ContractError("calibration seeds drifted")
    if calibration.get("candidate_seeds_excluded") != [101, 211, 307]:
        raise ContractError("candidate seed exclusion drifted")
    if set(calibration["calibration_seeds"]) & set(calibration["candidate_seeds_excluded"]):
        raise ContractError("calibration and candidate seeds overlap")
    if tuple(calibration.get("physical_order_strata", ())) != PHYSICAL_ORDERS:
        raise ContractError("physical-order null strata drifted")

    generator = calibration.get("matched_null_generator")
    if not isinstance(generator, Mapping):
        raise ContractError("matched-null generator missing")
    panels = generator.get("panels")
    if not isinstance(panels, list) or len(panels) != 5:
        raise ContractError("matched null requires five seed panels")
    if [panel.get("seed") for panel in panels] != calibration["calibration_seeds"]:
        raise ContractError("matched-null panel seeds drifted")
    expected_rationals = iter(f"{numerator}/23" for numerator in range(1, 11))
    for panel in panels:
        for order in PHYSICAL_ORDERS:
            value = panel.get(order)
            if value != next(expected_rationals) or Fraction(value) <= 0:
                raise ContractError("matched-null rational panel drifted")

    domain = calibration.get("I06_domain_relation")
    if not isinstance(domain, Mapping) or domain.get(
        "runtime_tolerance_inference_from_delta_forbidden"
    ) is not True:
        raise ContractError("I06 numerical-domain separation drifted")
    boundary = calibration.get("I04R1_execution_boundary")
    if not isinstance(boundary, Mapping) or any(boundary.values()):
        raise ContractError("I04-R1 execution boundary drifted")
    authorization = calibration.get("authorization_requirement")
    if not isinstance(authorization, Mapping):
        raise ContractError("I05 authorization requirement missing")
    if (
        authorization.get("must_be_absent_in_I04R1") is not True
        or authorization.get("required_artifact_id")
        != "P2-I2-I05-CALIBRATION-EXECUTION-FREEZE"
        or authorization.get("required_iteration_id") != "P2-I2-I05"
        or authorization.get("required_CAL_PRE_gate")
        != "passed_after_owner_acceptance_of_I04R1"
        or authorization.get("required_governed_invocations") != 1
    ):
        raise ContractError("I05 mechanical authorization gate drifted")


def build_calibration_record(
    calibration: Mapping[str, Any],
    analysis: Mapping[str, Any],
    *,
    analysis_path: Path,
    calibration_path: Path,
) -> dict[str, Any]:
    """Build the later governed I05 record from frozen equal pairs."""

    validate_calibration_policy(calibration, analysis)
    floor = float(calibration["analysis_arithmetic_floor"])
    rows: list[dict[str, Any]] = []
    for panel in calibration["matched_null_generator"]["panels"]:
        for order in PHYSICAL_ORDERS:
            rational = panel[order]
            response = float(Fraction(rational))
            margin = normalized_paired_difference(response, response, floor)
            rows.append(
                {
                    "seed": panel["seed"],
                    "physical_order_id": order,
                    "exact_rational_response": rational,
                    "null_left_response": response,
                    "null_right_response": response,
                    "normalized_margin": margin,
                }
            )
    delta = max(floor, max(abs(row["normalized_margin"]) for row in rows))
    return {
        "record_type": "P2-I2-analysis-arithmetic-matched-null-calibration",
        "record_version": "1.0.0",
        "iteration_id": "P2-I2-I05",
        "lane_id": "AE01-L02",
        "calibration_id": calibration["calibration_id"],
        "candidate_blind": True,
        "runtime_execution": False,
        "pygrc_imported": False,
        "calibrated_surface": "pure_analysis_arithmetic_and_serialization_only",
        "input_identities": {
            "analysis_policy_path": _repository_relative_identity(analysis_path),
            "analysis_policy_sha256": _sha256(analysis_path),
            "calibration_policy_path": _repository_relative_identity(calibration_path),
            "calibration_policy_sha256": _sha256(calibration_path),
        },
        "per_seed_order_margins": rows,
        "estimator": calibration["estimator"],
        "analysis_arithmetic_floor": floor,
        "analysis_arithmetic_delta": delta,
        "runtime_tolerance_authority": "none",
        "candidate_evidence_effect": "none",
    }


def validate_execution_authorization(
    authorization: Mapping[str, Any],
    *,
    analysis_path: Path,
    calibration_path: Path,
    preregistration_path: Path,
) -> None:
    """Require a later owner-authorized I05 execution freeze."""

    expected = {
        "artifact_id",
        "artifact_version",
        "iteration_id",
        "lane_id",
        "I04R1_owner_acceptance_authority",
        "CAL_PRE_gate",
        "governed_invocations_authorized",
        "candidate_execution_authorized",
        "analysis_policy_sha256",
        "calibration_policy_sha256",
        "I04R1_preregistration_sha256",
    }
    if set(authorization) != expected:
        raise ContractError("I05 calibration authorization fields drifted")
    if authorization["artifact_id"] != "P2-I2-I05-CALIBRATION-EXECUTION-FREEZE":
        raise ContractError("wrong I05 calibration authorization artifact")
    if authorization["iteration_id"] != "P2-I2-I05" or authorization["lane_id"] != "AE01-L02":
        raise ContractError("I05 calibration authorization scope drifted")
    if not isinstance(authorization["I04R1_owner_acceptance_authority"], str) or not authorization[
        "I04R1_owner_acceptance_authority"
    ]:
        raise ContractError("I05 authorization requires I04-R1 owner acceptance authority")
    if authorization["CAL_PRE_gate"] != "passed_after_owner_acceptance_of_I04R1":
        raise ContractError("CAL-PRE gate has not authorized I05")
    if authorization["governed_invocations_authorized"] != 1:
        raise ContractError("I05 authorization must permit exactly one invocation")
    if authorization["candidate_execution_authorized"] is not False:
        raise ContractError("I05 authorization cannot open candidate execution")
    identities = {
        "analysis_policy_sha256": _sha256(analysis_path),
        "calibration_policy_sha256": _sha256(calibration_path),
        "I04R1_preregistration_sha256": _sha256(preregistration_path),
    }
    if any(authorization[key] != value for key, value in identities.items()):
        raise ContractError("I05 authorization identity does not match supplied I04-R1 inputs")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis-policy", type=Path, required=True)
    parser.add_argument("--calibration-policy", type=Path, required=True)
    parser.add_argument("--preregistration", type=Path, required=True)
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ContractError("refusing to overwrite an existing calibration record")
    analysis = _load(args.analysis_policy)
    calibration = _load(args.calibration_policy)
    authorization = _load(args.authorization)
    validate_execution_authorization(
        authorization,
        analysis_path=args.analysis_policy,
        calibration_path=args.calibration_policy,
        preregistration_path=args.preregistration,
    )
    record = build_calibration_record(
        calibration,
        analysis,
        analysis_path=args.analysis_policy,
        calibration_path=args.calibration_policy,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(pretty_json_dumps(record), encoding="utf-8")
    sys.stdout.write(pretty_json_dumps(record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
