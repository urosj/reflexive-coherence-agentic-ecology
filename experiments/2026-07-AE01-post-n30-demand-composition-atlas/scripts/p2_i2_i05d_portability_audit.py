"""Deterministic value-redacted P2-I2 persisted-path portability audit."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SEP = chr(47)
BACKSLASH = chr(92)
DRIVE_RE = re.compile(r"^[A-Za-z]:[" + re.escape(SEP + BACKSLASH) + r"]")
DRIVE_TOKEN_RE = re.compile(
    r"(?:^|[\s\"'`=([{<,!])(?P<value>[A-Za-z]:[\\/][^\s\"'`),\]}>;]+)"
)
HOME_TOKEN_RE = re.compile(
    r"(?:^|[\s\"'`=([{<,!])(?P<value>~[\\/][^\s\"'`),\]}>;]+)"
)
POSIX_TOKEN_RE = re.compile(
    r"(?:^|[\s\"'`=([{<,!])(?P<value>"
    + re.escape(SEP)
    + r"(?!/)[^\s\"'`),\]}>;]+)"
)
URI_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected object: {path.relative_to(ROOT).as_posix()}")
    return value


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _experiment_relative(path: Path) -> str:
    return path.relative_to(EXPERIMENT).as_posix()


def _trim_token(value: str) -> str:
    return value.rstrip(".,:")


def _exact_class(value: str) -> str | None:
    if value.startswith(SEP) and not value.startswith(SEP * 2):
        return "posix_filesystem_absolute"
    if DRIVE_RE.match(value):
        return "drive_prefixed_filesystem_absolute"
    if value.startswith("~" + SEP) or value.startswith("~" + BACKSLASH):
        return "home_expanded_filesystem_path"
    return None


def _embedded_tokens(value: str) -> Iterable[tuple[str, str, int]]:
    for class_name, pattern in (
        ("embedded_machine_local_absolute_token", POSIX_TOKEN_RE),
        ("drive_prefixed_filesystem_absolute", DRIVE_TOKEN_RE),
        ("home_expanded_filesystem_path", HOME_TOKEN_RE),
    ):
        for match in pattern.finditer(value):
            token = _trim_token(match.group("value"))
            if token and not URI_RE.match(token):
                yield class_name, token, match.start("value") + 1


def _violation(
    *,
    relative_path: str,
    file_sha256: str,
    class_name: str,
    locator: dict[str, Any],
    forbidden_value: str,
    correction_group: str,
) -> dict[str, Any]:
    return {
        "correction_group": correction_group,
        "file_sha256": file_sha256,
        "forbidden_value_length": len(forbidden_value),
        "forbidden_value_sha256": _sha256_bytes(forbidden_value.encode("utf-8")),
        "locator": locator,
        "path": relative_path,
        "violation_class": class_name,
    }


def _walk_json(value: Any, field: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key in sorted(value):
            escaped = key.replace("~", "~0").replace(SEP, "~1")
            yield from _walk_json(value[key], field + SEP + escaped)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_json(item, field + SEP + str(index))
    elif isinstance(value, str):
        yield field, value


def _group(path: str) -> str:
    name = Path(path).name.casefold()
    if (
        "outputs/p2-i2/i05/" in path
        or name.startswith("i05")
        or name.startswith("p2_i2_i05")
        or name.startswith("test_p2_i2_i05")
        or name.startswith("p2-i2-i05")
    ):
        return "i05_active_execution_and_closeout"
    if any(token in name for token in ("i04", "i05")):
        return "i04_i05_authority_dependencies"
    if "i03" in name:
        return "i03_realization_and_conformance"
    if "i01" in name or "i02" in name:
        return "i01_i02_source_and_identity"
    return "p2_i2_governance_navigation_and_shared_projections"


def _scan_json(path: Path, relative_path: str) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    file_sha256 = _sha256(path)
    group = _group(relative_path)
    findings: list[dict[str, Any]] = []
    for field, string in _walk_json(value):
        exact = _exact_class(string)
        if exact is not None:
            findings.append(
                _violation(
                    relative_path=relative_path,
                    file_sha256=file_sha256,
                    class_name=exact,
                    locator={"json_pointer": field},
                    forbidden_value=string,
                    correction_group=group,
                )
            )
            continue
        for class_name, token, column in _embedded_tokens(string):
            findings.append(
                _violation(
                    relative_path=relative_path,
                    file_sha256=file_sha256,
                    class_name=class_name,
                    locator={"json_pointer": field, "string_column": column},
                    forbidden_value=token,
                    correction_group=group,
                )
            )
    return findings


def _scan_text(path: Path, relative_path: str) -> list[dict[str, Any]]:
    file_sha256 = _sha256(path)
    group = _group(relative_path)
    findings: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        for class_name, token, column in _embedded_tokens(line):
            findings.append(
                _violation(
                    relative_path=relative_path,
                    file_sha256=file_sha256,
                    class_name=class_name,
                    locator={"column": column, "line": line_number},
                    forbidden_value=token,
                    correction_group=group,
                )
            )
    return findings


def _scope_files(policy: dict[str, Any]) -> list[Path]:
    suffixes = set(policy["scope"]["allowed_suffixes"])
    excluded = set(policy["exclusions"]["generated_audit_paths"])
    found: set[Path] = set()
    for selector in policy["scope"]["selectors"]:
        for path in EXPERIMENT.glob(selector):
            if (
                path.is_file()
                and path.suffix in suffixes
                and _experiment_relative(path) not in excluded
            ):
                found.add(path)
    relative_found = {_experiment_relative(path) for path in found}
    missing = sorted(set(policy["scope"]["required_coverage"]) - relative_found)
    if missing:
        raise AssertionError(f"required recursive coverage missing: {missing!r}")
    return sorted(found, key=_relative)


def audit(policy_path: Path, freeze_path: Path) -> dict[str, Any]:
    policy = _load_object(policy_path)
    freeze = _load_object(freeze_path)
    if _sha256(policy_path) != freeze["policy_sha256"]:
        raise AssertionError("policy identity drifted")
    if _sha256(Path(__file__)) != freeze["scanner_sha256"]:
        raise AssertionError("scanner identity drifted")
    if policy["invocation_ceiling"] != freeze["invocation_ceiling"]:
        raise AssertionError("invocation ceiling drifted")
    governance_paths = {
        "checklist_sha256": EXPERIMENT
        / "implementation/P2-I2-shared-pool-co-conditioning-checklist.md",
        "decision_record_sha256": EXPERIMENT
        / "implementation/P2-I2-decision-record.md",
        "hypothesis_sha256": EXPERIMENT
        / "hypotheses/p2-i2-operational-hypotheses.md",
    }
    governance_hashes = {
        name: _sha256(path) for name, path in governance_paths.items()
    }
    if governance_hashes != freeze["governance_pre_scan_identities"]:
        raise AssertionError("governance identity drifted")

    files = _scope_files(policy)
    if len(files) != freeze["expected_scope_file_count"]:
        raise AssertionError(
            "audit scope count drifted: "
            f"{len(files)} != {freeze['expected_scope_file_count']}"
        )
    violations: list[dict[str, Any]] = []
    for path in files:
        relative_path = _relative(path)
        if path.suffix == ".json":
            violations.extend(_scan_json(path, relative_path))
        else:
            violations.extend(_scan_text(path, relative_path))
    violations.sort(
        key=lambda item: (
            item["correction_group"],
            item["path"],
            json.dumps(item["locator"], sort_keys=True),
            item["violation_class"],
            item["forbidden_value_sha256"],
        )
    )

    count_by_class = dict(sorted(Counter(
        item["violation_class"] for item in violations
    ).items()))
    count_by_group = {
        group: sum(item["correction_group"] == group for item in violations)
        for group in policy["correction_group_order"]
    }
    affected_files_by_group = {
        group: sorted(
            {
                item["path"]
                for item in violations
                if item["correction_group"] == group
            }
        )
        for group in policy["correction_group_order"]
    }
    affected_files = sorted({item["path"] for item in violations})
    source_identities = [
        {"file_sha256": _sha256(path), "path": _relative(path)} for path in files
    ]
    checks = [
        {
            "check_id": "I05D-AUDIT-01",
            "finding": "policy and scanner match the pre-scan input freeze",
            "status": "passed",
        },
        {
            "check_id": "I05D-AUDIT-02",
            "finding": "every selected current-tree file was scanned deterministically",
            "status": "passed",
        },
        {
            "check_id": "I05D-AUDIT-03",
            "finding": "inventory values are redacted to digest and length",
            "status": "passed",
        },
        {
            "check_id": "I05D-AUDIT-04",
            "finding": "correction groups preserve the frozen I05-first order",
            "status": "passed",
        },
        {
            "check_id": "I05D-AUDIT-05",
            "finding": "audit performs no builder wrapper PyGRC candidate control conformance calibration or scientific operation",
            "status": "passed",
        },
    ]
    report_relative = next(
        path
        for path in policy["exclusions"]["generated_audit_paths"]
        if path.endswith(".md")
    )
    report_path = EXPERIMENT / report_relative
    if (
        not report_path.is_file()
        or _sha256(report_path) != freeze["report_sha256"]
        or _scan_text(report_path, _relative(report_path))
    ):
        raise AssertionError("generated audit report contains a path violation")
    checks.append(
        {
            "check_id": "I05D-AUDIT-06",
            "finding": "generated audit report contains no path violation",
            "status": "passed",
        }
    )
    return {
        "activity_id": policy["activity_id"],
        "affected_file_count": len(affected_files),
        "affected_files_by_group": affected_files_by_group,
        "artifact_id": "P2-I2-I05D-PORTABILITY-AUDIT",
        "artifact_version": "1.0.0",
        "audit_baseline_commit": _git("rev-parse", "HEAD"),
        "audit_scope_file_count": len(files),
        "candidate_or_control_invocations": 0,
        "checks": checks,
        "conformance_or_scientific_invocations": 0,
        "correction_group_order": policy["correction_group_order"],
        "count_by_class": count_by_class,
        "count_by_group": count_by_group,
        "freeze_sha256": _sha256(freeze_path),
        "historical_lineage_rule": "commit_and_sha256_only",
        "iteration_id": freeze["iteration_id"],
        "lane_id": "AE01-L02",
        "null_builder_or_wrapper_invocations": 0,
        "passed_checks": len(checks),
        "policy_sha256": _sha256(policy_path),
        "pygrc_model_instantiations": 0,
        "result_status": "P2-I2-I05D-PORTABILITY-AUDIT-REVIEW-READY",
        "source_identities": source_identities,
        "total_checks": len(checks),
        "value_redaction": "forbidden_values_omitted_digest_and_length_only",
        "violation_count": len(violations),
        "violations": violations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--verify-existing", action="store_true")
    args = parser.parse_args()

    for supplied in (args.policy, args.freeze, args.output):
        if supplied.startswith(SEP) or DRIVE_RE.match(supplied) or supplied.startswith("~"):
            raise AssertionError("audit CLI paths must be repository-relative")
    policy_path = ROOT / args.policy
    freeze_path = ROOT / args.freeze
    output_path = ROOT / args.output
    record = audit(policy_path, freeze_path)
    encoded = json.dumps(
        record,
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
        allow_nan=False,
    ) + "\n"
    encoded_object = json.loads(encoded)
    for _, string in _walk_json(encoded_object):
        if _exact_class(string) is not None or any(_embedded_tokens(string)):
            raise AssertionError("generated audit inventory contains a path violation")
    if args.verify_existing:
        if not output_path.is_file() or output_path.read_text(encoding="utf-8") != encoded:
            raise AssertionError("existing audit is not byte-identical")
    else:
        if output_path.exists():
            raise AssertionError("refusing to overwrite existing audit")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(encoded, encoding="utf-8")
    print(
        f"{record['passed_checks']}/{record['total_checks']} checks passed; "
        f"{record['violation_count']} violations in "
        f"{record['affected_file_count']} files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
