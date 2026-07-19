"""Pure B-R response and estimator semantics for P2-I3 I04.

This module imports no PyGRC code, reads no candidate artifact, and performs
no calibration invocation.  I04 uses it as the exact future analysis surface
for typed response records and W/O/E pair estimators.  A later separately
authorized I05 builder may consume the same functions.
"""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Any, Mapping, Sequence

from ae01_tooling import ContractError


POLICY_ID = "rcae-p2-i3-br-i04-machine-policy-v1"
RESPONSE_SCHEMA_ID = "p2-i3-br-encounter-response-v1"
PAIR_RESULT_SCHEMA_ID = "p2-i3-br-normalized-pair-result-v1"
TRIPLET_RESULT_SCHEMA_ID = "p2-i3-br-woe-triplet-result-v1"

ARMS = ("W", "O", "E")
VALID_DISPOSITIONS = ("admitted", "field_limited_refusal")
INVALID_DISPOSITION = "invalid_or_infrastructure_failure"
PAIRING_FIELDS = (
    "calibration_stratum",
    "deterministic_replicate",
    "configuration_or_variation_id",
    "route_role",
    "clean_parent_identity",
    "causal_continuation_projection_identity",
    "encounter_index",
    "request_construction_id",
    "request_timing_id",
    "future_schedule_identity",
    "observation_boundary_id",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def parse_rational(value: str) -> Fraction:
    """Parse a finite exact rational string used by candidate-blind panels."""

    _require(isinstance(value, str) and value, "rational value must be a string")
    try:
        result = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ContractError(f"invalid rational value: {value!r}") from exc
    _require(math.isfinite(float(result)), "rational value must be finite")
    return result


def rational_string(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def canonical_zero(value: float) -> float:
    return 0.0 if value == 0.0 else value


def disposition_for_margin(margin: Fraction) -> str:
    return "admitted" if margin >= 0 else "field_limited_refusal"


def build_synthetic_response_record(
    *,
    record_id: str,
    pair_id: str,
    arm_id: str,
    margin: str,
    seed_alias: int,
    case_id: str,
    pairing: Mapping[str, Any],
) -> dict[str, Any]:
    """Build one complete arithmetic-synthetic record through DEC-036 shape.

    This helper does not iterate a calibration panel or derive ``delta``.  It
    exists so focused unit tests and a later authorized builder use the same
    typed response path.
    """

    _require(arm_id in ARMS, "synthetic response arm must be W, O, or E")
    _require(set(pairing) == set(PAIRING_FIELDS), "pairing fields drifted")
    mu = parse_rational(margin)
    q_probe = Fraction(1, 1)
    c_pre = q_probe + mu
    _require(c_pre >= 0, "synthetic carrier coherence must be nonnegative")
    return {
        "record_type": RESPONSE_SCHEMA_ID,
        "record_version": "1.0.0",
        "record_id": record_id,
        "pair_id": pair_id,
        "arm_id": arm_id,
        "case_id": case_id,
        "calibration_seed_alias": seed_alias,
        "randomness_used": False,
        "source_class": "candidate_blind_arithmetic_synthetic",
        "candidate_artifacts_consumed": False,
        "pygrc_runtime_inputs_consumed": False,
        "candidate_execution_performed": False,
        "coherence_units": "native_lgrc9v3_coherence",
        "c_pre_m_e": {
            "rational": rational_string(c_pre),
            "value": float(c_pre),
        },
        "q_probe": {
            "rational": rational_string(q_probe),
            "value": float(q_probe),
        },
        "admissibility_margin": {
            "rational": rational_string(mu),
            "value": canonical_zero(float(mu)),
        },
        "native_disposition": disposition_for_margin(mu),
        "validity_status": "valid",
        "diagnostic_margin": None,
        "pairing": dict(pairing),
    }


def validate_response_record(record: Mapping[str, Any]) -> None:
    _require(record.get("record_type") == RESPONSE_SCHEMA_ID, "response type drifted")
    _require(record.get("record_version") == "1.0.0", "response version drifted")
    _require(record.get("arm_id") in ARMS, "response arm drifted")
    _require(set(record.get("pairing", {})) == set(PAIRING_FIELDS), "pairing drifted")
    _require(record.get("source_class") in {
        "candidate_blind_arithmetic_synthetic",
        "registered_live_response",
    }, "response source class drifted")

    source_class = record.get("source_class")
    if source_class == "candidate_blind_arithmetic_synthetic":
        _require(record.get("calibration_seed_alias") is not None, "synthetic seed alias missing")
        _require(record.get("randomness_used") is False, "synthetic randomness forbidden")
        _require(record.get("candidate_artifacts_consumed") is False, "candidate artifact forbidden")
        _require(record.get("pygrc_runtime_inputs_consumed") is False, "PyGRC input forbidden")
        _require(record.get("candidate_execution_performed") is False, "candidate execution forbidden")
    else:
        _require(record.get("calibration_seed_alias") is None, "live response cannot use a calibration seed alias")
        _require(record.get("candidate_artifacts_consumed") is True, "live response must declare candidate artifact consumption")
        _require(record.get("pygrc_runtime_inputs_consumed") is True, "live response must declare PyGRC input consumption")
        _require(record.get("candidate_execution_performed") is True, "live response must declare candidate execution")

    c_pre = record.get("c_pre_m_e")
    q_probe = record.get("q_probe")
    _require(isinstance(c_pre, Mapping) and isinstance(q_probe, Mapping), "raw inputs missing")
    c_value = parse_rational(str(c_pre.get("rational")))
    q_value = parse_rational(str(q_probe.get("rational")))
    _require(float(c_value) == c_pre.get("value"), "carrier rational/value mismatch")
    _require(float(q_value) == q_probe.get("value"), "request rational/value mismatch")
    _require(c_value >= 0, "carrier coherence cannot be negative")
    _require(q_value >= 0, "probe request cannot be negative")

    status = record.get("validity_status")
    disposition = record.get("native_disposition")
    margin = record.get("admissibility_margin")
    if status == "invalid_or_infrastructure_failure":
        _require(disposition == INVALID_DISPOSITION, "invalid response disposition drifted")
        _require(margin is None, "invalid response cannot expose a primary margin")
        return

    _require(status == "valid", "unknown response validity status")
    _require(disposition in VALID_DISPOSITIONS, "valid response disposition drifted")
    _require(isinstance(margin, Mapping), "valid response margin missing")
    mu = parse_rational(str(margin.get("rational")))
    _require(float(mu) == margin.get("value"), "response rational/value mismatch")
    _require(math.isfinite(float(mu)), "response margin must be finite")
    expected = disposition_for_margin(mu)
    _require(disposition == expected, "native disposition/sign mismatch")

    _require(c_value - q_value == mu, "mu must equal C_pre(m_e) - q_probe")


def _same_pair(left: Mapping[str, Any], right: Mapping[str, Any]) -> None:
    _require(left.get("pair_id") == right.get("pair_id"), "pair identity mismatch")
    _require(left.get("pairing") == right.get("pairing"), "pairing projection mismatch")
    _require(left.get("coherence_units") == right.get("coherence_units"), "unit mismatch")
    _require(left.get("q_probe") == right.get("q_probe"), "request mismatch")


def estimate_pair(
    first: Mapping[str, Any],
    second: Mapping[str, Any],
    *,
    relation_id: str,
    epsilon_mu: float,
) -> dict[str, Any]:
    """Evaluate one ordered normalized pair without surviving-arm fallback."""

    _require(epsilon_mu > 0 and math.isfinite(epsilon_mu), "epsilon_mu must be positive")
    validate_response_record(first)
    validate_response_record(second)
    _same_pair(first, second)
    if (
        first.get("validity_status") != "valid"
        or second.get("validity_status") != "valid"
    ):
        return {
            "record_type": PAIR_RESULT_SCHEMA_ID,
            "record_version": "1.0.0",
            "relation_id": relation_id,
            "pair_id": first.get("pair_id"),
            "arm_record_ids": [first.get("record_id"), second.get("record_id")],
            "evaluable": False,
            "nonevaluable_record_ids": [
                row.get("record_id")
                for row in (first, second)
                if row.get("validity_status") != "valid"
            ],
            "raw_numerator": None,
            "denominator": None,
            "denominator_source": None,
            "normalized_margin": None,
        }

    first_mu = parse_rational(first["admissibility_margin"]["rational"])
    second_mu = parse_rational(second["admissibility_margin"]["rational"])
    epsilon_exact = Fraction(str(epsilon_mu))
    denominator_exact = max(abs(first_mu), abs(second_mu), epsilon_exact)
    if denominator_exact == epsilon_exact:
        denominator_source = "epsilon_mu"
    elif abs(first_mu) >= abs(second_mu):
        denominator_source = "first_arm"
    else:
        denominator_source = "second_arm"
    numerator_exact = first_mu - second_mu
    return {
        "record_type": PAIR_RESULT_SCHEMA_ID,
        "record_version": "1.0.0",
        "relation_id": relation_id,
        "pair_id": first["pair_id"],
        "arm_record_ids": [first["record_id"], second["record_id"]],
        "evaluable": True,
        "nonevaluable_record_ids": [],
        "raw_numerator": canonical_zero(float(numerator_exact)),
        "denominator": float(denominator_exact),
        "denominator_source": denominator_source,
        "normalized_margin": canonical_zero(float(numerator_exact / denominator_exact)),
    }


def estimate_woe_triplet(
    records: Sequence[Mapping[str, Any]], *, epsilon_mu: float
) -> dict[str, Any]:
    """Evaluate DEC-038 trace and export pairs from one exact W/O/E triplet."""

    _require(len(records) == 3, "exactly three W/O/E records required")
    by_arm = {str(row.get("arm_id")): row for row in records}
    _require(set(by_arm) == set(ARMS), "one unique W, O, and E record required")
    trace = estimate_pair(
        by_arm["E"], by_arm["W"], relation_id="m_trace", epsilon_mu=epsilon_mu
    )
    export = estimate_pair(
        by_arm["O"], by_arm["E"], relation_id="m_export", epsilon_mu=epsilon_mu
    )
    raw_identity = None
    if trace["evaluable"] and export["evaluable"]:
        mu_w = parse_rational(by_arm["W"]["admissibility_margin"]["rational"])
        mu_o = parse_rational(by_arm["O"]["admissibility_margin"]["rational"])
        mu_e = parse_rational(by_arm["E"]["admissibility_margin"]["rational"])
        delta_trace = mu_e - mu_w
        delta_export = mu_o - mu_e
        delta_formed = mu_o - mu_w
        raw_identity = {
            "delta_trace": canonical_zero(float(delta_trace)),
            "delta_export": canonical_zero(float(delta_export)),
            "delta_formed": canonical_zero(float(delta_formed)),
            "additive_identity_holds": delta_trace + delta_export == delta_formed,
        }
    return {
        "record_type": TRIPLET_RESULT_SCHEMA_ID,
        "record_version": "1.0.0",
        "pair_id": records[0].get("pair_id"),
        "trace_relation": trace,
        "export_relation": export,
        "raw_additive_identity": raw_identity,
        "normalized_relations_additive": False,
        "normalized_relations_are_percentages": False,
        "normalized_relations_clipped": False,
    }
