#!/usr/bin/env python3
"""Registration-only validation and identity projection for P2-I1.

This module does not execute candidate cells.  It validates the experiment-local
registration policy and proves that its measurement and realization projections
import the retained v2 CAL-PRE/CAL identities unchanged.
"""

from __future__ import annotations

import argparse
from contextlib import nullcontext
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping

from ae01_tooling import (
    build_artifact_manifest,
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
from p2_i1 import CONFIG_PATHS, experiment_root, find_repository_root, validate_configs
from p2_i1_analysis import policy_projection_digests, static_profile_identities
from p2_i1_runtime import (
    OPERATION_CAPABILITY_PATHS,
    bind_runtime,
    build_fixture,
    resolve_node_coherences,
    resolve_reader_packet_amount,
    validate_runtime_operation_capabilities,
)


REGISTRATION_POLICY_PATH = "configs/p2_i1_registration_policy.json"
COMMON_CONTROL_IDS = [f"AE01-CTRL-{index:02d}" for index in range(1, 20)]
LANE_CONTROL_IDS = [f"AE01-L01-CTRL-{index:02d}" for index in range(1, 6)]
CONTROL_IDS = COMMON_CONTROL_IDS + LANE_CONTROL_IDS
RESOLUTION_STAGES = {
    "registration_guard",
    "execution_comparison",
    "terminal_report_guard",
    "inherited_verification",
}
EXPECTED_EVIDENCE_BINDINGS = {
    "AE01-CTRL-01/record-role-guard": [
        "source-inventory",
        "rcae-p2-i1-l01-registered-probe",
    ],
    "AE01-CTRL-02/n30-ceiling-verification": [
        "inherited:n30_replay_controls_i7",
        "inherited:n30_closeout_and_spiral_handoff_i8",
    ],
    "AE01-CTRL-03/n29-component-scope": [
        "inherited:n29_closeout_and_ecology_handoff_i18",
        "inherited:n29_prototype_atlas_i15",
    ],
    "AE01-CTRL-04/boundary-registration": [
        "rcae-p2-i1-l01-registered-probe",
        "rcae-p2-i1-feedback-row-surface-v1",
        "rcae-p2-i1-registration-claim-boundary-v1",
    ],
    "AE01-CTRL-05/non-private-carrier-guard": [
        "rcae-p2-i1-feedback-row-surface-v1"
    ],
    "AE01-CTRL-07/composition-scope-guard": [
        "inherited:n29_prototype_atlas_i15",
        "rcae-p2-i1-l01-registered-probe",
    ],
    "AE01-CTRL-08/producer-ownership": [
        "rcae-p2-i1-option-a-adapter-v1",
        "rcae-p2-i1-registered-realization-v1",
    ],
    "AE01-CTRL-09/budget-registration": ["rcae-p2-i1-l01-registered-probe"],
    "AE01-CTRL-10/parent-context-declaration": [
        "rcae-p2-i1-l01-registered-probe",
        "rcae-p2-i1-parent-context-debt",
        "rcae-p2-i1-registration-claim-boundary-v1",
    ],
    "AE01-CTRL-11/carrier-separation": [
        "rcae-p2-i1-l01-registered-probe",
        "rcae-p2-i1-feedback-row-surface-v1",
    ],
    "AE01-CTRL-15/constructed-role": [
        "rcae-p2-i1-option-a-adapter-v1",
        "rcae-p2-i1-registered-realization-v1",
        "rcae-p2-i1-naturalization-debt",
    ],
    "AE01-CTRL-16/construction-completeness": [
        "rcae-p2-i1-option-a-adapter-v1",
        "rcae-p2-i1-registration-claim-boundary-v1",
    ],
    "AE01-CTRL-17/runtime-registration": [
        "rcae-p2-i1-registered-realization-v1",
        "ae01:runtime-receipt:5c1ea774e3cfc31e",
        "baseline-identity-registry",
    ],
}
EXPECTED_RESOLVABLE_EVIDENCE_DESCRIPTIONS = {
    "AE01-CTRL-01/record-role-guard": ["source role and runtime-permission audit"],
    "AE01-CTRL-02/n30-ceiling-verification": [
        "N30 artifact path and digest",
        "inherited role",
        "identical-scope result",
        "must_not_consume_as",
        "new lane execution required",
    ],
    "AE01-CTRL-03/n29-component-scope": [
        "N29 artifact path and digest",
        "inherited role",
        "identical-scope result",
        "must_not_consume_as",
        "new lane execution required",
    ],
    "AE01-CTRL-04/boundary-registration": [
        "participant and medium carrier account",
        "parent-context declaration",
    ],
    "AE01-CTRL-05/non-private-carrier-guard": [
        "model-owned surface identity and access scope"
    ],
    "AE01-CTRL-07/composition-scope-guard": [
        "component ownership",
        "ordered interface plan",
        "must_not_consume_as composition success",
    ],
    "AE01-CTRL-08/producer-ownership": [
        "constructed mechanism and native operation ownership"
    ],
    "AE01-CTRL-09/budget-registration": ["reserve and packet debit projections"],
    "AE01-CTRL-10/parent-context-declaration": [
        "parent absent declaration and claim ceiling"
    ],
    "AE01-CTRL-11/carrier-separation": [
        "participant and medium IDs",
        "non-circular continuity",
        "writer-reader relation",
    ],
    "AE01-CTRL-15/constructed-role": [
        "realization profile",
        "producer transition discipline",
        "constructed evidence role",
    ],
    "AE01-CTRL-16/construction-completeness": [
        "necessity minimality counterfactual withdrawal debt discriminator and claim ceiling"
    ],
    "AE01-CTRL-17/runtime-registration": [
        "path-free profile binding receipt and no-fallback policy"
    ],
}
REGISTRATION_RECORD_DIR = "contracts/p2-i1/registration-records"
REGISTRATION_PROFILE_REGISTRY_PATH = "configs/p2_i1_registration_profiles.json"
RETAINED_GENERATED_PATHS = {
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/inherited-control-verification.json",
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-runtime-binding-receipt.json",
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/baseline-identity-registry.json",
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-freeze.json",
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-manifest.json",
}
REGISTRATION_RECORD_IDS = {
    "claim_boundary": "rcae-p2-i1-registration-claim-boundary-v1",
    "constructed_mechanism": "rcae-p2-i1-option-a-adapter-v1",
    "medium_surface": "rcae-p2-i1-feedback-row-surface-v1",
    "pattern_card": "rcae-p2-i1-l01-registered-probe",
}
REGISTRATION_DEBT_IDS = {
    "rcae-p2-i1-naturalization-debt",
    "rcae-p2-i1-participant-mediated-reader-debt",
    "rcae-p2-i1-fixed-order-debt",
    "rcae-p2-i1-parent-context-debt",
}
INHERITED_SOURCES = (
    {
        "reference_id": "n29_closeout_and_ecology_handoff_i18",
        "graph_relative_path": "experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_closeout_and_ecology_handoff_i18.json",
        "file_sha256": "842ba57e994bbb3e219acff741afd85c87d102bea5eec6d134f3b84f2445cb52",
        "output_digest": "fa21662f0a69d582bfe574311110f2610a21e6e4e352991823ce47280e0e8ff5",
        "inherited_role": "claim-clean bridge, debt, and probe-contract handoff",
        "must_not_consume_as": "executed ecology runtime, native ecology, agency, life, or Phase 8 completion",
    },
    {
        "reference_id": "n29_prototype_atlas_i15",
        "graph_relative_path": "experiments/2026-06-N29-lgrc-agentic-ecology-convergence-bridge/outputs/n29_prototype_atlas_classification_i15.json",
        "file_sha256": "1a810918df2923b5f5fe475ec9d0cc1f843fe614640b8149ea25173aab985a26",
        "output_digest": "e139dd61fcd2b0998282033e5fe1a041891291d5db036982063e510be33f7cd2",
        "inherited_role": "prototype component classification and explicit producer/composition debt",
        "must_not_consume_as": "executed P2-I1 composition, native support, or ecology success",
    },
    {
        "reference_id": "n30_replay_controls_i7",
        "graph_relative_path": "experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_replay_controls_i7.json",
        "file_sha256": "bf29695841f87fc40b2464114129a19e8616c2f8e6efa49a09a472ed65cca264",
        "output_digest": "46f7eba93fa206355f4dc3eb5b2ae8e70dd1126eba975030a2e2fc15f1603fec",
        "inherited_role": "replay/control method and bounded artifact-level medium candidate",
        "must_not_consume_as": "fresh P2-I1 runtime, final N30 closeout, or native shared-medium organization",
    },
    {
        "reference_id": "n30_closeout_and_spiral_handoff_i8",
        "graph_relative_path": "experiments/2026-07-N30-lgrc-minimal-shared-medium-participation/outputs/n30_closeout_and_spiral_handoff_i8.json",
        "file_sha256": "ade32c848cbffa4d5757bfce50eaadb72a63a8252a8ba09e5fd562c6c100718c",
        "output_digest": "7971163b1d7bd4027f5375270cfb2445cfe4698a8869b28e26f9273d0a5b5af6",
        "inherited_role": "P2/M2 trace-mediated eligibility evidence and control-pattern handoff",
        "must_not_consume_as": "niche formation, coordination, agency, parent-basin modulation, or executed agentic ecology",
    },
    {
        "reference_id": "n30_plus_shared_medium_ecology_handoff",
        "graph_relative_path": "experiments/N30_plus_LGRC_SharedMediumEcologyHandoff.md",
        "file_sha256": "8fa69faf1631256fc1ef116715ee51387b578cc6d053df9ed3e51fdfcc831bb4",
        "output_digest": None,
        "inherited_role": "current cross-project spiral direction and method",
        "must_not_consume_as": "runtime evidence, fixed N31 selection, or a positive P2-I1 result",
    },
)


def _load_cal_pre_configs() -> dict[str, Any]:
    root = experiment_root()
    return {name: load_json(root / path) for name, path in CONFIG_PATHS.items()}


def load_registration_policy() -> dict[str, Any]:
    return load_json(experiment_root() / REGISTRATION_POLICY_PATH)


def _registration_identity_projections(
    configs: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    experiment = experiment_root()
    config_digests = {
        f"{name}_config_digest": digest_canonical_data(configs[name])
        for name in CONFIG_PATHS
    }
    policy_digests = policy_projection_digests(configs["analysis"])
    profile_identities = static_profile_identities(configs["fixture"])
    realization = {
        "fixture_config_digest": config_digests["fixture_config_digest"],
        "analysis_config_digest": config_digests["analysis_config_digest"],
        "calibration_config_digest": config_digests["calibration_config_digest"],
        "provenance_config_digest": config_digests["provenance_config_digest"],
        "analysis_script_sha256": digest_file(experiment / "scripts/p2_i1_analysis.py"),
        **policy_digests,
        "static_opportunity_profile_digests": [
            row["opportunity_profile_digest"] for row in profile_identities
        ],
    }
    measurement = {
        **realization,
        "cells_config_digest": config_digests["cells_config_digest"],
        "runtime_config_digest": config_digests["runtime_config_digest"],
    }
    return realization, measurement


def _validate_control_plans(policy: Mapping[str, Any], cell_ids: list[str]) -> None:
    controls = policy.get("control_plans")
    if not isinstance(controls, list):
        raise ContractError("registration policy requires control_plans list")
    observed_ids = [row.get("control_id") for row in controls]
    if observed_ids != CONTROL_IDS:
        raise ContractError("registration control IDs or order drifted")
    if len(observed_ids) != len(set(observed_ids)):
        raise ContractError("registration control IDs must be unique")
    observed_binding_keys: set[str] = set()
    for control in controls:
        control_id = control["control_id"]
        applicability = control.get("applicability")
        if applicability not in {"applicable", "not_applicable"}:
            raise ContractError(f"{control_id}: invalid applicability")
        if not isinstance(control.get("rationale"), str) or not control["rationale"]:
            raise ContractError(f"{control_id}: applicability rationale required")
        if "outcome_status" in control:
            raise ContractError(f"{control_id}: input policy cannot declare outcome")
        legs = control.get("legs")
        if not isinstance(legs, list):
            raise ContractError(f"{control_id}: legs must be a list")
        if applicability == "not_applicable":
            if control_id != "AE01-L01-CTRL-05" or legs:
                raise ContractError(
                    "only D-025 scaffold withdrawal may be not applicable"
                )
            if control.get("not_applicable_decision_ref") != "P2-I1-DEC-025":
                raise ContractError("scaffold inapplicability must cite D-025")
            continue
        if not legs:
            raise ContractError(f"{control_id}: applicable control requires legs")
        leg_ids: set[str] = set()
        for leg in legs:
            leg_id = leg.get("leg_id")
            if not isinstance(leg_id, str) or not leg_id or leg_id in leg_ids:
                raise ContractError(f"{control_id}: invalid or duplicate leg ID")
            leg_ids.add(leg_id)
            if leg.get("resolution_stage") not in RESOLUTION_STAGES:
                raise ContractError(f"{control_id}/{leg_id}: invalid resolution stage")
            binding_key = f"{control_id}/{leg_id}"
            evidence_bindings = leg.get("evidence_binding_refs")
            if leg["resolution_stage"] in {
                "registration_guard",
                "inherited_verification",
            }:
                observed_binding_keys.add(binding_key)
                if evidence_bindings != EXPECTED_EVIDENCE_BINDINGS.get(binding_key):
                    raise ContractError(
                        f"{binding_key}: exact evidence bindings drifted"
                    )
                if leg.get("required_evidence") != (
                    EXPECTED_RESOLVABLE_EVIDENCE_DESCRIPTIONS.get(binding_key)
                ):
                    raise ContractError(
                        f"{binding_key}: evidence obligation description drifted"
                    )
            elif evidence_bindings is not None:
                raise ContractError(
                    f"{binding_key}: pending leg cannot claim resolved evidence"
                )
            evidence = leg.get("required_evidence")
            if not isinstance(evidence, list) or not evidence or any(
                not isinstance(value, str) or not value for value in evidence
            ):
                raise ContractError(f"{control_id}/{leg_id}: evidence required")
            if not isinstance(leg.get("fail_closed_effect"), str) or not leg[
                "fail_closed_effect"
            ]:
                raise ContractError(f"{control_id}/{leg_id}: fail-closed effect required")
            exact_cells = leg.get("exact_cells", [])
            if leg["resolution_stage"] == "execution_comparison" and not exact_cells:
                raise ContractError(
                    f"{control_id}/{leg_id}: execution leg requires exact cells"
                )
            if leg["resolution_stage"] == "execution_comparison":
                if not isinstance(leg.get("broken_relation"), str) or not leg[
                    "broken_relation"
                ]:
                    raise ContractError(
                        f"{control_id}/{leg_id}: broken relation required"
                    )
                preserved = leg.get("preserved_fields")
                if not isinstance(preserved, list) or not preserved or any(
                    not isinstance(value, str) or not value for value in preserved
                ):
                    raise ContractError(
                        f"{control_id}/{leg_id}: preserved fields required"
                    )
                if not isinstance(leg.get("expected_artifact_role"), str) or not leg[
                    "expected_artifact_role"
                ]:
                    raise ContractError(
                        f"{control_id}/{leg_id}: expected artifact role required"
                    )
            unknown_cells = set(exact_cells) - set(cell_ids)
            if unknown_cells:
                raise ContractError(
                    f"{control_id}/{leg_id}: unknown cells {sorted(unknown_cells)}"
                )
    if observed_binding_keys != set(EXPECTED_EVIDENCE_BINDINGS):
        raise ContractError("registration evidence-binding leg set drifted")


def validate_registration_policy(
    policy: Mapping[str, Any], configs: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    """Validate the registration input and return its non-evidential projection."""

    validate_configs(dict(configs))
    if policy.get("artifact_kind") != "p2_i1_registration_policy":
        raise ContractError("registration policy kind drifted")
    if policy.get("policy_id") != "rcae-p2-i1-registration-policy-v1":
        raise ContractError("registration policy identity drifted")
    if policy.get("lane_id") != "AE01-L01" or policy.get("cycle_id") != "P2-I1-C00":
        raise ContractError("registration lane or cycle drifted")
    if policy.get("candidate_outcomes_absent_required") is not True:
        raise ContractError("registration must require candidate absence")
    if policy.get("candidate_execution_authorized") is not False:
        raise ContractError("registration policy cannot authorize execution")
    if policy.get("decision_refs") != [
        f"P2-I1-DEC-{index:03d}" for index in range(1, 26)
    ]:
        raise ContractError("registration decision set drifted")

    imports = policy.get("identity_imports", {})
    for key in ("cal_pre_identity_path", "calibration_path", "frozen_metric_sheet_path"):
        validate_portable_path(str(imports.get(key, "")))
    cal_pre = load_json(experiment_root() / imports["cal_pre_identity_path"])
    calibration = load_json(experiment_root() / imports["calibration_path"])
    metric_sheet = load_json(experiment_root() / imports["frozen_metric_sheet_path"])
    if cal_pre.get("identity_id") != "rcae-p2-i1-cal-pre-identity-v2":
        raise ContractError("registration must import the v2 CAL-PRE identity")
    if cal_pre.get("candidate_outcomes_absent") is not True:
        raise ContractError("CAL-PRE identity does not preserve candidate absence")
    if calibration.get("record", {}).get("calibration_id") != imports.get(
        "metric_calibration_id"
    ):
        raise ContractError("metric calibration reference drifted")
    sheet_record = metric_sheet.get("record", {})
    if sheet_record.get("metric_sheet_id") != imports.get("metric_sheet_id"):
        raise ContractError("metric sheet reference drifted")
    frozen_delta = sheet_record.get("resolution_policy", {}).get("delta", {})
    if frozen_delta.get("status") != "frozen" or frozen_delta.get("value") != imports.get(
        "delta"
    ):
        raise ContractError("registration delta differs from frozen metric sheet")

    realization_projection, measurement_projection = _registration_identity_projections(
        configs
    )
    registration_realization_digest = digest_canonical_data(realization_projection)
    registration_measurement_digest = digest_canonical_data(measurement_projection)
    calibration_realization_digest = imports.get("calibration_realization_digest")
    calibration_measurement_digest = imports.get(
        "calibration_measurement_identity_digest"
    )
    if registration_realization_digest != calibration_realization_digest:
        raise ContractError("registration realization differs from calibration")
    if registration_measurement_digest != calibration_measurement_digest:
        raise ContractError("registration measurement differs from calibration")
    if cal_pre.get("calibration_realization_digest") != calibration_realization_digest:
        raise ContractError("imported CAL-PRE realization digest drifted")
    if cal_pre.get("measurement_identity_digest") != calibration_measurement_digest:
        raise ContractError("imported CAL-PRE measurement digest drifted")

    cells = policy.get("execution_policy", {}).get("cell_order")
    expected_cells = [row["cell_id"] for row in configs["cells"]["cells"]]
    if cells != expected_cells:
        raise ContractError("registration cell order differs from frozen cells")
    seeds = policy.get("execution_policy", {}).get("seeds")
    if seeds != [row["seed"] for row in configs["fixture"]["seeds"]]:
        raise ContractError("registration seeds differ from frozen fixture")
    execution = policy["execution_policy"]
    if execution.get("attempts_per_seed") != 1:
        raise ContractError("registration attempt limit drifted")
    if execution.get("infrastructure_retries_per_cell") != 1:
        raise ContractError("registration retry limit drifted")
    if execution.get("retry_seed_selection") != "lowest_seed_with_first_infrastructure_failure":
        raise ContractError("registration retry allocation drifted")
    if execution.get("fresh_worker_per_attempt") is not True:
        raise ContractError("registration must require fresh workers")
    if execution.get("worker_reuse_allowed") is not False:
        raise ContractError("registration cannot permit worker reuse")
    if policy.get("baseline_policy", {}).get("expected_configuration_count") != 21:
        raise ContractError("registration requires 21 baseline configurations")
    measurement_scope = policy.get("measurement_scope", {})
    if not (
        measurement_scope.get("primary_response_family")
        == "later_native_packet_opportunity_formation"
        and measurement_scope.get("cross_response_family_magnitude_comparison")
        == "prohibited_not_applicable_single_primary_family"
        and isinstance(measurement_scope.get("interpretation_rule"), str)
        and measurement_scope["interpretation_rule"]
    ):
        raise ContractError("registration response-family comparison boundary drifted")
    expected_roles = policy.get("expected_artifact_roles", {})
    if expected_roles.get("per_live_run") != [
        "runtime_binding_receipt",
        "initial_state_identity",
        "raw_opportunity_records",
        "branch_restoration_audit",
        "support_budget_matching_audit",
    ] or expected_roles.get("per_cell_seed") != [
        "comparison_record",
        "control_record",
        "terminal_classification_input",
    ] or expected_roles.get("registration") != [
        "registration_policy",
        "registration_freeze",
        "baseline_identity_registry",
        "realization_profile",
        "reconstruction_profile_registry",
        "runtime_preflight",
        "pattern_card",
        "medium_surface",
        "constructed_mechanism",
        "claim_boundary",
        "debt_records",
        "artifact_manifest",
    ]:
        raise ContractError("registration expected artifact roles drifted")

    realization = policy.get("realization_policy", {})
    runtime = configs["runtime"]
    if realization.get("execution_class") != runtime.get("execution_class"):
        raise ContractError("registration execution class differs from runtime policy")
    if realization.get("required_pygrc_identity") != runtime.get(
        "required_pygrc_identity"
    ):
        raise ContractError("registration PyGRC identity drifted")
    expected_operations = [runtime["preflight_operation_id"], *runtime["required_operations"]]
    if realization.get("allowed_operation_classes") != expected_operations:
        raise ContractError("registration operation classes drifted")
    if realization.get("profile_grants_execution_authority") is not False:
        raise ContractError("realization profile cannot grant execution authority")

    _validate_control_plans(policy, expected_cells)
    claims = policy.get("claim_boundary", {})
    if any(
        claims.get(key) is not False
        for key in (
            "positive_lane_evidence_opened",
            "candidate_execution_opened",
            "native_niche_claim_opened",
        )
    ):
        raise ContractError("registration policy opened an unsafe claim")

    result = {
        "artifact_kind": "p2_i1_registration_policy_validation",
        "schema_version": "1.0.0",
        "evidence_effect": "none_registration_validation_only",
        "status": "passed",
        "lane_id": policy["lane_id"],
        "cycle_id": policy["cycle_id"],
        "registration_policy_digest": digest_canonical_data(policy),
        "registration_measurement_identity_digest": registration_measurement_digest,
        "calibration_measurement_identity_digest": calibration_measurement_digest,
        "measurement_identity_match": True,
        "registration_realization_digest": registration_realization_digest,
        "calibration_realization_digest": calibration_realization_digest,
        "realization_identity_match": True,
        "control_count": len(policy["control_plans"]),
        "candidate_outcomes_absent_required": True,
        "candidate_execution_authorized": False,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def _write_output(path_value: str | None, value: Any) -> None:
    rendered = pretty_json_dumps(value)
    if path_value is None:
        sys.stdout.write(rendered)
        return
    path = find_repository_root() / validate_portable_path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def _assert_no_machine_local_paths(value: Any, *, field: str = "record") -> None:
    """Reject machine-local path strings while allowing portable repo identities."""

    if isinstance(value, Mapping):
        for key, item in value.items():
            _assert_no_machine_local_paths(item, field=f"{field}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_no_machine_local_paths(item, field=f"{field}[{index}]")
        return
    if isinstance(value, str) and (
        value.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", value)
    ):
        raise ContractError(f"machine-local path recorded at {field}")


def _git_revision_for_tree(tree: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(tree), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _source_changes_from_porcelain(status_text: str) -> list[str]:
    changes: list[str] = []
    for line in status_text.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        if path not in RETAINED_GENERATED_PATHS:
            changes.append(line)
    return changes


def _source_worktree_changes() -> list[str]:
    """Return source changes while ignoring only the five generated outputs."""

    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=find_repository_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    return _source_changes_from_porcelain(completed.stdout)


def _source_state(*, allow_dirty_preview: bool) -> dict[str, Any]:
    changes = _source_worktree_changes()
    clean = not changes
    if not clean and not allow_dirty_preview:
        raise ContractError(
            "registration retention requires a clean source worktree; "
            "use --allow-dirty-preview only for non-retainable review output"
        )
    return {
        "source_revision": _git_revision(),
        "source_worktree_clean": clean,
        "retention_eligible": clean,
        "preview_only": not clean,
    }


def build_inherited_verification(
    graph_root: Path, *, allow_dirty_preview: bool = False
) -> dict[str, Any]:
    """Verify the exact read-only graph sources without retaining a local path."""

    rows: list[dict[str, Any]] = []
    with ReadOnlyTreeGuard(graph_root):
        if _git_revision_for_tree(graph_root) != "1f42cb1d1e591159afc2ca54cc656b574d41c8d3":
            raise ContractError("graph source revision differs from admitted inventory")
        status = subprocess.run(
            ["git", "-C", str(graph_root), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        )
        if status.stdout.strip():
            raise ContractError("graph source worktree must be clean for verification")
        for expected in INHERITED_SOURCES:
            path = graph_root / expected["graph_relative_path"]
            if not path.is_file():
                raise ContractError(
                    f"missing inherited source: {expected['reference_id']}"
                )
            observed_sha = digest_file(path)
            if observed_sha != expected["file_sha256"]:
                raise ContractError(
                    f"inherited source digest drifted: {expected['reference_id']}"
                )
            observed_output_digest = None
            if expected["output_digest"] is not None:
                payload = load_json(path)
                observed_output_digest = payload.get("output_digest")
                if observed_output_digest != expected["output_digest"]:
                    raise ContractError(
                        "inherited semantic digest drifted: "
                        f"{expected['reference_id']}"
                    )
            row = {
                "reference_id": expected["reference_id"],
                "source_path": f"grc:{expected['graph_relative_path']}",
                "file_sha256": observed_sha,
                "inherited_role": expected["inherited_role"],
                "identical_scope_verification": {
                    "carrier": False,
                    "mechanism": False,
                    "intervention": False,
                    "claim_scope": False,
                    "identical_scope": False,
                    "rationale": "P2-I1 uses a fresh fixture, intervention matrix, live realization, and ecology-side claim boundary",
                },
                "must_not_consume_as": expected["must_not_consume_as"],
                "new_lane_execution_required": True,
            }
            if observed_output_digest is not None:
                row["output_digest"] = observed_output_digest
            rows.append(row)
    source_state = _source_state(allow_dirty_preview=allow_dirty_preview)
    result = {
        "artifact_kind": (
            "p2_i1_inherited_control_verification"
            if source_state["retention_eligible"]
            else "p2_i1_inherited_control_verification_preview"
        ),
        "schema_version": "1.0.0",
        "evidence_effect": "registration_only_inherited_boundary",
        "lane_id": "AE01-L01",
        "cycle_id": "P2-I1-C00",
        "graph_source_revision": "1f42cb1d1e591159afc2ca54cc656b574d41c8d3",
        "graph_source_worktree_clean": True,
        "graph_repository_write_observed": False,
        **source_state,
        "source_count": len(rows),
        "sources": rows,
        "candidate_artifacts_consumed": False,
        "candidate_execution_performed": False,
        "lane_specific_causal_evidence_inherited": False,
        "new_lane_execution_required": True,
    }
    with_digest = {**result, "canonical_payload_digest": digest_canonical_data(result)}
    validate_inherited_verification(
        with_digest, allow_preview=allow_dirty_preview
    )
    return with_digest


def validate_inherited_verification(
    record: Mapping[str, Any], *, allow_preview: bool = False
) -> None:
    expected_kind = (
        "p2_i1_inherited_control_verification_preview"
        if record.get("preview_only") is True
        else "p2_i1_inherited_control_verification"
    )
    if record.get("artifact_kind") != expected_kind:
        raise ContractError("inherited verification kind drifted")
    if record.get("preview_only") is True and not allow_preview:
        raise ContractError("inherited verification preview is not retainable")
    if not (
        isinstance(record.get("source_revision"), str)
        and re.fullmatch(r"[0-9a-f]{40}", record["source_revision"])
        and record.get("source_worktree_clean")
        is record.get("retention_eligible")
        and record.get("preview_only") is (not record.get("retention_eligible"))
    ):
        raise ContractError("inherited verification source-state boundary drifted")
    if record.get("graph_source_revision") != (
        "1f42cb1d1e591159afc2ca54cc656b574d41c8d3"
    ):
        raise ContractError("inherited graph revision drifted")
    if record.get("graph_repository_write_observed") is not False:
        raise ContractError("inherited verification violated graph read-only boundary")
    if record.get("graph_source_worktree_clean") is not True:
        raise ContractError("inherited verification requires a clean graph source")
    if any(
        record.get(key) is not False
        for key in (
            "candidate_artifacts_consumed",
            "candidate_execution_performed",
            "lane_specific_causal_evidence_inherited",
        )
    ):
        raise ContractError("inherited verification opened candidate evidence")
    if record.get("new_lane_execution_required") is not True:
        raise ContractError("inherited verification must require fresh lane execution")
    rows = record.get("sources")
    if not isinstance(rows, list) or len(rows) != len(INHERITED_SOURCES):
        raise ContractError("inherited source set drifted")
    if record.get("source_count") != len(rows):
        raise ContractError("inherited source count drifted")
    for row, expected in zip(rows, INHERITED_SOURCES):
        if row.get("reference_id") != expected["reference_id"]:
            raise ContractError("inherited source order or identity drifted")
        if row.get("source_path") != f"grc:{expected['graph_relative_path']}":
            raise ContractError(f"{expected['reference_id']}: source path drifted")
        if row.get("file_sha256") != expected["file_sha256"]:
            raise ContractError(f"{expected['reference_id']}: file digest drifted")
        if row.get("output_digest") != expected["output_digest"]:
            raise ContractError(f"{expected['reference_id']}: output digest drifted")
        if row.get("inherited_role") != expected["inherited_role"]:
            raise ContractError(f"{expected['reference_id']}: inherited role drifted")
        if row.get("must_not_consume_as") != expected["must_not_consume_as"]:
            raise ContractError(f"{expected['reference_id']}: claim boundary drifted")
        scope = row.get("identical_scope_verification", {})
        if any(
            scope.get(key) is not False
            for key in (
                "carrier",
                "mechanism",
                "intervention",
                "claim_scope",
                "identical_scope",
            )
        ):
            raise ContractError(f"{expected['reference_id']}: scope was over-inherited")
        if row.get("new_lane_execution_required") is not True:
            raise ContractError(f"{expected['reference_id']}: fresh execution omitted")
    _assert_no_machine_local_paths(record)
    payload = {
        key: value for key, value in record.items() if key != "canonical_payload_digest"
    }
    if record.get("canonical_payload_digest") != digest_canonical_data(payload):
        raise ContractError("inherited verification canonical digest drifted")


def validate_registration_records(
    record_dir: Path, realization_profile: Mapping[str, Any]
) -> dict[str, dict[str, Any]]:
    """Validate and cross-resolve the existing-schema registration records."""

    schema = load_json(experiment_root() / "contracts/schemas/ae01-contract.schema.json")
    records = [load_json(path) for path in sorted(record_dir.glob("*.json"))]
    if len(records) != 8:
        raise ContractError("registration requires exactly eight experiment records")
    by_type: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        validate_record(record, schema)
        _assert_no_machine_local_paths(record)
        by_type.setdefault(record["record_type"], []).append(record)
    for record_type in REGISTRATION_RECORD_IDS:
        if len(by_type.get(record_type, [])) != 1:
            raise ContractError(f"registration requires one {record_type} record")
    debts = by_type.get("debt_record", [])
    if {row["record"]["debt_id"] for row in debts} != REGISTRATION_DEBT_IDS:
        raise ContractError("registration debt set drifted")
    id_fields = {
        "claim_boundary": "claim_boundary_id",
        "constructed_mechanism": "mechanism_id",
        "medium_surface": "medium_surface_id",
        "pattern_card": "pattern_id",
    }
    resolved: dict[str, dict[str, Any]] = {}
    for record_type, expected_id in REGISTRATION_RECORD_IDS.items():
        record = by_type[record_type][0]
        if record["record"].get(id_fields[record_type]) != expected_id:
            raise ContractError(f"registration {record_type} identity drifted")
        resolved[record_type] = record
    profile = realization_profile.get("record", realization_profile)
    claim_id = REGISTRATION_RECORD_IDS["claim_boundary"]
    mechanism_id = REGISTRATION_RECORD_IDS["constructed_mechanism"]
    medium_id = REGISTRATION_RECORD_IDS["medium_surface"]
    expected_profile_id = "rcae-p2-i1-registered-realization-v1"
    if profile.get("profile_id") != expected_profile_id:
        raise ContractError("registration realization profile identity drifted")
    if profile.get("claim_boundary_ref") != claim_id:
        raise ContractError("realization profile claim boundary does not resolve")
    if set(profile.get("debt_refs", [])) - REGISTRATION_DEBT_IDS:
        raise ContractError("realization profile has unresolved debt")
    mechanism = resolved["constructed_mechanism"]["record"]
    if not (
        mechanism.get("claim_boundary_ref") == claim_id
        and mechanism.get("realization_profile_ref") == expected_profile_id
        and set(mechanism.get("debt_refs", [])) <= REGISTRATION_DEBT_IDS
    ):
        raise ContractError("constructed mechanism references do not resolve")
    medium = resolved["medium_surface"]["record"]
    if not (
        medium.get("claim_boundary_ref") == claim_id
        and set(medium.get("debt_refs", [])) <= REGISTRATION_DEBT_IDS
    ):
        raise ContractError("medium surface references do not resolve")
    pattern = resolved["pattern_card"]["record"]
    if not (
        pattern.get("claim_boundary_ref") == claim_id
        and pattern.get("medium_surface_refs") == [medium_id]
        and pattern.get("constructed_mechanism_refs") == [mechanism_id]
        and pattern.get("realization_profile_refs") == [expected_profile_id]
        and set(pattern.get("debt_refs", [])) == REGISTRATION_DEBT_IDS
        and pattern.get("control_refs") == CONTROL_IDS
    ):
        raise ContractError("pattern card registration references do not resolve")
    if pattern.get("composition_refs") != []:
        raise ContractError("L01 registration cannot carry a composition result")
    if {row.get("metric_id") for row in pattern.get("economy_metrics", [])} != {
        "p2_i1_participant_repeat_reserve",
        "p2_i1_packet_load",
        "p2_i1_state_leakage",
    }:
        raise ContractError("pattern card economy evidence drifted")
    root = find_repository_root()
    for source_ref in pattern.get("source_refs", []):
        if source_ref.get("evidence_role") != "conceptual_motivation":
            raise ContractError("pattern conceptual source role drifted")
        path = root / validate_portable_path(source_ref["path"])
        if not path.is_file() or digest_file(path) != source_ref.get("file_sha256"):
            raise ContractError("pattern conceptual source digest drifted")
    resolved["debt_records"] = {row["record"]["debt_id"]: row for row in debts}
    return resolved


def load_registration_profile_registry() -> dict[str, Any]:
    registry = load_json(experiment_root() / REGISTRATION_PROFILE_REGISTRY_PATH)
    schema = load_json(experiment_root() / "contracts/schemas/ae01-contract.schema.json")
    validate_record(registry, schema)
    _assert_no_machine_local_paths(registry)
    expected = {
        "rcae-p2-i1-environment-v1": "environment",
        "rcae-p2-i1-command-digest-v1": "command",
        "rcae-p2-i1-command-inherited-v1": "command",
        "rcae-p2-i1-command-runtime-receipt-v1": "command",
        "rcae-p2-i1-command-baseline-v1": "command",
        "rcae-p2-i1-command-freeze-v1": "command",
        "rcae-p2-i1-command-manifest-v1": "command",
        "rcae-p2-i1-dependencies-v1": "dependency",
        "rcae-p2-i1-resource-v1": "resource",
    }
    profiles = registry["record"]["profiles"]
    observed = {row["profile_id"]: row["profile_type"] for row in profiles}
    if observed != expected:
        raise ContractError("registration reconstruction profile set drifted")
    return registry


def _load_realization_profile(path_value: str) -> dict[str, Any]:
    path = find_repository_root() / validate_portable_path(path_value)
    profile = load_json(path)
    schema = load_json(experiment_root() / "contracts/schemas/ae01-contract.schema.json")
    validate_record(profile, schema)
    if profile.get("record_type") != "realization_profile":
        raise ContractError("registration baseline requires a realization_profile")
    return profile


def _validate_profile_against_policy(
    profile: Mapping[str, Any], policy: Mapping[str, Any]
) -> None:
    payload = profile.get("record", profile)
    expected = policy["realization_policy"]
    if payload.get("profile_id") != expected["profile_id"]:
        raise ContractError("realization profile ID differs from registration policy")
    if payload.get("required_pygrc_identity") != expected["required_pygrc_identity"]:
        raise ContractError("realization profile PyGRC identity drifted")
    if payload.get("required_capabilities") != expected["required_public_capabilities"]:
        raise ContractError("realization profile capability set drifted")
    if payload.get("allowed_scheduling_operations") != expected[
        "allowed_operation_classes"
    ]:
        raise ContractError("realization profile operation classes drifted")


def build_baseline_entry(
    *,
    seed: int,
    cell_id: str,
    configs: Mapping[str, Mapping[str, Any]],
    realization_profile: Mapping[str, Any],
) -> dict[str, Any]:
    """Construct one W0 baseline without scheduling a scientific operation."""

    modules = bind_runtime(configs["runtime"], realization_profile)
    model, route_aspect = build_fixture(
        configs["fixture"],
        configs["cells"],
        modules,
        seed=seed,
        cell_id=cell_id,
    )
    snapshot = model.snapshot()
    state = model.get_state()
    queue = state.packet_ledger.event_queue_records
    surfaces = state.causal_pulse_substrate_surface_log
    if queue or surfaces:
        raise ContractError("registered W0 baseline requires empty queue and surface")
    cell = next(
        row for row in configs["cells"]["cells"] if row["cell_id"] == cell_id
    )
    route_artifact = route_aspect.to_artifact()
    projection = {
        "cell_id": cell_id,
        "seed": seed,
        "fixture_config_digest": digest_canonical_data(configs["fixture"]),
        "cell_configuration_digest": digest_canonical_data(cell),
        "runtime_config_digest": digest_canonical_data(configs["runtime"]),
        "resolved_node_coherences": resolve_node_coherences(
            configs["fixture"], seed, cell_id, configs["cells"]
        ),
        "reader_packet_amount": resolve_reader_packet_amount(
            configs["fixture"], configs["cells"], cell_id
        ),
        "route_aspect_digest": route_artifact["route_aspect_digest"],
        "snapshot_digest": digest_canonical_data(snapshot),
        "queue_digest": digest_canonical_data(list(queue)),
        "focal_surface_digest": digest_canonical_data(list(surfaces)),
    }
    return {
        **projection,
        "expected_composite_baseline_digest": digest_canonical_data(projection),
    }


def command_baseline_one(args: argparse.Namespace) -> int:
    configs = _load_cal_pre_configs()
    policy = load_registration_policy()
    validate_registration_policy(policy, configs)
    if args.cell not in policy["execution_policy"]["cell_order"]:
        raise ContractError("baseline worker received an unregistered cell")
    if args.seed not in policy["execution_policy"]["seeds"]:
        raise ContractError("baseline worker received an unregistered seed")
    profile = _load_realization_profile(args.realization_profile)
    _validate_profile_against_policy(profile, policy)
    guard = ReadOnlyTreeGuard(Path(args.graph_root)) if args.graph_root else nullcontext()
    with guard:
        entry = build_baseline_entry(
            seed=args.seed,
            cell_id=args.cell,
            configs=configs,
            realization_profile=profile,
        )
    sys.stdout.write(pretty_json_dumps(entry))
    return 0


def validate_baseline_registry(
    registry: Mapping[str, Any],
    policy: Mapping[str, Any],
    configs: Mapping[str, Mapping[str, Any]],
    *,
    allow_preview: bool = False,
) -> None:
    """Validate ordering, static identities, and candidate-free W0 entries."""

    expected_kind = (
        "p2_i1_baseline_identity_registry_preview"
        if registry.get("preview_only") is True
        else "p2_i1_baseline_identity_registry"
    )
    if registry.get("artifact_kind") != expected_kind:
        raise ContractError("baseline registry kind drifted")
    if registry.get("preview_only") is True and not allow_preview:
        raise ContractError("baseline registry preview is not retainable")
    if not (
        isinstance(registry.get("source_revision"), str)
        and re.fullmatch(r"[0-9a-f]{40}", registry["source_revision"])
        and registry.get("source_worktree_clean")
        is registry.get("retention_eligible")
        and registry.get("preview_only") is (not registry.get("retention_eligible"))
    ):
        raise ContractError("baseline registry source-state boundary drifted")
    if registry.get("fresh_worker_per_entry") is not True:
        raise ContractError("baseline registry must use one fresh worker per entry")
    if registry.get("candidate_operations_executed") is not False:
        raise ContractError("baseline registry cannot execute candidate operations")
    if registry.get("candidate_outcomes_absent") is not True:
        raise ContractError("baseline registry must preserve candidate absence")
    if not (
        registry.get("lane_id") == policy["lane_id"]
        and registry.get("cycle_id") == policy["cycle_id"]
        and registry.get("registration_policy_digest")
        == digest_canonical_data(policy)
        and registry.get("realization_profile_id")
        == policy["realization_policy"]["profile_id"]
    ):
        raise ContractError("baseline registry registration identity drifted")
    expected_pairs = [
        (cell_id, seed)
        for cell_id in policy["execution_policy"]["cell_order"]
        for seed in policy["execution_policy"]["seeds"]
    ]
    entries = registry.get("entries")
    if not isinstance(entries, list) or len(entries) != len(expected_pairs):
        raise ContractError("baseline registry entry count drifted")
    if registry.get("entry_count") != len(expected_pairs):
        raise ContractError("baseline registry declared count drifted")
    observed_pairs = [(row.get("cell_id"), row.get("seed")) for row in entries]
    if observed_pairs != expected_pairs:
        raise ContractError("baseline registry order or configuration set drifted")
    empty_digest = digest_canonical_data([])
    fixture_digest = digest_canonical_data(configs["fixture"])
    runtime_digest = digest_canonical_data(configs["runtime"])
    cell_map = {row["cell_id"]: row for row in configs["cells"]["cells"]}
    for entry in entries:
        cell_id = entry["cell_id"]
        seed = int(entry["seed"])
        if entry.get("fixture_config_digest") != fixture_digest:
            raise ContractError(f"{cell_id}/{seed}: fixture digest drifted")
        if entry.get("cell_configuration_digest") != digest_canonical_data(
            cell_map[cell_id]
        ):
            raise ContractError(f"{cell_id}/{seed}: cell digest drifted")
        if entry.get("runtime_config_digest") != runtime_digest:
            raise ContractError(f"{cell_id}/{seed}: runtime digest drifted")
        if entry.get("resolved_node_coherences") != resolve_node_coherences(
            configs["fixture"], seed, cell_id, configs["cells"]
        ):
            raise ContractError(f"{cell_id}/{seed}: node coherences drifted")
        if entry.get("reader_packet_amount") != resolve_reader_packet_amount(
            configs["fixture"], configs["cells"], cell_id
        ):
            raise ContractError(f"{cell_id}/{seed}: reader packet amount drifted")
        if entry.get("queue_digest") != empty_digest:
            raise ContractError(f"{cell_id}/{seed}: queue is not empty")
        if entry.get("focal_surface_digest") != empty_digest:
            raise ContractError(f"{cell_id}/{seed}: surface is not empty")
        for key in ("route_aspect_digest", "snapshot_digest"):
            value = entry.get(key)
            if not isinstance(value, str) or len(value) != 64:
                raise ContractError(f"{cell_id}/{seed}: invalid {key}")
        projection = {
            key: value
            for key, value in entry.items()
            if key != "expected_composite_baseline_digest"
        }
        if entry.get("expected_composite_baseline_digest") != digest_canonical_data(
            projection
        ):
            raise ContractError(f"{cell_id}/{seed}: composite digest drifted")
    payload = {
        key: value for key, value in registry.items() if key != "canonical_payload_digest"
    }
    if registry.get("canonical_payload_digest") != digest_canonical_data(payload):
        raise ContractError("baseline registry canonical digest drifted")


def derive_control_lifecycle(
    policy: Mapping[str, Any], resolved_evidence_ids: set[str]
) -> list[dict[str, Any]]:
    """Derive registration-time statuses only after the evidence bundle validates."""

    derived: list[dict[str, Any]] = []
    for control in policy["control_plans"]:
        if control["applicability"] == "not_applicable":
            derived.append(
                {
                    "control_id": control["control_id"],
                    "applicability": "not_applicable",
                    "applicability_rationale": control["rationale"],
                    "outcome_status": "not_applicable",
                    "decision_ref": control["not_applicable_decision_ref"],
                    "legs": [],
                }
            )
            continue
        legs: list[dict[str, Any]] = []
        for leg in control["legs"]:
            stage = leg["resolution_stage"]
            bindings = leg.get("evidence_binding_refs", [])
            missing_bindings = sorted(set(bindings) - resolved_evidence_ids)
            resolvable_stage = stage in {
                "registration_guard",
                "inherited_verification",
            }
            status = (
                "blocked"
                if resolvable_stage and missing_bindings
                else "resolved"
                if resolvable_stage
                else "pending_execution"
            )
            legs.append(
                {
                    "leg_id": leg["leg_id"],
                    "resolution_stage": stage,
                    "outcome_status": status,
                    "required_evidence": leg["required_evidence"],
                    "evidence_binding_refs": bindings,
                    "resolved_evidence_refs": (
                        bindings if status == "resolved" else []
                    ),
                    "missing_evidence_refs": missing_bindings,
                    "exact_cells": leg.get("exact_cells", []),
                    "broken_relation": leg.get("broken_relation"),
                    "preserved_fields": leg.get("preserved_fields", []),
                    "expected_artifact_role": leg.get("expected_artifact_role"),
                    "fail_closed_effect": leg["fail_closed_effect"],
                    "resolution_basis": (
                        "All exact evidence bindings passed deterministic outcome-independent validation"
                        if status == "resolved"
                        else "One or more exact evidence bindings did not resolve"
                        if status == "blocked"
                        else "No outcome may be inferred before authorized execution and terminal closure"
                    ),
                }
            )
        outcome = (
            "blocked"
            if any(leg["outcome_status"] == "blocked" for leg in legs)
            else "resolved"
            if all(leg["outcome_status"] == "resolved" for leg in legs)
            else "pending_execution"
        )
        derived.append(
            {
                "control_id": control["control_id"],
                "applicability": "applicable",
                "applicability_rationale": control["rationale"],
                "outcome_status": outcome,
                "legs": legs,
            }
        )
    return derived


def _validate_registration_runtime_receipt(
    receipt: Mapping[str, Any],
    profile: Mapping[str, Any],
    policy: Mapping[str, Any],
    *,
    allow_preview: bool = False,
) -> None:
    schema = load_json(experiment_root() / "contracts/schemas/ae01-contract.schema.json")
    validate_record(receipt, schema)
    if receipt.get("record_type") != "runtime_binding_receipt":
        raise ContractError("registration preflight must be a runtime receipt")
    payload = receipt["record"]
    expected = policy["realization_policy"]
    if not (
        payload.get("run_id") == "rcae-p2-i1-registration-preflight"
        and payload.get("execution_class") == expected["execution_class"]
        and payload.get("profile_id") == expected["profile_id"]
        and payload.get("conformance_status") == "passed"
        and payload.get("observed_runtime_identity")
        == expected["required_pygrc_identity"]
        and payload.get("requested_operations")
        == expected["allowed_operation_classes"]
        and payload.get("graph_repository_write_observed") is False
    ):
        raise ContractError("registration runtime binding receipt does not conform")
    extensions = payload.get("extensions", {})
    if not (
        isinstance(extensions.get("x_source_revision"), str)
        and re.fullmatch(r"[0-9a-f]{40}", extensions["x_source_revision"])
        and extensions.get("x_source_worktree_clean")
        is extensions.get("x_retention_eligible")
        and extensions.get("x_preview_only")
        is (not extensions.get("x_retention_eligible"))
    ):
        raise ContractError("registration runtime receipt source-state boundary drifted")
    if extensions.get("x_preview_only") is True and not allow_preview:
        raise ContractError("registration runtime receipt preview is not retainable")
    if extensions.get("x_operation_capabilities") != {
        key: list(value) for key, value in OPERATION_CAPABILITY_PATHS.items()
    }:
        raise ContractError("registration runtime operation capabilities drifted")
    pattern_receipts = profile.get("record", profile).get("profile_id")
    if pattern_receipts != expected["profile_id"]:
        raise ContractError("runtime receipt profile does not resolve")
    _assert_no_machine_local_paths(receipt)


def _bundle_file_identity(root: Path, path: Path) -> dict[str, Any]:
    relative = path.relative_to(root).as_posix()
    validate_portable_path(relative)
    result = {
        "path": relative,
        "file_sha256": digest_file(path),
        "size_bytes": path.stat().st_size,
    }
    if path.suffix == ".json":
        result["canonical_json_digest"] = digest_canonical_data(load_json(path))
    return result


def _resolved_registration_evidence_ids(
    *,
    records: Mapping[str, Any],
    profile_registry: Mapping[str, Any],
    profile: Mapping[str, Any],
    baseline: Mapping[str, Any],
    inherited: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> set[str]:
    """Return only evidence identities whose concrete validators have passed."""

    source_inventory = experiment_root() / "contracts/source-inventory.md"
    if not source_inventory.is_file():
        raise ContractError("accepted source inventory is unavailable")
    result = {
        "source-inventory",
        records["claim_boundary"]["record"]["claim_boundary_id"],
        records["constructed_mechanism"]["record"]["mechanism_id"],
        records["medium_surface"]["record"]["medium_surface_id"],
        records["pattern_card"]["record"]["pattern_id"],
        *records["debt_records"].keys(),
        profile_registry["record"]["profile_registry_id"],
        profile["record"]["profile_id"],
        "baseline-identity-registry",
        receipt["record"]["receipt_id"],
    }
    if baseline.get("candidate_outcomes_absent") is not True:
        raise ContractError("baseline evidence identity did not validate")
    for row in inherited["sources"]:
        result.add(f"inherited:{row['reference_id']}")
    return result


def build_registration_freeze(
    *,
    baseline_path: Path,
    inherited_path: Path,
    receipt_path: Path,
    record_dir: Path,
    allow_dirty_preview: bool = False,
) -> dict[str, Any]:
    """Resolve the registration bundle without authorizing candidate execution."""

    root = find_repository_root()
    source_state = _source_state(allow_dirty_preview=allow_dirty_preview)
    configs = _load_cal_pre_configs()
    policy = load_registration_policy()
    policy_validation = validate_registration_policy(policy, configs)
    profile_registry = load_registration_profile_registry()
    profile_path = experiment_root() / policy["realization_policy"]["profile_path"]
    profile = _load_realization_profile(
        profile_path.relative_to(root).as_posix()
    )
    _validate_profile_against_policy(profile, policy)
    resolved_records = validate_registration_records(record_dir, profile)
    baseline = load_json(baseline_path)
    validate_baseline_registry(
        baseline, policy, configs, allow_preview=allow_dirty_preview
    )
    current_revision = source_state["source_revision"]
    if baseline.get("source_revision") != current_revision:
        raise ContractError("baseline registry does not anchor to current source revision")
    inherited = load_json(inherited_path)
    validate_inherited_verification(inherited, allow_preview=allow_dirty_preview)
    receipt = load_json(receipt_path)
    _validate_registration_runtime_receipt(
        receipt, profile, policy, allow_preview=allow_dirty_preview
    )
    receipt_source = receipt["record"]["extensions"]
    if not (
        inherited.get("source_revision") == current_revision
        and receipt_source.get("x_source_revision") == current_revision
    ):
        raise ContractError("registration inputs do not share the source revision")
    inputs_retention_eligible = all(
        (
            baseline.get("retention_eligible") is True,
            inherited.get("retention_eligible") is True,
            receipt_source.get("x_retention_eligible") is True,
        )
    )
    freeze_retention_eligible = (
        source_state["source_worktree_clean"] and inputs_retention_eligible
    )
    freeze_state = {
        "source_revision": current_revision,
        "source_worktree_clean": source_state["source_worktree_clean"],
        "retention_eligible": freeze_retention_eligible,
        "preview_only": not freeze_retention_eligible,
    }
    receipt_id = receipt["record"]["receipt_id"]
    if resolved_records["pattern_card"]["record"].get(
        "runtime_binding_receipt_refs"
    ) != [receipt_id]:
        raise ContractError("pattern card runtime receipt does not resolve")

    authority_paths = [
        experiment_root() / REGISTRATION_POLICY_PATH,
        experiment_root() / REGISTRATION_PROFILE_REGISTRY_PATH,
        experiment_root() / "implementation/P2-I1-minimal-shared-medium-niche-brief.md",
        experiment_root() / "implementation/P2-I1-decision-record.md",
        experiment_root() / "hypotheses/lane-hypotheses.md",
        experiment_root() / "hypotheses/control-and-failure-register.md",
        experiment_root() / "contracts/source-inventory.md",
        experiment_root() / "contracts/lane-registry.json",
        experiment_root() / "contracts/p2-i1/frozen-metric-sheet.json",
        experiment_root() / "contracts/p2-i1/metric-calibration.json",
        experiment_root() / "contracts/p2-i1/cal-pre-identity-v2.json",
        profile_path,
        baseline_path,
        inherited_path,
        receipt_path,
        experiment_root() / "scripts/p2_i1_analysis.py",
        experiment_root() / "scripts/p2_i1_runtime.py",
        experiment_root() / "scripts/p2_i1_registration.py",
    ]
    authority_paths.extend(sorted(record_dir.glob("*.json")))
    authority_paths.extend(experiment_root() / path for path in CONFIG_PATHS.values())
    if len(authority_paths) != len(set(authority_paths)):
        raise ContractError("registration bundle contains duplicate artifact paths")
    identities = [_bundle_file_identity(root, path) for path in authority_paths]
    resolved_evidence_ids = _resolved_registration_evidence_ids(
        records=resolved_records,
        profile_registry=profile_registry,
        profile=profile,
        baseline=baseline,
        inherited=inherited,
        receipt=receipt,
    )
    controls = derive_control_lifecycle(policy, resolved_evidence_ids)
    leg_statuses = [
        leg["outcome_status"] for control in controls for leg in control["legs"]
    ]
    if "blocked" in leg_statuses:
        raise ContractError("registration freeze has unresolved evidence bindings")
    result = {
        "artifact_kind": (
            "p2_i1_registration_freeze"
            if freeze_state["retention_eligible"]
            else "p2_i1_registration_freeze_preview"
        ),
        "schema_version": "1.0.0",
        "evidence_effect": "registration_only",
        "freeze_id": "rcae-p2-i1-registration-freeze-v1",
        "lane_id": "AE01-L01",
        "cycle_id": "P2-I1-C00",
        **freeze_state,
        "registration_policy_digest": policy_validation[
            "registration_policy_digest"
        ],
        "profile_registry_id": profile_registry["record"]["profile_registry_id"],
        "calibration_measurement_identity_digest": policy_validation[
            "calibration_measurement_identity_digest"
        ],
        "registration_measurement_identity_digest": policy_validation[
            "registration_measurement_identity_digest"
        ],
        "measurement_identity_match": policy_validation["measurement_identity_match"],
        "calibration_realization_digest": policy_validation[
            "calibration_realization_digest"
        ],
        "registration_realization_digest": policy_validation[
            "registration_realization_digest"
        ],
        "realization_identity_match": policy_validation["realization_identity_match"],
        "realization_profile_id": policy["realization_policy"]["profile_id"],
        "runtime_binding_receipt_id": receipt_id,
        "baseline_registry_digest": baseline["canonical_payload_digest"],
        "inherited_verification_digest": inherited["canonical_payload_digest"],
        "registration_record_ids": {
            **REGISTRATION_RECORD_IDS,
            "debt_records": sorted(REGISTRATION_DEBT_IDS),
        },
        "bundle_file_count": len(identities),
        "bundle_files": identities,
        "controls": controls,
        "resolved_evidence_ids": sorted(resolved_evidence_ids),
        "control_summary": {
            "control_count": len(controls),
            "resolved_control_count": sum(
                row["outcome_status"] == "resolved" for row in controls
            ),
            "pending_execution_control_count": sum(
                row["outcome_status"] == "pending_execution" for row in controls
            ),
            "not_applicable_control_count": sum(
                row["outcome_status"] == "not_applicable" for row in controls
            ),
            "resolved_leg_count": leg_statuses.count("resolved"),
            "pending_execution_leg_count": leg_statuses.count("pending_execution"),
            "blocked_leg_count": leg_statuses.count("blocked"),
        },
        "manifest_boundary": {
            "expected_path": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-manifest.json",
            "status": "pending_resolution_after_freeze",
            "rationale": "The manifest may digest this freeze; the freeze therefore declares but cannot recursively digest the manifest",
        },
        "reconstruction": {
            "environment": ".venv with pinned repository dependencies and locally configured pygrc==0.1",
            "commands": [
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-inherited-verification --graph-root LOCAL_GRAPH_CHECKOUT --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/inherited-control-verification.json",
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-runtime-receipt --graph-root LOCAL_GRAPH_CHECKOUT --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-runtime-binding-receipt.json",
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-baseline-registry --realization-profile experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-realization-profile.json --graph-root LOCAL_GRAPH_CHECKOUT --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/baseline-identity-registry.json",
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py build-registration-freeze --baseline-registry experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/baseline-identity-registry.json --inherited-verification experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/inherited-control-verification.json --runtime-receipt experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-runtime-binding-receipt.json --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/registration-freeze.json",
            ],
        },
        "candidate_artifacts_consumed": False,
        "candidate_execution_performed": False,
        "candidate_outcomes_absent": True,
        "candidate_execution_authorized": False,
        "positive_lane_evidence_opened": False,
        "negative_lane_evidence_opened": False,
        "native_niche_claim_opened": False,
        "reg_gate_disposition": "pending_review_and_manifest",
    }
    _assert_no_machine_local_paths(result)
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def _manifest_declaration(
    *,
    path: Path,
    artifact_id: str,
    command_profile_ref: str,
    execution_class: str,
    realization_profile_id: str,
    input_digests: Mapping[str, str],
    random_seeds: list[int] | None = None,
) -> dict[str, Any]:
    payload = load_json(path)
    live = execution_class == "pygrc_runtime_with_rcae_producer"
    return {
        "artifact_id": artifact_id,
        "expected_path": path.relative_to(find_repository_root()).as_posix(),
        "command_profile_ref": command_profile_ref,
        "working_directory": ".",
        "environment_profile_ref": "rcae-p2-i1-environment-v1",
        "dependency_profile_ref": "rcae-p2-i1-dependencies-v1",
        "configuration_id": "rcae-p2-i1-registration-policy-v1",
        "input_digests": dict(input_digests),
        "random_seeds": random_seeds or [],
        "execution_class": execution_class,
        "realization_profile": (
            {
                "status": "applicable",
                "reference_id": realization_profile_id,
                "rationale": "Artifact construction bound the registered live realization",
            }
            if live
            else {
                "status": "not_applicable",
                "rationale": "Artifact is inspected or derived without a live PyGRC transition",
            }
        ),
        "artifact_kind": payload.get("artifact_kind", payload.get("record_type")),
        "schema_version": payload["schema_version"],
        "retention_mode": "tracked_selected_evidence",
        "resource_profile_ref": "rcae-p2-i1-resource-v1",
        "verification_command_profile_ref": "rcae-p2-i1-command-digest-v1",
        "evidence_use_tier": "registered_probe",
        "claim_dependency_refs": [],
    }


def build_registration_manifest(
    *,
    baseline_path: Path,
    inherited_path: Path,
    receipt_path: Path,
    freeze_path: Path,
) -> dict[str, Any]:
    """Build the non-recursive resolved manifest after verifying the freeze."""

    root = find_repository_root()
    policy = load_registration_policy()
    profile_registry = load_registration_profile_registry()
    profile_path = experiment_root() / policy["realization_policy"]["profile_path"]
    profile = _load_realization_profile(profile_path.relative_to(root).as_posix())
    expected_freeze = build_registration_freeze(
        baseline_path=baseline_path,
        inherited_path=inherited_path,
        receipt_path=receipt_path,
        record_dir=experiment_root() / REGISTRATION_RECORD_DIR,
    )
    freeze = load_json(freeze_path)
    if freeze != expected_freeze:
        raise ContractError("registration freeze does not reconstruct exactly")
    if not (
        freeze.get("artifact_kind") == "p2_i1_registration_freeze"
        and freeze.get("retention_eligible") is True
        and freeze.get("preview_only") is False
    ):
        raise ContractError("registration manifest cannot retain a preview freeze")
    policy_digest = freeze["registration_policy_digest"]
    common_input = {"registration_policy": policy_digest}
    declarations: list[dict[str, Any]] = []
    static_paths = [
        experiment_root() / REGISTRATION_PROFILE_REGISTRY_PATH,
        experiment_root() / REGISTRATION_POLICY_PATH,
        profile_path,
        *sorted((experiment_root() / REGISTRATION_RECORD_DIR).glob("*.json")),
    ]
    for path in static_paths:
        payload = load_json(path)
        record_id = payload.get("record", {}).get(
            {
                "profile_registry": "profile_registry_id",
                "realization_profile": "profile_id",
                "claim_boundary": "claim_boundary_id",
                "constructed_mechanism": "mechanism_id",
                "medium_surface": "medium_surface_id",
                "pattern_card": "pattern_id",
                "debt_record": "debt_id",
            }.get(payload.get("record_type"), "")
        )
        artifact_id = record_id or payload.get("policy_id")
        if not isinstance(artifact_id, str) or not artifact_id:
            raise ContractError(f"cannot resolve manifest artifact ID for {path.name}")
        declarations.append(
            _manifest_declaration(
                path=path,
                artifact_id=artifact_id,
                command_profile_ref="rcae-p2-i1-command-digest-v1",
                execution_class="artifact_inspection",
                realization_profile_id=policy["realization_policy"]["profile_id"],
                input_digests=common_input,
            )
        )
    generated = (
        (
            inherited_path,
            "rcae-p2-i1-inherited-control-verification",
            "rcae-p2-i1-command-inherited-v1",
            "artifact_inspection",
            [],
        ),
        (
            receipt_path,
            load_json(receipt_path)["record"]["receipt_id"],
            "rcae-p2-i1-command-runtime-receipt-v1",
            "pygrc_runtime_with_rcae_producer",
            [],
        ),
        (
            baseline_path,
            "rcae-p2-i1-baseline-identity-registry",
            "rcae-p2-i1-command-baseline-v1",
            "pygrc_runtime_with_rcae_producer",
            policy["execution_policy"]["seeds"],
        ),
        (
            freeze_path,
            freeze["freeze_id"],
            "rcae-p2-i1-command-freeze-v1",
            "artifact_inspection",
            [],
        ),
    )
    for path, artifact_id, command, execution_class, seeds in generated:
        declarations.append(
            _manifest_declaration(
                path=path,
                artifact_id=artifact_id,
                command_profile_ref=command,
                execution_class=execution_class,
                realization_profile_id=policy["realization_policy"]["profile_id"],
                input_digests=common_input,
                random_seeds=seeds,
            )
        )
    manifest = build_artifact_manifest(
        manifest_id="rcae-p2-i1-registration-manifest-v1",
        profile_registry=profile_registry,
        declarations=declarations,
        repository_root=root,
        source_revisions={
            "rcae": _git_revision(),
            "grc": load_json(inherited_path)["graph_source_revision"],
        },
        resolved_realization_profiles=[profile],
    )
    schema = load_json(experiment_root() / "contracts/schemas/ae01-contract.schema.json")
    validate_record(manifest, schema)
    _assert_no_machine_local_paths(manifest)
    return manifest


def _git_revision() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=find_repository_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def command_build_baselines(args: argparse.Namespace) -> int:
    source_state = _source_state(allow_dirty_preview=args.allow_dirty_preview)
    configs = _load_cal_pre_configs()
    policy = load_registration_policy()
    validation = validate_registration_policy(policy, configs)
    profile = _load_realization_profile(args.realization_profile)
    _validate_profile_against_policy(profile, policy)
    script = (
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
        "scripts/p2_i1_registration.py"
    )
    entries: list[dict[str, Any]] = []
    guard = ReadOnlyTreeGuard(Path(args.graph_root)) if args.graph_root else nullcontext()
    with guard:
        for cell_id in policy["execution_policy"]["cell_order"]:
            for seed in policy["execution_policy"]["seeds"]:
                command = [
                    sys.executable,
                    script,
                    "baseline-one",
                    "--realization-profile",
                    args.realization_profile,
                    "--cell",
                    cell_id,
                    "--seed",
                    str(seed),
                ]
                completed = subprocess.run(
                    command,
                    cwd=find_repository_root(),
                    check=True,
                    capture_output=True,
                    text=True,
                )
                entries.append(json.loads(completed.stdout))
    if len(entries) != policy["baseline_policy"]["expected_configuration_count"]:
        raise ContractError("baseline registry entry count drifted")
    result = {
        "artifact_kind": (
            "p2_i1_baseline_identity_registry"
            if source_state["retention_eligible"]
            else "p2_i1_baseline_identity_registry_preview"
        ),
        "schema_version": "1.0.0",
        "evidence_effect": "none_registration_infrastructure_only",
        "lane_id": policy["lane_id"],
        "cycle_id": policy["cycle_id"],
        **source_state,
        "registration_policy_digest": validation["registration_policy_digest"],
        "realization_profile_id": policy["realization_policy"]["profile_id"],
        "fresh_worker_per_entry": True,
        "entry_count": len(entries),
        "candidate_operations_executed": False,
        "candidate_outcomes_absent": True,
        "entries": entries,
    }
    with_digest = {**result, "canonical_payload_digest": digest_canonical_data(result)}
    validate_baseline_registry(
        with_digest, policy, configs, allow_preview=args.allow_dirty_preview
    )
    _write_output(args.output, with_digest)
    return 0


def command_build_inherited_verification(args: argparse.Namespace) -> int:
    result = build_inherited_verification(
        Path(args.graph_root), allow_dirty_preview=args.allow_dirty_preview
    )
    _write_output(args.output, result)
    return 0


def command_build_runtime_receipt(args: argparse.Namespace) -> int:
    source_state = _source_state(allow_dirty_preview=args.allow_dirty_preview)
    policy = load_registration_policy()
    validate_registration_policy(policy, _load_cal_pre_configs())
    profile_path = policy["realization_policy"]["profile_path"]
    profile = _load_realization_profile(
        (experiment_root() / profile_path).relative_to(find_repository_root()).as_posix()
    )
    _validate_profile_against_policy(profile, policy)
    with ReadOnlyTreeGuard(Path(args.graph_root)):
        runtime_modules = bind_runtime(_load_cal_pre_configs()["runtime"], profile)
        operation_capabilities = validate_runtime_operation_capabilities(
            runtime_modules,
            policy["realization_policy"]["allowed_operation_classes"],
        )
        receipt = build_runtime_binding_receipt(
            profile["record"],
            run_id="rcae-p2-i1-registration-preflight",
            execution_class=policy["realization_policy"]["execution_class"],
            requested_operations=policy["realization_policy"][
                "allowed_operation_classes"
            ],
        )
    receipt["record"]["extensions"] = {
        "x_source_revision": source_state["source_revision"],
        "x_source_worktree_clean": source_state["source_worktree_clean"],
        "x_retention_eligible": source_state["retention_eligible"],
        "x_preview_only": source_state["preview_only"],
        "x_operation_capabilities": operation_capabilities,
    }
    _validate_registration_runtime_receipt(
        receipt, profile, policy, allow_preview=args.allow_dirty_preview
    )
    _write_output(args.output, receipt)
    return 0


def command_build_registration_freeze(args: argparse.Namespace) -> int:
    root = find_repository_root()
    result = build_registration_freeze(
        baseline_path=root / validate_portable_path(args.baseline_registry),
        inherited_path=root / validate_portable_path(args.inherited_verification),
        receipt_path=root / validate_portable_path(args.runtime_receipt),
        record_dir=experiment_root() / REGISTRATION_RECORD_DIR,
        allow_dirty_preview=args.allow_dirty_preview,
    )
    _write_output(args.output, result)
    return 0


def command_build_registration_manifest(args: argparse.Namespace) -> int:
    root = find_repository_root()
    result = build_registration_manifest(
        baseline_path=root / validate_portable_path(args.baseline_registry),
        inherited_path=root / validate_portable_path(args.inherited_verification),
        receipt_path=root / validate_portable_path(args.runtime_receipt),
        freeze_path=root / validate_portable_path(args.registration_freeze),
    )
    _write_output(args.output, result)
    return 0


def command_validate(args: argparse.Namespace) -> int:
    result = validate_registration_policy(
        load_registration_policy(), _load_cal_pre_configs()
    )
    _write_output(args.output, result)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate-policy")
    validate.add_argument("--output")
    validate.set_defaults(handler=command_validate)
    baseline_one = subparsers.add_parser("baseline-one")
    baseline_one.add_argument("--realization-profile", required=True)
    baseline_one.add_argument("--cell", required=True)
    baseline_one.add_argument("--seed", required=True, type=int)
    baseline_one.add_argument("--graph-root")
    baseline_one.set_defaults(handler=command_baseline_one)
    baselines = subparsers.add_parser("build-baseline-registry")
    baselines.add_argument("--realization-profile", required=True)
    baselines.add_argument("--graph-root")
    baselines.add_argument("--output", required=True)
    baselines.add_argument("--allow-dirty-preview", action="store_true")
    baselines.set_defaults(handler=command_build_baselines)
    inherited = subparsers.add_parser("build-inherited-verification")
    inherited.add_argument("--graph-root", required=True)
    inherited.add_argument("--output", required=True)
    inherited.add_argument("--allow-dirty-preview", action="store_true")
    inherited.set_defaults(handler=command_build_inherited_verification)
    receipt = subparsers.add_parser("build-runtime-receipt")
    receipt.add_argument("--graph-root", required=True)
    receipt.add_argument("--output", required=True)
    receipt.add_argument("--allow-dirty-preview", action="store_true")
    receipt.set_defaults(handler=command_build_runtime_receipt)
    freeze = subparsers.add_parser("build-registration-freeze")
    freeze.add_argument("--baseline-registry", required=True)
    freeze.add_argument("--inherited-verification", required=True)
    freeze.add_argument("--runtime-receipt", required=True)
    freeze.add_argument("--output", required=True)
    freeze.add_argument("--allow-dirty-preview", action="store_true")
    freeze.set_defaults(handler=command_build_registration_freeze)
    manifest = subparsers.add_parser("build-registration-manifest")
    manifest.add_argument("--baseline-registry", required=True)
    manifest.add_argument("--inherited-verification", required=True)
    manifest.add_argument("--runtime-receipt", required=True)
    manifest.add_argument("--registration-freeze", required=True)
    manifest.add_argument("--output", required=True)
    manifest.set_defaults(handler=command_build_registration_manifest)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        sys.stderr.write(f"P2-I1 registration error: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
