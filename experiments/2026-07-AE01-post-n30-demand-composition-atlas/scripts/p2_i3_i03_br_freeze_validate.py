"""Zero-runtime validator for the proposed P2-I3 B-R conformance freeze."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping

from p2_i3_conformance_quarantine import (
    FORBIDDEN_CONSUMER_CLASSES,
    ConformanceQuarantineError,
    assert_no_conformance_import,
)


ROOT = Path(__file__).resolve().parents[3]
FREEZE = ROOT / (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/"
    "p2-i3/i03-br-bounded-conformance-input-freeze.json"
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), f"expected object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", "-C", str(root), *args),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _resolve_symbol(name: str) -> Any:
    parts = name.split(".")
    module = importlib.import_module(".".join(parts[:2]))
    value: Any = module
    for part in parts[2:]:
        value = getattr(value, part)
    return value


def _strings(value: Any) -> list[str]:
    rows: list[str] = []
    if isinstance(value, str):
        rows.append(value)
    elif isinstance(value, Mapping):
        for child in value.values():
            rows.extend(_strings(child))
    elif isinstance(value, list):
        for child in value:
            rows.extend(_strings(child))
    return rows


def validate(graph_root: Path) -> dict[str, Any]:
    freeze = _load(FREEZE)
    checks: list[str] = []

    def passed(condition: bool, check_id: str) -> None:
        _require(condition, check_id)
        checks.append(check_id)

    passed(freeze["status"] == "accepted_inactive", "accepted_inactive_status")
    passed(
        freeze["runtime_authorized"] is False
        and freeze["review_boundary"]["harness_construction_currently_open"]
        is False,
        "runtime_and_harness_currently_disabled",
    )
    passed(
        freeze["scientific_evidence_effect"] == "none",
        "zero_scientific_effect",
    )
    output = ROOT / freeze["bounded_execution"]["planned_output"]
    passed(not output.exists(), "conformance_output_absent")

    anchor = freeze["authority"]["rcae_authority_source_anchor"]
    passed(
        _git(ROOT, "merge-base", "--is-ancestor", anchor, "HEAD") == "",
        "accepted_authority_anchor_is_ancestor",
    )
    for row in freeze["authority"]["bound_rcae_artifacts"]:
        path = ROOT / row["path"]
        passed(path.is_file(), f"rcae_artifact_exists:{row['path']}")
        passed(
            _sha256(path) == row["sha256"],
            f"rcae_artifact_digest:{row['path']}",
        )

    graph = freeze["authority"]["graph_repository"]
    graph_root = graph_root.resolve()
    passed(graph_root.is_dir(), "graph_root_exists")
    passed(
        _git(graph_root, "rev-parse", "HEAD") == graph["required_revision"],
        "graph_revision_exact",
    )
    passed(
        _git(graph_root, "status", "--porcelain=v1", "--untracked-files=all")
        == "",
        "graph_worktree_clean",
    )
    for row in freeze["bound_graph_sources"]:
        path = graph_root / row["path"]
        passed(path.is_file(), f"graph_source_exists:{row['path']}")
        passed(
            _sha256(path) == row["sha256"],
            f"graph_source_digest:{row['path']}",
        )
    contract_path = graph_root / graph["n31_return_contract_path"]
    contract = _load(contract_path)
    passed(
        _sha256(contract_path) == graph["n31_return_contract_sha256"],
        "n31_br_contract_digest",
    )
    passed(
        contract["output_digest"] == graph["n31_return_contract_output_digest"],
        "n31_br_contract_output_digest",
    )

    source_root = (graph_root / "src").resolve()
    sys.path.insert(0, str(source_root))
    for name in tuple(sys.modules):
        if name == "pygrc" or name.startswith("pygrc."):
            del sys.modules[name]
    pygrc = importlib.import_module("pygrc")
    imported = Path(pygrc.__file__).resolve()
    passed(imported.is_relative_to(source_root), "pygrc_import_from_exact_tree")
    for row in freeze["required_public_calls"]:
        value = _resolve_symbol(row["symbol"])
        passed(callable(value), f"public_symbol_callable:{row['symbol']}")

    required_symbols = {
        row["symbol"] for row in freeze["required_public_calls"]
    }
    blocked_symbols = {row["symbol"] for row in freeze["blocked_public_calls"]}
    passed(not required_symbols & blocked_symbols, "required_blocked_disjoint")
    passed(
        not any("pygrc.models.GRC9V3.step" == item for item in required_symbols),
        "no_synchronous_grc9v3_step",
    )

    for package, expected in freeze["environment"]["required_packages"].items():
        passed(
            importlib.metadata.version(package) == expected,
            f"package_version:{package}",
        )

    fixture = freeze["fixture"]
    nodes = fixture["nodes"]
    edges = fixture["edges"]
    passed(len(nodes) == 10, "ten_role_matched_nodes")
    passed(len({row["node_id"] for row in nodes}) == 10, "unique_node_ids")
    passed(len(edges) == 10, "ten_role_matched_edges")
    passed(len({row["edge_id"] for row in edges}) == 10, "unique_edge_ids")
    values = fixture["fixture_only_values"]
    formed_carrier = 0.1 + (
        values["formation_event_amount"] * values["formation_event_count"]
    )
    exported_carrier = formed_carrier - values["export_cap"]
    passed(values["formation_event_count"] >= 2, "repetition_floor")
    passed(
        abs(
            values["one_pulse_quantity_match_amount"]
            - values["formation_event_amount"] * values["formation_event_count"]
        )
        <= values["absolute_float_tolerance"],
        "formation_quantity_match",
    )
    passed(
        abs(exported_carrier - values["export_floor"])
        <= values["absolute_float_tolerance"],
        "eligible_positive_reaches_fixture_floor",
    )
    passed(
        formed_carrier >= values["encounter_probe_amount"]
        and exported_carrier < values["encounter_probe_amount"],
        "fixture_only_native_boundary_split",
    )

    cells = freeze["conformance_matrix"]
    passed(len(cells) == 11, "eleven_bounded_conformance_cells")
    passed(len({row["cell_id"] for row in cells}) == 11, "unique_cell_ids")
    contrast_ids = {
        value
        for row in cells
        for value in row.get("contrast_ids", [])
    }
    passed(
        contrast_ids
        == {
            "P2-I3-BR-Q13-FORMATION-QUANTITY-MATCH-001",
            "P2-I3-BR-Q13-EXPORT-MASS-MATCH-001",
            "P2-I3-BR-Q13-COMPLETE-STATE-HISTORY-MATCH-001",
        },
        "q013_contrast_ids_exact",
    )

    strings = _strings(freeze)
    passed(not any(value.startswith("/home/") for value in strings), "no_home_paths")
    passed(
        freeze["bounded_execution"]["attempts"] == 1
        and freeze["bounded_execution"]["retries"] == 0,
        "one_attempt_zero_retries",
    )
    passed(
        freeze["bounded_execution"]["external_repository_writes_allowed"]
        is False,
        "external_writes_forbidden",
    )

    clean_payload = {
        "source_class": "candidate_blind_preregistration",
        "value_id": "future-i04-value",
    }
    for consumer in sorted(FORBIDDEN_CONSUMER_CLASSES):
        assert_no_conformance_import(clean_payload, consumer_class=consumer)
        rejected = False
        try:
            assert_no_conformance_import(
                {"source_class": "i03_conformance"},
                consumer_class=consumer,
            )
        except ConformanceQuarantineError:
            rejected = True
        passed(rejected, f"quarantine_negative_self_test:{consumer}")

    return {
        "artifact_id": freeze["artifact_id"],
        "status": "passed_zero_runtime_freeze_validation",
        "check_count": len(checks),
        "runtime_operations": 0,
        "conformance_output_exists": output.exists(),
        "graph_revision": graph["required_revision"],
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-root", required=True, type=Path)
    args = parser.parse_args()
    result = validate(args.graph_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
