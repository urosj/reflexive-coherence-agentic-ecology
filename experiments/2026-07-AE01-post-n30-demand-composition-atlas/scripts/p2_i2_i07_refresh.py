#!/usr/bin/env python3
"""Refresh only I07 derived binding hashes after the owner-directed pytest install."""

from __future__ import annotations

import ast
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Mapping


EXPERIMENT_REL = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SOURCE_REL = EXPERIMENT_REL / "scripts" / "p2_i2_execution.py"
VALIDATOR_REL = EXPERIMENT_REL / "scripts" / "p2_i2_i07_validate.py"
TEST_REL = EXPERIMENT_REL / "implementation" / "tests" / "test_p2_i2_execution_freeze.py"
POLICY_REL = EXPERIMENT_REL / "configs" / "p2_i2_c01_execution_policy_v2.json"
CONTINUATION_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-dependency-install-and-validation-continuation.json"
ENVIRONMENT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-pytest-environment-receipt.json"
RECEIPT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-binding-refresh-receipt.json"


ORIGINAL = {
    "policy": "9a0649f18e99dff3c3f5bc7f8927ea8b369adde17e5160013a508e045c7d047e",
    "source": "42b8486908831a928535f9594c7a15cc0d634c0025391d28ce32fc3b75fb6a61",
    "test": "927f48c72e96bb6a8a49cd683a5c581d26de12a3435aebb02c6d585cd29f6ea2",
    "matrix": "57953a5fc93e8e05a95cdb7ca260c72bc28ea9388fd0804b064c1279ce8c48e8",
    "binding": "9e85703bbb055758c15c6082a28fb1ec4d8e9f08323ffa82db31c866d3141a1d",
    "freeze": "d416750ed938a3e2307a4e9d2d8fa586b8322c63d3c9e392f104718f60e35ff8",
}


def root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = root()


def load_execution():
    spec = importlib.util.spec_from_file_location("p2_i2_execution_i07_refresh", ROOT / SOURCE_REL)
    if spec is None or spec.loader is None:
        raise RuntimeError("execution source import specification unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


execution = load_execution()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path.name}")
    return value


def atomic_replace(path: Path, value: Mapping[str, Any]) -> None:
    temporary = path.with_name(path.name + ".i07-refresh-tmp")
    require(not temporary.exists() and not temporary.is_symlink(), "refresh temporary path occupied")
    with temporary.open("xb") as handle:
        handle.write(execution.pretty_bytes(value))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def normalized_freeze(value: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop("canonical_payload_digest", None)
    identity = result["bound_identity"]
    for key in (
        "validator_sha256",
        "binding_receipt_file_sha256",
        "binding_receipt_payload_digest",
    ):
        identity[key] = "<DERIVED_REFRESH_FIELD>"
    return result


def main() -> int:
    continuation = load_json(ROOT / CONTINUATION_REL)
    environment = load_json(ROOT / ENVIRONMENT_REL)
    require(continuation["authority"]["decision_id"] == "P2-I2-DEC-045", "continuation authority drift")
    require(environment["status"] == "owner_authorized_repository_venv_dependency_installed", "pytest installation receipt absent")
    require(execution.sha256(ROOT / POLICY_REL) == ORIGINAL["policy"], "execution policy changed")
    require(execution.sha256(ROOT / SOURCE_REL) == ORIGINAL["source"], "execution source changed")
    require(execution.sha256(ROOT / TEST_REL) == ORIGINAL["test"], "focused tests changed")
    ast.parse((ROOT / SOURCE_REL).read_text(encoding="utf-8"))
    ast.parse((ROOT / TEST_REL).read_text(encoding="utf-8"))
    ast.parse((ROOT / VALIDATOR_REL).read_text(encoding="utf-8"))
    require(
        all(execution.sha256(ROOT / row["metadata_path"]) == row["metadata_sha256"] for row in environment["resolved_packages"]),
        "installed pytest environment metadata drift",
    )

    policy = load_json(ROOT / POLICY_REL)
    artifacts = policy["artifact_contract"]
    matrix_path = ROOT / artifacts["run_matrix_path"]
    binding_path = ROOT / artifacts["binding_receipt_path"]
    freeze_path = ROOT / artifacts["exec_freeze_path"]
    require(execution.sha256(matrix_path) == ORIGINAL["matrix"], "run matrix changed")
    require(execution.sha256(binding_path) == ORIGINAL["binding"], "original binding is not exact")
    require(execution.sha256(freeze_path) == ORIGINAL["freeze"], "original inactive freeze is not exact")
    require(not (ROOT / RECEIPT_REL).exists(), "refresh receipt already exists")

    effective, _, _ = execution.load_effective_policy(ROOT)
    matrix = load_json(matrix_path)
    rebuilt_matrix = execution._matrix_document(execution.expand_run_matrix(effective))
    require(matrix == rebuilt_matrix, "run matrix no longer reconstructs")
    old_binding = load_json(binding_path)
    old_freeze = load_json(freeze_path)
    new_binding = execution._binding_document(ROOT, matrix)
    old_rows = {row["role"]: row for row in old_binding["bound_files"]}
    new_rows = {row["role"]: row for row in new_binding["bound_files"]}
    require(old_rows.keys() == new_rows.keys(), "binding role set changed")
    for role in old_rows:
        if role != "candidate_free_validator":
            require(old_rows[role] == new_rows[role], f"non-validator binding changed: {role}")
    require(old_rows["candidate_free_validator"]["path"] == new_rows["candidate_free_validator"]["path"], "validator path changed")
    require(old_rows["candidate_free_validator"]["sha256"] != new_rows["candidate_free_validator"]["sha256"], "validator accounting was not updated")

    atomic_replace(binding_path, new_binding)
    new_freeze = execution._exec_freeze_document(ROOT, matrix, new_binding)
    require(normalized_freeze(old_freeze) == normalized_freeze(new_freeze), "inactive freeze changed beyond derived validation bindings")
    atomic_replace(freeze_path, new_freeze)

    receipt = {
        "artifact_id": "P2-I2-I07-BINDING-REFRESH-RECEIPT",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I07",
        "lane_id": "AE01-L02",
        "refreshed_at": "2026-07-15",
        "status": "candidate_free_derived_binding_refresh_complete",
        "authority": {"decision_id": "P2-I2-DEC-045", "change_id": "P2-I2-CHG-040"},
        "preserved": {
            "policy_sha256": ORIGINAL["policy"],
            "execution_source_sha256": ORIGINAL["source"],
            "focused_tests_sha256": ORIGINAL["test"],
            "run_matrix_sha256": ORIGINAL["matrix"],
            "run_matrix_semantic_digest": matrix["semantic_digest"],
            "primary_entry_count": matrix["primary_entry_count"],
        },
        "historical": {
            "original_binding_receipt_sha256": ORIGINAL["binding"],
            "original_inactive_exec_freeze_sha256": ORIGINAL["freeze"],
        },
        "refreshed": {
            "validator_sha256": execution.sha256(ROOT / VALIDATOR_REL),
            "binding_receipt_sha256": execution.sha256(binding_path),
            "inactive_exec_freeze_sha256": execution.sha256(freeze_path),
        },
        "process_counters": {
            "pygrc_imports": 0,
            "models_constructed": 0,
            "packets_scheduled_or_processed": 0,
            "candidate_or_control_operations": 0,
            "scientific_evidence": False,
        },
        "gate_boundary": {
            "candidate_execution_authorized": False,
            "EXEC_FREEZE": "closed",
            "I08_authorized": False,
            "commit_authorized": False,
        },
    }
    execution.write_new(ROOT / RECEIPT_REL, receipt)
    print(json.dumps(receipt["refreshed"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
