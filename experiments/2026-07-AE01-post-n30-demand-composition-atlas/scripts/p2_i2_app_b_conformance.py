#!/usr/bin/env python3
"""Response-free PyGRC conformance for the frozen Appendix B realizations."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
import tempfile
from typing import Any

from p2_i2_app_b_analysis import canonical_bytes, digest_value
from p2_i2_app_b_run import _appendix_adapter, _pair_identity, _schedule_packet, load_json


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
REGISTRATION_REL = f"{EXPERIMENT_REL}/contracts/p2-i2/i06-three-mode-registration.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def exercise(mode: str, graph_root: Path) -> dict[str, Any]:
    graph_source = graph_root / "src"
    if str(graph_source) not in sys.path:
        sys.path.insert(0, str(graph_source))
    import pygrc
    from pygrc.models import LGRC9V3
    from p2_i2_app_b_history_adapter import RCAEAppendixBHistoryAdapter
    from p2_i2_i06_registration import _build_model

    require(Path(pygrc.__file__).resolve().is_relative_to(graph_source.resolve()), "PyGRC import drifted")
    registration = load_json(ROOT / REGISTRATION_REL)
    model, roles, edges, _ = _build_model(registration, mode)
    adapter = None if mode == "state_carried" else _appendix_adapter(registration, mode, roles, edges)
    model.rebase_reset_baseline()
    baseline = _pair_identity(registration, mode, model, adapter, roles, edges)["digest"]
    routes = [
        ("G", "S1", "P", "S1_TO_P", 0.625),
        ("E", "P", "K_P", "P_TO_K_P", 0.4375),
        ("P", "S2", "P", "S2_TO_P", 0.875),
    ]
    admissions: list[dict[str, Any]] = []
    operation_receipts: list[dict[str, Any]] = []
    for index, (operation, source, target, edge, amount) in enumerate(routes):
        receipt = _schedule_packet(
            model,
            roles,
            edges,
            source_role=source,
            target_role=target,
            edge_role=edge,
            amount=amount,
            departure=10.25 + 1.25 * index,
            arrival=10.875 + 1.25 * index,
            scheduler_index=20 + index,
            packet_index=20 + index,
            lineage=f"app-b-conformance:{mode}:slot-{index}",
        )
        operation_receipts.append({"operation": operation, **receipt})
        if adapter is not None:
            admissions.extend(adapter.ingest_new_rows(model))
    materialization = None
    if adapter is not None:
        require([item["physical_operation"] for item in admissions] == ["G", "E", "P"], "history route admission drifted")
        expected = 1.126953125
        require(math.isclose(adapter.readout(), expected, rel_tol=0.0, abs_tol=0.0), "history fold drifted")
        materialization = adapter.materialize_readout(
            model,
            departure_event_time_key=14.0,
            arrival_event_time_key=14.625,
            scheduler_event_index=23,
            packet_index=23,
        )
        require(math.isclose(materialization["readout_after"], expected, rel_tol=0.0, abs_tol=2.842170943040401e-14), "materialization drifted")
    current = _pair_identity(registration, mode, model, adapter, roles, edges)["digest"]
    with tempfile.TemporaryDirectory(prefix="app-b-conformance-") as directory:
        native = Path(directory) / "native.json"
        history = Path(directory) / "history.json"
        model.save(str(native))
        if adapter is not None:
            adapter.save(history)
        loaded_model = LGRC9V3.load(str(native))
        loaded_adapter = None if adapter is None else RCAEAppendixBHistoryAdapter.load(history)
        loaded = _pair_identity(registration, mode, loaded_model, loaded_adapter, roles, edges)["digest"]
        require(loaded == current, "save/load identity drifted")
        loaded_model.reset()
        if loaded_adapter is not None:
            loaded_adapter.reset()
        reset = _pair_identity(registration, mode, loaded_model, loaded_adapter, roles, edges)["digest"]
        require(reset == baseline, "reset identity drifted")
    return {
        "mode": mode,
        "baseline_identity": baseline,
        "operation_event_pairs": 3,
        "operation_budget_errors": [item["max_abs_budget_error"] for item in operation_receipts],
        "admitted_history_operations": [item["physical_operation"] for item in admissions],
        "materialization": materialization,
        "save_load_identity": True,
        "reset_identity": True,
        "feedback_surface_calls": 0,
        "producer_calls": 0,
        "response_packets": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    for value in (args.graph_root, args.output):
        require(not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute(), "absolute path refused")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    graph_root = (ROOT / args.graph_root).resolve()
    rows = [exercise(mode, graph_root) for mode in ("state_carried", "history_carried", "hybrid")]
    result = {
        "artifact_id": "P2-I2-APP-B1-RESPONSE-FREE-RUNTIME-CONFORMANCE",
        "status": "passed_no_scientific_response_invoked",
        "modes": rows,
        "execution_counts": {
            "process_starts": 1,
            "fresh_models": 3,
            "operation_packets": 9,
            "materialization_packets": 2,
            "feedback_surface_calls": 0,
            "producer_calls": 0,
            "response_packets": 0,
            "candidate_response_tuples": 0,
            "control_response_tuples": 0,
        },
        "evidence_effect": "implementation_conformance_only_not_Appendix_B_result",
    }
    result["canonical_payload_digest"] = digest_value(result)
    output = ROOT / args.output
    require(not output.exists(), "conformance output already exists")
    output.write_bytes(canonical_bytes(result))
    require(load_json(output) == result, "conformance readback drifted")
    print(json.dumps({"status": result["status"], "modes": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
