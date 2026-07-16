#!/usr/bin/env python3
"""Reconstruct the P2-I3 I02 exact source-admission proposal.

The validator performs source, public-identity, and evidence-role checks only.
It never constructs a field, invokes an LGRC transition, selects a realization,
or produces scientific evidence.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import inspect
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
from typing import Any


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
MANIFEST = EXPERIMENT / "contracts/p2-i3/i02-source-admission-manifest.json"
ALLOWED_STATUSES = {"review_ready", "accepted"}
ALLOWED_GRAPH_ROLES = {
    "admitted_package_identity",
    "admitted_interface_source",
    "admitted_runtime_option_source",
    "admitted_measurement_option_source",
    "admitted_restoration_option_source",
    "supporting_conformance_only",
    "supporting_claim_boundary_only",
    "supporting_comparative_substrate_only",
    "supporting_exclusion_only",
}
ALLOWED_CALLABLE_ROLES = {
    "admitted_runtime_option",
    "admitted_measurement_option",
    "admitted_restoration_option",
    "supporting_implementation_only",
    "supporting_comparative_substrate_only",
    "supporting_nonqualifying_boundary_only",
}
ALLOWED_EVIDENCE_CLASSES = {
    "inherited_evidence",
    "ecology_interpretation",
    "constructed_mechanism",
    "missing_surface",
    "proposed_discriminator",
}


class ValidationError(RuntimeError):
    """The retained I02 proposal cannot be reconstructed."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def _git_text(root: Path, *args: str) -> str:
    return _git_bytes(root, *args).decode("utf-8").strip()


def _revision_file(root: Path, revision: str, path: str) -> bytes:
    return _git_bytes(root, "show", f"{revision}:{path}")


def _require_portable(value: str, label: str) -> None:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value.startswith("file:" + "//"):
        raise ValidationError(f"non-portable {label}: {value}")


def _require_checkout(root: Path, revision: str, label: str) -> dict[str, Any]:
    if _git_text(root, "rev-parse", "HEAD") != revision:
        raise ValidationError(f"{label} checkout is not at admitted revision")
    status = _git_text(root, "status", "--short")
    if status:
        raise ValidationError(f"{label} checkout is not clean")
    if _git_text(root, "cat-file", "-t", revision) != "commit":
        raise ValidationError(f"{label} revision is unavailable")
    return {"revision": revision, "worktree": "clean"}


def _source_definitions(source: bytes) -> set[str]:
    tree = ast.parse(source.decode("utf-8"))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }


def _resolve_symbol(models: Any, symbol: str) -> Any:
    prefix = "pygrc.models."
    if not symbol.startswith(prefix):
        raise ValidationError(f"unexpected callable namespace: {symbol}")
    value = models
    for part in symbol[len(prefix) :].split("."):
        try:
            value = getattr(value, part)
        except AttributeError as exc:
            raise ValidationError(f"public callable missing: {symbol}") from exc
    if not callable(value):
        raise ValidationError(f"public identity is not callable: {symbol}")
    return value


def validate(
    *,
    repository_root: Path,
    graph_root: Path,
    theory_root: Path,
) -> dict[str, Any]:
    manifest_path = repository_root / MANIFEST
    manifest = _read_json(manifest_path)
    if manifest.get("status") not in ALLOWED_STATUSES:
        raise ValidationError("manifest status is not review_ready or accepted")
    if manifest.get("question_id") != "P2-I3-Q-002":
        raise ValidationError("manifest does not resolve P2-I3-Q-002")
    if manifest.get("decision_id") != "P2-I3-DEC-019":
        raise ValidationError("manifest does not bind P2-I3-DEC-019")
    validator_contract = manifest["reconstruction"]["validator"]
    _require_portable(validator_contract["path"], "validator path")
    validator_sha256 = _sha256((repository_root / validator_contract["path"]).read_bytes())
    if validator_sha256 != validator_contract["sha256"]:
        raise ValidationError("I02 validator digest mismatch")

    repository_identities = manifest["repository_identities"]
    graph_revision = repository_identities["graph_runtime"]["revision"]
    theory_revision = repository_identities["geometric_theory"]["revision"]
    rcae_revision = repository_identities["rcae_theory"]["revision"]
    graph_state = _require_checkout(graph_root, graph_revision, "graph")
    theory_state = _require_checkout(theory_root, theory_revision, "theory")
    if _git_text(repository_root, "cat-file", "-t", rcae_revision) != "commit":
        raise ValidationError("RCAE theory revision is unavailable")

    frozen_input_checks: list[dict[str, Any]] = []
    for entry in manifest["frozen_i01_inputs"]:
        _require_portable(entry["path"], "I01 input path")
        actual = _sha256((repository_root / entry["path"]).read_bytes())
        if actual != entry["sha256"]:
            raise ValidationError(f"I01 input digest mismatch: {entry['path']}")
        frozen_input_checks.append({"artifact_id": entry["artifact_id"], "sha256": actual})

    historical_authority = manifest["historical_source_authority"]
    _require_portable(historical_authority["path"], "historical source authority")
    historical_bytes = (repository_root / historical_authority["path"]).read_bytes()
    if _sha256(historical_bytes) != historical_authority["sha256"]:
        raise ValidationError("historical source authority digest mismatch")
    historical_text = historical_bytes.decode("utf-8")

    digest_inventory = _read_json(
        repository_root
        / "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i01-source-digests.json"
    )
    source_by_id = {entry["source_id"]: entry for entry in digest_inventory["sources"]}
    assignments = manifest["graph_source_admissions"]
    assigned_ids: list[str] = []
    graph_source_checks: list[dict[str, Any]] = []
    for assignment in assignments:
        role = assignment["admission_role"]
        if role not in ALLOWED_GRAPH_ROLES:
            raise ValidationError(f"invalid graph source role: {role}")
        for source_id in assignment["source_ids"]:
            if source_id in assigned_ids:
                raise ValidationError(f"duplicate graph source assignment: {source_id}")
            entry = source_by_id.get(source_id)
            if entry is None or entry["repository_name"] != "graph-reflexive-coherence":
                raise ValidationError(f"unknown graph source: {source_id}")
            _require_portable(entry["path"], "graph source path")
            actual = _sha256(_revision_file(graph_root, graph_revision, entry["path"]))
            if actual != entry["sha256"]:
                raise ValidationError(f"graph source digest mismatch: {source_id}")
            assigned_ids.append(source_id)
            graph_source_checks.append(
                {"source_id": source_id, "admission_role": role, "sha256": actual}
            )
    expected_graph_ids = {
        entry["source_id"]
        for entry in digest_inventory["sources"]
        if entry["repository_name"] == "graph-reflexive-coherence"
    }
    if set(assigned_ids) != expected_graph_ids:
        raise ValidationError("graph source assignments are not complete and exact")

    theory_source_checks: list[dict[str, Any]] = []
    theory_ids: set[str] = set()
    for entry in manifest["theory_source_admissions"]:
        if entry["source_id"] in theory_ids:
            raise ValidationError(f"duplicate theory source id: {entry['source_id']}")
        theory_ids.add(entry["source_id"])
        if entry["evidence_class"] != "ecology_interpretation":
            raise ValidationError(f"theory source has invalid evidence class: {entry['source_id']}")
        _require_portable(entry["path"], "theory source path")
        repository = entry["repository"]
        if repository == "reflexive-coherence-agentic-ecology":
            data = _revision_file(repository_root, rcae_revision, entry["path"])
        elif repository == "geometric-reflexive-coherence":
            data = _revision_file(theory_root, theory_revision, entry["path"])
        else:
            raise ValidationError(f"unknown theory repository: {repository}")
        actual = _sha256(data)
        if actual != entry["sha256"]:
            raise ValidationError(f"theory source digest mismatch: {entry['source_id']}")
        theory_source_checks.append({"source_id": entry["source_id"], "sha256": actual})
    if theory_ids != {f"P2-I3-I02-TH-{index:03d}" for index in range(1, 9)}:
        raise ValidationError("theory source admission set is not exact")

    theory_by_id = {
        entry["source_id"]: entry for entry in manifest["theory_source_admissions"]
    }
    transition_ids: set[str] = set()
    for transition in manifest["source_transitions"]:
        source_id = transition["source_id"]
        if source_id in transition_ids:
            raise ValidationError(f"duplicate source transition: {source_id}")
        transition_ids.add(source_id)
        if transition["historical_sha256"] not in historical_text:
            raise ValidationError(f"historical transition digest is ungrounded: {source_id}")
        if theory_by_id[source_id]["sha256"] != transition["admitted_sha256"]:
            raise ValidationError(f"admitted transition digest mismatch: {source_id}")
    if transition_ids != {"P2-I3-I02-TH-002", "P2-I3-I02-TH-003", "P2-I3-I02-TH-004", "P2-I3-I02-TH-005"}:
        raise ValidationError("RCAE theory-source transition set is not exact")

    group_checks: list[dict[str, Any]] = []
    for group in manifest["grouped_source_admissions"]:
        if group["evidence_class"] not in {"inherited_evidence", "constructed_mechanism"}:
            raise ValidationError(f"invalid grouped evidence class: {group['group_id']}")
        _require_portable(group["inventory_path"], "group inventory path")
        inventory_path = repository_root / group["inventory_path"]
        if _sha256(inventory_path.read_bytes()) != group["inventory_sha256"]:
            raise ValidationError(f"group inventory digest mismatch: {group['group_id']}")
        inventory = _read_json(inventory_path)
        sources = inventory["sources"]
        if len(sources) != group["source_count"]:
            raise ValidationError(f"group source count mismatch: {group['group_id']}")
        if group["group_id"] == "P2-I3-I02-GROUP-PREDECESSORS":
            visible_experiments = group.get("included_experiments")
            source_experiments = sorted({source["experiment"] for source in sources})
            if visible_experiments != source_experiments:
                raise ValidationError(
                    "predecessor experiment visibility does not match exact inventory"
                )
            summary = inventory["summary"]
            expected_roles = {
                "primary_mechanism_precedent": summary["primary_predecessors"],
                "supporting_mechanism_or_control_precedent": summary[
                    "supporting_predecessors"
                ],
                "projection_only_precedent": [summary["projection_only_predecessor"]],
            }
            if group.get("experiment_role_summary") != expected_roles:
                raise ValidationError(
                    "predecessor experiment role summary does not match exact inventory"
                )
            projected_experiments = sorted(
                experiment
                for experiments in expected_roles.values()
                for experiment in experiments
            )
            if projected_experiments != source_experiments:
                raise ValidationError(
                    "predecessor role projection is incomplete or overlapping"
                )
        for source in sources:
            _require_portable(source["path"], "grouped graph source path")
            actual = _sha256(_revision_file(graph_root, graph_revision, source["path"]))
            if actual != source["sha256"]:
                raise ValidationError(
                    f"grouped graph source digest mismatch: {source['source_id']}"
                )
        group_checks.append(
            {
                "group_id": group["group_id"],
                "source_count": len(sources),
                "admission_role": group["admission_role"],
            }
        )

    source_paths = {
        source_id: source_by_id[source_id]["path"] for source_id in expected_graph_ids
    }
    sys.dont_write_bytecode = True
    graph_src = str((graph_root / "src").resolve())
    if graph_src not in sys.path:
        sys.path.insert(0, graph_src)
    models = importlib.import_module("pygrc.models")
    callable_checks: list[dict[str, Any]] = []
    callable_symbols: set[str] = set()
    for entry in manifest["callable_admissions"]:
        role = entry["admission_role"]
        if role not in ALLOWED_CALLABLE_ROLES:
            raise ValidationError(f"invalid callable role: {role}")
        symbol = entry["symbol"]
        if symbol in callable_symbols:
            raise ValidationError(f"duplicate callable admission: {symbol}")
        callable_symbols.add(symbol)
        obj = _resolve_symbol(models, symbol)
        module = inspect.getmodule(obj)
        if module is None or module.__file__ is None:
            raise ValidationError(f"callable module unavailable: {symbol}")
        module_path = Path(module.__file__).resolve().relative_to((graph_root / "src").resolve())
        normalized = f"src/{module_path.as_posix()}"
        expected = source_paths[entry["implementation_source_id"]]
        if normalized != expected:
            raise ValidationError(
                f"callable source mismatch for {symbol}: {normalized} != {expected}"
            )
        callable_checks.append(
            {
                "symbol": symbol,
                "admission_role": role,
                "implementation_source_id": entry["implementation_source_id"],
            }
        )

    substrate = manifest["substrate_authority"]
    if substrate["primary_substrate"] != "LGRC9V3":
        raise ValidationError("P2-I3 primary substrate must remain LGRC9V3")
    if substrate["grc9v3_role"] != "supporting_comparative_substrate_only":
        raise ValidationError("GRC9V3 role must remain comparative-only")
    callable_role_by_symbol = {
        entry["symbol"]: entry["admission_role"]
        for entry in manifest["callable_admissions"]
    }
    for symbol in (
        "pygrc.models.GRC9V3",
        "pygrc.models.GRC9V3.apply_continuity",
        "pygrc.models.GRC9V3.step",
    ):
        if callable_role_by_symbol.get(symbol) != "supporting_comparative_substrate_only":
            raise ValidationError(f"GRC9V3 callable is not comparative-only: {symbol}")
    if manifest["claim_boundary"].get("grc9v3_substitution_authorized") is not False:
        raise ValidationError("GRC9V3 substitution must fail closed")

    test_names: set[str] = set()
    admitted_test_count = 0
    for entry in manifest["preexisting_test_admissions"]:
        source = source_by_id[entry["source_id"]]
        definitions = _source_definitions(_revision_file(graph_root, graph_revision, source["path"]))
        for test_name in entry["test_names"]:
            if test_name in test_names:
                raise ValidationError(f"duplicate admitted test: {test_name}")
            if test_name not in definitions:
                raise ValidationError(f"admitted test definition missing: {test_name}")
            test_names.add(test_name)
            admitted_test_count += 1
    if admitted_test_count != manifest["preexisting_test_summary"]["test_count"]:
        raise ValidationError("pre-existing test admission count mismatch")

    taxonomy = manifest["evidence_class_taxonomy"]
    if set(taxonomy) != ALLOWED_EVIDENCE_CLASSES:
        raise ValidationError("evidence-class taxonomy is incomplete or extended")
    accepted = manifest["status"] == "accepted"
    claim_boundary = manifest["claim_boundary"]
    if claim_boundary.get("source_admission_accepted") is not accepted:
        raise ValidationError("source-admission acceptance does not match status")
    if claim_boundary.get("source_admission_gate_passed") is not accepted:
        raise ValidationError("source-admission gate does not match status")
    if accepted:
        acceptance = manifest.get("acceptance", {})
        if acceptance.get("gate") != "P2-I3-SOURCE-ADMISSION-GATE":
            raise ValidationError("accepted manifest has wrong exit gate")
        if acceptance.get("gate_status") != "passed":
            raise ValidationError("accepted manifest does not pass exit gate")
    if claim_boundary["realization_selected"]:
        raise ValidationError("I02 may not select a realization")
    if claim_boundary["scientific_execution_performed"]:
        raise ValidationError("I02 may not perform scientific execution")

    return {
        "artifact_id": "P2-I3-I02-ADMISSION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I3-I02",
        "manifest_status": manifest["status"],
        "validation_result": "passed",
        "repository_checks": {
            "graph": graph_state,
            "geometric_theory": theory_state,
            "rcae_revision_available": True,
        },
        "counts": {
            "frozen_i01_inputs": len(frozen_input_checks),
            "graph_sources": len(graph_source_checks),
            "theory_sources": len(theory_source_checks),
            "grouped_source_inventories": len(group_checks),
            "grouped_graph_sources": sum(item["source_count"] for item in group_checks),
            "public_callables": len(callable_checks),
            "preexisting_tests": admitted_test_count,
            "evidence_classes": len(taxonomy),
            "source_transitions": len(transition_ids),
        },
        "checks": {
            "source_digests": "passed",
            "public_callable_identities": "passed",
            "preexisting_test_identities": "passed",
            "source_role_completeness": "passed",
            "source_transitions": "passed",
            "predecessor_experiment_visibility": "passed",
            "evidence_class_separation": "passed",
            "lgrc9v3_substrate_authority": "passed",
            "portable_identities": "passed",
            "validator_identity": "passed",
            "external_checkouts_clean": "passed",
            "no_realization_or_scientific_effect": "passed",
        },
        "manifest_sha256": _sha256(manifest_path.read_bytes()),
        "validator_sha256": validator_sha256,
        "claim_boundary": {
            "source_admission_proposed": True,
            "source_admission_accepted": manifest["status"] == "accepted",
            "source_admission_gate_passed": manifest["status"] == "accepted",
            "realization_selected": False,
            "grc9v3_substitution_authorized": False,
            "pygrc_transition_invoked": False,
            "candidate_or_control_executed": False,
            "scientific_evidence_produced": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-root", required=True, type=Path)
    parser.add_argument("--theory-root", required=True, type=Path)
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[3]
    result = validate(
        repository_root=repository_root,
        graph_root=args.graph_root,
        theory_root=args.theory_root,
    )
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
