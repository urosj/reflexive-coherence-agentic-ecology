#!/usr/bin/env python3
"""Candidate-free validation of the owner-accepted P2-I2 C02 activation."""

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
INPUT = C02 / "i08a-activation-input-freeze.json"
ACTIVATION = C02 / "owner-accepted-execution-authorization.json"
OUTPUT = C02 / "i08a-activation-validation.json"
CURRENT_HEAD = "c265279b2690fbd262e59248b0d84bfa3dc81ba1"


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


def cache_inventory(label: str, base: Path) -> list[str]:
    found: list[str] = []
    for current, directories, files in os.walk(base, followlinks=False):
        relative = Path(current).relative_to(base)
        for directory in directories:
            if directory == "__pycache__":
                found.append(f"{label}:{(relative / directory).as_posix()}")
        for name in files:
            if name.endswith((".pyc", ".pyo")):
                found.append(f"{label}:{(relative / name).as_posix()}")
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
    graph = (root / "../graph-reflexive-coherence").resolve()
    if (root / OUTPUT).exists():
        raise RuntimeError("C02 activation validation already exists")
    input_freeze = load_json(root / INPUT)
    activation = load_json(root / ACTIVATION)
    matrix = load_json(root / C02 / "run-matrix.json")
    freeze = load_json(root / C02 / "exec-freeze.json")
    checks: list[dict[str, Any]] = []

    def check(check_id: str, predicate: Callable[[], bool], detail: str) -> None:
        try:
            passed = bool(predicate())
            error = None
        except BaseException as exc:
            passed = False
            error = f"{type(exc).__name__}: {exc}"
        checks.append({"check_id": check_id, "passed": passed, "detail": detail, "error": error})

    reviewed = input_freeze["reviewed_package"]
    technical = input_freeze["live_technical_hashes"]
    runtime = input_freeze["runtime_identity"]
    check("I08A-ACT-01", lambda: sys.dont_write_bytecode and Path(sys.prefix).resolve() == (root / ".venv").resolve(), "repository .venv with -B")
    check("I08A-ACT-02", lambda: git(root, "rev-parse", "HEAD") == CURRENT_HEAD, "accepted starting HEAD")
    check("I08A-ACT-03", lambda: git(root, "diff", "--cached", "--quiet") == "", "index clean before activation commit")
    check("I08A-ACT-04", lambda: all(sha256(root / row["path"]) == row["sha256"] for row in reviewed), "reviewed I08A package hashes exact")
    check("I08A-ACT-05", lambda: matrix["primary_entry_count"] == 234 and len(matrix["entries"]) == 234 and matrix["scientific_projection_change_count"] == 0, "234 unchanged scientific projections")
    check("I08A-ACT-06", lambda: freeze["candidate_execution_authorized"] is False and freeze["I08_authorized"] is False and freeze["activation_record_present"] is False, "inactive freeze remains immutable")
    check(
        "I08A-ACT-07",
        lambda: activation["artifact_id"] == "P2-I2-C02-OWNER-ACCEPTED-EXECUTION-AUTHORIZATION"
        and activation["cycle_id"] == "P2-I2-C02"
        and activation["owner_acceptance"] is True
        and activation["candidate_execution_authorized"] is True
        and activation["I08_authorized"] is True
        and activation["commit_authorized"] is True,
        "owner-accepted activation fields exact",
    )
    check("I08A-ACT-08", lambda: all(activation[key] == value for key, value in technical.items()), "activation binds every live technical hash")
    check("I08A-ACT-09", lambda: activation["activation_commit_head"] is None and activation["expected_head_source"] == "separately_owner_authorized_normalized_command_argument", "activation avoids self-reference")
    check("I08A-ACT-10", lambda: activation["acceptance_authority"]["decision_id"] == "P2-I2-DEC-051" and activation["acceptance_authority"]["change_id"] == "P2-I2-CHG-048", "owner acceptance authority exact")
    check("I08A-ACT-11", lambda: sha256(root / INPUT) == activation["preparation_bindings"]["activation_input_freeze_sha256"], "activation input freeze bound")
    check("I08A-ACT-12", lambda: sha256(Path(sys.executable).resolve()) == runtime["interpreter_executable_sha256"], "interpreter digest exact")
    check("I08A-ACT-13", lambda: git(graph, "rev-parse", "HEAD") == runtime["graph_revision"] and git(graph, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph revision and worktree exact")
    check("I08A-ACT-14", lambda: sha256(graph / runtime["runtime_source_relative"]) == runtime["runtime_source_sha256"], "graph runtime source exact")
    check("I08A-ACT-15", lambda: not cache_inventory("experiment_scripts", root / EXPERIMENT / "scripts") and not cache_inventory("pygrc_source", graph / "src"), "live import roots cache-free")
    check("I08A-ACT-16", lambda: not (root / EXPERIMENT / "outputs/p2-i2/c02").exists() and not (root / C02 / "execution-manifest.json").exists(), "C02 outputs and manifest absent")
    check("I08A-ACT-17", lambda: not any(value.startswith("/") for value in strings(input_freeze) + strings(activation)), "activation artifacts contain no absolute paths")
    check("I08A-ACT-18", lambda: input_freeze["process_budget"]["candidate_free_activation_validation_starts"] == 1 and input_freeze["process_budget"]["infrastructure_retries"] == 0, "activation validation budget exact")
    check("I08A-ACT-19", lambda: not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules), "activation validation imports no PyGRC")
    blockers = [row["check_id"] for row in checks if not row["passed"]]
    document = {
        "artifact_id": "P2-I2-I08A-C02-ACTIVATION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08A",
        "cycle_id": "P2-I2-C02",
        "status": "passed_candidate_free" if not blockers else "failed_closed",
        "checks": checks,
        "check_count": len(checks),
        "passed_count": len(checks) - len(blockers),
        "blockers": blockers,
        "process_accounting": {
            "candidate_free_python_starts": 1,
            "infrastructure_retries": 0,
            "pygrc_imports": 0,
            "models_or_adapters_constructed": 0,
            "candidate_or_control_operations": 0,
            "scientific_windows": 0
        },
        "disposition": "commit_authorized_package_ready" if not blockers else "stop_without_commit_or_execution",
    }
    write_new(root / OUTPUT, document)
    print(json.dumps({"passed": document["passed_count"], "total": len(checks), "blockers": blockers}, sort_keys=True))
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
