#!/usr/bin/env python3
"""Pure final validation of the corrected APP-B2 retained evidence."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
from typing import Any, Mapping

import p2_i2_i04r2_analysis as accepted
from p2_i2_app_b_analysis import analyze_receipts, build_arm_registry, canonical_bytes, digest_value


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
MACHINE_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r2_machine_policy.json"
PARENT_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r1_analysis_policy.json"


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


def assert_portable(value: Any, field: str = "root") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            assert_portable(item, f"{field}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            assert_portable(item, f"{field}[{index}]")
        return
    if not isinstance(value, str):
        return
    tokens = [token.strip("\"'`") for token in re.split(r"[\s=,;()\[\]{}<>]+", value) if token.strip("\"'`")]
    require(
        not any(PurePosixPath(token).is_absolute() or PureWindowsPath(token).is_absolute() for token in tokens),
        f"absolute path retained in {field}",
    )


def close(left: float, right: float, tolerance: float = 2.842170943040401e-14) -> bool:
    return math.isclose(float(left), float(right), rel_tol=0.0, abs_tol=tolerance)


def validate(
    freeze_path: Path,
    runtime_path: Path,
    original_reconstruction_path: Path,
    corrected_path: Path,
    output: Path | None,
) -> dict[str, Any]:
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "validator not launched through lexical repository .venv")
    freeze = load_json(freeze_path)
    runtime = load_json(runtime_path)
    original_reconstruction = load_json(original_reconstruction_path)
    corrected = load_json(corrected_path)
    for path, value in (
        (runtime_path, runtime),
        (original_reconstruction_path, original_reconstruction),
        (corrected_path, corrected),
    ):
        require(path.read_bytes() == canonical_bytes(value), f"noncanonical artifact: {path.name}")
        require(
            digest_value({key: item for key, item in value.items() if key != "canonical_payload_digest"})
            == value["canonical_payload_digest"],
            f"payload digest drift: {path.name}",
        )
        assert_portable(value, path.name)
    require(original_reconstruction["analysis"] == runtime["analysis"], "historical reconstruction drifted")
    require(original_reconstruction["analysis_reconstruction_byte_identical"] is True, "historical byte reconstruction failed")

    rows = build_arm_registry(freeze["arm_registry_specification"])
    receipts = runtime["receipts"]
    require(runtime["arm_count"] == len(rows) == len(receipts) == 99, "runtime arm count drifted")
    require([item["arm_id"] for item in receipts] == [item["arm_id"] for item in rows], "runtime arm order drifted")
    require(len({item["arm_id"] for item in receipts}) == 99, "duplicate runtime arm")
    require(len({item["process_receipt"]["pid"] for item in receipts}) == 99, "fresh process isolation failed")
    require(all(item["process_receipt"]["fresh_process"] for item in receipts), "fresh-process receipt missing")
    require(all(item["process_receipt"]["logical_executable"] == ".venv/bin/python" for item in receipts), "non-venv child receipt")
    require(all(item["process_receipt"]["dont_write_bytecode"] for item in receipts), "child omitted -B")
    require(all(item["baseline"]["fresh_model"] for item in receipts), "fresh-model receipt missing")
    require(all(item["restoration_receipt"]["identity_before_save"] == item["restoration_receipt"]["identity_after_load"] for item in receipts), "save/load identity failure")
    require(all(item["restoration_receipt"]["identity_after_reset"] == item["baseline"]["identity"] for item in receipts), "reset identity failure")

    machine = load_json(ROOT / MACHINE_REL)
    parent = load_json(ROOT / PARENT_REL)
    for receipt in receipts:
        accepted.validate_response_envelope(receipt["response_envelope"], machine, parent)
    reconstructed = analyze_receipts(receipts, freeze, machine, parent)
    analysis = corrected["corrected_analysis"]
    require(reconstructed == analysis, "corrected analysis does not reconstruct")
    require(analysis["matrix_complete"] and analysis["all_arms_operationally_valid"], "corrected matrix invalid")
    require(analysis["arm_order_exact"] and analysis["arm_count_observed"] == 99, "corrected matrix order/count invalid")
    require(all(item["valid"] for item in analysis["operational_validity"].values()), "invalid corrected arm")
    require(analysis["supported_modes"] == ["history_carried"], "supported mode set drifted")
    require(analysis["terminal_classification"] == "supported_bounded_candidate", "terminal classification drifted")
    require(analysis["bounded_claim"] == "bounded P2-I2-grounded three-operation shared-pool composition candidate", "claim ceiling drifted")
    require(analysis["cross_appendix_recurrence_claimed"] is False, "cross-appendix recurrence claimed")

    expected_margins = {"state_carried": -1.0, "history_carried": 1.0, "hybrid": 0.0}
    expected_comparators = {"state_carried": "GP", "history_carried": "reference", "hybrid": "P"}
    for mode, margins in analysis["primary_results"].items():
        require(len(margins) == 3, f"primary seed count drift: {mode}")
        require(all(close(item["normalized_margin"], expected_margins[mode], 0.0) for item in margins), f"primary margin drift: {mode}")
        require(all(item["selected_comparator_subset"] == expected_comparators[mode] for item in margins), f"primary comparator drift: {mode}")
    dispositions = analysis["mode_dispositions"]
    require(dispositions["history_carried"]["supported"] is True, "history support absent")
    require(dispositions["state_carried"]["supported"] is False, "state unexpectedly supported")
    require(dispositions["hybrid"]["supported"] is False, "hybrid unexpectedly supported")
    require(all(analysis["controls"]["history_carried"]["common"]["operation_necessity"].values()), "history operation necessity failed")
    require(all(analysis["controls"]["history_carried"]["discriminator"].values()), "history discriminator failed")
    require(all(analysis["controls"]["hybrid"]["discriminator"].values()), "hybrid factorial discriminator failed")
    require(all(analysis["controls"]["state_carried"]["discriminator"].values()), "state discriminator failed")

    mode_counts = Counter(item["response_envelope"]["i04r1_response_record"]["mode"] for item in receipts)
    require(mode_counts == Counter({"hybrid": 34, "history_carried": 33, "state_carried": 32}), "mode arm counts drifted")
    operation_packets = sum(len(item["operation_receipts"]) for item in receipts)
    materialization_packets = sum(bool(item["history_materialization"] and item["history_materialization"]["packet_scheduled"]) for item in receipts)
    intervention_packets = sum(item["state_intervention"] is not None for item in receipts)
    response_packets = sum(item["response_receipt"]["scheduled"] for item in receipts)
    controller_responses = sum(item["response_receipt"]["controller_authored"] for item in receipts)
    packet_count = sum(item["resource_receipt"]["packet_count"] for item in receipts)
    history_tokens = sum(len(item["history_receipt"]["tokens"]) for item in receipts)
    require((operation_packets, materialization_packets, intervention_packets) == (297, 55, 6), "operation/materialization/intervention counts drifted")
    require((response_packets, controller_responses, packet_count, history_tokens) == (27, 3, 484, 111), "response/packet/history counts drifted")

    for mode in ("state_carried", "history_carried", "hybrid"):
        one_source = next(item for item in receipts if item["arm_id"] == f"control:{mode}:one_source")
        require(len({operation["participant_lineage"] for operation in one_source["operation_receipts"]}) == 1, f"one-source lineage drift: {mode}")
        for rotation in ("rotation_B", "rotation_C"):
            arm = next(item for item in receipts if item["arm_id"] == f"control:{mode}:{rotation}")
            require(len({operation["participant_lineage"] for operation in arm["operation_receipts"]}) == 3, f"rotation lineage drift: {mode}/{rotation}")

    require(runtime["runtime_invocation_count"] == 1 and runtime["scientific_retry_count"] == 0, "replacement attempt counts drifted")
    require(runtime["graph_repository_mutation_count"] == 0, "graph mutation recorded")
    require(corrected["reconstruction"] == {
        "runtime_generation_count": 0,
        "PyGRC_import_count": 0,
        "model_count": 0,
        "producer_count": 0,
        "arm_count": 0,
        "retained_aggregate_read_count": 1,
        "corrected_analysis_generation_count": 1,
    }, "corrected reconstruction counts drifted")
    require(
        subprocess.run(["git", "-C", str(ROOT.parent / "graph-reflexive-coherence"), "status", "--porcelain=v1", "--untracked-files=all"], check=True, capture_output=True, text=True).stdout.strip() == "",
        "graph worktree dirty at closeout validation",
    )
    pure_sources = (
        "scripts/p2_i2_app_b_analysis.py",
        "scripts/p2_i2_app_b_reconstruct.py",
        "scripts/p2_i2_app_b_corrected_closeout.py",
        "scripts/p2_i2_app_b_closeout_validate.py",
    )
    for relative in pure_sources:
        tree = ast.parse((ROOT / EXPERIMENT_REL / relative).read_text(encoding="utf-8"))
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        require(
            all(not ((isinstance(node, ast.Import) and any(alias.name.startswith("pygrc") for alias in node.names)) or (isinstance(node, ast.ImportFrom) and str(node.module).startswith("pygrc"))) for node in imports),
            f"PyGRC import in pure closeout source: {relative}",
        )

    result = {
        "artifact_id": "P2-I2-APP-B2-CLOSEOUT-VALIDATION",
        "status": "passed_owner_result_review_pending",
        "checks": {
            "canonical_and_digest_inputs": 3,
            "fresh_processes_and_models": 99,
            "accepted_response_envelopes": 99,
            "operationally_valid_arms": 99,
            "matrix_complete": True,
            "corrected_analysis_reconstructed": True,
            "supported_modes": analysis["supported_modes"],
            "primary_margins": expected_margins,
            "mode_arm_counts": dict(mode_counts),
            "operation_packets": operation_packets,
            "materialization_packets": materialization_packets,
            "state_intervention_packets": intervention_packets,
            "response_packets": response_packets,
            "controller_responses": controller_responses,
            "total_native_packets": packet_count,
            "history_tokens": history_tokens,
            "save_load_reset_receipts": 99,
            "graph_clean": True,
            "pure_closeout_sources": len(pure_sources),
            "portable_retained_artifacts": True,
            "blocked_claims_retained": analysis["blocked_claims"],
        },
        "process_counts": {
            "replacement_campaign_parents": 1,
            "replacement_child_processes": 99,
            "replacement_fresh_models": 99,
            "replacement_child_retries": 0,
            "original_reconstruction_processes": 1,
            "corrected_closeout_processes": 1,
            "closeout_validation_processes_this_start": 1,
            "closeout_PyGRC_imports_models_arms_responses": [0, 0, 0, 0],
        },
        "terminal": {
            "classification": analysis["terminal_classification"],
            "bounded_claim": analysis["bounded_claim"],
            "owner_acceptance_required": True,
            "result_commit_authorized": False,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    if output is not None:
        require(not output.exists(), "closeout validation output already exists")
        output.write_bytes(canonical_bytes(result))
        require(load_json(output) == result, "closeout validation readback drifted")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--original-reconstruction", required=True)
    parser.add_argument("--corrected", required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one validation mode")
    values = (args.freeze, args.runtime, args.original_reconstruction, args.corrected, args.output)
    for value in values:
        if value is not None:
            require(not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute(), "absolute path refused")
    result = validate(
        ROOT / args.freeze,
        ROOT / args.runtime,
        ROOT / args.original_reconstruction,
        ROOT / args.corrected,
        None if args.check_only else ROOT / args.output,
    )
    print(json.dumps({"status": result["status"], "supported_modes": result["checks"]["supported_modes"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
