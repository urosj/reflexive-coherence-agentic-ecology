#!/usr/bin/env python3
"""Validate the complete APP-A1 package without importing PyGRC or running models."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments" / "2026-07-AE01-post-n30-demand-composition-atlas"
CONTRACTS = EXPERIMENT / "contracts" / "p2-i2"
GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"


def load(name: str) -> dict[str, Any]:
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def contains_machine_path(value: Any) -> bool:
    text = json.dumps(value, sort_keys=True, ensure_ascii=True)
    return "/" + "home" + "/" in text or "Documents" + "/" + "RC-github" in text


def main() -> int:
    audit = load("app-a1-source-delta-audit.json")
    proposal = load("app-a1-gate-authority-proposal.json")
    acceptance = load("app-a1-gate-authority-acceptance.json")
    base = load("app-a1-fixture-control-conformance-freeze.json")
    base_validation = load("app-a1-freeze-validation.json")
    failed = load("app-a1-conformance-failed-start-001.json")
    correction_auth = load("app-a1-conformance-correction-authorization.json")
    correction_freeze = load("app-a1-conformance-correction-freeze.json")
    correction_validation = load("app-a1-conformance-correction-freeze-validation.json")
    runtime = load("app-a1-runtime-conformance.json")
    run_receipt = load("app-a1-conformance-run-receipt.json")
    execution = load("app-a1-app-a2-execution-freeze.json")
    report_path = EXPERIMENT / "reports" / "P2-I2-APP-A1-source-delta-and-gate-authority-review.md"

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed)})

    check("graph_head", git("rev-parse", "HEAD", cwd=GRAPH_ROOT) == execution["authority"]["graph_commit"])
    check("graph_clean", git("status", "--short", cwd=GRAPH_ROOT) == "")
    check("rcae_entry_head", git("rev-parse", "HEAD", cwd=ROOT) == audit["entry_identities"]["rcae"]["commit"])
    check("report_exists", report_path.is_file())
    check("audit_transport_failed", audit["transportability_audit"]["transportability_gate_passed"] is False)
    check("n29_not_authoritative", audit["transportability_audit"]["n29_numeric_gates_authoritative_for_app_a"] is False)
    check("native_realization", all(row["classification"] == "native_adequate" for row in audit["realization_selection_after_audit"]["operations"]))
    check("no_load_bearing_producer", audit["realization_selection_after_audit"]["load_bearing_external_producer_required"] is False)
    check("proposal_hash_accepted", acceptance["accepted_authority"]["sha256"] == sha256_file(CONTRACTS / "app-a1-gate-authority-proposal.json"))
    check("proposal_domain", proposal["proposed_measurement_domain"]["domain_id"] == base["measurement_authority"]["domain_id"])
    check("base_static_validation", base_validation["status"] == "passed_before_any_model_construction" and base_validation["checks_passed"] == base_validation["checks_total"] == 48)
    check("base_preceded_models", base["status"] == "frozen_before_any_model_construction")

    check("failed_start_consumed", failed["attempt"]["evidence_invocations_consumed"] == 1)
    check("failed_start_no_output", failed["attempt"]["governed_output_written"] is False)
    check("failed_start_not_scientific", failed["quarantine"]["app_a2_arms_executed"] == 0)
    check("correction_same_iteration", correction_auth["allowed_scope"]["same_iteration"] is True and correction_auth["allowed_scope"]["new_iteration_or_suffix"] is False)
    check("correction_counts", correction_auth["allowed_scope"]["replacement_evidence_invocations"] == 1 and correction_auth["allowed_scope"]["replacement_reconstruction_invocations"] == 1 and correction_auth["allowed_scope"]["replacement_retry_limit"] == 0)
    check("correction_static_validation", correction_validation["status"] == "passed" and correction_validation["result"]["checks_passed"] == correction_validation["result"]["checks_total"] == 60)
    check("correction_static_zero_models", correction_validation["result"]["models_constructed"] == 0 and correction_validation["result"]["pygrc_imports"] == 0)
    check("base_freeze_immutable", correction_freeze["base_freeze"]["sha256"] == sha256_file(CONTRACTS / "app-a1-fixture-control-conformance-freeze.json"))

    bound_hashes = all(
        (ROOT / row["path"]).is_file()
        and sha256_file(ROOT / row["path"]) == row["sha256"]
        for row in execution["bound_inputs"]
    )
    check("execution_bound_hashes", bound_hashes)
    check("execution_inactive", execution["authority"]["app_a2_authorized"] is False and execution["authority"]["scientific_runtime_authorized"] is False)
    check("execution_commit_closed", execution["authority"]["commit_authorized"] is False and execution["authority"]["app_a1_acceptance_granted"] is False)
    check("arm_count", execution["campaign_policy"]["arm_count"] == len(base["arm_registry"]) == 19)
    check("arm_order", execution["frozen_registry_import"]["arm_order"] == [row["arm_id"] for row in base["arm_registry"]])
    check("fresh_process_model", execution["entry_isolation"]["fresh_supervised_child_process_per_arm"] is True and execution["entry_isolation"]["fresh_model_and_registered_baseline_per_arm"] is True)
    check("cross_arm_reads_closed", execution["entry_isolation"]["earlier_outcome_reads"] is False and execution["entry_isolation"]["cross_arm_mutable_state"] is False)
    check("one_aggregate", execution["campaign_policy"]["per_arm_narrative_or_output_files"] is False)
    check("zero_retry", execution["campaign_policy"]["campaign_retry_limit"] == 0 and execution["campaign_policy"]["arm_retry_limit"] == 0)
    check("future_outputs_absent", not (ROOT / execution["campaign_policy"]["single_aggregate_persisted_output"]).exists() and not (ROOT / execution["campaign_policy"]["read_only_reconstruction_output"]).exists())
    check("app_a2_counts_zero", all(value == 0 for value in execution["current_counts"].values()))

    vectors = base["scientific_fixture"]["operation_vectors"]
    initial = base["scientific_fixture"]["initial_coherence"]
    expected_gep = {
        "environment": initial["c_environment"] + vectors["G"]["environment"] - vectors["E"]["environment"] + vectors["P"]["environment"],
        "support": initial["c_support"] + vectors["G"]["support"] - vectors["E"]["support"] + vectors["P"]["support"],
        "distinguishability": initial["c_distinguishability"] + vectors["G"]["distinguishability"] - vectors["E"]["distinguishability"] + vectors["P"]["distinguishability"],
        "boundary": initial["c_boundary"] + vectors["G"]["boundary"] - vectors["E"]["boundary"] - vectors["P"]["boundary_out"],
    }
    frozen_gep = execution["frozen_registry_import"]["registered_intervention_targets"]["registered_GEP_pre_r"]
    check("intervention_target_derived_before_app_a2", all(abs(expected_gep[key] - frozen_gep[key]) <= 1e-12 for key in expected_gep))
    check("retention_not_gate", base["measurement_authority"]["retention_role"] == "configuration_identity_not_measured_gate")
    check("four_measured_gates", set(base["measurement_authority"]["gates"]) == {"environment_feedback", "support_feedback", "phase_residual", "registered_route_merge_leakage"})

    check("runtime_passed", runtime["status"] == "passed" and runtime["checks_passed"] == runtime["checks_total"] == 29)
    check("all_runtime_checks_pass", all(row["passed"] for row in runtime["checks"]))
    runtime_without_digest = dict(runtime)
    embedded_digest = runtime_without_digest.pop("output_digest")
    check("runtime_embedded_digest", digest_value(runtime_without_digest) == embedded_digest)
    check("runtime_correction_freeze", runtime["provenance"]["freeze_sha256"] == sha256_file(CONTRACTS / "app-a1-conformance-correction-freeze.json"))
    check("runtime_venv", runtime["provenance"]["invoked_executable"] == ".venv/bin/python" and runtime["provenance"]["venv_prefix"] == ".venv")
    check("runtime_pygrc_checkout", runtime["provenance"]["pygrc_import_identity"] == {"repository_id": "graph-reflexive-coherence", "path": "src/pygrc/__init__.py"})
    clamp = runtime["branches"]["carrier_clamped"]["intervention"]["packet_ledger_rebase"]
    check("clamp_public_rebase", clamp["mechanism"] == "pygrc.models.build_lgrc9v3_packet_ledger")
    check("clamp_history_preserved", clamp["packet_history_preserved"] is True and clamp["packet_event_history_preserved"] is True)
    check("clamp_empty_queue_zero_error", clamp["queue_was_empty"] is True and abs(clamp["new_budget_error"]) <= 1e-12)
    check("common_diversion_receipts", len(runtime["branches"]["native_common"]["operation_receipts"]) == 12 and len(runtime["branches"]["all_diverted"]["operation_receipts"]) == 12)
    check("restoration_identity", runtime["restoration"]["save_load_identity_equal"] is True and runtime["restoration"]["empty_step_identity_equal"] is True)
    check("reset_baselines", runtime["restoration"]["original_reset_to_baseline"] is True and runtime["restoration"]["loaded_reset_to_baseline"] is True)
    check("runtime_quarantined", runtime["quarantine"] == {"scientific_vectors_used": False, "app_a2_arms_executed": 0, "scientific_gate_signatures_evaluated": 0, "support_or_falsification_assigned": False, "app_a1_accepted": False, "commit_authorized": False})

    attempts = run_receipt["attempt_ledger"]
    check("honest_attempt_ledger", attempts["original_failed_evidence_starts"] == 1 and attempts["owner_authorized_replacement_starts"] == 1 and attempts["deterministic_reconstruction_starts"] == 1)
    check("no_retries", attempts["replacement_retry_count"] == 0 and attempts["post_reconstruction_additional_starts"] == 0)
    check("byte_reconstruction", run_receipt["reconstruction"]["byte_identical_to_retained_output"] is True and run_receipt["reconstruction"]["reconstructed_sha256"] == sha256_file(CONTRACTS / "app-a1-runtime-conformance.json"))
    check("no_app_a2_runtime", attempts["app_a2_campaign_starts"] == 0 and attempts["app_a2_arm_starts"] == 0 and attempts["scientific_gate_evaluations"] == 0)

    portable_values = [
        audit,
        proposal,
        acceptance,
        base,
        base_validation,
        failed,
        correction_auth,
        correction_freeze,
        correction_validation,
        runtime,
        run_receipt,
        execution,
        report_path.read_text(encoding="utf-8"),
    ]
    check("portable_package", not any(contains_machine_path(value) for value in portable_values))
    check("validator_did_not_import_pygrc", "pygrc" not in sys.modules)

    failures = [row["check_id"] for row in checks if not row["passed"]]
    result = {
        "artifact_id": "p2_i2_app_a1_complete_validation_stdout",
        "iteration_id": "P2-I2-APP-A1",
        "status": "passed" if not failures else "failed",
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failure_count": len(failures),
        "failures": failures,
        "pygrc_imports": 0,
        "models_constructed": 0,
        "app_a2_arms_executed": 0,
        "scientific_gate_signatures_evaluated": 0,
        "app_a2_authorized": False,
        "commit_authorized": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
