#!/usr/bin/env python3
"""Command-line entry point for AE01 experiment-local infrastructure."""

from __future__ import annotations

import argparse
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from ae01_tooling import (
    ContractError,
    ReadOnlyTreeGuard,
    assemble_report,
    build_artifact_manifest,
    build_runtime_binding_receipt,
    classify_threshold_relation,
    digest_canonical_data,
    digest_file,
    find_repository_root,
    freeze_metric_resolution,
    load_json,
    pretty_json_dumps,
    resolve_execution_policy,
    semantic_file_digest,
    validate_execution_policy,
    validate_interpretation_policy,
    validate_lane_projections,
    validate_record,
    validate_portable_path,
    write_json,
)


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SCHEMA = EXPERIMENT / "contracts/schemas/ae01-contract.schema.json"
REGISTRY = EXPERIMENT / "contracts/lane-registry.json"
PROFILES = EXPERIMENT / "configs/p1_i5_profiles.json"
EXECUTION_POLICY = EXPERIMENT / "configs/p1_i5_execution_policy.json"
INTERPRETATION_POLICY = (
    EXPERIMENT / "configs/p1_i4_developmental_interpretation_policy.json"
)
METRIC_SHEETS = EXPERIMENT / "contracts/metric-sheets"
INTERPRETATION_CLAIM = (
    EXPERIMENT / "contracts/phase1-interpretation-claim-boundary.json"
)
FIXTURES = EXPERIMENT / "contracts/fixtures"


def _path(root: Path, value: str) -> Path:
    validate_portable_path(value)
    return root / value


def _validate_phase1(root: Path) -> dict[str, Any]:
    schema = load_json(root / SCHEMA)
    registry = load_json(root / REGISTRY)
    profiles = load_json(root / PROFILES)
    policy = load_json(root / EXECUTION_POLICY)
    interpretation_policy = load_json(root / INTERPRETATION_POLICY)
    interpretation_claim = load_json(root / INTERPRETATION_CLAIM)

    validate_record(registry, schema)
    validate_record(profiles, schema)
    validate_record(interpretation_claim, schema)
    validate_lane_projections(registry, root)
    validate_execution_policy(policy)
    validate_interpretation_policy(interpretation_policy)
    metric_sheet_paths = sorted((root / METRIC_SHEETS).glob("*.json"))
    if len(metric_sheet_paths) != 7:
        raise ContractError("exactly seven primary metric sheets are required")
    metric_sheets = [load_json(path) for path in metric_sheet_paths]
    for metric_sheet in metric_sheets:
        validate_record(metric_sheet, schema)
    if [item["record"]["lane_id"] for item in metric_sheets] != [
        f"AE01-L0{index}" for index in range(1, 8)
    ]:
        raise ContractError("metric sheets must be complete and lane-ordered")
    first = resolve_execution_policy(policy)
    second = resolve_execution_policy(policy)
    if digest_canonical_data(first) != digest_canonical_data(second):
        raise ContractError("duplicate execution-policy resolution is unstable")

    valid_paths = sorted((root / FIXTURES / "valid").glob("*.json"))
    invalid_paths = sorted((root / FIXTURES / "invalid").glob("*.json"))
    if not valid_paths or not invalid_paths:
        raise ContractError("valid and invalid conformance fixtures are required")
    for path in valid_paths:
        validate_record(load_json(path), schema)
    unexpected_valid: list[str] = []
    for path in invalid_paths:
        try:
            validate_record(load_json(path), schema)
        except ContractError:
            continue
        unexpected_valid.append(path.relative_to(root).as_posix())
    if unexpected_valid:
        raise ContractError(
            f"invalid fixtures unexpectedly passed: {unexpected_valid}"
        )

    return {
        "artifact_role": "p1_i5_infrastructure_validation",
        "contract_revision": "0.24",
        "evidence_effect": "none_infrastructure_only",
        "valid_fixture_count": len(valid_paths),
        "invalid_fixture_count": len(invalid_paths),
        "lane_projection_count": len(registry["record"]["projection_targets"]),
        "metric_sheet_count": len(metric_sheets),
        "resolved_execution_policy_digest": first["resolved_policy_digest"],
        "checks": {
            "schema_and_semantics": "passed",
            "lane_projections": "passed",
            "duplicate_resolution": "passed",
            "negative_fixtures": "passed",
            "portable_paths": "passed",
            "developmental_interpretation_policy": "passed",
            "candidate_execution_resolution_gate": "passed_pending_calibration",
        },
        "claim_boundary": {
            "positive_atlas_evidence_opened": False,
            "lane_execution_performed": False,
            "reusable_mechanism_admitted": False,
        },
    }


def command_validate(args: argparse.Namespace) -> int:
    root = find_repository_root()
    summary = _validate_phase1(root)
    if args.output:
        write_json(_path(root, args.output), summary)
    else:
        sys.stdout.write(pretty_json_dumps(summary))
    return 0


def command_resolve_policy(args: argparse.Namespace) -> int:
    root = find_repository_root()
    policy = load_json(_path(root, args.policy))
    resolved = resolve_execution_policy(policy)
    if args.output:
        write_json(_path(root, args.output), resolved)
    else:
        sys.stdout.write(pretty_json_dumps(resolved))
    return 0


def command_digest(args: argparse.Namespace) -> int:
    root = find_repository_root()
    path = _path(root, args.input)
    result = {
        "path": args.input,
        "output_digest": semantic_file_digest(path),
        "file_sha256": digest_file(path),
        "size_bytes": path.stat().st_size,
    }
    sys.stdout.write(pretty_json_dumps(result))
    return 0


def command_runtime_receipt(args: argparse.Namespace) -> int:
    root = find_repository_root()
    schema = load_json(root / SCHEMA)
    profile_record = load_json(_path(root, args.profile))
    if profile_record.get("record_type") != "realization_profile":
        raise ContractError("runtime profile must be a realization_profile record")
    validate_record(profile_record, schema)
    guard = ReadOnlyTreeGuard(Path(args.graph_root)) if args.graph_root else nullcontext()
    with guard:
        receipt = build_runtime_binding_receipt(
            profile_record["record"],
            run_id=args.run_id,
            execution_class=args.execution_class,
            requested_operations=args.operation,
        )
    validate_record(receipt, schema)
    write_json(_path(root, args.receipt_output), receipt)
    return 0 if receipt["record"]["conformance_status"] == "passed" else 2


def command_manifest(args: argparse.Namespace) -> int:
    root = find_repository_root()
    schema = load_json(root / SCHEMA)
    descriptor = load_json(_path(root, args.descriptor))
    profiles = load_json(_path(root, descriptor["profile_registry_path"]))
    validate_record(profiles, schema)
    realizations = [
        load_json(_path(root, value)) for value in descriptor.get("realization_paths", [])
    ]
    for realization in realizations:
        validate_record(realization, schema)
    manifest = build_artifact_manifest(
        manifest_id=descriptor["manifest_id"],
        profile_registry=profiles,
        declarations=descriptor["artifacts"],
        repository_root=root,
        source_revisions=descriptor["source_revisions"],
        resolved_realization_profiles=realizations,
    )
    validate_record(manifest, schema)
    write_json(_path(root, args.output), manifest)
    return 0


def command_report(args: argparse.Namespace) -> int:
    root = find_repository_root()
    schema = load_json(root / SCHEMA)
    projection = load_json(_path(root, args.projection))
    validate_record(projection, schema)
    authored = ""
    if args.authored:
        authored = _path(root, args.authored).read_text(encoding="utf-8")
    report = assemble_report(projection, authored_markdown=authored)
    actual_digest = hashlib.sha256(report.encode("utf-8")).hexdigest()
    if args.preview_digest:
        sys.stdout.write(
            pretty_json_dumps(
                {
                    "report_id": projection["record"]["report_id"],
                    "expected_output_digest": actual_digest,
                    "expected_file_sha256": actual_digest,
                    "size_bytes": len(report.encode("utf-8")),
                    "evidence_effect": "preview_only",
                }
            )
        )
        return 0
    expected_output = projection["record"]["expected_output_digest"]
    expected_file = projection["record"]["expected_file_sha256"]
    if actual_digest != expected_output or actual_digest != expected_file:
        raise ContractError(
            "assembled report digest does not match the frozen projection"
        )
    if not args.output:
        raise ContractError("assembled report output is required outside preview mode")
    output = _path(root, args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    return 0


def command_freeze_resolution(args: argparse.Namespace) -> int:
    root = find_repository_root()
    schema = load_json(root / SCHEMA)
    metric_sheet = load_json(_path(root, args.metric_sheet))
    calibration_input = load_json(_path(root, args.calibration_input))
    validate_record(metric_sheet, schema)
    calibration, frozen_sheet = freeze_metric_resolution(
        metric_sheet, calibration_input
    )
    validate_record(calibration, schema)
    validate_record(frozen_sheet, schema)
    write_json(_path(root, args.calibration_output), calibration)
    write_json(_path(root, args.frozen_sheet_output), frozen_sheet)
    return 0


def _parse_seed_margin(value: str) -> dict[str, int | float]:
    try:
        seed_text, margin_text = value.split(":", 1)
        return {"seed": int(seed_text), "margin": float(margin_text)}
    except ValueError as exc:
        raise ContractError("margin must use SEED:VALUE syntax") from exc


def command_classify_margin(args: argparse.Namespace) -> int:
    root = find_repository_root()
    schema = load_json(root / SCHEMA)
    metric_sheet = load_json(_path(root, args.metric_sheet))
    validate_record(metric_sheet, schema)
    payload = metric_sheet["record"]
    resolution = payload["resolution_policy"]
    margins = [_parse_seed_margin(value) for value in args.margin]
    frozen = resolution["status"] == "frozen"
    delta = resolution["delta"].get("value") if frozen else None
    relation = classify_threshold_relation(margins, delta=delta)
    result = {
        "metric_sheet_ref": payload["metric_sheet_id"],
        "seed_margins": margins,
        "resolution_status": "frozen" if frozen else "unknown",
        "relation": relation,
        "threshold_passed": all(item["margin"] > 0 for item in margins),
        "rationale": (
            "Relation derived from the frozen resolution band"
            if frozen
            else "Resolution is not calibrated; narrow or robust language is blocked"
        ),
    }
    if frozen:
        result["delta"] = delta
        result["calibration_artifact_ref"] = resolution["delta"][
            "calibration_artifact_ref"
        ]
    sys.stdout.write(pretty_json_dumps(result))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate-phase1")
    validate.add_argument("--output")
    validate.set_defaults(handler=command_validate)

    resolve = commands.add_parser("resolve-policy")
    resolve.add_argument("--policy", default=EXECUTION_POLICY.as_posix())
    resolve.add_argument("--output")
    resolve.set_defaults(handler=command_resolve_policy)

    digest = commands.add_parser("digest")
    digest.add_argument("--input", required=True)
    digest.set_defaults(handler=command_digest)

    runtime = commands.add_parser("runtime-receipt")
    runtime.add_argument("--profile", required=True)
    runtime.add_argument("--run-id", required=True)
    runtime.add_argument(
        "--execution-class",
        required=True,
        choices=("pygrc_runtime_with_rcae_producer", "pygrc_native_runtime"),
    )
    runtime.add_argument("--operation", action="append", required=True)
    runtime.add_argument("--receipt-output", required=True)
    runtime.add_argument("--graph-root")
    runtime.set_defaults(handler=command_runtime_receipt)

    manifest = commands.add_parser("build-manifest")
    manifest.add_argument("--descriptor", required=True)
    manifest.add_argument("--output", required=True)
    manifest.set_defaults(handler=command_manifest)

    report = commands.add_parser("assemble-report")
    report.add_argument("--projection", required=True)
    report.add_argument("--authored")
    report.add_argument("--output")
    report.add_argument("--preview-digest", action="store_true")
    report.set_defaults(handler=command_report)

    freeze_resolution = commands.add_parser("freeze-resolution")
    freeze_resolution.add_argument("--metric-sheet", required=True)
    freeze_resolution.add_argument("--calibration-input", required=True)
    freeze_resolution.add_argument("--calibration-output", required=True)
    freeze_resolution.add_argument("--frozen-sheet-output", required=True)
    freeze_resolution.set_defaults(handler=command_freeze_resolution)

    classify_margin = commands.add_parser("classify-margin")
    classify_margin.add_argument("--metric-sheet", required=True)
    classify_margin.add_argument("--margin", action="append", required=True)
    classify_margin.set_defaults(handler=command_classify_margin)

    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.handler(args))
    except (ContractError, KeyError, json.JSONDecodeError) as exc:
        print(f"AE01 tooling failure: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
