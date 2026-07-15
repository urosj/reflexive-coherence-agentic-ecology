"""Read-only validation of retained APP-B4 runtime and reconstruction outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
import sys
from typing import Any

from p2_i2_app_b4_analysis import build_registry, canonical_bytes, digest_value


ROOT = Path(__file__).resolve().parents[3]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_digest(value: dict[str, Any]) -> bool:
    unsigned = dict(value)
    observed = unsigned.pop("canonical_payload_digest")
    return digest_value(unsigned) == observed


def validate(
    freeze_path: Path,
    activation_path: Path,
    claim_path: Path,
    runtime_path: Path,
    reconstruction_path: Path,
) -> dict[str, Any]:
    freeze = load_json(freeze_path)
    activation = load_json(activation_path)
    claim = load_json(claim_path)
    runtime = load_json(runtime_path)
    reconstruction = load_json(reconstruction_path)
    for path, value in (
        (freeze_path, freeze),
        (activation_path, activation),
        (claim_path, claim),
        (runtime_path, runtime),
        (reconstruction_path, reconstruction),
    ):
        require(canonical_bytes(value) == path.read_bytes(), f"noncanonical retained artifact: {path.name}")
    require(validate_digest(freeze), "freeze digest drifted")
    require(validate_digest(runtime), "runtime digest drifted")
    require(validate_digest(reconstruction), "reconstruction digest drifted")
    require(runtime["artifact_id"] == "P2-I2-APP-B4-RUNTIME-EVIDENCE", "wrong runtime artifact")
    require(reconstruction["artifact_id"] == "P2-I2-APP-B4-RECONSTRUCTION-AND-CLOSEOUT", "wrong reconstruction")
    require(claim["artifact_id"] == "P2-I2-APP-B4-CAMPAIGN-CLAIM", "wrong campaign claim")
    require(claim["authorization_consumed"] is True and claim["governed_attempt"] == 1, "campaign claim not consumed once")
    require(claim["scientific_retries_allowed"] == claim["infrastructure_retries_allowed"] == 0, "claim retry policy drifted")
    require(runtime["authority"] == claim, "runtime authority differs from permanent claim")
    require(claim["freeze_sha256"] == sha256(freeze_path), "claim freeze hash drifted")
    require(claim["activation_sha256"] == sha256(activation_path), "claim activation hash drifted")
    require(claim["preflight"]["authority_head"] == subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip(), "runtime authority head differs from current activation commit")
    require(claim["preflight"]["authority_clean_before_claim"] is True, "authority was dirty before claim")
    require(claim["preflight"]["tracked_authorities_exact"] is True, "activation authorities not tracked exact")
    require(claim["preflight"]["lexical_interpreter"] == ".venv/bin/python", "runtime interpreter drifted")

    rows = build_registry(freeze)
    expected_ids = [row["arm_id"] for row in rows]
    receipts = runtime["receipts"]
    require(runtime["arm_count"] == len(receipts) == len(rows) == 75, "runtime arm count drifted")
    require([receipt["arm_id"] for receipt in receipts] == expected_ids, "runtime arm order/identity drifted")
    require(len(set(expected_ids)) == 75, "registry identities not unique")
    require(runtime["runtime_invocation_count"] == 1, "runtime invocation count drifted")
    require(runtime["scientific_retry_count"] == 0, "scientific retry occurred")
    require(runtime["candidate_parameter_search_count"] == 0, "candidate parameter search occurred")
    require(runtime["graph_repository_mutation_count"] == 0, "graph mutation recorded")
    analysis = runtime["analysis"]
    require(analysis["matrix_complete"] is True, "APP-B4 matrix incomplete")
    require(analysis["arm_count_expected"] == analysis["arm_count_observed"] == 75, "analysis arm count drifted")
    require(analysis["arm_order_exact"] is True, "analysis arm order drifted")
    require(analysis["all_arms_operationally_valid"] is True, "invalid APP-B4 arm")
    require(all(item["valid"] is True and not item["failed_checks"] for item in analysis["operational_validity"].values()), "operational validity failure")
    require(analysis["excluded_operationally_infeasible_sequences"] == ["EEG", "EEE", "EEP"], "excluded domain drifted")
    require(analysis["excluded_sequences_treated_as_scientific_zero"] is False, "excluded sequence treated as zero")
    classification = analysis["classification"]
    require(classification is not None, "classification absent")
    require(classification["operation_complementarity_claimed"] is False, "operation complementarity overclaimed")
    require(classification["claim_ceiling"] == "ordered quantitative-history pattern within the unchanged-baseline feasible domain", "claim ceiling drifted")
    require(analysis["operation_complementarity_claimed"] is False, "analysis overclaimed operation complementarity")
    require(analysis["scientific_interpretation"] is None, "runner authored scientific interpretation")

    require(reconstruction["retained_input"] == {"path": str(runtime_path.relative_to(ROOT)), "sha256": sha256(runtime_path)}, "reconstruction input drifted")
    require(reconstruction["freeze"] == {"path": str(freeze_path.relative_to(ROOT)), "sha256": sha256(freeze_path)}, "reconstruction freeze drifted")
    require(reconstruction["analysis"] == analysis, "reconstructed analysis differs")
    require(reconstruction["analysis_reconstruction_byte_identical"] is True, "analysis reconstruction not byte-identical")
    require(reconstruction["arm_count_reconstructed"] == 75, "reconstruction arm count drifted")
    require(reconstruction["runtime_generation_count"] == 0, "reconstructor generated runtime")
    require(reconstruction["PyGRC_import_count"] == 0, "reconstructor imported PyGRC")
    require(reconstruction["model_count"] == reconstruction["producer_count"] == 0, "reconstructor ran scientific machinery")
    require(reconstruction["output_readback_reconstruction_count"] == 1, "reconstruction count drifted")
    require(reconstruction["scientific_retry_count"] == 0, "reconstruction reports retry")

    result = {
        "artifact_id": "P2-I2-APP-B4-CLOSEOUT-VALIDATION",
        "artifact_version": "1.0",
        "iteration_id": "P2-I2-APP-B4",
        "status": "passed_runtime_complete_owner_result_review_pending",
        "retained": {
            "freeze": {"path": str(freeze_path.relative_to(ROOT)), "sha256": sha256(freeze_path)},
            "activation": {"path": str(activation_path.relative_to(ROOT)), "sha256": sha256(activation_path)},
            "claim": {"path": str(claim_path.relative_to(ROOT)), "sha256": sha256(claim_path)},
            "runtime": {"path": str(runtime_path.relative_to(ROOT)), "sha256": sha256(runtime_path)},
            "reconstruction": {"path": str(reconstruction_path.relative_to(ROOT)), "sha256": sha256(reconstruction_path)},
        },
        "checks": {
            "permanent_claim_consumed_once": True,
            "runtime_invocations": 1,
            "scientific_and_infrastructure_retries": 0,
            "fresh_process_model_arms": 75,
            "matrix_complete": True,
            "operationally_valid_arms": 75,
            "reconstruction_byte_identical": True,
            "excluded_sequences_not_scientific_zero": True,
            "operation_complementarity_claimed": False,
        },
        "classification": classification,
        "process_counts": {
            "validator_processes_this_start": 1,
            "PyGRC_imports": 0,
            "models": 0,
            "producers": 0,
            "arms": 0,
            "responses": 0,
        },
        "owner_result_acceptance_required": True,
        "result_commit_authorized": False,
    }
    result["canonical_payload_digest"] = digest_value(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--activation", required=True)
    parser.add_argument("--claim", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--reconstruction", required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one validation mode")
    for value in (args.freeze, args.activation, args.claim, args.runtime, args.reconstruction, args.output):
        if value is not None:
            require(portable_relative(value), "absolute path refused")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "lexical repository .venv required")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "-B required")
    result = validate(
        ROOT / args.freeze,
        ROOT / args.activation,
        ROOT / args.claim,
        ROOT / args.runtime,
        ROOT / args.reconstruction,
    )
    if args.output:
        output = ROOT / args.output
        require(not output.exists(), "closeout validation output already exists")
        output.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(output, flags, 0o644)
        try:
            os.write(descriptor, canonical_bytes(result))
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    print(json.dumps({"status": result["status"], "arms": result["checks"]["operationally_valid_arms"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
