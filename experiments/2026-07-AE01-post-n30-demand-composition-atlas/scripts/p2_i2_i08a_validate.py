#!/usr/bin/env python3
"""Candidate-free validation of the P2-I2 I08A/C02 successor freeze."""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import sys
from typing import Any, Callable


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
C02 = EXPERIMENT / "contracts/p2-i2/c02"
INPUT = C02 / "i08a-c02-input-freeze.json"
MATRIX = C02 / "run-matrix.json"
BINDING = C02 / "execution-binding-receipt.json"
FREEZE = C02 / "exec-freeze.json"
TEST_RECEIPT = C02 / "i08a-focused-tests-receipt.json"
OUTPUT = C02 / "i08a-candidate-free-validation.json"


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
        raise RuntimeError(f"object required: {path.name}")
    return value


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
        raise RuntimeError("I08A validation already exists")
    input_freeze = load_json(root / INPUT)
    policy = load_json(root / c02.POLICY_REL)
    matrix = load_json(root / MATRIX)
    binding = load_json(root / BINDING)
    freeze = load_json(root / FREEZE)
    test_receipt = load_json(root / TEST_RECEIPT)
    c01_audit = load_json(root / c02.C01_AUDIT_REL)
    checks: list[dict[str, Any]] = []

    def check(check_id: str, predicate: Callable[[], bool], detail: str) -> None:
        try:
            passed = bool(predicate())
            error = None
        except BaseException as exc:
            passed = False
            error = f"{type(exc).__name__}: {exc}"
        checks.append({"check_id": check_id, "passed": passed, "detail": detail, "error": error})

    check("I08A-01", lambda: sys.dont_write_bytecode and Path(sys.prefix).resolve() == (root / ".venv").resolve(), "repository .venv with -B")
    check(
        "I08A-02",
        lambda: c01_audit["status"] == "bounded_incomplete_owner_directed_successor_construction"
        and c01_audit["mechanical_disposition"]["matrix_entries_claimed"] == 1
        and c01_audit["mechanical_disposition"]["matrix_entries_evaluable"] == 0
        and sha256(root / c02.C01_CLAIM_REL) == c01_audit["retained_claim"]["sha256"],
        "C01 bounded-incomplete claim and audit are exact",
    )
    check(
        "I08A-03",
        lambda: all(sha256(root / pointer["path"]) == pointer["sha256"] for pointer in input_freeze["frozen_inputs"]),
        "all I08A frozen input hashes match",
    )
    expected = c02.translated_matrix(root)
    check("I08A-04", lambda: matrix == expected, "C02 matrix reconstructs exactly from C01")
    check(
        "I08A-05",
        lambda: matrix["primary_entry_count"] == 234
        and len(matrix["entries"]) == 234
        and len({row["entry_id"] for row in matrix["entries"]}) == 234
        and matrix["scientific_projection_change_count"] == 0,
        "C02 retains all 234 unique scientific projections",
    )
    check(
        "I08A-06",
        lambda: policy["resource_envelope_per_worker"]["address_space_limit"] is None
        and policy["resource_envelope_per_worker"]["RLIMIT_AS_applied"] is False
        and policy["resource_envelope_per_worker"]["max_runtime_seconds"] == 180
        and policy["resource_envelope_per_worker"]["max_file_size_mb"] == 512,
        "only address-space enforcement is removed",
    )
    source_text = (root / c02.SOURCE_REL).read_text(encoding="utf-8")
    check(
        "I08A-07",
        lambda: "resource.setrlimit(resource.RLIMIT_AS" not in source_text
        and "resource.setrlimit(resource.RLIMIT_FSIZE" in source_text,
        "source applies file-size but no address-space limit",
    )
    check(
        "I08A-08",
        lambda: all(sha256(root / pointer["path"]) == pointer["sha256"] for pointer in binding["bound_files"])
        and binding["bound_file_count"] == len(binding["bound_files"]),
        "C02 binding reconstructs every bound file",
    )
    check(
        "I08A-09",
        lambda: freeze["cycle_id"] == "P2-I2-C02"
        and freeze["candidate_execution_authorized"] is False
        and freeze["I08_authorized"] is False
        and freeze["activation_record_present"] is False
        and freeze["scientific_projection_change_count"] == 0,
        "C02 freeze remains exact and inactive",
    )
    check(
        "I08A-10",
        lambda: policy["supervisor_contract"]["claim_owner"] == "external_supervisor"
        and policy["supervisor_contract"]["failure_receipt_owner"] == "external_supervisor"
        and policy["supervisor_contract"]["native_or_unattested_failure_retryable"] is False
        and '"retry_unknown_phase_is_refused": not attested_failure' in source_text,
        "native worker termination remains outside evidence-loss boundary",
    )
    check(
        "I08A-11",
        lambda: test_receipt["status"] == "passed"
        and test_receipt["passed"] == 8
        and test_receipt["failed"] == 0
        and test_receipt["native_exit_child_process_starts"] == 1
        and test_receipt["success_attestation_child_process_starts"] == 1,
        "focused tests and child-process accounting pass",
    )
    check(
        "I08A-12",
        lambda: len(
            {
                path
                for row in matrix["entries"]
                for path in (
                    row["primary_claim_path"], row["retry_claim_path"],
                    row["primary_output_path"], row["retry_output_path"],
                    c02._relative_failure(row, 1), c02._relative_failure(row, 2),
                )
            }
        )
        == 1404,
        "all 1,404 C02 governed paths are unique",
    )
    check(
        "I08A-13",
        lambda: not any(
            value.startswith("/")
            for value in strings(input_freeze) + strings(policy) + strings(matrix) + strings(binding) + strings(freeze) + strings(test_receipt)
        ),
        "C02 machine artifacts persist no absolute paths",
    )
    check(
        "I08A-14",
        lambda: not (root / c02.ACTIVATION_REL).exists()
        and not (root / c02.OUTPUT_ROOT_REL).exists()
        and not (root / c02.MANIFEST_REL).exists(),
        "C02 activation, outputs, and manifest remain absent",
    )
    check(
        "I08A-15",
        lambda: policy["cross_entry_isolation"]["fresh_worker_process_per_attempt"] is True
        and policy["cross_entry_isolation"]["parallel_workers"] == 0
        and policy["cross_entry_isolation"]["prior_entry_result_reads"] is False,
        "fresh-process cross-entry isolation is retained",
    )
    check(
        "I08A-16",
        lambda: policy["retry_policy"]["requires_child_attestation"] is True
        and policy["retry_policy"]["unknown_phase_retryable"] is False
        and policy["retry_policy"]["scientific_or_control_outcome_retryable"] is False,
        "receipt-derived retry remains conservative",
    )
    check(
        "I08A-17",
        lambda: not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules),
        "I08A validation imports no PyGRC",
    )
    check(
        "I08A-18",
        lambda: input_freeze["process_budget"]["top_level_python_starts"] == 3
        and input_freeze["process_budget"]["test_child_python_starts"] == 2
        and input_freeze["process_budget"]["infrastructure_retries"] == 0,
        "I08A process budget is exact",
    )
    blockers = [row["check_id"] for row in checks if not row["passed"]]
    document = {
        "artifact_id": "P2-I2-I08A-CANDIDATE-FREE-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08A",
        "cycle_id": "P2-I2-C02",
        "status": "passed_candidate_free" if not blockers else "failed_closed",
        "checks": checks,
        "check_count": len(checks),
        "passed_count": len(checks) - len(blockers),
        "blockers": blockers,
        "process_accounting": {
            "top_level_python_starts": 3,
            "test_child_python_starts": 2,
            "infrastructure_retries": 0,
            "pygrc_imports": 0,
            "models_or_adapters_constructed": 0,
            "candidate_or_control_operations": 0,
            "scientific_windows": 0
        },
        "disposition": "return_uncommitted_for_owner_review" if not blockers else "stop_for_owner_direction",
    }
    write_new(root / OUTPUT, document)
    print(json.dumps({"passed": document["passed_count"], "total": len(checks), "blockers": blockers}, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
