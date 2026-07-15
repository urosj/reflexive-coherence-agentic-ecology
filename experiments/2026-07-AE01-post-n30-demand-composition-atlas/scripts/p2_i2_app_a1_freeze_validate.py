#!/usr/bin/env python3
"""Validate the APP-A1 freeze without importing PyGRC or constructing models."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments" / "2026-07-AE01-post-n30-demand-composition-atlas"
FREEZE_PATH = EXPERIMENT / "contracts" / "p2-i2" / "app-a1-fixture-control-conformance-freeze.json"
GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def deep_merge(base: dict[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in overrides.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def resolve_freeze(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = load_json(path)
    if "base_freeze" not in raw:
        return raw, raw
    base_path = ROOT / raw["base_freeze"]["path"]
    if sha256_file(base_path) != raw["base_freeze"]["sha256"]:
        raise AssertionError("base freeze hash mismatch")
    resolved = deep_merge(load_json(base_path), raw["overrides"])
    resolved["correction"] = deepcopy(raw["correction"])
    return resolved, raw


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def contains_machine_path(value: Any) -> bool:
    text = json.dumps(value, sort_keys=True, ensure_ascii=True)
    forbidden = ("/" + "home" + "/", "Documents" + "/" + "RC-github")
    return any(token in text for token in forbidden)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", default=str(FREEZE_PATH.relative_to(ROOT)))
    args = parser.parse_args()
    freeze_path = ROOT / args.freeze
    freeze, raw_freeze = resolve_freeze(freeze_path)
    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed)})

    check("freeze_id", freeze["artifact_id"] == "P2-I2-APP-A1-FIXTURE-CONTROL-CONFORMANCE-FREEZE")
    check("freeze_precedes_models", freeze["status"] == "frozen_before_any_model_construction")
    check("gate_authority_active", freeze["authority"]["candidate_free_conformance_authorized"] is True)
    check("app_a2_closed", freeze["authority"]["app_a2_authorized"] is False)
    check("scientific_runtime_closed", freeze["authority"]["scientific_runtime_authorized"] is False)
    check("commit_closed", freeze["authority"]["commit_authorized"] is False)
    check("graph_head", git("rev-parse", "HEAD", cwd=GRAPH_ROOT) == freeze["authority"]["graph_commit"])
    check("graph_clean", git("status", "--short", cwd=GRAPH_ROOT) == "")

    rc_hashes = all(
        (ROOT / row["path"]).is_file()
        and sha256_file(ROOT / row["path"]) == row["sha256"]
        for row in freeze["authority"]["bound_rcae_files"]
    )
    check("bound_rcae_hashes", rc_hashes)
    graph_hashes = all(
        (GRAPH_ROOT / row["path"]).is_file()
        and sha256_file(GRAPH_ROOT / row["path"]) == row["sha256"]
        for row in freeze["authority"]["bound_graph_files"]
    )
    check("bound_graph_hashes", graph_hashes)
    harness = freeze["authority"]["harness"]
    harness_path = ROOT / harness["path"]
    check("harness_hash", harness_path.is_file() and sha256_file(harness_path) == harness["sha256"])

    topology = freeze["topology"]
    nodes = topology["nodes"]
    edges = topology["edges"]
    check("node_count", len(nodes) == topology["node_count"] == 12)
    check("edge_count", len(edges) == topology["edge_count"] == 28)
    check("node_ids_contiguous", [row["node_id"] for row in nodes] == list(range(12)))
    check("edge_ids_contiguous", [row["edge_id"] for row in edges] == list(range(28)))
    roles = {row["role"] for row in nodes}
    check("roles_unique", len(roles) == 12)
    degree = {role: 0 for role in roles}
    edge_roles: set[str] = set()
    for edge in edges:
        degree[edge["left"]] += 1
        degree[edge["right"]] += 1
        edge_roles.add(edge["edge_role"])
    check("maximum_degree", max(degree.values()) == topology["maximum_node_degree"] == 8)
    check("edge_roles_unique", len(edge_roles) == 28)
    axes = freeze["measurement_authority"]["carrier_axes"]
    universal_access = all(
        "__".join(sorted((participant, f"{prefix}_{axis}"))) in edge_roles
        for participant in ("s_g", "s_e", "s_p")
        for prefix in ("c", "d")
        for axis in axes
    )
    check("universal_participant_access", universal_access)
    r_edges = {
        edge["edge_role"]
        for edge in edges
        if edge["left"] == "r" or edge["right"] == "r"
    }
    check("r_carrier_only", r_edges == {"__".join(sorted((f"c_{axis}", "r"))) for axis in axes})

    gates = freeze["measurement_authority"]["gates"]
    check("four_gates", set(gates) == {"environment_feedback", "support_feedback", "phase_residual", "registered_route_merge_leakage"})
    check("retention_config", freeze["measurement_authority"]["retention_fraction"] == 0.82)
    check("retention_not_gate", freeze["measurement_authority"]["retention_role"] == "configuration_identity_not_measured_gate")
    check("n29_equivalence_blocked", freeze["measurement_authority"]["n29_metric_equivalence_claimed"] is False)

    vectors = freeze["scientific_fixture"]["operation_vectors"]
    check("G_source_vector", vectors["G"] == {"environment": 0.123, "support": 0.082, "distinguishability": 0.133, "boundary": 0.126})
    check("E_source_vector", vectors["E"] == {"environment": 0.069, "support": 0.063, "distinguishability": 0.077, "boundary": 0.081})
    check("P_source_vector", vectors["P"] == {"environment": 0.003, "support": 0.008, "distinguishability": 0.016, "boundary_out": 0.01})
    initial = freeze["scientific_fixture"]["initial_coherence"]
    e_first_valid = all(initial[f"c_{axis}"] > vectors["E"][axis] for axis in axes)
    check("E_first_operational_capacity", e_first_valid)
    check("one_source_capacity_relaxed", freeze["scientific_fixture"]["one_source_capacity_override"]["s_g"] > initial["s_g"])

    arms = freeze["arm_registry"]
    arm_ids = [row["arm_id"] for row in arms]
    check("arm_count", len(arms) == freeze["execution_policy"]["arm_count"] == 19)
    check("arm_ids_unique", len(set(arm_ids)) == 19)
    check("primary_subset_matrix", arm_ids[:8] == ["reference", "G", "E", "P", "GE", "GP", "EP", "GEP"])
    check("one_source_pair", {"one_source_reference", "one_source_GEP"}.issubset(arm_ids))
    check("cyclic_rotation", "cyclic_rotation_GEP" in arm_ids)
    check("two_adjacent_inversions", {"order_EGP", "order_GPE"}.issubset(arm_ids))
    check("label_pair", {"label_permuted_reference", "label_permuted_GEP"}.issubset(arm_ids))
    check("carrier_clamp", "carrier_clamp_GEP" in arm_ids)
    check("three_mediator_restores", {"mediator_restore_G", "mediator_restore_E", "mediator_restore_P"}.issubset(arm_ids))
    check("references_exist", all(row["matched_reference"] == "self" or row["matched_reference"] in arm_ids for row in arms))

    conformance = freeze["conformance"]
    scientific_numbers = {
        float(value)
        for operation in vectors.values()
        for value in operation.values()
    }
    sentinel_numbers = {
        float(value)
        for operation in conformance["sentinel_vectors"].values()
        for value in operation.values()
    }
    check("sentinel_scientific_disjoint", scientific_numbers.isdisjoint(sentinel_numbers))
    policy = conformance["run_policy"]
    check("single_evidence_and_reconstruction", policy["evidence_invocations"] == 1 and policy["reconstruction_invocations"] == 1)
    check("zero_retries", policy["retry_limit"] == 0 and policy["rescue_variants"] == 0)
    check("no_scientific_values_in_conformance", policy["scientific_values_allowed"] is False and policy["app_a2_arms_allowed"] == 0)
    check("venv_command", ".venv/bin/python -B" in policy["evidence_command"])
    check("checkout_binding", "PYTHONPATH=external-repository:graph-reflexive-coherence/src" in policy["evidence_command"])

    if "base_freeze" in raw_freeze:
        correction = freeze["correction"]
        check("same_app_a1_iteration", correction["same_iteration"] is True)
        check("original_attempt_consumed", correction["original_attempt_consumed"] is True)
        check("original_retry_closed", correction["original_retry_allowed"] is False)
        check("replacement_authorized", correction["replacement_attempt_authorized"] is True)
        check("app_a2_still_closed", correction["app_a2_authorized"] is False)
        check("fixture_gate_unchanged", correction["fixture_or_gate_changed"] is False)
        for key in ("failed_start", "owner_authorization"):
            reference = correction[key]
            authority_path = ROOT / reference["path"]
            check(
                f"{key}_hash",
                authority_path.is_file()
                and sha256_file(authority_path) == reference["sha256"],
            )
        intervention = conformance["carrier_clamp_intervention"]
        check(
            "public_ledger_rebase",
            intervention["ledger_rebase_callable"]
            == "pygrc.models.build_lgrc9v3_packet_ledger",
        )
        check("rebase_before_set_state", intervention["ledger_rebase_required_before_set_state"] is True)
        check("history_preserved", intervention["packet_and_event_history_must_be_preserved"] is True)
        check("replacement_count", policy["original_failed_invocations"] == 1 and policy["evidence_invocations"] == 1)

    tree = ast.parse(harness_path.read_text(encoding="utf-8"))
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    check("static_validator_did_not_import_pygrc", "pygrc" not in sys.modules)
    check("harness_declares_pygrc", "pygrc" in imports)
    check("portable_artifacts", not contains_machine_path(raw_freeze))

    failures = [row["check_id"] for row in checks if not row["passed"]]
    result = {
        "artifact_id": "p2_i2_app_a1_freeze_validation_stdout",
        "iteration_id": "P2-I2-APP-A1",
        "status": "passed" if not failures else "failed",
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failure_count": len(failures),
        "failures": failures,
        "freeze_path": str(freeze_path.relative_to(ROOT)),
        "freeze_sha256": sha256_file(freeze_path),
        "correction_freeze": "base_freeze" in raw_freeze,
        "pygrc_imports": 0,
        "models_constructed": 0,
        "app_a2_arms_executed": 0
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
