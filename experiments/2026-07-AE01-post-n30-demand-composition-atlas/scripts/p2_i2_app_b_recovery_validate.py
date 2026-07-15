#!/usr/bin/env python3
"""Zero-science validation for the APP-B2 venv-only recovery."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
import tempfile
from typing import Any, Mapping

from p2_i2_app_b_analysis import canonical_bytes, digest_value
from p2_i2_app_b_run import (
    _child_failure,
    _progress_artifact,
    _write_cumulative,
    build_arm_registry,
    load_json,
)


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
RUNNER_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b_run.py"
FREEZE_REL = f"{EXPERIMENT_REL}/contracts/p2-i2/app-b1-runtime-input-freeze.json"
ORIGINAL_HEAD = "40fd9beecce8dfcc77c288c3f4d7f6f04eb3a765"
SCIENTIFIC_FUNCTIONS = (
    "_total_coherence",
    "_drain",
    "_schedule_packet",
    "_appendix_adapter",
    "_operation_route",
    "_participant_lineage",
    "_pair_identity",
    "_history_receipt",
    "_build_envelope",
    "execute_arm",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def assert_portable(value: Any, field: str = "root") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            assert_portable(item, f"{field}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            assert_portable(item, f"{field}[{index}]")
        return
    if not isinstance(value, str):
        return
    tokens = [token.strip("\"'`") for token in re.split(r"[\s=,;()\[\]{}<>]+", value) if token.strip("\"'`")]
    require(
        not any(PurePosixPath(token).is_absolute() or PureWindowsPath(token).is_absolute() for token in tokens),
        f"absolute path retained in {field}",
    )


def function_digests(source: str) -> dict[str, str]:
    tree = ast.parse(source)
    nodes = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    return {
        name: hashlib.sha256(ast.dump(nodes[name], include_attributes=False).encode("utf-8")).hexdigest()
        for name in SCIENTIFIC_FUNCTIONS
    }


def validate(authority_path: Path, output: Path | None) -> dict[str, Any]:
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "validator not launched through lexical .venv")
    authority = load_json(authority_path)
    freeze = load_json(ROOT / FREEZE_REL)
    require(authority["base_freeze"]["path"] == FREEZE_REL, "base-freeze path drifted")
    require(sha256(ROOT / FREEZE_REL) == authority["base_freeze"]["sha256"], "base-freeze hash drifted")
    for item in authority["permanent_failed_start_inputs"]:
        require(sha256(ROOT / item["path"]) == item["sha256"], f"failed-start input drift: {item['path']}")
    for relative, expected in authority["implementation_sha256"].items():
        require(sha256(ROOT / relative) == expected, f"implementation drift: {relative}")
    assert_portable(authority)

    current_source = (ROOT / RUNNER_REL).read_text(encoding="utf-8")
    original_source = subprocess.run(
        ["git", "show", f"{ORIGINAL_HEAD}:{RUNNER_REL}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    current_functions = function_digests(current_source)
    original_functions = function_digests(original_source)
    require(current_functions == original_functions, "scientific runtime function changed")
    require("str(Path(sys.executable).resolve())" not in current_source, "resolved child launcher remains")
    require('[".venv/bin/python", "-B", RUNNER_REL' not in current_source, "unexpected compact launcher form")
    require('".venv/bin/python", "-B", RUNNER_REL' in current_source, "lexical venv child launcher absent")
    worker_source = ast.get_source_segment(
        current_source,
        next(node for node in ast.parse(current_source).body if isinstance(node, ast.FunctionDef) and node.name == "worker_main"),
    )
    require(worker_source.index("repository .venv inactive") < worker_source.index("execute_arm("), "worker venv guard follows model path")
    parent_source = ast.get_source_segment(
        current_source,
        next(node for node in ast.parse(current_source).body if isinstance(node, ast.FunctionDef) and node.name == "parent_main"),
    )
    require(parent_source.count("subprocess.run(") == 1, "child launcher count drifted")
    require("check=False" in parent_source, "parent still raises before failure retention")
    require(parent_source.index("_write_cumulative(") < parent_source.index("if (index + 1) % 10"), "cumulative receipt is not retained before continuation")
    require("break" not in parent_source, "child failure can suppress later rows")

    probe_code = (
        "import json,sys; from pathlib import Path; "
        "root=Path.cwd(); "
        "print(json.dumps({'venv_prefix': Path(sys.prefix).resolve()==(root/'.venv').resolve(), "
        "'lexical_executable': Path(sys.executable)==root/'.venv/bin/python', "
        "'dont_write_bytecode': sys.dont_write_bytecode}))"
    )
    probe = subprocess.run(
        [".venv/bin/python", "-B", "-c", probe_code],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    probe_receipt = json.loads(probe.stdout)
    require(
        probe_receipt == {
            "venv_prefix": True,
            "lexical_executable": True,
            "dont_write_bytecode": True,
        },
        "live lexical venv child probe failed",
    )

    rows = build_arm_registry(freeze["arm_registry_specification"])
    fake = _child_failure(
        rows[0],
        0,
        failure_kind="validation_injected_failure",
        returncode=19,
        stdout="",
        stderr="validation-only synthetic stderr",
        detail="synthetic failure receipt; no subprocess or model",
    )
    progress = _progress_artifact(
        {"artifact_id": "validation-only-claim"},
        rows,
        [],
        [fake],
        1,
    )
    assert_portable(progress)
    require(fake["retry_eligible"] is False and fake["stderr_present"] is True, "failure receipt semantics drifted")
    require(progress["next_arm_index"] == 1 and progress["arm_count_expected"] == 99, "continuation index drifted")
    with tempfile.TemporaryDirectory(prefix="app-b-recovery-validation-") as directory:
        path = Path(directory) / "cumulative.json"
        _write_cumulative(path, progress)
        require(load_json(path) == progress, "cumulative failure receipt readback drifted")

    execution = authority["execution"]
    require(execution["replacement_attempts"] == 1, "replacement attempt ceiling drifted")
    require(execution["child_retries"] == 0, "child retry ceiling drifted")
    require(execution["child_interpreter"] == ".venv/bin/python", "child interpreter authority drifted")
    require((ROOT / execution["original_claim_path"]).exists(), "original claim missing")
    require(not (ROOT / execution["replacement_claim_path"]).exists(), "replacement claim already exists")
    require(not (ROOT / execution["replacement_output_path"]).exists(), "replacement output already exists")
    result = {
        "artifact_id": "P2-I2-APP-B2-RECOVERY-CANDIDATE-FREE-VALIDATION",
        "status": "passed_no_model_or_scientific_execution",
        "checks": {
            "authority_and_failed_start_hashes": True,
            "portable_authority": True,
            "scientific_function_digests_unchanged": current_functions,
            "resolved_global_child_launcher_absent": True,
            "lexical_venv_child_launcher_present": True,
            "worker_venv_guard_precedes_model_path": True,
            "live_model_free_venv_child_probe": probe_receipt,
            "failure_receipt_precedes_later_row_continuation": True,
            "failure_does_not_break_matrix_schedule": True,
            "pure_failure_receipt_readback": True,
            "replacement_claim_and_output_absent": True,
            "original_claim_preserved": True,
        },
        "execution_counts": {
            "validator_processes_this_start": 1,
            "child_processes": 1,
            "PyGRC_imports": 0,
            "models": 0,
            "candidate_arms": 0,
            "control_arms": 0,
            "response_calls": 0,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    if output is not None:
        require(not output.exists(), "validation output already exists")
        output.write_bytes(canonical_bytes(result))
        require(load_json(output) == result, "validation output readback drifted")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority", required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one validation mode")
    for value in (args.authority, args.output):
        if value is not None:
            require(not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute(), "absolute path refused")
    result = validate(ROOT / args.authority, None if args.check_only else ROOT / args.output)
    print(json.dumps({"status": result["status"], "checks": len(result["checks"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
