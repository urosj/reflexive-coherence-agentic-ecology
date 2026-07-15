#!/usr/bin/env python3
"""Read-only exact preflight for corrected P2-I2 I08 entry 1."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys


EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
SOURCE_REL = EXPERIMENT / "scripts/p2_i2_c02_postcommit_preflight.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--attempt", type=int, choices=(1, 2), required=True)
    args = parser.parse_args()
    require(
        sys.argv == [SOURCE_REL.as_posix(), "--expected-head", args.expected_head, "--attempt", str(args.attempt)],
        "preflight command drift",
    )
    require(sys.dont_write_bytecode, "preflight requires -B")
    root = Path(__file__).resolve().parents[3]
    scripts = root / EXPERIMENT / "scripts"
    if os.fspath(scripts) not in sys.path:
        sys.path.insert(0, os.fspath(scripts))
    import p2_i2_c02_execution as c02

    graph_argument = c02.load_json(root / c02.POLICY_REL)["runtime_invocation_identity"]["graph_root_argument"]
    graph = (root / graph_argument).resolve()
    matrix = c02.load_json(root / c02.MATRIX_REL)
    entry = dict(matrix["entries"][0])
    require(entry["sequence_index"] == 1, "first C02 sequence entry drift")
    identity = {key: entry[key] for key in ("mode", "cell_id", "branch_id", "physical_order_id", "seed")}
    normalized = c02.normalized_run_argv(entry, args.attempt, args.expected_head)
    c02.validate_activation(root, graph, identity, args.attempt, args.expected_head, normalized)
    helpers = c02._safe_helpers(root)
    if args.attempt == 1:
        require(helpers._governed_leaf_absent(root, entry["primary_claim_path"]), "entry-001 primary claim exists")
        require(helpers._governed_leaf_absent(root, entry["primary_output_path"]), "entry-001 primary output exists")
        require(helpers._governed_leaf_absent(root, c02._relative_failure(entry, 1)), "entry-001 primary failure exists")
    else:
        require(helpers._governed_leaf_exists(root, entry["primary_claim_path"]), "entry-001 retry predecessor claim absent")
        require(helpers._governed_leaf_exists(root, c02._relative_failure(entry, 1)), "entry-001 retry predecessor failure absent")
        require(helpers._governed_leaf_absent(root, entry["primary_output_path"]), "entry-001 primary output exists")
        require(helpers._governed_leaf_absent(root, entry["retry_claim_path"]), "entry-001 retry claim exists")
        require(helpers._governed_leaf_absent(root, entry["retry_output_path"]), "entry-001 retry output exists")
        require(helpers._governed_leaf_absent(root, c02._relative_failure(entry, 2)), "entry-001 retry failure exists")
    require(not (root / c02.MANIFEST_REL).exists(), "C02 execution manifest exists")
    require(not any(name == "pygrc" or name.startswith("pygrc.") for name in sys.modules), "preflight imported PyGRC")
    run_command = [".venv/bin/python", "-B", c02.SOURCE_REL.as_posix(), *normalized]
    print(json.dumps({
        "status": "passed_read_only",
        "cycle_id": c02.CYCLE_ID,
        "entry_id": entry["entry_id"],
        "sequence_index": 1,
        "attempt": args.attempt,
        "owner_authorized_full_HEAD": args.expected_head,
        "run_command": run_command,
        "pygrc_imports": 0,
        "governed_artifacts_written": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
