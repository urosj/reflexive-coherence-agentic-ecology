#!/usr/bin/env python3
"""Thin CLI and file boundary for P2-I1."""

from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import nullcontext
from pathlib import Path
import subprocess
import sys
from typing import Any

from ae01_tooling import (
    build_runtime_binding_receipt,
    ContractError,
    ReadOnlyTreeGuard,
    digest_canonical_data,
    digest_file,
    load_json,
    pretty_json_dumps,
    validate_record,
    validate_portable_path,
)
from p2_i1_analysis import (
    aggregate_seed,
    build_rung_and_terminal_inputs,
    generate_matched_null,
    paired_margin,
    policy_projection_digests,
    selectivity_interaction,
    static_profile_identities,
    validate_analysis_policy,
)
from p2_i1_runtime import preflight_fixture


EXPERIMENT_RELATIVE = Path(
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
)
CONFIG_PATHS = {
    "fixture": "configs/p2_i1_fixture.json",
    "cells": "configs/p2_i1_cells.json",
    "analysis": "configs/p2_i1_analysis_policy.json",
    "calibration": "configs/p2_i1_calibration_policy.json",
    "provenance": "configs/p2_i1_cal_pre_provenance.json",
    "runtime": "configs/p2_i1_runtime_policy.json",
}


def find_repository_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".git").exists() and (parent / EXPERIMENT_RELATIVE).is_dir():
            return parent
    raise ContractError("repository root not found")


def experiment_root() -> Path:
    return find_repository_root() / EXPERIMENT_RELATIVE


def _load_configs() -> dict[str, Any]:
    root = experiment_root()
    return {name: load_json(root / path) for name, path in CONFIG_PATHS.items()}


def _write_output(path_value: str | None, value: Any) -> None:
    rendered = pretty_json_dumps(value)
    if path_value is None:
        sys.stdout.write(rendered)
        return
    portable = validate_portable_path(path_value)
    path = find_repository_root() / portable
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def _validate_fixture(config: dict[str, Any]) -> None:
    if config.get("fixture_id") != "rcae_p2_i1_four_node_v1":
        raise ContractError("fixture ID drifted")
    nodes = config.get("nodes", [])
    edges = config.get("edges", [])
    if [(row["node_id"], row["role"]) for row in nodes] != [
        (0, "P"), (1, "W"), (2, "A"), (3, "B")
    ]:
        raise ContractError("frozen node identity drifted")
    if [row["edge_id"] for row in edges] != [0, 1, 2, 3]:
        raise ContractError("frozen edge identity drifted")
    if [row["seed"] for row in config.get("seeds", [])] != [101, 211, 307]:
        raise ContractError("live seed profile drifted")
    profiles = config.get("opportunity_profiles", [])
    if [row["opportunity_index"] for row in profiles] != [0, 1, 2, 3]:
        raise ContractError("opportunity profile indices drifted")
    if len({row["profile_id"] for row in profiles}) != 4:
        raise ContractError("opportunity profile IDs must be unique")


def _validate_cells(config: dict[str, Any]) -> None:
    expected = [
        "reference",
        "candidate-conditioning",
        "medium-freeze-withdrawal",
        "trace-shuffle",
        "parent-context-contrast",
        "susceptibility-inversion",
        "carrier-timescale-contrast",
    ]
    if [row["cell_id"] for row in config.get("cells", [])] != expected:
        raise ContractError("P2-I1 comparison-cell matrix drifted")
    expected_interventions = {
        "reference": {"kind": "feedback_reference_delta", "reference_delta": 0.25},
        "candidate-conditioning": {
            "kind": "accepted_writer_relative_feedback_history",
            "reference_delta": 0.0,
        },
        "medium-freeze-withdrawal": {
            "kind": "medium_freeze",
            "emit_feedback_row": False,
            "scaffold_withdrawal": False,
        },
        "trace-shuffle": {
            "kind": "expected_source_digest_substitution",
            "expected_source": "writer_departure_contact",
            "feedback_source": "writer_arrival_contact",
        },
        "parent-context-contrast": {
            "kind": "absolute_environmental_support_scale",
            "support_offset": -0.25,
            "P_transform": "P_seed",
            "W_transform": "W_seed + 2 * support_offset",
            "A_transform": "0.5 + support_offset",
            "B_transform": "0.5 + support_offset",
            "parent_context": "absent_not_represented",
        },
        "susceptibility-inversion": {
            "kind": "swap_expected_polarity_between_stable_reader_slots",
            "profile_polarity_overrides": {
                "ctx-a-aligned": "negative",
                "ctx-a-inverted": "positive",
                "ctx-b-aligned": "negative",
                "ctx-b-inverted": "positive",
            },
        },
        "carrier-timescale-contrast": {
            "kind": "reader_packet_amount",
            "reader_packet_amount": 0.25,
        },
    }
    for cell in config["cells"]:
        if cell["intervention"] != expected_interventions[cell["cell_id"]]:
            raise ContractError(f"{cell['cell_id']}: intervention identity drifted")
    if config.get("opportunities_per_seed") != 4:
        raise ContractError("P2-I1 requires four independent opportunities")


def _validate_calibration(config: dict[str, Any]) -> None:
    if not (
        config.get("candidate_blind") is True
        and config.get("runtime_execution") is False
        and config.get("pygrc_imported") is False
    ):
        raise ContractError("calibration must remain candidate-blind and non-runtime")
    seeds = [row["seed"] for row in config.get("panels", [])]
    if seeds != [19, 43, 71, 109, 163]:
        raise ContractError("calibration seed profile drifted")
    if set(seeds).intersection(config.get("candidate_seeds_excluded", [])):
        raise ContractError("calibration and candidate seeds must be disjoint")


def _validate_runtime_policy(config: dict[str, Any]) -> None:
    if config.get("runtime_policy_id") != "rcae-p2-i1-runtime-policy-v2":
        raise ContractError("runtime policy identity drifted")
    if config.get("execution_class") != "pygrc_runtime_with_rcae_producer":
        raise ContractError("runtime execution class drifted")
    if config.get("fallback_execution_class") is not None:
        raise ContractError("runtime fallback is prohibited")
    if config.get("candidate_execution_authorized") is not False:
        raise ContractError("CAL-PRE config cannot authorize candidate execution")
    if config.get("machine_local_runtime_path_recorded") is not False:
        raise ContractError("shared runtime policy cannot record machine-local path")
    if config.get("preflight_operation_id") != "p2_i1_runtime_preflight":
        raise ContractError("runtime preflight operation identity drifted")
    if config.get("candidate_execution_authorization_mode") != (
        "explicit_cycle_exec_freeze_only"
    ):
        raise ContractError("candidate authorization mode drifted")
    if config.get("execution_freeze_required") is not True:
        raise ContractError("candidate execution must require a cycle freeze")
    if config.get("execution_freeze_gate") != "P2-I1-EXEC-FREEZE":
        raise ContractError("execution-freeze gate identity drifted")
    if config.get("execution_close_gate") != "P2-I1-EXEC-GATE":
        raise ContractError("execution-close gate identity drifted")
    if config.get("authorization_boundary") != (
        "P2-I1-CAL-GATE and P2-I1-REG-GATE must pass and an active "
        "P2-I1-EXEC-FREEZE record must authorize the exact frozen cycle "
        "before candidate execution; P2-I1-EXEC-GATE is post-execution closure"
    ):
        raise ContractError("candidate authorization boundary drifted")


def _validate_provenance(config: dict[str, Any]) -> None:
    expected_keys = {
        "evidence_effect",
        "schema_version",
        "provenance_profile_id",
        "working_directory",
        "environment_profile",
        "dependency_profile",
        "command_profiles",
        "resource_envelope",
        "expected_artifacts",
        "source_identity_policy",
        "input_identity_policy",
    }
    if set(config) != expected_keys:
        raise ContractError("CAL-PRE provenance profile shape drifted")
    if config["working_directory"] != ".":
        raise ContractError("CAL-PRE commands must run from repository root")
    dependencies = config["dependency_profile"]
    if dependencies.get("analysis_runtime_dependencies") != [
        "python_standard_library"
    ]:
        raise ContractError("matched-null analysis dependency profile drifted")
    if dependencies.get("phase1_validation_dependencies") != [
        "jsonschema==4.26.0"
    ]:
        raise ContractError("Phase 1 validation dependency pin drifted")
    if dependencies.get("pygrc_required_for_calibration") is not False:
        raise ContractError("candidate-blind calibration must not require PyGRC")
    command_ids = [row.get("command_id") for row in config["command_profiles"]]
    if command_ids != [
        "p2-i1-validate-phase1-v1",
        "p2-i1-validate-configs-v1",
        "p2-i1-test-v1",
        "p2-i1-build-cal-pre-identity-v1",
        "p2-i1-generate-matched-null-v1",
    ]:
        raise ContractError("CAL-PRE command profile identity drifted")
    for command in config["command_profiles"]:
        argv = command.get("argv")
        if not isinstance(argv, list) or not argv or any(
            not isinstance(item, str) or not item for item in argv
        ):
            raise ContractError("CAL-PRE command argv must be non-empty strings")
        for value in argv:
            if value.startswith("/") or "\\" in value or value.startswith("~"):
                raise ContractError("CAL-PRE command profile contains non-portable path")
    resources = config["resource_envelope"]
    if resources != {
        "max_runtime_seconds": 120,
        "max_memory_mb": 512,
        "max_disk_mb": 256,
    }:
        raise ContractError("CAL-PRE resource envelope drifted")
    source_policy = config["source_identity_policy"]
    if source_policy.get("dirty_preview_retention_allowed") is not False:
        raise ContractError("dirty CAL-PRE identity previews cannot be retained")
    input_policy = config["input_identity_policy"]
    for field in (
        "candidate_artifacts_allowed",
        "candidate_seeds_allowed",
        "pygrc_runtime_inputs_allowed",
        "post_outcome_tuning_allowed",
    ):
        if input_policy.get(field) is not False:
            raise ContractError(f"CAL-PRE provenance must prohibit {field}")


def validate_configs(configs: dict[str, Any]) -> dict[str, Any]:
    _validate_fixture(configs["fixture"])
    _validate_cells(configs["cells"])
    validate_analysis_policy(configs["analysis"])
    _validate_calibration(configs["calibration"])
    _validate_provenance(configs["provenance"])
    _validate_runtime_policy(configs["runtime"])
    profiles = static_profile_identities(configs["fixture"])
    if len({row["opportunity_profile_digest"] for row in profiles}) != 4:
        raise ContractError("static opportunity profiles must have distinct digests")
    if len({row["reader_configuration_digest"] for row in profiles}) != 2:
        raise ContractError("P2-I1 requires exactly two reader configurations")
    result = {
        "artifact_kind": "p2_i1_config_validation",
        "schema_version": "1.0.0",
        "status": "passed",
        "evidence_effect": "none_infrastructure_only",
        "validated_config_paths": list(CONFIG_PATHS.values()),
        "comparison_cell_count": 7,
        "live_seed_count": 3,
        "opportunity_profile_count": 4,
        "candidate_execution_authorized": False,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def _git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_worktree_status(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def build_cal_pre_identity(
    configs: dict[str, Any], *, allow_dirty_preview: bool = False
) -> dict[str, Any]:
    validation = validate_configs(configs)
    root = find_repository_root()
    experiment = experiment_root()
    worktree_status = _git_worktree_status(root)
    if worktree_status and not allow_dirty_preview:
        raise ContractError(
            "CAL-PRE freeze identity requires a clean committed worktree; "
            "use --allow-dirty-preview only for non-retainable review output"
        )
    source_tree_clean = not worktree_status
    analysis_script = "scripts/p2_i1_analysis.py"
    cli_script = "scripts/p2_i1.py"
    runtime_script = "scripts/p2_i1_runtime.py"
    projections = policy_projection_digests(configs["analysis"])
    config_digests = {
        f"{name}_config_digest": digest_canonical_data(configs[name])
        for name in CONFIG_PATHS
    }
    profile_identities = static_profile_identities(configs["fixture"])
    calibration_projection = {
        "fixture_config_digest": config_digests["fixture_config_digest"],
        "analysis_config_digest": config_digests["analysis_config_digest"],
        "calibration_config_digest": config_digests["calibration_config_digest"],
        "provenance_config_digest": config_digests["provenance_config_digest"],
        "analysis_script_sha256": digest_file(experiment / analysis_script),
        **projections,
        "static_opportunity_profile_digests": [
            row["opportunity_profile_digest"] for row in profile_identities
        ],
    }
    measurement_projection = {
        **calibration_projection,
        "cells_config_digest": config_digests["cells_config_digest"],
        "runtime_config_digest": config_digests["runtime_config_digest"],
    }
    result = {
        "artifact_kind": (
            "p2_i1_cal_pre_identity"
            if source_tree_clean
            else "p2_i1_cal_pre_identity_preview"
        ),
        "schema_version": "1.0.0",
        "identity_id": (
            "rcae-p2-i1-cal-pre-identity-v2"
            if source_tree_clean
            else "rcae-p2-i1-cal-pre-identity-preview-v2"
        ),
        "supersedes_identity_id": "rcae-p2-i1-cal-pre-identity-v1",
        "bounded_refresh_reason": "P2-I1-DEC-020 execution authorization correction",
        "evidence_effect": "none_preregistration_identity_only",
        "source_revision": _git_revision(root),
        "source_tree_clean": source_tree_clean,
        "retention_eligible": source_tree_clean,
        "working_tree_change_count": len(worktree_status),
        "working_tree_status_digest": digest_canonical_data(worktree_status),
        "analysis_script_path": analysis_script,
        "analysis_script_sha256": calibration_projection["analysis_script_sha256"],
        "analysis_policy_path": CONFIG_PATHS["analysis"],
        "analysis_policy_digest": config_digests["analysis_config_digest"],
        "provenance_profile_path": CONFIG_PATHS["provenance"],
        "provenance_profile_digest": config_digests["provenance_config_digest"],
        **projections,
        "cli_path": cli_script,
        "cli_sha256": digest_file(experiment / cli_script),
        "runtime_harness_path": runtime_script,
        "runtime_harness_sha256": digest_file(experiment / runtime_script),
        "configuration_digests": config_digests,
        "static_profile_identities": profile_identities,
        "calibration_realization_digest": digest_canonical_data(calibration_projection),
        "measurement_identity_digest": digest_canonical_data(measurement_projection),
        "candidate_outcomes_absent": True,
        "candidate_execution_authorized": False,
        "validation_digest": validation["canonical_payload_digest"],
        "reconstruction": {
            "working_directory": configs["provenance"]["working_directory"],
            "environment_profile": configs["provenance"]["environment_profile"],
            "dependency_profile": configs["provenance"]["dependency_profile"],
            "command_profiles": configs["provenance"]["command_profiles"],
            "resource_envelope": configs["provenance"]["resource_envelope"],
            "expected_artifacts": configs["provenance"]["expected_artifacts"],
        }
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def analyze_records(payload: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    records = payload.get("opportunity_records")
    if not isinstance(records, list):
        raise ContractError("analysis input requires opportunity_records list")
    if "paired_comparisons" in payload or "selectivity_seeds" in payload:
        raise ContractError(
            "comparison roles and seeds come from the frozen analysis policy"
        )
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[(record["cell_id"], int(record["seed"]))].append(record)
    aggregates = {
        key: aggregate_seed(value, policy) for key, value in sorted(grouped.items())
    }
    aggregation_policy = policy["aggregation_policy"]
    seeds = policy["terminal_classifier_input_policy"]["required_seed_ids"]
    paired_results = []
    missing_comparisons = []
    for role in ("primary_comparison", "medium_dependency_comparison"):
        comparison = aggregation_policy[role]
        for seed in seeds:
            candidate_key = (comparison["candidate_cell"], int(seed))
            comparator_key = (comparison["comparator_cell"], int(seed))
            if candidate_key not in aggregates or comparator_key not in aggregates:
                missing_comparisons.append(
                    {"comparison_id": comparison["comparison_id"], "seed": seed}
                )
                continue
            paired_results.append(
                {
                    "comparison_id": comparison["comparison_id"],
                    "metric_role": comparison["metric_role"],
                    "uses_calibrated_delta": comparison["uses_calibrated_delta"],
                    **paired_margin(
                        aggregates[candidate_key], aggregates[comparator_key], policy
                    ),
                }
            )
    selectivity_results = []
    missing_selectivity_seeds = []
    selectivity_policy = aggregation_policy["selectivity"]
    for seed in seeds:
        candidate_key = (selectivity_policy["candidate_cell"], int(seed))
        comparator_key = (selectivity_policy["comparator_cell"], int(seed))
        if candidate_key not in grouped or comparator_key not in grouped:
            missing_selectivity_seeds.append(seed)
            continue
        selectivity_results.append(
            {
                "seed": int(seed),
                **selectivity_interaction(
                    grouped[candidate_key], grouped[comparator_key]
                ),
            }
        )
    result = build_rung_and_terminal_inputs(
        cell_aggregates=list(aggregates.values()),
        paired_margins=paired_results,
        selectivity_results=selectivity_results,
    )
    result["analysis_completeness"] = {
        "missing_comparisons": missing_comparisons,
        "missing_selectivity_seeds": missing_selectivity_seeds,
        "complete": not missing_comparisons and not missing_selectivity_seeds,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def command_validate_configs(args: argparse.Namespace) -> int:
    _write_output(args.output, validate_configs(_load_configs()))
    return 0


def command_build_identity(args: argparse.Namespace) -> int:
    _write_output(
        args.output,
        build_cal_pre_identity(
            _load_configs(), allow_dirty_preview=args.allow_dirty_preview
        ),
    )
    return 0


def command_generate_null(args: argparse.Namespace) -> int:
    configs = _load_configs()
    validate_configs(configs)
    _write_output(
        args.output,
        generate_matched_null(configs["calibration"], configs["analysis"]),
    )
    return 0


def command_analyze(args: argparse.Namespace) -> int:
    configs = _load_configs()
    validate_configs(configs)
    input_path = find_repository_root() / validate_portable_path(args.input)
    _write_output(args.output, analyze_records(load_json(input_path), configs["analysis"]))
    return 0


def command_runtime_preflight(args: argparse.Namespace) -> int:
    configs = _load_configs()
    validate_configs(configs)
    root = find_repository_root()
    profile = load_json(root / validate_portable_path(args.realization_profile))
    schema = load_json(experiment_root() / "contracts/schemas/ae01-contract.schema.json")
    validate_record(profile, schema)
    if profile.get("record_type") != "realization_profile":
        raise ContractError("runtime preflight requires a realization_profile record")
    guard = ReadOnlyTreeGuard(Path(args.graph_root)) if args.graph_root else nullcontext()
    with guard:
        receipt = build_runtime_binding_receipt(
            profile["record"],
            run_id=args.run_id,
            execution_class=configs["runtime"]["execution_class"],
            requested_operations=[configs["runtime"]["preflight_operation_id"]],
        )
        validate_record(receipt, schema)
        if receipt["record"]["conformance_status"] != "passed":
            blocked = {
                "artifact_kind": "p2_i1_runtime_preflight_blocked",
                "schema_version": "1.0.0",
                "evidence_effect": "none_infrastructure_only",
                "status": "failed",
                "runtime_binding_receipt": receipt,
                "candidate_execution_authorized": False,
            }
            _write_output(
                args.output,
                {**blocked, "canonical_payload_digest": digest_canonical_data(blocked)},
            )
            return 2
        result = preflight_fixture(
            configs["fixture"],
            configs["cells"],
            configs["runtime"],
            profile,
            seed=args.seed,
            cell_id=args.cell,
        )
    with_receipt = {**result, "runtime_binding_receipt": receipt}
    with_receipt["canonical_payload_digest"] = digest_canonical_data(
        {key: value for key, value in with_receipt.items() if key != "canonical_payload_digest"}
    )
    _write_output(args.output, with_receipt)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate-configs")
    validate.add_argument("--output")
    validate.set_defaults(handler=command_validate_configs)
    identity = subparsers.add_parser("build-cal-pre-identity")
    identity.add_argument("--output")
    identity.add_argument("--allow-dirty-preview", action="store_true")
    identity.set_defaults(handler=command_build_identity)
    matched_null = subparsers.add_parser("generate-matched-null")
    matched_null.add_argument("--output")
    matched_null.set_defaults(handler=command_generate_null)
    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--input", required=True)
    analyze.add_argument("--output")
    analyze.set_defaults(handler=command_analyze)
    preflight = subparsers.add_parser("runtime-preflight")
    preflight.add_argument("--realization-profile", required=True)
    preflight.add_argument("--run-id", required=True)
    preflight.add_argument("--graph-root")
    preflight.add_argument("--seed", type=int, default=211)
    preflight.add_argument("--cell", default="candidate-conditioning")
    preflight.add_argument("--output")
    preflight.set_defaults(handler=command_runtime_preflight)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (ContractError, KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        sys.stderr.write(f"P2-I1 error: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
