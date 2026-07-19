"""Read-only closeout validation for retained P2-I3 B-R I05 outputs.

This program never calls the calibration builder. It validates and canonically
reserializes only the already retained one-shot outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping


def _find_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _find_root()
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import (  # noqa: E402
    ContractError,
    digest_file,
    load_json,
    pretty_json_dumps,
)
from p2_i3_i05_br_calibration import validate_calibration_outputs  # noqa: E402
from p2_i3_i05_br_one_shot import (  # noqa: E402
    FREEZE_PATH,
    I04_POLICY_PATH,
    METRIC_SHEET_PATH,
    POLICY_PATH,
    _schema_validator,
    validate_consumable_closeout,
)


ACTIVATION_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i05-br-calibration-launch-authorization.json"
)
OUTPUT_NAMES = ("matched_null", "metric_calibration", "frozen_metric_sheet")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def _canonical_bytes(value: Any) -> bytes:
    return pretty_json_dumps(value).encode("utf-8")


def _exclusive_write(path: Path, payload: bytes) -> None:
    _require(not os.path.lexists(path), f"output already exists: {_relative(path)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(payload)


def validate_and_reconstruct(
    *, reconstruction_dir: Path, validation_output: Path
) -> dict[str, Any]:
    allowed_reconstruction_root = (ROOT / "outputs/reconstruction").resolve()
    resolved_reconstruction_dir = reconstruction_dir.resolve()
    _require(
        resolved_reconstruction_dir.is_relative_to(allowed_reconstruction_root),
        "reconstruction directory must be under outputs/reconstruction",
    )
    _require(validation_output.resolve().is_relative_to(EXPERIMENT / "outputs"), "validation output must be experiment-local")

    policy = load_json(ROOT / POLICY_PATH)
    activation = load_json(ROOT / ACTIVATION_PATH)
    outputs = {name: ROOT / relative for name, relative in policy["outputs"].items()}
    claim = load_json(outputs["attempt_claim"])
    receipt = load_json(outputs["final_receipt"])
    retained = {name: load_json(outputs[name]) for name in OUTPUT_NAMES}

    checks: list[str] = []

    def check(identifier: str, condition: bool) -> None:
        _require(condition, f"closeout check failed: {identifier}")
        checks.append(identifier)

    schema_validator = _schema_validator()
    for identifier, value in (
        ("activation", activation),
        ("attempt_claim", claim),
        ("final_receipt", receipt),
        *((name, retained[name]) for name in OUTPUT_NAMES),
    ):
        schema_validator.validate(value)
        checks.append(f"schema.{identifier}")

    activation_sha256 = digest_file(ROOT / ACTIVATION_PATH)
    claim_sha256 = digest_file(outputs["attempt_claim"])
    retained_sha256 = {name: digest_file(outputs[name]) for name in OUTPUT_NAMES}

    check("activation.authorized_once", activation["governed_invocations_authorized"] == 1)
    check("activation.candidate_forbidden", activation["candidate_execution_authorized"] is False)
    check("claim.authorization_consumed", claim["authorization_consumed"] is True)
    check("claim.attempt_one", claim["governed_attempt"] == 1)
    check("claim.zero_retries", claim["infrastructure_retries"] == 0)
    check("claim.builder_ceiling_one", claim["builder_invocation_ceiling"] == 1)
    check("claim.activation_digest", claim["activation"]["sha256"] == activation_sha256)
    check("claim.freeze_digest", claim["accepted_freeze_sha256"] == digest_file(ROOT / FREEZE_PATH))
    check("claim.launch_head", claim["launch_head"] == receipt["launch_head"])
    check("receipt.success", receipt["completion_status"] == "success")
    check("receipt.attempt_consumed", receipt["attempt_consumed"] is True)
    check("receipt.builder_once", receipt["builder_invocation_count"] == 1)
    check("receipt.candidate_forbidden", receipt["candidate_execution_authorized"] is False)
    check("receipt.no_scientific_result", receipt["scientific_result"] is False)
    check("receipt.second_start_refused", receipt["second_start_evidence"]["refused"] is True)
    check("receipt.claim_unchanged", receipt["second_start_evidence"]["claim_sha256_unchanged"] is True)
    check("receipt.claim_digest", receipt["claim_sha256"] == claim_sha256)
    check("receipt.activation_digest", receipt["activation_sha256"] == activation_sha256)
    check("receipt.case_count", receipt["case_count"] == 5)
    check("receipt.response_count", receipt["response_record_count"] == 15)
    check("receipt.triplet_count", receipt["triplet_count"] == 5)
    check("receipt.margin_count", receipt["entered_margin_count"] == 10)
    check("receipt.relation_ids", receipt["calibrated_relation_ids"] == ["m_trace", "m_export"])
    check("receipt.schema_passed", receipt["schema_validation"] == "passed")
    check("receipt.semantic_passed", receipt["semantic_validation"] == "passed")
    check(
        "receipt.readback_passed",
        receipt["readback_validation"] == "passed_exact_bytes_canonical_json_and_semantics",
    )

    for name in OUTPUT_NAMES:
        check(
            f"canonical.{name}",
            outputs[name].read_bytes() == _canonical_bytes(retained[name]),
        )
        binding = receipt["output_bindings"][name]
        check(f"binding.path.{name}", binding["path"] == policy["outputs"][name])
        check(f"binding.digest.{name}", binding["sha256"] == retained_sha256[name])

    source_metric_sheet_sha256 = digest_file(ROOT / METRIC_SHEET_PATH)
    validate_calibration_outputs(
        retained,
        i04_policy=load_json(ROOT / I04_POLICY_PATH),
        metric_sheet=load_json(ROOT / METRIC_SHEET_PATH),
        source_metric_sheet_sha256=source_metric_sheet_sha256,
    )
    checks.append("semantic.cross_record")
    validate_consumable_closeout(
        policy=policy,
        receipt=receipt,
        claim_sha256=claim_sha256,
        activation_sha256=activation_sha256,
        output_sha256=retained_sha256,
    )
    checks.append("semantic.receipt_admission")

    reconstruction_bindings: dict[str, dict[str, str]] = {}
    for name in OUTPUT_NAMES:
        reconstructed_path = resolved_reconstruction_dir / outputs[name].name
        payload = _canonical_bytes(retained[name])
        _exclusive_write(reconstructed_path, payload)
        reconstructed_sha256 = hashlib.sha256(reconstructed_path.read_bytes()).hexdigest()
        check(f"reconstruction.bytes.{name}", reconstructed_path.read_bytes() == outputs[name].read_bytes())
        check(f"reconstruction.digest.{name}", reconstructed_sha256 == retained_sha256[name])
        reconstruction_bindings[name] = {
            "path": _relative(reconstructed_path),
            "sha256": reconstructed_sha256,
        }

    metric_calibration = retained["metric_calibration"]
    validation = {
        "artifact_id": "P2-I3-I05-BR-RESULT-VALIDATION",
        "artifact_version": "1.0.0",
        "branch_id": "P2-I3-BR",
        "check_count": len(checks),
        "checks": checks,
        "evidence_effect": "numeric_measurement_resolution_only",
        "input_bindings": {
            "activation": {"path": ACTIVATION_PATH, "sha256": activation_sha256},
            "attempt_claim": {"path": policy["outputs"]["attempt_claim"], "sha256": claim_sha256},
            "final_receipt": {
                "path": policy["outputs"]["final_receipt"],
                "sha256": digest_file(outputs["final_receipt"]),
            },
            **{
                name: {"path": policy["outputs"][name], "sha256": retained_sha256[name]}
                for name in OUTPUT_NAMES
            },
        },
        "iteration_id": "P2-I3-I05",
        "lane_id": "AE01-L03",
        "launch_head": receipt["launch_head"],
        "reconstruction_bindings": reconstruction_bindings,
        "result": {
            "calibrated_relation_ids": metric_calibration["calibrated_relation_ids"],
            "case_count": receipt["case_count"],
            "delta": metric_calibration["delta"],
            "entered_margin_count": receipt["entered_margin_count"],
            "maximum_absolute_matched_null_margin": metric_calibration[
                "maximum_absolute_matched_null_margin"
            ],
            "measurement_resolution": metric_calibration["measurement_resolution"],
            "response_record_count": receipt["response_record_count"],
            "triplet_count": receipt["triplet_count"],
        },
        "scientific_result": False,
        "status": "passed",
        "validator_sha256": digest_file(Path(__file__)),
    }
    _exclusive_write(validation_output.resolve(), _canonical_bytes(validation))
    return validation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reconstruction-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    validation = validate_and_reconstruct(
        reconstruction_dir=arguments.reconstruction_dir,
        validation_output=arguments.output,
    )
    print(pretty_json_dumps(validation), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
