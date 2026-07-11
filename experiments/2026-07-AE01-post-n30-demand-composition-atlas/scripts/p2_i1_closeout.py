#!/usr/bin/env python3
"""Reconstruct and validate the P2-I1 C02 scientific closeout."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence

from ae01_tooling import (
    ContractError,
    classify_threshold_relation,
    digest_canonical_data,
    digest_file,
    load_json,
    pretty_json_dumps,
    semantic_file_digest,
    validate_record,
    validate_portable_path,
)
from p2_i1 import analyze_records, experiment_root, find_repository_root
from p2_i1_execution import validate_exec_freeze, validate_run_record


SCHEMA_PATH = "contracts/schemas/ae01-contract.schema.json"
ANALYSIS_POLICY_PATH = "configs/p2_i1_analysis_policy.json"
METRIC_SHEET_PATH = "contracts/p2-i1/frozen-metric-sheet.json"
CALIBRATION_PATH = "contracts/p2-i1/metric-calibration.json"
CYCLE_ROOT = "contracts/p2-i1/c02"
FREEZE_PATH = f"{CYCLE_ROOT}/exec-freeze.json"
AUDIT_PATH = f"{CYCLE_ROOT}/cycle-audit.json"
EXECUTION_MANIFEST_PATH = f"{CYCLE_ROOT}/execution-manifest.json"


def _write_output(path_value: str | None, value: Mapping[str, Any]) -> None:
    rendered = pretty_json_dumps(value)
    if path_value is None:
        sys.stdout.write(rendered)
        return
    path = find_repository_root() / validate_portable_path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def _verify_canonical_payload(value: Mapping[str, Any]) -> None:
    body = {
        key: item for key, item in value.items() if key != "canonical_payload_digest"
    }
    if value.get("canonical_payload_digest") != digest_canonical_data(body):
        raise ContractError("P2-I1 C02 closeout canonical payload drifted")


def _load_execution_evidence() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]
]:
    root = experiment_root()
    freeze = load_json(root / FREEZE_PATH)
    validate_exec_freeze(freeze)
    audit = load_json(root / AUDIT_PATH)
    manifest = load_json(root / EXECUTION_MANIFEST_PATH)
    _verify_canonical_payload(audit)
    _verify_canonical_payload(manifest)
    if not (
        audit.get("artifact_kind") == "p2_i1_c02_cycle_audit"
        and audit.get("cycle_id") == "P2-I1-C02"
        and audit.get("audit_complete") is True
        and audit.get("effective_run_count") == 21
        and audit.get("missing_run_ids") == []
        and len(audit.get("obligation_results", [])) == 12
        and all(
            row.get("status") == "structural_prerequisites_passed"
            for row in audit["obligation_results"]
        )
        and audit.get("scientific_rung_assigned") is False
        and audit.get("terminal_classification_opened") is False
    ):
        raise ContractError("P2-I1 C02 closeout requires the complete neutral audit")
    if not (
        manifest.get("artifact_kind") == "p2_i1_c02_execution_manifest"
        and manifest.get("cycle_id") == "P2-I1-C02"
        and manifest.get("all_expected_runs_present") is True
        and manifest.get("cycle_audit_complete") is True
        and manifest.get("scientific_interpretation_opened") is False
        and manifest.get("rung_assignment_opened") is False
        and manifest.get("terminal_classification_opened") is False
    ):
        raise ContractError("P2-I1 C02 execution manifest is not closeout-eligible")
    runs: list[dict[str, Any]] = []
    for artifact in manifest.get("artifacts", []):
        if artifact.get("artifact_role") != "cell_seed_run":
            continue
        path = find_repository_root() / validate_portable_path(artifact["path"])
        if not path.is_file() or artifact.get("file_sha256") != digest_file(path):
            raise ContractError("P2-I1 C02 retained run digest drifted")
        run = load_json(path)
        validate_run_record(run, freeze=freeze)
        runs.append(run)
    if len(runs) != 21:
        raise ContractError("P2-I1 C02 closeout requires exactly 21 validated runs")
    return freeze, audit, manifest, runs


def build_analysis() -> dict[str, Any]:
    freeze, audit, manifest, runs = _load_execution_evidence()
    policy = load_json(experiment_root() / ANALYSIS_POLICY_PATH)
    opportunities = [
        opportunity
        for run in sorted(runs, key=lambda row: (row["cell_id"], row["seed"]))
        for opportunity in run["opportunity_records"]
    ]
    machine = analyze_records({"opportunity_records": opportunities}, policy)
    metric_sheet = load_json(experiment_root() / METRIC_SHEET_PATH)
    calibration = load_json(experiment_root() / CALIBRATION_PATH)
    delta = float(calibration["record"]["delta"])
    if not (
        metric_sheet["record"]["resolution_policy"]["delta"]["value"] == delta
        and metric_sheet["record"]["resolution_policy"]["status"] == "frozen"
        and machine["analysis_completeness"]["complete"] is True
    ):
        raise ContractError("P2-I1 C02 frozen analysis identity is incomplete")
    primary = [
        row
        for row in machine["paired_margins"]
        if row["comparison_id"] == "writer-relative-history-content"
    ]
    dependency = [
        row
        for row in machine["paired_margins"]
        if row["comparison_id"] == "feedback-row-presence-dependency"
    ]
    if len(primary) != 3 or len(dependency) != 3:
        raise ContractError("P2-I1 C02 paired comparison coverage drifted")
    seed_margins = [
        {"seed": int(row["seed"]), "margin": float(row["normalized_margin"])}
        for row in sorted(primary, key=lambda row: row["seed"])
    ]
    relation = classify_threshold_relation(
        seed_margins, delta=delta, applicable=True
    )
    selectivity_relations = {
        row["selectivity_relation"] for row in machine["selectivity_results"]
    }
    result = {
        "artifact_kind": "p2_i1_c02_scientific_analysis",
        "schema_version": "1.0.0",
        "analysis_id": "p2-i1-c02-scientific-analysis",
        "lane_id": "AE01-L01",
        "cycle_id": "P2-I1-C02",
        "evidence_effect": "machine_scientific_inputs_only",
        "exec_freeze_digest": freeze["canonical_payload_digest"],
        "cycle_audit_digest": audit["canonical_payload_digest"],
        "execution_manifest_digest": manifest["canonical_payload_digest"],
        "metric_sheet_ref": metric_sheet["record"]["metric_sheet_id"],
        "metric_sheet_file_sha256": digest_file(experiment_root() / METRIC_SHEET_PATH),
        "calibration_artifact_ref": calibration["record"]["calibration_id"],
        "calibration_file_sha256": digest_file(experiment_root() / CALIBRATION_PATH),
        "delta": delta,
        "primary_seed_margins": seed_margins,
        "primary_relation": relation,
        "primary_threshold_passed": all(row["margin"] > 0 for row in seed_margins),
        "medium_dependency_seed_margins": [
            {
                "seed": int(row["seed"]),
                "margin": float(row["normalized_margin"]),
            }
            for row in sorted(dependency, key=lambda row: row["seed"])
        ],
        "selectivity_results": machine["selectivity_results"],
        "selectivity_relation_set": sorted(selectivity_relations),
        "cell_aggregates": machine["cell_aggregates"],
        "all_structural_obligations_passed": True,
        "rung_assignment": None,
        "terminal_classification": None,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def validate_closeout_records(
    *,
    analysis: Mapping[str, Any],
    developmental: Mapping[str, Any],
    terminal: Mapping[str, Any],
    requirement: Mapping[str, Any],
) -> None:
    expected_analysis = build_analysis()
    if analysis != expected_analysis:
        raise ContractError("P2-I1 C02 scientific analysis does not reconstruct")
    schema = load_json(experiment_root() / SCHEMA_PATH)
    validate_record(developmental, schema)
    validate_record(terminal, schema)
    validate_record(requirement, schema)
    interpretation = developmental["record"]
    terminal_record = terminal["record"]
    requirement_record = requirement["record"]
    metric = interpretation["metric_relations"]
    if not (
        len(metric) == 1
        and metric[0]["seed_margins"] == analysis["primary_seed_margins"]
        and metric[0]["relation"] == analysis["primary_relation"]
        and metric[0]["threshold_passed"]
        is analysis["primary_threshold_passed"]
        and metric[0]["delta"] == analysis["delta"]
    ):
        raise ContractError("P2-I1 C02 interpretation metric relation drifted")
    rungs = interpretation["boundary_rungs"]
    if not (
        [row["rung_id"] for row in rungs]
        == [f"AE01-L01-R0{index}" for index in range(1, 6)]
        and all(row["status"] == "reached" for row in rungs)
        and interpretation["highest_valid_rung"]["reference_id"]
        == "AE01-L01-R05"
        and interpretation["support_status"] == "explicit_constructed_support"
    ):
        raise ContractError("P2-I1 C02 accepted boundary/support interpretation drifted")
    if not (
        terminal_record["classification"] == "supported_bounded_candidate"
        and terminal_record["execution_status"] == "completed"
        and terminal_record["reconstruction_status"] == "verified"
        and terminal_record["record_complete"] is True
        and terminal_record["forces_n31_non_selection"] is False
        and terminal_record["developmental_interpretation_ref"]
        == interpretation["interpretation_id"]
    ):
        raise ContractError("P2-I1 C02 terminal disposition drifted")
    if not (
        requirement_record["lane_ids"] == ["AE01-L01"]
        and requirement_record["target_catalog_layer"] == "building_block"
        and requirement_record["surface_status"] == "apparently_adequate"
        and requirement_record["ranking_eligibility"] == "pending_synthesis"
        and {
            row["evidence_role"] for row in requirement_record["evidence_refs"]
        }
        == {
            "observed_ae01_result",
            "constructed_ecology_mechanism",
            "ecology_interpretation",
        }
    ):
        raise ContractError("P2-I1 C02 demand extraction boundary drifted")


def build_closeout_manifest(
    *,
    analysis_path: Path,
    developmental_path: Path,
    terminal_path: Path,
    requirement_path: Path,
    validation_path: Path,
    report_path: Path,
    review_path: Path,
) -> dict[str, Any]:
    analysis = load_json(analysis_path)
    developmental = load_json(developmental_path)
    terminal = load_json(terminal_path)
    requirement = load_json(requirement_path)
    validation = load_json(validation_path)
    validate_closeout_records(
        analysis=analysis,
        developmental=developmental,
        terminal=terminal,
        requirement=requirement,
    )
    if not (
        validation.get("artifact_kind") == "p2_i1_c02_closeout_validation"
        and validation.get("status") == "passed"
        and validation.get("analysis_digest")
        == analysis["canonical_payload_digest"]
    ):
        raise ContractError("P2-I1 C02 closeout validation record drifted")
    root = find_repository_root()
    paths = [
        experiment_root() / FREEZE_PATH,
        experiment_root() / f"{CYCLE_ROOT}/execution-binding-receipt.json",
        experiment_root() / f"{CYCLE_ROOT}/retry-ledger.json",
        experiment_root() / AUDIT_PATH,
        experiment_root() / EXECUTION_MANIFEST_PATH,
        analysis_path,
        developmental_path,
        terminal_path,
        requirement_path,
        validation_path,
        report_path,
        review_path,
        experiment_root() / "scripts/p2_i1_closeout.py",
    ]
    artifacts = []
    for path in paths:
        if not path.is_file():
            raise ContractError(f"P2-I1 C02 closeout artifact missing: {path.name}")
        artifacts.append(
            {
                "path": path.relative_to(root).as_posix(),
                "semantic_digest": semantic_file_digest(path),
                "file_sha256": digest_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    result = {
        "artifact_kind": "p2_i1_c02_closeout_manifest",
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "evidence_effect": "retention_and_reconstruction_index_only",
        "terminal_classification": terminal["record"]["classification"],
        "highest_valid_rung": developmental["record"]["highest_valid_rung"],
        "support_status": developmental["record"]["support_status"],
        "artifact_count": len(artifacts),
        "artifacts": sorted(artifacts, key=lambda row: row["path"]),
        "execution_manifest_ref": "p2-i1-c02-execution-manifest",
        "all_execution_artifacts_indexed_by_execution_manifest": True,
        "scientific_interpretation_opened_only_after_complete_audit": True,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def command_build_analysis(args: argparse.Namespace) -> int:
    _write_output(args.output, build_analysis())
    return 0


def command_validate_closeout(args: argparse.Namespace) -> int:
    analysis = load_json(find_repository_root() / validate_portable_path(args.analysis))
    developmental = load_json(
        find_repository_root() / validate_portable_path(args.developmental)
    )
    terminal = load_json(find_repository_root() / validate_portable_path(args.terminal))
    requirement = load_json(
        find_repository_root() / validate_portable_path(args.requirement)
    )
    validate_closeout_records(
        analysis=analysis,
        developmental=developmental,
        terminal=terminal,
        requirement=requirement,
    )
    result = {
        "artifact_kind": "p2_i1_c02_closeout_validation",
        "schema_version": "1.0.0",
        "status": "passed",
        "analysis_digest": analysis["canonical_payload_digest"],
        "developmental_semantic_digest": semantic_file_digest(
            find_repository_root() / validate_portable_path(args.developmental)
        ),
        "terminal_semantic_digest": semantic_file_digest(
            find_repository_root() / validate_portable_path(args.terminal)
        ),
        "requirement_semantic_digest": semantic_file_digest(
            find_repository_root() / validate_portable_path(args.requirement)
        ),
    }
    _write_output(args.output, result)
    return 0


def command_build_manifest(args: argparse.Namespace) -> int:
    root = find_repository_root()
    result = build_closeout_manifest(
        analysis_path=root / validate_portable_path(args.analysis),
        developmental_path=root / validate_portable_path(args.developmental),
        terminal_path=root / validate_portable_path(args.terminal),
        requirement_path=root / validate_portable_path(args.requirement),
        validation_path=root / validate_portable_path(args.validation),
        report_path=root / validate_portable_path(args.report),
        review_path=root / validate_portable_path(args.review),
    )
    _write_output(args.output, result)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    analysis = subparsers.add_parser("build-analysis")
    analysis.add_argument("--output", required=True)
    analysis.set_defaults(handler=command_build_analysis)
    closeout = subparsers.add_parser("validate-closeout")
    closeout.add_argument("--analysis", required=True)
    closeout.add_argument("--developmental", required=True)
    closeout.add_argument("--terminal", required=True)
    closeout.add_argument("--requirement", required=True)
    closeout.add_argument("--output")
    closeout.set_defaults(handler=command_validate_closeout)
    manifest = subparsers.add_parser("build-closeout-manifest")
    manifest.add_argument("--analysis", required=True)
    manifest.add_argument("--developmental", required=True)
    manifest.add_argument("--terminal", required=True)
    manifest.add_argument("--requirement", required=True)
    manifest.add_argument("--validation", required=True)
    manifest.add_argument("--report", required=True)
    manifest.add_argument("--review", required=True)
    manifest.add_argument("--output", required=True)
    manifest.set_defaults(handler=command_build_manifest)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        sys.stderr.write(f"P2-I1 C02 closeout error: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
