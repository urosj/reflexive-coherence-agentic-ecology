#!/usr/bin/env python3
"""Zero-science validation for the proposed APP-A2 activation authorization."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"
PREFIX = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
EXPECTED_HEAD = "c435b00472b97020041783c8b89d6cb7135edbb3"
EXPECTED_DIRTY_PATHS = {
    PREFIX + "hypotheses/p2-i2-operational-hypotheses.md",
    PREFIX + "implementation/P2-I2-decision-record.md",
    PREFIX + "implementation/P2-I2-shared-pool-co-conditioning-checklist.md",
    PREFIX + "contracts/p2-i2/app-a2-activation-authorization.json",
    PREFIX + "scripts/p2_i2_app_a2_activation_validate.py",
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path.name}")
    return value


def git(*args: str, cwd: Path = ROOT, text: bool = True) -> Any:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=text,
    ).stdout.rstrip()


def committed_bytes(path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def add(self, check_id: str, passed: bool, observed: Any = None) -> None:
        self.rows.append(
            {"check_id": check_id, "passed": bool(passed), "observed": observed}
        )


def validate(authorization_path: Path) -> dict[str, Any]:
    checks = Checks()
    authorization = load_json(authorization_path)
    checks.add("authority.artifact", authorization.get("artifact_id") == "P2-I2-APP-A2-ACTIVATION-AUTHORIZATION", authorization.get("artifact_id"))
    checks.add("authority.runtime_status", authorization.get("status") == "active_for_single_campaign", authorization.get("status"))
    checks.add("authority.candidate_no_effect", authorization["current_effect"]["candidate_uncommitted"] is True and authorization["current_effect"]["activation_commit_authorized"] is False and authorization["current_effect"]["campaign_start_authorized"] is False, authorization["current_effect"])

    head = git("rev-parse", "HEAD")
    checks.add("rcae.exact_head", head == EXPECTED_HEAD, head)
    checks.add("rcae.branch", git("branch", "--show-current") == "p2-i2-experiment", git("branch", "--show-current"))
    status_rows = [row for row in git("status", "--short").splitlines() if row]
    dirty_paths = {row[3:] for row in status_rows}
    checks.add("rcae.exact_candidate_dirty_scope", dirty_paths == EXPECTED_DIRTY_PATHS, sorted(dirty_paths))
    authorization_rel = str(authorization_path.relative_to(ROOT))
    tracked = subprocess.run(["git", "cat-file", "-e", f"HEAD:{authorization_rel}"], cwd=ROOT, capture_output=True).returncode == 0
    checks.add("authority.uncommitted", not tracked, tracked)

    freeze_ref = authorization["activation_freeze"]
    freeze_path = ROOT / freeze_ref["path"]
    freeze = load_json(freeze_path)
    checks.add("freeze.hash", sha256_file(freeze_path) == freeze_ref["sha256"], freeze_ref["sha256"])
    checks.add("freeze.status", freeze["status"] == "validated_inactive_pending_owner_activation", freeze["status"])
    checks.add("freeze.authorization_path", freeze["future_activation_authorization"]["path"] == authorization_rel, freeze["future_activation_authorization"]["path"])
    checks.add("freeze.implementation_commit", authorization["authority"]["implementation_commit"] == EXPECTED_HEAD, authorization["authority"]["implementation_commit"])

    for row in freeze["implementation_files"]:
        path = ROOT / row["path"]
        local = path.read_bytes()
        checks.add(f"implementation.{row['role']}.frozen_hash", hashlib.sha256(local).hexdigest() == row["sha256"], row["sha256"])
        checks.add(f"implementation.{row['role']}.committed_byte_equal", local == committed_bytes(row["path"]), None)

    inactive_ref = authorization["retained_inactive_validation"]
    inactive_path = ROOT / inactive_ref["path"]
    inactive = load_json(inactive_path)
    checks.add("inactive.hash", sha256_file(inactive_path) == inactive_ref["sha256"], inactive_ref["sha256"])
    checks.add("inactive.committed_byte_equal", inactive_path.read_bytes() == committed_bytes(inactive_ref["path"]), None)
    checks.add("inactive.passed", inactive["status"] == "passed" and inactive["checks_passed"] == inactive["checks_total"] == 96 and not inactive["failed_checks"], [inactive["checks_passed"], inactive["checks_total"]])
    unsigned_inactive = dict(inactive)
    observed_inactive_digest = unsigned_inactive.pop("output_digest")
    checks.add("inactive.digest", digest_value(unsigned_inactive) == observed_inactive_digest, observed_inactive_digest)
    checks.add("inactive.zero_science", all(value == 0 for value in inactive["zero_science_receipt"].values()), inactive["zero_science_receipt"])

    owner_ref = authorization["owner_acceptance_overlay"]
    owner_path = ROOT / owner_ref["path"]
    owner = load_json(owner_path)
    checks.add("owner.hash", sha256_file(owner_path) == owner_ref["sha256"], owner_ref["sha256"])
    checks.add("owner.committed_byte_equal", owner_path.read_bytes() == committed_bytes(owner_ref["path"]), None)
    checks.add("owner.accepted", owner["status"] == "owner_accepted_containing_commit_authorized" and owner["authority"]["activation_authorization_construction_after_commit_authorized"] is True, owner["status"])

    authority = authorization["authority"]
    policy = freeze["campaign_policy"]
    checks.add("policy.owner_acceptance", authority["owner_acceptance"] is True, authority["owner_acceptance"])
    checks.add("policy.one_campaign", authority["campaign_authorized"] is True and authority["campaign_invocations"] == policy["campaign_invocations"] == 1, authority["campaign_invocations"])
    checks.add("policy.zero_campaign_retry", authority["campaign_retry_limit"] == policy["campaign_retry_limit"] == 0, authority["campaign_retry_limit"])
    checks.add("policy.one_arm_attempt", authority["attempts_per_arm"] == policy["attempts_per_arm"] == 1, authority["attempts_per_arm"])
    checks.add("policy.zero_arm_retry", authority["arm_retry_limit"] == policy["arm_retry_limit"] == 0, authority["arm_retry_limit"])
    checks.add("policy.commands", authority["normalized_campaign_command"] == freeze["normalized_commands"]["campaign"] and authority["normalized_worker_command"] == freeze["normalized_commands"]["worker"] and authority["normalized_reconstruction_command"] == freeze["normalized_commands"]["reconstruction"], None)

    outputs = authorization["output_preconditions"]
    aggregate = ROOT / outputs["aggregate_path"]
    reconstruction = ROOT / outputs["reconstruction_path"]
    checks.add("outputs.match_freeze", outputs["aggregate_path"] == policy["single_aggregate_output"] and outputs["reconstruction_path"] == policy["read_only_reconstruction_output"], outputs)
    checks.add("outputs.absent", not aggregate.exists() and not reconstruction.exists(), [aggregate.exists(), reconstruction.exists()])
    checks.add("outputs.exclusive_permanent_claim", outputs["exclusive_aggregate_claim_consumes_authorization"] is True and outputs["claim_survives_failure"] is True and outputs["second_campaign_start_refused"] is True, outputs)
    checks.add("outputs.relative", all(not Path(value).is_absolute() for value in (outputs["aggregate_path"], outputs["reconstruction_path"])), outputs)

    checks.add("environment.venv", Path(sys.executable).resolve() == (ROOT / ".venv" / "bin" / "python").resolve(), ".venv/bin/python")
    environment = freeze["environment"]
    checks.add("environment.python", platform.python_version() == environment["python_version"], platform.python_version())
    checks.add("environment.interpreter", sha256_file(ROOT / ".venv" / "bin" / "python") == environment["interpreter_sha256"], environment["interpreter_sha256"])
    versions = {package: importlib.metadata.version(package) for package in environment["direct_dependencies"]}
    checks.add("environment.dependencies", versions == environment["direct_dependencies"], versions)
    checks.add("environment.commands_relative", all("/home/" not in value and "/Users/" not in value for value in freeze["normalized_commands"].values()), freeze["normalized_commands"])

    graph = freeze["graph"]
    checks.add("graph.commit", git("rev-parse", "HEAD", cwd=GRAPH_ROOT) == graph["commit"], git("rev-parse", "HEAD", cwd=GRAPH_ROOT))
    checks.add("graph.clean", git("status", "--short", cwd=GRAPH_ROOT) == "", git("status", "--short", cwd=GRAPH_ROOT))
    for row in graph["source_identities"]:
        checks.add(f"graph.source.{row['path']}", sha256_file(GRAPH_ROOT / row["path"]) == row["sha256"], row["sha256"])

    cache_files = sorted(str(path.relative_to(ROOT)) for path in (ROOT / PREFIX / "scripts" / "__pycache__").glob("p2_i2_app_a2*.pyc"))
    checks.add("isolation.no_app_a2_cache", not cache_files, cache_files)
    serialized_authority = json.dumps(authorization, sort_keys=True)
    checks.add("portability.no_absolute_paths", "/home/" not in serialized_authority and "/Users/" not in serialized_authority, None)
    checks.add("counts.zero", all(value == 0 for key, value in authorization["current_effect"].items() if key not in {"candidate_uncommitted", "activation_commit_authorized", "campaign_start_authorized"}), authorization["current_effect"])

    failed = [row["check_id"] for row in checks.rows if not row["passed"]]
    result: dict[str, Any] = {
        "artifact_id": "p2_i2_app_a2_activation_candidate_validation",
        "artifact_version": "1.0",
        "experiment_id": "2026-07-AE01",
        "iteration_id": "P2-I2-APP-A2",
        "generated_at": authorization["recorded_at"],
        "status": "passed" if not failed else "failed",
        "authorization": {"path": authorization_rel, "sha256": sha256_file(authorization_path)},
        "implementation_commit": EXPECTED_HEAD,
        "validator": {"path": PREFIX + "scripts/p2_i2_app_a2_activation_validate.py", "sha256": sha256_file(Path(__file__))},
        "checks": checks.rows,
        "checks_passed": len(checks.rows) - len(failed),
        "checks_total": len(checks.rows),
        "failed_checks": failed,
        "zero_science_receipt": {
            "pygrc_imports": 0,
            "scientific_models": 0,
            "child_arm_starts": 0,
            "scientific_gate_signatures": 0,
            "runtime_outputs_created": 0,
            "Appendix_results_assigned": 0
        },
        "authority_effect": "Candidate validation only; activation commit and campaign remain unauthorized."
    }
    result["output_digest"] = digest_value(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    if Path(args.authorization).is_absolute():
        raise AssertionError("authorization path must be relative")
    authorization_path = (ROOT / args.authorization).resolve()
    if not authorization_path.is_relative_to(ROOT):
        raise AssertionError("authorization outside repository")
    result = validate(authorization_path)
    if args.output:
        if Path(args.output).is_absolute():
            raise AssertionError("validation output path must be relative")
        output_path = (ROOT / args.output).resolve()
        if not output_path.is_relative_to(ROOT):
            raise AssertionError("validation output outside repository")
        if output_path.exists():
            raise AssertionError("validation output already exists")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(output_path, flags, 0o644)
        try:
            data = canonical_bytes(result)
            written = 0
            while written < len(data):
                written += os.write(fd, data[written:])
            os.fsync(fd)
        finally:
            os.close(fd)
    print(json.dumps({"status": result["status"], "checks_passed": result["checks_passed"], "checks_total": result["checks_total"], "output_digest": result["output_digest"]}, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
