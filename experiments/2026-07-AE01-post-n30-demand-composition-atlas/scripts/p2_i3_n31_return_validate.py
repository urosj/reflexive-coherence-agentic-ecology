#!/usr/bin/env python3
"""Validate and reconstruct the bounded N31-to-P2-I3 return transition.

The graph repository is consumed read-only. Reconstruction occurs in a
temporary local clone at the retained N31 source anchor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import tomllib
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
MANIFEST = EXPERIMENT / "contracts/p2-i3/i03-n31-return-admission.json"
DEFAULT_RESULT = EXPERIMENT / "contracts/p2-i3/i03-n31-return-validation.json"


class ValidationError(RuntimeError):
    """The bounded N31 return cannot be reconstructed or admitted."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
    ).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json_bytes(data: bytes, label: str) -> dict[str, Any]:
    value = json.loads(data.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must contain one JSON object")
    return value


def read_json(path: Path) -> dict[str, Any]:
    return read_json_bytes(path.read_bytes(), path.as_posix())


def git_bytes(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def git_text(root: Path, *args: str) -> str:
    return git_bytes(root, *args).decode("utf-8").strip()


def revision_bytes(root: Path, revision: str, path: str) -> bytes:
    return git_bytes(root, "show", f"{revision}:{path}")


def require_portable(path_text: str, label: str) -> None:
    path = PurePosixPath(path_text)
    if path.is_absolute() or ".." in path.parts or path_text.startswith("file://"):
        raise ValidationError(f"non-portable {label}: {path_text}")


def require_internal_digest(value: dict[str, Any], expected: str, label: str) -> None:
    actual = value.get("output_digest")
    derived = canonical_digest(
        {key: item for key, item in value.items() if key != "output_digest"}
    )
    if actual != expected or derived != expected:
        raise ValidationError(f"internal output digest mismatch: {label}")


def json_diff_paths(left: Any, right: Any, path: str = "") -> set[str]:
    if type(left) is not type(right):
        return {path or "/"}
    if isinstance(left, dict):
        differences: set[str] = set()
        for key in set(left) | set(right):
            child = f"{path}/{key}"
            if key not in left or key not in right:
                differences.add(child)
            else:
                differences.update(json_diff_paths(left[key], right[key], child))
        return differences
    if isinstance(left, list):
        differences = set()
        if len(left) != len(right):
            differences.add(f"{path}/length")
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences.update(
                json_diff_paths(left_item, right_item, f"{path}/{index}")
            )
        return differences
    return set() if left == right else {path or "/"}


def graph_python_version(graph_python: Path) -> str:
    return subprocess.check_output(
        [
            str(graph_python),
            "-c",
            "import importlib.metadata as m; print(m.version('pygrc'))",
        ],
        text=True,
    ).strip()


def graph_python_module_path(graph_python: Path) -> Path:
    return Path(
        subprocess.check_output(
            [str(graph_python), "-c", "import pygrc; print(pygrc.__file__)"],
            text=True,
        ).strip()
    ).resolve()


def validate_source_transition(
    manifest: dict[str, Any], graph_root: Path, graph_python: Path
) -> dict[str, Any]:
    if manifest.get("status") != "accepted":
        raise ValidationError("return admission is not accepted")
    if manifest.get("gate_disposition") != "passed":
        raise ValidationError("N31 return gate is not passed")
    if manifest.get("decision_id") != "P2-I3-DEC-025":
        raise ValidationError("return admission does not bind P2-I3-DEC-025")
    if manifest.get("selection_status") != "provider_options_admitted_none_selected":
        raise ValidationError("return admission silently selects a provider")

    validator = manifest["reconstruction"]["validator"]
    require_portable(validator["path"], "return validator path")
    if sha256((ROOT / validator["path"]).read_bytes()) != validator["sha256"]:
        raise ValidationError("return validator exact-file digest mismatch")

    identities = manifest["repository_identities"]
    merge_revision = identities["graph_checkout_merge_revision"]
    closeout_revision = identities["n31_closeout_commit"]
    source_anchor = identities["n31_evidence_source_anchor"]
    demand_revision = identities["rcae_demand_source_revision"]

    if git_text(graph_root, "rev-parse", "HEAD") != merge_revision:
        raise ValidationError("graph checkout is not at the admitted merge revision")
    if git_text(graph_root, "status", "--short"):
        raise ValidationError("graph checkout is not clean")
    if git_text(graph_root, "rev-parse", f"{closeout_revision}^") != source_anchor:
        raise ValidationError("N31 closeout/source-anchor lineage mismatch")
    merge_parents = git_text(graph_root, "show", "-s", "--format=%P", merge_revision).split()
    if closeout_revision not in merge_parents:
        raise ValidationError("N31 closeout is not a parent of the admitted merge")
    if git_text(graph_root, "rev-parse", f"{merge_revision}^{{tree}}") != git_text(
        graph_root, "rev-parse", f"{closeout_revision}^{{tree}}"
    ):
        raise ValidationError("merged graph tree differs from the N31 closeout tree")
    if git_text(ROOT, "cat-file", "-t", demand_revision) != "commit":
        raise ValidationError("RCAE demand-source revision is unavailable")

    historical = manifest["historical_i02_authority"]
    require_portable(historical["path"], "historical I02 path")
    if sha256((ROOT / historical["path"]).read_bytes()) != historical["sha256"]:
        raise ValidationError("historical I02 authority changed")

    closeout_identity = manifest["n31_closeout_identity"]
    closeout_path = closeout_identity["path"]
    require_portable(closeout_path, "N31 closeout path")
    closeout_bytes = revision_bytes(graph_root, closeout_revision, closeout_path)
    if sha256(closeout_bytes) != closeout_identity["sha256"]:
        raise ValidationError("N31 closeout exact-file digest mismatch")
    closeout = read_json_bytes(closeout_bytes, "N31 closeout")
    require_internal_digest(
        closeout, closeout_identity["output_digest"], "N31 closeout"
    )
    if closeout.get("graph_revision") != source_anchor:
        raise ValidationError("N31 closeout does not name its evidence source anchor")
    if closeout.get("n31_closeout_status") != closeout_identity["closeout_status"]:
        raise ValidationError("N31 closeout status mismatch")
    if closeout.get("candidate_dispositions") != manifest.get(
        "n31_candidate_dispositions"
    ):
        raise ValidationError("N31 candidate-disposition projection drift")
    expected_rcae_dispositions = {
        "D0a_native_spatial_organization": (
            "retained_native_foundation_not_selected_as_decay_provider"
        ),
        "D0b_finite_window_derived_observable": (
            "retained_diagnostic_not_selected_as_causal_provider"
        ),
        "D0c_instantaneous_geometry_comparator": (
            "retained_diagnostic_not_selected_as_decay_provider"
        ),
        "A_release_efficacy_attenuation": (
            "retained_semantic_boundary_not_selected_for_current_field_state_demand"
        ),
        "B_conserved_export_policy": "provider_contract_option_admitted_not_selected",
        "C2_exact_history_susceptibility_closure": (
            "provider_contract_option_admitted_not_selected"
        ),
        "B_R_plus_C2": "new_composition_option_not_inherited_not_selected",
    }
    if manifest.get("rcae_admission_dispositions") != expected_rcae_dispositions:
        raise ValidationError("RCAE admission dispositions are not exact and unselected")

    expected_roles = set(manifest["required_return_artifact_roles"])
    embedded = closeout["source_artifact_manifest"]
    roles: set[str] = set()
    artifact_checks: list[dict[str, Any]] = []
    for entry in embedded:
        role = entry.get("artifact_role") or entry.get("source_role")
        if not isinstance(role, str) or role in roles:
            raise ValidationError("N31 return artifact roles are missing or duplicated")
        roles.add(role)
        path = entry["path"]
        require_portable(path, f"N31 artifact path for {role}")
        data = revision_bytes(graph_root, closeout_revision, path)
        expected_sha = entry.get("sha256") or entry.get("actual_sha256")
        expected_output = entry.get("output_digest") or entry.get(
            "actual_output_digest"
        )
        if sha256(data) != expected_sha:
            raise ValidationError(f"N31 artifact exact-file digest mismatch: {role}")
        value = read_json_bytes(data, role)
        require_internal_digest(value, expected_output, role)
        artifact_checks.append(
            {"role": role, "sha256": expected_sha, "output_digest": expected_output}
        )
    if roles != expected_roles:
        raise ValidationError("N31 return artifact role set is not exact")

    recommendation = closeout["p2_i3_return_recommendation"]
    if recommendation.get("automatic_adoption_allowed") is not False:
        raise ValidationError("N31 recommendation permits automatic RCAE adoption")
    if recommendation.get("N31_positive_evidence_re_admitted_to_RCAE") is not False:
        raise ValidationError("N31 positive evidence was silently re-admitted")
    if recommendation.get("RCAE_ecology_evidence_must_be_generated_fresh") is not True:
        raise ValidationError("fresh RCAE ecology evidence is not required")
    if recommendation.get("rcae_source_revision") != demand_revision:
        raise ValidationError("N31 recommendation names the wrong RCAE demand source")

    for provider in manifest["provider_contract_options"]:
        if provider.get("selection_status") != "admitted_option_not_selected":
            raise ValidationError("provider option is not explicitly unselected")
        route = recommendation["semantic_routes"][provider["semantic_route"]]
        for field in (
            "candidate_id",
            "contract_artifact_path",
            "contract_artifact_sha256",
            "contract_output_digest",
            "authority_ceiling",
            "executed_rung",
            "contract_only_rung",
            "producer_residue",
            "naturalization_debt",
            "consumer_control_set",
            "forbidden_claims",
        ):
            if route[field] != provider[field]:
                raise ValidationError(
                    f"provider projection drift: {provider['semantic_route']}/{field}"
                )

    source_pyproject = tomllib.loads(
        revision_bytes(graph_root, source_anchor, "pyproject.toml").decode("utf-8")
    )
    declared_version = source_pyproject["project"]["version"]
    installed_version = graph_python_version(graph_python)
    installed_module_path = graph_python_module_path(graph_python)
    expected_module_path = (graph_root / "src/pygrc/__init__.py").resolve()
    if installed_module_path != expected_module_path:
        raise ValidationError("graph Python does not import the admitted graph source")
    protected_source_changes = git_text(
        graph_root,
        "diff",
        "--name-only",
        source_anchor,
        closeout_revision,
        "--",
        "src/pygrc",
    )
    if protected_source_changes:
        raise ValidationError("protected PyGRC source changed across N31 I12 closeout")
    discrepancy = manifest["environment_identity_discrepancy"]
    observed = {
        "retained_closeout_pygrc_version": closeout["pygrc_version"],
        "source_declared_pygrc_version": declared_version,
        "reconstruction_environment_pygrc_version": installed_version,
    }
    for key, value in observed.items():
        if discrepancy[key] != value:
            raise ValidationError(f"environment discrepancy projection drift: {key}")
    if discrepancy["disposition"] != (
        "bounded_distribution_metadata_error_no_provider_contract_effect"
    ):
        raise ValidationError("distribution metadata error is not bounded")
    if discrepancy.get("owner_disposition") != "distribution_metadata_error":
        raise ValidationError("owner distribution-metadata disposition is absent")
    if discrepancy.get("supporting_checks") != {
        "editable_import_resolves_to_admitted_graph_source": True,
        "protected_pygrc_source_changed_between_source_anchor_and_closeout": False,
    }:
        raise ValidationError("distribution-metadata supporting checks drift")
    if declared_version != installed_version or closeout["pygrc_version"] == declared_version:
        raise ValidationError("expected N31 environment identity discrepancy is absent")

    return {
        "status": "passed_with_bounded_distribution_metadata_error",
        "graph_checkout_merge_revision": merge_revision,
        "n31_closeout_commit": closeout_revision,
        "n31_evidence_source_anchor": source_anchor,
        "rcae_demand_source_revision": demand_revision,
        "n31_closeout_sha256": closeout_identity["sha256"],
        "n31_closeout_output_digest": closeout_identity["output_digest"],
        "verified_return_artifact_count": len(artifact_checks),
        "verified_return_artifacts": artifact_checks,
        "provider_options_admitted": [
            provider["candidate_id"] for provider in manifest["provider_contract_options"]
        ],
        "provider_selected": None,
        "environment_identity": observed,
        "distribution_metadata_error_support": {
            "editable_import_resolves_to_admitted_graph_source": True,
            "protected_pygrc_source_changed_between_source_anchor_and_closeout": False,
        },
        "evidence_effect": manifest["evidence_effect"],
    }


def reconstruct_closeout(
    manifest: dict[str, Any], graph_root: Path, graph_python: Path
) -> dict[str, Any]:
    identities = manifest["repository_identities"]
    source_anchor = identities["n31_evidence_source_anchor"]
    closeout_revision = identities["n31_closeout_commit"]
    experiment = PurePosixPath(manifest["n31_experiment_path"])
    script_relative = experiment / "scripts/build_n31_closeout_and_rcae_return_i12.py"
    output_relative = experiment / "outputs/n31_closeout_and_rcae_return_i12.json"
    trace_relative = experiment / "outputs/n31_i12_closeout_and_rcae_return_trace.json"
    artifact_dir = experiment / "outputs/n31_i12_closeout_and_rcae_return_artifacts"

    exact_names = {
        "n31_i12_B_R_reusable_contract.json",
        "n31_i12_C2_reusable_contract.json",
        "n31_i12_candidate_disposition_matrix.json",
        "n31_i12_claim_debt_and_nativeness_register.json",
        "n31_i12_rcae_p2_i3_recommendation.json",
    }
    source_authority_name = "n31_i12_source_authority_and_reconstruction.json"
    allowed_differences = {
        output_relative.as_posix(): set(
            manifest["reconstruction_difference_contract"]["closeout_json_pointers"]
        ),
        trace_relative.as_posix(): set(
            manifest["reconstruction_difference_contract"]["trace_json_pointers"]
        ),
        (artifact_dir / source_authority_name).as_posix(): set(
            manifest["reconstruction_difference_contract"][
                "source_authority_json_pointers"
            ]
        ),
    }

    with tempfile.TemporaryDirectory(prefix="p2-i3-n31-return-") as temp_text:
        temp = Path(temp_text)
        subprocess.run(
            ["git", "clone", "--quiet", "--no-checkout", str(graph_root), str(temp)],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(temp),
                "switch",
                "--quiet",
                "-c",
                "experiment-N31",
                source_anchor,
            ],
            check=True,
        )
        script_path = temp / script_relative
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_bytes(
            revision_bytes(graph_root, closeout_revision, script_relative.as_posix())
        )
        completed = subprocess.run(
            [str(graph_python), str(script_path)],
            cwd=temp,
            check=True,
            capture_output=True,
            text=True,
        )
        builder_receipt = json.loads(completed.stdout)
        if builder_receipt.get("status") != "passed":
            raise ValidationError("N31 closeout builder did not pass")

        exact_artifacts: list[str] = []
        bounded_artifacts: list[dict[str, Any]] = []
        paths = [output_relative, trace_relative]
        paths.extend(artifact_dir / name for name in sorted(exact_names))
        paths.append(artifact_dir / source_authority_name)
        for relative in paths:
            retained_bytes = revision_bytes(
                graph_root, closeout_revision, relative.as_posix()
            )
            rebuilt_bytes = (temp / relative).read_bytes()
            if retained_bytes == rebuilt_bytes:
                exact_artifacts.append(relative.as_posix())
                continue
            retained = read_json_bytes(retained_bytes, f"retained {relative}")
            rebuilt = read_json_bytes(rebuilt_bytes, f"rebuilt {relative}")
            actual_differences = json_diff_paths(retained, rebuilt)
            expected_differences = allowed_differences.get(relative.as_posix())
            if expected_differences is None or actual_differences != expected_differences:
                raise ValidationError(
                    f"unexpected reconstruction differences for {relative}: "
                    f"{sorted(actual_differences)}"
                )
            bounded_artifacts.append(
                {
                    "path": relative.as_posix(),
                    "difference_json_pointers": sorted(actual_differences),
                    "classification": "distribution_metadata_and_digest_cascade_only",
                }
            )

    if len(exact_artifacts) != 5 or len(bounded_artifacts) != 3:
        raise ValidationError("unexpected N31 exact/bounded reconstruction envelope")
    return {
        "status": "passed_with_bounded_distribution_metadata_error",
        "reconstruction_mode": "temporary_local_clone_at_n31_evidence_source_anchor",
        "builder_status": "passed",
        "exact_artifact_count": len(exact_artifacts),
        "exact_artifacts": exact_artifacts,
        "bounded_artifact_count": len(bounded_artifacts),
        "bounded_artifacts": bounded_artifacts,
        "scientific_or_provider_contract_difference": False,
        "graph_checkout_mutated": False,
    }


def build_result(
    manifest: dict[str, Any], graph_root: Path, graph_python: Path
) -> dict[str, Any]:
    source_validation = validate_source_transition(manifest, graph_root, graph_python)
    reconstruction = reconstruct_closeout(manifest, graph_root, graph_python)
    result = {
        "artifact_id": "P2-I3-N31-RETURN-VALIDATION-001",
        "artifact_version": "1.0",
        "status": "passed_with_bounded_distribution_metadata_error",
        "admission_id": manifest["admission_id"],
        "decision_id": manifest["decision_id"],
        "source_transition_validation": source_validation,
        "closeout_reconstruction": reconstruction,
        "selection_status": manifest["selection_status"],
        "claim_boundary": {
            "n31_graph_evidence_admitted": True,
            "provider_contracts_admitted_as_options": True,
            "provider_selected": False,
            "n31_positive_evidence_is_p2_i3_evidence": False,
            "p2_i3_candidate_execution_authorized": False,
            "q005_resolved": False,
        },
        "reproduction_commands": manifest["reconstruction"]["commands"],
    }
    result["output_digest"] = canonical_digest(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "reconstruct", "all"))
    parser.add_argument("--graph-root", type=Path, required=True)
    parser.add_argument("--graph-python", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / DEFAULT_RESULT)
    args = parser.parse_args()

    manifest = read_json(ROOT / MANIFEST)
    graph_root = args.graph_root.resolve()
    graph_python = (
        args.graph_python.resolve()
        if args.graph_python
        else graph_root / ".venv/bin/python"
    )
    if not graph_python.is_file():
        raise ValidationError("graph .venv Python is missing")

    if args.command == "validate":
        result = validate_source_transition(manifest, graph_root, graph_python)
    elif args.command == "reconstruct":
        result = reconstruct_closeout(manifest, graph_root, graph_python)
    else:
        result = build_result(manifest, graph_root, graph_python)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(canonical_json(result), encoding="utf-8")
    print(canonical_json(result), end="")


if __name__ == "__main__":
    main()
