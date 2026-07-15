#!/usr/bin/env python3
"""Candidate-free static and pure-arithmetic validation for Appendix B."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys
import tempfile
from types import SimpleNamespace
from typing import Any, Mapping

import p2_i2_i04r2_analysis as accepted
from p2_i2_app_b_analysis import build_arm_registry, digest_value, strongest_proper_subset_margin
from p2_i2_app_b_history_adapter import RCAEAppendixBHistoryAdapter


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
FREEZE = EXPERIMENT / "contracts/p2-i2/app-b1-runtime-input-freeze.json"
MACHINE = EXPERIMENT / "configs/p2_i2_i04r2_machine_policy.json"
PARENT = EXPERIMENT / "configs/p2_i2_i04r1_analysis_policy.json"


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
    absolute = [token for token in tokens if PurePosixPath(token).is_absolute() or PureWindowsPath(token).is_absolute()]
    require(not absolute, f"absolute path in {field}: {absolute}")
    require(not re.findall(r"\b[A-Z][A-Z0-9_]*_ROOT\b", value), f"root placeholder in {field}")


def synthetic_envelope(mode: str, seed: int, subset: str, response: float) -> dict[str, Any]:
    record_id = f"pure:{mode}:{seed}:{subset}"
    observed = response > 0.0
    packet = f"{record_id}:packet" if observed else None
    departure = f"{record_id}:departure" if observed else None
    arrival = f"{record_id}:arrival" if observed else None
    receipt = hashlib.sha256(f"receipt:{record_id}".encode()).hexdigest()
    return {
        "i04r1_response_record": {
            "record_id": record_id,
            "mode": mode,
            "seed": seed,
            "physical_order_id": "q1_then_q2",
            "cell_id": "pure-eight-arm-test",
            "branch_id": subset,
            "pairing_identity": f"pure:{mode}:{seed}",
            "opportunity_id": "pure-opportunity",
            "response_id": "fixed_window_native_B_target_coherence_gain",
            "unit": "native_coherence_amount",
            "status": "observed_response" if observed else "scientific_no_response",
            "B_before": 4.25,
            "B_after": 4.25 + response,
            "raw_response": response,
            "oriented_response": response,
            "carrier_state_digest": hashlib.sha256(record_id.encode()).hexdigest(),
            "window_protocol_id": "p2-i2-native-response-window-v2",
            "pre_packet_queue_length": 0,
            "pre_birth_queue_length": 0,
            "post_packet_queue_length": 0,
            "post_birth_queue_length": 0,
            "feedback_surface_call_count": 1,
            "producer_call_count": 1,
            "step_call_count": 2,
            "step_processed_event_kinds": ["packet_departure", "packet_arrival"] if observed else ["event_queue_empty", "event_queue_empty"],
            "producer_reason": "pure_scheduled" if observed else "pure_blocked",
            "response_packet_id": packet,
            "departure_event_id": departure,
            "arrival_event_id": arrival,
            "response_packet_amount": response if observed else None,
            "runtime_tolerance": 2.842170943040401e-14,
            "B_targeting_event_ids": [arrival] if observed else [],
            "native_chain_evidence_refs": [receipt, departure, arrival] if observed else [],
            "operational_failure_id": None,
        },
        "window_validity_receipt": {
            "feedback_evaluation_id": f"{record_id}:feedback",
            "feedback_policy_id": "pure-policy",
            "producer_invocation_id": f"{record_id}:producer",
            "producer_invocation_receipt_sha256": receipt,
            "pre_queue_identity_sha256": hashlib.sha256(f"pre:{record_id}".encode()).hexdigest(),
            "post_queue_identity_sha256": hashlib.sha256(f"post:{record_id}".encode()).hexdigest(),
            "step_processed_event_ids": [departure, arrival],
            "window_contamination_event_ids": [],
        },
        "arrival_gain_receipt": {
            "native_coherence_domain_id": "pure-[0,9.25]",
            "native_coherence_domain_lower": 0.0,
            "native_coherence_domain_upper": 9.25,
            "expected_native_arrival_gain": response,
            "arrival_transform_id": "identity_packet_amount_addition" if observed else "no_arrival",
            "arrival_semantics_source_sha256": accepted.ARRIVAL_SOURCE_SHA256,
            "arrival_semantics_receipt_sha256": receipt,
            "arrival_adjustment_event_ids": [],
        },
    }


class FakeModel:
    def __init__(self, rows: list[Any]) -> None:
        self._state = SimpleNamespace(causal_pulse_substrate_surface_log=rows)

    def get_state(self) -> Any:
        return self._state


def adapter_test() -> dict[str, Any]:
    registry = [
        {"operation": "G", "source_node_id": 0, "target_node_id": 2, "edge_id": 0, "amount": 0.625},
        {"operation": "E", "source_node_id": 2, "target_node_id": 5, "edge_id": 4, "amount": 0.4375},
        {"operation": "P", "source_node_id": 1, "target_node_id": 2, "edge_id": 1, "amount": 0.875},
    ]
    adapter = RCAEAppendixBHistoryAdapter(
        carrier_id="pure-adapter-test",
        pool_target_node_id=2,
        registered_source_node_ids=[0, 1, 2],
        readout_node_id=8,
        positive_reservoir_node_id=9,
        negative_sink_node_id=10,
        positive_edge_id=7,
        negative_edge_id=8,
        recency_coefficient=0.375,
        materialization_tolerance=2.842170943040401e-14,
        operation_registry=registry,
    )
    rows = [
        SimpleNamespace(
            surface_kind="route_local_pulse_contact",
            pulse_event_kind="lgrc9v3_packet_arrival",
            source_node_id=item["source_node_id"],
            target_node_id=item["target_node_id"],
            pulse_channel_id=f"edge:{item['edge_id']}",
            contact_amount=item["amount"],
            event_time_key=10.875 + 1.25 * index,
            surface_digest=hashlib.sha256(f"row:{index}".encode()).hexdigest(),
        )
        for index, item in enumerate(registry)
    ]
    rows.append(
        SimpleNamespace(
            surface_kind="route_local_pulse_contact",
            pulse_event_kind="lgrc9v3_packet_arrival",
            source_node_id=0,
            target_node_id=3,
            pulse_channel_id="edge:2",
            contact_amount=0.625,
            event_time_key=14.0,
            surface_digest=hashlib.sha256(b"diversion").hexdigest(),
        )
    )
    appended = adapter.ingest_new_rows(FakeModel(rows))
    require([item["physical_operation"] for item in appended] == ["G", "E", "P"], "route classification drifted")
    require(all(not item["source_label_retained"] and not item["actor_identity_retained"] for item in appended), "source label leaked")
    expected = 0.375 * (0.375 * 0.625 + 0.4375) + 0.875
    require(math.isclose(adapter.readout(), expected, rel_tol=0.0, abs_tol=0.0), "history fold drifted")
    before = adapter.restoration_identity_digest()
    with tempfile.TemporaryDirectory(prefix="app-b-pure-") as directory:
        path = Path(directory) / "adapter.json"
        adapter.save(path)
        loaded = RCAEAppendixBHistoryAdapter.load(path)
        require(loaded.restoration_identity_digest() == before, "adapter load identity drifted")
        loaded.reset()
        require(list(loaded.tokens) == [], "adapter reset baseline drifted")
    return {
        "admitted_operations": [item["physical_operation"] for item in appended],
        "diversion_admitted": False,
        "readout": expected,
        "save_load_identity": True,
        "reset_to_empty": True,
    }


def validate(output: Path | None) -> dict[str, Any]:
    freeze = load_json(FREEZE)
    assert_portable(freeze)
    for item in freeze["authority_inputs"]:
        require(sha256(ROOT / item["path"]) == item["sha256"], f"authority drift: {item['path']}")
    for relative, expected in freeze["implementation_sha256"].items():
        require(sha256(ROOT / relative) == expected, f"implementation drift: {relative}")
    rows = build_arm_registry(freeze["arm_registry_specification"])
    require(len(rows) == 99 and len({row["arm_id"] for row in rows}) == 99, "arm registry incomplete")
    require(digest_value(rows) == freeze["arm_registry_specification"]["expanded_registry_digest"], "registry digest drifted")
    counts = {
        "primary": sum(row["arm_kind"] == "primary_subset" for row in rows),
        "common_controls": sum(row["arm_kind"] == "common_control" for row in rows),
        "mode_discriminators": sum(row["arm_kind"] == "mode_discriminator" for row in rows),
    }
    require(counts == {"primary": 72, "common_controls": 21, "mode_discriminators": 6}, "arm class count drifted")

    machine = load_json(MACHINE)
    parent = load_json(PARENT)
    envelopes = {
        subset: synthetic_envelope("history_carried", 101, subset, 0.125 if subset == "GEP" else 0.0)
        for subset in freeze["arm_registry_specification"]["subsets"]
    }
    margin = strongest_proper_subset_margin(envelopes, machine, parent, delta=1e-12)
    require(margin["primary_passed"] and margin["selected_comparator_subset"] == "reference", "eight-arm estimator failed")
    incomplete_refused = False
    try:
        strongest_proper_subset_margin(dict(list(envelopes.items())[:-1]), machine, parent, delta=1e-12)
    except accepted.ContractError:
        incomplete_refused = True
    require(incomplete_refused, "incomplete eight-arm tuple accepted")
    cross_seed = deepcopy(envelopes)
    cross_seed["GP"]["i04r1_response_record"]["seed"] = 211
    cross_seed_refused = False
    try:
        strongest_proper_subset_margin(cross_seed, machine, parent, delta=1e-12)
    except accepted.ContractError:
        cross_seed_refused = True
    require(cross_seed_refused, "cross-seed max accepted")

    thresholds = freeze["mode_realizations"]
    history_full = 0.375 * (0.375 * 0.625 + 0.4375) + 0.875 - 0.25 - 0.0625
    history_gp = 0.375 * 0.625 + 0.875 - 0.25 - 0.0625
    require(thresholds["history_carried"]["feedback_threshold"] == (history_full + history_gp) / 2.0, "history threshold derivation drifted")
    hybrid_full = 1.8125 + 1.126953125 - 0.25 - 0.0625
    hybrid_single = 0.75 + 1.126953125 - 0.25 - 0.0625
    require(thresholds["hybrid"]["feedback_threshold"] == (hybrid_full + hybrid_single) / 2.0, "hybrid threshold derivation drifted")

    adapter = adapter_test()
    source_files = [ROOT / relative for relative in freeze["implementation_sha256"]]
    static_guard: dict[str, Any] = {}
    forbidden = "app" + "_a"
    forbidden_dash = "app" + "-a"
    for path in source_files:
        source = path.read_text(encoding="utf-8")
        lowered = source.lower()
        require(forbidden not in lowered and forbidden_dash not in lowered, f"outcome-quarantine source reference: {path.name}")
        ast.parse(source)
        static_guard[path.name] = {"prior_appendix_reference_absent": True, "syntax_valid": True}
    runner_tree = ast.parse((EXPERIMENT / "scripts/p2_i2_app_b_run.py").read_text(encoding="utf-8"))
    module_imports = [node for node in runner_tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    require(all(not (isinstance(node, ast.Import) and any(alias.name == "pygrc" for alias in node.names)) for node in module_imports), "parent runner imports PyGRC")
    claim = ROOT / freeze["execution"]["claim_path"]
    governed = ROOT / freeze["execution"]["output_path"]
    require(not claim.exists() and not governed.exists(), "runtime output exists during candidate-free validation")
    result = {
        "artifact_id": "P2-I2-APP-B1-CANDIDATE-FREE-VALIDATION",
        "status": "passed_runtime_not_started",
        "checks": {
            "authority_hashes": len(freeze["authority_inputs"]),
            "implementation_hashes": len(freeze["implementation_sha256"]),
            "portable_freeze": True,
            "arm_registry": {"count": len(rows), "class_counts": counts, "digest": digest_value(rows)},
            "pure_estimator": {"positive_margin": margin["normalized_margin"], "incomplete_refused": incomplete_refused, "cross_seed_refused": cross_seed_refused},
            "threshold_derivations": True,
            "adapter_pure_conformance": adapter,
            "static_outcome_quarantine": static_guard,
            "parent_imports_pygrc": False,
            "claim_absent": True,
            "governed_output_absent": True,
        },
        "execution_counts": {
            "PyGRC_model_instantiations": 0,
            "candidate_arms": 0,
            "control_arms": 0,
            "campaign_claims": 0,
            "scientific_outputs": 0,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    if output is not None:
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        require(load_json(output) == result, "validation readback drifted")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one validation mode")
    result = validate(None if args.check_only else ROOT / args.output)
    print(json.dumps({"status": result["status"], "checks": len(result["checks"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
