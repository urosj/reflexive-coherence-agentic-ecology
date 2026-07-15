"""Construct the inactive APP-B4 75-arm execution freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
from typing import Any

from p2_i2_app_b4_analysis import build_registry, canonical_bytes, digest_value, feasible_sequences


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


def build(capability_path: Path, base_freeze_path: Path) -> dict[str, Any]:
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "freeze builder not launched through lexical repository .venv")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "freeze builder requires -B")
    capability = load_json(capability_path)
    base = load_json(base_freeze_path)
    require(capability["status"] == "blocked_before_freeze_owner_choice_required", "wrong capability audit state")
    require(capability["unchanged_baseline_audit"]["feasible_sequence_count"] == 24, "capability feasible count drifted")
    require(capability["owner_choice"]["selection_made"] is False, "capability artifact was rewritten with a selection")
    paths = {
        "registration": f"{EXPERIMENT_REL}/contracts/p2-i2/i06-three-mode-registration.json",
        "machine_policy": f"{EXPERIMENT_REL}/configs/p2_i2_i04r2_machine_policy.json",
        "parent_policy": f"{EXPERIMENT_REL}/configs/p2_i2_i04r1_analysis_policy.json",
        "capability": str(capability_path.relative_to(ROOT)),
        "base_freeze": str(base_freeze_path.relative_to(ROOT)),
        "app_b_runner": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_run.py",
        "app_b_analysis": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_analysis.py",
        "history_adapter": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_history_adapter.py",
        "i06_registration_source": f"{EXPERIMENT_REL}/scripts/p2_i2_i06_registration.py",
        "i06_history_adapter": f"{EXPERIMENT_REL}/scripts/p2_i2_i06_history_adapter.py",
        "i03b_history_adapter": f"{EXPERIMENT_REL}/scripts/p2_i2_i03b_history_adapter.py",
        "analysis": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_analysis.py",
        "runner": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_run.py",
        "reconstructor": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_reconstruct.py",
        "validator": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_validate.py",
        "freeze_builder": f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_freeze.py",
    }
    require(all(portable_relative(value) for value in paths.values()), "absolute construction path")
    authority_keys = ("registration", "machine_policy", "parent_policy", "capability", "base_freeze")
    implementation_keys = (
        "app_b_runner",
        "app_b_analysis",
        "history_adapter",
        "i06_registration_source",
        "i06_history_adapter",
        "i03b_history_adapter",
        "analysis",
        "runner",
        "reconstructor",
        "validator",
    )
    authority_inputs = [
        {"path": paths[key], "sha256": sha256(ROOT / paths[key]), "role": key}
        for key in authority_keys
    ]
    implementation = {paths[key]: sha256(ROOT / paths[key]) for key in implementation_keys}
    freeze: dict[str, Any] = {
        "artifact_id": "P2-I2-APP-B4-INACTIVE-75-ARM-FREEZE",
        "artifact_version": "1.0",
        "iteration_id": "P2-I2-APP-B4",
        "status": "inactive_owner_review_pending",
        "authority": {
            "decision": "P2-I2-DEC-085",
            "change": "P2-I2-CHG-090",
            "owner_selection": "unchanged_baseline_24_sequence_panel",
            "construction_source": {"path": paths["freeze_builder"], "sha256": sha256(ROOT / paths["freeze_builder"])},
        },
        "authority_inputs": authority_inputs,
        "implementation_sha256": implementation,
        "candidate_free_sources": [paths[key] for key in ("analysis", "reconstructor", "validator")],
        "environment": {
            "interpreter": ".venv/bin/python",
            "interpreter_sha256": sha256(Path(sys.executable).resolve()),
            "python_version": platform.python_version(),
            "graph_repository": base["environment"]["graph_repository"],
            "graph_commit": base["environment"]["graph_commit"],
            "graph_source": base["environment"]["graph_source"],
            "graph_read_only": True,
            "absolute_persisted_paths_forbidden": True,
        },
        "panel": {
            "mode": "history_carried",
            "seeds": [101, 211, 307],
            "feasible_sequences": list(feasible_sequences()),
            "feasible_sequence_count": 24,
            "reference_per_seed": 1,
            "arm_count": 75,
            "excluded_operationally_infeasible_sequences": ["EEG", "EEE", "EEP"],
            "excluded_sequences_are_not_expected_outputs": True,
            "excluded_sequences_are_not_scientific_zero": True,
            "expanded_registry_digest": None,
        },
        "operation_registry": base["operation_registry"],
        "schedule": base["schedule"],
        "mode_realizations": {"history_carried": base["mode_realizations"]["history_carried"]},
        "response_authority": base["response_authority"],
        "fixture_and_scaffold": {
            "accepted_topology_and_initial_coherence_unchanged": True,
            "operation_routes_and_amounts_unchanged": True,
            "history_admission_and_fold_unchanged": True,
            "M_H_materialization_unchanged": True,
            "feedback_threshold_and_response_window_unchanged": True,
            "pre_funding_added": False,
            "new_producer_added": False,
            "APP_B2_runtime_outcomes_used_to_select_panel": False,
        },
        "analysis_policy": {
            "seed_replication": "positive aggregate classifiers require the same categorical response pattern at all three frozen seeds; exact numeric invariance is reported separately",
            "raw_cardinality": "all 24 feasible triples reproduce positive GEP response",
            "raw_cardinality_exclusion": "at least one valid feasible triple is zero while GEP is positive",
            "dose_multiset": "compare response groups by sorted three-symbol multiset",
            "ordering": "compare permutations only within the same native-dose multiset",
            "exact_total_permutations": ["GEP", "GPE", "EGP", "EPG", "PGE", "PEG"],
            "operation_complementarity_claimed": False,
            "maximum_positive_claim": "ordered quantitative-history pattern within the unchanged-baseline feasible domain",
            "state_and_hybrid_reinterpreted": False,
        },
        "execution": {
            "activation_path": f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-live-activation.json",
            "claim_path": f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-campaign-claim.json",
            "output_path": f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-runtime-evidence.json",
            "reconstruction_path": f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-reconstruction-and-closeout.json",
            "validation_path": f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-inactive-freeze-validation.json",
            "runner_path": paths["runner"],
            "reconstructor_path": paths["reconstructor"],
            "campaign_attempts": 1,
            "scientific_retries": 0,
            "infrastructure_retries": 0,
            "fresh_process_per_arm": True,
            "fresh_model_per_arm": True,
            "cumulative_single_output": True,
            "normalized_command_template": [
                ".venv/bin/python", "-B", paths["runner"],
                "--freeze", f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-inactive-75-arm-freeze.json",
                "--activation", f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-live-activation.json",
                "--claim", f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-campaign-claim.json",
                "--output", f"{EXPERIMENT_REL}/contracts/p2-i2/app-b4-runtime-evidence.json",
                "--expected-head", "{AUTHORITY_HEAD}",
                "--graph-root", "../graph-reflexive-coherence",
            ],
        },
        "lifecycle": {
            "freeze_active": False,
            "commit_authorized": False,
            "activation_artifact_exists": False,
            "campaign_authorized": False,
            "claim_consumed": False,
            "runtime_generation_count": 0,
            "result_assigned": False,
            "owner_review_required": True,
        },
    }
    rows = build_registry(freeze)
    freeze["panel"]["expanded_registry_digest"] = digest_value(rows)
    require(build_registry(freeze) == rows, "registry did not stabilize")
    freeze["canonical_payload_digest"] = digest_value(freeze)
    return freeze


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capability", required=True)
    parser.add_argument("--base-freeze", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    for value in (args.capability, args.base_freeze, args.output):
        require(portable_relative(value), "absolute path refused")
    result = build(ROOT / args.capability, ROOT / args.base_freeze)
    output = ROOT / args.output
    require(not output.exists(), "APP-B4 freeze already exists")
    output.write_bytes(canonical_bytes(result))
    require(load_json(output) == result, "APP-B4 freeze readback drifted")
    print(json.dumps({"status": result["status"], "arms": result["panel"]["arm_count"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
