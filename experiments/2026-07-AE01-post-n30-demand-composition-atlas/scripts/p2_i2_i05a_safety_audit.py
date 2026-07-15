"""Static, zero-execution audit of the proposed P2-I2 I05 authority path."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402


ENTRYPOINT = EXPERIMENT / "scripts/p2_i2_i04r2_calibration.py"
POLICY = EXPERIMENT / "configs/p2_i2_i04r2_calibration_policy.json"
AUTHORIZATION = EXPERIMENT / "contracts/p2-i2/i05-calibration-execution-freeze.json"
AUTH_VALIDATOR = EXPERIMENT / "scripts/p2_i2_i05_authorization_validate.py"
GOVERNED_OUTPUT = (
    EXPERIMENT
    / "outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json"
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def _main_calls(source: str) -> list[str]:
    tree = ast.parse(source, filename=str(ENTRYPOINT))
    main = next(
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "main"
    )
    calls: list[str] = []
    for node in ast.walk(main):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            calls.append(node.func.attr)
    return calls


def _check(
    check_id: str,
    name: str,
    passed: bool,
    finding: str,
    evidence: Any,
    blocker: str | None = None,
) -> dict[str, Any]:
    return {
        "acceptance_blocker": blocker if not passed else None,
        "check_id": check_id,
        "evidence": evidence,
        "finding": finding,
        "name": name,
        "status": "passed" if passed else "failed",
    }


def audit() -> dict[str, Any]:
    source = ENTRYPOINT.read_text(encoding="utf-8")
    auth_source = AUTH_VALIDATOR.read_text(encoding="utf-8")
    policy = _load(POLICY)
    authorization = _load(AUTHORIZATION)
    calls = _main_calls(source)
    execution_policy = policy["execution_policy"]

    has_consumption_surface = any(
        token in source
        for token in (
            "consumption_receipt",
            "authorization_consumed",
            "attempt_receipt",
            "consume_authorization",
        )
    )
    checks = [
        _check(
            "SAFE-01",
            "attempt-time single-use consumption",
            has_consumption_surface
            and source.find("authorization_consumed")
            < source.find("build_calibration_record"),
            "the current entry point validates a reusable JSON freeze but never consumes a separate attempt token before governed work",
            {
                "build_call_count_in_main": calls.count("build_calibration_record"),
                "consumption_surface_present": has_consumption_surface,
                "governed_invocations_authorized": authorization[
                    "governed_invocations_authorized"
                ],
            },
            "a crash or assertion failure leaves the same authorization reusable",
        ),
        _check(
            "SAFE-02",
            "atomic concurrent-start exclusion",
            ("O_EXCL" in source or "flock" in source or "lockf" in source)
            and has_consumption_surface,
            "output existence is checked before work, but no exclusive claim/lock atomically consumes permission",
            {
                "output_exists_check_count": calls.count("exists"),
                "exclusive_create_or_lock_present": any(
                    token in source for token in ("O_EXCL", "flock", "lockf")
                ),
                "output_write_count": calls.count("write_text"),
            },
            "two concurrent processes can both observe absent output and begin",
        ),
        _check(
            "SAFE-03",
            "failed-attempt and retry semantics",
            has_consumption_surface
            and execution_policy["max_infrastructure_retries"] == 0,
            "the policy freezes one infrastructure retry but defines no consumed-attempt identity or retry token distinct from the one governed invocation",
            {
                "max_governed_invocations": execution_policy[
                    "max_governed_invocations"
                ],
                "max_infrastructure_retries": execution_policy[
                    "max_infrastructure_retries"
                ],
                "attempt_consumption_present": has_consumption_surface,
            },
            "one attempted execution is not mechanically distinguished from an unregistered retry",
        ),
        _check(
            "SAFE-04",
            "committed I05 authority and immediate preflight binding",
            "ACCEPTED_I05_COMMIT" in auth_source
            and "status --short" in auth_source
            and "sys.executable" in auth_source
            and "execution_command_sha256" in auth_source,
            "the current validator binds accepted I04 commit b7b008c only; it does not bind a future commit containing I05 acceptance/freeze, interpreter/command identity, or clean authority files",
            {
                "accepted_I04_commit_bound": "ACCEPTED_I04_COMMIT" in auth_source,
                "accepted_I05_commit_bound": "ACCEPTED_I05_COMMIT" in auth_source,
                "clean_RCAE_authority_check": "status --short" in auth_source,
                "execution_command_digest_check": "execution_command_sha256" in auth_source,
                "python_executable_check": "sys.executable" in auth_source,
            },
            "validation-to-execution drift remains possible after the I05 commit",
        ),
        _check(
            "SAFE-05",
            "existing identity/output/candidate guards",
            calls.count("validate_execution_authorization") == 1
            and calls.count("exists") >= 1
            and authorization["candidate_execution_authorized"] is False,
            "the entry point does validate I04R2 identities, reject an existing governed output, and keep candidate authority false",
            {
                "authorization_validation_calls": calls.count(
                    "validate_execution_authorization"
                ),
                "candidate_execution_authorized": authorization[
                    "candidate_execution_authorized"
                ],
                "governed_output_absent": not GOVERNED_OUTPUT.exists(),
            },
        ),
        _check(
            "SAFE-06",
            "readback-only reconstruction within the governed call",
            calls.count("build_calibration_record") == 1
            and calls.count("write_text") == 1
            and calls.count("read_text") == 1
            and calls.count("loads") == 1,
            "the current main path builds once, writes once, then reconstructs by retained-output read/parse/reserialize without a second null generation",
            {
                "build_calls": calls.count("build_calibration_record"),
                "json_loads_calls": calls.count("loads"),
                "readback_calls": calls.count("read_text"),
                "write_calls": calls.count("write_text"),
            },
        ),
        _check(
            "SAFE-07",
            "retained attempt/reconstruction/refusal accounting",
            all(
                field in source
                for field in (
                    "null_invocation_count",
                    "null_reconstruction_generation_count",
                    "output_readback_reconstruction_count",
                    "authorization_consumed",
                    "second_invocation_refused",
                )
            ),
            "the entry point emits the calibration record only; it retains no consumption receipt, separate counts, or second-invocation refusal witness",
            {
                field: field in source
                for field in (
                    "authorization_consumed",
                    "null_invocation_count",
                    "null_reconstruction_generation_count",
                    "output_readback_reconstruction_count",
                    "second_invocation_refused",
                )
            },
            "the required post-run safety facts cannot be reconstructed from retained machine records",
        ),
        _check(
            "SAFE-08",
            "zero-execution audit boundary",
            not GOVERNED_OUTPUT.exists(),
            "I05A parsed source and contracts only; no governed output exists",
            {
                "candidate_or_control_invocations": 0,
                "governed_null_invocations": 0,
                "governed_output_absent": True,
                "PyGRC_model_instantiations": 0,
                "reconstruction_generations": 0,
            },
        ),
    ]
    failed = [check for check in checks if check["status"] == "failed"]
    return {
        "artifact_id": "P2-I2-I05A-EXECUTION-SAFETY-AUDIT",
        "artifact_version": "1.0.0",
        "checks": checks,
        "disposition": {
            "acceptance_ready": not failed,
            "active_I05_invocation_authority": False,
            "proposed_DEC_027": "blocked_pending_execution_safety_correction"
            if failed
            else "ready_for_owner_review",
            "source_correction_performed": False,
        },
        "execution_receipt": {
            "candidate_or_control_invocations": 0,
            "governed_null_invocations": 0,
            "PyGRC_model_instantiations": 0,
            "reconstruction_generations": 0,
            "scientific_result": False,
        },
        "failed_checks": len(failed),
        "input_identities": {
            "authorization_sha256": _sha256(AUTHORIZATION),
            "authorization_validator_sha256": _sha256(AUTH_VALIDATOR),
            "calibration_entrypoint_sha256": _sha256(ENTRYPOINT),
            "calibration_policy_sha256": _sha256(POLICY),
        },
        "iteration_id": "P2-I2-I05A",
        "lane_id": "AE01-L02",
        "passed_checks": len(checks) - len(failed),
        "total_checks": len(checks),
        "validator": {
            "path": str(Path(__file__).relative_to(ROOT)),
            "sha256": _sha256(Path(__file__)),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise AssertionError(f"refusing to overwrite audit result: {args.output}")
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(pretty_json_dumps(result), encoding="utf-8")
    print(
        f"P2-I2 I05A safety audit: {result['passed_checks']}/"
        f"{result['total_checks']} passed; {result['failed_checks']} blockers; "
        "governed invocations=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
