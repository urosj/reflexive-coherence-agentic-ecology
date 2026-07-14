#!/usr/bin/env python3
"""Validate the unconsumed P2-I2 I05 single-invocation authority.

This validator calls only the frozen I04R2 authorization validator.  It never
calls the arithmetic-null record builder or entry point and never imports
PyGRC.
"""

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
from p2_i2_i04r2_calibration import validate_execution_authorization  # noqa: E402


ACCEPTED_I04_COMMIT = "b7b008c402d837b529962a1a5edb062927939d28"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
EXPECTED_AUTHORIZATION_SHA256 = "97a78f7f5e8b1119ec059b82a7a5b6c14c573efc55411ac4392ff6cf2703545a"
EXPECTED = {
    "parent_analysis_policy": "91b8bd50633a19333935ec115bdd005697abdef5381ef59f4ceab21db08c090d",
    "machine_policy": "277dfc22c9e98268e950cb634ed1174b9ad4f0f654a72984b365655815c3a9ce",
    "calibration_policy": "57dc32d02b828bb21caf069c5690bf4fcfc240848faefcd8412a6505bba849fe",
    "calibration_entrypoint": "8a0ef5569705ea0619a628b3b5a25d9dc80448a273a68a92d131ce775793b61a",
    "preregistration": "dee89df45b4a5ece93d1d7ce461d2c0cb8f028ff44aa32b3f4e45e88a1b09e9b",
    "I04R2_validation": "637c07cc7d31824f4806459f7b4e8ddd1262eec3c5cc874b009ea7767b59d361",
    "owner_acceptance": "2ade4d6255c42044621489e1132d1030f48266e851bea614a11f1100c4f7dacf",
}
PATHS = {
    "parent_analysis_policy": EXPERIMENT / "configs/p2_i2_i04r1_analysis_policy.json",
    "machine_policy": EXPERIMENT / "configs/p2_i2_i04r2_machine_policy.json",
    "calibration_policy": EXPERIMENT / "configs/p2_i2_i04r2_calibration_policy.json",
    "calibration_entrypoint": EXPERIMENT / "scripts/p2_i2_i04r2_calibration.py",
    "preregistration": EXPERIMENT / "contracts/p2-i2/i04r2-machine-verification-preregistration.json",
    "I04R2_validation": EXPERIMENT / "contracts/p2-i2/i04r2-machine-verification-validation.json",
    "owner_acceptance": EXPERIMENT / "contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json",
}
AUTHORIZATION = EXPERIMENT / "contracts/p2-i2/i05-calibration-execution-freeze.json"
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


def _calibration_imports() -> list[str]:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=__file__)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "p2_i2_i04r2_calibration":
            imported.extend(alias.name for alias in node.names)
    return sorted(imported)


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    resolved_commit = _git(ROOT, "rev-parse", f"{ACCEPTED_I04_COMMIT}^{{commit}}")
    checks.append(
        _result(
            "AUTH-01",
            "accepted I04 commit exists",
            resolved_commit == ACCEPTED_I04_COMMIT,
            "the authorization names the exact committed accepted-I04 lineage",
            {"accepted_I04_commit": resolved_commit},
        )
    )

    current_hashes = {name: _sha256(path) for name, path in PATHS.items()}
    commit_hashes = {name: _commit_blob_sha256(path) for name, path in PATHS.items()}
    checks.append(
        _result(
            "AUTH-02",
            "accepted I04 identities are immutable and commit-bound",
            current_hashes == EXPECTED and commit_hashes == EXPECTED,
            "all active I04R2 inputs, validation, and acceptance bytes match the accepted commit",
            {"accepted_commit_hashes": commit_hashes, "current_hashes": current_hashes},
        )
    )

    acceptance = _load(PATHS["owner_acceptance"])
    progression = acceptance.get("progression_authority", {})
    history = acceptance.get("historical_lineage", [])
    tie = acceptance.get("exact_tie_rule", {})
    gate = acceptance.get("gate_effect", {})
    acceptance_ok = (
        acceptance.get("decision_id") == "P2-I2-DEC-026"
        and progression.get("iteration_id") == "P2-I2-I04R2"
        and progression.get("status") == "sole_active_I04_progression_authority"
        and len(history) == 2
        and all(item.get("parallel_execution_authority") is False for item in history)
        and tie.get("scientific_meaning") == "none"
        and tie.get("interpretive_use_forbidden") is True
        and gate.get("P2-I2-CAL-PRE-GATE")
        == "passed_after_explicit_owner_acceptance_of_I04R2"
        and "automatic_I05_invocation" in gate.get("does_not_open", [])
    )
    checks.append(
        _result(
            "AUTH-03",
            "owner-acceptance progression boundary",
            acceptance_ok,
            "DEC-026 makes only I04R2 active, keeps predecessors historical, and gives the tie no scientific meaning",
            {
                "decision_id": acceptance.get("decision_id"),
                "historical_iterations": [item.get("iteration_id") for item in history],
                "progression_status": progression.get("status"),
                "tie_scientific_meaning": tie.get("scientific_meaning"),
            },
        )
    )

    authorization = _load(AUTHORIZATION)
    validate_execution_authorization(
        authorization,
        parent_analysis_path=PATHS["parent_analysis_policy"],
        machine_policy_path=PATHS["machine_policy"],
        calibration_path=PATHS["calibration_policy"],
        preregistration_path=PATHS["preregistration"],
    )
    checks.append(
        _result(
            "AUTH-04",
            "frozen I04R2 authorization validator",
            True,
            "the exact authorization passes the already-frozen I04R2 validator",
            {"validator": "p2_i2_i04r2_calibration.validate_execution_authorization"},
        )
    )

    auth_sha = _sha256(AUTHORIZATION)
    authority = authorization["I04R2_owner_acceptance_authority"]
    checks.append(
        _result(
            "AUTH-05",
            "authorization identity and acceptance binding",
            auth_sha == EXPECTED_AUTHORIZATION_SHA256
            and "P2-I2-DEC-026" in authority
            and ACCEPTED_I04_COMMIT in authority
            and EXPECTED["owner_acceptance"] in authority,
            "the freeze has one exact identity and names its decision, accepted commit, and acceptance-record digest",
            {
                "authorization_sha256": auth_sha,
                "owner_acceptance_authority": authority,
            },
        )
    )

    checks.append(
        _result(
            "AUTH-06",
            "single-invocation and candidate exclusion",
            authorization["governed_invocations_authorized"] == 1
            and authorization["candidate_execution_authorized"] is False,
            "exactly one arithmetic-null invocation is authorized and no candidate execution is opened",
            {
                "candidate_execution_authorized": authorization[
                    "candidate_execution_authorized"
                ],
                "governed_invocations_authorized": authorization[
                    "governed_invocations_authorized"
                ],
            },
        )
    )

    imported = _calibration_imports()
    checks.append(
        _result(
            "AUTH-07",
            "zero-execution validator call surface",
            imported == ["validate_execution_authorization"],
            "this activity imports only the frozen authorization validator, never the record builder or main entry point",
            {"imported_from_p2_i2_i04r2_calibration": imported},
        )
    )

    pygrc_loaded = sorted(
        name for name in sys.modules if name == "pygrc" or name.startswith("pygrc.")
    )
    checks.append(
        _result(
            "AUTH-08",
            "PyGRC exclusion",
            not pygrc_loaded,
            "static authorization construction and validation did not import PyGRC",
            {"loaded_pygrc_modules": pygrc_loaded},
        )
    )

    checks.append(
        _result(
            "AUTH-09",
            "governed output absence",
            not GOVERNED_OUTPUT.exists(),
            "the authorized arithmetic-null output does not exist and the permission remains unconsumed",
            {"governed_output": str(GOVERNED_OUTPUT.relative_to(ROOT)), "exists": False},
        )
    )

    graph_revision = _git(GRAPH, "rev-parse", "HEAD")
    graph_status = _git(GRAPH, "status", "--short")
    checks.append(
        _result(
            "AUTH-10",
            "graph source read-only boundary",
            graph_revision == EXPECTED_GRAPH_REVISION and graph_status == "",
            "the admitted PyGRC source remains at the exact clean revision",
            {"graph_revision": graph_revision, "graph_status": graph_status},
        )
    )

    checks.append(
        _result(
            "AUTH-11",
            "construction invocation accounting",
            imported == ["validate_execution_authorization"]
            and not pygrc_loaded
            and not GOVERNED_OUTPUT.exists(),
            "authorization construction ran no governed null, PyGRC, candidate, or control invocation",
            {
                "candidate_or_control_invocations": 0,
                "governed_matched_null_invocations": 0,
                "PyGRC_model_instantiations": 0,
            },
        )
    )

    checks.append(
        _result(
            "AUTH-12",
            "gate and evidence ceiling",
            authorization["candidate_execution_authorized"] is False
            and not GOVERNED_OUTPUT.exists(),
            "the candidate encodes a one-call ceiling but activates nothing before owner review and commit authorization",
            {
                "P2-I2-CAL-GATE": "blocked_pending_authorized_I05_execution_and_reconstruction",
                "I06_registration_authorized": False,
                "analysis_arithmetic_delta_assigned": False,
                "authorization_active": False,
                "scientific_result": False,
            },
        )
    )

    return {
        "artifact_id": "P2-I2-I05-AUTHORIZATION-VALIDATION",
        "artifact_version": "1.0.0",
        "authorization": {
            "governed_invocations_authorized": 1,
            "path": str(AUTHORIZATION.relative_to(ROOT)),
            "sha256": auth_sha,
            "status": "candidate_validated_unconsumed_pending_owner_acceptance",
        },
        "checks": checks,
        "disposition": {
            "P2-I2-CAL-GATE": "blocked_pending_authorized_I05_execution_and_reconstruction",
            "authorization_active": False,
            "authorization_candidate_review_ready": True,
            "candidate_execution_authorized": False,
            "governed_invocation_consumed": False,
            "next_permitted_action": "owner review and explicit acceptance plus commit authorization",
        },
        "execution_receipt": {
            "PyGRC_model_instantiations": 0,
            "candidate_or_control_invocations": 0,
            "governed_matched_null_invocations": 0,
            "scientific_result": False,
        },
        "focused_checks_passed": len(checks),
        "iteration_id": "P2-I2-I05",
        "lane_id": "AE01-L02",
        "validation_scope": "authorization_integrity_only",
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
        f"P2-I2 I05 authorization valid: {result['focused_checks_passed']}/"
        f"{result['focused_checks_passed']}; governed invocations executed=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
