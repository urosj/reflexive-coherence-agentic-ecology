#!/usr/bin/env python3
"""I05-owned one-shot wrapper around the immutable accepted I04R2 builder.

The wrapper consumes authority by exclusive claim creation before importing or
calling the accepted builder.  The claim is never removed.  This module is not
invoked by I05B safety validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from typing import Any, Callable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import ContractError, pretty_json_dumps  # noqa: E402


class OneShotError(ContractError):
    """Base failure for the I05 one-shot boundary."""


class AttemptAlreadyClaimed(OneShotError):
    """Raised when an attempt receipt already consumed the authority."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise OneShotError(f"expected JSON object: {path}")
    return value


def _path(relative: str) -> Path:
    path = ROOT / relative
    try:
        path.resolve().relative_to(ROOT.resolve())
    except ValueError as exc:
        raise OneShotError(f"path escapes repository root: {relative}") from exc
    return path


def _lexical_repo_path(relative: str) -> Path:
    """Resolve a command path lexically without following its final symlink."""

    supplied = Path(relative)
    if supplied.is_absolute() or not relative or any(
        part in ("", ".", "..") for part in supplied.parts
    ):
        raise OneShotError(f"invalid repository-relative command path: {relative}")
    path = (ROOT / supplied).absolute()
    try:
        path.relative_to(ROOT.absolute())
    except ValueError as exc:
        raise OneShotError(f"command path escapes repository root: {relative}") from exc
    return path


def _git_text(*args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=True,
        capture_output=True,
    ).stdout


def _git_quiet(*args: str) -> bool:
    return (
        subprocess.run(
            ("git", "-C", str(ROOT), *args),
            check=False,
            capture_output=True,
        ).returncode
        == 0
    )


def collect_repository_snapshot() -> dict[str, Any]:
    """Collect the exact pre-claim repository state."""

    return {
        "head": _git_text("rev-parse", "HEAD"),
        "index_clean": _git_quiet("diff", "--cached", "--quiet"),
        "porcelain": _git_text("status", "--porcelain=v1", "--untracked-files=all"),
        "worktree_clean": _git_quiet("diff", "--quiet"),
    }


def validate_repository_snapshot(snapshot: Mapping[str, Any], expected_head: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", expected_head):
        raise OneShotError("expected HEAD must be a full lowercase commit hash")
    if snapshot.get("head") != expected_head:
        raise OneShotError("runtime HEAD does not match the owner-authorized launch HEAD")
    if (
        snapshot.get("porcelain") != ""
        or snapshot.get("index_clean") is not True
        or snapshot.get("worktree_clean") is not True
    ):
        raise OneShotError("RCAE index/worktree is not clean at attempt preflight")


def interpreter_identity(executable: Path | None = None) -> dict[str, Any]:
    invoked = (executable or Path(sys.executable)).absolute()
    resolved = invoked.resolve()
    return {
        "base_prefix": str(Path(sys.base_prefix).resolve()),
        "binary_sha256": _sha256(resolved),
        "implementation": platform.python_implementation(),
        "invoked_executable": str(invoked),
        "major_minor": [sys.version_info.major, sys.version_info.minor],
        "resolved_executable": str(resolved),
        "venv_active": sys.prefix != sys.base_prefix,
        "venv_prefix": str(Path(sys.prefix).resolve()),
        "version": platform.python_version(),
    }


def validate_interpreter(
    identity: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> None:
    expected = policy["interpreter"]
    expected_invoked = _lexical_repo_path(expected["executable_repo_relative"])
    expected_venv = _lexical_repo_path(expected["venv_prefix_repo_relative"])
    if identity.get("invoked_executable") != str(expected_invoked):
        raise OneShotError("governed I05 invocation did not use exact .venv command path")
    resolved = expected_invoked.resolve()
    if identity.get("resolved_executable") != str(resolved):
        raise OneShotError("governed I05 resolved interpreter identity drifted")
    if identity.get("venv_active") is not True:
        raise OneShotError("governed I05 invocation requires an active virtual environment")
    if identity.get("venv_prefix") != str(expected_venv.resolve()):
        raise OneShotError("governed I05 invocation used the wrong virtual environment")
    if identity.get("base_prefix") == identity.get("venv_prefix"):
        raise OneShotError("governed I05 virtual environment is not isolated")
    if identity.get("implementation") != expected["implementation"]:
        raise OneShotError("wrong Python implementation for governed I05 invocation")
    if identity.get("major_minor") != expected["major_minor"]:
        raise OneShotError("wrong Python version for governed I05 invocation")
    if identity.get("binary_sha256") != _sha256(resolved):
        raise OneShotError("reported Python binary identity is inconsistent")
    if identity.get("binary_sha256") != expected["binary_sha256"]:
        raise OneShotError("wrong Python binary identity for governed I05 invocation")


def normalized_command(policy: Mapping[str, Any], expected_head: str) -> list[str]:
    return [
        policy["interpreter"]["executable_repo_relative"],
        policy["paths"]["wrapper"],
        "--policy",
        policy["paths"]["policy"],
        "--expected-head",
        expected_head,
    ]


def validate_command(
    actual: Sequence[str],
    policy: Mapping[str, Any],
    expected_head: str,
) -> None:
    expected = normalized_command(policy, expected_head)
    if list(actual) != expected:
        raise OneShotError("normalized governed command does not match one-shot policy")


def validate_policy(policy: Mapping[str, Any]) -> None:
    if policy.get("artifact_id") != "P2-I2-I05B-ONE-SHOT-EXECUTION-POLICY":
        raise OneShotError("wrong I05B one-shot policy")
    if policy.get("artifact_version") != "1.2.0":
        raise OneShotError("wrong I05B policy version")
    if policy.get("iteration_id") != "P2-I2-I05B" or policy.get("lane_id") != "AE01-L02":
        raise OneShotError("wrong I05B policy scope")
    attempt = policy.get("attempt_policy")
    if not isinstance(attempt, Mapping) or (
        attempt.get("max_governed_attempts") != 1
        or attempt.get("max_infrastructure_retries") != 0
        or attempt.get("consume_before_builder") is not True
        or attempt.get("claim_deletion_forbidden") is not True
        or attempt.get("claim_survives_failure_and_crash") is not True
        or attempt.get("atomic_primitive") != "os.open(O_CREAT|O_EXCL|O_WRONLY)"
    ):
        raise OneShotError("I05B attempt policy drifted")
    reconstruction = policy.get("reconstruction_policy")
    if not isinstance(reconstruction, Mapping) or (
        reconstruction.get("null_reconstruction_generation_count") != 0
        or reconstruction.get("output_readback_reconstruction_count") != 1
        or reconstruction.get("builder_invocations_per_governed_attempt") != 1
        or reconstruction.get("readback_only") is not True
    ):
        raise OneShotError("I05B reconstruction policy drifted")
    paths = policy.get("paths")
    required_paths = {
        "attempt_receipt",
        "authorization",
        "calibration_policy",
        "final_receipt",
        "governed_output",
        "machine_policy",
        "null_launch_authorization",
        "owner_acceptance",
        "parent_analysis_policy",
        "policy",
        "preregistration",
        "wrapper",
    }
    if not isinstance(paths, Mapping) or set(paths) != required_paths:
        raise OneShotError("I05B governed paths drifted")
    if policy.get("candidate_execution_authorized") is not False:
        raise OneShotError("I05B cannot authorize candidate execution")
    interpreter = policy.get("interpreter")
    if not isinstance(interpreter, Mapping) or (
        interpreter.get("executable_repo_relative") != ".venv/bin/python"
        or interpreter.get("venv_prefix_repo_relative") != ".venv"
        or interpreter.get("require_active_venv") is not True
        or interpreter.get("implementation") != "CPython"
        or interpreter.get("major_minor") != [3, 12]
    ):
        raise OneShotError("I05B active-.venv interpreter policy drifted")
    template = policy.get("normalized_command_template")
    expected_template = normalized_command(policy, "<OWNER_AUTHORIZED_FULL_HEAD>")
    if template != expected_template:
        raise OneShotError("I05B normalized command template drifted")
    claim_storage = policy.get("claim_storage")
    if not isinstance(claim_storage, Mapping) or claim_storage != {
        "atomicity_basis": "local ext4 O_CREAT|O_EXCL",
        "expected_filesystem_type": "ext4",
        "repository_local": True,
        "symlink_components_forbidden": True,
        "temporary_location_forbidden": True,
    }:
        raise OneShotError("I05B permanent claim-storage policy drifted")


def validate_preclaim_absence(policy: Mapping[str, Any]) -> None:
    paths = policy["paths"]
    attempt = _path(paths["attempt_receipt"])
    if os.path.lexists(attempt):
        raise AttemptAlreadyClaimed("I05 authorization was already consumed")
    if os.path.lexists(_path(paths["governed_output"])):
        raise OneShotError("governed I05 output already exists")
    if os.path.lexists(_path(paths["final_receipt"])):
        raise OneShotError("I05 final receipt already exists without an available claim")


def validate_claim_storage(policy: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the permanent claim location without creating the claim."""

    claim = _path(policy["paths"]["attempt_receipt"])
    if str(claim).startswith("/tmp/") or str(claim).startswith("/var/tmp/"):
        raise OneShotError("I05 claim cannot use temporary storage")
    relative_parts = claim.relative_to(ROOT).parts
    cursor = ROOT
    for part in relative_parts[:-1]:
        cursor = cursor / part
        if os.path.lexists(cursor) and cursor.is_symlink():
            raise OneShotError("I05 claim path contains a symlink component")
    ancestor = claim.parent
    while not ancestor.exists():
        ancestor = ancestor.parent
    if ancestor.is_symlink():
        raise OneShotError("I05 claim ancestor cannot be a symlink")
    completed = subprocess.run(
        ("findmnt", "-T", str(ancestor), "-n", "-o", "FSTYPE,TARGET,OPTIONS"),
        check=True,
        capture_output=True,
        text=True,
    )
    fields = completed.stdout.strip().split(maxsplit=2)
    if len(fields) != 3 or fields[0] != policy["claim_storage"]["expected_filesystem_type"]:
        raise OneShotError("I05 claim filesystem is not the frozen local filesystem")
    return {
        "atomic_primitive": policy["attempt_policy"]["atomic_primitive"],
        "claim_path": str(claim.relative_to(ROOT)),
        "filesystem_type": fields[0],
        "mount_options": fields[2],
        "mount_target": fields[1],
        "nearest_existing_ancestor": str(ancestor.relative_to(ROOT)),
        "repository_local": True,
        "symlink_components_present": False,
        "temporary_location": False,
    }


def validate_committed_authority(
    policy: Mapping[str, Any],
    expected_head: str,
    *,
    blob_reader: Callable[[str], bytes] | None = None,
) -> dict[str, str]:
    reader = blob_reader or (lambda relative: _git_bytes("show", f"{expected_head}:{relative}"))
    identities: dict[str, str] = {}
    for relative in policy["committed_authority_paths"]:
        current = _path(relative)
        if not current.is_file():
            raise OneShotError(f"required committed authority file is absent: {relative}")
        current_bytes = current.read_bytes()
        try:
            committed_bytes = reader(relative)
        except subprocess.CalledProcessError as exc:
            raise OneShotError(f"authority file is not present in runtime HEAD: {relative}") from exc
        if committed_bytes != current_bytes:
            raise OneShotError(f"working authority bytes differ from runtime HEAD: {relative}")
        identities[relative] = _sha256_bytes(current_bytes)
    return identities


def validate_frozen_hashes(policy: Mapping[str, Any]) -> dict[str, str]:
    paths = policy["paths"]
    actual = {
        "analysis_module_sha256": _sha256(
            EXPERIMENT / "scripts/p2_i2_i04r2_analysis.py"
        ),
        "authorization_sha256": _sha256(_path(paths["authorization"])),
        "calibration_entrypoint_sha256": _sha256(
            EXPERIMENT / "scripts/p2_i2_i04r2_calibration.py"
        ),
        "calibration_policy_sha256": _sha256(_path(paths["calibration_policy"])),
        "I04R2_owner_acceptance_sha256": _sha256(
            EXPERIMENT / "contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json"
        ),
        "I04R2_test_sha256": _sha256(
            EXPERIMENT / "implementation/tests/test_p2_i2_i04r2_analysis.py"
        ),
        "I04R2_validation_sha256": _sha256(
            EXPERIMENT / "contracts/p2-i2/i04r2-machine-verification-validation.json"
        ),
        "machine_policy_sha256": _sha256(_path(paths["machine_policy"])),
        "parent_analysis_policy_sha256": _sha256(_path(paths["parent_analysis_policy"])),
        "preregistration_sha256": _sha256(_path(paths["preregistration"])),
        "wrapper_sha256": _sha256(_path(paths["wrapper"])),
    }
    if actual != policy["frozen_hashes"]:
        raise OneShotError("I05B or accepted I04R2 frozen hashes drifted")
    authorization = _load(_path(paths["authorization"]))
    if authorization.get("candidate_execution_authorized") is not False:
        raise OneShotError("candidate execution became authorized")
    return actual


def validate_owner_acceptance(
    policy: Mapping[str, Any],
    *,
    policy_sha256: str,
    frozen_hashes: Mapping[str, str],
) -> dict[str, Any]:
    acceptance_path = _path(policy["paths"]["owner_acceptance"])
    if not acceptance_path.is_file():
        raise OneShotError("I05B owner acceptance/commit authority is absent")
    acceptance = _load(acceptance_path)
    expected = {
        "artifact_id": "P2-I2-I05B-OWNER-ACCEPTANCE",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I05B",
        "lane_id": "AE01-L02",
        "accepted_at": "2026-07-14",
        "acceptance_change_id": "P2-I2-CHG-022",
        "acceptance_decision_id": "P2-I2-DEC-029",
        "correction_decision_id": "P2-I2-DEC-028",
        "preclaim_correction_change_id": "P2-I2-CHG-024",
        "preclaim_correction_decision_id": "P2-I2-DEC-031",
        "owner_acceptance": True,
        "commit_authorized": True,
        "null_invocation_authorized": False,
        "authorization_sha256": frozen_hashes["authorization_sha256"],
        "wrapper_sha256": frozen_hashes["wrapper_sha256"],
        "policy_sha256": policy_sha256,
        "I04R2_hashes": {
            key: frozen_hashes[key]
            for key in (
                "analysis_module_sha256",
                "calibration_entrypoint_sha256",
                "calibration_policy_sha256",
                "I04R2_owner_acceptance_sha256",
                "I04R2_test_sha256",
                "I04R2_validation_sha256",
                "machine_policy_sha256",
                "parent_analysis_policy_sha256",
                "preregistration_sha256",
            )
        },
    }
    if acceptance != expected:
        raise OneShotError("I05B owner acceptance/commit authority is absent or drifted")
    return acceptance


def validate_null_launch_authorization(
    policy: Mapping[str, Any],
    *,
    owner_acceptance_sha256: str,
    policy_sha256: str,
    frozen_hashes: Mapping[str, str],
) -> dict[str, Any]:
    launch_path = _path(policy["paths"]["null_launch_authorization"])
    if not launch_path.is_file():
        raise OneShotError("separate I05 arithmetic-null launch authority is absent")
    launch = _load(launch_path)
    expected = {
        "artifact_id": "P2-I2-I05-NULL-LAUNCH-AUTHORIZATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I05",
        "activity_id": "P2-I2-I05-ARITHMETIC-NULL-EXECUTION",
        "lane_id": "AE01-L02",
        "authorized_at": "2026-07-14",
        "launch_change_id": "P2-I2-CHG-023",
        "launch_decision_id": "P2-I2-DEC-030",
        "preclaim_correction_change_id": "P2-I2-CHG-024",
        "preclaim_correction_decision_id": "P2-I2-DEC-031",
        "owner_acceptance_sha256": owner_acceptance_sha256,
        "null_invocation_authorized": True,
        "max_governed_attempts": 1,
        "max_infrastructure_retries": 0,
        "candidate_execution_authorized": False,
        "authorization_sha256": frozen_hashes["authorization_sha256"],
        "wrapper_sha256": frozen_hashes["wrapper_sha256"],
        "policy_sha256": policy_sha256,
        "I04R2_hashes": {
            key: frozen_hashes[key]
            for key in (
                "analysis_module_sha256",
                "calibration_entrypoint_sha256",
                "calibration_policy_sha256",
                "I04R2_owner_acceptance_sha256",
                "I04R2_test_sha256",
                "I04R2_validation_sha256",
                "machine_policy_sha256",
                "parent_analysis_policy_sha256",
                "preregistration_sha256",
            )
        },
    }
    if launch != expected:
        raise OneShotError("separate I05 arithmetic-null launch authority is absent or drifted")
    return launch


def _write_exclusive_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(
            path,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o444,
        )
    except FileExistsError as exc:
        raise AttemptAlreadyClaimed(f"exclusive path already exists: {path}") from exc
    try:
        offset = 0
        while offset < len(data):
            offset += os.write(descriptor, data[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def claim_attempt(path: Path, receipt: Mapping[str, Any]) -> None:
    """Permanently consume the one attempt through atomic exclusive creation."""

    _write_exclusive_bytes(path, pretty_json_dumps(receipt).encode("utf-8"))


def demonstrate_second_start_refused(path: Path) -> bool:
    try:
        claim_attempt(path, {"forbidden_second_claim": True})
    except AttemptAlreadyClaimed:
        return True
    raise OneShotError("second claim unexpectedly succeeded")


def preflight(
    policy: Mapping[str, Any],
    *,
    expected_head: str,
    command: Sequence[str],
    repository_snapshot: Mapping[str, Any] | None = None,
    interpreter: Mapping[str, Any] | None = None,
    blob_reader: Callable[[str], bytes] | None = None,
) -> dict[str, Any]:
    validate_policy(policy)
    validate_preclaim_absence(policy)
    claim_storage = validate_claim_storage(policy)
    snapshot = dict(repository_snapshot or collect_repository_snapshot())
    validate_repository_snapshot(snapshot, expected_head)
    identity = dict(interpreter or interpreter_identity())
    validate_interpreter(identity, policy)
    validate_command(command, policy, expected_head)
    committed = validate_committed_authority(
        policy,
        expected_head,
        blob_reader=blob_reader,
    )
    frozen = validate_frozen_hashes(policy)
    policy_sha = _sha256(_path(policy["paths"]["policy"]))
    acceptance = validate_owner_acceptance(
        policy,
        policy_sha256=policy_sha,
        frozen_hashes=frozen,
    )
    acceptance_sha = _sha256(_path(policy["paths"]["owner_acceptance"]))
    launch = validate_null_launch_authorization(
        policy,
        owner_acceptance_sha256=acceptance_sha,
        policy_sha256=policy_sha,
        frozen_hashes=frozen,
    )
    return {
        "claim_storage": claim_storage,
        "committed_authority_sha256": committed,
        "expected_and_actual_head": expected_head,
        "frozen_hashes": frozen,
        "interpreter": identity,
        "normalized_command": list(command),
        "null_launch_authorization": launch,
        "null_launch_authorization_sha256": _sha256(
            _path(policy["paths"]["null_launch_authorization"])
        ),
        "owner_acceptance_sha256": acceptance_sha,
        "policy_sha256": policy_sha,
        "repository_state": {
            "index_clean": snapshot["index_clean"],
            "porcelain": snapshot["porcelain"],
            "worktree_clean": snapshot["worktree_clean"],
        },
        "owner_acceptance": acceptance,
    }


def _invoke_accepted_builder_once(
    policy: Mapping[str, Any],
    *,
    before_builder: Callable[[], None],
) -> dict[str, Any]:
    """Import and call the immutable accepted I04R2 builder exactly once."""

    from p2_i2_i04r2_calibration import (  # noqa: PLC0415
        build_calibration_record,
        validate_execution_authorization,
    )

    paths = policy["paths"]
    parent_path = _path(paths["parent_analysis_policy"])
    machine_path = _path(paths["machine_policy"])
    calibration_path = _path(paths["calibration_policy"])
    preregistration_path = _path(paths["preregistration"])
    authorization = _load(_path(paths["authorization"]))
    parent = _load(parent_path)
    machine = _load(machine_path)
    calibration = _load(calibration_path)
    validate_execution_authorization(
        authorization,
        parent_analysis_path=parent_path,
        machine_policy_path=machine_path,
        calibration_path=calibration_path,
        preregistration_path=preregistration_path,
    )
    before_builder()
    return build_calibration_record(
        calibration,
        machine,
        parent,
        parent_analysis_path=parent_path,
        machine_policy_path=machine_path,
        calibration_path=calibration_path,
    )


def _final_receipt(
    *,
    policy: Mapping[str, Any],
    claim_sha256: str,
    status: str,
    builder_invocations: int,
    readbacks: int,
    second_refused: bool,
    output_sha256: str | None,
    failure: str | None,
) -> dict[str, Any]:
    return {
        "artifact_id": "P2-I2-I05B-FINAL-RECEIPT",
        "artifact_version": "1.0.0",
        "accepted_builder_invocation_count": builder_invocations,
        "authorization_consumed": True,
        "builder_invocation_count": builder_invocations,
        "candidate_execution_authorized": False,
        "claim_receipt_sha256": claim_sha256,
        "failure": failure,
        "governed_attempt_count": 1,
        "iteration_id": "P2-I2-I05B",
        "lane_id": "AE01-L02",
        "null_invocation_count": builder_invocations,
        "null_reconstruction_generation_count": 0,
        "output_readback_reconstruction_count": readbacks,
        "output_sha256": output_sha256,
        "second_invocation_refused": second_refused,
        "status": status,
        "infrastructure_retries": 0,
        "scientific_result": False,
        "policy_id": policy["artifact_id"],
    }


def governed_run(
    policy: Mapping[str, Any],
    expected_head: str,
    command: Sequence[str],
) -> dict[str, Any]:
    preflight_receipt = preflight(
        policy,
        expected_head=expected_head,
        command=command,
    )
    paths = policy["paths"]
    claim_path = _path(paths["attempt_receipt"])
    final_path = _path(paths["final_receipt"])
    output_path = _path(paths["governed_output"])
    claim = {
        "artifact_id": "P2-I2-I05B-ATTEMPT-CLAIM",
        "artifact_version": "1.0.0",
        "authorization_consumed": True,
        "candidate_execution_authorized": False,
        "claim_deletion_forbidden": True,
        "claim_state": "consumed_before_builder",
        "infrastructure_retries_authorized": 0,
        "iteration_id": "P2-I2-I05B",
        "lane_id": "AE01-L02",
        "max_governed_attempts": 1,
        "preflight": preflight_receipt,
        "scientific_result": False,
    }
    claim_attempt(claim_path, claim)
    claim_sha = _sha256(claim_path)

    builder_invocations = 0
    readbacks = 0
    output_sha: str | None = None
    try:
        if output_path.exists():
            raise OneShotError("governed output appeared after claim and before builder")
        def mark_builder_invoked() -> None:
            nonlocal builder_invocations
            if builder_invocations != 0:
                raise OneShotError("accepted builder invocation counter drifted")
            builder_invocations = 1

        record = _invoke_accepted_builder_once(
            policy,
            before_builder=mark_builder_invoked,
        )
        serialized = pretty_json_dumps(record)
        _write_exclusive_bytes(output_path, serialized.encode("utf-8"))
        retained_text = output_path.read_text(encoding="utf-8")
        readbacks = 1
        reconstructed = json.loads(retained_text)
        if pretty_json_dumps(reconstructed) != retained_text or retained_text != serialized:
            raise OneShotError("retained I05 output failed byte reconstruction")
        output_sha = _sha256(output_path)
        second_refused = demonstrate_second_start_refused(claim_path)
        final = _final_receipt(
            policy=policy,
            claim_sha256=claim_sha,
            status="completed",
            builder_invocations=builder_invocations,
            readbacks=readbacks,
            second_refused=second_refused,
            output_sha256=output_sha,
            failure=None,
        )
        _write_exclusive_bytes(final_path, pretty_json_dumps(final).encode("utf-8"))
        return final
    except BaseException as exc:
        second_refused = demonstrate_second_start_refused(claim_path)
        final = _final_receipt(
            policy=policy,
            claim_sha256=claim_sha,
            status="failed_after_claim",
            builder_invocations=builder_invocations,
            readbacks=readbacks,
            second_refused=second_refused,
            output_sha256=output_sha,
            failure=f"{type(exc).__name__}: {exc}",
        )
        if not final_path.exists():
            _write_exclusive_bytes(final_path, pretty_json_dumps(final).encode("utf-8"))
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True)
    parser.add_argument("--expected-head", required=True)
    args = parser.parse_args()
    policy = _load(_path(args.policy))
    if args.policy != policy.get("paths", {}).get("policy"):
        raise OneShotError("policy argument is not the exact normalized policy path")
    if Path.cwd().resolve() != ROOT.resolve():
        raise OneShotError("governed I05 command must run from repository root")
    actual_command = [
        policy["interpreter"]["executable_repo_relative"],
        policy["paths"]["wrapper"],
        *sys.argv[1:],
    ]
    final = governed_run(policy, args.expected_head, actual_command)
    sys.stdout.write(pretty_json_dumps(final))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
