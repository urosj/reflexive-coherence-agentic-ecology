#!/usr/bin/env python3
"""Future I05 exact three-arm arithmetic-null entry point for P2-I2.

I04-R2 validates but never invokes the record builder or ``main``.  The later
owner-authorized I05 call must create three raw envelopes per tuple and route
them through the exact live ``primary_margin`` estimator.  This module imports
no PyGRC code and accepts no runtime/candidate input.
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
from p2_i2_i04r2_analysis import (
    PHYSICAL_ORDERS,
    build_synthetic_response_envelope,
    primary_margin,
    validate_machine_policy,
)


EXPECTED_CALIBRATION_ID = "rcae-p2-i2-complete-three-arm-analysis-arithmetic-null-v3"


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
    machine_policy: Mapping[str, Any],
    parent_analysis_policy: Mapping[str, Any],
) -> None:
    """Validate the future exact-estimator null without executing it."""

    validate_machine_policy(machine_policy, parent_analysis_policy)
    if calibration.get("calibration_id") != EXPECTED_CALIBRATION_ID:
        raise ContractError("I04-R2 calibration identity drifted")
    if calibration.get("schema_version") != "1.0.0":
        raise ContractError("I04-R2 calibration schema drifted")
    if (
        calibration.get("candidate_blind") is not True
        or calibration.get("runtime_execution") is not False
        or calibration.get("pygrc_imported") is not False
        or calibration.get("shared_across_modes") is not True
    ):
        raise ContractError("candidate/runtime exclusion or shared arithmetic identity drifted")
    if calibration.get("analysis_arithmetic_floor") != 1e-12:
        raise ContractError("analysis-arithmetic floor drifted")
    if calibration.get("delta_field") != "analysis_arithmetic_delta":
        raise ContractError("analysis-arithmetic delta field drifted")
    parent = calibration.get("parent_calibration_history")
    if not isinstance(parent, Mapping) or parent.get("sha256") != (
        "5eb921eeb49c0fb336b5176a98bfd615482b991293afbd579263a5275a8717ad"
    ):
        raise ContractError("I04-R1 calibration history identity drifted")
    if "bypassed" not in str(parent.get("disposition")):
        raise ContractError("superseded direct-margin route is not explicit")

    analysis = calibration.get("analysis_inputs")
    if not isinstance(analysis, Mapping):
        raise ContractError("I04-R2 analysis inputs missing")
    if (
        analysis.get("parent_analysis_policy_sha256")
        != "91b8bd50633a19333935ec115bdd005697abdef5381ef59f4ceab21db08c090d"
        or analysis.get("estimator_entrypoint") != "p2_i2_i04r2_analysis.primary_margin"
    ):
        raise ContractError("exact live estimator input drifted")
    if len(calibration.get("calibrates", ())) != 5 or len(
        calibration.get("does_not_calibrate", ())
    ) != 6:
        raise ContractError("analytic calibrated/excluded surfaces drifted")
    if calibration.get("calibration_seeds") != [19, 43, 71, 109, 163]:
        raise ContractError("calibration seeds drifted")
    if calibration.get("candidate_seeds_excluded") != [101, 211, 307]:
        raise ContractError("candidate seed exclusions drifted")
    if set(calibration["calibration_seeds"]) & set(calibration["candidate_seeds_excluded"]):
        raise ContractError("calibration and candidate seeds overlap")
    if tuple(calibration.get("physical_order_strata", ())) != PHYSICAL_ORDERS:
        raise ContractError("physical-order null strata drifted")

    reconstruction = calibration.get("serialization_and_reconstruction")
    if not isinstance(reconstruction, Mapping) or (
        reconstruction.get("serializer") != "ae01_tooling.pretty_json_dumps"
        or reconstruction.get("reconstructor") != "json.loads"
        or reconstruction.get("byte_equality_required") is not True
        or len(reconstruction.get("route", ())) != 5
        or "invalid or incomplete" not in str(reconstruction.get("failure_effect"))
    ):
        raise ContractError("future I05 serialization/reconstruction path drifted")

    generator = calibration.get("matched_null_generator")
    if not isinstance(generator, Mapping):
        raise ContractError("three-arm matched-null generator missing")
    if generator.get("kind") != "equal_raw_three_arm_response_envelopes_over_two_physical_order_strata":
        raise ContractError("matched-null generator does not create raw three-arm tuples")
    if generator.get("arms_per_tuple") != [
        "combined-orders",
        "q1_admitted_q2_diverted",
        "q2_admitted_q1_diverted",
    ] or generator.get("precollapsed_comparator_supplied") is not False:
        raise ContractError("complete raw three-arm null identity drifted")
    panels = generator.get("panels")
    if not isinstance(panels, list) or len(panels) != 5:
        raise ContractError("matched null requires five seed panels")
    if [row.get("seed") for row in panels] != calibration["calibration_seeds"]:
        raise ContractError("matched-null panel seeds drifted")
    expected = iter(f"{numerator}/23" for numerator in range(1, 11))
    for panel in panels:
        for order in PHYSICAL_ORDERS:
            rational = panel.get(order)
            if rational != next(expected) or Fraction(rational) <= 0:
                raise ContractError("matched-null exact rational panel drifted")

    auth = calibration.get("authorization_requirement")
    if not isinstance(auth, Mapping) or (
        auth.get("must_be_absent_in_I04R2") is not True
        or auth.get("required_CAL_PRE_gate")
        != "passed_after_explicit_owner_acceptance_of_I04R2"
        or auth.get("required_governed_invocations") != 1
    ):
        raise ContractError("future I05 authorization boundary drifted")
    required_artifacts = calibration.get("required_I05_artifacts")
    if not isinstance(required_artifacts, list) or len(required_artifacts) != 4:
        raise ContractError("future I05 retained-artifact boundary drifted")
    boundary = calibration.get("I04R2_execution_boundary")
    if not isinstance(boundary, Mapping) or any(boundary.values()):
        raise ContractError("I04-R2 execution boundary drifted")


def build_calibration_record(
    calibration: Mapping[str, Any],
    machine_policy: Mapping[str, Any],
    parent_analysis_policy: Mapping[str, Any],
    *,
    parent_analysis_path: Path,
    machine_policy_path: Path,
    calibration_path: Path,
) -> dict[str, Any]:
    """Build the later I05 record through the exact live three-arm path."""

    validate_calibration_policy(calibration, machine_policy, parent_analysis_policy)
    rows: list[dict[str, Any]] = []
    for panel in calibration["matched_null_generator"]["panels"]:
        for order in PHYSICAL_ORDERS:
            rational = panel[order]
            response = float(Fraction(rational))
            pairing = f"I05-pure-three-arm:{panel['seed']}:{order}"
            candidate = build_synthetic_response_envelope(
                record_id=f"{pairing}:candidate",
                branch_id="combined-orders",
                response=response,
                seed=panel["seed"],
                physical_order_id=order,
                carrier_state_digest=f"{pairing}:combined-carrier",
                pairing_identity=pairing,
            )
            q1_only = build_synthetic_response_envelope(
                record_id=f"{pairing}:q1-only",
                branch_id="q1_admitted_q2_diverted",
                response=response,
                seed=panel["seed"],
                physical_order_id=order,
                carrier_state_digest=f"{pairing}:q1-carrier",
                pairing_identity=pairing,
            )
            q2_only = build_synthetic_response_envelope(
                record_id=f"{pairing}:q2-only",
                branch_id="q2_admitted_q1_diverted",
                response=response,
                seed=panel["seed"],
                physical_order_id=order,
                carrier_state_digest=f"{pairing}:q2-carrier",
                pairing_identity=pairing,
            )
            result = primary_margin(
                candidate,
                q1_only,
                q2_only,
                machine_policy,
                parent_analysis_policy,
            )
            if not result["complete_three_arm_tuple_valid"] or not result["evaluable"]:
                raise ContractError("complete arithmetic-null tuple unexpectedly nonevaluable")
            rows.append(
                {
                    "seed": panel["seed"],
                    "physical_order_id": order,
                    "exact_rational_response": rational,
                    "raw_candidate_response": result["candidate_response"],
                    "raw_leave_q1_response": result["q1_only_response"],
                    "raw_leave_q2_response": result["q2_only_response"],
                    "selected_comparator_record_id": result[
                        "selected_comparator_record_id"
                    ],
                    "strongest_leave_one_response": result[
                        "strongest_leave_one_response"
                    ],
                    "normalized_margin": result["normalized_margin"],
                    "estimator_path_id": result["estimator_path_id"],
                }
            )
    floor = float(calibration["analysis_arithmetic_floor"])
    delta = max(floor, max(abs(row["normalized_margin"]) for row in rows))
    return {
        "record_type": "P2-I2-complete-three-arm-analysis-arithmetic-calibration",
        "record_version": "1.0.0",
        "iteration_id": "P2-I2-I05",
        "lane_id": "AE01-L02",
        "calibration_id": calibration["calibration_id"],
        "candidate_blind": True,
        "runtime_execution": False,
        "pygrc_imported": False,
        "calibrated_surface": "complete_pure_three_arm_primary_estimator_and_serialization_only",
        "input_identities": {
            "parent_analysis_policy_path": str(parent_analysis_path),
            "parent_analysis_policy_sha256": _sha256(parent_analysis_path),
            "machine_policy_path": str(machine_policy_path),
            "machine_policy_sha256": _sha256(machine_policy_path),
            "calibration_policy_path": str(calibration_path),
            "calibration_policy_sha256": _sha256(calibration_path),
        },
        "per_seed_order_three_arm_margins": rows,
        "estimator": calibration["estimator"],
        "analysis_arithmetic_floor": floor,
        "analysis_arithmetic_delta": delta,
        "runtime_tolerance_authority": "none",
        "candidate_evidence_effect": "none",
    }


def validate_execution_authorization(
    authorization: Mapping[str, Any],
    *,
    parent_analysis_path: Path,
    machine_policy_path: Path,
    calibration_path: Path,
    preregistration_path: Path,
) -> None:
    """Require a later explicit owner-authorized I05 execution freeze."""

    expected = {
        "artifact_id",
        "artifact_version",
        "iteration_id",
        "lane_id",
        "I04R2_owner_acceptance_authority",
        "CAL_PRE_gate",
        "governed_invocations_authorized",
        "candidate_execution_authorized",
        "parent_analysis_policy_sha256",
        "machine_policy_sha256",
        "calibration_policy_sha256",
        "calibration_entrypoint_sha256",
        "I04R2_preregistration_sha256",
    }
    if set(authorization) != expected:
        raise ContractError("I05 authorization fields drifted")
    if authorization["artifact_id"] != "P2-I2-I05-CALIBRATION-EXECUTION-FREEZE":
        raise ContractError("wrong I05 authorization artifact")
    if authorization["iteration_id"] != "P2-I2-I05" or authorization["lane_id"] != "AE01-L02":
        raise ContractError("I05 authorization scope drifted")
    if not isinstance(authorization["I04R2_owner_acceptance_authority"], str) or not authorization[
        "I04R2_owner_acceptance_authority"
    ]:
        raise ContractError("I05 requires explicit I04-R2 owner acceptance authority")
    if authorization["CAL_PRE_gate"] != "passed_after_explicit_owner_acceptance_of_I04R2":
        raise ContractError("CAL-PRE has not authorized I05")
    if authorization["governed_invocations_authorized"] != 1:
        raise ContractError("I05 authorization must permit exactly one invocation")
    if authorization["candidate_execution_authorized"] is not False:
        raise ContractError("I05 authorization cannot open candidate execution")
    identities = {
        "parent_analysis_policy_sha256": _sha256(parent_analysis_path),
        "machine_policy_sha256": _sha256(machine_policy_path),
        "calibration_policy_sha256": _sha256(calibration_path),
        "calibration_entrypoint_sha256": _sha256(Path(__file__)),
        "I04R2_preregistration_sha256": _sha256(preregistration_path),
    }
    if any(authorization[key] != value for key, value in identities.items()):
        raise ContractError("I05 authorization identity does not match I04-R2 inputs")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent-analysis-policy", type=Path, required=True)
    parser.add_argument("--machine-policy", type=Path, required=True)
    parser.add_argument("--calibration-policy", type=Path, required=True)
    parser.add_argument("--preregistration", type=Path, required=True)
    parser.add_argument("--authorization", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ContractError("refusing to overwrite an existing calibration record")
    parent_analysis = _load(args.parent_analysis_policy)
    machine_policy = _load(args.machine_policy)
    calibration = _load(args.calibration_policy)
    authorization = _load(args.authorization)
    validate_execution_authorization(
        authorization,
        parent_analysis_path=args.parent_analysis_policy,
        machine_policy_path=args.machine_policy,
        calibration_path=args.calibration_policy,
        preregistration_path=args.preregistration,
    )
    record = build_calibration_record(
        calibration,
        machine_policy,
        parent_analysis,
        parent_analysis_path=args.parent_analysis_policy,
        machine_policy_path=args.machine_policy,
        calibration_path=args.calibration_policy,
    )
    serialized = pretty_json_dumps(record)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(serialized, encoding="utf-8")
    retained_text = args.output.read_text(encoding="utf-8")
    reconstructed = json.loads(retained_text)
    reconstructed_serialized = pretty_json_dumps(reconstructed)
    if reconstructed_serialized != retained_text or retained_text != serialized:
        raise ContractError("retained I05 calibration output did not reconstruct byte-identically")
    sys.stdout.write(retained_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
