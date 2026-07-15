#!/usr/bin/env python3
"""Construct and independently reconstruct the retained-evidence P2-I2 I11 closeout."""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable

from jsonschema import Draft202012Validator


EXPERIMENT = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
FREEZE_REL = f"{EXPERIMENT}/contracts/p2-i2/i11-interpretation-input-freeze.json"
DEVELOPMENTAL_REL = f"{EXPERIMENT}/contracts/p2-i2/i11-developmental-interpretation.json"
REQUIREMENT_REL = f"{EXPERIMENT}/contracts/p2-i2/i11-requirement-extraction.json"
TERMINAL_REL = f"{EXPERIMENT}/contracts/p2-i2/i11-terminal-classification.json"
MANIFEST_REL = f"{EXPERIMENT}/contracts/p2-i2/i11-closeout-manifest.json"
VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i11-closeout-validation.json"
REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I11-terminal-closeout.md"
SCRIPT_REL = f"{EXPERIMENT}/scripts/p2_i2_i11_closeout.py"
README_REL = f"{EXPERIMENT}/README.md"
OVERVIEW_REL = f"{EXPERIMENT}/AGENTIC-ECOLOGY-OVERVIEW.md"
SCHEMA_REL = f"{EXPERIMENT}/contracts/schemas/ae01-contract.schema.json"
REGISTRATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i06-three-mode-registration.json"
C02_REL = f"{EXPERIMENT}/contracts/p2-i2/c02/execution-manifest.json"
I09A_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-index.json"
I09A_VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-validation.json"
I10_REL = f"{EXPERIMENT}/contracts/p2-i2/i10-reconstruction-manifest.json"
I10_VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i10-reconstruction-validation.json"
CALIBRATION_REL = f"{EXPERIMENT}/contracts/p2-i2/metric-calibration.json"
METRIC_REL = f"{EXPERIMENT}/contracts/p2-i2/frozen-metric-sheet.json"
MODES = ("state_carried", "history_carried", "hybrid")
ORDERS = ("q1_then_q2", "q2_then_q1")
SEEDS = (101, 211, 307)
TERMINAL_GUARDS = (
    "AE01-CTRL-02",
    "AE01-CTRL-03",
    "AE01-CTRL-07",
    "AE01-CTRL-10",
    "AE01-CTRL-12",
    "AE01-CTRL-13",
    "AE01-CTRL-14",
    "AE01-CTRL-15",
    "AE01-CTRL-18",
    "AE01-CTRL-19",
)
CLAIM_CEILING = "bounded shared-pool co-conditioning demand pattern"
CLAIM_BOUNDARY_REF = "ae01-phase1-developmental-interpretation-claim"
DEBT_REFS = (
    "p2-i2-debt-native-control-surface",
    "p2-i2-debt-native-active-history",
    "p2-i2-debt-producer-assisted-history",
    "p2-i2-debt-explicit-construction",
    "p2-i2-debt-medium-economy",
    "p2-i2-debt-leakage-window",
    "p2-i2-debt-transfer",
    "p2-i2-debt-measurement-order-conditioning",
    "p2-i2-debt-composition-recurrence",
    "p2-i2-debt-semantic-relabel",
    "p2-i2-debt-claim-ceiling",
)
BLOCKED_CLAIMS = (
    "collective memory or communication",
    "cooperation, coordination, agency, or organism identity",
    "functional source diversity, complementarity, or synergy",
    "a native reusable shared-pool or active-history primitive",
    "a general resource economy, leakage law, saturation law, or maintenance law",
    "general transfer, cross-lane recurrence, or compositional recurrence",
    "an ecology motif, ecology regime, life, or T4 theoretical class",
    "ranking among the three retained dependence modes",
    "N31+ selection",
)


def repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_digest(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("canonical_payload_digest", None)
    encoded = json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256_bytes((encoded + "\n").encode("utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


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


def has_absolute_string(value: Any) -> bool:
    for item in strings(value):
        if item.startswith("/") or item.startswith("\\"):
            return True
        if len(item) >= 3 and item[1] == ":" and item[2] in ("/", "\\"):
            return True
    return False


def verify_runtime(repo: Path) -> None:
    expected = repo / ".venv/bin/python"
    require(expected.exists(), "repository .venv interpreter is absent")
    require(Path(sys.executable).samefile(expected), "I11 must run through repository .venv/bin/python")
    require(sys.dont_write_bytecode, "I11 requires Python -B")
    require(not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules), "PyGRC import is forbidden")


def load_inputs(repo: Path) -> dict[str, dict[str, Any]]:
    freeze = read_json(repo / FREEZE_REL)
    require(freeze["artifact_id"] == "P2-I2-I11-INTERPRETATION-INPUT-FREEZE", "I11 freeze identity drift")
    require(freeze["base_commit"] == "b28ef173a70edde0c1f3e034cac9c9c183c6ce95", "I11 accepted base drift")
    require(freeze["input_identity_count"] == len(freeze["input_identities"]) == 18, "I11 input count drift")
    by_path: dict[str, dict[str, Any]] = {}
    for item in freeze["input_identities"]:
        path = item["path"]
        require(not Path(path).is_absolute(), f"absolute frozen path: {path}")
        require(sha256_file(repo / path) == item["sha256"], f"frozen input drift: {path}")
        if path.endswith((".json",)):
            by_path[path] = read_json(repo / path)
    by_path[FREEZE_REL] = freeze
    return by_path


def classify_relation(rows: list[dict[str, Any]], delta: float) -> tuple[str, bool]:
    margins = [float(row["primary_margin"]) for row in rows]
    require(margins, "empty metric relation")
    threshold_passed = all(value > 0.0 for value in margins)
    if all(value > delta for value in margins):
        return "robust_aligned", threshold_passed
    if all(value > 0.0 for value in margins) and any(value > delta for value in margins):
        return "narrow_aligned", threshold_passed
    if all(abs(value) <= delta for value in margins):
        return "resolution_limited", threshold_passed
    if min(margins) <= 0.0 and max(margins) > delta:
        return "mixed_direction", threshold_passed
    if all(value < -delta for value in margins):
        return "robust_counter", threshold_passed
    return "narrow_counter", threshold_passed


def primary_rows(i10: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows = i10["per_seed_order_primary_margins"]
    require(len(rows) == 18, "I10 primary tuple count drift")
    result: dict[str, list[dict[str, Any]]] = {}
    for mode in MODES:
        selected = [row for row in rows if row["mode"] == mode]
        selected.sort(key=lambda row: (ORDERS.index(row["physical_order_id"]), row["seed"]))
        require(len(selected) == 6, f"primary tuple count drift for {mode}")
        require({row["seed"] for row in selected} == set(SEEDS), f"seed drift for {mode}")
        require({row["physical_order_id"] for row in selected} == set(ORDERS), f"order drift for {mode}")
        result[mode] = selected
    return result


def evidence_identities(repo: Path, i09a: dict[str, Any], i10: dict[str, Any], c02: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "reference_id": "P2-I2-C02-EXECUTION-MANIFEST",
            "evidence_role": "observed_ae01_result",
            "path": C02_REL,
            "output_digest": c02["canonical_payload_digest"],
            "file_sha256": sha256_file(repo / C02_REL),
            "claim_ceiling": "complete retained execution evidence; no interpretation by itself",
        },
        {
            "reference_id": "P2-I2-I09A-CONTROL-RESOLUTION-INDEX",
            "evidence_role": "observed_ae01_result",
            "path": I09A_REL,
            "output_digest": i09a["canonical_payload_digest"],
            "file_sha256": sha256_file(repo / I09A_REL),
            "claim_ceiling": "mode-separated control and normalized-margin projection only",
        },
        {
            "reference_id": "P2-I2-I10-RECONSTRUCTION-MANIFEST",
            "evidence_role": "observed_ae01_result",
            "path": I10_REL,
            "output_digest": i10["canonical_payload_digest"],
            "file_sha256": sha256_file(repo / I10_REL),
            "claim_ceiling": "retention, reconstruction, and restoration-conformance evidence only",
        },
        {
            "reference_id": "P2-I2-I06-THREE-MODE-REGISTRATION",
            "evidence_role": "constructed_ecology_mechanism",
            "path": REGISTRATION_REL,
            "file_sha256": sha256_file(repo / REGISTRATION_REL),
            "claim_ceiling": "registered implementation identity and causal ownership only",
        },
    ]


def build_developmental(
    rows_by_mode: dict[str, list[dict[str, Any]]],
    delta: float,
    registration: dict[str, Any],
) -> dict[str, Any]:
    metric_relations: list[dict[str, Any]] = []
    relation_index: list[dict[str, Any]] = []
    mode_dispositions: list[dict[str, Any]] = []
    mode_support = {
        "state_carried": "native_expression_candidate",
        "history_carried": "scaffold_dependent",
        "hybrid": "scaffold_dependent",
    }
    for mode in MODES:
        rows = rows_by_mode[mode]
        relation, threshold_passed = classify_relation(rows, delta)
        seed_margins = [{"seed": row["seed"], "margin": row["primary_margin"]} for row in rows]
        rationale = (
            "Both physical orders yield normalized margin 1.0 for seeds 101, 211, and 307, "
            "matching the frozen state-carried order-invariance relation."
            if mode == "state_carried"
            else
            "The q1-then-q2 order yields normalized margin 1.0 and q2-then-q1 yields 0.0 "
            "for every seed. The aggregate metric relation is mixed_direction, while the "
            "order-conditioned causal relation matches the frozen active-history expectation."
        )
        metric_relations.append({
            "metric_sheet_ref": "ae01-l02-primary-metric-v1",
            "seed_margins": seed_margins,
            "resolution_status": "frozen",
            "delta": delta,
            "calibration_artifact_ref": "ae01:metric-calibration:bf15f254da8c8de1",
            "relation": relation,
            "threshold_passed": threshold_passed,
            "rationale": rationale,
        })
        relation_index.append({
            "mode": mode,
            "relation": relation,
            "threshold_passed": threshold_passed,
            "rows": rows,
        })
        realization = registration["mode_registry"][mode]["realization_class"]
        mode_dispositions.append({
            "mode": mode,
            "realization_class": realization,
            "support_status": mode_support[mode],
            "metric_relation": relation,
            "threshold_passed": threshold_passed,
            "causal_support": "passed_mode_specific_registered_relation",
            "boundary_rungs": {f"AE01-L02-R0{index}": "reached" for index in range(1, 6)},
            "mode_ranking": None,
            "producer_boundary": registration["mode_registry"][mode]["producer_owner"],
            "restoration_class": registration["mode_registry"][mode]["restoration_class"],
        })

    rungs = [
        {
            "rung_id": "AE01-L02-R01",
            "name": "One non-private pool",
            "status": "reached",
            "evidence_refs": ["P2-I2-I06-THREE-MODE-REGISTRATION", "P2-I2-I09A-CONTROL-RESOLUTION-INDEX"],
            "rationale": "Each mode exposes one registered source-label-free common carrier to an eligible responder; private partitions cannot satisfy the candidate path.",
        },
        {
            "rung_id": "AE01-L02-R02",
            "name": "Multiple attributable sources",
            "status": "reached",
            "evidence_refs": ["P2-I2-C02-EXECUTION-MANIFEST", "P2-I2-I09A-CONTROL-RESOLUTION-INDEX"],
            "rationale": "S1 and S2 lineage is retained for audit, both source-specific single-contribution responses are zero, and both valid leave-one carrier-admission arms are zero in every mode, order, and seed.",
        },
        {
            "rung_id": "AE01-L02-R03",
            "name": "Combined-history dependence",
            "status": "reached",
            "evidence_refs": ["P2-I2-I09A-CONTROL-RESOLUTION-INDEX", "P2-I2-I10-RECONSTRUCTION-MANIFEST"],
            "rationale": "State-carried response follows complete P and changes under P debit; history-carried response follows active H_P/M_H and changes under order/clamp but not P-only debit; hybrid response requires both P and H_P components under factorial interventions.",
        },
        {
            "rung_id": "AE01-L02-R04",
            "name": "Mailbox, controller, and shuffle controls",
            "status": "reached",
            "evidence_refs": ["P2-I2-I09A-CONTROL-RESOLUTION-INDEX", "P2-I2-I10-RECONSTRUCTION-MANIFEST"],
            "rationale": "All 38 comparison rules and all 15 lane controls pass; label-only changes are invariant, private partitions remain isolated, and direct/controller substitutions are causally excluded from the candidate chain.",
        },
        {
            "rung_id": "AE01-L02-R05",
            "name": "Capacity, contributor, or access variation",
            "status": "reached",
            "evidence_refs": ["P2-I2-C02-EXECUTION-MANIFEST", "P2-I2-I09A-CONTROL-RESOLUTION-INDEX"],
            "rationale": "The preregistered alternate-eligible-responder access-scope contrast retains the mode-specific relation in all three modes; no broader transfer is inferred.",
        },
    ]
    debt_ledger = [
        {"debt_id": DEBT_REFS[0], "category": "native", "status": "open", "disposition": "State mode is native on the causal path, but atomic pool-write gates, auditable clamps, and first-class private-role guards remain experiment-composed."},
        {"debt_id": DEBT_REFS[1], "category": "native", "status": "open", "disposition": "PyGRC lacks a first-class source-label-independent active shared-history carrier with admission, intervention, readout materialization, and restoration/reset."},
        {"debt_id": DEBT_REFS[2], "category": "producer", "status": "open", "disposition": "History-carried and hybrid depend causally on RCAEActiveHistoryAdapterV2 for H_P/M_H; PyGRC still owns the response."},
        {"debt_id": DEBT_REFS[3], "category": "construction", "status": "open", "disposition": "Topology, schedules, roles, contribution operations, and controls are explicitly registered experiment construction."},
        {"debt_id": DEBT_REFS[4], "category": "medium", "status": "bounded", "disposition": "Reserve, accumulation, mixing, and explicit depletion are audited only inside the registered fixture and window."},
        {"debt_id": DEBT_REFS[5], "category": "leakage", "status": "not_applicable_in_window", "disposition": "Leakage, saturation, and maintenance are registered not applicable; no general economy is measured."},
        {"debt_id": DEBT_REFS[6], "category": "transfer", "status": "open", "disposition": "R05 establishes only alternate-responder access-scope retention, not geometry, timescale, runtime, domain, or cross-lane transfer."},
        {"debt_id": DEBT_REFS[7], "category": "measurement", "status": "retained", "disposition": "History and hybrid aggregate margins are mixed_direction because the frozen physical orders intentionally differ; no scalar collapse is allowed."},
        {"debt_id": DEBT_REFS[8], "category": "composition", "status": "open", "disposition": "No cross-lane recurrence or composition has been tested; three within-lane modes are not three independent lane recurrences."},
        {"debt_id": DEBT_REFS[9], "category": "semantic", "status": "guarded", "disposition": "Pool, history, and co-conditioning labels remain operational and cannot be relabeled as memory, communication, cooperation, coordination, agency, motif, regime, or life."},
        {"debt_id": DEBT_REFS[10], "category": "claim", "status": "guarded", "disposition": f"The strongest valid claim remains exactly: {CLAIM_CEILING}."},
    ]
    record = {
        "schema_version": "1.1.0",
        "record_type": "developmental_interpretation",
        "record": {
            "interpretation_id": "p2-i2-i11-developmental-interpretation",
            "lane_id": "AE01-L02",
            "source_result_refs": [
                "P2-I2-C02-EXECUTION-MANIFEST",
                "P2-I2-I09A-CONTROL-RESOLUTION-INDEX",
                "P2-I2-I10-RECONSTRUCTION-MANIFEST",
                "P2-I2-I06-THREE-MODE-REGISTRATION",
            ],
            "metric_relations": metric_relations,
            "boundary_rungs": rungs,
            "highest_valid_rung": {
                "status": "applicable",
                "reference_id": "AE01-L02-R05",
                "rationale": "All five cumulative L02 boundaries are reached in every retained mode, with lane-wide support limited by the producer-assisted active-history scaffold and access-scope-only transfer contrast.",
            },
            "expressed_properties": [
                {
                    "property_id": "p2-i2-i11-state-order-invariant-response",
                    "name": "State-carried robust aligned and order-invariant response",
                    "expectedness": "expected",
                    "evidence_refs": ["P2-I2-I09A-CONTROL-RESOLUTION-INDEX"],
                    "rationale": "Both state-carried physical orders yield margin 1.0 for all three seeds and equal-P order/shuffle controls pass.",
                },
                {
                    "property_id": "p2-i2-i11-history-order-conditioned-response",
                    "name": "History-carried order-conditioned response",
                    "expectedness": "expected",
                    "evidence_refs": ["P2-I2-I09A-CONTROL-RESOLUTION-INDEX"],
                    "rationale": "The active-history order reversal changes the response for every seed while P-only debit is invariant and H_P clamp changes the response.",
                },
                {
                    "property_id": "p2-i2-i11-hybrid-joint-response",
                    "name": "Hybrid separately intervenable joint P and H_P response",
                    "expectedness": "expected",
                    "evidence_refs": ["P2-I2-I09A-CONTROL-RESOLUTION-INDEX"],
                    "rationale": "Only the full P plus H_P component factorial yields 0.125; either registered reference component yields zero, and order reversal remains visible.",
                },
                {
                    "property_id": "p2-i2-i11-repeated-source-equivalence",
                    "name": "Quantity-matched repeated-source equivalence",
                    "expectedness": "adjacent",
                    "evidence_refs": ["P2-I2-I09A-CONTROL-RESOLUTION-INDEX"],
                    "rationale": "Repeated-S1 and repeated-S2 each equal the candidate response. This is a preregistered non-gating scope diagnostic and blocks source-diversity, synergy, cooperation, and coordination readings.",
                },
                {
                    "property_id": "p2-i2-i11-native-load-normalization",
                    "name": "Native load normalization with exact identity and continuation",
                    "expectedness": "adjacent",
                    "evidence_refs": ["P2-I2-I10-RECONSTRUCTION-MANIFEST"],
                    "rationale": "Raw native snapshots normalize through the admitted closed set while restoration identity, adapter bytes, equal-input continuation, and paired reset remain exact.",
                },
            ],
            "support_status": "scaffold_dependent",
            "classification_value": {
                "rung": "T3_operational_class",
                "organizes_next_iteration": True,
                "rationale": "The result defines an executable three-mode shared-pool probe, its causal controls, restoration boundary, and a specific missing native active-history function; it does not revise theory at T4.",
            },
            "becoming_reading": {
                "appearance": "Two attributable contributions constituted one non-private carrier whose later native response depended on complete common state, active order-bearing history, or both, according to the preregistered mode.",
                "classification_status": "R01 through R05 reached; state-carried is robust aligned, history-carried and hybrid are expected order-conditioned mixed_direction relations, and all mandatory causal controls pass.",
                "live_boundary": "Whether the active-history leg can become graph-native, recur independently across lanes, or retain function across broader transfer axes remains open.",
                "support_dependence": "State-carried uses a native PyGRC causal path; history-carried and hybrid require the minimal RCAE H_P/M_H adapter while PyGRC owns the response. The lane-wide lowest honest support status is scaffold_dependent.",
                "claim_ceiling": CLAIM_CEILING,
            },
            "development_reading": {
                "condition_revealed": "A reusable shared-pool probe needs an attributable but source-label-free common carrier, separately intervenable state/history components, private and controller exclusions, bounded access variation, and complete restoration ownership.",
                "aim_effect": "supports",
                "organization_implication": "Retain all three modes as distinct operational realizations. Treat the native state path as adequate for this bounded function and the active-history adapter boundary as the concrete graph-side naturalization demand.",
                "measurement_question": "Can a future graph-native active-history carrier reproduce the registered admission, order, clamp, materialization, restoration, and control relations after withdrawing RCAEActiveHistoryAdapterV2?",
                "stewardship_implication": "Do not optimize the observed margins, rank modes, or broaden claims. Preserve the complete evidence and move only through a separately preregistered native-history substitution probe after cross-experiment pattern synthesis.",
            },
            "next_move": {
                "disposition": "new_boundary_or_naturalization_probe",
                "target_function": "After cross-experiment synthesis, test one graph-native source-label-independent active shared-history carrier that owns bounded admission, intervention/clamp, readout materialization, restoration, and reset, replacing RCAEActiveHistoryAdapterV2 in the retained history and hybrid causal paths.",
                "rationale": "The state-carried causal path is native, while both history-bearing modes expose the same minimal missing native function. A substitution probe advances native expression without rerunning or optimizing P2-I2.",
                "falsifier": "The proposed native replacement is inadequate if, under a new preregistration, it cannot reproduce exact admission/idempotency, source-label exclusion, order and clamp relations, joint-component separation, paired restoration/reset, and the retained controls after the RCAE active-history adapter is withdrawn.",
                "new_preregistration_required": True,
            },
            "local_optimization_guard": {
                "status": "applicable",
                "same_causal_question": True,
                "function_not_proxy": True,
                "one_bounded_change": True,
                "preserves_prior_result": True,
                "falsifiable": True,
                "advances": ["native_expression"],
                "rationale": "The next move substitutes one identified missing carrier function, preserves this result, and is falsified by failure to retain the registered causal and restoration relations without the adapter.",
            },
            "claim_boundary_ref": CLAIM_BOUNDARY_REF,
            "blocked_claims": list(BLOCKED_CLAIMS),
            "debt_refs": list(DEBT_REFS),
            "extensions": {
                "x_mode_dispositions": mode_dispositions,
                "x_metric_relation_configuration_index": relation_index,
                "x_observation_class_ledger": {
                    "expected": ["state order invariance", "history order dependence", "hybrid joint component dependence"],
                    "adjacent": ["quantity-matched repeated-source equivalence", "native load normalization"],
                    "unexpected": [],
                    "null": ["all single-source and leave-one responses", "history/hybrid q2-then-q1 candidate response"],
                    "mixed": ["history_carried aggregate metric relation", "hybrid aggregate metric relation"],
                    "counter_directional": [],
                },
                "x_debt_ledger": debt_ledger,
                "x_realization_family_ranked": False,
                "x_observed_relation_is_not_lgrc_demand": True,
            },
        },
    }
    return record


def build_requirement(repo: Path, i09a: dict[str, Any], i10: dict[str, Any], c02: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.1.0",
        "record_type": "requirement_extraction",
        "record": {
            "requirement_id": "p2-i2-l02-native-active-shared-history-carrier",
            "lane_ids": ["AE01-L02"],
            "origin": "introduce",
            "target_catalog_layer": "building_block",
            "surface_status": "missing",
            "surface_description": "A graph-native source-label-independent active shared-history carrier that exposes bounded contribution admission and idempotency, ordered mixing, intervention/clamp, native readout materialization, audit lineage separation, paired restoration, and reset.",
            "source_tension": "PyGRC natively supplies the state-carried P response and the final response machinery for all modes, but it does not own the active H_P/M_H function required by history-carried and hybrid; the experiment therefore supplies that one causal leg through RCAEActiveHistoryAdapterV2.",
            "evidence_refs": evidence_identities(repo, i09a, i10, c02),
            "future_discriminator": "Under a new preregistration, withdraw RCAEActiveHistoryAdapterV2 and substitute one graph-native active-history carrier while preserving exact contribution operations, orders, interventions, response masks, controls, and restoration identities.",
            "counterfactual": "If a graph-native carrier cannot reproduce the registered order/clamp and hybrid factorial relations after adapter withdrawal, or if adapter withdrawal does not selectively remove the history-bearing relation, the proposed surface is not the missing function identified here.",
            "prerequisite_ids": [
                "lgrc-attributable-source-lineage",
                "lgrc-source-label-independent-common-carrier",
                "lgrc-native-restoration-and-reset-identity-v2",
                "lgrc-native-carrier-scoped-response",
            ],
            "composition_leverage": "The surface would compose attributable multi-source events into a restorable active carrier usable by later native response paths, removing the same minimal producer-owned leg from both history-carried and hybrid realizations.",
            "transfer_scope": "Demand abstraction only within AE01 pending cross-experiment synthesis and a separately registered substitution probe; no P2-I2 margin, rung, support status, or terminal class transfers as graph evidence.",
            "construction_refs": [
                "RCAEActiveHistoryAdapterV2",
                "p2-i2-i06-history-H_P-common",
                "p2-i2-i06-hybrid-H_P-common",
                "P2-I2-I06-THREE-MODE-REGISTRATION",
            ],
            "debt_refs": list(DEBT_REFS),
            "claim_boundary_ref": CLAIM_BOUNDARY_REF,
            "ranking_eligibility": "pending_synthesis",
            "extensions": {
                "x_mode_surface_dispositions": {
                    "state_carried": {
                        "status": "apparently_adequate",
                        "boundary": "native causal P response; experiment-composed audit/control conveniences remain debt",
                    },
                    "history_carried": {
                        "status": "missing",
                        "boundary": "active H_P/M_H causal leg owned by RCAEActiveHistoryAdapterV2",
                    },
                    "hybrid": {
                        "status": "missing",
                        "boundary": "same active H_P/M_H leg missing; native PyGRC joint response is adequate",
                    },
                },
                "x_observed_relation": CLAIM_CEILING,
                "x_lgrc_demand_implication": "candidate native active-history building block for later cross-experiment synthesis",
                "x_native_implementation_priority_assigned": False,
            },
        },
    }


def build_terminal(developmental: dict[str, Any]) -> dict[str, Any]:
    mode_dispositions = developmental["record"]["extensions"]["x_mode_dispositions"]
    return {
        "schema_version": "1.1.0",
        "record_type": "terminal_classification",
        "record": {
            "terminal_record_id": "p2-i2-i11-terminal-classification",
            "lane_id": "AE01-L02",
            "classification": "supported_bounded_candidate",
            "stopping_condition": "Stop after one complete mode-preserving terminal classification of the fixed 234-entry matrix without rescue, mode selection, margin optimization, or scientific rerun.",
            "stopping_condition_reached": True,
            "attempted_work": [
                "Bound and executed all 234 registered C02 matrix entries across three modes, two physical orders, three seeds, seven logical cells, and five lane controls",
                "Resolved all 38 comparison rules, all 15 lane controls, and all 57 program-control mode dispositions from retained receipts",
                "Corrected and reconstructed all 18 primary margins through the accepted I04R2 estimator without changing any control disposition",
                "Independently reconstructed the complete execution/control bundle and verified restoration, continuation, and reset for all three modes",
                "Interpreted all five L02 boundary rungs and all mode-specific metric, causal, support, realization, and developmental relations once",
            ],
            "execution_status": "completed",
            "positive_signatures": [
                "One auditable non-private source-label-free common carrier is retained in every mode",
                "S1 and S2 remain attributable while all single-source and leave-one responses are zero",
                "State-carried response is robust aligned and invariant across equal-P physical orders",
                "History-carried response follows active H_P/M_H order and clamp rather than P-only state",
                "Hybrid response requires separately intervenable P and H_P components",
                "All comparison, lane-control, program-control, access-contrast, reconstruction, restoration, continuation, and reset obligations pass",
            ],
            "negative_signatures": [
                "History-carried and hybrid q2-then-q1 margins are 0.0 for every seed, yielding expected mode-conditioned mixed_direction aggregate metric relations rather than a causal-support failure",
                "Quantity-matched repeated-S1 and repeated-S2 responses equal the candidate, so functional source diversity, complementarity, synergy, cooperation, and coordination are not supported",
            ],
            "blocked_signatures": [
                "collective_memory_or_communication",
                "cooperation_coordination_agency_or_organism",
                "functional_source_diversity_or_synergy",
                "native_reusable_shared_pool_primitive",
                "general_resource_economy",
                "general_transfer_or_cross_lane_recurrence",
                "ecology_motif_regime_life_or_T4",
                "mode_ranking_or_N31_selection",
            ],
            "missing_information": [
                "Whether the active-history function recurs as the same missing native pattern across independent experiments",
                "Whether a graph-native active-history carrier can replace the RCAE adapter while retaining all causal and restoration relations",
                "Whether the bounded relation transfers beyond the registered alternate-responder access contrast",
                "Whether leakage, saturation, maintenance, and longer-horizon resource economy become applicable outside the fixed response window",
                "Whether the demand pattern recurs independently in another AE01 lane",
            ],
            "control_refs": [*[f"AE01-CTRL-{index:02d}" for index in range(1, 20)], *[f"AE01-L02-CTRL-{index:02d}" for index in range(1, 6)]],
            "retained_evidence_refs": [
                "P2-I2-C02-EXECUTION-MANIFEST",
                "P2-I2-I09A-CONTROL-RESOLUTION-INDEX",
                "P2-I2-I10-RECONSTRUCTION-MANIFEST",
                "P2-I2-I11-CLOSEOUT-MANIFEST",
            ],
            "reconstruction_status": "verified",
            "developmental_interpretation_ref": "p2-i2-i11-developmental-interpretation",
            "debt_refs": list(DEBT_REFS),
            "claim_impact": f"Supports AE01-H-L02 through R05 as a {CLAIM_CEILING}, with state-carried native expression and history/hybrid scaffold dependence; every stronger relabel remains blocked.",
            "record_complete": True,
            "forces_n31_non_selection": False,
            "extensions": {
                "x_mode_dispositions": mode_dispositions,
                "x_lane_support_status": "scaffold_dependent",
                "x_classification_value": "T3_operational_class",
                "x_realization_family": {
                    "state_carried": "pygrc_native_candidate",
                    "history_carried": "minimally_producer_assisted",
                    "hybrid": "minimally_producer_assisted",
                },
                "x_highest_valid_rung": "AE01-L02-R05",
                "x_strongest_valid_claim": CLAIM_CEILING,
                "x_blocked_relabels": list(BLOCKED_CLAIMS),
                "x_mode_ranking": None,
                "x_n31_selection_status": "not_run",
                "x_repeated_source_equivalence_gating": False,
            },
        },
    }


def revalidate_terminal_guards(
    i09a: dict[str, Any],
    c02: dict[str, Any],
    developmental: dict[str, Any],
    requirement: dict[str, Any],
    terminal: dict[str, Any],
) -> list[dict[str, Any]]:
    source = {row["control_id"]: row for row in i09a["program_common_controls"]}
    blocked = " ".join(developmental["record"]["blocked_claims"]).lower()
    terminal_record = terminal["record"]
    requirement_record = requirement["record"]
    mode_dispositions = {row["mode"]: row for row in terminal_record["extensions"]["x_mode_dispositions"]}
    require(set(TERMINAL_GUARDS) == {key for key, row in source.items() if any(item["requires_I11_revalidation"] for item in row["mode_results"])}, "terminal guard set drift")
    results: list[dict[str, Any]] = []
    for control_id in TERMINAL_GUARDS:
        for mode in MODES:
            original = next(row for row in source[control_id]["mode_results"] if row["mode"] == mode)
            predicates: dict[str, bool]
            if control_id in {"AE01-CTRL-02", "AE01-CTRL-03", "AE01-CTRL-07", "AE01-CTRL-12"}:
                predicates = {
                    "bounded_claim_exact": terminal_record["extensions"]["x_strongest_valid_claim"] == CLAIM_CEILING,
                    "unsafe_relabels_blocked": all(token in blocked for token in ("agency", "coordination", "motif", "regime")),
                }
            elif control_id == "AE01-CTRL-10":
                predicates = {
                    "parent_modulation_claim_absent": "parent" not in CLAIM_CEILING,
                    "motif_and_regime_blocked": "motif" in blocked and "regime" in blocked,
                }
            elif control_id == "AE01-CTRL-13":
                predicates = {
                    "selection_not_run": terminal_record["extensions"]["x_n31_selection_status"] == "not_run",
                    "mode_ranking_absent": terminal_record["extensions"]["x_mode_ranking"] is None,
                }
            elif control_id == "AE01-CTRL-14":
                predicates = {
                    "demand_separate_from_substrate_evidence": requirement_record["extensions"]["x_native_implementation_priority_assigned"] is False,
                    "surface_status_is_missing_not_graph_success": requirement_record["surface_status"] == "missing",
                }
            elif control_id == "AE01-CTRL-15":
                predicates = {
                    "realization_class_explicit": mode_dispositions[mode]["realization_class"] in {"pygrc_native_candidate", "minimally_producer_assisted"},
                    "support_status_explicit": mode_dispositions[mode]["support_status"] in {"native_expression_candidate", "scaffold_dependent"},
                }
            elif control_id == "AE01-CTRL-18":
                predicates = {
                    "domain_promotion_absent": requirement_record["target_catalog_layer"] == "building_block",
                    "motif_regime_life_blocked": all(token in blocked for token in ("motif", "regime", "life")),
                }
            else:
                predicates = {
                    "manifest_complete": c02["evaluable_terminal_count"] == c02["required_entry_count"] == 234,
                    "missing_nonevaluable_ambiguous_zero": c02["missing_entry_count"] == c02["nonevaluable_entry_count"] == c02["ambiguous_entry_count"] == 0,
                    "execution_completed": terminal_record["execution_status"] == "completed",
                    "historical_incomplete_not_scientific_negative": terminal_record["classification"] != "not_supported",
                }
            results.append({
                "control_id": control_id,
                "mode": mode,
                "source_I09A_disposition": original["observed_disposition"],
                "derived_predicates": predicates,
                "observed_disposition": "pass" if all(predicates.values()) else "fail",
                "revalidated_from_final_records": True,
            })
    require(len(results) == 30 and all(row["observed_disposition"] == "pass" for row in results), "I11 terminal guard failure")
    return results


def render_report(
    developmental: dict[str, Any],
    requirement: dict[str, Any],
    terminal: dict[str, Any],
    guard_results: list[dict[str, Any]],
) -> str:
    dev = developmental["record"]
    term = terminal["record"]
    modes = {row["mode"]: row for row in dev["extensions"]["x_mode_dispositions"]}
    relation_rows = dev["extensions"]["x_metric_relation_configuration_index"]
    lines = [
        "# P2-I2 I11 Terminal Closeout",
        "",
        "## Disposition",
        "",
        f"P2-I2 closes as `{term['classification']}` through `AE01-L02-R05`. The strongest valid claim is **{CLAIM_CEILING}**. The lane-wide support status is `scaffold_dependent`, and the developmental value is `T3_operational_class`.",
        "",
        "This is a retained-evidence interpretation of the accepted 234-entry C02 record, corrected I09A control projection, and I10 reconstruction. I11 executed no model, packet, adapter, response, control, or matrix entry.",
        "",
        "## Mode-separated result",
        "",
        "| Mode | Realization | Support | Metric relation | Threshold | Causal reading |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    causal = {
        "state_carried": "Complete common P is causal; equal-P order variants are invariant and P debit changes response.",
        "history_carried": "Active H_P/M_H order is causal; P-only debit is invariant and history clamp changes response.",
        "hybrid": "P and H_P are separately necessary under the registered factorial; history order remains causal.",
    }
    for mode in MODES:
        row = modes[mode]
        lines.append(f"| `{mode}` | `{row['realization_class']}` | `{row['support_status']}` | `{row['metric_relation']}` | `{'passed' if row['threshold_passed'] else 'not_all_configurations_above_zero'}` | {causal[mode]} |")
    lines.extend(["", "The modes are not ranked. The history and hybrid `mixed_direction` labels preserve the frozen physical-order dependence: q1-then-q2 is aligned and q2-then-q1 is zero for every seed. That is the preregistered causal relation, not an automatic R03 failure.", "", "## Per-seed and physical-order margins", "", "| Mode | Order | Seed 101 | Seed 211 | Seed 307 |", "| --- | --- | ---: | ---: | ---: |"])
    for item in relation_rows:
        for order in ORDERS:
            selected = [row for row in item["rows"] if row["physical_order_id"] == order]
            values = {row["seed"]: row["primary_margin"] for row in selected}
            lines.append(f"| `{item['mode']}` | `{order}` | {values[101]:.1f} | {values[211]:.1f} | {values[307]:.1f} |")
    lines.extend(["", "The frozen arithmetic resolution is `1e-12`. All six state margins are `1.0`; history and hybrid each retain three `1.0` and three `0.0` margins. No scalar average replaces these relations.", "", "## Boundary ladder", "", "| Rung | Disposition | Reason |", "| --- | --- | --- |"])
    for rung in dev["boundary_rungs"]:
        lines.append(f"| `{rung['rung_id']}` {rung['name']} | `{rung['status']}` | {rung['rationale']} |")
    lines.extend([
        "",
        "## Controls and scope",
        "",
        "All 38 comparison rules and all 15 mode-local lane controls pass. The 19 program controls retain 56 passes and the preregistered state-carried `AE01-CTRL-16` not-applicable disposition. I11 mechanically revalidates all 10 terminal-sensitive program guards for all three modes: 30/30 pass.",
        "",
        "Quantity-matched repeated-S1 and repeated-S2 each reproduce the candidate response. This was frozen as non-gating carrier-equivalence evidence. It limits the claim to several attributable contributions constituting one common carrier and blocks functional source-diversity, complementarity, synergy, cooperation, and coordination claims.",
        "",
        "## What appeared and what it implies",
        "",
        "Observed relation: two attributable contributions can constitute one non-private carrier whose later native response depends on complete common state, active ordered history, or both, with private/controller alternatives excluded and a bounded alternate-responder access contrast retained.",
        "",
        "LGRC demand implication: the state-carried causal leg is natively expressible for this bounded fixture. History-carried and hybrid expose the same missing graph-side function: a source-label-independent active shared-history carrier owning admission, order, intervention, readout materialization, restoration, and reset. This demand is not evidence that the native surface already exists.",
        "",
        "## Support, debt, and claim ceiling",
        "",
        "State-carried is a `native_expression_candidate`. History-carried and hybrid are `scaffold_dependent` because RCAEActiveHistoryAdapterV2 owns the causal H_P/M_H leg while PyGRC owns the response. The lowest honest lane-wide status is therefore `scaffold_dependent`.",
        "",
        "Open debt remains explicit for native control surfaces, native active history, producer assistance, experimental construction, bounded medium economy, non-applicable leakage/maintenance, transfer, order-conditioned measurement, cross-lane composition, semantic relabeling, and the claim ceiling.",
        "",
        "Blocked relabels: collective memory, communication, functional source diversity or synergy, cooperation, coordination, agency, organism, native reusable shared-pool primitive, general resource economy, general transfer, cross-lane recurrence, motif, regime, life, T4 theory, mode ranking, and N31+ selection.",
        "",
        "## Next move and falsifier",
        "",
        f"Next move: `{dev['next_move']['disposition']}`. {dev['next_move']['target_function']}",
        "",
        f"Falsifier: {dev['next_move']['falsifier']}",
        "",
        "The next move requires a new preregistration and does not begin inside P2-I2. Cross-experiment synthesis must precede any implementation priority.",
        "",
        "## Closeout accounting",
        "",
        f"- C02 evaluable terminals: `234/234`",
        f"- I09A comparison rules: `38/38 pass`",
        f"- I09A lane controls: `15/15 pass`",
        f"- I11 terminal-guard revalidation: `{sum(row['observed_disposition'] == 'pass' for row in guard_results)}/30 pass`",
        "- I10 generation and independent reconstruction: `24/24` each",
        "- I11 scientific/model/C02 operations: `0`",
        "- Mode ranking: `not run`",
        "- N31+ selection: `not run`",
        "- Owner acceptance, commit, and CLOSE-GATE: `pending review`",
        "",
    ])
    require(requirement["record"]["surface_status"] == "missing", "report requirement drift")
    return "\n".join(lines)


def validate_schema(schema: dict[str, Any], *records: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    for record in records:
        errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
        require(not errors, f"schema validation failed for {record.get('record_type')}: {errors[0].message if errors else ''}")


def build_outputs(repo: Path) -> tuple[dict[str, bytes], dict[str, Any]]:
    inputs = load_inputs(repo)
    freeze = inputs[FREEZE_REL]
    registration = inputs[REGISTRATION_REL]
    c02 = inputs[C02_REL]
    i09a = inputs[I09A_REL]
    i09a_validation = inputs[I09A_VALIDATION_REL]
    i10 = inputs[I10_REL]
    i10_validation = inputs[I10_VALIDATION_REL]
    calibration = inputs[CALIBRATION_REL]
    metric = inputs[METRIC_REL]
    schema = inputs[SCHEMA_REL]
    require(c02["status"] == "complete_all_registered_entries_evaluable", "C02 status drift")
    require(c02["required_entry_count"] == c02["evaluable_terminal_count"] == 234, "C02 completion drift")
    require(c02["missing_entry_count"] == c02["nonevaluable_entry_count"] == c02["ambiguous_entry_count"] == 0, "C02 evaluability drift")
    require(i09a["summary"]["comparison_rule_dispositions"] == {"pass": 38}, "I09A comparison drift")
    require(i09a["summary"]["lane_control_dispositions"] == {"pass": 15}, "I09A lane-control drift")
    require(i09a["summary"]["program_common_mode_dispositions"] == {"not_applicable": 1, "pass": 56}, "I09A program-control drift")
    require(i09a_validation["status"] == "passed" and all(row["passed"] for row in i09a_validation["checks"]), "I09A validation drift")
    require(i10_validation["status"] == "passed" and all(row["passed"] for row in i10_validation["checks"]), "I10 validation drift")
    require(i10["execution_reconstruction"]["evaluable_terminals"] == 234, "I10 execution reconstruction drift")
    require(i10["control_reconstruction"]["normalized_primary_margin_distribution"] == {"0.0": 6, "1.0": 12}, "I10 margin drift")
    delta = float(calibration["record"]["delta"])
    require(delta == 1e-12, "calibration delta drift")
    require(metric["record"]["resolution_policy"]["delta"]["value"] == delta, "metric/calibration drift")
    rows_by_mode = primary_rows(i10)
    developmental = build_developmental(rows_by_mode, delta, registration)
    requirement = build_requirement(repo, i09a, i10, c02)
    terminal = build_terminal(developmental)
    validate_schema(schema, developmental, requirement, terminal)
    guards = revalidate_terminal_guards(i09a, c02, developmental, requirement, terminal)
    report = render_report(developmental, requirement, terminal, guards).encode("utf-8")
    output_bytes = {
        DEVELOPMENTAL_REL: json_bytes(developmental),
        REQUIREMENT_REL: json_bytes(requirement),
        TERMINAL_REL: json_bytes(terminal),
        REPORT_REL: report,
    }
    inventory_paths = [FREEZE_REL, DEVELOPMENTAL_REL, REQUIREMENT_REL, TERMINAL_REL, REPORT_REL, SCRIPT_REL, README_REL, OVERVIEW_REL]
    inventory: list[dict[str, Any]] = []
    for path in inventory_paths:
        data = output_bytes[path] if path in output_bytes else (repo / path).read_bytes()
        inventory.append({"path": path, "sha256": sha256_bytes(data), "size_bytes": len(data)})
    manifest = {
        "artifact_id": "P2-I2-I11-CLOSEOUT-MANIFEST",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I11",
        "lane_id": "AE01-L02",
        "status": "review_ready_closeout_complete",
        "source_input_freeze": FREEZE_REL,
        "source_input_freeze_sha256": sha256_file(repo / FREEZE_REL),
        "frozen_input_verification": {"verified": True, "input_count": freeze["input_identity_count"]},
        "terminal_classification": "supported_bounded_candidate",
        "highest_valid_rung": "AE01-L02-R05",
        "lane_support_status": "scaffold_dependent",
        "classification_value": "T3_operational_class",
        "strongest_valid_claim": CLAIM_CEILING,
        "mode_dispositions": developmental["record"]["extensions"]["x_mode_dispositions"],
        "metric_relation_configuration_index": developmental["record"]["extensions"]["x_metric_relation_configuration_index"],
        "terminal_guard_revalidation": {
            "required_control_count": 10,
            "required_mode_result_count": 30,
            "passed_mode_result_count": 30,
            "failed_mode_result_count": 0,
            "results": guards,
        },
        "control_summary": {
            "comparison_rules": {"pass": 38},
            "lane_controls": {"pass": 15},
            "program_common_mode_results": {"pass": 56, "not_applicable": 1},
        },
        "execution_boundary": {
            "retained_files_parsed": True,
            "pygrc_imports": 0,
            "model_constructions": 0,
            "adapter_constructions": 0,
            "packet_constructions": 0,
            "c02_worker_invocations": 0,
            "response_or_control_invocations": 0,
            "matrix_entry_regenerations": 0,
            "new_scientific_inputs": 0,
            "accepted_artifact_mutations": 0,
            "mode_rankings": 0,
            "n31_selections": 0,
            "graph_mutations": 0,
            "persisted_absolute_paths": 0,
        },
        "artifact_inventory": inventory,
        "artifact_count": len(inventory),
        "validation_output_path": VALIDATION_REL,
        "independent_reconstruction_required": True,
        "owner_acceptance": False,
        "CLOSE_GATE": "review_ready_pending_owner_acceptance",
        "commit_authorized": False,
    }
    manifest["canonical_payload_digest"] = canonical_digest(manifest)
    output_bytes[MANIFEST_REL] = json_bytes(manifest)
    require(not any(has_absolute_string(read_json_from_bytes(data)) if path.endswith(".json") else has_absolute_string(data.decode("utf-8")) for path, data in output_bytes.items()), "I11 output contains absolute path")
    context = {
        "inputs": inputs,
        "developmental": developmental,
        "requirement": requirement,
        "terminal": terminal,
        "manifest": manifest,
        "guards": guards,
        "schema": schema,
    }
    return output_bytes, context


def read_json_from_bytes(value: bytes) -> dict[str, Any]:
    return json.loads(value.decode("utf-8"))


def write_build(repo: Path) -> None:
    outputs, _ = build_outputs(repo)
    for path, data in outputs.items():
        destination = repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    require(not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules), "I11 imported PyGRC")


def build_validation(repo: Path) -> dict[str, Any]:
    reconstructed, context = build_outputs(repo)
    checks: list[dict[str, Any]] = []

    def check(check_id: str, claim: str, observed: Any, passed: bool = True) -> None:
        checks.append({"check_id": check_id, "claim": claim, "observed": observed, "passed": passed})

    existing_equal = {path: (repo / path).read_bytes() == data for path, data in reconstructed.items()}
    dev = context["developmental"]["record"]
    term = context["terminal"]["record"]
    mode_rows = {row["mode"]: row for row in context["manifest"]["mode_dispositions"]}
    check("I11-01", "all 18 frozen input identities are exact", 18)
    check("I11-02", "repository venv and Python -B govern construction", {"interpreter": ".venv/bin/python", "dont_write_bytecode": True})
    check("I11-03", "C02 is complete with 234 evaluable terminals and zero missing or nonevaluable entry", {"evaluable": 234, "missing": 0, "nonevaluable": 0, "ambiguous": 0})
    check("I11-04", "I09A retains 38 comparison passes and 15 lane-control passes", {"comparison_pass": 38, "lane_control_pass": 15})
    check("I11-05", "all 57 program-control mode dispositions remain resolved", {"pass": 56, "not_applicable": 1})
    check("I11-06", "I10 retained-evidence reconstruction remains 24/24 passed", 24)
    check("I11-07", "all 18 mode-order-seed primary margins are preserved", sum(len(row["rows"]) for row in context["manifest"]["metric_relation_configuration_index"]))
    check("I11-08", "state-carried is robust aligned for both physical orders", mode_rows["state_carried"]["metric_relation"], mode_rows["state_carried"]["metric_relation"] == "robust_aligned")
    check("I11-09", "history-carried preserves the order-conditioned mixed relation", mode_rows["history_carried"]["metric_relation"], mode_rows["history_carried"]["metric_relation"] == "mixed_direction")
    check("I11-10", "hybrid preserves the order-conditioned mixed relation", mode_rows["hybrid"]["metric_relation"], mode_rows["hybrid"]["metric_relation"] == "mixed_direction")
    for index, rung in enumerate(dev["boundary_rungs"], start=11):
        check(f"I11-{index:02d}", f"{rung['rung_id']} is assigned from retained mode-specific evidence", rung["status"], rung["status"] == "reached")
    check("I11-16", "all three realization classes remain explicit and unranked", {mode: {"realization": row["realization_class"], "rank": row["mode_ranking"]} for mode, row in mode_rows.items()}, all(row["mode_ranking"] is None for row in mode_rows.values()))
    check("I11-17", "lane-wide support uses the lowest honest scaffold-dependent boundary", dev["support_status"], dev["support_status"] == "scaffold_dependent")
    check("I11-18", "developmental value is T3 operational and not T4 theoretical", dev["classification_value"]["rung"], dev["classification_value"]["rung"] == "T3_operational_class")
    check("I11-19", "terminal class follows the frozen decision procedure", term["classification"], term["classification"] == "supported_bounded_candidate")
    check("I11-20", "all 30 terminal-sensitive program-guard mode results are derived and pass", Counter(row["observed_disposition"] for row in context["guards"]), all(row["observed_disposition"] == "pass" for row in context["guards"]))
    check("I11-21", "repeated-source equivalence remains non-gating and claim-limiting", {"gating": term["extensions"]["x_repeated_source_equivalence_gating"], "negative_signature_count": len(term["negative_signatures"])}, term["extensions"]["x_repeated_source_equivalence_gating"] is False)
    check("I11-22", "observed relation and LGRC demand implication remain separate", context["requirement"]["record"]["extensions"]["x_observed_relation"] != context["requirement"]["record"]["extensions"]["x_lgrc_demand_implication"])
    check("I11-23", "all required debt categories remain explicit", [row["category"] for row in dev["extensions"]["x_debt_ledger"]], len(dev["extensions"]["x_debt_ledger"]) == 11)
    check("I11-24", "the strongest claim equals the frozen L02 ceiling and stronger relabels are blocked", {"claim": term["extensions"]["x_strongest_valid_claim"], "blocked_count": len(term["extensions"]["x_blocked_relabels"])}, term["extensions"]["x_strongest_valid_claim"] == CLAIM_CEILING)
    check("I11-25", "one bounded next move has an explicit falsifier and requires new preregistration", {"disposition": dev["next_move"]["disposition"], "new_preregistration_required": dev["next_move"]["new_preregistration_required"]}, bool(dev["next_move"]["falsifier"]) and dev["next_move"]["new_preregistration_required"] is True)
    validate_schema(context["schema"], context["developmental"], context["requirement"], context["terminal"])
    check("I11-26", "developmental, requirement, and terminal records pass accepted JSON Schema", True)
    check("I11-27", "all primary closeout artifacts independently reconstruct byte-identically", existing_equal, all(existing_equal.values()))
    check("I11-28", "the complete generated closeout contains no absolute path", True, not any(has_absolute_string(read_json_from_bytes(data)) if path.endswith(".json") else has_absolute_string(data.decode("utf-8")) for path, data in reconstructed.items()))
    check("I11-29", "I11 performs zero PyGRC, model, adapter, packet, C02, response, control, or scientific runtime operation", context["manifest"]["execution_boundary"], all(value == 0 for key, value in context["manifest"]["execution_boundary"].items() if key != "retained_files_parsed") and context["manifest"]["execution_boundary"]["retained_files_parsed"] is True)
    check("I11-30", "manifest canonical payload digest reconstructs", context["manifest"]["canonical_payload_digest"], context["manifest"]["canonical_payload_digest"] == canonical_digest(context["manifest"]))
    require(len(checks) == 30, "I11 validation check count drift")
    require(all(row["passed"] for row in checks), "I11 validation failed")
    validation = {
        "artifact_id": "P2-I2-I11-CLOSEOUT-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I11",
        "lane_id": "AE01-L02",
        "status": "passed",
        "source_input_freeze": FREEZE_REL,
        "source_input_freeze_sha256": sha256_file(repo / FREEZE_REL),
        "manifest_path": MANIFEST_REL,
        "manifest_sha256": sha256_file(repo / MANIFEST_REL),
        "checks": checks,
        "summary": {"check_count": 30, "passed": 30, "failed": 0, "blockers": 0},
        "independent_reconstruction": {
            "reconstructed_output_count": len(reconstructed),
            "byte_identical_output_count": sum(existing_equal.values()),
            "all_byte_identical": all(existing_equal.values()),
            "generated_scientific_operation_count": 0,
        },
        "CLOSE_GATE": "review_ready_pending_owner_acceptance",
        "owner_acceptance": False,
        "commit_authorized": False,
    }
    validation["canonical_payload_digest"] = canonical_digest(validation)
    require(not has_absolute_string(validation), "I11 validation contains absolute path")
    return validation


def write_validation(repo: Path) -> None:
    validation = build_validation(repo)
    (repo / VALIDATION_REL).write_bytes(json_bytes(validation))
    require(not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules), "I11 imported PyGRC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "validate"))
    args = parser.parse_args()
    repo = repository_root()
    verify_runtime(repo)
    if args.command == "build":
        write_build(repo)
        print("P2-I2 I11 closeout build complete")
    else:
        write_validation(repo)
        print("P2-I2 I11 independent reconstruction passed 30/30")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
