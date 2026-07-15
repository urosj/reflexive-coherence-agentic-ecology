#!/usr/bin/env python3
"""Validate the inactive APP-A1 source/delta and gate-proposal package."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments" / "2026-07-AE01-post-n30-demand-composition-atlas"
CONTRACTS = EXPERIMENT / "contracts" / "p2-i2"
AUDIT_PATH = CONTRACTS / "app-a1-source-delta-audit.json"
PROPOSAL_PATH = CONTRACTS / "app-a1-gate-authority-proposal.json"
REPORT_PATH = EXPERIMENT / "reports" / "P2-I2-APP-A1-source-delta-and-gate-authority-review.md"
GRAPH_ROOT = Path(
    os.environ.get("RCAE_GRAPH_REPO", ROOT.parent / "graph-reflexive-coherence")
).resolve()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def resolve_locator(locator: str) -> Path:
    if locator.startswith("grc:"):
        return GRAPH_ROOT / locator.removeprefix("grc:")
    if locator.startswith("rcae:"):
        rel = locator.removeprefix("rcae:").split("@", 1)[0]
        return ROOT / rel
    raise ValueError(f"unsupported locator: {locator}")


def contains_machine_path(value: Any) -> bool:
    text = json.dumps(value, sort_keys=True, ensure_ascii=True)
    forbidden = ("/" + "home" + "/", "Documents" + "/" + "RC-github")
    return any(token in text for token in forbidden)


def main() -> int:
    audit = load_json(AUDIT_PATH)
    proposal = load_json(PROPOSAL_PATH)
    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed)})

    check("audit_json_exists", AUDIT_PATH.is_file())
    check("proposal_json_exists", PROPOSAL_PATH.is_file())
    check("cumulative_report_exists", REPORT_PATH.is_file())
    check("rcae_entry_head_retained", git("rev-parse", "HEAD") == audit["entry_identities"]["rcae"]["commit"])
    check("graph_head_matches", git("rev-parse", "HEAD", cwd=GRAPH_ROOT) == audit["entry_identities"]["graph"]["commit"])
    check("graph_tree_clean", git("status", "--short", cwd=GRAPH_ROOT) == "")
    check("graph_read_only_boundary", audit["entry_identities"]["graph"]["mutation_allowed"] is False)
    check("repository_venv_bound", audit["entry_identities"]["python"]["logical_executable"] == ".venv/bin/python")
    check("bytecode_disabled", audit["entry_identities"]["python"]["bytecode_disabled_for_app_a1_commands"] is True)
    check("omitted_binding_diagnostic_retained", audit["entry_identities"]["import_probe_history"][0]["result"] == "nonconforming_diagnostic")
    check("omitted_binding_not_availability_defect", "not a PyGRC availability defect" in audit["entry_identities"]["import_probe_history"][0]["interpretation"])
    check("established_checkout_source_import_retained", audit["entry_identities"]["import_probe_history"][1]["result"] == "passed")

    app_a0_hashes_match = True
    for row in audit["accepted_app_a0_identities"]:
        locator = row["locator"]
        path_and_commit = locator.removeprefix("rcae:")
        rel, commit = path_and_commit.rsplit("@", 1)
        committed = subprocess.run(
            ["git", "show", f"{commit}:{rel}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        app_a0_hashes_match &= sha256_bytes(committed) == row["sha256"]
    check("accepted_app_a0_hashes_match", app_a0_hashes_match)

    n29_hashes_match = all(
        resolve_locator(row["locator"]).is_file()
        and sha256_file(resolve_locator(row["locator"])) == row["sha256"]
        for row in audit["retained_n29_sources"]
    )
    check("retained_n29_hashes_match", n29_hashes_match)
    builder_hashes_match = all(
        resolve_locator(row["locator"]).is_file()
        and sha256_file(resolve_locator(row["locator"])) == row["sha256"]
        for row in audit["source_builder_identities"]
    )
    check("n29_builder_hashes_match", builder_hashes_match)
    pygrc_hashes_match = all(
        resolve_locator(row["locator"]).is_file()
        and sha256_file(resolve_locator(row["locator"])) == row["sha256"]
        for row in audit["pygrc_source_identities"]
    )
    check("pygrc_source_hashes_match", pygrc_hashes_match)

    findings = audit["source_audit_findings"]
    check("n29_i141_i143_not_live_pygrc", findings["n29_i14_1_and_i14_3_are_live_pygrc_runs"] is False)
    check("n29_i1423_not_live_pygrc", findings["n29_i14_2_3_is_live_pygrc_run"] is False)
    check("n29_i1452_not_live_pygrc", findings["n29_i14_5_2_is_live_pygrc_run"] is False)
    selection = audit["realization_selection_after_audit"]
    check("carrier_selected_native", selection["carrier"]["classification"] == "native_adequate")
    check("four_operations_classified", [row["operation"] for row in selection["operations"]] == ["G", "E", "P", "R"])
    check("all_operations_native", all(row["classification"] == "native_adequate" for row in selection["operations"]))
    check("no_load_bearing_producer", selection["load_bearing_external_producer_required"] is False)

    transport = audit["transportability_audit"]
    check("metric_semantics_not_equivalent", transport["metric_semantics_equivalent"] is False)
    check("measurement_domain_not_equivalent", transport["measurement_domain_equivalent"] is False)
    check("transportability_failed", transport["transportability_gate_passed"] is False)
    check("n29_thresholds_not_authoritative", transport["n29_numeric_gates_authoritative_for_app_a"] is False)
    check("all_dimensions_failed_explicitly", len(transport["dimensions"]) == 10 and all(row["equivalent"] is False for row in transport["dimensions"]))

    disposition = audit["failed_closed_disposition"]
    check("fixture_freeze_closed", disposition["fixture_freeze_allowed"] is False)
    check("conformance_closed", disposition["candidate_free_conformance_allowed"] is False)
    check("app_a2_closed", disposition["app_a2_allowed"] is False)
    check("zero_runtime_counts", disposition["scientific_runtime_count"] == 0 and disposition["candidate_free_conformance_count"] == 0)
    check("proposal_inactive", proposal["authority_effect_now"]["gate_authority_active"] is False)
    check("proposal_requires_review", proposal["status"] == "proposal_only_requires_separate_owner_review")
    check("retention_is_configuration", proposal["proposed_gate_signature"]["retention_configuration_identity"]["role"].endswith("not a measured success gate"))
    check("four_proposed_measured_gates", set(proposal["proposed_gate_signature"]) == {"retention_configuration_identity", "environment_feedback", "support_feedback", "phase_residual", "registered_route_merge_leakage"})
    check("proposal_disclaims_equivalence", all(proposal["proposed_gate_signature"][key]["native_n29_equivalence_claimed"] is False for key in ("environment_feedback", "support_feedback", "phase_residual", "registered_route_merge_leakage")))
    check("no_machine_paths", not any(contains_machine_path(value) for value in (audit, proposal, REPORT_PATH.read_text(encoding="utf-8"))))

    failures = [row["check_id"] for row in checks if not row["passed"]]
    result = {
        "artifact_id": "p2_i2_app_a1_validation_stdout",
        "iteration_id": "P2-I2-APP-A1",
        "status": "passed" if not failures else "failed",
        "checks_passed": len(checks) - len(failures),
        "checks_total": len(checks),
        "failure_count": len(failures),
        "failures": failures,
        "scientific_runtime_count": 0,
        "candidate_free_conformance_count": 0,
        "app_a2_authorized": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
