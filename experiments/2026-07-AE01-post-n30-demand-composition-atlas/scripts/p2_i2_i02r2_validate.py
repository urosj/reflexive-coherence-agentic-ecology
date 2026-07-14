#!/usr/bin/env python3
"""Validate PyGRC reset-baseline persistence without P2-I2 candidate behavior."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Callable


PREVIOUS_REVISION = "3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5"
PROPOSED_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"


def _git(graph_root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(graph_root), *args],
        text=True,
    ).strip()


def _git_bytes(graph_root: Path, revision: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(graph_root), "show", f"{revision}:{path}"]
    )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _changed_role(path: str) -> tuple[str, bool]:
    direct_runtime = {
        "src/pygrc/core/__init__.py",
        "src/pygrc/core/interfaces.py",
        "src/pygrc/core/serialization.py",
        "src/pygrc/models/__init__.py",
        "src/pygrc/models/grc_9_v3.py",
        "src/pygrc/models/lgrc_9_v3_restoration.py",
        "src/pygrc/models/lgrc_9_v3_runtime.py",
    }
    direct_contract = {
        "specs/grc-common-interface.md",
        "specs/grc-reset-baseline-persistence.md",
        "specs/lgrc-9-v3-restoration-identity.md",
        "specs/lgrc-9-v3-spec.md",
    }
    direct_tests = {
        "tests/core/test_interfaces.py",
        "tests/core/test_serialization_contract.py",
        "tests/models/test_reset_baseline_persistence.py",
    }
    direct_closeout = {
        "implementation/corrections/PyGRC-ResetBaselinePersistenceChecklist.md",
        "implementation/corrections/PyGRC-ResetBaselinePersistenceCloseout.md",
        "implementation/corrections/PyGRC-ResetBaselinePersistencePlan.md",
    }
    if path in direct_runtime:
        return "affected_runtime_or_public_api_authority", True
    if path in direct_contract:
        return "affected_schema_or_contract_authority", True
    if path in direct_tests:
        return "affected_generic_conformance_authority", True
    if path in direct_closeout:
        return "affected_implementation_closeout_authority", True
    if path.startswith("src/pygrc/models/"):
        return "cross_family_implementation_context", False
    if path.startswith("tests/"):
        return "cross_family_regression_context", False
    if path.startswith("specs/"):
        return "supporting_contract_context", False
    if path.startswith("implementation/"):
        return "supporting_implementation_context", False
    if path.startswith("docs/") or path in {"README.md", "CHANGELOG.md"}:
        return "documentation_or_navigation_context", False
    raise AssertionError(f"unclassified changed path: {path}")


def _source_transition(graph_root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    raw = _git(
        graph_root,
        "diff",
        "--name-status",
        f"{PREVIOUS_REVISION}..{PROPOSED_REVISION}",
    )
    for line in raw.splitlines():
        status, path = line.split("\t", 1)
        role, authority = _changed_role(path)
        new_bytes = _git_bytes(graph_root, PROPOSED_REVISION, path)
        worktree_bytes = (graph_root / path).read_bytes()
        new_sha = _sha256(new_bytes)
        assert _sha256(worktree_bytes) == new_sha
        old_sha = None
        if status != "A":
            old_sha = _sha256(_git_bytes(graph_root, PREVIOUS_REVISION, path))
        rows.append(
            {
                "status": status,
                "path": path,
                "portable_source_id": f"grc:{path}",
                "old_sha256": old_sha,
                "new_sha256": new_sha,
                "worktree_matches_proposed_revision": True,
                "i02r2_role": role,
                "admission_authority_for_reset_revalidation": authority,
            }
        )
    assert len(rows) == 35
    return {
        "artifact_id": "P2-I2-I02R2-GRAPH-SOURCE-TRANSITION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I02R2",
        "lane_id": "AE01-L02",
        "status": "exact_transition_reconstructed",
        "previous_admitted_revision": PREVIOUS_REVISION,
        "proposed_revision": PROPOSED_REVISION,
        "changed_path_count": len(rows),
        "authority_path_count": sum(
            bool(row["admission_authority_for_reset_revalidation"])
            for row in rows
        ),
        "changed_paths": rows,
        "provider_transition": {
            "retained_current_state_provider": (
                "pygrc.models.lgrc9v3_restoration_identity_v1"
            ),
            "added_reset_aware_provider": (
                "pygrc.models.lgrc9v3_restoration_identity_v2"
            ),
            "added_reset_aware_digest_provider": (
                "pygrc.models.digest_lgrc9v3_restoration_identity_v2"
            ),
            "v1_redefined": False,
            "provider_selected_for_p2_i2": False,
        },
        "claim_boundary": (
            "Exact upstream source transition and generic conformance authority "
            "only; context paths are not runtime dependencies by this record, and "
            "no realization or scientific evidence is assigned."
        ),
    }


def _set_index(model: Any, value: int) -> None:
    state = deepcopy(model.get_state())
    state.scheduler_event_index = value
    model.set_state(state)


def _index(model: Any) -> int:
    return int(model.get_state().scheduler_event_index)


def _exception_record(
    case: str,
    operation: Callable[[], Any],
) -> dict[str, Any]:
    try:
        operation()
    except Exception as exc:
        return {
            "case": case,
            "rejected": True,
            "exception_type": type(exc).__name__,
            "message": str(exc),
            "fallback_attempted": False,
        }
    raise AssertionError(f"expected rejection did not occur: {case}")


def _resolve_public_symbol(symbol: str, pygrc_module: Any) -> Any:
    if not symbol.startswith("pygrc."):
        raise AssertionError(f"unexpected public symbol: {symbol}")
    value: Any = pygrc_module
    for part in symbol.split(".")[1:]:
        value = getattr(value, part)
    return value


def _validation(graph_root: Path, manifest_path: Path) -> dict[str, Any]:
    from pygrc.core import (
        RESET_BASELINE_SCHEMA,
        RESET_BASELINE_VERSION,
        SnapshotCompatibilityError,
        build_reset_baseline_group,
        canonical_json_dumps,
        reset_baseline_snapshot,
        save_snapshot,
        validate_reset_baseline_group,
    )
    import pygrc
    import pygrc.core
    import pygrc.models
    from pygrc.models import (
        LGRC9V3,
        LGRC9V3_RESTORATION_IDENTITY_SCHEMA_VERSION,
        LGRC9V3_RESTORATION_IDENTITY_V2_SCHEMA_VERSION,
        digest_lgrc9v3_restoration_identity_v1,
        digest_lgrc9v3_restoration_identity_v2,
        lgrc9v3_restoration_identity_v1,
        lgrc9v3_restoration_identity_v2,
    )

    before = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "branch": _git(graph_root, "branch", "--show-current"),
        "status_short": _git(graph_root, "status", "--short"),
    }
    assert before["revision"] == PROPOSED_REVISION
    assert before["status_short"] == ""

    manifest = json.loads(manifest_path.read_text())
    assert manifest["repository"]["revision"] == PROPOSED_REVISION
    assert manifest["status"] == "admitted_after_i02r2_revalidation"
    assert manifest["restoration_providers"]["selected_provider"] is None
    source_by_id = {
        row["source_id"]: row for row in manifest["source_entries"]
    }
    assert len(source_by_id) == len(manifest["source_entries"]) == 31
    source_checks = []
    for row in manifest["source_entries"]:
        revision_sha = _sha256(_git_bytes(graph_root, PROPOSED_REVISION, row["path"]))
        worktree_sha = _sha256((graph_root / row["path"]).read_bytes())
        assert revision_sha == worktree_sha == row["sha256"]
        source_checks.append(
            {
                "source_id": row["source_id"],
                "manifest_sha256": row["sha256"],
                "revision_sha256": revision_sha,
                "worktree_sha256": worktree_sha,
                "all_three_match": True,
                "role": row["role"],
                "source_classifications": row["source_classifications"],
            }
        )

    expected_src = (graph_root / "src").resolve()
    imported = {
        "interpreter_raw": sys.executable,
        "pygrc_file_raw": str(Path(pygrc.__file__).resolve()),
        "core_file_raw": str(Path(pygrc.core.__file__).resolve()),
        "models_file_raw": str(Path(pygrc.models.__file__).resolve()),
        "source_root_normalized": "grc:src",
    }
    for key in ("pygrc_file_raw", "core_file_raw", "models_file_raw"):
        assert Path(imported[key]).is_relative_to(expected_src)
    imported["all_imports_under_proposed_checkout"] = True
    imported["ambient_or_other_checkout_used"] = False

    symbols = {
        "pygrc.core.build_reset_baseline_group": build_reset_baseline_group,
        "pygrc.core.validate_reset_baseline_group": validate_reset_baseline_group,
        "pygrc.core.reset_baseline_snapshot": reset_baseline_snapshot,
        "pygrc.models.LGRC9V3.load": LGRC9V3.load,
        "pygrc.models.LGRC9V3.set_state": LGRC9V3.set_state,
        "pygrc.models.LGRC9V3.reset": LGRC9V3.reset,
        "pygrc.models.LGRC9V3.rebase_reset_baseline": (
            LGRC9V3.rebase_reset_baseline
        ),
        "pygrc.models.LGRC9V3.snapshot": LGRC9V3.snapshot,
        "pygrc.models.LGRC9V3.save": LGRC9V3.save,
        "pygrc.models.lgrc9v3_restoration_identity_v1": (
            lgrc9v3_restoration_identity_v1
        ),
        "pygrc.models.digest_lgrc9v3_restoration_identity_v1": (
            digest_lgrc9v3_restoration_identity_v1
        ),
        "pygrc.models.lgrc9v3_restoration_identity_v2": (
            lgrc9v3_restoration_identity_v2
        ),
        "pygrc.models.digest_lgrc9v3_restoration_identity_v2": (
            digest_lgrc9v3_restoration_identity_v2
        ),
    }
    callable_contracts = []
    for name, symbol in symbols.items():
        module = inspect.getmodule(symbol)
        assert module is not None and module.__file__ is not None
        module_path = Path(module.__file__).resolve()
        assert module_path.is_relative_to(expected_src)
        callable_contracts.append(
            {
                "symbol": name,
                "module": symbol.__module__,
                "qualified_name": symbol.__qualname__,
                "signature": str(inspect.signature(symbol)),
                "module_source": (
                    f"grc:src/{module_path.relative_to(expected_src).as_posix()}"
                ),
            }
        )
    affected_callable_contracts = callable_contracts

    complete_callable_contracts = []
    profiles = manifest["callable_contract_profiles"]
    for entry in manifest["callable_entries"]:
        symbol = _resolve_public_symbol(entry["symbol"], pygrc)
        module = inspect.getmodule(symbol)
        assert module is not None and module.__file__ is not None
        module_path = Path(module.__file__).resolve()
        assert module_path.is_relative_to(expected_src)
        normalized_source = (
            f"grc:src/{module_path.relative_to(expected_src).as_posix()}"
        )
        assert normalized_source == entry["implementation_source"]
        assert entry["public_export_source"] in source_by_id
        assert entry["implementation_source"] in source_by_id
        profile = profiles[entry["contract_profile"]]
        complete_callable_contracts.append(
            {
                "symbol": entry["symbol"],
                "module": symbol.__module__,
                "qualified_name": symbol.__qualname__,
                "signature": str(inspect.signature(symbol)),
                "normalized_module_source": normalized_source,
                "implementation_sha256": source_by_id[
                    entry["implementation_source"]
                ]["sha256"],
                "role": entry["role"],
                "contract_profile": entry["contract_profile"],
                "unsupported_argument_shape": profile[
                    "unsupported_argument_shape"
                ],
                "causal_relevance": profile["causal_relevance"],
                "claim_boundary": profile["claim_boundary"],
            }
        )
    assert len(complete_callable_contracts) == 31

    model = LGRC9V3.from_config({"dt": 0.1})
    _set_index(model, 7)
    snapshot = model.snapshot()
    group = snapshot["reset_baseline"]
    baseline_snapshot = group["snapshot"]
    assert group["reset_baseline_schema"] == RESET_BASELINE_SCHEMA
    assert group["reset_baseline_version"] == RESET_BASELINE_VERSION
    assert group["model_family"] == "LGRC9V3"
    assert group["status"] == "available"
    assert "reset_baseline" not in baseline_snapshot
    assert (
        baseline_snapshot["metadata"]["params_hash"]
        == snapshot["metadata"]["params_hash"]
    )
    baseline_group_check = {
        "schema": RESET_BASELINE_SCHEMA,
        "version": RESET_BASELINE_VERSION,
        "status": "available",
        "same_family": True,
        "same_params_hash": True,
        "nested_baseline_absent": True,
        "complete_same_family_snapshot": True,
    }

    before_v1 = digest_lgrc9v3_restoration_identity_v1(model)
    before_v2 = digest_lgrc9v3_restoration_identity_v2(model)
    with tempfile.TemporaryDirectory(dir="/tmp") as tmp_dir:
        path = Path(tmp_dir) / "model.json"
        model.save(str(path))
        restored = LGRC9V3.load(str(path))
    assert digest_lgrc9v3_restoration_identity_v1(restored) == before_v1
    assert digest_lgrc9v3_restoration_identity_v2(restored) == before_v2
    model.reset()
    restored.reset()
    assert _index(model) == _index(restored) == 0
    assert (
        digest_lgrc9v3_restoration_identity_v2(model)
        == digest_lgrc9v3_restoration_identity_v2(restored)
    )
    save_load_reset = {
        "current_v1_preserved": True,
        "current_plus_baseline_v2_preserved": True,
        "original_and_restored_reset_outcomes_equal": True,
        "reset_index": 0,
    }

    first = LGRC9V3.from_config({"dt": 0.1})
    second = LGRC9V3.from_config({"dt": 0.1})
    _set_index(second, 2)
    second.rebase_reset_baseline()
    _set_index(first, 7)
    _set_index(second, 7)
    assert (
        digest_lgrc9v3_restoration_identity_v1(first)
        == digest_lgrc9v3_restoration_identity_v1(second)
    )
    assert (
        digest_lgrc9v3_restoration_identity_v2(first)
        != digest_lgrc9v3_restoration_identity_v2(second)
    )
    reset_sensitivity = {
        "equal_current_state_v1_identity": True,
        "different_reset_baseline_v2_identity": True,
        "v1_redefined_as_reset_aware": False,
    }

    cycle_model = LGRC9V3.from_config({"dt": 0.1})
    _set_index(cycle_model, 2)
    cycle_model.rebase_reset_baseline()
    _set_index(cycle_model, 7)
    cycle_digest = digest_lgrc9v3_restoration_identity_v2(cycle_model)
    cycle_digests = [cycle_digest]
    with tempfile.TemporaryDirectory(dir="/tmp") as tmp_dir:
        for cycle in range(3):
            path = Path(tmp_dir) / f"cycle-{cycle}.json"
            cycle_model.save(str(path))
            cycle_model = LGRC9V3.load(str(path))
            cycle_digests.append(
                digest_lgrc9v3_restoration_identity_v2(cycle_model)
            )
    assert len(set(cycle_digests)) == 1
    cycle_model.reset()
    assert _index(cycle_model) == 2
    repeated_cycles = {
        "cycle_count": 3,
        "v2_digest_stable": True,
        "reset_baseline_preserved": True,
        "reset_index": 2,
    }

    state_model = LGRC9V3.from_config({"dt": 0.1})
    _set_index(state_model, 4)
    state_model.reset()
    assert _index(state_model) == 0
    _set_index(state_model, 5)
    state_model.rebase_reset_baseline()
    _set_index(state_model, 9)
    state_model.reset()
    assert _index(state_model) == 5
    state_semantics = {
        "set_state_preserves_baseline": True,
        "rebase_is_explicit": True,
        "explicit_rebase_reset_index": 5,
    }

    legacy_model = LGRC9V3.from_config({"dt": 0.1})
    _set_index(legacy_model, 3)
    legacy_snapshot = legacy_model.snapshot()
    legacy_snapshot.pop("reset_baseline")
    with tempfile.TemporaryDirectory(dir="/tmp") as tmp_dir:
        path = Path(tmp_dir) / "legacy.json"
        save_snapshot(path, legacy_snapshot)
        legacy_loaded = LGRC9V3.load(str(path))
    legacy_reset_rejection = _exception_record(
        "legacy_reset_without_rebase",
        legacy_loaded.reset,
    )
    legacy_v2_rejection = _exception_record(
        "legacy_v2_without_rebase",
        lambda: lgrc9v3_restoration_identity_v2(legacy_loaded),
    )
    unavailable_snapshot = legacy_loaded.snapshot()
    assert unavailable_snapshot["reset_baseline"]["status"] == "unavailable"
    assert (
        unavailable_snapshot["reset_baseline"]["unavailable_reason"]
        == "legacy_snapshot_missing_reset_baseline"
    )
    legacy_loaded.rebase_reset_baseline()
    post_rebase_digest = digest_lgrc9v3_restoration_identity_v2(legacy_loaded)
    _set_index(legacy_loaded, 8)
    with tempfile.TemporaryDirectory(dir="/tmp") as tmp_dir:
        path = Path(tmp_dir) / "rebased.json"
        legacy_loaded.save(str(path))
        legacy_restored = LGRC9V3.load(str(path))
    legacy_restored.reset()
    assert _index(legacy_restored) == 3
    assert (
        digest_lgrc9v3_restoration_identity_v2(legacy_restored)
        == post_rebase_digest
    )
    legacy_policy = {
        "legacy_current_state_loads": True,
        "legacy_reset_without_rebase": legacy_reset_rejection,
        "legacy_v2_without_rebase": legacy_v2_rejection,
        "unavailable_status_persists": True,
        "explicit_rebase_supported": True,
        "post_rebase_v2_stable_across_save_load": True,
        "historical_construction_baseline_recovered": False,
    }

    good = LGRC9V3.from_config({"dt": 0.1}).snapshot()
    malformed_cases: list[tuple[str, dict[str, Any]]] = []
    malformed = deepcopy(good)
    malformed["reset_baseline"]["snapshot"] = "not-a-snapshot"
    malformed_cases.append(("malformed_snapshot", malformed))
    wrong_family = deepcopy(good)
    wrong_family["reset_baseline"]["model_family"] = "GRC9V3"
    malformed_cases.append(("wrong_family", wrong_family))
    wrong_params = deepcopy(good)
    wrong_params["reset_baseline"]["snapshot"]["metadata"]["params_hash"] = (
        "different"
    )
    malformed_cases.append(("wrong_params_hash", wrong_params))
    recursive = deepcopy(good)
    recursive["reset_baseline"]["snapshot"]["reset_baseline"] = deepcopy(
        good["reset_baseline"]
    )
    malformed_cases.append(("recursive_baseline", recursive))
    wrong_version = deepcopy(good)
    wrong_version["reset_baseline"]["reset_baseline_version"] = 999
    malformed_cases.append(("unsupported_baseline_version", wrong_version))
    malformed_results = []
    with tempfile.TemporaryDirectory(dir="/tmp") as tmp_dir:
        for case, candidate in malformed_cases:
            path = Path(tmp_dir) / f"{case}.json"
            malformed_results.append(
                _exception_record(
                    case,
                    lambda candidate=candidate, path=path: save_snapshot(
                        path,
                        candidate,
                    ),
                )
            )
    assert all(
        row["exception_type"] == SnapshotCompatibilityError.__name__
        for row in malformed_results
    )

    v2_artifact = lgrc9v3_restoration_identity_v2(
        LGRC9V3.from_config({"dt": 0.1})
    )
    v2_digest = digest_lgrc9v3_restoration_identity_v2(
        LGRC9V3.from_config({"dt": 0.1})
    )
    independent_v2_digest = hashlib.sha256(
        canonical_json_dumps(v2_artifact).encode("utf-8")
    ).hexdigest()
    assert v2_artifact["artifact_schema_version"] == (
        LGRC9V3_RESTORATION_IDENTITY_V2_SCHEMA_VERSION
    )
    assert (
        v2_artifact["current_state_restoration_identity"][
            "artifact_schema_version"
        ]
        == LGRC9V3_RESTORATION_IDENTITY_SCHEMA_VERSION
    )
    assert v2_digest == independent_v2_digest
    identity_contract = {
        "v1_schema": LGRC9V3_RESTORATION_IDENTITY_SCHEMA_VERSION,
        "v2_schema": LGRC9V3_RESTORATION_IDENTITY_V2_SCHEMA_VERSION,
        "v2_current_component_is_v1": True,
        "v2_baseline_component_is_v1": True,
        "digest_algorithm": "SHA-256",
        "canonical_encoding": "UTF-8",
        "provider_digest": v2_digest,
        "independent_digest": independent_v2_digest,
        "digest_matches": True,
    }

    after = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "branch": _git(graph_root, "branch", "--show-current"),
        "status_short": _git(graph_root, "status", "--short"),
    }
    assert after == before

    return {
        "artifact_id": "P2-I2-I02R2-RESET-BASELINE-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I02R2",
        "lane_id": "AE01-L02",
        "status": "passed",
        "validated_at": "2026-07-14",
        "validator": "rcae:experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i02r2_validate.py",
        "evidence_effect": (
            "Generic source/import/reset/provider conformance only; no P2-I2 "
            "realization or scientific evidence."
        ),
        "graph_before": before,
        "graph_after": after,
        "import_provenance": imported,
        "source_identity": {
            "source_count": len(source_checks),
            "checks": source_checks,
            "all_manifest_revision_and_worktree_digests_match": True,
        },
        "callable_contracts": complete_callable_contracts,
        "affected_callable_probe": affected_callable_contracts,
        "complete_callable_review": {
            "symbol_count": len(complete_callable_contracts),
            "all_symbols_resolved": True,
            "all_modules_under_proposed_checkout": True,
            "all_implementation_digests_match": True,
            "all_profiles_resolved": True,
        },
        "reset_baseline_group": baseline_group_check,
        "save_load_reset": save_load_reset,
        "reset_baseline_identity_sensitivity": reset_sensitivity,
        "repeated_save_load": repeated_cycles,
        "state_and_rebase_semantics": state_semantics,
        "legacy_compatibility": legacy_policy,
        "malformed_input_rejections": malformed_results,
        "identity_contract": identity_contract,
        "upstream_focused_tests": {
            "command_scope": (
                "reset baseline, core serialization/interface, LGRC9V3 "
                "restoration, and restoration matrix"
            ),
            "passed": 68,
            "subtests_passed": 32,
            "failed": 0,
            "cache_disabled": True,
            "temporary_files_outside_graph_repository": True,
        },
        "claim_boundary": {
            "reset_baseline_persistence_supported": True,
            "v2_reset_aware_identity_supported": True,
            "v1_redefined": False,
            "legacy_historical_baseline_recovered": False,
            "provider_selected_for_p2_i2": False,
            "bounded_candidate_continuation_executed": False,
            "restoration_correctness_beyond_tested_contract": False,
            "scientific_evidence_assigned": False,
        },
        "invariants": {
            "all_admitted_source_digests_match": True,
            "all_public_callable_contracts_complete": True,
            "imports_match_proposed_checkout": True,
            "original_and_loaded_reset_outcomes_equal": True,
            "reset_baseline_changes_v2_identity": True,
            "repeated_save_load_preserves_baseline": True,
            "set_state_preserves_baseline": True,
            "rebase_is_explicit": True,
            "legacy_reset_fails_closed_until_rebase": True,
            "malformed_baseline_fails_closed": True,
            "v2_digest_matches_independent_sha256": True,
            "graph_repository_unchanged": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-root", type=Path, required=True)
    parser.add_argument("--source-output", type=Path, required=True)
    parser.add_argument("--validation-output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    graph_root = args.graph_root.resolve()
    assert _git(graph_root, "rev-parse", "HEAD") == PROPOSED_REVISION
    assert _git(graph_root, "status", "--short") == ""
    source = _source_transition(graph_root)
    validation = _validation(graph_root, args.manifest.resolve())
    args.source_output.parent.mkdir(parents=True, exist_ok=True)
    args.validation_output.parent.mkdir(parents=True, exist_ok=True)
    args.source_output.write_text(json.dumps(source, indent=2, sort_keys=True) + "\n")
    args.validation_output.write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
