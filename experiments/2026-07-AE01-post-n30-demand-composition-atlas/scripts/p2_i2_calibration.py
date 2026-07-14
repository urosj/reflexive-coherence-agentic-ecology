#!/usr/bin/env python3
"""Execute the frozen P2-I2 candidate-blind matched null in I05.

I04 freezes and validates this entry point but does not invoke it. The script
imports no PyGRC code and accepts no candidate or runtime inputs.
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
from p2_i2_analysis import (
    ORDERS,
    normalized_paired_difference,
    validate_analysis_policy,
)


EXPECTED_CALIBRATION_ID = "rcae-p2-i2-shared-candidate-blind-matched-null-v1"


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


def validate_calibration_policy(
    calibration: Mapping[str, Any],
    analysis: Mapping[str, Any],
) -> None:
    validate_analysis_policy(analysis)
    if calibration.get("calibration_id") != EXPECTED_CALIBRATION_ID:
        raise ContractError("calibration identity drifted")
    if calibration.get("candidate_blind") is not True:
        raise ContractError("calibration must remain candidate-blind")
    if calibration.get("runtime_execution") is not False:
        raise ContractError("calibration cannot execute a runtime")
    if calibration.get("pygrc_imported") is not False:
        raise ContractError("calibration cannot import PyGRC")
    if calibration.get("shared_across_modes") is not True:
        raise ContractError("shared calibration identity drifted")
    if calibration.get("measurement_resolution") != 1e-12:
        raise ContractError("calibration resolution drifted")
    if calibration.get("calibration_seeds") != [19, 43, 71, 109, 163]:
        raise ContractError("calibration seeds drifted")
    if calibration.get("candidate_seeds_excluded") != [101, 211, 307]:
        raise ContractError("candidate seed exclusion drifted")
    if set(calibration["calibration_seeds"]) & set(calibration["candidate_seeds_excluded"]):
        raise ContractError("calibration and candidate seeds overlap")
    if tuple(calibration.get("order_strata", ())) != ORDERS:
        raise ContractError("calibration must cover both order strata")
    generator = calibration.get("matched_null_generator")
    if not isinstance(generator, Mapping):
        raise ContractError("matched-null generator missing")
    panels = generator.get("panels")
    if not isinstance(panels, list) or len(panels) != 5:
        raise ContractError("matched null requires five seed panels")
    if [panel.get("seed") for panel in panels] != calibration["calibration_seeds"]:
        raise ContractError("matched-null panel seeds drifted")
    expected_rationals = iter(
        [f"{numerator}/23" for numerator in range(1, 11)]
    )
    for panel in panels:
        for order in ORDERS:
            value = panel.get(order)
            if value != next(expected_rationals):
                raise ContractError("matched-null rational panel drifted")
            if Fraction(value) <= 0:
                raise ContractError("matched-null response must be positive")
    boundary = calibration.get("I04_execution_boundary")
    if not isinstance(boundary, Mapping) or any(boundary.values()):
        raise ContractError("I04 calibration/candidate execution boundary drifted")
    authorization = calibration.get("authorization_requirement")
    if not isinstance(authorization, Mapping):
        raise ContractError("I05 execution-authorization requirement missing")
    if authorization.get("must_be_absent_in_I04") is not True:
        raise ContractError("I05 authorization file must remain absent in I04")
    if authorization.get("required_artifact_id") != "P2-I2-I05-CALIBRATION-EXECUTION-FREEZE":
        raise ContractError("I05 authorization artifact identity drifted")
    if authorization.get("required_iteration_id") != "P2-I2-I05":
        raise ContractError("I05 authorization iteration drifted")
    if authorization.get("required_CAL_PRE_gate") != "passed_after_owner_acceptance":
        raise ContractError("I05 authorization must require owner-accepted CAL-PRE")
    if authorization.get("required_governed_invocations") != 1:
        raise ContractError("I05 authorization must permit exactly one invocation")


def build_calibration_record(
    calibration: Mapping[str, Any],
    analysis: Mapping[str, Any],
    *,
    analysis_path: Path,
    calibration_path: Path,
) -> dict[str, Any]:
    """Build the governed I05 record from equal candidate-blind pairs."""

    validate_calibration_policy(calibration, analysis)
    resolution = float(calibration["measurement_resolution"])
    rows: list[dict[str, Any]] = []
    for panel in calibration["matched_null_generator"]["panels"]:
        for order in ORDERS:
            rational = panel[order]
            response = float(Fraction(rational))
            margin = normalized_paired_difference(response, response, resolution)
            rows.append(
                {
                    "seed": panel["seed"],
                    "order_id": order,
                    "exact_rational_response": rational,
                    "null_candidate_response": response,
                    "null_comparator_response": response,
                    "normalized_margin": margin,
                }
            )
    delta = max(resolution, max(abs(row["normalized_margin"]) for row in rows))
    return {
        "record_type": "P2-I2-candidate-blind-matched-null-calibration",
        "record_version": "1.0.0",
        "iteration_id": "P2-I2-I05",
        "lane_id": "AE01-L02",
        "calibration_id": calibration["calibration_id"],
        "candidate_blind": True,
        "runtime_execution": False,
        "pygrc_imported": False,
        "input_identities": {
            "analysis_policy_path": str(analysis_path),
            "analysis_policy_sha256": _sha256(analysis_path),
            "calibration_policy_path": str(calibration_path),
            "calibration_policy_sha256": _sha256(calibration_path),
        },
        "per_seed_order_margins": rows,
        "estimator": calibration["estimator"],
        "measurement_resolution": resolution,
        "delta": delta,
        "candidate_evidence_effect": "none",
    }


def validate_execution_authorization(
    authorization: Mapping[str, Any],
    *,
    analysis_path: Path,
    calibration_path: Path,
    preregistration_path: Path,
) -> None:
    """Require the later owner-authorized I05 execution freeze."""

    expected = {
        "artifact_id",
        "artifact_version",
        "iteration_id",
        "lane_id",
        "I04_owner_acceptance_authority",
        "CAL_PRE_gate",
        "governed_invocations_authorized",
        "candidate_execution_authorized",
        "analysis_policy_sha256",
        "calibration_policy_sha256",
        "I04_preregistration_sha256",
    }
    if set(authorization) != expected:
        raise ContractError("I05 calibration authorization fields drifted")
    if authorization["artifact_id"] != "P2-I2-I05-CALIBRATION-EXECUTION-FREEZE":
        raise ContractError("wrong I05 calibration authorization artifact")
    if authorization["iteration_id"] != "P2-I2-I05" or authorization["lane_id"] != "AE01-L02":
        raise ContractError("I05 calibration authorization scope drifted")
    if not isinstance(authorization["I04_owner_acceptance_authority"], str) or not authorization["I04_owner_acceptance_authority"]:
        raise ContractError("I05 authorization requires owner acceptance authority")
    if authorization["CAL_PRE_gate"] != "passed_after_owner_acceptance":
        raise ContractError("CAL-PRE gate has not authorized I05")
    if authorization["governed_invocations_authorized"] != 1:
        raise ContractError("I05 authorization must permit exactly one invocation")
    if authorization["candidate_execution_authorized"] is not False:
        raise ContractError("I05 authorization cannot open candidate execution")
    identities = {
        "analysis_policy_sha256": _sha256(analysis_path),
        "calibration_policy_sha256": _sha256(calibration_path),
        "I04_preregistration_sha256": _sha256(preregistration_path),
    }
    if any(authorization[key] != value for key, value in identities.items()):
        raise ContractError("I05 authorization identity does not match supplied I04 inputs")


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
