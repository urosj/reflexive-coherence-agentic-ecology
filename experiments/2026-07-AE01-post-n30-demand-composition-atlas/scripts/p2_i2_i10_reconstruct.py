#!/usr/bin/env python3
"""Independent P2-I2 I10 retained-evidence reconstruction.

This script never invokes a C02 worker or regenerates a scientific entry.  Its
only live PyGRC activity is the frozen registered-baseline restoration and
no-packet continuation check for each retained dependence mode.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from enum import Enum
import hashlib
import importlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence

import jsonschema


EXPERIMENT = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
FREEZE_REL = f"{EXPERIMENT}/contracts/p2-i2/i10-reconstruction-input-freeze-v2.json"
BASE_FREEZE_REL = f"{EXPERIMENT}/contracts/p2-i2/i10-reconstruction-input-freeze.json"
FAILED_START_REL = f"{EXPERIMENT}/contracts/p2-i2/i10-reconstruction-failed-start.json"
MANIFEST_REL = f"{EXPERIMENT}/contracts/p2-i2/i10-reconstruction-manifest.json"
VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i10-reconstruction-validation.json"
REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I10-reconstruction-and-identity.md"
SCRIPT_REL = f"{EXPERIMENT}/scripts/p2_i2_i10_reconstruct.py"
I06_MANIFEST_REL = f"{EXPERIMENT}/contracts/p2-i2/i06-registration-manifest.json"
I06B_MANIFEST_REL = f"{EXPERIMENT}/contracts/p2-i2/i06b-execution-readiness-manifest.json"
REGISTRATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i06-three-mode-registration.json"
REGISTRATION_VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i06-registration-validation.json"
I06A_VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i06a-registration-review-validation.json"
I06_HISTORICAL_MANIFEST_REL = f"{EXPERIMENT}/contracts/p2-i2/i06-registration-execution-manifest.json"
MATRIX_REL = f"{EXPERIMENT}/contracts/p2-i2/c02/run-matrix.json"
EXECUTION_MANIFEST_REL = f"{EXPERIMENT}/contracts/p2-i2/c02/execution-manifest.json"
I09_FREEZE_REL = f"{EXPERIMENT}/contracts/p2-i2/i09-control-resolution-input-freeze.json"
I09_INDEX_REL = f"{EXPERIMENT}/contracts/p2-i2/i09-control-resolution-index.json"
I09_VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i09-control-resolution-validation.json"
I09_REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I09-control-resolution.md"
I09A_FREEZE_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-input-freeze.json"
I09A_INDEX_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-index.json"
I09A_VALIDATION_REL = f"{EXPERIMENT}/contracts/p2-i2/i09a-control-resolution-validation.json"
I09A_REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I09A-normalized-estimator-correction.md"
I08_REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I08-execution.md"
I05_REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I05J-metric-closeout.md"
I06_REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I06-exact-registration.md"
I06B_REPORT_REL = f"{EXPERIMENT}/reports/P2-I2-I06B-execution-readiness-correction.md"
GOVERNED_NULL_REL = f"{EXPERIMENT}/outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json"
CALIBRATION_PROJECTION_REL = f"{EXPERIMENT}/contracts/p2-i2/i05j-analysis-arithmetic-resolution-input.json"
CALIBRATION_REL = f"{EXPERIMENT}/contracts/p2-i2/metric-calibration.json"
FROZEN_SHEET_REL = f"{EXPERIMENT}/contracts/p2-i2/frozen-metric-sheet.json"
SCHEMA_REL = f"{EXPERIMENT}/contracts/schemas/ae01-contract.schema.json"
ANALYSIS_POLICY_REL = f"{EXPERIMENT}/configs/p2_i2_i04r1_analysis_policy.json"
MACHINE_POLICY_REL = f"{EXPERIMENT}/configs/p2_i2_i04r2_machine_policy.json"
MODES = ("state_carried", "history_carried", "hybrid")
ORDERS = ("q1_then_q2", "q2_then_q1")
SEEDS = (101, 211, 307)
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root is not an object: {path.name}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def canonical_digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git(root: Path, *args: str, text: bool = True) -> str | bytes:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    ).stdout


def git_blob(root: Path, commit: str, relative: str) -> bytes:
    return git(root, "show", f"{commit}:{relative}", text=False)  # type: ignore[return-value]


def normalize(value: Any) -> Any:
    if is_dataclass(value):
        return normalize(asdict(value))
    if isinstance(value, Enum):
        return normalize(value.value)
    if isinstance(value, Mapping):
        return {str(key): normalize(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if isinstance(value, set):
        return sorted(normalize(item) for item in value)
    if isinstance(value, Path):
        return value.name
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "__dict__"):
        return normalize(vars(value))
    return repr(value)


def close_structure(left: Any, right: Any, tolerance: float) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return left is right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return math.isclose(float(left), float(right), abs_tol=tolerance, rel_tol=0.0)
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        return set(left) == set(right) and all(close_structure(left[key], right[key], tolerance) for key in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(close_structure(a, b, tolerance) for a, b in zip(left, right))
    return left == right


def structure_differences(left: Any, right: Any, tolerance: float, path: str = "$") -> list[dict[str, Any]]:
    if isinstance(left, bool) or isinstance(right, bool):
        return [] if left is right else [{"path": path, "left": left, "right": right}]
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return [] if math.isclose(float(left), float(right), abs_tol=tolerance, rel_tol=0.0) else [{"path": path, "left": left, "right": right}]
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        differences: list[dict[str, Any]] = []
        for key in sorted(set(left) | set(right), key=str):
            child = f"{path}.{key}"
            if key not in left:
                differences.append({"path": child, "left": "<missing>", "right": normalize(right[key])})
            elif key not in right:
                differences.append({"path": child, "left": normalize(left[key]), "right": "<missing>"})
            else:
                differences.extend(structure_differences(left[key], right[key], tolerance, child))
        return differences
    if isinstance(left, list) and isinstance(right, list):
        differences = []
        if len(left) != len(right):
            differences.append({"path": f"{path}.length", "left": len(left), "right": len(right)})
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences.extend(structure_differences(left_item, right_item, tolerance, f"{path}[{index}]"))
        return differences
    return [] if left == right else [{"path": path, "left": normalize(left), "right": normalize(right)}]


def strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            yield from strings(key)
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def portable_json(value: Any) -> tuple[bool, list[str]]:
    findings = sorted(
        {
            text
            for text in strings(value)
            if text.startswith("/")
            or re.search(r"/home/[^/]+/", text)
            or re.search(r"[A-Za-z]:\\\\", text)
        }
    )
    return not findings, findings


def safe_relative(root: Path, relative: str) -> Path:
    require(relative and not relative.startswith("/"), f"absolute or empty path: {relative}")
    candidate = root / relative
    require(not candidate.is_symlink(), f"symlink artifact refused: {relative}")
    resolved_parent = candidate.parent.resolve()
    require(resolved_parent == root or root in resolved_parent.parents, f"artifact escapes repository: {relative}")
    return candidate


def import_file(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def materialize_freeze(root: Path, overlay: Mapping[str, Any]) -> dict[str, Any]:
    require(overlay["status"] == "frozen_for_governed_v2_resume", "I10 v2 freeze is not final")
    base_ref = overlay["base_freeze"]
    require(base_ref["path"] == BASE_FREEZE_REL, "I10 base-freeze path drift")
    require(sha256_file(root / BASE_FREEZE_REL) == base_ref["sha256"], "I10 base-freeze hash drift")
    failed_ref = overlay["failed_start_001"]
    require(failed_ref["path"] == FAILED_START_REL, "I10 failed-start path drift")
    require(sha256_file(root / FAILED_START_REL) == failed_ref["sha256"], "I10 failed-start hash drift")
    failed_v2_ref = overlay["failed_start_002"]
    require(failed_v2_ref["path"].endswith("i10-reconstruction-failed-start-002.json"), "I10 v2 failed-start path drift")
    require(sha256_file(root / failed_v2_ref["path"]) == failed_v2_ref["sha256"], "I10 v2 failed-start hash drift")
    failed_load_ref = overlay["failed_start_003"]
    require(failed_load_ref["path"].endswith("i10-reconstruction-failed-start-003.json"), "I10 load failed-start path drift")
    require(sha256_file(root / failed_load_ref["path"]) == failed_load_ref["sha256"], "I10 load failed-start hash drift")
    base = read_json(root / BASE_FREEZE_REL)
    require(base["status"] == "frozen_before_governed_start", "I10 v1 freeze drift")
    freeze = deepcopy(base)
    freeze.update({
        "artifact_id": overlay["artifact_id"],
        "artifact_version": overlay["artifact_version"],
        "status": overlay["status"],
        "entry_authority": overlay["entry_authority"],
        "builder_identity": overlay["builder_identity"],
        "local_correction_artifacts": overlay["local_correction_artifacts"],
        "failed_start_002": overlay["failed_start_002"],
        "failed_start_003": overlay["failed_start_003"],
        "restoration_continuation_policy": overlay["restoration_continuation_policy"],
        "v2_process_boundary": overlay["v2_process_boundary"],
        "v2_gate_boundary": overlay["v2_gate_boundary"],
    })
    return freeze


def validate_freeze(root: Path, freeze: Mapping[str, Any]) -> dict[str, Any]:
    require(freeze["status"] == "frozen_for_governed_v2_resume", "I10 v2 freeze is not final")
    require(freeze["builder_identity"]["path"] == SCRIPT_REL, "I10 builder path drift")
    require(freeze["builder_identity"]["sha256"] == sha256_file(root / SCRIPT_REL), "I10 builder hash drift")
    commit = freeze["retained_byte_authority"]["commit"]
    require(commit == str(git(root, "rev-parse", "cfa19fe^{commit}")).strip(), "retained byte authority drift")
    identities = []
    for entry in freeze["input_artifacts"]:
        relative = entry["path"]
        path = safe_relative(root, relative)
        actual = sha256_file(path)
        committed = sha256_bytes(git_blob(root, commit, relative))
        require(actual == entry["sha256"], f"frozen input hash drift: {relative}")
        require(committed == actual, f"frozen input differs from retained commit: {relative}")
        identities.append({"path": relative, "role": entry["role"], "sha256": actual})
    local_identities = []
    for entry in freeze["local_correction_artifacts"]:
        relative = entry["path"]
        path = safe_relative(root, relative)
        actual = sha256_file(path)
        require(actual == entry["sha256"], f"local correction hash drift: {relative}")
        local_identities.append({"path": relative, "role": entry["role"], "sha256": actual})
    require(Path(sys.executable).absolute() == (root / ".venv/bin/python").absolute(), "I10 must use lexical .venv/bin/python")
    require(Path(sys.prefix).resolve() == (root / ".venv").resolve(), "repository venv is inactive")
    require(sys.dont_write_bytecode, "I10 requires -B")
    require(platform.python_version() == freeze["runtime_identity"]["python_version"], "Python version drift")
    require(
        sha256_file(Path(sys.executable).resolve()) == freeze["runtime_identity"]["interpreter_executable_sha256"],
        "interpreter digest drift",
    )
    return {
        "committed_input_artifact_count": len(identities),
        "local_correction_artifact_count": len(local_identities),
        "input_artifact_count": len(identities) + len(local_identities),
        "retained_byte_authority": commit,
        "all_committed_bytes_equal": True,
        "all_hash_bound_local_correction_bytes_equal": True,
        "all_frozen_bytes_exact": True,
        "interpreter_identity": ".venv/bin/python",
        "interpreter_executable_sha256": freeze["runtime_identity"]["interpreter_executable_sha256"],
    }


def validate_graph(graph_root: Path, freeze: Mapping[str, Any]) -> dict[str, Any]:
    head = str(git(graph_root, "rev-parse", "HEAD")).strip()
    status = str(git(graph_root, "status", "--porcelain=v1", "--untracked-files=all"))
    require(head == freeze["runtime_identity"]["graph_revision"], "admitted graph revision drift")
    require(status == "", "graph worktree is not clean")
    return {"graph_revision": head, "graph_worktree_clean": True, "graph_identity": "external-repository:graph-reflexive-coherence"}


def validate_resolved_manifests(root: Path) -> dict[str, Any]:
    summaries = []
    reached: set[str] = set()
    for relative in (I06_MANIFEST_REL, I06B_MANIFEST_REL):
        manifest = read_json(root / relative)
        files = manifest["files"]
        for item in files:
            path = safe_relative(root, item["path"])
            require(path.exists(), f"resolved manifest input missing: {item['path']}")
            require(sha256_file(path) == item["sha256"], f"resolved manifest hash drift: {item['path']}")
            reached.add(item["path"])
        ok, findings = portable_json(manifest)
        require(ok, f"manifest contains absolute paths: {findings}")
        summaries.append({"path": relative, "file_count": len(files), "all_files_exact": True})
    i09_freeze = read_json(root / I09_FREEZE_REL)
    for item in i09_freeze["input_artifacts"]:
        path = safe_relative(root, item["path"])
        require(path.exists() and sha256_file(path) == item["sha256"], f"I09 input drift: {item['path']}")
        reached.add(item["path"])
    return {"resolved_manifests": summaries, "distinct_reached_path_count": len(reached), "all_reached_paths_exact": True}


def reconstruct_calibration(root: Path, analysis: Any) -> dict[str, Any]:
    governed = read_json(root / GOVERNED_NULL_REL)
    projection = read_json(root / CALIBRATION_PROJECTION_REL)
    calibration = read_json(root / CALIBRATION_REL)
    sheet = read_json(root / FROZEN_SHEET_REL)
    parent_policy = read_json(root / ANALYSIS_POLICY_REL)
    machine_policy = read_json(root / MACHINE_POLICY_REL)
    rows = governed["per_seed_order_three_arm_margins"]
    require(len(rows) == 10, "arithmetic null row count drift")
    rebuilt: list[dict[str, Any]] = []
    by_seed: dict[int, list[float]] = defaultdict(list)
    for row in rows:
        seed = int(row["seed"])
        order = row["physical_order_id"]
        pairing = f"I10-calibration-reconstruction:{seed}:{order}"
        values = (row["raw_candidate_response"], row["raw_leave_q1_response"], row["raw_leave_q2_response"])
        envelopes = []
        for suffix, branch, value in zip(("candidate", "q1-only", "q2-only"), ("combined-orders", "q1_admitted_q2_diverted", "q2_admitted_q1_diverted"), values):
            envelopes.append(
                analysis.build_synthetic_response_envelope(
                    record_id=f"I10-null:{seed}:{order}:{suffix}",
                    branch_id=branch,
                    response=float(value),
                    seed=seed,
                    physical_order_id=order,
                    carrier_state_digest=sha256_bytes(f"I10-null-carrier:{seed}:{order}:{suffix}".encode()),
                    pairing_identity=pairing,
                )
            )
        result = analysis.primary_margin(*envelopes, machine_policy, parent_policy)
        margin = float(result["normalized_margin"])
        require(margin == float(row["normalized_margin"]), "calibration estimator reconstruction drift")
        by_seed[seed].append(margin)
        rebuilt.append({"seed": seed, "physical_order_id": order, "normalized_margin": margin})
    seed_margins = [{"matched_null_margin": max(abs(value) for value in by_seed[seed]), "seed": seed} for seed in sorted(by_seed)]
    require(seed_margins == projection["seed_margins"], "calibration seed projection drift")
    measurement_resolution = float(sheet["record"]["resolution_policy"]["measurement_resolution"])
    delta = max(measurement_resolution, max(item["matched_null_margin"] for item in seed_margins))
    require(delta == float(calibration["record"]["delta"]) == 1e-12, "calibration delta drift")
    require(calibration["record"]["seed_margins"] == seed_margins, "metric calibration seed margins drift")
    require(sheet["record"]["resolution_policy"]["delta"]["value"] == delta, "frozen sheet delta drift")
    schema = read_json(root / SCHEMA_REL)
    jsonschema.Draft202012Validator(schema).validate(calibration)
    jsonschema.Draft202012Validator(schema).validate(sheet)
    return {
        "arithmetic_null_row_count": len(rows),
        "reconstructed_rows": rebuilt,
        "seed_margins": seed_margins,
        "analysis_arithmetic_delta": delta,
        "metric_calibration_schema_valid": True,
        "frozen_metric_sheet_schema_valid": True,
        "estimator_path_id": "p2-i2-i04r2-exact-three-arm-primary-estimator-v1",
    }


def failure_path(entry: Mapping[str, Any], attempt: int) -> str:
    return (
        f"{EXPERIMENT}/outputs/p2-i2/c02/failures/{entry['mode']}/{entry['cell_id']}/"
        f"{entry['branch_id']}/{entry['physical_order_id']}/seed-{entry['seed']}/attempt-{attempt}.json"
    )


def reconstruct_execution(root: Path, freeze: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    matrix = read_json(root / MATRIX_REL)
    retained = read_json(root / EXECUTION_MANIFEST_REL)
    i08_commit = freeze["accepted_lineage_commits"]["i08_execution_closeout"]
    require(len(matrix["entries"]) == 234, "C02 matrix row count drift")
    require([entry["sequence_index"] for entry in matrix["entries"]] == list(range(1, 235)), "C02 sequence drift")
    terminals: list[dict[str, Any]] = []
    loaded: dict[str, dict[str, Any]] = {}
    claim_count = 0
    retained_failure_count = 0
    heads: Counter[str] = Counter()
    pending: list[tuple[Mapping[str, Any], int, str, str, dict[str, Any]]] = []
    governed_paths: set[str] = set()
    for entry in matrix["entries"]:
        primary = safe_relative(root, entry["primary_output_path"])
        retry = safe_relative(root, entry["retry_output_path"])
        require(primary.exists() != retry.exists(), f"missing or ambiguous terminal: {entry['entry_id']}")
        attempt = 1 if primary.exists() else 2
        output_rel = entry["primary_output_path"] if attempt == 1 else entry["retry_output_path"]
        claim_rel = entry["primary_claim_path"] if attempt == 1 else entry["retry_claim_path"]
        output = safe_relative(root, output_rel)
        claim = safe_relative(root, claim_rel)
        require(claim.exists(), f"terminal claim missing: {entry['entry_id']}")
        require(sha256_bytes(git_blob(root, i08_commit, output_rel)) == sha256_file(output), f"terminal not retained at I08 commit: {output_rel}")
        require(sha256_bytes(git_blob(root, i08_commit, claim_rel)) == sha256_file(claim), f"claim not retained at I08 commit: {claim_rel}")
        claim_count += 1
        governed_paths.update((output_rel, claim_rel))
        record = read_json(output)
        identity = record["entry_identity"]
        for key in ("entry_id", "mode", "cell_id", "branch_id", "physical_order_id", "seed"):
            require(identity[key] == entry[key], f"terminal identity drift: {entry['entry_id']}:{key}")
        require(identity["attempt"] == attempt, "terminal attempt drift")
        require(record["cycle_id"] == "P2-I2-C02", "terminal cycle drift")
        require(record["raw_response_record"]["operational_null"] is False, "terminal operational null")
        require(record["window_validity_receipt"]["valid"] is True, "terminal invalid response window")
        require(record["scientific_interpretation"] is None, "terminal contains scientific interpretation")
        require(record["R01_through_R05"] == "unassigned_until_I09_I11", "terminal contains rung assignment")
        value = record["raw_response_record"]["value"]
        require(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)), "terminal response nonnumeric")
        head = record["runtime_binding_receipt"]["owner_authorized_full_HEAD"]
        require(re.fullmatch(r"[0-9a-f]{40}", head) is not None, "terminal execution HEAD invalid")
        heads[head] += 1
        pending.append((entry, attempt, output_rel, claim_rel, record))
        loaded[entry["entry_id"]] = record
        if attempt == 1:
            require(not safe_relative(root, entry["retry_claim_path"]).exists(), "retry claim exists after primary success")
            require(not safe_relative(root, failure_path(entry, 1)).exists(), "failure exists with primary success")
        else:
            first_claim = safe_relative(root, entry["primary_claim_path"])
            first_failure_rel = failure_path(entry, 1)
            first_failure = safe_relative(root, first_failure_rel)
            require(first_claim.exists() and first_failure.exists(), "retry predecessor incomplete")
            require(sha256_bytes(git_blob(root, i08_commit, entry["primary_claim_path"])) == sha256_file(first_claim), "retry predecessor claim retention drift")
            require(sha256_bytes(git_blob(root, i08_commit, first_failure_rel)) == sha256_file(first_failure), "retry predecessor failure retention drift")
            claim_count += 1
            retained_failure_count += 1
            governed_paths.update((entry["primary_claim_path"], first_failure_rel))
    require(len(heads) == 2 and sorted(heads.values()) == [1, 233], f"execution HEAD distribution drift: {heads}")
    current_head = heads.most_common(1)[0][0]
    for entry, attempt, output_rel, _claim_rel, record in pending:
        execution_head = record["runtime_binding_receipt"]["owner_authorized_full_HEAD"]
        authority = "current_execution_head" if execution_head == current_head else "accepted_checkpoint_head"
        require(authority == "current_execution_head" or (entry["sequence_index"] == 1 and attempt == 2), "unadmitted historical execution head")
        terminals.append(
            {
                "entry_id": entry["entry_id"],
                "attempt": attempt,
                "output_path": output_rel,
                "output_sha256": sha256_file(root / output_rel),
                "raw_response_value": float(record["raw_response_record"]["value"]),
                "execution_authority_kind": authority,
                "execution_head": execution_head,
            }
        )
    document: dict[str, Any] = {
        "artifact_id": "P2-I2-C02-EXECUTION-MANIFEST",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I08",
        "cycle_id": "P2-I2-C02",
        "status": "complete_all_registered_entries_evaluable",
        "owner_authorized_full_HEAD": current_head,
        "run_matrix_sha256": sha256_file(root / MATRIX_REL),
        "run_matrix_semantic_digest": matrix["semantic_digest"],
        "required_entry_count": 234,
        "evaluable_terminal_count": 234,
        "missing_entry_count": 0,
        "nonevaluable_entry_count": 0,
        "ambiguous_entry_count": 0,
        "terminals": terminals,
        "completion_rule": "exact_matrix_paths_only_all_234_exactly_one_terminal_and_all_evaluable",
        "execution_head_rule": "current_execution_head_except_exact_owner_accepted_entry_001_checkpoint",
        "scientific_interpretation": None,
    }
    document["canonical_payload_digest"] = canonical_digest(document)
    require(document == retained, "C02 execution manifest semantic reconstruction drift")
    require(pretty_bytes(document) == (root / EXECUTION_MANIFEST_REL).read_bytes(), "C02 execution manifest byte reconstruction drift")
    require(len(governed_paths) == 470, f"governed path count drift: {len(governed_paths)}")
    return document, loaded, {
        "matrix_entries": 234,
        "evaluable_terminals": 234,
        "permanent_claims": claim_count,
        "retained_failures": retained_failure_count,
        "distinct_governed_paths_verified": len(governed_paths),
        "primary_successes": sum(item["attempt"] == 1 for item in terminals),
        "accepted_retry_successes": sum(item["attempt"] == 2 for item in terminals),
        "unsafe_terminal_claims": 0,
        "manifest_byte_identical": True,
    }


def terminal_for(matrix: Mapping[str, Any], loaded: Mapping[str, dict[str, Any]], mode: str, cell: str, branch: str, order: str, seed: int) -> dict[str, Any]:
    matches = [
        entry for entry in matrix["entries"]
        if entry["mode"] == mode and entry["cell_id"] == cell and entry["branch_id"] == branch
        and entry["physical_order_id"] == order and entry["seed"] == seed
    ]
    require(len(matches) == 1, f"primary tuple lookup drift: {mode}/{cell}/{branch}/{order}/{seed}")
    return loaded[matches[0]["entry_id"]]


def reconstruct_margins(root: Path, analysis: Any, loaded: Mapping[str, dict[str, Any]]) -> list[dict[str, Any]]:
    matrix = read_json(root / MATRIX_REL)
    parent_policy = read_json(root / ANALYSIS_POLICY_REL)
    machine_policy = read_json(root / MACHINE_POLICY_REL)
    delta = float(read_json(root / CALIBRATION_REL)["record"]["delta"])
    rows: list[dict[str, Any]] = []
    for mode in MODES:
        for order in ORDERS:
            for seed in SEEDS:
                records = (
                    terminal_for(matrix, loaded, mode, "combined-orders", "combined-orders", order, seed),
                    terminal_for(matrix, loaded, mode, "contributor-removal", "q1_admitted_q2_diverted", order, seed),
                    terminal_for(matrix, loaded, mode, "contributor-removal", "q2_admitted_q1_diverted", order, seed),
                )
                values = [float(record["raw_response_record"]["value"]) for record in records]
                pairing = f"I10-retained-primary:{mode}:{order}:{seed}"
                envelopes = []
                for suffix, branch, value in zip(("candidate", "q1-only", "q2-only"), ("combined-orders", "q1_admitted_q2_diverted", "q2_admitted_q1_diverted"), values):
                    envelope = analysis.build_synthetic_response_envelope(
                        record_id=f"I10-primary:{mode}:{order}:{seed}:{suffix}",
                        branch_id=branch,
                        response=max(value, 1e-15),
                        seed=seed,
                        physical_order_id=order,
                        carrier_state_digest=sha256_bytes(f"I10-primary-carrier:{mode}:{order}:{seed}:{suffix}".encode()),
                        pairing_identity=pairing,
                    )
                    envelope["i04r1_response_record"]["mode"] = mode
                    if value == 0.0:
                        record = envelope["i04r1_response_record"]
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
                    envelopes.append(envelope)
                result = analysis.primary_margin(*envelopes, machine_policy, parent_policy)
                margin = float(result["normalized_margin"])
                rows.append(
                    {
                        "mode": mode,
                        "physical_order_id": order,
                        "seed": seed,
                        "candidate_response": values[0],
                        "q1_only_response": values[1],
                        "q2_only_response": values[2],
                        "strongest_leave_one_response": max(values[1:]),
                        "strongest_leave_one_provenance": "q1-only" if values[1] >= values[2] else "q2-only",
                        "primary_margin": margin,
                        "threshold_relation": "above_delta" if margin > delta else "at_or_below_delta",
                    }
                )
    index = read_json(root / I09A_INDEX_REL)
    expected = {
        item["mode"]: item["observed_relation"]["complete_three_envelope_estimates"]
        for item in index["comparison_rules"]
        if item["control_id"] == "symmetric_leave_one_common_carrier_admission"
    }
    for mode in MODES:
        observed = [{key: row[key] for key in ("candidate_response", "physical_order_id", "primary_margin", "q1_only_response", "q2_only_response", "seed", "strongest_leave_one_provenance", "strongest_leave_one_response")} for row in rows if row["mode"] == mode]
        require(observed == expected[mode], f"I09A primary margin projection drift: {mode}")
    return rows


def raw_pair(model: Any, adapter: Any) -> dict[str, Any]:
    return {"native_snapshot": normalize(model.snapshot()), "adapter_snapshot": None if adapter is None else normalize(adapter.snapshot())}


def native_snapshot_groups(snapshot: Mapping[str, Any]) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    current = snapshot["caches"]["base_grc9v3_snapshot"]
    baseline = snapshot["reset_baseline"]["snapshot"]["caches"]["base_grc9v3_snapshot"]
    require(isinstance(current, Mapping) and isinstance(baseline, Mapping), "native GRC9V3 snapshot groups missing")
    return current, baseline


def compare_raw_pair_under_native_contract(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    tolerance: float,
    *,
    context: str,
) -> dict[str, Any]:
    """Compare raw witnesses without misrepresenting PyGRC's normalized identity.

    The admitted PyGRC restoration contract deliberately canonicalizes three
    deterministic defaults plus undirected port-edge orientation on load.  The
    adapter remains byte/structure exact.  Native differences must be exactly
    that closed set; continuation and reset are checked independently below.
    """

    require(
        close_structure(before["adapter_snapshot"], after["adapter_snapshot"], tolerance),
        f"adapter raw observation mismatch: {context}",
    )
    native_before = before["native_snapshot"]
    native_after = after["native_snapshot"]
    require(isinstance(native_before, Mapping) and isinstance(native_after, Mapping), "native snapshots must be mappings")
    differences = structure_differences(native_before, native_after, tolerance)
    suffixes = (
        ".dynamics.state.cached_quantities.budget_target_source",
        ".dynamics.state.params_identity",
        ".dynamics.state.port_edges.11.node_u",
        ".dynamics.state.port_edges.11.node_v",
        ".dynamics.state.port_edges.7.node_u",
        ".dynamics.state.port_edges.7.node_v",
        ".dynamics.state.port_edges.9.node_u",
        ".dynamics.state.port_edges.9.node_v",
        ".dynamics.state.rng_state",
        ".metadata.rng_state",
    )
    prefixes = (
        "$.caches.base_grc9v3_snapshot",
        "$.reset_baseline.snapshot.caches.base_grc9v3_snapshot",
    )
    expected_paths = {prefix + suffix for prefix in prefixes for suffix in suffixes}
    observed_paths = {item["path"] for item in differences}
    require(observed_paths == expected_paths, f"unexpected native raw normalization surface: {context}")

    for before_group, after_group in zip(
        native_snapshot_groups(native_before),
        native_snapshot_groups(native_after),
    ):
        before_state = before_group["dynamics"]["state"]
        after_state = after_group["dynamics"]["state"]
        require(before_state["params_identity"] is None, f"pre-load params identity unexpectedly materialized: {context}")
        require(after_state["params_identity"] == after_group["metadata"]["params_hash"], f"loaded params identity mismatch: {context}")
        require(before_state["rng_state"] is None and "rng_state" not in before_group["metadata"], f"pre-load RNG unexpectedly materialized: {context}")
        require(after_state["rng_state"] == after_group["metadata"]["rng_state"], f"loaded RNG state mismatch: {context}")
        require("budget_target_source" not in before_state["cached_quantities"], f"pre-load budget source unexpectedly materialized: {context}")
        require(after_state["cached_quantities"]["budget_target_source"] == "explicit_state", f"loaded budget source mismatch: {context}")
        for edge_id in ("7", "9", "11"):
            before_edge = before_state["port_edges"][edge_id]
            after_edge = after_state["port_edges"][edge_id]
            require(before_edge["node_u"] == after_edge["node_v"], f"port-edge node_u normalization mismatch: {context}/{edge_id}")
            require(before_edge["node_v"] == after_edge["node_u"], f"port-edge node_v normalization mismatch: {context}/{edge_id}")
            require(math.isclose(float(before_edge["flux_uv"]), 0.0, abs_tol=tolerance, rel_tol=0.0), f"nonzero pre-load normalized edge flux: {context}/{edge_id}")
            require(math.isclose(float(after_edge["flux_uv"]), 0.0, abs_tol=tolerance, rel_tol=0.0), f"nonzero loaded normalized edge flux: {context}/{edge_id}")

    return {
        "adapter_raw_exact": True,
        "native_raw_equal": False,
        "native_difference_count": len(differences),
        "native_difference_paths": sorted(observed_paths),
        "native_difference_digest": canonical_digest(differences),
        "native_normalization_categories": [
            "deterministic_budget_source_materialization",
            "deterministic_params_identity_materialization",
            "deterministic_rng_state_materialization",
            "undirected_zero_flux_port_edge_canonicalization",
        ],
        "unexpected_native_differences": 0,
    }


def diagnose_load(root: Path, graph_root: Path, freeze: Mapping[str, Any], mode: str) -> dict[str, Any]:
    require(mode in MODES, f"unknown diagnostic mode: {mode}")
    validate_freeze(root, freeze)
    graph_before = validate_graph(graph_root, freeze)
    graph_src = graph_root / "src"
    scripts = root / EXPERIMENT / "scripts"
    for path in (graph_src, scripts):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    registration_module = import_file("p2_i2_i10_load_diagnostic_runtime", root / EXPERIMENT / "scripts/p2_i2_i06_registration.py")
    registration = read_json(root / REGISTRATION_REL)
    tolerance = float(freeze["restoration_continuation_policy"]["runtime_tolerance"])
    model, roles, edges, adapter = registration_module._build_model(registration, mode)
    initial_identity = registration_module._composite_identity(registration, mode, model, adapter, roles, edges)
    initial_raw = raw_pair(model, adapter)
    with tempfile.TemporaryDirectory(prefix="p2-i2-i10-load-diagnostic-") as directory:
        temp = Path(directory)
        native_path = temp / "native.json"
        adapter_path = None if adapter is None else temp / "adapter.json"
        model.save(str(native_path))
        if adapter is not None:
            adapter.save(adapter_path)
        pair_manifest = registration_module._pair_manifest(mode, native_path, adapter_path, initial_identity["digest"])
        loaded_model, loaded_adapter, loaded_roles, loaded_edges = registration_module._load_pair(
            registration, pair_manifest, native_path, adapter_path
        )
        loaded_identity = registration_module._composite_identity(
            registration, mode, loaded_model, loaded_adapter, loaded_roles, loaded_edges
        )
        loaded_raw = raw_pair(loaded_model, loaded_adapter)
    require(loaded_identity["digest"] == initial_identity["digest"], "diagnostic composite identity mismatch")
    differences = structure_differences(initial_raw, loaded_raw, tolerance)
    graph_after = validate_graph(graph_root, freeze)
    require(graph_before == graph_after, "graph changed during load diagnostic")
    return {
        "status": "diagnostic_complete",
        "mode": mode,
        "composite_identity_match": True,
        "raw_snapshot_match": not differences,
        "difference_count": len(differences),
        "differences": differences,
        "model_instantiations": 2,
        "native_steps": 0,
        "candidate_or_scientific_operations": 0,
        "graph_unchanged": True,
    }


def restoration_checks(root: Path, graph_root: Path, freeze: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    graph_src = graph_root / "src"
    scripts = root / EXPERIMENT / "scripts"
    for path in (graph_src, scripts):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    registration_module = import_file("p2_i2_i10_registration_runtime", root / EXPERIMENT / "scripts/p2_i2_i06_registration.py")
    registration = read_json(root / REGISTRATION_REL)
    current_validation = registration_module.validate(graph_root)
    retained_validation = read_json(root / REGISTRATION_VALIDATION_REL)
    historical_manifest = read_json(root / I06_HISTORICAL_MANIFEST_REL)
    i06a_validation = read_json(root / I06A_VALIDATION_REL)
    current_manifest_count = next(
        item["evidence"]["bound_file_count"]
        for item in current_validation["checks"]
        if item["check_id"] == "I06-12"
    )
    historical_manifest_count = len(historical_manifest["files"])
    provenance = next(item["evidence"] for item in i06a_validation["checks"] if item["check_id"] == "I06A-12")
    require(current_manifest_count == 15, "current I06 manifest count drift")
    require(historical_manifest_count == provenance["historical_execution_manifest_file_count"] == 5, "historical I06 manifest count drift")
    require(sha256_file(root / I06_HISTORICAL_MANIFEST_REL) == provenance["historical_execution_manifest_sha256"], "historical I06 manifest hash drift")
    require(sha256_file(root / REGISTRATION_VALIDATION_REL) == provenance["retained_validation_sha256"], "retained I06 validation hash drift")
    require(sha256_file(root / EXPERIMENT / "scripts/p2_i2_i06_registration.py") == provenance["current_validator_sha256"], "current I06 validator hash drift")
    require(provenance["current_validator_claimed_as_producer"] is False, "current I06 validator misclaimed as historical producer")
    require(provenance["fourteen_check_projection_unchanged"] is True, "I06 fourteen-check projection drift")
    historical_reconstruction = deepcopy(current_validation)
    next(
        item for item in historical_reconstruction["checks"] if item["check_id"] == "I06-12"
    )["evidence"]["bound_file_count"] = historical_manifest_count
    require(pretty_bytes(historical_reconstruction) == (root / REGISTRATION_VALIDATION_REL).read_bytes(), "historical I06 validation byte reconstruction drift")
    tolerance = float(freeze["restoration_continuation_policy"]["runtime_tolerance"])
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="p2-i2-i10-restoration-") as directory:
        temp = Path(directory)
        for mode in MODES:
            model, roles, edges, adapter = registration_module._build_model(registration, mode)
            initial_identity = registration_module._composite_identity(registration, mode, model, adapter, roles, edges)
            initial_raw = raw_pair(model, adapter)
            mode_dir = temp / mode
            mode_dir.mkdir()
            native_path = mode_dir / "native.json"
            adapter_path = None if adapter is None else mode_dir / "adapter.json"
            model.save(str(native_path))
            if adapter is not None:
                adapter.save(adapter_path)
            pair_manifest = registration_module._pair_manifest(mode, native_path, adapter_path, initial_identity["digest"])
            loaded_model, loaded_adapter, loaded_roles, loaded_edges = registration_module._load_pair(
                registration, pair_manifest, native_path, adapter_path
            )
            loaded_identity = registration_module._composite_identity(
                registration, mode, loaded_model, loaded_adapter, loaded_roles, loaded_edges
            )
            loaded_raw = raw_pair(loaded_model, loaded_adapter)
            require(loaded_identity["digest"] == initial_identity["digest"], f"load identity mismatch: {mode}")
            load_raw_comparison = compare_raw_pair_under_native_contract(
                initial_raw, loaded_raw, tolerance, context=f"{mode}/load"
            )
            original_step = normalize(model.step())
            loaded_step = normalize(loaded_model.step())
            original_post = registration_module._composite_identity(registration, mode, model, adapter, roles, edges)
            loaded_post = registration_module._composite_identity(registration, mode, loaded_model, loaded_adapter, loaded_roles, loaded_edges)
            original_post_raw = raw_pair(model, adapter)
            loaded_post_raw = raw_pair(loaded_model, loaded_adapter)
            require(close_structure(original_step, loaded_step, tolerance), f"equal-input step result mismatch: {mode}")
            require(original_post["digest"] == loaded_post["digest"], f"equal-input identity mismatch: {mode}")
            post_step_raw_comparison = compare_raw_pair_under_native_contract(
                original_post_raw, loaded_post_raw, tolerance, context=f"{mode}/post-step"
            )
            original_reset = registration_module._reset_pair_once(
                registration, mode, model, adapter, roles, edges, set(), f"i10-reset:{mode}"
            )
            loaded_reset = registration_module._reset_pair_once(
                registration, mode, loaded_model, loaded_adapter, loaded_roles, loaded_edges, set(), f"i10-reset:{mode}"
            )
            original_reset_raw = raw_pair(model, adapter)
            loaded_reset_raw = raw_pair(loaded_model, loaded_adapter)
            require(original_reset["digest"] == loaded_reset["digest"] == initial_identity["digest"], f"paired reset identity mismatch: {mode}")
            reset_raw_comparison = compare_raw_pair_under_native_contract(
                original_reset_raw, loaded_reset_raw, tolerance, context=f"{mode}/reset"
            )
            require(close_structure(original_reset_raw, initial_raw, tolerance), f"reset baseline raw observation mismatch: {mode}")
            results.append(
                {
                    "mode": mode,
                    "initial_composite_digest": initial_identity["digest"],
                    "loaded_composite_digest": loaded_identity["digest"],
                    "post_step_composite_digest": original_post["digest"],
                    "loaded_post_step_composite_digest": loaded_post["digest"],
                    "reset_composite_digest": original_reset["digest"],
                    "initial_raw_observation_digest": canonical_digest(initial_raw),
                    "loaded_raw_observation_digest": canonical_digest(loaded_raw),
                    "post_step_raw_observation_digest": canonical_digest(original_post_raw),
                    "loaded_post_step_raw_observation_digest": canonical_digest(loaded_post_raw),
                    "reset_raw_observation_digest": canonical_digest(original_reset_raw),
                    "loaded_reset_raw_observation_digest": canonical_digest(loaded_reset_raw),
                    "identity_and_raw_observations_compared_separately": True,
                    "raw_observation_contract": {
                        "load": load_raw_comparison,
                        "post_step": post_step_raw_comparison,
                        "reset": reset_raw_comparison,
                    },
                    "pair_save_load_valid": True,
                    "equal_input_no_packet_step_valid": True,
                    "paired_reset_valid": True,
                }
            )
    return results, {
        "current_registration_validation_checks": f"{current_validation['passed_checks']}/{current_validation['total_checks']}",
        "current_final_manifest_file_count": current_manifest_count,
        "historical_registration_validation_byte_identical": True,
        "historical_execution_manifest_file_count": historical_manifest_count,
        "historical_current_provenance_separate": True,
        "registration_validation_model_instantiations": 6,
        "continuation_model_instantiations": 6,
        "continuation_checks": 3,
        "native_steps": 6,
        "candidate_or_control_contributions": 0,
        "active_history_token_admissions": 0,
        "neutral_contacts": 0,
        "response_or_comparator_windows": 0,
    }


def reconstruct_controls(root: Path) -> dict[str, Any]:
    historical_module = import_file("p2_i2_i10_i09_builder", root / EXPERIMENT / "scripts/p2_i2_i09_control_resolution.py")
    historical_index, historical_context = historical_module.build_index(root, I09_FREEZE_REL)
    historical_validation = historical_module.build_validation(historical_index, historical_context)
    historical_report = historical_module.build_report(historical_index, historical_validation)
    require(pretty_bytes(historical_index) == (root / I09_INDEX_REL).read_bytes(), "I09 index byte reconstruction drift")
    require(pretty_bytes(historical_validation) == (root / I09_VALIDATION_REL).read_bytes(), "I09 validation byte reconstruction drift")
    require(historical_report == (root / I09_REPORT_REL).read_text(encoding="utf-8"), "I09 report byte reconstruction drift")

    corrected_module = import_file("p2_i2_i10_i09a_builder", root / EXPERIMENT / "scripts/p2_i2_i09a_control_resolution.py")
    corrected_freeze = corrected_module.load_freeze(root, I09A_FREEZE_REL)
    corrected_index, corrected_context = corrected_module.build_corrected_index(root, corrected_freeze)
    corrected_validation = corrected_module.build_validation(root, corrected_index, corrected_context)
    corrected_report = corrected_module.build_report(corrected_index, corrected_validation)
    require(pretty_bytes(corrected_index) == (root / I09A_INDEX_REL).read_bytes(), "I09A index byte reconstruction drift")
    require(pretty_bytes(corrected_validation) == (root / I09A_VALIDATION_REL).read_bytes(), "I09A validation byte reconstruction drift")
    require(corrected_report == (root / I09A_REPORT_REL).read_text(encoding="utf-8"), "I09A report byte reconstruction drift")
    return {
        "historical_i09_index_byte_identical": True,
        "historical_i09_validation_byte_identical": True,
        "historical_i09_report_byte_identical": True,
        "corrected_i09a_index_byte_identical": True,
        "corrected_i09a_validation_byte_identical": True,
        "corrected_i09a_report_byte_identical": True,
        "comparison_rules": len(corrected_index["comparison_rules"]),
        "lane_controls": len(corrected_index["lane_controls"]),
        "program_common_controls": len(corrected_index["program_common_controls"]),
        "normalized_primary_margin_distribution": corrected_index["summary"]["normalized_primary_margin_distribution"],
        "terminal_interpretation_assigned": False,
    }


def report_claims(root: Path, manifest: Mapping[str, Any], loaded: Mapping[str, dict[str, Any]], calibration: Mapping[str, Any], registration: Mapping[str, Any]) -> dict[str, Any]:
    i05 = (root / I05_REPORT_REL).read_text(encoding="utf-8")
    i06 = (root / I06_REPORT_REL).read_text(encoding="utf-8")
    i06b = (root / I06B_REPORT_REL).read_text(encoding="utf-8")
    i08 = (root / I08_REPORT_REL).read_text(encoding="utf-8")
    i09a = (root / I09A_REPORT_REL).read_text(encoding="utf-8")
    responses = Counter(float(record["raw_response_record"]["value"]) for record in loaded.values())
    modes = Counter(record["entry_identity"]["mode"] for record in loaded.values())
    cells = Counter(record["entry_identity"]["cell_id"] for record in loaded.values())
    reasons = Counter(record["raw_response_record"]["producer_reason"] for record in loaded.values())
    causal = Counter(record["raw_response_record"]["candidate_chain_status"] for record in loaded.values())
    facts = {
        "i05_delta_and_validation": "`analysis_arithmetic_delta` is therefore `1e-12`" in i05 and "11/11" in i05 and calibration["analysis_arithmetic_delta"] == 1e-12,
        "i06_registration_validation": "14/14" in i06 and registration["current_registration_validation_checks"] == "14/14" and registration["historical_registration_validation_byte_identical"],
        "i06b_overlay_validation": "15/15" in i06b,
        "i08_terminal_inventory": "Required/evaluable terminals | 234 / 234" in i08 and len(loaded) == 234,
        "i08_response_distribution": responses == Counter({0.0: 132, 0.125: 102}) and "| All modes | 234 | 132 | 102 |" in i08,
        "i08_mode_distribution": modes == Counter({"state_carried": 72, "history_carried": 75, "hybrid": 87}),
        "i08_cell_distribution": cells == Counter({"reference-pool": 18, "individual-contributions": 36, "combined-orders": 18, "pooled-history-shuffle": 27, "contributor-removal": 45, "global-state-exclusion": 72, "access-capacity-contrast": 18}),
        "i08_producer_reason_distribution": reasons == Counter({"feedback_coupled_pulse_packet_departure_scheduled": 93, "feedback_coupled_pulse_subthreshold": 120, "feedback_coupled_pulse_wrong_polarity": 12, "controller_receipt_predicate_direct_native_schedule": 9}),
        "i08_causal_status_distribution": causal == Counter({"receipt_derived": 198, "excluded_diagnostic": 18, "excluded_private_partition": 18}),
        "i08_interpretation_boundary": manifest["scientific_interpretation"] is None and "`R01`–`R05` remain unassigned" in i08,
        "i09a_normalized_margin_correction": "twelve `1.0` values and six `0.0` values" in i09a and "24/24" in i09a,
    }
    require(all(facts.values()), f"report semantic claim drift: {[key for key, value in facts.items() if not value]}")
    return {"verified_report_count": 6, "semantic_claims": facts, "deterministic_i09_and_i09a_report_byte_reconstruction": True}


def complete_portability_scan(root: Path, freeze: Mapping[str, Any], manifest: Mapping[str, Any]) -> dict[str, Any]:
    paths = {BASE_FREEZE_REL, FAILED_START_REL, FREEZE_REL, freeze["failed_start_002"]["path"], freeze["failed_start_003"]["path"]}
    paths.update(item["path"] for item in freeze["input_artifacts"])
    paths.update(item["path"] for item in freeze["local_correction_artifacts"])
    for rel in (I06_MANIFEST_REL, I06B_MANIFEST_REL):
        paths.update(item["path"] for item in read_json(root / rel)["files"])
    paths.update(item["output_path"] for item in manifest["terminals"])
    matrix = read_json(root / MATRIX_REL)
    for entry in matrix["entries"]:
        for relative in (
            entry["primary_output_path"],
            entry["retry_output_path"],
            entry["primary_claim_path"],
            entry["retry_claim_path"],
            failure_path(entry, 1),
            failure_path(entry, 2),
        ):
            if safe_relative(root, relative).exists():
                paths.add(relative)
    findings: list[dict[str, Any]] = []
    json_count = 0
    for relative in sorted(paths):
        path = safe_relative(root, relative)
        if path.suffix == ".json":
            json_count += 1
            value = read_json(path)
            ok, absolute = portable_json(value)
            if not ok:
                findings.append({"path": relative, "absolute_values": absolute})
        elif path.suffix in {".md", ".py"}:
            text = path.read_text(encoding="utf-8")
            machine_roots = sorted(set(re.findall(r"/home/[^\s\"'`)]+", text)))
            if machine_roots:
                findings.append({"path": relative, "absolute_values": machine_roots})
    require(not findings, f"portable-path scan failed: {findings[:3]}")
    return {"scanned_path_count": len(paths), "scanned_json_count": json_count, "absolute_path_finding_count": 0}


def build(root: Path, graph_root: Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    freeze = materialize_freeze(root, read_json(root / FREEZE_REL))
    freeze_summary = validate_freeze(root, freeze)
    graph_before = validate_graph(graph_root, freeze)
    scripts = root / EXPERIMENT / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    analysis = importlib.import_module("p2_i2_i04r2_analysis")
    calibration = reconstruct_calibration(root, analysis)
    resolved = validate_resolved_manifests(root)
    execution_manifest, loaded, execution = reconstruct_execution(root, freeze)
    margins = reconstruct_margins(root, analysis, loaded)
    restoration, registration = restoration_checks(root, graph_root, freeze)
    controls = reconstruct_controls(root)
    reports = report_claims(root, execution_manifest, loaded, calibration, registration)
    portability = complete_portability_scan(root, freeze, execution_manifest)
    graph_after = validate_graph(graph_root, freeze)
    require(graph_before == graph_after, "graph identity changed during I10")
    manifest: dict[str, Any] = {
        "artifact_id": "P2-I2-I10-RECONSTRUCTION-MANIFEST",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I10",
        "lane_id": "AE01-L02",
        "status": "review_ready_reconstruction_complete",
        "source_input_freeze": FREEZE_REL,
        "source_input_freeze_sha256": sha256_file(root / FREEZE_REL),
        "builder_identity": {"path": SCRIPT_REL, "sha256": sha256_file(root / SCRIPT_REL)},
        "frozen_input_verification": freeze_summary,
        "resolved_manifest_verification": resolved,
        "calibration_reconstruction": calibration,
        "registration_reconstruction": registration,
        "restoration_and_continuation": restoration,
        "execution_reconstruction": execution,
        "control_reconstruction": controls,
        "report_reconstruction": reports,
        "portable_path_verification": portability,
        "per_seed_order_primary_margins": margins,
        "graph_read_only_verification": {"before": graph_before, "after": graph_after, "unchanged": True},
        "execution_boundary": {
            "c02_entry_worker_invocations": 0,
            "matrix_entry_regenerations": 0,
            "candidate_or_control_contributions": 0,
            "active_history_token_admissions": 0,
            "neutral_contacts": 0,
            "response_or_comparator_windows": 0,
            "new_scientific_inputs": 0,
            "accepted_artifact_overwrites": 0,
            "R01_through_R05": "unassigned_until_I11",
            "lane_support_status": None,
            "terminal_classification": None,
            "mode_ranking": False,
            "scientific_result": False,
        },
        "process_accounting_per_declared_pass": {
            "python_entrypoint_starts": 1,
            "registration_validation_model_instantiations": 6,
            "continuation_model_instantiations": 6,
            "restoration_continuation_mode_checks": 3,
            "native_no_packet_steps": 6,
            "c02_entry_worker_invocations": 0,
            "matrix_entry_regenerations": 0,
        },
        "gate_effect": {
            "RECON_GATE": "review_ready_pending_owner_acceptance",
            "I11_authorized": False,
            "commit_authorized": False,
        },
    }
    manifest["canonical_payload_digest"] = canonical_digest(manifest)
    checks: list[dict[str, Any]] = []

    def check(check_id: str, claim: str, passed: bool, observed: Any) -> None:
        checks.append({"check_id": check_id, "claim": claim, "passed": bool(passed), "observed": observed})

    check("I10-01", "all historical committed and additive correction inputs equal their frozen bytes", freeze_summary["all_frozen_bytes_exact"], freeze_summary)
    check("I10-02", "repository venv and exact interpreter identity match", freeze_summary["interpreter_identity"] == ".venv/bin/python", freeze_summary["interpreter_executable_sha256"])
    check("I10-03", "admitted graph revision remains clean and unchanged", graph_before == graph_after, graph_after)
    check("I10-04", "resolved registration/control manifests are complete", resolved["all_reached_paths_exact"], resolved)
    check("I10-05", "calibration reconstructs through the accepted estimator", len(calibration["reconstructed_rows"]) == 10, calibration["estimator_path_id"])
    check("I10-06", "metric calibration and frozen sheet pass accepted JSON Schema", calibration["metric_calibration_schema_valid"] and calibration["frozen_metric_sheet_schema_valid"], True)
    check("I10-07", "candidate-blind delta reconstructs exactly", calibration["analysis_arithmetic_delta"] == 1e-12, calibration["analysis_arithmetic_delta"])
    check("I10-08", "current I06 validates 14/14 over 15 files and the historical five-file validation reconstructs byte-identically", registration["current_registration_validation_checks"] == "14/14" and registration["current_final_manifest_file_count"] == 15 and registration["historical_registration_validation_byte_identical"] and registration["historical_execution_manifest_file_count"] == 5 and registration["historical_current_provenance_separate"], registration)
    check("I10-09", "all three paired restoration identities load exactly", all(item["pair_save_load_valid"] for item in restoration), [item["mode"] for item in restoration])
    check("I10-10", "restoration identity and raw observations remain separate witnesses, with only the exact admitted native normalization surface", all(item["identity_and_raw_observations_compared_separately"] and all(phase["unexpected_native_differences"] == 0 and phase["adapter_raw_exact"] for phase in item["raw_observation_contract"].values()) for item in restoration), 3)
    check("I10-11", "all three equal-input no-packet continuations pass", all(item["equal_input_no_packet_step_valid"] for item in restoration), 3)
    check("I10-12", "all three paired resets return to registered baseline", all(item["paired_reset_valid"] for item in restoration), 3)
    check("I10-13", "C02 exact paths retain 234 evaluable terminals", execution["evaluable_terminals"] == 234 and execution["distinct_governed_paths_verified"] == 470, execution)
    check("I10-14", "C02 execution manifest reconstructs byte-identically", execution["manifest_byte_identical"], execution_manifest["canonical_payload_digest"])
    check("I10-15", "terminal receipts retain no rung or interpretation assignment", execution["unsafe_terminal_claims"] == 0, 0)
    check("I10-16", "historical I09 and corrected I09A index validation and report reconstruct byte-identically", all(value is True for key, value in controls.items() if key.endswith("_byte_identical")), controls)
    check("I10-17", "calibration registration execution and control reports agree with machine facts", all(reports["semantic_claims"].values()), reports)
    check("I10-18", "all eighteen mode-order-seed margins reconstruct", len(margins) == 18, len(margins))
    check("I10-19", "recomputed margins equal the hash-bound corrected I09A projection", Counter(row["primary_margin"] for row in margins) == Counter({1.0: 12, 0.0: 6}), Counter(row["primary_margin"] for row in margins))
    check("I10-20", "threshold relations use only accepted delta", {row["threshold_relation"] for row in margins} == {"above_delta", "at_or_below_delta"}, Counter(row["threshold_relation"] for row in margins))
    check("I10-21", "the complete reached bundle contains no absolute path", portability["absolute_path_finding_count"] == 0, portability)
    check("I10-22", "no scientific entry or new scientific input was generated", all(manifest["execution_boundary"][key] == 0 for key in ("c02_entry_worker_invocations", "matrix_entry_regenerations", "candidate_or_control_contributions", "active_history_token_admissions", "neutral_contacts", "response_or_comparator_windows", "new_scientific_inputs", "accepted_artifact_overwrites")), manifest["execution_boundary"])
    check("I10-23", "I10 assigns no rung support ranking or terminal result", manifest["execution_boundary"]["terminal_classification"] is None and manifest["execution_boundary"]["lane_support_status"] is None and manifest["execution_boundary"]["mode_ranking"] is False, manifest["execution_boundary"])
    check("I10-24", "manifest canonical payload digest reconstructs", manifest["canonical_payload_digest"] == canonical_digest({key: value for key, value in manifest.items() if key != "canonical_payload_digest"}), manifest["canonical_payload_digest"])
    passed = sum(item["passed"] for item in checks)
    validation: dict[str, Any] = {
        "artifact_id": "P2-I2-I10-RECONSTRUCTION-VALIDATION",
        "artifact_version": "1.0.0",
        "iteration_id": "P2-I2-I10",
        "status": "passed" if passed == len(checks) else "failed_closed",
        "checks": checks,
        "passed_check_count": passed,
        "check_count": len(checks),
        "blocker_count": len(checks) - passed,
        "duplicate_reconstruction_required": True,
        "candidate_or_control_invocations": 0,
        "matrix_entry_regenerations": 0,
        "scientific_interpretation": False,
        "RECON_GATE": "review_ready_pending_owner_acceptance" if passed == len(checks) else "closed",
    }
    validation["canonical_payload_digest"] = canonical_digest(validation)
    report = build_report(manifest, validation)
    return manifest, validation, report


def build_report(manifest: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
    margin_counts = Counter(row["primary_margin"] for row in manifest["per_seed_order_primary_margins"])
    return "\n".join(
        [
            "# P2-I2-I10 Reconstruction and Identity Verification",
            "",
            "**Status:** review-ready; RECON-GATE and commit pending owner acceptance",
            "",
            "**Evidence effect:** independent reconstruction and identity conformance only; no new scientific execution or interpretation",
            "",
            "## Result",
            "",
            f"The compact I10 audit passes {validation['passed_check_count']}/{validation['check_count']} checks with {validation['blocker_count']} blockers. Accepted calibration, registration validation, the 234-terminal C02 execution manifest, historical I09 plus corrected I09A index/validation/report bytes, and controlling report facts reconstruct from retained inputs without a matrix-entry invocation.",
            "",
            f"All three registered modes pass paired save/load identity, exact adapter raw equality, closed-set native raw-normalization classification, one identical no-packet continuation, and paired reset. The native differences are limited to deterministic default materialization and undirected zero-flux edge canonicalization; no unexpected raw difference is admitted. Each declared pass instantiates 6 models for accepted I06 validation plus 6 for the three original/loaded continuation pairs; it performs 6 native no-packet steps and zero contributions, history-token admissions, neutral contacts, response/comparator windows, or C02 workers.",
            "",
            "## Primary-margin reconstruction",
            "",
            f"All 18 mode/order/seed margins reconstruct through the accepted I04R2 strongest-leave-one estimator: {margin_counts.get(1.0, 0)} are `1.0` and {margin_counts.get(0.0, 0)} are `0.0`. The frozen `delta` remains `1e-12`; per-seed relations remain explicit and are not collapsed into a terminal scalar.",
            "",
            "## Retention and boundary",
            "",
            f"The audit verifies {manifest['execution_reconstruction']['distinct_governed_paths_verified']} unique C02 governed paths and scans {manifest['portable_path_verification']['scanned_path_count']} reached retained paths with zero absolute-path findings. The admitted graph revision remains clean and unchanged.",
            "",
            "I10 does not assign `R01`-`R05`, L02 support, a mode ranking, or a terminal classification. Its successful output makes the combined CONTROL-GATE/RECON-GATE package review-ready only. I11 remains closed until explicit owner acceptance and retention.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "validate", "diagnose-load"))
    parser.add_argument("--graph-root", required=True)
    parser.add_argument("--mode", choices=MODES, default="state_carried")
    args = parser.parse_args()
    root = repo_root()
    graph_root = Path(args.graph_root).resolve()
    freeze = materialize_freeze(root, read_json(root / FREEZE_REL))
    if args.command == "diagnose-load":
        print(json.dumps(diagnose_load(root, graph_root, freeze, args.mode), sort_keys=True))
        return 0
    manifest, validation, report = build(root, graph_root)
    outputs = {
        root / MANIFEST_REL: pretty_bytes(manifest),
        root / VALIDATION_REL: pretty_bytes(validation),
        root / REPORT_REL: report.encode("utf-8"),
    }
    if args.command == "build":
        for path in outputs:
            require(not path.exists(), f"refusing to overwrite I10 output: {path.name}")
        for path, payload in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    else:
        for path, payload in outputs.items():
            require(path.exists(), f"retained I10 output missing: {path.name}")
            require(path.read_bytes() == payload, f"I10 duplicate reconstruction differs: {path.name}")
    print(
        json.dumps(
            {
                "status": validation["status"],
                "checks": f"{validation['passed_check_count']}/{validation['check_count']}",
                "blockers": validation["blocker_count"],
                "margins": len(manifest["per_seed_order_primary_margins"]),
                "restoration_modes": len(manifest["restoration_and_continuation"]),
                "RECON_GATE": validation["RECON_GATE"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
