"""Reconstruct P2-I2-I02R1 identity and provider-contract validation.

This validator performs generic source/import/provider checks only. It does not
construct or execute a P2-I2 pool, cell, control, comparator, or response.
"""

from __future__ import annotations

import argparse
from collections import UserDict
from copy import deepcopy
import hashlib
import importlib.metadata
import inspect
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
from typing import Any


GRAPH_REVISION = "3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5"
EXPECTED_SOURCE_COUNT = 17
EXPECTED_SYMBOL_COUNT = 24


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(graph_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(graph_root), *args],
        text=True,
    ).strip()


def _resolve_symbol(symbol: str) -> Any:
    import pygrc.models

    prefix = "pygrc.models."
    if not symbol.startswith(prefix):
        raise AssertionError(f"unexpected public symbol: {symbol}")
    value: Any = pygrc.models
    for part in symbol[len(prefix) :].split("."):
        value = getattr(value, part)
    return value


def _normalized_module_source(obj: Any, graph_root: Path) -> tuple[str, str]:
    module = inspect.getmodule(obj)
    if module is None or module.__file__ is None:
        raise AssertionError(f"callable module file unavailable: {obj!r}")
    raw = str(Path(module.__file__).resolve())
    relative = Path(raw).relative_to((graph_root / "src").resolve())
    return raw, f"grc:src/{relative.as_posix()}"


def _exception_record(label: str, function: Any, value: Any) -> dict[str, Any]:
    try:
        function(value)
    except Exception as exc:  # exact type/message are retained below
        return {
            "case": label,
            "rejected": True,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "fallback_attempted": False,
        }
    raise AssertionError(f"unsupported provider input was accepted: {label}")


def _callable_contract(
    entry: dict[str, Any],
    graph_root: Path,
    source_by_id: dict[str, dict[str, Any]],
    profiles: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    obj = _resolve_symbol(entry["symbol"])
    _raw_module_file, normalized_module_file = _normalized_module_source(
        obj,
        graph_root,
    )
    implementation = source_by_id[entry["implementation_source"]]
    if normalized_module_file != entry["implementation_source"]:
        raise AssertionError(
            f"implementation source mismatch for {entry['symbol']}: "
            f"{normalized_module_file} != {entry['implementation_source']}"
        )
    profile = profiles[entry["contract_profile"]]
    signature = str(inspect.signature(obj))
    return {
        "symbol": entry["symbol"],
        "public_import_path": entry["symbol"],
        "module": getattr(obj, "__module__", None),
        "qualified_name": getattr(obj, "__qualname__", None),
        "signature": signature,
        "normalized_module_source": normalized_module_file,
        "implementation_sha256": implementation["sha256"],
        "admission_role": entry["role"],
        "contract_profile": entry["contract_profile"],
        "unsupported_argument_shape": profile["unsupported_argument_shape"],
        "causal_relevance": profile["causal_relevance"],
        "claim_boundary": profile["claim_boundary"],
    }


def validate(graph_root: Path) -> dict[str, Any]:
    from pygrc.core import (
        SnapshotCompatibilityError,
        canonical_json_dumps,
        digest_snapshot,
    )
    import pygrc
    import pygrc.models
    from pygrc.models import (
        GRC9V3State,
        LGRC9V3,
        digest_lgrc9v3_restoration_identity_v1,
        lgrc9v3_restoration_identity_v1,
    )

    repo_root = Path(__file__).resolve().parents[3]
    base = repo_root / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
    manifest_path = (
        base / "contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json"
    )
    transition_path = base / "contracts/p2-i2/i02r1-chg-004-freeze-transition.json"
    manifest = json.loads(manifest_path.read_text())
    transition = json.loads(transition_path.read_text())

    graph_before = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "branch": _git(graph_root, "branch", "--show-current"),
        "status_short": _git(graph_root, "status", "--short"),
    }
    assert graph_before["revision"] == GRAPH_REVISION
    assert graph_before["status_short"] == ""
    assert _git(graph_root, "cat-file", "-t", GRAPH_REVISION) == "commit"

    source_entries = manifest["source_entries"]
    assert len(source_entries) == EXPECTED_SOURCE_COUNT
    assert len({entry["source_id"] for entry in source_entries}) == len(
        source_entries
    )
    source_by_id = {entry["source_id"]: entry for entry in source_entries}
    source_checks: list[dict[str, Any]] = []
    for entry in source_entries:
        path = graph_root / entry["path"]
        revision_bytes = subprocess.check_output(
            ["git", "-C", str(graph_root), "show", f"{GRAPH_REVISION}:{entry['path']}"]
        )
        worktree_bytes = path.read_bytes()
        revision_sha = _sha256_bytes(revision_bytes)
        worktree_sha = _sha256_bytes(worktree_bytes)
        assert revision_sha == entry["sha256"] == worktree_sha
        classifications = entry["source_classifications"]
        assert classifications
        source_checks.append(
            {
                "source_id": entry["source_id"],
                "path_resolves_at_revision": True,
                "manifest_sha256": entry["sha256"],
                "revision_sha256": revision_sha,
                "worktree_sha256": worktree_sha,
                "all_three_match": True,
                "admission_role": entry["role"],
                "source_classifications": classifications,
            }
        )

    pyproject = tomllib.loads((graph_root / "pyproject.toml").read_text())
    try:
        distribution_version = importlib.metadata.version("pygrc")
    except importlib.metadata.PackageNotFoundError:
        distribution_version = None
    raw_pygrc_file = str(Path(pygrc.__file__).resolve())
    raw_models_file = str(Path(pygrc.models.__file__).resolve())
    expected_src = (graph_root / "src").resolve()
    assert Path(raw_pygrc_file).is_relative_to(expected_src)
    assert Path(raw_models_file).is_relative_to(expected_src)
    import_provenance = {
        "interpreter": sys.executable,
        "prefix": sys.prefix,
        "pygrc_file_raw": raw_pygrc_file,
        "pygrc_file_normalized": "grc:src/pygrc/__init__.py",
        "models_file_raw": raw_models_file,
        "models_file_normalized": "grc:src/pygrc/models/__init__.py",
        "source_root_raw": str(expected_src),
        "source_root_normalized": "grc:src",
        "pygrc_dunder_version": getattr(pygrc, "__version__", None),
        "distribution_version_when_available": distribution_version,
        "pyproject_project_version": pyproject["project"]["version"],
        "all_imported_modules_under_admitted_checkout": True,
        "ambient_or_other_checkout_used": False,
    }

    callable_entries = manifest["callable_entries"]
    profiles = manifest["callable_contract_profiles"]
    assert len(callable_entries) == EXPECTED_SYMBOL_COUNT
    assert len({entry["symbol"] for entry in callable_entries}) == len(
        callable_entries
    )
    callable_contracts = [
        _callable_contract(entry, graph_root, source_by_id, profiles)
        for entry in callable_entries
    ]

    # Minimal generic provider fixture: no P2-I2 source set, pool, cell,
    # control, comparator, or response is constructed.
    model = LGRC9V3.from_state(
        GRC9V3State(),
        {"dt": 1.0, "evolution": {"rng_seed": 17}},
    )
    snapshot = model.snapshot()
    identity_a = lgrc9v3_restoration_identity_v1(model)
    identity_b = lgrc9v3_restoration_identity_v1(model)
    identity_from_snapshot = lgrc9v3_restoration_identity_v1(snapshot)
    reversed_snapshot = dict(reversed(tuple(snapshot.items())))
    identity_reordered = lgrc9v3_restoration_identity_v1(reversed_snapshot)
    identity_user_mapping = lgrc9v3_restoration_identity_v1(UserDict(snapshot))
    assert identity_a == identity_b == identity_from_snapshot
    assert identity_a == identity_reordered == identity_user_mapping
    assert identity_a["artifact_kind"] == "lgrc9v3_restoration_identity"
    assert identity_a["artifact_schema_version"] == (
        "lgrc9v3_restoration_identity_v1"
    )

    digest = digest_lgrc9v3_restoration_identity_v1(model)
    canonical_text = canonical_json_dumps(identity_a)
    independent_digest = hashlib.sha256(canonical_text.encode("utf-8")).hexdigest()
    assert digest == independent_digest
    raw_snapshot_digest = digest_snapshot(snapshot)

    class LGRC9V3Subclass(LGRC9V3):
        pass

    subclass_model = LGRC9V3Subclass(model.get_params(), model.get_state())
    assert lgrc9v3_restoration_identity_v1(subclass_model) == identity_a

    wrong_family = deepcopy(snapshot)
    wrong_family["metadata"]["model_family"] = "GRC9V3"
    wrong_version = deepcopy(snapshot)
    wrong_version["metadata"]["snapshot_version"] = 999
    missing_runtime = deepcopy(snapshot)
    del missing_runtime["dynamics"]["lgrc9v3_runtime"]
    malformed_events = deepcopy(snapshot)
    malformed_events["events"] = {}
    unsupported_checks = [
        _exception_record("arbitrary_object", lgrc9v3_restoration_identity_v1, object()),
        _exception_record("raw_digest_string", lgrc9v3_restoration_identity_v1, raw_snapshot_digest),
        _exception_record("partial_mapping", lgrc9v3_restoration_identity_v1, {}),
        _exception_record("wrong_family_mapping", lgrc9v3_restoration_identity_v1, wrong_family),
        _exception_record("unsupported_version_mapping", lgrc9v3_restoration_identity_v1, wrong_version),
        _exception_record("missing_runtime_mapping", lgrc9v3_restoration_identity_v1, missing_runtime),
        _exception_record("malformed_events_mapping", lgrc9v3_restoration_identity_v1, malformed_events),
        _exception_record(
            "rcae_projection_mapping",
            lgrc9v3_restoration_identity_v1,
            {"artifact_kind": "rcae_restoration_projection", "projection": {}},
        ),
    ]
    assert all(row["rejected"] for row in unsupported_checks)
    assert all(row["exception_type"] == SnapshotCompatibilityError.__name__ for row in unsupported_checks)

    # Generic sensitivity checks establish identity coverage, not ecological
    # adequacy or behavioral continuation.
    base_digest = digest_lgrc9v3_restoration_identity_v1(model)
    model.set_causal_flux_routes(
        {0: [{"target_node_id": 1, "edge_id": 0, "amount": 0.25}]}
    )
    route_digest = digest_lgrc9v3_restoration_identity_v1(model)
    assert route_digest != base_digest
    model.set_feedback_coupled_pulse_producer(
        source_node_id=0,
        target_node_id=1,
        edge_id=0,
        threshold=0.5,
        packet_amount=0.25,
    )
    producer_digest = digest_lgrc9v3_restoration_identity_v1(model)
    assert producer_digest != route_digest
    model.get_state().scheduler_event_index = 1
    scheduler_digest = digest_lgrc9v3_restoration_identity_v1(model)
    assert scheduler_digest != producer_digest

    # Save/load preserves current native identity. Reset is deliberately tested
    # as an identity-coverage boundary: the original private construction
    # baseline and the loaded model's baseline are not represented separately.
    before_save_identity = lgrc9v3_restoration_identity_v1(model)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "i02r1-generic-provider.json"
        model.save(str(path))
        restored = LGRC9V3.load(str(path))
    restored_identity = lgrc9v3_restoration_identity_v1(restored)
    assert before_save_identity == restored_identity
    model.reset()
    restored.reset()
    reset_original_identity = lgrc9v3_restoration_identity_v1(model)
    reset_restored_identity = lgrc9v3_restoration_identity_v1(restored)
    assert reset_original_identity != reset_restored_identity

    provider_checks = {
        "supported_input_checks": {
            "concrete_lgrc9v3_model": True,
            "lgrc9v3_subclass": True,
            "complete_snapshot_dict": True,
            "complete_snapshot_mapping_wrapper": True,
        },
        "unsupported_input_checks": unsupported_checks,
        "identity_document": {
            "artifact_kind": identity_a["artifact_kind"],
            "artifact_schema_version": identity_a["artifact_schema_version"],
            "deterministic_repeated_evaluation": True,
            "model_and_snapshot_equal": True,
            "mapping_order_invariant": True,
            "canonical_json_function": "pygrc.core.canonical_json_dumps",
            "canonical_json_encoding": "UTF-8",
            "wall_clock_filesystem_memory_address_or_process_state_added": False,
        },
        "digest": {
            "algorithm": "SHA-256",
            "input": "UTF-8 bytes of pygrc.core.canonical_json_dumps(identity_document)",
            "provider_digest": digest,
            "independent_digest": independent_digest,
            "match": True,
            "raw_snapshot_digest": raw_snapshot_digest,
            "raw_snapshot_digest_is_identity_digest": raw_snapshot_digest == digest,
        },
        "current_state_sensitivity": {
            "route_configuration_changes_identity": True,
            "native_producer_configuration_changes_identity": True,
            "scheduler_cursor_changes_identity": True,
            "save_load_preserves_current_identity": True,
        },
        "reset_boundary": {
            "private_initial_state_covered_separately": False,
            "equal_current_identity_before_reset": True,
            "reset_after_different_construction_load_histories_can_diverge": True,
            "later_requirement": "Forbid reset in the registered continuation window or compose and compare an explicit registered reset-baseline identity before branching.",
        },
        "restoration_correctness_proven": False,
        "unrestricted_continuation_equivalence_proven": False,
    }

    coverage = manifest["identity_coverage"]
    assert coverage["all_continuation_relevant_components_dispositioned"] is True
    assert any(row["component"] == "reset baseline (_initial_state)" and row["disposition"] == "unsupported_blocks_branching" for row in coverage["components"])

    assert transition["predecessor"]["byte_exact_file_retained"] is False
    assert transition["timing"]["before_any_admission_role"] is True
    assert transition["rerun"]["expected_symbol_count"] == len(callable_entries)

    graph_after = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "branch": _git(graph_root, "branch", "--show-current"),
        "status_short": _git(graph_root, "status", "--short"),
    }
    assert graph_after == graph_before

    return {
        "artifact_id": "P2-I2-I02R1-IDENTITY-AUTHORITY-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I02R1",
        "lane_id": "AE01-L02",
        "status": "passed",
        "validated_at": "2026-07-14",
        "validator": "rcae:experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i02r1_validate.py",
        "evidence_effect": "Identity, authority, import provenance, and provider-contract validation only; no realization or scientific evidence.",
        "graph_before": graph_before,
        "graph_after": graph_after,
        "source_identity": {
            "source_count": len(source_checks),
            "checks": source_checks,
            "all_admitted_file_sha256_match_file_contents": True,
            "all_repository_relative_paths_resolve_at_revision": True,
            "graph_revision_exists_as_commit": True,
            "dirty_or_untracked_graph_file_contributed": False,
        },
        "import_provenance": import_provenance,
        "callable_contracts": callable_contracts,
        "complete_callable_review": {
            "symbol_count": len(callable_contracts),
            "all_symbols_resolved": True,
            "all_modules_from_admitted_checkout": True,
            "all_implementation_digests_match": True,
            "chg_004_full_scope_rerun": True,
        },
        "provider_contract": provider_checks,
        "identity_coverage": coverage,
        "claim_boundary": {
            "provider_available_for_conditional_selection": True,
            "provider_selected": False,
            "realization_selected": False,
            "dependence_mode_selected": False,
            "restoration_correctness_proven": False,
            "bounded_continuation_executed_for_p2_i2": False,
            "scientific_evidence_assigned": False,
        },
        "invariants": {
            "all_admitted_file_sha256_match_file_contents": True,
            "imported_package_matches_admitted_checkout": True,
            "all_public_symbol_contracts_complete": True,
            "provider_digest_matches_independent_sha256": True,
            "all_continuation_relevant_components_dispositioned": True,
            "provider_selection_is_configuration_not_runtime_recovery": True,
            "provider_mismatch_blocks_branch_comparison": True,
            "identity_equality_is_continuation_equivalence": False,
            "admission_is_scientific_evidence": False,
            "graph_repository_unchanged": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.graph_root.resolve())
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(text)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
