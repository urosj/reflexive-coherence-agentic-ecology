#!/usr/bin/env python3
"""Frozen P2-I2 cycle builder, isolated entry runner, and completion surface.

The build-freeze command is candidate-free and does not import PyGRC. The
run-entry command fails closed unless a later owner-accepted activation record
binds the committed inactive freeze and exact entry. I07A adds beneath-root
artifact I/O, import-cache isolation, row-local retry reconstruction, and an
exact-path fail-closed completion manifest.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import resource
import signal
import stat
import subprocess
import sys
from typing import Any, Iterable, Mapping, Sequence


EXPERIMENT_REL = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
BASE_POLICY_REL = EXPERIMENT_REL / "configs" / "p2_i2_c01_execution_policy.json"
POLICY_REL = EXPERIMENT_REL / "configs" / "p2_i2_c01_execution_policy_v2.json"
REGISTRATION_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "i06-three-mode-registration.json"
I06_VALIDATION_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "i06-registration-validation.json"
OVERLAY_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "i06b-execution-readiness-overlay.json"
RESUMPTION_FREEZE_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07-candidate-cycle-resumption-input-freeze.json"
SOURCE_REL = EXPERIMENT_REL / "scripts" / "p2_i2_execution.py"
VALIDATOR_REL = EXPERIMENT_REL / "scripts" / "p2_i2_i07a_validate.py"
TEST_REL = EXPERIMENT_REL / "implementation" / "tests" / "test_p2_i2_execution_freeze.py"
I07_VALIDATION_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-candidate-free-validation.json"
I07A_INPUT_REL = EXPERIMENT_REL / "contracts" / "p2-i2" / "c01" / "i07a-cross-entry-isolation-input-freeze.json"
OUTPUT_ROOT_REL = EXPERIMENT_REL / "outputs" / "p2-i2" / "c01"
CYCLE_ID = "P2-I2-C01"
_LIVE_ENTRY_STARTS = 0


class ContractError(RuntimeError):
    """Raised when a frozen execution or authority contract fails closed."""


def repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise ContractError("repository root not found")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError(f"JSON object required: {path.name}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


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
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _verify_pointer(root: Path, pointer: Mapping[str, Any]) -> None:
    path = root / str(pointer["path"])
    require(path.is_file(), f"missing bound file: {pointer['path']}")
    require(sha256(path) == pointer["sha256"], f"bound file drift: {pointer['path']}")


def load_effective_policy(root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    root = repo_root() if root is None else root
    successor = load_json(root / POLICY_REL)
    composition = successor["composition"]
    for key in (
        "base_blocked_policy",
        "resumption_input_freeze",
        "I07A_cross_entry_isolation_input_freeze",
        "accepted_I06B_overlay",
        "accepted_I06B_authority",
    ):
        _verify_pointer(root, composition[key])
    base = load_json(root / composition["base_blocked_policy"]["path"])
    overlay = load_json(root / composition["accepted_I06B_overlay"]["path"])
    require(base["cycle_id"] == successor["cycle_id"] == CYCLE_ID, "cycle identity drift")
    require("blocked" in base["status"], "base policy is not retained blocked history")
    require(len(base["known_registration_blockers"]) == 3, "base blocker history drift")
    require(all(row["status"] == "closed_by_accepted_I06B" for row in successor["blocker_dispositions"]), "I06B blocker closeout incomplete")
    effective = deepcopy(base)
    effective["artifact_id"] = successor["artifact_id"]
    effective["artifact_version"] = successor["artifact_version"]
    effective["status"] = successor["status"]
    effective["known_registration_blockers"] = []
    effective["input_freeze"] = deepcopy(composition["resumption_input_freeze"])
    effective["successor"] = deepcopy(successor)
    effective["artifact_contract"] = deepcopy(successor["artifact_contract"])
    effective["authorization"] = deepcopy(successor["activation_and_gate_boundary"])
    return effective, successor, overlay


def _order_ids(plan: Mapping[str, Any]) -> list[str]:
    if plan["order_scope"] in {"explicit_registration", "I04R2_complete_arm_lift"}:
        return ["q1_then_q2", "q2_then_q1"]
    return ["not_applicable"]


def _output_path(template: str, entry: Mapping[str, Any], attempt: int) -> str:
    values = {**entry, "attempt": attempt}
    return template.format(**values)


def normalized_run_argv(
    successor: Mapping[str, Any],
    entry: Mapping[str, Any],
    attempt: int,
    expected_head: str,
) -> list[str]:
    invocation = successor["runtime_invocation_identity"]
    output_path = entry["primary_output_path"] if attempt == 1 else entry["retry_output_path"]
    values = {
        **entry,
        "attempt": attempt,
        "output_path": output_path,
        "expected_head": expected_head,
    }
    return [str(token).format(**values) for token in invocation["argument_order"]]


def expand_run_matrix(effective: Mapping[str, Any]) -> list[dict[str, Any]]:
    successor = effective["successor"]
    artifacts = successor["artifact_contract"]
    seeds = successor["matrix"]["seeds"]
    entries: list[dict[str, Any]] = []
    sequence = 0
    for mode in effective["matrix"]["mode_order"]:
        for cell_id in effective["matrix"]["cell_order"]:
            for plan in effective["branch_plans"]:
                if plan["cell_id"] != cell_id or mode not in plan["modes"]:
                    continue
                for order_id in _order_ids(plan):
                    for seed in seeds:
                        sequence += 1
                        identity = {
                            "cycle_id": CYCLE_ID,
                            "mode": mode,
                            "cell_id": cell_id,
                            "branch_id": plan["branch_id"],
                            "physical_order_id": order_id,
                            "seed": int(seed),
                            "attempt": 1,
                        }
                        entry = {
                                **identity,
                                "sequence_index": sequence,
                                "entry_id": (
                                    f"{CYCLE_ID}:{mode}:{cell_id}:{plan['branch_id']}:"
                                    f"{order_id}:seed-{seed}"
                                ),
                                "order_scope": plan["order_scope"],
                                "analysis_role": plan["analysis_role"],
                                "candidate_chain": plan["candidate_chain"],
                                "primary_output_path": _output_path(artifacts["primary_output_template"], identity, 1),
                                "retry_output_path": _output_path(artifacts["retry_output_template"], identity, 2),
                                "primary_claim_path": _output_path(artifacts["claim_template"], identity, 1),
                                "retry_claim_path": _output_path(artifacts["claim_template"], identity, 2),
                        }
                        entry["normalized_primary_argv_template"] = normalized_run_argv(
                            successor, entry, 1, "<OWNER_AUTHORIZED_FULL_HEAD>"
                        )
                        entry["normalized_retry_argv_template"] = normalized_run_argv(
                            successor, entry, 2, "<OWNER_AUTHORIZED_FULL_HEAD>"
                        )
                        entries.append(entry)
    require(len(entries) == 234, "primary matrix count drift")
    require(len({row["entry_id"] for row in entries}) == 234, "duplicate matrix entry")
    counts = {
        mode: sum(1 for row in entries if row["mode"] == mode) // len(seeds)
        for mode in effective["matrix"]["mode_order"]
    }
    require(counts == successor["matrix"]["mode_branch_order_counts"], "mode matrix count drift")
    return entries


def _matrix_document(entries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    payload = {
        "artifact_id": "P2-I2-C01-RUN-MATRIX",
        "artifact_version": "1.1.0",
        "iteration_id": "P2-I2-I07A",
        "cycle_id": CYCLE_ID,
        "status": "inactive_pre_execution_matrix_pending_owner_acceptance",
        "primary_entry_count": len(entries),
        "maximum_conditional_retry_count": len(entries),
        "maximum_total_attempt_count": 2 * len(entries),
        "entries": list(entries),
        "candidate_execution_authorized": False,
        "evidence_effect": "none_pre_execution_matrix_only",
    }
    payload["semantic_digest"] = digest({key: value for key, value in payload.items() if key != "semantic_digest"})
    return payload


def _binding_document(root: Path, matrix: Mapping[str, Any]) -> dict[str, Any]:
    freeze = load_json(root / RESUMPTION_FREEZE_REL)
    successor = load_json(root / POLICY_REL)
    bound_files: list[dict[str, str]] = []
    for item in freeze["retained_blocked_drafts"] + freeze["progression_authority"]:
        _verify_pointer(root, item)
        bound_files.append({"path": item["path"], "role": item["role"], "sha256": item["sha256"]})
    local_roles = [
        (POLICY_REL, "effective_policy_successor"),
        (SOURCE_REL, "future_execution_source"),
        (VALIDATOR_REL, "candidate_free_validator"),
        (TEST_REL, "focused_pure_tests"),
        (RESUMPTION_FREEZE_REL, "resumption_input_freeze"),
        (I07A_INPUT_REL, "I07A_cross_entry_isolation_input_freeze"),
    ]
    for relative, role in local_roles:
        bound_files.append({"path": relative.as_posix(), "role": role, "sha256": sha256(root / relative)})
    document: dict[str, Any] = {
        "artifact_id": "P2-I2-C01-EXECUTION-BINDING-RECEIPT",
        "artifact_version": "1.1.0",
        "iteration_id": "P2-I2-I07A",
        "cycle_id": CYCLE_ID,
        "status": "inactive_exact_binding_pending_owner_acceptance",
        "bound_files": bound_files,
        "run_matrix": {
            "path": successor["artifact_contract"]["run_matrix_path"],
            "semantic_digest": matrix["semantic_digest"],
            "primary_entry_count": matrix["primary_entry_count"],
        },
        "runtime_identity": deepcopy(freeze["runtime_identity"]),
        "construction_process": {
            "python_command": ".venv/bin/python",
            "pygrc_imports": 0,
            "models_constructed": 0,
            "candidate_or_control_operations": 0,
            "packets_scheduled_or_processed": 0,
            "scientific_result": False,
        },
        "gate_boundary": {
            "REG_GATE": "passed_after_explicit_owner_acceptance_of_I06B",
            "EXEC_FREEZE": "closed",
            "candidate_execution_authorized": False,
            "I08_authorized": False,
            "commit_authorized": False,
        },
        "evidence_effect": "pre_execution_identity_binding_only",
    }
    document["canonical_payload_digest"] = digest({key: value for key, value in document.items() if key != "canonical_payload_digest"})
    return document


def _exec_freeze_document(root: Path, matrix: Mapping[str, Any], binding: Mapping[str, Any]) -> dict[str, Any]:
    successor = load_json(root / POLICY_REL)
    artifacts = successor["artifact_contract"]
    document: dict[str, Any] = {
        "artifact_id": "P2-I2-C01-INACTIVE-EXEC-FREEZE",
        "artifact_version": "1.1.0",
        "iteration_id": "P2-I2-I07A",
        "lane_id": "AE01-L02",
        "cycle_id": CYCLE_ID,
        "status": "inactive_pending_candidate_free_validation_and_explicit_owner_acceptance",
        "evidence_effect": "none_pre_execution_authorization_only",
        "authorization_gate": "P2-I2-EXEC-FREEZE",
        "authorization_scope": "exact_cycle_mode_cell_branch_order_seed_attempt_resource_only",
        "candidate_execution_authorized": False,
        "I08_authorized": False,
        "commit_authorized": False,
        "activation_record": {
            "path": artifacts["activation_record_path"],
            "required_before_any_run": True,
            "required_absent_during_I07A": True,
            "present_at_freeze": (root / artifacts["activation_record_path"]).exists(),
        },
        "bound_identity": {
            "policy_path": POLICY_REL.as_posix(),
            "policy_sha256": sha256(root / POLICY_REL),
            "execution_source_path": SOURCE_REL.as_posix(),
            "execution_source_sha256": sha256(root / SOURCE_REL),
            "validator_path": VALIDATOR_REL.as_posix(),
            "validator_sha256": sha256(root / VALIDATOR_REL),
            "test_path": TEST_REL.as_posix(),
            "test_sha256": sha256(root / TEST_REL),
            "resumption_freeze_path": RESUMPTION_FREEZE_REL.as_posix(),
            "resumption_freeze_sha256": sha256(root / RESUMPTION_FREEZE_REL),
            "i07a_input_freeze_path": I07A_INPUT_REL.as_posix(),
            "i07a_input_freeze_sha256": sha256(root / I07A_INPUT_REL),
            "run_matrix_path": artifacts["run_matrix_path"],
            "run_matrix_file_sha256": sha256(root / artifacts["run_matrix_path"]),
            "run_matrix_semantic_digest": matrix["semantic_digest"],
            "binding_receipt_path": artifacts["binding_receipt_path"],
            "binding_receipt_file_sha256": sha256(root / artifacts["binding_receipt_path"]),
            "binding_receipt_payload_digest": binding["canonical_payload_digest"],
        },
        "matrix": {
            "primary_entry_count": matrix["primary_entry_count"],
            "maximum_conditional_retry_count": matrix["maximum_conditional_retry_count"],
            "maximum_total_attempt_count": matrix["maximum_total_attempt_count"],
            "seeds": successor["matrix"]["seeds"],
            "mode_branch_order_counts": successor["matrix"]["mode_branch_order_counts"],
        },
        "resource_envelope_per_entry": load_json(root / BASE_POLICY_REL)["resource_envelope_per_entry"],
        "retry_policy": deepcopy(successor["retry_policy"]),
        "claim_policy": {
            "template": artifacts["claim_template"],
            "semantics": artifacts["claim_semantics"],
            "claim_before_runtime_import_or_model": True,
            "claim_survives_every_failure": True,
        },
        "output_contract": deepcopy(artifacts),
        "future_activation_requirements": [
            "explicit owner acceptance of this exact inactive freeze",
            "separate tracked activation record",
            "activation record is committed before execution",
            "full committed HEAD is supplied through the separately owner-authorized normalized command to avoid self-reference",
            "runtime HEAD and clean authority tree/index match that command binding",
            "activation binds policy, source, validator, matrix, binding, and inactive freeze hashes",
            "activation binds the passed I07A candidate-free validation hash",
            "repository and PyGRC import roots contain no bytecode cache and the live interpreter has -B active",
            "exact entry is present in run matrix",
            "primary or mechanically eligible current-entry-only conditional retry attempt",
            "permanent atomic claim and governed output both absent before start",
            "every claim, output, and failure path is opened beneath the governed root without following symlink components",
            "graph checkout exact and clean before and after attempt",
        ],
        "review_boundary": {
            "owner_review_required": True,
            "validation_can_activate": False,
            "candidate_outcomes_absent_required": True,
            "I07_returns_uncommitted": True,
        },
    }
    require(not document["activation_record"]["present_at_freeze"], "activation record already exists")
    document["canonical_payload_digest"] = digest({key: value for key, value in document.items() if key != "canonical_payload_digest"})
    return document


def write_new(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(pretty_bytes(value))


def build_freeze(root: Path | None = None) -> dict[str, Any]:
    root = repo_root() if root is None else root
    effective, successor, _ = load_effective_policy(root)
    artifacts = successor["artifact_contract"]
    output_paths = [root / artifacts[key] for key in ("run_matrix_path", "binding_receipt_path", "exec_freeze_path")]
    require(not any(path.exists() or path.is_symlink() for path in output_paths), "freeze output already exists")
    require(not (root / artifacts["activation_record_path"]).exists(), "activation record must be absent")
    matrix = _matrix_document(expand_run_matrix(effective))
    write_new(output_paths[0], matrix)
    binding = _binding_document(root, matrix)
    write_new(output_paths[1], binding)
    freeze = _exec_freeze_document(root, matrix, binding)
    write_new(output_paths[2], freeze)
    return {
        "run_matrix_entries": matrix["primary_entry_count"],
        "binding_files": len(binding["bound_files"]),
        "exec_freeze_status": freeze["status"],
        "candidate_execution_authorized": freeze["candidate_execution_authorized"],
    }


def _find_entry(matrix: Mapping[str, Any], identity: Mapping[str, Any]) -> dict[str, Any]:
    keys = ("mode", "cell_id", "branch_id", "physical_order_id", "seed")
    matches = [row for row in matrix["entries"] if all(row[key] == identity[key] for key in keys)]
    require(len(matches) == 1, "entry is outside exact run matrix")
    return dict(matches[0])


def _clean_repo(root: Path) -> bool:
    return git(root, "status", "--porcelain=v1", "--untracked-files=all") == ""


def _authority_tree_clean(root: Path) -> bool:
    """Require clean tracked authority while allowing prior governed C01 outputs."""

    allowed = (EXPERIMENT_REL / "outputs" / "p2-i2" / "c01").as_posix() + "/"
    status = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        check=True,
        capture_output=True,
    ).stdout
    for raw in status.split(b"\0"):
        if not raw:
            continue
        value = raw.decode("utf-8")
        require(len(value) >= 4, "unparseable authority status")
        code, relative = value[:2], value[3:]
        require(code == "??" and relative.startswith(allowed), f"dirty authority path: {relative}")
    return True


def _committed_bytes_equal(root: Path, expected_head: str, relative: str) -> bool:
    committed = subprocess.run(
        ["git", "-C", str(root), "show", f"{expected_head}:{relative}"],
        check=True,
        capture_output=True,
    ).stdout
    return committed == (root / relative).read_bytes()


def _apply_resource_envelope(envelope: Mapping[str, Any]) -> Any:
    for resource_id, megabytes in (
        (resource.RLIMIT_AS, int(envelope["max_memory_mb"])),
        (resource.RLIMIT_FSIZE, int(envelope["max_disk_mb"])),
    ):
        soft, hard = resource.getrlimit(resource_id)
        requested = megabytes * 1024 * 1024
        bounded = requested if hard == resource.RLIM_INFINITY else min(requested, hard)
        require(bounded > 0, "resource hard limit prohibits execution")
        resource.setrlimit(resource_id, (bounded, hard))

    def _timeout(_signum: int, _frame: Any) -> None:
        raise TimeoutError("frozen per-entry runtime ceiling exceeded")

    previous = signal.signal(signal.SIGALRM, _timeout)
    signal.alarm(int(envelope["max_runtime_seconds"]))
    return previous


def validate_activation(
    root: Path,
    graph_root: Path,
    identity: Mapping[str, Any],
    attempt: int,
    expected_head: str,
    actual_argv: Sequence[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    effective, successor, _ = load_effective_policy(root)
    artifacts = successor["artifact_contract"]
    matrix_path = root / artifacts["run_matrix_path"]
    binding_path = root / artifacts["binding_receipt_path"]
    freeze_path = root / artifacts["exec_freeze_path"]
    activation_path = root / artifacts["activation_record_path"]
    for path in (matrix_path, binding_path, freeze_path, activation_path):
        require(path.is_file() and not path.is_symlink(), f"missing or unsafe authority: {path.name}")
    matrix = load_json(matrix_path)
    binding = load_json(binding_path)
    freeze = load_json(freeze_path)
    activation = load_json(activation_path)
    entry = _find_entry(matrix, identity)
    require(re.fullmatch(r"[0-9a-f]{40}", expected_head) is not None, "expected HEAD must be a full lowercase commit hash")
    require(list(actual_argv) == normalized_run_argv(successor, entry, attempt, expected_head), "runtime command differs from normalized freeze")
    require(freeze["candidate_execution_authorized"] is False, "inactive freeze mutated into activation")
    require(activation["artifact_id"] == "P2-I2-C01-OWNER-ACCEPTED-EXECUTION-AUTHORIZATION", "wrong activation kind")
    require(activation["cycle_id"] == CYCLE_ID, "activation cycle drift")
    require(activation["owner_acceptance"] is True, "owner acceptance absent")
    require(activation["candidate_execution_authorized"] is True and activation["I08_authorized"] is True, "activation remains inactive")
    expected_hashes = {
        "inactive_exec_freeze_sha256": sha256(freeze_path),
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
        "validator_sha256": sha256(root / VALIDATOR_REL),
        "test_sha256": sha256(root / TEST_REL),
        "resumption_freeze_sha256": sha256(root / RESUMPTION_FREEZE_REL),
        "i07a_validation_sha256": sha256(root / I07_VALIDATION_REL),
        "i07a_input_freeze_sha256": sha256(root / I07A_INPUT_REL),
        "run_matrix_sha256": sha256(matrix_path),
        "binding_receipt_sha256": sha256(binding_path),
    }
    require(all(activation[key] == value for key, value in expected_hashes.items()), "activation byte binding drift")
    for pointer in binding["bound_files"]:
        _verify_pointer(root, pointer)
    require(
        activation["expected_head_source"] == "separately_owner_authorized_normalized_command_argument",
        "self-referential or missing HEAD source",
    )
    require(git(root, "rev-parse", "HEAD") == expected_head, "owner-authorized runtime HEAD drift")
    _authority_tree_clean(root)
    committed_authority = [
        artifacts["activation_record_path"],
        artifacts["exec_freeze_path"],
        artifacts["run_matrix_path"],
        artifacts["binding_receipt_path"],
        POLICY_REL.as_posix(),
        SOURCE_REL.as_posix(),
        VALIDATOR_REL.as_posix(),
        TEST_REL.as_posix(),
        RESUMPTION_FREEZE_REL.as_posix(),
        I07_VALIDATION_REL.as_posix(),
        I07A_INPUT_REL.as_posix(),
    ]
    require(
        all(_committed_bytes_equal(root, expected_head, relative) for relative in committed_authority),
        "committed/local authority byte drift",
    )
    freeze_runtime = load_json(root / RESUMPTION_FREEZE_REL)["runtime_identity"]
    require(git(graph_root, "rev-parse", "HEAD") == freeze_runtime["graph_revision"], "graph revision drift")
    require(_clean_repo(graph_root), "graph worktree dirty")
    runtime_source = graph_root / "src" / "pygrc" / "models" / "lgrc_9_v3_runtime.py"
    require(sha256(runtime_source) == freeze_runtime["runtime_source_sha256"], "graph runtime source drift")
    require(
        not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules),
        "ambient PyGRC import is prohibited",
    )
    require(Path(sys.prefix).resolve() == (root / ".venv").resolve(), "repository .venv inactive")
    runtime_identity = load_json(root / RESUMPTION_FREEZE_REL)["runtime_identity"]
    require(
        sha256(Path(sys.executable).resolve()) == runtime_identity["interpreter_executable_sha256"],
        "interpreter executable drift",
    )
    _assert_import_cache_clean(root, graph_root)
    require(attempt in {1, 2}, "attempt outside freeze")
    if attempt == 2:
        _validate_retry_predecessor(root, successor, entry, expected_head, freeze_path)
    return effective, entry, activation


def _governed_relative(relative: str | Path) -> Path:
    path = Path(relative)
    require(not path.is_absolute(), "governed artifact path must be relative")
    require(".." not in path.parts and "." not in path.parts, "governed artifact path traversal is prohibited")
    prefix = OUTPUT_ROOT_REL.parts
    require(path.parts[: len(prefix)] == prefix, "governed artifact is outside the C01 output root")
    require(path.suffix == ".json", "governed artifact must be JSON")
    return path


def _open_governed_parent(
    root: Path,
    relative: str | Path,
    *,
    create: bool,
) -> tuple[int, str] | None:
    """Open a governed parent beneath root without following any symlink."""

    path = _governed_relative(relative)
    directory_flags = os.O_RDONLY | os.O_DIRECTORY
    if hasattr(os, "O_CLOEXEC"):
        directory_flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        directory_flags |= os.O_NOFOLLOW
    descriptor = os.open(root.resolve(), directory_flags)
    try:
        for part in path.parent.parts:
            if create:
                try:
                    os.mkdir(part, 0o755, dir_fd=descriptor)
                except FileExistsError:
                    pass
            try:
                child = os.open(part, directory_flags, dir_fd=descriptor)
            except FileNotFoundError:
                if not create:
                    os.close(descriptor)
                    return None
                raise
            except OSError as error:
                raise ContractError(f"unsafe governed parent component: {part}") from error
            os.close(descriptor)
            descriptor = child
        return descriptor, path.name
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


def _governed_leaf_exists(root: Path, relative: str | Path) -> bool:
    opened = _open_governed_parent(root, relative, create=False)
    if opened is None:
        return False
    descriptor, leaf = opened
    try:
        try:
            os.stat(leaf, dir_fd=descriptor, follow_symlinks=False)
        except FileNotFoundError:
            return False
        return True
    finally:
        os.close(descriptor)


def _governed_leaf_absent(root: Path, relative: str | Path) -> bool:
    return not _governed_leaf_exists(root, relative)


def _read_governed_bytes(root: Path, relative: str | Path) -> bytes:
    opened = _open_governed_parent(root, relative, create=False)
    require(opened is not None, "governed artifact parent is absent")
    descriptor, leaf = opened
    file_flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        file_flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        file_flags |= os.O_NOFOLLOW
    try:
        try:
            file_descriptor = os.open(leaf, file_flags, dir_fd=descriptor)
        except (FileNotFoundError, OSError) as error:
            raise ContractError(f"missing or unsafe governed artifact: {leaf}") from error
        try:
            metadata = os.fstat(file_descriptor)
            require(stat.S_ISREG(metadata.st_mode), "governed artifact is not a regular file")
            with os.fdopen(file_descriptor, "rb", closefd=False) as handle:
                return handle.read()
        finally:
            os.close(file_descriptor)
    finally:
        os.close(descriptor)


def _read_governed_json(root: Path, relative: str | Path) -> dict[str, Any]:
    try:
        value = json.loads(_read_governed_bytes(root, relative))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ContractError("governed artifact is not valid JSON") from error
    require(isinstance(value, dict), "governed JSON object required")
    return value


def _governed_sha256(root: Path, relative: str | Path) -> str:
    return hashlib.sha256(_read_governed_bytes(root, relative)).hexdigest()


def _exclusive_json(root: Path, relative: str | Path, value: Mapping[str, Any]) -> None:
    opened = _open_governed_parent(root, relative, create=True)
    require(opened is not None, "governed parent creation failed")
    descriptor, leaf = opened
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        file_descriptor = os.open(leaf, flags, 0o644, dir_fd=descriptor)
        try:
            with os.fdopen(file_descriptor, "wb", closefd=False) as handle:
                handle.write(pretty_bytes(value))
                handle.flush()
                os.fsync(handle.fileno())
        finally:
            os.close(file_descriptor)
    finally:
        os.close(descriptor)


def _find_import_cache_artifacts(roots: Sequence[tuple[str, Path]]) -> list[str]:
    violations: list[str] = []
    for label, import_root in roots:
        require(import_root.is_dir() and not import_root.is_symlink(), f"unsafe import root: {label}")
        for current, directories, files in os.walk(import_root, followlinks=False):
            current_path = Path(current)
            relative = current_path.relative_to(import_root)
            for directory in directories:
                candidate = current_path / directory
                if candidate.is_symlink():
                    violations.append(f"{label}:{(relative / directory).as_posix()}:symlink")
                if directory == "__pycache__":
                    violations.append(f"{label}:{(relative / directory).as_posix()}:bytecode_cache")
            for name in files:
                if name.endswith((".pyc", ".pyo")):
                    violations.append(f"{label}:{(relative / name).as_posix()}:bytecode_file")
    return sorted(set(violations))


def _assert_import_cache_clean(root: Path, graph_root: Path) -> None:
    require(sys.dont_write_bytecode is True, "live execution requires .venv/bin/python -B")
    violations = _find_import_cache_artifacts(
        (
            ("experiment_scripts", root / EXPERIMENT_REL / "scripts"),
            ("pygrc_source", graph_root / "src"),
        )
    )
    require(not violations, "shared import cache present: " + ", ".join(violations[:8]))


def _retry_predecessor_paths(
    artifacts: Mapping[str, Any],
    entry: Mapping[str, Any],
) -> tuple[str, str, str]:
    return (
        _output_path(str(artifacts["claim_template"]), entry, 1),
        _output_path(str(artifacts["failure_receipt_template"]), entry, 1),
        str(entry["primary_output_path"]),
    )


def _validate_retry_predecessor(
    root: Path,
    successor: Mapping[str, Any],
    entry: Mapping[str, Any],
    expected_head: str,
    freeze_path: Path,
) -> dict[str, Any]:
    artifacts = successor["artifact_contract"]
    claim_relative, failure_relative, primary_output_relative = _retry_predecessor_paths(artifacts, entry)
    require(_governed_leaf_exists(root, claim_relative), "current-entry primary claim absent")
    require(_governed_leaf_exists(root, failure_relative), "current-entry primary failure receipt absent")
    require(_governed_leaf_absent(root, primary_output_relative), "current-entry primary output exists")
    claim = _read_governed_json(root, claim_relative)
    failure = _read_governed_json(root, failure_relative)
    claim_sha256 = _governed_sha256(root, claim_relative)
    primary_argv = normalized_run_argv(successor, entry, 1, expected_head)
    expected_command = [
        ".venv/bin/python",
        "-B",
        SOURCE_REL.as_posix(),
        *primary_argv,
    ]
    require(claim["artifact_id"] == "P2-I2-C01-PERMANENT-ATTEMPT-CLAIM", "wrong primary claim kind")
    require(claim["entry_id"] == entry["entry_id"] and claim["attempt"] == 1, "primary claim identity drift")
    require(claim["owner_authorized_full_HEAD"] == expected_head, "primary claim HEAD drift")
    require(claim["normalized_command"] == expected_command, "primary claim command drift")
    require(claim["inactive_exec_freeze_sha256"] == sha256(freeze_path), "primary claim freeze drift")
    require(failure["artifact_id"] == "P2-I2-C01-ATTEMPT-FAILURE-RECEIPT", "wrong primary failure kind")
    require(failure["entry_id"] == entry["entry_id"] and failure["attempt_index"] == 1, "primary failure identity drift")
    require(failure["claim_sha256"] == claim_sha256, "primary failure does not bind its claim")
    require(failure["inactive_exec_freeze_sha256"] == sha256(freeze_path), "primary failure freeze drift")
    byte_identity = failure["byte_identity_digests"]
    require(byte_identity["owner_authorized_full_HEAD"] == expected_head, "primary failure HEAD drift")
    require(byte_identity["normalized_argv"] == primary_argv, "primary failure command drift")
    require(byte_identity["policy_sha256"] == sha256(root / POLICY_REL), "primary failure policy drift")
    require(byte_identity["execution_source_sha256"] == sha256(root / SOURCE_REL), "primary failure source drift")
    counters = failure["zero_state_counters"]
    reconstructed = (
        counters["model_or_adapter_construction_started"] == 0
        and counters["models_constructed"] == 0
        and counters["adapters_constructed"] == 0
        and counters["candidate_or_control_operations_started"] == 0
        and counters["governed_output_written"] == 0
        and failure["output_absence"] is True
        and _governed_leaf_absent(root, primary_output_relative)
    )
    require(reconstructed and failure["retry_eligibility"] is True, "primary failure is not mechanically retry-eligible")
    return {
        "entry_id": entry["entry_id"],
        "primary_claim_path": claim_relative,
        "primary_claim_sha256": claim_sha256,
        "primary_failure_path": failure_relative,
        "primary_failure_sha256": _governed_sha256(root, failure_relative),
        "eligibility_reconstructed": True,
    }


def _roles(registration: Mapping[str, Any]) -> dict[str, int]:
    return {row["role"]: int(row["node_id"]) for row in registration["topology"]["nodes"]}


def _edges(registration: Mapping[str, Any]) -> dict[str, int]:
    return {row["edge_role"]: int(row["edge_id"]) for row in registration["topology"]["edges"]}


def _drain(model: Any, count: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for _ in range(count):
        require(bool(model.get_state().packet_ledger.event_queue_records), "queue drained before frozen event count")
        result = model.step()
        records.append({"events": [event.kind for event in result.events], "bookkeeping": dict(result.bookkeeping)})
    require(not model.get_state().packet_ledger.event_queue_records, "queue not empty after frozen drain")
    return records


def _adapter_for_branch(registration: Mapping[str, Any], mode: str, branch_id: str, role_ids: Mapping[str, int], edge_ids: Mapping[str, int], common_adapter: Any) -> Any:
    if mode == "state_carried":
        return None
    if branch_id == "private_partition_one":
        profile_id = "history_private_one" if mode == "history_carried" else "hybrid_private_one"
    elif branch_id == "private_partition_two":
        profile_id = "history_private_two" if mode == "history_carried" else "hybrid_private_two"
    else:
        return common_adapter
    from p2_i2_i06_history_adapter import RCAEActiveHistoryAdapterV2
    profile = registration["history_adapter_profiles"][profile_id]
    return RCAEActiveHistoryAdapterV2(
        carrier_id=profile["carrier_id"],
        pool_target_node_id=role_ids[profile["pool_target_role"]],
        registered_source_node_ids=[role_ids[item] for item in profile["registered_source_roles"]],
        readout_node_id=role_ids[profile["readout_role"]],
        positive_reservoir_node_id=role_ids[profile["positive_reservoir_role"]],
        negative_sink_node_id=role_ids[profile["negative_sink_role"]],
        positive_edge_id=edge_ids[profile["positive_edge_role"]],
        negative_edge_id=edge_ids[profile["negative_edge_role"]],
        recency_coefficient=float(profile["recency_coefficient"]),
        materialization_tolerance=float(profile["materialization_tolerance"]),
    )


def _front_roles(successor: Mapping[str, Any], registration: Mapping[str, Any], mode: str, response_path: str) -> list[str]:
    resolution = successor["response_path_resolution"][response_path]
    if "front_masks_by_mode" in resolution:
        return list(resolution["front_masks_by_mode"][mode])
    value = resolution.get("front_mask")
    if isinstance(value, list):
        return list(value)
    return list(registration["mode_registry"][mode]["response_front_mask"])


def _producer_roles(response_path: str) -> tuple[str, str, str]:
    if response_path == "registered_common_alternate":
        return "A_ALTERNATE", "B", "A_ALTERNATE_TO_B"
    return "A_PRIMARY", "B", "A_PRIMARY_TO_B"


def _lineage(branch_id: str, q_id: str, side: str) -> str:
    label = {"q1": "q2", "q2": "q1"}.get(q_id, q_id) if "label_permutation" in branch_id else q_id
    return f"lineage:p2-i2:{branch_id}:{label}:{side}"


def _registered_common_baseline_digest(root: Path, mode: str) -> str:
    validation = load_json(root / I06_VALIDATION_REL)
    rows = [row for row in validation["checks"] if row["check_id"] == "I06-10"]
    require(len(rows) == 1 and rows[0]["status"] == "passed", "accepted I06 baseline receipt absent")
    return str(rows[0]["evidence"][mode]["composite_digest"])


def execute_entry(
    root: Path,
    graph_root: Path,
    effective: Mapping[str, Any],
    entry: Mapping[str, Any],
    runtime_state: dict[str, int],
) -> dict[str, Any]:
    scripts = root / EXPERIMENT_REL / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    graph_source = graph_root / "src"
    if str(graph_source) not in sys.path:
        sys.path.insert(0, str(graph_source))
    from p2_i2_i06_registration import _build_model, _composite_identity
    import pygrc
    from pygrc.models import (
        LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY,
        LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED,
    )
    require(
        Path(pygrc.__file__).resolve().is_relative_to(graph_source.resolve()),
        "PyGRC import did not originate in the frozen external checkout",
    )
    runtime_state["pygrc_imports"] = 1

    registration = load_json(root / REGISTRATION_REL)
    overlay = load_json(root / OVERLAY_REL)
    successor = effective["successor"]
    mode = str(entry["mode"])
    branch_id = str(entry["branch_id"])
    plan_rows = [row for row in effective["branch_plans"] if row["branch_id"] == branch_id and row["cell_id"] == entry["cell_id"]]
    require(len(plan_rows) == 1 and mode in plan_rows[0]["modes"], "branch plan mismatch")
    plan = plan_rows[0]
    random.seed(int(entry["seed"]))
    runtime_state["model_or_adapter_construction_started"] = 1
    model, role_ids, edge_ids, common_adapter = _build_model(registration, mode)
    runtime_state["models_constructed"] = 1
    runtime_state["adapters_constructed"] = int(common_adapter is not None)
    adapter = _adapter_for_branch(registration, mode, branch_id, role_ids, edge_ids, common_adapter)
    if adapter is not None and adapter is not common_adapter:
        runtime_state["adapters_constructed"] += 1
    initial_identity = _composite_identity(registration, mode, model, adapter, role_ids, edge_ids)
    if mode == "state_carried" or branch_id not in {"private_partition_one", "private_partition_two"}:
        require(
            initial_identity["digest"] == _registered_common_baseline_digest(root, mode),
            "fresh registered composite baseline drift",
        )
    runtime_state["candidate_or_control_operations_started"] = 1
    schedule_slots = {row["slot_index"]: row for row in overlay["matched_event_schedule"]["slots"]}
    order = successor["order_resolution"][entry["physical_order_id"]]
    q_slot = {q_id: index for index, q_id in enumerate(order)}
    contribution_specs = [deepcopy(successor["contribution_operations"][name]) for name in plan["contributions"]]
    contribution_specs.sort(key=lambda row: q_slot[row["slot_kind"]])
    contribution_receipts: list[dict[str, Any]] = []
    used_slots: set[int] = set()
    for spec in contribution_specs:
        slot_index = q_slot[spec["slot_kind"]]
        slot = schedule_slots[slot_index]
        used_slots.add(slot_index)
        model.schedule_packet_departure(
            source_node_id=role_ids[spec["source_role"]],
            target_node_id=role_ids[spec["target_role"]],
            edge_id=edge_ids[spec["edge_role"]],
            amount=float(spec["amount"]),
            departure_event_time_key=float(slot["departure_event_time_key"]),
            arrival_event_time_key=float(slot["arrival_event_time_key"]),
            scheduler_event_index=int(slot["departure_scheduler_event_index"]),
            packet_index=int(slot["packet_index_if_used"]),
            source_lineage_id=_lineage(branch_id, spec["q_id"], "source"),
            target_lineage_id=_lineage(branch_id, spec["q_id"], "target"),
        )
        steps = _drain(model, 2)
        contribution_receipts.append({**spec, "slot_index": slot_index, "slot": deepcopy(slot), "arrival_committed": True, "steps": steps})
    contribution_slot_receipts = [
        {"slot_index": index, "disposition": "used" if index in used_slots else "explicit_no_op", "packet_scheduled": index in used_slots}
        for index in (0, 1)
    ]

    appended_tokens: list[dict[str, Any]] = []
    history_intervention = None
    if adapter is not None:
        appended_tokens = list(adapter.ingest_new_rows(model))
        if plan["carrier_action"] in {"history_to_reference", "state_and_history_to_derived_reference"}:
            history_intervention = adapter.replace_history(
                (),
                intervention_id=f"{CYCLE_ID}:{entry['entry_id']}:history-reference",
                reason="registered active-history reference intervention",
            )
        materialization = adapter.materialize_readout(
            model,
            departure_event_time_key=float(schedule_slots[2]["departure_event_time_key"]),
            arrival_event_time_key=float(schedule_slots[2]["arrival_event_time_key"]),
            scheduler_event_index=int(schedule_slots[2]["departure_scheduler_event_index"]),
            packet_index=int(schedule_slots[2]["packet_index_if_used"]),
        )
        slot_2 = {"slot_index": 2, "disposition": "materialization", "packet_scheduled": bool(materialization["packet_scheduled"]), "record": materialization}
    else:
        slot_2 = {"slot_index": 2, "disposition": "explicit_no_op", "packet_scheduled": False, "record": None}

    debit_rows = [row for row in overlay["native_P_intervention"]["branch_amounts"] if row["mode"] == mode and row["subconfiguration_id"] == branch_id]
    if debit_rows:
        require(len(debit_rows) == 1, "ambiguous P debit")
        call = overlay["native_P_intervention"]["call"]
        debit = debit_rows[0]
        model.schedule_packet_departure(
            source_node_id=role_ids["P"],
            target_node_id=role_ids["K_P"],
            edge_id=edge_ids["P_TO_K_P"],
            amount=float(debit["amount"]),
            departure_event_time_key=float(call["departure_event_time_key"]),
            arrival_event_time_key=float(call["arrival_event_time_key"]),
            scheduler_event_index=int(call["scheduler_event_index"]),
            packet_index=int(call["packet_index"]),
            source_lineage_id=str(call["source_lineage_id"]),
            target_lineage_id=str(call["target_lineage_id"]),
        )
        debit_steps = _drain(model, 2)
        slot_3 = {"slot_index": 3, "disposition": "native_P_intervention", "packet_scheduled": True, "amount": debit["amount"], "amount_identity": debit["amount_identity"], "steps": debit_steps}
    else:
        slot_3 = {"slot_index": 3, "disposition": "explicit_no_op", "packet_scheduled": False}

    neutral = registration["contribution_and_schedule"]["neutral_contact"]
    neutral_slot = schedule_slots[4]
    model.schedule_packet_departure(
        source_node_id=role_ids[neutral["source_role"]],
        target_node_id=role_ids[neutral["target_role"]],
        edge_id=edge_ids[neutral["edge_role"]],
        amount=float(neutral["amount"]),
        departure_event_time_key=float(neutral_slot["departure_event_time_key"]),
        arrival_event_time_key=float(neutral_slot["arrival_event_time_key"]),
        scheduler_event_index=int(neutral_slot["departure_scheduler_event_index"]),
        packet_index=int(neutral_slot["packet_index_if_used"]),
        source_lineage_id="lineage:p2-i2:neutral-source",
        target_lineage_id="lineage:p2-i2:neutral-target",
    )
    neutral_steps = _drain(model, 2)
    state_before_response = model.get_state()
    require(not state_before_response.packet_ledger.event_queue_records, "pre-window queue not empty")
    require(bool(state_before_response.causal_pulse_substrate_surface_log), "neutral contact produced no native surface row")
    neutral_surface_digest = str(state_before_response.causal_pulse_substrate_surface_log[-1].surface_digest)
    B_before = float(state_before_response.base_state.nodes[role_ids["B"]].coherence)
    response_path = str(plan["response_path"])
    mode_config = registration["mode_registry"][mode]
    call_trace: list[dict[str, Any]] = []
    feedback_receipt: dict[str, Any] | None = None
    production_receipt: dict[str, Any] | None = None
    controller_receipt: dict[str, Any] | None = None

    if response_path == "diagnostic_controller_authored_schedule":
        controller = overlay["controller_assembled_bypass"]
        q_receipts = {row["q_id"]: row for row in contribution_receipts}
        predicate = all(q_id in q_receipts and q_receipts[q_id]["arrival_committed"] for q_id in ("q1", "q2"))
        controller_receipt = {
            "predicate_inputs": {q_id: {"amount": q_receipts[q_id]["amount"], "target_role": q_receipts[q_id]["target_role"], "arrival_committed": q_receipts[q_id]["arrival_committed"]} for q_id in ("q1", "q2")},
            "predicate_result": predicate,
            "common_carrier_reads": [],
            "active_history_reads": [],
            "native_feedback_surface_reads": [],
            "latest_pre_response_neutral_surface_digest": neutral_surface_digest,
            "candidate_chain": False,
        }
        require(predicate, "registered controller branch lacks complete q receipts")
        call = controller["direct_native_packet_call_if_true"]
        packet_count = len(model.get_state().packet_ledger.packet_records)
        model.schedule_packet_departure(
            source_node_id=role_ids["A_PRIMARY"],
            target_node_id=role_ids["B"],
            edge_id=edge_ids["A_PRIMARY_TO_B"],
            amount=float(call["amount"]),
            departure_event_time_key=float(call["departure_event_time_key"]),
            arrival_event_time_key=float(call["arrival_event_time_key"]),
            scheduler_event_index=int(call["scheduler_event_index"]),
            packet_index=packet_count,
            source_lineage_id=None,
            target_lineage_id=None,
        )
        call_trace.append({"method": "LGRC9V3.schedule_packet_departure", "authority": "accepted_I06B.controller_assembled_bypass", "candidate_chain": False})
        response_steps = _drain(model, 2)
        response_scheduled = True
        producer_reason = "controller_receipt_predicate_direct_native_schedule"
    else:
        if response_path == "diagnostic_direct_contributor_mask":
            direct = overlay["direct_address_bypass"]
            front_roles = ["S1", "S2"]
            candidate_chain = False
            authority = "accepted_I06B.direct_address_bypass"
        else:
            front_roles = _front_roles(successor, registration, mode, response_path)
            candidate_chain = bool(successor["response_path_resolution"][response_path]["candidate_chain"])
            authority = "accepted_I06_mode_response"
        row = model.emit_feedback_eligibility_surface_row(
            front_node_ids=tuple(role_ids[role] for role in front_roles),
            rear_node_ids=(role_ids["B_REF"],),
            reference_delta=float(registration["response_registration"]["reference_delta"]),
            feedback_threshold=float(mode_config["feedback_threshold"]),
            expected_next_route_id=None,
            expected_next_channel_id=None,
        )
        feedback_receipt = {
            "surface_digest": row.surface_digest,
            "source_surface_digest": row.surface_values_after["source_surface_digest"],
            "front_roles": front_roles,
            "rear_roles": ["B_REF"],
            "front_mass": float(row.surface_values_after["front_mass"]),
            "rear_mass": float(row.surface_values_after["rear_mass"]),
            "boundary_polarity_score": float(row.surface_values_after["boundary_polarity_score"]),
            "threshold": float(mode_config["feedback_threshold"]),
            "reference_delta": float(registration["response_registration"]["reference_delta"]),
            "candidate_chain": candidate_chain,
            "latest_pre_feedback_neutral_surface_digest": neutral_surface_digest,
        }
        call_trace.append({"method": "LGRC9V3.emit_feedback_eligibility_surface_row", "authority": authority, "front_roles": front_roles, "candidate_chain": candidate_chain})
        source_role, target_role, edge_role = _producer_roles(response_path)
        response_schedule = overlay["matched_event_schedule"]["response"]
        model.set_feedback_coupled_pulse_producer(
            source_node_id=role_ids[source_role],
            target_node_id=role_ids[target_role],
            edge_id=edge_ids[edge_role],
            threshold=float(mode_config["feedback_threshold"]),
            packet_amount=float(registration["response_registration"]["response_packet_amount"]),
            expected_polarity=str(mode_config["expected_polarity"]),
            expected_source_surface_digest=None,
            expected_next_route_id=None,
            expected_next_channel_id=None,
            arrival_event_time_key=float(response_schedule["arrival_event_time_key"]),
            enabled=True,
        )
        call_trace.append({"method": "LGRC9V3.set_feedback_coupled_pulse_producer", "authority": authority, "source_role": source_role, "target_role": target_role, "edge_role": edge_role})
        result = model.produce_events(policy=LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY)
        require(len(result.production_records) == 1, "expected exactly one native producer record")
        record = result.production_records[0]
        response_scheduled = record.reason_code == LGRC9V3_AUTONOMOUS_PRODUCER_REASON_FEEDBACK_SCHEDULED
        production_receipt = {
            "reason_code": record.reason_code,
            "scheduled": response_scheduled,
            "observed_evidence": dict(record.observed_evidence),
            "producer_mutated_coherence": bool(record.observed_evidence.get("producer_mutated_coherence", False)),
            "direct_claim_write": bool(record.observed_evidence.get("direct_claim_write", False)),
        }
        call_trace.append({"method": "LGRC9V3.produce_events", "authority": "native_model_owned_producer", "reason_code": record.reason_code})
        response_steps = []
        for _ in range(2):
            step = model.step()
            response_steps.append({"events": [event.kind for event in step.events], "bookkeeping": dict(step.bookkeeping)})
        require(not model.get_state().packet_ledger.event_queue_records, "response queue not empty")
        producer_reason = str(record.reason_code)

    state_after = model.get_state()
    B_after = float(state_after.base_state.nodes[role_ids["B"]].coherence)
    gain = B_after - B_before
    tolerance = float(registration["response_registration"]["response_gain_tolerance"])
    expected_gain = float(registration["response_registration"]["response_packet_amount"]) if response_scheduled else 0.0
    gain_matches = math.isclose(gain, expected_gain, rel_tol=0.0, abs_tol=tolerance)
    queues_empty = not state_after.packet_ledger.event_queue_records and not state_after.boundary_birth_trial_queue
    window_valid = queues_empty and gain_matches
    raw_response = None if not window_valid else gain
    post_identity = _composite_identity(registration, mode, model, adapter, role_ids, edge_ids)
    coherences = {role: float(state_after.base_state.nodes[node_id].coherence) for role, node_id in sorted(role_ids.items())}
    packet_records = [row.to_record() for row in state_after.packet_ledger.packet_records]
    surface_rows = [row.to_artifact() for row in state_after.causal_pulse_substrate_surface_log]
    bounds = registration["pool_economy_and_capacity"]["bounds"]
    processed_packet_events = 2 * len(packet_records)
    b_packets = [row for row in packet_records if row["target_node_id"] == role_ids["B"]]
    require(len(b_packets) == int(response_scheduled), "unexpected B-targeting packet count")
    if response_scheduled:
        response_packet = b_packets[0]
        expected_source_role, _, expected_edge_role = _producer_roles(response_path)
        if response_path == "diagnostic_controller_authored_schedule":
            expected_source_role, expected_edge_role = "A_PRIMARY", "A_PRIMARY_TO_B"
        response_schedule = overlay["matched_event_schedule"]["response"]
        require(response_packet["source_node_id"] == role_ids[expected_source_role], "wrong response source")
        require(response_packet["edge_id"] == edge_ids[expected_edge_role], "wrong response edge")
        require(
            math.isclose(
                float(response_packet["amount"]),
                float(registration["response_registration"]["response_packet_amount"]),
                rel_tol=0.0,
                abs_tol=0.0,
            ),
            "wrong response amount",
        )
        require(
            float(response_packet["arrival_event_time_key"])
            == float(response_schedule["arrival_event_time_key"]),
            "wrong response arrival time",
        )
    require(len(packet_records) <= int(bounds["max_scheduled_packets_per_branch"]), "scheduled packet capacity exceeded")
    require(processed_packet_events <= int(bounds["max_processed_packet_events_per_branch"]), "processed packet-event capacity exceeded")
    require(len(surface_rows) <= int(bounds["max_surface_rows_per_branch"]), "surface-row capacity exceeded")
    require(len(state_after.packet_ledger.event_queue_records) <= int(bounds["max_pending_queue_records"]), "pending queue capacity exceeded")
    require(
        float(bounds["P_closed_interval"][0]) <= coherences["P"] <= float(bounds["P_closed_interval"][1]),
        "registered P interval exceeded",
    )
    response_source_role = "A_PRIMARY" if response_path != "registered_common_alternate" else "A_ALTERNATE"
    require(
        coherences[response_source_role] >= float(bounds["minimum_response_source_after_window"]),
        "response-source reserve exceeded",
    )
    capacity_receipt = {
        "resource_envelope": deepcopy(effective["resource_envelope_per_entry"]),
        "scheduled_packet_count": len(packet_records),
        "processed_packet_event_count": processed_packet_events,
        "surface_row_count": len(surface_rows),
        "pending_queue_record_count": len(state_after.packet_ledger.event_queue_records),
        "registered_bounds": deepcopy(bounds),
        "P_after": coherences["P"],
        "response_source_role": response_source_role,
        "response_source_after": coherences[response_source_role],
        "all_capacity_guards_passed": True,
    }
    return {
        "artifact_id": "P2-I2-C01-RUN-RECORD",
        "artifact_version": "1.1.0",
        "cycle_id": CYCLE_ID,
        "entry_identity": {key: entry[key] for key in ("entry_id", "mode", "cell_id", "branch_id", "physical_order_id", "seed", "attempt")},
        "runtime_binding_receipt": {
            "graph_revision": git(graph_root, "rev-parse", "HEAD"),
            "python_command": ".venv/bin/python",
            "python_flags": ["-B"],
            "dont_write_bytecode": sys.dont_write_bytecode,
            "owner_authorized_full_HEAD": entry["owner_authorized_full_HEAD"],
            "normalized_argv": entry["normalized_argv"],
            "interpreter_executable_sha256": sha256(Path(sys.executable).resolve()),
            "execution_source_sha256": sha256(root / SOURCE_REL),
            "policy_sha256": sha256(root / POLICY_REL),
        },
        "initial_composite_identity": initial_identity,
        "branch_configuration": deepcopy(plan),
        "source_debit_activity_receipt": {"contributions": contribution_receipts, "slot_dispositions": contribution_slot_receipts},
        "timing_queue_receipt": {"slot_2": slot_2, "slot_3": slot_3, "neutral_slot": deepcopy(neutral_slot), "neutral_steps": neutral_steps, "latest_pre_response_neutral_surface_digest": neutral_surface_digest, "response_steps": response_steps, "queues_empty_after": queues_empty},
        "history_receipt": {"appended_tokens": appended_tokens, "intervention": history_intervention, "final_tokens": [] if adapter is None else list(adapter.tokens)},
        "support_capacity_route_receipt": capacity_receipt,
        "inert_sink_no_influence_receipt": {"sink_roles": ["K_DIV_Q1", "K_DIV_Q2", "K_P", "K_H", "K_H1", "K_H2"], "outgoing_registered_edges": []},
        "window_validity_receipt": {"protocol_id": registration["response_registration"]["window_protocol"]["protocol_id"], "B_before": B_before, "B_after": B_after, "gain": gain, "expected_gain": expected_gain, "runtime_tolerance": tolerance, "gain_matches": gain_matches, "queues_empty": queues_empty, "valid": window_valid, "scientific_zero": window_valid and not response_scheduled},
        "arrival_gain_receipt": {"native_packet_gain": expected_gain, "measured_B_gain": gain, "within_runtime_tolerance": gain_matches},
        "causal_chain_call_trace": call_trace,
        "feedback_receipt": feedback_receipt,
        "native_production_receipt": production_receipt,
        "controller_receipt": controller_receipt,
        "raw_response_record": {
            "response_id": registration["response_registration"]["response_id"],
            "value": raw_response,
            "operational_null": not window_valid,
            "producer_reason": producer_reason,
            "candidate_chain_status": (
                "receipt_derived"
                if plan["candidate_chain"] == "eligible"
                else (
                    "excluded_diagnostic"
                    if plan["candidate_chain"] == "excluded"
                    else "excluded_private_partition"
                )
            ),
        },
        "post_run_composite_identity": post_identity,
        "final_coherences": coherences,
        "packet_records": packet_records,
        "surface_rows": surface_rows,
        "R01_through_R05": "unassigned_until_I09_I11",
        "scientific_interpretation": None,
    }


def _terminal_output_summary(
    root: Path,
    relative: str,
    entry: Mapping[str, Any],
    attempt: int,
    expected_head: str,
) -> dict[str, Any]:
    record = _read_governed_json(root, relative)
    identity = record.get("entry_identity")
    require(isinstance(identity, dict), "terminal output entry identity absent")
    for key in ("entry_id", "mode", "cell_id", "branch_id", "physical_order_id", "seed"):
        require(identity.get(key) == entry[key], f"terminal output identity drift: {key}")
    require(identity.get("attempt") == attempt, "terminal output attempt drift")
    binding = record.get("runtime_binding_receipt")
    require(isinstance(binding, dict), "terminal output runtime binding absent")
    require(binding.get("owner_authorized_full_HEAD") == expected_head, "terminal output HEAD drift")
    raw = record.get("raw_response_record")
    window = record.get("window_validity_receipt")
    require(isinstance(raw, dict) and isinstance(window, dict), "terminal evaluability receipts absent")
    value = raw.get("value")
    require(raw.get("operational_null") is False, "terminal output is operationally null")
    require(window.get("valid") is True, "terminal response window is invalid")
    require(isinstance(value, (int, float)) and not isinstance(value, bool), "terminal response is not numeric")
    require(math.isfinite(float(value)), "terminal response is non-finite")
    return {
        "entry_id": entry["entry_id"],
        "attempt": attempt,
        "output_path": relative,
        "output_sha256": _governed_sha256(root, relative),
        "raw_response_value": float(value),
        "operational_null": False,
        "evaluable": True,
    }


def _execution_manifest_document(
    root: Path,
    matrix: Mapping[str, Any],
    successor: Mapping[str, Any],
    expected_head: str,
) -> dict[str, Any]:
    required_count = int(matrix["primary_entry_count"])
    require(required_count > 0 and len(matrix["entries"]) == required_count, "completion matrix count drift")
    artifacts = successor["artifact_contract"]
    terminals: list[dict[str, Any]] = []
    for entry in matrix["entries"]:
        primary_output = str(entry["primary_output_path"])
        retry_output = str(entry["retry_output_path"])
        primary_claim = str(entry["primary_claim_path"])
        retry_claim = str(entry["retry_claim_path"])
        primary_failure = _output_path(str(artifacts["failure_receipt_template"]), entry, 1)
        retry_failure = _output_path(str(artifacts["failure_receipt_template"]), entry, 2)
        primary_present = _governed_leaf_exists(root, primary_output)
        retry_present = _governed_leaf_exists(root, retry_output)
        require(primary_present != retry_present, f"missing or ambiguous terminal output: {entry['entry_id']}")
        if primary_present:
            require(_governed_leaf_exists(root, primary_claim), "primary terminal claim absent")
            require(_governed_leaf_absent(root, primary_failure), "primary output and failure both exist")
            require(_governed_leaf_absent(root, retry_claim), "retry claim exists after primary success")
            require(_governed_leaf_absent(root, retry_failure), "retry failure exists after primary success")
            terminals.append(_terminal_output_summary(root, primary_output, entry, 1, expected_head))
            continue
        require(_governed_leaf_exists(root, retry_claim), "retry terminal claim absent")
        require(_governed_leaf_absent(root, retry_failure), "retry output and failure both exist")
        predecessor = _validate_retry_predecessor(root, successor, entry, expected_head, root / artifacts["exec_freeze_path"])
        terminal = _terminal_output_summary(root, retry_output, entry, 2, expected_head)
        terminal["retry_predecessor"] = predecessor
        terminals.append(terminal)
    require(len(terminals) == required_count and all(row["evaluable"] for row in terminals), "matrix completion is not fully evaluable")
    document: dict[str, Any] = {
        "artifact_id": "P2-I2-C01-EXECUTION-MANIFEST",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08",
        "cycle_id": CYCLE_ID,
        "status": "complete_all_registered_entries_evaluable",
        "owner_authorized_full_HEAD": expected_head,
        "run_matrix_sha256": sha256(root / artifacts["run_matrix_path"]),
        "run_matrix_semantic_digest": matrix["semantic_digest"],
        "required_entry_count": required_count,
        "evaluable_terminal_count": len(terminals),
        "missing_entry_count": 0,
        "nonevaluable_entry_count": 0,
        "ambiguous_entry_count": 0,
        "terminals": terminals,
        "completion_rule": "exact_matrix_paths_only_all_234_exactly_one_terminal_and_all_evaluable",
        "scientific_interpretation": None,
    }
    document["canonical_payload_digest"] = digest(
        {key: value for key, value in document.items() if key != "canonical_payload_digest"}
    )
    return document


def build_execution_manifest(root: Path, expected_head: str) -> dict[str, Any]:
    require(sys.dont_write_bytecode is True, "manifest construction requires .venv/bin/python -B")
    require(re.fullmatch(r"[0-9a-f]{40}", expected_head) is not None, "expected HEAD must be a full lowercase commit hash")
    effective, successor, _ = load_effective_policy(root)
    artifacts = successor["artifact_contract"]
    matrix_path = root / artifacts["run_matrix_path"]
    binding_path = root / artifacts["binding_receipt_path"]
    freeze_path = root / artifacts["exec_freeze_path"]
    activation_path = root / artifacts["activation_record_path"]
    manifest_path = root / artifacts["execution_manifest_path"]
    for path in (matrix_path, binding_path, freeze_path, activation_path):
        require(path.is_file() and not path.is_symlink(), f"missing or unsafe authority: {path.name}")
    require(not manifest_path.exists() and not manifest_path.is_symlink(), "execution manifest already exists")
    matrix = load_json(matrix_path)
    require(matrix["primary_entry_count"] == 234 and len(matrix["entries"]) == 234, "live completion requires all 234 frozen rows")
    binding = load_json(binding_path)
    activation = load_json(activation_path)
    require(activation["artifact_id"] == "P2-I2-C01-OWNER-ACCEPTED-EXECUTION-AUTHORIZATION", "wrong activation kind")
    require(activation["owner_acceptance"] is True and activation["I08_authorized"] is True, "I08 activation absent")
    require(git(root, "rev-parse", "HEAD") == expected_head, "owner-authorized completion HEAD drift")
    _authority_tree_clean(root)
    expected_hashes = {
        "inactive_exec_freeze_sha256": sha256(freeze_path),
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
        "validator_sha256": sha256(root / VALIDATOR_REL),
        "test_sha256": sha256(root / TEST_REL),
        "resumption_freeze_sha256": sha256(root / RESUMPTION_FREEZE_REL),
        "i07a_validation_sha256": sha256(root / I07_VALIDATION_REL),
        "i07a_input_freeze_sha256": sha256(root / I07A_INPUT_REL),
        "run_matrix_sha256": sha256(matrix_path),
        "binding_receipt_sha256": sha256(binding_path),
    }
    require(all(activation[key] == value for key, value in expected_hashes.items()), "completion activation byte binding drift")
    for pointer in binding["bound_files"]:
        _verify_pointer(root, pointer)
    committed_authority = [
        artifacts["activation_record_path"],
        artifacts["exec_freeze_path"],
        artifacts["run_matrix_path"],
        artifacts["binding_receipt_path"],
        POLICY_REL.as_posix(),
        SOURCE_REL.as_posix(),
        VALIDATOR_REL.as_posix(),
        TEST_REL.as_posix(),
        RESUMPTION_FREEZE_REL.as_posix(),
        I07_VALIDATION_REL.as_posix(),
        I07A_INPUT_REL.as_posix(),
    ]
    require(
        all(_committed_bytes_equal(root, expected_head, relative) for relative in committed_authority),
        "committed/local completion authority byte drift",
    )
    document = _execution_manifest_document(root, matrix, successor, expected_head)
    write_new(manifest_path, document)
    return document


def _claim_document(
    root: Path,
    entry: Mapping[str, Any],
    attempt: int,
    expected_head: str,
    actual_argv: Sequence[str],
    freeze_path: Path,
) -> dict[str, Any]:
    return {
        "artifact_id": "P2-I2-C01-PERMANENT-ATTEMPT-CLAIM",
        "artifact_version": "1.1.0",
        "cycle_id": CYCLE_ID,
        "entry_id": entry["entry_id"],
        "attempt": attempt,
        "owner_authorized_full_HEAD": expected_head,
        "normalized_command": [".venv/bin/python", "-B", SOURCE_REL.as_posix(), *actual_argv],
        "import_cache_policy": "-B_active_and_project_PyGRC_import_roots_cache_free_before_and_after",
        "interpreter_executable_sha256": sha256(Path(sys.executable).resolve()),
        "inactive_exec_freeze_sha256": sha256(freeze_path),
        "policy_sha256": sha256(root / POLICY_REL),
        "execution_source_sha256": sha256(root / SOURCE_REL),
        "claim_semantics": "permanent_and_never_deleted_to_permit_repeat",
    }


def run_entry(
    root: Path,
    graph_root: Path,
    identity: Mapping[str, Any],
    attempt: int,
    output_path: Path,
    expected_head: str,
    actual_argv: Sequence[str],
) -> dict[str, Any]:
    global _LIVE_ENTRY_STARTS
    require(_LIVE_ENTRY_STARTS == 0, "cross-entry worker reuse is prohibited")
    _LIVE_ENTRY_STARTS = 1
    effective, entry, _ = validate_activation(
        root, graph_root, identity, attempt, expected_head, actual_argv
    )
    successor = effective["successor"]
    artifacts = successor["artifact_contract"]
    expected_output = entry["primary_output_path"] if attempt == 1 else entry["retry_output_path"]
    require(output_path == root / expected_output, "output path differs from exact freeze")
    claim_template = artifacts["claim_template"]
    claim_relative = _output_path(claim_template, entry, attempt)
    failure_relative = _output_path(artifacts["failure_receipt_template"], entry, attempt)
    require(_governed_leaf_absent(root, expected_output), "governed output already exists or is unsafe")
    require(_governed_leaf_absent(root, claim_relative), "attempt already claimed or claim path is unsafe")
    require(_governed_leaf_absent(root, failure_relative), "attempt failure receipt already exists or is unsafe")
    freeze_path = root / artifacts["exec_freeze_path"]
    _exclusive_json(
        root,
        claim_relative,
        _claim_document(root, entry, attempt, expected_head, actual_argv, freeze_path),
    )
    phase = "claimed_before_runtime_import"
    runtime_state = {
        "pygrc_imports": 0,
        "model_or_adapter_construction_started": 0,
        "models_constructed": 0,
        "adapters_constructed": 0,
        "candidate_or_control_operations_started": 0,
    }
    previous_alarm_handler = None
    try:
        phase = "runtime_resource_envelope"
        previous_alarm_handler = _apply_resource_envelope(effective["resource_envelope_per_entry"])
        phase = "runtime_import_and_model_construction"
        result = execute_entry(
            root,
            graph_root,
            effective,
            {
                **entry,
                "attempt": attempt,
                "owner_authorized_full_HEAD": expected_head,
                "normalized_argv": list(actual_argv),
            },
            runtime_state,
        )
        phase = "post_execution_graph_guard"
        _assert_import_cache_clean(root, graph_root)
        require(_clean_repo(graph_root), "graph worktree changed during attempt")
        phase = "write_governed_output"
        _exclusive_json(root, expected_output, result)
        return result
    except BaseException as error:
        failure = {
            "artifact_id": "P2-I2-C01-ATTEMPT-FAILURE-RECEIPT",
            "artifact_version": "1.1.0",
            "cycle_id": CYCLE_ID,
            "entry_id": entry["entry_id"],
            "attempt": attempt,
            "entry_identity": {
                key: entry[key]
                for key in (
                    "cycle_id",
                    "mode",
                    "cell_id",
                    "branch_id",
                    "physical_order_id",
                    "seed",
                )
            },
            "attempt_index": attempt,
            "failure_phase": phase,
            "exception_class": type(error).__name__,
            "exception_message": str(error),
            "byte_identity_digests": {
                "owner_authorized_full_HEAD": expected_head,
                "inactive_exec_freeze_sha256": sha256(freeze_path),
                "policy_sha256": sha256(root / POLICY_REL),
                "execution_source_sha256": sha256(root / SOURCE_REL),
                "validator_sha256": sha256(root / VALIDATOR_REL),
                "test_sha256": sha256(root / TEST_REL),
                "interpreter_executable_sha256": sha256(Path(sys.executable).resolve()),
                "normalized_argv": list(actual_argv),
            },
            "zero_state_counters": {
                **runtime_state,
                "governed_output_written": 0,
            },
            "output_absence": _governed_leaf_absent(root, expected_output),
            "retry_eligibility": (
                runtime_state["model_or_adapter_construction_started"] == 0
                and runtime_state["models_constructed"] == 0
                and runtime_state["adapters_constructed"] == 0
                and runtime_state["candidate_or_control_operations_started"] == 0
                and _governed_leaf_absent(root, expected_output)
            ),
            "claim_retained": _governed_leaf_exists(root, claim_relative),
            "claim_sha256": _governed_sha256(root, claim_relative),
            "inactive_exec_freeze_sha256": sha256(freeze_path),
        }
        _exclusive_json(root, failure_relative, failure)
        raise
    finally:
        signal.alarm(0)
        if previous_alarm_handler is not None:
            signal.signal(signal.SIGALRM, previous_alarm_handler)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("build-freeze")
    complete = subparsers.add_parser("build-execution-manifest")
    complete.add_argument("--expected-head", required=True)
    run = subparsers.add_parser("run-entry")
    run.add_argument("--expected-head", required=True)
    run.add_argument("--graph-root", required=True)
    run.add_argument("--mode", required=True)
    run.add_argument("--cell-id", required=True)
    run.add_argument("--branch-id", required=True)
    run.add_argument("--physical-order-id", required=True)
    run.add_argument("--seed", required=True, type=int)
    run.add_argument("--attempt", required=True, type=int)
    run.add_argument("--output", required=True)
    actual_argv = list(sys.argv[1:] if argv is None else argv)
    args = parser.parse_args(actual_argv)
    root = repo_root()
    if args.command == "build-freeze":
        print(json.dumps(build_freeze(root), sort_keys=True))
        return 0
    require(sys.argv[0] == SOURCE_REL.as_posix(), "execution source argument differs from normalized freeze")
    require(sys.dont_write_bytecode is True, "future execution commands require .venv/bin/python -B")
    if args.command == "build-execution-manifest":
        require(
            actual_argv == ["build-execution-manifest", "--expected-head", args.expected_head],
            "completion command differs from normalized freeze",
        )
        manifest = build_execution_manifest(root, args.expected_head)
        print(json.dumps({"entries": manifest["evaluable_terminal_count"], "status": manifest["status"]}, sort_keys=True))
        return 0
    identity = {
        "mode": args.mode,
        "cell_id": args.cell_id,
        "branch_id": args.branch_id,
        "physical_order_id": args.physical_order_id,
        "seed": args.seed,
    }
    graph_argument = Path(args.graph_root)
    output_argument = Path(args.output)
    require(not graph_argument.is_absolute(), "absolute graph root is prohibited")
    require(not output_argument.is_absolute(), "absolute output path is prohibited")
    successor = load_json(root / POLICY_REL)
    require(
        args.graph_root == successor["runtime_invocation_identity"]["graph_root_argument"],
        "graph root argument drift",
    )
    graph_root = (root / graph_argument).resolve()
    output = root / output_argument
    result = run_entry(
        root,
        graph_root,
        identity,
        args.attempt,
        output,
        args.expected_head,
        actual_argv,
    )
    print(json.dumps({"entry_id": result["entry_identity"]["entry_id"], "status": "completed"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
