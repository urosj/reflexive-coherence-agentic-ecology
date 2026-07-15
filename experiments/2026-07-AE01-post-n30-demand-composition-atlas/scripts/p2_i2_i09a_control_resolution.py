#!/usr/bin/env python3
"""Build and validate the additive P2-I2 I09A estimator correction."""

from __future__ import annotations

import argparse
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable


EXPERIMENT = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
FREEZE_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-input-freeze.json"
INDEX_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-index.json"
VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-validation.json"
REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I09A-normalized-estimator-correction.md"
SCRIPT_REL = f"{EXPERIMENT}/scripts/p2_i2_i09a_control_resolution.py"
I09_FREEZE_REL = f"{EXPERIMENT}/contracts/p2-i2/i09-control-resolution-input-freeze.json"
I09_INDEX_REL = f"{EXPERIMENT}/contracts/p2-i2/i09-control-resolution-index.json"
I09_VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i09-control-resolution-validation.json"
I09_REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I09-control-resolution.md"
MACHINE_POLICY_REL = f"{EXPERIMENT}/configs/p2_i2_i04r2_machine_policy.json"
PARENT_POLICY_REL = f"{EXPERIMENT}/configs/p2_i2_i04r1_analysis_policy.json"
CALIBRATION_REL = f"{EXPERIMENT}/contracts/p2-i2/metric-calibration.json"
MODES = ("state_carried", "history_carried", "hybrid")
ORDERS = ("q1_then_q2", "q2_then_q1")
SEEDS = (101, 211, 307)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(payload: dict[str, Any]) -> str:
    clean = copy.deepcopy(payload)
    clean.pop("canonical_payload_digest", None)
    encoded = json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256((encoded + "\n").encode("utf-8")).hexdigest()


def json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


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


def verify_runtime(repo: Path) -> None:
    expected = repo / ".venv/bin/python"
    require(expected.exists(), "repository .venv interpreter is absent")
    require(Path(sys.executable).samefile(expected), "I09A must run through repository .venv/bin/python")
    require(sys.dont_write_bytecode, "I09A requires Python -B")


def load_freeze(repo: Path, freeze_rel: str) -> dict[str, Any]:
    freeze = read_json(repo / freeze_rel)
    require(freeze["artifact_id"] == "P2-I2-I09A-CONTROL-RESOLUTION-INPUT-FREEZE", "I09A freeze identity drift")
    require(freeze["iteration_id"] == "P2-I2-I09A", "I09A iteration drift")
    for item in freeze["input_artifacts"]:
        require(not Path(item["path"]).is_absolute(), f"absolute input path: {item['role']}")
        require(sha256(repo / item["path"]) == item["sha256"], f"input identity drift: {item['role']}")
    builder = freeze["authorized_builder"]
    require(builder["path"] == SCRIPT_REL, "authorized builder path drift")
    require(sha256(repo / builder["path"]) == builder["sha256"], "authorized builder hash drift")
    require(
        freeze["authorized_commands"] == [
            [".venv/bin/python", "-B", SCRIPT_REL, "build"],
            [".venv/bin/python", "-B", SCRIPT_REL, "validate"],
        ],
        "authorized command drift",
    )
    return freeze


def make_envelope(
    analysis: Any,
    *,
    mode: str,
    order: str,
    seed: int,
    suffix: str,
    branch: str,
    value: float,
) -> dict[str, Any]:
    record_id = f"I09A-retained-primary:{mode}:{order}:{seed}:{suffix}"
    pairing = f"I09A-retained-primary:{mode}:{order}:{seed}"
    carrier_digest = hashlib.sha256(f"{pairing}:{suffix}".encode("utf-8")).hexdigest()
    envelope = analysis.build_synthetic_response_envelope(
        record_id=record_id,
        branch_id=branch,
        response=max(value, 1e-15),
        seed=seed,
        physical_order_id=order,
        carrier_state_digest=carrier_digest,
        pairing_identity=pairing,
    )
    record = envelope["i04r1_response_record"]
    record["mode"] = mode
    if value == 0.0:
        record["status"] = "scientific_no_response"
        record["B_after"] = 0.0
        record["raw_response"] = 0.0
        record["oriented_response"] = 0.0
        record["response_packet_amount"] = None
        record["producer_reason"] = "scientific_zero"
        record["response_packet_id"] = None
        record["departure_event_id"] = None
        record["arrival_event_id"] = None
        record["B_targeting_event_ids"] = []
        record["native_chain_evidence_refs"] = []
        record["step_processed_event_kinds"] = ["event_queue_empty", "event_queue_empty"]
        envelope["window_validity_receipt"]["step_processed_event_ids"] = [None, None]
        envelope["arrival_gain_receipt"]["expected_native_arrival_gain"] = 0.0
        envelope["arrival_gain_receipt"]["arrival_transform_id"] = "no_arrival"
    return envelope


def corrected_primary_estimates(
    analysis: Any,
    by_ref: dict[str, dict[str, Any]],
    original: Any,
    machine_policy: dict[str, Any],
    parent_policy: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for mode in MODES:
        rows: list[dict[str, Any]] = []
        for order in ORDERS:
            candidate_ref = original._branch_ref(mode, "combined-orders", "combined-orders", order)
            q1_ref = original._branch_ref(mode, "contributor-removal", "q1_admitted_q2_diverted", order)
            q2_ref = original._branch_ref(mode, "contributor-removal", "q2_admitted_q1_diverted", order)
            for seed in SEEDS:
                candidate = original._values(by_ref, candidate_ref)[seed]
                q1_only = original._values(by_ref, q1_ref)[seed]
                q2_only = original._values(by_ref, q2_ref)[seed]
                envelopes = (
                    make_envelope(analysis, mode=mode, order=order, seed=seed, suffix="candidate", branch="combined-orders", value=candidate),
                    make_envelope(analysis, mode=mode, order=order, seed=seed, suffix="q1-only", branch="q1_admitted_q2_diverted", value=q1_only),
                    make_envelope(analysis, mode=mode, order=order, seed=seed, suffix="q2-only", branch="q2_admitted_q1_diverted", value=q2_only),
                )
                estimate = analysis.primary_margin(*envelopes, machine_policy, parent_policy)
                require(estimate["complete_three_arm_tuple_valid"] is True, "incomplete I09A estimator tuple")
                require(estimate["evaluable"] is True, "nonevaluable I09A estimator tuple")
                strongest = max(q1_only, q2_only)
                rows.append({
                    "physical_order_id": order,
                    "seed": seed,
                    "candidate_response": candidate,
                    "q1_only_response": q1_only,
                    "q2_only_response": q2_only,
                    "strongest_leave_one_response": strongest,
                    "strongest_leave_one_provenance": "q1-only" if q1_only >= q2_only else "q2-only",
                    "primary_margin": float(estimate["normalized_margin"]),
                })
        result[mode] = rows
    return result


def build_corrected_index(repo: Path, freeze: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    scripts = repo / EXPERIMENT / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    import p2_i2_i04r2_analysis as analysis
    import p2_i2_i09_control_resolution as original

    historical, historical_context = original.build_index(repo, I09_FREEZE_REL)
    historical_validation = original.build_validation(historical, historical_context)
    historical_report = original.build_report(historical, historical_validation)
    require(json_bytes(historical) == (repo / I09_INDEX_REL).read_bytes(), "accepted I09 index reconstruction drift")
    require(json_bytes(historical_validation) == (repo / I09_VALIDATION_REL).read_bytes(), "accepted I09 validation reconstruction drift")
    require(historical_report == (repo / I09_REPORT_REL).read_text(encoding="utf-8"), "accepted I09 report reconstruction drift")

    original_freeze, inputs = original._load_inputs(repo, I09_FREEZE_REL)
    policy = inputs["analysis_policy"]["payload"]
    registration = inputs["exact_registration"]["payload"]
    template = inputs["lane_control_template"]["payload"]
    matrix = inputs["run_matrix"]["payload"]
    manifest = inputs["execution_manifest"]["payload"]
    c01_audit = inputs["c01_bounded_incomplete_audit"]["payload"]
    fail_effects = original._parse_program_fail_effects(inputs["program_control_register"]["payload"])
    branch_index, by_ref, loaded = original._load_observations(repo, matrix, manifest)
    comparisons = [
        item
        for mode in MODES
        for item in (original._common_comparison_rules(mode, by_ref, policy) + original._mode_comparison_rules(mode, by_ref, policy))
    ]
    machine_policy = read_json(repo / MACHINE_POLICY_REL)
    parent_policy = read_json(repo / PARENT_POLICY_REL)
    corrected = corrected_primary_estimates(analysis, by_ref, original, machine_policy, parent_policy)
    for comparison in comparisons:
        if comparison["control_id"] == "symmetric_leave_one_common_carrier_admission":
            comparison["observed_relation"]["complete_three_envelope_estimates"] = corrected[comparison["mode"]]
            comparison["observed_relation"]["estimator_path_id"] = "p2-i2-i04r2-exact-three-arm-primary-estimator-v1"

    lane_controls = original._lane_controls(original_freeze, template, comparisons)
    predicates = original._program_predicates(
        registration,
        manifest,
        branch_index,
        comparisons,
        loaded["outputs"],
        c01_audit,
    )
    program_controls = original._program_controls(original_freeze, fail_effects, predicates)
    comparison_counts = Counter(item["observed_disposition"] for item in comparisons)
    lane_counts = Counter(item["observed_disposition"] for item in lane_controls)
    program_counts = Counter(
        result["observed_disposition"]
        for item in program_controls
        for result in item["mode_results"]
    )

    index = copy.deepcopy(historical)
    index.update({
        "artifact_id": "P2-I2-I09A-CONTROL-RESOLUTION-INDEX",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I09A",
        "status": "review_ready_corrected_control_projection",
        "source_input_freeze": FREEZE_REL,
        "source_input_freeze_sha256": sha256(repo / FREEZE_REL),
        "builder_identity": copy.deepcopy(freeze["authorized_builder"]),
        "input_identity_count": len(freeze["input_artifacts"]),
        "accepted_i09_historical_authority": {
            "commit": freeze["accepted_authority"]["i09_commit"],
            "index_path": I09_INDEX_REL,
            "index_sha256": sha256(repo / I09_INDEX_REL),
            "reconstructed_byte_identically_before_correction": True,
        },
        "program_common_controls": program_controls,
        "comparison_rules": comparisons,
        "lane_controls": lane_controls,
        "observed_branch_index": original._compact_branch_index(branch_index),
    })
    margins = [
        row["primary_margin"]
        for rows in corrected.values()
        for row in rows
    ]
    index["summary"] = {
        "program_common_control_count": len(program_controls),
        "program_common_mode_dispositions": dict(sorted(program_counts.items())),
        "comparison_rule_count": len(comparisons),
        "comparison_rule_dispositions": dict(sorted(comparison_counts.items())),
        "lane_control_count": len(lane_controls),
        "lane_control_dispositions": dict(sorted(lane_counts.items())),
        "observed_branch_configuration_count": len(branch_index),
        "matrix_entry_count": len(matrix["entries"]),
        "seed_varying_branch_configuration_count": sum(not item["seed_invariant"] for item in branch_index),
        "normalized_primary_estimate_count": len(margins),
        "normalized_primary_margin_distribution": {"0.0": margins.count(0.0), "1.0": margins.count(1.0)},
        "estimator_invocation_count": len(margins),
        "CONTROL_GATE_candidate": all(item["observed_disposition"] in {"pass", "not_applicable"} for item in lane_controls)
        and all(result["observed_disposition"] in {"pass", "not_applicable"} for item in program_controls for result in item["mode_results"]),
    }
    index["correction_boundary"] = copy.deepcopy(freeze["correction_boundary"])
    index["canonical_payload_digest"] = canonical_digest(index)
    return index, {
        "freeze": freeze,
        "historical": historical,
        "historical_validation": historical_validation,
        "historical_report": historical_report,
        "corrected": corrected,
    }


def build_validation(repo: Path, index: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, claim: str, passed: bool, observed: Any) -> None:
        checks.append({"check_id": check_id, "claim": claim, "passed": bool(passed), "observed": observed})

    historical = context["historical"]
    historical_primary = {
        item["mode"]: item["observed_relation"]["complete_three_envelope_estimates"]
        for item in historical["comparison_rules"]
        if item["control_id"] == "symmetric_leave_one_common_carrier_admission"
    }
    corrected_primary = {
        item["mode"]: item["observed_relation"]["complete_three_envelope_estimates"]
        for item in index["comparison_rules"]
        if item["control_id"] == "symmetric_leave_one_common_carrier_admission"
    }
    raw_keys = (
        "candidate_response",
        "q1_only_response",
        "q2_only_response",
        "strongest_leave_one_response",
        "strongest_leave_one_provenance",
        "physical_order_id",
        "seed",
    )
    raw_unchanged = all(
        [{key: row[key] for key in raw_keys} for row in historical_primary[mode]]
        == [{key: row[key] for key in raw_keys} for row in corrected_primary[mode]]
        for mode in MODES
    )
    primary_rules = [item for item in index["comparison_rules"] if item["control_id"] == "symmetric_leave_one_common_carrier_admission"]
    margins = [row["primary_margin"] for item in primary_rules for row in item["observed_relation"]["complete_three_envelope_estimates"]]
    accepted_roles = {item["role"]: item for item in context["freeze"]["input_artifacts"] if item["role"].startswith("accepted_i09_")}
    absolute_values = sorted({value for value in strings(index) if value.startswith("/")})

    check("I09A-01", "all frozen input identities are exact", index["input_identity_count"] == len(context["freeze"]["input_artifacts"]), index["input_identity_count"])
    check("I09A-02", "the authorized builder identity is exact", index["builder_identity"] == context["freeze"]["authorized_builder"], index["builder_identity"])
    check("I09A-03", "accepted I09 index reconstructs byte-identically before correction", json_bytes(historical) == (repo / I09_INDEX_REL).read_bytes(), True)
    check("I09A-04", "accepted I09 validation reconstructs byte-identically before correction", json_bytes(context["historical_validation"]) == (repo / I09_VALIDATION_REL).read_bytes(), True)
    check("I09A-05", "accepted I09 report reconstructs byte-identically before correction", context["historical_report"] == (repo / I09_REPORT_REL).read_text(encoding="utf-8"), True)
    check("I09A-06", "all accepted I09 artifacts retain their frozen hashes", all(sha256(repo / item["path"]) == item["sha256"] for item in accepted_roles.values()), sorted(accepted_roles))
    check("I09A-07", "all eighteen retained primary tuples are represented", len(margins) == 18, len(margins))
    check("I09A-08", "every tuple records the accepted exact three-arm estimator path", all(item["observed_relation"].get("estimator_path_id") == "p2-i2-i04r2-exact-three-arm-primary-estimator-v1" for item in primary_rules), len(primary_rules))
    check("I09A-09", "twelve positive margins normalize to one and six remain zero", Counter(margins) == Counter({1.0: 12, 0.0: 6}), dict(sorted(Counter(margins).items())))
    check("I09A-10", "retained raw responses and tie provenance are unchanged", raw_unchanged, raw_unchanged)
    check("I09A-11", "all 38 comparison rules are recomputed and pass", index["summary"]["comparison_rule_dispositions"] == {"pass": 38}, index["summary"]["comparison_rule_dispositions"])
    check("I09A-12", "all 15 lane controls are recomputed and pass", index["summary"]["lane_control_dispositions"] == {"pass": 15}, index["summary"]["lane_control_dispositions"])
    check("I09A-13", "all 57 program-mode dispositions are recomputed", sum(len(item["mode_results"]) for item in index["program_common_controls"]) == 57, sum(len(item["mode_results"]) for item in index["program_common_controls"]))
    check("I09A-14", "program-mode dispositions remain 56 pass and one not-applicable", index["summary"]["program_common_mode_dispositions"] == {"not_applicable": 1, "pass": 56}, index["summary"]["program_common_mode_dispositions"])
    check("I09A-15", "no matched branch configuration varies by seed", index["summary"]["seed_varying_branch_configuration_count"] == 0, index["summary"]["seed_varying_branch_configuration_count"])
    check("I09A-16", "the corrected projection remains a CONTROL-GATE candidate", index["summary"]["CONTROL_GATE_candidate"] is True, index["summary"]["CONTROL_GATE_candidate"])
    check("I09A-17", "the calibration delta remains exactly 1e-12", read_json(repo / CALIBRATION_REL)["record"]["delta"] == 1e-12, read_json(repo / CALIBRATION_REL)["record"]["delta"])
    check("I09A-18", "the projection assigns no R01-R05 or terminal result", index["interpretation_boundary"]["R01_through_R05"] == "unassigned_until_I11" and index["interpretation_boundary"]["terminal_classification"] is None, index["interpretation_boundary"])
    check("I09A-19", "the projection creates no new evidence or schema authority", index["projection_only"] is True and index["introduces_evidence_or_schema_authority"] is False, {"projection_only": index["projection_only"], "schema_authority": index["introduces_evidence_or_schema_authority"]})
    check("I09A-20", "the correction boundary records zero runtime operations", all(index["correction_boundary"][key] == 0 for key in ("pygrc_imports", "model_or_adapter_constructions", "candidate_or_control_invocations", "matrix_entry_regenerations", "scientific_runtime_invocations")), index["correction_boundary"])
    check("I09A-21", "the corrected index contains no absolute paths", not absolute_values, absolute_values)
    check("I09A-22", "the corrected index canonical digest reconstructs exactly", index["canonical_payload_digest"] == canonical_digest(index), index["canonical_payload_digest"])
    check("I09A-23", "the accepted I09 authority is retained as immutable history", index["accepted_i09_historical_authority"]["reconstructed_byte_identically_before_correction"] is True, index["accepted_i09_historical_authority"])
    check("I09A-24", "no corrected output shadows an input path", not ({INDEX_REL, VALIDATION_REL, REPORT_REL} & {item["path"] for item in context["freeze"]["input_artifacts"]}), [INDEX_REL, VALIDATION_REL, REPORT_REL])

    passed = sum(item["passed"] for item in checks)
    validation: dict[str, Any] = {
        "artifact_id": "P2-I2-I09A-CONTROL-RESOLUTION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I09A",
        "status": "passed" if passed == len(checks) else "failed_closed",
        "checks": checks,
        "passed_check_count": passed,
        "check_count": len(checks),
        "blocker_count": len(checks) - passed,
        "estimator_invocation_count": 18,
        "candidate_or_control_invocations": 0,
        "matrix_entry_regenerations": 0,
        "pygrc_imports": 0,
        "scientific_interpretation": False,
        "CONTROL_GATE": "review_ready_pending_owner_acceptance" if passed == len(checks) else "closed",
        "I10_retry_authorized": False,
    }
    validation["canonical_payload_digest"] = canonical_digest(validation)
    return validation


def build_report(index: dict[str, Any], validation: dict[str, Any]) -> str:
    mode_rows = []
    for mode in MODES:
        rule = next(item for item in index["comparison_rules"] if item["mode"] == mode and item["control_id"] == "symmetric_leave_one_common_carrier_admission")
        by_order = {
            order: sorted({row["primary_margin"] for row in rule["observed_relation"]["complete_three_envelope_estimates"] if row["physical_order_id"] == order})
            for order in ORDERS
        }
        mode_rows.append(f"| `{mode}` | `{by_order['q1_then_q2'][0]}` | `{by_order['q2_then_q1'][0]}` | `pass` |")
    return "\n".join([
        "# P2-I2-I09A Normalized-Estimator Correction",
        "",
        "**Status:** review-ready; owner acceptance, commit, CONTROL-GATE reconciliation, and I10 resumption pending",
        "",
        "**Evidence effect:** corrected derived control projection over retained I08 evidence only",
        "",
        "## Result",
        "",
        f"I09A passes {validation['passed_check_count']}/{validation['check_count']} deterministic checks with {validation['blocker_count']} blockers. Before correction it reconstructs the accepted I09 index, validation, and report byte-identically. It then routes all 18 retained mode/order/seed tuples through `p2_i2_i04r2_analysis.primary_margin`.",
        "",
        "The retained raw responses do not change: candidate and leave-one values remain `0.125` or `0.0`, and exact comparator ties retain deterministic `q1-only` provenance without scientific meaning. The corrected normalized margins are twelve `1.0` values and six `0.0` values:",
        "",
        "| Mode | q1 then q2 | q2 then q1 | Comparison disposition |",
        "| --- | ---: | ---: | --- |",
        *mode_rows,
        "",
        "All dependent layers were rebuilt after the correction. The outcome remains 38/38 comparison-rule passes, 15/15 mode-local L02 control passes, and 56 program-mode passes plus one explicit not-applicable state-carried `AE01-CTRL-16`. Thus the defect changes the numeric normalized-margin projection and its prose, but no control disposition.",
        "",
        "## Boundary",
        "",
        "Accepted I09 remains immutable historical authority. I09A imports no PyGRC, constructs no model or adapter, runs no candidate/control branch, regenerates no matrix entry, introduces no scientific input, and assigns no `R01`–`R05`, support status, mode ranking, or terminal class. CONTROL-GATE remains reopened pending explicit owner acceptance; this package does not authorize commit or resume I10.",
        "",
    ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "validate"))
    parser.add_argument("--freeze", default=FREEZE_REL)
    parser.add_argument("--index", default=INDEX_REL)
    parser.add_argument("--validation", default=VALIDATION_REL)
    parser.add_argument("--report", default=REPORT_REL)
    args = parser.parse_args()
    repo = Path.cwd().resolve()
    require((repo / ".git").exists(), "run from repository root")
    verify_runtime(repo)
    freeze = load_freeze(repo, args.freeze)
    index, context = build_corrected_index(repo, freeze)
    validation = build_validation(repo, index, context)
    report = build_report(index, validation)
    if args.command == "build":
        (repo / args.index).write_bytes(json_bytes(index))
        (repo / args.validation).write_bytes(json_bytes(validation))
        (repo / args.report).write_text(report, encoding="utf-8")
    else:
        require((repo / args.index).read_bytes() == json_bytes(index), "retained I09A index is not byte-identical")
        require((repo / args.validation).read_bytes() == json_bytes(validation), "retained I09A validation is not byte-identical")
        require((repo / args.report).read_text(encoding="utf-8") == report, "retained I09A report is not byte-identical")
    print(json.dumps({
        "status": validation["status"],
        "checks": f"{validation['passed_check_count']}/{validation['check_count']}",
        "blockers": validation["blocker_count"],
        "estimator_invocations": validation["estimator_invocation_count"],
        "CONTROL_GATE": validation["CONTROL_GATE"],
        "I10_retry_authorized": validation["I10_retry_authorized"],
    }, sort_keys=True))
    return 0 if validation["blocker_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
