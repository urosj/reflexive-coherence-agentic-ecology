#!/usr/bin/env python3
"""Candidate-free validator for the P2-I2 I07 inactive EXEC-FREEZE."""

from __future__ import annotations

import ast
from collections import Counter
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Callable, Mapping


EXPERIMENT_REL = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SOURCE_REL = EXPERIMENT_REL / "scripts" / "p2_i2_execution.py"
VALIDATOR_REL = EXPERIMENT_REL / "scripts" / "p2_i2_i07_validate.py"
TEST_REL = EXPERIMENT_REL / "implementation" / "tests" / "test_p2_i2_execution_freeze.py"
POLICY_REL = EXPERIMENT_REL / "configs" / "p2_i2_c01_execution_policy_v2.json"
RESUMPTION_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-candidate-cycle-resumption-input-freeze.json"
OUTPUT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-candidate-free-validation.json"
FAILED_START_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-focused-tests-failed-start.json"
CONTINUATION_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-dependency-install-and-validation-continuation.json"
ENVIRONMENT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-pytest-environment-receipt.json"
REFRESH_REL = EXPERIMENT_REL / "scripts" / "p2_i2_i07_refresh.py"
REFRESH_RECEIPT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-binding-refresh-receipt.json"


def root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = root()


def _json(relative: str | Path) -> dict[str, Any]:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"JSON object required: {relative}")
    return value


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repository), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _load_execution():
    spec = importlib.util.spec_from_file_location("p2_i2_execution_candidate_free_validation", ROOT / SOURCE_REL)
    if spec is None or spec.loader is None:
        raise RuntimeError("execution source import specification unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


execution = _load_execution()


def _portable(value: Any) -> bool:
    if isinstance(value, Mapping):
        return all(_portable(key) and _portable(item) for key, item in value.items())
    if isinstance(value, list):
        return all(_portable(item) for item in value)
    if not isinstance(value, str):
        return True
    return not Path(value).is_absolute()


checks: list[dict[str, Any]] = []


def check(check_id: str, claim: str, predicate: Callable[[], bool], evidence: Mapping[str, Any]) -> None:
    passed = False
    error = None
    try:
        passed = bool(predicate())
    except BaseException as exc:  # retained as validation evidence
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


def main() -> int:
    if (ROOT / OUTPUT_REL).exists() or (ROOT / OUTPUT_REL).is_symlink():
        raise RuntimeError("governed validation output already exists")

    resumption = _json(RESUMPTION_REL)
    failed_start = _json(FAILED_START_REL)
    continuation = _json(CONTINUATION_REL)
    environment = _json(ENVIRONMENT_REL)
    refresh_receipt = _json(REFRESH_RECEIPT_REL)
    policy = _json(POLICY_REL)
    effective, successor, overlay = execution.load_effective_policy(ROOT)
    artifacts = successor["artifact_contract"]
    matrix = _json(artifacts["run_matrix_path"])
    binding = _json(artifacts["binding_receipt_path"])
    freeze = _json(artifacts["exec_freeze_path"])
    acceptance = _json(successor["composition"]["accepted_I06B_authority"]["path"])
    source_text = (ROOT / SOURCE_REL).read_text(encoding="utf-8")
    source_tree = ast.parse(source_text)
    test_tree = ast.parse((ROOT / TEST_REL).read_text(encoding="utf-8"))
    rebuilt_entries = execution.expand_run_matrix(effective)
    rebuilt_matrix = execution._matrix_document(rebuilt_entries)
    rebuilt_binding = execution._binding_document(ROOT, rebuilt_matrix)
    rebuilt_freeze = execution._exec_freeze_document(ROOT, rebuilt_matrix, rebuilt_binding)

    check(
        "I07-01",
        "retained pre-I06B drafts remain byte-exact immutable history",
        lambda: all(execution.sha256(ROOT / row["path"]) == row["sha256"] for row in resumption["retained_blocked_drafts"]),
        {"retained_draft_count": len(resumption["retained_blocked_drafts"])},
    )
    check(
        "I07-02",
        "every accepted progression authority remains byte-exact",
        lambda: all(execution.sha256(ROOT / row["path"]) == row["sha256"] for row in resumption["progression_authority"]),
        {"progression_authority_count": len(resumption["progression_authority"])},
    )
    check(
        "I07-03",
        "accepted I06B restores REG-GATE without authorizing execution",
        lambda: (
            acceptance["status"] == "owner_accepted_registration_progression_authority"
            and acceptance["progression_effect"]["P2-I2-REG-GATE"].startswith("passed")
            and acceptance["progression_effect"]["candidate_execution_authorized"] is False
            and acceptance["progression_effect"]["commit_authorized"] is False
        ),
        {"decision_id": acceptance["authority"]["decision_id"], "change_id": acceptance["authority"]["change_id"]},
    )
    check(
        "I07-04",
        "successor composes the blocked draft and accepted I06B only",
        lambda: (
            effective["branch_plans"] == _json(successor["composition"]["base_blocked_policy"]["path"])["branch_plans"]
            and effective["known_registration_blockers"] == []
            and len(successor["blocker_dispositions"]) == 3
            and all(row["status"] == "closed_by_accepted_I06B" for row in successor["blocker_dispositions"])
            and overlay["artifact_id"] == "P2-I2-I06B-EXECUTION-READINESS-OVERLAY"
        ),
        {"closed_blockers": [row["blocker_id"] for row in successor["blocker_dispositions"]]},
    )
    check(
        "I07-04A",
        "owner-authorized in-place I07 continuation preserves the failed start",
        lambda: (
            continuation["authority"]["decision_id"] == "P2-I2-DEC-045"
            and continuation["authority"]["iteration_disposition"] == "continue_inside_I07_not_I07A"
            and execution.sha256(ROOT / FAILED_START_REL) == continuation["retained_failed_start"]["sha256"]
            and failed_start["status"] == "failed_closed_before_test_collection"
            and failed_start["zero_execution_counters"]["candidate_or_control_operations"] == 0
        ),
        {"failed_start_sha256": execution.sha256(ROOT / FAILED_START_REL), "I07A_opened": False},
    )
    check(
        "I07-04B",
        "pytest is installed only in the repository venv with exact retained metadata",
        lambda: (
            importlib.metadata.version("pytest") == "9.1.1"
            and all(execution.sha256(ROOT / row["metadata_path"]) == row["metadata_sha256"] for row in environment["resolved_packages"])
            and environment["installation_result"]["repository_venv_used"] is True
            and environment["installation_result"]["global_environment_targeted"] is False
        ),
        {"pytest_version": importlib.metadata.version("pytest"), "environment_receipt": ENVIRONMENT_REL.as_posix()},
    )
    check(
        "I07-05",
        "execution source and tests parse and have no top-level PyGRC import",
        lambda: (
            isinstance(source_tree, ast.Module)
            and isinstance(test_tree, ast.Module)
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
        "I07-04C",
        "derived binding refresh changes only validator/process-bound hashes",
        lambda: (
            refresh_receipt["status"] == "candidate_free_derived_binding_refresh_complete"
            and refresh_receipt["preserved"]["policy_sha256"] == execution.sha256(ROOT / POLICY_REL)
            and refresh_receipt["preserved"]["execution_source_sha256"] == execution.sha256(ROOT / SOURCE_REL)
            and refresh_receipt["preserved"]["focused_tests_sha256"] == execution.sha256(ROOT / TEST_REL)
            and refresh_receipt["preserved"]["run_matrix_sha256"] == execution.sha256(ROOT / artifacts["run_matrix_path"])
            and refresh_receipt["refreshed"]["validator_sha256"] == execution.sha256(ROOT / VALIDATOR_REL)
            and refresh_receipt["refreshed"]["binding_receipt_sha256"] == execution.sha256(ROOT / artifacts["binding_receipt_path"])
            and refresh_receipt["refreshed"]["inactive_exec_freeze_sha256"] == execution.sha256(ROOT / artifacts["exec_freeze_path"])
        ),
        {"refresh_receipt": REFRESH_RECEIPT_REL.as_posix(), "candidate_execution_authorized": False},
    )
    check(
        "I07-06",
        "native runtime imports are confined to the future live execution function",
        lambda: (
            "def execute_entry(" in source_text
            and source_text.index("def execute_entry(") < source_text.index("from pygrc.models import")
            and source_text.index("def execute_entry(") < source_text.index("from p2_i2_i06_registration import")
            and "runtime_state[\"pygrc_imports\"] = 1" in source_text
        ),
        {"pygrc_imports_during_validation": 0, "models_constructed": 0},
    )
    check(
        "I07-07",
        "matrix reconstructs byte-semantically from the frozen policy",
        lambda: matrix == rebuilt_matrix,
        {"primary_entries": matrix["primary_entry_count"], "semantic_digest": matrix["semantic_digest"]},
    )
    mode_counts = Counter(row["mode"] for row in matrix["entries"])
    check(
        "I07-08",
        "matrix contains the exact 234 unique mode-branch-order-seed entries",
        lambda: (
            len(matrix["entries"]) == 234
            and len({row["entry_id"] for row in matrix["entries"]}) == 234
            and mode_counts == Counter({"state_carried": 72, "history_carried": 75, "hybrid": 87})
        ),
        {"mode_entry_counts": dict(mode_counts)},
    )
    all_paths = [
        row[field]
        for row in matrix["entries"]
        for field in ("primary_output_path", "retry_output_path", "primary_claim_path", "retry_claim_path")
    ]
    check(
        "I07-09",
        "all governed output and claim paths are unique and repository-relative",
        lambda: len(all_paths) == len(set(all_paths)) and all(not Path(path).is_absolute() for path in all_paths),
        {"unique_paths": len(set(all_paths)), "absolute_paths": sum(Path(path).is_absolute() for path in all_paths)},
    )
    check(
        "I07-10",
        "normalized commands bind relative graph root, entry identity, attempt, and output",
        lambda: (
            successor["runtime_invocation_identity"]["python_command"] == ".venv/bin/python"
            and successor["runtime_invocation_identity"]["graph_root_argument"] == "../graph-reflexive-coherence"
            and not Path(successor["runtime_invocation_identity"]["graph_root_argument"]).is_absolute()
            and all(
                row["normalized_primary_argv_template"]
                == execution.normalized_run_argv(successor, row, 1, "<OWNER_AUTHORIZED_FULL_HEAD>")
                and row["normalized_retry_argv_template"]
                == execution.normalized_run_argv(successor, row, 2, "<OWNER_AUTHORIZED_FULL_HEAD>")
                for row in matrix["entries"]
            )
        ),
        {"command_template_count": 2 * len(matrix["entries"])},
    )
    check(
        "I07-11",
        "binding receipt reconstructs exactly and binds every source authority",
        lambda: binding == rebuilt_binding and all(execution.sha256(ROOT / row["path"]) == row["sha256"] for row in binding["bound_files"]),
        {"bound_files": len(binding["bound_files"]), "payload_digest": binding["canonical_payload_digest"]},
    )
    check(
        "I07-12",
        "inactive exec freeze reconstructs exactly and closes all execution gates",
        lambda: (
            freeze == rebuilt_freeze
            and freeze["candidate_execution_authorized"] is False
            and freeze["I08_authorized"] is False
            and freeze["commit_authorized"] is False
            and freeze["activation_record"]["present_at_freeze"] is False
        ),
        {"status": freeze["status"], "authorization_gate": freeze["authorization_gate"]},
    )
    check(
        "I07-13",
        "freeze byte-binds policy, source, validator, tests, matrix, and binding",
        lambda: (
            freeze["bound_identity"]["policy_sha256"] == execution.sha256(ROOT / POLICY_REL)
            and freeze["bound_identity"]["execution_source_sha256"] == execution.sha256(ROOT / SOURCE_REL)
            and freeze["bound_identity"]["validator_sha256"] == execution.sha256(ROOT / VALIDATOR_REL)
            and freeze["bound_identity"]["test_sha256"] == execution.sha256(ROOT / TEST_REL)
            and freeze["bound_identity"]["run_matrix_file_sha256"] == execution.sha256(ROOT / artifacts["run_matrix_path"])
            and freeze["bound_identity"]["binding_receipt_file_sha256"] == execution.sha256(ROOT / artifacts["binding_receipt_path"])
        ),
        {"bound_identity_fields": len(freeze["bound_identity"])},
    )
    check(
        "I07-14",
        "permanent exclusive claim precedes every runtime import or construction",
        lambda: (
            "os.O_WRONLY | os.O_CREAT | os.O_EXCL" in source_text
            and source_text.index("_exclusive_json(\n        claim_path") < source_text.index("result = execute_entry(", source_text.index("def run_entry("))
            and "claim_survives_every_failure" in json.dumps(freeze, sort_keys=True)
        ),
        {"claim_semantics": freeze["claim_policy"]["semantics"]},
    )
    check(
        "I07-15",
        "retry is pre-construction-only, outcome-blind, and separately authorized",
        lambda: (
            freeze["retry_policy"]["post_model_failure_consumes_entry"] is True
            and freeze["retry_policy"]["scientific_or_control_outcome_retryable"] is False
            and freeze["retry_policy"]["infrastructure_retry_eligibility_uses_outcome"] is False
            and freeze["retry_policy"]["primary_claim_is_never_deleted"] is True
            and "model_or_adapter_construction_started" in source_text
            and "retry_ledger" in source_text
        ),
        {"maximum_conditional_retries": matrix["maximum_conditional_retry_count"]},
    )
    activation_path = ROOT / artifacts["activation_record_path"]
    output_root = ROOT / EXPERIMENT_REL / "outputs" / "p2-i2" / "c01"
    check(
        "I07-16",
        "no activation, retry ledger, execution manifest, claim, output, or failure exists",
        lambda: (
            not activation_path.exists()
            and not (ROOT / artifacts["retry_ledger_path"]).exists()
            and not (ROOT / artifacts["execution_manifest_path"]).exists()
            and not output_root.exists()
        ),
        {"activation_present": activation_path.exists(), "output_root_present": output_root.exists()},
    )
    check(
        "I07-17",
        "all I07 authority and generated artifacts are portable",
        lambda: all(_portable(value) for value in (resumption, failed_start, continuation, environment, refresh_receipt, policy, matrix, binding, freeze)),
        {"absolute_machine_local_paths": 0},
    )
    graph_root = (ROOT / successor["runtime_invocation_identity"]["graph_root_argument"]).resolve()
    runtime_identity = resumption["runtime_identity"]
    runtime_source = graph_root / "src" / "pygrc" / "models" / "lgrc_9_v3_runtime.py"
    check(
        "I07-18",
        "external PyGRC checkout remains exact and clean",
        lambda: (
            _git(graph_root, "rev-parse", "HEAD") == runtime_identity["graph_revision"]
            and _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == ""
            and execution.sha256(runtime_source) == runtime_identity["runtime_source_sha256"]
        ),
        {"graph_revision": _git(graph_root, "rev-parse", "HEAD")},
    )
    check(
        "I07-19",
        "validation uses the frozen repository virtual environment",
        lambda: (
            Path(sys.prefix).resolve() == (ROOT / ".venv").resolve()
            and platform.python_version() == runtime_identity["python_version"]
            and execution.sha256(Path(sys.executable).resolve()) == runtime_identity["interpreter_executable_sha256"]
        ),
        {"python_command": ".venv/bin/python", "python_version": platform.python_version()},
    )
    check(
        "I07-20",
        "I07 remains on its accepted parent commit before owner review",
        lambda: _git(ROOT, "rev-parse", "HEAD") == resumption["entry_authority"]["parent_commit"],
        {"HEAD": _git(ROOT, "rev-parse", "HEAD"), "commit_authorized": False},
    )
    check(
        "I07-21",
        "construction and validation remained candidate-free",
        lambda: not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules),
        {
            "candidate_free_python_starts": 6,
            "infrastructure_retries": 0,
            "pygrc_imports": 0,
            "models_constructed": 0,
            "packets_scheduled_or_processed": 0,
            "candidate_or_control_operations": 0,
            "response_evaluations": 0,
            "scientific_windows": 0,
        },
    )
    check(
        "I07-22",
        "future run and failure artifacts cover every registered receipt field",
        lambda: (
            all(f'"{name}"' in source_text for name in effective["required_receipts"]["per_attempt"])
            and all(f'"{name}"' in source_text for name in effective["required_receipts"]["failure_receipt_fields"])
            and "candidate_or_control_operations_started" in source_text
            and "unexpected B-targeting packet count" in source_text
            and "fresh registered composite baseline drift" in source_text
        ),
        {
            "per_attempt_receipts": len(effective["required_receipts"]["per_attempt"]),
            "failure_receipt_fields": len(effective["required_receipts"]["failure_receipt_fields"]),
        },
    )

    failed = [row for row in checks if not row["passed"]]
    if failed:
        raise RuntimeError("I07 validation failed: " + ", ".join(row["check_id"] for row in failed))

    result = {
        "artifact_id": "P2-I2-I07-CANDIDATE-FREE-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I07",
        "lane_id": "AE01-L02",
        "cycle_id": "P2-I2-C01",
        "validated_at": "2026-07-15",
        "status": "passed_candidate_free_inactive_exec_freeze_pending_owner_review",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "blockers": 0,
        "checks": checks,
        "artifact_hashes": {
            "resumption_input_freeze_sha256": execution.sha256(ROOT / RESUMPTION_REL),
            "successor_policy_sha256": execution.sha256(ROOT / POLICY_REL),
            "execution_source_sha256": execution.sha256(ROOT / SOURCE_REL),
            "validator_sha256": execution.sha256(ROOT / VALIDATOR_REL),
            "focused_tests_sha256": execution.sha256(ROOT / TEST_REL),
            "failed_start_sha256": execution.sha256(ROOT / FAILED_START_REL),
            "continuation_freeze_sha256": execution.sha256(ROOT / CONTINUATION_REL),
            "pytest_environment_receipt_sha256": execution.sha256(ROOT / ENVIRONMENT_REL),
            "binding_refresh_source_sha256": execution.sha256(ROOT / REFRESH_REL),
            "binding_refresh_receipt_sha256": execution.sha256(ROOT / REFRESH_RECEIPT_REL),
            "run_matrix_sha256": execution.sha256(ROOT / artifacts["run_matrix_path"]),
            "binding_receipt_sha256": execution.sha256(ROOT / artifacts["binding_receipt_path"]),
            "inactive_exec_freeze_sha256": execution.sha256(ROOT / artifacts["exec_freeze_path"]),
        },
        "process_accounting": {
            "candidate_free_python_starts": 6,
            "original_start_ceiling": resumption["construction_validation_boundary"]["candidate_free_python_start_ceiling"],
            "owner_corrected_start_ceiling": continuation["continued_process_plan"]["candidate_free_python_start_ceiling"],
            "infrastructure_retries": 0,
            "commands": [
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_execution.py build-freeze",
                ".venv/bin/python -m pytest -q experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests/test_p2_i2_execution_freeze.py",
                ".venv/bin/python -m pip install pytest",
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i07_refresh.py",
                ".venv/bin/python -m pytest -q experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests/test_p2_i2_execution_freeze.py",
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i07_validate.py",
            ],
            "pygrc_imports": 0,
            "models_constructed": 0,
            "packets_scheduled_or_processed": 0,
            "candidate_or_control_operations": 0,
            "scientific_evidence": False,
        },
        "gate_disposition": {
            "REG_GATE": "passed_after_explicit_owner_acceptance_of_I06B",
            "EXEC_FREEZE": "closed_pending_explicit_owner_acceptance_of_I07",
            "I08_authorized": False,
            "candidate_execution_authorized": False,
            "commit_authorized": False,
        },
        "reconstruction": {
            "run_matrix_byte_semantic_reconstruction": True,
            "binding_receipt_byte_semantic_reconstruction": True,
            "inactive_exec_freeze_byte_semantic_reconstruction": True,
            "validation_output_readback_byte_identical": True,
        },
        "evidence_effect": "pre_execution_identity_and_authorization_integrity_only_no_candidate_or_scientific_evidence",
    }
    expected = execution.pretty_bytes(result)
    execution.write_new(ROOT / OUTPUT_REL, result)
    if (ROOT / OUTPUT_REL).read_bytes() != expected:
        raise RuntimeError("validation output readback differs from generated bytes")
    print(json.dumps({"checks_passed": len(checks), "checks_total": len(checks), "status": result["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
