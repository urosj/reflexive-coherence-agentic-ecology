#!/usr/bin/env python3
"""Construct the P2-I3 B-R inactive execution freeze without candidate work.

The retained build is deliberately available only from a clean committed RCAE
tree.  Public PyGRC objects are imported and inspected, never invoked.  Dirty
trees may emit explicitly retention-ineligible preview records outside retained
contract paths.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import importlib
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Mapping, Sequence

import jsonschema

from p2_i3_br_execution_runtime import (
    CALL_SITE_REGISTRY,
    FORBIDDEN_SYMBOLS,
    LIVE_OPERATION_SYMBOLS,
    POLICY_REL,
    REGISTRATION_REL,
    ROOT,
    SCHEMA_REL,
    build_entry_rows,
    build_expected_terminal_set,
    canonical_bytes,
    identity,
    load_json,
    payload_digest,
    portable_path,
    require,
    sha256_file,
    validate_policy_command_environments,
    verify_digest,
    with_digest,
    write_exclusive_json,
)


SCRIPT_REL = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i07_br_freeze.py")
VALIDATOR_REL = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i07_br_validate.py")
EXPECTED_GRAPH_REVISION = "565706f8b7647f6b7638b9afbe52372e170bf724"


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=False
    )
    require(completed.returncode == 0, f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


def clean_source(root: Path) -> tuple[str, bool, list[str]]:
    head = git(root, "rev-parse", "HEAD")
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return head, not status, status


def resolve_public_symbol(symbol: str) -> Any:
    parts = symbol.split(".")
    require(parts[0] == "pygrc" and len(parts) >= 3, f"unregistered public namespace: {symbol}")
    value: Any = importlib.import_module("pygrc")
    for part in parts[1:]:
        value = getattr(value, part)
    return value


def source_owner(value: Any, graph_root: Path) -> tuple[str, str]:
    raw = inspect.getsourcefile(value) or inspect.getfile(value)
    path = Path(raw).resolve()
    source_root = (graph_root / "src").resolve()
    require(path.is_relative_to(source_root), f"public symbol owner outside admitted graph source: {path.name}")
    relative = path.relative_to(graph_root.resolve()).as_posix()
    return relative, sha256_file(path)


def normalized_signature(value: Any) -> str:
    try:
        return str(inspect.signature(value))
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"public signature unavailable: {value!r}") from exc


def path_projection(graph_root: Path) -> list[str]:
    graph_source = (graph_root / "src").resolve()
    repo = ROOT.resolve()
    venv = (ROOT / ".venv").resolve()
    projection: list[str] = []
    for raw in sys.path:
        if not raw:
            role = "rcae_repository_root"
        else:
            path = Path(raw).resolve()
            if path == graph_source:
                role = "graph_source_root"
            elif path == repo or path.is_relative_to(repo / "experiments"):
                role = "rcae_source_root"
            elif path.is_relative_to(venv):
                role = "rcae_venv_site_or_runtime"
            elif (
                ("python3.12" in path.parts or path.name.startswith("python312.zip"))
                and ("lib" in path.parts or "lib-dynload" in path.parts)
            ):
                role = "python_standard_library"
            else:
                role = "unregistered_path"
        projection.append(role)
    require("graph_source_root" in projection, "exact graph source root absent from sys.path")
    require("unregistered_path" not in projection, f"ambient sys.path entry detected: {projection}")
    return projection


def inspect_runtime(graph_root: Path, i03: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    require(git(graph_root, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION, "graph revision mismatch")
    require(not git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"), "graph worktree is dirty")
    graph_source = (graph_root / "src").resolve()
    imported = importlib.import_module("pygrc")
    require(Path(imported.__file__).resolve() == graph_source / "pygrc" / "__init__.py", "PyGRC did not import from exact source root")

    authority_symbols = tuple(row["symbol"] for row in i03["required_public_calls"])
    require(authority_symbols == LIVE_OPERATION_SYMBOLS, "I03 public-call order or closure drifted")
    require(tuple(row["symbol"] for row in i03["blocked_public_calls"]) == FORBIDDEN_SYMBOLS, "I03 forbidden-call closure drifted")
    require(set(CALL_SITE_REGISTRY) == set(LIVE_OPERATION_SYMBOLS), "call-site registry is not closed")

    rows: list[dict[str, Any]] = []
    allowed_by_symbol = {row["symbol"]: row for row in i03["required_public_calls"]}
    for symbol in LIVE_OPERATION_SYMBOLS:
        value = resolve_public_symbol(symbol)
        require(callable(value), f"public API entry is not callable: {symbol}")
        owner, owner_digest = source_owner(value, graph_root)
        rows.append(
            {
                "symbol": symbol,
                "module": getattr(value, "__module__", ""),
                "public_name": getattr(value, "__qualname__", getattr(value, "__name__", "")),
                "signature": normalized_signature(value),
                "owning_source": owner,
                "owning_source_sha256": owner_digest,
                "registered_call_sites": CALL_SITE_REGISTRY[symbol],
                "operation_class": allowed_by_symbol[symbol]["operation_class"],
                "allowed_role": allowed_by_symbol[symbol]["allowed_use"],
                "private": any(part.startswith("_") for part in symbol.split(".")),
                "dynamic_runtime_lookup_allowed": False,
            }
        )
    require(not any(row["private"] for row in rows), "private PyGRC entry entered closure")

    versions = {
        package: importlib.metadata.version(package)
        for package in policy["environment"]["required_packages"]
    }
    require(versions == policy["environment"]["required_packages"], "required package versions drifted")
    require(platform.python_version() == policy["environment"]["python_version"], "Python version drifted")
    require(platform.python_implementation() == policy["environment"]["python_implementation"], "Python implementation drifted")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository-local .venv is not active")
    for key, expected in policy["environment"]["required_environment"].items():
        require(os.environ.get(key) == expected, f"required environment mismatch: {key}")
    require("PYTHONHOME" not in os.environ, "PYTHONHOME must be absent")
    graph_root_value = os.environ.get(policy["environment"]["graph_root_environment_variable"])
    require(bool(graph_root_value), "RCAE_PYGRC_ROOT is required")
    require(Path(str(graph_root_value)).resolve() == graph_root, "RCAE_PYGRC_ROOT target drifted")
    expected_pythonpath = policy["environment"]["normalized_pythonpath"].replace(
        "${RCAE_PYGRC_ROOT}", str(graph_root_value)
    )
    require(os.environ.get("PYTHONPATH") == expected_pythonpath, "normalized PYTHONPATH mismatch")

    admitted_sources = []
    for source in i03["bound_graph_sources"]:
        path = graph_root / source["path"]
        require(path.is_file() and sha256_file(path) == source["sha256"], f"admitted graph source drift: {source['path']}")
        admitted_sources.append(deepcopy(source))
    return {
        "artifact_id": "P2-I3-BR-I07-RUNTIME-BINDING",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I3-I07",
        "branch_id": "P2-I3-BR",
        "source_anchor": git(ROOT, "rev-parse", "HEAD"),
        "graph": {
            "repository_id": "graph-reflexive-coherence",
            "revision": EXPECTED_GRAPH_REVISION,
            "worktree_clean": True,
            "retained_root": "${RCAE_PYGRC_ROOT}",
            "machine_local_path_retained": False,
            "pygrc_import": "${RCAE_PYGRC_ROOT}/src/pygrc/__init__.py",
            "admitted_sources": admitted_sources,
        },
        "environment": {
            "interpreter": ".venv/bin/python",
            "interpreter_target_retained": False,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "packages": versions,
            "required_environment": deepcopy(policy["environment"]["required_environment"]),
            "normalized_pythonpath": policy["environment"]["normalized_pythonpath"],
            "pythonhome": policy["environment"]["pythonhome"],
            "sys_path_role_projection": path_projection(graph_root),
            "usersite_enabled": False,
            "network_allowed": False,
        },
        "public_api": rows,
        "public_api_count": len(rows),
        "forbidden_runtime_paths": list(FORBIDDEN_SYMBOLS),
        "inspection_activity": {
            "module_imports": ["pygrc"],
            "public_symbols_resolved": len(rows),
            "signature_inspections": len(rows),
            "public_symbol_invocations": 0,
            "model_constructions": 0,
            "packet_operations": 0,
            "event_operations": 0,
            "save_load_reset_operations": 0,
            "candidate_or_control_operations": 0,
        },
    }


def validate_predecessors(policy: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    authority = policy["authority"]
    package = authority["i06_package"]
    i03 = load_json(ROOT / authority["i03_public_call_authority"])
    i05 = load_json(ROOT / authority["i05_calibration_acceptance"])
    registration = load_json(ROOT / authority["i06_registration"])
    i06_validation = load_json(ROOT / authority["i06_registration_validation"])
    reg_gate = load_json(ROOT / authority["i06_reg_gate"])
    verify_digest(registration)
    verify_digest(i06_validation)
    require(
        sha256_file(ROOT / authority["i06_registration"])
        == package["registration_sha256"],
        "accepted I06A registration bytes drifted",
    )
    require(
        sha256_file(ROOT / authority["i06_registration_validation"])
        == package["registration_validation_sha256"],
        "accepted I06A validation bytes drifted",
    )
    require(
        sha256_file(ROOT / authority["i06_reg_gate"])
        == package["reg_gate_sha256"],
        "accepted I06A REG-GATE bytes drifted",
    )
    require(i05["gate_effect"]["P2-I3-CAL-GATE"].startswith("passed"), "CAL-GATE is not passed")
    require(reg_gate["gate_effect"]["P2-I3-REG-GATE"].startswith("passed_"), "REG-GATE is not passed")
    require(registration["artifact_version"] == package["package_version"], "I06A package version drifted")
    require(registration["matrix"]["governed_case_count"] == package["canonical_case_count"], "I06 case count drifted")
    require(registration["schedule"]["canonical_case_registry_count"] == package["canonical_case_count"], "I06 canonical registry count drifted")
    require(registration["schedule"]["operational_baseline_entry_count"] == package["operational_baseline_entry_count"], "I06 operational baseline count drifted")
    require(registration["schedule"]["governed_entry_count"] == package["governed_entry_count"], "I06 governed entry count drifted")
    require(registration["attempt_governance"]["maximum_governed_child_starts"] == package["maximum_governed_child_starts"], "I06 child-start ceiling drifted")
    require(registration["scientific_outcomes_assigned"] == 0, "I06 contains scientific outcomes")
    retained_commit = authority["i06_retention_commit"]
    require(
        git(ROOT, "merge-base", retained_commit, "HEAD") == retained_commit,
        "I06 retention commit is not an ancestor",
    )
    for relative in (
        authority["i06_registration"],
        authority["i06_registration_validation"],
        authority["i06_reg_gate"],
    ):
        require(
            git(ROOT, "rev-parse", f"{retained_commit}:{relative}")
            == git(ROOT, "rev-parse", f"HEAD:{relative}"),
            f"I06 retained authority changed after its retention commit: {relative}",
        )
    identities = [
        identity(authority["i03_public_call_authority"]),
        identity(authority["i05_calibration_acceptance"]),
        identity(authority["i06_registration"]),
        identity(authority["i06_registration_validation"]),
        identity(authority["i06_reg_gate"]),
    ]
    return i03, registration, identities


def build_records(graph_root: Path, *, allow_dirty_preview: bool = False) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy = load_json(ROOT / POLICY_REL)
    validate_policy_command_environments(policy)
    source_head, source_clean, source_status = clean_source(ROOT)
    if not source_clean and not allow_dirty_preview:
        raise RuntimeError("retained I07-B construction requires a clean committed I07-A source tree")
    for relative in policy["source_package"]["files"]:
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), f"I07-A source file missing: {relative}")
        if source_clean:
            require(git(ROOT, "ls-files", "--error-unmatch", relative) == relative, f"I07-A source file is not tracked: {relative}")

    i03, registration, authority_identities = validate_predecessors(policy)
    runtime = with_digest(inspect_runtime(graph_root, i03, policy))
    rows = build_entry_rows(registration, policy)
    terminal_set = build_expected_terminal_set(rows, registration)
    matrix = with_digest(
        {
            "artifact_id": "P2-I3-BR-I07-RUN-MATRIX",
            "artifact_version": "1.0.0",
            "iteration_id": "P2-I3-I07",
            "branch_id": "P2-I3-BR",
            "source_anchor": source_head,
            "registration": identity(policy["authority"]["i06_registration"]),
            "canonical_case_count": registration["schedule"]["canonical_case_registry_count"],
            "operational_baseline_entry_count": registration["schedule"]["operational_baseline_entry_count"],
            "governed_entry_count": len(rows),
            "maximum_governed_child_starts": registration["attempt_governance"]["maximum_governed_child_starts"],
            "entries": rows,
            "campaign_resource_envelope": {
                "campaign": deepcopy(registration["resource_governance"]["campaign"]),
                "bytes": deepcopy(registration["resource_governance"]["bytes"]),
                "memory": deepcopy(registration["resource_governance"]["memory"]),
                "process_policy": deepcopy(registration["resource_governance"]["process_policy"]),
            },
            "attempt_governance": {
                "class_retry_tokens": deepcopy(registration["attempt_governance"]["class_retry_tokens"]),
                "retry_eligibility": registration["attempt_governance"]["retry_eligibility"],
                "retry_token_allocation_rule": registration["attempt_governance"]["retry_token_allocation_rule"],
                "resume_requirements": deepcopy(registration["attempt_governance"]["resume_requirements"]),
                "statuses": deepcopy(registration["attempt_governance"]["statuses"]),
                "cycle_closure_precedence": deepcopy(registration["attempt_governance"]["cycle_closure_precedence"]),
            },
            "expected_terminal_set": terminal_set,
            "expected_terminal_set_digest": payload_digest({"terminals": terminal_set}),
            "candidate_operations": 0,
        }
    )
    source_identities = [identity(relative) for relative in policy["source_package"]["files"]]
    freeze = with_digest(
        {
            "artifact_id": "P2-I3-BR-I07-INACTIVE-EXEC-FREEZE",
            "artifact_version": "1.0.0",
            "iteration_id": "P2-I3-I07",
            "branch_id": "P2-I3-BR",
            "status": "inactive_pending_owner_freeze_acceptance",
            "source_anchor": source_head,
            "source_identities": source_identities,
            "authority_identities": authority_identities,
            "matrix": {"path": policy["retained_outputs"]["run_matrix"], "sha256": sha256_bytes(matrix)},
            "runtime_binding": {"path": policy["retained_outputs"]["runtime_binding"], "sha256": sha256_bytes(runtime)},
            "activation_boundary": {
                "freeze_acceptance_separate": True,
                "freeze_acceptance_authorizes_execution": False,
                "explicit_owner_execution_direction_required": True,
                "activation_record_separate": True,
                "activation_binds_freeze_retention_commit": True,
                "activation_embeds_own_future_commit": False,
                "launch_head_supplied_at_runtime": True,
                "activation_consumed_by": "permanent_campaign_claim",
            },
            "claim_boundary": {
                "campaign_claim_crosses_p5": False,
                "campaign_claim_permanent": True,
                "governed_entry_claim_permanent": True,
                "entry_specific_p5_separate": True,
                "required_dispatch_conjunction": [
                    "passed_REG_GATE",
                    "accepted_inactive_freeze",
                    "valid_activation",
                    "durable_campaign_claim",
                    "durable_governed_entry_attempt_claim",
                    "supervisor_owned_entry_specific_P5",
                ],
                "phase_protocol": list(registration["attempt_governance"]["phases"]),
            },
            "reconstruction_boundary": {
                "read_only_from_retained_primary_blobs": True,
                "scientific_rerun_is_reconstruction": False,
                "lost_primary_blob_status": "evidence_unavailable_no_rerun",
                "derived_reports_regenerable": True,
                "content_store": deepcopy(registration["resource_governance"]["content_store"]),
            },
            "candidate_activity": {
                "model_constructions": 0,
                "packet_operations": 0,
                "event_operations": 0,
                "native_save_load_reset_operations": 0,
                "responses": 0,
                "control_outcomes": 0,
                "integrity_fault_dispatches": 0,
                "scientific_or_ecology_results": 0,
            },
            "gate_effect": {
                "P2-I3-EXEC-FREEZE": "unopened_pending_owner_freeze_acceptance",
                "activation_construction": False,
                "candidate_execution": False,
                "control_execution": False,
                "integrity_fault_execution": False,
                "I08": "closed",
            },
        }
    )
    schema = load_json(ROOT / SCHEMA_REL)
    for record in (matrix, runtime):
        record["retention_eligible"] = source_clean
        record["preview_only"] = not source_clean
        record["source_status_entry_count"] = len(source_status)
        record["canonical_payload_digest"] = payload_digest(record)
        schema_candidate = deepcopy(record)
        schema_candidate.pop("retention_eligible")
        schema_candidate.pop("preview_only")
        schema_candidate.pop("source_status_entry_count")
        schema_candidate["canonical_payload_digest"] = payload_digest(schema_candidate)
        jsonschema.validate(schema_candidate, schema)
        if source_clean:
            record.clear()
            record.update(schema_candidate)
    freeze["matrix"]["sha256"] = sha256_bytes(matrix)
    freeze["runtime_binding"]["sha256"] = sha256_bytes(runtime)
    freeze["retention_eligible"] = source_clean
    freeze["preview_only"] = not source_clean
    freeze["source_status_entry_count"] = len(source_status)
    freeze["canonical_payload_digest"] = payload_digest(freeze)
    schema_freeze = deepcopy(freeze)
    schema_freeze.pop("retention_eligible")
    schema_freeze.pop("preview_only")
    schema_freeze.pop("source_status_entry_count")
    schema_freeze["canonical_payload_digest"] = payload_digest(schema_freeze)
    jsonschema.validate(schema_freeze, schema)
    if source_clean:
        freeze.clear()
        freeze.update(schema_freeze)
    return matrix, runtime, freeze


def sha256_bytes(value: Mapping[str, Any]) -> str:
    import hashlib

    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def write_records(records: Sequence[Mapping[str, Any]], paths: Sequence[Path]) -> None:
    require(len(records) == len(paths), "record/path count mismatch")
    for path in paths:
        require(not path.exists(), f"output already exists: {path}")
    for record, path in zip(records, paths, strict=True):
        write_exclusive_json(path, record)


def command_build(args: argparse.Namespace) -> int:
    graph_root = Path(args.graph_root).resolve()
    matrix, runtime, freeze = build_records(graph_root, allow_dirty_preview=args.allow_dirty_preview)
    policy = load_json(ROOT / POLICY_REL)
    if args.output_dir:
        output_dir = Path(args.output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        paths = [output_dir / "run-matrix.json", output_dir / "runtime-binding.json", output_dir / "inactive-freeze.json"]
    else:
        require(not args.allow_dirty_preview, "dirty preview requires --output-dir outside retained paths")
        paths = [ROOT / policy["retained_outputs"][key] for key in ("run_matrix", "runtime_binding", "inactive_freeze")]
    write_records((matrix, runtime, freeze), paths)
    print(json.dumps({"status": "built", "outputs": [str(path) for path in paths], "candidate_operations": 0}, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    sub = result.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--graph-root", required=True)
    build.add_argument("--allow-dirty-preview", action="store_true")
    build.add_argument("--output-dir")
    build.set_defaults(func=command_build)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
