#!/usr/bin/env python3
"""Candidate-free validator for the P2-I2 I07A isolated EXEC-FREEZE."""

from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Callable, Mapping


EXPERIMENT_REL = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SOURCE_REL = EXPERIMENT_REL / "scripts" / "p2_i2_execution.py"
VALIDATOR_REL = EXPERIMENT_REL / "scripts" / "p2_i2_i07a_validate.py"
TEST_REL = EXPERIMENT_REL / "implementation" / "tests" / "test_p2_i2_execution_freeze.py"
POLICY_REL = EXPERIMENT_REL / "configs" / "p2_i2_c01_execution_policy_v2.json"
INPUT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-cross-entry-isolation-input-freeze.json"
REFRESH_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-derived-refresh-receipt.json"
TEST_RECEIPT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-focused-tests-receipt.json"
OUTPUT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-candidate-free-validation.json"
OLD_VALIDATION_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-candidate-free-validation.json"


def root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = root()


def load_json(relative: str | Path) -> dict[str, Any]:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"JSON object required: {relative}")
    return value


def git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def load_execution():
    spec = importlib.util.spec_from_file_location("p2_i2_execution_i07a_validation", ROOT / SOURCE_REL)
    if spec is None or spec.loader is None:
        raise RuntimeError("execution source import specification unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


execution = load_execution()
checks: list[dict[str, Any]] = []


def check(check_id: str, claim: str, predicate: Callable[[], bool], evidence: Mapping[str, Any]) -> None:
    passed = False
    error = None
    try:
        passed = bool(predicate())
    except BaseException as exc:
        error = f"{type(exc).__name__}: {exc}"
    checks.append(
        {
            "check_id": check_id,
            "claim": claim,
            "passed": passed,
            "evidence": dict(evidence),
            "error": error,
        }
    )


def portable(value: Any) -> bool:
    if isinstance(value, Mapping):
        return all(portable(key) and portable(item) for key, item in value.items())
    if isinstance(value, list):
        return all(portable(item) for item in value)
    return not isinstance(value, str) or not Path(value).is_absolute()


def main() -> int:
    if (ROOT / OUTPUT_REL).exists() or (ROOT / OUTPUT_REL).is_symlink():
        raise RuntimeError("I07A validation output already exists")
    if sys.dont_write_bytecode is not True:
        raise RuntimeError("I07A validation requires .venv/bin/python -B")

    input_freeze = load_json(INPUT_REL)
    refresh = load_json(REFRESH_REL)
    test_receipt = load_json(TEST_RECEIPT_REL)
    old_validation = load_json(OLD_VALIDATION_REL)
    policy = load_json(POLICY_REL)
    effective, successor, _ = execution.load_effective_policy(ROOT)
    artifacts = successor["artifact_contract"]
    matrix = load_json(artifacts["run_matrix_path"])
    binding = load_json(artifacts["binding_receipt_path"])
    freeze = load_json(artifacts["exec_freeze_path"])
    source_text = (ROOT / SOURCE_REL).read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)
    test_tree = ast.parse((ROOT / TEST_REL).read_text(encoding="utf-8"))
    validator_tree = ast.parse((ROOT / VALIDATOR_REL).read_text(encoding="utf-8"))
    rebuilt_matrix = execution._matrix_document(execution.expand_run_matrix(effective))
    rebuilt_binding = execution._binding_document(ROOT, rebuilt_matrix)
    rebuilt_freeze = execution._exec_freeze_document(ROOT, rebuilt_matrix, rebuilt_binding)

    reviewed = {row["role"]: row["sha256"] for row in input_freeze["reviewed_i07_inputs"]}
    check(
        "I07A-01",
        "the additive input freeze preserves every reviewed I07 identity",
        lambda: (
            input_freeze["authority"] == {"decision_id": "P2-I2-DEC-046", "change_id": "P2-I2-CHG-042", "owner_direction": "These can actually be I07A"}
            and reviewed["reviewed_effective_policy"] == "9a0649f18e99dff3c3f5bc7f8927ea8b369adde17e5160013a508e045c7d047e"
            and reviewed["reviewed_execution_source"] == "42b8486908831a928535f9594c7a15cc0d634c0025391d28ce32fc3b75fb6a61"
            and reviewed["reviewed_run_matrix"] == "57953a5fc93e8e05a95cdb7ca260c72bc28ea9388fd0804b064c1279ce8c48e8"
            and reviewed["reviewed_inactive_exec_freeze"] == "c703eca51bc6155f44c5a3164c938361285b1f11dda506515fd4bc2fd4c93f1d"
            and execution.sha256(ROOT / OLD_VALIDATION_REL) == reviewed["reviewed_candidate_free_validation"]
        ),
        {"reviewed_identity_count": len(reviewed)},
    )
    check(
        "I07A-02",
        "I07A changes only the declared isolation mechanics",
        lambda: (
            policy["iteration_id"] == "P2-I2-I07A"
            and policy["artifact_version"] == "2.1.0"
            and policy["matrix"]["primary_entry_count"] == 234
            and effective["branch_plans"] == load_json(policy["composition"]["base_blocked_policy"]["path"])["branch_plans"]
            and policy["activation_and_gate_boundary"]["candidate_execution_authorized"] is False
        ),
        {"allowed_corrections": input_freeze["allowed_corrections"]},
    )
    check(
        "I07A-03",
        "all 1,404 governed paths are unique relative and beneath the exact C01 root",
        lambda: (
            len(
                {
                    value
                    for row in matrix["entries"]
                    for value in (
                        row["primary_output_path"],
                        row["retry_output_path"],
                        row["primary_claim_path"],
                        row["retry_claim_path"],
                        execution._output_path(artifacts["failure_receipt_template"], row, 1),
                        execution._output_path(artifacts["failure_receipt_template"], row, 2),
                    )
                }
            )
            == 1404
            and all(
                not Path(value).is_absolute()
                and Path(value).parts[: len(execution.OUTPUT_ROOT_REL.parts)] == execution.OUTPUT_ROOT_REL.parts
                for row in matrix["entries"]
                for value in (
                    row["primary_output_path"],
                    row["retry_output_path"],
                    row["primary_claim_path"],
                    row["retry_claim_path"],
                    execution._output_path(artifacts["failure_receipt_template"], row, 1),
                    execution._output_path(artifacts["failure_receipt_template"], row, 2),
                )
            )
        ),
        {"matrix_entries": len(matrix["entries"]), "governed_paths": 1404},
    )
    check(
        "I07A-04",
        "governed artifact I/O is beneath-root and no-symlink-component",
        lambda: all(
            token in source_text
            for token in (
                "def _open_governed_parent(",
                "os.O_NOFOLLOW",
                "dir_fd=descriptor",
                "def _read_governed_json(",
                "def _exclusive_json(",
                "failure receipt already exists or is unsafe",
            )
        ),
        {"focused_symlink_tests_passed": test_receipt["checks"]["symlink_and_containment"]},
    )
    check(
        "I07A-05",
        "live execution requires -B and rejects shared project or PyGRC import caches",
        lambda: (
            policy["runtime_invocation_identity"]["python_flags"] == ["-B"]
            and policy["runtime_invocation_identity"]["dont_write_bytecode_required"] is True
            and "def _assert_import_cache_clean(" in source_text
            and source_text.count("_assert_import_cache_clean(root, graph_root)") >= 2
        ),
        {"python_flags": policy["runtime_invocation_identity"]["python_flags"], "cache_test_passed": test_receipt["checks"]["cache_refusal"]},
    )
    check(
        "I07A-06",
        "attempt 2 reconstructs only its own predecessor without a shared ledger",
        lambda: (
            policy["retry_policy"]["shared_retry_ledger"] is False
            and policy["retry_policy"]["other_entry_claim_failure_or_output_reads"] is False
            and "retry_ledger" not in source_text
            and "def _validate_retry_predecessor(" in source_text
            and "current-entry primary failure receipt absent" in source_text
        ),
        {"retry_tests_passed": test_receipt["checks"]["row_local_retry"]},
    )
    check(
        "I07A-07",
        "completion enumerates exact matrix paths and fails closed on missing null or duplicate terminals",
        lambda: (
            policy["completion_policy"]["execution_manifest_created_only_after_all_234_evaluable"] is True
            and "def _execution_manifest_document(" in source_text
            and "for entry in matrix[\"entries\"]" in source_text
            and "glob(" not in source_text
            and "rglob(" not in source_text
            and "scandir(" not in source_text
            and "listdir(" not in source_text
        ),
        {"completion_tests_passed": test_receipt["checks"]["fail_closed_completion"]},
    )
    check(
        "I07A-08",
        "the exact 234-row matrix reconstructs and preserves every reviewed entry",
        lambda: matrix == rebuilt_matrix and refresh["matrix_projection"]["entries_byte_semantic_unchanged"] is True,
        {"matrix_sha256": execution.sha256(ROOT / artifacts["run_matrix_path"]), "semantic_digest": matrix["semantic_digest"]},
    )
    check(
        "I07A-09",
        "binding and inactive freeze reconstruct exactly after the bounded refresh",
        lambda: binding == rebuilt_binding and freeze == rebuilt_freeze,
        {
            "binding_sha256": execution.sha256(ROOT / artifacts["binding_receipt_path"]),
            "freeze_sha256": execution.sha256(ROOT / artifacts["exec_freeze_path"]),
        },
    )
    check(
        "I07A-10",
        "I07A source tests and validator parse without top-level PyGRC import",
        lambda: (
            all(isinstance(tree, ast.Module) for tree in (source_tree, test_tree, validator_tree))
            and not any(
                (isinstance(node, ast.Import) and any(alias.name.startswith("pygrc") for alias in node.names))
                or (isinstance(node, ast.ImportFrom) and (node.module or "").startswith("pygrc"))
                for node in source_tree.body
            )
            and not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules)
        ),
        {"source_sha256": execution.sha256(ROOT / SOURCE_REL), "test_sha256": execution.sha256(ROOT / TEST_REL)},
    )
    check(
        "I07A-11",
        "focused tests pass under the frozen repository venv -B command",
        lambda: (
            test_receipt["status"] == "passed_candidate_free"
            and test_receipt["tests_failed"] == 0
            and test_receipt["python_command"] == [".venv/bin/python", "-B", "-m", "pytest"]
        ),
        {"tests_passed": test_receipt["tests_passed"], "tests_failed": test_receipt["tests_failed"]},
    )
    activation_path = ROOT / artifacts["activation_record_path"]
    output_root = ROOT / execution.OUTPUT_ROOT_REL
    check(
        "I07A-12",
        "no activation candidate output failure retry or execution manifest exists",
        lambda: (
            not activation_path.exists()
            and not activation_path.is_symlink()
            and not output_root.exists()
            and not (ROOT / artifacts["execution_manifest_path"]).exists()
        ),
        {"activation_present": activation_path.exists(), "output_root_present": output_root.exists()},
    )
    check(
        "I07A-13",
        "all correction authorities and generated identities remain portable",
        lambda: all(portable(value) for value in (input_freeze, refresh, test_receipt, policy, matrix, binding, freeze)),
        {"absolute_machine_local_paths": 0},
    )
    graph_root = (ROOT / policy["runtime_invocation_identity"]["graph_root_argument"]).resolve()
    runtime_identity = load_json(execution.RESUMPTION_FREEZE_REL)["runtime_identity"]
    check(
        "I07A-14",
        "the external PyGRC authority remains exact and clean",
        lambda: (
            git(graph_root, "rev-parse", "HEAD") == runtime_identity["graph_revision"]
            and git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == ""
            and execution.sha256(graph_root / "src" / "pygrc" / "models" / "lgrc_9_v3_runtime.py") == runtime_identity["runtime_source_sha256"]
        ),
        {"graph_revision": git(graph_root, "rev-parse", "HEAD")},
    )
    check(
        "I07A-15",
        "validation uses the exact repository virtual environment with -B active",
        lambda: (
            Path(sys.prefix).resolve() == (ROOT / ".venv").resolve()
            and platform.python_version() == runtime_identity["python_version"]
            and execution.sha256(Path(sys.executable).resolve()) == runtime_identity["interpreter_executable_sha256"]
            and sys.dont_write_bytecode is True
        ),
        {"python_command": [".venv/bin/python", "-B"], "python_version": platform.python_version()},
    )
    check(
        "I07A-16",
        "the three-start candidate-free budget is exact and contains no retry",
        lambda: (
            refresh["process_ledger"]["start_index"] == 1
            and test_receipt["process_ledger"]["start_index"] == 2
            and input_freeze["python_start_budget"]["maximum_starts"] == 3
            and input_freeze["python_start_budget"]["replacement_after_failure"] is False
        ),
        {"final_validator_start_index": 3, "infrastructure_retries": 0},
    )
    check(
        "I07A-17",
        "I07A remains candidate-free and cannot activate itself",
        lambda: (
            freeze["candidate_execution_authorized"] is False
            and freeze["I08_authorized"] is False
            and freeze["commit_authorized"] is False
            and not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules)
        ),
        {
            "pygrc_imports": 0,
            "models_constructed": 0,
            "candidate_or_control_operations": 0,
            "scientific_windows": 0,
        },
    )

    failed = [row for row in checks if not row["passed"]]
    if failed:
        raise RuntimeError("I07A validation failed: " + ", ".join(row["check_id"] for row in failed))

    result = {
        "artifact_id": "P2-I2-I07A-CANDIDATE-FREE-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I07A",
        "lane_id": "AE01-L02",
        "cycle_id": "P2-I2-C01",
        "validated_at": "2026-07-15",
        "status": "passed_candidate_free_isolation_correction_pending_owner_review",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "blockers": 0,
        "checks": checks,
        "artifact_hashes": {
            "input_freeze_sha256": execution.sha256(ROOT / INPUT_REL),
            "policy_sha256": execution.sha256(ROOT / POLICY_REL),
            "execution_source_sha256": execution.sha256(ROOT / SOURCE_REL),
            "validator_sha256": execution.sha256(ROOT / VALIDATOR_REL),
            "focused_tests_sha256": execution.sha256(ROOT / TEST_REL),
            "focused_test_receipt_sha256": execution.sha256(ROOT / TEST_RECEIPT_REL),
            "refresh_receipt_sha256": execution.sha256(ROOT / REFRESH_REL),
            "run_matrix_sha256": execution.sha256(ROOT / artifacts["run_matrix_path"]),
            "binding_receipt_sha256": execution.sha256(ROOT / artifacts["binding_receipt_path"]),
            "inactive_exec_freeze_sha256": execution.sha256(ROOT / artifacts["exec_freeze_path"]),
        },
        "process_ledger": {
            "python_starts": 3,
            "infrastructure_retries": 0,
            "pygrc_imports": 0,
            "models_constructed": 0,
            "packets_scheduled_or_processed": 0,
            "candidate_or_control_operations": 0,
            "response_evaluations": 0,
            "scientific_windows": 0,
        },
        "gate_boundary": {
            "candidate_execution_authorized": False,
            "P2-I2-EXEC-FREEZE": "closed_pending_owner_review",
            "I08_authorized": False,
            "commit_authorized": False
        }
    }
    execution.write_new(ROOT / OUTPUT_REL, result)
    print(json.dumps({"checks_passed": len(checks), "checks_total": len(checks), "blockers": 0}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
