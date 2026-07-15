"""Pure unchanged-baseline capability audit for APP-B4 ordered triples."""

from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def portable_relative(value: str) -> bool:
    return not PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute()


def audit(registration_path: Path, freeze_path: Path) -> dict[str, Any]:
    require(Path(sys.executable) == ROOT / ".venv/bin/python", "audit not launched through lexical repository .venv")
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv inactive")
    require(sys.dont_write_bytecode, "audit requires -B")
    registration = load_json(registration_path)
    freeze = load_json(freeze_path)
    nodes = {item["role"]: float(item["initial_coherence"]) for item in registration["topology"]["nodes"]}
    native_lower, native_upper = map(float, registration["response_registration"]["native_closed_coherence_interval"])
    operation_registry = freeze["operation_registry"]
    coefficient = float(freeze["mode_realizations"]["history_carried"]["recency_coefficient"])
    schedule = freeze["schedule"]
    require(schedule["operation_order"] == ["G", "E", "P"], "accepted three-slot schedule drifted")
    require(nodes["P"] == 0.75, "accepted P baseline drifted")
    require(nodes["S1"] == nodes["S2"] == 7.5, "accepted contribution source baseline drifted")

    rows: list[dict[str, Any]] = []
    for symbols in product(("G", "E", "P"), repeat=3):
        state = dict(nodes)
        steps: list[dict[str, Any]] = []
        operationally_feasible = True
        first_failure = None
        history_readout = 0.0
        for slot, symbol in enumerate(symbols):
            registered = operation_registry[symbol]
            source, target, edge = registered["common_route"]
            amount = float(registered["amount"])
            source_before = state[source]
            target_before = state[target]
            sufficient = source_before >= amount
            step = {
                "slot": slot,
                "operation": symbol,
                "source_role": source,
                "target_role": target,
                "edge_role": edge,
                "amount": amount,
                "source_before": source_before,
                "target_before": target_before,
                "source_budget_sufficient": sufficient,
            }
            if not sufficient:
                operationally_feasible = False
                step["shortfall"] = amount - source_before
                first_failure = {
                    "slot": slot,
                    "operation": symbol,
                    "source_role": source,
                    "source_before": source_before,
                    "required_amount": amount,
                    "shortfall": amount - source_before,
                }
                steps.append(step)
                break
            state[source] -= amount
            state[target] += amount
            step["source_after"] = state[source]
            step["target_after"] = state[target]
            step["native_domain_after"] = (
                native_lower <= state[source] <= native_upper
                and native_lower <= state[target] <= native_upper
            )
            require(step["native_domain_after"], f"native coherence domain exceeded: {''.join(symbols)}")
            history_readout = coefficient * history_readout + amount
            steps.append(step)
        total_amount = sum(float(operation_registry[symbol]["amount"]) for symbol in symbols)
        rows.append(
            {
                "sequence": "".join(symbols),
                "symbols": list(symbols),
                "operation_counts": {symbol: symbols.count(symbol) for symbol in ("G", "E", "P")},
                "native_amount_total": total_amount,
                "same_total_as_GEP": math.isclose(total_amount, 1.9375, rel_tol=0.0, abs_tol=0.0),
                "all_three_operation_types_present": set(symbols) == {"G", "E", "P"},
                "operationally_feasible_unchanged_baseline": operationally_feasible,
                "first_failure": first_failure,
                "steps": steps,
                "final_P_if_feasible": state["P"] if operationally_feasible else None,
                "history_readout_if_feasible": history_readout if operationally_feasible else None,
            }
        )

    feasible = [row for row in rows if row["operationally_feasible_unchanged_baseline"]]
    infeasible = [row for row in rows if not row["operationally_feasible_unchanged_baseline"]]
    require(len(rows) == 27, "ordered triple count drifted")
    require(len(feasible) == 24, "unchanged-baseline feasible count drifted")
    require([row["sequence"] for row in infeasible] == ["EEG", "EEE", "EEP"], "infeasible sequence set drifted")
    require(all(row["first_failure"]["slot"] == 1 for row in infeasible), "failure slot drifted")
    require(all(math.isclose(row["first_failure"]["shortfall"], 0.125, rel_tol=0.0, abs_tol=0.0) for row in infeasible), "E-repeat shortfall drifted")
    exact_total = [row["sequence"] for row in rows if row["same_total_as_GEP"]]
    require(exact_total == ["GEP", "GPE", "EGP", "EPG", "PGE", "PEG"], "GEP-total permutation set drifted")
    require(max(row["final_P_if_feasible"] for row in feasible) == 3.375, "maximum feasible P drifted")
    require(max(row["history_readout_if_feasible"] for row in feasible) == 1.326171875, "maximum readout drifted")
    require(min(state_value for row in feasible for step in row["steps"] for state_value in (step["source_after"], step["target_after"])) >= native_lower, "feasible sequence left native domain")
    minimum_uniform_P_prefunding = 0.5625
    require(math.isclose(nodes["P"] + minimum_uniform_P_prefunding, 1.3125, rel_tol=0.0, abs_tol=0.0), "prefunding arithmetic drifted")

    result = {
        "artifact_id": "P2-I2-APP-B4-UNCHANGED-BASELINE-CAPABILITY-AUDIT",
        "artifact_version": "1.0",
        "status": "blocked_before_freeze_owner_choice_required",
        "inputs": {
            "registration": {"path": str(registration_path.relative_to(ROOT)), "sha256": sha256(registration_path)},
            "app_b1_freeze": {"path": str(freeze_path.relative_to(ROOT)), "sha256": sha256(freeze_path)},
        },
        "prospective_panel": {
            "mode": "history_carried",
            "ordered_triple_count": 27,
            "reference_rows_per_seed": 1,
            "seeds": [101, 211, 307],
            "complete_arm_count": 84,
            "baseline_changed": False,
            "operation_amounts_changed": False,
            "history_admission_changed": False,
        },
        "unchanged_baseline_audit": {
            "initial_coherence": {role: nodes[role] for role in ("S1", "S2", "P")},
            "native_closed_coherence_interval": [native_lower, native_upper],
            "feasible_sequence_count": len(feasible),
            "feasible_sequences": [row["sequence"] for row in feasible],
            "infeasible_sequence_count": len(infeasible),
            "infeasible_sequences": [row["sequence"] for row in infeasible],
            "infeasible_reason": "second consecutive E requires 0.4375 from P after first E leaves 0.3125",
            "shortfall_per_infeasible_sequence": 0.125,
            "maximum_feasible_final_P": max(row["final_P_if_feasible"] for row in feasible),
            "maximum_feasible_history_readout": max(row["history_readout_if_feasible"] for row in feasible),
            "all_sources_and_targets_inside_native_domain_for_feasible_sequences": True,
            "rows": rows,
        },
        "quantity_and_order_structure": {
            "GEP_native_total": 1.9375,
            "exact_total_sequences": exact_total,
            "exact_total_sequences_are_only_GEP_permutations": True,
            "repeated_operation_exact_total_sequence_exists": False,
            "cardinality_only_and_quantity_matched_simultaneously": False,
        },
        "owner_choice": {
            "option_A": {
                "id": "unchanged_baseline_24_sequence_panel",
                "description": "Freeze 24 feasible triples plus reference across three seeds",
                "arm_count": 75,
                "tradeoff": "native and closest to APP-B2, but EEG/EEE/EEP remain operationally outside the tested domain",
            },
            "option_B": {
                "id": "uniform_native_prefunding_full_27_sequence_panel",
                "description": "Add a frozen prehistory native P funding packet of 0.5625 to every arm, excluded from H_C, plus unfunded GEP anchors",
                "minimum_prefunding": minimum_uniform_P_prefunding,
                "prospective_arm_count_with_three_unfunded_GEP_anchors": 87,
                "tradeoff": "complete sequence space, but adds a new scaffold and requires explicit inertness/admission controls",
            },
            "option_C": {
                "id": "accept_operationally_infeasible_rows_in_84_arm_registry",
                "description": "Retain all 27 triples but preregister EEG/EEE/EEP as operationally infeasible rather than scientific negatives",
                "arm_count": 84,
                "tradeoff": "preserves complete registry but cannot evaluate a complete three-token response landscape",
            },
            "selection_made": False,
        },
        "process_counts": {
            "capability_audit_processes_this_start": 1,
            "PyGRC_imports": 0,
            "models": 0,
            "producers": 0,
            "arms": 0,
            "responses": 0,
        },
        "authority_boundary": {
            "freeze_authorized": False,
            "runtime_authorized": False,
            "commit_authorized": False,
            "owner_choice_required": True,
        },
    }
    result["canonical_payload_digest"] = digest_value(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registration", required=True)
    parser.add_argument("--freeze", required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    require(args.check_only != bool(args.output), "choose exactly one audit mode")
    for value in (args.registration, args.freeze, args.output):
        if value is not None:
            require(portable_relative(value), "absolute path refused")
    result = audit(ROOT / args.registration, ROOT / args.freeze)
    if args.output:
        output = ROOT / args.output
        require(not output.exists(), "capability audit output already exists")
        output.write_bytes(canonical_bytes(result))
        require(load_json(output) == result, "capability audit readback drifted")
    print(json.dumps({
        "status": result["status"],
        "feasible": result["unchanged_baseline_audit"]["feasible_sequence_count"],
        "infeasible": result["unchanged_baseline_audit"]["infeasible_sequences"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
