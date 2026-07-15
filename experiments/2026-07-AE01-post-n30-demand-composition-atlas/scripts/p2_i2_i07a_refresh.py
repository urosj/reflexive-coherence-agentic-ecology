#!/usr/bin/env python3
"""Candidate-free I07A refresh of the matrix, binding, and inactive freeze."""

from __future__ import annotations

import ast
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping


EXPERIMENT_REL = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SOURCE_REL = EXPERIMENT_REL / "scripts" / "p2_i2_execution.py"
VALIDATOR_REL = EXPERIMENT_REL / "scripts" / "p2_i2_i07a_validate.py"
TEST_REL = EXPERIMENT_REL / "implementation" / "tests" / "test_p2_i2_execution_freeze.py"
POLICY_REL = EXPERIMENT_REL / "configs" / "p2_i2_c01_execution_policy_v2.json"
INPUT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-cross-entry-isolation-input-freeze.json"
RECEIPT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-derived-refresh-receipt.json"

ORIGINAL = {
    "policy": "9a0649f18e99dff3c3f5bc7f8927ea8b369adde17e5160013a508e045c7d047e",
    "source": "42b8486908831a928535f9594c7a15cc0d634c0025391d28ce32fc3b75fb6a61",
    "test": "927f48c72e96bb6a8a49cd683a5c581d26de12a3435aebb02c6d585cd29f6ea2",
    "matrix": "57953a5fc93e8e05a95cdb7ca260c72bc28ea9388fd0804b064c1279ce8c48e8",
    "binding": "c73276a0de176ce250691fbc03740a9011d938ea46acbf46510bcf5fed9811e6",
    "freeze": "c703eca51bc6155f44c5a3164c938361285b1f11dda506515fd4bc2fd4c93f1d",
}


def root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = root()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path.name}")
    return value


def load_execution():
    spec = importlib.util.spec_from_file_location("p2_i2_execution_i07a_refresh", ROOT / SOURCE_REL)
    if spec is None or spec.loader is None:
        raise RuntimeError("execution source import specification unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


execution = load_execution()


def atomic_replace(path: Path, value: Mapping[str, Any]) -> None:
    temporary = path.with_name(path.name + ".i07a-refresh-tmp")
    require(not temporary.exists() and not temporary.is_symlink(), "I07A refresh temporary path occupied")
    with temporary.open("xb") as handle:
        handle.write(execution.pretty_bytes(value))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def main() -> int:
    require(sys.dont_write_bytecode is True, "I07A refresh requires .venv/bin/python -B")
    require(not (ROOT / RECEIPT_REL).exists() and not (ROOT / RECEIPT_REL).is_symlink(), "I07A refresh receipt already exists")
    input_freeze = load_json(ROOT / INPUT_REL)
    require(input_freeze["authority"]["decision_id"] == "P2-I2-DEC-046", "I07A decision authority drift")
    require(input_freeze["authority"]["change_id"] == "P2-I2-CHG-042", "I07A change authority drift")
    reviewed = {row["role"]: row["sha256"] for row in input_freeze["reviewed_i07_inputs"]}
    require(reviewed["reviewed_effective_policy"] == ORIGINAL["policy"], "reviewed policy identity drift")
    require(reviewed["reviewed_execution_source"] == ORIGINAL["source"], "reviewed source identity drift")
    require(reviewed["reviewed_focused_tests"] == ORIGINAL["test"], "reviewed test identity drift")
    require(reviewed["reviewed_run_matrix"] == ORIGINAL["matrix"], "reviewed matrix identity drift")
    require(reviewed["reviewed_execution_binding"] == ORIGINAL["binding"], "reviewed binding identity drift")
    require(reviewed["reviewed_inactive_exec_freeze"] == ORIGINAL["freeze"], "reviewed freeze identity drift")
    require(execution.sha256(ROOT / INPUT_REL) == "d375f66e6d739ddcaad159bb6f29e82b7e2fcbb28bc74e14d24c7e30c9a2c93b", "I07A input freeze drift")
    for relative in (SOURCE_REL, VALIDATOR_REL, TEST_REL):
        ast.parse((ROOT / relative).read_text(encoding="utf-8"))
    require(not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules), "candidate runtime imported during refresh")

    policy = load_json(ROOT / POLICY_REL)
    require(policy["iteration_id"] == "P2-I2-I07A", "corrected policy iteration drift")
    require(policy["runtime_invocation_identity"]["python_flags"] == ["-B"], "live cache flag absent")
    require(policy["retry_policy"]["shared_retry_ledger"] is False, "shared retry ledger remains active")
    require(policy["completion_policy"]["execution_manifest_created_only_after_all_234_evaluable"] is True, "completion rule absent")
    artifacts = policy["artifact_contract"]
    matrix_path = ROOT / artifacts["run_matrix_path"]
    binding_path = ROOT / artifacts["binding_receipt_path"]
    freeze_path = ROOT / artifacts["exec_freeze_path"]
    require(execution.sha256(matrix_path) == ORIGINAL["matrix"], "reviewed matrix is not exact before refresh")
    require(execution.sha256(binding_path) == ORIGINAL["binding"], "reviewed binding is not exact before refresh")
    require(execution.sha256(freeze_path) == ORIGINAL["freeze"], "reviewed freeze is not exact before refresh")
    require(not (ROOT / artifacts["activation_record_path"]).exists(), "activation must remain absent")
    require(not (ROOT / artifacts["execution_manifest_path"]).exists(), "execution manifest must remain absent")
    require(not (ROOT / execution.OUTPUT_ROOT_REL).exists(), "candidate output root must remain absent")

    old_matrix = load_json(matrix_path)
    effective, _, _ = execution.load_effective_policy(ROOT)
    new_matrix = execution._matrix_document(execution.expand_run_matrix(effective))
    require(old_matrix["entries"] == new_matrix["entries"], "I07A changed a matrix row")
    require(old_matrix["primary_entry_count"] == new_matrix["primary_entry_count"] == 234, "matrix count changed")
    require(old_matrix["maximum_conditional_retry_count"] == new_matrix["maximum_conditional_retry_count"] == 234, "retry ceiling changed")
    new_binding = execution._binding_document(ROOT, new_matrix)

    atomic_replace(matrix_path, new_matrix)
    atomic_replace(binding_path, new_binding)
    new_freeze = execution._exec_freeze_document(ROOT, new_matrix, new_binding)
    atomic_replace(freeze_path, new_freeze)

    receipt = {
        "artifact_id": "P2-I2-I07A-DERIVED-REFRESH-RECEIPT",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I07A",
        "lane_id": "AE01-L02",
        "refreshed_at": "2026-07-15",
        "status": "candidate_free_isolation_correction_refresh_complete",
        "authority": {"decision_id": "P2-I2-DEC-046", "change_id": "P2-I2-CHG-042"},
        "historical_reviewed_hashes": ORIGINAL,
        "corrected_hashes": {
            "policy_sha256": execution.sha256(ROOT / POLICY_REL),
            "execution_source_sha256": execution.sha256(ROOT / SOURCE_REL),
            "validator_sha256": execution.sha256(ROOT / VALIDATOR_REL),
            "focused_tests_sha256": execution.sha256(ROOT / TEST_REL),
            "run_matrix_sha256": execution.sha256(matrix_path),
            "binding_receipt_sha256": execution.sha256(binding_path),
            "inactive_exec_freeze_sha256": execution.sha256(freeze_path),
        },
        "matrix_projection": {
            "entries_byte_semantic_unchanged": old_matrix["entries"] == new_matrix["entries"],
            "primary_entry_count": 234,
            "conditional_retry_ceiling": 234,
            "old_semantic_digest": old_matrix["semantic_digest"],
            "corrected_semantic_digest": new_matrix["semantic_digest"],
        },
        "process_ledger": {
            "start_index": 1,
            "python_command": [".venv/bin/python", "-B", "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i07a_refresh.py"],
            "status": "passed",
            "infrastructure_retries": 0,
            "pygrc_imports": 0,
            "models_constructed": 0,
            "candidate_or_control_operations": 0,
            "scientific_windows": 0,
        },
        "gate_boundary": {
            "candidate_execution_authorized": False,
            "P2-I2-EXEC-FREEZE": "closed",
            "I08_authorized": False,
            "commit_authorized": False,
        },
    }
    execution.write_new(ROOT / RECEIPT_REL, receipt)
    print(json.dumps(receipt["corrected_hashes"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
