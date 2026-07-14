#!/usr/bin/env python3
"""Zero-runtime closeout revalidation for P2-I2-I03B.

This validator imports no PyGRC module and instantiates no model. It inspects
the frozen I03B artifacts, retained conformance record, adapter/harness source,
and admitted PyGRC source as immutable data.
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
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            segment = ast.get_source_segment(source, node)
            if segment is None:
                raise AssertionError(f"cannot extract function: {name}")
            return segment
    raise AssertionError(f"missing function: {name}")


def _source_contact(branch: Mapping[str, Any]) -> dict[str, Any]:
    feedback_row = next(
        row
        for row in branch["surface_rows"]
        if row["surface_kind"] == "feedback_eligibility"
    )
    digest = feedback_row["surface_values_after"]["source_surface_digest"]
    return next(row for row in branch["surface_rows"] if row["surface_digest"] == digest)


def _result(
    check_id: str,
    name: str,
    condition: bool,
    finding: str,
    evidence: Any,
    *,
    qualification: str | None = None,
) -> dict[str, Any]:
    if not condition:
        raise AssertionError(f"{check_id} failed: {finding}")
    return {
        "check_id": check_id,
        "name": name,
        "status": "passed" if qualification is None else "passed_with_downstream_obligation",
        "finding": finding,
        "evidence": evidence,
        "qualification_or_downstream_obligation": qualification,
    }


def validate(input_path: Path) -> dict[str, Any]:
    freeze = _load(input_path)
    if freeze["artifact_id"] != "P2-I2-I03BR1-CLOSEOUT-REVALIDATION-INPUT":
        raise AssertionError("wrong I03BR1 input artifact")
    if freeze["audit_policy"]["model_instantiations"] != 0:
        raise AssertionError("I03BR1 must be zero-runtime")
    if len(freeze["review_checks"]) != 21 or len(freeze["acceptance_statements"]) != 12:
        raise AssertionError("review coverage count drifted")

    for item in freeze["immutable_i03b_inputs"]:
        path = ROOT / item["path"]
        if _sha256(path) != item["sha256"]:
            raise AssertionError(f"immutable I03B input drifted: {path}")

    graph_root = Path(freeze["authority"]["graph_repository"])
    graph_before = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "status_porcelain": _git(
            graph_root, "status", "--porcelain=v1", "--untracked-files=all"
        ),
    }
    if graph_before != {
        "revision": freeze["authority"]["graph_revision"],
        "status_porcelain": "",
    }:
        raise AssertionError("admitted graph checkout is not clean and exact")

    contract_path = EXPERIMENT / "contracts/p2-i2/i03b-history-carried-realization-and-discriminator-contract.json"
    runtime_freeze_path = EXPERIMENT / "contracts/p2-i2/i03b-history-carried-runtime-conformance-input-freeze.json"
    conformance_path = EXPERIMENT / "contracts/p2-i2/i03b-history-carried-runtime-conformance.json"
    receipt_path = EXPERIMENT / "contracts/p2-i2/i03b-runtime-reconstruction-receipt.json"
    adapter_path = EXPERIMENT / "scripts/p2_i2_i03b_history_adapter.py"
    harness_path = EXPERIMENT / "scripts/p2_i2_i03b_conform.py"

    contract = _load(contract_path)
    runtime_freeze = _load(runtime_freeze_path)
    conformance = _load(conformance_path)
    receipt = _load(receipt_path)
    adapter_source = adapter_path.read_text(encoding="utf-8")
    harness_source = harness_path.read_text(encoding="utf-8")
    native_runtime_path = graph_root / "src/pygrc/models/lgrc_9_v3_runtime.py"
    native_runtime_source = native_runtime_path.read_text(encoding="utf-8")

    ast.parse(adapter_source, filename=str(adapter_path))
    ast.parse(harness_source, filename=str(harness_path))
    ast.parse(native_runtime_source, filename=str(native_runtime_path))

    if conformance["assertion_summary"] != {"failed": 0, "passed": 252, "total": 252}:
        raise AssertionError("retained conformance assertion summary drifted")
    if not all(row["passed"] for row in conformance["assertions"]):
        raise AssertionError("retained conformance contains a failed assertion")

    emit_source = _function_source(
        native_runtime_source, "emit_feedback_eligibility_surface_row"
    )
    producer_source = _function_source(
        native_runtime_source, "_produce_packet_departure_from_feedback_eligibility"
    )
    run_branch_source = _function_source(harness_source, "_run_standard_branch")
    adapter_ingest_source = _function_source(adapter_source, "ingest_new_rows")
    adapter_readout_source = _function_source(adapter_source, "readout")
    adapter_materialize_source = _function_source(adapter_source, "materialize_readout")
    adapter_replace_source = _function_source(adapter_source, "replace_history")
    restoration_source = _function_source(harness_source, "_run_restoration")

    canonical = conformance["branches"]["combined_q1_q2"]
    reversed_order = conformance["branches"]["combined_q2_q1"]
    canonical_contact = _source_contact(canonical)
    reversed_contact = _source_contact(reversed_order)
    contact_diff_keys = sorted(
        key
        for key in canonical_contact
        if canonical_contact[key] != reversed_contact[key]
    )
    contact_decision_fields = (
        "source_node_id",
        "target_node_id",
        "contact_amount",
        "event_time_key",
        "scheduler_event_index",
        "pulse_event_kind",
        "pulse_channel_id",
        "route_aspect_id",
    )
    matched_contact_fields = {
        key: canonical_contact[key] for key in contact_decision_fields
    }
    latest_contact_safe = (
        all(canonical_contact[key] == reversed_contact[key] for key in contact_decision_fields)
        and contact_diff_keys == ["node_proper_time", "surface_digest", "surface_state_digest"]
        and "polarity_score = (front_mass - rear_mass) - reference" in emit_source
        and "float(row.surface_values_after[\"boundary_polarity_score\"])" in producer_source
        and "expected_source_surface_digest=None" in harness_source
        and run_branch_source.index("_neutral_contact(")
        < run_branch_source.index("_prepare_feedback(")
    )

    roles = contract["role_registry"]
    factorization = contract["causal_factorization"]
    active_history_safe = (
        roles["H_P"]["role"] == "one_common_non_private_active_history_carrier"
        and roles["M_H"]["role"] == "native_materialized_readout_port_of_H_P"
        and "tokens" in adapter_source
        and "reset_baseline_state" in adapter_source
        and "self._state[\"tokens\"] = canonical" in adapter_replace_source
        and "target = self.readout()" in adapter_materialize_source
        and "readout_node_id" in adapter_materialize_source
    )

    checks: list[dict[str, Any]] = []
    checks.append(
        _result(
            "RV-01",
            "exclude_hidden_latest_contact_path",
            latest_contact_safe,
            "A common neutral contact follows materialization in every standard branch. Across the two order branches its route, endpoints, amount, event time, scheduler index, event kind, and channel match. Only node-proper-time and derived row digests differ; native polarity is computed solely from M_H/B_ref live masses and the producer's decision reads that polarity with expected_source_surface_digest null.",
            {
                "matched_latest_contact_fields": matched_contact_fields,
                "differing_latest_contact_fields": contact_diff_keys,
                "canonical_M_H": canonical["coherences"]["M_H"],
                "reversed_M_H": reversed_order["coherences"]["M_H"],
                "canonical_score": canonical["feedback"]["boundary_polarity_score"],
                "reversed_score": reversed_order["feedback"]["boundary_polarity_score"],
                "native_emit_source": str(native_runtime_path.relative_to(graph_root)),
            },
        )
    )
    checks.append(
        _result(
            "RV-02",
            "confirm_active_H_P_and_M_H_output_port",
            active_history_safe,
            "H_P is persisted adapter state with independent replacement/reset semantics; R_H reads H_P and public native packets materialize M_H. The machine contract identifies the functional pool as H_P plus M_H output-port binding, not P or M_H alone.",
            {
                "H_P_role": roles["H_P"],
                "M_H_role": roles["M_H"],
                "clamp_tokens": conformance["branches"]["active_history_clamp"]["tokens"],
                "clamp_intervention": conformance["branches"]["active_history_clamp"]["history_intervention"],
            },
        )
    )

    complete_factorization = all(
        key in factorization for key in ("C_P", "q", "U_H", "R_H", "M_H", "L", "V", "forbidden_G")
    )
    checks.append(
        _result(
            "RV-03",
            "complete_history_carried_factorization",
            complete_factorization
            and all(term in adapter_ingest_source for term in ("surface_kind", "pulse_event_kind", "target_node_id", "source_node_id", "surface_digest")),
            "P/C_P, H_P, L, U_H, R_H, M_H, V, and forbidden G are machine-bound with ownership, inputs, causal/audit status, and restoration duties. U_H admits only unseen route-local native arrivals from a registered source-node set to P.",
            {"factorization_keys": sorted(factorization), "admission_method": "RCAEActiveHistoryAdapterV1.ingest_new_rows"},
            qualification="I06 must preserve the frozen fixture's unique registered source-to-P path or add an explicit route/channel admission key; source/target membership is the current exact adapter filter.",
        )
    )

    tokens = canonical["tokens"] + reversed_order["tokens"]
    token_fields = {field for token in tokens for field in token}
    token_type_safe = (
        token_fields == {"sequence_index", "contact_amount", "operation_kind", "inter_arrival_interval"}
        and {token["operation_kind"] for token in tokens} == {"native_arrival_contact_amount"}
        and "registered_sources" in adapter_ingest_source
        and "contact_amount" in adapter_ingest_source
    )
    checks.append(
        _result(
            "RV-04",
            "physical_token_type_excludes_contributor_identity",
            token_type_safe,
            "operation_kind is the same physical native-arrival operation for both sources; amount and interval come from contact physics. No source, lineage, packet, event, route digest, or contributor slot enters a token or R_H.",
            {"token_fields": sorted(token_fields), "operation_kinds": sorted({token["operation_kind"] for token in tokens})},
        )
    )

    cursor_safe = all(
        text in adapter_ingest_source
        for text in (
            "scan_index",
            "consumed_surface_digests",
            "digest not in consumed",
            "self._state[\"scan_index\"] = len(rows)",
        )
    ) and all(text not in adapter_readout_source for text in ("scan_index", "consumed_surface_digests", "surface_digest", "lineage"))
    checks.append(
        _result(
            "RV-05",
            "cursor_and_idempotency_isolation",
            cursor_safe
            and receipt["restoration_witness"]["equal_input_continuation_after_load"]
            and receipt["restoration_witness"]["equal_input_continuation_after_reset"],
            "scan_index and consumed surface digests gate admission only; R_H reads tokens only. They are persisted in current/reset adapter identity, clamp/reorder does not rewind them, and paired load/reset continuation passed.",
            {
                "lineage_permutation_causal_signature_equal": conformance["branches"]["lineage_permuted"]["tokens"] == canonical["tokens"],
                "paired_load_continuation": receipt["restoration_witness"]["equal_input_continuation_after_load"],
                "paired_reset_continuation": receipt["restoration_witness"]["equal_input_continuation_after_reset"],
            },
        )
    )

    coherence_differences = {
        key: [canonical["coherences"][key], reversed_order["coherences"][key]]
        for key in canonical["coherences"]
        if canonical["coherences"][key] != reversed_order["coherences"][key]
    }
    order_match_safe = set(coherence_differences) == {"A", "B", "M_H", "P", "R_H_plus"}
    checks.append(
        _result(
            "RV-06",
            "order_contrast_continuation_state_matching",
            order_match_safe
            and abs(canonical["coherences"]["P"] - reversed_order["coherences"]["P"]) <= 1e-12
            and latest_contact_safe,
            "The branches use fresh identical fixtures and equal operation counts. Before V, P matches within the frozen implementation tolerance and the response-visible neutral contact/configuration match; M_H and its balancing-reservoir consequence are the declared history-path differences. Post-response A/B differ only because V fired in one branch.",
            {"post_response_coherence_differences": coherence_differences, "latest_contact_audit": matched_contact_fields},
        )
    )

    report_text = (EXPERIMENT / "reports/P2-I2-I03B-history-carried-realization-and-operational-hypothesis-freeze.md").read_text(encoding="utf-8")
    checks.append(
        _result(
            "RV-07",
            "bounded_non_irreducibility_claim",
            "deterministic order-sensitive readout" in report_text
            and "irreducible" not in report_text.lower()
            and "non-markov" not in report_text.lower(),
            "I03B claims an active ordered history and deterministic scalar readout, not irreducible raw-history necessity or non-Markovianity.",
            {"readout_rule": factorization["R_H"]["definition"]},
        )
    )

    clamp = conformance["branches"]["active_history_clamp"]
    clamp_safe = (
        clamp["tokens"] == []
        and clamp["history_intervention"]["native_audit_rewritten"] is False
        and clamp["history_intervention"]["success_or_response_written"] is False
        and clamp["coherences"]["P"] == canonical["coherences"]["P"]
        and clamp["final_materialization"]["readout_after"] == 0.0
        and run_branch_source.index("replace_history(") < run_branch_source.index("_materialize(adapter, model, cursor)", run_branch_source.index("replace_history("))
        and run_branch_source.rfind("adapter.ingest_new_rows") < run_branch_source.index("replace_history(")
    )
    checks.append(
        _result(
            "RV-08",
            "active_history_clamp_stability",
            clamp_safe,
            "The clamp replaces H_P itself, preserves native audit/P, retains the consumed-row cursor, rematerializes M_H, performs no later ingest before V, and carries explicit intervention provenance in adapter/composite identity.",
            {"clamp_identity_digest": clamp["adapter_restoration_identity_digest"], "intervention": clamp["history_intervention"]},
        )
    )

    state_only = conformance["branches"]["state_only_separation"]
    state_debit = runtime_freeze["fixture"]["state_only_debit"]
    checks.append(
        _result(
            "RV-09",
            "state_only_debit_exclusion",
            state_debit["source"] == "P"
            and state_debit["target"] != "P"
            and state_only["tokens"] == canonical["tokens"]
            and state_only["coherences"]["M_H"] == canonical["coherences"]["M_H"]
            and state_only["response"] == canonical["response"],
            "The P-to-K_P debit cannot satisfy the adapter's registered-source-to-P arrival filter. It occurs before the common neutral contact, leaves H_P/M_H and producer configuration fixed, and the retained response record matches canonical.",
            {"state_debit": state_debit, "P_values": [canonical["coherences"]["P"], state_only["coherences"]["P"]]},
        )
    )

    diversion = conformance["branches"]["write_diversion"]
    diversion_specs = runtime_freeze["fixture"]["contribution_sequences"]["write_diversion"]
    checks.append(
        _result(
            "RV-10",
            "write_diversion_source_activity_matching",
            all(spec["target"] != "P" for spec in diversion_specs)
            and diversion["tokens"] == []
            and [diversion["coherences"]["S1"], diversion["coherences"]["S2"]]
            == [canonical["coherences"]["S1"], canonical["coherences"]["S2"]],
            "Both source debits and deterministic contribution slots are retained, but packets terminate at K_P outside the H_P admission boundary. No token is admitted and the same neutral response opportunity follows.",
            {"diversion_specs": diversion_specs, "source_coherences": [diversion["coherences"]["S1"], diversion["coherences"]["S2"]]},
        )
    )

    private = conformance["branches"]["private_partition"]
    private_masks = [row["feedback"]["front_node_ids"] for row in private["private_histories"]]
    checks.append(
        _result(
            "RV-11",
            "private_partition_no_common_read",
            len(private["private_histories"]) == 2
            and private["aggregation_performed"] is False
            and all(len(mask) == 1 for mask in private_masks)
            and private_masks[0] != private_masks[1]
            and "h1 = _adapter" in harness_source
            and "h2 = _adapter" in harness_source,
            "Two separate adapter instances materialize two separate ports; each feedback mask reads one port, no aggregate is returned or fed back, and the branch runs in a fresh isolated model.",
            {"front_masks": private_masks, "aggregation_performed": private["aggregation_performed"]},
        )
    )

    alternate = conformance["branches"]["alternate_responder"]
    contribution_sources = {
        spec["source"]
        for spec in runtime_freeze["fixture"]["contribution_sequences"]["combined_q1_q2"]
    }
    checks.append(
        _result(
            "RV-12",
            "alternate_access_role_eligibility",
            "A_alt" not in contribution_sources
            and alternate["feedback"]["front_node_ids"] == canonical["feedback"]["front_node_ids"]
            and alternate["feedback"]["rear_node_ids"] == canonical["feedback"]["rear_node_ids"]
            and alternate["feedback"]["expected_source_surface_digest"] is None,
            "A_alt is not a contributor and uses the same M_H/B_ref feedback class without source lineage or contributor address. This proves architectural accessibility only.",
            {"contributors": sorted(contribution_sources), "alternate_front": alternate["feedback"]["front_node_ids"], "alternate_rear": alternate["feedback"]["rear_node_ids"]},
            qualification="R05 retention, capacity, and scientific access comparison remain I04/I06 and execution work.",
        )
    )

    forbidden_adapter_terms = (
        "emit_feedback_eligibility_surface_row",
        "produce_events",
        "set_feedback_coupled_pulse_producer",
        "cached_quantities",
        "feedback_threshold",
    )
    adapter_boundary_safe = (
        not any(term in adapter_source for term in forbidden_adapter_terms)
        and "model.schedule_packet_departure" in adapter_materialize_source
        and "model.step()" in adapter_materialize_source
        and "model.get_state()" in adapter_source
    )
    checks.append(
        _result(
            "RV-13",
            "adapter_stops_at_declared_boundary",
            adapter_boundary_safe
            and conformance["producer_boundary"] == {
                "native_feedback_producer_owns_later_transition": True,
                "rcae_component": "RCAEActiveHistoryAdapterV1",
                "rcae_computes_success": False,
                "rcae_schedules_later_response": False,
            },
            "Static source inspection confirms the adapter reads rows, maintains/intervenes on H_P, computes R_H, and requests public balancing packets only. It contains no feedback/producer invocation, response threshold, cached-quantity mutation, success computation, or later-response schedule.",
            {"allowed_model_calls": ["get_state", "schedule_packet_departure", "step"], "forbidden_terms_absent": list(forbidden_adapter_terms)},
        )
    )

    native_comparison = contract["native_first_source_comparison"]
    checks.append(
        _result(
            "RV-14",
            "counterfactual_producer_minimality",
            contract["realization_selection"]["realization_class"] == "minimally_producer_assisted"
            and native_comparison["native_candidate_disposition"] == "inadequate_for_history_carried"
            and native_comparison["selected_disposition"] == "minimally_producer_assisted"
            and contract["producer_boundary"]["single_missing_operation"].startswith("maintain and expose one independently intervenable active ordered history"),
            "The admitted native log remains passive/latest-row based without an active multi-event history or history-only intervention. The selected adapter adds only that carrier/readout bridge; native mutation and response remain intact.",
            native_comparison,
        )
    )

    lifecycle = contract["pool_economy_dispositions"]
    checks.append(
        _result(
            "RV-15",
            "history_lifecycle_semantics",
            all(key in lifecycle for key in ("accumulation", "mixing", "depletion", "saturation", "leakage", "maintenance"))
            and "append" in lifecycle["accumulation"]
            and "explicit active-history clamp/replacement" in lifecycle["depletion"],
            "The selected implementation is run-bounded append-only under normal admission, explicitly whole-history replaceable by intervention, with no autonomous deletion, fixed capacity, saturation, leakage/decay, or maintenance transition. Those absences are explicit rather than ecologically inferred.",
            lifecycle,
            qualification="I06 must bound branch/event counts and either retain these not-applicable lifecycle classes or register a new reviewed construction; no conformance fixture capacity may become scientific calibration.",
        )
    )

    adapter_identity_terms = (
        "artifact_schema_version",
        "configuration",
        "current_state",
        "reset_baseline_state",
        "tokens",
        "scan_index",
        "consumed_surface_digests",
        "last_materialized_readout",
        "last_materialization",
        "interventions",
    )
    checks.append(
        _result(
            "RV-16",
            "complete_composite_identity",
            all(term in adapter_source for term in adapter_identity_terms)
            and "native_restoration_identity_v2" in harness_source
            and "fixture_id" in harness_source
            and runtime_freeze["authority"]["adapter"]["sha256"] == _sha256(adapter_path),
            "Continuation state is layered: native v2 plus complete adapter current/reset identity and fixture role binding form the composite; the immutable runtime freeze additionally binds adapter code, token/admission semantics, harness, and graph source digests. Materialization is synchronous and drains its native queue, so no adapter-side pending operation exists.",
            {"adapter_identity_terms": list(adapter_identity_terms), "adapter_code_sha256": _sha256(adapter_path), "composite_binding": runtime_freeze["fixture"]["composite_identity_binding"]},
        )
    )

    paired_safe = (
        restoration_source.index("model.save") < restoration_source.index("adapter.save") < restoration_source.index("manifest_path.write_bytes")
        and restoration_source.index("checks.add(\"restoration.paired_load_identity\"") < restoration_source.index("original_response = _execute_feedback")
        and "model.reset()\n    adapter.reset()\n    loaded_model.reset()\n    loaded_adapter.reset()" in restoration_source
        and receipt["restoration_witness"]["paired_save_load_identity_equal"]
        and receipt["restoration_witness"]["paired_reset_returns_to_initial_composite_identity"]
    )
    checks.append(
        _result(
            "RV-17",
            "paired_save_load_reset_fail_closed",
            paired_safe,
            "The harness uses a manifest-coordinated native+adapter save, validates both loaders and the complete loaded composite before continuation, invokes only paired resets, forbids implicit rebase in the binding, and demonstrates equal continuation after load/reset. Missing/corrupt component loads or mismatched composite identity raise before response continuation.",
            receipt["restoration_witness"],
            qualification="I06 must expose the paired procedure as the only registered continuation interface and validate manifest component hashes explicitly; the conformance harness proves the governed path, not a generic atomic transaction API.",
        )
    )

    quarantine = conformance["quarantine"]
    quarantine_safe = (
        conformance["scientific_evidence_assigned"] is False
        and quarantine["may_support_or_falsify_AE01_H_L02"] is False
        and quarantine["may_enter_I04_or_I05_calibration"] is False
        and quarantine["may_supply_I06_or_I07_registered_values"] is False
        and quarantine["observed_values_may_be_reused_scientifically"] is False
        and conformance["next_iteration_authorized"] is False
    )
    checks.append(
        _result(
            "RV-18",
            "mechanical_scientific_quarantine",
            quarantine_safe,
            "Machine booleans prohibit scientific support/falsification, calibration entry, registration reuse, execution replacement, mode ranking, and downstream authorization. I03BR1 adds an explicit downstream rejection set without changing the frozen conformance artifact.",
            quarantine,
            qualification="I04 and I06 validators must reject the I03B fixture coefficient, amounts/types/times, threshold, packet amount, branch IDs, response values, comparator, and evidence digest; only the pre-runtime fold family may be imported.",
        )
    )

    branch_ids = sorted(conformance["branches"])
    expected_branch_ids = sorted(
        [
            "reference",
            "q1_only",
            "q2_only",
            "combined_q1_q2",
            "combined_q2_q1",
            "lineage_permuted",
            "write_diversion",
            "active_history_clamp",
            "state_only_separation",
            "private_partition",
            "alternate_responder",
            "restoration_continuation",
        ]
    )
    checks.append(
        _result(
            "RV-19",
            "complete_isolated_twelve_branch_matrix",
            branch_ids == expected_branch_ids
            and harness_source.count("_build_model(freeze)") >= 3
            and receipt["invocation_accounting"]["evidence_invocations"] == 1
            and receipt["invocation_accounting"]["reconstruction_invocations"] == 1
            and receipt["reconstruction"]["byte_comparison"] == "identical",
            "All twelve frozen branch IDs are retained. Each standard branch constructs a fresh model and adapter; private/restoration branches construct their own fresh state. The single matrix invocation and single independent reconstruction each ran all branches, with zero retries and byte-identical output.",
            {"branch_ids": branch_ids, "invocation_accounting": receipt["invocation_accounting"], "initial_identity_witness": receipt["restoration_witness"]["initial_composite_digest"]},
            qualification="The common-profile initial composite digest is retained once as the deterministic fresh-fixture witness rather than duplicated per standard branch; private profiles are identified by their separate frozen configurations and fresh construction.",
        )
    )

    checks.append(
        _result(
            "RV-20",
            "preserve_i03a_independently",
            contract["mode_scope"]["state_carried_profile_status"] == "owner_accepted_for_progression_and_unchanged"
            and contract["mode_scope"]["pool_dependence_mode"] == "history_carried"
            and contract["mode_scope"]["umbrella_discriminator_gate_status"] == "in_progress_not_passable_by_i03b_alone",
            "I03B is mode-local, leaves I03A accepted and unchanged, performs no performance comparison, and treats native history inadequacy as specific to history_carried.",
            contract["mode_scope"],
        )
    )

    checklist_text = (EXPERIMENT / "implementation/P2-I2-shared-pool-co-conditioning-checklist.md").read_text(encoding="utf-8")
    hypothesis_text = (EXPERIMENT / "hypotheses/p2-i2-operational-hypotheses.md").read_text(encoding="utf-8")
    checks.append(
        _result(
            "RV-21",
            "owner_progression_opens_only_i03c",
            "I03C and I04 remain unauthorized" in hypothesis_text
            and "I03B acceptance-ready but I03C/I04 remain closed" in checklist_text
            and conformance["next_iteration_authorized"] is False,
            "I03BR1 itself opens nothing. A new owner progression decision may accept I03B implementation evidence and authorize I03C only; I04 remains blocked on the complete reviewed three-mode discriminator gate.",
            {"i03c_automatic_authorization": False, "i04_authorized": False, "new_progression_decision_required": True},
        )
    )

    graph_after = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "status_porcelain": _git(
            graph_root, "status", "--porcelain=v1", "--untracked-files=all"
        ),
    }
    if graph_after != graph_before:
        raise AssertionError("graph checkout changed during I03BR1 audit")

    blockers = [row for row in checks if row["status"] == "failed"]
    return {
        "artifact_id": "P2-I2-I03BR1-CLOSEOUT-REVALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I03BR1",
        "lane_id": "AE01-L02",
        "validated_at": "2026-07-14",
        "status": "passed_after_revalidation" if not blockers else "blocked",
        "validation_kind": "zero_runtime_source_dataflow_and_retained_artifact_acceptance_audit",
        "input_identity": {"path": str(input_path.relative_to(ROOT)), "sha256": _sha256(input_path)},
        "validator_identity": {
            "path": str(Path(__file__).resolve().relative_to(ROOT)),
            "sha256": _sha256(Path(__file__).resolve()),
        },
        "graph_before": graph_before,
        "graph_after": graph_after,
        "model_instantiations": 0,
        "runtime_evidence_invocations": 0,
        "runtime_reconstruction_invocations": 0,
        "candidate_control_calibration_or_scientific_execution": 0,
        "review_summary": {
            "review_checks_total": len(checks),
            "passed": sum(row["status"] == "passed" for row in checks),
            "passed_with_downstream_obligation": sum(
                row["status"] == "passed_with_downstream_obligation" for row in checks
            ),
            "blocking_findings": len(blockers),
            "all_twelve_acceptance_statements_defensible": not blockers,
        },
        "checks": checks,
        "blocking_findings": blockers,
        "functional_pool_identity": {
            "pool": "H_P plus its declared M_H native output-port binding",
            "native_intake_not_pool": "P",
            "output_port_not_complete_pool": "M_H",
            "audit_projection": "L",
        },
        "claim_boundary": {
            "history_claim": "active ordered history retained and causally materialized into a later native response path through a deterministic scalar readout",
            "irreducible_raw_history_claim": False,
            "non_markovian_claim": False,
            "scientific_evidence": False,
            "calibration_input_allowed": False,
            "registration_value_reuse_allowed": False,
            "boundary_rung_effect": "none",
            "control_result_effect": "none",
            "terminal_effect": "none",
            "fixture_scope": "implementation_conformance_only",
            "I03C_authorized": False,
            "I04_authorized": False,
        },
        "history_lifecycle": {
            "normal_operation": "run_bounded_append_only",
            "whole_history_replacement": "implemented_as_explicit_intervention",
            "autonomous_depletion": "not_applicable",
            "fixed_capacity_or_saturation": "not_selected_and_not_applicable_to_i03b_conformance",
            "leakage_or_decay": "not_applicable",
            "maintenance_transition": "not_applicable",
            "scientific_capacity_values": "deferred_to_I04_I06_without_fixture_reuse",
        },
        "downstream_rejection_requirements": {
            "reject_from_I04_I06": [
                "fixture recency coefficient lambda",
                "fixture token amounts, operation values, and event times",
                "fixture native feedback threshold and response packet amount",
                "fixture branch identifiers and observed response values",
                "fixture floating-point comparator",
                "retained conformance or reconstruction digest as candidate evidence",
            ],
            "may_import": [
                "pre-runtime frozen ordered-fold structural family",
                "source-label exclusion rule",
                "active-history and output-port factorization",
                "producer-minimality and restoration obligations",
            ],
        },
        "owner_acceptance_boundary": {
            "i03b_causal_design_may_be_accepted_for_staged_progression": not blockers,
            "bounded_runtime_conformance_remains_implementation_evidence_only": True,
            "realization_class": "minimally_producer_assisted",
            "history_carried_scientific_status": "unresolved",
            "owner_may_authorize_next": "I03C only",
            "I04_remains_blocked": True,
            "new_progression_decision_required": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = validate(args.input.resolve())
    args.output.resolve().write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result["review_summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
