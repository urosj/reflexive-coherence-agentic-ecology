#!/usr/bin/env python3
"""Cycle-scoped execution boundary for P2-I1 C02.

The module has three deliberately separate responsibilities:

1. validate the exact executable policy and build a candidate-free EXEC-FREEZE;
2. require that retained, tracked freeze before any native candidate operation;
3. emit per-run and cross-run audit records without selecting a scientific rung.

Importing this module never imports PyGRC or executes a candidate operation.
"""

from __future__ import annotations

import argparse
from contextlib import nullcontext
from dataclasses import asdict, is_dataclass
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Mapping, Sequence

from ae01_tooling import (
    ContractError,
    ReadOnlyTreeGuard,
    digest_canonical_data,
    digest_file,
    load_json,
    pretty_json_dumps,
    semantic_file_digest,
    validate_portable_path,
)
from p2_i1 import CONFIG_PATHS, experiment_root, find_repository_root, validate_configs
from p2_i1_analysis import (
    static_profile_identities,
    validate_cross_cell_static_profile_matching,
    validate_opportunity,
)
from p2_i1_registration import (
    load_registration_policy,
    validate_registration_policy,
)
from p2_i1_runtime import (
    bind_runtime,
    build_fixture,
    resolve_node_coherences,
    resolve_reader_packet_amount,
)


EXECUTION_POLICY_PATH = "configs/p2_i1_c02_execution_policy.json"
EXECUTION_SCRIPT_PATH = "scripts/p2_i1_execution.py"
EXPECTED_CELLS = [
    "reference",
    "candidate-conditioning",
    "medium-freeze-withdrawal",
    "trace-shuffle",
    "parent-context-contrast",
    "susceptibility-inversion",
    "carrier-timescale-contrast",
]
EXPECTED_SEEDS = [101, 211, 307]
EXPECTED_OBLIGATIONS = [f"C02-OBL-{index:02d}" for index in range(1, 13)]
EXECUTION_SOURCE_PATHS = [
    "configs/p2_i1_c02_execution_policy.json",
    "configs/p2_i1_fixture.json",
    "configs/p2_i1_cells.json",
    "configs/p2_i1_analysis_policy.json",
    "configs/p2_i1_runtime_policy.json",
    "configs/p2_i1_registration_policy.json",
    "scripts/p2_i1_execution.py",
    "scripts/p2_i1_runtime.py",
    "scripts/p2_i1_analysis.py",
]
SCIENTIFIC_RESULT_PATH_KEYS = (
    "cycle_audit_path",
    "retry_ledger_path",
    "execution_manifest_path",
)
EXECUTION_BINDING_RECEIPT_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i1/c02/execution-binding-receipt.json"
)


def load_execution_policy() -> dict[str, Any]:
    return load_json(experiment_root() / EXECUTION_POLICY_PATH)


def _load_configs() -> dict[str, Any]:
    root = experiment_root()
    return {name: load_json(root / path) for name, path in CONFIG_PATHS.items()}


def _write_output(path_value: str | None, value: Any) -> None:
    rendered = pretty_json_dumps(value)
    if path_value is None:
        sys.stdout.write(rendered)
        return
    path = find_repository_root() / validate_portable_path(path_value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")


def _git_revision(*, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=cwd or find_repository_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ContractError("git revision is not a full SHA-1 identity")
    return value


def _git_status() -> list[str]:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=find_repository_root(),
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def _source_state(
    *,
    allow_dirty_preview: bool,
    allowed_generated_paths: set[str] | None = None,
) -> dict[str, Any]:
    allowed = allowed_generated_paths or set()
    status = []
    for line in _git_status():
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        if path not in allowed:
            status.append(line)
    clean = not status
    if not clean and not allow_dirty_preview:
        raise ContractError(
            "retained C02 freeze generation requires a clean source worktree"
        )
    return {
        "source_revision": _git_revision(),
        "source_worktree_clean": clean,
        "retention_eligible": clean,
        "preview_only": not clean,
        "source_status_entry_count": len(status),
    }


def _require_exact_keys(
    value: Mapping[str, Any], expected: set[str], *, context: str
) -> None:
    actual = set(value)
    if actual != expected:
        raise ContractError(
            f"{context} fields drifted; missing={sorted(expected - actual)}, "
            f"unknown={sorted(actual - expected)}"
        )


def validate_execution_policy(
    policy: Mapping[str, Any],
    *,
    configs: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate the exact C02 executable policy without importing PyGRC."""

    expected_top = {
        "artifact_kind",
        "schema_version",
        "lane_id",
        "cycle_id",
        "predecessor_cycle_id",
        "evidence_effect",
        "authorization",
        "authorities",
        "execution_identity",
        "restoration_identity",
        "matrix",
        "window_operations",
        "cell_realizations",
        "live_obligations",
        "artifact_contract",
        "claim_boundary",
    }
    _require_exact_keys(policy, expected_top, context="C02 execution policy")
    if not (
        policy.get("artifact_kind") == "p2_i1_c02_execution_policy"
        and policy.get("schema_version") == "1.0.0"
        and policy.get("lane_id") == "AE01-L01"
        and policy.get("cycle_id") == "P2-I1-C02"
        and policy.get("predecessor_cycle_id") == "P2-I1-C01"
        and policy.get("evidence_effect") == "none_pre_execution_policy_only"
    ):
        raise ContractError("C02 policy identity drifted")

    authorization = policy["authorization"]
    if not (
        authorization.get("candidate_execution_authorized") is False
        and authorization.get("authorization_record_kind")
        == "p2_i1_c02_exec_freeze"
        and authorization.get("authorization_gate") == "P2-I1-EXEC-FREEZE"
        and authorization.get("authorization_scope")
        == "exact_cycle_cell_seed_attempt_only"
        and authorization.get("candidate_outcomes_absent_required_at_freeze")
        is True
        and authorization.get("tracked_freeze_required_before_run") is True
        and authorization.get("fallback_execution_class") is None
    ):
        raise ContractError("C02 authorization boundary drifted")

    authorities = policy["authorities"]
    expected_authority_keys = {
        "registration_freeze_path",
        "registration_manifest_path",
        "registration_review_path",
        "registration_review_marker",
        "decision_record_path",
        "decision_026_acceptance_marker",
        "decision_027_acceptance_marker",
        "predecessor_retry_ledger_path",
        "predecessor_cycle_audit_path",
        "predecessor_result_report_path",
        "calibration_freeze_path",
        "cal_pre_identity_path",
        "fixture_path",
        "cells_path",
        "analysis_policy_path",
        "registration_policy_path",
        "realization_profile_path",
        "baseline_registry_path",
    }
    _require_exact_keys(
        authorities, expected_authority_keys, context="C02 authorities"
    )
    for key, value in authorities.items():
        if key.endswith("_path"):
            validate_portable_path(value)

    identity = policy["execution_identity"]
    if not (
        identity.get("execution_class") == "pygrc_runtime_with_rcae_producer"
        and identity.get("required_pygrc_identity") == "pygrc==0.1"
        and identity.get("binding_relation_to_registration")
        == "strict_execution_specific_superset"
        and identity.get("machine_local_runtime_path_recorded") is False
        and identity.get("graph_repository_access")
        == "read_only_fingerprint_guard"
    ):
        raise ContractError("C02 execution identity drifted")
    capability_paths = identity.get("execution_specific_capability_paths")
    expected_paths = {
        "writer_packet_scheduling": [
            "models.LGRC9V3.schedule_packet_departure"
        ],
        "feedback_conditioned_packet_production": [
            "models.LGRC9V3.produce_events"
        ],
        "branch_snapshot_persistence": [
            "models.LGRC9V3.save",
            "models.LGRC9V3.load",
        ],
        "runtime_state_audit": [
            "models.LGRC9V3.get_state",
            "models.LGRC9V3.snapshot",
        ],
    }
    if capability_paths != expected_paths:
        raise ContractError("C02 execution-specific capability map drifted")

    restoration = policy["restoration_identity"]
    if restoration != {
        "policy": "declared_native_restoration_projection",
        "included_snapshot_groups": [
            "metadata",
            "topology",
            "basin_attributes",
            "edge_labels",
            "dynamics.lgrc9v3_runtime",
            "observables",
            "events",
        ],
        "excluded_snapshot_path": "caches.base_grc9v3_snapshot",
        "raw_snapshot_digests_retained": True,
        "projection_digests_must_match": True,
        "medium_reconstruction_verified_separately": True,
        "equal_input_continuation_required": True,
        "normalization_is_observation_not_failure": True,
        "pygrc_state_mutation_permitted": False,
        "pygrc_modification_permitted": False,
    }:
        raise ContractError("C02 restoration identity drifted")

    matrix = policy["matrix"]
    if not (
        matrix.get("cell_order") == EXPECTED_CELLS
        and matrix.get("seeds") == EXPECTED_SEEDS
        and matrix.get("attempts_per_seed") == 1
        and matrix.get("infrastructure_retries_per_cell") == 1
        and matrix.get("retry_seed_selection")
        == "lowest_seed_with_first_infrastructure_failure"
        and matrix.get("fresh_worker_per_attempt") is True
        and matrix.get("worker_reuse_allowed") is False
        and matrix.get("scientific_refinement_by_retry") is False
        and matrix.get("opportunities_per_cell_seed") == 4
        and matrix.get("expected_primary_run_count") == 21
    ):
        raise ContractError("C02 matrix drifted")
    if list(policy["cell_realizations"]) != EXPECTED_CELLS:
        raise ContractError("C02 cell realization order or set drifted")
    if policy["cell_realizations"]["medium-freeze-withdrawal"] != {
        "feedback_row": "not_emitted",
        "reference_delta_source": "not_applicable",
        "expected_source_digest": "writer_arrival_contact",
        "profile_polarity_mode": "registered",
        "reader_packet_amount_source": "fixture",
        "producer_invocation_preserved": True,
        "participant_opportunity_preserved": True,
        "scaffold_withdrawal": False,
    }:
        raise ContractError("C02 medium-freeze realization drifted")
    if policy["cell_realizations"]["trace-shuffle"].get("broken_relation") != (
        "expected_source_digest_only"
    ):
        raise ContractError("C02 trace-shuffle must remain single-axis")

    obligations = policy.get("live_obligations", [])
    if [row.get("obligation_id") for row in obligations] != EXPECTED_OBLIGATIONS:
        raise ContractError("C02 live-obligation order or set drifted")
    if len({row.get("meaning") for row in obligations}) != len(obligations):
        raise ContractError("C02 live-obligation meanings must be unique")
    for row in obligations:
        if row.get("resolution_scope") not in {
            "per_run",
            "per_opportunity",
            "cross_cell_seed",
            "cycle",
        }:
            raise ContractError("C02 live-obligation resolution scope drifted")
        required_fields = row.get("required_fields")
        if not isinstance(required_fields, list) or not required_fields:
            raise ContractError("C02 live obligation requires machine fields")

    contract = policy["artifact_contract"]
    for key, value in contract.items():
        if key.endswith("_path") or key.endswith("_path_template"):
            validate_portable_path(value)
    if not (
        contract.get("per_run_opportunity_count") == 4
        and contract.get("retain_failed_attempts") is True
        and contract.get("derived_reports_cannot_support_positive_rung") is True
        and contract.get("candidate_result_paths_must_be_absent_at_freeze") is True
    ):
        raise ContractError("C02 artifact contract drifted")

    claims = policy["claim_boundary"]
    if not (
        claims.get("registration_facts_are_not_lane_evidence") is True
        and claims.get("thresholds_are_interpretive_ladders_not_terminal_boolean_gates")
        is True
        and claims.get("positive_or_negative_classification_requires_completed_verified_execution")
        is True
        and claims.get("maximum_claim")
        == "bounded niche-conditioning demand pattern"
        and all(
            claims.get(key) is False
            for key in (
                "native_niche_claim",
                "agency_claim",
                "coordination_claim",
                "motif_or_regime_claim",
            )
        )
    ):
        raise ContractError("C02 claim boundary drifted")

    resolved_configs = dict(configs or _load_configs())
    validate_configs(resolved_configs)
    registration_policy = load_registration_policy()
    validate_registration_policy(registration_policy, resolved_configs)
    if not (
        registration_policy["execution_policy"]["cell_order"] == EXPECTED_CELLS
        and registration_policy["execution_policy"]["seeds"] == EXPECTED_SEEDS
        and resolved_configs["cells"]["cycle_id"] == "P2-I1-C00"
    ):
        raise ContractError("C02 does not import the registered design unchanged")
    return {
        "artifact_kind": "p2_i1_c02_execution_policy_validation",
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "status": "passed",
        "cell_count": 7,
        "seed_count": 3,
        "run_count": 21,
        "live_obligation_count": 12,
        "candidate_execution_authorized": False,
        "canonical_payload_digest": digest_canonical_data(policy),
    }


def _authority_records(policy: Mapping[str, Any]) -> list[dict[str, Any]]:
    root = experiment_root()
    records: list[dict[str, Any]] = []
    for authority_id, relative in policy["authorities"].items():
        if not authority_id.endswith("_path"):
            continue
        portable = validate_portable_path(relative)
        path = root / portable
        if not path.is_file():
            raise ContractError(f"missing C02 authority: {relative}")
        records.append(
            {
                "authority_id": authority_id.removesuffix("_path"),
                "path": path.relative_to(find_repository_root()).as_posix(),
                "semantic_digest": semantic_file_digest(path),
                "file_sha256": digest_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return records


def _validate_registration_authority(policy: Mapping[str, Any]) -> None:
    root = experiment_root()
    authorities = policy["authorities"]
    freeze = load_json(root / authorities["registration_freeze_path"])
    manifest = load_json(root / authorities["registration_manifest_path"])
    review = (root / authorities["registration_review_path"]).read_text(
        encoding="utf-8"
    )
    if not (
        freeze.get("artifact_kind") == "p2_i1_registration_freeze"
        and freeze.get("retention_eligible") is True
        and freeze.get("preview_only") is False
        and freeze.get("candidate_execution_authorized") is False
        and freeze.get("candidate_outcomes_absent") is True
        and freeze.get("measurement_identity_match") is True
        and freeze.get("realization_identity_match") is True
    ):
        raise ContractError("C02 requires the retained passing registration freeze")
    record = manifest.get("record", {})
    if not (
        manifest.get("record_type") == "artifact_manifest"
        and record.get("manifest_id") == "rcae-p2-i1-registration-manifest-v1"
        and record.get("fully_resolved") is True
    ):
        raise ContractError("C02 requires the fully resolved registration manifest")
    if policy["authorities"]["registration_review_marker"] not in review:
        raise ContractError("C02 requires the passed REG-GATE review marker")


def _validate_predecessor_authority(policy: Mapping[str, Any]) -> None:
    authorities = policy["authorities"]
    root = experiment_root()
    ledger = load_json(root / authorities["predecessor_retry_ledger_path"])
    audit = load_json(root / authorities["predecessor_cycle_audit_path"])
    report = (root / authorities["predecessor_result_report_path"]).read_text(
        encoding="utf-8"
    )
    if not (
        ledger.get("artifact_kind") == "p2_i1_c01_retry_ledger"
        and ledger.get("cycle_id") == "P2-I1-C01"
        and len(ledger.get("primary_failures", [])) == 21
        and len(ledger.get("retry_authorizations", [])) == 7
        and len(ledger.get("retry_results", [])) == 7
        and all(
            row.get("seed") == 101 and row.get("status") == "authorized"
            for row in ledger.get("retry_authorizations", [])
        )
        and all(
            row.get("status") == "failed"
            for row in ledger.get("retry_results", [])
        )
        and len(
            {
                row.get("diagnostic_digest")
                for row in ledger.get("primary_failures", [])
                + ledger.get("retry_results", [])
            }
        )
        == 1
        and all(
            row.get("candidate_scientific_effect") == "none_operational_only"
            for row in ledger.get("primary_failures", [])
            + ledger.get("retry_results", [])
        )
    ):
        raise ContractError("C02 predecessor retry evidence drifted")
    if not (
        audit.get("artifact_kind") == "p2_i1_c01_cycle_audit"
        and audit.get("cycle_id") == "P2-I1-C01"
        and audit.get("audit_complete") is False
        and audit.get("effective_run_count") == 0
        and len(audit.get("missing_run_ids", [])) == 21
        and audit.get("candidate_outcomes_present") is False
        and audit.get("scientific_rung_assigned") is False
        and audit.get("terminal_classification_opened") is False
        and len(audit.get("obligation_results", [])) == 12
        and all(
            row.get("status") == "blocked_or_incomplete"
            for row in audit.get("obligation_results", [])
        )
    ):
        raise ContractError("C02 predecessor audit evidence drifted")
    if not (
        "P2-I1-C01 = bounded_incomplete_operational" in report
        and "successor = P2-I1-C02" in report
    ):
        raise ContractError("C02 predecessor report disposition drifted")


def _validate_decision_authority(
    policy: Mapping[str, Any], *, required: bool
) -> None:
    authorities = policy["authorities"]
    decision = (
        experiment_root() / authorities["decision_record_path"]
    ).read_text(encoding="utf-8")
    markers = [
        authorities["decision_026_acceptance_marker"],
        authorities["decision_027_acceptance_marker"],
    ]
    if required and any(marker not in decision for marker in markers):
        raise ContractError("C02 requires accepted P2-I1-DEC-026 and DEC-027")


def _expected_run_specs(policy: Mapping[str, Any]) -> list[dict[str, Any]]:
    template = policy["artifact_contract"]["run_artifact_path_template"]
    specs = []
    for cell_id in policy["matrix"]["cell_order"]:
        for seed in policy["matrix"]["seeds"]:
            scientific_identity = {
                "cycle_id": policy["cycle_id"],
                "cell_id": cell_id,
                "seed": seed,
                "cell_realization": policy["cell_realizations"][cell_id],
            }
            specs.append(
                {
                    **scientific_identity,
                    "attempt": 1,
                    "run_id": f"P2-I1-C02:{cell_id}:seed-{seed}:attempt-1",
                    "worker_scope_id": (
                        f"P2-I1-C02-worker:{cell_id}:seed-{seed}:attempt-1"
                    ),
                    "expected_path": validate_portable_path(
                        template.format(cell_id=cell_id, seed=seed)
                    ),
                    "execution_configuration_digest": digest_canonical_data(
                        scientific_identity
                    ),
                }
            )
    return specs


def _candidate_result_paths(policy: Mapping[str, Any]) -> list[Path]:
    root = find_repository_root()
    contract = policy["artifact_contract"]
    paths = [root / spec["expected_path"] for spec in _expected_run_specs(policy)]
    retry_template = contract["retry_run_artifact_path_template"]
    paths.extend(
        root / retry_template.format(cell_id=cell_id, seed=seed)
        for cell_id in policy["matrix"]["cell_order"]
        for seed in policy["matrix"]["seeds"]
    )
    paths.extend(root / contract[key] for key in SCIENTIFIC_RESULT_PATH_KEYS)
    return paths


def _require_candidate_outcomes_absent(policy: Mapping[str, Any]) -> None:
    present = [
        path.relative_to(find_repository_root()).as_posix()
        for path in _candidate_result_paths(policy)
        if path.exists()
    ]
    if present:
        raise ContractError(
            "C02 candidate outcomes must be absent at freeze: " + ", ".join(present)
        )


def build_execution_binding_receipt(
    *, graph_root: Path, allow_dirty_preview: bool = False
) -> dict[str, Any]:
    """Bind exact C02 callables without scheduling a candidate operation."""

    policy = load_execution_policy()
    validation = validate_execution_policy(policy)
    source_state = _source_state(allow_dirty_preview=allow_dirty_preview)
    configs = _load_configs()
    profile = load_json(
        experiment_root() / policy["authorities"]["realization_profile_path"]
    )
    inherited = load_json(
        experiment_root() / "contracts/p2-i1/inherited-control-verification.json"
    )
    with ReadOnlyTreeGuard(graph_root):
        graph_revision = _git_revision(cwd=graph_root)
        if graph_revision != inherited["graph_source_revision"]:
            raise ContractError("C02 binding graph revision differs from registration")
        modules = bind_runtime(configs["runtime"], profile)
        capabilities = validate_execution_specific_capabilities(modules, policy)
    retained = source_state["retention_eligible"]
    result = {
        "artifact_kind": (
            "p2_i1_c02_execution_binding_receipt"
            if retained
            else "p2_i1_c02_execution_binding_receipt_preview"
        ),
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "evidence_effect": "none_pre_execution_binding_only",
        **source_state,
        "execution_policy_digest": validation["canonical_payload_digest"],
        "runtime_identity": "pygrc==0.1",
        "execution_class": "pygrc_runtime_with_rcae_producer",
        "binding_relation_to_registration": "strict_execution_specific_superset",
        "registered_operation_classes": policy["execution_identity"][
            "registered_operation_classes"
        ],
        "execution_specific_capabilities": capabilities,
        "graph_source_revision": graph_revision,
        "graph_repository_write_observed": False,
        "machine_local_runtime_path_recorded": False,
        "machine_local_graph_path_recorded": False,
        "candidate_operation_executed": False,
        "candidate_outcome_observed": False,
        "fallback_used": False,
        "conformance_status": "passed",
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def validate_execution_binding_receipt(
    receipt: Mapping[str, Any],
    *,
    policy: Mapping[str, Any],
    allow_preview: bool = False,
) -> None:
    _verify_canonical_payload(receipt)
    preview = receipt.get("preview_only") is True
    expected_kind = (
        "p2_i1_c02_execution_binding_receipt_preview"
        if preview
        else "p2_i1_c02_execution_binding_receipt"
    )
    if preview and not allow_preview:
        raise ContractError("C02 preview binding receipt cannot enter retained freeze")
    if not (
        receipt.get("artifact_kind") == expected_kind
        and receipt.get("cycle_id") == "P2-I1-C02"
        and receipt.get("source_worktree_clean")
        is receipt.get("retention_eligible")
        and receipt.get("preview_only") is (not receipt.get("retention_eligible"))
        and receipt.get("execution_policy_digest") == digest_canonical_data(policy)
        and receipt.get("runtime_identity") == "pygrc==0.1"
        and receipt.get("execution_class")
        == "pygrc_runtime_with_rcae_producer"
        and receipt.get("binding_relation_to_registration")
        == "strict_execution_specific_superset"
        and receipt.get("execution_specific_capabilities")
        == policy["execution_identity"]["execution_specific_capability_paths"]
        and receipt.get("graph_repository_write_observed") is False
        and receipt.get("machine_local_runtime_path_recorded") is False
        and receipt.get("machine_local_graph_path_recorded") is False
        and receipt.get("candidate_operation_executed") is False
        and receipt.get("candidate_outcome_observed") is False
        and receipt.get("fallback_used") is False
        and receipt.get("conformance_status") == "passed"
    ):
        raise ContractError("C02 execution binding receipt drifted")


def build_exec_freeze(
    *,
    execution_binding_path: Path,
    allow_dirty_preview: bool = False,
) -> dict[str, Any]:
    """Build the exact candidate-free C02 authorization record."""

    policy = load_execution_policy()
    validation = validate_execution_policy(policy)
    _validate_registration_authority(policy)
    _validate_predecessor_authority(policy)
    _require_candidate_outcomes_absent(policy)
    expected_binding = policy["artifact_contract"]["execution_binding_receipt_path"]
    binding_path_value = execution_binding_path.relative_to(
        find_repository_root()
    ).as_posix()
    receipt = load_json(execution_binding_path)
    validate_execution_binding_receipt(
        receipt, policy=policy, allow_preview=allow_dirty_preview
    )
    if receipt.get("retention_eligible") is True and binding_path_value != expected_binding:
        raise ContractError("retained C02 execution binding receipt path drifted")
    source_state = _source_state(
        allow_dirty_preview=allow_dirty_preview,
        allowed_generated_paths={binding_path_value},
    )
    if not (
        receipt.get("source_revision") == source_state["source_revision"]
        and receipt.get("retention_eligible")
        is source_state["retention_eligible"]
        and receipt.get("preview_only") is source_state["preview_only"]
    ):
        raise ContractError("C02 binding receipt and freeze source states differ")
    _validate_decision_authority(
        policy, required=bool(source_state["retention_eligible"])
    )
    source_files = []
    for relative in EXECUTION_SOURCE_PATHS:
        path = experiment_root() / relative
        if not path.is_file():
            raise ContractError(f"missing C02 execution source: {relative}")
        source_files.append(
            {
                "path": path.relative_to(find_repository_root()).as_posix(),
                "semantic_digest": semantic_file_digest(path),
                "file_sha256": digest_file(path),
            }
        )
    retained = source_state["retention_eligible"]
    result = {
        "artifact_kind": (
            "p2_i1_c02_exec_freeze"
            if retained
            else "p2_i1_c02_exec_freeze_preview"
        ),
        "schema_version": "1.0.0",
        "lane_id": policy["lane_id"],
        "cycle_id": policy["cycle_id"],
        "predecessor_cycle_id": policy["predecessor_cycle_id"],
        "evidence_effect": "none_pre_execution_authorization_only",
        **source_state,
        "execution_policy_digest": validation["canonical_payload_digest"],
        "authority_records": _authority_records(policy),
        "execution_binding_receipt": {
            "path": binding_path_value,
            "semantic_digest": semantic_file_digest(execution_binding_path),
            "file_sha256": digest_file(execution_binding_path),
            "canonical_payload_digest": receipt["canonical_payload_digest"],
        },
        "execution_source_files": source_files,
        "run_specs": _expected_run_specs(policy),
        "live_obligations": policy["live_obligations"],
        "artifact_contract": policy["artifact_contract"],
        "candidate_outcomes_absent_at_freeze": True,
        "candidate_execution_performed_at_freeze": False,
        "candidate_execution_authorized": retained,
        "authorization_gate": "P2-I1-EXEC-FREEZE",
        "authorization_scope": "exact_cycle_cell_seed_attempt_only",
        "runtime_binding_required_per_run": True,
        "graph_read_only_guard_required_per_run": True,
        "fallback_permitted": False,
        "positive_or_negative_lane_evidence_opened": False,
        "thresholds_are_terminal_boolean_gates": False,
        "claim_ceiling": policy["claim_boundary"]["maximum_claim"],
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def _verify_canonical_payload(record: Mapping[str, Any]) -> None:
    payload = dict(record)
    observed = payload.pop("canonical_payload_digest", None)
    if observed != digest_canonical_data(payload):
        raise ContractError("C02 EXEC-FREEZE canonical payload digest mismatch")


def _tracked_head_bytes(path: Path) -> bytes:
    relative = path.relative_to(find_repository_root()).as_posix()
    result = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=find_repository_root(),
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ContractError("C02 EXEC-FREEZE must be tracked in the current HEAD")
    return result.stdout


def validate_exec_freeze(
    freeze: Mapping[str, Any],
    *,
    freeze_path: Path | None = None,
    require_tracked: bool = False,
) -> None:
    """Validate authorization without checking post-freeze result absence."""

    _verify_canonical_payload(freeze)
    policy = load_execution_policy()
    validation = validate_execution_policy(policy)
    _validate_registration_authority(policy)
    _validate_predecessor_authority(policy)
    _validate_decision_authority(policy, required=True)
    if not (
        freeze.get("artifact_kind") == "p2_i1_c02_exec_freeze"
        and freeze.get("retention_eligible") is True
        and freeze.get("preview_only") is False
        and freeze.get("source_worktree_clean") is True
        and freeze.get("candidate_outcomes_absent_at_freeze") is True
        and freeze.get("candidate_execution_performed_at_freeze") is False
        and freeze.get("candidate_execution_authorized") is True
        and freeze.get("fallback_permitted") is False
        and freeze.get("positive_or_negative_lane_evidence_opened") is False
        and freeze.get("execution_policy_digest")
        == validation["canonical_payload_digest"]
        and freeze.get("run_specs") == _expected_run_specs(policy)
        and freeze.get("live_obligations") == policy["live_obligations"]
        and freeze.get("artifact_contract") == policy["artifact_contract"]
    ):
        raise ContractError("C02 EXEC-FREEZE authorization boundary drifted")
    current_authorities = _authority_records(policy)
    if freeze.get("authority_records") != current_authorities:
        raise ContractError("C02 EXEC-FREEZE authority digest drifted")
    binding_ref = freeze.get("execution_binding_receipt", {})
    expected_binding_path = policy["artifact_contract"][
        "execution_binding_receipt_path"
    ]
    if binding_ref.get("path") != expected_binding_path:
        raise ContractError("C02 EXEC-FREEZE binding receipt path drifted")
    binding_path = find_repository_root() / expected_binding_path
    binding = load_json(binding_path)
    validate_execution_binding_receipt(binding, policy=policy)
    if binding_ref != {
        "path": expected_binding_path,
        "semantic_digest": semantic_file_digest(binding_path),
        "file_sha256": digest_file(binding_path),
        "canonical_payload_digest": binding["canonical_payload_digest"],
    }:
        raise ContractError("C02 EXEC-FREEZE binding receipt digest drifted")
    if require_tracked and _tracked_head_bytes(binding_path) != binding_path.read_bytes():
        raise ContractError(
            "C02 execution binding receipt must match its tracked HEAD record"
        )
    expected_sources = []
    for row in freeze.get("execution_source_files", []):
        path = find_repository_root() / validate_portable_path(row["path"])
        if not path.is_file():
            raise ContractError("C02 frozen execution source is missing")
        expected_sources.append(
            {
                "path": row["path"],
                "semantic_digest": semantic_file_digest(path),
                "file_sha256": digest_file(path),
            }
        )
    if expected_sources != freeze.get("execution_source_files"):
        raise ContractError("C02 execution source differs from EXEC-FREEZE")
    if require_tracked:
        if freeze_path is None:
            raise ContractError("tracked EXEC-FREEZE validation requires its path")
        current = freeze_path.read_bytes()
        if _tracked_head_bytes(freeze_path) != current:
            raise ContractError("C02 EXEC-FREEZE differs from the tracked HEAD record")


def validate_execution_specific_capabilities(
    runtime_modules: Mapping[str, Any], policy: Mapping[str, Any]
) -> dict[str, list[str]]:
    """Resolve the exact calls needed by C02 in addition to REG conformance."""

    resolved: dict[str, list[str]] = {}
    for operation_id, paths in policy["execution_identity"][
        "execution_specific_capability_paths"
    ].items():
        for path in paths:
            parts = path.split(".")
            value: Any = runtime_modules.get(parts[0])
            for part in parts[1:]:
                value = getattr(value, part, None)
            if not callable(value):
                raise ContractError(
                    f"C02 execution-specific capability unavailable: {path}"
                )
        resolved[operation_id] = list(paths)
    return resolved


def _event_artifact(event: Any) -> dict[str, Any]:
    if is_dataclass(event):
        return asdict(event)
    if isinstance(event, Mapping):
        return dict(event)
    return {
        "kind": str(getattr(event, "kind", type(event).__name__)),
        "step_index": int(getattr(event, "step_index", -1)),
        "payload": dict(getattr(event, "payload", {})),
        "source_family": getattr(event, "source_family", None),
    }


def _drain_queue(model: Any, *, maximum_events: int = 8) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for _ in range(maximum_events):
        queue = model.get_state().packet_ledger.event_queue_records
        if not queue:
            return results
        step_result = model.step()
        results.append(
            {
                "step_index": int(step_result.step_index),
                "time": float(step_result.time),
                "events": [_event_artifact(event) for event in step_result.events],
                "bookkeeping": dict(step_result.bookkeeping),
            }
        )
    if model.get_state().packet_ledger.event_queue_records:
        raise ContractError("C02 queue did not drain within the registered event bound")
    return results


def _surface_artifacts(model: Any) -> list[dict[str, Any]]:
    return [
        row.to_artifact() if hasattr(row, "to_artifact") else dict(row)
        for row in model.get_state().causal_pulse_substrate_surface_log
    ]


def _contact_rows(model: Any) -> list[dict[str, Any]]:
    return [
        row
        for row in _surface_artifacts(model)
        if row.get("surface_kind") == "route_local_pulse_contact"
    ]


def _base_snapshot_projection(snapshot: Mapping[str, Any]) -> Mapping[str, Any]:
    caches = snapshot.get("caches", {})
    if not isinstance(caches, Mapping):
        raise ContractError("C02 runtime snapshot caches are unavailable")
    base = caches.get("base_grc9v3_snapshot")
    if not isinstance(base, Mapping):
        raise ContractError("C02 runtime snapshot lacks native base snapshot")
    return base


def restoration_projection(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Project the native state D-027 assigns to branch identity."""

    metadata = snapshot.get("metadata")
    topology = snapshot.get("topology")
    dynamics = snapshot.get("dynamics")
    observables = snapshot.get("observables")
    events = snapshot.get("events")
    if not all(
        isinstance(value, Mapping)
        for value in (metadata, topology, dynamics, observables)
    ) or not isinstance(events, list):
        raise ContractError("C02 restoration projection source shape drifted")
    runtime = dynamics.get("lgrc9v3_runtime")
    if not isinstance(runtime, Mapping):
        raise ContractError("C02 restoration projection lacks LGRC runtime state")
    return {
        "metadata": dict(metadata),
        "topology": dict(topology),
        "basin_attributes": snapshot.get("basin_attributes"),
        "edge_labels": snapshot.get("edge_labels"),
        "dynamics": {"lgrc9v3_runtime": dict(runtime)},
        "observables": dict(observables),
        "events": list(events),
    }


def _observed_baseline_entry(
    *,
    model: Any,
    route_aspect: Any,
    configs: Mapping[str, Mapping[str, Any]],
    seed: int,
    cell_id: str,
) -> dict[str, Any]:
    snapshot = model.snapshot()
    queue = model.get_state().packet_ledger.event_queue_records
    surfaces = model.get_state().causal_pulse_substrate_surface_log
    if queue or surfaces:
        raise ContractError("C02 W0 must begin with empty queue and surface")
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


def _registered_baseline(
    registry: Mapping[str, Any], *, cell_id: str, seed: int
) -> Mapping[str, Any]:
    matches = [
        row
        for row in registry.get("entries", [])
        if row.get("cell_id") == cell_id and row.get("seed") == seed
    ]
    if len(matches) != 1:
        raise ContractError("C02 cannot resolve one registered baseline entry")
    return matches[0]


def _medium_projection(row: Mapping[str, Any] | None) -> dict[str, Any]:
    if row is None:
        return {
            "medium_present": False,
            "surface_kind": "feedback_eligibility_absent",
        }
    after = row.get("surface_values_after", {})
    update = row.get("surface_update_policy", {})
    return {
        "medium_present": True,
        "surface_id": row.get("surface_id"),
        "surface_digest": row.get("surface_digest"),
        "surface_kind": row.get("surface_kind"),
        "source_surface_digest": after.get("source_surface_digest"),
        "surface_nodes": row.get("surface_nodes"),
        "boundary_polarity_score": after.get("boundary_polarity_score"),
        "reference_delta": after.get("reference_delta"),
        "feedback_threshold": after.get("feedback_threshold"),
        "declared_front_node_ids": update.get("declared_front_node_ids"),
        "declared_rear_node_ids": update.get("declared_rear_node_ids"),
        "event_time_key": row.get("event_time_key"),
        "scheduler_event_index": row.get("scheduler_event_index"),
    }


def _latest_feedback_artifact(model: Any) -> dict[str, Any] | None:
    rows = [
        row
        for row in _surface_artifacts(model)
        if row.get("surface_kind") == "feedback_eligibility"
    ]
    return None if not rows else rows[-1]


def _support_budget_projection(
    *,
    configs: Mapping[str, Mapping[str, Any]],
    cell_id: str,
    seed: int,
) -> dict[str, Any]:
    fixture = configs["fixture"]
    coherences = resolve_node_coherences(fixture, seed, cell_id, configs["cells"])
    reader_amount = resolve_reader_packet_amount(fixture, configs["cells"], cell_id)
    return {
        "resolved_node_coherences": coherences,
        "total_native_coherence": sum(coherences.values()),
        "participant_reserve": coherences["P"],
        "writer_packet_amount": fixture["packets"]["writer_amount"],
        "reader_packet_amount": reader_amount,
        "edge_policy": fixture["edge_policy"],
        "topology_digest": digest_canonical_data(
            {"nodes": fixture["nodes"], "edges": fixture["edges"]}
        ),
    }


def _cell_by_id(cells: Mapping[str, Any], cell_id: str) -> Mapping[str, Any]:
    matches = [row for row in cells["cells"] if row["cell_id"] == cell_id]
    if len(matches) != 1:
        raise ContractError("C02 cannot resolve exact cell configuration")
    return matches[0]


def _profile_polarity(
    profile: Mapping[str, Any], cell: Mapping[str, Any]
) -> str:
    intervention = cell["intervention"]
    if intervention["kind"] == "swap_expected_polarity_between_stable_reader_slots":
        return str(intervention["profile_polarity_overrides"][profile["profile_id"]])
    return str(profile["expected_polarity"])


def _reference_delta(
    fixture: Mapping[str, Any], cell: Mapping[str, Any]
) -> float:
    intervention = cell["intervention"]
    if intervention["kind"] in {
        "feedback_reference_delta",
        "accepted_writer_relative_feedback_history",
    }:
        return float(intervention["reference_delta"])
    return float(fixture["feedback"]["reference_delta"])


def _runtime_source_revisions(
    freeze: Mapping[str, Any], *, graph_root: Path
) -> dict[str, str]:
    graph_revision = _git_revision(cwd=graph_root)
    registration_graph = next(
        row
        for row in freeze["authority_records"]
        if row["authority_id"] == "registration_freeze"
    )
    registration_freeze = load_json(
        find_repository_root() / registration_graph["path"]
    )
    inherited = load_json(
        experiment_root() / "contracts/p2-i1/inherited-control-verification.json"
    )
    if graph_revision != inherited["graph_source_revision"]:
        raise ContractError("C02 graph source revision differs from registration")
    return {
        "rcae_execution_source": freeze["source_revision"],
        "rcae_current_head": _git_revision(),
        "graph": graph_revision,
        "registration_freeze": registration_freeze["source_revision"],
    }


def _producer_configuration_projection(
    *,
    fixture: Mapping[str, Any],
    profile: Mapping[str, Any],
    expected_polarity: str,
    reader_amount: float,
) -> dict[str, Any]:
    return {
        "source_node_id": profile["source_node_id"],
        "target_node_id": profile["target_node_id"],
        "edge_id": profile["edge_id"],
        "threshold": fixture["feedback"]["producer_threshold"],
        "packet_amount": reader_amount,
        "expected_polarity": expected_polarity,
        "expected_next_route_id": fixture["feedback"]["expected_next_route_id"],
        "expected_next_channel_id": fixture["feedback"]["expected_next_channel_id"],
    }


def _resolved_restoration_profile_identity(
    static_profile: Mapping[str, Any],
    *,
    pulse_contact_surface_digest: str,
    medium_history_digest: str,
    branch_point_snapshot_digest: str,
    restored_snapshot_digest: str,
    branch_point_restoration_projection_digest: str,
    restored_restoration_projection_digest: str,
) -> dict[str, Any]:
    required = {
        "profile_id",
        "reader_configuration_digest",
        "opportunity_profile_digest",
        "identity",
    }
    if set(static_profile) != required:
        raise ContractError("C02 static opportunity-profile identity shape drifted")
    values = {
        "pulse_contact_surface_digest": pulse_contact_surface_digest,
        "medium_history_digest": medium_history_digest,
        "branch_point_snapshot_digest": branch_point_snapshot_digest,
        "restored_snapshot_digest": restored_snapshot_digest,
        "branch_point_restoration_projection_digest": (
            branch_point_restoration_projection_digest
        ),
        "restored_restoration_projection_digest": (
            restored_restoration_projection_digest
        ),
    }
    if any(not isinstance(value, str) or not value for value in values.values()):
        raise ContractError("C02 resolved profile requires non-empty digest strings")
    if (
        restored_restoration_projection_digest
        != branch_point_restoration_projection_digest
    ):
        raise ContractError("C02 resolved profile restoration projection drifted")
    identity = {
        "static_opportunity_profile_digest": static_profile[
            "opportunity_profile_digest"
        ],
        "reader_configuration_digest": static_profile[
            "reader_configuration_digest"
        ],
        **values,
        "raw_snapshot_equal": (
            restored_snapshot_digest == branch_point_snapshot_digest
        ),
        "cross_branch_state_carryover": False,
    }
    return {
        "profile_id": static_profile["profile_id"],
        "opportunity_profile_digest": static_profile[
            "opportunity_profile_digest"
        ],
        "reader_configuration_digest": static_profile[
            "reader_configuration_digest"
        ],
        "resolved_opportunity_profile_digest": digest_canonical_data(identity),
        "identity": identity,
    }


def _execute_reader_continuation(
    branch: Any,
    *,
    producer_projection: Mapping[str, Any],
    expected_source_digest: str,
) -> dict[str, Any]:
    branch.set_feedback_coupled_pulse_producer(
        **producer_projection,
        expected_source_surface_digest=expected_source_digest,
    )
    production = branch.produce_events(
        policy="packet_departure_from_feedback_eligibility_policy"
    )
    production_artifact = production.to_artifact()
    records = production_artifact.get("production_records", [])
    if len(records) != 1:
        raise ContractError("C02 producer must emit exactly one audit record")
    production_record = records[0]
    formed = (
        production_record["reason_code"]
        == "feedback_coupled_pulse_packet_departure_scheduled"
    )
    response_steps = _drain_queue(branch) if formed else []
    if branch.get_state().packet_ledger.event_queue_records:
        raise ContractError("C02 opportunity branch must end with empty queue")
    final_snapshot = branch.snapshot()
    continuation_projection = {
        "production_artifact": production_artifact,
        "response_steps": response_steps,
        "final_restoration_projection_digest": digest_canonical_data(
            restoration_projection(final_snapshot)
        ),
    }
    return {
        "production_artifact": production_artifact,
        "production_record": production_record,
        "formed": formed,
        "response_steps": response_steps,
        "continuation_projection": continuation_projection,
        "continuation_digest": digest_canonical_data(continuation_projection),
    }


def _run_one_authorized(
    *,
    freeze: Mapping[str, Any],
    freeze_path: Path,
    cell_id: str,
    seed: int,
    attempt: int,
    graph_root: Path,
    output_path: str,
    retry_ledger_path: Path | None = None,
) -> dict[str, Any]:
    """Execute one exact native cell/seed only after retained authorization."""

    validate_exec_freeze(freeze, freeze_path=freeze_path, require_tracked=True)
    policy = load_execution_policy()
    specs = [
        row
        for row in freeze["run_specs"]
        if row["cell_id"] == cell_id
        and row["seed"] == seed
    ]
    if len(specs) != 1:
        raise ContractError("C02 run is outside exact EXEC-FREEZE scope")
    primary_spec = specs[0]
    if attempt not in {1, 2}:
        raise ContractError("C02 attempt must be primary or one conditional retry")
    if attempt == 1:
        spec = dict(primary_spec)
        expected_output = spec["expected_path"]
    else:
        if retry_ledger_path is None or not retry_ledger_path.is_file():
            raise ContractError("C02 retry requires the cycle retry ledger")
        ledger = load_json(retry_ledger_path)
        validate_retry_ledger(ledger, freeze=freeze)
        authorized = [
            row
            for row in ledger["retry_authorizations"]
            if row["cell_id"] == cell_id
            and row["seed"] == seed
            and row["retry_attempt"] == 2
            and row["status"] == "authorized"
        ]
        if len(authorized) != 1:
            raise ContractError("C02 retry is not authorized by deterministic ledger")
        spec = {
            **primary_spec,
            "attempt": 2,
            "run_id": f"P2-I1-C02:{cell_id}:seed-{seed}:attempt-2",
            "worker_scope_id": (
                f"P2-I1-C02-worker:{cell_id}:seed-{seed}:attempt-2"
            ),
        }
        expected_output = policy["artifact_contract"][
            "retry_run_artifact_path_template"
        ].format(cell_id=cell_id, seed=seed)
    if validate_portable_path(output_path) != expected_output:
        raise ContractError("C02 output path differs from EXEC-FREEZE")
    output = find_repository_root() / output_path
    if output.exists():
        raise ContractError("C02 refuses to overwrite an existing run artifact")

    configs = _load_configs()
    validate_execution_policy(policy, configs=configs)
    profile = load_json(
        experiment_root() / policy["authorities"]["realization_profile_path"]
    )
    registry = load_json(
        experiment_root() / policy["authorities"]["baseline_registry_path"]
    )
    cell = _cell_by_id(configs["cells"], cell_id)
    graph_guard = ReadOnlyTreeGuard(graph_root)
    with graph_guard:
        modules = bind_runtime(configs["runtime"], profile)
        execution_capabilities = validate_execution_specific_capabilities(
            modules, policy
        )
        model, route_aspect = build_fixture(
            configs["fixture"], configs["cells"], modules, seed=seed, cell_id=cell_id
        )
        observed_baseline = _observed_baseline_entry(
            model=model,
            route_aspect=route_aspect,
            configs=configs,
            seed=seed,
            cell_id=cell_id,
        )
        registered_baseline = _registered_baseline(
            registry, cell_id=cell_id, seed=seed
        )
        baseline_match = observed_baseline == registered_baseline
        if not baseline_match:
            raise ContractError("C02 observed W0 baseline differs from registration")

        fixture = configs["fixture"]
        model.schedule_packet_departure(
            source_node_id=0,
            target_node_id=1,
            edge_id=0,
            amount=float(fixture["packets"]["writer_amount"]),
            departure_event_time_key=float(
                fixture["packets"]["writer_departure_event_time_key"]
            ),
            scheduler_event_index=1,
        )
        writer_steps = _drain_queue(model)
        contacts = _contact_rows(model)
        if len(contacts) != 2:
            raise ContractError("C02 writer window requires departure and arrival contacts")
        departure_contact, arrival_contact = contacts
        post_writer_snapshot = model.snapshot()
        post_writer_base_state_digest = digest_canonical_data(
            _base_snapshot_projection(post_writer_snapshot)
        )
        writer_event_digest = digest_canonical_data(writer_steps)

        emit_feedback = cell_id != "medium-freeze-withdrawal"
        feedback_row_artifact: dict[str, Any] | None = None
        if emit_feedback:
            row = model.emit_feedback_eligibility_surface_row(
                front_node_ids=fixture["feedback"]["front_node_ids"],
                rear_node_ids=fixture["feedback"]["rear_node_ids"],
                reference_delta=_reference_delta(fixture, cell),
                feedback_threshold=float(fixture["feedback"]["feedback_threshold"]),
                expected_next_route_id=fixture["feedback"]["expected_next_route_id"],
                expected_next_channel_id=fixture["feedback"]["expected_next_channel_id"],
            )
            feedback_row_artifact = row.to_artifact()
        medium_projection = _medium_projection(feedback_row_artifact)
        medium_history_digest = digest_canonical_data(medium_projection)
        branch_point_snapshot = model.snapshot()
        branch_point_snapshot_digest = digest_canonical_data(branch_point_snapshot)
        branch_point_restoration_projection_digest = digest_canonical_data(
            restoration_projection(branch_point_snapshot)
        )

        static_profiles = static_profile_identities(fixture)
        static_by_id = {row["profile_id"]: row for row in static_profiles}
        participant_opportunity_signature = digest_canonical_data(
            {
                "post_writer_base_state_digest": post_writer_base_state_digest,
                "static_profile_digests": [
                    row["opportunity_profile_digest"] for row in static_profiles
                ],
                "reader_packet_amount": resolve_reader_packet_amount(
                    fixture, configs["cells"], cell_id
                ),
            }
        )
        support_budget = _support_budget_projection(
            configs=configs, cell_id=cell_id, seed=seed
        )
        reader_amount = float(support_budget["reader_packet_amount"])
        expected_source_digest = (
            departure_contact["surface_digest"]
            if cell_id == "trace-shuffle"
            else arrival_contact["surface_digest"]
        )

        opportunities: list[dict[str, Any]] = []
        resolved_profiles: list[dict[str, Any]] = []
        production_artifacts: list[dict[str, Any]] = []
        with tempfile.TemporaryDirectory(prefix="rcae-p2-i1-c02-") as tmp_dir:
            branch_file = Path(tmp_dir) / "branch-point.json"
            model.save(str(branch_file))
            for profile_row in fixture["opportunity_profiles"]:
                branch = modules["models"].LGRC9V3.load(str(branch_file))
                restored_snapshot = branch.snapshot()
                restored_digest = digest_canonical_data(restored_snapshot)
                restored_restoration_projection_digest = digest_canonical_data(
                    restoration_projection(restored_snapshot)
                )
                if (
                    restored_restoration_projection_digest
                    != branch_point_restoration_projection_digest
                ):
                    raise ContractError(
                        "C02 branch restoration projection differs from W2"
                    )
                reconstructed_feedback = _latest_feedback_artifact(branch)
                reconstructed_projection = _medium_projection(reconstructed_feedback)
                reconstructed_digest = digest_canonical_data(reconstructed_projection)
                if reconstructed_digest != medium_history_digest:
                    raise ContractError("C02 medium projection failed independent reconstruction")

                polarity = _profile_polarity(profile_row, cell)
                producer_projection = _producer_configuration_projection(
                    fixture=fixture,
                    profile=profile_row,
                    expected_polarity=polarity,
                    reader_amount=reader_amount,
                )
                continuation = _execute_reader_continuation(
                    branch,
                    producer_projection=producer_projection,
                    expected_source_digest=expected_source_digest,
                )
                twin = modules["models"].LGRC9V3.load(str(branch_file))
                twin_snapshot = twin.snapshot()
                twin_restoration_projection_digest = digest_canonical_data(
                    restoration_projection(twin_snapshot)
                )
                if (
                    twin_restoration_projection_digest
                    != branch_point_restoration_projection_digest
                ):
                    raise ContractError(
                        "C02 continuation twin restoration projection drifted"
                    )
                twin_continuation = _execute_reader_continuation(
                    twin,
                    producer_projection=producer_projection,
                    expected_source_digest=expected_source_digest,
                )
                equal_input_continuation = (
                    continuation["continuation_digest"]
                    == twin_continuation["continuation_digest"]
                )
                if not equal_input_continuation:
                    raise ContractError(
                        "C02 independently restored branches continue differently"
                    )
                production_artifact = continuation["production_artifact"]
                production_artifacts.append(production_artifact)
                production_record = continuation["production_record"]
                reason = production_record["reason_code"]
                formed = continuation["formed"]
                response_steps = continuation["response_steps"]
                resolved = _resolved_restoration_profile_identity(
                    static_by_id[profile_row["profile_id"]],
                    pulse_contact_surface_digest=arrival_contact["surface_digest"],
                    medium_history_digest=medium_history_digest,
                    branch_point_snapshot_digest=branch_point_snapshot_digest,
                    restored_snapshot_digest=restored_digest,
                    branch_point_restoration_projection_digest=(
                        branch_point_restoration_projection_digest
                    ),
                    restored_restoration_projection_digest=(
                        restored_restoration_projection_digest
                    ),
                )
                resolved_profiles.append(resolved)
                opportunity_index = int(profile_row["opportunity_index"])
                opportunity = {
                    "opportunity_id": (
                        f"{spec['run_id']}:opportunity-{opportunity_index}"
                    ),
                    "seed": seed,
                    "cell_id": cell_id,
                    "relation_chain_id": f"{spec['run_id']}:writer-medium-reader",
                    "writer_carrier_id": fixture["lineage_id_templates"]["participant"].format(seed=seed),
                    "writer_event_id": f"{spec['run_id']}:writer-window",
                    "medium_surface_id": (
                        "medium-absent-by-freeze"
                        if feedback_row_artifact is None
                        else str(feedback_row_artifact["surface_id"])
                    ),
                    "medium_change_event_id": (
                        "medium-row-not-emitted"
                        if feedback_row_artifact is None
                        else f"{spec['run_id']}:feedback-row"
                    ),
                    "medium_history_digest": medium_history_digest,
                    "later_opportunity_event_id": (
                        str(production_record.get("scheduled_event_id"))
                        if formed
                        else f"{spec['run_id']}:no-event-{opportunity_index}"
                    ),
                    "reader_or_local_differentiation_id": str(profile_row["profile_id"]),
                    "opportunity_index": opportunity_index,
                    "profile_id": str(profile_row["profile_id"]),
                    "context": str(profile_row["context"]),
                    "selectivity_group": str(profile_row["group"]),
                    "raw_response": 1 if formed else 0,
                    "oriented_response": 1 if formed else 0,
                    "admissibility": "admissible",
                    "opportunity_status": "observed",
                    "complete_registered_chain": formed,
                    "causal_order_verified": True,
                    "medium_dependency_control_refs": [
                        "AE01-CTRL-04",
                        "AE01-CTRL-05",
                        "AE01-CTRL-08",
                        "AE01-L01-CTRL-01",
                    ],
                    "resolved_expected_polarity": polarity,
                    "producer_reason_code": reason,
                    "producer_record": production_record,
                    "response_steps": response_steps,
                    "branch_point_snapshot_digest": branch_point_snapshot_digest,
                    "restored_snapshot_digest": restored_digest,
                    "branch_point_restoration_projection_digest": (
                        branch_point_restoration_projection_digest
                    ),
                    "restored_restoration_projection_digest": (
                        restored_restoration_projection_digest
                    ),
                    "raw_snapshot_equal": (
                        restored_digest == branch_point_snapshot_digest
                    ),
                    "raw_snapshot_normalization_observed": (
                        restored_digest != branch_point_snapshot_digest
                    ),
                    "continuation_digest": continuation["continuation_digest"],
                    "twin_continuation_digest": twin_continuation[
                        "continuation_digest"
                    ],
                    "equal_input_continuation": equal_input_continuation,
                    "cross_branch_state_carryover": False,
                    "resolved_profile_identity": resolved,
                }
                validate_opportunity(opportunity)
                opportunities.append(opportunity)

        medium_reconstruction = {
            "medium_projection_digest": medium_history_digest,
            "reconstructed_medium_projection_digest": medium_history_digest,
            "participant_label_input_consumed": False,
            "lookup_basis": "surface_kind_and_native_lineage_only",
            "passed": True,
        }
        exposure_match = len(
            {
                row["identity"]["medium_history_digest"] for row in resolved_profiles
            }
        ) == 1
        baseline_viability = {
            "profile_count": len(static_profiles),
            "reader_configuration_count": len(
                {row["reader_configuration_digest"] for row in static_profiles}
            ),
            "all_node_coherences_positive": all(
                value > 0.0 for value in support_budget["resolved_node_coherences"].values()
            ),
            "participant_reserve_positive": support_budget["participant_reserve"] > 0.0,
        }
        if not exposure_match or not all(baseline_viability.values()):
            raise ContractError("C02 selectivity baseline or exposure audit failed")
        graph_revision_after = _git_revision(cwd=graph_root)
        source_revisions = _runtime_source_revisions(freeze, graph_root=graph_root)
        if graph_revision_after != source_revisions["graph"]:
            raise ContractError("C02 graph source changed during live run")

    run = {
        "artifact_kind": "p2_i1_c02_run",
        "schema_version": "1.0.0",
        "evidence_effect": "candidate_observation_pending_cycle_controls",
        "lane_id": "AE01-L01",
        "cycle_id": "P2-I1-C02",
        "run_id": spec["run_id"],
        "worker_scope_id": spec["worker_scope_id"],
        "cell_id": cell_id,
        "seed": seed,
        "attempt": attempt,
        "execution_configuration_digest": spec["execution_configuration_digest"],
        "exec_freeze_digest": freeze["canonical_payload_digest"],
        "source_revisions": source_revisions,
        "runtime_binding": {
            "observed_identity": "pygrc==0.1",
            "execution_class": "pygrc_runtime_with_rcae_producer",
            "execution_specific_capabilities": execution_capabilities,
            "fallback_used": False,
        },
        "registered_baseline_digest": registered_baseline[
            "expected_composite_baseline_digest"
        ],
        "observed_baseline_digest": observed_baseline[
            "expected_composite_baseline_digest"
        ],
        "baseline_match": baseline_match,
        "w0_queue_empty": True,
        "w0_surface_empty": True,
        "writer_event_digest": writer_event_digest,
        "writer_steps": writer_steps,
        "departure_contact_surface_digest": departure_contact["surface_digest"],
        "pulse_contact_surface_digest": arrival_contact["surface_digest"],
        "post_writer_base_state_digest": post_writer_base_state_digest,
        "medium_presence": feedback_row_artifact is not None,
        "medium_projection": medium_projection,
        "medium_history_digest": medium_history_digest,
        "medium_reconstruction": medium_reconstruction,
        "participant_opportunity_signature": participant_opportunity_signature,
        "static_profile_identities": static_profiles,
        "resolved_profile_identities": resolved_profiles,
        "baseline_viability_audit": baseline_viability,
        "exposure_match_audit": {
            "same_medium_history_across_profiles": exposure_match,
            "same_pulse_contact_across_profiles": True,
            "passed": exposure_match,
        },
        "branch_point_snapshot_digest": branch_point_snapshot_digest,
        "branch_point_restoration_projection_digest": (
            branch_point_restoration_projection_digest
        ),
        "raw_snapshot_normalization_observed": any(
            row["raw_snapshot_normalization_observed"] for row in opportunities
        ),
        "restoration_projection_match": all(
            row["restored_restoration_projection_digest"]
            == branch_point_restoration_projection_digest
            for row in opportunities
        ),
        "equal_input_continuation_audit": all(
            row["equal_input_continuation"] for row in opportunities
        ),
        "cross_branch_state_carryover": False,
        "support_budget_projection": support_budget,
        "support_budget_projection_digest": digest_canonical_data(support_budget),
        "declared_cell_exception": (
            "support_scale"
            if cell_id == "parent-context-contrast"
            else "reader_packet_amount"
            if cell_id == "carrier-timescale-contrast"
            else None
        ),
        "producer_policy": "packet_departure_from_feedback_eligibility_policy",
        "producer_invocation_count": len(production_artifacts),
        "continuation_validation_invocation_count": len(opportunities),
        "producer_configuration_except_medium_digest": digest_canonical_data(
            [
                {
                    "profile_id": row["profile_id"],
                    "expected_polarity": _profile_polarity(row, cell),
                    "reader_packet_amount": reader_amount,
                }
                for row in fixture["opportunity_profiles"]
            ]
        ),
        "expected_source_surface_digest": expected_source_digest,
        "feedback_row_content_projection_digest": digest_canonical_data(
            medium_projection
        ),
        "preserved_trace_fields_audit": {
            "single_axis_declared": cell_id != "trace-shuffle"
            or policy["cell_realizations"][cell_id]["broken_relation"]
            == "expected_source_digest_only",
            "passed": True,
        },
        "opportunity_records": opportunities,
        "runtime_receipt": {
            "run_id": spec["run_id"],
            "runtime_identity": "pygrc==0.1",
            "requested_operation_classes": policy["execution_identity"][
                "registered_operation_classes"
            ],
            "execution_specific_capabilities": execution_capabilities,
            "conformance_status": "passed",
            "fallback_used": False,
        },
        "graph_repository_write_observed": False,
        "reconstruction": {
            "command": (
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
                f"scripts/p2_i1_execution.py run-one --exec-freeze {policy['artifact_contract']['exec_freeze_path']} "
                f"--cell {cell_id} --seed {seed} --attempt {attempt} "
                "--graph-root LOCAL_GRAPH_CHECKOUT "
                f"--output {expected_output}"
                + (
                    f" --retry-ledger {policy['artifact_contract']['retry_ledger_path']}"
                    if attempt == 2
                    else ""
                )
            ),
            "expected_path": expected_output,
            "status": "not_yet_independently_reconstructed",
        },
        "terminal_classification_opened": False,
        "rung_assignment_opened": False,
    }
    return {**run, "canonical_payload_digest": digest_canonical_data(run)}


def validate_run_record(
    record: Mapping[str, Any], *, freeze: Mapping[str, Any]
) -> None:
    _verify_canonical_payload(record)
    if not (
        record.get("artifact_kind") == "p2_i1_c02_run"
        and record.get("schema_version") == "1.0.0"
        and record.get("lane_id") == "AE01-L01"
        and record.get("cycle_id") == "P2-I1-C02"
        and record.get("exec_freeze_digest") == freeze["canonical_payload_digest"]
        and record.get("cell_id") in EXPECTED_CELLS
        and record.get("seed") in EXPECTED_SEEDS
        and record.get("attempt") in {1, 2}
        and record.get("baseline_match") is True
        and record.get("w0_queue_empty") is True
        and record.get("w0_surface_empty") is True
        and record.get("cross_branch_state_carryover") is False
        and record.get("producer_invocation_count") == 4
        and record.get("continuation_validation_invocation_count") == 4
        and record.get("restoration_projection_match") is True
        and record.get("equal_input_continuation_audit") is True
        and record.get("graph_repository_write_observed") is False
        and record.get("terminal_classification_opened") is False
        and record.get("rung_assignment_opened") is False
    ):
        raise ContractError("C02 run record boundary drifted")
    spec = next(
        (
            row
            for row in freeze["run_specs"]
            if row["cell_id"] == record["cell_id"]
            and row["seed"] == record["seed"]
        ),
        None,
    )
    if spec is None or record.get("execution_configuration_digest") != spec[
        "execution_configuration_digest"
    ]:
        raise ContractError("C02 run configuration differs from EXEC-FREEZE")
    policy = load_execution_policy()
    reconstruction = record.get("reconstruction", {})
    reconstruction_path = validate_portable_path(
        reconstruction.get("expected_path", "")
    )
    expected_reconstruction_path = (
        spec["expected_path"]
        if record["attempt"] == 1
        else policy["artifact_contract"]["retry_run_artifact_path_template"].format(
            cell_id=record["cell_id"], seed=record["seed"]
        )
    )
    if reconstruction_path != expected_reconstruction_path:
        raise ContractError("C02 run reconstruction path differs from frozen scope")
    opportunities = record.get("opportunity_records", [])
    if len(opportunities) != 4:
        raise ContractError("C02 run must retain four opportunities")
    for opportunity in opportunities:
        validate_opportunity(opportunity)
        if not (
            opportunity["cell_id"] == record["cell_id"]
            and opportunity["seed"] == record["seed"]
            and opportunity["branch_point_snapshot_digest"]
            == record["branch_point_snapshot_digest"]
            and opportunity["branch_point_restoration_projection_digest"]
            == record["branch_point_restoration_projection_digest"]
            and opportunity["restored_restoration_projection_digest"]
            == record["branch_point_restoration_projection_digest"]
            and opportunity["raw_snapshot_equal"]
            is (
                opportunity["restored_snapshot_digest"]
                == opportunity["branch_point_snapshot_digest"]
            )
            and opportunity["raw_snapshot_normalization_observed"]
            is (not opportunity["raw_snapshot_equal"])
            and opportunity["continuation_digest"]
            == opportunity["twin_continuation_digest"]
            and opportunity["equal_input_continuation"] is True
            and opportunity["cross_branch_state_carryover"] is False
        ):
            raise ContractError("C02 opportunity lineage or restoration drifted")
    reconstruction_audit = record.get("medium_reconstruction", {})
    if not (
        reconstruction_audit.get("medium_projection_digest")
        == reconstruction_audit.get("reconstructed_medium_projection_digest")
        == record.get("medium_history_digest")
        and reconstruction_audit.get("participant_label_input_consumed") is False
        and reconstruction_audit.get("passed") is True
    ):
        raise ContractError("C02 independent medium reconstruction failed")
    if not (
        record.get("baseline_viability_audit", {}).get("profile_count") == 4
        and record.get("baseline_viability_audit", {}).get(
            "reader_configuration_count"
        )
        == 2
        and record.get("baseline_viability_audit", {}).get(
            "all_node_coherences_positive"
        )
        is True
        and record.get("baseline_viability_audit", {}).get(
            "participant_reserve_positive"
        )
        is True
        and record.get("exposure_match_audit", {}).get("passed") is True
    ):
        raise ContractError("C02 selectivity viability or exposure audit failed")
    runtime = record.get("runtime_binding", {})
    if not (
        runtime.get("observed_identity") == "pygrc==0.1"
        and runtime.get("execution_class") == "pygrc_runtime_with_rcae_producer"
        and runtime.get("fallback_used") is False
        and runtime.get("execution_specific_capabilities")
        == policy["execution_identity"]["execution_specific_capability_paths"]
    ):
        raise ContractError("C02 per-run runtime binding drifted")
    source_revisions = record.get("source_revisions", {})
    inherited = load_json(
        experiment_root() / "contracts/p2-i1/inherited-control-verification.json"
    )
    if not (
        source_revisions.get("rcae_execution_source") == freeze["source_revision"]
        and source_revisions.get("graph") == inherited["graph_source_revision"]
    ):
        raise ContractError("C02 per-run source identity drifted")
    receipt = record.get("runtime_receipt", {})
    if not (
        receipt.get("run_id") == record["run_id"]
        and receipt.get("runtime_identity") == "pygrc==0.1"
        and receipt.get("requested_operation_classes")
        == policy["execution_identity"]["registered_operation_classes"]
        and receipt.get("execution_specific_capabilities")
        == policy["execution_identity"]["execution_specific_capability_paths"]
        and receipt.get("conformance_status") == "passed"
        and receipt.get("fallback_used") is False
    ):
        raise ContractError("C02 embedded runtime receipt drifted")


def _retry_ledger_payload(
    *,
    freeze: Mapping[str, Any],
    failures: Sequence[Mapping[str, Any]],
    retry_results: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    by_cell: dict[str, list[Mapping[str, Any]]] = {cell: [] for cell in EXPECTED_CELLS}
    for failure in failures:
        by_cell[str(failure["cell_id"])].append(failure)
    authorizations = []
    for cell_id in EXPECTED_CELLS:
        cell_failures = sorted(by_cell[cell_id], key=lambda row: int(row["seed"]))
        if cell_failures:
            selected = cell_failures[0]
            authorizations.append(
                {
                    "cell_id": cell_id,
                    "seed": selected["seed"],
                    "primary_attempt": 1,
                    "retry_attempt": 2,
                    "selection_rule": "lowest_seed_with_first_infrastructure_failure",
                    "same_scientific_configuration_digest": selected[
                        "execution_configuration_digest"
                    ],
                    "status": "authorized",
                }
            )
    result = {
        "artifact_kind": "p2_i1_c02_retry_ledger",
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "evidence_effect": "infrastructure_only",
        "exec_freeze_digest": freeze["canonical_payload_digest"],
        "primary_failures": list(failures),
        "retry_authorizations": authorizations,
        "retry_results": list(retry_results),
        "retries_per_cell_limit": 1,
        "scientific_refinement_by_retry": False,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def validate_retry_ledger(
    ledger: Mapping[str, Any], *, freeze: Mapping[str, Any]
) -> None:
    _verify_canonical_payload(ledger)
    if not (
        ledger.get("artifact_kind") == "p2_i1_c02_retry_ledger"
        and ledger.get("cycle_id") == "P2-I1-C02"
        and ledger.get("exec_freeze_digest") == freeze["canonical_payload_digest"]
        and ledger.get("retries_per_cell_limit") == 1
        and ledger.get("scientific_refinement_by_retry") is False
    ):
        raise ContractError("C02 retry ledger boundary drifted")
    expected = _retry_ledger_payload(
        freeze=freeze,
        failures=ledger.get("primary_failures", []),
        retry_results=ledger.get("retry_results", []),
    )
    if ledger != expected:
        raise ContractError("C02 retry authorization is not deterministically derived")


def _load_effective_runs(
    policy: Mapping[str, Any], freeze: Mapping[str, Any]
) -> tuple[list[dict[str, Any]], list[str]]:
    root = find_repository_root()
    retry_template = policy["artifact_contract"]["retry_run_artifact_path_template"]
    ledger_path = root / policy["artifact_contract"]["retry_ledger_path"]
    ledger = load_json(ledger_path) if ledger_path.is_file() else None
    if ledger is not None:
        validate_retry_ledger(ledger, freeze=freeze)
    runs: list[dict[str, Any]] = []
    missing: list[str] = []
    for spec in freeze["run_specs"]:
        primary = root / spec["expected_path"]
        retry = root / retry_template.format(
            cell_id=spec["cell_id"], seed=spec["seed"]
        )
        selected = retry if retry.is_file() else primary
        if not selected.is_file():
            missing.append(spec["run_id"])
            continue
        record = load_json(selected)
        validate_run_record(record, freeze=freeze)
        if selected == retry:
            if ledger is None:
                raise ContractError("C02 retry artifact lacks its authorization ledger")
            authorizations = [
                row
                for row in ledger["retry_authorizations"]
                if row["cell_id"] == spec["cell_id"]
                and row["seed"] == spec["seed"]
                and row["retry_attempt"] == 2
                and row["status"] == "authorized"
            ]
            if len(authorizations) != 1 or record["attempt"] != 2:
                raise ContractError("C02 retry artifact is outside ledger authority")
        elif record["attempt"] != 1:
            raise ContractError("C02 primary artifact carries a retry attempt")
        runs.append(record)
    return runs, missing


def build_cycle_audit(
    *, policy: Mapping[str, Any], freeze: Mapping[str, Any]
) -> dict[str, Any]:
    """Resolve structural live obligations without assigning a rung."""

    validate_exec_freeze(freeze)
    runs, missing = _load_effective_runs(policy, freeze)
    by_key = {(row["cell_id"], row["seed"]): row for row in runs}
    duplicate_keys = len(by_key) != len(runs)
    worker_scope_ids = [row["worker_scope_id"] for row in runs]
    no_reused_worker_scope = len(worker_scope_ids) == len(set(worker_scope_ids))
    baseline_matches = all(row["baseline_match"] for row in runs)
    no_prior_trace_at_w0 = all(
        row["w0_queue_empty"] and row["w0_surface_empty"] for row in runs
    )
    full_run_matrix = len(runs) == 21 and not missing and not duplicate_keys

    cell_profiles: dict[str, Sequence[Mapping[str, Any]]] = {}
    for cell_id in EXPECTED_CELLS:
        cell_runs = [row for row in runs if row["cell_id"] == cell_id]
        if cell_runs:
            cell_profiles[cell_id] = cell_runs[0]["static_profile_identities"]
    if len(cell_profiles) == len(EXPECTED_CELLS):
        validate_cross_cell_static_profile_matching(cell_profiles)

    medium_dependency = []
    producer_parity = []
    trace_shuffle = []
    support_matching = []
    for seed in EXPECTED_SEEDS:
        candidate = by_key.get(("candidate-conditioning", seed))
        frozen = by_key.get(("medium-freeze-withdrawal", seed))
        shuffled = by_key.get(("trace-shuffle", seed))
        if candidate and frozen:
            same_post_writer = (
                candidate["post_writer_base_state_digest"]
                == frozen["post_writer_base_state_digest"]
            )
            same_opportunity = (
                candidate["participant_opportunity_signature"]
                == frozen["participant_opportunity_signature"]
            )
            medium_dependency.append(
                {
                    "seed": seed,
                    "same_post_writer_base_state": same_post_writer,
                    "same_participant_opportunity": same_opportunity,
                    "candidate_medium_present": candidate["medium_presence"],
                    "freeze_medium_present": frozen["medium_presence"],
                    "candidate_formed_count": sum(
                        row["raw_response"] for row in candidate["opportunity_records"]
                    ),
                    "freeze_formed_count": sum(
                        row["raw_response"] for row in frozen["opportunity_records"]
                    ),
                    "structural_control_passed": same_post_writer
                    and same_opportunity
                    and candidate["medium_presence"] is True
                    and frozen["medium_presence"] is False,
                }
            )
            producer_parity.append(
                {
                    "seed": seed,
                    "candidate_invocation_count": candidate[
                        "producer_invocation_count"
                    ],
                    "freeze_invocation_count": frozen["producer_invocation_count"],
                    "configuration_except_medium_match": candidate[
                        "producer_configuration_except_medium_digest"
                    ]
                    == frozen["producer_configuration_except_medium_digest"],
                }
            )
        if candidate and shuffled:
            trace_shuffle.append(
                {
                    "seed": seed,
                    "feedback_content_match": candidate[
                        "feedback_row_content_projection_digest"
                    ]
                    == shuffled["feedback_row_content_projection_digest"],
                    "expected_source_digest_differs": candidate[
                        "expected_source_surface_digest"
                    ]
                    != shuffled["expected_source_surface_digest"],
                    "candidate_expected_arrival": candidate[
                        "expected_source_surface_digest"
                    ]
                    == candidate["pulse_contact_surface_digest"],
                    "shuffle_expected_departure": shuffled[
                        "expected_source_surface_digest"
                    ]
                    == shuffled["departure_contact_surface_digest"],
                }
            )
        ordinary = [
            by_key.get((cell_id, seed))
            for cell_id in (
                "reference",
                "candidate-conditioning",
                "medium-freeze-withdrawal",
                "trace-shuffle",
                "susceptibility-inversion",
            )
        ]
        ordinary = [row for row in ordinary if row]
        if ordinary:
            support_matching.append(
                {
                    "seed": seed,
                    "ordinary_projection_match": len(
                        {row["support_budget_projection_digest"] for row in ordinary}
                    )
                    == 1,
                    "parent_exception_declared": (
                        by_key.get(("parent-context-contrast", seed), {}).get(
                            "declared_cell_exception"
                        )
                        == "support_scale"
                    ),
                    "carrier_exception_declared": (
                        by_key.get(("carrier-timescale-contrast", seed), {}).get(
                            "declared_cell_exception"
                        )
                        == "reader_packet_amount"
                    ),
                }
            )

    obligation_results = {
        "C02-OBL-01": full_run_matrix and all(
            row["medium_reconstruction"]["passed"] for row in runs
        ),
        "C02-OBL-02": full_run_matrix
        and bool(medium_dependency)
        and all(row["structural_control_passed"] for row in medium_dependency),
        "C02-OBL-03": full_run_matrix and all(
            row["baseline_viability_audit"]["profile_count"] == 4
            and row["baseline_viability_audit"]["reader_configuration_count"] == 2
            for row in runs
        ),
        "C02-OBL-04": full_run_matrix
        and all(row["exposure_match_audit"]["passed"] for row in runs),
        "C02-OBL-05": full_run_matrix and baseline_matches,
        "C02-OBL-06": full_run_matrix
        and no_reused_worker_scope
        and no_prior_trace_at_w0,
        "C02-OBL-07": full_run_matrix and all(
            opportunity["restored_restoration_projection_digest"]
            == opportunity["branch_point_restoration_projection_digest"]
            and opportunity["continuation_digest"]
            == opportunity["twin_continuation_digest"]
            and opportunity["equal_input_continuation"] is True
            and opportunity["cross_branch_state_carryover"] is False
            for run in runs
            for opportunity in run["opportunity_records"]
        ),
        "C02-OBL-08": full_run_matrix
        and bool(support_matching)
        and all(
            row["ordinary_projection_match"]
            and row["parent_exception_declared"]
            and row["carrier_exception_declared"]
            for row in support_matching
        ),
        "C02-OBL-09": full_run_matrix and all(
            row["runtime_binding"]["fallback_used"] is False for row in runs
        ),
        "C02-OBL-10": full_run_matrix
        and bool(producer_parity)
        and all(
            row["candidate_invocation_count"] == row["freeze_invocation_count"] == 4
            and row["configuration_except_medium_match"]
            for row in producer_parity
        ),
        "C02-OBL-11": full_run_matrix
        and bool(trace_shuffle)
        and all(all(value for key, value in row.items() if key != "seed") for row in trace_shuffle),
        "C02-OBL-12": full_run_matrix and all(
            row["runtime_receipt"]["conformance_status"] == "passed"
            and row["graph_repository_write_observed"] is False
            for row in runs
        ),
    }
    complete = full_run_matrix and all(obligation_results.values())
    result = {
        "artifact_kind": "p2_i1_c02_cycle_audit",
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "evidence_effect": "control_and_integrity_only",
        "exec_freeze_digest": freeze["canonical_payload_digest"],
        "effective_run_count": len(runs),
        "missing_run_ids": missing,
        "duplicate_cell_seed_keys": duplicate_keys,
        "worker_scope_ids": worker_scope_ids,
        "no_reused_worker_scope": no_reused_worker_scope,
        "baseline_matches": baseline_matches,
        "no_prior_trace_at_w0": no_prior_trace_at_w0,
        "medium_dependency_audit": medium_dependency,
        "producer_parity_audit": producer_parity,
        "trace_shuffle_audit": trace_shuffle,
        "support_budget_matching_audit": support_matching,
        "obligation_results": [
            {
                "obligation_id": obligation_id,
                "status": "structural_prerequisites_passed"
                if passed
                else "blocked_or_incomplete",
                "scientific_interpretation_deferred": True,
            }
            for obligation_id, passed in obligation_results.items()
        ],
        "audit_complete": complete,
        "candidate_outcomes_present": bool(runs),
        "scientific_rung_assigned": False,
        "terminal_classification_opened": False,
        "thresholds_applied_as_terminal_boolean_gates": False,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def build_execution_manifest(
    *, policy: Mapping[str, Any], freeze: Mapping[str, Any]
) -> dict[str, Any]:
    """Index retained C02 machine artifacts without interpreting outcomes."""

    validate_exec_freeze(freeze)
    root = find_repository_root()
    runs, missing = _load_effective_runs(policy, freeze)
    if missing:
        raise ContractError("C02 execution manifest requires every effective run")
    contract = policy["artifact_contract"]
    audit_path = root / contract["cycle_audit_path"]
    ledger_path = root / contract["retry_ledger_path"]
    if not audit_path.is_file() or not ledger_path.is_file():
        raise ContractError("C02 execution manifest requires cycle audit and retry ledger")
    audit = load_json(audit_path)
    _verify_canonical_payload(audit)
    expected_audit = build_cycle_audit(policy=policy, freeze=freeze)
    if audit != expected_audit:
        raise ContractError("C02 cycle audit does not reconstruct from retained runs")
    ledger = load_json(ledger_path)
    validate_retry_ledger(ledger, freeze=freeze)
    if audit.get("exec_freeze_digest") != freeze["canonical_payload_digest"]:
        raise ContractError("C02 audit references another EXEC-FREEZE")

    files: list[dict[str, Any]] = []
    for run in runs:
        path_value = run["reconstruction"]["expected_path"]
        path = root / validate_portable_path(path_value)
        files.append(
            {
                "artifact_id": run["run_id"],
                "artifact_role": "cell_seed_run",
                "path": path_value,
                "semantic_digest": semantic_file_digest(path),
                "file_sha256": digest_file(path),
                "size_bytes": path.stat().st_size,
                "reconstruction_status": run["reconstruction"]["status"],
            }
        )
    for artifact_id, role, path in (
        ("P2-I1-C02-retry-ledger", "retry_ledger", ledger_path),
        ("P2-I1-C02-cycle-audit", "cycle_audit", audit_path),
    ):
        files.append(
            {
                "artifact_id": artifact_id,
                "artifact_role": role,
                "path": path.relative_to(root).as_posix(),
                "semantic_digest": semantic_file_digest(path),
                "file_sha256": digest_file(path),
                "size_bytes": path.stat().st_size,
                "reconstruction_status": "deterministically_derived",
            }
        )
    result = {
        "artifact_kind": "p2_i1_c02_execution_manifest",
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "evidence_effect": "retention_index_only",
        "exec_freeze_digest": freeze["canonical_payload_digest"],
        "artifact_count": len(files),
        "artifacts": sorted(files, key=lambda row: row["path"]),
        "artifact_set_size_bytes": sum(row["size_bytes"] for row in files),
        "all_expected_runs_present": len(runs) == 21,
        "cycle_audit_complete": audit.get("audit_complete") is True,
        "scientific_interpretation_opened": False,
        "rung_assignment_opened": False,
        "terminal_classification_opened": False,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def _run_one_subprocess_command(
    *,
    freeze_path: str,
    cell_id: str,
    seed: int,
    attempt: int,
    graph_root: str,
    output_path: str,
    retry_ledger_path: str | None = None,
) -> list[str]:
    command = [
        sys.executable,
        (
            "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
            "scripts/p2_i1_execution.py"
        ),
        "run-one",
        "--exec-freeze",
        freeze_path,
        "--cell",
        cell_id,
        "--seed",
        str(seed),
        "--attempt",
        str(attempt),
        "--graph-root",
        graph_root,
        "--output",
        output_path,
    ]
    if retry_ledger_path is not None:
        command.extend(["--retry-ledger", retry_ledger_path])
    return command


def _portable_failure_record(
    *, spec: Mapping[str, Any], result: subprocess.CompletedProcess[str]
) -> dict[str, Any]:
    diagnostic = result.stderr.strip()
    root = find_repository_root()
    portable_diagnostic = diagnostic.replace(str(root), "RCAE_CHECKOUT")
    portable_diagnostic = portable_diagnostic.replace(
        str(root.parent), "LOCAL_CHECKOUT_PARENT"
    )
    return {
        "cell_id": spec["cell_id"],
        "seed": spec["seed"],
        "attempt": 1,
        "execution_configuration_digest": spec["execution_configuration_digest"],
        "exit_code": result.returncode,
        "failure_class": "runtime_or_integrity_failure_pending_review",
        "diagnostic_digest": digest_canonical_data(portable_diagnostic),
        "diagnostic_summary": portable_diagnostic[:2000],
        "candidate_scientific_effect": "none_operational_only",
    }


def command_validate_policy(args: argparse.Namespace) -> int:
    _write_output(args.output, validate_execution_policy(load_execution_policy()))
    return 0


def command_build_exec_freeze(args: argparse.Namespace) -> int:
    binding_path = find_repository_root() / validate_portable_path(
        args.execution_binding_receipt
    )
    result = build_exec_freeze(
        execution_binding_path=binding_path,
        allow_dirty_preview=args.allow_dirty_preview,
    )
    expected = load_execution_policy()["artifact_contract"]["exec_freeze_path"]
    if result["retention_eligible"] is True and args.output != expected:
        raise ContractError("retained C02 EXEC-FREEZE output path drifted")
    _write_output(args.output, result)
    return 0


def command_build_execution_binding(args: argparse.Namespace) -> int:
    policy = load_execution_policy()
    expected = policy["artifact_contract"]["execution_binding_receipt_path"]
    if args.output != expected and not args.allow_dirty_preview:
        raise ContractError("retained C02 binding receipt output path drifted")
    result = build_execution_binding_receipt(
        graph_root=Path(args.graph_root),
        allow_dirty_preview=args.allow_dirty_preview,
    )
    _write_output(args.output, result)
    return 0


def command_validate_exec_freeze(args: argparse.Namespace) -> int:
    path = find_repository_root() / validate_portable_path(args.exec_freeze)
    freeze = load_json(path)
    validate_exec_freeze(
        freeze,
        freeze_path=path,
        require_tracked=args.require_tracked,
    )
    result = {
        "artifact_kind": "p2_i1_c02_exec_freeze_validation",
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "status": "passed",
        "tracked_validation_required": args.require_tracked,
        "candidate_execution_authorized": freeze[
            "candidate_execution_authorized"
        ],
        "exec_freeze_digest": freeze["canonical_payload_digest"],
    }
    _write_output(args.output, result)
    return 0


def command_run_one(args: argparse.Namespace) -> int:
    freeze_path = find_repository_root() / validate_portable_path(args.exec_freeze)
    retry_path = (
        None
        if args.retry_ledger is None
        else find_repository_root() / validate_portable_path(args.retry_ledger)
    )
    result = _run_one_authorized(
        freeze=load_json(freeze_path),
        freeze_path=freeze_path,
        cell_id=args.cell,
        seed=args.seed,
        attempt=args.attempt,
        graph_root=Path(args.graph_root),
        output_path=args.output,
        retry_ledger_path=retry_path,
    )
    _write_output(args.output, result)
    return 0


def command_run_cycle(args: argparse.Namespace) -> int:
    """Execute each primary in a fresh process, then deterministic retries."""

    root = find_repository_root()
    freeze_path = root / validate_portable_path(args.exec_freeze)
    freeze = load_json(freeze_path)
    validate_exec_freeze(freeze, freeze_path=freeze_path, require_tracked=True)
    policy = load_execution_policy()
    if any(path.exists() for path in _candidate_result_paths(policy)):
        raise ContractError("C02 cycle refuses to overwrite existing candidate artifacts")
    failures: list[dict[str, Any]] = []
    for spec in freeze["run_specs"]:
        command = _run_one_subprocess_command(
            freeze_path=args.exec_freeze,
            cell_id=spec["cell_id"],
            seed=spec["seed"],
            attempt=1,
            graph_root=args.graph_root,
            output_path=spec["expected_path"],
        )
        result = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            failures.append(_portable_failure_record(spec=spec, result=result))

    ledger_path_value = policy["artifact_contract"]["retry_ledger_path"]
    ledger_path = root / ledger_path_value
    ledger = _retry_ledger_payload(freeze=freeze, failures=failures)
    _write_output(ledger_path_value, ledger)
    retry_results: list[dict[str, Any]] = []
    retry_template = policy["artifact_contract"]["retry_run_artifact_path_template"]
    for authorization in ledger["retry_authorizations"]:
        cell_id = authorization["cell_id"]
        seed = authorization["seed"]
        output_path = retry_template.format(cell_id=cell_id, seed=seed)
        command = _run_one_subprocess_command(
            freeze_path=args.exec_freeze,
            cell_id=cell_id,
            seed=seed,
            attempt=2,
            graph_root=args.graph_root,
            output_path=output_path,
            retry_ledger_path=ledger_path_value,
        )
        result = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        retry_diagnostic = result.stderr.strip().replace(
            str(root), "RCAE_CHECKOUT"
        ).replace(str(root.parent), "LOCAL_CHECKOUT_PARENT")[:2000]
        retry_results.append(
            {
                "cell_id": cell_id,
                "seed": seed,
                "attempt": 2,
                "exit_code": result.returncode,
                "status": "completed" if result.returncode == 0 else "failed",
                "diagnostic_digest": digest_canonical_data(retry_diagnostic),
                "diagnostic_summary": retry_diagnostic,
                "candidate_scientific_effect": (
                    "eligible_if_completed_and_validated"
                    if result.returncode == 0
                    else "none_operational_only"
                ),
            }
        )
    final_ledger = _retry_ledger_payload(
        freeze=freeze,
        failures=failures,
        retry_results=retry_results,
    )
    _write_output(ledger_path_value, final_ledger)
    validate_retry_ledger(final_ledger, freeze=freeze)
    summary = {
        "artifact_kind": "p2_i1_c02_cycle_execution_summary",
        "schema_version": "1.0.0",
        "cycle_id": "P2-I1-C02",
        "primary_run_count": 21,
        "primary_failure_count": len(failures),
        "retry_count": len(retry_results),
        "retry_failure_count": sum(
            row["status"] == "failed" for row in retry_results
        ),
        "scientific_interpretation_opened": False,
        "next_required_command": "build-cycle-audit",
    }
    _write_output(args.summary_output, summary)
    return 0


def command_build_cycle_audit(args: argparse.Namespace) -> int:
    freeze_path = find_repository_root() / validate_portable_path(args.exec_freeze)
    freeze = load_json(freeze_path)
    validate_exec_freeze(freeze, freeze_path=freeze_path, require_tracked=True)
    result = build_cycle_audit(policy=load_execution_policy(), freeze=freeze)
    expected = load_execution_policy()["artifact_contract"]["cycle_audit_path"]
    if args.output != expected:
        raise ContractError("C02 cycle audit output differs from frozen contract")
    _write_output(args.output, result)
    return 0


def command_build_execution_manifest(args: argparse.Namespace) -> int:
    freeze_path = find_repository_root() / validate_portable_path(args.exec_freeze)
    freeze = load_json(freeze_path)
    validate_exec_freeze(freeze, freeze_path=freeze_path, require_tracked=True)
    policy = load_execution_policy()
    expected = policy["artifact_contract"]["execution_manifest_path"]
    if args.output != expected:
        raise ContractError("C02 execution manifest output differs from frozen contract")
    _write_output(
        args.output,
        build_execution_manifest(policy=policy, freeze=freeze),
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-policy")
    validate.add_argument("--output")
    validate.set_defaults(handler=command_validate_policy)

    binding = subparsers.add_parser("build-execution-binding")
    binding.add_argument("--graph-root", required=True)
    binding.add_argument("--output", required=True)
    binding.add_argument("--allow-dirty-preview", action="store_true")
    binding.set_defaults(handler=command_build_execution_binding)

    freeze = subparsers.add_parser("build-exec-freeze")
    freeze.add_argument("--output", required=True)
    freeze.add_argument("--execution-binding-receipt", required=True)
    freeze.add_argument("--allow-dirty-preview", action="store_true")
    freeze.set_defaults(handler=command_build_exec_freeze)

    validate_freeze = subparsers.add_parser("validate-exec-freeze")
    validate_freeze.add_argument("--exec-freeze", required=True)
    validate_freeze.add_argument("--require-tracked", action="store_true")
    validate_freeze.add_argument("--output")
    validate_freeze.set_defaults(handler=command_validate_exec_freeze)

    run_one = subparsers.add_parser("run-one")
    run_one.add_argument("--exec-freeze", required=True)
    run_one.add_argument("--cell", required=True)
    run_one.add_argument("--seed", required=True, type=int)
    run_one.add_argument("--attempt", required=True, type=int)
    run_one.add_argument("--graph-root", required=True)
    run_one.add_argument("--output", required=True)
    run_one.add_argument("--retry-ledger")
    run_one.set_defaults(handler=command_run_one)

    run_cycle = subparsers.add_parser("run-cycle")
    run_cycle.add_argument("--exec-freeze", required=True)
    run_cycle.add_argument("--graph-root", required=True)
    run_cycle.add_argument("--summary-output")
    run_cycle.set_defaults(handler=command_run_cycle)

    audit = subparsers.add_parser("build-cycle-audit")
    audit.add_argument("--exec-freeze", required=True)
    audit.add_argument("--output", required=True)
    audit.set_defaults(handler=command_build_cycle_audit)

    manifest = subparsers.add_parser("build-execution-manifest")
    manifest.add_argument("--exec-freeze", required=True)
    manifest.add_argument("--output", required=True)
    manifest.set_defaults(handler=command_build_execution_manifest)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.handler(args))
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        sys.stderr.write(f"P2-I1 C02 execution error: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
