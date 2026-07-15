"""Validate the fifth/final P2-I2 portability correction."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
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


POLICY = EXPERIMENT / "configs/p2_i2_i05i_portability_correction_policy.json"
FREEZE = EXPERIMENT / "contracts/p2-i2/i05i-portability-correction-input-freeze.json"
AUDIT_POLICY = EXPERIMENT / "configs/p2_i2_i05d_portability_audit_policy.json"
BASELINE = EXPERIMENT / "contracts/p2-i2/i05d-portability-audit.json"
LINEAGE = EXPERIMENT / "contracts/p2-i2/i05i-portable-projection-lineage.json"
REPORT = EXPERIMENT / "reports/P2-I2-I05I-portability-correction.md"
SOURCE_COMMIT = "1279e177d6691417a1d692dd8fdfc5cf50060e11"
GRAPH_REPOSITORY_ID = "graph-reflexive-coherence"
SEP = chr(47)
OWNER_IDENTIFIED_VALIDATORS = {
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i05g_validate.py",
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i05h_validate.py",
}
VALIDATOR_IDENTIFIED_CONSTRUCTOR_SOURCES = {
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i05f_validate.py",
}
CONSTRUCTOR_CORRECTION_SOURCES = (
    OWNER_IDENTIFIED_VALIDATORS | VALIDATOR_IDENTIFIED_CONSTRUCTOR_SOURCES
)


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


def _replace_once(value: str, old: str, new: str, label: str) -> str:
    if value.count(old) != 1:
        raise AssertionError(f"expected one historical replacement surface: {label}")
    return value.replace(old, new, 1)


def _absolute_token_span(value: str, marker: str) -> tuple[int, int]:
    marker_start = value.find(marker)
    if marker_start < 0:
        raise AssertionError(f"historical token marker absent: {marker}")
    boundaries = set(" \t\n\r\"'`=([{<,!")
    start = marker_start
    while start > 0 and value[start - 1] not in boundaries:
        start -= 1
    end = marker_start + len(marker)
    while end < len(value) and value[end] not in boundaries and value[end] not in "),]}>;":
        end += 1
    if value[start:start + 1] != SEP:
        raise AssertionError(f"historical marker is not inside an absolute token: {marker}")
    return start, end


def _replace_absolute_root(value: str, marker: str, replacement: str) -> str:
    start, _ = _absolute_token_span(value, marker)
    marker_end = value.find(marker, start) + len(marker)
    return value[:start] + replacement + value[marker_end:]


def _replace_absolute_token(value: str, marker: str, replacement: str) -> str:
    start, end = _absolute_token_span(value, marker)
    return value[:start] + replacement + value[end:]


def _replace_temporary_tokens(value: str) -> str:
    projected = value
    while True:
        starts = [
            index
            for index, character in enumerate(projected)
            if character == SEP
            and (index == 0 or projected[index - 1] in " \t\n\r\"'`=([{<,!")
        ]
        replaced = False
        for start in starts:
            name_start = start + 1
            name_end = name_start + len("tmp")
            next_character = projected[name_end:name_end + 1]
            if (
                projected[name_start:name_end] == "tmp"
                and (not next_character or next_character == SEP or next_character in " \t\n\r\"'`),]}>;:")
            ):
                prefix_end = name_end
                projected = projected[:start] + "${TMPDIR}" + projected[prefix_end:]
                replaced = True
                break
        if not replaced:
            return projected


def _remove_historical_shebang(value: str, label: str) -> str:
    lines = value.splitlines(keepends=True)
    if not lines or not lines[0].startswith("#!"):
        raise AssertionError(f"historical shebang absent: {label}")
    return "".join(lines[1:])


def _constructed_absolute_bindings(source: str, label: str) -> list[str]:
    tree = ast.parse(source, filename=label)
    findings: list[str] = []
    for statement in tree.body:
        if isinstance(statement, (ast.Assign, ast.AnnAssign)):
            targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
            value = statement.value
        else:
            continue
        names = [target.id for target in targets if isinstance(target, ast.Name)]
        referenced_names = {
            node.id for node in ast.walk(value) if isinstance(node, ast.Name)
        }
        for name in names:
            historical_constructor = name.startswith("OLD_") and "SEP" in referenced_names
            absolute_root_constructor = name.endswith("_ROOT") and "SEP" in referenced_names
            shebang_constructor = "SHEBANG" in name and "SEP" in referenced_names
            if historical_constructor or absolute_root_constructor or shebang_constructor:
                findings.append(name)
    return findings


def _i00_suffix() -> str:
    return "\n".join(
        (
            "",
            "## I05I portability projection",
            "",
            "This representation-only projection is governed by `P2-I2-DEC-039` and",
            "`P2-I2-CHG-032`. The graph command is historical non-executable provenance.",
            f"Raw bytes remain at commit `{SOURCE_COMMIT}`,",
            "SHA-256 `47fbd01b02327ac8ff08a0bc9e98431e92e3beaea121debe2c1e71e089f3c8b7`.",
            "No validation or gate meaning changed.",
            "",
        )
    )


def _readme_suffix() -> str:
    return "\n".join(
        (
            "",
            "## I05I portability projection",
            "",
            "Historical commands in this README are non-executable documentation. This",
            "representation-only projection is governed by `P2-I2-DEC-039` and",
            "`P2-I2-CHG-032`. Raw bytes remain at commit",
            f"`{SOURCE_COMMIT}`, SHA-256",
            "`94a0882655376b95a4618af861c712e86d587a88c36ee136e1057c00ab2aa11e`.",
            "No command authority, runtime, or scientific meaning changed.",
            "",
        )
    )


def _project_historical(relative: str, historical: str) -> str:
    name = Path(relative).name
    if name == "p2-i2-operational-hypotheses.md":
        return _replace_absolute_token(
            historical,
            "python3.12",
            "system-interpreter:python3.12",
        )
    if name == "P2-I2-decision-record.md":
        return _replace_absolute_token(
            historical,
            "python3.12",
            "system-interpreter:python3.12",
        )
    if name == "P2-I2-shared-pool-co-conditioning-checklist.md":
        return _replace_temporary_tokens(historical)
    if name == "P2-I2-I00-validation.md":
        return _replace_absolute_root(
            historical,
            GRAPH_REPOSITORY_ID,
            "${GRC}",
        ) + _i00_suffix()
    if name == "README.md":
        return _replace_temporary_tokens(historical) + _readme_suffix()
    if name == "p2_i2_calibration.py":
        return _remove_historical_shebang(historical, "calibration shebang")
    raise AssertionError(f"unrecognized terminal projection: {relative}")


def _diff_hunks(historical: str, current: str) -> list[str]:
    lines = list(
        difflib.unified_diff(
            historical.splitlines(),
            current.splitlines(),
            fromfile="historical",
            tofile="projected",
            n=2,
            lineterm="",
        )
    )
    hunks: list[list[str]] = []
    active: list[str] | None = None
    for line in lines:
        if line.startswith("@@"):
            active = [line]
            hunks.append(active)
        elif active is not None:
            active.append(line)
    return ["\n".join(hunk) for hunk in hunks]


def _governance_diff_allowed(relative: str, historical: str, current: str) -> bool:
    projected = _project_historical(relative, historical)
    hunks = _diff_hunks(projected, current)
    name = Path(relative).name
    markers = {
        "p2-i2-operational-hypotheses.md": (
            "3.2.20 I05I",
            "1279e17",
        ),
        "P2-I2-decision-record.md": (
            "P2-I2-DEC-039",
            "42. Pending decision queue",
        ),
        "P2-I2-shared-pool-co-conditioning-checklist.md": (
            "P2-I2-I05I",
            "P2-I2-CHG-032",
            "1279e17",
        ),
    }[name]
    return bool(hunks) and all(any(marker in hunk for marker in markers) for hunk in hunks)


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY)
    freeze = _load(FREEZE)
    audit_policy = _load(AUDIT_POLICY)
    baseline = _load(BASELINE)
    lineage = _load(LINEAGE)

    if _sha256(POLICY) != freeze["policy_sha256"]:
        raise AssertionError("I05I policy identity drifted")
    if _sha256(BASELINE) != policy["baseline_audit"]["result_sha256"]:
        raise AssertionError("accepted I05D audit identity drifted")
    if _sha256(AUDIT_POLICY) != policy["baseline_audit"]["audit_policy_sha256"]:
        raise AssertionError("accepted I05D audit policy identity drifted")
    if Path(sys.executable).resolve() != (ROOT / ".venv/bin/python").resolve():
        raise AssertionError("I05I validator must run through repository .venv")

    source_scope = {
        item["path"]: item["source_sha256"] for item in policy["correction_scope"]
    }
    baseline_scope = set(
        baseline["affected_files_by_group"]
        ["p2_i2_governance_navigation_and_shared_projections"]
    )
    baseline_findings = [
        item
        for item in baseline["violations"]
        if item["correction_group"]
        == "p2_i2_governance_navigation_and_shared_projections"
    ]
    owner_supplement = set(
        policy["owner_identified_constructed_root_supplement"]["paths"]
    )
    validator_supplement = set(
        policy["validator_identified_constructed_absolute_supplement"]["paths"]
    )
    checks.append(
        _check(
            "I05I-01",
            "accepted terminal I05D group plus owner-identified constructor supplement",
            set(source_scope) == baseline_scope | owner_supplement | validator_supplement
            and owner_supplement == OWNER_IDENTIFIED_VALIDATORS
            and validator_supplement == VALIDATOR_IDENTIFIED_CONSTRUCTOR_SOURCES
            and len(source_scope) == 9
            and len(baseline_findings) == 14
            and all(
                item["violation_class"] == "embedded_machine_local_absolute_token"
                for item in baseline_findings
            )
            and policy["baseline_audit"]["remaining_group_count"] == 1
            and policy["owner_identified_constructed_root_supplement"]
            ["constructed_root_surface_count"] == 3
            and policy["validator_identified_constructed_absolute_supplement"]
            ["constructed_absolute_surface_count"] == 1,
            "the accepted six-file/14-finding group is supplemented by three validators with four constructed absolute surfaces",
            {
                "accepted_audit_files": 6,
                "baseline_findings": 14,
                "constructed_root_surfaces": 3,
                "constructed_shebang_surfaces": 1,
                "correction_files": 9,
                "owner_identified_validators": 2,
                "validator_identified_sources": 1,
                "remaining_groups": 1,
            },
        )
    )

    historical_hashes = {
        relative: _sha256_bytes(_historical_bytes(relative))
        for relative in source_scope
    }
    checks.append(
        _check(
            "I05I-02",
            "historical source bytes",
            historical_hashes == source_scope,
            "every terminal-group source reconstructs from the accepted I05H commit",
            {"source_commit": SOURCE_COMMIT, "source_file_count": len(source_scope)},
        )
    )

    rows = {item["path"]: item for item in lineage["projection_rows"]}
    current_hashes = {relative: _sha256(ROOT / relative) for relative in source_scope}
    checks.append(
        _check(
            "I05I-03",
            "portable projection lineage identities",
            lineage["file_count"] == 9
            and lineage["scientific_change"] is False
            and set(rows) == set(source_scope)
            and all(
                rows[path]["source_sha256"] == source_scope[path]
                and rows[path]["projection_sha256"] == current_hashes[path]
                for path in source_scope
            ),
            "the lineage binds all nine historical and projected bytes",
            {"lineage_sha256": _sha256(LINEAGE), "projection_count": len(rows)},
        )
    )

    scope_files = portability_audit._scope_files(audit_policy)
    terminal_findings: list[dict[str, Any]] = []
    for path in scope_files:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix == ".json":
            terminal_findings.extend(portability_audit._scan_json(path, relative))
        else:
            terminal_findings.extend(portability_audit._scan_text(path, relative))
    constructor_scope = set(scope_files) | {
        ROOT / relative for relative in CONSTRUCTOR_CORRECTION_SOURCES
    } | {Path(__file__).resolve()}
    constructed_bindings = {
        path.relative_to(ROOT).as_posix(): _constructed_absolute_bindings(
            path.read_text(encoding="utf-8"),
            path.relative_to(ROOT).as_posix(),
        )
        for path in sorted(constructor_scope)
        if path.suffix == ".py"
        and _constructed_absolute_bindings(
            path.read_text(encoding="utf-8"),
            path.relative_to(ROOT).as_posix(),
        )
    }
    checks.append(
        _check(
            "I05I-04",
            "complete current P2-I2 audit scope is portable",
            not terminal_findings and not constructed_bindings,
            "the complete current accepted P2-I2 scope contains zero literal or constructed absolute-path findings",
            {
                "constructed_absolute_binding_count": 0,
                "scanned_file_count": len(scope_files),
                "violation_count": 0,
            },
        )
    )

    exact_names = {
        "P2-I2-I00-validation.md",
        "README.md",
        "p2_i2_calibration.py",
    }
    exact_count = 0
    for relative in source_scope:
        if Path(relative).name not in exact_names:
            continue
        historical = _historical_bytes(relative).decode("utf-8")
        current = (ROOT / relative).read_text(encoding="utf-8")
        if current != _project_historical(relative, historical):
            raise AssertionError(f"non-governance projection is not exact: {relative}")
        if relative.endswith(".py"):
            ast.parse(current, filename=relative)
        exact_count += 1
    validator_historical_findings = {
        relative: _constructed_absolute_bindings(
            _historical_bytes(relative).decode("utf-8"),
            relative + "@" + SOURCE_COMMIT,
        )
        for relative in CONSTRUCTOR_CORRECTION_SOURCES
    }
    validator_current_findings = {
        relative: _constructed_absolute_bindings(
            (ROOT / relative).read_text(encoding="utf-8"),
            relative,
        )
        for relative in CONSTRUCTOR_CORRECTION_SOURCES
    }
    validator_ast_valid = all(
        ast.parse(
            (ROOT / relative).read_text(encoding="utf-8"),
            filename=relative,
        )
        for relative in CONSTRUCTOR_CORRECTION_SOURCES
    )
    checks.append(
        _check(
            "I05I-05",
            "exact projections and constructed-root removal",
            exact_count == 3
            and validator_ast_valid
            and all(validator_historical_findings.values())
            and not any(validator_current_findings.values()),
            "three ordinary projections are exact and all three validator sources replace constructed absolute constants with retained-source-driven logic",
            {
                "exact_projection_count": exact_count,
                "historical_constructed_binding_count": sum(
                    len(items) for items in validator_historical_findings.values()
                ),
                "validator_projection_count": len(validator_current_findings),
            },
        )
    )

    governance_names = {
        "p2-i2-operational-hypotheses.md",
        "P2-I2-decision-record.md",
        "P2-I2-shared-pool-co-conditioning-checklist.md",
    }
    governance_paths = [
        relative
        for relative in source_scope
        if Path(relative).name in governance_names
    ]
    governance_allowed = all(
        _governance_diff_allowed(
            relative,
            _historical_bytes(relative).decode("utf-8"),
            (ROOT / relative).read_text(encoding="utf-8"),
        )
        for relative in governance_paths
    )
    checks.append(
        _check(
            "I05I-06",
            "bounded self-governance projections",
            governance_allowed and len(governance_paths) == 3,
            "all self-governance diff hunks are confined to I05H acceptance I05I/DEC-039/CHG-032 closeout owner-identified scope correction or frozen path substitutions",
            {"bounded_governance_files": len(governance_paths)},
        )
    )

    raw_hypothesis = _historical_bytes(
        next(path for path in source_scope if path.endswith("operational-hypotheses.md"))
    ).decode("utf-8")
    current_hypothesis = (
        ROOT / next(path for path in source_scope if path.endswith("operational-hypotheses.md"))
    ).read_text(encoding="utf-8")
    raw_science = raw_hypothesis.split("### 3.3 I03A", 1)[1]
    current_science = current_hypothesis.split("### 3.3 I03A", 1)[1]
    op_counts_equal = Counter(
        token for token in raw_science.split() if "H-L02-OP-" in token
    ) == Counter(token for token in current_science.split() if "H-L02-OP-" in token)
    checks.append(
        _check(
            "I05I-07",
            "scientific hypothesis body unchanged",
            raw_science == current_science and op_counts_equal,
            "the complete I03-and-later operational hypothesis body is byte-unchanged",
            {"scientific_change": False},
        )
    )

    calibration = (
        EXPERIMENT / "scripts/p2_i2_calibration.py"
    ).read_text(encoding="utf-8")
    checks.append(
        _check(
            "I05I-08",
            "portable explicit-venv script boundary",
            not calibration.startswith("#!")
            and policy["transformation_rules"]["script_entry"].endswith(
                ".venv/bin/python"
            ),
            "the calibration source is parsed but not imported and requires explicit repository-venv invocation",
            {"interpreter_identity": ".venv/bin/python", "module_imported": False},
        )
    )

    prior = freeze["prior_group_identities"]
    prior_paths = {
        "I05H_lineage_sha256": "contracts/p2-i2/i05h-portable-projection-lineage.json",
        "I05H_validation_sha256": "contracts/p2-i2/i05h-portability-correction-validation.json",
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
            "I05I-09",
            "prior accepted group authority",
            prior["I05H_commit"] == SOURCE_COMMIT
            and prior_current == {key: prior[key] for key in prior_paths}
            and prior_historical == {key: prior[key] for key in prior_paths},
            "I05H commit validation and lineage identities remain exact",
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
            "I05I-10",
            "zero-execution and progression boundary",
            all(ceiling[key] == 0 for key in zero_keys)
            and ceiling["I05I_validator_entrypoint_starts"] == 3
            and freeze["later_correction_groups_authorized"] is False
            and freeze["scientific_change_authorized"] is False,
            "I05I remains static portability validation with no runtime/scientific or automatic CAL-GATE authority",
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
        "artifact_id": "P2-I2-I05I-TERMINAL-PORTABILITY-CORRECTION-VALIDATION",
        "artifact_version": "1.0.0",
        "calibration_builder_invocations": 0,
        "candidate_or_control_invocations": 0,
        "checks": checks,
        "complete_current_scope_violation_count": len(terminal_findings),
        "constructed_absolute_binding_count": sum(
            len(items) for items in constructed_bindings.values()
        ),
        "constructor_correction_source_count": len(CONSTRUCTOR_CORRECTION_SOURCES),
        "corrected_file_count": len(source_scope),
        "corrected_group_violation_count": 0,
        "failed_closed_pre_output_starts": 2,
        "freeze_sha256": _sha256(FREEZE),
        "interpreter_identity": ".venv/bin/python",
        "iteration_id": "P2-I2-I05I",
        "lane_id": "AE01-L02",
        "lineage_sha256": _sha256(LINEAGE),
        "null_or_one_shot_wrapper_invocations": 0,
        "other_python_process_starts": 0,
        "passed_checks": len(checks),
        "policy_sha256": _sha256(POLICY),
        "pygrc_imports_or_model_instantiations": 0,
        "result_status": "P2-I2-I05I-TERMINAL-GROUP-REVIEW-READY",
        "scientific_result": False,
        "total_checks": len(checks),
        "validator_entrypoint_starts": 3,
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
        "P2-I2 I05I terminal portability correction: "
        f"{result['passed_checks']}/{result['total_checks']}; "
        f"complete-scope violations={result['complete_current_scope_violation_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
