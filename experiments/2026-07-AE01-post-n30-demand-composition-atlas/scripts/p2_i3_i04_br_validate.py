"""Zero-calibration validator for the P2-I3 B-R I04 machine package."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from ae01_tooling import ContractError, pretty_json_dumps
from p2_i3_i04_br_analysis import PAIRING_FIELDS, parse_rational


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
DEFAULT_POLICY = EXPERIMENT / "configs/p2_i3_br_i04_machine_policy.json"
DEFAULT_SCHEMA = EXPERIMENT / "contracts/p2-i3/i04-br-machine-records.schema.json"
DEFAULT_PREREGISTRATION = EXPERIMENT / "contracts/p2-i3/i04-br-calibration-preregistration.json"
RETAINED_VALIDATION = EXPERIMENT / "contracts/p2-i3/i04-br-calibration-preregistration-validation.json"
ANALYSIS = EXPERIMENT / "scripts/p2_i3_i04_br_analysis.py"
TESTS = EXPERIMENT / "implementation/tests/test_p2_i3_i04_br.py"

EXPECTED_DECISIONS = [f"P2-I3-DEC-{index:03d}" for index in range(36, 41)]
EXPECTED_COMMON = {f"AE01-CTRL-{index:02d}" for index in range(1, 20)}
EXPECTED_LANE = {f"AE01-L03-CTRL-{index:02d}" for index in range(1, 6)}
EXPECTED_SEEDS = [19, 43, 71, 109, 163]
EXPECTED_CANDIDATE_SEEDS = [101, 211, 307]
EXPECTED_PANEL_A = {
    "EQ-NEG-HALF": "-1/2",
    "EQ-NEG-QUARTER": "-1/4",
    "EQ-ZERO": "0",
    "EQ-POS-QUARTER": "1/4",
    "EQ-POS-HALF": "1/2",
}
EXPECTED_CONFORMANCE_CASES = {
    "TRACE-FIRST-DOM-POS",
    "TRACE-SECOND-DOM-NEG",
    "EXPORT-FIRST-DOM-POS",
    "EXPORT-SECOND-DOM-NEG",
    "FLOOR-DOM-POS",
    "FLOOR-EQUALITY",
    "TRACE-CROSS-ZERO",
    "EXPORT-CROSS-ZERO",
}
EXPECTED_CTRL08 = {
    "P2-I3-BR-CTRL-08-LEG-01-EXPORT-POLICY-OMISSION",
    "P2-I3-BR-CTRL-08-LEG-02-LIFECYCLE-SCHEDULE",
    "P2-I3-BR-CTRL-08-LEG-03-ENCOUNTER-ADAPTER-BOUNDARY",
    "P2-I3-BR-CTRL-08-LEG-04-COMPOSITE-COORDINATION",
}
EXPECTED_CTRL09 = {
    "P2-I3-BR-CTRL-09-LEG-01-FORMATION-COST",
    "P2-I3-BR-CTRL-09-LEG-02-GLOBAL-CONSERVATION",
    "P2-I3-BR-CTRL-09-LEG-03-UNREGISTERED-LEAKAGE",
    "P2-I3-BR-CTRL-09-LEG-04-RESERVOIR-ISOLATION",
    "P2-I3-BR-CTRL-09-LEG-05-EXPORT-MASS-ORGANIZATION",
}
EXPECTED_FALSE_TRACE = {
    "P2-I3-BR-L03-CTRL-03-LEG-01-CARRIER-MATCHED-FALSE-TRACE",
    "P2-I3-BR-L03-CTRL-03-LEG-02-CAUSAL-PROJECTION-MATCHED-FALSE-TRACE",
}
EXPECTED_DYNAMIC_FAMILY = {
    "P2-I3-BR-L03-CTRL-04-LEG-01-O-E-LIFECYCLE",
    "P2-I3-BR-L03-CTRL-04-LEG-02-EQUAL-CARRIER-CLAMP",
    "P2-I3-BR-L03-CTRL-04-LEG-03-RESERVOIR-CLAMP",
    "P2-I3-BR-L03-CTRL-04-LEG-04-EXPORT-MASS-ORGANIZATION",
    "P2-I3-BR-L03-CTRL-04-LEG-05-ELIGIBLE-ZERO-FLOOR",
}
EXPECTED_REQUIREMENTS = {
    "P2-I3-BR-DISC-01-FORMATION-QUANTITY-TEMPORAL-MATCH",
    "P2-I3-BR-DISC-02-EXPORT-MASS-ORGANIZATION",
    "P2-I3-BR-DISC-03-COMPLETE-STATE-HISTORY",
    "P2-I3-BR-DISC-04-GEOMETRY-OR-TIMESCALE",
    "P2-I3-BR-DISC-05-FRESH-NONDEPOSITOR",
    "P2-I3-BR-VALID-01-EXACT-RESTORATION",
    "P2-I3-BR-VALID-02-EQUAL-INPUT-CONTINUATION",
    "P2-I3-BR-VALID-03-RECONSTRUCTION",
    "P2-I3-BR-VALID-04-FORBIDDEN-READ",
    "P2-I3-BR-VALID-05-RUNTIME-SOURCE-BINDING",
    "P2-I3-BR-CLAIM-01-PRODUCER-DEPENDENCE",
    "P2-I3-BR-CLAIM-02-FIXTURE-LOCK",
    "P2-I3-BR-CLAIM-03-NATIVE-RCAE-ATTRIBUTION",
    "P2-I3-BR-CLAIM-04-TRAIL-STIGMERGIC-PARTICIPANT",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise ContractError(f"path outside repository: {path}") from exc


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_blob(revision: str, relative_path: str) -> bytes:
    _require(not relative_path.startswith("/"), "git blob path must be relative")
    result = subprocess.run(
        ("git", "show", f"{revision}:{relative_path}"),
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    _require(result.returncode == 0, f"source absent at authority anchor: {relative_path}")
    return result.stdout


def _all_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        return [item for child in value.values() for item in _all_strings(child)]
    if isinstance(value, list):
        return [item for child in value for item in _all_strings(child)]
    return []


def _leg_ids(rows: list[dict[str, Any]], parent: str) -> set[str]:
    return {row["leg_id"] for row in rows if row["parent_control_id"] == parent}


def _initial_leg_state(row: Mapping[str, Any], status: Mapping[str, Any]) -> dict[str, Any]:
    key = "not_applicable" if row["applicability"] == "not_applicable" else (
        "applicable_or_conditional"
    )
    return {
        "leg_id": row["leg_id"],
        "parent_control_id": row["parent_control_id"],
        "applicability": row["applicability"],
        "control_class": row["control_class"],
        "evidence_types": row["evidence_types"],
        **status[key],
    }


def validate_policy(policy: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    checks: list[str] = []

    def passed(condition: bool, check_id: str) -> None:
        _require(condition, check_id)
        checks.append(check_id)

    Draft202012Validator.check_schema(schema)
    root_validator = Draft202012Validator(schema)
    passed(not root_validator.is_valid({}), "schema_root_rejects_empty_object")
    passed(not root_validator.is_valid({"nonsense": 1}), "schema_root_rejects_unknown_object")
    passed(not root_validator.is_valid({"record_type": "garbage"}), "schema_root_rejects_unknown_record")
    passed(schema.get("$id", "").endswith(":1.0.1"), "schema_bundle_version")
    passed(len(schema.get("$defs", {})) == 8, "schema_definition_count")
    passed(policy.get("policy_id") == "rcae-p2-i3-br-i04-machine-policy-v1", "policy_id")
    passed(policy.get("artifact_version") == "1.0.1", "policy_version")
    passed(policy.get("iteration_id") == "P2-I3-I04", "iteration_id")
    passed(policy.get("lane_id") == "AE01-L03" and policy.get("branch_id") == "P2-I3-BR", "lane_branch")
    passed(policy.get("scientific_outcomes_assigned") is False, "no_scientific_outcome")
    passed(policy["authority"]["decision_ids"] == EXPECTED_DECISIONS, "decision_chain")
    anchor = policy["authority"]["rcae_source_anchor"]
    passed(_git("merge-base", "--is-ancestor", anchor, "HEAD") == "", "authority_anchor_ancestor")
    for row in policy["authority"]["source_artifacts"]:
        blob = _git_blob(anchor, row["path"])
        passed(True, f"source_exists_at_anchor:{row['path']}")
        passed(
            hashlib.sha256(blob).hexdigest() == row["sha256"],
            f"source_digest_at_anchor:{row['path']}",
        )

    primary = policy["primary_response"]
    passed(primary["formula"] == "mu[e,j]=C_pre(m_e)-q_probe", "response_formula")
    passed(primary["raw_inputs_unrounded"] is True, "response_unrounded")
    passed(primary["disposition"]["nonnegative_margin"] == "admitted", "zero_admitted")
    passed(primary["disposition"]["negative_margin"] == "field_limited_refusal", "negative_refusal")
    passed("immediately before" in primary["observation_boundary"], "response_boundary")

    observation = policy["observation_policies"]
    passed(observation["geometric_distance"] == "derived_annotation_only", "geometric_annotation")
    passed(observation["functional_distance"] == "derived_annotation_only", "functional_annotation")
    passed(observation["causal_temporal"]["native_event_and_internal_time"] == "measured_native", "native_time_measured")
    passed(observation["causal_temporal"]["causal_shortest_path"] == "derived_annotation_only", "causal_path_annotation")
    influence = observation["experimental_causal_influence"]
    passed(influence["mandatory"] is True and influence["direct_observation_claim"] is False, "causal_influence_estimated")

    estimator = policy["estimator"]
    passed(estimator["pairing_fields"] == list(PAIRING_FIELDS), "pairing_fields")
    passed(estimator["trace_relation"]["formula"] == "N(E,W;epsilon_mu)", "trace_orientation")
    passed(estimator["export_relation"]["formula"] == "N(O,E;epsilon_mu)", "export_orientation")
    passed(estimator["normalized_relations_additive"] is False, "normalized_nonadditive")
    passed(estimator["normalized_relations_clipped"] is False, "normalized_unclipped")
    passed("no imputation" in estimator["missingness"], "no_imputation")
    passed("first_arm" in estimator["denominator_tie_rule"] and "epsilon_mu" in estimator["denominator_tie_rule"], "denominator_tie_rule")
    passed("canonical positive zero" in estimator["relation_tie_rule"], "relation_tie_rule")

    measurement = policy["measurement_design"]
    passed(measurement["contrast_identities"] == [
        "P2-I3-BR-Q13-FORMATION-QUANTITY-MATCH-001",
        "P2-I3-BR-Q13-EXPORT-MASS-MATCH-001",
        "P2-I3-BR-Q13-COMPLETE-STATE-HISTORY-MATCH-001",
    ], "contrast_identities")
    cadence = measurement["observation_cadence"]
    passed(cadence["primary_encounter_count_per_pair"] == 1, "one_primary_encounter")
    passed(cadence["exact_numeric_times"] == "deferred_to_I06", "numeric_times_deferred")
    passed(len(cadence["field_dynamic_checkpoints"]) == 6, "dynamic_cadence")
    passed("external wall time" in cadence["timescale_justification"], "internal_time_only")
    passed({row["panel_id"] for row in measurement["panels"]} == {
        "primary_response",
        "selected_field_dynamic",
        "distance_surfaces",
        "cost_and_conservation",
        "causal_interventions",
    }, "measurement_panels")
    ladder = measurement["interpretation_ladder"]
    passed(ladder["automatic_terminal_gate"] is False, "threshold_not_terminal_gate")
    passed(ladder["narrow_or_resolution_limited_result_requires_interpretation"] is True, "narrow_result_interpreted")

    calibration = policy["calibration"]
    epsilon = parse_rational(calibration["epsilon_mu"]["rational"])
    passed(float(epsilon) == calibration["epsilon_mu"]["value"] == 1e-12, "epsilon_identity")
    panel_a = calibration["panel_a_exact_null"]
    passed([row["seed_alias"] for row in panel_a] == EXPECTED_SEEDS, "calibration_seed_aliases")
    passed(calibration["candidate_seed_exclusions"] == EXPECTED_CANDIDATE_SEEDS, "candidate_seed_exclusions")
    passed(not set(EXPECTED_SEEDS) & set(EXPECTED_CANDIDATE_SEEDS), "seed_disjointness")
    passed({row["case_id"] for row in panel_a} == set(EXPECTED_PANEL_A), "panel_a_cases")
    for row in panel_a:
        expected = EXPECTED_PANEL_A[row["case_id"]]
        passed(set(row["values"]) == {"W", "O", "E"}, f"panel_a_arms:{row['case_id']}")
        passed(set(row["values"].values()) == {expected}, f"panel_a_equality:{row['case_id']}")
    passed(calibration["panel_a_rules"]["randomness_used"] is False, "panel_a_no_randomness")
    passed(calibration["panel_a_rules"]["only_panel_entering_delta"] is True, "panel_a_only_delta")
    conformance = calibration["panels_b_c_estimator_conformance"]
    passed({row["case_id"] for row in conformance} == EXPECTED_CONFORMANCE_CASES, "conformance_cases")
    for row in conformance:
        passed(set(row["values"]) == {"W", "O", "E"}, f"conformance_arms:{row['case_id']}")
        for value in row["values"].values():
            parse_rational(value)
    passed(calibration["panels_b_c_rules"]["intentionally_nonzero_margins_enter_delta"] is False, "conformance_excluded_from_delta")
    passed(len(calibration["panel_e_validity_missingness"]) == 6, "missingness_cases")
    passed(calibration["panel_d_reconstruction"]["byte_exact_output_required"] is True, "byte_reconstruction")
    passed(calibration["delta_policy"]["generated_value_status"] == "pending_I05", "delta_pending")

    boundary = policy["candidate_blind_boundary"]
    passed(boundary["generator_accepts_candidate_shaped_arguments"] is False, "no_candidate_args")
    passed(boundary["i04_calibration_invocations"] == 0, "zero_calibration_invocations")
    passed(boundary["i04_candidate_or_control_invocations"] == 0, "zero_candidate_control_invocations")
    passed(boundary["i04_pygrc_model_instantiations"] == 0, "zero_pygrc_models")

    controls = policy["control_governance"]
    parent = controls["parent_applicability"]
    common_applicable = set(parent["common"]["applicable"])
    common_partial = set(parent["common"]["partially_applicable"])
    passed(common_applicable | common_partial == EXPECTED_COMMON, "common_parent_coverage")
    passed(common_partial == {"AE01-CTRL-10"}, "ctrl10_only_partial")
    passed(not parent["common"]["not_applicable"], "no_common_parent_na")
    passed(set(parent["lane"]["applicable"]) == EXPECTED_LANE, "lane_parent_coverage")
    common_rows = controls["common_control_legs"]
    lane_rows = controls["lane_control_legs"]
    all_rows = common_rows + lane_rows
    passed(len({row["leg_id"] for row in all_rows}) == len(all_rows), "unique_leg_ids")
    passed({row["parent_control_id"] for row in common_rows} == EXPECTED_COMMON, "common_leg_coverage")
    passed({row["parent_control_id"] for row in lane_rows} == EXPECTED_LANE, "lane_leg_coverage")
    passed(_leg_ids(common_rows, "AE01-CTRL-08") == EXPECTED_CTRL08, "ctrl08_factorization")
    passed(_leg_ids(common_rows, "AE01-CTRL-09") == EXPECTED_CTRL09, "ctrl09_factorization")
    passed(_leg_ids(lane_rows, "AE01-L03-CTRL-03") == EXPECTED_FALSE_TRACE, "false_trace_factorization")
    passed(_leg_ids(lane_rows, "AE01-L03-CTRL-04") == EXPECTED_DYNAMIC_FAMILY, "dynamic_family_factorization")
    ctrl10 = [row for row in common_rows if row["parent_control_id"] == "AE01-CTRL-10"]
    passed({row["applicability"] for row in ctrl10} == {"applicable", "not_applicable"}, "ctrl10_leg_applicability")
    passed(controls["o_arm_and_producer_omission"]["same_control"] is False, "o_not_omission")
    passed(controls["producer_cost_classes"] == ["contract_required", "rcae_ecology_required", "evidence_only"], "producer_cost_classes")
    passed(controls["false_trace_interpretation"]["costly_formation_effect"].startswith("unsupported"), "false_trace_cost_boundary")
    leg_policy = controls["leg_policy_registry"]
    all_leg_ids = {row["leg_id"] for row in all_rows}
    passed(set(leg_policy) == all_leg_ids, "leg_policy_exact_coverage")
    expected_leg_policy_fields = {
        "target_relation_ids",
        "owning_iteration",
        "allowed_evidence_resolutions",
        "claim_effect",
        "invalidity_effect",
        "unavailability_effect",
        "terminal_guard_role",
    }
    allowed_resolutions = {
        "supportive",
        "equivalent",
        "counterdirectional",
        "generic_effect",
        "mixed",
        "unresolved",
        "not_evaluated",
    }
    allowed_owners = {"P2-I3-I04", "P2-I3-I09", "P2-I3-I10", "P2-I3-I11"}
    allowed_terminal_roles = {
        "none",
        "preterminal_guard_armed_I09",
        "reconstruction_guard_consumed_I11",
        "terminal_overlay_guard_I11",
        "not_applicable",
    }
    by_leg = {row["leg_id"]: row for row in all_rows}
    for leg_id, row in leg_policy.items():
        passed(set(row) == expected_leg_policy_fields, f"leg_policy_fields:{leg_id}")
        passed(bool(row["target_relation_ids"]) and len(row["target_relation_ids"]) == len(set(row["target_relation_ids"])), f"leg_policy_targets:{leg_id}")
        passed(row["owning_iteration"] in allowed_owners, f"leg_policy_owner:{leg_id}")
        passed(bool(row["allowed_evidence_resolutions"]) and set(row["allowed_evidence_resolutions"]) <= allowed_resolutions, f"leg_policy_resolutions:{leg_id}")
        passed(all(isinstance(row[field], str) and row[field] for field in ("claim_effect", "invalidity_effect", "unavailability_effect")), f"leg_policy_effects:{leg_id}")
        passed(row["terminal_guard_role"] in allowed_terminal_roles, f"leg_policy_terminal_role:{leg_id}")
        source_leg = by_leg[leg_id]
        if source_leg["applicability"] == "not_applicable":
            passed(row["owning_iteration"] == "P2-I3-I04", f"leg_policy_na_owner:{leg_id}")
            passed(row["allowed_evidence_resolutions"] == ["not_evaluated"], f"leg_policy_na_resolution:{leg_id}")
            passed(row["terminal_guard_role"] == "not_applicable", f"leg_policy_na_terminal:{leg_id}")
        elif source_leg["control_class"] == "terminal_semantic_guard":
            passed(row["owning_iteration"] == "P2-I3-I11", f"leg_policy_i11_owner:{leg_id}")
            passed(row["terminal_guard_role"] == "terminal_overlay_guard_I11", f"leg_policy_i11_terminal:{leg_id}")
        elif source_leg["control_class"] == "reconstruction_guard":
            passed(row["owning_iteration"] == "P2-I3-I10", f"leg_policy_i10_owner:{leg_id}")
            passed(row["terminal_guard_role"] == "reconstruction_guard_consumed_I11", f"leg_policy_i10_terminal:{leg_id}")
        else:
            passed(row["owning_iteration"] == "P2-I3-I09", f"leg_policy_i09_owner:{leg_id}")
    conservation = leg_policy["P2-I3-BR-CTRL-09-LEG-02-GLOBAL-CONSERVATION"]
    passed(conservation["allowed_evidence_resolutions"] == ["supportive"], "conservation_support_only")
    passed(conservation["invalidity_effect"] == "invalidate affected execution", "conservation_invalidates_execution")
    mass_specificity = leg_policy["P2-I3-BR-CTRL-09-LEG-05-EXPORT-MASS-ORGANIZATION"]
    passed("generic_effect" in mass_specificity["allowed_evidence_resolutions"], "mass_generic_effect_allowed")
    passed("does not invalidate" in mass_specificity["claim_effect"], "mass_generic_not_invalid")
    passed("R01" in leg_policy["P2-I3-BR-CTRL-09-LEG-01-FORMATION-COST"]["claim_effect"], "formation_cost_r01_effect")
    passed("without invalidating" in leg_policy["P2-I3-BR-CTRL-08-LEG-01-EXPORT-POLICY-OMISSION"]["claim_effect"], "producer_dependence_noninvalidating")
    passed("I09 facts" in leg_policy["P2-I3-BR-CTRL-12-LEG-01-SEMANTIC-CEILING"]["claim_effect"], "terminal_guard_preserves_i09")
    requirements = controls["requirement_registry"]
    passed({row["requirement_id"] for row in requirements} == EXPECTED_REQUIREMENTS, "requirement_ids")
    fresh = next(row for row in requirements if row["requirement_id"].endswith("FRESH-NONDEPOSITOR"))
    passed(fresh["applicability"] == "conditional" and fresh["required_for_tags"] == ["stigmergic_field_candidate"], "fresh_participant_conditional")

    control_schema = Draft202012Validator(schema["$defs"]["control_leg_state"])
    status = controls["initial_status_by_applicability"]
    for row in all_rows:
        errors = sorted(control_schema.iter_errors(_initial_leg_state(row, status)), key=lambda item: list(item.path))
        passed(not errors, f"control_leg_schema:{row['leg_id']}")

    sequencing = controls["sequencing"]
    passed("arm terminal guards" in sequencing["I09"], "i09_arms_terminal")
    passed("block I11" in sequencing["I10"], "i10_blocks_mismatch")
    passed("never change I09" in sequencing["I11"], "i11_overlay_immutable")
    passed("every claim-mandatory scientific leg" in controls["closeout_rules"]["not_supported"], "not_supported_completion")
    passed("no support or refutation" in controls["closeout_rules"]["blocked_incomplete_or_missing_surface"], "blocked_no_inference")

    tree = ast.parse(ANALYSIS.read_text(encoding="utf-8"))
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    passed(not any(name == "pygrc" or name.startswith("pygrc.") for name in imports), "analysis_no_pygrc_import")
    passed("build_calibration_record" not in ANALYSIS.read_text(encoding="utf-8"), "no_i04_calibration_builder")
    passed(not any(value.startswith("/home/") for value in _all_strings(policy)), "no_absolute_home_paths")
    i05 = policy["future_i05_boundary"]
    construction = i05["canonical_arithmetic_response_construction"]
    passed(construction["construction_status"] == "must_be_selected_and_frozen_in_separate_I05_invocation_freeze", "i05_construction_deferred")
    passed(construction["candidate_shaped_arguments_allowed"] is False, "i05_candidate_args_forbidden")
    passed(construction["carrier_coherence_may_be_negative"] is False, "i05_negative_carrier_forbidden")
    passed("c_pre_m_e - q_probe" in construction["exact_requirement"], "i05_exact_margin_requirement")
    passed("mechanically prohibited" in construction["scientific_reuse"], "i05_scientific_reuse_forbidden")
    passed(policy["gate_boundary"]["CAL_PRE_status"] == "pending_bounded_correction_review", "cal_pre_pending")
    passed(policy["future_i05_boundary"]["authorization_present"] is False, "i05_unauthorized")
    return checks


def validate_preregistration(
    preregistration: Mapping[str, Any], policy_path: Path, schema_path: Path
) -> list[str]:
    checks: list[str] = []

    def passed(condition: bool, check_id: str) -> None:
        _require(condition, check_id)
        checks.append(check_id)

    passed(preregistration.get("artifact_id") == "P2-I3-I04-BR-CALIBRATION-PREREGISTRATION", "preregistration_id")
    passed(preregistration.get("artifact_version") == "1.0.1", "preregistration_version")
    passed(preregistration.get("status") == "review_ready_not_accepted", "preregistration_status")
    passed(preregistration.get("calibration_invocations") == 0, "preregistration_zero_calibration")
    summary = preregistration["implementation_summary"]
    passed(summary["machine_schema_definitions"] == 8, "preregistration_schema_definition_count")
    passed(summary["per_leg_policy_records"] == 42, "preregistration_leg_policy_count")
    passed(summary["test_count"] == 22, "preregistration_test_count")
    identities = preregistration["machine_identities"]
    expected = {
        _relative(policy_path): _sha256(policy_path),
        _relative(schema_path): _sha256(schema_path),
        _relative(ANALYSIS): _sha256(ANALYSIS),
        _relative(Path(__file__)): _sha256(Path(__file__)),
        _relative(TESTS): _sha256(TESTS),
    }
    passed({row["path"]: row["sha256"] for row in identities} == expected, "machine_identity_digests")
    passed(preregistration["gate_boundary"]["CAL_PRE_status"] == "pending_review", "preregistration_gate_pending")
    passed(preregistration["gate_boundary"]["I05_authorized"] is False, "preregistration_i05_disabled")
    reconstruction = preregistration["reconstruction"]
    passed("outputs/reconstruction/" in reconstruction["validation_reconstruction_command"], "preregistration_safe_reconstruction_path")
    passed("cmp " in reconstruction["validation_compare_command"], "preregistration_explicit_compare")
    passed("--artifact-construction" in reconstruction["validation_artifact_construction_command"], "preregistration_explicit_construction")
    return checks


def build_validation(
    policy_path: Path, schema_path: Path, preregistration_path: Path
) -> dict[str, Any]:
    policy = _load(policy_path)
    schema = _load(schema_path)
    preregistration = _load(preregistration_path)
    checks = validate_policy(policy, schema)
    checks.extend(validate_preregistration(preregistration, policy_path, schema_path))
    return {
        "artifact_id": "P2-I3-I04-BR-CALIBRATION-PREREGISTRATION-VALIDATION",
        "artifact_version": "1.0.1",
        "iteration_id": "P2-I3-I04",
        "lane_id": "AE01-L03",
        "branch_id": "P2-I3-BR",
        "status": "passed_review_readiness_validation",
        "check_count": len(checks),
        "checks": checks,
        "source_anchor": policy["authority"]["rcae_source_anchor"],
        "current_source_revision": _git("rev-parse", "HEAD"),
        "machine_identities": {
            _relative(path): _sha256(path)
            for path in (policy_path, schema_path, ANALYSIS, Path(__file__), TESTS, preregistration_path)
        },
        "reconstruction": {
            "serializer": "ae01_tooling.pretty_json_dumps",
            "semantic_round_trip": "passed",
            "validation_rebuild_command": (
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
                "scripts/p2_i3_i04_br_validate.py --output "
                "outputs/reconstruction/p2-i3-i04-validation.reconstructed.json"
            ),
            "validation_compare_command": (
                "cmp experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
                "contracts/p2-i3/i04-br-calibration-preregistration-validation.json "
                "outputs/reconstruction/p2-i3-i04-validation.reconstructed.json"
            ),
            "artifact_construction_command": (
                ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
                "scripts/p2_i3_i04_br_validate.py --artifact-construction --output "
                "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
                "contracts/p2-i3/i04-br-calibration-preregistration-validation.json"
            ),
        },
        "execution_boundary": {
            "calibration_invocations": 0,
            "candidate_or_control_invocations": 0,
            "pygrc_imports_or_model_instantiations": 0,
            "scientific_outcomes": 0,
        },
        "gate_boundary": {
            "P2-I3-CAL-PRE-GATE": "pending_review",
            "I05_authorized": False,
            "candidate_execution_authorized": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--preregistration", type=Path, default=DEFAULT_PREREGISTRATION)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--artifact-construction", action="store_true")
    args = parser.parse_args()
    retained_output = args.output is not None and args.output.resolve() == RETAINED_VALIDATION.resolve()
    if retained_output and not args.artifact_construction:
        raise ContractError(
            "refusing to overwrite retained validation during reconstruction; "
            "use a distinct output path"
        )
    if args.artifact_construction and not retained_output:
        raise ContractError(
            "artifact construction mode is restricted to the retained validation path"
        )
    result = build_validation(args.policy, args.schema, args.preregistration)
    text = pretty_json_dumps(result)
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
