"""One-shot launcher for the P2-I3 B-R arithmetic calibration.

The launcher is inert without a committed owner launch authorization.  It
creates a permanent exclusive claim before importing or calling the builder.
"""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Callable, Mapping


def _find_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _find_root()
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import (  # noqa: E402
    ContractError,
    digest_file,
    load_json,
    pretty_json_dumps,
    validate_portable_path,
)


POLICY_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i3_br_i05_one_shot_policy.json"
FREEZE_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-invocation-freeze.json"
I04_POLICY_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i3_br_i04_machine_policy.json"
I04_SCHEMA_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i04-br-machine-records.schema.json"
I05_SCHEMA_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-output.schema.json"
METRIC_SHEET_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/metric-sheets/AE01-L03.json"
BUILDER_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_calibration.py"
VALIDATOR_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_freeze_validate.py"
WRAPPER_PATH = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_one_shot.py"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def _load_relative(path: str) -> dict[str, Any]:
    validate_portable_path(path)
    value = load_json(ROOT / path)
    _require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def _committed_file_digest(head: str, relative: str) -> str:
    blob = subprocess.run(
        ("git", "show", f"{head}:{relative}"),
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()


def _assert_no_symlink_components(path: Path) -> None:
    current = ROOT
    for part in path.absolute().relative_to(ROOT.resolve()).parts:
        current = current / part
        if current.is_symlink():
            raise ContractError(f"symlink output component forbidden: {_relative(current)}")


def _exclusive_write(path: Path, value: Mapping[str, Any]) -> bytes:
    _assert_no_symlink_components(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = pretty_json_dumps(value).encode("utf-8")
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        raise
    parent_descriptor = os.open(
        path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    )
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)
    return payload


def _checkpoint(
    fault_injector: Callable[[str], None] | None, boundary: str
) -> None:
    if fault_injector is not None:
        fault_injector(boundary)


def _process_environment(policy: Mapping[str, Any]) -> dict[str, str]:
    required = policy["environment"]["required_process_environment"]
    actual = {name: os.environ.get(name) for name in required}
    _require(actual == required, "deterministic process environment drifted")
    return dict(required)


def _interpreter_facts(policy: Mapping[str, Any]) -> dict[str, Any]:
    environment = policy["environment"]
    venv = (ROOT / ".venv").resolve()
    _require(Path(sys.prefix).resolve() == venv, "active interpreter is not repository .venv")
    _require(sys.prefix != sys.base_prefix, "system interpreter is forbidden")
    _require(platform.python_version() == environment["python"], "Python version drifted")
    _require(version("jsonschema") == environment["jsonschema"], "jsonschema version drifted")
    _require(version("pytest") == environment["pytest"], "pytest version drifted")
    binary_digest = digest_file(Path(sys.executable).resolve())
    _require(binary_digest == environment["interpreter_binary_sha256"], "interpreter digest drifted")
    _process_environment(policy)
    return {
        "binary_sha256": binary_digest,
        "command": environment["interpreter_command"],
        "implementation": platform.python_implementation(),
        "jsonschema": version("jsonschema"),
        "pytest": version("pytest"),
        "version": platform.python_version(),
    }


def _schema_validator() -> Any:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    i04_schema = _load_relative(I04_SCHEMA_PATH)
    i05_schema = _load_relative(I05_SCHEMA_PATH)
    registry = Registry().with_resource(
        i04_schema["$id"], Resource.from_contents(i04_schema)
    )
    return Draft202012Validator(i05_schema, registry=registry)


def validate_preclaim(
    *, policy_path: Path, activation_path: Path, expected_head: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str], list[str], dict[str, Any], str]:
    policy_relative = _relative(policy_path)
    activation_relative = _relative(activation_path)
    _require(policy_relative == POLICY_PATH, "policy path drifted")
    policy = _load_relative(policy_relative)
    _require(policy["artifact_id"] == "P2-I3-I05-BR-ONE-SHOT-POLICY", "policy ID drifted")
    _require(policy["governed_invocation"]["calibration_invocation_authorized"] is False, "policy cannot self-authorize")
    _require(policy["candidate_blindness"]["candidate_execution_authorized"] is False, "candidate execution forbidden")
    _require(len(expected_head) == 40 and all(c in "0123456789abcdef" for c in expected_head), "full lowercase expected HEAD required")
    _require(_git("rev-parse", "HEAD") == expected_head, "launch HEAD drifted")
    _require(_git("status", "--porcelain=v1", "--untracked-files=all") == "", "launch worktree must be clean")
    _require(_git("merge-base", "--is-ancestor", policy["authority"]["accepted_i04_source_anchor"], expected_head) == "", "I04 source anchor is not an ancestor")

    activation = _load_relative(activation_relative)
    _require(activation_relative in policy["committed_authority_paths"], "activation path is not frozen")
    _schema_validator().validate(activation)
    expected_activation_fields = {
        "artifact_id": "P2-I3-I05-BR-CALIBRATION-LAUNCH-AUTHORIZATION",
        "artifact_version": "1.0.2",
        "attempt_claim_path": policy["outputs"]["attempt_claim"],
        "branch_id": "P2-I3-BR",
        "calibration_invocation_authorized": True,
        "candidate_execution_authorized": False,
        "freeze_artifact_id": "P2-I3-I05-BR-CALIBRATION-INVOCATION-FREEZE",
        "governed_invocations_authorized": 1,
        "governed_paths": policy["outputs"],
        "iteration_id": "P2-I3-I05",
        "lane_id": "AE01-L03",
        "launch_head_binding_method": "runtime_expected_head_verified_clean_and_retained_in_claim_and_receipt",
        "normalized_command_prefix": policy["normalized_command_template"][:-1],
        "owner_accepted_freeze": True,
    }
    _require(
        set(activation) == set(expected_activation_fields)
        | {
            "accepted_freeze_commit",
            "authority_sha256",
            "freeze_sha256",
            "interpreter_environment",
        },
        "launch authorization shape drifted",
    )
    _require(
        all(activation.get(key) == value for key, value in expected_activation_fields.items()),
        "launch authorization values drifted",
    )
    accepted_freeze_commit = activation.get("accepted_freeze_commit")
    _require(
        isinstance(accepted_freeze_commit, str)
        and len(accepted_freeze_commit) == 40
        and all(c in "0123456789abcdef" for c in accepted_freeze_commit),
        "launch authorization requires a full accepted-freeze commit",
    )
    _git("merge-base", "--is-ancestor", accepted_freeze_commit, expected_head)
    freeze_sha256 = digest_file(ROOT / FREEZE_PATH)
    _require(activation.get("freeze_sha256") == freeze_sha256, "accepted freeze digest drifted")
    _require(
        _committed_file_digest(accepted_freeze_commit, FREEZE_PATH) == freeze_sha256,
        "accepted freeze commit does not contain the active freeze bytes",
    )

    current_hashes: dict[str, str] = {}
    for relative in policy["committed_authority_paths"]:
        validate_portable_path(relative)
        path = ROOT / relative
        _require(path.is_file(), f"committed authority missing: {relative}")
        current = digest_file(path)
        committed = _committed_file_digest(expected_head, relative)
        _require(current == committed, f"authority is not byte-identical to HEAD: {relative}")
        current_hashes[relative] = current

    expected_authority_sha256 = {
        "builder": current_hashes[BUILDER_PATH],
        "freeze": current_hashes[FREEZE_PATH],
        "output_schema": current_hashes[I05_SCHEMA_PATH],
        "policy": current_hashes[POLICY_PATH],
        "validator": current_hashes[VALIDATOR_PATH],
        "wrapper": current_hashes[WRAPPER_PATH],
    }
    _require(
        activation.get("authority_sha256") == expected_authority_sha256,
        "launch authorization source identities drifted",
    )

    freeze = _load_relative(FREEZE_PATH)
    source_hashes = freeze["source_hashes"]
    for name, binding in source_hashes.items():
        _require(digest_file(ROOT / binding["path"]) == binding["sha256"], f"frozen source hash drifted: {name}")

    expected_command = [
        policy["environment"]["interpreter_command"],
        policy["normalized_command_template"][1],
        "--policy",
        policy_relative,
        "--activation",
        activation_relative,
        "--expected-head",
        expected_head,
    ]
    actual_command = [policy["environment"]["interpreter_command"], *sys.argv]
    _require(actual_command == expected_command, "normalized launch command drifted")
    interpreter = _interpreter_facts(policy)
    expected_activation_environment = {
        "binary_sha256": interpreter["binary_sha256"],
        "command": interpreter["command"],
        "jsonschema": interpreter["jsonschema"],
        "process_environment": _process_environment(policy),
        "pytest": interpreter["pytest"],
        "python": interpreter["version"],
    }
    _require(
        activation.get("interpreter_environment") == expected_activation_environment,
        "launch authorization environment drifted",
    )
    return policy, interpreter, current_hashes, expected_command, activation, activation_relative


def validate_postclaim(
    *,
    policy: Mapping[str, Any],
    expected_head: str,
    current_hashes: Mapping[str, str],
    activation_relative: str,
    activation_sha256: str,
    claim_sha256: str,
) -> None:
    """Close the preflight/import TOCTOU window after permanent consumption."""

    claim_relative = policy["outputs"]["attempt_claim"]
    _require(_git("rev-parse", "HEAD") == expected_head, "post-claim HEAD drifted")
    _require(
        _git("status", "--porcelain=v1", "--untracked-files=all")
        == f"?? {claim_relative}",
        "post-claim worktree changed beyond the exact permanent claim",
    )
    _require(digest_file(ROOT / claim_relative) == claim_sha256, "post-claim bytes drifted")
    _require(
        digest_file(ROOT / activation_relative) == activation_sha256,
        "post-claim activation bytes drifted",
    )
    for relative, expected_digest in current_hashes.items():
        _require(digest_file(ROOT / relative) == expected_digest, f"post-claim authority drifted: {relative}")
        _require(
            _committed_file_digest(expected_head, relative) == expected_digest,
            f"post-claim authority no longer matches launch HEAD: {relative}",
        )
    _interpreter_facts(policy)
    for name, relative in policy["outputs"].items():
        if name != "attempt_claim":
            _require(not os.path.lexists(ROOT / relative), f"post-claim governed path appeared: {name}")


def validate_consumable_closeout(
    *,
    policy: Mapping[str, Any],
    receipt: Mapping[str, Any] | None,
    claim_sha256: str,
    activation_sha256: str,
    output_sha256: Mapping[str, str],
) -> None:
    """Fail closed unless the completed receipt admits these exact output bytes."""

    _require(receipt is not None, "missing final receipt quarantines calibration outputs")
    _require(receipt.get("completion_status") == "success", "failed final receipt quarantines calibration outputs")
    _require(receipt.get("attempt_consumed") is True, "receipt does not consume the attempt")
    _require(receipt.get("case_count") == 5, "receipt case count drifted")
    _require(receipt.get("entered_margin_count") == 10, "receipt entered-margin count drifted")
    _require(receipt.get("calibrated_relation_ids") == ["m_trace", "m_export"], "receipt relation coverage drifted")
    _require(receipt.get("claim_sha256") == claim_sha256, "receipt claim digest drifted")
    _require(receipt.get("activation_sha256") == activation_sha256, "receipt activation digest drifted")
    _require(receipt.get("schema_validation") == "passed", "schema validation did not pass")
    _require(receipt.get("semantic_validation") == "passed", "semantic validation did not pass")
    _require(
        receipt.get("readback_validation") == "passed_exact_bytes_canonical_json_and_semantics",
        "readback validation did not pass",
    )
    bindings = receipt.get("output_bindings", {})
    for name in ("matched_null", "metric_calibration", "frozen_metric_sheet"):
        _require(bindings.get(name, {}).get("path") == policy["outputs"][name], f"receipt output path drifted: {name}")
        _require(bindings.get(name, {}).get("sha256") == output_sha256[name], f"receipt output digest drifted: {name}")


def run_once(
    *,
    policy_path: Path,
    activation_path: Path,
    expected_head: str,
    _fault_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    policy, interpreter, current_hashes, command, activation, activation_relative = validate_preclaim(
        policy_path=policy_path,
        activation_path=activation_path,
        expected_head=expected_head,
    )
    outputs = {name: ROOT / relative for name, relative in policy["outputs"].items()}
    for name, path in outputs.items():
        _require(not path.lexists() if hasattr(path, "lexists") else not os.path.lexists(path), f"governed path already exists: {name}")
    _checkpoint(_fault_injector, "after_preflight_before_claim")

    freeze_sha256 = digest_file(ROOT / FREEZE_PATH)
    activation_sha256 = digest_file(ROOT / activation_relative)
    claim = {
        "artifact_id": "P2-I3-I05-BR-ATTEMPT-CLAIM",
        "artifact_version": "1.0.2",
        "accepted_freeze_commit": activation["accepted_freeze_commit"],
        "accepted_freeze_sha256": freeze_sha256,
        "activation": {
            "artifact_id": activation["artifact_id"],
            "path": activation_relative,
            "sha256": activation_sha256,
        },
        "authorization_consumed": True,
        "bound_source_sha256": {
            "builder": current_hashes["experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_calibration.py"],
            "freeze": freeze_sha256,
            "output_schema": current_hashes[I05_SCHEMA_PATH],
            "policy": current_hashes[POLICY_PATH],
            "validator": current_hashes[VALIDATOR_PATH],
            "wrapper": current_hashes[WRAPPER_PATH],
        },
        "builder_invocation_ceiling": 1,
        "candidate_execution_authorized": False,
        "claim_id": "P2-I3-I05-BR-ATTEMPT-1",
        "creation_disposition": "exclusive_pre_builder_attempt_consumption",
        "governed_attempt": 1,
        "infrastructure_retries": 0,
        "interpreter": interpreter,
        "launch_head": expected_head,
        "normalized_command": command,
        "output_paths": policy["outputs"],
        "process_environment": _process_environment(policy),
    }
    output_validator = _schema_validator()
    output_validator.validate(claim)
    claim_payload = _exclusive_write(outputs["attempt_claim"], claim)
    claim_sha256 = hashlib.sha256(claim_payload).hexdigest()
    _checkpoint(_fault_injector, "after_claim")
    validate_postclaim(
        policy=policy,
        expected_head=expected_head,
        current_hashes=current_hashes,
        activation_relative=activation_relative,
        activation_sha256=activation_sha256,
        claim_sha256=claim_sha256,
    )
    _checkpoint(_fault_injector, "after_postclaim_revalidation")
    _checkpoint(_fault_injector, "before_builder_import")

    # Import only after the permanent claim has consumed the single attempt.
    from p2_i3_i05_br_calibration import (  # noqa: PLC0415
        build_calibration_outputs,
        validate_calibration_outputs,
    )
    _checkpoint(_fault_injector, "after_builder_import")

    source_metric_sheet_sha256 = digest_file(ROOT / METRIC_SHEET_PATH)
    built = build_calibration_outputs(
        i04_policy=_load_relative(I04_POLICY_PATH),
        metric_sheet=_load_relative(METRIC_SHEET_PATH),
        source_metric_sheet_sha256=source_metric_sheet_sha256,
    )
    _checkpoint(_fault_injector, "after_builder_calculation")
    i04_policy = _load_relative(I04_POLICY_PATH)
    metric_sheet = _load_relative(METRIC_SHEET_PATH)
    validate_calibration_outputs(
        built,
        i04_policy=i04_policy,
        metric_sheet=metric_sheet,
        source_metric_sheet_sha256=source_metric_sheet_sha256,
    )
    for value in built.values():
        output_validator.validate(value)
    _checkpoint(_fault_injector, "after_in_memory_validation")
    payloads: dict[str, bytes] = {}
    for name in ("matched_null", "metric_calibration", "frozen_metric_sheet"):
        payloads[name] = _exclusive_write(outputs[name], built[name])
        _checkpoint(_fault_injector, f"after_{name}_write")
    readback_hashes: dict[str, str] = {}
    readback_bundle: dict[str, dict[str, Any]] = {}
    for name, payload in payloads.items():
        path = outputs[name]
        retained = path.read_bytes()
        readback = json.loads(retained)
        output_validator.validate(readback)
        readback_bundle[name] = readback
        reconstructed = pretty_json_dumps(readback).encode("utf-8")
        _require(retained == payload == reconstructed, f"readback reconstruction failed: {name}")
        readback_hashes[name] = hashlib.sha256(retained).hexdigest()
    validate_calibration_outputs(
        readback_bundle,
        i04_policy=i04_policy,
        metric_sheet=metric_sheet,
        source_metric_sheet_sha256=source_metric_sheet_sha256,
    )
    _checkpoint(_fault_injector, "after_readback_validation")

    second_start_refused = False
    try:
        _exclusive_write(outputs["attempt_claim"], claim)
    except FileExistsError:
        second_start_refused = True
    _require(second_start_refused, "second start was not refused")
    _require(digest_file(outputs["attempt_claim"]) == claim_sha256, "second-start check changed claim bytes")
    _checkpoint(_fault_injector, "after_second_start_refusal")

    receipt = {
        "artifact_id": "P2-I3-I05-BR-FINAL-RECEIPT",
        "artifact_version": "1.0.2",
        "activation_artifact_id": activation["artifact_id"],
        "activation_sha256": activation_sha256,
        "attempt_consumed": True,
        "builder_invocation_count": 1,
        "case_count": built["matched_null"]["case_count"],
        "calibrated_relation_ids": built["metric_calibration"]["calibrated_relation_ids"],
        "candidate_execution_authorized": False,
        "claim_id": claim["claim_id"],
        "claim_sha256": claim_sha256,
        "completion_status": "success",
        "delta": built["metric_calibration"]["delta"],
        "entered_margin_count": built["metric_calibration"]["entered_margin_count"],
        "launch_head": expected_head,
        "output_bindings": {
            name: {"path": policy["outputs"][name], "sha256": readback_hashes[name]}
            for name in ("matched_null", "metric_calibration", "frozen_metric_sheet")
        },
        "readback_validation": "passed_exact_bytes_canonical_json_and_semantics",
        "response_record_count": built["matched_null"]["response_record_count"],
        "schema_validation": "passed",
        "scientific_result": False,
        "second_start_evidence": {
            "attempted": True,
            "claim_sha256_unchanged": True,
            "refusal_reason": "attempt_claim_exists",
            "refused": True,
        },
        "semantic_validation": "passed",
        "triplet_count": built["matched_null"]["case_count"],
    }
    output_validator.validate(receipt)
    validate_consumable_closeout(
        policy=policy,
        receipt=receipt,
        claim_sha256=claim_sha256,
        activation_sha256=activation_sha256,
        output_sha256=readback_hashes,
    )
    _checkpoint(_fault_injector, "before_final_receipt")
    _exclusive_write(outputs["final_receipt"], receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--activation", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    arguments = parser.parse_args()
    receipt = run_once(
        policy_path=arguments.policy,
        activation_path=arguments.activation,
        expected_head=arguments.expected_head,
    )
    print(pretty_json_dumps(receipt), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
