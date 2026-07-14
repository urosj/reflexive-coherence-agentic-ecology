#!/usr/bin/env python3
"""Zero-null validation of the P2-I2 I05C active-.venv correction."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
GRAPH = Path("/home/uros/Documents/RC-github/graph-reflexive-coherence")
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402
import p2_i2_i05b_one_shot as one_shot  # noqa: E402


ACCEPTED_I04_COMMIT = "b7b008c402d837b529962a1a5edb062927939d28"
FAILED_LAUNCH_HEAD = "98770ae4860ddc269a9ed21bb4803ec75682fc34"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
POLICY = EXPERIMENT / "configs/p2_i2_i05b_one_shot_policy.json"
WRAPPER = EXPERIMENT / "scripts/p2_i2_i05b_one_shot.py"
TEST = EXPERIMENT / "implementation/tests/test_p2_i2_i05b_one_shot.py"
FAILURE = EXPERIMENT / "contracts/p2-i2/i05c-preclaim-interpreter-path-failure.json"
ACCEPTANCE = EXPERIMENT / "contracts/p2-i2/i05b-owner-acceptance.json"
LAUNCH = EXPERIMENT / "contracts/p2-i2/i05-null-launch-authorization.json"
ATTEMPT = EXPERIMENT / "outputs/p2-i2/i05/i05b-attempt-claim.json"
FINAL = EXPERIMENT / "outputs/p2-i2/i05/i05b-final-receipt.json"
OUTPUT = (
    EXPERIMENT
    / "outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json"
)

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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def _commit_sha(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    value = subprocess.run(
        ("git", "show", f"{ACCEPTED_I04_COMMIT}:{relative}"),
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(value).hexdigest()


def _calls(function_name: str) -> list[str]:
    tree = ast.parse(WRAPPER.read_text(encoding="utf-8"), filename=str(WRAPPER))
    function = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == function_name
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


def _test_names() -> set[str]:
    tree = ast.parse(TEST.read_text(encoding="utf-8"), filename=str(TEST))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    }


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


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY)
    one_shot.validate_policy(policy)
    frozen = one_shot.validate_frozen_hashes(policy)
    checks.append(
        _result(
            "I05C-01",
            "bounded active-.venv correction policy",
            policy["artifact_version"] == "1.2.0"
            and policy["interpreter"]["executable_repo_relative"]
            == ".venv/bin/python"
            and policy["interpreter"]["venv_prefix_repo_relative"] == ".venv"
            and policy["interpreter"]["require_active_venv"] is True
            and policy["preclaim_correction_authority"]["decision_id"]
            == "P2-I2-DEC-031",
            "policy requires the exact active repository .venv and bounds DEC-031 scope",
            {
                "interpreter": policy["interpreter"],
                "preclaim_correction_authority": policy[
                    "preclaim_correction_authority"
                ],
            },
        )
    )

    failure = _load(FAILURE)
    zero_fields = {
        "attempt_claim_created": False,
        "accepted_builder_invocations": 0,
        "governed_null_invocations": 0,
        "null_reconstruction_generation_count": 0,
        "PyGRC_model_instantiations": 0,
        "candidate_or_control_invocations": 0,
        "final_receipt_created": False,
        "governed_output_created": False,
    }
    checks.append(
        _result(
            "I05C-02",
            "failed preflight retained before claim",
            failure["launch_head"] == FAILED_LAUNCH_HEAD
            and failure["venv_active"] is True
            and failure["failure_stage"] == "read_only_final_preflight_before_claim"
            and failure["authority_consumed"] is False
            and all(failure[key] == value for key, value in zero_fields.items()),
            "the valid active venv was rejected before claim and all governed counts remain zero",
            {"failure_message": failure["failure_message"], **zero_fields},
        )
    )

    identity = one_shot.interpreter_identity()
    one_shot.validate_interpreter(identity, policy)
    checks.append(
        _result(
            "I05C-03",
            "real repository venv passes exact identity",
            identity["venv_active"] is True
            and identity["invoked_executable"]
            == str((ROOT / ".venv/bin/python").absolute())
            and identity["venv_prefix"] == str((ROOT / ".venv").resolve())
            and identity["base_prefix"] != identity["venv_prefix"]
            and identity["binary_sha256"] == policy["interpreter"]["binary_sha256"],
            "the actual command uses the active repository venv while retaining exact target digest/version",
            identity,
        )
    )

    validate_calls = _calls("validate_interpreter")
    checks.append(
        _result(
            "I05C-04",
            "lexical command and resolved binary identities are separate",
            validate_calls.count("_lexical_repo_path") == 2
            and "_path" not in validate_calls
            and "resolve" in validate_calls
            and "_sha256" in validate_calls,
            "interpreter validation no longer routes the venv command symlink through the repository-data path guard",
            {"validate_interpreter_calls": validate_calls},
        )
    )

    acceptance = one_shot.validate_owner_acceptance(
        policy,
        policy_sha256=_sha256(POLICY),
        frozen_hashes=frozen,
    )
    launch = one_shot.validate_null_launch_authorization(
        policy,
        owner_acceptance_sha256=_sha256(ACCEPTANCE),
        policy_sha256=_sha256(POLICY),
        frozen_hashes=frozen,
    )
    checks.append(
        _result(
            "I05C-05",
            "consequential acceptance and launch identities",
            acceptance["preclaim_correction_decision_id"] == "P2-I2-DEC-031"
            and acceptance["null_invocation_authorized"] is False
            and launch["preclaim_correction_decision_id"] == "P2-I2-DEC-031"
            and launch["null_invocation_authorized"] is True,
            "immutable package acceptance remains distinct from the corrected launch authority",
            {
                "acceptance_sha256": _sha256(ACCEPTANCE),
                "launch_sha256": _sha256(LAUNCH),
            },
        )
    )

    current_i04 = {name: _sha256(path) for name, path in I04_PATHS.items()}
    committed_i04 = {name: _commit_sha(path) for name, path in I04_PATHS.items()}
    checks.append(
        _result(
            "I05C-06",
            "accepted I04R2 bytes immutable",
            current_i04 == I04_EXPECTED and committed_i04 == I04_EXPECTED,
            "all accepted I04R2 scientific/code/policy/test bytes remain exact",
            {
                "accepted_commit": ACCEPTED_I04_COMMIT,
                "current_hashes": current_i04,
            },
        )
    )

    required_tests = {
        "test_active_repository_venv_identity_passes",
        "test_wrong_interpreter_or_command_is_refused",
        "test_concurrent_second_start_is_refused",
        "test_start_after_simulated_crash_following_claim_is_refused",
        "test_owner_acceptance_does_not_substitute_for_launch_authority",
    }
    names = _test_names()
    completed = subprocess.run(
        (
            str(ROOT / ".venv/bin/python"),
            "-m",
            "unittest",
            str(TEST.relative_to(ROOT)),
        ),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    test_output = completed.stdout + completed.stderr
    checks.append(
        _result(
            "I05C-07",
            "positive and negative active-.venv tests",
            required_tests <= names and "Ran 13 tests" in test_output and "OK" in test_output,
            "thirteen zero-null tests include a real active-venv pass and wrong/inactive/digest refusals",
            {"required_tests": sorted(required_tests), "tests_passed": 13},
        )
    )

    one_shot.validate_preclaim_absence(policy)
    storage = one_shot.validate_claim_storage(policy)
    checks.append(
        _result(
            "I05C-08",
            "authority remains unconsumed",
            not ATTEMPT.exists()
            and not FINAL.exists()
            and not OUTPUT.exists()
            and storage["filesystem_type"] == "ext4",
            "claim/final/output remain absent and the permanent local claim boundary is unchanged",
            {
                "attempt_absent": not ATTEMPT.exists(),
                "final_absent": not FINAL.exists(),
                "output_absent": not OUTPUT.exists(),
                "claim_storage": storage,
            },
        )
    )

    checks.append(
        _result(
            "I05C-09",
            "one-attempt zero-retry and scientific quarantine",
            policy["attempt_policy"]["max_governed_attempts"] == 1
            and policy["attempt_policy"]["max_infrastructure_retries"] == 0
            and policy["candidate_execution_authorized"] is False
            and policy["preclaim_correction_authority"]["scientific_revision"]
            is False,
            "the correction changes no execution count or scientific authority",
            {
                "attempt_policy": policy["attempt_policy"],
                "candidate_execution_authorized": False,
            },
        )
    )

    graph_revision = _git(GRAPH, "rev-parse", "HEAD")
    graph_status = _git(GRAPH, "status", "--short")
    checks.append(
        _result(
            "I05C-10",
            "graph read-only boundary",
            graph_revision == EXPECTED_GRAPH_REVISION and graph_status == "",
            "PyGRC remains at the admitted clean revision and was not invoked",
            {"graph_revision": graph_revision, "graph_status": graph_status},
        )
    )

    checks.append(
        _result(
            "I05C-11",
            "corrected wrapper and policy identities",
            frozen["wrapper_sha256"] == _sha256(WRAPPER)
            and acceptance["wrapper_sha256"] == _sha256(WRAPPER)
            and acceptance["policy_sha256"] == _sha256(POLICY)
            and launch["wrapper_sha256"] == _sha256(WRAPPER)
            and launch["policy_sha256"] == _sha256(POLICY),
            "policy, acceptance, and launch all bind the exact corrected wrapper/policy",
            {
                "policy_sha256": _sha256(POLICY),
                "wrapper_sha256": _sha256(WRAPPER),
            },
        )
    )

    checks.append(
        _result(
            "I05C-12",
            "zero-execution correction boundary",
            True,
            "validation imports no builder and executes zero null, PyGRC, candidate, or control operations",
            {
                "accepted_builder_invocations": 0,
                "governed_null_invocations": 0,
                "PyGRC_model_instantiations": 0,
                "candidate_or_control_invocations": 0,
                "scientific_result": False,
            },
        )
    )

    return {
        "artifact_id": "P2-I2-I05C-ZERO-NULL-INTERPRETER-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I05C",
        "lane_id": "AE01-L02",
        "checks": checks,
        "passed_checks": len(checks),
        "total_checks": len(checks),
        "disposition": {
            "correction_review_ready": True,
            "authority_consumed": False,
            "governed_attempts": 0,
            "infrastructure_retries": 0,
            "commit_authorized": False,
            "P2-I2-CAL-GATE": "closed",
        },
        "input_identities": {
            "failure_sha256": _sha256(FAILURE),
            "owner_acceptance_sha256": _sha256(ACCEPTANCE),
            "launch_authorization_sha256": _sha256(LAUNCH),
            "policy_sha256": _sha256(POLICY),
            "test_sha256": _sha256(TEST),
            "wrapper_sha256": _sha256(WRAPPER),
        },
        "execution_receipt": {
            "accepted_builder_invocations": 0,
            "governed_null_invocations": 0,
            "PyGRC_model_instantiations": 0,
            "candidate_or_control_invocations": 0,
            "scientific_result": False,
        },
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
        f"P2-I2 I05C zero-null validation: {result['passed_checks']}/"
        f"{result['total_checks']}; governed attempts=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
