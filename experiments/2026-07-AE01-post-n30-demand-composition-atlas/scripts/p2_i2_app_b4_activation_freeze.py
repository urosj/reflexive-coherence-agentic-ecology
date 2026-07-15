"""Construct the candidate APP-B4 activation-binding correction and activation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
import sys
from typing import Any

from p2_i2_app_b4_analysis import canonical_bytes, digest_value


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
RUNNER_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_run.py"
IMPLEMENTATION_COMMIT = "863d73c956286efb631d7a6fdd579837325dc2c0"
ACCEPTANCE_REL = f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-activation-owner-acceptance.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def committed_bytes(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def exclusive_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o644)
    try:
        payload = canonical_bytes(value)
        written = 0
        while written < len(payload):
            written += os.write(descriptor, payload[written:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--correction-output", required=True)
    parser.add_argument("--activation-output", required=True)
    args = parser.parse_args()
    for value in (args.freeze, args.correction_output, args.activation_output):
        require(portable_relative(value), "absolute path refused")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "lexical repository .venv required")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "-B required")

    freeze_path = ROOT / args.freeze
    correction_path = ROOT / args.correction_output
    activation_path = ROOT / args.activation_output
    for output in (correction_path, activation_path, ROOT / ACCEPTANCE_REL):
        require(not output.exists(), f"activation authority already exists: {output.name}")
    freeze = load_json(freeze_path)
    require(freeze["artifact_id"] == "P2-I2-APP-B4-INACTIVE-75-ARM-FREEZE", "wrong base freeze")
    require(freeze["status"] == "inactive_owner_review_pending", "base freeze lifecycle drifted")
    require(freeze["panel"]["arm_count"] == 75, "base arm count drifted")
    require(freeze["lifecycle"]["runtime_generation_count"] == 0, "base freeze records runtime")

    original_runner = committed_bytes(IMPLEMENTATION_COMMIT, RUNNER_REL)
    original_hash = sha256_bytes(original_runner)
    require(original_hash == freeze["implementation_sha256"][RUNNER_REL], "committed runner does not match freeze")
    corrected_hash = sha256(ROOT / RUNNER_REL)
    require(corrected_hash != original_hash, "activation correction did not change runner")
    unchanged_hashes: dict[str, str] = {}
    for relative, expected in freeze["implementation_sha256"].items():
        if relative == RUNNER_REL:
            continue
        observed = sha256(ROOT / relative)
        require(observed == expected, f"scientific implementation drift: {relative}")
        unchanged_hashes[relative] = observed

    correction: dict[str, Any] = {
        "artifact_id": "P2-I2-APP-B4-ACTIVATION-BINDING-CORRECTION",
        "artifact_version": "1.0",
        "iteration_id": "P2-I2-APP-B4",
        "status": "candidate_free_owner_review_pending",
        "authority": {
            "decision": "P2-I2-DEC-089",
            "change": "P2-I2-CHG-094",
            "owner_direction": "complete APP-B4",
        },
        "base_freeze": {
            "path": args.freeze,
            "sha256": sha256(freeze_path),
            "canonical_payload_digest": freeze["canonical_payload_digest"],
            "implementation_commit": IMPLEMENTATION_COMMIT,
        },
        "defect": {
            "kind": "impossible_self_referential_activation_head",
            "original_template_token": "{AUTHORITY_HEAD}",
            "explanation": "An activation file cannot contain the hash of the same commit that first contains that file.",
            "failed_scientific_attempts": 0,
        },
        "original_runner": {"path": RUNNER_REL, "sha256": original_hash},
        "corrected_runner": {"path": RUNNER_REL, "sha256": corrected_hash},
        "unchanged_frozen_implementation_sha256": unchanged_hashes,
        "corrected_binding": {
            "immutable_implementation_commit_must_be_ancestor": True,
            "invocation_head_must_equal_command_head": True,
            "activation_correction_and_acceptance_must_be_tracked_byte_exact": True,
            "authority_worktree_must_be_clean": True,
            "graph_commit_and_cleanliness_unchanged": True,
            "activation_head_template_token": "{ACTIVATION_HEAD}",
        },
        "scientific_invariance": {
            "registry_rows_changed": 0,
            "operation_registry_changed": False,
            "amounts_changed": False,
            "schedule_changed": False,
            "response_or_estimator_changed": False,
            "classifiers_or_claim_ceiling_changed": False,
            "attempt_or_retry_policy_changed": False,
            "accepted_scientific_implementation_files_changed": 0,
        },
        "process_receipt": {
            "builder_processes_this_start": 1,
            "PyGRC_imports": 0,
            "models": 0,
            "producers": 0,
            "arms": 0,
            "responses": 0,
        },
    }
    correction["canonical_payload_digest"] = digest_value(correction)
    exclusive_write(correction_path, correction)

    command = list(freeze["execution"]["normalized_command_template"])
    command[command.index("{AUTHORITY_HEAD}")] = "{ACTIVATION_HEAD}"
    activation: dict[str, Any] = {
        "artifact_id": "P2-I2-APP-B4-LIVE-ACTIVATION",
        "artifact_version": "1.0",
        "iteration_id": "P2-I2-APP-B4",
        "status": "active_for_single_campaign_after_owner_acceptance",
        "implementation_commit": IMPLEMENTATION_COMMIT,
        "freeze": {"path": args.freeze, "sha256": sha256(freeze_path)},
        "execution_correction": {"path": args.correction_output, "sha256": sha256(correction_path)},
        "owner_acceptance": {"path": ACCEPTANCE_REL},
        "campaign_authorized": True,
        "authorization_consumed": False,
        "campaign_attempts": 1,
        "scientific_retries": 0,
        "infrastructure_retries": 0,
        "claim_path": freeze["execution"]["claim_path"],
        "output_path": freeze["execution"]["output_path"],
        "reconstruction_path": freeze["execution"]["reconstruction_path"],
        "graph_commit": freeze["environment"]["graph_commit"],
        "graph_repository": freeze["environment"]["graph_repository"],
        "interpreter": ".venv/bin/python",
        "normalized_command": command,
        "candidate_current_effect": {
            "owner_acceptance_artifact_exists": False,
            "containing_commit_authorized": False,
            "campaign_start_authorized": False,
            "claim_created": False,
            "runtime_generation_count": 0,
        },
    }
    activation["canonical_payload_digest"] = digest_value(activation)
    exclusive_write(activation_path, activation)
    print(json.dumps({"status": "candidate_constructed", "scientific_rows_changed": 0}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
