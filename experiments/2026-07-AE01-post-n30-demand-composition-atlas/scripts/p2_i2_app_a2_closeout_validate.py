#!/usr/bin/env python3
"""Read-only retained-output validation for P2-I2 APP-A2 closeout."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
PREFIX = "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
ACTIVATION_COMMIT = "e61daccd9258d5511394112b2be7fb5ece310852"
EXPECTED_DIRTY_PATHS = {
    PREFIX + "contracts/p2-i2/app-a2-runtime-evidence.json",
    PREFIX + "contracts/p2-i2/app-a2-reconstruction-and-closeout.json",
    PREFIX + "scripts/p2_i2_app_a2_closeout_validate.py",
}


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path.name}")
    return value


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.rstrip()


def validate_digest(value: dict[str, Any], key: str) -> bool:
    unsigned = dict(value)
    observed = unsigned.pop(key)
    return digest_value(unsigned) == observed


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def add(self, check_id: str, passed: bool, observed: Any = None) -> None:
        self.rows.append(
            {"check_id": check_id, "passed": bool(passed), "observed": observed}
        )


def validate(aggregate_path: Path, closeout_path: Path) -> dict[str, Any]:
    checks = Checks()
    aggregate = load_json(aggregate_path)
    closeout = load_json(closeout_path)

    checks.add("rcae.activation_commit", git("rev-parse", "HEAD") == ACTIVATION_COMMIT, git("rev-parse", "HEAD"))
    status_rows = [row for row in git("status", "--short").splitlines() if row]
    dirty_paths = {row[3:] for row in status_rows}
    checks.add("rcae.exact_closeout_dirty_scope", dirty_paths == EXPECTED_DIRTY_PATHS, sorted(dirty_paths))

    checks.add("aggregate.artifact", aggregate.get("artifact_id") == "p2_i2_app_a2_runtime_evidence", aggregate.get("artifact_id"))
    checks.add("aggregate.status", aggregate.get("status") == "complete", aggregate.get("status"))
    checks.add("aggregate.digest", validate_digest(aggregate, "output_digest"), aggregate.get("output_digest"))
    checks.add("aggregate.activation_commit", aggregate["authority"]["activation_commit"] == ACTIVATION_COMMIT, aggregate["authority"]["activation_commit"])
    checks.add("aggregate.attempt_consumed", aggregate["attempt_consumed"] is True, aggregate["attempt_consumed"])

    campaign = aggregate["campaign_receipt"]
    checks.add("campaign.one_invocation", campaign["campaign_invocations"] == 1, campaign["campaign_invocations"])
    checks.add("campaign.zero_retry", campaign["campaign_retries"] == 0 and campaign["child_arm_retries"] == 0, [campaign["campaign_retries"], campaign["child_arm_retries"]])
    checks.add("campaign.nineteen_starts", campaign["child_arm_starts"] == 19 and len(campaign["child_invocations"]) == 19, campaign["child_arm_starts"])
    checks.add("campaign.fresh_processes", campaign["fresh_process_per_arm"] is True and all(row["fresh_process_started"] is True for row in campaign["child_invocations"]), campaign["fresh_process_per_arm"])
    checks.add("campaign.all_receipts_accepted", all(row.get("receipt_accepted") is True and row.get("exit_code") == 0 and row.get("stderr_empty") is True and row.get("timed_out") is False for row in campaign["child_invocations"]), None)
    checks.add("campaign.no_per_arm_files", campaign["per_arm_persisted_files"] == 0 and campaign["single_aggregate_output"] is True, [campaign["per_arm_persisted_files"], campaign["single_aggregate_output"]])

    receipts = aggregate["arm_receipts"]
    checks.add("receipts.nineteen", len(receipts) == 19, len(receipts))
    checks.add("receipts.unique", len({row["arm_id"] for row in receipts}) == 19, [row["arm_id"] for row in receipts])
    checks.add("receipts.digest", all(validate_digest(dict(row), "arm_receipt_digest") for row in receipts), None)
    checks.add("receipts.fresh_model", all(row["baseline"]["fresh_model"] is True and row["process_receipt"]["fresh_child_process"] is True for row in receipts), None)
    checks.add("receipts.resource_bounds", all(row["resource_receipt"]["node_count"] == 12 and row["resource_receipt"]["edge_count"] == 28 and row["resource_receipt"]["packet_events"] <= 32 and row["resource_receipt"]["maximum_queue_length"] <= 4 for row in receipts), None)

    analysis = aggregate["analysis"]
    checks.add("analysis.digest", validate_digest(analysis, "analysis_digest"), analysis.get("analysis_digest"))
    checks.add("analysis.complete", analysis["matrix_complete"] is True and analysis["arm_count_observed"] == analysis["arm_count_expected"] == 19, [analysis["arm_count_observed"], analysis["arm_count_expected"]])
    checks.add("analysis.operational_validity", analysis["all_arms_operationally_valid"] is True and all(row["valid"] is True and not row["failed_predicates"] for row in analysis["operational_validity"].values()), None)
    checks.add("analysis.signatures", analysis["all_gate_signatures_derived"] is True and len(analysis["gate_signatures"]) == 19, len(analysis["gate_signatures"]))
    checks.add("analysis.proper_subsets", all(analysis["proper_subset_failures"].values()) and set(analysis["proper_subset_failures"]) == {"reference", "G", "E", "P", "GE", "GP", "EP"}, analysis["proper_subset_failures"])
    checks.add("analysis.primary", analysis["primary_relation_passed"] is True, analysis["primary_relation_passed"])
    checks.add("analysis.operation_causality", all(row["causal_requirement_passed"] is True and row["direct_response_changed"] is True and row["mediator_intervention_changed_response"] is True for row in analysis["operation_causality"].values()), analysis["operation_causality"])
    checks.add("analysis.clamp", analysis["carrier_clamp_changed_response"] is True, analysis["carrier_clamp_changed_response"])
    checks.add("analysis.causal", analysis["causal_relation_passed"] is True, analysis["causal_relation_passed"])

    fixture_path = ROOT / PREFIX / "contracts/p2-i2/app-a1-fixture-control-conformance-freeze.json"
    fixture = load_json(fixture_path)
    gates = fixture["measurement_authority"]["gates"]
    signature = analysis["gate_signatures"]["GEP"]
    measured = signature["measured_gates"]
    tolerance = float(fixture["measurement_authority"]["runtime_tolerance"])
    checks.add("gates.configuration", signature["configuration_condition_passed"] is True and math.isclose(signature["configuration_retention_fraction"], fixture["measurement_authority"]["retention_fraction"], rel_tol=0.0, abs_tol=tolerance), signature["configuration_retention_fraction"])
    checks.add("gates.environment", measured["environment_feedback"]["passed"] is True and measured["environment_feedback"]["value"] + tolerance >= gates["environment_feedback"]["threshold"], measured["environment_feedback"]["value"])
    checks.add("gates.support", measured["support_feedback"]["passed"] is True and measured["support_feedback"]["value"] + tolerance >= gates["support_feedback"]["threshold"], measured["support_feedback"]["value"])
    checks.add("gates.phase", measured["phase_residual"]["passed"] is True and measured["phase_residual"]["value"] <= gates["phase_residual"]["threshold"] + tolerance, measured["phase_residual"]["value"])
    checks.add("gates.leakage", measured["registered_route_merge_leakage"]["passed"] is True and measured["registered_route_merge_leakage"]["value"] <= gates["registered_route_merge_leakage"]["threshold"] + tolerance, measured["registered_route_merge_leakage"]["value"])

    controls = analysis["controls"]
    checks.add("controls.one_source", controls["one_source_reproduces"] is True, controls["one_source_reproduces"])
    checks.add("controls.rotation", controls["cyclic_role_rotation_reproduces"] is True, controls["cyclic_role_rotation_reproduces"])
    checks.add("controls.label", controls["label_permutation_invariant"] is True, controls["label_permutation_invariant"])
    checks.add("controls.orders", all(controls["order_inversion_gate_passes"].values()) and controls["order_resolution"] == "tested_adjacent_inversions_do_not_make_order_load_bearing", controls["order_inversion_gate_passes"])
    checks.add("controls.private_and_carrier", controls["reference_all_diverted"] is True and controls["response_sources_carrier_only"] is True, controls)

    checks.add("closeout.artifact", closeout.get("artifact_id") == "p2_i2_app_a2_reconstruction_and_closeout", closeout.get("artifact_id"))
    checks.add("closeout.status", closeout.get("status") == "complete", closeout.get("status"))
    checks.add("closeout.digest", validate_digest(closeout, "output_digest"), closeout.get("output_digest"))
    checks.add("closeout.aggregate_hash", closeout["source"]["aggregate_sha256"] == sha256_file(aggregate_path), closeout["source"]["aggregate_sha256"])
    checks.add("closeout.analysis_byte_equal", canonical_bytes(closeout["analysis"]) == canonical_bytes(analysis) and closeout["reconstruction_receipt"]["analysis_byte_identical"] is True, closeout["reconstruction_receipt"]["analysis_byte_identical"])
    reconstruction = closeout["reconstruction_receipt"]
    checks.add("closeout.read_once", reconstruction["retained_aggregate_reads"] == 1, reconstruction["retained_aggregate_reads"])
    checks.add("closeout.zero_regeneration", all(reconstruction[key] == 0 for key in ("pygrc_imports", "model_invocations", "child_process_invocations", "producer_invocations", "scientific_regeneration_invocations")), reconstruction)
    checks.add("closeout.terminal", closeout["terminal_classification"] == analysis["terminal_classification"] == "supported_bounded_candidate", closeout["terminal_classification"])
    checks.add("closeout.claim", closeout["bounded_claim"] == "bounded generator-extractor-redistributor shared-carrier composition candidate", closeout["bounded_claim"])
    checks.add("closeout.plurality", closeout["plurality_resolution"] == "physical_participant_plurality_non_load_bearing_in_frozen_fixture", closeout["plurality_resolution"])
    checks.add("closeout.order", closeout["order_resolution"] == "tested_adjacent_inversions_do_not_make_order_load_bearing", closeout["order_resolution"])
    checks.add("closeout.main_unchanged", closeout["claim_scope"]["main_p2_i2_terminal_changed"] is False, closeout["claim_scope"])
    checks.add("closeout.blocked_claims", set(closeout["blocked_claims"]) == {"coalition", "functional cooperation", "coordination", "resource economy", "agency", "collective identity", "ecology motif or regime", "cross-lane recurrence", "N31+ selection"}, closeout["blocked_claims"])

    serialized = json.dumps({"aggregate": aggregate, "closeout": closeout}, sort_keys=True)
    checks.add("portability.no_absolute_paths", "/home/" not in serialized and "/Users/" not in serialized, None)
    checks.add("validator.repository_venv", Path(sys.executable).resolve() == (ROOT / ".venv" / "bin" / "python").resolve(), ".venv/bin/python")
    source = Path(__file__).read_text(encoding="utf-8")
    import_token = "import " + "pygrc"
    from_token = "from " + "pygrc"
    checks.add("validator.no_pygrc", import_token not in source and from_token not in source, None)

    failed = [row["check_id"] for row in checks.rows if not row["passed"]]
    result: dict[str, Any] = {
        "artifact_id": "p2_i2_app_a2_closeout_validation",
        "artifact_version": "1.0",
        "experiment_id": "2026-07-AE01",
        "iteration_id": "P2-I2-APP-A2",
        "generated_at": closeout["generated_at"],
        "status": "passed" if not failed else "failed",
        "sources": {
            "aggregate": {"path": str(aggregate_path.relative_to(ROOT)), "sha256": sha256_file(aggregate_path)},
            "closeout": {"path": str(closeout_path.relative_to(ROOT)), "sha256": sha256_file(closeout_path)}
        },
        "validator": {"path": PREFIX + "scripts/p2_i2_app_a2_closeout_validate.py", "sha256": sha256_file(Path(__file__))},
        "checks": checks.rows,
        "checks_passed": len(checks.rows) - len(failed),
        "checks_total": len(checks.rows),
        "failed_checks": failed,
        "validation_execution": {
            "retained_aggregate_reads": 1,
            "retained_closeout_reads": 1,
            "pygrc_imports": 0,
            "model_invocations": 0,
            "child_arm_invocations": 0,
            "producer_invocations": 0,
            "scientific_regeneration_invocations": 0
        },
        "terminal_classification": closeout["terminal_classification"],
        "bounded_claim": closeout["bounded_claim"],
        "authority_effect": "Read-only result validation; owner result acceptance and commit remain pending."
    }
    result["output_digest"] = digest_value(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregate", required=True)
    parser.add_argument("--closeout", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    raw_paths = [args.aggregate, args.closeout] + ([] if args.output is None else [args.output])
    if any(Path(value).is_absolute() for value in raw_paths):
        raise AssertionError("all paths must be relative")
    aggregate_path = (ROOT / args.aggregate).resolve()
    closeout_path = (ROOT / args.closeout).resolve()
    result = validate(aggregate_path, closeout_path)
    if args.output:
        output_path = (ROOT / args.output).resolve()
        if output_path.exists():
            raise AssertionError("validation output already exists")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(output_path, flags, 0o644)
        try:
            data = canonical_bytes(result)
            written = 0
            while written < len(data):
                written += os.write(fd, data[written:])
            os.fsync(fd)
        finally:
            os.close(fd)
    print(json.dumps({"status": result["status"], "checks_passed": result["checks_passed"], "checks_total": result["checks_total"], "terminal_classification": result["terminal_classification"], "output_digest": result["output_digest"]}, sort_keys=True))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
