"""Focused candidate-free tests for the P2-I2 I07A isolated execution freeze."""

from __future__ import annotations

import ast
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "experiments" / "2026-07-AE01-post-n30-demand-composition-atlas"
SOURCE = EXPERIMENT / "scripts" / "p2_i2_execution.py"


def _load_execution():
    spec = importlib.util.spec_from_file_location("p2_i2_execution_under_test", SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


execution = _load_execution()


def _json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_source_import_is_candidate_free() -> None:
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    top_level_imports = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            top_level_imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            top_level_imports.append(node.module or "")
    assert not any(name == "pygrc" or name.startswith("pygrc.") for name in top_level_imports)
    assert not any(name.startswith("p2_i2_i06") for name in top_level_imports)
    assert not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules)


def test_effective_policy_is_exact_successor_composition() -> None:
    effective, successor, overlay = execution.load_effective_policy(ROOT)
    base = _json(successor["composition"]["base_blocked_policy"]["path"])
    assert "blocked" in base["status"]
    assert len(base["known_registration_blockers"]) == 3
    assert effective["known_registration_blockers"] == []
    assert effective["cycle_id"] == successor["cycle_id"] == "P2-I2-C01"
    assert effective["branch_plans"] == base["branch_plans"]
    assert effective["resource_envelope_per_entry"] == base["resource_envelope_per_entry"]
    assert all(row["status"] == "closed_by_accepted_I06B" for row in successor["blocker_dispositions"])
    assert overlay["artifact_id"] == "P2-I2-I06B-EXECUTION-READINESS-OVERLAY"


def test_matrix_is_complete_unique_and_order_exact() -> None:
    effective, successor, _ = execution.load_effective_policy(ROOT)
    rows = execution.expand_run_matrix(effective)
    assert len(rows) == successor["matrix"]["primary_entry_count"] == 234
    assert len({row["entry_id"] for row in rows}) == 234
    counts = {
        mode: sum(row["mode"] == mode for row in rows) // len(successor["matrix"]["seeds"])
        for mode in effective["matrix"]["mode_order"]
    }
    assert counts == {"state_carried": 24, "history_carried": 25, "hybrid": 29}
    two_order_branches = {
        "combined-orders",
        "physical_order_reverse",
        "q1_admitted_q2_diverted",
        "q2_admitted_q1_diverted",
    }
    for row in rows:
        expected_orders = {"q1_then_q2", "q2_then_q1"} if row["branch_id"] in two_order_branches else {"not_applicable"}
        observed_orders = {
            item["physical_order_id"]
            for item in rows
            if item["mode"] == row["mode"] and item["branch_id"] == row["branch_id"]
        }
        assert observed_orders == expected_orders


def test_paths_and_commands_are_relative_unique_and_exact() -> None:
    effective, successor, _ = execution.load_effective_policy(ROOT)
    rows = execution.expand_run_matrix(effective)
    path_fields = (
        "primary_output_path",
        "retry_output_path",
        "primary_claim_path",
        "retry_claim_path",
    )
    all_paths = [row[field] for row in rows for field in path_fields]
    for row in rows:
        all_paths.extend(
            execution._output_path(successor["artifact_contract"]["failure_receipt_template"], row, attempt)
            for attempt in (1, 2)
        )
    assert len(all_paths) == 1404
    assert len(all_paths) == len(set(all_paths))
    assert all(not Path(value).is_absolute() for value in all_paths)
    assert all(Path(value).parts[: len(execution.OUTPUT_ROOT_REL.parts)] == execution.OUTPUT_ROOT_REL.parts for value in all_paths)
    invocation = successor["runtime_invocation_identity"]
    assert invocation["python_command"] == ".venv/bin/python"
    assert invocation["python_flags"] == ["-B"]
    assert invocation["dont_write_bytecode_required"] is True
    assert invocation["graph_root_argument"] == "../graph-reflexive-coherence"
    assert not Path(invocation["graph_root_argument"]).is_absolute()
    sample = rows[0]
    expected_head = "a" * 40
    argv = execution.normalized_run_argv(successor, sample, 1, expected_head)
    values = {
        **sample,
        "attempt": 1,
        "output_path": sample["primary_output_path"],
        "expected_head": expected_head,
    }
    assert argv == [token.format(**values) for token in invocation["argument_order"]]
    assert sample["normalized_primary_argv_template"] == execution.normalized_run_argv(
        successor, sample, 1, "<OWNER_AUTHORIZED_FULL_HEAD>"
    )


def test_generated_freeze_is_inactive_and_byte_linked() -> None:
    successor = _json("experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i2_c01_execution_policy_v2.json")
    artifacts = successor["artifact_contract"]
    matrix = _json(artifacts["run_matrix_path"])
    binding = _json(artifacts["binding_receipt_path"])
    freeze = _json(artifacts["exec_freeze_path"])
    assert matrix["primary_entry_count"] == 234
    assert matrix["semantic_digest"] == execution.digest({key: value for key, value in matrix.items() if key != "semantic_digest"})
    assert binding["run_matrix"]["semantic_digest"] == matrix["semantic_digest"]
    assert binding["canonical_payload_digest"] == execution.digest({key: value for key, value in binding.items() if key != "canonical_payload_digest"})
    assert freeze["candidate_execution_authorized"] is False
    assert freeze["I08_authorized"] is False
    assert freeze["commit_authorized"] is False
    assert freeze["activation_record"]["present_at_freeze"] is False
    assert execution.sha256(ROOT / artifacts["run_matrix_path"]) == freeze["bound_identity"]["run_matrix_file_sha256"]
    assert execution.sha256(ROOT / artifacts["binding_receipt_path"]) == freeze["bound_identity"]["binding_receipt_file_sha256"]
    assert matrix["iteration_id"] == binding["iteration_id"] == freeze["iteration_id"] == "P2-I2-I07A"
    assert freeze["bound_identity"]["i07a_input_freeze_sha256"] == execution.sha256(ROOT / execution.I07A_INPUT_REL)


def test_atomic_claim_refuses_a_second_start(tmp_path: Path) -> None:
    claim = execution.OUTPUT_ROOT_REL / "claims" / "permanent" / "claim.json"
    execution._exclusive_json(tmp_path, claim, {"attempt": 1})
    with pytest.raises(FileExistsError):
        execution._exclusive_json(tmp_path, claim, {"attempt": 2})
    assert execution._read_governed_json(tmp_path, claim) == {"attempt": 1}


def test_governed_artifact_rejects_escape_and_symlink_parent(tmp_path: Path) -> None:
    with pytest.raises(execution.ContractError):
        execution._exclusive_json(tmp_path, Path("..") / "escape.json", {"unsafe": True})
    output_root = tmp_path / execution.OUTPUT_ROOT_REL
    output_root.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    (output_root / "claims").symlink_to(outside, target_is_directory=True)
    with pytest.raises(execution.ContractError):
        execution._exclusive_json(
            tmp_path,
            execution.OUTPUT_ROOT_REL / "claims" / "shadow.json",
            {"unsafe": True},
        )
    assert list(outside.iterdir()) == []


def test_import_cache_detection_is_explicit_and_row_external(tmp_path: Path) -> None:
    import_root = tmp_path / "imports"
    (import_root / "package").mkdir(parents=True)
    assert execution._find_import_cache_artifacts((("fixture", import_root),)) == []
    (import_root / "package" / "__pycache__").mkdir()
    violations = execution._find_import_cache_artifacts((("fixture", import_root),))
    assert violations == ["fixture:package/__pycache__:bytecode_cache"]


def _retry_fixture(root: Path, *, failure_entry_id: str = "entry-1"):
    expected_head = "a" * 40
    entry = {
        "cycle_id": "P2-I2-C01",
        "entry_id": "entry-1",
        "mode": "state_carried",
        "cell_id": "cell",
        "branch_id": "branch",
        "physical_order_id": "not_applicable",
        "seed": 101,
        "primary_output_path": (execution.OUTPUT_ROOT_REL / "runs" / "entry-1" / "attempt-1.json").as_posix(),
        "retry_output_path": (execution.OUTPUT_ROOT_REL / "retries" / "entry-1" / "attempt-2.json").as_posix(),
    }
    artifacts = {
        "claim_template": (execution.OUTPUT_ROOT_REL / "claims" / "{entry_id}" / "attempt-{attempt}.json").as_posix(),
        "failure_receipt_template": (execution.OUTPUT_ROOT_REL / "failures" / "{entry_id}" / "attempt-{attempt}.json").as_posix(),
        "exec_freeze_path": "authority/exec-freeze.json",
    }
    successor = {
        "artifact_contract": artifacts,
        "runtime_invocation_identity": {
            "argument_order": [
                "run-entry",
                "--expected-head",
                "{expected_head}",
                "--mode",
                "{mode}",
                "--cell-id",
                "{cell_id}",
                "--branch-id",
                "{branch_id}",
                "--physical-order-id",
                "{physical_order_id}",
                "--seed",
                "{seed}",
                "--attempt",
                "{attempt}",
                "--output",
                "{output_path}",
            ]
        },
    }
    for relative, value in (
        (execution.POLICY_REL, "policy"),
        (execution.SOURCE_REL, "source"),
        (Path(artifacts["exec_freeze_path"]), "freeze"),
    ):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
    freeze_path = root / artifacts["exec_freeze_path"]
    primary_argv = execution.normalized_run_argv(successor, entry, 1, expected_head)
    claim_relative, failure_relative, _ = execution._retry_predecessor_paths(artifacts, entry)
    claim = {
        "artifact_id": "P2-I2-C01-PERMANENT-ATTEMPT-CLAIM",
        "entry_id": entry["entry_id"],
        "attempt": 1,
        "owner_authorized_full_HEAD": expected_head,
        "normalized_command": [".venv/bin/python", "-B", execution.SOURCE_REL.as_posix(), *primary_argv],
        "inactive_exec_freeze_sha256": execution.sha256(freeze_path),
    }
    execution._exclusive_json(root, claim_relative, claim)
    failure = {
        "artifact_id": "P2-I2-C01-ATTEMPT-FAILURE-RECEIPT",
        "entry_id": failure_entry_id,
        "attempt_index": 1,
        "claim_sha256": execution._governed_sha256(root, claim_relative),
        "inactive_exec_freeze_sha256": execution.sha256(freeze_path),
        "byte_identity_digests": {
            "owner_authorized_full_HEAD": expected_head,
            "normalized_argv": primary_argv,
            "policy_sha256": execution.sha256(root / execution.POLICY_REL),
            "execution_source_sha256": execution.sha256(root / execution.SOURCE_REL),
        },
        "zero_state_counters": {
            "pygrc_imports": 0,
            "model_or_adapter_construction_started": 0,
            "models_constructed": 0,
            "adapters_constructed": 0,
            "candidate_or_control_operations_started": 0,
            "governed_output_written": 0,
        },
        "output_absence": True,
        "retry_eligibility": True,
    }
    execution._exclusive_json(root, failure_relative, failure)
    return successor, entry, expected_head, freeze_path


def test_retry_reconstructs_only_its_current_entry_predecessor(tmp_path: Path) -> None:
    successor, entry, expected_head, freeze_path = _retry_fixture(tmp_path)
    result = execution._validate_retry_predecessor(tmp_path, successor, entry, expected_head, freeze_path)
    assert result["entry_id"] == entry["entry_id"]
    assert result["eligibility_reconstructed"] is True


def test_retry_refuses_another_entry_failure_receipt(tmp_path: Path) -> None:
    successor, entry, expected_head, freeze_path = _retry_fixture(tmp_path, failure_entry_id="entry-2")
    with pytest.raises(execution.ContractError, match="failure identity drift"):
        execution._validate_retry_predecessor(tmp_path, successor, entry, expected_head, freeze_path)


def _completion_fixture(root: Path, *, null_second: bool = False, omit_second: bool = False, duplicate_first: bool = False):
    expected_head = "b" * 40
    entries = []
    for index in (1, 2):
        identity = {
            "entry_id": f"entry-{index}",
            "mode": "state_carried",
            "cell_id": "cell",
            "branch_id": f"branch-{index}",
            "physical_order_id": "not_applicable",
            "seed": 100 + index,
        }
        entries.append(
            {
                **identity,
                "primary_output_path": (execution.OUTPUT_ROOT_REL / "runs" / identity["entry_id"] / "attempt-1.json").as_posix(),
                "retry_output_path": (execution.OUTPUT_ROOT_REL / "retries" / identity["entry_id"] / "attempt-2.json").as_posix(),
                "primary_claim_path": (execution.OUTPUT_ROOT_REL / "claims" / identity["entry_id"] / "attempt-1.json").as_posix(),
                "retry_claim_path": (execution.OUTPUT_ROOT_REL / "claims" / identity["entry_id"] / "attempt-2.json").as_posix(),
            }
        )
    artifacts = {
        "failure_receipt_template": (execution.OUTPUT_ROOT_REL / "failures" / "{entry_id}" / "attempt-{attempt}.json").as_posix(),
        "exec_freeze_path": "authority/exec-freeze.json",
        "run_matrix_path": "authority/run-matrix.json",
    }
    successor = {"artifact_contract": artifacts}
    matrix = {"primary_entry_count": 2, "semantic_digest": "fixture", "entries": entries}
    matrix_path = root / artifacts["run_matrix_path"]
    matrix_path.parent.mkdir(parents=True, exist_ok=True)
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
    for index, entry in enumerate(entries, start=1):
        if omit_second and index == 2:
            continue
        execution._exclusive_json(root, entry["primary_claim_path"], {"entry_id": entry["entry_id"]})
        output = {
            "entry_identity": {
                **{key: entry[key] for key in ("entry_id", "mode", "cell_id", "branch_id", "physical_order_id", "seed")},
                "attempt": 1,
            },
            "runtime_binding_receipt": {"owner_authorized_full_HEAD": expected_head},
            "raw_response_record": {
                "value": None if null_second and index == 2 else float(index),
                "operational_null": null_second and index == 2,
            },
            "window_validity_receipt": {"valid": not (null_second and index == 2)},
        }
        execution._exclusive_json(root, entry["primary_output_path"], output)
    if duplicate_first:
        first = entries[0]
        execution._exclusive_json(root, first["retry_claim_path"], {"entry_id": first["entry_id"]})
        duplicate = deepcopy(execution._read_governed_json(root, first["primary_output_path"]))
        duplicate["entry_identity"]["attempt"] = 2
        execution._exclusive_json(root, first["retry_output_path"], duplicate)
    return matrix, successor, expected_head


def test_completion_accepts_exactly_one_evaluable_terminal_per_row(tmp_path: Path) -> None:
    matrix, successor, expected_head = _completion_fixture(tmp_path)
    manifest = execution._execution_manifest_document(tmp_path, matrix, successor, expected_head)
    assert manifest["evaluable_terminal_count"] == 2
    assert manifest["missing_entry_count"] == 0


@pytest.mark.parametrize(
    "fixture_options",
    (
        {"omit_second": True},
        {"null_second": True},
        {"duplicate_first": True},
    ),
)
def test_completion_fails_closed_without_a_complete_evaluable_matrix(tmp_path: Path, fixture_options: dict) -> None:
    matrix, successor, expected_head = _completion_fixture(tmp_path, **fixture_options)
    with pytest.raises(execution.ContractError):
        execution._execution_manifest_document(tmp_path, matrix, successor, expected_head)


def test_absent_activation_refuses_before_runtime_import() -> None:
    successor = _json("experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i2_c01_execution_policy_v2.json")
    activation = ROOT / successor["artifact_contract"]["activation_record_path"]
    assert not activation.exists()
    assert not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules)
