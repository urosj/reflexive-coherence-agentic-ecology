"""Pure, zero-PyGRC tests for the P2-I3 B-R conformance implementation."""

from __future__ import annotations

import ast
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = (
    ROOT
    / "experiments"
    / "2026-07-AE01-post-n30-demand-composition-atlas"
    / "scripts"
)
RUNTIME = SCRIPTS / "p2_i3_br_runtime.py"
HARNESS = SCRIPTS / "p2_i3_i03_br_conform.py"


def load_runtime():
    spec = importlib.util.spec_from_file_location("p2_i3_br_runtime_under_test", RUNTIME)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime = load_runtime()


def policy_binding() -> dict:
    return {
        "policy_id": "policy",
        "route_id": "route",
        "source_node_id": 6,
        "destination_node_id": 7,
        "edge_id": 6,
        "export_floor": 0.4,
        "export_cap": 0.1,
        "absolute_tolerance": 1e-12,
        "schedule_by_sequence": {
            "0": {
                "departure_event_time_key": 8.0,
                "arrival_event_time_key": 9.0,
                "scheduler_event_index": 8,
                "packet_index": 4,
                "source_lineage_id": "export-0",
                "target_lineage_id": "reservoir",
            },
            "1": {
                "departure_event_time_key": 10.0,
                "arrival_event_time_key": 11.0,
                "scheduler_event_index": 10,
                "packet_index": 5,
                "source_lineage_id": "export-1",
                "target_lineage_id": "reservoir",
            },
        },
    }


def receipt(state: dict, receipt_id: str, sequence: int, predecessor: str) -> dict:
    return {
        "schema": runtime.RECEIPT_SCHEMA,
        "receipt_id": receipt_id,
        "route_id": state["route_id"],
        "sequence_index": sequence,
        "qualifying_native_event_identity": f"event-{sequence}",
        "predecessor_composite_identity": predecessor,
        "policy_id": state["policy_id"],
        "source_node_id": state["source_node_id"],
        "destination_node_id": state["destination_node_id"],
        "edge_id": state["edge_id"],
        "prior_settlement_status": "settled",
        "eligible": True,
    }


def test_runtime_module_has_no_pygrc_or_blocked_native_calls() -> None:
    tree = ast.parse(RUNTIME.read_text(encoding="utf-8"))
    imports = []
    called_attributes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            called_attributes.append(node.func.attr)
    assert not any(name == "pygrc" or name.startswith("pygrc.") for name in imports)
    assert "set_state" not in called_attributes
    assert "rebase_reset_baseline" not in called_attributes
    assert "apply_continuity" not in called_attributes
    assert not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules)


def test_export_policy_serializes_positive_pending_settlement_zero_and_duplicate() -> None:
    initial = runtime.initial_policy_state(policy_binding())
    first = receipt(initial, "r0", 0, "parent-0")
    positive = runtime.evaluate_export_policy(
        carrier_coherence=0.5,
        receipt=first,
        predecessor_composite_identity="parent-0",
        policy_state=initial,
    )
    assert positive["disposition"] == "eligible_positive"
    assert positive["reserved_amount"] == pytest.approx(0.1)
    assert positive["native_request"]["source_node_id"] == 6
    assert positive["native_request"]["target_node_id"] == 7
    assert positive["native_mutation_authored"] is False

    pending = positive["policy_state"]
    second = receipt(pending, "r1", 1, "parent-1")
    blocked = runtime.evaluate_export_policy(
        carrier_coherence=0.4,
        receipt=second,
        predecessor_composite_identity="parent-1",
        policy_state=pending,
    )
    assert blocked["reason"] == "prior_export_not_settled"
    assert blocked["policy_state"] == pending

    settled = runtime.settle_export_policy(
        pending, receipt_id="r0", native_settlement_identity="native-settled"
    )
    zero = runtime.evaluate_export_policy(
        carrier_coherence=0.4,
        receipt=second,
        predecessor_composite_identity="parent-1",
        policy_state=settled,
    )
    assert zero["disposition"] == "eligible_zero"
    assert zero["native_request"] is None
    assert zero["policy_state"]["next_sequence_index"] == 2

    duplicate = runtime.evaluate_export_policy(
        carrier_coherence=0.4,
        receipt=first,
        predecessor_composite_identity="parent-1",
        policy_state=zero["policy_state"],
    )
    assert duplicate["disposition"] == "duplicate_consumed"
    assert duplicate["policy_state"] == zero["policy_state"]


def test_export_policy_invalid_receipt_is_exact_noop() -> None:
    initial = runtime.initial_policy_state(policy_binding())
    invalid = receipt(initial, "bad", 0, "parent")
    invalid["route_id"] = "other"
    result = runtime.evaluate_export_policy(
        carrier_coherence=0.5,
        receipt=invalid,
        predecessor_composite_identity="parent",
        policy_state=initial,
    )
    assert result["disposition"] == "invalid"
    assert result["policy_state"] == initial
    assert result["native_request"] is None


def test_blind_adapter_accepts_structure_only_and_fails_on_extra_field() -> None:
    opportunity = {
        "opportunity_id": "o",
        "parent_composite_identity": "parent",
        "source_node_id": 1,
        "target_node_id": 3,
        "edge_id": 2,
        "amount": 0.45,
        "departure_event_time_key": 12.0,
        "arrival_event_time_key": 13.0,
        "scheduler_event_index": 12,
        "packet_index": 6,
        "source_lineage_id": "probe",
        "target_lineage_id": "continuation",
    }
    request = runtime.build_blind_encounter_request(
        opportunity=opportunity, parent_composite_identity="parent"
    )
    assert set(request) == set(opportunity) - {
        "opportunity_id",
        "parent_composite_identity",
    }
    forbidden = deepcopy(opportunity)
    forbidden["carrier_coherence"] = 0.5
    with pytest.raises(runtime.BRContractError):
        runtime.build_blind_encounter_request(
            opportunity=forbidden, parent_composite_identity="parent"
        )


class FakeModel:
    def __init__(self, identity: str) -> None:
        self.identity = identity

    def save(self, path: str) -> None:
        Path(path).write_text(
            json.dumps({"identity": self.identity}, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def test_composite_validates_all_components_before_native_load(tmp_path: Path) -> None:
    model = FakeModel("native")
    policy = runtime.initial_policy_state(policy_binding())
    branch = runtime.make_branch_state(
        branch_id="branch", parent_composite_identity="parent", opportunity_id="opportunity"
    )
    reset = runtime.make_reset_state(
        reset_id="reset", baseline_composite_identity="baseline"
    )
    audit = runtime.make_audit_state(lineage=["one", "two"])
    directory = tmp_path / "complete"
    manifest = runtime.save_composite(
        directory,
        model=model,
        native_digest=lambda item: item.identity,
        policy_state=policy,
        branch_state=branch,
        reset_state=reset,
        audit_state=audit,
    )
    bindings = manifest["bindings"]
    load_count = 0

    def loader(path: str) -> FakeModel:
        nonlocal load_count
        load_count += 1
        return FakeModel(json.loads(Path(path).read_text(encoding="utf-8"))["identity"])

    loaded = runtime.load_composite(
        directory,
        native_loader=loader,
        native_digest=lambda item: item.identity,
        expected_bindings=bindings,
    )
    assert load_count == 1
    assert loaded["manifest"]["exact_composite_identity"] == manifest["exact_composite_identity"]

    (directory / "policy.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(runtime.BRContractError):
        runtime.load_composite(
            directory,
            native_loader=loader,
            native_digest=lambda item: item.identity,
            expected_bindings=bindings,
        )
    assert load_count == 1


def test_q13_and_control_interfaces_remain_distinct_and_result_free() -> None:
    constructors = runtime.build_q13_constructor_records()
    assert tuple(row["contrast_id"] for row in constructors) == runtime.Q13_CONTRAST_IDS
    assert len({row["meaning"] for row in constructors}) == 3

    controls = runtime.build_control_interface_records(carrier_value=0.5)
    assert tuple(row["control_id"] for row in controls) == runtime.CONTROL_INTERFACE_IDS
    assert len({row["operation"] for row in controls}) == len(controls)
    assert all("outcome" not in row and "passed" not in row for row in controls)
    relocation = controls[0]
    assert set(relocation["payload"]) == {
        "source_binding",
        "target_binding",
        "carrier_coherence",
    }


def test_rcae_reset_restores_independent_baseline_components() -> None:
    policy = runtime.initial_policy_state(policy_binding())
    branch = runtime.make_branch_state(
        branch_id="baseline", parent_composite_identity="parent", opportunity_id="none"
    )
    reset = runtime.make_reset_state(
        reset_id="reset", baseline_composite_identity="parent"
    )
    audit = runtime.make_audit_state(lineage=["constructed"])
    restored = runtime.reset_rcae_components(
        baseline_policy_state=policy,
        baseline_branch_state=branch,
        baseline_reset_state=reset,
        baseline_audit_state=audit,
    )
    restored["policy"]["next_sequence_index"] = 9
    restored["audit"]["lineage"].append("changed")
    assert policy["next_sequence_index"] == 0
    assert audit["lineage"] == ["constructed"]


def test_harness_is_syntax_valid_and_keeps_scientific_flags_false() -> None:
    source = HARNESS.read_text(encoding="utf-8")
    ast.parse(source)
    assert '"candidate_execution": False' in source
    assert '"calibration_execution": False' in source
    assert '"scientific_control_execution": False' in source
    assert '"scientific_interpretation": False' in source
    assert "FREEZE_SOURCE_ANCHOR" in source
