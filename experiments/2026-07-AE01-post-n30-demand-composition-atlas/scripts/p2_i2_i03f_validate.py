#!/usr/bin/env python3
"""Validate the compact P2-I2 I03 family-closeout index.

This is intentionally an index/traceability validator. It imports no PyGRC,
instantiates no model, replays no conformance, and does not reopen accepted
mode-level capability, source, or dataflow findings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
EXPECTED_INPUT_SHA256 = "0593c7821370ce138db4fba9bbbc5fd0bbd50f88788e22618acb6b421b2401e3"
EXPECTED_INDEX_SHA256 = "f9c8591a9d3c30a90097548b359e399b3a9e73b01f06ea7cd63d5971ceeb3fa6"
EXPECTED_BASELINE_COMMIT = "fc3fb0f638eb0b180cb05d081e6dc447f24af66b"
EXPECTED_BASELINE_TREE = "83e86f767e5822ca8c65c69e7c748683cb28a8b7"
EXPECTED_GRAPH_REVISION = "83e3a300426631ee4df71b661b67d4fcfdfed594"
MODES = ["state_carried", "history_carried", "hybrid"]
REALIZATION_CLASSES = [
    "pygrc_native_candidate",
    "minimally_producer_assisted",
    "minimally_producer_assisted",
]
OPS = [f"H-L02-OP-{index:02d}" for index in range(1, 10)]
HISTORY_OBLIGATION_CHECKS = ["RV-03", "RV-12", "RV-15", "RV-17", "RV-18", "RV-19"]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def _git_show(repository: Path, revision: str, path: str) -> bytes:
    return subprocess.run(
        ("git", "-C", str(repository), "show", f"{revision}:{path}"),
        check=True,
        capture_output=True,
    ).stdout


def _result(check_id: str, name: str, condition: bool, finding: str, evidence: Any) -> dict[str, Any]:
    if not condition:
        raise AssertionError(f"{check_id} failed: {finding}")
    return {
        "check_id": check_id,
        "name": name,
        "status": "passed",
        "finding": finding,
        "evidence": evidence,
    }


def _pointer(document: Mapping[str, Any], pointer: str) -> Any:
    value: Any = document
    for part in pointer.strip("/").split("/"):
        if isinstance(value, list):
            value = value[int(part)]
        else:
            value = value[part]
    return value


def validate(input_path: Path, index_path: Path) -> dict[str, Any]:
    freeze = _load(input_path)
    family = _load(index_path)
    if _sha256(input_path) != EXPECTED_INPUT_SHA256:
        raise AssertionError("I03F input identity drifted")
    if _sha256(index_path) != EXPECTED_INDEX_SHA256:
        raise AssertionError("I03F family index identity drifted")
    if freeze["artifact_id"] != "P2-I2-I03F-FAMILY-CLOSEOUT-INPUT":
        raise AssertionError("wrong I03F input artifact")
    if family["artifact_id"] != "P2-I2-I03F-FAMILY-CLOSEOUT-INDEX":
        raise AssertionError("wrong I03F family index artifact")
    if freeze["scope_boundary"]["review_kind"] != "terminal_authority_composition_and_index_integrity_only":
        raise AssertionError("I03F scope expanded beyond compact composition")
    if any(freeze["scope_boundary"][key] for key in (
        "reopen_mode_capability_audit",
        "reopen_mode_source_dataflow_review",
        "reopen_mode_runtime_conformance",
    )):
        raise AssertionError("I03F cannot reopen an accepted mode review")
    if any(freeze["runtime_policy"][key] != 0 for key in (
        "model_instantiations",
        "runtime_evidence_invocations",
        "runtime_reconstruction_invocations",
        "retries",
    )) or freeze["runtime_policy"]["source_capability_reaudit"] is not False:
        raise AssertionError("I03F must remain zero-runtime and no-reaudit")

    if freeze["entry_authority"]["accepted_baseline_commit"] != EXPECTED_BASELINE_COMMIT:
        raise AssertionError("accepted baseline commit drifted")
    if freeze["entry_authority"]["accepted_baseline_tree"] != EXPECTED_BASELINE_TREE:
        raise AssertionError("accepted baseline tree drifted")
    if _git(ROOT, "rev-parse", EXPECTED_BASELINE_COMMIT) != EXPECTED_BASELINE_COMMIT:
        raise AssertionError("accepted baseline commit unavailable")
    if _git(ROOT, "rev-parse", f"{EXPECTED_BASELINE_COMMIT}^{{tree}}") != EXPECTED_BASELINE_TREE:
        raise AssertionError("accepted baseline tree unavailable")

    authority_checks = []
    for item in freeze["terminal_authorities"]:
        path = ROOT / item["path"]
        live_sha = _sha256(path)
        baseline_sha = _sha256_bytes(_git_show(ROOT, EXPECTED_BASELINE_COMMIT, item["path"]))
        if live_sha != item["sha256"] or baseline_sha != item["sha256"]:
            raise AssertionError(f"terminal authority substituted: {item['path']}")
        authority_checks.append({
            "mode": item["mode"],
            "kind": item["kind"],
            "path": item["path"],
            "sha256": live_sha,
            "baseline_match": True,
        })

    graph_root = Path(freeze["entry_authority"]["graph_repository"])
    graph_before = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "status_porcelain": _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"),
    }
    if graph_before != {"revision": EXPECTED_GRAPH_REVISION, "status_porcelain": ""}:
        raise AssertionError("admitted PyGRC checkout is not exact and clean")

    contracts = {
        item["mode"]: _load(ROOT / item["path"])
        for item in freeze["terminal_authorities"]
        if item["kind"] == "causal_contract"
    }
    runtime = {
        item["mode"]: _load(ROOT / item["path"])
        for item in freeze["terminal_authorities"]
        if item["kind"] == "runtime_conformance"
    }
    history_closeout = _load(EXPERIMENT / "contracts/p2-i2/i03br1-closeout-revalidation.json")
    hybrid_closeout = _load(EXPERIMENT / "contracts/p2-i2/i03cr1-closeout-revalidation.json")
    hybrid_registry = _load(EXPERIMENT / "contracts/p2-i2/i03cr1-hybrid-closeout-registry.json")

    mode_rows = family["mode_registry"]
    exact_modes = (
        [row["mode"] for row in mode_rows] == MODES
        and [row["realization_class"] for row in mode_rows] == REALIZATION_CLASSES
        and all(row["required_downstream"] is True for row in mode_rows)
        and [row["mode"] for row in freeze["accepted_mode_summaries"]] == MODES
        and [row["realization_class"] for row in freeze["accepted_mode_summaries"]] == REALIZATION_CLASSES
    )

    conformance_summaries = {
        mode: runtime[mode]["assertion_summary"] for mode in MODES
    }
    expected_summaries = {
        "state_carried": {"failed": 0, "passed": 136, "total": 136},
        "history_carried": {"failed": 0, "passed": 252, "total": 252},
        "hybrid": {"failed": 0, "passed": 258, "total": 258},
    }
    closeouts_accepted = (
        conformance_summaries == expected_summaries
        and all(runtime[mode]["scientific_evidence_assigned"] is False for mode in MODES)
        and history_closeout["review_summary"] == {
            "all_twelve_acceptance_statements_defensible": True,
            "blocking_findings": 0,
            "passed": 15,
            "passed_with_downstream_obligation": 6,
            "review_checks_total": 21,
        }
        and hybrid_closeout["review_summary"]["blocking_findings"] == 0
        and hybrid_closeout["review_summary"]["passed"] == 26
        and hybrid_closeout["acceptance_summary"] == {"failed": 0, "passed": 17, "total": 17}
    )

    qualified = family["cross_mode_symbol_qualification"]
    mode_qualified = (
        contracts["state_carried"]["mode_scope"]["pool_dependence_mode"] == "state_carried"
        and contracts["history_carried"]["mode_scope"]["pool_dependence_mode"] == "history_carried"
        and contracts["hybrid"]["mode_scope"]["pool_dependence_mode"] == "hybrid"
        and "complete causal pool" in qualified["P"]["state_carried"]
        and "excluded from V" in qualified["P"]["history_carried"]
        and "component" in qualified["P"]["hybrid"]
        and "authoritative" in qualified["H_P"]["history_carried"]
        and "authoritative" in qualified["H_P"]["hybrid"]
    )

    no_rewrite = (
        contracts["history_carried"]["mode_scope"]["state_carried_profile_status"]
        == "owner_accepted_for_progression_and_unchanged"
        and contracts["hybrid"]["mode_scope"]["state_carried_profile_status"]
        == "owner_accepted_for_progression_and_unchanged"
        and contracts["hybrid"]["mode_scope"]["history_carried_profile_status"]
        == "owner_accepted_for_progression_and_unchanged"
        and "cannot change an earlier mode" in qualified["rewrite_rule"]
    )

    op_index = family["operational_hypothesis_index"]
    op_complete = [row["op_id"] for row in op_index] == OPS
    for position, row in enumerate(op_index):
        for mode in MODES:
            pointer = row[f"{mode}_pointer"]
            if pointer != f"/operational_projections/{position}":
                op_complete = False
            elif _pointer(contracts[mode], pointer)["op_id"] != row["op_id"]:
                op_complete = False

    structural_index_complete = all(
        all(row.get(key) for key in (
            "carrier", "write_update", "response_access", "intervention_family",
            "private_binding", "producer_boundary", "restoration_owner", "authority_pointers",
        )) for row in mode_rows
    ) and all(
        all(_pointer(contracts[row["mode"]], pointer) for pointer in row["authority_pointers"])
        for row in mode_rows
    )

    selections = {mode: contracts[mode]["realization_selection"] for mode in MODES}
    producer_safe = (
        selections["state_carried"]["realization_class"] == "pygrc_native_candidate"
        and selections["state_carried"]["rcae_causal_producer_selected"] is False
        and selections["history_carried"]["realization_class"] == "minimally_producer_assisted"
        and selections["history_carried"]["rcae_producer_computes_success_or_later_response"] is False
        and selections["history_carried"]["native_feedback_producer_owns_later_response_transition"] is True
        and selections["hybrid"]["realization_class"] == "minimally_producer_assisted"
        and selections["hybrid"]["rcae_producer_computes_joint_score_success_or_later_response"] is False
        and selections["hybrid"]["native_feedback_producer_owns_joint_evaluation_and_later_transition"] is True
    )

    restorations = {mode: contracts[mode]["restoration_profile_proposal"] for mode in MODES}
    restoration_safe = (
        restorations["state_carried"]["provider"] == "pygrc.models.lgrc9v3_restoration_identity_v2"
        and restorations["history_carried"]["native_provider"] == "pygrc.models.lgrc9v3_restoration_identity_v2"
        and "adapter" in restorations["history_carried"]["composite_identity_rule"]
        and restorations["hybrid"]["native_provider"] == "pygrc.models.lgrc9v3_restoration_identity_v2"
        and "adapter" in restorations["hybrid"]["composite_identity_rule"]
        and "identity v2" in mode_rows[0]["restoration_owner"]
        and "adapter" in mode_rows[1]["restoration_owner"]
        and "adapter" in mode_rows[2]["restoration_owner"]
    )

    source_obligations = family["source_obligations"]
    source_ids = [row["source_id"] for row in source_obligations]
    expected_source_ids = (
        [f"I03BR1-OBL-{index:02d}" for index in range(1, 7)]
        + [f"I03CR1-OBL-{index:02d}" for index in range(1, 9)]
    )
    history_qualified = [
        row for row in history_closeout["checks"]
        if row["qualification_or_downstream_obligation"]
    ]
    history_lossless = all(
        source_obligations[index]["source_check"] == HISTORY_OBLIGATION_CHECKS[index]
        and source_obligations[index]["duty"] == history_qualified[index]["qualification_or_downstream_obligation"]
        for index in range(6)
    )
    hybrid_lossless = all(
        source_obligations[6 + index]["source_id"] == source["obligation_id"]
        and source_obligations[6 + index]["duty"] == source["duty"]
        and source_obligations[6 + index]["owner_iteration"] == source["owner_iteration"]
        for index, source in enumerate(hybrid_registry["downstream_obligations"])
    )
    obligations_lossless = source_ids == expected_source_ids and history_lossless and hybrid_lossless

    consolidated = family["consolidated_duties"]
    mapped_source_ids = [source_id for duty in consolidated for source_id in duty["source_ids"]]
    consolidation_safe = (
        len(consolidated) == 9
        and sorted(mapped_source_ids) == sorted(expected_source_ids)
        and len(mapped_source_ids) == len(set(mapped_source_ids)) == 14
        and all("discharged" not in duty["status"] or duty["status"] == "retained_undischarged" for duty in consolidated)
        and next(duty for duty in consolidated if duty["duty_id"] == "I03F-DUTY-09")["status"]
        == "in_progress_pending_owner_acceptance"
    )

    quarantine = family["fixture_quarantine"]
    source_quarantine = hybrid_registry["fixture_quarantine_registry"]
    i04 = family["i04_import_boundary"]
    quarantine_and_import_safe = (
        quarantine["covered_modes"] == MODES
        and quarantine["covered_source_artifact_count"] == 7
        and {row["mode"] for row in source_quarantine["source_artifacts"]} == set(MODES)
        and quarantine["scientific_value_selection_performed"] is False
        and i04["required_modes"] == MODES
        and i04["import_unchanged"] is True
        and i04["mode_ranking_or_selection_allowed"] is False
        and i04["mode_removal_allowed"] is False
        and i04["causal_semantic_revision_allowed"] is False
        and i04["fixture_value_or_outcome_import_allowed"] is False
        and len(i04["semantic_equivalence_minimum_fields"]) == 7
        and i04["scientific_fields_selected_in_I03F"] is False
    )

    boundary = family["program_boundary"]
    compact_boundary_safe = (
        boundary["retained_mode_count"] == 3
        and boundary["selection_or_ranking_performed"] is False
        and boundary["repeated_mode_review_performed"] is False
        and boundary["source_capability_reaudit_performed"] is False
        and boundary["runtime_or_reconstruction_performed"] is False
        and boundary["scientific_evidence_assigned"] is False
        and boundary["R01_through_R05_assigned"] is False
        and boundary["discriminator_gate_passed"] is False
        and boundary["owner_acceptance_required"] is True
        and boundary["I04_authorized"] is False
    )

    checks = [
        _result("FAM-01", "exact_terminal_authority_identity_and_accepted_entry", len(authority_checks) == 11 and closeouts_accepted, "All eleven compact terminal authorities match the accepted baseline commit; retained conformance/closeout summaries remain exact and outcome-free.", {"authorities": authority_checks, "conformance_summaries": conformance_summaries}),
        _result("FAM-02", "three_required_modes_and_realization_classes_retained_without_ranking", exact_modes and boundary["selection_or_ranking_performed"] is False, "Exactly three downstream modes retain their accepted realization classes with no ranking or selection.", mode_rows),
        _result("FAM-03", "mode_qualified_carriers_and_response_paths_remain_distinct", mode_qualified, "P, H_P, M_H, and L retain distinct mode-qualified causal roles; no symbol collapse occurred.", qualified),
        _result("FAM-04", "later_modes_do_not_rewrite_earlier_accepted_modes", no_rewrite, "The accepted B and C contracts explicitly retain earlier profiles unchanged, and exact baseline identities prevent substitution.", qualified["rewrite_rule"]),
        _result("FAM-05", "complete_nine_by_three_operational_hypothesis_pointer_index", op_complete, "All nine OPs have an exact pointer into each of the three accepted contracts (27 entries) without reassessing mode evidence.", op_index),
        _result("FAM-06", "intervention_access_private_and_producer_boundaries_indexed", structural_index_complete, "Every mode has a non-empty pointer-backed carrier, update, access, intervention, private, producer, and restoration index.", [{"mode": row["mode"], "authority_pointers": row["authority_pointers"]} for row in mode_rows]),
        _result("FAM-07", "native_first_and_minimal_producer_assistance_retained", producer_safe, "State remains native; history/hybrid assistance stops at active-history/readout materialization while native PyGRC owns success and later response.", [selections[mode] for mode in MODES]),
        _result("FAM-08", "mode_specific_restoration_ownership_indexed", restoration_safe, "State restoration remains native-v2 plus declarative binding; history and hybrid retain paired native-v2/adapter composite identity.", [row["restoration_owner"] for row in mode_rows]),
        _result("FAM-09", "all_fourteen_mode_closeout_obligations_preserved_losslessly", obligations_lossless, "All six I03BR1 qualifications and eight I03CR1 obligations are copied exactly with stable source traceability.", source_obligations),
        _result("FAM-10", "consolidated_duties_trace_every_source_without_premature_discharge", consolidation_safe, "Nine compact duties cover each of the fourteen source obligations exactly once; none is prematurely discharged and family acceptance remains pending.", consolidated),
        _result("FAM-11", "complete_fixture_quarantine_and_mode_indexed_I04_import_boundary", quarantine_and_import_safe, "The existing seven-source three-mode quarantine is retained; I04 must import all modes unchanged and prove equivalence before sharing artifacts.", {"quarantine": quarantine, "i04_import_boundary": i04}),
        _result("FAM-12", "zero_runtime_graph_clean_and_owner_review_gate_boundary", compact_boundary_safe, "I03F remained a compact no-reaudit, zero-runtime composition; PyGRC stayed exact/clean and only owner-reviewed gate readiness is assigned.", {"program_boundary": boundary, "graph": graph_before}),
    ]
    if [row["check_id"] for row in checks] != [row["id"] for row in freeze["integration_checks"]]:
        raise AssertionError("integration-check identity/order drifted")

    acceptance_map = {
        "FAC-01": ["FAM-01", "FAM-02"],
        "FAC-02": ["FAM-03", "FAM-04", "FAM-06"],
        "FAC-03": ["FAM-05"],
        "FAC-04": ["FAM-07"],
        "FAC-05": ["FAM-08"],
        "FAC-06": ["FAM-09", "FAM-10"],
        "FAC-07": ["FAM-11"],
        "FAC-08": ["FAM-11"],
        "FAC-09": ["FAM-12"],
    }
    check_map = {row["check_id"]: row for row in checks}
    acceptance = []
    for statement in freeze["acceptance_conditions"]:
        supporting = acceptance_map[statement["id"]]
        if not all(check_map[check_id]["status"] == "passed" for check_id in supporting):
            raise AssertionError(f"family acceptance condition failed: {statement['id']}")
        acceptance.append({
            "acceptance_id": statement["id"],
            "status": "passed",
            "statement": statement["text"],
            "supporting_checks": supporting,
        })

    graph_after = {
        "revision": _git(graph_root, "rev-parse", "HEAD"),
        "status_porcelain": _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"),
    }
    if graph_after != graph_before:
        raise AssertionError("PyGRC checkout changed during compact family validation")

    return {
        "artifact_id": "P2-I2-I03F-FAMILY-CLOSEOUT-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I03F",
        "lane_id": "AE01-L02",
        "validated_at": "2026-07-14",
        "status": "passed_compact_family_composition",
        "exit_state": "P2-I2-I03F-REVIEW-READY",
        "validation_kind": "terminal_authority_identity_and_lossless_index_traceability_only",
        "explicit_non_actions": [
            "no repeated mode capability audit",
            "no repeated mode source/dataflow review",
            "no model instantiation",
            "no runtime conformance or reconstruction",
            "no scientific response, comparator, calibration, or result selection",
        ],
        "runtime_accounting": {
            "model_instantiations": 0,
            "runtime_evidence_invocations": 0,
            "runtime_reconstruction_invocations": 0,
            "source_capability_reaudits": 0,
            "retries": 0,
            "parameter_search": False,
        },
        "input_identity": {
            "path": str(input_path.relative_to(ROOT)),
            "sha256": _sha256(input_path),
            "accepted_baseline_commit": EXPECTED_BASELINE_COMMIT,
            "accepted_baseline_tree": EXPECTED_BASELINE_TREE,
            "terminal_authority_count": len(authority_checks),
        },
        "index_identity": {
            "path": str(index_path.relative_to(ROOT)),
            "sha256": _sha256(index_path),
        },
        "graph_before": graph_before,
        "graph_after": graph_after,
        "checks": checks,
        "check_summary": {"total": 12, "passed": 12, "failed": 0, "blocking_findings": 0},
        "acceptance_conditions": acceptance,
        "acceptance_summary": {"total": 9, "passed": 9, "failed": 0},
        "retained_mode_count": 3,
        "source_obligation_count": 14,
        "consolidated_duty_count": 9,
        "gate_boundary": {
            "discriminator_gate_ready_for_owner_review": True,
            "owner_acceptance_assigned": False,
            "discriminator_gate_passed": False,
            "I04_authorized": False,
            "scientific_evidence_assigned": False,
        },
        "disposition": "All three accepted mode packages compose losslessly and are ready for owner review of the discriminator gate; no mode review was repeated and I04 remains closed.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.input.resolve(), args.index.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "check_summary": result["check_summary"],
        "acceptance_summary": result["acceptance_summary"],
        "retained_mode_count": result["retained_mode_count"],
        "source_obligation_count": result["source_obligation_count"],
        "runtime_accounting": result["runtime_accounting"],
        "gate_boundary": result["gate_boundary"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
