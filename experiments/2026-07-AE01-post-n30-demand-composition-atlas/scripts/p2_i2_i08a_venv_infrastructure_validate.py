#!/usr/bin/env python3
"""Candidate-free validation of the in-place I08A active-venv child correction."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
C02 = EXPERIMENT / "contracts/p2-i2/c02"
INPUT = C02 / "i08a-venv-infrastructure-correction-input.json"
CORRECTION = C02 / "i08a-venv-infrastructure-correction.json"
TEST_RECEIPT = C02 / "i08a-venv-infrastructure-tests.json"
ACTIVATION = C02 / "owner-accepted-execution-authorization.json"
BINDING = C02 / "execution-binding-receipt.json"
MATRIX = C02 / "run-matrix.json"
OUTPUT = C02 / "i08a-venv-infrastructure-validation.json"
SOURCE = EXPERIMENT / "scripts/p2_i2_c02_execution.py"
TEST_SOURCE = EXPERIMENT / "implementation/tests/test_p2_i2_c02_execution.py"
PREFLIGHT = EXPERIMENT / "scripts/p2_i2_c02_postcommit_preflight.py"
VALIDATOR = EXPERIMENT / "scripts/p2_i2_i08a_venv_infrastructure_validate.py"


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON object required: {path.name}")
    return value


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", os.fspath(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for member in value for item in strings(member)]
    if isinstance(value, dict):
        return [item for member in value.values() for item in strings(member)]
    return []


def write_new(path: Path, document: dict[str, Any]) -> None:
    payload = (json.dumps(document, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode()
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
    except BaseException:
        if path.exists() and not path.is_symlink():
            path.unlink()
        raise


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    scripts = root / EXPERIMENT / "scripts"
    if os.fspath(scripts) not in sys.path:
        sys.path.insert(0, os.fspath(scripts))
    import p2_i2_c02_execution as c02

    if (root / OUTPUT).exists():
        raise RuntimeError("I08A venv infrastructure validation already exists")
    input_freeze = load_json(root / INPUT)
    correction = load_json(root / CORRECTION)
    test_receipt = load_json(root / TEST_RECEIPT)
    activation = load_json(root / ACTIVATION)
    binding = load_json(root / BINDING)
    matrix = load_json(root / MATRIX)
    claim = c02._safe_helpers(root)._read_governed_json(root, matrix["entries"][0]["primary_claim_path"])
    failure = c02._safe_helpers(root)._read_governed_json(root, c02._relative_failure(matrix["entries"][0], 1))
    checks: list[dict[str, Any]] = []

    def check(check_id: str, predicate: Callable[[], bool], detail: str) -> None:
        try:
            passed = bool(predicate())
            error = None
        except BaseException as exc:
            passed = False
            error = f"{type(exc).__name__}: {exc}"
        checks.append({"check_id": check_id, "passed": passed, "detail": detail, "error": error})

    expected = input_freeze["corrected_source_hashes"]
    source_text = (root / SOURCE).read_text(encoding="utf-8")
    test_text = (root / TEST_SOURCE).read_text(encoding="utf-8")
    first = matrix["entries"][0]
    helpers = c02._safe_helpers(root)
    check("I08A-VENV-01", lambda: sys.dont_write_bytecode and Path(sys.prefix).resolve() == (root / ".venv").resolve() and Path(sys.executable).absolute() == (root / ".venv/bin/python").absolute(), "validator uses exact active repository .venv")
    check("I08A-VENV-02", lambda: git(root, "rev-parse", "HEAD") == input_freeze["starting_authority"]["commit"] and git(root, "diff", "--cached", "--quiet") == "", "starting commit and index exact")
    check("I08A-VENV-03", lambda: sha256(root / SOURCE) == expected["execution_source_sha256"] and sha256(root / TEST_SOURCE) == expected["test_sha256"] and sha256(root / PREFLIGHT) == expected["postcommit_preflight_sha256"] and sha256(root / VALIDATOR) == expected["validator_sha256"], "all corrected sources match freeze")
    check("I08A-VENV-04", lambda: "Path(sys.executable).resolve()), \"-B\"" not in source_text and "os.fspath(_venv_python(root)), \"-B\"" in source_text, "worker launcher keeps lexical venv command")
    check("I08A-VENV-05", lambda: "c02._venv_python(ROOT)" in test_text and "child_sys_prefix" in test_text and "matplotlib_version" in test_text, "child regression test covers command, prefix, and dependency")
    check("I08A-VENV-06", lambda: claim["attempt"] == 1 and failure["attempt"] == 1 and failure["retry_eligibility"] is True and failure["child_attestation_present"] is True, "attempt-1 failure remains mechanically retry-eligible")
    check("I08A-VENV-07", lambda: all(value == 0 for value in failure["zero_state_counters"].values()), "all attempt-1 construction and candidate counters remain zero")
    check("I08A-VENV-08", lambda: sha256(root / first["primary_claim_path"]) == correction["predecessor_attempt"]["claim_sha256"] and sha256(root / c02._relative_failure(first, 1)) == correction["predecessor_attempt"]["failure_sha256"], "attempt-1 claim and failure bytes exact")
    check("I08A-VENV-09", lambda: correction["scope"]["new_iteration_or_cycle"] is False and correction["scope"]["scientific_change_count"] == 0 and correction["corrected_authority"]["execution_source_sha256"] == sha256(root / SOURCE), "correction is infrastructure-only and exact")
    check("I08A-VENV-10", lambda: test_receipt["status"] == "passed" and test_receipt["passed"] == 8 and test_receipt["failed"] == 0 and test_receipt["child_active_repository_venv"] is True and test_receipt["matplotlib_imported_in_child"] is True, "focused tests pass through active child venv")
    check("I08A-VENV-11", lambda: all(sha256(root / row["path"]) == row["sha256"] for row in binding["bound_files"]) and binding["bound_file_count"] == len(binding["bound_files"]), "updated live binding exact")
    check("I08A-VENV-12", lambda: activation["execution_source_sha256"] == sha256(root / SOURCE) and activation["test_sha256"] == sha256(root / TEST_SOURCE) and activation["binding_receipt_sha256"] == sha256(root / BINDING) and activation["infrastructure_correction_sha256"] == sha256(root / CORRECTION), "activation binds corrected infrastructure")
    check("I08A-VENV-13", lambda: matrix["primary_entry_count"] == 234 and matrix["scientific_projection_change_count"] == 0, "234 scientific projections unchanged")
    check("I08A-VENV-14", lambda: helpers._governed_leaf_absent(root, first["primary_output_path"]) and helpers._governed_leaf_absent(root, first["retry_claim_path"]) and helpers._governed_leaf_absent(root, first["retry_output_path"]) and helpers._governed_leaf_absent(root, c02._relative_failure(first, 2)), "attempt-2 paths remain absent")
    check("I08A-VENV-15", lambda: input_freeze["launch_audit"]["resolved_system_python_as_command_count_before"] == 3 and input_freeze["launch_audit"]["resolved_system_python_as_command_count_after"] == 0, "all three new C02 resolved-command launch sites corrected")
    check("I08A-VENV-16", lambda: not any(value.startswith("/") for value in strings(input_freeze) + strings(correction) + strings(test_receipt) + strings(activation) + strings(binding)), "machine artifacts persist no absolute paths")
    check("I08A-VENV-17", lambda: input_freeze["process_budget"]["top_level_python_starts"] == 2 and input_freeze["process_budget"]["test_child_python_starts"] == 2 and input_freeze["process_budget"]["infrastructure_retries"] == 0, "candidate-free correction process budget exact")
    check("I08A-VENV-18", lambda: not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules), "validator imports no PyGRC")
    blockers = [row["check_id"] for row in checks if not row["passed"]]
    document = {
        "artifact_id": "P2-I2-I08A-VENV-INFRASTRUCTURE-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08A",
        "cycle_id": "P2-I2-C02",
        "status": "passed_candidate_free" if not blockers else "failed_closed",
        "checks": checks,
        "check_count": len(checks),
        "passed_count": len(checks) - len(blockers),
        "blockers": blockers,
        "process_accounting": {
            "top_level_python_starts": 2,
            "test_child_python_starts": 2,
            "infrastructure_retries": 0,
            "pygrc_imports": 0,
            "models_or_adapters_constructed": 0,
            "candidate_or_control_operations": 0,
            "scientific_windows": 0
        },
        "disposition": "commit_then_exact_preflight_attempt_2" if not blockers else "stop_without_commit_or_retry",
    }
    write_new(root / OUTPUT, document)
    print(json.dumps({"passed": document["passed_count"], "total": len(checks), "blockers": blockers}, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
