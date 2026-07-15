#!/usr/bin/env python3
"""Additive retained-only operational projection correction for APP-B2."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
from typing import Any

from p2_i2_app_b_analysis import analyze_receipts, canonical_bytes, digest_value


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--original-reconstruction", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    for value in (args.freeze, args.runtime, args.original_reconstruction, args.output):
        require(not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute(), "absolute path refused")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "closeout not invoked through lexical repository .venv")
    freeze = load_json(ROOT / args.freeze)
    runtime = load_json(ROOT / args.runtime)
    original_reconstruction = load_json(ROOT / args.original_reconstruction)
    require((ROOT / args.runtime).read_bytes() == canonical_bytes(runtime), "runtime aggregate not canonical")
    require(
        digest_value({key: value for key, value in runtime.items() if key != "canonical_payload_digest"})
        == runtime["canonical_payload_digest"],
        "runtime aggregate digest drifted",
    )
    require(original_reconstruction["analysis"] == runtime["analysis"], "original reconstruction no longer matches embedded analysis")
    original = runtime["analysis"]
    require(original["matrix_complete"] is False, "historical projection defect is not present")
    require(original["all_arms_operationally_valid"] is False, "historical all-arm defect is not present")
    corrected = analyze_receipts(
        runtime["receipts"],
        freeze,
        load_json(ROOT / MACHINE_REL),
        load_json(ROOT / PARENT_REL),
    )
    require(corrected["matrix_complete"] is True, "corrected matrix remains incomplete")
    require(corrected["all_arms_operationally_valid"] is True, "corrected arms remain invalid")
    require(corrected["primary_results"] == original["primary_results"], "primary estimator result changed")
    require(corrected["controls"] == original["controls"], "control result changed")
    require(corrected["supported_modes"] == ["history_carried"], "corrected supported-mode set drifted")
    result = {
        "artifact_id": "P2-I2-APP-B2-CORRECTED-ANALYSIS-AND-CLOSEOUT",
        "artifact_version": "1.0",
        "status": "retained_only_projection_corrected_owner_review_pending",
        "inputs": {
            "freeze": {"path": args.freeze, "sha256": sha256(ROOT / args.freeze)},
            "runtime": {"path": args.runtime, "sha256": sha256(ROOT / args.runtime)},
            "original_reconstruction": {
                "path": args.original_reconstruction,
                "sha256": sha256(ROOT / args.original_reconstruction),
            },
            "original_analysis_source_sha256": "63804bc70e412a76813cda49455c9b72e8e2fe83589f3816ac842d3a7861cb8b",
            "corrected_analysis_source_sha256": sha256(
                ROOT / f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_analysis.py"
            ),
        },
        "historical_projection_disposition": {
            "runtime_bytes_changed": False,
            "original_reconstruction_bytes_changed": False,
            "original_matrix_complete": original["matrix_complete"],
            "original_all_arms_operationally_valid": original["all_arms_operationally_valid"],
            "original_terminal_had_conclusion_authority": False,
            "defects": [
                "reduced flattened-event-list expectation ignored registered PyGRC surface/local-update events",
                "last packet-ledger record was incorrectly treated as append-ordered operation identity",
                "terminal support was not gated on matrix completeness and all-arm operational validity",
            ],
        },
        "correction_boundary": {
            "native_step_bookkeeping_is_event_authority": True,
            "frozen_route_and_amount_registry_is_operation_authority": True,
            "legacy_last_ledger_packet_projection_authoritative": False,
            "matrix_and_all_arm_validity_gate_supported_modes": True,
            "response_values_changed": False,
            "estimator_values_changed": False,
            "control_values_changed": False,
        },
        "corrected_analysis": corrected,
        "reconstruction": {
            "runtime_generation_count": 0,
            "PyGRC_import_count": 0,
            "model_count": 0,
            "producer_count": 0,
            "arm_count": 0,
            "retained_aggregate_read_count": 1,
            "corrected_analysis_generation_count": 1,
        },
        "owner_boundary": {
            "result_acceptance_required": True,
            "result_commit_authorized": False,
            "cross_appendix_recurrence_claimed": False,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    output = ROOT / args.output
    require(not output.exists(), "corrected closeout already exists")
    output.write_bytes(canonical_bytes(result))
    require(load_json(output) == result, "corrected closeout readback drifted")
    print(
        json.dumps(
            {
                "status": result["status"],
                "matrix_complete": corrected["matrix_complete"],
                "supported_modes": corrected["supported_modes"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
