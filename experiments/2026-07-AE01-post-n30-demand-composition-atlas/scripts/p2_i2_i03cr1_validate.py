"""Zero-runtime causal-well-formedness closeout for P2-I2-I03C.

This validator imports no PyGRC package and instantiates no model. It inspects
the frozen owner review, immutable I03C artifacts, retained conformance data,
adapter/harness source, admitted PyGRC source, and the I03CR1 closure registry.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
EXPECTED_INPUT_SHA256 = "81e8b72be0df84cc757e2ff2d1b0dc398daabef4a8422de3b525897d19ff1dba"
EXPECTED_REGISTRY_SHA256 = "87232487b0937345f9f79db1b3618674ad683737672332f09ea9e3beefcee463"
EXPECTED_RUNTIME_SHA256 = "217c8972e8e1199409343fb72b0eca12b2ba24dceb6a1f213c97af9143f0e96c"
EXPECTED_RUNTIME_FREEZE_SHA256 = "e19be7110597252517f3531a1eddb82dc2e5fdf9a16fcb1c07ec1b9921ed6f5d"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
EXPECTED_BRANCHES = [
    "reference",
    "q1_only",
    "q2_only",
    "combined_q1_q2",
    "combined_q2_q1",
    "lineage_permuted",
    "write_diversion",
    "history_only_clamp",
    "state_only_debit",
    "private_partition",
    "alternate_responder",
    "restoration_continuation",
]
STANDARD_BRANCHES = EXPECTED_BRANCHES[:9] + ["alternate_responder"]
EXPECTED_OPS = [f"H-L02-OP-{index:02d}" for index in range(1, 10)]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(repository), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _function_source(source: str, name: str) -> str:
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            segment = ast.get_source_segment(source, node)
            if segment is None:
                raise AssertionError(f"cannot extract function: {name}")
            return segment
    raise AssertionError(f"missing function: {name}")


def _assertion_map(conformance: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {row["check_id"]: row for row in conformance["assertions"]}


def _passed(assertions: Mapping[str, Mapping[str, Any]], *ids: str) -> bool:
    return all(assertions[item]["passed"] is True for item in ids)


def _result(
    check_id: str,
    name: str,
    condition: bool,
    classification: str,
    finding: str,
    evidence: Any,
    *,
    obligations: list[str] | None = None,
) -> dict[str, Any]:
    if not condition:
        raise AssertionError(f"{check_id} failed: {finding}")
    if classification not in {"direct_pass", "closure_clarification", "downstream_obligation"}:
        raise AssertionError(f"invalid passing classification: {classification}")
    return {
        "check_id": check_id,
        "name": name,
        "status": "passed",
        "classification": classification,
        "finding": finding,
        "evidence": evidence,
        "downstream_obligation_ids": obligations or [],
    }


def validate(input_path: Path, registry_path: Path) -> dict[str, Any]:
    freeze = _load(input_path)
    registry = _load(registry_path)
    if _sha256(input_path) != EXPECTED_INPUT_SHA256:
        raise AssertionError("I03CR1 input freeze identity drifted")
    if _sha256(registry_path) != EXPECTED_REGISTRY_SHA256:
        raise AssertionError("I03CR1 closeout registry identity drifted")
    if freeze["artifact_id"] != "P2-I2-I03CR1-CLOSEOUT-REVALIDATION-INPUT":
        raise AssertionError("wrong I03CR1 input artifact")
    if registry["artifact_id"] != "P2-I2-I03CR1-HYBRID-CLOSEOUT-REGISTRY":
        raise AssertionError("wrong I03CR1 registry artifact")
    if len(freeze["review_checks"]) != 26 or len(freeze["acceptance_statements"]) != 17:
        raise AssertionError("owner-review coverage count drifted")
    if any(freeze["audit_policy"][key] != 0 for key in (
        "model_instantiations", "runtime_evidence_invocations",
        "runtime_reconstruction_invocations", "retries", "rescue_variants",
    )):
        raise AssertionError("I03CR1 must remain zero-runtime")

    owner_review = Path(freeze["authority"]["owner_review_path"])
    if _sha256(owner_review) != freeze["authority"]["owner_review_sha256"]:
        raise AssertionError("owner review identity drifted")
    immutable_checks: list[dict[str, Any]] = []
    for item in freeze["immutable_i03c_inputs"]:
        path = ROOT / item["path"]
        actual = _sha256(path)
        if actual != item["sha256"]:
            raise AssertionError(f"immutable I03C input drifted: {path}")
        immutable_checks.append({"path": item["path"], "sha256": actual, "match": True})

    graph_root = Path(freeze["authority"]["graph_repository"])
    graph_before = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "status_porcelain": _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"),
    }
    if graph_before != {"revision": EXPECTED_GRAPH_REVISION, "status_porcelain": ""}:
        raise AssertionError("admitted graph checkout is not exact and clean")

    contract = _load(EXPERIMENT / "contracts/p2-i2/i03c-hybrid-realization-and-discriminator-contract.json")
    runtime_freeze = _load(EXPERIMENT / "contracts/p2-i2/i03c-hybrid-runtime-conformance-input-freeze.json")
    conformance = _load(EXPERIMENT / "contracts/p2-i2/i03c-hybrid-runtime-conformance.json")
    receipt = _load(EXPERIMENT / "contracts/p2-i2/i03c-runtime-reconstruction-receipt.json")
    adapter_path = EXPERIMENT / "scripts/p2_i2_i03b_history_adapter.py"
    harness_path = EXPERIMENT / "scripts/p2_i2_i03c_conform.py"
    adapter_source = adapter_path.read_text(encoding="utf-8")
    harness_source = harness_path.read_text(encoding="utf-8")
    native_path = graph_root / "src/pygrc/models/lgrc_9_v3_runtime.py"
    native_source = native_path.read_text(encoding="utf-8")
    ast.parse(adapter_source, filename=str(adapter_path))
    ast.parse(harness_source, filename=str(harness_path))
    ast.parse(native_source, filename=str(native_path))

    if _sha256(EXPERIMENT / "contracts/p2-i2/i03c-hybrid-runtime-conformance.json") != EXPECTED_RUNTIME_SHA256:
        raise AssertionError("runtime evidence identity drifted")
    if _sha256(EXPERIMENT / "contracts/p2-i2/i03c-hybrid-runtime-conformance-input-freeze.json") != EXPECTED_RUNTIME_FREEZE_SHA256:
        raise AssertionError("runtime freeze identity drifted")
    if conformance["assertion_summary"] != {"failed": 0, "passed": 258, "total": 258}:
        raise AssertionError("retained I03C assertion summary drifted")
    if not all(row["passed"] for row in conformance["assertions"]):
        raise AssertionError("retained conformance contains failed assertions")
    if set(conformance["branches"]) != set(EXPECTED_BRANCHES):
        raise AssertionError("retained twelve-branch identity drifted")
    if conformance["next_iteration_authorized"] is not False:
        raise AssertionError("runtime evidence improperly authorizes progression")

    assertions = _assertion_map(conformance)
    ingest = _function_source(adapter_source, "ingest_new_rows")
    readout = _function_source(adapter_source, "readout")
    replace_history = _function_source(adapter_source, "replace_history")
    materialize = _function_source(adapter_source, "materialize_readout")
    adapter_load = _function_source(adapter_source, "load")
    adapter_reset = _function_source(adapter_source, "reset")
    execute_branch = _function_source(harness_source, "_execute_branch")
    private_branch = _function_source(harness_source, "_run_private_partition")
    restoration = _function_source(harness_source, "_run_restoration")
    composite_summary = _function_source(harness_source, "_composite_summary")
    prepare_feedback = _function_source(harness_source, "_prepare_feedback")
    emit_feedback = _function_source(native_source, "emit_feedback_eligibility_surface_row")
    producer = _function_source(native_source, "_produce_packet_departure_from_feedback_eligibility")

    canonical = conformance["branches"]["combined_q1_q2"]
    state_only = conformance["branches"]["state_only_debit"]
    history_only = conformance["branches"]["history_only_clamp"]
    reverse = conformance["branches"]["combined_q2_q1"]
    private = conformance["branches"]["private_partition"]

    carrier = registry["hybrid_carrier_authority"]
    carrier_safe = (
        carrier["carrier_id_class"] == "one_bound_common_composite_carrier"
        and set(carrier["components"]) == {"P", "H_P", "M_H", "V", "L"}
        and len(carrier["prohibited_substitutes"]) == 8
        and contract["common_access_witness"]["common_pool_identity"]
        == "P plus H_P with its M_H output-port binding"
    )

    history_authoritative = (
        registry["authoritative_history_output_rule"]["authority"] == "H_P"
        and "fail closed" in registry["authoritative_history_output_rule"]["disagreement_effect"]
        and "self._state[\"tokens\"]" in readout
        and "self._state[\"tokens\"] = canonical" in replace_history
        and "target = self.readout()" in materialize
        and "native readout materialization does not match active history" in materialize
        and "reset_baseline_state" in adapter_source
    )

    p_independent = (
        _passed(assertions, "cross.state_only_preserves_H_M", "cross.state_only_changes_joint_response")
        and state_only["tokens"] == canonical["tokens"]
        and state_only["coherences"]["M_H"] == canonical["coherences"]["M_H"]
        and state_only["coherences"]["P"] != canonical["coherences"]["P"]
        and state_only["feedback"]["boundary_polarity_score"]
        != canonical["feedback"]["boundary_polarity_score"]
        and "front_node_ids=tuple(role_ids[role] for role in front_roles)" in prepare_feedback
        and "model" not in readout
    )

    h_independent = (
        _passed(assertions, "cross.history_only_preserves_P", "cross.history_only_changes_joint_response")
        and history_only["coherences"]["P"] == canonical["coherences"]["P"]
        and history_only["tokens"] != canonical["tokens"]
        and history_only["coherences"]["M_H"] != canonical["coherences"]["M_H"]
        and execute_branch.index("adapter.replace_history")
        < execute_branch.index(
            "base._materialize", execute_branch.index("adapter.replace_history")
        )
        < execute_branch.index("_neutral_contact")
        < execute_branch.index("_prepare_feedback")
    )

    factorial = registry["qualitative_component_factorial"]
    factorial_safe = (
        len(factorial["cells"]) == 4
        and {item["cell_id"] for item in factorial["cells"]} == {
            "P_reference__H_reference", "P_candidate__H_reference",
            "P_reference__H_candidate", "P_candidate__H_candidate",
        }
        and factorial["scientific_values_selected"] is False
        and "not executed" in next(
            item["i03c_conformance_witness"]
            for item in factorial["cells"]
            if item["cell_id"] == "P_reference__H_candidate"
        )
    )

    continuous = registry["continuous_joint_causality"]
    threshold_safe = (
        continuous["nonlinearity_required"] is False
        and len(continuous["raw_fields_required_for_later_retention"]) == 8
        and "cannot define hybrid" in continuous["threshold_rule"]
        and all(key in canonical["feedback"] for key in ("front_mass", "boundary_polarity_score"))
        and all(key in canonical["response"] for key in ("scheduled", "reason_code", "response_delta"))
    )

    admission = registry["admission_filter"]
    admission_source_safe = all(token in ingest for token in (
        "row.surface_kind != ROUTE_LOCAL_CONTACT",
        "row.pulse_event_kind != PACKET_ARRIVAL",
        "row.target_node_id",
        "pool_target_node_id",
        "row.source_node_id",
        "registered_sources",
        "digest not in consumed",
    ))
    excluded_traffic = {item["traffic"] for item in admission["excluded_traffic"]}
    all_traffic_safe = excluded_traffic == {
        "M_H materialization", "common neutral contact", "P-only debit",
        "native response", "feedback eligibility row", "reset/load",
        "private contribution/materialization", "write diversion",
    }
    token_fields = set(canonical["tokens"][0])
    token_safe = (
        token_fields == {"sequence_index", "contact_amount", "operation_kind", "inter_arrival_interval"}
        and set(admission["forbidden_token_fields"]).issuperset({
            "source node identity", "contributor role/name", "source/target lineage",
            "event ID", "packet ID", "row/surface digest", "contributor count", "branch ID",
        })
    )

    neutral = registry["neutral_contact"]
    neutral_assertions = [f"{branch}.neutral_latest" for branch in STANDARD_BRANCHES]
    neutral_queue_assertions = [f"{branch}.queue_drained" for branch in STANDARD_BRANCHES]
    neutral_safe = (
        _passed(assertions, *neutral_assertions, *neutral_queue_assertions)
        and runtime_freeze["fixture"]["neutral_contact"] == {
            "source": "E_source", "target": "E_target",
            "edge_role": "E_source_to_E_target", "amount": 0.013,
            "source_lineage_id": "lineage:hybrid-neutral-source",
            "target_lineage_id": "lineage:hybrid-neutral-target",
        }
        and all(
            conformance["branches"][branch]["feedback"]["source_surface_digest"]
            == conformance["branches"][branch]["feedback"]["neutral_trigger_digest"]
            and conformance["branches"][branch]["feedback"]["expected_source_surface_digest"] is None
            for branch in STANDARD_BRANCHES
        )
        and "polarity_score = (front_mass - rear_mass) - reference" in emit_feedback
        and "signed_feedback < threshold" in producer
        and "expected_source_digest != source_surface_digest" in producer
        and "absolute event/scheduler indices are not identical" in neutral["absolute_schedule_qualification"]
    )
    neutral_slots = {
        branch: conformance["branches"][branch]["feedback"]["response_slot"]
        for branch in ("combined_q1_q2", "state_only_debit", "history_only_clamp")
    }

    mask = registry["mask_identity"]
    common_mask_safe = (
        mask["common_front"] == ["P", "M_H"]
        and mask["common_rear"] == ["B_ref"]
        and _passed(assertions, *[
            check
            for branch in STANDARD_BRANCHES
            for check in (f"{branch}.joint_mask", f"{branch}.mask_exact_once", f"{branch}.rear_mask")
        ])
        and "for node_id in front_nodes" in emit_feedback
        and "for node_id in rear_nodes" in emit_feedback
        and _passed(assertions, "private.separate_joint_masks", "private.no_common_or_cross_pair")
    )

    intervention = registry["component_interventions"]
    p_pure = p_independent and set(intervention["P_only"]["held_fixed"]).issuperset({
        "H_P tokens", "R_H", "M_H", "B_ref", "response configuration", "joint masks"
    })
    h_pure = h_independent and intervention["H_only"]["direct_scalar_clamp_forbidden"] is True
    same_joint_path = (
        intervention["joint"]["V"] == "identical [P,M_H]/[B_ref] native feedback/producer path"
        and canonical["feedback"]["front_node_ids"]
        == state_only["feedback"]["front_node_ids"]
        == history_only["feedback"]["front_node_ids"]
        and _passed(assertions, "cross.both_components_required_same_joint_path")
    )

    common_private = registry["common_private_binding"]
    common_binding_safe = (
        common_private["common"]["writers"] == ["S1", "S2"]
        and common_private["common"]["mask"] == ["P", "M_H"]
        and _passed(assertions, "cross.alternate_same_common_mask", "cross.alternate_same_relation")
    )
    private_safe = (
        len(common_private["private"]) == 2
        and len(private["private_histories"]) == 2
        and private["aggregation_performed"] is False
        and _passed(assertions, "private.tokens", "private.separate_joint_masks", "private.no_common_or_cross_pair", "private.adapter_boundary")
        and "h1 = base._adapter" in private_branch
        and "h2 = base._adapter" in private_branch
    )

    layered = registry["layered_hybrid_identity"]
    hashes = layered["exact_package_hashes"]
    identity_safe = (
        len(layered["layers"]) == 6
        and hashes["runtime_freeze_sha256"] == EXPECTED_RUNTIME_FREEZE_SHA256
        and hashes["runtime_evidence_sha256"] == EXPECTED_RUNTIME_SHA256
        and hashes["harness_sha256"] == _sha256(harness_path)
        and hashes["adapter_sha256"] == _sha256(adapter_path)
        and len(layered["fail_closed_rules"]) == 6
        and _passed(assertions, "restoration.paired_load_identity", "restoration.manifest_validated", "restoration.paired_reset_equal", "restoration.reset_initial_identity")
        and receipt["identity"]["byte_identical"] is True
    )
    hm_consistent = (
        history_authoritative
        and _passed(assertions, *[
            check
            for branch in STANDARD_BRANCHES
            for check in (f"{branch}.readout", f"{branch}.materialized")
        ])
        and _passed(assertions, "restoration.paired_load_identity", "restoration.equal_saved_continuation", "restoration.equal_reset_continuation")
        and "adapter.restoration_identity_digest()" in composite_summary
        and "adapter.restoration_identity_digest()" in adapter_load
    )
    paired_safe = (
        identity_safe
        and "model.save" in restoration and "adapter.save" in restoration
        and "LGRC9V3.load" in restoration and "RCAEActiveHistoryAdapterV1.load" in restoration
        and "model.reset()" in restoration and "adapter.reset()" in restoration
        and "self._state = deepcopy(self._reset_baseline)" in adapter_reset
        and receipt["invocation_accounting"]["retries"] == 0
    )

    lifecycle = registry["lifecycle_dispositions"]
    lifecycle_safe = (
        len(lifecycle) == 11
        and {item["property"] for item in lifecycle} == {
            "maximum H_P length", "overflow behavior", "token retention window",
            "truncation", "saturation", "leakage/decay", "replacement/clamp",
            "reset", "maintenance cost", "P capacity/bounds", "M_H bounds",
        }
        and all(item["status"] in {
            "fixture_bounded", "deferred_I06", "not_selected", "not_applicable_to_conformance",
            "not_applicable", "implemented", "implemented_bounded",
        } for item in lifecycle)
    )

    ops = registry["hybrid_operational_hypotheses"]
    ops_safe = (
        [item["op_id"] for item in ops] == EXPECTED_OPS
        and [item["op_id"] for item in contract["operational_projections"]] == EXPECTED_OPS
        and all("hybrid" in item["meaning"] or key in item["meaning"] for item, key in zip(
            ops, ("P/H_P/M_H", "P and H_P", "P, H_P, M_H", "P-only", "state-only", "P1/H1", "P+R_H", "order reversal", "P/M_H/B_ref"), strict=True
        ))
    )

    quarantine = registry["fixture_quarantine_registry"]
    quarantine_safe = (
        len(quarantine["source_artifacts"]) == 7
        and len(quarantine["i03c_exact_numeric_inputs_and_observations"]) == 16
        and quarantine["i03c_exact_branch_ids"] == EXPECTED_BRANCHES
        and len(quarantine["i03c_hashes"]) == 4
        and "258/258" in quarantine["assertion_outcome_rule"]
        and all(value is False for key, value in conformance["quarantine"].items() if key.startswith("may_") or key == "observed_values_may_be_reused_scientifically")
        and conformance["scientific_evidence_assigned"] is False
    )
    modes_safe = (
        registry["program_boundary"]["retained_modes"] == [
            "state_carried: pygrc_native_candidate",
            "history_carried: minimally_producer_assisted",
            "hybrid: minimally_producer_assisted",
        ]
        and registry["program_boundary"]["selection_or_ranking_performed"] is False
        and registry["program_boundary"]["family_closeout_required"] is True
        and registry["program_boundary"]["discriminator_gate_passed"] is False
        and registry["program_boundary"]["I04_authorized"] is False
    )

    obligation_ids = [item["obligation_id"] for item in registry["downstream_obligations"]]
    if obligation_ids != [f"I03CR1-OBL-{index:02d}" for index in range(1, 9)]:
        raise AssertionError("downstream obligation identity drifted")

    checks = [
        _result("RV-01", "exact_hybrid_composite_carrier_identity", carrier_safe, "direct_pass", "One stable bound P + authoritative H_P/M_H + common-access carrier is explicit; all single-component/query/controller substitutes are rejected.", carrier),
        _result("RV-02", "not_merely_two_node_state_carried", carrier_safe and history_authoritative, "direct_pass", "Native V reads current P/M_H, but persistent independently intervenable/restorable H_P remains authoritative and M_H is a verified output port; claim is architectural and not irreducible-history.", registry["authoritative_history_output_rule"]),
        _result("RV-03", "P_independent_nonredundant_native_input", p_independent, "direct_pass", "P is in the exact native mask once; adapter R_H never reads P; same H_P/M_H with changed P changes the raw native score.", {"canonical": {"P": canonical["coherences"]["P"], "M_H": canonical["coherences"]["M_H"], "score": canonical["feedback"]["boundary_polarity_score"]}, "P_only": {"P": state_only["coherences"]["P"], "M_H": state_only["coherences"]["M_H"], "score": state_only["feedback"]["boundary_polarity_score"]}}),
        _result("RV-04", "H_P_authoritative_nonredundant_chain", h_independent and history_authoritative, "direct_pass", "H-only clamp changes authoritative H_P, recomputes/materializes M_H through native packets, preserves P, and then changes the same native score.", {"canonical": {"tokens": canonical["tokens"], "P": canonical["coherences"]["P"], "M_H": canonical["coherences"]["M_H"]}, "H_only": {"tokens": history_only["tokens"], "P": history_only["coherences"]["P"], "M_H": history_only["coherences"]["M_H"]}}),
        _result("RV-05", "complete_qualitative_two_component_factorial", factorial_safe, "closure_clarification", "The full qualitative 2x2 is now frozen before science. I03C demonstrated perturbation feasibility, not a complete scientific 2x2; the P-reference/H-candidate cell remains an exact I04/I06 duty.", factorial, obligations=["I03CR1-OBL-01"]),
        _result("RV-06", "hybrid_not_defined_by_threshold_crossing", threshold_safe, "direct_pass", "Raw P, H_P/R_H/M_H, native score, producer decision, and continuation remain distinct; fixture threshold crossing cannot define hybrid or be inherited scientifically.", continuous),
        _result("RV-07", "nonlinearity_interaction_and_synergy_not_required", threshold_safe and len(carrier["prohibited_claims"]) >= 8, "direct_pass", "I03C requires two causal components in one V, not nonlinearity, interaction, synergy, superadditivity, or irreducibility.", carrier["prohibited_claims"]),
        _result("RV-08", "adapter_self_admission_and_recursive_growth_excluded", admission_source_safe and all_traffic_safe, "direct_pass", "Exact filter conjunction excludes materialization, neutral, debit, response, feedback, reset/load, private, and diversion traffic; unseen suffix plus digest set provides exactly-once admission.", admission["excluded_traffic"]),
        _result("RV-09", "unique_physical_admission_route_or_explicit_key", admission_source_safe and admission["fixture_unique_route_status"].startswith("adequate"), "downstream_obligation", "Fixture common S-to-P paths are unique and role-physical; exact scientific route/channel identity remains an I06 registration duty and cannot use labels/digests.", {"fixture": admission["fixture_unique_route_status"], "later": admission["i06_route_rule"]}, obligations=["I03CR1-OBL-02"]),
        _result("RV-10", "token_schema_excludes_disguised_source_identity", token_safe, "downstream_obligation", "Tokens contain only sequence, physical amount/type, and interval. I06 must reject contributor-unique types/amounts used solely as disguised identity.", {"token_fields": sorted(token_fields), "typed_amount_guard": admission["typed_amount_guard"]}, obligations=["I03CR1-OBL-02"]),
        _result("RV-11", "common_neutral_contact_fully_qualified", neutral_safe, "downstream_obligation", "Every response branch uses the same neutral route/type/amount in final relative position, excluded from H_P, with empty queue and null digest authorization. Absolute audit slots differ after explicit operations but do not enter live-state score/polarity/threshold; I06 must match any scientifically causal timing fields.", {"configuration": neutral["fixture_configuration"], "response_slots": neutral_slots, "qualification": neutral["absolute_schedule_qualification"]}, obligations=["I03CR1-OBL-03"]),
        _result("RV-12", "exact_distinct_multi_node_mask_and_live_read", common_mask_safe, "direct_pass", "P and M_H are distinct live nodes read exactly once, B_ref is the only rear node, no cached aggregate enters, and private reads use only their own pairs.", mask),
        _result("RV-13", "P_only_intervention_purity", p_pure, "direct_pass", "Native P debit preserves H_P/R_H/M_H, adapter identity, contribution audit, B_ref/config/masks, and follows with the common neutral contact; score changes through P.", intervention["P_only"]),
        _result("RV-14", "H_only_intervention_purity", h_pure, "direct_pass", "Explicit H_P replacement/rematerialization preserves P and native contributions; adapter cannot scalar-clamp M_H or alter response configuration.", intervention["H_only"]),
        _result("RV-15", "joint_branch_uses_same_component_constructions_and_V", same_joint_path, "direct_pass", "Joint and component-intervention branches share the same contribution/adapter construction and exact native V; only named component state differs.", intervention["joint"]),
        _result("RV-16", "one_common_composite_pool_binding", common_binding_safe and carrier_safe, "direct_pass", "Both writers constitute one bound P/H_P/M_H surface and alternate responders use the same common mask without contributor address.", common_private["common"]),
        _result("RV-17", "private_competitor_isolated_and_no_cross_pair", private_safe, "downstream_obligation", "Private nodes, adapters, histories, masks, and responses are isolated with no aggregate/dispatcher. Exact manifest cross-load failure injection remains I06.", {"private": common_private["private"], "guards": common_private["guards"]}, obligations=["I03CR1-OBL-04", "I03CR1-OBL-07"]),
        _result("RV-18", "complete_layered_hybrid_identity", identity_safe, "closure_clarification", "Completeness is explicitly layered across native v2, adapter current/reset, joint binding, runtime freeze, paired manifest, evidence, and reconstruction—not claimed as one native atomic API.", layered, obligations=["I03CR1-OBL-04", "I03CR1-OBL-07"]),
        _result("RV-19", "H_P_to_M_H_coherence_invariant", hm_consistent, "direct_pass", "Adapter fails closed unless native M_H equals R_H(H_P); branch, clamp/order, load/reset, and continuation identities retain the relation.", registry["authoritative_history_output_rule"]),
        _result("RV-20", "paired_save_load_reset_atomic_boundary", paired_safe, "downstream_obligation", "Paired save/load/reset and equal-input continuation passed. One atomic public interface plus partial/mismatch/cross-load/repeated-reset failure injection remains I06.", {"demonstrated": layered["demonstrated"], "deferred": layered["not_demonstrated_and_deferred"]}, obligations=["I03CR1-OBL-04"]),
        _result("RV-21", "bounded_history_and_pool_lifecycle_semantics", lifecycle_safe, "closure_clarification", "All requested lifecycle/economy properties now have explicit implemented, fixture-bounded, deferred, not-selected, or not-applicable dispositions and rationale.", lifecycle, obligations=["I03CR1-OBL-05"]),
        _result("RV-22", "all_nine_OPs_have_hybrid_specific_semantics", ops_safe, "direct_pass", "OP-01..OP-09 each retain hybrid-specific composite, intervention, exclusion, order, and access meanings without assigning R01-R05.", ops),
        _result("RV-23", "complete_machine_fixture_quarantine_registry", quarantine_safe, "closure_clarification", "A recursive seven-source rejection registry covers all three modes and explicitly indexes every I03C numeric value, branch/topology identity, comparator, observation/outcome, and digest for direct/trivial-copy rejection.", quarantine, obligations=["I03CR1-OBL-06"]),
        _result("RV-24", "258_of_258_claim_boundary_machine_visible", quarantine_safe and conformance["evidence_class"] == "quarantined_realization_implementation_conformance", "direct_pass", "258/258 is machine-visible only as synthetic implementation conformance; it assigns no robustness, scientific control passage, R03/R04, support, calibration, or lane result.", {"summary": conformance["assertion_summary"], "evidence_class": conformance["evidence_class"], "quarantine": conformance["quarantine"]}),
        _result("RV-25", "three_modes_retained_without_ranking", modes_safe, "direct_pass", "State, history, and hybrid remain separately retained with their own realization classes; no preference, supersession, or rank is assigned.", registry["program_boundary"]["retained_modes"]),
        _result("RV-26", "separate_umbrella_I03_family_closeout_required", modes_safe, "direct_pass", "I03C owner acceptance may open only a separately declared umbrella family closeout. That action may pass only the discriminator gate and open I04; I04 is currently closed.", registry["program_boundary"], obligations=["I03CR1-OBL-08"]),
    ]

    if [item["check_id"] for item in checks] != [item["id"] for item in freeze["review_checks"]]:
        raise AssertionError("review-check identity/order drifted")
    classification_counts = {
        name: sum(item["classification"] == name for item in checks)
        for name in ("direct_pass", "closure_clarification", "downstream_obligation")
    }
    if classification_counts != {"direct_pass": 17, "closure_clarification": 4, "downstream_obligation": 5}:
        raise AssertionError("review classification count drifted")

    acceptance_to_checks = {
        "AT-01": ["RV-01", "RV-16"], "AT-02": ["RV-02", "RV-04", "RV-19"],
        "AT-03": ["RV-03", "RV-12", "RV-13"], "AT-04": ["RV-04", "RV-14"],
        "AT-05": ["RV-05", "RV-15"], "AT-06": ["RV-06", "RV-07"],
        "AT-07": ["RV-11"], "AT-08": ["RV-08", "RV-09"],
        "AT-09": ["RV-10"], "AT-10": ["RV-17"], "AT-11": ["RV-03", "RV-04", "RV-15"],
        "AT-12": ["RV-16", "RV-18", "RV-20"], "AT-13": ["RV-04", "RV-19"],
        "AT-14": ["RV-21"], "AT-15": ["RV-23", "RV-24"],
        "AT-16": ["RV-25"], "AT-17": ["RV-26"],
    }
    check_map = {item["check_id"]: item for item in checks}
    acceptance_results = []
    for statement in freeze["acceptance_statements"]:
        ids = acceptance_to_checks[statement["id"]]
        if not all(check_map[item]["status"] == "passed" for item in ids):
            raise AssertionError(f"acceptance condition failed: {statement['id']}")
        acceptance_results.append({
            "acceptance_id": statement["id"],
            "status": "passed",
            "statement": statement["text"],
            "supporting_review_checks": ids,
        })

    graph_after = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "status_porcelain": _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"),
    }
    if graph_after != graph_before:
        raise AssertionError("graph checkout changed during zero-runtime audit")

    return {
        "artifact_id": "P2-I2-I03CR1-CLOSEOUT-REVALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I03CR1",
        "lane_id": "AE01-L02",
        "validated_at": "2026-07-14",
        "status": "passed_with_downstream_obligations",
        "closeout_gate": "P2-I2-I03CR1-CLOSEOUT-PASSED",
        "validation_kind": "zero_runtime_owner_review_source_dataflow_retained_artifact_causal_well_formedness_and_closure_registry_audit",
        "runtime_accounting": {
            "model_instantiations": 0,
            "runtime_evidence_invocations": 0,
            "runtime_reconstruction_invocations": 0,
            "retries": 0,
            "parameter_search": False,
            "retained_i03c_evidence_invocations_unchanged": 1,
            "retained_i03c_reconstruction_invocations_unchanged": 1,
        },
        "input_identity": {
            "input_freeze_path": str(input_path.relative_to(ROOT)),
            "input_freeze_sha256": _sha256(input_path),
            "owner_review_sha256": _sha256(owner_review),
            "registry_path": str(registry_path.relative_to(ROOT)),
            "registry_sha256": _sha256(registry_path),
            "immutable_i03c_input_count": len(immutable_checks),
            "immutable_i03c_inputs": immutable_checks,
        },
        "graph_before": graph_before,
        "graph_after": graph_after,
        "review_results": checks,
        "review_summary": {
            "total": len(checks),
            "passed": len(checks),
            "blocking_findings": 0,
            "classification_counts": classification_counts,
        },
        "acceptance_results": acceptance_results,
        "acceptance_summary": {"total": 17, "passed": 17, "failed": 0},
        "downstream_obligations": registry["downstream_obligations"],
        "downstream_obligation_count": len(registry["downstream_obligations"]),
        "important_qualifications": {
            "complete_scientific_2x2_executed_in_i03c": False,
            "complete_qualitative_2x2_now_frozen": True,
            "restoration_identity_is_layered_package_identity": True,
            "single_new_native_atomic_restoration_api_claimed": False,
            "neutral_absolute_scheduler_indices_matched": False,
            "neutral_absolute_indices_are_score_or_threshold_inputs": False,
            "failure_injection_deferred_to_i06": True,
        },
        "claim_boundary": {
            "i03c_closeout_acceptance_ready": True,
            "owner_acceptance_assigned": False,
            "scientific_evidence_assigned": False,
            "R01_through_R05_assigned": False,
            "mode_ranking_assigned": False,
            "discriminator_gate_passed": False,
            "umbrella_family_closeout_authorized": False,
            "I04_authorized": False,
        },
        "disposition": "I03C causally well formed as a bounded minimally producer-assisted hybrid implementation-conformance package; owner acceptance may open only a separately declared umbrella I03 family closeout, with eight fail-closed downstream obligations retained",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.input.resolve(), args.registry.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "review_summary": result["review_summary"],
        "acceptance_summary": result["acceptance_summary"],
        "downstream_obligation_count": result["downstream_obligation_count"],
        "runtime_accounting": result["runtime_accounting"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
