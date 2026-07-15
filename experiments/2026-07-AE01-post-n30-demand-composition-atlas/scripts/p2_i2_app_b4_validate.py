"""Candidate-free validation of the inactive APP-B4 75-arm freeze."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
from typing import Any

from p2_i2_app_b4_analysis import (
    SEEDS,
    build_registry,
    canonical_bytes,
    classify_response_landscape,
    digest_value,
    feasible_sequences,
)
from p2_i2_app_b4_run import project_app_b4_envelope
from p2_i2_app_b_validate import synthetic_envelope
import p2_i2_i04r2_analysis as accepted


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def imports_pygrc(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(alias.name.startswith("pygrc") for alias in node.names):
            return True
        if isinstance(node, ast.ImportFrom) and str(node.module).startswith("pygrc"):
            return True
    return False


def validate(freeze_path: Path) -> dict[str, Any]:
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "validator not launched through lexical repository .venv")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "validator requires -B")
    freeze = load_json(freeze_path)
    without_digest = {key: value for key, value in freeze.items() if key != "canonical_payload_digest"}
    require(digest_value(without_digest) == freeze["canonical_payload_digest"], "freeze payload digest drifted")
    require(freeze_path.read_bytes() == canonical_bytes(freeze), "freeze is not canonical")
    require(freeze["status"] == "inactive_owner_review_pending", "freeze unexpectedly active")
    require(freeze["lifecycle"]["campaign_authorized"] is False, "campaign authorized inside inactive freeze")
    require(freeze["lifecycle"]["commit_authorized"] is False, "commit authorized inside inactive freeze")
    require(freeze["lifecycle"]["runtime_generation_count"] == 0, "runtime count nonzero in freeze")
    require(freeze["panel"]["arm_count"] == 75, "panel arm count drifted")
    require(freeze["panel"]["feasible_sequence_count"] == 24, "panel sequence count drifted")
    require(freeze["panel"]["excluded_operationally_infeasible_sequences"] == ["EEG", "EEE", "EEP"], "excluded sequence set drifted")
    rows = build_registry(freeze)
    require(len(rows) == len({row["arm_id"] for row in rows}) == 75, "registry identity drifted")
    require(sum(row["arm_kind"] == "reference" for row in rows) == 3, "reference count drifted")
    require(sum(row["arm_kind"] == "ordered_three_token" for row in rows) == 72, "triple arm count drifted")
    require(all(len(row["history_operations"]) == 3 for row in rows if row["arm_kind"] != "reference"), "three-token row drifted")
    require(not ({"EEG", "EEE", "EEP"} & {row["sequence"] for row in rows}), "infeasible row entered freeze")

    for item in freeze["authority_inputs"]:
        require(portable_relative(item["path"]), "absolute authority path")
        require(sha256(ROOT / item["path"]) == item["sha256"], f"authority input drift: {item['path']}")
    for relative, expected in freeze["implementation_sha256"].items():
        require(portable_relative(relative), "absolute implementation path")
        require(sha256(ROOT / relative) == expected, f"implementation drift: {relative}")
    require(freeze["environment"]["interpreter"] == ".venv/bin/python", "non-venv interpreter frozen")
    require(freeze["environment"]["absolute_persisted_paths_forbidden"] is True, "absolute path boundary open")
    for value in freeze["execution"].values():
        if isinstance(value, str) and ("path" in value or "/" in value):
            require(portable_relative(value), "absolute execution path")
    for relative in freeze["candidate_free_sources"]:
        source = (ROOT / relative).read_text(encoding="utf-8")
        tree = ast.parse(source)
        require(not imports_pygrc(tree), f"candidate-free source imports PyGRC: {relative}")
        outcome_markers = ("app-b2-" + "replacement-runtime-evidence", "app-b2-" + "corrected-analysis")
        require(all(marker not in source for marker in outcome_markers), f"APP-B2 outcome dependency in {relative}")

    runner_source = (ROOT / f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_run.py").read_text(encoding="utf-8")
    runner_tree = ast.parse(runner_source)
    require("P2-I2-APP-B4-LIVE-ACTIVATION" in runner_source, "runner lacks separate activation requirement")
    require("owner_accepted_committed_single_campaign" in runner_source, "runner lacks accepted activation state")
    require("os.O_EXCL" in runner_source, "runner claim is not exclusive")
    require('".venv/bin/python", "-B", RUNNER_REL' in runner_source, "runner child is not lexical .venv")
    require(not imports_pygrc(runner_tree), "APP-B4 runner imports PyGRC at module scope")

    synthetic = {"response_envelope": synthetic_envelope("history_carried", 101, "GGG", 0.125)}
    projected = project_app_b4_envelope(synthetic, {"sequence": "GGG", "seed": 101})
    projection = projected["app_b4_measurement_projection"]
    require(projection["actual_operation_sequence"] == "GGG", "APP-B4 sequence identity projection drifted")
    require(projection["accepted_envelope_physical_order_id"] == "q1_then_q2", "accepted physical-order protocol identity drifted")
    accepted.validate_response_envelope(
        projected["response_envelope"],
        load_json(ROOT / f"{EXPERIMENT_REL}/configs/p2_i2_i04r2_machine_policy.json"),
        load_json(ROOT / f"{EXPERIMENT_REL}/configs/p2_i2_i04r1_analysis_policy.json"),
    )

    sequences = feasible_sequences()
    all_positive = {
        seed: {"reference": 0.0, **{sequence: 0.125 for sequence in sequences}}
        for seed in SEEDS
    }
    cardinality = classify_response_landscape(all_positive, tolerance=1e-12)
    require(cardinality["raw_three_event_cardinality_sufficient"] is True, "cardinality classifier positive path failed")
    unique_gep = {
        seed: {"reference": 0.0, **{sequence: 0.125 if sequence == "GEP" else 0.0 for sequence in sequences}}
        for seed in SEEDS
    }
    specific = classify_response_landscape(unique_gep, tolerance=1e-12)
    require(specific["GEP_unique_positive_within_feasible_panel"] is True, "GEP-specific classifier path failed")
    order_case = {
        seed: {"reference": 0.0, **{sequence: 0.125 if sequence == "GEP" else 0.0 for sequence in sequences}}
        for seed in SEEDS
    }
    order = classify_response_landscape(order_case, tolerance=1e-12)
    require(order["exact_total_order_effect"] is True, "order-effect classifier path failed")
    divergent = {
        seed: {
            "reference": 0.0,
            **{
                sequence: 0.125
                if seed == 211 or sequence == "GEP"
                else 0.0
                for sequence in sequences
            },
        }
        for seed in SEEDS
    }
    divergent_result = classify_response_landscape(divergent, tolerance=1e-12)
    require(divergent_result["seed_pattern_invariant"] is False, "seed divergence was not detected")
    require(divergent_result["raw_three_event_cardinality_sufficient"] is False, "seed divergence passed cardinality")
    require(divergent_result["GEP_unique_positive_within_feasible_panel"] is False, "seed divergence passed GEP uniqueness")
    require(cardinality["operation_complementarity_claimed"] is False, "classifier opened operation complementarity")
    require(specific["claim_ceiling"] == "ordered quantitative-history pattern within the unchanged-baseline feasible domain", "claim ceiling drifted")

    for path_key in ("activation_path", "claim_path", "output_path", "reconstruction_path"):
        require(not (ROOT / freeze["execution"][path_key]).exists(), f"inactive output exists: {path_key}")

    result = {
        "artifact_id": "P2-I2-APP-B4-INACTIVE-FREEZE-VALIDATION",
        "artifact_version": "1.0",
        "status": "passed_inactive_owner_review_pending",
        "checks": {
            "canonical_freeze_and_digest": True,
            "authority_and_implementation_hashes": len(freeze["authority_inputs"]) + len(freeze["implementation_sha256"]),
            "registry_rows": 75,
            "reference_rows": 3,
            "ordered_three_token_rows": 72,
            "feasible_sequences": 24,
            "excluded_infeasible_sequences": 3,
            "candidate_free_source_files": len(freeze["candidate_free_sources"]),
            "pure_classifier_cases": 4,
            "accepted_envelope_identity_projection_cases": 1,
            "separate_activation_required": True,
            "exclusive_claim_required": True,
            "lexical_venv_parent_and_child": True,
            "outcome_quarantine": True,
            "output_absence": True,
            "operation_complementarity_blocked": True,
        },
        "process_counts": {
            "validator_processes_this_start": 1,
            "PyGRC_imports": 0,
            "models": 0,
            "producers": 0,
            "arms": 0,
            "responses": 0,
        },
        "lifecycle": {
            "freeze_active": False,
            "commit_authorized": False,
            "campaign_authorized": False,
            "owner_review_required": True,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one validation mode")
    for value in (args.freeze, args.output):
        if value is not None:
            require(portable_relative(value), "absolute path refused")
    result = validate(ROOT / args.freeze)
    if args.output:
        output = ROOT / args.output
        require(not output.exists(), "APP-B4 validation output exists")
        output.write_bytes(canonical_bytes(result))
        require(load_json(output) == result, "APP-B4 validation readback drifted")
    print(json.dumps({"status": result["status"], "registry_rows": result["checks"]["registry_rows"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
