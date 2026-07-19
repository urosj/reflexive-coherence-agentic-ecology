#!/usr/bin/env python3
"""Independent candidate-free validation for the P2-I3 B-R I07 freeze."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import hashlib
import importlib
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
    ROOT,
    SCHEMA_REL,
    ENTRY_PHASES,
    build_entry_rows,
    build_expected_terminal_set,
    canonical_bytes,
    identity,
    load_json,
    payload_digest,
    require,
    sha256_file,
    validate_policy_command_environments,
    verify_digest,
    with_digest,
)


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SUPERVISOR_REL = EXPERIMENT / "scripts/p2_i3_i08_br_supervisor.py"
CASE_REL = EXPERIMENT / "scripts/p2_i3_i08_br_case.py"
I06_SOURCE_REL = EXPERIMENT / "scripts/p2_i3_i06_br_registration.py"
EXPECTED_GRAPH_REVISION = "565706f8b7647f6b7638b9afbe52372e170bf724"


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def add(self, check_id: str, condition: bool, observed: Any, expected: Any) -> None:
        if not condition:
            raise RuntimeError(f"{check_id}: {observed!r} != {expected!r}")
        self.rows.append({"check_id": check_id, "status": "passed", "observed": observed, "expected": expected})


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    require(result.returncode == 0, f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def resolve_symbol(symbol: str) -> Any:
    parts = symbol.split(".")
    require(parts[0] == "pygrc" and symbol in LIVE_OPERATION_SYMBOLS, f"unregistered symbol: {symbol}")
    value: Any = importlib.import_module("pygrc")
    for part in parts[1:]:
        value = getattr(value, part)
    return value


def source_owner(value: Any, graph_root: Path) -> tuple[str, str]:
    path = Path(inspect.getsourcefile(value) or inspect.getfile(value)).resolve()
    require(path.is_relative_to((graph_root / "src").resolve()), "public API owner escaped graph source")
    return path.relative_to(graph_root.resolve()).as_posix(), sha256_file(path)


def source_functions(relative: Path) -> tuple[ast.AST, set[str]]:
    source = (ROOT / relative).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=relative.as_posix())
    names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
    return tree, names


def imported_roots(tree: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def attribute_calls(tree: ast.AST) -> set[str]:
    return {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }


def validate_records(graph_root: Path) -> dict[str, Any]:
    checks = Checks()
    policy = load_json(ROOT / POLICY_REL)
    validate_policy_command_environments(policy)
    schema = load_json(ROOT / SCHEMA_REL)
    paths = {key: ROOT / value for key, value in policy["retained_outputs"].items()}
    matrix = load_json(paths["run_matrix"])
    runtime = load_json(paths["runtime_binding"])
    freeze = load_json(paths["inactive_freeze"])
    for name, record in (("matrix", matrix), ("runtime", runtime), ("freeze", freeze)):
        verify_digest(record)
        jsonschema.validate(record, schema)
        checks.add(f"schema_and_digest:{name}", True, "passed", "passed")

    head = git(ROOT, "rev-parse", "HEAD")
    checks.add("common_source_anchor", matrix["source_anchor"] == runtime["source_anchor"] == freeze["source_anchor"] == head, [matrix["source_anchor"], runtime["source_anchor"], freeze["source_anchor"], head], [head] * 4)
    expected_dirty = sorted(
        f"?? {policy['retained_outputs'][key]}" for key in ("run_matrix", "runtime_binding", "inactive_freeze")
    )
    actual_dirty = sorted(git(ROOT, "status", "--porcelain=v1", "--untracked-files=all").splitlines())
    checks.add("only_retained_i07b_outputs_untracked", actual_dirty == expected_dirty, actual_dirty, expected_dirty)

    registration = load_json(ROOT / policy["authority"]["i06_registration"])
    expected_rows = build_entry_rows(registration, policy)
    expected_terminals = build_expected_terminal_set(expected_rows, registration)
    entry_ordinals = {row["entry_id"]: row["schedule_ordinal"] for row in matrix["entries"]}
    checks.add("matrix_exact_reconstruction", matrix["entries"] == expected_rows, len(matrix["entries"]), len(expected_rows))
    checks.add("terminal_set_exact_reconstruction", matrix["expected_terminal_set"] == expected_terminals, len(matrix["expected_terminal_set"]), len(expected_terminals))
    checks.add("terminal_set_digest", matrix["expected_terminal_set_digest"] == payload_digest({"terminals": expected_terminals}), matrix["expected_terminal_set_digest"], payload_digest({"terminals": expected_terminals}))
    checks.add("closed_canonical_case_count", matrix["canonical_case_count"] == 450, matrix["canonical_case_count"], 450)
    checks.add("closed_operational_baseline_count", matrix["operational_baseline_entry_count"] == 6, matrix["operational_baseline_entry_count"], 6)
    checks.add("closed_governed_entry_count", matrix["governed_entry_count"] == 456, matrix["governed_entry_count"], 456)
    checks.add("closed_child_start_ceiling", matrix["maximum_governed_child_starts"] == 460, matrix["maximum_governed_child_starts"], 460)
    checks.add("closed_terminal_count", len(matrix["expected_terminal_set"]) == 919, len(matrix["expected_terminal_set"]), 919)
    checks.add("schedule_ordinals", [row["schedule_ordinal"] for row in matrix["entries"]] == list(range(1, 457)), [matrix["entries"][0]["schedule_ordinal"], matrix["entries"][-1]["schedule_ordinal"]], [1, 456])
    checks.add("unique_entry_ids", len({row["entry_id"] for row in matrix["entries"]}) == 456, len({row["entry_id"] for row in matrix["entries"]}), 456)
    checks.add("unique_case_ids", len({row["case_id"] for row in matrix["entries"] if row["case_id"] is not None}) == 450, len({row["case_id"] for row in matrix["entries"] if row["case_id"] is not None}), 450)
    checks.add("dependency_ids_closed", all(parent in entry_ordinals for row in matrix["entries"] for parent in row["parent_entry_ids"]), True, True)
    checks.add("parents_precede_dependents", all(entry_ordinals[parent] < row["schedule_ordinal"] for row in matrix["entries"] for parent in row["parent_entry_ids"]), True, True)
    checks.add("registered_phases_exact", all(tuple(row["phases"]) == ENTRY_PHASES for row in matrix["entries"]), True, True)
    checks.add("class_population", {name: sum(row["execution_class"] == name for row in matrix["entries"]) for name in registration["resource_governance"]["class_counts"]} == registration["resource_governance"]["class_counts"], registration["resource_governance"]["class_counts"], registration["resource_governance"]["class_counts"])

    checks.add("matrix_file_binding", freeze["matrix"] == {"path": policy["retained_outputs"]["run_matrix"], "sha256": sha256_file(paths["run_matrix"])}, freeze["matrix"], {"path": policy["retained_outputs"]["run_matrix"], "sha256": sha256_file(paths["run_matrix"])})
    checks.add("runtime_file_binding", freeze["runtime_binding"] == {"path": policy["retained_outputs"]["runtime_binding"], "sha256": sha256_file(paths["runtime_binding"])}, freeze["runtime_binding"], {"path": policy["retained_outputs"]["runtime_binding"], "sha256": sha256_file(paths["runtime_binding"])})
    expected_sources = [identity(relative) for relative in policy["source_package"]["files"]]
    checks.add("source_package_exact", freeze["source_identities"] == expected_sources, len(freeze["source_identities"]), len(expected_sources))

    checks.add("graph_revision", git(graph_root, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION, git(graph_root, "rev-parse", "HEAD"), EXPECTED_GRAPH_REVISION)
    checks.add("graph_clean", git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "", git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"), "")
    source_root = (graph_root / "src").resolve()
    pygrc = importlib.import_module("pygrc")
    checks.add("exact_pygrc_import", Path(pygrc.__file__).resolve() == source_root / "pygrc" / "__init__.py", "src/pygrc/__init__.py", "src/pygrc/__init__.py")
    observed_api: list[dict[str, Any]] = []
    for row in runtime["public_api"]:
        value = resolve_symbol(row["symbol"])
        owner, owner_digest = source_owner(value, graph_root)
        observed_api.append(
            {
                **deepcopy(row),
                "signature": str(inspect.signature(value)),
                "owning_source": owner,
                "owning_source_sha256": owner_digest,
            }
        )
    checks.add("public_api_exact", observed_api == runtime["public_api"], len(observed_api), 18)
    checks.add("public_api_closed", tuple(row["symbol"] for row in runtime["public_api"]) == LIVE_OPERATION_SYMBOLS, tuple(row["symbol"] for row in runtime["public_api"]), LIVE_OPERATION_SYMBOLS)
    checks.add("forbidden_api_closed", tuple(runtime["forbidden_runtime_paths"]) == FORBIDDEN_SYMBOLS, runtime["forbidden_runtime_paths"], list(FORBIDDEN_SYMBOLS))
    checks.add("no_dynamic_runtime_lookup", all(row["dynamic_runtime_lookup_allowed"] is False for row in runtime["public_api"]), True, True)
    checks.add("normalized_runtime_environment", runtime["environment"]["required_environment"] == policy["environment"]["required_environment"] and runtime["environment"]["normalized_pythonpath"] == policy["environment"]["normalized_pythonpath"] and runtime["environment"]["pythonhome"] == "absent", runtime["environment"], "exact policy environment")

    supervisor_tree, supervisor_names = source_functions(SUPERVISOR_REL)
    case_tree, case_names = source_functions(CASE_REL)
    i06_tree, i06_names = source_functions(I06_SOURCE_REL)
    checks.add("supervisor_no_pygrc_import", "pygrc" not in imported_roots(supervisor_tree), sorted(imported_roots(supervisor_tree)), "no pygrc")
    checks.add("supervisor_no_case_import", "p2_i3_i08_br_case" not in imported_roots(supervisor_tree), sorted(imported_roots(supervisor_tree)), "no case module")
    checks.add("case_no_dynamic_import", "importlib" not in imported_roots(case_tree), sorted(imported_roots(case_tree)), "no importlib")
    unsafe_getattrs = [
        node
        for node in ast.walk(case_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "getattr"
        and not (
            len(node.args) >= 2
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id == "os"
            and isinstance(node.args[1], ast.Constant)
            and node.args[1].value == "O_NOFOLLOW"
        )
    ]
    checks.add("case_no_dynamic_getattr_dispatch", not unsafe_getattrs, len(unsafe_getattrs), 0)
    function_sets = {
        "p2_i3_i06_br_registration": i06_names,
        "p2_i3_i08_br_case": case_names,
    }
    for symbol, sites in CALL_SITE_REGISTRY.items():
        for site in sites:
            module, function = site.split(".", 1)
            checks.add(f"registered_call_site:{symbol}:{site}", function in function_sets[module], function in function_sets[module], True)
    case_calls = attribute_calls(case_tree)
    forbidden_leaf_names = {symbol.rsplit(".", 1)[-1] for symbol in FORBIDDEN_SYMBOLS}
    checks.add("case_forbidden_call_leaves_absent", not case_calls & forbidden_leaf_names, sorted(case_calls & forbidden_leaf_names), [])

    checks.add("activation_separate", freeze["activation_boundary"]["freeze_acceptance_separate"] is True and freeze["activation_boundary"]["explicit_owner_execution_direction_required"] is True, freeze["activation_boundary"], "separate acceptance and activation")
    checks.add("campaign_does_not_cross_p5", freeze["claim_boundary"]["campaign_claim_crosses_p5"] is False and freeze["claim_boundary"]["entry_specific_p5_separate"] is True, freeze["claim_boundary"], "campaign claim plus separate P5")
    checks.add("read_only_reconstruction", freeze["reconstruction_boundary"]["read_only_from_retained_primary_blobs"] is True and freeze["reconstruction_boundary"]["scientific_rerun_is_reconstruction"] is False, freeze["reconstruction_boundary"], "read-only only")
    checks.add("candidate_activity_zero", all(value == 0 for value in freeze["candidate_activity"].values()), freeze["candidate_activity"], "all zero")
    checks.add("inspection_activity_zero", runtime["inspection_activity"]["public_symbol_invocations"] == 0 and runtime["inspection_activity"]["candidate_or_control_operations"] == 0, runtime["inspection_activity"], "zero public invocation and candidate/control operation")
    checks.add("gate_remains_inactive", freeze["gate_effect"]["candidate_execution"] is False and freeze["gate_effect"]["I08"] == "closed", freeze["gate_effect"], "inactive")

    validated = [
        {"path": policy["retained_outputs"]["run_matrix"], "sha256": sha256_file(paths["run_matrix"])},
        {"path": policy["retained_outputs"]["runtime_binding"], "sha256": sha256_file(paths["runtime_binding"])},
        {"path": policy["retained_outputs"]["inactive_freeze"], "sha256": sha256_file(paths["inactive_freeze"])},
    ]
    return with_digest(
        {
            "artifact_id": "P2-I3-BR-I07-INACTIVE-FREEZE-VALIDATION",
            "artifact_version": "1.0.0",
            "iteration_id": "P2-I3-I07",
            "branch_id": "P2-I3-BR",
            "status": "passed_candidate_free_inactive_validation",
            "source_anchor": head,
            "checks": checks.rows,
            "total_checks": len(checks.rows),
            "passed_checks": len(checks.rows),
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
            "validated_identities": validated,
            "gate_effect": {
                "P2-I3-EXEC-FREEZE": "review_ready_inactive_not_accepted",
                "activation_construction": False,
                "candidate_execution": False,
                "I08": "closed",
            },
        }
    )


def command_validate(args: argparse.Namespace) -> int:
    record = validate_records(Path(args.graph_root).resolve())
    policy = load_json(ROOT / POLICY_REL)
    output = Path(args.output).resolve() if args.output else ROOT / policy["retained_outputs"]["validation"]
    require(not output.exists(), f"validation output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_bytes(record))
    print(json.dumps({"status": record["status"], "checks": record["total_checks"], "candidate_operations": 0, "output": str(output)}, sort_keys=True))
    return 0


def command_reconstruct(args: argparse.Namespace) -> int:
    record = validate_records(Path(args.graph_root).resolve())
    policy = load_json(ROOT / POLICY_REL)
    retained = load_json(ROOT / policy["retained_outputs"]["validation"])
    require(record == retained, "reconstructed validation differs from retained validation")
    output = Path(args.output).resolve()
    require(not output.exists(), "reconstruction output already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_bytes(record))
    require(output.read_bytes() == (ROOT / policy["retained_outputs"]["validation"]).read_bytes(), "reconstruction is not byte-exact")
    print(json.dumps({"status": "byte_exact_reconstruction", "checks": record["total_checks"], "candidate_operations": 0, "output": str(output)}, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    sub = result.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--graph-root", required=True)
    validate.add_argument("--output")
    validate.set_defaults(func=command_validate)
    reconstruct = sub.add_parser("reconstruct")
    reconstruct.add_argument("--graph-root", required=True)
    reconstruct.add_argument("--output", required=True)
    reconstruct.set_defaults(func=command_reconstruct)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
