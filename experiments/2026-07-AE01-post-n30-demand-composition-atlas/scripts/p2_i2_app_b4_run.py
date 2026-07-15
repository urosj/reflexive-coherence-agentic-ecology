"""One-shot fresh-process APP-B4 ordered-three-token campaign runner."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
import sys
from typing import Any, Mapping

from p2_i2_app_b4_analysis import (
    analyze_receipts,
    build_registry,
    canonical_bytes,
    digest_value,
    measurement_payload,
)
from p2_i2_app_b_run import execute_arm


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT_REL = "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
RUNNER_REL = f"{EXPERIMENT_REL}/scripts/p2_i2_app_b4_run.py"
MACHINE_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r2_machine_policy.json"
PARENT_REL = f"{EXPERIMENT_REL}/configs/p2_i2_i04r1_analysis_policy.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(directory: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(directory), *arguments],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def committed_bytes(relative: str) -> bytes:
    process = subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        check=True,
        capture_output=True,
    )
    return process.stdout


def require_tracked_exact(relative: str) -> None:
    require(portable_relative(relative), "absolute tracked authority path refused")
    local = ROOT / relative
    require(local.is_file(), f"tracked authority missing: {relative}")
    require(committed_bytes(relative) == local.read_bytes(), f"tracked authority differs from HEAD: {relative}")


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def project_app_b4_envelope(receipt: Mapping[str, Any], row: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(receipt))
    envelope = result["response_envelope"]
    before_digest = digest_value(measurement_payload(envelope))
    record = envelope["i04r1_response_record"]
    identity_before = {
        key: record[key]
        for key in ("cell_id", "pairing_identity", "opportunity_id")
    }
    sequence = str(row["sequence"])
    record["cell_id"] = "app-b4-ordered-three-token-panel"
    record["pairing_identity"] = f"app-b4:history_carried:seed-{row['seed']}:three-slot-panel"
    record["opportunity_id"] = "app-b4-fixed-three-slot-response-opportunity"
    after_digest = digest_value(measurement_payload(envelope))
    require(before_digest == after_digest, "APP-B4 identity projection changed measurement payload")
    result["app_b4_measurement_projection"] = {
        "projection_kind": "identity_only_before_receipt_retention",
        "source_execute_arm": "p2_i2_app_b_run.execute_arm",
        "identity_before": identity_before,
        "identity_after": {
            key: record[key]
            for key in ("cell_id", "pairing_identity", "opportunity_id")
        },
        "actual_operation_sequence": sequence,
        "accepted_envelope_physical_order_id": record["physical_order_id"],
        "physical_order_field_role": "legacy accepted q-contribution response-protocol identity; APP-B4 sequence authority is actual_operation_sequence",
        "measurement_payload_digest": after_digest,
        "measurement_values_changed": False,
    }
    return result


def claim_once(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(canonical_bytes(value))
        handle.flush()
        os.fsync(handle.fileno())


def write_cumulative(path: Path, value: Mapping[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.next")
    temporary.write_bytes(canonical_bytes(value))
    os.replace(temporary, path)


def preflight(args: argparse.Namespace, freeze: Mapping[str, Any], activation: Mapping[str, Any]) -> dict[str, Any]:
    for value in (args.freeze, args.activation, args.claim, args.output, args.graph_root):
        require(portable_relative(value), "absolute path refused")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "parent not launched through lexical repository .venv")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "-B required")
    require(activation["artifact_id"] == "P2-I2-APP-B4-LIVE-ACTIVATION", "wrong activation artifact")
    require(activation["status"] == "active_for_single_campaign_after_owner_acceptance", "APP-B4 activation inactive")
    require(activation["campaign_authorized"] is True, "APP-B4 campaign unauthorized")
    require(activation["authorization_consumed"] is False, "APP-B4 activation already consumed")
    require(activation["freeze"]["path"] == args.freeze, "activation freeze path drifted")
    require(activation["freeze"]["sha256"] == sha256(ROOT / args.freeze), "activation freeze hash drifted")
    correction_ref = activation["execution_correction"]
    acceptance_ref = activation["owner_acceptance"]
    for item in (correction_ref, acceptance_ref):
        require(portable_relative(item["path"]), "absolute activation authority path refused")
    correction = load_json(ROOT / correction_ref["path"])
    acceptance = load_json(ROOT / acceptance_ref["path"])
    require(correction["artifact_id"] == "P2-I2-APP-B4-ACTIVATION-BINDING-CORRECTION", "wrong execution correction")
    require(correction_ref["sha256"] == sha256(ROOT / correction_ref["path"]), "execution correction hash drifted")
    require(correction["base_freeze"]["sha256"] == activation["freeze"]["sha256"], "correction freeze identity drifted")
    require(acceptance["artifact_id"] == "P2-I2-APP-B4-ACTIVATION-OWNER-ACCEPTANCE", "wrong owner acceptance")
    require(acceptance["status"] == "owner_accepted_containing_commit_and_single_campaign", "owner acceptance inactive")
    require(acceptance["activation"]["sha256"] == sha256(ROOT / args.activation), "accepted activation hash drifted")
    require(acceptance["execution_correction"]["sha256"] == correction_ref["sha256"], "accepted correction hash drifted")
    require(acceptance["single_campaign_authorized"] is True, "single campaign not owner-authorized")
    require(acceptance["containing_commit_authorized"] is True, "activation containing commit unauthorized")
    head = git(ROOT, "rev-parse", "HEAD")
    require(head == args.expected_head, "invocation HEAD drifted")
    implementation_commit = activation["implementation_commit"]
    require(
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", implementation_commit, "HEAD"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        ).returncode == 0,
        "immutable implementation commit is not an ancestor of invocation HEAD",
    )
    require(git(ROOT, "status", "--porcelain=v1", "--untracked-files=all") == "", "authority worktree dirty")
    activation_relative = str((ROOT / args.activation).relative_to(ROOT))
    require_tracked_exact(activation_relative)
    require_tracked_exact(correction_ref["path"])
    require_tracked_exact(acceptance_ref["path"])
    graph_root = (ROOT / args.graph_root).resolve()
    require(git(graph_root, "rev-parse", "HEAD") == freeze["environment"]["graph_commit"], "graph HEAD drifted")
    require(git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "", "graph worktree dirty")
    require(not (ROOT / args.claim).exists(), "APP-B4 claim already exists")
    require(not (ROOT / args.output).exists(), "APP-B4 output already exists")
    require(activation["claim_path"] == args.claim and activation["output_path"] == args.output, "activation output identity drifted")
    for relative, expected in freeze["implementation_sha256"].items():
        if relative == RUNNER_REL:
            require(correction["original_runner"]["sha256"] == expected, "original runner freeze identity drifted")
            require(correction["corrected_runner"]["path"] == relative, "corrected runner path drifted")
            require(sha256(ROOT / relative) == correction["corrected_runner"]["sha256"], "corrected runner drifted")
        else:
            require(sha256(ROOT / relative) == expected, f"implementation drift: {relative}")
    for item in freeze["authority_inputs"]:
        require(sha256(ROOT / item["path"]) == item["sha256"], f"authority drift: {item['path']}")
    normalized = [
        ".venv/bin/python", "-B", RUNNER_REL,
        "--freeze", args.freeze,
        "--activation", args.activation,
        "--claim", args.claim,
        "--output", args.output,
        "--expected-head", args.expected_head,
        "--graph-root", args.graph_root,
    ]
    expected = [args.expected_head if value == "{ACTIVATION_HEAD}" else value for value in activation["normalized_command"]]
    require(normalized == expected, "activation command drifted")
    return {
        "authority_head": head,
        "immutable_implementation_commit": implementation_commit,
        "authority_clean_before_claim": True,
        "activation_sha256": sha256(ROOT / args.activation),
        "execution_correction_sha256": correction_ref["sha256"],
        "owner_acceptance_sha256": sha256(ROOT / acceptance_ref["path"]),
        "tracked_authorities_exact": True,
        "graph_commit": freeze["environment"]["graph_commit"],
        "graph_clean": True,
        "lexical_interpreter": ".venv/bin/python",
        "normalized_command": normalized,
    }


def child_failure(row: Mapping[str, Any], index: int, process: subprocess.CompletedProcess[str], detail: str) -> dict[str, Any]:
    return {
        "arm_id": row["arm_id"],
        "arm_index": index,
        "attempt": 1,
        "returncode": process.returncode,
        "stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(process.stderr.encode()).hexdigest(),
        "detail": detail,
        "retry_eligible": False,
    }


def parent_main(args: argparse.Namespace) -> int:
    freeze = load_json(ROOT / args.freeze)
    activation = load_json(ROOT / args.activation)
    preflight_receipt = preflight(args, freeze, activation)
    rows = build_registry(freeze)
    claim = {
        "artifact_id": "P2-I2-APP-B4-CAMPAIGN-CLAIM",
        "authorization_consumed": True,
        "governed_attempt": 1,
        "scientific_retries_allowed": 0,
        "infrastructure_retries_allowed": 0,
        "freeze_sha256": sha256(ROOT / args.freeze),
        "activation_sha256": sha256(ROOT / args.activation),
        "arm_registry_digest": digest_value(rows),
        "preflight": preflight_receipt,
    }
    claim_once(ROOT / args.claim, claim)
    receipts: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    output = ROOT / args.output
    for index, row in enumerate(rows):
        process = subprocess.run(
            [
                ".venv/bin/python", "-B", RUNNER_REL,
                "--worker", "--freeze", args.freeze,
                "--graph-root", args.graph_root,
                "--row-json", json.dumps(row, sort_keys=True, separators=(",", ":")),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        if process.returncode != 0:
            failures.append(child_failure(row, index, process, "nonzero child exit"))
        else:
            try:
                receipt = json.loads(process.stdout)
                require(receipt["arm_id"] == row["arm_id"], "wrong child arm")
            except (json.JSONDecodeError, AssertionError, KeyError) as error:
                failures.append(child_failure(row, index, process, f"malformed child receipt: {type(error).__name__}"))
            else:
                receipts.append(receipt)
        progress = {
            "artifact_id": "P2-I2-APP-B4-CUMULATIVE-RUNTIME-PROGRESS",
            "status": "campaign_in_progress",
            "authority": claim,
            "arm_count_expected": 75,
            "arm_attempts_completed": index + 1,
            "successful_receipts": receipts,
            "failure_receipts": failures,
            "child_retry_count": 0,
            "analysis": None,
            "scientific_interpretation": None,
        }
        write_cumulative(output, progress)
    if failures:
        result = {
            "artifact_id": "P2-I2-APP-B4-INCOMPLETE-RUNTIME-EVIDENCE",
            "status": "nonevaluable_child_failures_retained",
            "authority": claim,
            "arm_count_expected": 75,
            "arm_attempt_count": 75,
            "receipts": receipts,
            "failure_receipts": failures,
            "runtime_invocation_count": 1,
            "child_retry_count": 0,
            "analysis": None,
            "scientific_result_assigned": False,
        }
        result["canonical_payload_digest"] = digest_value(result)
        write_cumulative(output, result)
        return 1
    analysis = analyze_receipts(
        receipts,
        freeze,
        load_json(ROOT / MACHINE_REL),
        load_json(ROOT / PARENT_REL),
    )
    result = {
        "artifact_id": "P2-I2-APP-B4-RUNTIME-EVIDENCE",
        "artifact_version": "1.0",
        "authority": claim,
        "arm_count": 75,
        "receipts": receipts,
        "analysis": analysis,
        "runtime_invocation_count": 1,
        "scientific_retry_count": 0,
        "candidate_parameter_search_count": 0,
        "graph_repository_mutation_count": 0,
    }
    result["canonical_payload_digest"] = digest_value(result)
    write_cumulative(output, result)
    require(load_json(output) == result, "APP-B4 output readback drifted")
    print(json.dumps({"status": "complete", "arms": 75}))
    return 0


def worker_main(args: argparse.Namespace) -> int:
    require(args.row_json is not None, "worker row required")
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "worker not launched through lexical repository .venv")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "worker repository .venv inactive")
    require(sys.dont_write_bytecode, "worker requires -B")
    freeze = load_json(ROOT / args.freeze)
    row = json.loads(args.row_json)
    expected = {item["arm_id"]: item for item in build_registry(freeze)}
    require(row["arm_id"] in expected and row == expected[row["arm_id"]], "worker row outside frozen registry")
    receipt = execute_arm(ROOT, (ROOT / args.graph_root).resolve(), freeze, row)
    receipt = project_app_b4_envelope(receipt, row)
    sys.stdout.buffer.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode())
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--activation")
    parser.add_argument("--claim")
    parser.add_argument("--output")
    parser.add_argument("--expected-head")
    parser.add_argument("--graph-root", required=True)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--row-json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.worker:
        return worker_main(args)
    require(all((args.activation, args.claim, args.output, args.expected_head)), "parent authority arguments required")
    return parent_main(args)


if __name__ == "__main__":
    raise SystemExit(main())
