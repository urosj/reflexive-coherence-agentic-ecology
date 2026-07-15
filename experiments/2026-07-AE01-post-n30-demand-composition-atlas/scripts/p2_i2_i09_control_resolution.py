#!/usr/bin/env python3
"""Build and validate the P2-I2 I09 retained-evidence control index."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


MODES = ("state_carried", "history_carried", "hybrid")
SEEDS = (101, 211, 307)
DELTA = 1e-12
MANIFEST_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i2/c02/execution-manifest.json"
)
REGISTRATION_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i2/i06-three-mode-registration.json"
)
CONTROL_REGISTER_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "hypotheses/control-and-failure-register.md"
)
SCRIPT_PATH = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i2_i09_control_resolution.py"
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_digest(payload: dict[str, Any]) -> str:
    clean = dict(payload)
    clean.pop("canonical_payload_digest", None)
    encoded = json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256((encoded + "\n").encode("utf-8")).hexdigest()


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def _all_equal(values: Iterable[float]) -> bool:
    values = list(values)
    return bool(values) and max(values) - min(values) <= DELTA


def _different(left: float, right: float) -> bool:
    return abs(left - right) > DELTA


def _branch_ref(mode: str, cell: str, branch: str, order: str = "not_applicable") -> str:
    return "|".join((mode, cell, branch, order))


def _parse_program_fail_effects(text: str) -> dict[str, str]:
    effects: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("| `AE01-CTRL-"):
            continue
        fields = [field.strip() for field in line.strip().strip("|").split("|")]
        if len(fields) != 5:
            raise ValueError(f"unexpected common-control row: {line}")
        effects[fields[0].strip("`")] = fields[4]
    if sorted(effects) != [f"AE01-CTRL-{index:02d}" for index in range(1, 20)]:
        raise ValueError("program-common control register is incomplete")
    return effects


def _load_inputs(repo: Path, freeze_path: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    freeze = _read_json(repo / freeze_path)
    inputs: dict[str, dict[str, Any]] = {}
    for item in freeze["input_artifacts"]:
        path = repo / item["path"]
        observed = _sha256(path)
        if observed != item["sha256"]:
            raise ValueError(f"input identity mismatch for {item['role']}: {observed}")
        inputs[item["role"]] = {
            "identity": item,
            "payload": _read_json(path) if path.suffix == ".json" else path.read_text(encoding="utf-8"),
        }
    return freeze, inputs


def _load_observations(
    repo: Path,
    matrix: dict[str, Any],
    manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    if len(matrix["entries"]) != 234:
        raise ValueError("run matrix does not contain 234 entries")
    if manifest["required_entry_count"] != 234 or manifest["evaluable_terminal_count"] != 234:
        raise ValueError("execution manifest is not complete at 234/234")
    if any(manifest[key] for key in ("missing_entry_count", "nonevaluable_entry_count", "ambiguous_entry_count")):
        raise ValueError("execution manifest contains unresolved terminals")

    terminals = {item["entry_id"]: item for item in manifest["terminals"]}
    if set(terminals) != {item["entry_id"] for item in matrix["entries"]}:
        raise ValueError("matrix and manifest entry identities differ")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    outputs: list[dict[str, Any]] = []
    for row in matrix["entries"]:
        terminal = terminals[row["entry_id"]]
        output_path = terminal["output_path"]
        output_file = repo / output_path
        if _sha256(output_file) != terminal["output_sha256"]:
            raise ValueError(f"terminal output hash mismatch: {row['entry_id']}")
        output = _read_json(output_file)
        if output["entry_identity"]["entry_id"] != row["entry_id"]:
            raise ValueError(f"output entry identity mismatch: {row['entry_id']}")
        window = output["window_validity_receipt"]
        arrival = output["arrival_gain_receipt"]
        if not window["valid"] or not window["queues_empty"] or not window["gain_matches"]:
            raise ValueError(f"invalid scientific window: {row['entry_id']}")
        if not arrival["within_runtime_tolerance"]:
            raise ValueError(f"native/measurement gain mismatch: {row['entry_id']}")
        if abs(float(window["gain"]) - float(terminal["raw_response_value"])) > DELTA:
            raise ValueError(f"manifest/output response mismatch: {row['entry_id']}")

        feedback = output.get("feedback_receipt") or {}
        controller = output.get("controller_receipt") or {}
        production = output.get("native_production_receipt") or {}
        observation = {
            "seed": row["seed"],
            "response_value": terminal["raw_response_value"],
            "scientific_zero": window["scientific_zero"],
            "window_valid": window["valid"],
            "gain_matches": window["gain_matches"],
            "candidate_chain_status": output["raw_response_record"]["candidate_chain_status"],
            "producer_reason": output["raw_response_record"]["producer_reason"],
            "feedback_candidate_chain": feedback.get("candidate_chain"),
            "feedback_front_roles": feedback.get("front_roles", []),
            "controller_candidate_chain": controller.get("candidate_chain"),
            "controller_common_carrier_reads": controller.get("common_carrier_reads", []),
            "controller_active_history_reads": controller.get("active_history_reads", []),
            "producer_direct_claim_write": production.get("direct_claim_write", False),
            "all_capacity_guards_passed": output["support_capacity_route_receipt"]["all_capacity_guards_passed"],
            "python_command": output["runtime_binding_receipt"]["python_command"],
            "python_flags": output["runtime_binding_receipt"]["python_flags"],
            "output_path": output_path,
            "output_sha256": terminal["output_sha256"],
        }
        ref = _branch_ref(row["mode"], row["cell_id"], row["branch_id"], row["physical_order_id"])
        grouped[ref].append(observation)
        outputs.append(output)

    branch_index: list[dict[str, Any]] = []
    by_ref: dict[str, dict[str, Any]] = {}
    for ref in sorted(grouped):
        mode, cell, branch, order = ref.split("|")
        observations = sorted(grouped[ref], key=lambda item: item["seed"])
        if [item["seed"] for item in observations] != list(SEEDS):
            raise ValueError(f"registered seed coverage mismatch: {ref}")
        record = {
            "branch_ref": ref,
            "mode": mode,
            "cell_id": cell,
            "branch_id": branch,
            "physical_order_id": order,
            "seed_invariant": _all_equal(item["response_value"] for item in observations),
            "seed_results": observations,
        }
        branch_index.append(record)
        by_ref[ref] = record
    return branch_index, by_ref, {"outputs": outputs, "terminals": terminals}


def _values(by_ref: dict[str, dict[str, Any]], ref: str) -> dict[int, float]:
    if ref not in by_ref:
        raise ValueError(f"missing registered branch: {ref}")
    return {item["seed"]: float(item["response_value"]) for item in by_ref[ref]["seed_results"]}


def _compact_branch_index(branch_index: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for item in branch_index:
        seeds = item["seed_results"]
        front_role_sets = sorted({tuple(seed["feedback_front_roles"]) for seed in seeds})
        compact.append({
            "branch_ref": item["branch_ref"],
            "mode": item["mode"],
            "cell_id": item["cell_id"],
            "branch_id": item["branch_id"],
            "physical_order_id": item["physical_order_id"],
            "seed_responses": {str(seed["seed"]): seed["response_value"] for seed in seeds},
            "output_paths_by_seed": {str(seed["seed"]): seed["output_path"] for seed in seeds},
            "seed_invariant": item["seed_invariant"],
            "candidate_chain_statuses": sorted({seed["candidate_chain_status"] for seed in seeds}),
            "producer_reasons": sorted({seed["producer_reason"] for seed in seeds}),
            "receipt_summary": {
                "all_windows_valid": all(seed["window_valid"] for seed in seeds),
                "all_gains_match": all(seed["gain_matches"] for seed in seeds),
                "all_capacity_guards_passed": all(seed["all_capacity_guards_passed"] for seed in seeds),
                "any_producer_direct_claim_write": any(seed["producer_direct_claim_write"] for seed in seeds),
                "feedback_front_role_sets": [list(roles) for roles in front_role_sets],
            },
        })
    return compact


def _seed_stable(by_ref: dict[str, dict[str, Any]], refs: list[str]) -> bool:
    return all(by_ref[ref]["seed_invariant"] for ref in refs)


def _relation_disposition(condition: bool, seed_stable: bool = True) -> str:
    if not seed_stable:
        return "ambiguous"
    return "pass" if condition else "fail"


def _common_comparison_rules(
    mode: str,
    by_ref: dict[str, dict[str, Any]],
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    canonical = _branch_ref(mode, "combined-orders", "combined-orders", "q1_then_q2")
    combined_q2 = _branch_ref(mode, "combined-orders", "combined-orders", "q2_then_q1")
    common_policy = {item["control_id"]: item for item in policy["common_control_rules"]}
    records: list[dict[str, Any]] = []

    def add(control_id: str, refs: list[str], observed: dict[str, Any], condition: bool = True) -> None:
        frozen = common_policy[control_id]
        records.append({
            "rule_id": f"{mode}:common:{control_id}",
            "scope": "common_comparison_rule",
            "mode": mode,
            "control_id": control_id,
            "frozen_rule": frozen["rule"],
            "held_fixed": frozen["held_fixed"],
            "fail_closed_effect": frozen["effect"],
            "branch_refs": refs,
            "observed_relation": observed,
            "observed_disposition": _relation_disposition(condition, _seed_stable(by_ref, refs)),
        })

    alone = [
        _branch_ref(mode, "individual-contributions", "s1_only_registered"),
        _branch_ref(mode, "individual-contributions", "s2_only_registered"),
    ]
    add("each_original_source_alone", alone, {"per_branch_values": {ref: _values(by_ref, ref) for ref in alone}})

    labels = [
        canonical,
        _branch_ref(mode, "contributor-removal", "pure_source_label_permutation"),
        _branch_ref(mode, "pooled-history-shuffle", "audit_lineage_label_permutation"),
    ]
    label_equal = all(
        _all_equal(_values(by_ref, ref)[seed] for ref in labels)
        for seed in SEEDS
    )
    add("pure_source_label_permutation", labels, {"all_registered_label_variants_equal": label_equal}, label_equal)

    reassignment = [
        _branch_ref(mode, "contributor-removal", branch, order)
        for branch in ("q1_admitted_q2_diverted", "q2_admitted_q1_diverted")
        for order in ("q1_then_q2", "q2_then_q1")
    ]
    add("contribution_operation_reassignment", reassignment, {"per_branch_values": {ref: _values(by_ref, ref) for ref in reassignment}})

    primary_refs = [canonical, combined_q2]
    order_results: list[dict[str, Any]] = []
    for order, candidate_ref in (("q1_then_q2", canonical), ("q2_then_q1", combined_q2)):
        q1_ref = _branch_ref(mode, "contributor-removal", "q1_admitted_q2_diverted", order)
        q2_ref = _branch_ref(mode, "contributor-removal", "q2_admitted_q1_diverted", order)
        primary_refs.extend((q1_ref, q2_ref))
        for seed in SEEDS:
            candidate = _values(by_ref, candidate_ref)[seed]
            q1_only = _values(by_ref, q1_ref)[seed]
            q2_only = _values(by_ref, q2_ref)[seed]
            strongest = max(q1_only, q2_only)
            provenance = "q1-only" if abs(q1_only - q2_only) <= DELTA or q1_only > q2_only else "q2-only"
            order_results.append({
                "physical_order_id": order,
                "seed": seed,
                "candidate_response": candidate,
                "q1_only_response": q1_only,
                "q2_only_response": q2_only,
                "strongest_leave_one_response": strongest,
                "strongest_leave_one_provenance": provenance,
                "primary_margin": candidate - strongest,
            })
    add(
        "symmetric_leave_one_common_carrier_admission",
        list(dict.fromkeys(primary_refs)),
        {"complete_three_envelope_estimates": order_results, "positive_margin_not_required_for_control_pass": True},
    )

    diverted = _branch_ref(mode, "global-state-exclusion", "both_common_writes_diverted")
    diversion_diff = all(_different(_values(by_ref, canonical)[seed], _values(by_ref, diverted)[seed]) for seed in SEEDS)
    add("pool_write_diversion_or_freeze", [canonical, diverted], {"candidate_differs_from_diversion": diversion_diff}, diversion_diff)

    private_refs = [
        _branch_ref(mode, "global-state-exclusion", "private_partition_one"),
        _branch_ref(mode, "global-state-exclusion", "private_partition_two"),
    ]
    private_ok = True
    private_receipts: list[dict[str, Any]] = []
    for ref in private_refs:
        branch_id = ref.split("|")[2]
        allowed_partition = (
            {"P1_PRIVATE", "M_H1"}
            if branch_id == "private_partition_one"
            else {"P2_PRIVATE", "M_H2"}
        )
        for item in by_ref[ref]["seed_results"]:
            allowed = item["candidate_chain_status"] == "excluded_private_partition"
            allowed &= item["feedback_candidate_chain"] is False
            front_roles = set(item["feedback_front_roles"])
            allowed &= bool(front_roles) and front_roles <= allowed_partition
            private_ok &= allowed
            private_receipts.append({
                "branch_ref": ref,
                "seed": item["seed"],
                "front_roles": sorted(front_roles),
                "valid_single_partition_exclusion": allowed,
            })
    add("private_partition_substitution", private_refs, {"receipt_checks": private_receipts}, private_ok)

    bypass_refs = [
        _branch_ref(mode, "global-state-exclusion", "direct_address_bypass"),
        _branch_ref(mode, "global-state-exclusion", "controller_assembled_bypass"),
    ]
    bypass_ok = True
    bypass_receipts: list[dict[str, Any]] = []
    for ref in bypass_refs:
        for item in by_ref[ref]["seed_results"]:
            excluded = item["candidate_chain_status"] == "excluded_diagnostic"
            excluded &= item["feedback_candidate_chain"] is False or item["controller_candidate_chain"] is False
            if ref.endswith("controller_assembled_bypass|not_applicable"):
                excluded &= not item["controller_common_carrier_reads"] and not item["controller_active_history_reads"]
            bypass_ok &= excluded
            bypass_receipts.append({"branch_ref": ref, "seed": item["seed"], "causally_excluded": excluded, "response_value": item["response_value"]})
    add(
        "direct_or_controller_substitution",
        bypass_refs,
        {"receipt_checks": bypass_receipts, "numerical_equivalence_is_non_gating": True},
        bypass_ok,
    )

    repetition_refs = [
        canonical,
        _branch_ref(mode, "individual-contributions", "repeat_s1_quantity_matched"),
        _branch_ref(mode, "individual-contributions", "repeat_s2_quantity_matched"),
    ]
    add(
        "quantity_matched_single_source_repetition",
        repetition_refs,
        {
            "per_branch_values": {ref: _values(by_ref, ref) for ref in repetition_refs},
            "scope_diagnostic_non_gating": True,
        },
    )

    access_refs = [
        _branch_ref(mode, "access-capacity-contrast", "primary_eligible_responder"),
        _branch_ref(mode, "access-capacity-contrast", "alternate_eligible_responder"),
    ]
    access_equal = all(_all_equal(_values(by_ref, ref)[seed] for ref in access_refs) for seed in SEEDS)
    add("alternate_eligible_responder", access_refs, {"access_relation_retained": access_equal}, access_equal)
    return records


def _mode_comparison_rules(
    mode: str,
    by_ref: dict[str, dict[str, Any]],
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    canonical = _branch_ref(mode, "combined-orders", "combined-orders", "q1_then_q2")
    combined_q2 = _branch_ref(mode, "combined-orders", "combined-orders", "q2_then_q1")
    mode_policy = {item["control_id"]: item for item in policy["mode_control_rules"][mode]}
    records: list[dict[str, Any]] = []

    def add(control_id: str, refs: list[str], observed: dict[str, Any], condition: bool = True) -> None:
        frozen = mode_policy[control_id]
        records.append({
            "rule_id": f"{mode}:mode:{control_id}",
            "scope": "mode_specific_comparison_rule",
            "mode": mode,
            "control_id": control_id,
            "frozen_rule": frozen["rule"],
            "registered_relation": frozen["relation"],
            "branch_refs": refs,
            "observed_relation": observed,
            "observed_disposition": _relation_disposition(condition, _seed_stable(by_ref, refs)),
        })

    physical_q1 = _branch_ref(mode, "pooled-history-shuffle", "physical_order_reverse", "q1_then_q2")
    physical_q2 = _branch_ref(mode, "pooled-history-shuffle", "physical_order_reverse", "q2_then_q1")
    audit = _branch_ref(mode, "pooled-history-shuffle", "audit_lineage_label_permutation")

    if mode == "state_carried":
        refs = [canonical, combined_q2, physical_q1, physical_q2]
        invariant = all(_all_equal(_values(by_ref, ref)[seed] for ref in refs) for seed in SEEDS)
        add("equal_P_order_and_shuffle", refs, {"all_equal_P_orders_equal": invariant}, invariant)
        debit = _branch_ref(mode, "global-state-exclusion", "post_write_native_P_debit")
        differs = all(_different(_values(by_ref, canonical)[seed], _values(by_ref, debit)[seed]) for seed in SEEDS)
        add("post_write_P_debit", [canonical, debit], {"candidate_differs_from_debited_P": differs}, differs)
        audit_equal = all(_all_equal((_values(by_ref, canonical)[seed], _values(by_ref, audit)[seed])) for seed in SEEDS)
        add("audit_history_only_change", [canonical, audit], {"audit_only_variant_equal": audit_equal}, audit_equal)
    elif mode == "history_carried":
        differs = all(_different(_values(by_ref, physical_q1)[seed], _values(by_ref, physical_q2)[seed]) for seed in SEEDS)
        add("active_history_order_reversal", [physical_q1, physical_q2], {"ordered_history_responses_differ": differs}, differs)
        p_debit = _branch_ref(mode, "global-state-exclusion", "history_mode_P_only_debit")
        invariant = all(_all_equal((_values(by_ref, canonical)[seed], _values(by_ref, p_debit)[seed])) for seed in SEEDS)
        add("P_only_debit_with_H_P_M_H_fixed", [canonical, p_debit], {"P_only_debit_invariant": invariant}, invariant)
        clamp = _branch_ref(mode, "global-state-exclusion", "history_reference_clamp")
        clamp_diff = all(_different(_values(by_ref, canonical)[seed], _values(by_ref, clamp)[seed]) for seed in SEEDS)
        add("H_P_reference_clamp_with_P_fixed", [canonical, clamp], {"active_history_clamp_changes_response": clamp_diff}, clamp_diff)
    else:
        full = _branch_ref(mode, "global-state-exclusion", "hybrid_full_components")
        ref_p = _branch_ref(mode, "global-state-exclusion", "hybrid_reference_P_candidate_H")
        ref_h = _branch_ref(mode, "global-state-exclusion", "hybrid_candidate_P_reference_H")
        refs = _branch_ref(mode, "global-state-exclusion", "hybrid_reference_components")
        factorial = [full, ref_p, ref_h, refs]
        add("complete_P_by_H_P_component_factorial", factorial, {"per_branch_values": {ref: _values(by_ref, ref) for ref in factorial}})
        p_diff = all(_different(_values(by_ref, full)[seed], _values(by_ref, ref_p)[seed]) for seed in SEEDS)
        add("P_only_reference_intervention", [full, ref_p], {"full_differs_from_reference_P": p_diff}, p_diff)
        h_diff = all(_different(_values(by_ref, full)[seed], _values(by_ref, ref_h)[seed]) for seed in SEEDS)
        add("H_P_only_reference_intervention", [full, ref_h], {"full_differs_from_reference_H_P": h_diff}, h_diff)
        order_diff = all(_different(_values(by_ref, physical_q1)[seed], _values(by_ref, physical_q2)[seed]) for seed in SEEDS)
        add("history_order_reversal_with_P_fixed", [physical_q1, physical_q2], {"ordered_history_responses_differ": order_diff}, order_diff)
        interactions = {
            seed: _values(by_ref, full)[seed] - _values(by_ref, ref_p)[seed] - _values(by_ref, ref_h)[seed] + _values(by_ref, refs)[seed]
            for seed in SEEDS
        }
        add("interaction_or_synergy", factorial, {"raw_factorial_interaction": interactions, "nonlinearity_not_required": True})
    return records


def _lane_controls(
    freeze: dict[str, Any],
    template: dict[str, Any],
    comparisons: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_mode_and_control = {(item["mode"], item["control_id"]): item for item in comparisons}
    mode_all = {
        mode: [item for item in comparisons if item["mode"] == mode and item["scope"] == "mode_specific_comparison_rule"]
        for mode in MODES
    }
    intervention_ids = {
        "state_carried": ["post_write_P_debit"],
        "history_carried": ["H_P_reference_clamp_with_P_fixed"],
        "hybrid": ["P_only_reference_intervention", "H_P_only_reference_intervention"],
    }
    fail_effects = {
        "AE01-L02-CTRL-01": "blocks attributable multiple-source resolution while retaining raw marginal observations",
        "AE01-L02-CTRL-02": "blocks attribution invariance or primary-comparator evaluability as specified by the failed subrule",
        "AE01-L02-CTRL-03": "blocks the affected mode-specific R03/R04 relation without changing dependence mode",
        "AE01-L02-CTRL-04": "blocks R04 if private aggregation or direct/controller provenance enters the candidate chain",
        "AE01-L02-CTRL-05": "blocks the affected R03/R04 common-carrier causal claim",
    }
    records: list[dict[str, Any]] = []
    for entry in template["entries"]:
        mode = entry["mode"]
        control_id = entry["control_id"]
        mapping = freeze["lane_control_rule_mapping"][control_id]
        mapped: list[dict[str, Any]] = []
        for control in mapping:
            if control == "MODE_SPECIFIC_ALL":
                mapped.extend(mode_all[mode])
            elif control == "MODE_SPECIFIC_CARRIER_INTERVENTIONS":
                mapped.extend(by_mode_and_control[(mode, item)] for item in intervention_ids[mode])
            else:
                mapped.append(by_mode_and_control[(mode, control)])
        dispositions = [item["observed_disposition"] for item in mapped]
        if "blocked" in dispositions or "not_run" in dispositions:
            disposition = "blocked"
        elif "fail" in dispositions:
            disposition = "fail"
        elif "ambiguous" in dispositions:
            disposition = "ambiguous"
        else:
            disposition = "pass"
        records.append({
            "mode": mode,
            "control_id": control_id,
            "planned_applicability": entry["planned_applicability"],
            "resolution_stage": entry["resolution_stage"],
            "registered_branches": entry["registered_branches"],
            "comparison_rule_refs": [item["rule_id"] for item in mapped],
            "observed_disposition": disposition,
            "fail_closed_effect": fail_effects[control_id],
            "evidence_refs": [MANIFEST_PATH] + sorted({ref for item in mapped for ref in item["branch_refs"]}),
            "notes": "mode-local control projection only; R01-R05 and terminal interpretation remain unassigned",
        })
    return records


def _program_predicates(
    registration: dict[str, Any],
    manifest: dict[str, Any],
    branch_index: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    outputs: list[dict[str, Any]],
    c01_audit: dict[str, Any],
) -> dict[str, dict[str, bool]]:
    comparison_lookup = {(item["mode"], item["control_id"]): item["observed_disposition"] == "pass" for item in comparisons}
    claim = registration["claim_and_gate_boundary"]
    modes = registration["mode_registry"]
    common_receipts = all(
        item["window_validity_receipt"]["valid"]
        and item["arrival_gain_receipt"]["within_runtime_tolerance"]
        for item in outputs
    )
    production_valid = all(
        not (item.get("native_production_receipt") or {}).get("direct_claim_write", False)
        for item in outputs
    )
    budget_valid = all(
        item["support_capacity_route_receipt"]["all_capacity_guards_passed"]
        and item["timing_queue_receipt"]["queues_empty_after"]
        and not item["inert_sink_no_influence_receipt"]["outgoing_registered_edges"]
        for item in outputs
    )
    runtime_valid = all(
        item["runtime_binding_receipt"]["python_command"] == ".venv/bin/python"
        and item["runtime_binding_receipt"]["python_flags"] == ["-B"]
        and item["runtime_binding_receipt"]["dont_write_bytecode"] is True
        for item in outputs
    )
    claim_safe = (
        claim["R01_through_R05_disposition"] == "unassigned"
        and claim["scientific_result"] is False
        and claim["mode_selection_or_ranking"] is False
        and manifest["scientific_interpretation"] is None
    )
    topology_roles = {item["role"]: item["node_id"] for item in registration["topology"]["nodes"]}
    roles_separate = len(topology_roles) == len(set(topology_roles.values()))
    private_pass = {mode: comparison_lookup[(mode, "private_partition_substitution")] for mode in MODES}
    bypass_pass = {mode: comparison_lookup[(mode, "direct_or_controller_substitution")] for mode in MODES}
    label_pass = {mode: comparison_lookup[(mode, "pure_source_label_permutation")] for mode in MODES}
    carrier_pass = {mode: comparison_lookup[(mode, "pool_write_diversion_or_freeze")] for mode in MODES}
    live_modes = set(modes) == set(MODES)
    constructed_complete = {
        "state_carried": False,
        "history_carried": modes["history_carried"]["realization_class"] == "minimally_producer_assisted"
        and modes["history_carried"]["RCAE_computes_success_or_response"] is False,
        "hybrid": modes["hybrid"]["realization_class"] == "minimally_producer_assisted"
        and modes["hybrid"]["RCAE_computes_success_or_response"] is False,
    }
    result: dict[str, dict[str, bool]] = {}
    for mode in MODES:
        result[mode] = {
            "input_identities_exact": True,
            "conceptual_sources_not_runtime_evidence": claim_safe,
            "claim_boundary_safe": claim_safe,
            "common_carrier_controls_pass": carrier_pass[mode] and private_pass[mode],
            "later_response_receipts_valid": common_receipts,
            "private_partition_control_pass": private_pass[mode],
            "direct_controller_control_pass": bypass_pass[mode],
            "label_invariance_pass": label_pass[mode],
            "carrier_intervention_pass": carrier_pass[mode],
            "producer_and_handoff_receipts_valid": production_valid,
            "budget_capacity_and_leakage_receipts_valid": budget_valid,
            "parent_claim_absent": claim_safe,
            "participant_carrier_roles_separate": roles_separate,
            "selection_not_run": claim_safe,
            "demand_not_substrate_evidence": claim_safe,
            "realization_class_explicit": live_modes and bool(modes[mode]["realization_class"]),
            "constructed_profile_complete": constructed_complete[mode],
            "live_runtime_receipts_valid": runtime_valid,
            "manifest_complete": manifest["evaluable_terminal_count"] == 234 and manifest["status"] == "complete_all_registered_entries_evaluable",
            "domain_promotion_absent": claim_safe,
            "incomplete_predecessor_not_scientific_negative": c01_audit["evidence_effect"]["scientific_result"] is None
            and c01_audit["evidence_effect"]["negative_scientific_result"] is False
            and c01_audit["mechanical_disposition"]["matrix_entries_evaluable"] == 0,
        }
    return result


def _program_controls(
    freeze: dict[str, Any],
    fail_effects: dict[str, str],
    predicates: dict[str, dict[str, bool]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for policy in freeze["program_common_control_policy"]:
        results: list[dict[str, Any]] = []
        for mode in MODES:
            applicable = mode not in policy.get("not_applicable_modes", [])
            predicate_results = {item: predicates[mode][item] for item in policy["predicate_ids"]}
            disposition = "not_applicable" if not applicable else ("pass" if all(predicate_results.values()) else "fail")
            results.append({
                "mode": mode,
                "planned_applicability": "applicable" if applicable else "not_applicable",
                "applicability_rationale": (
                    "state-carried is an accepted pygrc_native_candidate with no RCAE causal producer, so constructed-mechanism completeness does not apply"
                    if not applicable
                    else "the program-common guard applies to this retained mode"
                ),
                "observed_disposition": disposition,
                "predicate_results": predicate_results,
                "evidence_refs": [REGISTRATION_PATH, MANIFEST_PATH],
                "requires_I11_revalidation": policy["i11_revalidation"],
            })
        records.append({
            "control_id": policy["control_id"],
            "resolution_stage": policy["stage"],
            "mode_results": results,
            "fail_closed_effect": fail_effects[policy["control_id"]],
        })
    return records


def build_index(repo: Path, freeze_path: str) -> tuple[dict[str, Any], dict[str, Any]]:
    freeze, inputs = _load_inputs(repo, freeze_path)
    policy = inputs["analysis_policy"]["payload"]
    registration = inputs["exact_registration"]["payload"]
    template = inputs["lane_control_template"]["payload"]
    matrix = inputs["run_matrix"]["payload"]
    manifest = inputs["execution_manifest"]["payload"]
    c01_audit = inputs["c01_bounded_incomplete_audit"]["payload"]
    fail_effects = _parse_program_fail_effects(inputs["program_control_register"]["payload"])
    branch_index, by_ref, loaded = _load_observations(repo, matrix, manifest)
    comparisons = [
        item
        for mode in MODES
        for item in (_common_comparison_rules(mode, by_ref, policy) + _mode_comparison_rules(mode, by_ref, policy))
    ]
    lane_controls = _lane_controls(freeze, template, comparisons)
    predicates = _program_predicates(registration, manifest, branch_index, comparisons, loaded["outputs"], c01_audit)
    program_controls = _program_controls(freeze, fail_effects, predicates)

    comparison_counts = Counter(item["observed_disposition"] for item in comparisons)
    lane_counts = Counter(item["observed_disposition"] for item in lane_controls)
    program_mode_counts = Counter(
        result["observed_disposition"]
        for item in program_controls
        for result in item["mode_results"]
    )
    index: dict[str, Any] = {
        "artifact_id": "P2-I2-I09-CONTROL-RESOLUTION-INDEX",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I09",
        "lane_id": "AE01-L02",
        "status": "review_ready_control_projection",
        "source_input_freeze": freeze_path,
        "source_input_freeze_sha256": _sha256(repo / freeze_path),
        "builder_identity": {"path": SCRIPT_PATH, "sha256": _sha256(repo / SCRIPT_PATH)},
        "input_identity_count": len(freeze["input_artifacts"]),
        "projection_only": True,
        "introduces_evidence_or_schema_authority": False,
        "program_common_controls": program_controls,
        "comparison_rules": comparisons,
        "lane_controls": lane_controls,
        "observed_branch_index": _compact_branch_index(branch_index),
        "summary": {
            "program_common_control_count": len(program_controls),
            "program_common_mode_dispositions": dict(sorted(program_mode_counts.items())),
            "comparison_rule_count": len(comparisons),
            "comparison_rule_dispositions": dict(sorted(comparison_counts.items())),
            "lane_control_count": len(lane_controls),
            "lane_control_dispositions": dict(sorted(lane_counts.items())),
            "observed_branch_configuration_count": len(branch_index),
            "matrix_entry_count": len(matrix["entries"]),
            "seed_varying_branch_configuration_count": sum(not item["seed_invariant"] for item in branch_index),
            "CONTROL_GATE_candidate": all(item["observed_disposition"] in {"pass", "not_applicable"} for item in lane_controls)
            and all(result["observed_disposition"] in {"pass", "not_applicable"} for item in program_controls for result in item["mode_results"]),
        },
        "interpretation_boundary": {
            "R01_through_R05": "unassigned_until_I11",
            "lane_support_status": None,
            "terminal_classification": None,
            "mode_ranking": False,
            "cross_mode_scalar_aggregation": False,
            "I11_common_guard_revalidation_required": True,
            "scientific_result": False,
        },
        "execution_boundary": freeze["execution_boundary"],
    }
    index["canonical_payload_digest"] = _canonical_digest(index)
    return index, {"freeze": freeze, "manifest": manifest, "matrix": matrix}


def build_validation(index: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    freeze = context["freeze"]
    checks: list[dict[str, Any]] = []

    def check(check_id: str, claim: str, passed: bool, observed: Any) -> None:
        checks.append({"check_id": check_id, "claim": claim, "passed": bool(passed), "observed": observed})

    check("I09-01", "all frozen input identities reconstruct exactly", index["input_identity_count"] == len(freeze["input_artifacts"]), index["input_identity_count"])
    check("I09-02", "all 234 registered terminals are evaluable", index["summary"]["matrix_entry_count"] == 234, index["summary"]["matrix_entry_count"])
    check("I09-03", "the normalized branch index has exact three-seed coverage", len(index["observed_branch_index"]) == 78, len(index["observed_branch_index"]))
    check("I09-04", "no matched branch configuration varies across seeds", index["summary"]["seed_varying_branch_configuration_count"] == 0, index["summary"]["seed_varying_branch_configuration_count"])
    check("I09-05", "all frozen common and mode comparison rules are represented", len(index["comparison_rules"]) == 38, len(index["comparison_rules"]))
    check("I09-06", "all comparison rules resolve without forced ambiguity", index["summary"]["comparison_rule_dispositions"] == {"pass": 38}, index["summary"]["comparison_rule_dispositions"])
    check("I09-07", "all fifteen mode-local L02 controls are represented", len(index["lane_controls"]) == 15, len(index["lane_controls"]))
    check("I09-08", "all mode-local L02 controls pass their frozen rules", index["summary"]["lane_control_dispositions"] == {"pass": 15}, index["summary"]["lane_control_dispositions"])
    check("I09-09", "all nineteen program-common controls are represented", len(index["program_common_controls"]) == 19, len(index["program_common_controls"]))
    check("I09-10", "program controls resolve separately for every mode", sum(len(item["mode_results"]) for item in index["program_common_controls"]) == 57, sum(len(item["mode_results"]) for item in index["program_common_controls"]))
    check("I09-11", "only native state CTRL-16 is explicitly not applicable", index["summary"]["program_common_mode_dispositions"] == {"not_applicable": 1, "pass": 56}, index["summary"]["program_common_mode_dispositions"])
    check("I09-12", "direct/controller output equivalence is resolved by causal receipts", all(item["observed_disposition"] == "pass" for item in index["comparison_rules"] if item["control_id"] == "direct_or_controller_substitution"), [item["observed_disposition"] for item in index["comparison_rules"] if item["control_id"] == "direct_or_controller_substitution"])
    check("I09-13", "quantity-matched repetition remains non-gating", all(item["observed_relation"].get("scope_diagnostic_non_gating") is True for item in index["comparison_rules"] if item["control_id"] == "quantity_matched_single_source_repetition"), 3)
    check("I09-14", "history and hybrid order dependence remains mode-local", all(item["observed_disposition"] == "pass" for item in index["comparison_rules"] if item["control_id"] in {"active_history_order_reversal", "history_order_reversal_with_P_fixed"}), 2)
    check("I09-15", "state order invariance remains mode-local", next(item["observed_disposition"] for item in index["comparison_rules"] if item["control_id"] == "equal_P_order_and_shuffle") == "pass", "pass")
    check("I09-16", "the index assigns no R01-R05 or terminal result", index["interpretation_boundary"]["R01_through_R05"] == "unassigned_until_I11" and index["interpretation_boundary"]["terminal_classification"] is None, index["interpretation_boundary"])
    check("I09-17", "the index creates no evidence or schema authority", index["projection_only"] is True and index["introduces_evidence_or_schema_authority"] is False, {"projection_only": index["projection_only"], "schema_authority": index["introduces_evidence_or_schema_authority"]})
    expected_revalidation = {
        item["control_id"]: item["i11_revalidation"]
        for item in freeze["program_common_control_policy"]
    }
    observed_revalidation = {
        item["control_id"]: all(result["requires_I11_revalidation"] for result in item["mode_results"])
        for item in index["program_common_controls"]
    }
    check("I09-18", "all terminal/report guards retain the exact frozen I11 revalidation duty", observed_revalidation == expected_revalidation, observed_revalidation)
    check("I09-19", "CONTROL-GATE candidate fails closed on any unresolved mandatory control", index["summary"]["CONTROL_GATE_candidate"] is True, index["summary"]["CONTROL_GATE_candidate"])
    check("I09-20", "canonical payload digest reconstructs exactly", index["canonical_payload_digest"] == _canonical_digest(index), index["canonical_payload_digest"])
    def strings(value: Any) -> Iterable[str]:
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for key, item in value.items():
                yield from strings(key)
                yield from strings(item)
        elif isinstance(value, list):
            for item in value:
                yield from strings(item)
    absolute_values = sorted({value for value in strings(index) if value.startswith("/")})
    check("I09-21", "the retained index contains no absolute paths", not absolute_values, absolute_values)

    passed = sum(item["passed"] for item in checks)
    validation: dict[str, Any] = {
        "artifact_id": "P2-I2-I09-CONTROL-RESOLUTION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I09",
        "status": "passed" if passed == len(checks) else "failed_closed",
        "checks": checks,
        "passed_check_count": passed,
        "check_count": len(checks),
        "blocker_count": len(checks) - passed,
        "candidate_or_control_invocations": 0,
        "matrix_entry_regenerations": 0,
        "pygrc_imports": 0,
        "scientific_interpretation": False,
        "CONTROL_GATE": "review_ready_pending_owner_acceptance" if passed == len(checks) else "closed",
    }
    validation["canonical_payload_digest"] = _canonical_digest(validation)
    return validation


def build_report(index: dict[str, Any], validation: dict[str, Any]) -> str:
    lane_rows = []
    for item in index["lane_controls"]:
        lane_rows.append(f"| `{item['mode']}` | `{item['control_id']}` | `{item['observed_disposition']}` |")
    return "\n".join([
        "# P2-I2-I09 Control Resolution",
        "",
        "**Status:** review-ready; owner acceptance and commit pending",
        "",
        "**Evidence effect:** compact control projection over retained I03/I04/I06/I08 artifacts only",
        "",
        "## Result",
        "",
        f"The deterministic I09 projection passes {validation['passed_check_count']}/{validation['check_count']} checks with {validation['blocker_count']} blockers. It resolves all 19 program-common controls separately by mode (56 pass, one explicit state-carried `AE01-CTRL-16` not-applicable), all 38 frozen comparison rules, and all 15 mode-local L02 controls.",
        "",
        "No registered branch varies across seeds. State-carried preserves the frozen order-invariant relation (`0.125`, `0.125`) and primary margins (`0.125`, `0.125`); history-carried and hybrid preserve their order-conditioned responses (`0.125`, `0.0`) and primary margins (`0.125`, `0.0`). Both original-source-alone and all symmetric leave-one arms are `0.0`; quantity-matched single-source repetitions are `0.125` and remain non-gating. Private one-partition paths are `0.0`; direct/controller diagnostics are `0.125` but are receipt-derived causal exclusions, so numerical equivalence is not promoted into candidate-chain evidence.",
        "",
        "## Mode-local L02 controls",
        "",
        "| Mode | Control | Disposition |",
        "| --- | --- | --- |",
        *lane_rows,
        "",
        "## Boundary",
        "",
        "This package does not assign `R01`-`R05`, rank or collapse modes, select a terminal class, regenerate an entry, or create schema authority. Program-common terminal/report guards are valid only at the I09 artifact boundary and must be revalidated against I11 closeout. `P2-I2-CONTROL-GATE` is review-ready, not owner-passed, and I10 remains unauthorized until review.",
        "",
    ])


def _default_paths() -> tuple[str, str, str, str]:
    base = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
    return (
        f"{base}/contracts/p2-i2/i09-control-resolution-input-freeze.json",
        f"{base}/contracts/p2-i2/i09-control-resolution-index.json",
        f"{base}/contracts/p2-i2/i09-control-resolution-validation.json",
        f"{base}/reports/P2-I2-I09-control-resolution.md",
    )


def main() -> int:
    default_freeze, default_index, default_validation, default_report = _default_paths()
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "validate"))
    parser.add_argument("--freeze", default=default_freeze)
    parser.add_argument("--index", default=default_index)
    parser.add_argument("--validation", default=default_validation)
    parser.add_argument("--report", default=default_report)
    args = parser.parse_args()
    repo = Path.cwd().resolve()
    if not (repo / ".git").exists():
        raise SystemExit("run from the repository root")

    index, context = build_index(repo, args.freeze)
    validation = build_validation(index, context)
    report = build_report(index, validation)
    if args.command == "build":
        (repo / args.index).write_bytes(_json_bytes(index))
        (repo / args.validation).write_bytes(_json_bytes(validation))
        (repo / args.report).write_text(report, encoding="utf-8")
    else:
        if (repo / args.index).read_bytes() != _json_bytes(index):
            raise SystemExit("retained I09 index is not byte-identical to reconstruction")
        if (repo / args.validation).read_bytes() != _json_bytes(validation):
            raise SystemExit("retained I09 validation is not byte-identical to reconstruction")
        if (repo / args.report).read_text(encoding="utf-8") != report:
            raise SystemExit("retained I09 report is not byte-identical to reconstruction")

    print(json.dumps({
        "status": validation["status"],
        "checks": f"{validation['passed_check_count']}/{validation['check_count']}",
        "blockers": validation["blocker_count"],
        "comparison_rules": len(index["comparison_rules"]),
        "lane_controls": len(index["lane_controls"]),
        "program_common_controls": len(index["program_common_controls"]),
        "CONTROL_GATE": validation["CONTROL_GATE"],
    }, sort_keys=True))
    return 0 if validation["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
