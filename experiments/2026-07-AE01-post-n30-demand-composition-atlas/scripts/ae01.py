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
    digest_canonical_data,
    digest_file,
    find_repository_root,
    load_json,
    pretty_json_dumps,
    resolve_execution_policy,
    semantic_file_digest,
    validate_execution_policy,
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
FIXTURES = EXPERIMENT / "contracts/fixtures"


def _path(root: Path, value: str) -> Path:
    validate_portable_path(value)
    return root / value


def _validate_phase1(root: Path) -> dict[str, Any]:
    schema = load_json(root / SCHEMA)
    registry = load_json(root / REGISTRY)
    profiles = load_json(root / PROFILES)
    policy = load_json(root / EXECUTION_POLICY)

    validate_record(registry, schema)
    validate_record(profiles, schema)
    validate_lane_projections(registry, root)
    validate_execution_policy(policy)
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
        "contract_revision": "0.23",
        "evidence_effect": "none_infrastructure_only",
        "valid_fixture_count": len(valid_paths),
        "invalid_fixture_count": len(invalid_paths),
        "lane_projection_count": len(registry["record"]["projection_targets"]),
        "resolved_execution_policy_digest": first["resolved_policy_digest"],
        "checks": {
            "schema_and_semantics": "passed",
            "lane_projections": "passed",
            "duplicate_resolution": "passed",
            "negative_fixtures": "passed",
            "portable_paths": "passed",
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
