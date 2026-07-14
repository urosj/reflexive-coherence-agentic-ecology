"""Validate the bounded I03 realization/conformance portability correction."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import pretty_json_dumps  # noqa: E402
import p2_i2_i05d_portability_audit as portability_audit  # noqa: E402


POLICY = EXPERIMENT / "configs/p2_i2_i05g_portability_correction_policy.json"
FREEZE = EXPERIMENT / "contracts/p2-i2/i05g-portability-correction-input-freeze.json"
BASELINE = EXPERIMENT / "contracts/p2-i2/i05d-portability-audit.json"
LINEAGE = EXPERIMENT / "contracts/p2-i2/i05g-portable-projection-lineage.json"
REPORT = EXPERIMENT / "reports/P2-I2-I05G-portability-correction.md"
SOURCE_COMMIT = "99c64dd20db1cf83b79e8bfdf2ac956f7ec46b50"
GRAPH_REPOSITORY_ID = "graph-reflexive-coherence"
SEP = chr(47)
PORTABLE_SHEBANG = "#!" + SEP + "usr/bin/env python3"
OLD_RCAE_ROOT = SEP + SEP.join(
    ("home", "uros", "Documents", "RC-github", "reflexive-coherence-agentic-ecology")
)
OLD_GRAPH_ROOT = SEP + SEP.join(
    ("home", "uros", "Documents", "RC-github", GRAPH_REPOSITORY_ID)
)
OLD_TEMP_PREFIX = SEP + "tmp" + SEP
ATTACHMENTS = (
    "050693b2-7c8a-4ad4-8506-0f39985a0a7a",
    "b9e2a79f-b3d2-480d-a019-f78701836a7b",
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
        "change_id": "P2-I2-CHG-030",
        "decision_id": "P2-I2-DEC-037",
        "projected_commands_executable": False,
        "projection_kind": "historical_portability_projection",
        "scientific_change": False,
        "source_commit": SOURCE_COMMIT,
        "source_sha256": source_sha256,
    }


def _structured_pointer(value: str) -> dict[str, Any]:
    parts = value[1:].split(SEP)
    return {
        "segments": [int(part) if part.isdigit() else part for part in parts]
    }


def _project_string(value: str) -> Any:
    projected = value
    projected = projected.replace(
        OLD_RCAE_ROOT + SEP + ".venv" + SEP + "bin" + SEP + "python",
        ".venv/bin/python",
    )
    projected = projected.replace(OLD_RCAE_ROOT + SEP + ".venv", ".venv")
    projected = projected.replace(
        OLD_GRAPH_ROOT,
        "external-repository:" + GRAPH_REPOSITORY_ID,
    )
    projected = projected.replace(OLD_TEMP_PREFIX, "temporary-output:")
    for attachment_id in ATTACHMENTS:
        old = (
            SEP
            + SEP.join(("home", "uros", ".codex", "attachments", attachment_id))
            + SEP
            + "pasted-text.txt"
        )
        projected = projected.replace(
            old,
            "attachment:" + attachment_id + SEP + "pasted-text.txt",
        )
    if projected == SEP + "usr":
        projected = "base-runtime:system"
    if projected.startswith(SEP):
        return _structured_pointer(projected)
    return projected


def _project_nested(value: Any) -> Any:
    if isinstance(value, str):
        return _project_string(value)
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


def _expected_script(relative: str, historical: str) -> str:
    value = _replace_once(
        historical,
        PORTABLE_SHEBANG + "\n",
        "",
        relative + " shebang",
    )
    name = Path(relative).name
    if name in {
        "p2_i2_i03ar1_conform.py",
        "p2_i2_i03b_conform.py",
        "p2_i2_i03c_conform.py",
    }:
        value = _replace_once(
            value,
            'GRAPH_ROOT = Path("' + OLD_GRAPH_ROOT + '")',
            'GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"',
            name + " graph root",
        )
        value = _replace_once(
            value,
            '        "pygrc_import_file": str(actual_import),',
            "\n".join(
                (
                    '        "pygrc_import_identity": {',
                    '            "repository_id": "graph-reflexive-coherence",',
                    '            "path": "src/pygrc/__init__.py",',
                    "        },",
                )
            ),
            name + " import identity",
        )
        value = _replace_once(
            value,
            "\n".join(
                (
                    '        "sys_executable": sys.executable,',
                    '        "sys_prefix": sys.prefix,',
                )
            ),
            "\n".join(
                (
                    '        "invoked_executable_repo_relative": ".venv/bin/python",',
                    '        "venv_prefix_repo_relative": ".venv",',
                )
            ),
            name + " venv identity",
        )
    elif name == "p2_i2_i03f_validate.py":
        old_function = "\n".join(
            (
                "def _pointer(document: Mapping[str, Any], pointer: str) -> Any:",
                "    value: Any = document",
                '    for part in pointer.strip("' + SEP + '").split("' + SEP + '"):',
                "        if isinstance(value, list):",
                "            value = value[int(part)]",
                "        else:",
                "            value = value[part]",
                "    return value",
            )
        )
        new_function = "\n".join(
            (
                "def _pointer(document: Mapping[str, Any], pointer: Mapping[str, Any]) -> Any:",
                '    if set(pointer) != {"segments"} or not isinstance(pointer["segments"], list):',
                '        raise AssertionError("pointer must be a structured ordered segment list")',
                "    value: Any = document",
                '    for part in pointer["segments"]:',
                "        if isinstance(value, list):",
                "            if not isinstance(part, int):",
                '                raise AssertionError("list pointer segment must be an integer")',
                "            value = value[part]",
                "        else:",
                "            if not isinstance(part, str):",
                '                raise AssertionError("mapping pointer segment must be a string")',
                "            value = value[part]",
                "    return value",
            )
        )
        value = _replace_once(value, old_function, new_function, name + " pointer reader")
        value = _replace_once(
            value,
            '            if pointer != f"' + SEP + 'operational_projections/{position}":',
            '            if pointer != {"segments": ["operational_projections", position]}:',
            name + " pointer expectation",
        )
    return value


def _expected_report(historical: str) -> str:
    old = (
        "The retained conformance artifact and `"
        + SEP
        + "tmp` reconstruction both have SHA-256"
    )
    new = (
        "The retained conformance artifact and the logical temporary-output "
        "reconstruction both have SHA-256"
    )
    return _replace_once(historical, old, new, "I03AR1 report temporary identity")


def _legacy_pointer(document: Any, pointer: str) -> Any:
    value = document
    for part in pointer[1:].split(SEP):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def _portable_pointer(document: Any, pointer: Mapping[str, Any]) -> Any:
    if set(pointer) != {"segments"} or not isinstance(pointer["segments"], list):
        raise AssertionError("invalid structured pointer")
    value = document
    for part in pointer["segments"]:
        value = value[part]
    return value


def _collect_pointer_pairs(raw: Any, projected: Any) -> list[tuple[str, Mapping[str, Any]]]:
    pairs: list[tuple[str, Mapping[str, Any]]] = []
    if isinstance(raw, str) and raw.startswith(SEP):
        if not isinstance(projected, dict):
            raise AssertionError("legacy pointer did not become a structured pointer")
        pairs.append((raw, projected))
    elif isinstance(raw, list):
        if not isinstance(projected, list) or len(raw) != len(projected):
            raise AssertionError("pointer projection list shape drifted")
        for left, right in zip(raw, projected):
            pairs.extend(_collect_pointer_pairs(left, right))
    elif isinstance(raw, dict):
        if not isinstance(projected, dict):
            raise AssertionError("pointer projection object shape drifted")
        for key, item in raw.items():
            pairs.extend(_collect_pointer_pairs(item, projected[key]))
    return pairs


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY)
    freeze = _load(FREEZE)
    baseline = _load(BASELINE)
    lineage = _load(LINEAGE)

    if _sha256(POLICY) != freeze["policy_sha256"]:
        raise AssertionError("I05G policy identity drifted")
    if _sha256(BASELINE) != policy["baseline_audit"]["result_sha256"]:
        raise AssertionError("accepted I05D audit identity drifted")
    if Path(sys.executable).resolve() != (ROOT / ".venv/bin/python").resolve():
        raise AssertionError("I05G validator must run through repository .venv")

    source_scope = {
        item["path"]: item["source_sha256"] for item in policy["correction_scope"]
    }
    baseline_scope = set(
        baseline["affected_files_by_group"]["i03_realization_and_conformance"]
    )
    baseline_findings = [
        item
        for item in baseline["violations"]
        if item["correction_group"] == "i03_realization_and_conformance"
    ]
    checks.append(
        _check(
            "I05G-01",
            "accepted exact third I05D group",
            set(source_scope) == baseline_scope
            and len(source_scope) == 30
            and len(baseline_findings) == 201
            and all(
                item["file_sha256"] == source_scope[item["path"]]
                for item in baseline_findings
            ),
            "the scope is exactly the accepted thirty-file 201-finding I03 group",
            {"affected_files": 30, "baseline_findings": 201},
        )
    )

    historical_hashes = {
        relative: _sha256_bytes(_historical_bytes(relative))
        for relative in source_scope
    }
    checks.append(
        _check(
            "I05G-02",
            "historical source bytes",
            historical_hashes == source_scope,
            "every source reconstructs from the accepted I05F commit",
            {"source_commit": SOURCE_COMMIT, "source_file_count": len(source_scope)},
        )
    )

    rows = {item["path"]: item for item in lineage["projection_rows"]}
    current_hashes = {relative: _sha256(ROOT / relative) for relative in source_scope}
    checks.append(
        _check(
            "I05G-03",
            "portable projection lineage identities",
            lineage["file_count"] == 30
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
            "I05G-04",
            "zero corrected-group path violations",
            not findings,
            "the 30 corrected files and I05G package contain no persisted absolute paths",
            {"scanned_file_count": len(package_subjects), "violation_count": 0},
        )
    )

    json_paths = [path for path in source_scope if path.endswith(".json")]
    for relative in json_paths:
        expected = _project_json(_historical_json(relative), source_scope[relative])
        if _load(ROOT / relative) != expected:
            raise AssertionError(f"JSON projection is not exact: {relative}")
    checks.append(
        _check(
            "I05G-05",
            "exact JSON historical-to-portable reconstruction",
            len(json_paths) == 20,
            "all 20 JSON files equal their frozen representation-only projections",
            {"exactly_reconstructed_json_projections": len(json_paths)},
        )
    )

    python_paths = [path for path in source_scope if path.endswith(".py")]
    for relative in python_paths:
        historical = _historical_bytes(relative).decode("utf-8")
        expected = _expected_script(relative, historical)
        current = (ROOT / relative).read_text(encoding="utf-8")
        if current != expected:
            raise AssertionError(f"Python correction exceeds frozen surfaces: {relative}")
        ast.parse(current, filename=relative)
    report_path = next(path for path in source_scope if path.endswith(".md"))
    report_exact = (
        (ROOT / report_path).read_text(encoding="utf-8")
        == _expected_report(_historical_bytes(report_path).decode("utf-8"))
    )
    checks.append(
        _check(
            "I05G-06",
            "bounded text source corrections",
            len(python_paths) == 9 and report_exact,
            "nine Python sources and one report differ only on frozen portability surfaces",
            {"parsed_python_files": 9, "report_projections": 1, "scientific_code_changes": 0},
        )
    )

    index_relative = (
        EXPERIMENT / "contracts/p2-i2/i03f-family-closeout-index.json"
    ).relative_to(ROOT).as_posix()
    raw_index = _historical_json(index_relative)
    portable_index = _load(ROOT / index_relative)
    pointer_pairs = _collect_pointer_pairs(raw_index, portable_index)
    resolved_targets = 0
    for raw_row, portable_row in zip(
        raw_index["mode_registry"], portable_index["mode_registry"]
    ):
        contract = _load(ROOT / portable_row["contract_path"])
        for old_pointer, new_pointer in zip(
            raw_row["authority_pointers"], portable_row["authority_pointers"]
        ):
            if _legacy_pointer(contract, old_pointer) != _portable_pointer(
                contract, new_pointer
            ):
                raise AssertionError("authority pointer target changed")
            resolved_targets += 1
    for raw_row, portable_row in zip(
        raw_index["operational_hypothesis_index"],
        portable_index["operational_hypothesis_index"],
    ):
        for mode_row in portable_index["mode_registry"]:
            mode = mode_row["mode"]
            contract = _load(ROOT / mode_row["contract_path"])
            old_pointer = raw_row[f"{mode}_pointer"]
            new_pointer = portable_row[f"{mode}_pointer"]
            if _legacy_pointer(contract, old_pointer) != _portable_pointer(
                contract, new_pointer
            ):
                raise AssertionError("operational pointer target changed")
            resolved_targets += 1
    validation_relative = (
        EXPERIMENT / "contracts/p2-i2/i03f-family-closeout-validation.json"
    ).relative_to(ROOT).as_posix()
    validation_pairs = _collect_pointer_pairs(
        _historical_json(validation_relative), _load(ROOT / validation_relative)
    )
    pairs_structurally_exact = all(
        _structured_pointer(old) == new
        for old, new in pointer_pairs + validation_pairs
    )
    checks.append(
        _check(
            "I05G-07",
            "structured pointer target equivalence",
            pairs_structurally_exact
            and resolved_targets == 44
            and len(pointer_pairs) + len(validation_pairs) == 105,
            "all 105 pointer projections preserve ordered segments and all 44 indexed targets resolve identically",
            {
                "indexed_targets_resolved": resolved_targets,
                "projected_pointer_occurrences": len(pointer_pairs) + len(validation_pairs),
            },
        )
    )

    conform_names = {
        "p2_i2_i03ar1_conform.py",
        "p2_i2_i03b_conform.py",
        "p2_i2_i03c_conform.py",
    }
    scripts_portable = True
    for relative in python_paths:
        text = (ROOT / relative).read_text(encoding="utf-8")
        if text.startswith("#!"):
            scripts_portable = False
        if Path(relative).name in conform_names:
            scripts_portable = scripts_portable and all(
                fragment in text
                for fragment in (
                    'GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"',
                    '"pygrc_import_identity"',
                    '"invoked_executable_repo_relative": ".venv/bin/python"',
                    '"venv_prefix_repo_relative": ".venv"',
                )
            )
    checks.append(
        _check(
            "I05G-08",
            "portable harness identity and non-executable projections",
            scripts_portable
            and all(
                _load(ROOT / relative)["portability_projection"]
                == _metadata(source_scope[relative])
                for relative in json_paths
            ),
            "scripts require explicit .venv invocation and every projected JSON is labelled non-executable and non-scientific",
            {"explicit_venv_identity": ".venv/bin/python", "projected_json_files": 20},
        )
    )

    prior = freeze["prior_group_identities"]
    prior_paths = {
        "I05F_acceptance_sha256": "contracts/p2-i2/i05f-owner-acceptance-and-commit-authority.json",
        "I05F_lineage_sha256": "contracts/p2-i2/i05f-portable-projection-lineage.json",
        "I05F_validation_sha256": "contracts/p2-i2/i05f-portability-correction-validation.json",
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
            "I05G-09",
            "prior accepted group authority",
            prior_current == prior and prior_historical == prior,
            "I05F acceptance validation and lineage identities remain exact",
            {"prior_identity_count": len(prior), "source_commit": SOURCE_COMMIT},
        )
    )

    ceiling = policy["invocation_ceiling_after_freeze"]
    zero_keys = (
        "calibration_builder_invocations",
        "candidate_or_control_invocations",
        "conformance_or_scientific_invocations",
        "null_or_one_shot_wrapper_invocations",
        "other_python_process_starts",
        "pygrc_model_instantiations",
    )
    checks.append(
        _check(
            "I05G-10",
            "zero-execution and progression boundary",
            all(ceiling[key] == 0 for key in zero_keys)
            and ceiling["I05G_validator_entrypoint_starts"] == 3
            and freeze["later_correction_groups_authorized"] is False
            and freeze["scientific_change_authorized"] is False,
            "I05G remains static portability validation with no scientific execution or later-group authority",
            {
                "calibration_builder_invocations": 0,
                "candidate_or_control_invocations": 0,
                "conformance_or_scientific_invocations": 0,
                "other_python_process_starts": 0,
                "pygrc_model_instantiations": 0,
                "scientific_result": False,
            },
        )
    )

    return {
        "activity_id": policy["activity_id"],
        "artifact_id": "P2-I2-I05G-I03-PORTABILITY-CORRECTION-VALIDATION",
        "artifact_version": "1.0.0",
        "calibration_builder_invocations": 0,
        "candidate_or_control_invocations": 0,
        "checks": checks,
        "corrected_file_count": len(source_scope),
        "corrected_group_violation_count": len(findings),
        "freeze_sha256": _sha256(FREEZE),
        "interpreter_identity": ".venv/bin/python",
        "iteration_id": "P2-I2-I05G",
        "lane_id": "AE01-L02",
        "lineage_sha256": _sha256(LINEAGE),
        "null_or_one_shot_wrapper_invocations": 0,
        "other_python_process_starts": 0,
        "passed_checks": len(checks),
        "policy_sha256": _sha256(POLICY),
        "pygrc_model_instantiations": 0,
        "result_status": "P2-I2-I05G-I03-GROUP-REVIEW-READY",
        "scientific_result": False,
        "total_checks": len(checks),
        "validator_entrypoint_starts": 2,
        "failed_closed_pre_output_starts": 1,
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
        "P2-I2 I05G I03 portability correction: "
        f"{result['passed_checks']}/{result['total_checks']}; "
        f"corrected-group violations={result['corrected_group_violation_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
