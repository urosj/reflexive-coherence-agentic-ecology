"""Pure deterministic analysis for the P2-I1 minimal niche probe.

This module has no PyGRC dependency and performs no file I/O.  Synthetic
calibration panels and later live opportunity records use the same aggregation
and paired-margin functions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import math
from typing import Any

from ae01_tooling import ContractError, digest_canonical_data


OPPORTUNITY_STATUSES = (
    "observed",
    "inadmissible",
    "structurally_unavailable",
    "censored_runtime",
    "missing_infrastructure",
    "blocked_by_control",
)
SCIENTIFIC_STATUSES = frozenset(OPPORTUNITY_STATUSES[:3])
OPERATIONAL_STATUSES = frozenset(OPPORTUNITY_STATUSES[3:])
ADMISSIBILITY_VALUES = ("admissible", "inadmissible", "not_evaluable")

_POLICY_KEYS = {
    "evidence_effect",
    "schema_version",
    "policy_id",
    "aggregation_policy",
    "rung_classifier_policy",
    "terminal_classifier_input_policy",
}
_AGGREGATION_KEYS = {
    "opportunity_count_per_seed",
    "valid_raw_responses",
    "scientific_statuses",
    "operational_statuses",
    "formation_status",
    "formation_requires_complete_chain",
    "operational_missingness_policy",
    "scientific_denominator_policy",
    "orientation_transform",
    "direction",
    "paired_margin",
    "primary_comparison",
    "medium_dependency_comparison",
    "selectivity",
}
_PAIRED_MARGIN_KEYS = {
    "formula",
    "measurement_resolution",
    "retain_raw_coverage",
}
_SELECTIVITY_KEYS = {
    "contexts",
    "groups",
    "candidate_cell",
    "comparator_cell",
    "minimum_margin",
    "threshold_source",
    "uses_calibrated_delta",
    "threshold_candidate_blind",
    "expected_direction",
    "zero_interaction_relation",
}
_COMPARISON_KEYS = {
    "comparison_id",
    "candidate_cell",
    "comparator_cell",
    "metric_role",
    "uses_calibrated_delta",
}
_RUNG_KEYS = {
    "lane_id",
    "rungs",
    "machine_output",
    "authoritative_terminal_claim",
    "required_dimensions",
}
_TERMINAL_KEYS = {
    "machine_output",
    "terminal_classification_deferred",
    "required_cell_ids",
    "required_seed_ids",
    "required_control_resolution",
    "integrity_fail_closed",
    "threshold_crossing_is_not_terminal_acceptance",
    "claim_ceiling",
}


def _require_exact_keys(
    value: Mapping[str, Any], expected: set[str], *, context: str
) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise ContractError(
            f"{context} fields drifted; missing={missing}, unknown={unknown}"
        )


def _finite_float(value: Any, *, context: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{context} must be numeric") from exc
    if not math.isfinite(result):
        raise ContractError(f"{context} must be finite")
    return result


def validate_analysis_policy(policy: Mapping[str, Any]) -> None:
    """Fail closed when the frozen analysis policy changes shape or semantics."""

    _require_exact_keys(policy, _POLICY_KEYS, context="analysis policy")
    aggregation = policy.get("aggregation_policy")
    if not isinstance(aggregation, Mapping):
        raise ContractError("aggregation_policy must be an object")
    _require_exact_keys(
        aggregation, _AGGREGATION_KEYS, context="aggregation policy"
    )
    if aggregation["opportunity_count_per_seed"] != 4:
        raise ContractError("P2-I1 requires exactly four opportunities per seed")
    if aggregation["valid_raw_responses"] != [0, 1]:
        raise ContractError("P2-I1 raw-response vocabulary drifted")
    if tuple(aggregation["scientific_statuses"]) != tuple(OPPORTUNITY_STATUSES[:3]):
        raise ContractError("P2-I1 scientific-status vocabulary drifted")
    if tuple(aggregation["operational_statuses"]) != tuple(OPPORTUNITY_STATUSES[3:]):
        raise ContractError("P2-I1 operational-status vocabulary drifted")
    if aggregation["orientation_transform"] != "identity":
        raise ContractError("P2-I1 orientation must remain identity")
    paired = aggregation["paired_margin"]
    if not isinstance(paired, Mapping):
        raise ContractError("paired-margin policy shape drifted")
    _require_exact_keys(paired, _PAIRED_MARGIN_KEYS, context="paired-margin policy")
    resolution = _finite_float(
        paired["measurement_resolution"], context="measurement resolution"
    )
    if resolution <= 0.0:
        raise ContractError("measurement resolution must be positive")
    primary = aggregation["primary_comparison"]
    dependency = aggregation["medium_dependency_comparison"]
    if not isinstance(primary, Mapping) or not isinstance(dependency, Mapping):
        raise ContractError("comparison policies must be objects")
    _require_exact_keys(primary, _COMPARISON_KEYS, context="primary comparison")
    _require_exact_keys(
        dependency, _COMPARISON_KEYS, context="medium-dependency comparison"
    )
    if primary != {
        "comparison_id": "writer-relative-history-content",
        "candidate_cell": "candidate-conditioning",
        "comparator_cell": "reference",
        "metric_role": "primary_normalized_margin",
        "uses_calibrated_delta": True,
    }:
        raise ContractError("primary normalized-margin comparator drifted")
    if dependency != {
        "comparison_id": "feedback-row-presence-dependency",
        "candidate_cell": "candidate-conditioning",
        "comparator_cell": "medium-freeze-withdrawal",
        "metric_role": "causal_control_diagnostic",
        "uses_calibrated_delta": False,
    }:
        raise ContractError("medium-dependency comparator role drifted")
    selectivity = aggregation["selectivity"]
    if not isinstance(selectivity, Mapping):
        raise ContractError("selectivity policy must be an object")
    _require_exact_keys(selectivity, _SELECTIVITY_KEYS, context="selectivity policy")
    if selectivity.get("uses_calibrated_delta") is not False:
        raise ContractError("selectivity must not consume calibrated delta")
    if selectivity.get("threshold_candidate_blind") is not True:
        raise ContractError("selectivity threshold must remain candidate-blind")
    if selectivity.get("minimum_margin") != 0.5:
        raise ContractError("selectivity combinatorial resolution drifted")
    if selectivity.get("zero_interaction_relation") != "generic_main_effect_or_no_effect":
        raise ContractError("zero selectivity-interaction relation drifted")
    if selectivity.get("contexts") != ["A", "B"] or selectivity.get("groups") != [
        "aligned",
        "inverted",
    ]:
        raise ContractError("selectivity pair structure drifted")
    rung = policy.get("rung_classifier_policy")
    if not isinstance(rung, Mapping):
        raise ContractError("rung classifier policy must be an object")
    _require_exact_keys(rung, _RUNG_KEYS, context="rung classifier policy")
    if rung.get("lane_id") != "AE01-L01" or rung.get("authoritative_terminal_claim") is not False:
        raise ContractError("rung classifier claim boundary drifted")
    terminal = policy.get("terminal_classifier_input_policy")
    if not isinstance(terminal, Mapping):
        raise ContractError("terminal input policy must be an object")
    _require_exact_keys(terminal, _TERMINAL_KEYS, context="terminal input policy")
    if terminal.get("terminal_classification_deferred") is not True:
        raise ContractError("terminal classification must remain deferred")
    if terminal.get("integrity_fail_closed") is not True:
        raise ContractError("terminal integrity boundary must remain fail-closed")


def validate_opportunity(record: Mapping[str, Any]) -> None:
    """Validate one raw opportunity at the analysis boundary."""

    required = {
        "opportunity_id",
        "seed",
        "cell_id",
        "relation_chain_id",
        "writer_carrier_id",
        "writer_event_id",
        "medium_surface_id",
        "medium_change_event_id",
        "medium_history_digest",
        "later_opportunity_event_id",
        "reader_or_local_differentiation_id",
        "opportunity_index",
        "profile_id",
        "context",
        "selectivity_group",
        "raw_response",
        "oriented_response",
        "admissibility",
        "opportunity_status",
        "complete_registered_chain",
        "causal_order_verified",
        "medium_dependency_control_refs",
    }
    missing = sorted(required - set(record))
    if missing:
        raise ContractError(f"opportunity record missing fields: {missing}")
    if record["opportunity_status"] not in OPPORTUNITY_STATUSES:
        raise ContractError("unknown opportunity status")
    if record["admissibility"] not in ADMISSIBILITY_VALUES:
        raise ContractError("unknown admissibility value")
    status = str(record["opportunity_status"])
    raw = record["raw_response"]
    oriented = record["oriented_response"]
    if status in SCIENTIFIC_STATUSES:
        if raw not in (0, 1) or oriented != raw:
            raise ContractError("scientific opportunity requires identity-oriented 0/1")
        if status != "observed" and raw != 0:
            raise ContractError("non-observed scientific status must be non-formation")
        if raw == 1 and (
            status != "observed"
            or record["complete_registered_chain"] is not True
            or record["causal_order_verified"] is not True
        ):
            raise ContractError("formation requires observed complete ordered chain")
        if record["admissibility"] == "not_evaluable":
            raise ContractError("scientific opportunity cannot be not_evaluable")
    else:
        if raw is not None or oriented is not None:
            raise ContractError("operational opportunity response must be null")
        if record["admissibility"] != "not_evaluable":
            raise ContractError("operational opportunity must be not_evaluable")
    index = record["opportunity_index"]
    if not isinstance(index, int) or isinstance(index, bool) or index not in range(4):
        raise ContractError("opportunity_index must be one of 0, 1, 2, 3")
    refs = record["medium_dependency_control_refs"]
    if not isinstance(refs, list) or any(not isinstance(item, str) for item in refs):
        raise ContractError("medium dependency control refs must be string IDs")


def aggregate_seed(
    opportunities: Sequence[Mapping[str, Any]],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Aggregate one complete registered four-opportunity panel."""

    validate_analysis_policy(policy)
    if len(opportunities) != 4:
        raise ContractError("seed aggregation requires exactly four opportunities")
    for record in opportunities:
        validate_opportunity(record)
    seeds = {record["seed"] for record in opportunities}
    cells = {record["cell_id"] for record in opportunities}
    indices = {record["opportunity_index"] for record in opportunities}
    if len(seeds) != 1 or len(cells) != 1 or indices != set(range(4)):
        raise ContractError("opportunity panel must share seed/cell and cover indices 0..3")
    ordered = sorted(opportunities, key=lambda item: int(item["opportunity_index"]))
    counts = {status: 0 for status in OPPORTUNITY_STATUSES}
    for record in ordered:
        counts[str(record["opportunity_status"])] += 1
    operational = sum(counts[status] for status in OPERATIONAL_STATUSES)
    formed = sum(1 for record in ordered if record["raw_response"] == 1)
    evaluable = operational == 0
    fraction = formed / 4 if evaluable else None
    return {
        "seed": ordered[0]["seed"],
        "cell_id": ordered[0]["cell_id"],
        "planned_count": 4,
        "formed_count": formed,
        "status_counts": counts,
        "evaluable": evaluable,
        "formation_fraction": fraction,
        "oriented_response": fraction,
        "opportunity_ids": [record["opportunity_id"] for record in ordered],
        "profile_ids": [record["profile_id"] for record in ordered],
    }


def paired_margin(
    candidate: Mapping[str, Any],
    comparator: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Derive the frozen paired response while retaining absolute coverage."""

    validate_analysis_policy(policy)
    if candidate.get("seed") != comparator.get("seed"):
        raise ContractError("paired responses require identical seed")
    left = candidate.get("formation_fraction")
    right = comparator.get("formation_fraction")
    if left is None or right is None:
        return {
            "seed": candidate.get("seed"),
            "candidate_cell_id": candidate.get("cell_id"),
            "comparator_cell_id": comparator.get("cell_id"),
            "candidate_fraction": left,
            "comparator_fraction": right,
            "raw_paired_difference": None,
            "normalized_margin": None,
            "resolution_status": "resolution_unknown",
        }
    candidate_value = _finite_float(left, context="candidate fraction")
    comparator_value = _finite_float(right, context="comparator fraction")
    if not (0.0 <= candidate_value <= 1.0 and 0.0 <= comparator_value <= 1.0):
        raise ContractError("formation fractions must be within [0, 1]")
    resolution = float(
        policy["aggregation_policy"]["paired_margin"]["measurement_resolution"]
    )
    difference = candidate_value - comparator_value
    margin = difference / max(abs(candidate_value), abs(comparator_value), resolution)
    return {
        "seed": candidate["seed"],
        "candidate_cell_id": candidate["cell_id"],
        "comparator_cell_id": comparator["cell_id"],
        "candidate_fraction": candidate_value,
        "comparator_fraction": comparator_value,
        "raw_paired_difference": difference,
        "normalized_margin": margin,
        "resolution_status": "numeric_unclassified",
    }


def selectivity_interaction(
    candidate_opportunities: Sequence[Mapping[str, Any]],
    comparator_opportunities: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Derive both matched-pair interactions without applying calibrated delta."""

    for record in (*candidate_opportunities, *comparator_opportunities):
        validate_opportunity(record)
    candidate = {record["profile_id"]: record for record in candidate_opportunities}
    comparator = {record["profile_id"]: record for record in comparator_opportunities}
    if set(candidate) != set(comparator) or len(candidate) != 4:
        raise ContractError("selectivity requires matched four-profile panels")
    pairs: list[dict[str, Any]] = []
    for context in ("A", "B"):
        aligned = [
            item for item in candidate.values()
            if item["context"] == context and item["selectivity_group"] == "aligned"
        ]
        inverted = [
            item for item in candidate.values()
            if item["context"] == context and item["selectivity_group"] == "inverted"
        ]
        if len(aligned) != 1 or len(inverted) != 1:
            raise ContractError(f"context {context} must have one aligned/inverted pair")
        a = aligned[0]
        i = inverted[0]
        ca = comparator[a["profile_id"]]
        ci = comparator[i["profile_id"]]
        values = (a["raw_response"], i["raw_response"], ca["raw_response"], ci["raw_response"])
        if any(value is None for value in values):
            interaction = None
        else:
            interaction = (int(values[0]) - int(values[2])) - (
                int(values[1]) - int(values[3])
            )
        pairs.append({"context": context, "pair_interaction": interaction})
    if any(item["pair_interaction"] is None for item in pairs):
        relation = "non_evaluable"
        margin = None
    else:
        values = [float(item["pair_interaction"]) for item in pairs]
        margin = sum(values) / 2.0
        if all(value > 0 for value in values):
            relation = "strong_constructed_selectivity"
        elif any(value > 0 for value in values) and all(value >= 0 for value in values):
            relation = "weak_directionally_resolved"
        elif values[0] * values[1] < 0:
            relation = "mixed"
        elif margin == 0:
            relation = "generic_main_effect_or_no_effect"
        else:
            relation = "counter_selective"
    return {
        "pair_interactions": pairs,
        "selectivity_margin": margin,
        "selectivity_relation": relation,
        "uses_calibrated_delta": False,
    }


def _synthetic_opportunity(
    *, seed: int, side: str, index: int, raw_response: int
) -> dict[str, Any]:
    context = "A" if index < 2 else "B"
    group = "aligned" if index % 2 == 0 else "inverted"
    profile_id = f"ctx-{context.casefold()}-{group}"
    prefix = f"cal-{seed}-{side}-{index}"
    return {
        "opportunity_id": prefix,
        "seed": seed,
        "cell_id": side,
        "relation_chain_id": f"{prefix}-chain",
        "writer_carrier_id": "synthetic_no_runtime",
        "writer_event_id": "synthetic_no_runtime",
        "medium_surface_id": "synthetic_no_runtime",
        "medium_change_event_id": "synthetic_no_runtime",
        "medium_history_digest": "synthetic_no_runtime",
        "later_opportunity_event_id": f"{prefix}-later",
        "reader_or_local_differentiation_id": f"synthetic-{context}",
        "opportunity_index": index,
        "profile_id": profile_id,
        "context": context,
        "selectivity_group": group,
        "raw_response": raw_response,
        "oriented_response": raw_response,
        "admissibility": "admissible",
        "opportunity_status": "observed",
        "complete_registered_chain": True,
        "causal_order_verified": True,
        "medium_dependency_control_refs": [],
    }


def generate_matched_null(
    calibration_policy: Mapping[str, Any],
    analysis_policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Generate candidate-blind margins through the live-analysis code path."""

    validate_analysis_policy(analysis_policy)
    if calibration_policy.get("candidate_blind") is not True:
        raise ContractError("matched-null generation requires candidate blindness")
    if calibration_policy.get("runtime_execution") is not False:
        raise ContractError("matched-null generation must remain non-runtime")
    if calibration_policy.get("pygrc_imported") is not False:
        raise ContractError("matched-null generation must not import PyGRC")
    panels = calibration_policy.get("panels")
    if not isinstance(panels, list) or len(panels) != 5:
        raise ContractError("matched-null policy requires five panels")
    seed_margins: list[dict[str, Any]] = []
    panel_results: list[dict[str, Any]] = []
    for panel in panels:
        seed = int(panel["seed"])
        left_records = [
            _synthetic_opportunity(seed=seed, side="null_a", index=index, raw_response=value)
            for index, value in enumerate(panel["null_a"])
        ]
        right_records = [
            _synthetic_opportunity(seed=seed, side="null_b", index=index, raw_response=value)
            for index, value in enumerate(panel["null_b"])
        ]
        left = aggregate_seed(left_records, analysis_policy)
        right = aggregate_seed(right_records, analysis_policy)
        paired = paired_margin(left, right, analysis_policy)
        margin = paired["normalized_margin"]
        seed_margins.append({"seed": seed, "matched_null_margin": margin})
        panel_results.append(
            {
                "seed": seed,
                "null_a": left,
                "null_b": right,
                "paired": paired,
            }
        )
    resolution = float(calibration_policy["measurement_resolution"])
    delta = max(
        [resolution]
        + [abs(float(item["matched_null_margin"])) for item in seed_margins]
    )
    result = {
        "artifact_kind": "p2_i1_candidate_blind_matched_null",
        "schema_version": "1.0.0",
        "calibration_id": calibration_policy["calibration_id"],
        "candidate_blind": True,
        "runtime_execution": False,
        "pygrc_imported": False,
        "evidence_effect": "resolution_only_no_candidate_evidence",
        "measurement_resolution": resolution,
        "seed_margins": seed_margins,
        "delta": delta,
        "panel_results": panel_results,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}


def policy_projection_digests(policy: Mapping[str, Any]) -> dict[str, str]:
    """Return the three scientific policy identities from the one policy file."""

    validate_analysis_policy(policy)
    return {
        "aggregation_policy_digest": digest_canonical_data(
            policy["aggregation_policy"]
        ),
        "rung_classifier_digest": digest_canonical_data(
            policy["rung_classifier_policy"]
        ),
        "terminal_classifier_digest": digest_canonical_data(
            policy["terminal_classifier_input_policy"]
        ),
    }


def static_profile_identities(
    fixture: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Materialize candidate-blind static opportunity/profile digests."""

    feedback = fixture["feedback"]
    packet = fixture["packets"]
    result: list[dict[str, Any]] = []
    for profile in fixture["opportunity_profiles"]:
        identity = {
            **dict(profile),
            "fixture_id": fixture["fixture_id"],
            "packet_amount": packet["reader_amount"],
            "arrival_event_time_key": packet["arrival_event_time_key"],
            "feedback_threshold": feedback["producer_threshold"],
            "front_node_ids": feedback["front_node_ids"],
            "rear_node_ids": feedback["rear_node_ids"],
            "expected_source_surface_digest": "SYMBOLIC_REGISTERED_WRITER_ARRIVAL_CONTACT",
            "expected_next_route_id": None,
            "expected_next_channel_id": None,
        }
        reader_identity = {
            "source_node_id": profile["source_node_id"],
            "target_node_id": profile["target_node_id"],
            "edge_id": profile["edge_id"],
        }
        result.append(
            {
                "profile_id": profile["profile_id"],
                "reader_configuration_digest": digest_canonical_data(reader_identity),
                "opportunity_profile_digest": digest_canonical_data(identity),
                "identity": identity,
            }
        )
    return result


def build_rung_and_terminal_inputs(
    *,
    cell_aggregates: Sequence[Mapping[str, Any]],
    paired_margins: Sequence[Mapping[str, Any]],
    selectivity_results: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Assemble machine inputs without selecting a rung or terminal class."""

    return {
        "artifact_kind": "p2_i1_interpretation_inputs",
        "schema_version": "1.0.0",
        "cell_aggregates": list(cell_aggregates),
        "paired_margins": list(paired_margins),
        "selectivity_results": list(selectivity_results),
        "rung_assignment": None,
        "terminal_classification": None,
        "authored_recomputation_required": False,
    }
