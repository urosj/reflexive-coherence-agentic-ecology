#!/usr/bin/env python3
"""Candidate-free validation of the inactive P2-I2 I08 activation package."""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Callable


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
C01 = EXPERIMENT / "contracts/p2-i2/c01"
OUTPUT = C01 / "i08-preactivation-validation.json"
ACTIVATION = C01 / "owner-accepted-execution-authorization.json"
INPUT_FREEZE = C01 / "i08-activation-input-freeze.json"
CLEANUP_RECEIPT = C01 / "i08-import-cache-cleanup-receipt.json"
EXPECTED_HEAD = "5c2c248647e78526474210649c0a7ba84fcef13d"
EXPECTED_GRAPH_HEAD = "83e3a300426631ee4df71b661b67d4fcfdfed594"

TECHNICAL_HASHES = {
    "inactive_exec_freeze_sha256": (C01 / "exec-freeze.json", "8e4533d37f3de3140dca84aaf3683989988d25a79fcc4aff4e88ca686a90ab22"),
    "policy_sha256": (EXPERIMENT / "configs/p2_i2_c01_execution_policy_v2.json", "773b9fc231942f59e7d5b74a49ad8ce722471badcc554afd74d5cfaadb4327d3"),
    "execution_source_sha256": (EXPERIMENT / "scripts/p2_i2_execution.py", "9a92d90997ba80a0ae626fcfe3549fb77a49c108b9c4e84149aecf35fb1336fe"),
    "validator_sha256": (EXPERIMENT / "scripts/p2_i2_i07a_validate.py", "e304b542a2e4d0b350c3605e376caaad306e7dfa878f65b97eaf8379cb54a162"),
    "test_sha256": (EXPERIMENT / "implementation/tests/test_p2_i2_execution_freeze.py", "22df990af1d4d45729263e5740cc41b2990819fab8e3d64a2ed138eb19846420"),
    "resumption_freeze_sha256": (C01 / "i07-candidate-cycle-resumption-input-freeze.json", "c73b4c814a33bfd80c3fbb072928b4f4f9f59de5ba9dbe3bf8c424526a261c98"),
    "i07a_validation_sha256": (C01 / "i07a-candidate-free-validation.json", "32f69dadc8cd10db3bb57fa7f837be921f91da2315369b2842e37d2737d9997c"),
    "i07a_input_freeze_sha256": (C01 / "i07a-cross-entry-isolation-input-freeze.json", "d375f66e6d739ddcaad159bb6f29e82b7e2fcbb28bc74e14d24c7e30c9a2c93b"),
    "run_matrix_sha256": (C01 / "run-matrix.json", "5e9130bddb3fc888a8376100dcfccc4984a4435310cd0432e5096d29629cd427"),
    "binding_receipt_sha256": (C01 / "execution-binding-receipt.json", "99a474836b25014b31a887861c065e568a91d5ad2a0a58338cffc14aceb64479"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise RuntimeError(f"expected object: {path.name}")
    return value


def git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", os.fspath(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def committed_sha256(repository: Path, revision: str, relative: Path) -> str:
    payload = subprocess.run(
        ["git", "-C", os.fspath(repository), "show", f"{revision}:{relative.as_posix()}"],
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(payload).hexdigest()


def cache_inventory(label: str, root: Path) -> list[str]:
    found: list[str] = []
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        relative = current_path.relative_to(root)
        for directory in directories:
            if directory == "__pycache__":
                found.append(f"{label}:{(relative / directory).as_posix()}:cache_directory")
        for name in files:
            if name.endswith((".pyc", ".pyo")):
                found.append(f"{label}:{(relative / name).as_posix()}:bytecode_file")
    return sorted(found)


def strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for member in value for item in strings(member)]
    if isinstance(value, dict):
        return [item for member in value.values() for item in strings(member)]
    return []


def write_new(path: Path, document: dict[str, Any]) -> None:
    payload = json.dumps(document, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
    except BaseException:
        if path.exists() and not path.is_symlink():
            path.unlink()
        raise


def main() -> int:
    repository = Path(__file__).resolve().parents[3]
    graph = (repository / "../graph-reflexive-coherence").resolve()
    if (repository / OUTPUT).exists():
        raise RuntimeError("I08 preactivation validation already exists")
    activation = load_json(repository / ACTIVATION)
    input_freeze = load_json(repository / INPUT_FREEZE)
    cleanup = load_json(repository / CLEANUP_RECEIPT)
    matrix = load_json(repository / C01 / "run-matrix.json")
    resumption = load_json(repository / C01 / "i07-candidate-cycle-resumption-input-freeze.json")
    checks: list[dict[str, Any]] = []

    def check(check_id: str, predicate: Callable[[], bool], detail: str) -> None:
        try:
            passed = bool(predicate())
            error = None
        except BaseException as exc:
            passed = False
            error = f"{type(exc).__name__}: {exc}"
        checks.append({"check_id": check_id, "passed": passed, "detail": detail, "error": error})

    check("I08-PRE-01", lambda: sys.dont_write_bytecode, ".venv Python runs with -B")
    check(
        "I08-PRE-02",
        lambda: Path(sys.prefix).resolve() == (repository / ".venv").resolve()
        and sha256(Path(sys.executable).resolve()) == resumption["runtime_identity"]["interpreter_executable_sha256"],
        "repository .venv and frozen interpreter digest match",
    )
    check("I08-PRE-03", lambda: git(repository, "rev-parse", "HEAD") == EXPECTED_HEAD, "accepted parent HEAD matches")
    check("I08-PRE-04", lambda: git(repository, "diff", "--cached", "--quiet") == "", "index is clean")
    check(
        "I08-PRE-05",
        lambda: all(
            sha256(repository / relative) == expected
            and committed_sha256(repository, EXPECTED_HEAD, relative) == expected
            for relative, expected in TECHNICAL_HASHES.values()
        ),
        "all accepted live technical bytes equal the accepted commit",
    )
    check(
        "I08-PRE-06",
        lambda: git(graph, "rev-parse", "HEAD") == EXPECTED_GRAPH_HEAD
        and git(graph, "status", "--porcelain", "--untracked-files=no") == "",
        "graph revision and tracked worktree match",
    )
    check(
        "I08-PRE-07",
        lambda: sha256(graph / "src/pygrc/models/lgrc_9_v3_runtime.py")
        == resumption["runtime_identity"]["runtime_source_sha256"],
        "graph runtime source digest matches",
    )
    check(
        "I08-PRE-08",
        lambda: cleanup["status"] == "complete_candidate_free"
        and cleanup["before_count"] > 0
        and cleanup["after_count"] == 0
        and cleanup["tracked_bytes_changed"] == 0,
        "cache cleanup receipt retains nonempty before and zero after inventory",
    )
    check(
        "I08-PRE-09",
        lambda: not cache_inventory("experiment_scripts", repository / EXPERIMENT / "scripts")
        and not cache_inventory("pygrc_source", graph / "src"),
        "both frozen live import roots are cache-free",
    )
    check(
        "I08-PRE-10",
        lambda: activation["artifact_id"] == "P2-I2-C01-OWNER-ACCEPTED-EXECUTION-AUTHORIZATION"
        and activation["cycle_id"] == "P2-I2-C01"
        and activation["owner_acceptance"] is False
        and activation["candidate_execution_authorized"] is False
        and activation["I08_authorized"] is False,
        "activation candidate is exact kind and remains inactive",
    )
    check(
        "I08-PRE-11",
        lambda: all(activation[key] == expected for key, (_, expected) in TECHNICAL_HASHES.items()),
        "activation candidate binds every live-validator technical hash",
    )
    check(
        "I08-PRE-12",
        lambda: activation["expected_head_source"]
        == "separately_owner_authorized_normalized_command_argument"
        and activation["activation_commit_head"] is None,
        "activation avoids self-referential HEAD",
    )
    check(
        "I08-PRE-13",
        lambda: input_freeze["starting_authority"]["commit"] == EXPECTED_HEAD
        and input_freeze["process_budget"]["candidate_free_python_starts"] == 2
        and input_freeze["process_budget"]["infrastructure_retries"] == 0,
        "input freeze binds accepted start and exact preparation budget",
    )
    entries = matrix["entries"]
    check(
        "I08-PRE-14",
        lambda: matrix["primary_entry_count"] == 234
        and len(entries) == 234
        and [entry["sequence_index"] for entry in entries] == list(range(1, 235))
        and len({entry["entry_id"] for entry in entries}) == 234,
        "matrix has exactly 234 unique entries in complete frozen order",
    )
    check(
        "I08-PRE-15",
        lambda: len(
            {
                path
                for entry in entries
                for path in (
                    entry["primary_claim_path"],
                    entry["retry_claim_path"],
                    entry["primary_output_path"],
                    entry["retry_output_path"],
                )
            }
        )
        == 936,
        "all frozen claim and output paths are unique",
    )
    check(
        "I08-PRE-16",
        lambda: not (repository / EXPERIMENT / "outputs/p2-i2/c01").exists()
        and not (repository / C01 / "execution-manifest.json").exists(),
        "governed output root and execution manifest are absent",
    )
    check(
        "I08-PRE-17",
        lambda: not any(value.startswith("/") for value in strings(input_freeze) + strings(activation) + strings(cleanup)),
        "new machine artifacts persist no absolute paths",
    )
    check(
        "I08-PRE-18",
        lambda: not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules),
        "candidate-free validation imports no PyGRC",
    )
    blockers = [item["check_id"] for item in checks if not item["passed"]]
    document = {
        "artifact_id": "P2-I2-I08-PREACTIVATION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08",
        "cycle_id": "P2-I2-C01",
        "status": "passed_candidate_free" if not blockers else "failed_closed",
        "checks": checks,
        "check_count": len(checks),
        "passed_count": len(checks) - len(blockers),
        "blockers": blockers,
        "process_accounting": {
            "candidate_free_python_starts": 2,
            "infrastructure_retries": 0,
            "pygrc_imports": 0,
            "models_or_adapters_constructed": 0,
            "candidate_or_control_operations": 0,
            "scientific_windows": 0,
        },
        "disposition": "return_uncommitted_for_owner_review" if not blockers else "stop_for_owner_direction",
    }
    write_new(repository / OUTPUT, document)
    print(json.dumps({"passed": document["passed_count"], "total": len(checks), "blockers": blockers}, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
