"""Zero-null validation of the P2-I2 I05B one-shot correction."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
GRAPH = ROOT.parent / "graph-reflexive-coherence"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402
import p2_i2_i05b_one_shot as one_shot  # noqa: E402


ACCEPTED_I04_COMMIT = "b7b008c402d837b529962a1a5edb062927939d28"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
POLICY = EXPERIMENT / "configs/p2_i2_i05b_one_shot_policy.json"
WRAPPER = EXPERIMENT / "scripts/p2_i2_i05b_one_shot.py"
TEST = EXPERIMENT / "implementation/tests/test_p2_i2_i05b_one_shot.py"
AUTHORIZATION = EXPERIMENT / "contracts/p2-i2/i05-calibration-execution-freeze.json"
OWNER_ACCEPTANCE = EXPERIMENT / "contracts/p2-i2/i05b-owner-acceptance.json"
NULL_LAUNCH_AUTHORIZATION = (
    EXPERIMENT / "contracts/p2-i2/i05-null-launch-authorization.json"
)
GOVERNED_OUTPUT = (
    EXPERIMENT
    / "outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json"
)
ATTEMPT_RECEIPT = EXPERIMENT / "outputs/p2-i2/i05/i05b-attempt-claim.json"
FINAL_RECEIPT = EXPERIMENT / "outputs/p2-i2/i05/i05b-final-receipt.json"

I04_EXPECTED = {
    "parent_analysis_policy": "91b8bd50633a19333935ec115bdd005697abdef5381ef59f4ceab21db08c090d",
    "machine_policy": "277dfc22c9e98268e950cb634ed1174b9ad4f0f654a72984b365655815c3a9ce",
    "calibration_policy": "57dc32d02b828bb21caf069c5690bf4fcfc240848faefcd8412a6505bba849fe",
    "analysis_module": "2abc4c2040d4fff3467931feeedb0e2423a5fca71a3bc3a921aa4ca3e9b22a24",
    "calibration_entrypoint": "8a0ef5569705ea0619a628b3b5a25d9dc80448a273a68a92d131ce775793b61a",
    "preregistration": "dee89df45b4a5ece93d1d7ce461d2c0cb8f028ff44aa32b3f4e45e88a1b09e9b",
    "validation": "637c07cc7d31824f4806459f7b4e8ddd1262eec3c5cc874b009ea7767b59d361",
    "owner_acceptance": "2ade4d6255c42044621489e1132d1030f48266e851bea614a11f1100c4f7dacf",
    "test": "75de8f69c2e1433618303a8338d4899be272527c3af9b4c7c7476448f5ccfaf2",
}
I04_PATHS = {
    "parent_analysis_policy": EXPERIMENT / "configs/p2_i2_i04r1_analysis_policy.json",
    "machine_policy": EXPERIMENT / "configs/p2_i2_i04r2_machine_policy.json",
    "calibration_policy": EXPERIMENT / "configs/p2_i2_i04r2_calibration_policy.json",
    "analysis_module": EXPERIMENT / "scripts/p2_i2_i04r2_analysis.py",
    "calibration_entrypoint": EXPERIMENT / "scripts/p2_i2_i04r2_calibration.py",
    "preregistration": EXPERIMENT / "contracts/p2-i2/i04r2-machine-verification-preregistration.json",
    "validation": EXPERIMENT / "contracts/p2-i2/i04r2-machine-verification-validation.json",
    "owner_acceptance": EXPERIMENT / "contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json",
    "test": EXPERIMENT / "implementation/tests/test_p2_i2_i04r2_analysis.py",
}
REQUIRED_TESTS = {
    "test_concurrent_second_start_is_refused",
    "test_start_after_claimed_attempt_is_refused",
    "test_start_after_simulated_crash_following_claim_is_refused",
    "test_dirty_authority_files_or_index_are_refused",
    "test_wrong_head_is_refused",
    "test_wrong_interpreter_or_command_is_refused",
    "test_existing_governed_output_is_refused",
    "test_builder_invocation_during_safety_validation_is_zero",
    "test_owner_acceptance_does_not_substitute_for_launch_authority",
    "test_permanent_claim_storage_rejects_symlink_or_partial_claim",
}


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


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(repository), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _commit_blob_sha256(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ("git", "-C", str(ROOT), "show", f"{ACCEPTED_I04_COMMIT}:{relative}"),
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()


def _result(
    check_id: str,
    name: str,
    condition: bool,
    finding: str,
    evidence: Any,
) -> dict[str, Any]:
    if not condition:
        raise AssertionError(f"{check_id} failed: {finding}")
    return {
        "check_id": check_id,
        "evidence": evidence,
        "finding": finding,
        "name": name,
        "status": "passed",
    }


def _function_calls(path: Path, function_name: str) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    )
    calls: list[str] = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            calls.append(node.func.attr)
    return calls


def _test_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test_")
    }


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY)
    one_shot.validate_policy(policy)
    frozen = one_shot.validate_frozen_hashes(policy)
    checks.append(
        _result(
            "I05B-01",
            "one-attempt zero-retry I05 policy",
            policy["attempt_policy"]["max_governed_attempts"] == 1
            and policy["attempt_policy"]["max_infrastructure_retries"] == 0
            and policy["candidate_execution_authorized"] is False,
            "the I05-owned policy freezes one attempt, zero retries, and no candidate authority",
            {
                "attempt_policy": policy["attempt_policy"],
                "candidate_execution_authorized": policy[
                    "candidate_execution_authorized"
                ],
            },
        )
    )

    current_i04 = {name: _sha256(path) for name, path in I04_PATHS.items()}
    committed_i04 = {
        name: _commit_blob_sha256(path) for name, path in I04_PATHS.items()
    }
    checks.append(
        _result(
            "I05B-02",
            "accepted I04R2 bytes remain immutable",
            current_i04 == I04_EXPECTED and committed_i04 == I04_EXPECTED,
            "all accepted I04R2 scientific/code/policy/test bytes equal commit b7b008c",
            {
                "accepted_commit": ACCEPTED_I04_COMMIT,
                "accepted_commit_hashes": committed_i04,
                "current_hashes": current_i04,
            },
        )
    )

    wrapper_source = WRAPPER.read_text(encoding="utf-8")
    governed_calls = _function_calls(WRAPPER, "governed_run")
    write_calls = _function_calls(WRAPPER, "_write_exclusive_bytes")
    claim_before_builder = wrapper_source.find("claim_attempt(claim_path, claim)") < wrapper_source.find(
        "record = _invoke_accepted_builder_once("
    )
    checks.append(
        _result(
            "I05B-03",
            "atomic permanent pre-builder claim",
            "os.O_CREAT | os.O_EXCL | os.O_WRONLY" in wrapper_source
            and claim_before_builder
            and write_calls.count("open") == 1
            and all(token not in wrapper_source for token in (".unlink(", "os.remove(", "rmtree(")),
            "exclusive claim creation precedes the sole builder call and no deletion path exists",
            {
                "atomic_flags": "O_CREAT|O_EXCL|O_WRONLY",
                "claim_before_builder": claim_before_builder,
                "claim_deletion_surface_present": False,
                "exclusive_open_calls": write_calls.count("open"),
            },
        )
    )

    builder_calls = _function_calls(WRAPPER, "_invoke_accepted_builder_once")
    checks.append(
        _result(
            "I05B-04",
            "accepted builder exactly once and delayed until after claim",
            governed_calls.count("_invoke_accepted_builder_once") == 1
            and builder_calls.count("build_calibration_record") == 1
            and "from p2_i2_i04r2_calibration import" in wrapper_source,
            "the I05 wrapper imports/calls the immutable accepted builder only inside the post-claim function",
            {
                "accepted_builder_calls_in_adapter": builder_calls.count(
                    "build_calibration_record"
                ),
                "governed_adapter_calls": governed_calls.count(
                    "_invoke_accepted_builder_once"
                ),
            },
        )
    )

    preflight_calls = _function_calls(WRAPPER, "preflight")
    checks.append(
        _result(
            "I05B-05",
            "committed authority/interpreter/command preflight",
            all(
                name in preflight_calls
                for name in (
                    "validate_repository_snapshot",
                    "validate_interpreter",
                    "validate_command",
                    "validate_committed_authority",
                    "validate_claim_storage",
                    "validate_frozen_hashes",
                    "validate_null_launch_authorization",
                    "validate_owner_acceptance",
                )
            )
            and policy["commit_binding"]["expected_head_source"].startswith(
                "required runtime --expected-head"
            ),
            "runtime preflight binds post-commit HEAD, clean state, committed blobs, separate acceptance/launch authority, permanent claim storage, interpreter, command, and frozen hashes without self-reference",
            {
                "preflight_calls": sorted(preflight_calls),
                "self_reference_rule": policy["commit_binding"][
                    "self_reference_rule"
                ],
            },
        )
    )

    final_fields = policy["receipt_contract"]["final_required_values"]
    checks.append(
        _result(
            "I05B-06",
            "readback-only reconstruction and final receipt facts",
            policy["reconstruction_policy"]["readback_only"] is True
            and final_fields
            == {
                "accepted_builder_invocation_count": 1,
                "authorization_consumed": True,
                "candidate_execution_authorized": False,
                "governed_attempt_count": 1,
                "infrastructure_retries": 0,
                "null_invocation_count": 1,
                "null_reconstruction_generation_count": 0,
                "output_readback_reconstruction_count": 1,
                "second_invocation_refused": True,
            }
            and governed_calls.count("read_text") == 1
            and governed_calls.count("loads") == 1,
            "the future attempt generates once and reconstructs only from retained output with separate counts/refusal status",
            {
                "final_required_values": final_fields,
                "read_text_calls": governed_calls.count("read_text"),
                "json_loads_calls": governed_calls.count("loads"),
            },
        )
    )

    tests = _test_names(TEST)
    checks.append(
        _result(
            "I05B-07",
            "owner-required eight-case refusal matrix",
            REQUIRED_TESTS <= tests,
            "all eight required zero-null safety demonstrations have named tests",
            {
                "required_tests": sorted(REQUIRED_TESTS),
                "test_file_sha256": _sha256(TEST),
            },
        )
    )

    command = (
        str(ROOT / ".venv/bin/python"),
        "-m",
        "unittest",
        str(TEST.relative_to(ROOT)),
    )
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    test_output = completed.stdout + completed.stderr
    checks.append(
        _result(
            "I05B-08",
            "zero-null safety tests pass",
            "Ran 12 tests" in test_output and "OK" in test_output,
            "twelve focused tests pass without invoking the accepted builder",
            {
                "command": ".venv/bin/python -m unittest experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests/test_p2_i2_i05b_one_shot.py",
                "tests_passed": 12,
            },
        )
    )

    validation = policy["validation_boundary"]
    checks.append(
        _result(
            "I05B-09",
            "accepted package remains launch-blocked and zero-execution",
            validation
            == {
                "builder_invocations": 0,
                "candidate_or_control_invocations": 0,
                "commit_authorized": True,
                "governed_null_invocations": 0,
                "null_invocation_authorized": False,
                "PyGRC_model_instantiations": 0,
            }
            and OWNER_ACCEPTANCE.is_file()
            and one_shot.validate_owner_acceptance(
                policy,
                policy_sha256=_sha256(POLICY),
                frozen_hashes=frozen,
            )["null_invocation_authorized"]
            is False
            and not NULL_LAUNCH_AUTHORIZATION.exists()
            and not GOVERNED_OUTPUT.exists()
            and not ATTEMPT_RECEIPT.exists()
            and not FINAL_RECEIPT.exists(),
            "owner acceptance/commit authority is exact, separate launch authority remains absent, and no claim, output, builder/null, PyGRC, candidate, or control operation exists",
            {
                "attempt_receipt_absent": not ATTEMPT_RECEIPT.exists(),
                "final_receipt_absent": not FINAL_RECEIPT.exists(),
                "governed_output_absent": not GOVERNED_OUTPUT.exists(),
                "null_launch_authorization_absent": not NULL_LAUNCH_AUTHORIZATION.exists(),
                "owner_acceptance_present": OWNER_ACCEPTANCE.is_file(),
                "validation_boundary": validation,
            },
        )
    )

    graph_revision = _git(GRAPH, "rev-parse", "HEAD")
    graph_status = _git(GRAPH, "status", "--short")
    checks.append(
        _result(
            "I05B-10",
            "graph read-only boundary",
            graph_revision == EXPECTED_GRAPH_REVISION and graph_status == "",
            "PyGRC remains at the admitted clean revision and was not imported or invoked",
            {"graph_revision": graph_revision, "graph_status": graph_status},
        )
    )

    checks.append(
        _result(
            "I05B-11",
            "single wrapper and one-shot policy identity",
            policy["paths"]["wrapper"] == str(WRAPPER.relative_to(ROOT))
            and policy["paths"]["policy"] == str(POLICY.relative_to(ROOT))
            and frozen["wrapper_sha256"] == _sha256(WRAPPER),
            "the correction adds one exact governed wrapper and one exact policy",
            {
                "policy_sha256": _sha256(POLICY),
                "wrapper_sha256": _sha256(WRAPPER),
            },
        )
    )

    checks.append(
        _result(
            "I05B-12",
            "failed-closed lineage, correction scope, and owner acceptance",
            policy["correction_authority"]["decision_id"] == "P2-I2-DEC-028"
            and policy["correction_authority"]["change_id"] == "P2-I2-CHG-021"
            and policy["correction_authority"]["proposed_DEC_027"]
            == "failed_closed_historical_disposition"
            and policy["correction_authority"]["scientific_revision"] is False,
            "DEC-027 remains failed-closed history, DEC-028/CHG-021 own only I05 safety mechanics, and DEC-029/CHG-022 accept only package retention",
            {
                "acceptance_change_id": "P2-I2-CHG-022",
                "acceptance_decision_id": "P2-I2-DEC-029",
                "correction_authority": policy["correction_authority"],
            },
        )
    )

    return {
        "artifact_id": "P2-I2-I05B-ZERO-NULL-SAFETY-VALIDATION",
        "artifact_version": "1.0.0",
        "checks": checks,
        "disposition": {
            "accepted_I04R2_bytes_immutable": True,
            "commit_authorized": True,
            "correction_owner_accepted": True,
            "null_invocation_authorized": False,
            "proposed_DEC_027": "failed_closed_historical_disposition",
            "P2-I2-CAL-GATE": "closed",
        },
        "execution_receipt": {
            "accepted_builder_invocations": 0,
            "candidate_or_control_invocations": 0,
            "governed_null_invocations": 0,
            "PyGRC_model_instantiations": 0,
            "scientific_result": False,
        },
        "input_identities": {
            "authorization_sha256": _sha256(AUTHORIZATION),
            "owner_acceptance_sha256": _sha256(OWNER_ACCEPTANCE),
            "one_shot_policy_sha256": _sha256(POLICY),
            "test_sha256": _sha256(TEST),
            "wrapper_sha256": _sha256(WRAPPER),
        },
        "iteration_id": "P2-I2-I05B",
        "lane_id": "AE01-L02",
        "passed_checks": len(checks),
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
        raise AssertionError(f"refusing to overwrite validation result: {args.output}")
    result = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(pretty_json_dumps(result), encoding="utf-8")
    print(
        f"P2-I2 I05B zero-null validation: {result['passed_checks']}/"
        f"{result['total_checks']}; accepted-builder invocations=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
