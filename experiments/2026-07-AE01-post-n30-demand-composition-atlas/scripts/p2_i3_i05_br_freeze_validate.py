"""Validate the inactive P2-I3 B-R I05 freeze without invoking calibration."""

from __future__ import annotations

import argparse
import ast
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any

from jsonschema import Draft202012Validator


def _find_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("repository root not found")


ROOT = _find_root()
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
SCRIPTS = EXPERIMENT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ae01_tooling import (  # noqa: E402
    ContractError,
    digest_file,
    load_json,
    pretty_json_dumps,
    validate_portable_path,
)


POLICY_PATH = EXPERIMENT / "configs/p2_i3_br_i05_one_shot_policy.json"
FREEZE_PATH = EXPERIMENT / "contracts/p2-i3/i05-br-calibration-invocation-freeze.json"
I05_SCHEMA_PATH = EXPERIMENT / "contracts/p2-i3/i05-br-calibration-output.schema.json"
I04_SCHEMA_PATH = EXPERIMENT / "contracts/p2-i3/i04-br-machine-records.schema.json"
RETAINED_VALIDATION_PATH = EXPERIMENT / "contracts/p2-i3/i05-br-calibration-freeze-validation.json"
ACTIVATION_PATH = EXPERIMENT / "contracts/p2-i3/i05-br-calibration-launch-authorization.json"
BUILDER_PATH = EXPERIMENT / "scripts/p2_i3_i05_br_calibration.py"
WRAPPER_PATH = EXPERIMENT / "scripts/p2_i3_i05_br_one_shot.py"
TEST_PATH = EXPERIMENT / "implementation/tests/test_p2_i3_i05_br_freeze.py"
SOURCE_ANCHOR = "1097547ad30b77d4cf9312fb05753902f6d1cc81"
EXPECTED_SOURCE_KEYS = {
    "i04_analysis",
    "i04_machine_policy",
    "i04_preregistration",
    "i04_schema",
    "i04_validation",
    "i05_builder",
    "i05_policy",
    "i05_schema",
    "i05_tests",
    "i05_validator",
    "i05_wrapper",
    "metric_sheet",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def _load(path: Path) -> dict[str, Any]:
    value = load_json(path)
    _require(isinstance(value, dict), f"expected JSON object: {path.relative_to(ROOT)}")
    return value


def _check(
    checks: list[dict[str, Any]], check_id: str, condition: bool, finding: str, evidence: Any
) -> None:
    _require(condition, f"{check_id}: {finding}")
    checks.append(
        {
            "check_id": check_id,
            "evidence": evidence,
            "finding": finding,
            "status": "passed",
        }
    )


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    return sorted(imported)


def _function_arguments(path: Path, name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    )
    return {
        argument.arg
        for argument in (*function.args.posonlyargs, *function.args.args, *function.args.kwonlyargs)
    }


def validate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    policy = _load(POLICY_PATH)
    freeze = _load(FREEZE_PATH)
    i04_schema = _load(I04_SCHEMA_PATH)
    i05_schema = _load(I05_SCHEMA_PATH)

    _check(
        checks,
        "I05F-001",
        _git("rev-parse", f"{SOURCE_ANCHOR}^{{commit}}") == SOURCE_ANCHOR,
        "accepted I04 source anchor exists",
        SOURCE_ANCHOR,
    )
    _git("merge-base", "--is-ancestor", SOURCE_ANCHOR, "HEAD")
    _check(checks, "I05F-002", True, "accepted I04 source anchor is an ancestor", "passed")

    _check(
        checks,
        "I05F-003",
        policy.get("artifact_id") == "P2-I3-I05-BR-ONE-SHOT-POLICY"
        and policy.get("artifact_version") == "1.0.2"
        and freeze.get("artifact_id") == "P2-I3-I05-BR-CALIBRATION-INVOCATION-FREEZE"
        and freeze.get("artifact_version") == "1.0.2",
        "policy and freeze identities are exact",
        {"freeze": freeze.get("artifact_id"), "policy": policy.get("artifact_id")},
    )

    source_hashes = freeze.get("source_hashes", {})
    _check(
        checks,
        "I05F-004",
        set(source_hashes) == EXPECTED_SOURCE_KEYS,
        "freeze binds the exact twelve-source identity set",
        sorted(source_hashes),
    )
    for index, (name, binding) in enumerate(sorted(source_hashes.items()), start=5):
        relative = validate_portable_path(binding["path"])
        actual = digest_file(ROOT / relative)
        _check(
            checks,
            f"I05F-{index:03d}",
            actual == binding["sha256"],
            f"source identity matches: {name}",
            {"path": relative, "sha256": actual},
        )

    frozen_i04 = policy["frozen_i04_hashes"]
    i04_bindings = {
        "analysis": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i04_br_analysis.py",
        "machine_policy": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i3_br_i04_machine_policy.json",
        "machine_schema": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i04-br-machine-records.schema.json",
        "metric_sheet": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/metric-sheets/AE01-L03.json",
        "preregistration": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i04-br-calibration-preregistration.json",
        "retained_validation": "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i04-br-calibration-preregistration-validation.json",
    }
    for offset, (name, relative) in enumerate(sorted(i04_bindings.items()), start=17):
        actual = digest_file(ROOT / relative)
        _check(
            checks,
            f"I05F-{offset:03d}",
            actual == frozen_i04[name],
            f"accepted I04 identity is unchanged: {name}",
            actual,
        )

    construction = policy["calibration_construction"]
    _check(
        checks,
        "I05F-023",
        construction["q_probe"] == {"rational": "1/2", "value": 0.5}
        and construction["carrier_formula"] == "c_pre_m_e = 1/2 + registered_margin"
        and construction["minimum_carrier_coherence"] == "0"
        and construction["maximum_carrier_coherence"] == "1",
        "DEC-041 half-unit arithmetic construction is exact and bounded",
        construction,
    )
    _check(
        checks,
        "I05F-024",
        construction["candidate_shaped_arguments_allowed"] is False
        and policy["candidate_blindness"]
        == {
            "candidate_artifacts_allowed": False,
            "candidate_execution_authorized": False,
            "candidate_seed_values_allowed": False,
            "candidate_shaped_inputs_allowed": False,
            "pygrc_import_allowed": False,
            "pygrc_runtime_inputs_allowed": False,
            "scientific_effect": "none",
        },
        "candidate and PyGRC inputs are mechanically prohibited",
        policy["candidate_blindness"],
    )

    invocation = policy["governed_invocation"]
    _check(
        checks,
        "I05F-025",
        invocation["calibration_invocation_authorized"] is False
        and invocation["candidate_execution_authorized"] is False
        and invocation["builder_invocations"] == 1
        and invocation["exact_null_case_count"] == 5
        and invocation["expected_response_record_count"] == 15
        and invocation["non_delta_conformance_case_count"] == 8,
        "the inactive invocation has the exact finite calibration envelope",
        invocation,
    )
    _check(
        checks,
        "I05F-025A",
        construction["calibrated_relation_ids"] == ["m_trace", "m_export"]
        and construction["exact_entered_case_ids"]
        == ["EQ-NEG-HALF", "EQ-NEG-QUARTER", "EQ-ZERO", "EQ-POS-QUARTER", "EQ-POS-HALF"]
        and construction["entered_margin_count"] == 10
        and construction["margins_per_case"] == {"m_trace": 1, "m_export": 1}
        and construction["shared_delta_formula"]
        == "max(measurement_resolution, max(abs(m_trace[c]), abs(m_export[c])) for c in entered_case_ids)",
        "shared delta is explicitly bound to both estimators and all ten margins",
        {
            "calibrated_relation_ids": construction["calibrated_relation_ids"],
            "entered_case_ids": construction["exact_entered_case_ids"],
            "entered_margin_count": construction["entered_margin_count"],
        },
    )
    attempt = policy["attempt_policy"]
    _check(
        checks,
        "I05F-026",
        attempt["max_governed_attempts"] == 1
        and attempt["max_infrastructure_retries"] == 0
        and attempt["consume_before_builder"] is True
        and attempt["claim_deletion_forbidden"] is True
        and attempt["claim_parent_directory_fsync_required"] is True,
        "one permanent pre-builder claim and zero retries are frozen",
        attempt,
    )

    for relative in policy["outputs"].values():
        validate_portable_path(relative)
    absent = {
        name: os.path.lexists(ROOT / relative)
        for name, relative in policy["outputs"].items()
    }
    _check(
        checks,
        "I05F-027",
        not any(absent.values()),
        "all governed outputs and the permanent claim are absent",
        absent,
    )
    _check(
        checks,
        "I05F-028",
        not ACTIVATION_PATH.exists(),
        "separate launch authorization is absent",
        str(ACTIVATION_PATH.relative_to(ROOT)),
    )

    expected_command = [
        ".venv/bin/python",
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_one_shot.py",
        "--policy",
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i3_br_i05_one_shot_policy.json",
        "--activation",
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-launch-authorization.json",
        "--expected-head",
        "<OWNER_AUTHORIZED_FULL_HEAD>",
    ]
    _check(
        checks,
        "I05F-029",
        policy["normalized_command_template"] == expected_command,
        "future launch command is exact and repository-relative",
        expected_command,
    )

    all_imports = _imports(BUILDER_PATH) + _imports(WRAPPER_PATH) + _imports(Path(__file__))
    _check(
        checks,
        "I05F-030",
        not any(name == "pygrc" or name.startswith("pygrc.") for name in all_imports),
        "builder, wrapper, and validator import no PyGRC module",
        sorted(set(all_imports)),
    )
    arguments = _function_arguments(BUILDER_PATH, "build_calibration_outputs")
    _check(
        checks,
        "I05F-031",
        arguments == {"i04_policy", "metric_sheet", "source_metric_sheet_sha256"}
        and not any(
            token in name
            for name in arguments
            for token in ("candidate", "runtime", "pygrc")
        ),
        "complete builder accepts only frozen authority inputs",
        sorted(arguments),
    )
    wrapper_source = WRAPPER_PATH.read_text(encoding="utf-8")
    claim_offset = wrapper_source.index('_exclusive_write(outputs["attempt_claim"], claim)')
    postclaim_offset = wrapper_source.index("validate_postclaim(", claim_offset)
    _check(
        checks,
        "I05F-032",
        claim_offset
        < postclaim_offset
        < wrapper_source.index("from p2_i3_i05_br_calibration import (")
        < wrapper_source.index("built = build_calibration_outputs("),
        "permanent durable claim and post-claim revalidation precede builder import and invocation",
        "claim < post-claim revalidation < import < invocation",
    )

    Draft202012Validator.check_schema(i04_schema)
    Draft202012Validator.check_schema(i05_schema)
    _check(
        checks,
        "I05F-033",
        i05_schema.get("$id") == "urn:rcae:ae01:p2-i3:i05-br-calibration-output:1.0.2"
        and len(i05_schema.get("oneOf", [])) == 6
        and {"attempt_claim", "final_receipt", "launch_authorization", "matched_null", "metric_calibration", "frozen_metric_sheet"}
        <= set(i05_schema.get("$defs", {}))
        and all(
            i05_schema["$defs"][name].get("additionalProperties") is False
            for name in ("attempt_claim", "final_receipt", "launch_authorization")
        )
        and {
            "claim_id", "activation", "launch_head", "accepted_freeze_commit",
            "accepted_freeze_sha256", "bound_source_sha256", "normalized_command",
            "interpreter", "output_paths", "governed_attempt", "builder_invocation_ceiling",
        }
        <= set(i05_schema["$defs"]["attempt_claim"]["required"])
        and {
            "claim_id", "claim_sha256", "activation_artifact_id", "activation_sha256",
            "launch_head", "builder_invocation_count", "response_record_count",
            "case_count", "triplet_count", "entered_margin_count", "output_bindings", "schema_validation", "semantic_validation",
            "readback_validation", "delta", "calibrated_relation_ids", "attempt_consumed",
            "completion_status", "second_start_evidence",
        }
        <= set(i05_schema["$defs"]["final_receipt"]["required"]),
        "I05 schema closes three outputs plus activation, claim, and final receipt",
        {"definitions": sorted(i05_schema.get("$defs", {})), "root_classes": len(i05_schema.get("oneOf", []))},
    )
    _check(
        checks,
        "I05F-033A",
        'validate_calibration_outputs(' in wrapper_source
        and wrapper_source.count('validate_calibration_outputs(') == 2
        and 'validate_consumable_closeout(' in wrapper_source
        and policy["record_contracts"]["output_admission"]["delta_admitted_without_successful_receipt"] is False,
        "semantic readback and fail-closed output admission are mechanically bound",
        policy["record_contracts"],
    )
    activation_required = set(i05_schema["$defs"]["launch_authorization"]["required"])
    _check(
        checks,
        "I05F-033B",
        {
            "accepted_freeze_commit", "freeze_sha256", "authority_sha256",
            "normalized_command_prefix", "interpreter_environment", "attempt_claim_path",
            "governed_paths", "launch_head_binding_method",
        }
        <= activation_required
        and policy["record_contracts"]["activation"]["launch_head_binding_method"]
        == "runtime_expected_head_verified_clean_and_retained_in_claim_and_receipt",
        "launch authorization meaning is frozen without a circular self-commit field",
        sorted(activation_required),
    )
    builder_source = BUILDER_PATH.read_text(encoding="utf-8")
    test_source = TEST_PATH.read_text(encoding="utf-8")
    _check(
        checks,
        "I05F-033C",
        "def exact_triplet_margins(" in builder_source
        and 'Fraction(str(triplet[key]["normalized_margin"]))' not in builder_source
        and '"entered_margins"' in builder_source
        and "test_exact_margin_path_never_round_trips_through_projected_float" in test_source,
        "delta inputs are derived from exact rational response fields before projection",
        "exact_triplet_margins plus retained exact entered-margin ledger",
    )
    _check(
        checks,
        "I05F-033D",
        freeze["invocation_envelope"]["injected_failure_boundaries_tested"] == 13
        and "test_transaction_failure_boundaries_fail_closed" in test_source
        and 'os.fsync(parent_descriptor)' in wrapper_source
        and '== f"?? {claim_relative}"' in wrapper_source,
        "durability, TOCTOU closure, and thirteen fail-closed transaction boundaries are tested",
        {
            "failure_boundaries": 13,
            "file_and_parent_fsync": True,
            "post_claim_status": "exact claim only",
        },
    )

    environment = policy["environment"]
    _check(
        checks,
        "I05F-034",
        platform.python_version() == environment["python"]
        and version("jsonschema") == environment["jsonschema"]
        and version("pytest") == environment["pytest"]
        and Path(sys.prefix).resolve() == (ROOT / ".venv").resolve()
        and sys.prefix != sys.base_prefix
        and digest_file(Path(sys.executable).resolve()) == environment["interpreter_binary_sha256"]
        and environment["required_process_environment"]
        == {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"}
        and all(
            os.environ.get(name) == value
            for name, value in environment["required_process_environment"].items()
        ),
        "active .venv and frozen packages/interpreter are available",
        {
            "interpreter_command": environment["interpreter_command"],
            "jsonschema": version("jsonschema"),
            "pytest": version("pytest"),
            "python": platform.python_version(),
        },
    )
    pygrc_loaded = sorted(
        name for name in sys.modules if name == "pygrc" or name.startswith("pygrc.")
    )
    _check(
        checks,
        "I05F-035",
        not pygrc_loaded,
        "freeze validation loaded no PyGRC module",
        pygrc_loaded,
    )

    boundary = freeze["gate_boundary"]
    _check(
        checks,
        "I05F-036",
        boundary["freeze_active"] is False
        and boundary["calibration_invocations"] == 0
        and boundary["delta_assigned"] is False
        and boundary["candidate_execution_authorized"] is False
        and boundary["next_permitted_action"] == "owner review and retention commit only",
        "freeze is inactive and opens no calibration or scientific authority",
        boundary,
    )
    _check(
        checks,
        "I05F-037",
        freeze["test_count"] == 50,
        "focused zero-calibration test count is frozen",
        freeze["test_count"],
    )

    return {
        "artifact_id": "P2-I3-I05-BR-CALIBRATION-FREEZE-VALIDATION",
        "artifact_version": "1.0.2",
        "branch_id": "P2-I3-BR",
        "check_count": len(checks),
        "checks": checks,
        "evidence_effect": "inactive_invocation_integrity_only",
        "gate_boundary": boundary,
        "iteration_id": "P2-I3-I05",
        "lane_id": "AE01-L03",
        "reconstruction": {
            "artifact_construction_command": ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_freeze_validate.py --artifact-construction --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-freeze-validation.json",
            "compare_command": "cmp experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-freeze-validation.json outputs/reconstruction/p2-i3-i05-freeze-validation.reconstructed.json",
            "rebuild_command": ".venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_freeze_validate.py --output outputs/reconstruction/p2-i3-i05-freeze-validation.reconstructed.json",
        },
        "source_hashes": source_hashes,
        "status": "inactive_freeze_review_ready",
        "test_count": freeze["test_count"],
        "validator": {
            "path": str(Path(__file__).relative_to(ROOT)),
            "sha256": digest_file(Path(__file__)),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-construction", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    output = arguments.output.resolve()
    retained = RETAINED_VALIDATION_PATH.resolve()
    if output == retained and not arguments.artifact_construction:
        raise ContractError("refusing to overwrite retained validation without artifact-construction mode")
    if arguments.artifact_construction and output != retained:
        raise ContractError("artifact-construction mode is valid only for the retained validation path")
    result = validate()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(pretty_json_dumps(result), encoding="utf-8")
    print(f"P2-I3 I05 inactive freeze valid: {result['check_count']}/{result['check_count']}; calibration invocations=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
