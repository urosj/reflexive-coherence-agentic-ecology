"""Validate the bounded I01/I02 source-and-identity portability correction."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
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


POLICY = EXPERIMENT / "configs/p2_i2_i05h_portability_correction_policy.json"
FREEZE = EXPERIMENT / "contracts/p2-i2/i05h-portability-correction-input-freeze.json"
BASELINE = EXPERIMENT / "contracts/p2-i2/i05d-portability-audit.json"
LINEAGE = EXPERIMENT / "contracts/p2-i2/i05h-portable-projection-lineage.json"
REPORT = EXPERIMENT / "reports/P2-I2-I05H-portability-correction.md"
SOURCE_COMMIT = "62882efc5ecf3c131d21345ad89796f0b2ebccb7"
GRAPH_REPOSITORY_ID = "graph-reflexive-coherence"
SEP = chr(47)
OLD_GRAPH_ROOT = SEP + SEP.join(
    ("home", "uros", "Documents", "RC-github", GRAPH_REPOSITORY_ID)
)
OLD_TEMP_ROOT = SEP + "tmp"
PORTABLE_SHEBANG = "#!" + SEP + "usr/bin/env python3"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected object: {path.relative_to(ROOT).as_posix()}")
    return value


def _historical_bytes(relative: str) -> bytes:
    return subprocess.run(
        ("git", "-C", str(ROOT), "show", f"{SOURCE_COMMIT}:{relative}"),
        check=True,
        capture_output=True,
    ).stdout


def _historical_json(relative: str) -> dict[str, Any]:
    value = json.loads(_historical_bytes(relative))
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


def _metadata(source_sha256: str) -> dict[str, Any]:
    return {
        "change_id": "P2-I2-CHG-031",
        "decision_id": "P2-I2-DEC-038",
        "projected_commands_executable": False,
        "projection_kind": "historical_portability_projection",
        "scientific_change": False,
        "source_commit": SOURCE_COMMIT,
        "source_sha256": source_sha256,
    }


def _project_nested(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace(
            OLD_GRAPH_ROOT,
            "external-repository:" + GRAPH_REPOSITORY_ID,
        ).replace(OLD_TEMP_ROOT, "${TMPDIR}")
    if isinstance(value, list):
        return [_project_nested(item) for item in value]
    if isinstance(value, dict):
        return {key: _project_nested(item) for key, item in value.items()}
    return value


def _project_json(raw: dict[str, Any], source_sha256: str) -> dict[str, Any]:
    projected = _project_nested(deepcopy(raw))
    if not isinstance(projected, dict):
        raise AssertionError("projected JSON root is not an object")
    projected["portability_projection"] = _metadata(source_sha256)
    return projected


def _replace_once(value: str, old: str, new: str, label: str) -> str:
    if value.count(old) != 1:
        raise AssertionError(f"expected one historical replacement surface: {label}")
    return value.replace(old, new, 1)


def _report_suffix(name: str, source_sha256: str) -> str:
    common = [
        "",
        "## I05H portability projection",
        "",
    ]
    if name == "P2-I2-I01-command-provenance.md":
        body = [
            "This is a representation-only projection under `P2-I2-DEC-038` and",
            "`P2-I2-CHG-031`. Historical commands are non-executable provenance. Raw bytes",
            f"remain at commit `{SOURCE_COMMIT}`, SHA-256",
            f"`{source_sha256}`.",
            "No capability or scientific meaning changed.",
        ]
    elif name == "P2-I2-I01R1-capability-audit-closeout-revalidation.md":
        body = [
            "This is a representation-only projection under `P2-I2-DEC-038` and",
            "`P2-I2-CHG-031`. Raw bytes remain at commit",
            f"`{SOURCE_COMMIT}`, SHA-256",
            f"`{source_sha256}`.",
            "No source-audit, capability, quarantine, or scientific meaning changed.",
        ]
    elif name == "P2-I2-I02R1-admission-closeout-revalidation.md":
        body = [
            "This is a representation-only projection under `P2-I2-DEC-038` and",
            "`P2-I2-CHG-031`. Raw bytes remain at commit",
            f"`{SOURCE_COMMIT}`, SHA-256",
            f"`{source_sha256}`.",
            "No source-admission, identity-authority, or scientific meaning changed.",
        ]
    else:
        raise AssertionError(f"unrecognized report projection: {name}")
    return "\n".join(common + body + [""])


def _expected_report(relative: str, historical: str, source_sha256: str) -> str:
    name = Path(relative).name
    value = historical
    if name == "P2-I2-I01-command-provenance.md":
        old = "below denotes `" + OLD_GRAPH_ROOT + "`."
        new = "below denotes the logical sibling checkout `${GRC}`."
        value = _replace_once(value, old, new, name + " graph notation")
    value = value.replace(OLD_GRAPH_ROOT, "${GRC}")
    value = value.replace(OLD_TEMP_ROOT, "${TMPDIR}")
    return value + _report_suffix(name, source_sha256)


def _expected_script(relative: str, historical: str) -> str:
    value = _replace_once(
        historical,
        PORTABLE_SHEBANG + "\n",
        "",
        relative + " shebang",
    )
    if Path(relative).name == "p2_i2_i02r2_validate.py":
        old = 'tempfile.TemporaryDirectory(dir="' + OLD_TEMP_ROOT + '")'
        if value.count(old) != 5:
            raise AssertionError("expected five fixed temporary-directory surfaces")
        value = value.replace(old, "tempfile.TemporaryDirectory()")
    return value


def _external_identity_values(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, str) and value.startswith("external-repository:"):
        values.append(value)
    elif isinstance(value, list):
        for item in value:
            values.extend(_external_identity_values(item))
    elif isinstance(value, dict):
        for item in value.values():
            values.extend(_external_identity_values(item))
    return values


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY)
    freeze = _load(FREEZE)
    baseline = _load(BASELINE)
    lineage = _load(LINEAGE)

    if _sha256(POLICY) != freeze["policy_sha256"]:
        raise AssertionError("I05H policy identity drifted")
    if _sha256(BASELINE) != policy["baseline_audit"]["result_sha256"]:
        raise AssertionError("accepted I05D audit identity drifted")
    if Path(sys.executable).resolve() != (ROOT / ".venv/bin/python").resolve():
        raise AssertionError("I05H validator must run through repository .venv")

    source_scope = {
        item["path"]: item["source_sha256"] for item in policy["correction_scope"]
    }
    baseline_scope = set(
        baseline["affected_files_by_group"]["i01_i02_source_and_identity"]
    )
    baseline_findings = [
        item
        for item in baseline["violations"]
        if item["correction_group"] == "i01_i02_source_and_identity"
    ]
    class_counts = {
        class_name: sum(
            item["violation_class"] == class_name for item in baseline_findings
        )
        for class_name in policy["baseline_audit"]["violation_classes"]
    }
    checks.append(
        _check(
            "I05H-01",
            "accepted exact fourth I05D group",
            set(source_scope) == baseline_scope
            and len(source_scope) == 10
            and len(baseline_findings) == 35
            and class_counts == policy["baseline_audit"]["violation_classes"]
            and all(
                item["file_sha256"] == source_scope[item["path"]]
                for item in baseline_findings
            ),
            "the scope is exactly the accepted ten-file 35-finding I01/I02 group",
            {"affected_files": 10, "baseline_findings": 35, "class_counts": class_counts},
        )
    )

    historical_hashes = {
        relative: _sha256_bytes(_historical_bytes(relative))
        for relative in source_scope
    }
    checks.append(
        _check(
            "I05H-02",
            "historical source bytes",
            historical_hashes == source_scope,
            "every source reconstructs from the accepted I05G commit",
            {"source_commit": SOURCE_COMMIT, "source_file_count": len(source_scope)},
        )
    )

    rows = {item["path"]: item for item in lineage["projection_rows"]}
    current_hashes = {relative: _sha256(ROOT / relative) for relative in source_scope}
    checks.append(
        _check(
            "I05H-03",
            "portable projection lineage identities",
            lineage["file_count"] == 10
            and lineage["scientific_change"] is False
            and set(rows) == set(source_scope)
            and all(
                rows[path]["source_sha256"] == source_scope[path]
                and rows[path]["projection_sha256"] == current_hashes[path]
                for path in source_scope
            ),
            "the lineage binds all historical and projected bytes",
            {"lineage_sha256": _sha256(LINEAGE), "projection_count": len(rows)},
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
            "I05H-04",
            "zero corrected-group path violations",
            not findings,
            "the ten corrected files and I05H package contain no persisted absolute paths",
            {"scanned_file_count": len(package_subjects), "violation_count": 0},
        )
    )

    json_paths = [path for path in source_scope if path.endswith(".json")]
    current_json: list[dict[str, Any]] = []
    for relative in json_paths:
        expected = _project_json(_historical_json(relative), source_scope[relative])
        current = _load(ROOT / relative)
        if current != expected:
            raise AssertionError(f"JSON projection is not exact: {relative}")
        current_json.append(current)
    checks.append(
        _check(
            "I05H-05",
            "exact JSON historical-to-portable reconstruction",
            len(json_paths) == 4,
            "all four JSON files equal their frozen representation-only projections",
            {"exactly_reconstructed_json_projections": len(json_paths)},
        )
    )

    report_paths = [path for path in source_scope if path.endswith(".md")]
    reports_exact = all(
        (ROOT / relative).read_text(encoding="utf-8")
        == _expected_report(
            relative,
            _historical_bytes(relative).decode("utf-8"),
            source_scope[relative],
        )
        for relative in report_paths
    )
    checks.append(
        _check(
            "I05H-06",
            "exact historical report projections",
            reports_exact and len(report_paths) == 3,
            "all three reports differ only on frozen location representation and additive lineage",
            {"exactly_reconstructed_report_projections": len(report_paths)},
        )
    )

    python_paths = [path for path in source_scope if path.endswith(".py")]
    scripts_exact = True
    for relative in python_paths:
        historical = _historical_bytes(relative).decode("utf-8")
        current = (ROOT / relative).read_text(encoding="utf-8")
        scripts_exact = scripts_exact and current == _expected_script(relative, historical)
        ast.parse(current, filename=relative)
    reset_validator = (
        EXPERIMENT / "scripts/p2_i2_i02r2_validate.py"
    ).read_text(encoding="utf-8")
    checks.append(
        _check(
            "I05H-07",
            "bounded portable Python source corrections",
            scripts_exact
            and len(python_paths) == 3
            and reset_validator.count("tempfile.TemporaryDirectory()") == 5
            and "TemporaryDirectory(dir=" not in reset_validator,
            "three Python sources parse and differ only by shebang removal and five system-selected temporary directories",
            {"parsed_python_files": 3, "system_selected_temporary_contexts": 5},
        )
    )

    external_values = [
        item for document in current_json for item in _external_identity_values(document)
    ]
    metadata_exact = all(
        document["portability_projection"] == _metadata(source_scope[relative])
        for document, relative in zip(current_json, json_paths)
    )
    checks.append(
        _check(
            "I05H-08",
            "logical identities and immutable semantics",
            metadata_exact
            and len(external_values) == 11
            and all(
                value.startswith("external-repository:" + GRAPH_REPOSITORY_ID)
                for value in external_values
            ),
            "all eleven graph identities are logical and every JSON projection declares zero scientific change",
            {"logical_external_identities": len(external_values), "scientific_change": False},
        )
    )

    prior = freeze["prior_group_identities"]
    prior_paths = {
        "I05G_lineage_sha256": "contracts/p2-i2/i05g-portable-projection-lineage.json",
        "I05G_validation_sha256": "contracts/p2-i2/i05g-portability-correction-validation.json",
    }
    prior_current = {
        key: _sha256(EXPERIMENT / short) for key, short in prior_paths.items()
    }
    prior_historical = {
        key: _sha256_bytes(
            _historical_bytes((EXPERIMENT / short).relative_to(ROOT).as_posix())
        )
        for key, short in prior_paths.items()
    }
    checks.append(
        _check(
            "I05H-09",
            "prior accepted group authority",
            prior["I05G_commit"] == SOURCE_COMMIT
            and prior_current == {key: prior[key] for key in prior_paths}
            and prior_historical == {key: prior[key] for key in prior_paths},
            "I05G commit validation and lineage identities remain exact",
            {"prior_identity_count": len(prior_paths), "source_commit": SOURCE_COMMIT},
        )
    )

    ceiling = policy["invocation_ceiling_after_freeze"]
    zero_keys = (
        "calibration_builder_invocations",
        "candidate_or_control_invocations",
        "conformance_or_scientific_invocations",
        "null_or_one_shot_wrapper_invocations",
        "other_python_process_starts",
        "pygrc_imports_or_model_instantiations",
    )
    checks.append(
        _check(
            "I05H-10",
            "zero-execution and progression boundary",
            all(ceiling[key] == 0 for key in zero_keys)
            and ceiling["I05H_validator_entrypoint_starts"] == 3
            and freeze["later_correction_groups_authorized"] is False
            and freeze["scientific_change_authorized"] is False,
            "I05H remains static portability validation with no runtime/scientific or fifth-group authority",
            {
                "candidate_or_control_invocations": 0,
                "conformance_or_scientific_invocations": 0,
                "other_python_process_starts": 0,
                "pygrc_imports_or_model_instantiations": 0,
                "scientific_result": False,
            },
        )
    )

    return {
        "activity_id": policy["activity_id"],
        "artifact_id": "P2-I2-I05H-I01-I02-PORTABILITY-CORRECTION-VALIDATION",
        "artifact_version": "1.0.0",
        "calibration_builder_invocations": 0,
        "candidate_or_control_invocations": 0,
        "checks": checks,
        "corrected_file_count": len(source_scope),
        "corrected_group_violation_count": len(findings),
        "failed_closed_pre_output_starts": 0,
        "freeze_sha256": _sha256(FREEZE),
        "interpreter_identity": ".venv/bin/python",
        "iteration_id": "P2-I2-I05H",
        "lane_id": "AE01-L02",
        "lineage_sha256": _sha256(LINEAGE),
        "null_or_one_shot_wrapper_invocations": 0,
        "other_python_process_starts": 0,
        "passed_checks": len(checks),
        "policy_sha256": _sha256(POLICY),
        "pygrc_imports_or_model_instantiations": 0,
        "result_status": "P2-I2-I05H-I01-I02-GROUP-REVIEW-READY",
        "scientific_result": False,
        "total_checks": len(checks),
        "validator_entrypoint_starts": 1,
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
        "P2-I2 I05H I01/I02 portability correction: "
        f"{result['passed_checks']}/{result['total_checks']}; "
        f"corrected-group violations={result['corrected_group_violation_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
