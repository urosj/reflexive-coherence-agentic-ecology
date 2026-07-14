"""No-model closeout validator for the P2-I2-I06 owner review."""

from __future__ import annotations

import argparse
import ast
from copy import deepcopy
import hashlib
import inspect
import itertools
import json
import math
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import textwrap
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from p2_i2_i03b_history_adapter import (  # noqa: E402
    PACKET_ARRIVAL,
    ROUTE_LOCAL_CONTACT,
    RCAEActiveHistoryAdapterV1,
)
from p2_i2_i06_history_adapter import RCAEActiveHistoryAdapterV2  # noqa: E402


FREEZE_PATH = EXPERIMENT / "contracts/p2-i2/i06a-registration-review-input-freeze.json"
POLICY_PATH = EXPERIMENT / "contracts/p2-i2/i06a-registration-review-policy.json"
REGISTRATION_PATH = EXPERIMENT / "contracts/p2-i2/i06-three-mode-registration.json"
EXECUTION_MANIFEST_PATH = (
    EXPERIMENT / "contracts/p2-i2/i06-registration-execution-manifest.json"
)
POST_PORTABILITY_MANIFEST_PATH = (
    EXPERIMENT
    / "contracts/p2-i2/i06-registration-post-portability-manifest.json"
)
HISTORICAL_VALIDATION_PATH = (
    EXPERIMENT / "contracts/p2-i2/i06-registration-validation.json"
)
CURRENT_VALIDATOR_PATH = EXPERIMENT / "scripts/p2_i2_i06_registration.py"
I03B_RUNTIME_PATH = (
    EXPERIMENT / "contracts/p2-i2/i03b-history-carried-runtime-conformance.json"
)
I03C_RUNTIME_PATH = (
    EXPERIMENT / "contracts/p2-i2/i03c-hybrid-runtime-conformance.json"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"JSON object required: {path.name}")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _pretty(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _check(
    check_id: str,
    name: str,
    condition: bool,
    evidence: Any,
) -> dict[str, Any]:
    _require(condition, f"{check_id} failed: {name}")
    return {
        "check_id": check_id,
        "name": name,
        "status": "passed",
        "evidence": evidence,
    }


def _token(index: int, amount: float, interval: float) -> dict[str, Any]:
    return {
        "sequence_index": index,
        "contact_amount": amount,
        "operation_kind": "native_arrival_contact_amount",
        "inter_arrival_interval": interval,
    }


class _FakeNative:
    """Small packet-interface double; it is not a PyGRC model."""

    instance_count = 0

    def __init__(self, *, readout: float, rows: list[Any] | None = None) -> None:
        type(self).instance_count += 1
        self.calls: list[dict[str, Any]] = []
        self._pending: dict[str, Any] | None = None
        self._state = SimpleNamespace(
            causal_pulse_substrate_surface_log=[] if rows is None else rows,
            base_state=SimpleNamespace(
                nodes={
                    8: SimpleNamespace(coherence=float(readout)),
                    9: SimpleNamespace(coherence=7.5),
                    10: SimpleNamespace(coherence=0.0),
                }
            ),
            packet_ledger=SimpleNamespace(event_queue_records=[]),
        )

    def get_state(self) -> Any:
        return self._state

    def schedule_packet_departure(self, **kwargs: Any) -> None:
        _require(self._pending is None, "fake queue already occupied")
        self.calls.append(deepcopy(kwargs))
        self._pending = deepcopy(kwargs)
        self._state.packet_ledger.event_queue_records[:] = [
            {"kind": "packet_departure"},
            {"kind": "packet_arrival"},
        ]

    def step(self) -> None:
        queue = self._state.packet_ledger.event_queue_records
        _require(bool(queue) and self._pending is not None, "fake queue empty")
        record = queue.pop(0)
        source = int(self._pending["source_node_id"])
        target = int(self._pending["target_node_id"])
        amount = float(self._pending["amount"])
        if record["kind"] == "packet_departure":
            self._state.base_state.nodes[source].coherence -= amount
        else:
            self._state.base_state.nodes[target].coherence += amount
            self._pending = None


def _adapter(
    cls: type[RCAEActiveHistoryAdapterV1],
    *,
    tolerance: float = 1e-12,
) -> RCAEActiveHistoryAdapterV1:
    kwargs: dict[str, Any] = {
        "carrier_id": "i06a-pure-history",
        "pool_target_node_id": 2,
        "registered_source_node_ids": [0, 1],
        "readout_node_id": 8,
        "positive_reservoir_node_id": 9,
        "negative_sink_node_id": 10,
        "positive_edge_id": 7,
        "negative_edge_id": 8,
        "recency_coefficient": 0.375,
    }
    if cls is RCAEActiveHistoryAdapterV2:
        kwargs["materialization_tolerance"] = tolerance
    return cls(**kwargs)


def _row(
    index: int,
    *,
    source: int,
    target: int,
    amount: float,
    time: float,
    surface_kind: str = ROUTE_LOCAL_CONTACT,
    event_kind: str = PACKET_ARRIVAL,
) -> Any:
    return SimpleNamespace(
        surface_kind=surface_kind,
        pulse_event_kind=event_kind,
        target_node_id=target,
        source_node_id=source,
        surface_digest=f"i06a-row-{index}",
        event_time_key=time,
        contact_amount=amount,
    )


def _normalized_materialize_ast(cls: type[Any]) -> str:
    tree = ast.parse(textwrap.dedent(inspect.getsource(cls.materialize_readout)))
    function = tree.body[0]
    _require(isinstance(function, ast.FunctionDef), "materialize function missing")
    if function.body and isinstance(function.body[0], ast.Expr) and isinstance(
        function.body[0].value, ast.Constant
    ) and isinstance(function.body[0].value.value, str):
        function.body.pop(0)

    class Normalize(ast.NodeTransformer):
        def visit_Assign(self, node: ast.Assign) -> Any:
            if any(
                isinstance(target, ast.Name) and target.id == "tolerance"
                for target in node.targets
            ):
                return None
            return self.generic_visit(node)

        def visit_Name(self, node: ast.Name) -> Any:
            if node.id == "tolerance" and isinstance(node.ctx, ast.Load):
                return ast.copy_location(ast.Constant(value=1e-12), node)
            return node

        def visit_Dict(self, node: ast.Dict) -> Any:
            node = self.generic_visit(node)
            kept = [
                (key, value)
                for key, value in zip(node.keys, node.values, strict=True)
                if not (
                    isinstance(key, ast.Constant)
                    and key.value == "materialization_tolerance"
                )
            ]
            node.keys = [item[0] for item in kept]
            node.values = [item[1] for item in kept]
            return node

    Normalize().visit(function)
    ast.fix_missing_locations(function)
    return ast.dump(function, include_attributes=False)


def _adapter_source_equivalence(policy: Mapping[str, Any]) -> dict[str, Any]:
    expected_inherited = policy["adapter_conformance_authority"][
        "exact_inherited_members"
    ]
    inherited: dict[str, bool] = {}
    for name in expected_inherited:
        parent = inspect.getattr_static(RCAEActiveHistoryAdapterV1, name)
        child = inspect.getattr_static(RCAEActiveHistoryAdapterV2, name)
        inherited[name] = parent is child
    _require(all(inherited.values()), "V2 changed an inherited I03 behavior")

    metadata = {"__module__", "__doc__"}
    actual_overrides = sorted(set(RCAEActiveHistoryAdapterV2.__dict__) - metadata)
    expected_overrides = sorted(
        policy["adapter_conformance_authority"]["allowed_overrides"]
    )
    _require(actual_overrides == expected_overrides, "unexpected V2 override")

    parent_ast = _normalized_materialize_ast(RCAEActiveHistoryAdapterV1)
    child_ast = _normalized_materialize_ast(RCAEActiveHistoryAdapterV2)
    _require(parent_ast == child_ast, "materialization differs beyond tolerance/record")

    method_tree = ast.parse(
        textwrap.dedent(inspect.getsource(RCAEActiveHistoryAdapterV2.materialize_readout))
    )
    model_calls = {
        node.func.attr
        for node in ast.walk(method_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "model"
    }
    _require(
        model_calls == {"get_state", "schedule_packet_departure", "step"},
        "V2 model call surface changed",
    )
    return {
        "exact_inherited_member_count": len(inherited),
        "exact_inherited_members": sorted(inherited),
        "allowed_override_set_exact": True,
        "normalized_materialization_ast_equal": True,
        "model_call_surface": sorted(model_calls),
    }


def _pure_adapter_tests(tolerance: float) -> dict[str, Any]:
    start_instances = _FakeNative.instance_count
    decoys = [
        _row(0, source=0, target=3, amount=0.625, time=1.0),
        _row(1, source=2, target=5, amount=0.4375, time=1.1),
        _row(2, source=9, target=8, amount=0.625, time=1.2),
        _row(3, source=18, target=19, amount=0.03125, time=1.3),
        _row(4, source=20, target=22, amount=0.125, time=1.4),
        _row(5, source=0, target=6, amount=0.625, time=1.5),
        _row(
            6,
            source=0,
            target=2,
            amount=0.625,
            time=1.6,
            surface_kind="non_contact",
        ),
        _row(
            7,
            source=0,
            target=2,
            amount=0.625,
            time=1.7,
            event_kind="packet_departure",
        ),
    ]
    valid = [
        _row(8, source=0, target=2, amount=0.625, time=2.0),
        _row(9, source=1, target=2, amount=0.875, time=3.25),
    ]
    v1 = _adapter(RCAEActiveHistoryAdapterV1)
    v2 = _adapter(RCAEActiveHistoryAdapterV2, tolerance=tolerance)
    rows = decoys + valid
    ingested_v1 = v1.ingest_new_rows(_FakeNative(readout=0.0, rows=rows))
    ingested_v2 = v2.ingest_new_rows(_FakeNative(readout=0.0, rows=rows))
    _require(ingested_v1 == ingested_v2, "V1/V2 ingest differs")
    _require(len(ingested_v2) == 2, "admission filter accepted a decoy")
    _require(v1.tokens == v2.tokens, "token identity differs")
    _require(v1.readout() == v2.readout() == 1.109375, "ordered fold differs")
    _require(v1.ingest_new_rows(_FakeNative(readout=0.0, rows=rows)) == (), "V1 cursor failed")
    _require(v2.ingest_new_rows(_FakeNative(readout=0.0, rows=rows)) == (), "V2 cursor failed")

    replacement = [_token(0, 0.875, 0.0), _token(1, 0.625, 1.25)]
    intervention_v1 = v1.replace_history(
        replacement, intervention_id="i06a-v1", reason="pure-equivalence"
    )
    intervention_v2 = v2.replace_history(
        replacement, intervention_id="i06a-v2", reason="pure-equivalence"
    )
    _require(v1.tokens == v2.tokens, "intervention token state differs")
    _require(v1.readout() == v2.readout() == 0.953125, "intervention fold differs")
    _require(
        not intervention_v1["success_or_response_written"]
        and not intervention_v2["success_or_response_written"],
        "intervention wrote response state",
    )

    eq_v1 = _adapter(RCAEActiveHistoryAdapterV1)
    eq_v2 = _adapter(RCAEActiveHistoryAdapterV2, tolerance=1e-12)
    for adapter in (eq_v1, eq_v2):
        adapter.replace_history(
            [_token(0, 0.625, 0.0)],
            intervention_id=f"equal-{adapter.__class__.__name__}",
            reason="equal-tolerance-materialization",
        )
    native_v1 = _FakeNative(readout=0.0)
    native_v2 = _FakeNative(readout=0.0)
    kwargs = {
        "departure_event_time_key": 10.0,
        "arrival_event_time_key": 10.625,
        "scheduler_event_index": 10,
        "packet_index": 10,
    }
    record_v1 = eq_v1.materialize_readout(native_v1, **kwargs)
    record_v2 = eq_v2.materialize_readout(native_v2, **kwargs)
    _require(native_v1.calls == native_v2.calls, "packet construction changed")
    comparable_v1 = {
        key: value
        for key, value in record_v1.items()
        if key != "history_current_identity_digest"
    }
    comparable_v2 = {
        key: value
        for key, value in record_v2.items()
        if key not in {"history_current_identity_digest", "materialization_tolerance"}
    }
    _require(comparable_v1 == comparable_v2, "materialization record changed")

    eq_v1.replace_history([], intervention_id="negative-v1", reason="negative")
    eq_v2.replace_history([], intervention_id="negative-v2", reason="negative")
    negative_v1 = eq_v1.materialize_readout(native_v1, **kwargs)
    negative_v2 = eq_v2.materialize_readout(native_v2, **kwargs)
    _require(
        native_v1.calls[-1] == native_v2.calls[-1]
        and negative_v1["native_transfer"]["direction"]
        == negative_v2["native_transfer"]["direction"]
        == "readout_to_negative_sink",
        "negative native handoff changed",
    )

    boundary = _adapter(RCAEActiveHistoryAdapterV2, tolerance=tolerance)
    within = _FakeNative(readout=tolerance)
    within_record = boundary.materialize_readout(within, **kwargs)
    _require(not within_record["packet_scheduled"] and not within.calls, "deadband failed")
    above = _FakeNative(readout=2.0 * tolerance)
    above_record = boundary.materialize_readout(above, **kwargs)
    _require(
        above_record["packet_scheduled"]
        and above_record["native_transfer"]["direction"] == "readout_to_negative_sink",
        "above-tolerance handoff failed",
    )

    identity = boundary.restoration_identity_artifact()
    _require(
        identity["configuration"]["materialization_tolerance"] == tolerance,
        "tolerance absent from restoration identity",
    )
    alternate = _adapter(RCAEActiveHistoryAdapterV2, tolerance=2.0 * tolerance)
    _require(
        boundary.restoration_identity_digest()
        != alternate.restoration_identity_digest(),
        "identity insensitive to tolerance",
    )
    with tempfile.TemporaryDirectory(prefix="p2-i2-i06a-pure-") as directory:
        path = Path(directory) / "adapter.json"
        boundary.save(path)
        loaded = RCAEActiveHistoryAdapterV2.load(path)
        _require(
            loaded.restoration_identity_digest()
            == boundary.restoration_identity_digest(),
            "V2 save/load identity mismatch",
        )
        loaded.reset()
        _require(
            loaded.tokens == ()
            and loaded.materialization_tolerance == tolerance,
            "V2 reset changed configuration or baseline",
        )

    _require("pygrc" not in sys.modules, "pure tests imported PyGRC")
    return {
        "pure_cases_passed": 9,
        "decoy_admission_classes_rejected": len(decoys),
        "valid_tokens_admitted": len(ingested_v2),
        "positive_and_negative_packet_construction_equal": True,
        "configured_deadband_checked": True,
        "identity_and_save_load_reset_checked": True,
        "fake_native_instances": _FakeNative.instance_count - start_instances,
        "PyGRC_imported": False,
        "PyGRC_model_instantiations": 0,
    }


def _tolerance_validation(
    registration: Mapping[str, Any], policy: Mapping[str, Any]
) -> dict[str, Any]:
    expected = policy["tolerance_domain"]
    response = registration["response_registration"]
    bounds = registration["pool_economy_and_capacity"]["bounds"]
    tolerance = float(expected["runtime_tolerance"])
    domain = [float(item) for item in expected["closed_native_domain"]]
    derived = 16.0 * max(math.ulp(item) for item in domain)
    _require(tolerance == derived, "tolerance ULP derivation mismatch")
    _require(response["native_closed_coherence_interval"] == domain, "domain drift")
    _require(response["response_gain_tolerance"] == tolerance, "response tolerance drift")
    _require(bounds["M_H_closed_interval"] == expected["registered_M_H_interval"], "M_H domain drift")

    q1, q2 = map(float, expected["contribution_amounts"])
    coefficient = float(expected["history_recency_coefficient"])
    common = [0.0, q1, q2, coefficient * q2 + q1, coefficient * q1 + q2]
    private = [0.0, q1, q2]
    _require(sorted(common) == sorted(expected["required_common_fold_values"]), "common fold domain incomplete")
    _require(sorted(private) == sorted(expected["required_private_fold_values"]), "private fold domain incomplete")
    nonzero_deltas = sorted(
        {
            abs(left - right)
            for left, right in itertools.combinations(sorted(set(common + private)), 2)
            if left != right
        }
    )
    _require(nonzero_deltas and min(nonzero_deltas) > tolerance, "deadband can erase a registered transition")
    _require(max(common) == bounds["M_H_closed_interval"][1], "M_H maximum drift")
    _require(
        expected["history_reservoir_before"] - max(common)
        == expected["minimum_history_reservoir_after"]
        == bounds["minimum_history_reservoir_after_materialization"],
        "history reserve domain incomplete",
    )

    gain = float(expected["response_gain"])
    delta = float(expected["analysis_arithmetic_delta"])
    before = float(expected["B_before"])
    after = float(expected["B_after"])
    _require(tolerance < gain / 1024.0, "runtime tolerance too large")
    _require(gain >= 1024.0 * delta, "response gain below analysis floor")
    _require(domain[0] <= before <= domain[1] and domain[0] <= after <= domain[1], "B outside domain")
    _require(after == before + gain, "B gain arithmetic drift")
    _require(tolerance != delta, "runtime and scientific tolerances conflated")
    return {
        "closed_native_domain": domain,
        "runtime_tolerance": tolerance,
        "derived_16x_max_ULP": derived,
        "common_fold_values": sorted(common),
        "private_fold_values": sorted(private),
        "minimum_nonzero_materialization_delta": min(nonzero_deltas),
        "response_gain_over_tolerance": gain / tolerance,
        "response_gain_over_analysis_delta": gain / delta,
        "all_values_and_roundtrips_inside_domain": True,
        "deadband_changes_registered_response": False,
    }


def _diversion_and_admission_validation(
    registration: Mapping[str, Any], policy: Mapping[str, Any]
) -> dict[str, Any]:
    exact = policy["diversion_and_admission"]
    comparator = registration["primary_comparator"]
    _require(comparator["must_match"] == exact["must_match_exactly"], "matching dimensions drift")
    _require(comparator["all_or_none_evaluability"], "comparator arms not all-or-none")
    modes = exact["modes"]
    orders = exact["physical_orders"]
    _require(modes == list(registration["mode_registry"]), "mode scope drift")
    _require(orders == list(registration["contribution_and_schedule"]["physical_orders"]), "order scope drift")
    cells = {
        item["id"]: item
        for cell in registration["cell_registry"]
        for item in cell["subconfigurations"]
    }
    for arm in exact["leave_one_arms"]:
        _require(arm["branch"] in comparator["branch_ids"], "leave-one arm absent")
        _require(cells[arm["branch"]]["modes"] == modes, "arm mode coverage incomplete")
    contributions = {
        item["contribution_id"]: item
        for item in registration["contribution_and_schedule"]["contributions"]
    }
    for arm in exact["leave_one_arms"]:
        diverted = contributions[arm["diverted"]]
        _require(diverted["diversion_target_role"] == arm["diversion_target"], "diversion target drift")

    edges = registration["topology"]["edges"]
    roles = {item["role"] for item in registration["topology"]["nodes"]}
    positive = exact["H_P_positive_filter"]
    _require(positive["surface_kind"] == ROUTE_LOCAL_CONTACT, "surface filter drift")
    _require(positive["pulse_event_kind"] == PACKET_ARRIVAL, "arrival filter drift")
    _require(set(positive["source_roles"]) <= roles, "admission sources missing")
    admission_edges = [
        item
        for item in edges
        if item["source"] in positive["source_roles"]
        and item["target"] == positive["target_role"]
    ]
    _require(len(admission_edges) == 2, "unique H_P admission paths missing")
    _require(
        all(
            sum(
                edge["source"] == item["source_role"]
                and edge["target"] == item["target_role"]
                for edge in edges
            )
            == item["route_count"]
            == 1
            for item in registration["topology"]["unique_history_admission_paths"]
        ),
        "history admission route not unique",
    )
    excluded_route_roles = {
        "S1_TO_K_DIV_Q1",
        "S2_TO_K_DIV_Q2",
        "P_TO_K_P",
        "R_H_PLUS_TO_M_H",
        "M_H_TO_K_H",
        "E_SOURCE_TO_E_TARGET",
        "A_PRIMARY_TO_B",
        "A_ALTERNATE_TO_B",
        "S1_TO_P1_PRIVATE",
        "S2_TO_P2_PRIVATE",
    }
    _require(
        not excluded_route_roles
        & {item["edge_role"] for item in admission_edges},
        "excluded traffic can enter H_P",
    )
    return {
        "mode_order_arm_tuples": len(modes) * len(orders) * 2,
        "matching_dimensions": len(comparator["must_match"]),
        "leave_one_arms": [item["branch"] for item in exact["leave_one_arms"]],
        "unique_admission_edges": [item["edge_role"] for item in admission_edges],
        "excluded_event_classes": exact["H_P_excluded_event_classes"],
        "only_allowed_difference": exact["only_allowed_difference"],
    }


def _mode_isolation_validation(
    registration: Mapping[str, Any],
    policy: Mapping[str, Any],
    validation: Mapping[str, Any],
) -> dict[str, Any]:
    isolation = policy["positive_mode_isolation"]
    modes = registration["mode_registry"]
    for mode, expected in isolation["modes"].items():
        actual = modes[mode]
        _require(actual["response_front_mask"] == expected["response_front_mask"], f"{mode} front mask drift")
        _require(actual["response_rear_mask"] == expected["response_rear_mask"], f"{mode} rear mask drift")
        has_adapter = bool(actual["causal_carrier"]["history_carriers"])
        if "adapter_allowed" in expected:
            _require(has_adapter == expected["adapter_allowed"], "state adapter isolation failed")
        if "adapter_required" in expected:
            _require(has_adapter == expected["adapter_required"], f"{mode} adapter missing")
    _require("P" not in modes["history_carried"]["response_front_mask"], "history reads P")
    _require(modes["hybrid"]["response_front_mask"] == ["P", "M_H"], "hybrid mask not exact")

    profiles = registration["history_adapter_profiles"]
    _require(
        profiles["history_common"]["carrier_id"]
        != profiles["hybrid_common"]["carrier_id"],
        "history/hybrid carrier alias",
    )
    common_roles = {"P", "M_H"}
    for expected in isolation["modes"].values():
        for private_mask in expected["private_masks"]:
            _require(not common_roles & set(private_mask), "private mask uses common role")
    registered_roles = {item["role"] for item in registration["topology"]["nodes"]}
    _require(
        all(
            set(mask) <= registered_roles
            for expected in isolation["modes"].values()
            for mask in expected["private_masks"]
        ),
        "private mask role missing",
    )
    _require(
        "fresh model and adapter baseline" in registration["execution_registration"]["isolation"]
        and "no cross-mode state" in registration["execution_registration"]["isolation"],
        "fresh isolation not registered",
    )

    baseline_check = next(
        item for item in validation["checks"] if item["check_id"] == "I06-10"
    )["evidence"]
    refusal_check = next(
        item for item in validation["checks"] if item["check_id"] == "I06-11"
    )["evidence"]
    composite = [baseline_check[mode]["composite_digest"] for mode in isolation["modes"]]
    _require(len(set(composite)) == 3, "mode composite identities aliased")
    _require(refusal_check["cross_pair_refused"], "cross-pair refusal absent")
    _require(
        isolation["branch_configuration_must_explicitly_authorize_operations"]
        and isolation["unregistered_edge_or_producer_use"] == "operational_invalid",
        "inactive route invariant absent",
    )
    return {
        "mode_front_masks": {
            mode: modes[mode]["response_front_mask"] for mode in isolation["modes"]
        },
        "private_masks": {
            mode: expected["private_masks"]
            for mode, expected in isolation["modes"].items()
        },
        "distinct_composite_identities": len(set(composite)),
        "cross_pair_refused": True,
        "explicit_operation_authority_required": True,
        "unregistered_operation_effect": "operational_invalid",
    }


def _retry_validation(
    registration: Mapping[str, Any], policy: Mapping[str, Any]
) -> dict[str, Any]:
    core = registration["execution_registration"]
    exact = policy["infrastructure_retry"]
    _require(core["infrastructure_retry_ceiling"] == exact["ceiling"] == 1, "retry ceiling drift")
    _require(core["attempts_per_matrix_entry"] == 1, "scientific attempt count drift")
    _require(not core["scientific_retry_or_refinement"], "scientific retry admitted")
    for phrase in ("pre-model", "pre-candidate", "zero output", "unchanged committed identities"):
        _require(phrase in core["infrastructure_retry_eligibility"], f"retry phase missing: {phrase}")
    _require("any candidate operation consumes the entry" in core["infrastructure_retry_eligibility"], "candidate consumption absent")
    _require(exact["scope"] == "per_matrix_entry", "retry scope ambiguous")
    _require(exact["any_post_construction_failure_consumes_entry"], "post-construction retry admitted")
    _require(not exact["failed_scientific_or_control_result_retryable"], "result retry admitted")
    _require(not exact["eligibility_inputs_may_include_outcomes"], "outcome-dependent retry admitted")
    _require(len(exact["byte_identical_retry_inputs"]) == 6, "retry identity incomplete")
    _require(len(exact["required_failed_attempt_receipt"]) == 7, "failure receipt incomplete")
    return {
        "scope": exact["scope"],
        "infrastructure_retry_ceiling": exact["ceiling"],
        "scientific_attempts_per_entry": core["attempts_per_matrix_entry"],
        "qualifying_phase": exact["qualifying_failure_phase"],
        "byte_identical_input_classes": len(exact["byte_identical_retry_inputs"]),
        "failed_attempt_receipt_fields": len(exact["required_failed_attempt_receipt"]),
        "outcome_independent_eligibility": True,
        "failed_scientific_or_control_result_retryable": False,
    }


def _source_functions(tree: ast.Module) -> dict[str, str]:
    return {
        node.name: ast.dump(node, include_attributes=False)
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _reconstruct_historical_validator(
    current_source: str,
) -> tuple[str, dict[str, Any]]:
    current_tree = ast.parse(current_source)
    portable = next(
        node
        for node in current_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "_assert_portable"
    )
    lines = current_source.splitlines(keepends=True)
    current_function = "".join(lines[portable.lineno - 1 : portable.end_lineno])
    prefix = current_function.split("    tokens = [", 1)[0]
    separator = chr(47)
    forbidden_values = (
        separator + "home" + separator,
        separator + "tmp" + separator,
        separator + "var" + separator,
        separator + "opt" + separator,
        "OLD_" + "GRAPH_ROOT",
        "OLD_" + "RCAE_ROOT",
    )
    tuple_literal = "(" + ", ".join(json.dumps(item) for item in forbidden_values) + ")"
    old_function = (
        prefix
        + f"    forbidden = {tuple_literal}\n"
        + "    _require(not any(item in value for item in forbidden), f\"machine-local path: {field}\")\n"
    )
    historical = current_source.replace(
        "from pathlib import Path, PurePosixPath, PureWindowsPath\n",
        "from pathlib import Path\n",
        1,
    ).replace("import re\n", "", 1)
    _require(
        historical.count(current_function) == 1,
        "current portability function not unique",
    )
    historical = historical.replace(current_function, old_function, 1)
    return historical, {
        "replaced_import_surfaces": 2,
        "replaced_function": "_assert_portable",
    }


def _provenance_validation(policy: Mapping[str, Any]) -> dict[str, Any]:
    transition = policy["validator_transition"]
    execution_manifest = _load(EXECUTION_MANIFEST_PATH)
    _require(
        _sha256(EXECUTION_MANIFEST_PATH)
        == transition["historical_execution_manifest_sha256"],
        "historical execution manifest bytes drifted",
    )
    _require(len(execution_manifest["files"]) == 5, "historical manifest count drift")
    for entry in execution_manifest["files"]:
        if entry["path"].endswith("p2_i2_i06_registration.py"):
            _require(
                entry["sha256"] == transition["historical_execution_validator_sha256"],
                "historical manifest validator role drift",
            )
        else:
            _require(_sha256(ROOT / entry["path"]) == entry["sha256"], "historical manifest file drift")

    current_source = CURRENT_VALIDATOR_PATH.read_text(encoding="utf-8")
    _require(_sha256(CURRENT_VALIDATOR_PATH) == transition["current_validator_sha256"], "current validator drift")
    historical_source, reconstruction = _reconstruct_historical_validator(current_source)
    historical_hash = _sha256_bytes(historical_source.encode("utf-8"))
    _require(historical_hash == transition["historical_execution_validator_sha256"], "historical validator reconstruction mismatch")

    current_functions = _source_functions(ast.parse(current_source))
    historical_functions = _source_functions(ast.parse(historical_source))
    required = transition["required_unchanged_functions"]
    _require(
        all(current_functions[name] == historical_functions[name] for name in required),
        "non-portability validation function changed",
    )
    changed_functions = sorted(
        name
        for name in set(current_functions) & set(historical_functions)
        if current_functions[name] != historical_functions[name]
    )
    _require(changed_functions == ["_assert_portable"], "transition not guard-only")

    validation = _load(HISTORICAL_VALIDATION_PATH)
    _require(_sha256(HISTORICAL_VALIDATION_PATH) == transition["historical_validation_sha256"], "validation drift")
    _require(validation["passed_checks"] == validation["total_checks"] == 14, "retained validation not 14/14")
    manifest_check = next(
        item for item in validation["checks"] if item["check_id"] == "I06-12"
    )["evidence"]
    _require(
        manifest_check
        == {
            "manifest_id": execution_manifest["artifact_id"],
            "bound_file_count": len(execution_manifest["files"]),
        },
        "retained validation does not project historical manifest",
    )
    _require(
        _sha256(POST_PORTABILITY_MANIFEST_PATH)
        == "cb6f2d86d43839e64cf768683c1417b4ba6c9195266fad19f5344ade36d8ef54",
        "post-portability manifest drift",
    )
    return {
        "historical_execution_manifest_sha256": _sha256(EXECUTION_MANIFEST_PATH),
        "historical_execution_manifest_file_count": len(execution_manifest["files"]),
        "historical_execution_validator_reconstructed_sha256": historical_hash,
        "current_validator_sha256": _sha256(CURRENT_VALIDATOR_PATH),
        "changed_functions": changed_functions,
        "unchanged_registration_validation_functions": len(required),
        "model_construction_function_unchanged": current_functions["_build_model"] == historical_functions["_build_model"],
        "restoration_function_unchanged": current_functions["_baseline_restoration_validation"] == historical_functions["_baseline_restoration_validation"],
        "fourteen_check_projection_unchanged": current_functions["validate"] == historical_functions["validate"],
        "retained_validation_sha256": _sha256(HISTORICAL_VALIDATION_PATH),
        "retained_validation_producer": "historical_execution_validator",
        "current_validator_claimed_as_producer": False,
        **reconstruction,
    }


def validate() -> dict[str, Any]:
    _require("pygrc" not in sys.modules, "PyGRC imported before I06A validation")
    freeze = _load(FREEZE_PATH)
    policy = _load(POLICY_PATH)
    registration = _load(REGISTRATION_PATH)
    historical_validation = _load(HISTORICAL_VALIDATION_PATH)

    authority_failures = [
        entry["path"]
        for entry in freeze["exact_inputs"]
        if _sha256(ROOT / entry["path"]) != entry["sha256"]
    ]
    _require(not authority_failures, f"I06A authority drift: {authority_failures}")
    i03b = _load(I03B_RUNTIME_PATH)
    i03c = _load(I03C_RUNTIME_PATH)
    parent_hash = policy["adapter_conformance_authority"]["tested_parent"]["source_sha256"]
    _require(
        i03b["runtime_receipt"]["adapter_sha256"]
        == i03c["runtime_receipt"]["adapter_sha256"]
        == parent_hash,
        "I03 runtime authority does not bind AdapterV1",
    )
    _require(
        i03b["assertion_summary"] == {"failed": 0, "passed": 252, "total": 252}
        and i03c["assertion_summary"] == {"failed": 0, "passed": 258, "total": 258},
        "I03 runtime assertion authority drift",
    )

    source_equivalence = _adapter_source_equivalence(policy)
    pure = _pure_adapter_tests(policy["tolerance_domain"]["runtime_tolerance"])
    tolerance = _tolerance_validation(registration, policy)
    diversion = _diversion_and_admission_validation(registration, policy)
    isolation = _mode_isolation_validation(registration, policy, historical_validation)
    retry = _retry_validation(registration, policy)
    provenance = _provenance_validation(policy)
    _require("pygrc" not in sys.modules, "I06A validation imported PyGRC")

    checks = [
        _check("I06A-01", "exact owner-review and I06/I03 authority", True, {"input_count": len(freeze["exact_inputs"]), "owner_review_sha256": freeze["entry_authority"]["owner_review_sha256"]}),
        _check("I06A-02", "I03 AdapterV1 runtime-conformance authority", True, {"I03B_assertions": 252, "I03C_assertions": 258, "adapter_sha256": parent_hash}),
        _check("I06A-03", "exact inherited adapter behavior", True, source_equivalence),
        _check("I06A-04", "normalized materialization implementation equivalence", source_equivalence["normalized_materialization_ast_equal"], source_equivalence),
        _check("I06A-05", "configured-tolerance pure adapter conformance", pure["pure_cases_passed"] == 9, pure),
        _check("I06A-06", "forbidden response authority absent", source_equivalence["model_call_surface"] == ["get_state", "schedule_packet_departure", "step"], {"model_call_surface": source_equivalence["model_call_surface"], "response_reads_or_schedules": 0}),
        _check("I06A-07", "complete tolerance domain and separation", not tolerance["deadband_changes_registered_response"], tolerance),
        _check("I06A-08", "leave-one diversion matching", diversion["mode_order_arm_tuples"] == 12, diversion),
        _check("I06A-09", "unique H_P admission and exclusions", len(diversion["unique_admission_edges"]) == 2, diversion),
        _check("I06A-10", "positive shared-topology mode isolation", isolation["distinct_composite_identities"] == 3, isolation),
        _check("I06A-11", "exact per-entry infrastructure retry semantics", retry["scope"] == "per_matrix_entry", retry),
        _check("I06A-12", "byte-exact historical execution manifest and validator", provenance["historical_execution_manifest_file_count"] == 5, provenance),
        _check("I06A-13", "guard-only validator transition", provenance["changed_functions"] == ["_assert_portable"], provenance),
        _check("I06A-14", "honest retained 14/14 provenance and review stop", not provenance["current_validator_claimed_as_producer"], {"retained_validation_producer": provenance["retained_validation_producer"], "retained_validation_sha256": provenance["retained_validation_sha256"], "REG_GATE_passed": False, "I07_authorized": False}),
    ]
    return {
        "artifact_id": "P2-I2-I06A-REGISTRATION-REVIEW-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I06A",
        "lane_id": "AE01-L02",
        "status": "P2-I2-I06A-REVIEW-READY",
        "checks": checks,
        "passed_checks": len(checks),
        "total_checks": len(checks),
        "process_accounting": {
            "prevalidation_syntax_json_starts": 1,
            "failed_closed_static_validation_starts_before_retained_output": 1,
            "retained_output_producing_static_validation_starts": 1,
            "total_static_validation_starts": 2,
            "infrastructure_retries": 0,
            "pure_fake_native_instances": pure["fake_native_instances"],
            "PyGRC_imports": 0,
            "PyGRC_model_instantiations": 0,
            "baseline_validation_reruns": 0,
            "candidate_or_control_operations": 0,
            "active_history_candidate_admissions": 0,
            "response_evaluations": 0,
            "comparator_or_scientific_windows": 0
        },
        "blocker_disposition": {
            "AdapterV2_conformance_authority": "resolved_by_exact_inheritance_normalized_AST_and_pure_tests",
            "validator_manifest_provenance": "resolved_by_byte_exact_two_stage_authority"
        },
        "evidence_effect": "implementation_conformance_and_registration_provenance_only",
        "scientific_result": False,
        "gate_effect": {
            "REG_GATE_passed": False,
            "I07_authorized": False,
            "owner_acceptance_required": True,
            "commit_authorized": False
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    _require(not output.exists(), "refusing to overwrite I06A validation")
    result = validate()
    output.write_bytes(_pretty(result))
    _require(_load(output) == result, "I06A validation readback mismatch")
    print(
        json.dumps(
            {
                "status": result["status"],
                "passed_checks": result["passed_checks"],
                "total_checks": result["total_checks"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
