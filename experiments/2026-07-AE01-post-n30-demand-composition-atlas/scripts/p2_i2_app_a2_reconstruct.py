#!/usr/bin/env python3
"""Read-only APP-A2 reconstruction and bounded closeout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from typing import Any

from p2_i2_app_a2_analysis import analyze_receipts, canonical_bytes, digest_value


ROOT = Path(__file__).resolve().parents[3]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_root_path(value: str) -> Path:
    path = Path(value)
    require(not path.is_absolute(), "absolute paths prohibited")
    return ROOT / path


def validate_embedded_digest(value: dict[str, Any], key: str) -> None:
    copy = dict(value)
    observed = copy.pop(key)
    require(digest_value(copy) == observed, f"{key} mismatch")


def validate_implementation_hashes(freeze: dict[str, Any]) -> None:
    for row in freeze["implementation_files"]:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing implementation file: {row['path']}")
        require(sha256_file(path) == row["sha256"], f"implementation hash mismatch: {row['path']}")


def validate_static_validation(freeze: dict[str, Any], freeze_path: Path) -> None:
    validation_path = ROOT / freeze["static_validation_policy"]["output"]
    validation = load_json(validation_path)
    require(validation["status"] == "passed", "inactive static validation failed")
    require(validation["checks_passed"] == validation["checks_total"], "inactive checks incomplete")
    require(not validation["failed_checks"], "inactive validation retains failures")
    require(
        validation["activation_freeze"]["sha256"] == sha256_file(freeze_path),
        "inactive validation freeze identity drift",
    )
    validate_embedded_digest(validation, "output_digest")
    require(
        all(value == 0 for value in validation["zero_science_receipt"].values()),
        "inactive validation crossed scientific boundary",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    authorization_path = resolve_root_path(args.authorization).resolve()
    input_path = resolve_root_path(args.input).resolve()
    output_path = resolve_root_path(args.output).resolve()
    for path in (authorization_path, input_path, output_path):
        require(path.is_relative_to(ROOT), f"path outside repository: {path}")

    authorization = load_json(authorization_path)
    require(authorization["artifact_id"] == "P2-I2-APP-A2-ACTIVATION-AUTHORIZATION", "wrong authorization")
    require(authorization["status"] == "active_for_single_campaign", "authorization inactive")
    authority = authorization["authority"]
    require(authority["owner_acceptance"] is True, "owner acceptance absent")
    require(authority["campaign_authorized"] is True, "campaign authorization absent")
    freeze_ref = authorization["activation_freeze"]
    freeze_path = ROOT / freeze_ref["path"]
    require(sha256_file(freeze_path) == freeze_ref["sha256"], "activation freeze drift")
    activation_freeze = load_json(freeze_path)
    require(activation_freeze["status"] == "validated_inactive_pending_owner_activation", "activation freeze status drift")
    require(
        authorization_path
        == (ROOT / activation_freeze["future_activation_authorization"]["path"]).resolve(),
        "authorization path drift",
    )
    require(
        authority["normalized_reconstruction_command"]
        == activation_freeze["normalized_commands"]["reconstruction"],
        "reconstruction command identity drift",
    )
    validate_implementation_hashes(activation_freeze)
    validate_static_validation(activation_freeze, freeze_path)

    require(Path(sys.executable).resolve() == (ROOT / ".venv" / "bin" / "python").resolve(), "repository venv inactive")
    environment = activation_freeze["environment"]
    require(platform.python_version() == environment["python_version"], "Python version drift")
    require(sha256_file(ROOT / ".venv" / "bin" / "python") == environment["interpreter_sha256"], "interpreter drift")

    execution_ref = activation_freeze["retained_app_a1"]["execution_freeze"]
    fixture_ref = activation_freeze["retained_app_a1"]["fixture_freeze"]
    execution_path = ROOT / execution_ref["path"]
    fixture_path = ROOT / fixture_ref["path"]
    require(sha256_file(execution_path) == execution_ref["sha256"], "execution freeze drift")
    require(sha256_file(fixture_path) == fixture_ref["sha256"], "fixture freeze drift")
    execution = load_json(execution_path)
    fixture = load_json(fixture_path)
    expected_input = ROOT / execution["campaign_policy"]["single_aggregate_persisted_output"]
    expected_output = ROOT / execution["campaign_policy"]["read_only_reconstruction_output"]
    require(input_path == expected_input.resolve(), "input path differs from freeze")
    require(output_path == expected_output.resolve(), "output path differs from freeze")
    require(input_path.is_file(), "retained aggregate missing")
    require(not output_path.exists(), "reconstruction output already exists")

    aggregate = load_json(input_path)
    require(aggregate["artifact_id"] == "p2_i2_app_a2_runtime_evidence", "wrong aggregate")
    require(aggregate["status"] in {"complete", "nonevaluable"}, "aggregate incomplete")
    validate_embedded_digest(aggregate, "output_digest")
    require(
        aggregate["authority"]["activation_authorization_sha256"]
        == sha256_file(authorization_path),
        "aggregate authorization drift",
    )
    require(
        aggregate["authority"]["activation_freeze_sha256"]
        == freeze_ref["sha256"],
        "aggregate activation freeze drift",
    )

    reconstructed = analyze_receipts(
        aggregate["arm_receipts"],
        fixture,
        execution,
    )
    require(
        canonical_bytes(reconstructed) == canonical_bytes(aggregate["analysis"]),
        "analysis reconstruction differs from aggregate",
    )
    closeout: dict[str, Any] = {
        "artifact_id": "p2_i2_app_a2_reconstruction_and_closeout",
        "artifact_version": "1.0",
        "experiment_id": "2026-07-AE01",
        "generated_at": aggregate["generated_at"],
        "iteration_id": "P2-I2-APP-A2",
        "status": "complete" if reconstructed["matrix_complete"] else "nonevaluable",
        "source": {
            "aggregate_path": str(input_path.relative_to(ROOT)),
            "aggregate_sha256": sha256_file(input_path),
            "aggregate_output_digest": aggregate["output_digest"],
            "activation_authorization_sha256": sha256_file(authorization_path),
            "activation_freeze_sha256": freeze_ref["sha256"],
        },
        "reconstruction_receipt": {
            "retained_aggregate_reads": 1,
            "pygrc_imports": 0,
            "model_invocations": 0,
            "child_process_invocations": 0,
            "producer_invocations": 0,
            "scientific_regeneration_invocations": 0,
            "analysis_byte_identical": True,
            "analysis_digest": reconstructed["analysis_digest"],
        },
        "analysis": reconstructed,
        "terminal_classification": reconstructed["terminal_classification"],
        "bounded_claim": reconstructed["bounded_claim"],
        "functional_description": reconstructed["functional_description"],
        "plurality_resolution": reconstructed["plurality_resolution"],
        "order_resolution": reconstructed["controls"]["order_resolution"],
        "blocked_claims": reconstructed["blocked_claims"],
        "claim_scope": {
            "fixture_bounded": True,
            "gate_signature_bounded": True,
            "main_p2_i2_terminal_changed": False,
            "n29_metric_equivalence_claimed": False,
            "cross_lane_recurrence_claimed": False,
            "n31_plus_selected": False,
        },
    }
    closeout["output_digest"] = digest_value(closeout)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(output_path, flags, 0o644)
    try:
        data = canonical_bytes(closeout)
        written = 0
        while written < len(data):
            written += os.write(fd, data[written:])
        os.fsync(fd)
    finally:
        os.close(fd)
    print(
        json.dumps(
            {
                "status": closeout["status"],
                "terminal_classification": closeout["terminal_classification"],
                "output_digest": closeout["output_digest"],
            },
            sort_keys=True,
        )
    )
    return 0 if reconstructed["matrix_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
