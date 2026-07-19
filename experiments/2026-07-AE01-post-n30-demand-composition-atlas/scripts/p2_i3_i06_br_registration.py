#!/usr/bin/env python3
"""Build and validate the candidate-free P2-I3 B-R I06 registration.

The builder materializes exact future execution authority but performs no
formation, export, encounter, scientific-control, or integrity-fault request.
PyGRC is imported only from the locally selected graph checkout source tree.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import platform
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Mapping

import jsonschema
import pygrc
from pygrc.core import PortGraphBackend
from pygrc.models import (
    GRC9V3NodeState,
    GRC9V3State,
    LGRC9V3,
    PortEdge,
    digest_lgrc9v3_restoration_identity_v2,
)


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/2026-07-AE01-post-n30-demand-composition-atlas"
CONTRACT_DIR = EXPERIMENT / "contracts/p2-i3"
CONFIG_DIR = EXPERIMENT / "configs"
SCRIPT_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "scripts/p2_i3_i06_br_registration.py"
)
SCHEMA_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i06-br-registration.schema.json"
)
EXECUTION_SCHEMA_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i06-br-execution-records.schema.json"
)
POLICY_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "configs/p2_i3_br_i06_registration_policy.json"
)
TIMING_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i06-br-candidate-free-timing.json"
)
REGISTRATION_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i06-br-exact-registration.json"
)
VALIDATION_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i06-br-registration-validation.json"
)
TEST_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "implementation/tests/test_p2_i3_i06_br.py"
)
REPORT_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "reports/P2-I3-I06-BR-exact-registration.md"
)
I03_RETURN_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i03-n31-return-admission.json"
)
I03_FREEZE_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i03-br-bounded-conformance-input-freeze.json"
)
I04_POLICY_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "configs/p2_i3_br_i04_machine_policy.json"
)
I05_ACCEPTANCE_RELATIVE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/i05-br-owner-acceptance-and-cal-gate.json"
)

SOURCE_ANCHOR = "2e63a0dc6147bf124966374341c126f09b765cdd"
EXPECTED_GRAPH_REVISION = "565706f8b7647f6b7638b9afbe52372e170bf724"
CALIBRATION_SEEDS = {19, 43, 71, 109, 163}
REALIZATIONS = (101, 211, 307)
PROFILES = (("tau-1", 1), ("tau-2", 2))
ARMS = ("W", "O", "E")
DELTA = Fraction(1, 1_000_000_000_000)
ARTIFACT_VERSION = "1.0.2"
MIB = 1024 * 1024
GIB = 1024 * MIB
THREAD_ENV = {
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "BLIS_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "PYTHONHASHSEED": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
}


class RegistrationError(RuntimeError):
    """Raised when I06 cannot close exactly and portably."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RegistrationError(message)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def digest_data(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(root), *args),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def committed_file_sha256(revision: str, relative: str) -> str:
    result = subprocess.run(
        ("git", "-C", str(ROOT), "show", f"{revision}:{relative}"),
        check=True,
        capture_output=True,
    )
    return hashlib.sha256(result.stdout).hexdigest()


def with_digest(value: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result["canonical_payload_digest"] = digest_data(result)
    return result


def fraction(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "value": float(value),
    }


def normalized_margin(a: Fraction, b: Fraction) -> Fraction:
    """Apply the exact DEC-038 normalizer without float arithmetic."""
    return (a - b) / max(abs(a), abs(b), DELTA)


def as_fraction(value: Mapping[str, Any]) -> Fraction:
    result = Fraction(value["numerator"], value["denominator"])
    require(float(result) == value["value"], "rational projection drift")
    return result


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
    normalized = value.replace("${RCAE_PYGRC_ROOT}", "RCAE_PYGRC_ROOT")
    tokens = [item.strip("\"'`") for item in re.split(r"[\s=,;\[\]{}<>]+", normalized) if item.strip("\"'`")]
    absolute = next(
        (
            item
            for item in tokens
            if re.match(r"^/(?:home|root|tmp|var|usr|opt|etc|mnt|srv)/", item)
            or PureWindowsPath(item).is_absolute()
            or item.startswith("file:///")
        ),
        None,
    )
    require(absolute is None, f"machine-local absolute path at {field}")


def require_environment(graph_root: Path) -> dict[str, Any]:
    require(Path(sys.prefix).resolve() == (ROOT / ".venv").resolve(), "repository .venv required")
    for key, expected in THREAD_ENV.items():
        require(os.environ.get(key) == expected, f"environment mismatch: {key}")
    require(git(graph_root, "rev-parse", "HEAD") == EXPECTED_GRAPH_REVISION, "graph revision drift")
    git(ROOT, "merge-base", "--is-ancestor", SOURCE_ANCHOR, "HEAD")
    require(
        git(graph_root, "status", "--porcelain=v1", "--untracked-files=all") == "",
        "graph worktree must be clean",
    )
    source_root = (graph_root / "src").resolve()
    require(
        Path(pygrc.__file__).resolve() == source_root / "pygrc/__init__.py",
        "PyGRC must resolve from exact graph src; installed copy/fallback forbidden",
    )
    require(any(Path(item).resolve() == source_root for item in sys.path if item), "graph src absent from sys.path")
    i03 = load_json(ROOT / I03_FREEZE_RELATIVE)
    for entry in i03["bound_graph_sources"]:
        require(sha256_file(graph_root / entry["path"]) == entry["sha256"], f"graph source drift: {entry['path']}")
    versions = {
        name: importlib.metadata.version(name)
        for name in ("jsonschema", "networkx", "PyYAML", "pygrc")
    }
    return {
        "graph_repository_id": "graph-reflexive-coherence",
        "graph_revision": EXPECTED_GRAPH_REVISION,
        "graph_worktree_clean": True,
        "pygrc_source_import": "${RCAE_PYGRC_ROOT}/src/pygrc/__init__.py",
        "installed_distribution_metadata_authoritative": False,
        "distribution_metadata_discrepancy_effect": "none_on_source_bound_runtime",
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "interpreter": ".venv/bin/python",
        "packages": versions,
        "thread_environment": deepcopy(THREAD_ENV),
        "network_allowed": False,
        "graph_mutation_allowed": False,
        "machine_local_path_retained": False,
    }


def host_resource_observation() -> dict[str, Any]:
    meminfo: dict[str, int] = {}
    source = Path("/proc/meminfo")
    if source.is_file():
        for line in source.read_text(encoding="utf-8").splitlines():
            key, raw = line.split(":", 1)
            value = raw.strip().split()[0]
            if value.isdigit():
                meminfo[key] = int(value) * 1024
    cgroup_limit: int | None = None
    for candidate in (Path("/sys/fs/cgroup/memory.max"), Path("/sys/fs/cgroup/memory/memory.limit_in_bytes")):
        if candidate.is_file():
            raw = candidate.read_text(encoding="utf-8").strip()
            if raw.isdigit():
                cgroup_limit = int(raw)
                break
    return {
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
        "logical_cpu_count": os.cpu_count(),
        "host_physical_memory_bytes": meminfo.get("MemTotal"),
        "available_memory_at_characterization_bytes": meminfo.get("MemAvailable"),
        "swap_total_bytes": meminfo.get("SwapTotal"),
        "swap_available_at_characterization_bytes": meminfo.get("SwapFree"),
        "cgroup_memory_ceiling_bytes": cgroup_limit,
        "identity_fields_for_I07_match": ["platform_system", "platform_machine", "logical_cpu_count", "host_physical_memory_bytes", "cgroup_memory_ceiling_bytes"],
        "observation_only_fields_not_exact_launch_match": ["available_memory_at_characterization_bytes", "swap_available_at_characterization_bytes"],
        "machine_local_path_retained": False,
    }


def _timed(function: Any, repetitions: int) -> list[int]:
    rows: list[int] = []
    for _ in range(repetitions):
        start = time.monotonic_ns()
        function()
        rows.append(time.monotonic_ns() - start)
    return rows


def _timing_model() -> LGRC9V3:
    graph = PortGraphBackend()
    source = graph.add_node({"role": "candidate-free-timing-source"})
    target = graph.add_node({"role": "candidate-free-timing-target"})
    edge = graph.connect_ports(source, 0, target, 0, {"role": "candidate-free-timing-edge"})
    base = GRC9V3State(
        topology=graph,
        nodes={source: GRC9V3NodeState(coherence=1.0), target: GRC9V3NodeState(coherence=0.0)},
        port_edges={edge: PortEdge(source, 1, target, 1, conductance=1.0, flux_uv=0.0)},
        base_conductance={edge: 1.0},
        geometric_length={edge: 1.0},
        temporal_delay={edge: 1.0},
        flux_coupling={edge: 0.0},
    )
    return LGRC9V3.from_state(
        base,
        {
            "dt": 1.0,
            "causal_modes": {
                "causal_layer_mode": "packetized_fixed_topology",
                "lgrc_runtime_level": "lgrc2",
                "lapse_policy": "unit",
                "edge_delay_policy": "constant_delay",
                "event_time_policy": "explicit_event_time_key",
                "proper_time_accumulation_policy": "local_event_frontier",
            },
        },
    )


def characterize_timing(environment: Mapping[str, Any]) -> dict[str, Any]:
    repetitions = 7
    sample = {
        "schema": "p2_i3_i06_candidate_free_sample_v1",
        "values": list(range(32)),
    }
    sample_schema = {
        "type": "object",
        "required": ["schema", "values"],
        "properties": {
            "schema": {"const": "p2_i3_i06_candidate_free_sample_v1"},
            "values": {"type": "array", "minItems": 32, "maxItems": 32},
        },
        "additionalProperties": False,
    }
    with tempfile.TemporaryDirectory(prefix="p2-i3-i06-timing-") as raw:
        temporary = Path(raw)
        sample_path = temporary / "sample.json"
        sample_path.write_bytes(pretty_bytes(sample))

        startup = _timed(
            lambda: subprocess.run(
                (str(ROOT / ".venv/bin/python"), "-B", "-c", "pass"),
                cwd=ROOT,
                env={**os.environ, **THREAD_ENV},
                check=True,
                capture_output=True,
            ),
            repetitions,
        )
        load = _timed(lambda: json.loads(sample_path.read_text(encoding="utf-8")), repetitions)

        def event_operation() -> None:
            model = _timing_model()
            model.schedule_packet_departure(
                source_node_id=0,
                target_node_id=1,
                edge_id=0,
                amount=1.0 / 128.0,
                departure_event_time_key=0.0,
                arrival_event_time_key=1.0,
                scheduler_event_index=0,
                packet_index=0,
                source_lineage_id="candidate-free-source",
                target_lineage_id="candidate-free-target",
            )
            observed = model.run_event_queue(max_events=2)
            require(len(observed) == 2, "candidate-free native event timing did not settle")

        event = _timed(event_operation, repetitions)

        def bundle_operation() -> None:
            bundle = temporary / "bundle"
            if bundle.exists():
                for child in bundle.iterdir():
                    child.unlink()
            else:
                bundle.mkdir()
            for index in range(8):
                (bundle / f"{index}.json").write_bytes(pretty_bytes({**sample, "component": index}))

        bundle = _timed(bundle_operation, repetitions)
        validation = _timed(lambda: jsonschema.validate(sample, sample_schema), repetitions)

        def reconstruction_operation() -> None:
            bundle_operation()
            for child in sorted((temporary / "bundle").iterdir()):
                json.loads(child.read_text(encoding="utf-8"))
                sha256_file(child)

        reconstruction = _timed(reconstruction_operation, repetitions)

    raw_rows = {
        "startup": startup,
        "inert_load": load,
        "fixed_native_event_pair": event,
        "eight_component_bundle_serialization": bundle,
        "schema_validation": validation,
        "eight_component_reconstruction_read": reconstruction,
    }
    references = {
        "startup_reference_ns": max(startup),
        "load_reference_ns": max(load),
        "event_reference_ns": (max(event) + 1) // 2,
        "bundle_reference_ns": (max(bundle) + 7) // 8,
        "validation_reference_ns": max(validation),
        "reconstruction_read_reference_ns": (max(reconstruction) + 7) // 8,
    }
    return with_digest(
        {
            "artifact_id": "P2-I3-I06-BR-CANDIDATE-FREE-TIMING",
            "artifact_version": ARTIFACT_VERSION,
            "iteration_id": "P2-I3-I06",
            "branch_id": "P2-I3-BR",
            "status": "retained_candidate_free_infrastructure_characterization",
            "environment": deepcopy(dict(environment)),
            "command": (
                "env PYTHONPATH=${RCAE_PYGRC_ROOT}/src OMP_NUM_THREADS=1 "
                "OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 "
                "BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONHASHSEED=0 "
                "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B "
                f"{SCRIPT_RELATIVE} build --graph-root ${{RCAE_PYGRC_ROOT}}"
            ),
            "clock": "time.monotonic_ns",
            "repetitions_per_operation": repetitions,
            "raw_monotonic_elapsed_ns": raw_rows,
            "host_resource_observation": host_resource_observation(),
            "reference_derivation": "maximum observed elapsed divided by fixed operation cardinality with upward integer rounding",
            "references": references,
            "candidate_blindness": {
                "candidate_topology_consumed": False,
                "candidate_values_consumed": False,
                "candidate_artifacts_consumed": False,
                "candidate_producer_invoked": False,
                "scientific_control_disposition_consumed": False,
                "scientific_result": False,
            },
            "evidence_effect": "infrastructure_resource_derivation_only",
        }
    )


NODE_ROLES = (
    "O",
    "T",
    "A_s",
    "A_m",
    "A_x",
    "A_d",
    "A_z_s",
    "A_z_m",
    "B_s",
    "B_m",
    "B_x",
    "B_d",
    "B_z_s",
    "B_z_m",
)
EDGE_DEFINITIONS = (
    ("A_boundary_in", "O", "A_s"),
    ("A_formation", "A_s", "A_m"),
    ("A_encounter", "A_m", "A_x"),
    ("A_boundary_out", "A_x", "T"),
    ("A_export", "A_m", "A_d"),
    ("A_source_control", "A_s", "A_z_s"),
    ("A_carrier_control", "A_m", "A_z_m"),
    ("B_boundary_in", "O", "B_s"),
    ("B_formation", "B_s", "B_m"),
    ("B_encounter", "B_m", "B_x"),
    ("B_boundary_out", "B_x", "T"),
    ("B_export", "B_m", "B_d"),
    ("B_source_control", "B_s", "B_z_s"),
    ("B_carrier_control", "B_m", "B_z_m"),
)
NODE_ORDERS = {
    101: NODE_ROLES,
    211: ("A_m", "B_x", "O", "A_d", "B_s", "T", "A_z_m", "B_d", "A_s", "B_m", "A_x", "B_z_s", "A_z_s", "B_z_m"),
    307: ("B_z_m", "A_x", "B_m", "T", "A_z_s", "B_d", "A_s", "O", "B_x", "A_m", "B_s", "A_d", "B_z_s", "A_z_m"),
}
EDGE_ORDERS = {
    101: tuple(row[0] for row in EDGE_DEFINITIONS),
    211: ("B_encounter", "A_export", "A_boundary_in", "B_source_control", "A_formation", "B_boundary_out", "A_z_unused"),
    307: ("A_carrier_control", "B_export", "A_boundary_out", "B_formation", "A_source_control", "B_boundary_in", "B_z_unused"),
}


def edge_order(realization: int) -> tuple[str, ...]:
    if realization == 101:
        return EDGE_ORDERS[101]
    prefix = tuple(item for item in EDGE_ORDERS[realization] if not item.endswith("_unused"))
    remaining = tuple(row[0] for row in EDGE_DEFINITIONS if row[0] not in prefix)
    return prefix + remaining


def baseline_values() -> dict[str, Fraction]:
    values = {"O": Fraction(1, 2), "T": Fraction(1, 2)}
    for route in ("A", "B"):
        values.update(
            {
                f"{route}_s": Fraction(7, 8),
                f"{route}_m": Fraction(3, 16),
                f"{route}_x": Fraction(1, 4),
                f"{route}_d": Fraction(1, 16),
                f"{route}_z_s": Fraction(1, 16),
                f"{route}_z_m": Fraction(1, 16),
            }
        )
    return values


def topology_record(realization: int) -> dict[str, Any]:
    node_ids = {role: index for index, role in enumerate(NODE_ORDERS[realization])}
    definitions = {role: (source, target) for role, source, target in EDGE_DEFINITIONS}
    edges = []
    for index, role in enumerate(edge_order(realization)):
        source, target = definitions[role]
        request_direction = {
            "A_formation": "A_s_to_A_m",
            "A_encounter": "A_m_to_A_x",
            "A_export": "A_m_to_A_d",
            "A_source_control": "A_s_to_A_z_s",
            "A_carrier_control": "A_m_to_A_z_m",
            "B_formation": "B_s_to_B_m",
            "B_encounter": "B_m_to_B_x",
            "B_export": "B_m_to_B_d",
            "B_source_control": "B_s_to_B_z_s",
            "B_carrier_control": "B_m_to_B_z_m",
        }.get(role)
        edges.append(
            {
                "edge_id": index,
                "edge_role": role,
                "native_structural_semantics": "undirected_port_edge",
                "source_role": source,
                "target_role": target,
                "source_node_id": node_ids[source],
                "target_node_id": node_ids[target],
                "conductance": fraction(Fraction(1, 1)),
                "base_conductance": fraction(Fraction(1, 1)),
                "geometric_length": fraction(Fraction(1, 1)),
                "flux_uv": fraction(Fraction(0, 1)),
                "flux_coupling": fraction(Fraction(0, 1)),
                "temporal_delay": "registered_delay_profile_tau",
                "allowed_packet_direction_ids": [] if request_direction is None else [request_direction],
                "unregistered_reverse_request_prohibited": True,
            }
        )
    return {
        "realization_id": realization,
        "seed_semantics": "deterministic_raw_node_and_edge_id_permutation_only",
        "node_role_to_raw_id": node_ids,
        "edge_role_to_raw_id": {row["edge_role"]: row["edge_id"] for row in edges},
        "nodes": [
            {"node_id": node_ids[role], "role": role, "initial_coherence": fraction(value)}
            for role, value in baseline_values().items()
        ],
        "edges": edges,
        "shared_nodes": ["O", "T"],
        "route_local_nodes": {
            route: [f"{route}_{suffix}" for suffix in ("s", "m", "x", "d", "z_s", "z_m")]
            for route in ("A", "B")
        },
        "interior_cross_route_edges": 0,
        "reservoir_outgoing_edges": 0,
        "structural_edge_directionality": "undirected",
        "packet_request_directionality": "operation_role_whitelist",
        "shared_boundary_packet_requests": "prohibited",
        "role_preserving": True,
    }


def build_baseline_model(topology: Mapping[str, Any], delay: int) -> LGRC9V3:
    graph = PortGraphBackend()
    nodes_by_id = sorted(topology["nodes"], key=lambda row: row["node_id"])
    for row in nodes_by_id:
        observed = graph.add_node({"role": row["role"], "registration_only": True})
        require(observed == row["node_id"], "node allocation drift")
    slots = {row["node_id"]: 0 for row in nodes_by_id}
    port_edges: dict[int, PortEdge] = {}
    for row in sorted(topology["edges"], key=lambda item: item["edge_id"]):
        source = row["source_node_id"]
        target = row["target_node_id"]
        source_slot = slots[source]
        target_slot = slots[target]
        observed = graph.connect_ports(source, source_slot, target, target_slot, {"role": row["edge_role"]})
        require(observed == row["edge_id"], "edge allocation drift")
        slots[source] += 1
        slots[target] += 1
        port_edges[observed] = PortEdge(source, source_slot, target, target_slot, conductance=1.0, flux_uv=0.0)
    states = {
        row["node_id"]: GRC9V3NodeState(coherence=row["initial_coherence"]["value"])
        for row in nodes_by_id
    }
    edge_ids = sorted(port_edges)
    base = GRC9V3State(
        topology=graph,
        nodes=states,
        port_edges=port_edges,
        base_conductance={edge_id: 1.0 for edge_id in edge_ids},
        geometric_length={edge_id: 1.0 for edge_id in edge_ids},
        temporal_delay={edge_id: float(delay) for edge_id in edge_ids},
        flux_coupling={edge_id: 0.0 for edge_id in edge_ids},
    )
    return LGRC9V3.from_state(
        base,
        {
            "dt": 1.0,
            "causal_modes": {
                "causal_layer_mode": "packetized_fixed_topology",
                "lgrc_runtime_level": "lgrc2",
                "lapse_policy": "unit",
                "edge_delay_policy": "constant_delay",
                "event_time_policy": "explicit_event_time_key",
                "proper_time_accumulation_policy": "local_event_frontier",
            },
        },
    )


def baseline_registry() -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]], dict[str, Any]]:
    topologies = {realization: topology_record(realization) for realization in REALIZATIONS}
    baselines: list[dict[str, Any]] = []
    check = {"model_instantiations": 0, "save_load_pairs": 0, "resets": 0, "candidate_operations": 0}
    with tempfile.TemporaryDirectory(prefix="p2-i3-i06-baseline-") as raw:
        temp = Path(raw)
        for profile, delay in PROFILES:
            for realization in REALIZATIONS:
                model = build_baseline_model(topologies[realization], delay)
                check["model_instantiations"] += 1
                original = digest_lgrc9v3_restoration_identity_v2(model)
                path = temp / f"{profile}-{realization}.json"
                model.save(str(path))
                loaded = LGRC9V3.load(str(path))
                check["save_load_pairs"] += 1
                loaded_digest = digest_lgrc9v3_restoration_identity_v2(loaded)
                require(loaded_digest == original, "native save/load semantic identity drift")
                loaded.reset()
                check["resets"] += 1
                reset_digest = digest_lgrc9v3_restoration_identity_v2(loaded)
                require(reset_digest == original, "native reset semantic identity drift")
                baselines.append(
                    {
                        "substrate_base_id": f"P2-I3-BR-BASE-{profile.upper()}-R{realization}",
                        "delay_profile_id": profile,
                        "edge_delay": delay,
                        "realization_id": realization,
                        "topology_identity": digest_data(topologies[realization]),
                        "native_restoration_v2_digest": original,
                        "load_restoration_v2_digest": loaded_digest,
                        "reset_restoration_v2_digest": reset_digest,
                        "registration_model_constructed": True,
                        "formation_operations": 0,
                        "lifecycle_operations": 0,
                        "encounter_operations": 0,
                    }
                )
    return baselines, topologies, check


FAMILIES = (
    ("core", 18, "arm", "standard"),
    ("formation_quantity_history", 6, "single", "complex"),
    ("focal_reference_role_exchange", 18, "arm", "standard"),
    ("current_state_relocation", 6, "single", "complex"),
    ("carrier_matched_false_trace", 6, "single", "complex"),
    ("causal_projection_matched_false_trace", 6, "single", "complex"),
    ("equal_carrier_clamp", 6, "single", "complex"),
    ("reservoir_clamp", 6, "single", "complex"),
    ("export_mass_organization", 6, "single", "complex"),
    ("export_policy_omission", 6, "single", "standard"),
    ("lifecycle_schedule_omission", 6, "single", "standard"),
)


def configurations(baselines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family, _, multiplicity, trajectory_class in FAMILIES:
        for base in baselines:
            arms = ARMS if multiplicity == "arm" else ("E",)
            for arm in arms:
                config_id = f"P2-I3-BR-CFG-{family.upper().replace('_','-')}-{base['delay_profile_id'].upper()}-R{base['realization_id']}-{arm}"
                intervention = {
                    "core": "none_primary_arm",
                    "formation_quantity_history": "one_pulse_9_over_32_versus_three_pulses_3_over_32",
                    "focal_reference_role_exchange": "exchange_focal_and_reference_route_roles",
                    "current_state_relocation": "move_complete_route_local_mutable_state_and_regenerate_destination_bindings",
                    "carrier_matched_false_trace": "match_carrier_and_encounter_without_valid_depositor_history",
                    "causal_projection_matched_false_trace": "match_all_causal_fields_replace_only_proven_noncause_provenance_and_cost_classification",
                    "equal_carrier_clamp": "clamp_C_m_equal_across_compared_arms",
                    "reservoir_clamp": "clamp_C_d_without_lifecycle_feedback",
                    "export_mass_organization": "remove_q_over_2_from_s_and_m_to_isolated_control_destinations",
                    "export_policy_omission": "omit_B_R_policy_with_native_future_schedule_held",
                    "lifecycle_schedule_omission": "neutralize_lifecycle_receipt_schedule_separately_from_O",
                }[family]
                rows.append(
                    {
                        "configuration_id": config_id,
                        "family_id": family,
                        "substrate_base_id": base["substrate_base_id"],
                        "delay_profile_id": base["delay_profile_id"],
                        "realization_id": base["realization_id"],
                        "arm": arm,
                        "trajectory_execution_class": trajectory_class,
                        "intervention_semantics": intervention,
                        "appendix": False,
                        "outcome": None,
                    }
                )
    return rows


def branch_registry(configs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for config in configs:
        family = config["family_id"]
        if family == "core":
            probes = (("j1", "focal"), ("j1", "reference"), ("j2", "focal"), ("j2", "reference"), ("j3", "focal"), ("j3", "reference"))
        elif family in {"formation_quantity_history", "causal_projection_matched_false_trace"}:
            probes = (("j2", "focal"), ("j2", "reference"), ("j3", "focal"), ("j3", "reference"))
        else:
            probes = (("j2", "focal"), ("j2", "reference"))
        trajectory_id = f"{config['configuration_id']}-TRAJECTORY"
        rows.append(
            {
                "case_id": trajectory_id,
                "case_kind": "scientific_branch",
                "branch_kind": "unprobed_trajectory",
                "configuration_id": config["configuration_id"],
                "substrate_base_id": config["substrate_base_id"],
                "execution_class": config["trajectory_execution_class"] + ("_trajectory" if config["trajectory_execution_class"] == "standard" else "_construction_or_comparison"),
                "parent_ids": [f"baseline:{config['substrate_base_id']}"],
                "terminal_probe": False,
                "outcome": None,
            }
        )
        for checkpoint, route_role in probes:
            rows.append(
                {
                    "case_id": f"{config['configuration_id']}-PROBE-{checkpoint.upper()}-{route_role.upper()}",
                    "case_kind": "scientific_branch",
                    "branch_kind": "terminal_probe",
                    "configuration_id": config["configuration_id"],
                    "substrate_base_id": config["substrate_base_id"],
                    "execution_class": "probe_only",
                    "parent_ids": [trajectory_id, f"checkpoint:{trajectory_id}:{checkpoint}"],
                    "checkpoint": checkpoint,
                    "participant_class": "same_participant",
                    "route_role": route_role,
                    "terminal_probe": True,
                    "outcome": None,
                }
            )
    core_e = {
        (row["substrate_base_id"]): row
        for row in configs
        if row["family_id"] == "core" and row["arm"] == "E"
    }
    for base_id, config in sorted(core_e.items()):
        trajectory_id = f"{config['configuration_id']}-TRAJECTORY"
        for route_role in ("focal", "reference"):
            rows.append(
                {
                    "case_id": f"P2-I3-BR-FRESH-NONDEPOSITOR-{base_id}-{route_role.upper()}",
                    "case_kind": "scientific_branch",
                    "branch_kind": "fresh_nondepositor_terminal_probe",
                    "configuration_id": config["configuration_id"],
                    "substrate_base_id": base_id,
                    "execution_class": "probe_only",
                    "parent_ids": [trajectory_id, f"checkpoint:{trajectory_id}:j2"],
                    "checkpoint": "j2",
                    "participant_class": "fresh_nondepositor",
                    "route_role": route_role,
                    "terminal_probe": True,
                    "outcome": None,
                }
            )
    for row in rows:
        if row["execution_class"] == "standard_trajectory":
            row["execution_class"] = "standard_trajectory"
        elif row["execution_class"] == "complex_construction_or_comparison":
            pass
    return rows


def integrity_registry(configs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    core = [row for row in configs if row["family_id"] == "core"]
    for config in core:
        for fault in ("invalid_load", "invalid_reset", "invalid_branch", "invalid_continuation"):
            rows.append(
                {
                    "case_id": f"P2-I3-BR-INTEGRITY-{config['configuration_id']}-{fault.upper().replace('_','-')}",
                    "case_kind": "quarantined_integrity_fault",
                    "fault_type": fault,
                    "configuration_id": config["configuration_id"],
                    "substrate_base_id": config["substrate_base_id"],
                    "execution_class": "integrity_fault",
                    "parent_ids": [f"cell-envelope:{config['configuration_id']}"],
                    "expected_terminal": "atomic_fail_closed_quarantined_no_scientific_continuation",
                    "scientific_evidence_effect": "none",
                    "outcome": None,
                }
            )
    return rows


def canonical_case_registry(
    branches: list[dict[str, Any]], faults: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return the immutable 450-case evidence identity space.

    Execution order is deliberately not encoded here. Control selectors and
    requirement sets retain the original one-based ordinal universe:
    integrity faults followed by the scientific branch registry.
    """
    rows = faults + branches
    require(len(rows) == 450, "canonical case registry count drift")
    require(len({row["case_id"] for row in rows}) == len(rows), "canonical case identity collision")
    return rows


def operational_baseline_entries(
    baselines: list[dict[str, Any]], configs: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Register six scientifically inert campaign baseline constructions."""
    core_by_base: dict[str, list[str]] = {row["substrate_base_id"]: [] for row in baselines}
    for config in configs:
        if config["family_id"] == "core":
            core_by_base[config["substrate_base_id"]].append(config["configuration_id"])
    rows = []
    for baseline in baselines:
        base_id = baseline["substrate_base_id"]
        rows.append(
            {
                "entry_id": f"P2-I3-BR-OPBASE-{baseline['delay_profile_id'].upper()}-R{baseline['realization_id']}",
                "entry_kind": "operational_baseline_construction",
                "case_id": None,
                "substrate_base_id": base_id,
                "delay_profile_id": baseline["delay_profile_id"],
                "realization_id": baseline["realization_id"],
                "execution_class": "complex_construction_or_comparison",
                "scientific_evidence_effect": "none",
                "declared_parent_refs": [],
                "parent_entry_ids": [],
                "produced_restoration_refs": [
                    f"baseline:{base_id}",
                    *[
                        f"cell-envelope:{config_id}"
                        for config_id in sorted(core_by_base[base_id])
                    ],
                ],
                "obligations": [
                    "construct_registered_native_topology_and_immutable_RCAE_baseline",
                    "verify_registered_source_and_runtime_identity",
                    "save_and_validate_native_restoration_identity_v2",
                    "emit_immutable_content_addressed_baseline_bundle",
                    "emit_typed_operational_baseline_terminal",
                ],
                "scientific_operation_counts": {
                    "formation": 0,
                    "export": 0,
                    "encounter_probe": 0,
                    "scientific_control": 0,
                    "integrity_fault_dispatch": 0,
                },
                "expected_terminal": "p2_i3_br_operational_baseline_terminal",
            }
        )
    require(len(rows) == 6, "operational baseline entry count drift")
    return rows


def _scientific_schedule_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    kind_rank = {
        "unprobed_trajectory": 0,
        "terminal_probe": 1,
        "fresh_nondepositor_terminal_probe": 2,
    }
    return (
        row["substrate_base_id"],
        row["configuration_id"],
        kind_rank[row["branch_kind"]],
        row.get("checkpoint", ""),
        row.get("participant_class", ""),
        row.get("route_role", ""),
        row["case_id"],
    )


def topological_scientific_order(branches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the frozen deterministic parent-before-probe permutation."""
    by_id = {row["case_id"]: row for row in branches}
    require(len(by_id) == len(branches), "scientific schedule identity collision")
    parents: dict[str, set[str]] = {}
    children: dict[str, set[str]] = {case_id: set() for case_id in by_id}
    for case_id, row in by_id.items():
        dependencies: set[str] = set()
        for parent in row["parent_ids"]:
            candidate = parent.split(":", 2)[1] if parent.startswith("checkpoint:") else parent
            if candidate in by_id:
                dependencies.add(candidate)
        parents[case_id] = dependencies
        for dependency in dependencies:
            children[dependency].add(case_id)
    ready = sorted((by_id[item] for item, deps in parents.items() if not deps), key=_scientific_schedule_key)
    ordered: list[dict[str, Any]] = []
    while ready:
        row = ready.pop(0)
        ordered.append(row)
        for child in sorted(children[row["case_id"]]):
            parents[child].remove(row["case_id"])
            if not parents[child]:
                ready.append(by_id[child])
        ready.sort(key=_scientific_schedule_key)
    require(len(ordered) == len(branches), "scientific dependency graph is cyclic or incomplete")
    return ordered


def governed_execution_schedule(
    baselines: list[dict[str, Any]],
    configs: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    faults: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the six-baseline plus 450-case governed execution DAG."""
    baseline_entries = operational_baseline_entries(baselines, configs)
    baseline_entry_by_base = {row["substrate_base_id"]: row["entry_id"] for row in baseline_entries}
    scientific_order = topological_scientific_order(branches)
    branch_ids = {row["case_id"] for row in branches}
    produced_checkpoints: dict[str, set[str]] = {
        row["case_id"]: set() for row in branches if row["branch_kind"] == "unprobed_trajectory"
    }
    for row in branches:
        for parent in row["parent_ids"]:
            if parent.startswith("checkpoint:"):
                trajectory_id = parent.split(":", 2)[1]
                require(trajectory_id in produced_checkpoints, "checkpoint has no registered trajectory producer")
                produced_checkpoints[trajectory_id].add(parent)
    case_rows = faults + scientific_order
    entries = deepcopy(baseline_entries)
    for case in case_rows:
        parent_entries: set[str] = {baseline_entry_by_base[case["substrate_base_id"]]}
        checkpoint_refs = [parent for parent in case["parent_ids"] if parent.startswith("checkpoint:")]
        for parent in case["parent_ids"]:
            candidate = parent.split(":", 2)[1] if parent.startswith("checkpoint:") else parent
            if candidate in branch_ids:
                parent_entries.add(candidate)
        entries.append(
            {
                "entry_id": case["case_id"],
                "entry_kind": case["case_kind"],
                "case_id": case["case_id"],
                "substrate_base_id": case["substrate_base_id"],
                "configuration_id": case["configuration_id"],
                "execution_class": case["execution_class"],
                "scientific_evidence_effect": case.get("scientific_evidence_effect", "registered_case_evidence"),
                "declared_parent_refs": deepcopy(case["parent_ids"]),
                "parent_entry_ids": sorted(parent_entries),
                "produced_checkpoint_refs": sorted(produced_checkpoints.get(case["case_id"], set())),
                "fresh_runtime_load_ref": checkpoint_refs[0] if checkpoint_refs else f"baseline:{case['substrate_base_id']}",
                "fresh_runtime_process": True,
                "parent_trajectory_advanced_in_child": False,
            }
        )
    ordinals = {row["entry_id"]: index for index, row in enumerate(entries, start=1)}
    for row in entries:
        row["schedule_ordinal"] = ordinals[row["entry_id"]]
        require(
            all(ordinals[parent] < row["schedule_ordinal"] for parent in row["parent_entry_ids"]),
            f"execution dependency does not precede child: {row['entry_id']}",
        )
    subtrees = []
    for baseline in baseline_entries:
        dependent_ids = [
            row["entry_id"]
            for row in entries
            if row["substrate_base_id"] == baseline["substrate_base_id"]
            and row["entry_id"] != baseline["entry_id"]
        ]
        subtrees.append(
            {
                "baseline_entry_id": baseline["entry_id"],
                "substrate_base_id": baseline["substrate_base_id"],
                "dependent_entry_ids": dependent_ids,
                "failure_status": "blocked_dependency",
            }
        )
    return {
        "canonical_case_registry_order": [row["case_id"] for row in canonical_case_registry(branches, faults)],
        "canonical_case_registry_count": 450,
        "canonical_case_registry_digest": digest_data([row["case_id"] for row in canonical_case_registry(branches, faults)]),
        "operational_baseline_entries": baseline_entries,
        "operational_baseline_entry_count": 6,
        "governed_entry_count": 456,
        "entries": entries,
        "order": [row["entry_id"] for row in entries],
        "dependency_dag": [
            {"entry_id": row["entry_id"], "parent_entry_ids": row["parent_entry_ids"]}
            for row in entries
        ],
        "baseline_failure_subtrees": subtrees,
        "independent_substrate_bases_continue_after_local_baseline_failure": True,
        "integrity_block_after_baselines": True,
        "scientific_order": "deterministic_topological_sort",
        "topological_tie_break_key": [
            "substrate_base_id",
            "configuration_id",
            "branch_kind_rank",
            "checkpoint",
            "participant_class",
            "route_role",
            "case_id",
        ],
        "result_responsive_reordering": False,
        "fresh_child_per_entry": True,
        "mutable_cross_child_state": False,
        "implicit_parent_trajectory_reexecution": False,
    }


CLASS_PROFILES = {
    "probe_only": {"startup_count": 1, "event_count": 1, "load_count": 1, "bundle_count": 1, "validation_count": 2, "class_minimum_seconds": 5, "outer_seconds": 180, "logical_bytes": 8 * MIB, "physical_bytes": 1 * MIB, "temporary_bytes": 2 * MIB, "stdout_bytes": 1 * MIB, "stderr_bytes": 1 * MIB},
    "standard_trajectory": {"startup_count": 1, "event_count": 30, "load_count": 1, "bundle_count": 4, "validation_count": 4, "class_minimum_seconds": 20, "outer_seconds": 180, "logical_bytes": 32 * MIB, "physical_bytes": 8 * MIB, "temporary_bytes": 16 * MIB, "stdout_bytes": 1 * MIB, "stderr_bytes": 1 * MIB},
    "complex_construction_or_comparison": {"startup_count": 1, "event_count": 36, "load_count": 3, "bundle_count": 8, "validation_count": 8, "class_minimum_seconds": 45, "outer_seconds": 180, "logical_bytes": 64 * MIB, "physical_bytes": 16 * MIB, "temporary_bytes": 32 * MIB, "stdout_bytes": 1 * MIB, "stderr_bytes": 1 * MIB},
    "integrity_fault": {"startup_count": 1, "event_count": 0, "load_count": 2, "bundle_count": 1, "validation_count": 4, "class_minimum_seconds": 5, "outer_seconds": 60, "logical_bytes": 4 * MIB, "physical_bytes": 1 * MIB, "temporary_bytes": 4 * MIB, "stdout_bytes": 1 * MIB, "stderr_bytes": 1 * MIB},
}


def resource_registry(entries: list[dict[str, Any]], timing: Mapping[str, Any]) -> dict[str, Any]:
    refs = timing["references"]
    safety_factor = 8
    profiles = deepcopy(CLASS_PROFILES)
    for name, row in profiles.items():
        reference_ns = (
            row["startup_count"] * refs["startup_reference_ns"]
            + row["event_count"] * refs["event_reference_ns"]
            + row["load_count"] * refs["load_reference_ns"]
            + row["bundle_count"] * refs["bundle_reference_ns"]
            + row["validation_count"] * refs["validation_reference_ns"]
        )
        derived = max(row["class_minimum_seconds"], (safety_factor * reference_ns + 999_999_999) // 1_000_000_000)
        require(derived <= row["outer_seconds"], f"class timeout exceeds outer ceiling: {name}")
        row["reference_time_ns"] = reference_ns
        row["safety_factor"] = safety_factor
        row["case_timeout_seconds"] = derived
    assignments = []
    counts = {name: 0 for name in profiles}
    for index, entry in enumerate(entries, start=1):
        class_id = entry["execution_class"]
        require(class_id in profiles, f"unknown execution class: {class_id}")
        counts[class_id] += 1
        assignments.append(
            {
                "entry_id": entry["entry_id"],
                "entry_kind": entry["entry_kind"],
                "case_id": entry["case_id"],
                "schedule_ordinal": index,
                "execution_class": class_id,
                "case_timeout_seconds": profiles[class_id]["case_timeout_seconds"],
                "prospective_logical_bytes": profiles[class_id]["logical_bytes"],
                "prospective_physical_bytes": profiles[class_id]["physical_bytes"],
                "prospective_temporary_bytes": profiles[class_id]["temporary_bytes"],
                "prospective_stdout_bytes": profiles[class_id]["stdout_bytes"],
                "prospective_stderr_bytes": profiles[class_id]["stderr_bytes"],
            }
        )
    child_seconds = sum(row["case_timeout_seconds"] for row in assignments)
    aggregation = 1800
    overhead = 600
    retry_child_grace = sum(profiles[name]["case_timeout_seconds"] + 10 for name, count in counts.items() if count)
    retry_admin = max(5, (8 * refs["reconstruction_read_reference_ns"] + 999_999_999) // 1_000_000_000)
    campaign = child_seconds + aggregation + overhead + retry_child_grace + retry_admin
    logical = sum(row["prospective_logical_bytes"] for row in assignments)
    physical = sum(row["prospective_physical_bytes"] for row in assignments)
    logs = sum(row["prospective_stdout_bytes"] + row["prospective_stderr_bytes"] for row in assignments)
    active_temp = max(row["prospective_temporary_bytes"] for row in assignments)
    retry_disk = sum(
        profiles[name]["physical_bytes"] + profiles[name]["temporary_bytes"] + profiles[name]["stdout_bytes"] + profiles[name]["stderr_bytes"] + 4 * MIB
        for name, count in counts.items()
        if count
    )
    physical_governed = physical + logs + active_temp + retry_disk
    require(campaign <= 30 * 3600, "derived campaign exceeds 30 hours")
    require(physical_governed <= 8 * GIB, "derived physical budget exceeds 8 GiB")
    return {
        "execution_classes": profiles,
        "class_counts": counts,
        "assignment_digest": digest_data(assignments),
        "assignments": assignments,
        "operational_baseline_artifact_projection": {
            "immutable_content_addressed_bundles": sum(
                row["entry_kind"] == "operational_baseline_construction" for row in entries
            ),
            "typed_operational_terminals": sum(
                row["entry_kind"] == "operational_baseline_construction" for row in entries
            ),
            "attempt_claims_and_resource_receipts": sum(
                row["entry_kind"] == "operational_baseline_construction" for row in entries
            ),
            "scientific_artifacts": 0,
        },
        "case_timeout_formula": "max(class_minimum_seconds,ceil(8*reference_time_ns/1e9))",
        "campaign": {
            "primary_child_seconds": child_seconds,
            "aggregation_allowance_seconds": aggregation,
            "campaign_overhead_seconds": overhead,
            "retry_child_and_grace_reserve_seconds": retry_child_grace,
            "retry_administration_seconds": retry_admin,
            "exact_campaign_ceiling_seconds": campaign,
            "outer_campaign_ceiling_seconds": 30 * 3600,
            "uniform_outer_child_projection_seconds": 72 * 60 + 384 * 180,
            "retry_outer_projection_seconds": 640,
        },
        "bytes": {
            "exact_logical_artifact_maximum_bytes": logical,
            "prospective_unique_physical_blob_bytes": physical,
            "prospective_captured_log_bytes": logs,
            "maximum_active_temporary_bytes": active_temp,
            "incremental_retry_disk_reserve_bytes": retry_disk,
            "governed_physical_projection_bytes": physical_governed,
            "governed_physical_ceiling_bytes": 8 * GIB,
            "individual_file_ceiling_bytes": 512 * MIB,
            "child_stdout_ceiling_bytes": 16 * MIB,
            "child_stderr_ceiling_bytes": 16 * MIB,
        },
        "memory": {
            "experiment_RLIMIT_AS": None,
            "experiment_RSS_kill_threshold": None,
            "required_observations": ["host_physical_memory", "available_memory", "swap_total", "swap_available", "cgroup_ceiling_if_present", "supervisor_peak_RSS", "child_peak_RSS", "process_tree_peak_RSS", "exit_status", "signal", "OOM_evidence"],
        },
        "process_policy": {"supervisor_max": 1, "active_child_max": 1, "child_parallelism": 1, "worker_reuse": False, "network": False, "accelerator": False, "distributed": False, "termination_grace_seconds": 10},
        "content_store": {"identity": "sha256_exact_bytes_only", "write_once": True, "exclusive_create": True, "rehash_before_use": True, "semantic_deduplication": False, "garbage_collection_during_campaign_or_reconstruction": False},
    }


def component_contracts() -> dict[str, Any]:
    roles = {
        "native.json": "exact_retained_native_bytes_noncanonical_resave",
        "native-identity-v2.json": "native_restoration_semantic_identity",
        "policy.json": "B_R_export_policy_and_lifecycle_state",
        "execution.json": "schedule_pending_events_and_case_semantics",
        "measurement.json": "registered_response_and_observation_boundary",
        "reset.json": "paired_native_and_RCAE_baseline_identity",
        "audit.json": "lineage_provenance_and_forbidden_read_attestation",
        "manifest.json": "noncircular_component_and_binding_graph",
    }
    return {
        "bundle_schema_id": "P2-I3-BR-I06-EIGHT-COMPONENT-BUNDLE-V1",
        "machine_record_schema": EXECUTION_SCHEMA_RELATIVE,
        "machine_record_root_class": "checkpoint_manifest",
        "component_roles": roles,
        "component_count": 8,
        "exact_composite_identity": "detached_sha256_of_canonical_manifest_payload_after_component_file_and_semantic_digests",
        "causal_projection_identity": "closed_normalized_continuation_fields_only_unknown_fields_rejected",
        "native_identity_rule": "retain_original_bytes_and_restoration_v2_digest; later resave byte equality not required",
        "reset_rule": "semantic_identity_equal_fresh_lineage_exact_bundle_identity_distinct",
        "atomic_refusal_rule": "native_and_B_R_mechanism_state_unchanged_typed_terminal_evidence_only",
        "logical_reconstruction": "all_eight_paths_reconstructed_byte_exactly_from_rehashed_blobs",
        "unknown_continuation_fields": "reject",
    }


def cell_envelopes(configs: list[dict[str, Any]], baselines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_base = {row["substrate_base_id"]: row for row in baselines}
    rows = []
    for config in configs:
        if config["family_id"] != "core":
            continue
        base = by_base[config["substrate_base_id"]]
        payload = {
            "configuration_id": config["configuration_id"],
            "substrate_base_id": config["substrate_base_id"],
            "arm": config["arm"],
            "native_restoration_v2_digest": base["native_restoration_v2_digest"],
            "policy_enabled": config["arm"] == "E",
            "formation_mode": "withdrawn" if config["arm"] == "W" else "repeated_three_by_3_over_32",
            "lifecycle_mode": {"W": "none", "O": "neutralized", "E": "enabled"}[config["arm"]],
            "initial_lineage": "fresh_at_execution",
        }
        rows.append({**payload, "cell_semantic_envelope_digest": digest_data(payload), "exact_native_bytes_deferred_to_immutable_campaign_baseline_construction": True})
    return rows


def pairing_registry() -> dict[str, Any]:
    fields = [
        "delay_profile_id", "realization_id", "role_assignment_id", "base_arm_or_treatment_id",
        "control_family_id", "checkpoint_or_encounter_id", "participant_class", "route_role",
        "clean_parent_semantic_id", "causal_projection_id_or_match", "request_construction_id",
        "request_timing_id", "future_schedule_id", "observation_boundary_id",
    ]
    return {
        "pairing_key_id": "P2-I3-BR-DEC038-FULL-SEMANTIC-PAIRING-KEY",
        "fields": fields,
        "candidate_and_reference_match_all_except": ["prospectively_declared_intervention_field_ids"],
        "numeric_delta_applies_to": ["m_trace", "m_export", "encounter_margin_comparisons"],
        "exact_equality_applies_to": ["global_conservation", "native_restoration_v2", "causal_continuation_projection", "registered_held_fixed_fields"],
    }


def evidence_case_sets(
    configs: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    faults: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Materialize the exact finite evidence populations used by I06.

    Sets are centralized so controls and requirements can reuse exact case
    identities without duplicating hundreds of IDs in every leg record.
    """
    by_config = {row["configuration_id"]: row for row in configs}
    case_universe = faults + branches
    case_ordinal = {row["case_id"]: index for index, row in enumerate(case_universe, start=1)}
    config_ordinal = {row["configuration_id"]: index for index, row in enumerate(configs, start=1)}

    def select_science(
        *,
        families: set[str] | None = None,
        arms: set[str] | None = None,
        branch_kinds: set[str] | None = None,
        terminal_only: bool = False,
    ) -> list[dict[str, Any]]:
        selected = []
        for row in branches:
            config = by_config[row["configuration_id"]]
            if families is not None and config["family_id"] not in families:
                continue
            if arms is not None and config["arm"] not in arms:
                continue
            if branch_kinds is not None and row["branch_kind"] not in branch_kinds:
                continue
            if terminal_only and not row["terminal_probe"]:
                continue
            selected.append(row)
        return selected

    ordinary_branches = {"unprobed_trajectory", "terminal_probe"}
    specifications: list[tuple[str, str, list[dict[str, Any]], list[str], list[str]]] = [
        ("ALL-SCIENTIFIC", "all_live_scientific_and_control_branches", branches, [], []),
        ("ALL-GOVERNED", "all_scientific_and_quarantined_integrity_cases", branches + faults, [], []),
        ("ALL-TERMINAL-PROBES", "all_fixed_branch_local_terminal_requests", select_science(terminal_only=True), ["checkpoint_or_encounter_id", "participant_class", "route_role"], []),
        ("ALL-TRAJECTORIES", "all_unprobed_scientific_trajectories", select_science(branch_kinds={"unprobed_trajectory"}), ["base_arm_or_treatment_id", "control_family_id"], []),
        ("CORE-ALL", "core_W_O_E_trajectory_and_probe_population", select_science(families={"core"}, branch_kinds=ordinary_branches), ["base_arm_or_treatment_id"], []),
        ("CORE-W-E", "core_deposition_withdrawal_W_versus_E", select_science(families={"core"}, arms={"W", "E"}, branch_kinds=ordinary_branches), ["base_arm_or_treatment_id"], []),
        ("CORE-O-E", "core_lifecycle_O_versus_E", select_science(families={"core"}, arms={"O", "E"}, branch_kinds=ordinary_branches), ["base_arm_or_treatment_id"], []),
        ("CORE-E", "core_repeated_formation_export_enabled", select_science(families={"core"}, arms={"E"}, branch_kinds=ordinary_branches), ["base_arm_or_treatment_id"], []),
        ("CORE-TRAJECTORIES", "core_unprobed_formation_and_lifecycle_trajectories", select_science(families={"core"}, branch_kinds={"unprobed_trajectory"}), ["base_arm_or_treatment_id"], []),
        ("FORMATION-HISTORY", "quantity_matched_one_pulse_versus_repeated_formation", select_science(families={"formation_quantity_history"}), ["control_family_id", "request_timing_id"], []),
        ("ROLE-EXCHANGE", "semantic_focal_reference_role_exchange", select_science(families={"focal_reference_role_exchange"}), ["role_assignment_id"], []),
        ("RAW-ID-PERMUTATION", "cross_realization_role_preserving_raw_id_permutation", select_science(families={"core"}, branch_kinds=ordinary_branches), ["realization_id"], ["role_assignment_id", "base_arm_or_treatment_id", "checkpoint_or_encounter_id", "participant_class", "route_role"]),
        ("CURRENT-STATE-RELOCATION", "complete_current_route_local_mechanism_state_relocation", select_science(families={"current_state_relocation"}), ["control_family_id"], []),
        ("CARRIER-FALSE-TRACE", "carrier_matched_invalid_formation_history", select_science(families={"carrier_matched_false_trace"}), ["control_family_id", "causal_projection_id_or_match"], []),
        ("CAUSAL-PROJECTION-FALSE-TRACE", "complete_causal_projection_matched_invalid_formation_history", select_science(families={"causal_projection_matched_false_trace"}), ["control_family_id", "causal_projection_id_or_match"], []),
        ("EQUAL-CARRIER", "equal_carrier_clamp", select_science(families={"equal_carrier_clamp"}), ["control_family_id"], []),
        ("RESERVOIR-CLAMP", "isolated_reservoir_clamp", select_science(families={"reservoir_clamp"}), ["control_family_id"], []),
        ("EXPORT-MASS-ORGANIZATION", "equal_mass_loss_different_route_organization", select_science(families={"export_mass_organization"}), ["control_family_id"], []),
        ("EXPORT-POLICY-OMISSION", "B_R_export_policy_omission", select_science(families={"export_policy_omission"}), ["control_family_id"], []),
        ("LIFECYCLE-SCHEDULE-OMISSION", "lifecycle_invocation_omission_distinct_from_O", select_science(families={"lifecycle_schedule_omission"}), ["future_schedule_id", "control_family_id"], []),
        ("STATE-HISTORY-DISCRIMINATOR", "core_repeated_E_plus_quantity_and_causal_projection_history_controls", select_science(families={"core"}, arms={"E"}, branch_kinds=ordinary_branches) + select_science(families={"formation_quantity_history", "causal_projection_matched_false_trace"}), ["control_family_id", "causal_projection_id_or_match", "request_timing_id"], []),
        ("TAU-VARIATION", "matched_tau_1_versus_tau_2_core_comparisons", select_science(families={"core"}, branch_kinds=ordinary_branches), ["delay_profile_id"], ["realization_id", "role_assignment_id", "base_arm_or_treatment_id", "checkpoint_or_encounter_id", "participant_class", "route_role"]),
        ("FRESH-NONDEPOSITOR", "twelve_conditional_fresh_nondepositor_probes", select_science(branch_kinds={"fresh_nondepositor_terminal_probe"}), ["participant_class"], ["delay_profile_id", "realization_id", "checkpoint_or_encounter_id", "route_role"]),
        ("INTEGRITY-FAULTS", "quarantined_composite_integrity_faults", faults, ["fault_type"], []),
    ]
    pairing_fields = pairing_registry()["fields"]
    result = []
    for set_id, selector_kind, cases, interventions, extra_held in specifications:
        case_ids = sorted({row["case_id"] for row in cases})
        case_ordinals = sorted(case_ordinal[case_id] for case_id in case_ids)
        config_ids = sorted({row["configuration_id"] for row in cases})
        config_ordinals = sorted(config_ordinal[config_id] for config_id in config_ids)
        family_ids = sorted({by_config[row["configuration_id"]]["family_id"] for row in cases})
        held = sorted(set(pairing_fields).difference(interventions).union(extra_held))
        result.append(
            {
                "case_set_id": f"P2-I3-BR-CASESET-{set_id}",
                "selector_kind": selector_kind,
                "case_universe": "matrix.integrity_fault_cases_then_scientific_branches_registry_order_1_based",
                "case_ordinals": case_ordinals,
                "selected_case_count": len(case_ordinals),
                "configuration_universe": "matrix.configurations_registry_order_1_based",
                "configuration_ordinals": config_ordinals,
                "configuration_family_ids": family_ids,
                "intervention_field_ids": interventions,
                "held_fixed_field_ids": held,
                "exact_membership_digest": digest_data(case_ids),
                "exact_configuration_membership_digest": digest_data(config_ids),
            }
        )
    return result


CONTROL_CASE_SET_IDS = {
    "P2-I3-BR-CTRL-04-LEG-01-PARTICIPANT-FIELD-BOUNDARY": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-04-LEG-02-CAUSAL-CHAIN": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-05-LEG-01-NONPRIVATE-LOCAL-CARRIER": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-06-LEG-01-SURFACE-DEPENDENCE": ["CORE-W-E", "CURRENT-STATE-RELOCATION", "RAW-ID-PERMUTATION", "ROLE-EXCHANGE", "CARRIER-FALSE-TRACE", "CAUSAL-PROJECTION-FALSE-TRACE"],
    "P2-I3-BR-CTRL-07-LEG-01-ORDERED-COMPOSITION": ["CORE-ALL"],
    "P2-I3-BR-CTRL-08-LEG-01-EXPORT-POLICY-OMISSION": ["EXPORT-POLICY-OMISSION"],
    "P2-I3-BR-CTRL-08-LEG-02-LIFECYCLE-SCHEDULE": ["LIFECYCLE-SCHEDULE-OMISSION"],
    "P2-I3-BR-CTRL-08-LEG-03-ENCOUNTER-ADAPTER-BOUNDARY": ["ALL-TERMINAL-PROBES"],
    "P2-I3-BR-CTRL-08-LEG-04-COMPOSITE-COORDINATION": ["ALL-GOVERNED"],
    "P2-I3-BR-CTRL-09-LEG-01-FORMATION-COST": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-09-LEG-02-GLOBAL-CONSERVATION": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-09-LEG-03-UNREGISTERED-LEAKAGE": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-09-LEG-04-RESERVOIR-ISOLATION": ["RESERVOIR-CLAMP"],
    "P2-I3-BR-CTRL-09-LEG-05-EXPORT-MASS-ORGANIZATION": ["EXPORT-MASS-ORGANIZATION"],
    "P2-I3-BR-CTRL-11-LEG-01-PARTICIPANT-MEDIUM-BOUNDARY": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-15-LEG-01-CONSTRUCTED-NATIVE-TRANSITION": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-16-LEG-01-CONSTRUCTION-COMPLETENESS": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CTRL-17-LEG-01-RUNTIME-SOURCE-BINDING": ["ALL-GOVERNED"],
    "P2-I3-BR-CTRL-17-LEG-02-RUNTIME-RECONSTRUCTION": ["ALL-GOVERNED"],
    "P2-I3-BR-L03-CTRL-01-LEG-01-DEPOSITION-WITHDRAWAL": ["CORE-W-E"],
    "P2-I3-BR-L03-CTRL-02-LEG-01-COMPLETE-STATE-RELOCATION": ["CURRENT-STATE-RELOCATION"],
    "P2-I3-BR-L03-CTRL-02-LEG-02-ROLE-ID-PERMUTATION": ["RAW-ID-PERMUTATION"],
    "P2-I3-BR-L03-CTRL-03-LEG-01-CARRIER-MATCHED-FALSE-TRACE": ["CARRIER-FALSE-TRACE"],
    "P2-I3-BR-L03-CTRL-03-LEG-02-CAUSAL-PROJECTION-MATCHED-FALSE-TRACE": ["CAUSAL-PROJECTION-FALSE-TRACE"],
    "P2-I3-BR-L03-CTRL-04-LEG-01-O-E-LIFECYCLE": ["CORE-O-E"],
    "P2-I3-BR-L03-CTRL-04-LEG-02-EQUAL-CARRIER-CLAMP": ["EQUAL-CARRIER"],
    "P2-I3-BR-L03-CTRL-04-LEG-03-RESERVOIR-CLAMP": ["RESERVOIR-CLAMP"],
    "P2-I3-BR-L03-CTRL-04-LEG-04-EXPORT-MASS-ORGANIZATION": ["EXPORT-MASS-ORGANIZATION"],
    "P2-I3-BR-L03-CTRL-04-LEG-05-ELIGIBLE-ZERO-FLOOR": ["CORE-ALL"],
    "P2-I3-BR-L03-CTRL-05-LEG-01-FIXED-BRANCH-REQUESTS": ["ALL-TERMINAL-PROBES"],
    "P2-I3-BR-L03-CTRL-05-LEG-02-FORBIDDEN-CROSS-ROUTE-READS": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-L03-CTRL-05-LEG-03-PARTICIPANT-TAG-BOUNDARY": ["ALL-TERMINAL-PROBES"],
}


REQUIREMENT_CASE_SET_IDS = {
    "P2-I3-BR-DISC-01-FORMATION-QUANTITY-TEMPORAL-MATCH": ["FORMATION-HISTORY"],
    "P2-I3-BR-DISC-02-EXPORT-MASS-ORGANIZATION": ["EXPORT-MASS-ORGANIZATION"],
    "P2-I3-BR-DISC-03-COMPLETE-STATE-HISTORY": ["STATE-HISTORY-DISCRIMINATOR"],
    "P2-I3-BR-DISC-04-GEOMETRY-OR-TIMESCALE": ["TAU-VARIATION"],
    "P2-I3-BR-DISC-05-FRESH-NONDEPOSITOR": ["FRESH-NONDEPOSITOR"],
    "P2-I3-BR-VALID-01-EXACT-RESTORATION": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-VALID-02-EQUAL-INPUT-CONTINUATION": ["STATE-HISTORY-DISCRIMINATOR"],
    "P2-I3-BR-VALID-03-RECONSTRUCTION": ["ALL-GOVERNED"],
    "P2-I3-BR-VALID-04-FORBIDDEN-READ": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-VALID-05-RUNTIME-SOURCE-BINDING": ["ALL-GOVERNED"],
    "P2-I3-BR-CLAIM-01-PRODUCER-DEPENDENCE": ["ALL-SCIENTIFIC"],
    "P2-I3-BR-CLAIM-02-FIXTURE-LOCK": ["ALL-GOVERNED"],
    "P2-I3-BR-CLAIM-03-NATIVE-RCAE-ATTRIBUTION": ["ALL-GOVERNED"],
    "P2-I3-BR-CLAIM-04-TRAIL-STIGMERGIC-PARTICIPANT": ["ALL-TERMINAL-PROBES"],
}

EXPECTED_CASE_SET_COUNTS = {
    "ALL-SCIENTIFIC": 378,
    "ALL-GOVERNED": 450,
    "ALL-TERMINAL-PROBES": 288,
    "ALL-TRAJECTORIES": 90,
    "CORE-ALL": 126,
    "CORE-W-E": 84,
    "CORE-O-E": 84,
    "CORE-E": 42,
    "CORE-TRAJECTORIES": 18,
    "FORMATION-HISTORY": 30,
    "ROLE-EXCHANGE": 54,
    "RAW-ID-PERMUTATION": 126,
    "CURRENT-STATE-RELOCATION": 18,
    "CARRIER-FALSE-TRACE": 18,
    "CAUSAL-PROJECTION-FALSE-TRACE": 30,
    "EQUAL-CARRIER": 18,
    "RESERVOIR-CLAMP": 18,
    "EXPORT-MASS-ORGANIZATION": 18,
    "EXPORT-POLICY-OMISSION": 18,
    "LIFECYCLE-SCHEDULE-OMISSION": 18,
    "STATE-HISTORY-DISCRIMINATOR": 102,
    "TAU-VARIATION": 126,
    "FRESH-NONDEPOSITOR": 12,
    "INTEGRITY-FAULTS": 72,
}


def control_projection(
    i04: Mapping[str, Any],
    case_sets: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    governance = i04["control_governance"]
    original = governance["leg_policy_registry"]
    source_rows = governance["common_control_legs"] + governance["lane_control_legs"]
    descriptors = {row["leg_id"]: row for row in source_rows}
    require(set(original) == set(descriptors), "I04 control-leg identity mismatch")
    rows = []
    for leg_id in sorted(original):
        meaning = deepcopy(original[leg_id])
        descriptor = descriptors[leg_id]
        selected_suffixes = CONTROL_CASE_SET_IDS.get(leg_id, [])
        selected_ids = [f"P2-I3-BR-CASESET-{item}" for item in selected_suffixes]
        selected_records = [row for row in case_sets if row["case_set_id"] in selected_ids]
        require(len(selected_records) == len(selected_ids), f"unknown case set for {leg_id}")
        selected_cases = sorted({ordinal for record in selected_records for ordinal in record["case_ordinals"]})
        interventions = sorted({field for record in selected_records for field in record["intervention_field_ids"]})
        held = sorted(set(pairing_registry()["fields"]).difference(interventions))
        scientific = descriptor["control_class"] in {"causal_intervention", "scientific_comparison"}
        require(
            not scientific or descriptor["applicability"] == "not_applicable" or selected_cases,
            f"applicable scientific leg has no exact case selector: {leg_id}",
        )
        exemption = (
            "no_registered_parent_basin_in_B_R_realization"
            if descriptor["applicability"] == "not_applicable"
            else ("guard_or_source_leg_has_no_case_population" if not selected_cases else "")
        )
        evidence_roles = sorted(
            {
                {
                    "inherited/source verification": "source_verification_record",
                    "terminal report guard": "terminal_guard_record",
                    "registration guard": "registration_validation_record",
                    "causal-chain evidence": "causal_chain_receipt",
                    "numeric execution comparison": "paired_numeric_comparison_record",
                    "withdrawal comparison": "withdrawal_comparison_record",
                    "reconstruction evidence": "reconstruction_receipt",
                }[evidence_type]
                for evidence_type in descriptor["evidence_types"]
            }
        )
        rows.append(
            {
                "leg_id": leg_id,
                "parent_control_id": descriptor["parent_control_id"],
                "applicability": descriptor["applicability"],
                "control_class": descriptor["control_class"],
                "evidence_types": descriptor["evidence_types"],
                **meaning,
                "intervention_field_ids": interventions,
                "held_fixed_field_ids": held,
                "pairing_exemption_reason": exemption,
                "scientific_or_guard_class": "scientific" if scientific else "guard",
                "minimum_valid_artifact_count": len(selected_cases) if selected_cases else 1,
                "completion_rule": "every_selected_case_has_valid_terminal_evidence_plus_independent_leg_resolution_no_disposition_copying" if selected_cases else "independent_noncase_guard_resolution_required_no_disposition_copying",
                "selected_case_set_ids": selected_ids,
                "selected_case_count": len(selected_cases),
                "evidence_artifact_roles": evidence_roles,
                "case_selector_rule": "exact_union_of_digest_bound_case_set_registry_entries" if selected_cases else "guard_or_source_artifact_selector_only",
                "observed_resolution": None,
                "evidence_refs": [],
            }
        )
    requirements = []
    for row in governance["requirement_registry"]:
        selected_ids = [
            f"P2-I3-BR-CASESET-{item}"
            for item in REQUIREMENT_CASE_SET_IDS[row["requirement_id"]]
        ]
        selected_records = [item for item in case_sets if item["case_set_id"] in selected_ids]
        require(len(selected_records) == len(selected_ids), f"unknown requirement case set: {row['requirement_id']}")
        selected_cases = sorted({ordinal for item in selected_records for ordinal in item["case_ordinals"]})
        require(selected_cases, f"requirement has no exact case selector: {row['requirement_id']}")
        requirements.append(
            {
                **deepcopy(row),
                "selected_case_set_ids": selected_ids,
                "selected_case_count": len(selected_cases),
                "minimum_valid_artifact_count": len(selected_cases),
                "registered_evidence_selectors": [
                    "case_terminal_records", "control_leg_resolutions", "causal_chain_receipts",
                    "reconstruction_receipt", "runtime_source_binding",
                ],
                "completion_owner": "P2-I3-I09" if row["group"] == "scientific" else ("P2-I3-I10" if row["group"] == "validity" else "P2-I3-I11"),
                "observed_resolution": None,
            }
        )
    return rows, requirements


def attempt_policy(entries: list[dict[str, Any]], resources: Mapping[str, Any]) -> dict[str, Any]:
    slots = [
        {
            "entry_id": row["entry_id"],
            "entry_kind": row["entry_kind"],
            "case_id": row["case_id"],
            "primary_attempt": 1,
            "scientific_retries": 0,
            "inactive_class_retry_position": 2,
            "execution_class": row["execution_class"],
            "schedule_ordinal": index,
        }
        for index, row in enumerate(entries, start=1)
    ]
    propagation = [
        {"trigger": "failed_terminal_probe", "scope": "branch", "dependent_status": "none_independent_cases_continue"},
        {"trigger": "failed_trajectory_parent", "scope": "registered_probe_subtree", "dependent_status": "blocked_dependency"},
        {"trigger": "failed_substrate_baseline", "scope": "profile_realization_subtree", "dependent_status": "blocked_dependency"},
        {"trigger": "case_specific_invalid_binding", "scope": "prospectively_bound_branch_or_configuration", "dependent_status": "invalid_execution"},
        {"trigger": "shared_authority_schema_validator_content_store_or_graph_guard", "scope": "whole_campaign", "dependent_status": "not_started_campaign_stop"},
    ]
    return {
        "registered_case_count": sum(row["case_id"] is not None for row in entries),
        "registered_operational_baseline_entry_count": sum(
            row["entry_kind"] == "operational_baseline_construction" for row in entries
        ),
        "governed_entry_count": len(entries),
        "primary_attempt_slots": len(slots),
        "slots": slots,
        "class_retry_tokens": [
            {"token_id": f"P2-I3-BR-RETRY-{name.upper().replace('_','-')}", "execution_class": name, "maximum_allocations": 1, "allocation": None}
            for name, count in resources["class_counts"].items()
            if count
        ],
        "retry_token_allocation_rule": "first_retry_eligible_failure_in_frozen_schedule_order_with_matching_execution_class_including_operational_baselines",
        "maximum_governed_child_starts": len(entries) + 4,
        "campaign_supervisor_starts": {"primary": 1, "resume_maximum": 1},
        "claim_protocol": {"campaign_claim_consumes": "P2-I3-EXEC-FREEZE", "governed_entry_claim_before_child": True, "case_claim_required_when_case_id_present": True, "operational_baseline_claim_required": True, "exclusive": True, "durably_flushed": True, "immutable": True, "deletion_or_reuse": False},
        "phases": ["P0_governed_entry_claim_durable", "P1_child_started", "P2_authorities_and_inputs_loaded", "P3_parent_restored_and_validated", "P4_entry_boundary_armed", "P5_entry_specific_dispatch_authorized", "P6_output_observed", "P7_terminal_receipt_complete"],
        "P5_owner": "external_supervisor_one_shot_authorization",
        "retry_eligibility": "complete_externally_attested_failure_at_or_before_P4_and_no_P5_or_result_artifact",
        "statuses": ["valid_terminal", "attested_pre_candidate_infrastructure_failure", "post_candidate_infrastructure_failure", "invalid_execution", "unknown_boundary_failure", "preclaim_failure", "blocked_dependency", "not_started_campaign_stop", "authority_breach"],
        "dependency_propagation": propagation,
        "resume_requirements": ["same_host_boot", "no_active_child", "no_unresolved_case_claim", "complete_ledger", "next_position_unclaimed", "unchanged_authority_environment_worktree", "consistent_paths_and_content_store", "campaign_time_and_byte_budgets_open", "resume_count_zero"],
        "cycle_closure_precedence": ["failed_closed", "invalid", "bounded_incomplete", "complete"],
        "cross_cycle_rule": "new_registration_and_activation_preserve_prior_cycle_and_rerun_complete_affected_comparison_closure",
    }


def producer_inventory(configs: list[dict[str, Any]], branches: list[dict[str, Any]], faults: list[dict[str, Any]]) -> list[dict[str, Any]]:
    populations = {"configurations": len(configs), "scientific_branches": len(branches), "integrity_cases": len(faults)}
    definitions = [
        ("BR-PROD-01-EXPORT-POLICY", "RCAE", "contract_required", "after_native_lifecycle_receipt_before_native_export_request", "eligibility_amount_cap_time_destination", "native_route_local_export_policy_surface"),
        ("BR-PROD-02-POLICY-STATE-RESTORATION", "RCAE", "contract_required", "mechanism_continuation_and_reset", "cursor_consumed_receipts_pending_reservation", "native_serialized_route_local_export_lifecycle"),
        ("BR-PROD-03-LOCAL-ENCOUNTER-REQUEST", "RCAE", "rcae_ecology_required", "later_local_opportunity_before_native_admission", "fixed_field_blind_branch_local_request", "native_local_opportunity_request_surface"),
        ("BR-PROD-04-COMPOSITE-COORDINATION", "RCAE", "rcae_ecology_required", "atomic_native_plus_policy_load_reset_branch", "eight_component_manifest_coordination", "native_extension_state_registration_and_atomic_composite_restoration"),
        ("BR-PROD-05-CONTROL-CONSTRUCTION", "RCAE", "evidence_only", "prospective_control_setup", "relocation_false_trace_clamps_omissions", "none_evidence_harness_only"),
        ("BR-PROD-06-RESTORATION-VERIFICATION", "RCAE", "evidence_only", "post_load_and_reconstruction_verification", "semantic_digest_replay_and_hashing", "none_evidence_verification_only"),
        ("BR-PROD-07-SUPERVISION-TELEMETRY", "RCAE", "evidence_only", "outside_scientific_causal_chain", "claims_phases_resources_logs_ledger", "none_governance_only"),
    ]
    rows = []
    for item_id, owner, klass, position, operations, debt in definitions:
        if item_id.startswith("BR-PROD-01"):
            expected = {"configurations": 30, "scientific_branches": 90, "integrity_cases": 0}
        elif item_id.startswith("BR-PROD-02"):
            expected = {"configurations": 90, "scientific_branches": 378, "integrity_cases": 0}
        elif item_id.startswith("BR-PROD-03"):
            expected = {"configurations": 90, "scientific_branches": sum(row["terminal_probe"] for row in branches), "integrity_cases": 0}
        elif item_id.startswith("BR-PROD-04"):
            expected = populations
        elif item_id.startswith("BR-PROD-05"):
            expected = {"configurations": 72, "scientific_branches": 252, "integrity_cases": 72}
        elif item_id.startswith("BR-PROD-06"):
            expected = {"configurations": 90, "scientific_branches": 378, "integrity_cases": 72}
        else:
            expected = populations
        rows.append(
            {
                "producer_item_id": item_id,
                "implementation_owner": owner,
                "causal_chain_position": position,
                "producer_class": klass,
                "precedence": ["contract_required", "rcae_ecology_required", "evidence_only"].index(klass),
                "owned_operations": operations,
                "expected_invocation_formula": "registered_population_projection_v1",
                "expected_counts": expected,
                "realized_counts": None,
                "six_unsummed_realized_dimensions": ["causal_invocations", "setup_state_construction_invocations", "evidence_only_observations", "validation_reconstruction_invocations", "process_and_elapsed_time", "RSS_bytes_and_artifact_counts"],
                "restoration_role": "mechanism" if item_id == "BR-PROD-02-POLICY-STATE-RESTORATION" else ("evidence_verification" if item_id == "BR-PROD-06-RESTORATION-VERIFICATION" else "not_restoration"),
                "omission_effect": "classified_by_registered_control_no_automatic_scientific_failure",
                "naturalization_debt": debt,
                "scalar_cost_score_allowed": False,
            }
        )
    return rows


def machine_policy() -> dict[str, Any]:
    return {
        "policy_id": "P2-I3-I06-BR-REGISTRATION-POLICY",
        "artifact_version": ARTIFACT_VERSION,
        "source_anchor": SOURCE_ANCHOR,
        "required_decisions": [f"P2-I3-DEC-{number:03d}" for number in range(20, 47)],
        "bounded_correction": {
            "change_id": "P2-I3-CHG-064",
            "correction_iteration_id": "P2-I3-I06A",
            "reason": "separate_the_450_case_evidence_registry_from_the_456_entry_dependency_ordered_execution_schedule",
            "scientific_redesign": False,
        },
        "entry_gate": {"gate_id": "P2-I3-CAL-GATE", "status": "passed"},
        "exit_gate": {"gate_id": "P2-I3-REG-GATE", "status": "unopened_owner_review_required"},
        "allowed_actions": ["source_binding", "candidate_free_timing", "static_registry_construction", "baseline_constructor_and_restoration_validation", "schema_validation", "reconstruction"],
        "prohibited_actions": ["formation", "export", "encounter_probe", "scientific_control", "integrity_fault_dispatch", "campaign_claim", "P5_authorization", "candidate_interpretation", "C2_work"],
        "runtime": {"required": True, "fallback": False, "source_binding": "${RCAE_PYGRC_ROOT}/src", "graph_mutation": False, "native_priority": True, "explicit_RCAE_producer_when_native_surface_missing": True, "silent_native_substitution": False},
        "claim_ceiling": "exact_inactive_candidate_and_control_authority_only",
    }


def build_registration(
    graph_root: Path,
    timing: Mapping[str, Any],
    implementation_source_anchor: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    environment = timing["environment"]
    baselines, topologies, baseline_checks = baseline_registry()
    configs = configurations(baselines)
    branches = branch_registry(configs)
    faults = integrity_registry(configs)
    cases = canonical_case_registry(branches, faults)
    schedule = governed_execution_schedule(baselines, configs, branches, faults)
    resources = resource_registry(schedule["entries"], timing)
    i04 = load_json(ROOT / I04_POLICY_RELATIVE)
    case_sets = evidence_case_sets(configs, branches, faults)
    controls, requirements = control_projection(i04, case_sets)
    return_admission = load_json(ROOT / I03_RETURN_RELATIVE)
    acceptance = load_json(ROOT / I05_ACCEPTANCE_RELATIVE)
    require(
        acceptance["gate_effect"]["P2-I3-CAL-GATE"]
        == "passed_after_explicit_owner_acceptance_of_I05",
        "CAL-GATE not passed",
    )
    source_authorities = []
    for relative in (
        I03_RETURN_RELATIVE,
        I03_FREEZE_RELATIVE,
        I04_POLICY_RELATIVE,
        I05_ACCEPTANCE_RELATIVE,
        SCRIPT_RELATIVE,
        SCHEMA_RELATIVE,
        EXECUTION_SCHEMA_RELATIVE,
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_br_runtime.py",
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i04_br_analysis.py",
    ):
        source_authorities.append(
            {
                "path": relative,
                "sha256": sha256_file(ROOT / relative),
                "sha256_at_implementation_source_anchor": (
                    committed_file_sha256(implementation_source_anchor, relative)
                    if implementation_source_anchor is not None
                    else None
                ),
            }
        )
    source_anchor_files = [
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/P2-I3-decision-record.md",
        "experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/P2-I3-trail-or-stigmergic-field-checklist.md",
    ]
    registration = with_digest(
        {
            "artifact_id": "P2-I3-I06-BR-EXACT-REGISTRATION",
            "artifact_version": ARTIFACT_VERSION,
            "iteration_id": "P2-I3-I06",
            "branch_id": "P2-I3-BR",
            "status": "review_ready_inactive_registration",
            "schema_contract": {
                "json_schema_role": "closed_root_and_structural_envelope_only",
                "semantic_closure_authority": f"{SCRIPT_RELATIVE}:validate_registration",
                "semantic_validator_required": True,
                "schema_alone_is_complete_experiment_validation": False,
            },
            "authority": {
                "rcae_source_anchor": SOURCE_ANCHOR,
                "implementation_source_anchor": implementation_source_anchor,
                "retention_eligible_source_binding": implementation_source_anchor is not None,
                "required_decisions": [f"P2-I3-DEC-{number:03d}" for number in range(20, 47)],
                "bounded_correction": {
                    "change_id": "P2-I3-CHG-064",
                    "correction_iteration_id": "P2-I3-I06A",
                    "owner_accepted": True,
                    "scientific_redesign": False,
                },
                "source_artifacts": source_authorities,
                "source_anchor_files": [
                    {"path": relative, "sha256_at_source_anchor": committed_file_sha256(SOURCE_ANCHOR, relative)}
                    for relative in source_anchor_files
                ],
                "implementation_governance_files": [
                    {
                        "path": relative,
                        "sha256_at_implementation_source_anchor": (
                            committed_file_sha256(implementation_source_anchor, relative)
                            if implementation_source_anchor is not None
                            else None
                        ),
                    }
                    for relative in (TEST_RELATIVE, REPORT_RELATIVE, *source_anchor_files)
                ],
                "graph_revision": EXPECTED_GRAPH_REVISION,
                "n31_contract_id": "n31_B_R_conserved_redistribution_contract_v2",
                "n31_contract_output_digest": return_admission["provider_contract_options"][0]["contract_output_digest"],
                "calibrated_delta": fraction(DELTA),
            },
            "runtime_identity": deepcopy(dict(environment)),
            "candidate_design": {
                "topology_by_realization": [topologies[key] for key in REALIZATIONS],
                "substrate_baselines": baselines,
                "baseline_constructor_validation": baseline_checks,
                "numeric_parameters": {
                    "C_floor": fraction(Fraction(3, 16)),
                    "q_cap": fraction(Fraction(3, 32)),
                    "q_probe": fraction(Fraction(15, 64)),
                    "formation_repeated": {"count": 3, "amount_each": fraction(Fraction(3, 32)), "system_times": [0, 4, 8]},
                    "formation_one_pulse": {"count": 1, "amount": fraction(Fraction(9, 32)), "system_time": 8},
                    "lifecycle_opportunities": [12, 16, 20, 24],
                    "terminal_encounters": {"j1": 16, "j2_primary": 20, "j3_floor": 28},
                    "construction_targets_not_thresholds": {"m_trace": fraction(Fraction(2, 1)), "m_export": fraction(Fraction(4, 5))},
                    "registered_primary_margins": {
                        "mu_W": fraction(Fraction(-3, 64)),
                        "mu_E": fraction(Fraction(3, 64)),
                        "mu_O": fraction(Fraction(15, 64)),
                    },
                },
                "arms": {"W": "deposition_withdrawn_matched_nonfield_activity_diversion", "O": "formation_present_lifecycle_neutralized", "E": "formation_present_export_enabled"},
                "route_roles": {"focal": "receives_registered_W_O_or_E_treatment", "reference": "receives_matched_nonfield_activity_diversion_and_equal_probe_opportunity", "role_exchange": "separate_control_family_not_a_primary_arm"},
                "state_history_mode": {"primary": "complete_current_native_plus_B_R_composite_state", "audit_formation_history_is_causal_input": False, "mandatory_discriminator": "repeated_E_versus_quantity_matched_one_pulse_E_at_equal_complete_causal_projection"},
                "response": {"primary": "signed_native_admissibility_margin", "mandatory_companion": "native_disposition", "equation": "mu=C_pre(m_e)-q_probe", "dispositions": ["admitted", "field_limited_refusal", "invalid_or_infrastructure_failure"]},
                "metrics": {
                    "normalizer": "N(a,b)=(mu_a-mu_b)/max(abs(mu_a),abs(mu_b),delta)",
                    "m_trace": "(mu_E-mu_W)/max(abs(mu_E),abs(mu_W),delta)",
                    "m_export": "(mu_O-mu_E)/max(abs(mu_O),abs(mu_E),delta)",
                    "analysis_projection": {
                        "m_trace": {"numerator": fraction(Fraction(3, 32)), "denominator": fraction(Fraction(3, 64)), "target": fraction(Fraction(2, 1))},
                        "m_export": {"numerator": fraction(Fraction(3, 16)), "denominator": fraction(Fraction(15, 64)), "target": fraction(Fraction(4, 5))},
                    },
                    "shared_delta": fraction(DELTA),
                    "threshold_semantics": "resolution_and_interpretive_ladder_not_accept_reject_gate",
                },
                "observation_panels": {
                    "native_state": {"disposition": "measured_native", "fields": ["node_coherence", "packet_ledger", "event_queue", "native_disposition"]},
                    "geometric_distance": {"disposition": "derived_annotation_only", "source": "registered_shortest_path_geometric_edge_lengths", "scientific_substitution_allowed": False},
                    "functional_distance": {"disposition": "derived_annotation_only", "source": "registered_inverse_conductance_projection", "scientific_substitution_allowed": False},
                    "causal_temporal": {
                        "native_event_internal_time": {"disposition": "measured_native", "source": "event_time_key_scheduler_order_and_local_event_frontier"},
                        "shortest_path_delay": {"disposition": "derived_annotation_only", "source": "registered_edge_temporal_delay_projection"},
                        "wall_clock_scientific_role": "none",
                    },
                    "experimental_causal_influence": {
                        "disposition": "estimated_from_measured_intervention_arms",
                        "mandatory": True,
                        "direct_native_measurement": False,
                        "annotation_can_satisfy": False,
                    },
                },
                "field_dynamic_panels": {
                    "carrier": "F_e=C(m_e)",
                    "settled_route_mass": "M_e=C(s_e)+C(m_e)",
                    "settled_route_organization": "O_e=C(m_e)-C(s_e)",
                    "checkpoints": ["post_formation", "E1", "E2_primary", "E3_floor", "E4_eligible_zero", "j1", "j2", "j3"],
                    "stored_as_hidden_causal_state": False,
                },
                "relation_ladder": {
                    "R01": "costly_attributable_repeated_formation",
                    "R02": "persistent_route_local_carrier_plus_nonstatic_dynamic",
                    "R03": "dynamic_changes_fixed_local_encounter",
                    "R04": "specificity_under_mandatory_control_package",
                    "R05": "registered_geometry_or_internal_timescale_variation",
                    "classification_style": "graded_interpretive_ladder_not_single_boolean_gate",
                },
                "rungs": ["AE01-L03-R01", "AE01-L03-R02", "AE01-L03-R03", "AE01-L03-R04", "AE01-L03-R05"],
                "interpretation_tags": ["trail_field_candidate", "stigmergic_field_candidate"],
                "seed_sets": {"candidate_deterministic_raw_id_realizations": list(REALIZATIONS), "calibration_seeds": sorted(CALIBRATION_SEEDS), "disjoint": not bool(set(REALIZATIONS) & CALIBRATION_SEEDS), "stochastic_sampling": False},
            },
            "restoration": {"component_contract": component_contracts(), "cell_envelopes": cell_envelopes(configs, baselines), "substrate_baseline_count": len(baselines), "cell_envelope_count": 18, "terminal_probe_is_invasive": True, "clean_fork_required": True, "primary_continuation_horizon": "j2", "floor_continuation_horizon": "j3", "counter_rewriting_or_event_padding": False},
            "matrix": {"family_registry": [{"family_id": row[0], "configuration_count": row[1]} for row in FAMILIES], "configurations": configs, "scientific_branches": branches, "integrity_fault_cases": faults, "configuration_count": len(configs), "scientific_branch_count": len(branches), "integrity_case_count": len(faults), "governed_case_count": len(cases), "appendix_case_count": 0},
            "universal_live_branch_obligations": [
                "runtime_and_source_identity",
                "before_and_after_exact_composite_identity",
                "causal_chain_receipts",
                "formation_cost_and_budget_receipts",
                "global_conservation_receipt",
                "request_and_native_disposition_record",
                "forbidden_read_instrumentation",
                "producer_operation_receipts",
                "reconstruction_selectors",
                "resource_receipt",
                "attempt_and_case_terminal_records",
            ],
            "pairing": pairing_registry(),
            "control_governance": {"evidence_case_set_registry": case_sets, "evidence_case_set_count": len(case_sets), "control_legs": controls, "control_leg_count": len(controls), "requirements": requirements, "requirement_count": len(requirements), "outcomes_assigned": 0, "disposition_copying_allowed": False},
            "resource_governance": resources,
            "attempt_governance": attempt_policy(schedule["entries"], resources),
            "producer_inventory": producer_inventory(configs, branches, faults),
            "schedule": schedule,
            "artifact_governance": {"logical_components": ["native.json", "native-identity-v2.json", "policy.json", "execution.json", "measurement.json", "reset.json", "audit.json", "manifest.json"], "large_individual_review_bytes": 1 * MIB, "large_selected_set_review_bytes": 10 * MIB, "reconstructable_local_only_allowed_with_complete_metadata": True, "exact_byte_dedup_only": True},
            "terminal_record_templates": {"schema": EXECUTION_SCHEMA_RELATIVE, "root_classes": ["checkpoint_manifest", "operational_baseline_terminal", "attempt_terminal", "case_resolution", "control_leg_resolution", "resource_receipt", "cycle_closeout"], "status": "closed_shapes_registered_no_instances_or_observations"},
            "reconstruction": {
                "validate_command": f"env PYTHONPATH=${{RCAE_PYGRC_ROOT}}/src {' '.join(f'{k}={v}' for k,v in THREAD_ENV.items())} .venv/bin/python -B {SCRIPT_RELATIVE} validate --graph-root ${{RCAE_PYGRC_ROOT}}",
                "reconstruct_command": f"env PYTHONPATH=${{RCAE_PYGRC_ROOT}}/src {' '.join(f'{k}={v}' for k,v in THREAD_ENV.items())} .venv/bin/python -B {SCRIPT_RELATIVE} reconstruct --graph-root ${{RCAE_PYGRC_ROOT}} --output outputs/reconstruction/p2-i3-i06-br-registration-validation.reconstructed.json",
                "timing_reexecution_rule": "new_characterization_only; retained monotonic observations are validated not expected_to_recur_byte_exactly",
                "large_artifact_regeneration": "future campaign artifacts reconstruct from exact registry, immutable source/runtime identities, and content manifests",
            },
            "gate_boundary": {"P2-I3-REG-GATE": "unopened_pending_owner_review", "P2-I3-EXEC-FREEZE": "unopened", "candidate_execution_authorized": False, "control_execution_authorized": False, "integrity_fault_execution_authorized": False, "C2_open": False},
            "scientific_outcomes_assigned": False,
            "evidence_effect": "exact_inactive_candidate_control_resource_and_attempt_authority_only",
        }
    )
    policy = machine_policy()
    return policy, registration


def validate_registration(policy: Mapping[str, Any], timing: Mapping[str, Any], registration: Mapping[str, Any], schema: Mapping[str, Any]) -> dict[str, Any]:
    jsonschema.validate(registration, schema)
    execution_schema = load_json(ROOT / EXECUTION_SCHEMA_RELATIVE)
    jsonschema.Draft202012Validator.check_schema(execution_schema)
    require(
        registration["schema_contract"]
        == {
            "json_schema_role": "closed_root_and_structural_envelope_only",
            "semantic_closure_authority": f"{SCRIPT_RELATIVE}:validate_registration",
            "semantic_validator_required": True,
            "schema_alone_is_complete_experiment_validation": False,
        },
        "schema/semantic-validator authority drift",
    )
    lifecycle = execution_schema["$defs"]["control_leg_resolution"]["properties"]
    require(set(lifecycle) == {"artifact_kind", "leg_id", "execution_status", "evidence_resolution", "control_resolution", "terminal_guard_status", "evidence_refs"}, "control lifecycle schema field collapse")
    require(lifecycle["execution_status"]["enum"] == ["not_due", "registered", "executed_valid", "executed_invalid", "unavailable"], "execution lifecycle enum drift")
    require(lifecycle["evidence_resolution"]["enum"] == ["supportive", "equivalent", "counterdirectional", "generic_effect", "mixed", "unresolved", "not_evaluated"], "evidence lifecycle enum drift")
    require(lifecycle["control_resolution"]["enum"] == ["resolved", "unresolved", "invalid", "unavailable"], "control lifecycle enum drift")
    require(lifecycle["terminal_guard_status"]["enum"] == ["not_armed", "armed", "passed", "failed", "not_applicable"], "terminal lifecycle enum drift")
    require(registration["canonical_payload_digest"] == digest_data({key: value for key, value in registration.items() if key != "canonical_payload_digest"}), "registration payload digest drift")
    require(timing["canonical_payload_digest"] == digest_data({key: value for key, value in timing.items() if key != "canonical_payload_digest"}), "timing payload digest drift")
    require(policy == machine_policy(), "machine policy does not reconstruct from accepted decisions")
    expected_decisions = [f"P2-I3-DEC-{number:03d}" for number in range(20, 47)]
    require(registration["authority"]["required_decisions"] == expected_decisions, "registration decision chain drift")
    implementation_source_anchor = registration["authority"]["implementation_source_anchor"]
    retention_eligible = registration["authority"]["retention_eligible_source_binding"]
    require(retention_eligible == (implementation_source_anchor is not None), "implementation source-binding eligibility drift")
    if retention_eligible:
        git(ROOT, "merge-base", "--is-ancestor", implementation_source_anchor, "HEAD")
    for source in registration["authority"]["source_artifacts"]:
        require(sha256_file(ROOT / source["path"]) == source["sha256"], f"registration source drift: {source['path']}")
        if retention_eligible:
            require(
                source["sha256_at_implementation_source_anchor"] == source["sha256"],
                f"registration source was not cleanly committed at implementation anchor: {source['path']}",
            )
        else:
            require(source["sha256_at_implementation_source_anchor"] is None, "preview acquired a committed source digest")
    for source in registration["authority"]["source_anchor_files"]:
        require(committed_file_sha256(SOURCE_ANCHOR, source["path"]) == source["sha256_at_source_anchor"], f"source-anchor file drift: {source['path']}")
    for source in registration["authority"]["implementation_governance_files"]:
        if retention_eligible:
            require(
                committed_file_sha256(implementation_source_anchor, source["path"])
                == source["sha256_at_implementation_source_anchor"],
                f"implementation governance source-anchor drift: {source['path']}",
            )
        else:
            require(source["sha256_at_implementation_source_anchor"] is None, "preview acquired committed governance digest")
    raw_timing = timing["raw_monotonic_elapsed_ns"]
    require(all(len(values) == timing["repetitions_per_operation"] == 7 and all(isinstance(value, int) and value > 0 for value in values) for values in raw_timing.values()), "timing observation closure failure")
    expected_timing_references = {
        "startup_reference_ns": max(raw_timing["startup"]),
        "load_reference_ns": max(raw_timing["inert_load"]),
        "event_reference_ns": (max(raw_timing["fixed_native_event_pair"]) + 1) // 2,
        "bundle_reference_ns": (max(raw_timing["eight_component_bundle_serialization"]) + 7) // 8,
        "validation_reference_ns": max(raw_timing["schema_validation"]),
        "reconstruction_read_reference_ns": (max(raw_timing["eight_component_reconstruction_read"]) + 7) // 8,
    }
    require(timing["references"] == expected_timing_references, "timing reference derivation drift")
    matrix = registration["matrix"]
    require(matrix["configuration_count"] == len(matrix["configurations"]) == 90, "configuration closure failure")
    require(matrix["scientific_branch_count"] == len(matrix["scientific_branches"]) == 378, "scientific branch closure failure")
    require(matrix["integrity_case_count"] == len(matrix["integrity_fault_cases"]) == 72, "integrity closure failure")
    case_ids = [row["case_id"] for row in matrix["integrity_fault_cases"] + matrix["scientific_branches"]]
    require(len(case_ids) == len(set(case_ids)) == 450, "case identity closure failure")
    config_ids = [row["configuration_id"] for row in matrix["configurations"]]
    require(len(config_ids) == len(set(config_ids)) == 90, "configuration identity collision")
    require(sum(row["family_id"] == "core" for row in matrix["configurations"]) == 18, "core count drift")
    observed_families = {
        family: sum(row["family_id"] == family for row in matrix["configurations"])
        for family, _, _, _ in FAMILIES
    }
    require(observed_families == {family: count for family, count, _, _ in FAMILIES}, "configuration family count drift")
    fresh_branches = [row for row in matrix["scientific_branches"] if row["branch_kind"] == "fresh_nondepositor_terminal_probe"]
    core_branches = [row for row in matrix["scientific_branches"] if row["configuration_id"] in {item["configuration_id"] for item in matrix["configurations"] if item["family_id"] == "core"} and row not in fresh_branches]
    special_ids = {item["configuration_id"] for item in matrix["configurations"] if item["family_id"] in {"formation_quantity_history", "causal_projection_matched_false_trace"}}
    special_branches = [row for row in matrix["scientific_branches"] if row["configuration_id"] in special_ids]
    other_branches = [row for row in matrix["scientific_branches"] if row not in core_branches and row not in special_branches and row not in fresh_branches]
    require((len(core_branches), len(special_branches), len(other_branches), len(fresh_branches)) == (126, 60, 180, 12), "scientific branch family expansion drift")
    fault_counts = {name: sum(row["fault_type"] == name for row in matrix["integrity_fault_cases"]) for name in ("invalid_load", "invalid_reset", "invalid_branch", "invalid_continuation")}
    require(set(fault_counts.values()) == {18}, "integrity fault expansion drift")
    require(registration["restoration"]["substrate_baseline_count"] == 6, "baseline count drift")
    require(registration["restoration"]["cell_envelope_count"] == 18, "cell envelope count drift")
    baselines = registration["candidate_design"]["substrate_baselines"]
    require(registration["candidate_design"]["topology_by_realization"] == [topology_record(key) for key in REALIZATIONS], "topology registry does not reconstruct")
    for topology in registration["candidate_design"]["topology_by_realization"]:
        require(topology["structural_edge_directionality"] == "undirected", "native topology directionality drift")
        require(topology["packet_request_directionality"] == "operation_role_whitelist", "packet request whitelist missing")
        require(topology["shared_boundary_packet_requests"] == "prohibited", "shared boundary request prohibition drift")
        for edge in topology["edges"]:
            require(edge["native_structural_semantics"] == "undirected_port_edge", "edge recorded as directed")
            require(as_fraction(edge["conductance"]) == as_fraction(edge["base_conductance"]) == as_fraction(edge["geometric_length"]) == 1, "edge geometry/conductance drift")
            require(as_fraction(edge["flux_uv"]) == as_fraction(edge["flux_coupling"]) == 0, "nonzero initial edge flux state")
            require(edge["unregistered_reverse_request_prohibited"] is True, "reverse-request prohibition missing")
            require(len(edge["allowed_packet_direction_ids"]) <= 1, "ambiguous packet request whitelist")
    design = registration["candidate_design"]
    margins = design["numeric_parameters"]["registered_primary_margins"]
    mu_w, mu_e, mu_o = (as_fraction(margins[key]) for key in ("mu_W", "mu_E", "mu_O"))
    require((mu_w, mu_e, mu_o) == (Fraction(-3, 64), Fraction(3, 64), Fraction(15, 64)), "registered dyadic margin drift")
    metrics = design["metrics"]
    require(metrics["normalizer"] == "N(a,b)=(mu_a-mu_b)/max(abs(mu_a),abs(mu_b),delta)", "DEC-038 normalizer text drift")
    require(metrics["m_trace"] == "(mu_E-mu_W)/max(abs(mu_E),abs(mu_W),delta)", "m_trace formula drift")
    require(metrics["m_export"] == "(mu_O-mu_E)/max(abs(mu_O),abs(mu_E),delta)", "m_export formula drift")
    expected_metric_parts = {
        "m_trace": (mu_e - mu_w, max(abs(mu_e), abs(mu_w), DELTA), normalized_margin(mu_e, mu_w)),
        "m_export": (mu_o - mu_e, max(abs(mu_o), abs(mu_e), DELTA), normalized_margin(mu_o, mu_e)),
    }
    for metric_id, (numerator, denominator, target) in expected_metric_parts.items():
        projection = metrics["analysis_projection"][metric_id]
        require((as_fraction(projection["numerator"]), as_fraction(projection["denominator"]), as_fraction(projection["target"])) == (numerator, denominator, target), f"{metric_id} exact analysis projection drift")
        require(as_fraction(design["numeric_parameters"]["construction_targets_not_thresholds"][metric_id]) == target, f"{metric_id} target disagrees with exact estimator")
    panels = design["observation_panels"]
    require(panels["geometric_distance"] == {"disposition": "derived_annotation_only", "source": "registered_shortest_path_geometric_edge_lengths", "scientific_substitution_allowed": False}, "geometric observation semantics drift")
    require(panels["functional_distance"] == {"disposition": "derived_annotation_only", "source": "registered_inverse_conductance_projection", "scientific_substitution_allowed": False}, "functional observation semantics drift")
    require(panels["causal_temporal"]["native_event_internal_time"]["disposition"] == "measured_native", "native internal time must be measured")
    require(panels["causal_temporal"]["shortest_path_delay"]["disposition"] == "derived_annotation_only", "shortest-path delay must remain annotation")
    require(panels["experimental_causal_influence"] == {"disposition": "estimated_from_measured_intervention_arms", "mandatory": True, "direct_native_measurement": False, "annotation_can_satisfy": False}, "experimental causal-influence semantics drift")
    require(matrix["configurations"] == configurations(baselines), "configuration registry does not reconstruct")
    require(matrix["scientific_branches"] == branch_registry(matrix["configurations"]), "scientific branch registry does not reconstruct")
    require(matrix["integrity_fault_cases"] == integrity_registry(matrix["configurations"]), "integrity registry does not reconstruct")
    require(registration["pairing"] == pairing_registry(), "full DEC-038 pairing registry drift")
    require(registration["restoration"]["component_contract"] == component_contracts(), "component contract drift")
    require(registration["restoration"]["cell_envelopes"] == cell_envelopes(matrix["configurations"], baselines), "cell envelope registry does not reconstruct")
    require(registration["control_governance"]["control_leg_count"] == 42, "control-leg count drift")
    require(registration["control_governance"]["requirement_count"] == 14, "requirement count drift")
    expected_case_sets = evidence_case_sets(matrix["configurations"], matrix["scientific_branches"], matrix["integrity_fault_cases"])
    require(registration["control_governance"]["evidence_case_set_count"] == len(expected_case_sets), "evidence case-set count drift")
    require(registration["control_governance"]["evidence_case_set_registry"] == expected_case_sets, "evidence case-set registry does not reconstruct")
    case_set_by_id = {row["case_set_id"]: row for row in expected_case_sets}
    require(len(case_set_by_id) == len(expected_case_sets), "case-set identity collision")
    observed_case_set_counts = {
        set_id.removeprefix("P2-I3-BR-CASESET-"): row["selected_case_count"]
        for set_id, row in case_set_by_id.items()
    }
    require(observed_case_set_counts == EXPECTED_CASE_SET_COUNTS, "evidence case-set population drift")
    require(case_set_by_id["P2-I3-BR-CASESET-RAW-ID-PERMUTATION"]["configuration_family_ids"] == ["core"], "raw-ID permutation selected role-exchange or another family")
    require(case_set_by_id["P2-I3-BR-CASESET-ROLE-EXCHANGE"]["configuration_family_ids"] == ["focal_reference_role_exchange"], "role exchange selected raw-ID permutation or another family")
    require(case_set_by_id["P2-I3-BR-CASESET-FORMATION-HISTORY"]["configuration_family_ids"] == ["formation_quantity_history"], "DISC-01 unintended family")
    require(case_set_by_id["P2-I3-BR-CASESET-EXPORT-MASS-ORGANIZATION"]["configuration_family_ids"] == ["export_mass_organization"], "DISC-02 unintended family")
    require(case_set_by_id["P2-I3-BR-CASESET-STATE-HISTORY-DISCRIMINATOR"]["configuration_family_ids"] == ["causal_projection_matched_false_trace", "core", "formation_quantity_history"], "DISC-03 unintended family")
    require(case_set_by_id["P2-I3-BR-CASESET-TAU-VARIATION"]["configuration_family_ids"] == ["core"], "DISC-04 unintended family")
    require(case_set_by_id["P2-I3-BR-CASESET-FRESH-NONDEPOSITOR"]["configuration_family_ids"] == ["core"], "DISC-05 unintended family")
    pairing_fields = set(registration["pairing"]["fields"])
    for case_set in expected_case_sets:
        ordinals = case_set["case_ordinals"]
        require(case_set["selected_case_count"] == len(ordinals) == len(set(ordinals)) > 0, "empty, duplicate, or miscounted evidence case set")
        require(all(1 <= ordinal <= len(case_ids) for ordinal in ordinals), "case set selects an unknown case ordinal")
        selected_case_ids = sorted(case_ids[ordinal - 1] for ordinal in ordinals)
        require(case_set["exact_membership_digest"] == digest_data(selected_case_ids), "case-set membership digest drift")
        config_ordinals = case_set["configuration_ordinals"]
        require(len(config_ordinals) == len(set(config_ordinals)) and all(1 <= ordinal <= len(config_ids) for ordinal in config_ordinals), "case-set configuration ordinal closure failure")
        selected_config_ids = sorted(config_ids[ordinal - 1] for ordinal in config_ordinals)
        require(case_set["exact_configuration_membership_digest"] == digest_data(selected_config_ids), "case-set configuration membership digest drift")
        require(set(case_set["intervention_field_ids"]).isdisjoint(case_set["held_fixed_field_ids"]), "case-set intervention/held-fixed overlap")
        if case_set["case_set_id"] != "P2-I3-BR-CASESET-INTEGRITY-FAULTS":
            require(set(case_set["intervention_field_ids"]).issubset(pairing_fields), "undeclared intervention outside DEC-038 pairing key")
            require(set(case_set["intervention_field_ids"]).union(case_set["held_fixed_field_ids"]) == pairing_fields, "intervention and held-fixed fields do not close pairing key")
    expected_controls, expected_requirements = control_projection(load_json(ROOT / I04_POLICY_RELATIVE), expected_case_sets)
    require(registration["control_governance"]["control_legs"] == expected_controls, "control-leg projection drift")
    require(registration["control_governance"]["requirements"] == expected_requirements, "requirement projection drift")
    for row in expected_controls:
        selected = {ordinal for set_id in row["selected_case_set_ids"] for ordinal in case_set_by_id[set_id]["case_ordinals"]}
        require(row["selected_case_count"] == len(selected), f"control selector count drift: {row['leg_id']}")
        require(row["minimum_valid_artifact_count"] <= max(1, len(selected)), f"control minimum cannot be achieved: {row['leg_id']}")
        require(row["scientific_or_guard_class"] != "scientific" or row["applicability"] == "not_applicable" or selected, f"applicable scientific control lacks cases: {row['leg_id']}")
    for row in expected_requirements:
        selected = {ordinal for set_id in row["selected_case_set_ids"] for ordinal in case_set_by_id[set_id]["case_ordinals"]}
        require(row["selected_case_count"] == len(selected) > 0, f"requirement selector closure drift: {row['requirement_id']}")
        require(row["minimum_valid_artifact_count"] <= len(selected), f"requirement minimum cannot be achieved: {row['requirement_id']}")
    require(all(row["observed_resolution"] is None for row in registration["control_governance"]["control_legs"]), "control outcome leaked into registration")
    require(all(row["observed_resolution"] is None for row in registration["control_governance"]["requirements"]), "requirement outcome leaked into registration")
    expected_schedule = governed_execution_schedule(
        baselines,
        matrix["configurations"],
        matrix["scientific_branches"],
        matrix["integrity_fault_cases"],
    )
    require(registration["schedule"] == expected_schedule, "governed execution schedule does not reconstruct")
    classes = registration["resource_governance"]["class_counts"]
    require(classes == {"probe_only": 288, "standard_trajectory": 48, "complex_construction_or_comparison": 48, "integrity_fault": 72}, "execution-class counts drift")
    assignments = registration["resource_governance"]["assignments"]
    schedule_entry_ids = registration["schedule"]["order"]
    require(len(assignments) == 456 and {row["entry_id"] for row in assignments} == set(schedule_entry_ids), "resource assignment closure failure")
    require({row["case_id"] for row in assignments if row["case_id"] is not None} == set(case_ids), "resource case assignment closure failure")
    require(registration["resource_governance"]["assignment_digest"] == digest_data(assignments), "assignment digest drift")
    expected_resources = resource_registry(expected_schedule["entries"], timing)
    require(registration["resource_governance"] == expected_resources, "resource registry does not reconstruct")
    require(registration["resource_governance"]["campaign"]["primary_child_seconds"] == 4920, "I06A primary child allowance drift")
    require(registration["resource_governance"]["campaign"]["exact_campaign_ceiling_seconds"] == 7440, "I06A exact campaign ceiling drift")
    require(registration["resource_governance"]["campaign"]["exact_campaign_ceiling_seconds"] <= 108000, "campaign ceiling exceeded")
    require(registration["resource_governance"]["bytes"]["governed_physical_projection_bytes"] <= 8 * GIB, "physical bytes exceeded")
    require(registration["attempt_governance"]["registered_case_count"] == 450, "attempt case count drift")
    require(registration["attempt_governance"]["registered_operational_baseline_entry_count"] == 6, "attempt baseline entry count drift")
    require(registration["attempt_governance"]["governed_entry_count"] == 456, "attempt governed entry count drift")
    require(registration["attempt_governance"]["primary_attempt_slots"] == 456, "primary attempt-slot count drift")
    require(len(registration["attempt_governance"]["class_retry_tokens"]) == 4, "retry token count drift")
    require(registration["attempt_governance"]["maximum_governed_child_starts"] == 460, "child start ceiling drift")
    require(registration["attempt_governance"] == attempt_policy(expected_schedule["entries"], expected_resources), "attempt policy does not reconstruct")
    require(registration["producer_inventory"] == producer_inventory(matrix["configurations"], matrix["scientific_branches"], matrix["integrity_fault_cases"]), "producer inventory does not reconstruct")
    require(len(schedule_entry_ids) == len(set(schedule_entry_ids)) == 456, "schedule closure failure")
    require(registration["schedule"]["canonical_case_registry_order"] == case_ids, "canonical case-registry order drift")
    require(registration["schedule"]["canonical_case_registry_digest"] == digest_data(case_ids), "canonical case-registry digest drift")
    require(set(schedule_entry_ids[6:]) == set(case_ids), "schedule case membership failure")
    baseline_entries = registration["schedule"]["operational_baseline_entries"]
    require(schedule_entry_ids[:6] == [row["entry_id"] for row in baseline_entries], "operational baselines are not first")
    require(schedule_entry_ids[6:78] == [row["case_id"] for row in matrix["integrity_fault_cases"]], "integrity block does not follow operational baselines")
    require(all(row["scientific_evidence_effect"] == "none" for row in baseline_entries), "operational baseline acquired scientific effect")
    require(all(set(row["scientific_operation_counts"].values()) == {0} for row in baseline_entries), "operational baseline performs scientific operation")
    observed_subtree_entries: set[str] = set()
    for subtree in registration["schedule"]["baseline_failure_subtrees"]:
        dependent_ids = set(subtree["dependent_entry_ids"])
        require(len(dependent_ids) == 75, "baseline dependency subtree population drift")
        require(not observed_subtree_entries.intersection(dependent_ids), "baseline dependency subtrees overlap")
        observed_subtree_entries.update(dependent_ids)
    require(observed_subtree_entries == set(case_ids), "baseline dependency subtrees do not cover canonical cases exactly")
    ordinal_by_entry = {entry_id: index for index, entry_id in enumerate(schedule_entry_ids, start=1)}
    execution_entry_by_id = {row["entry_id"]: row for row in registration["schedule"]["entries"]}
    for edge in registration["schedule"]["dependency_dag"]:
        require(all(ordinal_by_entry[parent] < ordinal_by_entry[edge["entry_id"]] for parent in edge["parent_entry_ids"]), f"non-topological schedule edge: {edge['entry_id']}")
    baseline_ids = {row["substrate_base_id"] for row in registration["candidate_design"]["substrate_baselines"]}
    core_config_ids = {row["configuration_id"] for row in matrix["configurations"] if row["family_id"] == "core"}
    config_by_id = {row["configuration_id"]: row for row in matrix["configurations"]}
    case_by_id = {row["case_id"]: row for row in matrix["scientific_branches"] + matrix["integrity_fault_cases"]}
    for case in matrix["scientific_branches"] + matrix["integrity_fault_cases"]:
        for parent in case["parent_ids"]:
            if parent.startswith("baseline:"):
                require(parent.removeprefix("baseline:") in baseline_ids, "unknown baseline dependency")
            elif parent.startswith("cell-envelope:"):
                require(parent.removeprefix("cell-envelope:") in core_config_ids, "unknown cell-envelope dependency")
            elif parent.startswith("checkpoint:"):
                require(parent.split(":", 2)[1] in case_ids, "unknown checkpoint producer")
            else:
                require(parent in case_ids, "unknown case dependency")
        if case.get("branch_kind") in {"terminal_probe", "fresh_nondepositor_terminal_probe"}:
            trajectory_parents = [parent for parent in case["parent_ids"] if parent in case_by_id]
            require(len(trajectory_parents) == 1, "probe does not bind exactly one trajectory parent")
            trajectory = case_by_id[trajectory_parents[0]]
            require(trajectory["branch_kind"] == "unprobed_trajectory", "probe parent is not a trajectory")
            require(trajectory["substrate_base_id"] == case["substrate_base_id"], "probe crossed substrate base")
            require(trajectory["configuration_id"] == case["configuration_id"], "probe crossed configuration")
            require(ordinal_by_entry[trajectory["case_id"]] < ordinal_by_entry[case["case_id"]], "probe precedes trajectory parent")
            checkpoints = [parent for parent in case["parent_ids"] if parent.startswith("checkpoint:")]
            require(len(checkpoints) == 1 and checkpoints[0].split(":", 2)[1] == trajectory["case_id"], "probe checkpoint producer drift")
            require(checkpoints[0] in execution_entry_by_id[trajectory["case_id"]]["produced_checkpoint_refs"], "required checkpoint is not produced by trajectory parent")
            require(execution_entry_by_id[case["case_id"]]["parent_trajectory_advanced_in_child"] is False, "probe implicitly advances or reconstructs its parent trajectory")
            if case["branch_kind"] == "fresh_nondepositor_terminal_probe":
                config = config_by_id[case["configuration_id"]]
                require(config["family_id"] == "core" and config["arm"] == "E" and case["checkpoint"] == "j2", "fresh nondepositor did not bind clean core-E j2")
    require(all(row["case_kind"] == "quarantined_integrity_fault" for row in matrix["integrity_fault_cases"]), "integrity quarantine drift")
    require(registration["matrix"]["appendix_case_count"] == 0, "appendix entered core matrix")
    require(registration["scientific_outcomes_assigned"] is False, "scientific outcome assigned")
    require(registration["gate_boundary"]["candidate_execution_authorized"] is False, "candidate execution opened")
    require(registration["candidate_design"]["seed_sets"]["disjoint"] is True, "seed collision")
    require(policy["exit_gate"]["status"] == "unopened_owner_review_required", "REG-GATE silently passed")
    assert_portable(policy)
    assert_portable(timing)
    assert_portable(registration)
    checks = [
        ("I06-01", "source-bound runtime and environment", 1),
        ("I06-02", "N31 B-R and CAL-GATE authorities", 1),
        ("I06-03", "undirected two-route topology, request whitelist, and dyadic values", 6),
        ("I06-04", "six native baseline construction/load/reset identities", 6),
        ("I06-05", "18 cell envelope and eight-component contract", 18),
        ("I06-06", "90 configuration closure", 90),
        ("I06-07", "378 scientific branch closure", 378),
        ("I06-08", "72 integrity-case quarantine closure", 72),
        ("I06-09", "DEC-038 estimator formulas and exact 2 and 4/5 projections", 2),
        ("I06-10", "separated Q-010 observation surfaces", 5),
        ("I06-11", "full pairing key and exact/delta split", len(registration["pairing"]["fields"])),
        ("I06-12", "digest-bound exact evidence case-set registry", len(registration["control_governance"]["evidence_case_set_registry"])),
        ("I06-13", "42 independent exact control-leg projections", 42),
        ("I06-14", "14 exact supplemental requirement bindings", 14),
        ("I06-15", "candidate-free timing characterization", timing["repetitions_per_operation"]),
        ("I06A-16", "456 immutable operational-entry class and numeric resource assignments", 456),
        ("I06-17", "campaign time and byte envelope", 1),
        ("I06A-18", "456 primary slots and four retry tokens", 460),
        ("I06A-19", "six baseline entries plus closed topological schedule and dependency propagation", 456),
        ("I06A-20", "unchanged 450-case canonical evidence registry", 450),
        ("I06-21", "static producer inventory with unsummed dimensions", len(registration["producer_inventory"])),
        ("I06-22", "structural schema role and mandatory semantic validator", 1),
        ("I06-23", "four-field I04 control lifecycle schema", 4),
        ("I06-24", "appendix exclusion", 0),
        ("I06-25", "portable reconstruction and no absolute path", 0),
        ("I06-26", "candidate/control/claim execution stop", 0),
    ]
    return with_digest(
        {
            "artifact_id": "P2-I3-I06-BR-REGISTRATION-VALIDATION",
            "artifact_version": ARTIFACT_VERSION,
            "iteration_id": "P2-I3-I06",
            "branch_id": "P2-I3-BR",
            "status": "review_ready_all_registration_checks_passed",
            "policy_sha256": sha256_file(ROOT / POLICY_RELATIVE),
            "schema_sha256": sha256_file(ROOT / SCHEMA_RELATIVE),
            "execution_records_schema_sha256": sha256_file(ROOT / EXECUTION_SCHEMA_RELATIVE),
            "timing_sha256": sha256_file(ROOT / TIMING_RELATIVE),
            "registration_sha256": sha256_file(ROOT / REGISTRATION_RELATIVE),
            "checks": [{"check_id": item[0], "name": item[1], "status": "passed", "bound_count": item[2]} for item in checks],
            "passed_checks": len(checks),
            "total_checks": len(checks),
            "closed_counts": {"substrate_bases": 6, "cell_envelopes": 18, "configurations": 90, "scientific_branches": 378, "integrity_cases": 72, "governed_cases": 450, "operational_baseline_entries": 6, "governed_execution_entries": 456, "evidence_case_sets": len(expected_case_sets), "control_legs": 42, "requirements": 14, "retry_tokens": 4, "maximum_child_starts": 460},
            "construction_activity": registration["candidate_design"]["baseline_constructor_validation"],
            "candidate_free_timing_only": True,
            "scientific_operations": {"formation": 0, "export": 0, "encounter_probe": 0, "scientific_control": 0, "integrity_fault_dispatch": 0},
            "gate_effect": {"P2-I3-REG-GATE": "unopened_pending_owner_review", "P2-I3-EXEC-FREEZE": "unopened", "candidate_execution_authorized": False, "owner_review_required": True},
            "evidence_effect": "registration_integrity_only_no_scientific_or_ecology_result",
        }
    )


def write(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pretty_bytes(value))


def command_build(graph_root: Path, implementation_source_anchor: str) -> dict[str, Any]:
    environment = require_environment(graph_root)
    require(git(ROOT, "rev-parse", "HEAD") == implementation_source_anchor, "I06A build HEAD differs from supplied source anchor")
    timing = load_json(ROOT / TIMING_RELATIVE)
    require(timing["artifact_version"] == "1.0.1", "accepted I06 timing authority version drift")
    require(timing["environment"] == environment, "accepted I06 timing environment drift")
    require(
        all(value is False for value in timing["candidate_blindness"].values()),
        "accepted I06 timing authority is not candidate-free",
    )
    policy, registration = build_registration(
        graph_root,
        timing,
        implementation_source_anchor=implementation_source_anchor,
    )
    for source in registration["authority"]["source_artifacts"]:
        require(
            source["sha256"] == source["sha256_at_implementation_source_anchor"],
            f"I06A consumed source is not cleanly committed: {source['path']}",
        )
    write(ROOT / POLICY_RELATIVE, policy)
    write(ROOT / REGISTRATION_RELATIVE, registration)
    schema = load_json(ROOT / SCHEMA_RELATIVE)
    validation = validate_registration(policy, timing, registration, schema)
    write(ROOT / VALIDATION_RELATIVE, validation)
    return validation


def command_validate(graph_root: Path) -> dict[str, Any]:
    require_environment(graph_root)
    policy = load_json(ROOT / POLICY_RELATIVE)
    timing = load_json(ROOT / TIMING_RELATIVE)
    registration = load_json(ROOT / REGISTRATION_RELATIVE)
    require(registration["authority"]["retention_eligible_source_binding"] is True, "retained I06A lacks a clean implementation source anchor")
    schema = load_json(ROOT / SCHEMA_RELATIVE)
    rebuilt_baselines, _, rebuilt_activity = baseline_registry()
    require(
        rebuilt_baselines == registration["candidate_design"]["substrate_baselines"],
        "native baseline registry does not reconstruct at retained source",
    )
    require(
        rebuilt_activity
        == registration["candidate_design"]["baseline_constructor_validation"],
        "native baseline construction accounting drift",
    )
    validation = validate_registration(policy, timing, registration, schema)
    retained = load_json(ROOT / VALIDATION_RELATIVE)
    require(validation == retained, "retained validation does not reconstruct byte-semantically")
    return validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "validate"):
        child = subparsers.add_parser(name)
        child.add_argument("--graph-root", required=True)
        if name == "build":
            child.add_argument("--implementation-source-anchor", required=True)
    reconstruct = subparsers.add_parser("reconstruct")
    reconstruct.add_argument("--graph-root", required=True)
    reconstruct.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    graph_root = Path(args.graph_root).resolve()
    if args.command == "build":
        result = command_build(graph_root, args.implementation_source_anchor)
    else:
        result = command_validate(graph_root)
        if args.command == "reconstruct":
            output = Path(args.output)
            require(output.resolve().is_relative_to(ROOT.resolve()), "reconstruction output must remain under RCAE root")
            require(output.resolve() != (ROOT / VALIDATION_RELATIVE).resolve(), "reconstruction cannot overwrite retained validation")
            write(output, result)
    print(json.dumps({"status": result["status"], "passed_checks": result["passed_checks"], "total_checks": result["total_checks"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
