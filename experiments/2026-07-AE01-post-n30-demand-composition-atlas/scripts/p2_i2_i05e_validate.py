"""Validate the bounded I05 historical-to-portable projection correction."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402
import p2_i2_i05d_portability_audit as portability_audit  # noqa: E402


POLICY = EXPERIMENT / "configs/p2_i2_i05e_portability_correction_policy.json"
FREEZE = EXPERIMENT / "contracts/p2-i2/i05e-portability-correction-input-freeze.json"
BASELINE = EXPERIMENT / "contracts/p2-i2/i05d-portability-audit.json"
LINEAGE = EXPERIMENT / "contracts/p2-i2/i05e-portable-projection-lineage.json"
REPORT = EXPERIMENT / "reports/P2-I2-I05E-portability-correction.md"
FINAL = EXPERIMENT / "outputs/p2-i2/i05/i05b-final-receipt.json"
ONE_SHOT_POLICY = EXPERIMENT / "configs/p2_i2_i05b_one_shot_policy.json"

I04_IDENTITIES = {
    "configs/p2_i2_i04r1_analysis_policy.json": "91b8bd50633a19333935ec115bdd005697abdef5381ef59f4ceab21db08c090d",
    "configs/p2_i2_i04r2_calibration_policy.json": "57dc32d02b828bb21caf069c5690bf4fcfc240848faefcd8412a6505bba849fe",
    "configs/p2_i2_i04r2_machine_policy.json": "277dfc22c9e98268e950cb634ed1174b9ad4f0f654a72984b365655815c3a9ce",
    "contracts/p2-i2/i04r2-machine-verification-preregistration.json": "dee89df45b4a5ece93d1d7ce461d2c0cb8f028ff44aa32b3f4e45e88a1b09e9b",
    "contracts/p2-i2/i04r2-machine-verification-validation.json": "637c07cc7d31824f4806459f7b4e8ddd1262eec3c5cc874b009ea7767b59d361",
    "contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json": "2ade4d6255c42044621489e1132d1030f48266e851bea614a11f1100c4f7dacf",
    "implementation/tests/test_p2_i2_i04r2_analysis.py": "75de8f69c2e1433618303a8338d4899be272527c3af9b4c7c7476448f5ccfaf2",
    "scripts/p2_i2_i04r2_analysis.py": "2abc4c2040d4fff3467931feeedb0e2423a5fca71a3bc3a921aa4ca3e9b22a24",
    "scripts/p2_i2_i04r2_calibration.py": "8a0ef5569705ea0619a628b3b5a25d9dc80448a273a68a92d131ce775793b61a"
}


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected object: {path.relative_to(ROOT).as_posix()}")
    return value


def _historical_bytes(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ("git", "-C", str(ROOT), "show", f"{commit}:{relative}"),
        check=True,
        capture_output=True,
    ).stdout


def _historical_json(commit: str, relative: str) -> dict[str, Any]:
    value = json.loads(_historical_bytes(commit, relative))
    if not isinstance(value, dict):
        raise AssertionError(f"historical object expected: {relative}")
    return value


def _projection_metadata(kind: str, source_sha256: str) -> dict[str, Any]:
    return {
        "change_id": "P2-I2-CHG-026",
        "decision_id": "P2-I2-DEC-033",
        "projection_kind": kind,
        "scientific_change": False,
        "source_commit": "c3eabf30c9214055b43d7d2fbe86c3bc903be844",
        "source_sha256": source_sha256,
    }


def _project_failure(raw: dict[str, Any], source_sha256: str) -> dict[str, Any]:
    value = deepcopy(raw)
    value["artifact_version"] = "1.1.0"
    for field in ("invoked_executable", "venv_prefix", "base_prefix", "resolved_executable"):
        value.pop(field)
    value.update(
        {
            "invoked_executable_repo_relative": ".venv/bin/python",
            "venv_prefix_repo_relative": ".venv",
            "base_runtime_separated": True,
            "resolved_binary_identity": "sha256:1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118",
            "portability_projection": _projection_metadata(
                "historical_record_portable_projection", source_sha256
            ),
        }
    )
    return value


def _project_validation(raw: dict[str, Any], source_sha256: str) -> dict[str, Any]:
    value = deepcopy(raw)
    value["artifact_version"] = "1.1.0"
    identity = value["checks"][2]["evidence"]
    for field in ("invoked_executable", "venv_prefix", "base_prefix", "resolved_executable"):
        identity.pop(field)
    binary_sha256 = identity["binary_sha256"]
    identity.update(
        {
            "invoked_executable_repo_relative": ".venv/bin/python",
            "venv_prefix_repo_relative": ".venv",
            "base_runtime_separated": True,
            "resolved_binary_identity": f"sha256:{binary_sha256}",
        }
    )
    storage = value["checks"][7]["evidence"]["claim_storage"]
    storage.pop("mount_target")
    storage["mount_identity"] = "repository_worktree"
    value["portability_projection"] = _projection_metadata(
        "historical_validation_portable_projection", source_sha256
    )
    return value


def _project_output(raw: dict[str, Any], source_sha256: str) -> dict[str, Any]:
    value = deepcopy(raw)
    identities = value["input_identities"]
    identities["calibration_policy_path"] = (
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
        "configs/p2_i2_i04r2_calibration_policy.json"
    )
    identities["machine_policy_path"] = (
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
        "configs/p2_i2_i04r2_machine_policy.json"
    )
    identities["parent_analysis_policy_path"] = (
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
        "configs/p2_i2_i04r1_analysis_policy.json"
    )
    value["record_version"] = "1.1.0"
    value["portability_projection"] = _projection_metadata(
        "governed_output_portable_projection", source_sha256
    )
    return value


def _project_claim(raw: dict[str, Any], source_sha256: str) -> dict[str, Any]:
    value = deepcopy(raw)
    value["artifact_version"] = "1.1.0"
    storage = value["preflight"]["claim_storage"]
    storage.pop("mount_target")
    storage["mount_identity"] = "repository_worktree"
    identity = value["preflight"]["interpreter"]
    for field in ("invoked_executable", "venv_prefix", "base_prefix", "resolved_executable"):
        identity.pop(field)
    binary_sha256 = identity["binary_sha256"]
    identity.update(
        {
            "invoked_executable_repo_relative": ".venv/bin/python",
            "venv_prefix_repo_relative": ".venv",
            "base_runtime_separated": True,
            "resolved_binary_identity": f"sha256:{binary_sha256}",
        }
    )
    value["portability_projection"] = _projection_metadata(
        "permanent_claim_portable_projection", source_sha256
    )
    return value


def _check(
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


def _calls_in(source: str, function_name: str) -> list[tuple[str, int]]:
    tree = ast.parse(source)
    function = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == function_name
    )
    calls: list[tuple[str, int]] = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            calls.append((node.func.id, node.lineno))
        elif isinstance(node.func, ast.Attribute):
            calls.append((node.func.attr, node.lineno))
    return calls


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY)
    freeze = _load(FREEZE)
    baseline = _load(BASELINE)
    lineage = _load(LINEAGE)
    one_shot_policy = _load(ONE_SHOT_POLICY)
    if _sha256(POLICY) != freeze["policy_sha256"]:
        raise AssertionError("I05E policy identity drifted")
    if _sha256(BASELINE) != policy["baseline_audit"]["result_sha256"]:
        raise AssertionError("accepted I05D inventory identity drifted")

    source_scope = {item["path"]: item["source_sha256"] for item in policy["correction_scope"]}
    baseline_scope = set(
        baseline["affected_files_by_group"]["i05_active_execution_and_closeout"]
    )
    baseline_violations = [
        item
        for item in baseline["violations"]
        if item["correction_group"] == "i05_active_execution_and_closeout"
    ]
    checks.append(
        _check(
            "I05E-01",
            "accepted exact I05D group",
            set(source_scope) == baseline_scope
            and len(source_scope) == 11
            and len(baseline_violations) == 32
            and all(
                item["file_sha256"] == source_scope[item["path"]]
                for item in baseline_violations
            ),
            "the correction scope is exactly the accepted eleven-file thirty-two-finding I05D group",
            {"affected_files": 11, "baseline_violations": 32},
        )
    )

    historical_commit = policy["historical_evidence"]["commit"]
    historical_hashes = {
        relative: _sha256_bytes(_historical_bytes(historical_commit, relative))
        for relative in source_scope
    }
    checks.append(
        _check(
            "I05E-02",
            "historical source bytes",
            historical_hashes == source_scope,
            "every source digest reconstructs from the frozen historical commit",
            {"historical_commit": historical_commit, "source_file_count": len(source_scope)},
        )
    )

    projections = {item["path"]: item for item in lineage["projections"]}
    current_hashes = {relative: _sha256(ROOT / relative) for relative in source_scope}
    checks.append(
        _check(
            "I05E-03",
            "portable projection lineage identities",
            set(projections) == set(source_scope)
            and all(
                projections[path]["source_sha256"] == source_scope[path]
                and projections[path]["current_sha256"] == current_hashes[path]
                for path in source_scope
            ),
            "the lineage manifest binds every historical and current byte without a machine location",
            {"projection_count": len(projections), "lineage_sha256": _sha256(LINEAGE)},
        )
    )

    package_subjects = [ROOT / relative for relative in source_scope] + [
        POLICY,
        FREEZE,
        LINEAGE,
        REPORT,
        Path(__file__),
    ]
    findings: list[dict[str, Any]] = []
    for path in package_subjects:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix == ".json":
            findings.extend(portability_audit._scan_json(path, relative))
        else:
            findings.extend(portability_audit._scan_text(path, relative))
    checks.append(
        _check(
            "I05E-04",
            "zero corrected-group path violations",
            not findings,
            "all corrected files and I05E package inputs contain zero persisted absolute-path violations",
            {"scanned_file_count": len(package_subjects), "violation_count": len(findings)},
        )
    )

    paths_by_name = {Path(path).name: path for path in source_scope}
    failure_path = paths_by_name["i05c-preclaim-interpreter-path-failure.json"]
    validation_path = paths_by_name["i05c-zero-null-interpreter-validation.json"]
    output_path = paths_by_name["complete-three-arm-analysis-arithmetic-calibration.json"]
    claim_path = paths_by_name["i05b-attempt-claim.json"]
    exact_projections = {
        failure_path: _project_failure(
            _historical_json(historical_commit, failure_path), source_scope[failure_path]
        ),
        validation_path: _project_validation(
            _historical_json(historical_commit, validation_path), source_scope[validation_path]
        ),
        output_path: _project_output(
            _historical_json(historical_commit, output_path), source_scope[output_path]
        ),
        claim_path: _project_claim(
            _historical_json(historical_commit, claim_path), source_scope[claim_path]
        ),
    }
    checks.append(
        _check(
            "I05E-05",
            "exact historical-to-portable reconstruction",
            all(_load(ROOT / path) == expected for path, expected in exact_projections.items()),
            "all changed JSON records equal the frozen field-only transformation of their historical bytes",
            {"exactly_reconstructed_json_projections": len(exact_projections)},
        )
    )

    raw_final = _historical_json(historical_commit, FINAL.relative_to(ROOT).as_posix())
    current_final = _load(FINAL)
    immutable = policy["immutable_facts"]
    final_matches = (
        current_final == raw_final
        and _sha256(FINAL) == policy["historical_evidence"]["final_receipt_sha256"]
        and current_final["claim_receipt_sha256"]
        == policy["historical_evidence"]["permanent_claim_sha256"]
        and current_final["output_sha256"]
        == policy["historical_evidence"]["governed_output_sha256"]
        and all(current_final[field] == immutable[field] for field in (
            "authorization_consumed",
            "builder_invocation_count",
            "governed_attempt_count",
            "infrastructure_retries",
            "null_invocation_count",
            "null_reconstruction_generation_count",
            "output_readback_reconstruction_count",
            "scientific_result",
            "second_invocation_refused",
        ))
    )
    checks.append(
        _check(
            "I05E-06",
            "immutable raw execution receipt",
            final_matches,
            "the byte-identical final receipt preserves one attempt one builder call zero retries readback-only reconstruction and second-start refusal",
            {
                "final_receipt_sha256": _sha256(FINAL),
                "governed_attempt_count": current_final["governed_attempt_count"],
                "builder_invocation_count": current_final["builder_invocation_count"],
                "infrastructure_retries": current_final["infrastructure_retries"],
                "second_invocation_refused": current_final["second_invocation_refused"],
            },
        )
    )

    claim = _load(ROOT / claim_path)
    claim_mode = os.stat(ROOT / claim_path, follow_symlinks=False).st_mode
    checks.append(
        _check(
            "I05E-07",
            "permanent consumed-claim guard",
            (ROOT / claim_path).is_file()
            and not (ROOT / claim_path).is_symlink()
            and not claim_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
            and claim["authorization_consumed"] is True
            and claim["claim_deletion_forbidden"] is True
            and claim["max_governed_attempts"] == 1
            and claim["infrastructure_retries_authorized"] == 0,
            "the read-only current claim projection remains present and permanently blocks another start",
            {
                "authorization_consumed": claim["authorization_consumed"],
                "claim_deletion_forbidden": claim["claim_deletion_forbidden"],
                "max_governed_attempts": claim["max_governed_attempts"],
                "writable": bool(claim_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)),
            },
        )
    )

    output = _load(ROOT / output_path)
    i04_current = {
        relative: _sha256(EXPERIMENT / relative) for relative in I04_IDENTITIES
    }
    checks.append(
        _check(
            "I05E-08",
            "scientific and arithmetic invariants",
            i04_current == I04_IDENTITIES
            and output["analysis_arithmetic_delta"] == immutable["analysis_arithmetic_delta"]
            and output["analysis_arithmetic_floor"] == immutable["analysis_arithmetic_floor"]
            and output["candidate_blind"] is True
            and output["runtime_execution"] is False
            and output["runtime_tolerance_authority"] == "none"
            and output["portability_projection"]["scientific_change"] is False,
            "accepted I04R2 bytes and every I05 arithmetic/scientific boundary remain unchanged",
            {
                "I04R2_identity_count": len(i04_current),
                "analysis_arithmetic_delta": output["analysis_arithmetic_delta"],
                "analysis_arithmetic_floor": output["analysis_arithmetic_floor"],
                "scientific_change": False,
            },
        )
    )

    wrapper_path = ROOT / paths_by_name["p2_i2_i05b_one_shot.py"]
    wrapper_source = wrapper_path.read_text(encoding="utf-8")
    governed_calls = _calls_in(wrapper_source, "governed_run")
    claim_line = next(line for name, line in governed_calls if name == "claim_attempt")
    builder_line = next(
        line for name, line in governed_calls if name == "_invoke_accepted_builder_once"
    )
    claim_function_calls = [name for name, _ in _calls_in(wrapper_source, "claim_attempt")]
    source_files = [ROOT / path for path in source_scope if Path(path).suffix == ".py"]
    for path in source_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
    checks.append(
        _check(
            "I05E-09",
            "portable one-shot source safety",
            claim_line < builder_line
            and "_write_exclusive_bytes" in claim_function_calls
            and "os.O_CREAT | os.O_EXCL | os.O_WRONLY" in wrapper_source
            and "HISTORICAL_AUTHORITY_COMMIT" in wrapper_source
            and "PORTABLE_PROJECTION_EXECUTION_AUTHORIZED = False" in wrapper_source
            and "portable projection wrapper has no execution authority" in wrapper_source,
            "portable source remains parseable, is non-executable, and preserves historical exclusive consume-before-builder mechanics plus authority binding",
            {
                "claim_call_line": claim_line,
                "builder_call_line": builder_line,
                "parsed_python_files": len(source_files),
            },
        )
    )

    interpreter = one_shot_policy["interpreter"]
    checks.append(
        _check(
            "I05E-10",
            "venv and zero-execution boundary",
            interpreter["executable_repo_relative"] == ".venv/bin/python"
            and interpreter["venv_prefix_repo_relative"] == ".venv"
            and interpreter["require_active_venv"] is True
            and policy["invocation_ceiling"]["null_builder_or_wrapper_invocations"] == 0
            and policy["invocation_ceiling"]["pygrc_model_instantiations"] == 0
            and policy["invocation_ceiling"]["candidate_or_control_invocations"] == 0,
            "I05E requires the repository venv and authorizes no governed null wrapper PyGRC candidate control or scientific operation",
            {
                "candidate_or_control_invocations": 0,
                "governed_null_or_wrapper_invocations": 0,
                "interpreter": ".venv/bin/python",
                "pygrc_model_instantiations": 0,
                "scientific_result": False,
            },
        )
    )

    return {
        "activity_id": policy["activity_id"],
        "artifact_id": "P2-I2-I05E-I05-PORTABILITY-CORRECTION-VALIDATION",
        "artifact_version": "1.0.0",
        "candidate_or_control_invocations": 0,
        "checks": checks,
        "corrected_file_count": len(source_scope),
        "corrected_group_violation_count": len(findings),
        "freeze_sha256": _sha256(FREEZE),
        "governed_null_or_wrapper_invocations": 0,
        "historical_execution_commit": historical_commit,
        "iteration_id": "P2-I2-I05E",
        "lane_id": "AE01-L02",
        "lineage_sha256": _sha256(LINEAGE),
        "passed_checks": len(checks),
        "policy_sha256": _sha256(POLICY),
        "pygrc_model_instantiations": 0,
        "result_status": "P2-I2-I05E-I05-GROUP-REVIEW-READY",
        "scientific_result": False,
        "total_checks": len(checks),
        "validator": {
            "path": Path(__file__).relative_to(ROOT).as_posix(),
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
        f"P2-I2 I05E I05 portability correction: {result['passed_checks']}/"
        f"{result['total_checks']}; corrected-group violations="
        f"{result['corrected_group_violation_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
