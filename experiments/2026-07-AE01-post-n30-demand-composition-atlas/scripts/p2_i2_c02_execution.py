#!/usr/bin/env python3
"""P2-I2 C02 external-supervisor execution and exact completion surface."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
from typing import Any, Mapping, Sequence


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SOURCE_REL = EXPERIMENT / "scripts/p2_i2_c02_execution.py"
POLICY_REL = EXPERIMENT / "configs/p2_i2_c02_execution_policy.json"
INPUT_FREEZE_REL = EXPERIMENT / "contracts/p2-i2/c02/i08a-c02-input-freeze.json"
MATRIX_REL = EXPERIMENT / "contracts/p2-i2/c02/run-matrix.json"
BINDING_REL = EXPERIMENT / "contracts/p2-i2/c02/execution-binding-receipt.json"
FREEZE_REL = EXPERIMENT / "contracts/p2-i2/c02/exec-freeze.json"
ACTIVATION_REL = EXPERIMENT / "contracts/p2-i2/c02/owner-accepted-execution-authorization.json"
MANIFEST_REL = EXPERIMENT / "contracts/p2-i2/c02/execution-manifest.json"
C01_MATRIX_REL = EXPERIMENT / "contracts/p2-i2/c01/run-matrix.json"
C01_BINDING_REL = EXPERIMENT / "contracts/p2-i2/c01/execution-binding-receipt.json"
C01_ACTIVATION_REL = EXPERIMENT / "contracts/p2-i2/c01/owner-accepted-execution-authorization.json"
C01_AUDIT_REL = EXPERIMENT / "contracts/p2-i2/c01/i08-entry-001-native-termination-audit.json"
C01_CLAIM_REL = EXPERIMENT / "outputs/p2-i2/c01/claims/state_carried/reference-pool/reference_pool_empty/not_applicable/seed-101/attempt-1.json"
TEST_REL = EXPERIMENT / "implementation/tests/test_p2_i2_c02_execution.py"
VALIDATOR_REL = EXPERIMENT / "scripts/p2_i2_i08a_validate.py"
INFRA_INPUT_REL = EXPERIMENT / "contracts/p2-i2/c02/i08a-venv-infrastructure-correction-input.json"
INFRA_CORRECTION_REL = EXPERIMENT / "contracts/p2-i2/c02/i08a-venv-infrastructure-correction.json"
INFRA_TEST_RECEIPT_REL = EXPERIMENT / "contracts/p2-i2/c02/i08a-venv-infrastructure-tests.json"
INFRA_VALIDATOR_REL = EXPERIMENT / "scripts/p2_i2_i08a_venv_infrastructure_validate.py"
INFRA_VALIDATION_REL = EXPERIMENT / "contracts/p2-i2/c02/i08a-venv-infrastructure-validation.json"
POSTCOMMIT_PREFLIGHT_REL = EXPERIMENT / "scripts/p2_i2_c02_postcommit_preflight.py"
OUTPUT_ROOT_REL = EXPERIMENT / "outputs/p2-i2/c02"
CYCLE_ID = "P2-I2-C02"
C01_CYCLE_ID = "P2-I2-C01"
PLACEHOLDER_HEAD = "<OWNER_AUTHORIZED_FULL_HEAD>"
MAX_STDERR_BYTES = 16384


class ContractError(RuntimeError):
    """Raised when C02 must fail closed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise ContractError("repository root not found")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"JSON object required: {path.name}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", os.fspath(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _c01_module(root: Path) -> Any:
    scripts = root / EXPERIMENT / "scripts"
    if os.fspath(scripts) not in sys.path:
        sys.path.insert(0, os.fspath(scripts))
    import p2_i2_execution as module

    module.OUTPUT_ROOT_REL = OUTPUT_ROOT_REL
    return module


def _safe_helpers(root: Path) -> Any:
    module = _c01_module(root)
    module.OUTPUT_ROOT_REL = OUTPUT_ROOT_REL
    return module


def write_new(path: Path, document: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = pretty_bytes(document)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
    except BaseException:
        if path.exists() and not path.is_symlink():
            path.unlink()
        raise


def _translate_entry(row: Mapping[str, Any]) -> dict[str, Any]:
    entry = deepcopy(dict(row))
    require(entry["cycle_id"] == C01_CYCLE_ID, "C01 row cycle drift")
    entry["cycle_id"] = CYCLE_ID
    entry["entry_id"] = str(entry["entry_id"]).replace(f"{C01_CYCLE_ID}:", f"{CYCLE_ID}:", 1)
    for key in (
        "primary_claim_path",
        "retry_claim_path",
        "primary_output_path",
        "retry_output_path",
    ):
        entry[key] = str(entry[key]).replace("outputs/p2-i2/c01/", "outputs/p2-i2/c02/", 1)
    for key in ("normalized_primary_argv_template", "normalized_retry_argv_template"):
        argv = [str(token).replace("outputs/p2-i2/c01/", "outputs/p2-i2/c02/", 1) for token in entry[key]]
        entry[key] = argv
    return entry


def translated_matrix(root: Path) -> dict[str, Any]:
    c01 = load_json(root / C01_MATRIX_REL)
    require(c01["cycle_id"] == C01_CYCLE_ID and c01["primary_entry_count"] == 234, "C01 matrix drift")
    entries = [_translate_entry(row) for row in c01["entries"]]
    require([row["sequence_index"] for row in entries] == list(range(1, 235)), "C02 order drift")
    document = {
        "artifact_id": "P2-I2-C02-RUN-MATRIX",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08A",
        "cycle_id": CYCLE_ID,
        "status": "inactive_exact_projection",
        "predecessor_cycle_id": C01_CYCLE_ID,
        "predecessor_matrix_sha256": sha256(root / C01_MATRIX_REL),
        "primary_entry_count": 234,
        "maximum_conditional_retry_count": 234,
        "entries": entries,
        "scientific_projection_change_count": 0,
    }
    document["semantic_digest"] = digest({"entries": entries})
    return document


def _pointer(root: Path, relative: Path, role: str) -> dict[str, str]:
    path = root / relative
    require(path.is_file() and not path.is_symlink(), f"missing bound file: {relative}")
    return {"path": relative.as_posix(), "role": role, "sha256": sha256(path)}


def _binding_document(root: Path, matrix: Mapping[str, Any]) -> dict[str, Any]:
    c01_binding = load_json(root / C01_BINDING_REL)
    bound = deepcopy(c01_binding["bound_files"])
    additions = (
        (C01_ACTIVATION_REL, "accepted_C01_activation"),
        (C01_AUDIT_REL, "C01_bounded_incomplete_audit"),
        (C01_CLAIM_REL, "C01_permanent_entry_001_claim"),
        (INPUT_FREEZE_REL, "I08A_C02_input_freeze"),
        (POLICY_REL, "C02_execution_policy"),
        (SOURCE_REL, "C02_external_supervisor_and_worker"),
        (TEST_REL, "C02_candidate_free_tests"),
        (VALIDATOR_REL, "I08A_candidate_free_validator"),
    )
    bound.extend(_pointer(root, relative, role) for relative, role in additions)
    paths = [row["path"] for row in bound]
    require(len(paths) == len(set(paths)), "duplicate C02 bound file")
    document = {
        "artifact_id": "P2-I2-C02-EXECUTION-BINDING-RECEIPT",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08A",
        "cycle_id": CYCLE_ID,
        "status": "inactive_candidate_free_binding",
        "bound_files": bound,
        "bound_file_count": len(bound),
        "run_matrix_sha256": sha256(root / MATRIX_REL),
        "run_matrix_semantic_digest": matrix["semantic_digest"],
        "C01_scientific_projection_change_count": 0,
    }
    document["canonical_payload_digest"] = digest(document)
    return document


def _freeze_document(root: Path, matrix: Mapping[str, Any], binding: Mapping[str, Any]) -> dict[str, Any]:
    policy = load_json(root / POLICY_REL)
    document = {
        "artifact_id": "P2-I2-C02-EXEC-FREEZE",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08A",
        "cycle_id": CYCLE_ID,
        "status": "inactive_pending_candidate_free_validation_and_owner_acceptance",
        "candidate_execution_authorized": False,
        "I08_authorized": False,
        "activation_record_present": (root / ACTIVATION_REL).exists(),
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
        "test_sha256": sha256(root / TEST_REL),
        "validator_sha256": sha256(root / VALIDATOR_REL),
        "input_freeze_sha256": sha256(root / INPUT_FREEZE_REL),
        "run_matrix_sha256": sha256(root / MATRIX_REL),
        "binding_receipt_sha256": sha256(root / BINDING_REL),
        "primary_entry_count": matrix["primary_entry_count"],
        "resource_envelope_per_worker": deepcopy(policy["resource_envelope_per_worker"]),
        "supervisor_contract": deepcopy(policy["supervisor_contract"]),
        "artifact_contract": deepcopy(policy["artifact_contract"]),
        "future_activation_requirements": deepcopy(policy["future_activation_requirements"]),
        "scientific_projection_change_count": 0,
        "bound_file_count": binding["bound_file_count"],
    }
    require(document["activation_record_present"] is False, "C02 activation already exists")
    document["canonical_payload_digest"] = digest(document)
    return document


def build_freeze(root: Path) -> dict[str, Any]:
    outputs = (root / MATRIX_REL, root / BINDING_REL, root / FREEZE_REL)
    require(not any(path.exists() or path.is_symlink() for path in outputs), "C02 freeze output already exists")
    require(not (root / ACTIVATION_REL).exists(), "C02 activation must be absent")
    matrix = translated_matrix(root)
    write_new(outputs[0], matrix)
    binding = _binding_document(root, matrix)
    write_new(outputs[1], binding)
    freeze = _freeze_document(root, matrix, binding)
    write_new(outputs[2], freeze)
    return {"entries": 234, "bound_files": binding["bound_file_count"], "status": freeze["status"]}


def _find_entry(matrix: Mapping[str, Any], identity: Mapping[str, Any]) -> dict[str, Any]:
    keys = ("mode", "cell_id", "branch_id", "physical_order_id", "seed")
    matches = [row for row in matrix["entries"] if all(row[key] == identity[key] for key in keys)]
    require(len(matches) == 1, "entry outside exact C02 matrix")
    return dict(matches[0])


def normalized_run_argv(entry: Mapping[str, Any], attempt: int, expected_head: str) -> list[str]:
    template = entry["normalized_primary_argv_template"] if attempt == 1 else entry["normalized_retry_argv_template"]
    return [expected_head if token == PLACEHOLDER_HEAD else str(token) for token in template]


def _authority_tree_clean(root: Path) -> None:
    allowed = OUTPUT_ROOT_REL.as_posix() + "/"
    status = subprocess.run(
        ["git", "-C", os.fspath(root), "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        check=True,
        capture_output=True,
    ).stdout
    for raw in status.split(b"\0"):
        if not raw:
            continue
        value = raw.decode("utf-8")
        require(len(value) >= 4, "unparseable C02 authority status")
        code, relative = value[:2], value[3:]
        require(code == "??" and relative.startswith(allowed), f"dirty C02 authority path: {relative}")


def _committed_equal(root: Path, head: str, relative: str) -> bool:
    committed = subprocess.run(
        ["git", "-C", os.fspath(root), "show", f"{head}:{relative}"],
        check=True,
        capture_output=True,
    ).stdout
    return committed == (root / relative).read_bytes()


def _cache_artifacts(root: Path, graph: Path) -> list[str]:
    found: list[str] = []
    for label, base in (("experiment_scripts", root / EXPERIMENT / "scripts"), ("pygrc_source", graph / "src")):
        require(base.is_dir() and not base.is_symlink(), f"unsafe import root: {label}")
        for current, directories, files in os.walk(base, followlinks=False):
            relative = Path(current).relative_to(base)
            for directory in directories:
                if directory == "__pycache__":
                    found.append(f"{label}:{(relative / directory).as_posix()}")
            for name in files:
                if name.endswith((".pyc", ".pyo")):
                    found.append(f"{label}:{(relative / name).as_posix()}")
    return sorted(found)


def validate_activation(
    root: Path,
    graph: Path,
    identity: Mapping[str, Any],
    attempt: int,
    expected_head: str,
    actual_argv: Sequence[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    require(re.fullmatch(r"[0-9a-f]{40}", expected_head) is not None, "full lowercase HEAD required")
    matrix = load_json(root / MATRIX_REL)
    entry = _find_entry(matrix, identity)
    require(list(actual_argv) == normalized_run_argv(entry, attempt, expected_head), "C02 command drift")
    freeze = load_json(root / FREEZE_REL)
    activation = load_json(root / ACTIVATION_REL)
    policy = load_json(root / POLICY_REL)
    require(freeze["candidate_execution_authorized"] is False, "inactive C02 freeze mutated")
    require(
        activation["artifact_id"] == "P2-I2-C02-OWNER-ACCEPTED-EXECUTION-AUTHORIZATION"
        and activation["cycle_id"] == CYCLE_ID
        and activation["owner_acceptance"] is True
        and activation["candidate_execution_authorized"] is True
        and activation["I08_authorized"] is True,
        "C02 activation absent",
    )
    expected_hashes = {
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
        "test_sha256": sha256(root / TEST_REL),
        "validator_sha256": sha256(root / VALIDATOR_REL),
        "input_freeze_sha256": sha256(root / INPUT_FREEZE_REL),
        "run_matrix_sha256": sha256(root / MATRIX_REL),
        "binding_receipt_sha256": sha256(root / BINDING_REL),
        "inactive_exec_freeze_sha256": sha256(root / FREEZE_REL),
        "infrastructure_input_sha256": sha256(root / INFRA_INPUT_REL),
        "infrastructure_correction_sha256": sha256(root / INFRA_CORRECTION_REL),
        "infrastructure_test_receipt_sha256": sha256(root / INFRA_TEST_RECEIPT_REL),
        "infrastructure_validator_sha256": sha256(root / INFRA_VALIDATOR_REL),
        "postcommit_preflight_sha256": sha256(root / POSTCOMMIT_PREFLIGHT_REL),
        "infrastructure_input_sha256": sha256(root / INFRA_INPUT_REL),
        "infrastructure_correction_sha256": sha256(root / INFRA_CORRECTION_REL),
        "infrastructure_test_receipt_sha256": sha256(root / INFRA_TEST_RECEIPT_REL),
        "infrastructure_validator_sha256": sha256(root / INFRA_VALIDATOR_REL),
        "postcommit_preflight_sha256": sha256(root / POSTCOMMIT_PREFLIGHT_REL),
    }
    require(all(activation[key] == value for key, value in expected_hashes.items()), "C02 activation hash drift")
    require(git(root, "rev-parse", "HEAD") == expected_head, "C02 HEAD drift")
    _authority_tree_clean(root)
    binding = load_json(root / BINDING_REL)
    committed = [
        ACTIVATION_REL.as_posix(), POLICY_REL.as_posix(), SOURCE_REL.as_posix(),
        TEST_REL.as_posix(), VALIDATOR_REL.as_posix(), INPUT_FREEZE_REL.as_posix(),
        MATRIX_REL.as_posix(), BINDING_REL.as_posix(), FREEZE_REL.as_posix(),
        C01_AUDIT_REL.as_posix(), C01_CLAIM_REL.as_posix(),
        INFRA_INPUT_REL.as_posix(), INFRA_CORRECTION_REL.as_posix(),
        INFRA_TEST_RECEIPT_REL.as_posix(), INFRA_VALIDATOR_REL.as_posix(),
        INFRA_VALIDATION_REL.as_posix(), POSTCOMMIT_PREFLIGHT_REL.as_posix(),
        INFRA_INPUT_REL.as_posix(), INFRA_CORRECTION_REL.as_posix(),
        INFRA_TEST_RECEIPT_REL.as_posix(), INFRA_VALIDATOR_REL.as_posix(),
        INFRA_VALIDATION_REL.as_posix(), POSTCOMMIT_PREFLIGHT_REL.as_posix(),
    ]
    require(all(_committed_equal(root, expected_head, relative) for relative in committed), "C02 committed byte drift")
    for pointer in binding["bound_files"]:
        require(sha256(root / pointer["path"]) == pointer["sha256"], f"C02 bound drift: {pointer['path']}")
    runtime = load_json(root / INPUT_FREEZE_REL)["runtime_identity"]
    require(git(graph, "rev-parse", "HEAD") == runtime["graph_revision"], "graph revision drift")
    require(git(graph, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph worktree dirty")
    require(sha256(graph / runtime["runtime_source_relative"]) == runtime["runtime_source_sha256"], "runtime source drift")
    require(Path(sys.prefix).resolve() == (root / ".venv").resolve(), "repository .venv inactive")
    require(Path(sys.executable).absolute() == (root / ".venv/bin/python").absolute(), "exact .venv command path inactive")
    require(sys.dont_write_bytecode, "C02 requires -B")
    require(sha256(Path(sys.executable).resolve()) == runtime["interpreter_executable_sha256"], "interpreter drift")
    require(not _cache_artifacts(root, graph), "C02 import cache present")
    require(attempt in {1, 2}, "attempt outside C02 freeze")
    if attempt == 2:
        _validate_retry(root, entry, expected_head)
    return policy, entry, activation


def _relative_failure(entry: Mapping[str, Any], attempt: int) -> str:
    return (
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/outputs/p2-i2/c02/failures/"
        f"{entry['mode']}/{entry['cell_id']}/{entry['branch_id']}/{entry['physical_order_id']}/"
        f"seed-{entry['seed']}/attempt-{attempt}.json"
    )


def _validate_retry(
    root: Path,
    entry: Mapping[str, Any],
    expected_head: str,
    retry_execution_source_sha256: str | None = None,
) -> None:
    helpers = _safe_helpers(root)
    failure_path = _relative_failure(entry, 1)
    failure = helpers._read_governed_json(root, failure_path)
    require(failure["entry_id"] == entry["entry_id"] and failure["attempt"] == 1, "C02 retry predecessor drift")
    if failure["owner_authorized_full_HEAD"] != expected_head:
        correction = load_json(root / INFRA_CORRECTION_REL)
        activation = load_json(root / ACTIVATION_REL)
        require(
            correction["artifact_id"] == "P2-I2-I08A-VENV-INFRASTRUCTURE-CORRECTION"
            and correction["scope"]["scientific_change_count"] == 0
            and correction["scope"]["new_iteration_or_cycle"] is False,
            "C02 retry correction kind drift",
        )
        require(
            correction["predecessor_attempt"]["owner_authorized_full_HEAD"]
            == failure["owner_authorized_full_HEAD"]
            and correction["predecessor_attempt"]["claim_sha256"]
            == helpers._governed_sha256(root, entry["primary_claim_path"])
            and correction["predecessor_attempt"]["failure_sha256"]
            == helpers._governed_sha256(root, failure_path),
            "C02 retry correction predecessor drift",
        )
        require(
            correction["corrected_authority"]["expected_head_source"]
            == "current_committed_normalized_retry_command"
            and correction["corrected_authority"]["execution_source_sha256"]
            == (retry_execution_source_sha256 or sha256(root / SOURCE_REL))
            and activation["infrastructure_correction_sha256"]
            == sha256(root / INFRA_CORRECTION_REL),
            "C02 retry correction authority drift",
        )
    require(failure["retry_eligibility"] is True, "C02 retry not mechanically eligible")
    require(failure["child_attestation_present"] is True, "C02 retry lacks child attestation")
    require(failure["zero_state_counters"]["model_or_adapter_construction_started"] == 0, "C02 retry after model start")
    require(helpers._governed_leaf_exists(root, entry["primary_claim_path"]), "C02 primary claim absent")
    require(helpers._governed_leaf_absent(root, entry["primary_output_path"]), "C02 primary output exists")


def _validate_terminal_execution_authority(
    root: Path,
    activation: Mapping[str, Any],
    entry: Mapping[str, Any],
    attempt: int,
    expected_head: str,
    output_relative: str,
    record: Mapping[str, Any],
) -> str:
    binding = record.get("runtime_binding_receipt", {})
    recorded_head = binding.get("owner_authorized_full_HEAD")
    require(isinstance(recorded_head, str) and re.fullmatch(r"[0-9a-f]{40}", recorded_head) is not None, "C02 terminal execution HEAD invalid")
    if recorded_head == expected_head:
        require(
            binding.get("execution_source_sha256") == activation["execution_source_sha256"]
            and binding.get("policy_sha256") == activation["policy_sha256"],
            "C02 current-head terminal authority drift",
        )
        return "current_execution_head"
    continuation = activation.get("continuation_authority", {})
    admitted = continuation.get("admitted_prior_terminals", [])
    require(
        continuation.get("new_iteration_or_cycle") is False
        and continuation.get("scientific_change_count") == 0
        and len(admitted) == 1,
        "C02 prior-terminal continuation authority absent or broad",
    )
    matches = [
        row for row in admitted
        if row.get("entry_id") == entry["entry_id"]
        and row.get("attempt") == attempt
        and row.get("owner_authorized_full_HEAD") == recorded_head
        and row.get("output_path") == output_relative
    ]
    require(len(matches) == 1, "C02 terminal historical HEAD not explicitly admitted")
    admission = matches[0]
    claim_relative = entry["primary_claim_path"] if attempt == 1 else entry["retry_claim_path"]
    helpers = _safe_helpers(root)
    require(admission.get("claim_path") == claim_relative, "C02 admitted checkpoint claim path drift")
    require(
        helpers._governed_sha256(root, claim_relative) == admission.get("claim_sha256")
        and helpers._governed_sha256(root, output_relative) == admission.get("output_sha256"),
        "C02 admitted checkpoint governed byte drift",
    )
    require(
        binding.get("execution_source_sha256") == admission.get("execution_source_sha256")
        and binding.get("policy_sha256") == admission.get("policy_sha256"),
        "C02 admitted checkpoint authority byte drift",
    )
    return "accepted_checkpoint_head"


def _claim_document(root: Path, entry: Mapping[str, Any], attempt: int, head: str, argv: Sequence[str]) -> dict[str, Any]:
    return {
        "artifact_id": "P2-I2-C02-PERMANENT-ATTEMPT-CLAIM",
        "artifact_version": "1.0.0",
        "cycle_id": CYCLE_ID,
        "entry_id": entry["entry_id"],
        "attempt": attempt,
        "owner_authorized_full_HEAD": head,
        "normalized_command": [".venv/bin/python", "-B", SOURCE_REL.as_posix(), *argv],
        "supervisor_owns_final_receipt": True,
        "address_space_limit_applied": False,
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
        "permanent": True,
    }


def _venv_python(root: Path) -> Path:
    executable = (root / ".venv/bin/python").absolute()
    require(executable.exists() and not executable.is_dir(), "repository .venv Python absent")
    return executable


def _worker_command(root: Path, entry: Mapping[str, Any], attempt: int, head: str, graph_argument: str) -> list[str]:
    return [
        os.fspath(_venv_python(root)), "-B", SOURCE_REL.as_posix(), "worker-entry",
        "--expected-head", head, "--graph-root", graph_argument,
        "--mode", str(entry["mode"]), "--cell-id", str(entry["cell_id"]),
        "--branch-id", str(entry["branch_id"]), "--physical-order-id", str(entry["physical_order_id"]),
        "--seed", str(entry["seed"]), "--attempt", str(attempt),
    ]


def _bounded_stderr(payload: bytes) -> tuple[str, str, bool]:
    clipped = payload[:MAX_STDERR_BYTES]
    return clipped.decode("utf-8", errors="replace"), hashlib.sha256(payload).hexdigest(), len(payload) > len(clipped)


def _child_envelope(stdout: bytes) -> dict[str, Any] | None:
    try:
        value = json.loads(stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) and value.get("artifact_id") == "P2-I2-C02-WORKER-ENVELOPE" else None


def _run_child_process(
    command: Sequence[str],
    cwd: Path,
    environment: Mapping[str, str],
    timeout_seconds: int,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            env=dict(environment),
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        return {
            "timed_out": False,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired as error:
        return {
            "timed_out": True,
            "returncode": None,
            "stdout": error.stdout or b"",
            "stderr": error.stderr or b"",
        }


def supervise_entry(
    root: Path,
    graph: Path,
    policy: Mapping[str, Any],
    entry: Mapping[str, Any],
    attempt: int,
    head: str,
    actual_argv: Sequence[str],
) -> dict[str, Any]:
    helpers = _safe_helpers(root)
    output_relative = entry["primary_output_path"] if attempt == 1 else entry["retry_output_path"]
    claim_relative = entry["primary_claim_path"] if attempt == 1 else entry["retry_claim_path"]
    failure_relative = _relative_failure(entry, attempt)
    require(helpers._governed_leaf_absent(root, output_relative), "C02 output exists or unsafe")
    require(helpers._governed_leaf_absent(root, claim_relative), "C02 attempt already claimed or unsafe")
    require(helpers._governed_leaf_absent(root, failure_relative), "C02 failure exists or unsafe")
    helpers._exclusive_json(root, claim_relative, _claim_document(root, entry, attempt, head, actual_argv))
    command = _worker_command(root, entry, attempt, head, policy["runtime_invocation_identity"]["graph_root_argument"])
    environment = os.environ.copy()
    environment["P2_I2_C02_SUPERVISED_ENTRY_ID"] = entry["entry_id"]
    environment["P2_I2_C02_SUPERVISED_HEAD"] = head
    child = _run_child_process(
        command,
        root,
        environment,
        int(policy["resource_envelope_per_worker"]["max_runtime_seconds"]),
    )
    timed_out = child["timed_out"]
    returncode = child["returncode"]
    stdout = child["stdout"]
    stderr = child["stderr"]
    require(not _cache_artifacts(root, graph), "C02 child created import cache")
    require(git(graph, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph changed during C02 child")
    envelope = _child_envelope(stdout)
    if not timed_out and returncode == 0 and envelope is not None and envelope.get("status") == "success":
        result = envelope["result"]
        require(result["cycle_id"] == CYCLE_ID and result["entry_identity"]["entry_id"] == entry["entry_id"], "C02 child result drift")
        stderr_text, stderr_digest, clipped = _bounded_stderr(stderr)
        result["artifact_id"] = "P2-I2-C02-RUN-RECORD"
        result["supervisor_receipt"] = {
            "child_returncode": returncode,
            "child_attestation_present": True,
            "stderr_text": stderr_text,
            "stderr_sha256": stderr_digest,
            "stderr_truncated": clipped,
            "address_space_limit_applied": False,
            "max_runtime_seconds": policy["resource_envelope_per_worker"]["max_runtime_seconds"],
            "max_file_size_mb": policy["resource_envelope_per_worker"]["max_file_size_mb"],
        }
        helpers._exclusive_json(root, output_relative, result)
        return {"status": "success", "entry_id": entry["entry_id"], "attempt": attempt}
    stderr_text, stderr_digest, clipped = _bounded_stderr(stderr)
    counters = envelope.get("zero_state_counters") if envelope is not None else None
    attested_failure = envelope is not None and envelope.get("status") == "python_failure" and isinstance(counters, dict)
    retry_eligible = bool(
        attested_failure
        and counters.get("model_or_adapter_construction_started") == 0
        and counters.get("models_constructed") == 0
        and counters.get("adapters_constructed") == 0
        and counters.get("candidate_or_control_operations_started") == 0
    )
    failure = {
        "artifact_id": "P2-I2-C02-SUPERVISOR-FAILURE-RECEIPT",
        "artifact_version": "1.0.0",
        "cycle_id": CYCLE_ID,
        "entry_id": entry["entry_id"],
        "attempt": attempt,
        "owner_authorized_full_HEAD": head,
        "child_returncode": returncode,
        "child_timed_out": timed_out,
        "child_attestation_present": attested_failure,
        "failure_phase": envelope.get("failure_phase") if attested_failure else "unknown_native_or_unattested_termination",
        "exception_class": envelope.get("exception_class") if attested_failure else None,
        "exception_message": envelope.get("exception_message") if attested_failure else None,
        "zero_state_counters": counters,
        "stderr_text": stderr_text,
        "stderr_sha256": stderr_digest,
        "stderr_truncated": clipped,
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "output_absent": helpers._governed_leaf_absent(root, output_relative),
        "claim_retained": helpers._governed_leaf_exists(root, claim_relative),
        "retry_eligibility": retry_eligible,
        "retry_unknown_phase_is_refused": not attested_failure,
        "address_space_limit_applied": False,
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
    }
    helpers._exclusive_json(root, failure_relative, failure)
    raise ContractError(f"C02 child failed; receipt retained at {failure_relative}")


def worker_entry(root: Path, graph: Path, identity: Mapping[str, Any], attempt: int, head: str) -> dict[str, Any]:
    require(Path(sys.executable).absolute() == _venv_python(root), "C02 worker bypassed repository .venv command")
    require(Path(sys.prefix).resolve() == (root / ".venv").resolve(), "C02 worker repository .venv inactive")
    require(os.environ.get("P2_I2_C02_SUPERVISED_HEAD") == head, "C02 worker lacks supervisor HEAD")
    matrix = load_json(root / MATRIX_REL)
    entry = _find_entry(matrix, identity)
    require(os.environ.get("P2_I2_C02_SUPERVISED_ENTRY_ID") == entry["entry_id"], "C02 worker lacks supervisor entry")
    envelope = load_json(root / POLICY_REL)["resource_envelope_per_worker"]
    max_file = int(envelope["max_file_size_mb"]) * 1024 * 1024
    soft, hard = resource.getrlimit(resource.RLIMIT_FSIZE)
    resource.setrlimit(resource.RLIMIT_FSIZE, (max_file if hard == resource.RLIM_INFINITY else min(max_file, hard), hard))
    require(resource.getrlimit(resource.RLIMIT_AS)[0] == resource.RLIM_INFINITY, "C02 worker inherited address-space limit")
    module = _c01_module(root)
    effective, _, _ = module.load_effective_policy(root)
    module.CYCLE_ID = CYCLE_ID
    module.POLICY_REL = POLICY_REL
    module.SOURCE_REL = SOURCE_REL
    module.OUTPUT_ROOT_REL = OUTPUT_ROOT_REL
    effective["resource_envelope_per_entry"] = {
        "max_runtime_seconds": envelope["max_runtime_seconds"],
        "max_file_size_mb": envelope["max_file_size_mb"],
        "address_space_limit": None,
        "hardware": envelope["hardware"],
    }
    runtime_state = {
        "pygrc_imports": 0,
        "model_or_adapter_construction_started": 0,
        "models_constructed": 0,
        "adapters_constructed": 0,
        "candidate_or_control_operations_started": 0,
    }
    parent_argv = normalized_run_argv(entry, attempt, head)
    try:
        result = module.execute_entry(
            root,
            graph,
            effective,
            {**entry, "attempt": attempt, "owner_authorized_full_HEAD": head, "normalized_argv": parent_argv},
            runtime_state,
        )
        return {"artifact_id": "P2-I2-C02-WORKER-ENVELOPE", "status": "success", "result": result}
    except BaseException as error:
        return {
            "artifact_id": "P2-I2-C02-WORKER-ENVELOPE",
            "status": "python_failure",
            "failure_phase": "worker_execute_entry",
            "exception_class": type(error).__name__,
            "exception_message": str(error),
            "zero_state_counters": runtime_state,
        }


def build_manifest(root: Path, expected_head: str) -> dict[str, Any]:
    require(sys.dont_write_bytecode, "C02 manifest construction requires -B")
    require(re.fullmatch(r"[0-9a-f]{40}", expected_head) is not None, "full HEAD required")
    require(not (root / MANIFEST_REL).exists(), "C02 manifest already exists")
    activation = load_json(root / ACTIVATION_REL)
    require(
        activation["artifact_id"] == "P2-I2-C02-OWNER-ACCEPTED-EXECUTION-AUTHORIZATION"
        and activation["cycle_id"] == CYCLE_ID
        and activation["owner_acceptance"] is True
        and activation["candidate_execution_authorized"] is True
        and activation["I08_authorized"] is True,
        "C02 activation absent",
    )
    expected_hashes = {
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
        "test_sha256": sha256(root / TEST_REL),
        "validator_sha256": sha256(root / VALIDATOR_REL),
        "input_freeze_sha256": sha256(root / INPUT_FREEZE_REL),
        "run_matrix_sha256": sha256(root / MATRIX_REL),
        "binding_receipt_sha256": sha256(root / BINDING_REL),
        "inactive_exec_freeze_sha256": sha256(root / FREEZE_REL),
    }
    require(all(activation[key] == value for key, value in expected_hashes.items()), "C02 manifest activation hash drift")
    require(git(root, "rev-parse", "HEAD") == expected_head, "manifest HEAD drift")
    _authority_tree_clean(root)
    binding = load_json(root / BINDING_REL)
    for pointer in binding["bound_files"]:
        require(sha256(root / pointer["path"]) == pointer["sha256"], f"C02 manifest bound drift: {pointer['path']}")
    committed = [
        ACTIVATION_REL.as_posix(), POLICY_REL.as_posix(), SOURCE_REL.as_posix(),
        TEST_REL.as_posix(), VALIDATOR_REL.as_posix(), INPUT_FREEZE_REL.as_posix(),
        MATRIX_REL.as_posix(), BINDING_REL.as_posix(), FREEZE_REL.as_posix(),
        C01_AUDIT_REL.as_posix(), C01_CLAIM_REL.as_posix(),
    ]
    require(all(_committed_equal(root, expected_head, relative) for relative in committed), "C02 manifest committed byte drift")
    runtime = load_json(root / INPUT_FREEZE_REL)["runtime_identity"]
    require(Path(sys.prefix).resolve() == (root / ".venv").resolve(), "repository .venv inactive")
    require(Path(sys.executable).absolute() == (root / ".venv/bin/python").absolute(), "exact .venv command path inactive")
    require(sha256(Path(sys.executable).resolve()) == runtime["interpreter_executable_sha256"], "manifest interpreter drift")
    matrix = load_json(root / MATRIX_REL)
    helpers = _safe_helpers(root)
    terminals: list[dict[str, Any]] = []
    for entry in matrix["entries"]:
        primary = helpers._governed_leaf_exists(root, entry["primary_output_path"])
        retry = helpers._governed_leaf_exists(root, entry["retry_output_path"])
        require(primary != retry, f"missing or ambiguous C02 terminal: {entry['entry_id']}")
        attempt = 1 if primary else 2
        relative = entry["primary_output_path"] if primary else entry["retry_output_path"]
        claim_relative = entry["primary_claim_path"] if primary else entry["retry_claim_path"]
        failure_relative = _relative_failure(entry, attempt)
        require(helpers._governed_leaf_exists(root, claim_relative), "C02 terminal claim absent")
        require(helpers._governed_leaf_absent(root, failure_relative), "C02 terminal output and failure both exist")
        if primary:
            require(helpers._governed_leaf_absent(root, entry["retry_claim_path"]), "C02 retry claim exists after primary success")
            require(helpers._governed_leaf_absent(root, _relative_failure(entry, 2)), "C02 retry failure exists after primary success")
        record = helpers._read_governed_json(root, relative)
        if not primary:
            _validate_retry(
                root,
                entry,
                expected_head,
                record.get("runtime_binding_receipt", {}).get("execution_source_sha256"),
            )
        identity = record.get("entry_identity", {})
        for key in ("entry_id", "mode", "cell_id", "branch_id", "physical_order_id", "seed"):
            require(identity.get(key) == entry[key], f"C02 terminal identity drift: {key}")
        require(identity.get("attempt") == attempt, "C02 terminal attempt drift")
        execution_authority_kind = _validate_terminal_execution_authority(
            root, activation, entry, attempt, expected_head, relative, record,
        )
        raw = record.get("raw_response_record", {})
        window = record.get("window_validity_receipt", {})
        value = raw.get("value")
        require(record.get("cycle_id") == CYCLE_ID, "C02 terminal cycle drift")
        require(raw.get("operational_null") is False and window.get("valid") is True, "C02 nonevaluable terminal")
        require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)), "C02 nonnumeric terminal")
        terminals.append({
            "entry_id": entry["entry_id"],
            "attempt": attempt,
            "output_path": relative,
            "output_sha256": helpers._governed_sha256(root, relative),
            "raw_response_value": float(value),
            "execution_authority_kind": execution_authority_kind,
            "execution_head": record["runtime_binding_receipt"]["owner_authorized_full_HEAD"],
        })
    require(len(terminals) == 234, "C02 matrix incomplete")
    document = {
        "artifact_id": "P2-I2-C02-EXECUTION-MANIFEST",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08",
        "cycle_id": CYCLE_ID,
        "status": "complete_all_registered_entries_evaluable",
        "owner_authorized_full_HEAD": expected_head,
        "run_matrix_sha256": sha256(root / MATRIX_REL),
        "run_matrix_semantic_digest": matrix["semantic_digest"],
        "required_entry_count": 234,
        "evaluable_terminal_count": 234,
        "missing_entry_count": 0,
        "nonevaluable_entry_count": 0,
        "ambiguous_entry_count": 0,
        "terminals": terminals,
        "completion_rule": "exact_matrix_paths_only_all_234_exactly_one_terminal_and_all_evaluable",
        "execution_head_rule": "current_execution_head_except_exact_owner_accepted_entry_001_checkpoint",
        "scientific_interpretation": None,
    }
    document["canonical_payload_digest"] = digest(document)
    write_new(root / MANIFEST_REL, document)
    return document


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("build-freeze")
    manifest = subparsers.add_parser("build-execution-manifest")
    manifest.add_argument("--expected-head", required=True)
    for name in ("run-entry", "worker-entry"):
        run = subparsers.add_parser(name)
        run.add_argument("--expected-head", required=True)
        run.add_argument("--graph-root", required=True)
        run.add_argument("--mode", required=True)
        run.add_argument("--cell-id", required=True)
        run.add_argument("--branch-id", required=True)
        run.add_argument("--physical-order-id", required=True)
        run.add_argument("--seed", type=int, required=True)
        run.add_argument("--attempt", type=int, required=True)
        if name == "run-entry":
            run.add_argument("--output", required=True)
    actual_argv = list(sys.argv[1:] if argv is None else argv)
    args = parser.parse_args(actual_argv)
    root = repo_root()
    if args.command == "build-freeze":
        print(json.dumps(build_freeze(root), sort_keys=True))
        return 0
    require(sys.argv[0] == SOURCE_REL.as_posix(), "C02 source argument drift")
    require(sys.dont_write_bytecode, "C02 requires .venv/bin/python -B")
    if args.command == "build-execution-manifest":
        document = build_manifest(root, args.expected_head)
        print(json.dumps({"entries": len(document["terminals"]), "status": document["status"]}, sort_keys=True))
        return 0
    graph_argument = Path(args.graph_root)
    require(not graph_argument.is_absolute(), "absolute C02 graph root prohibited")
    graph = (root / graph_argument).resolve()
    identity = {"mode": args.mode, "cell_id": args.cell_id, "branch_id": args.branch_id, "physical_order_id": args.physical_order_id, "seed": args.seed}
    if args.command == "worker-entry":
        envelope = worker_entry(root, graph, identity, args.attempt, args.expected_head)
        print(json.dumps(envelope, sort_keys=True))
        return 0 if envelope["status"] == "success" else 20
    policy, entry, _ = validate_activation(root, graph, identity, args.attempt, args.expected_head, actual_argv)
    require(args.graph_root == policy["runtime_invocation_identity"]["graph_root_argument"], "C02 graph argument drift")
    output = Path(args.output)
    require(not output.is_absolute(), "absolute C02 output prohibited")
    expected_output = entry["primary_output_path"] if args.attempt == 1 else entry["retry_output_path"]
    require(output.as_posix() == expected_output, "C02 output path drift")
    result = supervise_entry(root, graph, policy, entry, args.attempt, args.expected_head, actual_argv)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
