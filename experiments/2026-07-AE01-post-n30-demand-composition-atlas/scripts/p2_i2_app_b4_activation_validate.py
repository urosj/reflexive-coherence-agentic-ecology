"""Candidate-free validation of the APP-B4 activation correction and authority."""

from __future__ import annotations

import argparse
import ast
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
VALIDATOR_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_activation_validate.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def unsigned_digest(value: dict[str, Any]) -> str:
    unsigned = dict(value)
    unsigned.pop("canonical_payload_digest")
    return digest_value(unsigned)


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


def module_scope_imports(source: str) -> list[str]:
    result = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.Import):
            result.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            result.append(node.module or "")
    return result


def validate(freeze_path: Path, correction_path: Path, activation_path: Path) -> dict[str, Any]:
    freeze = load_json(freeze_path)
    correction = load_json(correction_path)
    activation = load_json(activation_path)
    require(canonical_bytes(freeze) == freeze_path.read_bytes(), "freeze noncanonical")
    require(canonical_bytes(correction) == correction_path.read_bytes(), "correction noncanonical")
    require(canonical_bytes(activation) == activation_path.read_bytes(), "activation noncanonical")
    require(unsigned_digest(freeze) == freeze["canonical_payload_digest"], "freeze digest drifted")
    require(unsigned_digest(correction) == correction["canonical_payload_digest"], "correction digest drifted")
    require(unsigned_digest(activation) == activation["canonical_payload_digest"], "activation digest drifted")
    require(correction["artifact_id"] == "P2-I2-APP-B4-ACTIVATION-BINDING-CORRECTION", "wrong correction")
    require(activation["artifact_id"] == "P2-I2-APP-B4-LIVE-ACTIVATION", "wrong activation")
    require(activation["status"] == "active_for_single_campaign_after_owner_acceptance", "activation status drifted")
    require(correction["base_freeze"]["sha256"] == sha256(freeze_path), "correction freeze hash drifted")
    require(activation["freeze"]["sha256"] == sha256(freeze_path), "activation freeze hash drifted")
    require(activation["execution_correction"]["sha256"] == sha256(correction_path), "activation correction hash drifted")

    implementation_commit = correction["base_freeze"]["implementation_commit"]
    require(activation["implementation_commit"] == implementation_commit, "implementation commit drifted")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", implementation_commit, "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    ).returncode == 0
    require(ancestor, "implementation commit is not an ancestor")
    original = committed_bytes(implementation_commit, RUNNER_REL)
    require(sha256_bytes(original) == freeze["implementation_sha256"][RUNNER_REL], "original runner/freeze mismatch")
    require(sha256_bytes(original) == correction["original_runner"]["sha256"], "original runner correction mismatch")
    require(sha256(ROOT / RUNNER_REL) == correction["corrected_runner"]["sha256"], "corrected runner drifted")
    for relative, expected in correction["unchanged_frozen_implementation_sha256"].items():
        require(sha256(ROOT / relative) == expected == freeze["implementation_sha256"][relative], f"frozen implementation drift: {relative}")
    invariance = correction["scientific_invariance"]
    require(invariance["registry_rows_changed"] == 0, "registry changed")
    require(all(not value for key, value in invariance.items() if key.endswith("_changed")), "scientific semantics changed")
    require(invariance["accepted_scientific_implementation_files_changed"] == 0, "scientific implementation changed")

    command = activation["normalized_command"]
    require(command[0:2] == [".venv/bin/python", "-B"], "command is not repository-venv-only")
    require(command.count("{ACTIVATION_HEAD}") == 1 and "{AUTHORITY_HEAD}" not in command, "activation token drifted")
    require(command == [
        ".venv/bin/python", "-B", RUNNER_REL,
        "--freeze", str(freeze_path.relative_to(ROOT)),
        "--activation", str(activation_path.relative_to(ROOT)),
        "--claim", freeze["execution"]["claim_path"],
        "--output", freeze["execution"]["output_path"],
        "--expected-head", "{ACTIVATION_HEAD}",
        "--graph-root", freeze["environment"]["graph_repository"],
    ], "normalized command drifted")
    for value in (
        str(freeze_path.relative_to(ROOT)),
        str(correction_path.relative_to(ROOT)),
        str(activation_path.relative_to(ROOT)),
        activation["owner_acceptance"]["path"],
        activation["claim_path"],
        activation["output_path"],
        activation["reconstruction_path"],
    ):
        require(portable_relative(value), "absolute authority/output path")
    require(not (ROOT / activation["owner_acceptance"]["path"]).exists(), "owner acceptance already exists")
    require(not (ROOT / activation["claim_path"]).exists(), "campaign claim already exists")
    require(not (ROOT / activation["output_path"]).exists(), "runtime output already exists")
    require(not (ROOT / activation["reconstruction_path"]).exists(), "reconstruction already exists")

    runner_source = (ROOT / RUNNER_REL).read_text(encoding="utf-8")
    imports = module_scope_imports(runner_source)
    require(not any(name.startswith("pygrc") for name in imports), "candidate validator would import PyGRC through runner")
    for required_source in (
        "require_tracked_exact(activation_relative)",
        "merge-base", "--is-ancestor", "head == args.expected_head",
        "authority worktree dirty", "owner acceptance inactive",
        "os.O_EXCL", "scientific_retries_allowed\": 0", "infrastructure_retries_allowed\": 0",
    ):
        require(required_source in runner_source, f"corrected runner guard missing: {required_source}")
    serialized = json.dumps([freeze, correction, activation], sort_keys=True)
    forbidden_prefixes = ("/" + "home/", "/" + "Users/")
    require(not any(prefix in serialized for prefix in forbidden_prefixes), "absolute persisted path found")

    result = {
        "artifact_id": "P2-I2-APP-B4-ACTIVATION-CANDIDATE-VALIDATION",
        "artifact_version": "1.0",
        "iteration_id": "P2-I2-APP-B4",
        "status": "passed_candidate_free_owner_review_pending",
        "validator": {"path": VALIDATOR_REL, "sha256": sha256(ROOT / VALIDATOR_REL)},
        "checks": {
            "canonical_authorities_and_digests": 3,
            "immutable_implementation_ancestor": True,
            "original_runner_matches_inactive_freeze": True,
            "corrected_runner_matches_correction": True,
            "unchanged_frozen_implementation_files": len(correction["unchanged_frozen_implementation_sha256"]),
            "scientific_rows_changed": 0,
            "normalized_venv_command_exact": True,
            "tracked_byte_and_clean_head_guards_present": True,
            "exclusive_claim_and_zero_retry_guards_present": True,
            "owner_acceptance_absent": True,
            "claim_output_and_reconstruction_absent": True,
            "absolute_persisted_paths": 0,
        },
        "process_counts": {
            "validator_processes_this_start": 1,
            "PyGRC_imports": 0,
            "models": 0,
            "producers": 0,
            "arms": 0,
            "responses": 0,
        },
        "lifecycle": {
            "candidate_uncommitted": True,
            "owner_review_required": True,
            "containing_commit_authorized": False,
            "campaign_start_authorized": False,
            "runtime_generation_count": 0,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--correction", required=True)
    parser.add_argument("--activation", required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one validation mode")
    for value in (args.freeze, args.correction, args.activation, args.output):
        if value is not None:
            require(portable_relative(value), "absolute path refused")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "lexical repository .venv required")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "-B required")
    result = validate(ROOT / args.freeze, ROOT / args.correction, ROOT / args.activation)
    if args.output:
        output = ROOT / args.output
        require(not output.exists(), "activation validation output already exists")
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
    print(json.dumps({"status": result["status"], "scientific_rows_changed": 0}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
