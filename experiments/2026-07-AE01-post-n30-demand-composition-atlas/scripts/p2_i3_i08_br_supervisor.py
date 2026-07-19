#!/usr/bin/env python3
"""External one-shot supervisor for the frozen P2-I3 B-R campaign.

The supervisor intentionally imports no PyGRC or case-runtime module.  It owns
activation consumption, durable campaign/entry claims, the P0-P5 boundary,
fresh-child launch, resource observation, terminal ledgers, and closeout.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import resource
import signal
import shutil
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

import jsonschema

from p2_i3_br_execution_runtime import (
    ROOT,
    canonical_bytes,
    classify_retry_token_closure,
    ensure_no_symlink_components,
    load_json,
    payload_digest,
    require,
    sha256_file,
    validate_policy_command_environments,
    verify_digest,
    with_digest,
    write_exclusive_json,
)


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
POLICY_REL = EXPERIMENT / "configs/p2_i3_br_i07_execution_policy.json"
MATRIX_REL = EXPERIMENT / "contracts/p2-i3/i07-br-run-matrix.json"
FREEZE_REL = EXPERIMENT / "contracts/p2-i3/i07-br-inactive-exec-freeze.json"
CASE_SOURCE_REL = EXPERIMENT / "scripts/p2_i3_i08_br_case.py"
EXPECTED_GRAPH_REVISION = "565706f8b7647f6b7638b9afbe52372e170bf724"
SCHEMA_REL = EXPERIMENT / "contracts/p2-i3/i07-br-execution-authority.schema.json"

FREEZE_ACCEPTANCE_FIELDS = frozenset(
    {
        "artifact_id",
        "artifact_version",
        "iteration_id",
        "branch_id",
        "freeze_retention_commit",
        "accepted_freeze",
        "execution_authorized",
        "activation_construction_permitted",
        "canonical_payload_digest",
    }
)
ACTIVATION_FIELDS = frozenset(
    {
        "artifact_id",
        "artifact_version",
        "iteration_id",
        "branch_id",
        "freeze_acceptance",
        "accepted_freeze",
        "freeze_retention_commit",
        "owner_execution_direction",
        "launch_head_binding",
        "launch_environment",
        "interpreter_binding",
        "graph_root_binding",
        "governed_path_policy",
        "consumed",
        "canonical_payload_digest",
    }
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    require(result.returncode == 0, f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def tracked_tree_clean(root: Path) -> bool:
    return git(root, "status", "--porcelain=v1", "--untracked-files=no") == ""


def full_head(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", value))


def require_exact_fields(record: Mapping[str, Any], expected: frozenset[str], name: str) -> None:
    require(set(record) == expected, f"{name} fields are not closed")


def expected_launch_environment(policy: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "required_environment": deepcopy(policy["environment"]["required_environment"]),
        "pythonpath_template": policy["environment"]["normalized_pythonpath"],
        "pythonhome": policy["environment"]["pythonhome"],
        "ambient_or_installed_fallback_allowed": policy["environment"]["ambient_or_installed_fallback_allowed"],
    }


def validate_launch_binding(
    policy: Mapping[str, Any], activation: Mapping[str, Any], graph_root: Path
) -> None:
    require(
        activation["launch_environment"] == expected_launch_environment(policy),
        "activation launch environment drifted",
    )
    for key, expected in policy["environment"]["required_environment"].items():
        require(os.environ.get(key) == expected, f"launch environment mismatch: {key}")
    require("PYTHONHOME" not in os.environ, "PYTHONHOME must be absent")
    graph_root_value = os.environ.get(policy["environment"]["graph_root_environment_variable"])
    require(bool(graph_root_value), "RCAE_PYGRC_ROOT is required")
    require(Path(str(graph_root_value)).resolve() == graph_root, "RCAE_PYGRC_ROOT target drifted")
    expected_pythonpath = policy["environment"]["normalized_pythonpath"].replace(
        "${RCAE_PYGRC_ROOT}", str(graph_root_value)
    )
    require(os.environ.get("PYTHONPATH") == expected_pythonpath, "launch PYTHONPATH drifted")

    interpreter = activation["interpreter_binding"]
    invocation = ROOT / policy["environment"]["interpreter"]
    resolved_interpreter = invocation.resolve()
    require(invocation.exists() and resolved_interpreter.is_file(), "registered interpreter is missing")
    require(Path(sys.executable).resolve() == resolved_interpreter, "supervisor interpreter target drifted")
    require(sha256_file(resolved_interpreter) == interpreter["resolved_target_sha256"], "interpreter target digest drifted")
    require(interpreter["invocation_path"] == policy["environment"]["interpreter"], "interpreter invocation path drifted")
    require(interpreter["python_version"] == platform.python_version(), "interpreter version drifted")
    require(interpreter["python_implementation"] == platform.python_implementation(), "interpreter implementation drifted")

    graph = activation["graph_root_binding"]
    require(graph["environment_variable"] == policy["environment"]["graph_root_environment_variable"], "graph-root variable drifted")
    require(graph["retained_root"] == policy["environment"]["retained_graph_root"], "retained graph-root placeholder drifted")
    require(graph["resolved_target_revision"] == EXPECTED_GRAPH_REVISION, "activation graph revision drifted")
    require(graph["resolved_target_source_root"] == "src", "activation graph source root drifted")
    require(graph["machine_local_path_retained"] is False, "activation retained a machine-local graph path")
    require(
        sha256_file(graph_root / "src/pygrc/__init__.py")
        == graph["resolved_target_pygrc_init_sha256"],
        "activation PyGRC root identity drifted",
    )
    require(
        all(activation["governed_path_policy"].values()),
        "activation weakens governed path symlink refusal",
    )


def host_boot_id() -> str:
    path = Path("/proc/sys/kernel/random/boot_id")
    return path.read_text(encoding="utf-8").strip() if path.is_file() else f"platform:{platform.node()}"


def append_phase(
    path: Path, *, phase: str, entry_id: str, case_id: str | None, attempt: int
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = (
        json.dumps(
            {
                "phase": phase,
                "entry_id": entry_id,
                "case_id": case_id,
                "attempt": attempt,
                "monotonic_ns": time.monotonic_ns(),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(descriptor, record)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    parent_descriptor = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)


def load_authority(expected_head: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], Path]:
    require(full_head(expected_head), "launch HEAD must be a full 40-character commit")
    require(git(ROOT, "rev-parse", "HEAD") == expected_head, "launch HEAD drifted")
    require(tracked_tree_clean(ROOT), "tracked RCAE authority tree is dirty")
    policy = load_json(ROOT / POLICY_REL)
    validate_policy_command_environments(policy)
    matrix = load_json(ROOT / MATRIX_REL)
    freeze = load_json(ROOT / FREEZE_REL)
    verify_digest(matrix)
    verify_digest(freeze)
    acceptance_path = ROOT / policy["future_authority_paths"]["freeze_acceptance"]
    activation_path = ROOT / policy["future_authority_paths"]["activation"]
    ensure_no_symlink_components(ROOT, policy["future_authority_paths"]["freeze_acceptance"])
    ensure_no_symlink_components(ROOT, policy["future_authority_paths"]["activation"])
    acceptance = load_json(acceptance_path)
    activation = load_json(activation_path)
    verify_digest(acceptance)
    verify_digest(activation)
    schema = load_json(ROOT / SCHEMA_REL)
    jsonschema.validate(acceptance, schema)
    jsonschema.validate(activation, schema)
    require_exact_fields(acceptance, FREEZE_ACCEPTANCE_FIELDS, "freeze acceptance")
    require_exact_fields(activation, ACTIVATION_FIELDS, "activation")
    require(acceptance["artifact_id"] == "P2-I3-BR-I07-FREEZE-ACCEPTANCE", "freeze acceptance missing")
    require(acceptance["execution_authorized"] is False, "freeze acceptance improperly authorizes execution")
    require(acceptance["activation_construction_permitted"] is True, "activation construction was not permitted")
    require(activation["artifact_id"] == "P2-I3-BR-I07-EXECUTION-ACTIVATION", "execution activation missing")
    require(activation["owner_execution_direction"] is True, "explicit owner execution direction absent")
    require(activation["consumed"] is False, "retained activation shape drifted")
    require(activation["freeze_acceptance"]["sha256"] == sha256_file(acceptance_path), "activation acceptance digest drift")
    require(activation["accepted_freeze"]["sha256"] == sha256_file(ROOT / FREEZE_REL), "activation freeze digest drift")
    require(activation["freeze_retention_commit"] == acceptance["freeze_retention_commit"], "freeze retention commit drift")
    require(git(ROOT, "merge-base", activation["freeze_retention_commit"], "HEAD") == activation["freeze_retention_commit"], "freeze retention anchor is not an ancestor")
    for source in freeze["source_identities"]:
        require(sha256_file(ROOT / source["path"]) == source["sha256"], f"frozen source drift: {source['path']}")
    graph_raw = os.environ.get(policy["environment"]["graph_root_environment_variable"])
    require(bool(graph_raw), "RCAE_PYGRC_ROOT is required")
    graph_root = Path(str(graph_raw)).resolve()
    require(graph_root.is_dir(), "RCAE_PYGRC_ROOT does not resolve to a directory")
    require(git(graph_root, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION, "graph revision drifted")
    require(git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph worktree is dirty")
    require((graph_root / "src/pygrc/__init__.py").is_file(), "exact PyGRC source import is missing")
    ensure_no_symlink_components(ROOT, policy["live_paths"]["governed_root"])
    validate_launch_binding(policy, activation, graph_root)
    return policy, matrix, freeze, activation, graph_root


def campaign_claim_document(
    *, expected_head: str, freeze: Mapping[str, Any], activation: Mapping[str, Any], matrix: Mapping[str, Any]
) -> dict[str, Any]:
    return with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-PERMANENT-CAMPAIGN-CLAIM",
            "artifact_version": "1.0.0",
            "branch_id": "P2-I3-BR",
            "cycle_id": "P2-I3-BR-C01",
            "launch_head": expected_head,
            "activation_canonical_payload_digest": activation["canonical_payload_digest"],
            "launch_environment_digest": payload_digest(activation["launch_environment"]),
            "interpreter_target_sha256": activation["interpreter_binding"]["resolved_target_sha256"],
            "graph_root_binding_digest": payload_digest(activation["graph_root_binding"]),
            "inactive_freeze_canonical_payload_digest": freeze["canonical_payload_digest"],
            "matrix_canonical_payload_digest": matrix["canonical_payload_digest"],
            "expected_terminal_set_digest": matrix["expected_terminal_set_digest"],
            "canonical_case_count": matrix["canonical_case_count"],
            "governed_entry_count": matrix["governed_entry_count"],
            "maximum_governed_child_starts": matrix["maximum_governed_child_starts"],
            "boot_id": host_boot_id(),
            "campaign_started_monotonic_ns": time.monotonic_ns(),
            "campaign_ceiling_seconds": matrix["campaign_resource_envelope"]["campaign"]["exact_campaign_ceiling_seconds"],
            "activation_consumed": True,
            "campaign_claim_crosses_p5": False,
            "permanent": True,
            "reusable": False,
        }
    )


def entry_claim_document(
    *, entry: Mapping[str, Any], attempt: int, expected_head: str, campaign_claim: Mapping[str, Any]
) -> dict[str, Any]:
    return with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-ENTRY-ATTEMPT-CLAIM",
            "artifact_version": "1.0.0",
            "entry_id": entry["entry_id"],
            "entry_kind": entry["entry_kind"],
            "case_id": entry["case_id"],
            "schedule_ordinal": entry["schedule_ordinal"],
            "execution_class": entry["execution_class"],
            "attempt": attempt,
            "launch_head": expected_head,
            "campaign_claim_digest": campaign_claim["canonical_payload_digest"],
            "entry_operation_identity": payload_digest({"entry": entry}),
            "resource": deepcopy(entry["resource"]),
            "permanent": True,
            "claimed_monotonic_ns": time.monotonic_ns(),
        }
    )


def p5_document(*, entry: Mapping[str, Any], attempt: int, expected_head: str, claim: Mapping[str, Any]) -> dict[str, Any]:
    return with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-P5-AUTHORIZATION",
            "artifact_version": "1.0.0",
            "entry_id": entry["entry_id"],
            "entry_kind": entry["entry_kind"],
            "case_id": entry["case_id"],
            "attempt": attempt,
            "launch_head": expected_head,
            "entry_claim_digest": claim["canonical_payload_digest"],
            "entry_operation_identity": payload_digest({"entry": entry}),
            "dispatch_authorized": True,
            "single_use": True,
            "issued_monotonic_ns": time.monotonic_ns(),
        }
    )


def child_environment(policy: Mapping[str, Any], graph_root: Path) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONHOME"}}
    env.update(policy["environment"]["required_environment"])
    scripts = ROOT / EXPERIMENT / "scripts"
    env["PYTHONPATH"] = os.pathsep.join((str(graph_root / "src"), str(scripts)))
    env["RCAE_PYGRC_ROOT"] = str(graph_root)
    return env


def preflight_schedule(policy: Mapping[str, Any], matrix: Mapping[str, Any]) -> None:
    entries = matrix["entries"]
    require(len(entries) == matrix["governed_entry_count"] == 456, "governed entry population drifted")
    require(matrix["canonical_case_count"] == 450, "canonical case population drifted")
    require(matrix["operational_baseline_entry_count"] == 6, "operational baseline population drifted")
    require(matrix["maximum_governed_child_starts"] == 460, "child-start ceiling drifted")
    ordinals = {row["entry_id"]: row["schedule_ordinal"] for row in entries}
    require(len(ordinals) == 456, "governed entry identities are not unique")
    require(sorted(ordinals.values()) == list(range(1, 457)), "governed schedule ordinals drifted")
    for key in ("governed_root", "content_store", "campaign_claim", "resume_claim", "cycle_closeout"):
        ensure_no_symlink_components(ROOT, policy["live_paths"][key])
    retry_classes = {
        row["execution_class"] for row in matrix["attempt_governance"]["class_retry_tokens"]
    }
    require(len(retry_classes) == 4, "retry-token execution classes are not closed")
    for execution_class in retry_classes:
        ensure_no_symlink_components(
            ROOT,
            policy["live_paths"]["retry_token_template"].format(
                execution_class=execution_class
            ),
        )
    for entry in entries:
        require(
            all(parent in ordinals and ordinals[parent] < entry["schedule_ordinal"] for parent in entry["parent_entry_ids"]),
            f"dependency order drifted: {entry['entry_id']}",
        )
        for relative in entry["governed_paths"].values():
            path = ensure_no_symlink_components(ROOT, relative)
            require(not path.exists(), f"governed entry path is not absent at campaign preflight: {relative}")
    envelope = matrix["campaign_resource_envelope"]
    require(
        envelope["campaign"]["exact_campaign_ceiling_seconds"]
        <= envelope["campaign"]["outer_campaign_ceiling_seconds"],
        "campaign time envelope exceeds outer ceiling",
    )
    require(
        envelope["bytes"]["governed_physical_projection_bytes"]
        <= envelope["bytes"]["governed_physical_ceiling_bytes"],
        "physical byte projection exceeds outer ceiling",
    )
    governed_root = ROOT / policy["live_paths"]["governed_root"]
    governed_root.parent.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(governed_root.parent).free
    require(
        free >= envelope["bytes"]["governed_physical_projection_bytes"],
        "host free space cannot admit frozen physical projection",
    )


def dependency_available(entry: Mapping[str, Any], matrix_by_id: Mapping[str, Mapping[str, Any]]) -> bool:
    for parent in entry["dependency_ids"]:
        if parent in matrix_by_id:
            path = ROOT / matrix_by_id[parent]["governed_paths"]["entry_resolution"]
            if not path.is_file():
                return False
            resolution = load_json(path)
            if resolution["status"] != "valid_terminal":
                return False
    return True


def write_blocked_resolution(entry: Mapping[str, Any], reason: str) -> None:
    write_entry_resolution(
        entry=entry,
        primary_terminal=None,
        unstarted_status="blocked_dependency",
        reason=reason,
    )


def process_tree_rss_bytes(root_pid: int) -> int:
    parents: dict[int, int] = {}
    rss: dict[int, int] = {}
    proc = Path("/proc")
    if not proc.is_dir():
        return 0
    for child in proc.iterdir():
        if not child.name.isdigit():
            continue
        try:
            status = (child / "status").read_text(encoding="utf-8")
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
        values: dict[str, str] = {}
        for line in status.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                values[key] = value.strip()
        try:
            pid = int(values["Pid"])
            parents[pid] = int(values["PPid"])
            rss[pid] = int(values.get("VmRSS", "0 kB").split()[0]) * 1024
        except (KeyError, ValueError):
            continue
    members = {root_pid}
    changed = True
    while changed:
        changed = False
        for pid, parent in parents.items():
            if parent in members and pid not in members:
                members.add(pid)
                changed = True
    return sum(rss.get(pid, 0) for pid in members)


def terminate_process_group(process: subprocess.Popen[bytes]) -> tuple[str, int | None]:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return "already_exited", process.poll()
    try:
        return "terminated_gracefully", process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        return "forcibly_terminated_after_10_seconds", process.wait()


def finalize_captured_stream(partial: Path, final: Path, *, ceiling: int) -> tuple[bytes, bool]:
    require(partial.is_file() and not partial.is_symlink(), "captured stream partial is absent or symlinked")
    size = partial.stat().st_size
    overflow = size > ceiling
    if overflow:
        with partial.open("r+b") as handle:
            handle.truncate(ceiling)
            handle.flush()
            os.fsync(handle.fileno())
    require(not final.exists(), "captured stream final path already exists")
    os.rename(partial, final)
    parent_descriptor = os.open(final.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)
    return final.read_bytes(), overflow


def run_child(
    *,
    policy: Mapping[str, Any],
    graph_root: Path,
    entry: Mapping[str, Any],
    attempt: int,
    expected_head: str,
    campaign_claim: Mapping[str, Any],
) -> dict[str, Any]:
    prefix = "primary" if attempt == 1 else "retry"
    paths = entry["governed_paths"]
    claim_path = ROOT / paths[f"{prefix}_claim"]
    phase_path = ROOT / paths[f"{prefix}_phase_ledger"]
    ready_path = ROOT / paths[f"{prefix}_ready"]
    failure_path = ROOT / paths[f"{prefix}_failure"]
    p5_path = ROOT / paths[f"{prefix}_p5"]
    p5_consumption_path = ROOT / paths[f"{prefix}_p5_consumption"]
    stdout_path = ROOT / paths[f"{prefix}_stdout"]
    stdout_partial_path = ROOT / paths[f"{prefix}_stdout_partial"]
    stderr_path = ROOT / paths[f"{prefix}_stderr"]
    stderr_partial_path = ROOT / paths[f"{prefix}_stderr_partial"]
    terminal_path = ROOT / paths[f"{prefix}_terminal"]
    resource_path = ROOT / paths[f"{prefix}_resource"]
    output_path = ROOT / paths["logical_manifest"]
    for path in (
        claim_path,
        phase_path,
        ready_path,
        failure_path,
        p5_path,
        p5_consumption_path,
        stdout_path,
        stdout_partial_path,
        stderr_path,
        stderr_partial_path,
        terminal_path,
        resource_path,
    ):
        ensure_no_symlink_components(ROOT, path.relative_to(ROOT))
        require(not path.exists(), f"governed attempt path already exists: {path}")
    require(not output_path.exists(), "entry logical output already exists")

    claim = entry_claim_document(entry=entry, attempt=attempt, expected_head=expected_head, campaign_claim=campaign_claim)
    write_exclusive_json(claim_path, claim)
    append_phase(phase_path, phase="P0_governed_entry_claim_durable", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)

    command = [
        ".venv/bin/python",
        "-B",
        CASE_SOURCE_REL.as_posix(),
        "run-entry",
        "--entry-id",
        entry["entry_id"],
        "--claim",
        str(claim_path),
        "--ready",
        str(ready_path),
        "--failure",
        str(failure_path),
        "--p5",
        str(p5_path),
        "--p5-consumption",
        str(p5_consumption_path),
        "--p5-wait-seconds",
        str(entry["resource"]["case_timeout_seconds"]),
        "--expected-head",
        expected_head,
        "--governed-root",
        str(ROOT / policy["live_paths"]["governed_root"]),
        "--output",
        str(output_path),
    ]
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    timeout_seconds = int(entry["resource"]["case_timeout_seconds"])
    stdout_ceiling = int(entry["resource"]["prospective_stdout_bytes"])
    stderr_ceiling = int(entry["resource"]["prospective_stderr_bytes"])
    started_ns = time.monotonic_ns()
    deadline_ns = started_ns + timeout_seconds * 1_000_000_000
    peak_tree_rss = 0
    p5: dict[str, Any] | None = None
    termination_reason: str | None = None
    with stdout_partial_path.open("xb") as stdout_handle, stderr_partial_path.open("xb") as stderr_handle:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=child_environment(policy, graph_root),
            stdout=stdout_handle,
            stderr=stderr_handle,
            start_new_session=True,
        )
        append_phase(phase_path, phase="P1_child_started", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)
        while process.poll() is None:
            peak_tree_rss = max(peak_tree_rss, process_tree_rss_bytes(process.pid))
            stdout_handle.flush()
            stderr_handle.flush()
            if stdout_partial_path.stat().st_size > stdout_ceiling or stderr_partial_path.stat().st_size > stderr_ceiling:
                termination_reason, _ = terminate_process_group(process)
                termination_reason = f"log_overflow:{termination_reason}"
                break
            if time.monotonic_ns() >= deadline_ns:
                termination_reason, _ = terminate_process_group(process)
                termination_reason = f"timeout:{termination_reason}"
                break
            if ready_path.is_file() and p5 is None:
                ready = load_json(ready_path)
                verify_digest(ready)
                require(ready["entry_id"] == entry["entry_id"], "child readiness entry drift")
                require(ready["claim_digest"] == claim["canonical_payload_digest"], "child readiness claim drift")
                require(ready["scientific_or_integrity_operation_count"] == 0, "child crossed operation boundary before P5")
                append_phase(phase_path, phase="P2_authorities_and_inputs_loaded", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)
                append_phase(phase_path, phase="P3_parent_restored_and_validated", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)
                append_phase(phase_path, phase="P4_entry_boundary_armed", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)
                p5 = p5_document(entry=entry, attempt=attempt, expected_head=expected_head, claim=claim)
                write_exclusive_json(p5_path, p5)
                append_phase(phase_path, phase="P5_entry_specific_dispatch_authorized", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)
            time.sleep(0.01)
        returncode = process.wait()
        peak_tree_rss = max(peak_tree_rss, process_tree_rss_bytes(process.pid))
        stdout_handle.flush()
        stderr_handle.flush()
        os.fsync(stdout_handle.fileno())
        os.fsync(stderr_handle.fileno())
    elapsed = time.monotonic_ns() - started_ns
    stdout, stdout_overflow = finalize_captured_stream(
        stdout_partial_path,
        stdout_path,
        ceiling=stdout_ceiling,
    )
    stderr, stderr_overflow = finalize_captured_stream(
        stderr_partial_path,
        stderr_path,
        ceiling=stderr_ceiling,
    )
    log_overflow = stdout_overflow or stderr_overflow
    child_failure = load_json(failure_path) if failure_path.is_file() else None
    if child_failure is not None:
        verify_digest(child_failure)
        require(child_failure["entry_id"] == entry["entry_id"], "child failure entry drift")
    success = returncode == 0 and output_path.is_file() and p5 is not None and child_failure is None
    if success:
        status = "valid_terminal"
    elif child_failure is not None:
        status = child_failure["status_hint"]
    elif termination_reason is not None and p5 is None:
        status = "attested_pre_candidate_infrastructure_failure"
    elif termination_reason is not None:
        status = "post_candidate_infrastructure_failure"
    elif returncode == 0 and not output_path.is_file():
        status = "invalid_execution"
    else:
        status = "unknown_boundary_failure"
    retry_eligible = (
        status == "attested_pre_candidate_infrastructure_failure"
        and p5 is None
        and not output_path.exists()
    )
    if p5 is not None:
        append_phase(phase_path, phase="P6_output_observed", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)
    resource_receipt = with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-ENTRY-RESOURCE-RECEIPT",
            "artifact_version": "1.0.0",
            "entry_id": entry["entry_id"],
            "attempt": attempt,
            "elapsed_monotonic_ns": elapsed,
            "peak_process_tree_rss_bytes": peak_tree_rss,
            "stdout_bytes": len(stdout),
            "stderr_bytes": len(stderr),
            "stdout_ceiling_bytes": stdout_ceiling,
            "stderr_ceiling_bytes": stderr_ceiling,
            "log_overflow": log_overflow,
            "termination_reason": termination_reason,
            "returncode": returncode,
            "experiment_RLIMIT_AS": None,
            "experiment_RSS_kill_threshold": None,
        }
    )
    write_exclusive_json(resource_path, resource_receipt)
    terminal = with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-ATTEMPT-TERMINAL",
            "artifact_version": "1.0.0",
            "entry_id": entry["entry_id"],
            "entry_kind": entry["entry_kind"],
            "case_id": entry["case_id"],
            "attempt": attempt,
            "launch_head": expected_head,
            "claim_digest": claim["canonical_payload_digest"],
            "p5_digest": p5["canonical_payload_digest"] if p5 is not None else None,
            "p5_consumption_sha256": sha256_file(p5_consumption_path) if p5_consumption_path.is_file() else None,
            "status": status,
            "returncode": returncode,
            "elapsed_monotonic_ns": elapsed,
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "logical_manifest_sha256": sha256_file(output_path) if output_path.is_file() else None,
            "resource_receipt_digest": resource_receipt["canonical_payload_digest"],
            "child_failure_digest": child_failure["canonical_payload_digest"] if child_failure else None,
            "p5_crossed": p5 is not None,
            "retry_eligible": retry_eligible,
            "scientific_interpretation_assigned": False,
        }
    )
    write_exclusive_json(terminal_path, terminal)
    append_phase(phase_path, phase="P7_terminal_receipt_complete", entry_id=entry["entry_id"], case_id=entry["case_id"], attempt=attempt)
    return terminal


def retry_token_path(policy: Mapping[str, Any], execution_class: str) -> Path:
    relative = policy["live_paths"]["retry_token_template"].format(
        execution_class=execution_class
    )
    ensure_no_symlink_components(ROOT, relative)
    return ROOT / relative


def allocate_retry_token(
    *,
    policy: Mapping[str, Any],
    entry: Mapping[str, Any],
    primary_terminal: Mapping[str, Any],
) -> dict[str, Any] | None:
    require(primary_terminal["retry_eligible"] is True, "ineligible terminal requested retry allocation")
    path = retry_token_path(policy, entry["execution_class"])
    if path.exists():
        existing = load_json(path)
        verify_digest(existing)
        return existing if existing["entry_id"] == entry["entry_id"] else None
    primary_claim_path = ROOT / entry["governed_paths"]["primary_claim"]
    primary_phase_path = ROOT / entry["governed_paths"]["primary_phase_ledger"]
    require(not (ROOT / entry["governed_paths"]["primary_p5"]).exists(), "retry allocation found P5 authority")
    require(not (ROOT / entry["governed_paths"]["logical_manifest"]).exists(), "retry allocation found result artifact")
    token = with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-CLASS-RETRY-TOKEN-ALLOCATION",
            "artifact_version": "1.0.0",
            "execution_class": entry["execution_class"],
            "entry_id": entry["entry_id"],
            "case_id": entry["case_id"],
            "schedule_ordinal": entry["schedule_ordinal"],
            "attempt_1_claim_sha256": sha256_file(primary_claim_path),
            "attempt_1_phase_ledger_sha256": sha256_file(primary_phase_path),
            "attempt_1_terminal_digest": primary_terminal["canonical_payload_digest"],
            "eligibility": "attested_failure_at_or_before_P4_no_P5_no_result",
            "attempt_2_timeout_seconds": entry["resource"]["case_timeout_seconds"],
            "allocation_ordinal": 1,
            "permanent": True,
            "reassignable": False,
        }
    )
    write_exclusive_json(path, token)
    return token


def write_entry_resolution(
    *,
    entry: Mapping[str, Any],
    primary_terminal: Mapping[str, Any] | None,
    retry_terminal: Mapping[str, Any] | None = None,
    retry_token: Mapping[str, Any] | None = None,
    unstarted_status: str | None = None,
    reason: str | None = None,
) -> dict[str, Any]:
    if unstarted_status is not None:
        require(primary_terminal is None and retry_terminal is None, "unstarted resolution has an attempt terminal")
        status = unstarted_status
        admitted_attempt = None
    elif retry_terminal is not None:
        require(primary_terminal is not None and retry_token is not None, "retry resolution is incomplete")
        status = retry_terminal["status"]
        admitted_attempt = 2 if status == "valid_terminal" else None
    else:
        require(primary_terminal is not None, "started resolution lacks primary terminal")
        status = primary_terminal["status"]
        admitted_attempt = 1 if status == "valid_terminal" else None
    artifact_id = (
        "P2-I3-BR-C01-OPERATIONAL-BASELINE-TERMINAL"
        if entry["entry_kind"] == "operational_baseline_construction"
        else "P2-I3-BR-C01-CASE-RESOLUTION"
    )
    record = with_digest(
        {
            "artifact_id": artifact_id,
            "artifact_version": "1.0.0",
            "entry_id": entry["entry_id"],
            "entry_kind": entry["entry_kind"],
            "case_id": entry["case_id"],
            "status": status,
            "reason": reason,
            "admitted_attempt": admitted_attempt,
            "primary_terminal_digest": primary_terminal["canonical_payload_digest"] if primary_terminal else None,
            "retry_terminal_digest": retry_terminal["canonical_payload_digest"] if retry_terminal else None,
            "retry_token_digest": retry_token["canonical_payload_digest"] if retry_token else None,
            "attempt_1_retained": primary_terminal is not None,
            "attempt_2_retained": retry_terminal is not None,
            "scientific_interpretation_assigned": False,
        }
    )
    write_exclusive_json(ROOT / entry["governed_paths"]["entry_resolution"], record)
    return record


def retry_token_closure(
    *,
    policy: Mapping[str, Any],
    matrix: Mapping[str, Any],
    token_spec: Mapping[str, Any],
) -> dict[str, Any]:
    execution_class = str(token_spec["execution_class"])
    token_path = retry_token_path(policy, execution_class)
    class_entries = [
        row for row in matrix["entries"] if row["execution_class"] == execution_class
    ]
    retry_keys = sorted(
        key
        for key in class_entries[0]["governed_paths"]
        if key.startswith("retry_")
    )
    existing_by_entry: dict[str, list[str]] = {}
    for entry in class_entries:
        existing = [
            entry["governed_paths"][key]
            for key in retry_keys
            if (ROOT / entry["governed_paths"][key]).exists()
        ]
        if existing:
            existing_by_entry[entry["entry_id"]] = existing

    if not token_path.exists():
        state = classify_retry_token_closure(
            token_present=False,
            attempt_2_claim_present=False,
            attempt_2_terminal_status=None,
            attempt_2_descendant_count=sum(map(len, existing_by_entry.values())),
        )
        return {
            "token_id": token_spec["token_id"],
            "execution_class": execution_class,
            "closure_model": "token_root_owns_optional_attempt_2_descendants",
            "state": state,
            "token_identity": None,
            "descendants": [],
        }

    token = load_json(token_path)
    verify_digest(token)
    require(token["execution_class"] == execution_class, "retry token class drifted")
    require(token["permanent"] is True and token["reassignable"] is False, "retry token is not permanent")
    require(set(existing_by_entry) <= {token["entry_id"]}, "retry output is not owned by its class token")
    entry = next(
        (row for row in class_entries if row["entry_id"] == token["entry_id"]), None
    )
    require(entry is not None, "retry token names an unregistered entry")
    paths = entry["governed_paths"]
    claim_path = ROOT / paths["retry_claim"]
    terminal_path = ROOT / paths["retry_terminal"]
    terminal = load_json(terminal_path) if terminal_path.is_file() else None
    if terminal is not None:
        verify_digest(terminal)
        require(terminal["attempt"] == 2, "retry token reached a non-retry terminal")
        require(terminal["entry_id"] == entry["entry_id"], "retry terminal entry drifted")
    existing = existing_by_entry.get(entry["entry_id"], [])
    state = classify_retry_token_closure(
        token_present=True,
        attempt_2_claim_present=claim_path.is_file(),
        attempt_2_terminal_status=terminal["status"] if terminal else None,
        attempt_2_descendant_count=len(existing),
    )
    require(
        not (ROOT / paths["retry_stdout_partial"]).exists()
        and not (ROOT / paths["retry_stderr_partial"]).exists(),
        "retry closure contains an unresolved captured-stream partial",
    )
    descendant_paths = list(existing)
    for key in ("entry_resolution", "logical_manifest"):
        relative = paths[key]
        if (ROOT / relative).is_file():
            descendant_paths.append(relative)
    descendants = []
    for relative in sorted(set(descendant_paths)):
        ensure_no_symlink_components(ROOT, relative, leaf_may_be_absent=False)
        descendants.append({"path": relative, "sha256": sha256_file(ROOT / relative)})
    return {
        "token_id": token_spec["token_id"],
        "execution_class": execution_class,
        "closure_model": "token_root_owns_optional_attempt_2_descendants",
        "state": state,
        "token_identity": {
            "path": token_path.relative_to(ROOT).as_posix(),
            "sha256": sha256_file(token_path),
        },
        "descendants": descendants,
    }


def close_cycle(
    *, policy: Mapping[str, Any], matrix: Mapping[str, Any], campaign_claim: Mapping[str, Any], expected_head: str
) -> dict[str, Any]:
    resolutions = []
    for entry in matrix["entries"]:
        path = ROOT / entry["governed_paths"]["entry_resolution"]
        require(path.is_file(), f"entry resolution missing: {entry['entry_id']}")
        resolutions.append(load_json(path))
    statuses = {status: sum(row["status"] == status for row in resolutions) for status in sorted({row["status"] for row in resolutions})}
    if statuses == {"valid_terminal": 456}:
        closure = "complete"
    elif "authority_breach" in statuses:
        closure = "failed_closed"
    elif "invalid_execution" in statuses:
        closure = "invalid"
    else:
        closure = "bounded_incomplete"
    record = with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-CYCLE-CLOSEOUT",
            "artifact_version": "1.0.0",
            "launch_head": expected_head,
            "campaign_claim_digest": campaign_claim["canonical_payload_digest"],
            "expected_terminal_set_digest": matrix["expected_terminal_set_digest"],
            "entry_resolution_count": len(resolutions),
            "entry_status_counts": statuses,
            "retry_token_closures": [
                retry_token_closure(policy=policy, matrix=matrix, token_spec=token)
                for token in matrix["attempt_governance"]["class_retry_tokens"]
            ],
            "resume_closure": (
                "used_once_and_closed"
                if (ROOT / policy["live_paths"]["resume_claim"]).is_file()
                else "unused"
            ),
            "cycle_status": closure,
            "scientific_interpretation_assigned": False,
            "control_outcomes_assigned": 0,
        }
    )
    write_exclusive_json(ROOT / policy["live_paths"]["cycle_closeout"], record)
    return record


def validate_no_unresolved_attempt_claims(matrix: Mapping[str, Any]) -> None:
    for entry in matrix["entries"]:
        for prefix in ("primary", "retry"):
            claim = ROOT / entry["governed_paths"][f"{prefix}_claim"]
            terminal = ROOT / entry["governed_paths"][f"{prefix}_terminal"]
            require(
                not claim.exists() or terminal.is_file(),
                f"unresolved governed entry claim blocks resumption: {entry['entry_id']}:{prefix}",
            )


def resume_claim_document(
    *, expected_head: str, campaign_claim: Mapping[str, Any], matrix: Mapping[str, Any]
) -> dict[str, Any]:
    return with_digest(
        {
            "artifact_id": "P2-I3-BR-C01-PERMANENT-SUPERVISOR-RESUME-CLAIM",
            "artifact_version": "1.0.0",
            "launch_head": expected_head,
            "campaign_claim_digest": campaign_claim["canonical_payload_digest"],
            "boot_id": host_boot_id(),
            "resumed_monotonic_ns": time.monotonic_ns(),
            "governed_entry_count": matrix["governed_entry_count"],
            "schedule_digest": payload_digest(
                {"entry_ids": [row["entry_id"] for row in matrix["entries"]]}
            ),
            "campaign_clock_reset": False,
            "resource_budget_reset": False,
            "resume_count": 1,
            "permanent": True,
        }
    )


def run_campaign(args: argparse.Namespace) -> int:
    policy, matrix, freeze, activation, graph_root = load_authority(args.expected_head)
    claim_path = ROOT / policy["live_paths"]["campaign_claim"]
    ensure_no_symlink_components(ROOT, policy["live_paths"]["campaign_claim"])
    resume = bool(getattr(args, "resume", False))
    if resume:
        require(claim_path.is_file(), "campaign claim is absent; no campaign can be resumed")
        require(not (ROOT / policy["live_paths"]["cycle_closeout"]).exists(), "closed campaign cannot resume")
        campaign_claim = load_json(claim_path)
        verify_digest(campaign_claim)
        require(campaign_claim["launch_head"] == args.expected_head, "resume launch HEAD drifted")
        require(campaign_claim["boot_id"] == host_boot_id(), "resume host boot identity drifted")
        validate_no_unresolved_attempt_claims(matrix)
        resume_path = ROOT / policy["live_paths"]["resume_claim"]
        ensure_no_symlink_components(ROOT, policy["live_paths"]["resume_claim"])
        require(not resume_path.exists(), "bounded supervisor resume was already consumed")
        write_exclusive_json(
            resume_path,
            resume_claim_document(
                expected_head=args.expected_head,
                campaign_claim=campaign_claim,
                matrix=matrix,
            ),
        )
    else:
        require(not claim_path.exists(), "activation has already been consumed by a campaign claim")
        preflight_schedule(policy, matrix)
        campaign_claim = campaign_claim_document(expected_head=args.expected_head, freeze=freeze, activation=activation, matrix=matrix)
        write_exclusive_json(claim_path, campaign_claim)
        require(git(ROOT, "rev-parse", "HEAD") == args.expected_head and tracked_tree_clean(ROOT), "authority changed across campaign-claim creation")
    deadline_ns = campaign_claim["campaign_started_monotonic_ns"] + int(campaign_claim["campaign_ceiling_seconds"]) * 1_000_000_000
    matrix_by_id = {row["entry_id"]: row for row in matrix["entries"]}
    for entry in matrix["entries"]:
        if (ROOT / entry["governed_paths"]["entry_resolution"]).exists():
            continue
        if time.monotonic_ns() >= deadline_ns:
            write_entry_resolution(
                entry=entry,
                primary_terminal=None,
                unstarted_status="not_started_campaign_stop",
                reason="campaign_deadline",
            )
            continue
        if not dependency_available(entry, matrix_by_id):
            write_blocked_resolution(entry, "registered_parent_not_valid_terminal")
            continue
        primary_terminal_path = ROOT / entry["governed_paths"]["primary_terminal"]
        primary = (
            load_json(primary_terminal_path)
            if primary_terminal_path.is_file()
            else run_child(policy=policy, graph_root=graph_root, entry=entry, attempt=1, expected_head=args.expected_head, campaign_claim=campaign_claim)
        )
        verify_digest(primary)
        retry_token = None
        retry_terminal = None
        if primary["retry_eligible"]:
            retry_token = allocate_retry_token(
                policy=policy,
                entry=entry,
                primary_terminal=primary,
            )
            if retry_token is not None:
                retry_terminal_path = ROOT / entry["governed_paths"]["retry_terminal"]
                retry_terminal = (
                    load_json(retry_terminal_path)
                    if retry_terminal_path.is_file()
                    else run_child(
                        policy=policy,
                        graph_root=graph_root,
                        entry=entry,
                        attempt=2,
                        expected_head=args.expected_head,
                        campaign_claim=campaign_claim,
                    )
                )
                verify_digest(retry_terminal)
        write_entry_resolution(
            entry=entry,
            primary_terminal=primary,
            retry_terminal=retry_terminal,
            retry_token=retry_token,
        )
        require(git(graph_root, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION and git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph source changed during campaign")
    closeout = close_cycle(policy=policy, matrix=matrix, campaign_claim=campaign_claim, expected_head=args.expected_head)
    print(json.dumps({"status": closeout["cycle_status"], "entry_resolutions": closeout["entry_resolution_count"]}, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    sub = result.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run-campaign")
    run.add_argument("--expected-head", required=True)
    run.set_defaults(resume=False)
    run.set_defaults(func=run_campaign)
    resume = sub.add_parser("resume-campaign")
    resume.add_argument("--expected-head", required=True)
    resume.set_defaults(resume=True)
    resume.set_defaults(func=run_campaign)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
