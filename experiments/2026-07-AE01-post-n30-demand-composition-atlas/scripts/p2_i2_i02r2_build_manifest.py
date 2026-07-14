#!/usr/bin/env python3
"""Build the effective P2-I2 I02R2 source and reset-provider manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


PREVIOUS_REVISION = "3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5"
PROPOSED_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"


def _git_bytes(graph_root: Path, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(graph_root), "show", f"{PROPOSED_REVISION}:{path}"]
    )


def _sha(graph_root: Path, path: str) -> str:
    return hashlib.sha256(_git_bytes(graph_root, path)).hexdigest()


def _source(
    graph_root: Path,
    path: str,
    role: str,
    classifications: list[str],
    purpose: str,
) -> dict[str, Any]:
    return {
        "source_id": f"grc:{path}",
        "path": path,
        "sha256": _sha(graph_root, path),
        "role": role,
        "source_classifications": classifications,
        "purpose": purpose,
    }


def build(graph_root: Path, previous_manifest_path: Path) -> dict[str, Any]:
    previous = json.loads(previous_manifest_path.read_text())
    previous_sha = hashlib.sha256(previous_manifest_path.read_bytes()).hexdigest()
    source_entries = []
    for row in previous["source_entries"]:
        updated = dict(row)
        updated["sha256"] = _sha(graph_root, row["path"])
        source_entries.append(updated)

    additions = [
        _source(
            graph_root,
            "src/pygrc/core/__init__.py",
            "admitted_package_identity",
            ["public_api_source", "schema_or_contract_source"],
            "Public reset-baseline serialization exports",
        ),
        _source(
            graph_root,
            "src/pygrc/core/interfaces.py",
            "admitted_runtime_source",
            ["runtime_source", "public_api_source", "schema_or_contract_source"],
            "Common public rebase_reset_baseline lifecycle interface",
        ),
        _source(
            graph_root,
            "src/pygrc/core/serialization.py",
            "admitted_runtime_source",
            ["runtime_source", "public_api_source", "schema_or_contract_source"],
            "Versioned non-recursive reset-baseline snapshot group, validation, and legacy boundary",
        ),
        _source(
            graph_root,
            "src/pygrc/models/grc_9_v3.py",
            "admitted_runtime_source",
            ["runtime_source", "public_api_source"],
            "Embedded GRC9V3 snapshot and reset-baseline persistence used by LGRC9V3",
        ),
        _source(
            graph_root,
            "specs/grc-common-interface.md",
            "supporting_boundary_only",
            ["schema_or_contract_source", "documentation_only"],
            "Common lifecycle method contract",
        ),
        _source(
            graph_root,
            "specs/grc-reset-baseline-persistence.md",
            "supporting_boundary_only",
            ["schema_or_contract_source", "documentation_only"],
            "Normative reset-baseline persistence and compatibility contract",
        ),
        _source(
            graph_root,
            "specs/lgrc-9-v3-restoration-identity.md",
            "supporting_boundary_only",
            ["schema_or_contract_source", "documentation_only"],
            "LGRC9V3 restoration identity v1/v2 boundary",
        ),
        _source(
            graph_root,
            "specs/lgrc-9-v3-spec.md",
            "supporting_boundary_only",
            ["schema_or_contract_source", "documentation_only"],
            "LGRC9V3 reset lifecycle integration boundary",
        ),
        _source(
            graph_root,
            "tests/core/test_interfaces.py",
            "supporting_evidence_only",
            ["test_or_conformance_source"],
            "Common interface conformance",
        ),
        _source(
            graph_root,
            "tests/core/test_serialization_contract.py",
            "supporting_evidence_only",
            ["test_or_conformance_source"],
            "Reset-baseline serialization and malformed-input conformance",
        ),
        _source(
            graph_root,
            "tests/models/test_reset_baseline_persistence.py",
            "supporting_evidence_only",
            ["test_or_conformance_source"],
            "Cross-family reset persistence, legacy, and LGRC9V3 identity-v2 conformance",
        ),
        _source(
            graph_root,
            "implementation/corrections/PyGRC-ResetBaselinePersistenceChecklist.md",
            "supporting_evidence_only",
            ["evidence_or_closeout_source"],
            "Upstream correction checklist",
        ),
        _source(
            graph_root,
            "implementation/corrections/PyGRC-ResetBaselinePersistenceCloseout.md",
            "supporting_evidence_only",
            ["evidence_or_closeout_source"],
            "Upstream correction closeout and claim boundary",
        ),
        _source(
            graph_root,
            "implementation/corrections/PyGRC-ResetBaselinePersistencePlan.md",
            "supporting_evidence_only",
            ["evidence_or_closeout_source"],
            "Upstream correction plan and intended validation scope",
        ),
    ]
    existing = {row["source_id"] for row in source_entries}
    for row in additions:
        assert row["source_id"] not in existing
        source_entries.append(row)
    assert len(source_entries) == 31

    profiles = dict(previous["callable_contract_profiles"])
    profiles["reset"] = {
        "unsupported_argument_shape": "No arguments beyond self; unavailable legacy baseline raises SnapshotCompatibilityError.",
        "causal_relevance": "Restores the persisted construction or explicitly rebased baseline represented by reset-aware identity v2.",
        "claim_boundary": "Reset conformance does not select a P2-I2 branch point or prove unrestricted continuation equivalence.",
    }
    profiles["reset_rebase"] = {
        "unsupported_argument_shape": "No arguments beyond self.",
        "causal_relevance": "Explicitly replaces the future reset baseline with current native state.",
        "claim_boundary": "Rebase is prospective and does not recover legacy construction provenance; RCAE must record rebase provenance separately.",
    }
    profiles["reset_group_builder"] = {
        "unsupported_argument_shape": "Requires a non-empty model family and exactly one available baseline snapshot or unavailable reason.",
        "causal_relevance": "Builds the versioned native lifecycle group persisted by save/load.",
        "claim_boundary": "Artifact construction alone does not establish family-valid restoration.",
    }
    profiles["reset_group_validator"] = {
        "unsupported_argument_shape": "Malformed, recursive, wrong-family, unsupported-version, or inconsistent status payloads fail explicitly.",
        "causal_relevance": "Guards the baseline lifecycle artifact before load or provider use.",
        "claim_boundary": "Shape validation is not behavioral replay.",
    }
    profiles["reset_group_reader"] = {
        "unsupported_argument_shape": "Requires a valid snapshot and expected family; legacy or explicitly unavailable data returns no baseline.",
        "causal_relevance": "Separates available reset state from legacy/unavailable state without inventing provenance.",
        "claim_boundary": "A missing return does not authorize implicit rebase or fallback.",
    }
    profiles["restoration_identity_v2"] = {
        "unsupported_argument_shape": "Requires a supported LGRC9V3 model/snapshot with an available valid reset-baseline group.",
        "causal_relevance": "Composes current-state identity v1 and reset-baseline identity v1 into reset-aware identity v2.",
        "claim_boundary": "Equality covers declared current/reset native state, not construction history, RCAE-owned state, or unrestricted continuation.",
    }
    profiles["restoration_digest_v2"] = {
        "unsupported_argument_shape": "Same input boundary as restoration_identity_v2; unsupported input fails without fallback.",
        "causal_relevance": "Digests canonical reset-aware identity v2.",
        "claim_boundary": "Digest equality is not raw snapshot equality, behavioral replay, or scientific evidence.",
    }

    callables = list(previous["callable_entries"])
    additions_callables = [
        {
            "symbol": "pygrc.core.GRCModel.rebase_reset_baseline",
            "role": "admitted_contract_callable",
            "contract_profile": "reset_rebase",
            "public_export_source": "grc:src/pygrc/core/__init__.py",
            "implementation_source": "grc:src/pygrc/core/interfaces.py",
        },
        {
            "symbol": "pygrc.core.build_reset_baseline_group",
            "role": "admitted_runtime_callable",
            "contract_profile": "reset_group_builder",
            "public_export_source": "grc:src/pygrc/core/__init__.py",
            "implementation_source": "grc:src/pygrc/core/serialization.py",
        },
        {
            "symbol": "pygrc.core.validate_reset_baseline_group",
            "role": "admitted_runtime_callable",
            "contract_profile": "reset_group_validator",
            "public_export_source": "grc:src/pygrc/core/__init__.py",
            "implementation_source": "grc:src/pygrc/core/serialization.py",
        },
        {
            "symbol": "pygrc.core.reset_baseline_snapshot",
            "role": "admitted_runtime_callable",
            "contract_profile": "reset_group_reader",
            "public_export_source": "grc:src/pygrc/core/__init__.py",
            "implementation_source": "grc:src/pygrc/core/serialization.py",
        },
        {
            "symbol": "pygrc.models.LGRC9V3.rebase_reset_baseline",
            "role": "admitted_runtime_callable",
            "contract_profile": "reset_rebase",
            "public_export_source": "grc:src/pygrc/models/__init__.py",
            "implementation_source": "grc:src/pygrc/models/lgrc_9_v3_runtime.py",
        },
        {
            "symbol": "pygrc.models.lgrc9v3_restoration_identity_v2",
            "role": "admitted_restoration_callable",
            "contract_profile": "restoration_identity_v2",
            "public_export_source": "grc:src/pygrc/models/__init__.py",
            "implementation_source": "grc:src/pygrc/models/lgrc_9_v3_restoration.py",
        },
        {
            "symbol": "pygrc.models.digest_lgrc9v3_restoration_identity_v2",
            "role": "admitted_restoration_callable",
            "contract_profile": "restoration_digest_v2",
            "public_export_source": "grc:src/pygrc/models/__init__.py",
            "implementation_source": "grc:src/pygrc/models/lgrc_9_v3_restoration.py",
        },
    ]
    existing_symbols = {row["symbol"] for row in callables}
    for row in additions_callables:
        assert row["symbol"] not in existing_symbols
        callables.append(row)
    assert len(callables) == 31

    return {
        "artifact_id": "P2-I2-I02R2-ADMITTED-SOURCE-AND-RESET-PROVIDER-MANIFEST",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I02R2",
        "lane_id": "AE01-L02",
        "status": "admitted_after_i02r2_revalidation",
        "admitted_at": "2026-07-14",
        "evidence_effect": "Exact updated source and reset-aware provider admission only; no realization, calibration, candidate behavior, restoration claim beyond tested generic conformance, or scientific evidence.",
        "historical_authority": {
            "previous_manifest": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json",
            "previous_manifest_sha256_at_i02r2_entry": previous_sha,
            "previous_graph_revision": PREVIOUS_REVISION,
            "previous_provider": "pygrc.models.lgrc9v3_restoration_identity_v1",
            "previous_reset_boundary": "Reset baseline not represented; reset-dependent branching prohibited or externally composed.",
            "historical_record_rewritten": False,
        },
        "repository": {
            "repository_id": "grc",
            "repository_name": "graph-reflexive-coherence",
            "revision": PROPOSED_REVISION,
            "branch_observed": "main",
            "worktree_state_at_admission": "clean",
            "read_only": True,
            "portable_identity_rule": "grc:<repository-relative path> at full revision plus SHA-256",
            "local_checkout_is_identity": False,
            "complete_transitive_dependency_lock": False,
            "dependency_boundary": "This manifest binds the effective prior P2-I2 source scope plus every new reset-correction authority. I06 must still bind the complete executable environment it registers.",
        },
        "rcae_entry_authority": {
            "committed_head_revision": "10c18fad2ba8ecac9ddacb0f0bc55813e6356c60",
            "input_freeze": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i2/i02r2-reset-baseline-revalidation-input-freeze.json",
            "separate_from_graph_revision": True,
        },
        "source_role_taxonomy": previous["source_role_taxonomy"],
        "source_entries": source_entries,
        "callable_contract_profiles": profiles,
        "callable_entries": callables,
        "snapshot_reset_contract": {
            "snapshot_schema": "pygrc.snapshot",
            "snapshot_version": 1,
            "reset_baseline_schema": "pygrc.reset_baseline",
            "reset_baseline_version": 1,
            "available_baseline_is_complete_same_family_snapshot": True,
            "nested_reset_baseline_forbidden": True,
            "params_hash_must_match_outer_snapshot": True,
            "set_state_rebases_baseline": False,
            "explicit_rebase_callable": "pygrc.models.LGRC9V3.rebase_reset_baseline",
            "legacy_missing_baseline": "current state loads; reset and v2 identity fail until explicit prospective rebase",
            "historical_baseline_recovered_by_rebase": False,
        },
        "restoration_providers": {
            "current_state_v1": {
                "provider": "pygrc.models.lgrc9v3_restoration_identity_v1",
                "digest_provider": "pygrc.models.digest_lgrc9v3_restoration_identity_v1",
                "artifact_schema_version": "lgrc9v3_restoration_identity_v1",
                "reset_aware": False,
                "redefined_by_i02r2": False,
                "status": "admitted_current_state_provider_not_selected",
            },
            "current_plus_reset_v2": {
                "provider": "pygrc.models.lgrc9v3_restoration_identity_v2",
                "digest_provider": "pygrc.models.digest_lgrc9v3_restoration_identity_v2",
                "artifact_schema_version": "lgrc9v3_restoration_identity_v2",
                "artifact_kind": "lgrc9v3_restoration_identity",
                "accepted_input": "Supported LGRC9V3 model or complete version-1 snapshot with valid available reset-baseline group",
                "unsupported_input": "Legacy/unavailable baseline, wrong family/version, malformed/partial/recursive group, raw digest, RCAE projection, or arbitrary object",
                "unsupported_behavior": "SnapshotCompatibilityError or strict snapshot validation error; no fallback",
                "digest_rule": "SHA-256 over UTF-8 pygrc.core.canonical_json_dumps(identity_document)",
                "included_state": [
                    "current_state_restoration_identity_v1",
                    "reset_baseline_restoration_identity_v1"
                ],
                "status": "admitted_for_conditional_later_selection",
            },
            "selected_provider": None,
            "selection_stage": "I03 proposes a compatible provider; I06 freezes exact provider/schema and reset-baseline provenance before branch comparison.",
            "provider_selection_is_runtime_recovery": False,
            "provider_mismatch_blocks_comparison": True,
        },
        "identity_coverage": {
            "reset_baseline": {
                "owner": "PyGRC",
                "v1_disposition": "not_covered_current_state_only",
                "v2_disposition": "covered_by_native_provider",
                "legacy_without_rebase": "unsupported_blocks_branching",
                "explicit_rebase": "covered_prospectively_with_external_rebase_provenance_required",
            },
            "current_native_state": "covered_by_v1_and_v2_current_component",
            "rcae_external_state": "external_composition_required_as_in_historical_manifest",
            "all_continuation_relevant_components_dispositioned": True,
        },
        "validation_authority": {
            "source_transition": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i2/i02r2-graph-source-transition.json",
            "validator": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i02r2_validate.py",
            "validation_record": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i2/i02r2-reset-baseline-validation.json",
            "focused_upstream_tests": "68 passed and 32 subtests passed; cache disabled; temporary files outside graph repository",
        },
        "admission_disposition": {
            "updated_source_admitted": True,
            "reset_baseline_persistence_contract_admitted": True,
            "reset_aware_v2_provider_admitted": True,
            "provider_selected": False,
            "realization_selected": False,
            "dependence_mode_selected": False,
            "calibration_opened": False,
            "candidate_execution_opened": False,
            "scientific_evidence_assigned": False,
            "source_admission_gate": "passed_after_i02r2_revalidation",
        },
        "change_control": {
            "change_id": "P2-I2-CHG-006",
            "governance_class": "source_admission_revision_update",
            "reopening_conditions": [
                "Updated revision/path/digest/import/export/signature fails reconstruction",
                "Reset baseline does not persist across save/load or repeated cycles",
                "V2 does not distinguish reset-baseline-only differences",
                "Legacy or malformed input does not fail according to the admitted policy",
                "A different provider/schema or reset-rebase provenance is proposed",
                "A later profile requires source or state outside this manifest"
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-root", type=Path, required=True)
    parser.add_argument("--previous-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.graph_root.resolve(), args.previous_manifest.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
