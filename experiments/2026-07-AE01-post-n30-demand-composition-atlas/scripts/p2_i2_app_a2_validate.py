#!/usr/bin/env python3
"""Zero-science static validation for the inactive P2-I2 APP-A2 package."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[3]
GRAPH_ROOT = ROOT.parent / "graph-reflexive-coherence"
APP_A2_PREFIX = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
)
MACHINE_PATH_PREFIXES = ("/home/" + "uros/", "/Users/" + "uros/")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    def add(self, check_id: str, passed: bool, observed: Any = None) -> None:
        self.rows.append(
            {
                "check_id": check_id,
                "passed": bool(passed),
                "observed": observed,
            }
        )


def imported_roots(tree: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def attribute_calls(tree: ast.AST) -> set[str]:
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            calls.add(node.func.attr)
    return calls


def validate(
    entry_path: Path,
    activation_path: Path,
) -> dict[str, Any]:
    checks = Checks()
    entry = load_json(entry_path)
    activation = load_json(activation_path)
    checks.add(
        "entry.artifact",
        entry.get("artifact_id") == "P2-I2-APP-A2-ENTRY-FREEZE",
        entry.get("artifact_id"),
    )
    checks.add(
        "activation.artifact",
        activation.get("artifact_id")
        == "P2-I2-APP-A2-INACTIVE-ACTIVATION-FREEZE",
        activation.get("artifact_id"),
    )
    checks.add(
        "activation.inactive_status",
        activation.get("status")
        == "validated_inactive_pending_owner_activation",
        activation.get("status"),
    )
    entry_ref = activation["entry_freeze"]
    checks.add("activation.entry_path", ROOT / entry_ref["path"] == entry_path, entry_ref["path"])
    checks.add("activation.entry_hash", sha256_file(entry_path) == entry_ref["sha256"], entry_ref["sha256"])

    checks.add(
        "environment.repository_venv",
        Path(sys.executable).resolve() == (ROOT / ".venv" / "bin" / "python").resolve(),
        ".venv/bin/python" if sys.prefix == str(ROOT / ".venv") else "unexpected",
    )
    environment = activation["environment"]
    checks.add("environment.python", platform.python_version() == environment["python_version"], platform.python_version())
    checks.add("environment.interpreter", sha256_file(ROOT / ".venv" / "bin" / "python") == environment["interpreter_sha256"], environment["interpreter_sha256"])
    checks.add("environment.logical_executable", environment["logical_executable"] == ".venv/bin/python", environment["logical_executable"])
    checks.add("environment.pythonpath", environment["pythonpath"] == "external-repository:graph-reflexive-coherence/src", environment["pythonpath"])

    checks.add("entry.commit", git("rev-parse", "HEAD") == entry["retained_rcae_entry"]["commit"], git("rev-parse", "HEAD"))
    checks.add("entry.branch", git("branch", "--show-current") == entry["retained_rcae_entry"]["branch"], git("branch", "--show-current"))
    graph = activation["graph"]
    checks.add("graph.commit", git("rev-parse", "HEAD", cwd=GRAPH_ROOT) == graph["commit"], git("rev-parse", "HEAD", cwd=GRAPH_ROOT))
    checks.add("graph.clean", git("status", "--short", cwd=GRAPH_ROOT) == "", git("status", "--short", cwd=GRAPH_ROOT))
    checks.add("graph.read_only", graph["mutation_allowed"] is False, graph["mutation_allowed"])
    for row in graph["source_identities"]:
        checks.add(
            f"graph.source.{row['path']}",
            sha256_file(GRAPH_ROOT / row["path"]) == row["sha256"],
            row["sha256"],
        )

    retained = activation["retained_app_a1"]
    for role, row in retained.items():
        checks.add(
            f"app_a1.{role}",
            sha256_file(ROOT / row["path"]) == row["sha256"],
            row["sha256"],
        )
    execution = load_json(ROOT / retained["execution_freeze"]["path"])
    fixture = load_json(ROOT / retained["fixture_freeze"]["path"])
    expected_ids = execution["frozen_registry_import"]["arm_order"]
    actual_ids = [row["arm_id"] for row in fixture["arm_registry"]]
    checks.add("registry.exact_order", actual_ids == expected_ids, actual_ids)
    checks.add("registry.count", len(actual_ids) == len(set(actual_ids)) == 19, len(actual_ids))

    policy = execution["campaign_policy"]
    checks.add("policy.one_campaign", policy["campaign_invocations"] == 1, policy["campaign_invocations"])
    checks.add("policy.zero_campaign_retry", policy["campaign_retry_limit"] == 0, policy["campaign_retry_limit"])
    checks.add("policy.one_arm_attempt", policy["attempts_per_arm"] == 1, policy["attempts_per_arm"])
    checks.add("policy.zero_arm_retry", policy["arm_retry_limit"] == 0, policy["arm_retry_limit"])
    checks.add("policy.fresh_process", policy["maximum_child_processes"] == 19, policy["maximum_child_processes"])
    checks.add("policy.packet_bound", policy["maximum_packet_events_per_arm"] == 32, policy["maximum_packet_events_per_arm"])
    checks.add("policy.queue_bound", policy["maximum_queue_length"] == 4, policy["maximum_queue_length"])
    checks.add("policy.topology_bound", (policy["maximum_nodes"], policy["maximum_edges"]) == (12, 28), [policy["maximum_nodes"], policy["maximum_edges"]])
    checks.add("policy.no_address_space_limit", policy["address_space_limit"] == "none", policy["address_space_limit"])

    aggregate_path = ROOT / policy["single_aggregate_persisted_output"]
    reconstruction_path = ROOT / policy["read_only_reconstruction_output"]
    allowed_parent = ROOT / (APP_A2_PREFIX + "contracts/p2-i2")
    for role, path in (("aggregate", aggregate_path), ("reconstruction", reconstruction_path)):
        checks.add(f"output.{role}.parent", path.parent == allowed_parent, str(path.relative_to(ROOT)))
        checks.add(f"output.{role}.json_only", path.suffix == ".json", path.suffix)
        checks.add(f"output.{role}.absent", not path.exists(), path.exists())
        checks.add(f"output.{role}.not_module_or_config", path.suffix not in {".py", ".toml", ".ini", ".yaml", ".yml"}, path.suffix)
    checks.add("output.distinct", aggregate_path != reconstruction_path, None)
    checks.add("output.no_per_arm_directory", entry["output_preconditions"]["per_arm_output_directory"] is None, entry["output_preconditions"]["per_arm_output_directory"])

    sources: dict[str, str] = {}
    trees: dict[str, ast.AST] = {}
    implementation_roles: set[str] = set()
    for row in activation["implementation_files"]:
        role = row["role"]
        path = ROOT / row["path"]
        implementation_roles.add(role)
        text = path.read_text(encoding="utf-8")
        sources[role] = text
        trees[role] = ast.parse(text, filename=row["path"])
        checks.add(f"implementation.{role}.hash", sha256_file(path) == row["sha256"], row["sha256"])
        checks.add(
            f"implementation.{role}.portable",
            not any(prefix in text for prefix in MACHINE_PATH_PREFIXES),
            None,
        )
    checks.add("implementation.roles", implementation_roles == {"analysis", "runner", "reconstructor", "validator"}, sorted(implementation_roles))
    checks.add("portability.runner_rejects_absolute_arguments", 'require(not path.is_absolute(), "absolute paths prohibited")' in sources["runner"], None)
    checks.add("portability.reconstructor_rejects_absolute_arguments", 'require(not path.is_absolute(), "absolute paths prohibited")' in sources["reconstructor"], None)
    checks.add("portability.validator_rejects_absolute_arguments", "validation input must be relative" in sources["validator"] and "validation output must be relative" in sources["validator"], None)
    checks.add("runner.pygrc_import", "pygrc" in imported_roots(trees["runner"]), sorted(imported_roots(trees["runner"])))
    checks.add("runner.subprocess_import", "subprocess" in imported_roots(trees["runner"]), sorted(imported_roots(trees["runner"])))
    checks.add("analysis.no_pygrc", "pygrc" not in imported_roots(trees["analysis"]), sorted(imported_roots(trees["analysis"])))
    checks.add("reconstructor.no_pygrc", "pygrc" not in imported_roots(trees["reconstructor"]), sorted(imported_roots(trees["reconstructor"])))
    checks.add("reconstructor.no_subprocess", "subprocess" not in imported_roots(trees["reconstructor"]), sorted(imported_roots(trees["reconstructor"])))
    checks.add("validator.no_pygrc", "pygrc" not in imported_roots(trees["validator"]), sorted(imported_roots(trees["validator"])))

    forbidden_scans = {"glob", "rglob", "iterdir", "listdir", "scandir", "walk"}
    runner_calls = attribute_calls(trees["runner"])
    checks.add("isolation.no_result_scans", not (runner_calls & forbidden_scans), sorted(runner_calls & forbidden_scans))
    checks.add("isolation.no_break", not any(isinstance(node, ast.Break) for node in ast.walk(trees["runner"])), None)
    checks.add("isolation.no_shared_runtime", not ({"random", "multiprocessing", "threading", "queue"} & imported_roots(trees["runner"])), sorted(imported_roots(trees["runner"])))
    cache_files = sorted(
        str(path.relative_to(ROOT))
        for path in (ROOT / APP_A2_PREFIX / "scripts" / "__pycache__").glob(
            "p2_i2_app_a2*.pyc"
        )
    )
    checks.add("isolation.no_app_a2_import_cache", not cache_files, cache_files)
    checks.add("isolation.worker_input_arm_only", 'require(set(worker_input) == {"arm"}' in sources["runner"], None)
    checks.add("isolation.exact_frozen_row", 'require(arm == frozen_rows[arm["arm_id"]]' in sources["runner"], None)
    checks.add("isolation.fresh_model", "model, role_ids, edge_ids = build_model(fixture, arm)" in sources["runner"], None)
    checks.add("isolation.all_attempts_retained", "child_invocations.append(invocation)" in sources["runner"], None)
    adaptive_retry_loops = [
        node
        for node in ast.walk(trees["runner"])
        if isinstance(node, ast.While)
        and any(
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr in {"run", "Popen"}
            for child in ast.walk(node)
        )
    ]
    checks.add("isolation.no_adaptive_retry_loop", not adaptive_retry_loops, len(adaptive_retry_loops))
    checks.add("isolation.aggregate_exclusive_claim", "os.O_CREAT | os.O_EXCL | os.O_WRONLY" in sources["runner"] and "os.O_NOFOLLOW" in sources["runner"], None)
    checks.add("activation.runner_requires_static_validation", "validate_static_validation(freeze, freeze_path)" in sources["runner"], None)
    checks.add("activation.reconstructor_requires_static_validation", "validate_static_validation(activation_freeze, freeze_path)" in sources["reconstructor"], None)
    checks.add("isolation.no_per_arm_persist", '"persistent_per_arm_output": False' in sources["runner"], None)
    checks.add("isolation.portable_failure", "portable_failure_message(exc)" in sources["runner"], None)
    checks.add("isolation.temporary_failure_path_normalized", 'tempfile.gettempdir(), "temporary-root"' in sources["runner"], None)
    checks.add("isolation.matrix_fails_closed", '"nonevaluable_incomplete_or_invalid_matrix"' in sources["analysis"], None)

    checks.add("native.operations", "schedule_packet_departure" in sources["runner"], None)
    checks.add("native.response", "set_causal_flux_routes" in sources["runner"] and "produce_events" in sources["runner"], None)
    checks.add("native.intervention", "build_lgrc9v3_packet_ledger" in sources["runner"] and "model.set_state(state)" in sources["runner"], None)
    checks.add("native.restoration", "model.save" in sources["runner"] and "LGRC9V3.load" in sources["runner"] and "model.reset" in sources["runner"], None)
    checks.add("receipts.packet_records", '"packet_record": new_packets[0].to_record()' in sources["runner"], None)
    checks.add("receipts.native_producer", '"producer_records": [row.to_artifact()' in sources["runner"], None)
    checks.add("receipts.target_roles", '"target_roles": sorted(' in sources["runner"], None)

    recon_calls = attribute_calls(trees["reconstructor"])
    checks.add("reconstruction.no_process_calls", not ({"run", "Popen", "system", "spawn"} & recon_calls), sorted(recon_calls))
    checks.add("reconstruction.analysis_from_receipts", "analyze_receipts(" in sources["reconstructor"], None)
    checks.add("reconstruction.byte_identity", "canonical_bytes(reconstructed) == canonical_bytes(aggregate[\"analysis\"])" in sources["reconstructor"], None)
    checks.add("reconstruction.exclusive_output", "os.O_CREAT | os.O_EXCL | os.O_WRONLY" in sources["reconstructor"] and "os.O_NOFOLLOW" in sources["reconstructor"], None)

    combined = "\n".join(
        sources[role] for role in ("analysis", "runner", "reconstructor")
    )
    frozen_only_literals = ("0.123", "0.082", "0.133", "0.126", "0.069", "0.063", "0.077", "0.081", "0.003", "0.008", "0.016", "0.01", "0.82", "0.04", "0.02", "0.015")
    checks.add("freeze.no_scientific_literals_duplicated", not any(value in combined for value in frozen_only_literals), [value for value in frozen_only_literals if value in combined])

    commands = activation["normalized_commands"]
    checks.add("commands.campaign_venv", ".venv/bin/python -B " in commands["campaign"], commands["campaign"])
    checks.add("commands.worker_venv", ".venv/bin/python -B " in commands["worker"], commands["worker"])
    checks.add("commands.reconstruction_venv", ".venv/bin/python -B " in commands["reconstruction"], commands["reconstruction"])
    checks.add("commands.no_absolute_paths", all(not value.startswith("/") and "/home/" not in value for value in commands.values()), commands)
    auth = activation["future_activation_authorization"]
    checks.add("activation.future_only", auth["present_now"] is False and auth["campaign_authorized_now"] is False, auth)
    checks.add("activation.owner_required", auth["owner_acceptance_required"] is True and auth["containing_commit_required"] is True, auth)
    checks.add("activation.authorization_absent", not (ROOT / auth["path"]).exists(), auth["path"])

    failed = [row["check_id"] for row in checks.rows if not row["passed"]]
    result: dict[str, Any] = {
        "artifact_id": "p2_i2_app_a2_inactive_static_validation",
        "artifact_version": "1.0",
        "experiment_id": "2026-07-AE01",
        "generated_at": activation["frozen_at"],
        "iteration_id": "P2-I2-APP-A2",
        "status": "passed" if not failed else "failed",
        "entry_freeze": {
            "path": str(entry_path.relative_to(ROOT)),
            "sha256": sha256_file(entry_path),
        },
        "activation_freeze": {
            "path": str(activation_path.relative_to(ROOT)),
            "sha256": sha256_file(activation_path),
        },
        "checks": checks.rows,
        "checks_passed": len(checks.rows) - len(failed),
        "checks_total": len(checks.rows),
        "failed_checks": failed,
        "zero_science_receipt": {
            "pygrc_imports": 0,
            "scientific_models": 0,
            "child_arm_starts": 0,
            "scientific_gate_signatures": 0,
            "runtime_outputs_created": 0,
            "Appendix_results_assigned": 0,
        },
        "authority_effect": "Inactive implementation-conformance evidence only; APP-A2 campaign remains unauthorized.",
    }
    unsigned = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["output_digest"] = hashlib.sha256(unsigned.encode("utf-8")).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--entry-freeze", required=True)
    parser.add_argument("--activation-freeze", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    if Path(args.entry_freeze).is_absolute() or Path(args.activation_freeze).is_absolute():
        raise AssertionError("validation input must be relative")
    entry_path = (ROOT / args.entry_freeze).resolve()
    activation_path = (ROOT / args.activation_freeze).resolve()
    for path in (entry_path, activation_path):
        if not path.is_relative_to(ROOT):
            raise AssertionError("validation input outside repository")
    result = validate(entry_path, activation_path)
    if args.output:
        if Path(args.output).is_absolute():
            raise AssertionError("validation output must be relative")
        output_path = (ROOT / args.output).resolve()
        if not output_path.is_relative_to(ROOT):
            raise AssertionError("validation output outside repository")
        if output_path.exists():
            raise AssertionError("validation output already exists")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(output_path, flags, 0o644)
        try:
            data = canonical_bytes(result)
            written = 0
            while written < len(data):
                written += os.write(fd, data[written:])
            os.fsync(fd)
        finally:
            os.close(fd)
    print(
        json.dumps(
            {
                "status": result["status"],
                "checks_passed": result["checks_passed"],
                "checks_total": result["checks_total"],
                "output_digest": result["output_digest"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
