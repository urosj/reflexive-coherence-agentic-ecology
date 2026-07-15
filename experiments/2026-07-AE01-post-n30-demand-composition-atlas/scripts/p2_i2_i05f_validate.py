"""Validate the bounded I04/I05 authority-dependency portability correction."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import difflib
import hashlib
import json
from pathlib import Path
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


POLICY = EXPERIMENT / "configs/p2_i2_i05f_portability_correction_policy.json"
FREEZE = EXPERIMENT / "contracts/p2-i2/i05f-portability-correction-input-freeze.json"
BASELINE = EXPERIMENT / "contracts/p2-i2/i05d-portability-audit.json"
LINEAGE = EXPERIMENT / "contracts/p2-i2/i05f-portable-projection-lineage.json"
REPORT = EXPERIMENT / "reports/P2-I2-I05F-portability-correction.md"
SOURCE_COMMIT = "6dd689811949b51ef9a2e9e0d0d14c06bf7346ba"
I04R2_COMMIT = "b7b008c402d837b529962a1a5edb062927939d28"
GRAPH_REPOSITORY_ID = "graph-reflexive-coherence"
GRAPH = ROOT.parent / GRAPH_REPOSITORY_ID
ATTACHMENT_ID = "5f7e5ef9-d600-4f97-a668-3b67afa14284"
SEP = chr(47)

JSON_PROJECTION_KINDS = {
    "configs/p2_i2_i04r2_machine_policy.json": (
        "repository_relative_external_source_identity"
    ),
    "contracts/p2-i2/i04-calibration-preregistration.json": (
        "structured_authority_reference"
    ),
    "contracts/p2-i2/i04r1-calibration-preregistration-validation.json": (
        "repository_relative_external_source_identity"
    ),
    "contracts/p2-i2/i04r1-calibration-preregistration.json": (
        "structured_authority_and_repository_relative_source_identity"
    ),
    "contracts/p2-i2/i04r1-critical-review-correction-input.json": (
        "repository_relative_external_source_identity"
    ),
    "contracts/p2-i2/i04r2-conditional-machine-verification-input.json": (
        "stable_attachment_identity"
    ),
    "contracts/p2-i2/i04r2-machine-verification-preregistration.json": (
        "repository_relative_external_source_identity"
    ),
    "contracts/p2-i2/i04r2-machine-verification-validation.json": (
        "stable_attachment_and_repository_relative_source_identity"
    ),
}

I05_IMMUTABLE = {
    "outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json": (
        "87a3635324a4ccccd983d0c33db8e7dba3e4c958396252b6edda7c56ea6eba2d"
    ),
    "outputs/p2-i2/i05/i05b-attempt-claim.json": (
        "7e6d37ae6281e6f7c305a332a082b9bfcf1254f8acba8815da8b48b0cfc76109"
    ),
    "outputs/p2-i2/i05/i05b-final-receipt.json": (
        "1f1694b96f22cde12b54a2e0c00ce76b58f2fdf2fc7cff1114bcc46b9a3396be"
    ),
}

I04R2_ACCEPTED = {
    "configs/p2_i2_i04r2_machine_policy.json": (
        "277dfc22c9e98268e950cb634ed1174b9ad4f0f654a72984b365655815c3a9ce"
    ),
    "contracts/p2-i2/i04r2-machine-verification-preregistration.json": (
        "dee89df45b4a5ece93d1d7ce461d2c0cb8f028ff44aa32b3f4e45e88a1b09e9b"
    ),
    "contracts/p2-i2/i04r2-machine-verification-validation.json": (
        "637c07cc7d31824f4806459f7b4e8ddd1262eec3c5cc874b009ea7767b59d361"
    ),
    "scripts/p2_i2_i04r2_calibration.py": (
        "8a0ef5569705ea0619a628b3b5a25d9dc80448a273a68a92d131ce775793b61a"
    ),
    "scripts/p2_i2_i04r2_validate.py": (
        "5417b5b9e7c488b3c0b1bc2f4d39ff292697e2358378c4e00e4787a3d13c7680"
    ),
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


def _projection_metadata(kind: str, source_sha256: str) -> dict[str, Any]:
    return {
        "change_id": "P2-I2-CHG-027",
        "decision_id": "P2-I2-DEC-034",
        "projection_kind": kind,
        "scientific_change": False,
        "source_commit": SOURCE_COMMIT,
        "source_sha256": source_sha256,
    }


def _portable_nested(value: Any) -> Any:
    if isinstance(value, list):
        return [_portable_nested(item) for item in value]
    if not isinstance(value, dict):
        if (
            isinstance(value, str)
            and value.startswith("configs/")
            and "common_control_rules" in value
            and "mode_control_rules" in value
        ):
            return {
                "artifact_path": value.split("#", 1)[0],
                "fields": ["common_control_rules", "mode_control_rules"],
            }
        return value

    projected = {key: _portable_nested(item) for key, item in value.items()}
    path = projected.get("path")
    if isinstance(path, str) and GRAPH_REPOSITORY_ID in path:
        marker = f"{GRAPH_REPOSITORY_ID}/"
        if marker not in path:
            raise AssertionError("historical graph source has no source-relative suffix")
        projected["repository_id"] = GRAPH_REPOSITORY_ID
        projected["path"] = path.split(marker, 1)[1]
    elif (
        isinstance(path, str)
        and ATTACHMENT_ID in path
        and path.endswith("pasted-text.txt")
    ):
        projected["attachment_id"] = ATTACHMENT_ID
        projected["path"] = "pasted-text.txt"
    return projected


def _project_json(
    raw: dict[str, Any], kind: str, source_sha256: str
) -> dict[str, Any]:
    projected = _portable_nested(deepcopy(raw))
    projected["portability_projection"] = _projection_metadata(kind, source_sha256)
    return projected


def _external_source_rows(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, list):
        for item in value:
            rows.extend(_external_source_rows(item))
    elif isinstance(value, dict):
        if value.get("repository_id") == GRAPH_REPOSITORY_ID and "path" in value:
            rows.append(value)
        for item in value.values():
            rows.extend(_external_source_rows(item))
    return rows


def _script_diff_allowed(relative: str, historical: str, current: str) -> bool:
    historical_lines = historical.splitlines()
    if not historical_lines or not historical_lines[0].startswith("#!"):
        raise AssertionError(f"historical shebang absent: {relative}")
    historical_shebang = historical_lines[0]
    removed: list[str] = []
    added: list[str] = []
    for line in difflib.ndiff(historical.splitlines(), current.splitlines()):
        if line.startswith("- "):
            removed.append(line[2:])
        elif line.startswith("+ "):
            added.append(line[2:])

    def allowed_removed(line: str) -> bool:
        return (
            line == historical_shebang
            or GRAPH_REPOSITORY_ID in line
            or "str(analysis_path)" in line
            or "str(calibration_path)" in line
            or "str(parent_analysis_path)" in line
            or "str(machine_policy_path)" in line
            or "_sha256(Path(row[\"path\"]))" in line
            or "packet_source = Path(source_rows[0][\"path\"])" in line
        )

    allowed_addition_fragments = (
        "GRAPH_REPOSITORY_ID",
        "GRAPH = ROOT.parent",
        "graph_repository_id",
        "graph_root = ROOT.parent",
        "graph repository identity drifted",
        "ROOT = Path(__file__).resolve().parents[3]",
        "_repository_relative_identity",
        "stable RCAE-relative identity",
        "path.resolve().relative_to(ROOT.resolve()).as_posix()",
        "except ValueError as exc:",
        "input path is outside the RCAE repository",
        "_external_source_path",
        "external source repository identity drifted",
        "external source path is not source-relative",
        "row.get(\"repository_id\")",
        "relative = Path(str(row[\"path\"]))",
        "relative.is_absolute()",
        "return GRAPH " + SEP + " relative",
        "for row in correction[\"public_source_semantics\"]",
        "for row in source_rows",
    )

    def allowed_added(line: str) -> bool:
        stripped = line.strip()
        return (
            not stripped
            or stripped
            in {
                ")",
                "sources_exact = all(",
                "try:",
                "if graph_repository_id != \"graph-reflexive-coherence\":",
            }
            or any(fragment in line for fragment in allowed_addition_fragments)
        )

    required = [historical_shebang]
    current_requirements = [historical_shebang]
    if relative.endswith("i04_validate.py"):
        required.append("graph_repository")
        current_requirements.extend(("graph_repository_id", "ROOT.parent"))
    if relative.endswith("_calibration.py"):
        required.append("str(")
        current_requirements.extend(("_repository_relative_identity", "ROOT = Path"))
    if relative.endswith("r1_validate.py") or relative.endswith("r2_validate.py"):
        required.append(GRAPH_REPOSITORY_ID)
        current_requirements.extend(("_external_source_path", "GRAPH = ROOT.parent"))

    return (
        bool(removed)
        and bool(added)
        and all(allowed_removed(line) for line in removed)
        and all(allowed_added(line) for line in added)
        and all(item in historical for item in required)
        and all(item not in current for item in current_requirements[:1])
        and all(item in current for item in current_requirements[1:])
    )


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY)
    freeze = _load(FREEZE)
    baseline = _load(BASELINE)
    lineage = _load(LINEAGE)

    if _sha256(POLICY) != freeze["policy_sha256"]:
        raise AssertionError("I05F policy identity drifted")
    if _sha256(BASELINE) != policy["baseline_audit"]["result_sha256"]:
        raise AssertionError("accepted I05D audit identity drifted")

    source_scope = {
        item["path"]: item["source_sha256"] for item in policy["correction_scope"]
    }
    baseline_scope = set(
        baseline["affected_files_by_group"]["i04_i05_authority_dependencies"]
    )
    baseline_violations = [
        item
        for item in baseline["violations"]
        if item["correction_group"] == "i04_i05_authority_dependencies"
    ]
    checks.append(
        _check(
            "I05F-01",
            "accepted exact I05D group",
            set(source_scope) == baseline_scope
            and len(source_scope) == 13
            and len(baseline_violations) == 30
            and all(
                item["file_sha256"] == source_scope[item["path"]]
                for item in baseline_violations
            ),
            "the scope is exactly the accepted thirteen-file thirty-finding I04/I05 dependency group",
            {"affected_files": 13, "baseline_violations": 30},
        )
    )

    historical_hashes = {
        relative: _sha256_bytes(_historical_bytes(SOURCE_COMMIT, relative))
        for relative in source_scope
    }
    checks.append(
        _check(
            "I05F-02",
            "historical source bytes",
            historical_hashes == source_scope,
            "every correction source reconstructs from the accepted I05E commit",
            {"source_commit": SOURCE_COMMIT, "source_file_count": len(source_scope)},
        )
    )

    projections = {item["path"]: item for item in lineage["projections"]}
    current_hashes = {relative: _sha256(ROOT / relative) for relative in source_scope}
    checks.append(
        _check(
            "I05F-03",
            "portable projection lineage identities",
            set(projections) == set(source_scope)
            and all(
                projections[path]["source_sha256"] == source_scope[path]
                and projections[path]["current_sha256"] == current_hashes[path]
                for path in source_scope
            ),
            "the lineage binds every historical and current byte without a checkout location",
            {"lineage_sha256": _sha256(LINEAGE), "projection_count": len(projections)},
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
            "I05F-04",
            "zero corrected-group path violations",
            not findings,
            "the corrected group and I05F package contain no persisted absolute-path violations",
            {"scanned_file_count": len(package_subjects), "violation_count": len(findings)},
        )
    )

    exact_json_count = 0
    for short_path, kind in JSON_PROJECTION_KINDS.items():
        relative = (EXPERIMENT / short_path).relative_to(ROOT).as_posix()
        raw = _historical_json(SOURCE_COMMIT, relative)
        expected = _project_json(raw, kind, source_scope[relative])
        if _load(ROOT / relative) != expected:
            raise AssertionError(f"JSON projection is not exact: {short_path}")
        exact_json_count += 1
    checks.append(
        _check(
            "I05F-05",
            "exact JSON historical-to-portable reconstruction",
            exact_json_count == 8,
            "all eight JSON artifacts equal their frozen path-only projection",
            {"exactly_reconstructed_json_projections": exact_json_count},
        )
    )

    python_paths = [path for path in source_scope if path.endswith(".py")]
    source_diffs_valid = True
    for relative in python_paths:
        historical = _historical_bytes(SOURCE_COMMIT, relative).decode("utf-8")
        current = (ROOT / relative).read_text(encoding="utf-8")
        ast.parse(current, filename=relative)
        source_diffs_valid = source_diffs_valid and _script_diff_allowed(
            relative, historical, current
        )
    checks.append(
        _check(
            "I05F-06",
            "bounded portable Python source corrections",
            source_diffs_valid and len(python_paths) == 5,
            "all five Python files parse and differ from history only on frozen path-portability surfaces",
            {"parsed_python_files": len(python_paths), "scientific_code_changes": 0},
        )
    )

    current_json = [
        _load(EXPERIMENT / short_path) for short_path in JSON_PROJECTION_KINDS
    ]
    source_rows = [
        row for artifact in current_json for row in _external_source_rows(artifact)
    ]
    sources_valid = all(
        row["repository_id"] == GRAPH_REPOSITORY_ID
        and not Path(row["path"]).is_absolute()
        and ".." not in Path(row["path"]).parts
        and _sha256(GRAPH / row["path"]) == row["sha256"]
        for row in source_rows
    )
    checks.append(
        _check(
            "I05F-07",
            "external source identity and current bytes",
            sources_valid and len(source_rows) == 18,
            "all projected PyGRC source identities resolve from the logical sibling repository and retain their accepted digests",
            {"repository_id": GRAPH_REPOSITORY_ID, "verified_source_rows": len(source_rows)},
        )
    )

    accepted_hashes = {
        short: _sha256_bytes(
            _historical_bytes(
                I04R2_COMMIT, (EXPERIMENT / short).relative_to(ROOT).as_posix()
            )
        )
        for short in I04R2_ACCEPTED
    }
    checks.append(
        _check(
            "I05F-08",
            "accepted I04R2 historical authority",
            accepted_hashes == I04R2_ACCEPTED,
            "the accepted I04R2 estimator measurement calibration and progression authority remains byte-addressable at its accepted commit",
            {"accepted_commit": I04R2_COMMIT, "verified_authority_files": len(accepted_hashes)},
        )
    )

    i05_current = {
        short: _sha256(EXPERIMENT / short) for short in I05_IMMUTABLE
    }
    i05_at_source_commit = {
        short: _sha256_bytes(
            _historical_bytes(
                SOURCE_COMMIT, (EXPERIMENT / short).relative_to(ROOT).as_posix()
            )
        )
        for short in I05_IMMUTABLE
    }
    final = _load(EXPERIMENT / "outputs/p2-i2/i05/i05b-final-receipt.json")
    checks.append(
        _check(
            "I05F-09",
            "immutable I05 execution evidence",
            i05_current == I05_IMMUTABLE
            and i05_at_source_commit == I05_IMMUTABLE
            and final["governed_attempt_count"] == 1
            and final["builder_invocation_count"] == 1
            and final["infrastructure_retries"] == 0
            and final["authorization_consumed"] is True
            and final["second_invocation_refused"] is True,
            "the I05 output projection claim projection and raw final receipt remain byte-unchanged with one consumed attempt and no retry",
            {
                "authorization_consumed": final["authorization_consumed"],
                "builder_invocation_count": final["builder_invocation_count"],
                "governed_attempt_count": final["governed_attempt_count"],
                "second_invocation_refused": final["second_invocation_refused"],
            },
        )
    )

    prior = freeze["prior_group_identities"]
    prior_exact = (
        _sha256_bytes(
            _historical_bytes(
                SOURCE_COMMIT,
                (EXPERIMENT / "contracts/p2-i2/i05e-portability-correction-validation.json")
                .relative_to(ROOT)
                .as_posix(),
            )
        )
        == prior["i05e_validation_sha256"]
        and _sha256_bytes(
            _historical_bytes(
                SOURCE_COMMIT,
                (EXPERIMENT / "contracts/p2-i2/i05e-portable-projection-lineage.json")
                .relative_to(ROOT)
                .as_posix(),
            )
        )
        == prior["i05e_lineage_sha256"]
    )
    invocation = policy["invocation_ceiling"]
    checks.append(
        _check(
            "I05F-10",
            "prior acceptance and zero-execution boundary",
            prior_exact
            and invocation["calibration_builder_invocations"] == 0
            and invocation["null_or_one_shot_wrapper_invocations"] == 0
            and invocation["pygrc_model_instantiations"] == 0
            and invocation["candidate_or_control_invocations"] == 0
            and invocation["conformance_or_scientific_invocations"] == 0,
            "accepted I05E authority is exact and I05F authorizes no builder wrapper PyGRC candidate control conformance or scientific operation",
            {
                "calibration_builder_invocations": 0,
                "candidate_or_control_invocations": 0,
                "null_or_one_shot_wrapper_invocations": 0,
                "pygrc_model_instantiations": 0,
                "scientific_result": False,
            },
        )
    )

    return {
        "activity_id": policy["activity_id"],
        "artifact_id": "P2-I2-I05F-I04-I05-AUTHORITY-DEPENDENCY-PORTABILITY-CORRECTION-VALIDATION",
        "artifact_version": "1.0.0",
        "calibration_builder_invocations": 0,
        "candidate_or_control_invocations": 0,
        "checks": checks,
        "corrected_file_count": len(source_scope),
        "corrected_group_violation_count": len(findings),
        "freeze_sha256": _sha256(FREEZE),
        "iteration_id": "P2-I2-I05F",
        "lane_id": "AE01-L02",
        "lineage_sha256": _sha256(LINEAGE),
        "null_or_one_shot_wrapper_invocations": 0,
        "passed_checks": len(checks),
        "policy_sha256": _sha256(POLICY),
        "pygrc_model_instantiations": 0,
        "result_status": "P2-I2-I05F-I04-I05-GROUP-REVIEW-READY",
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
        raise AssertionError(f"refusing to overwrite validation result: {args.output.name}")
    result = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(pretty_json_dumps(result), encoding="utf-8")
    print(
        f"P2-I2 I05F I04/I05 dependency portability correction: "
        f"{result['passed_checks']}/{result['total_checks']}; "
        f"corrected-group violations={result['corrected_group_violation_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
