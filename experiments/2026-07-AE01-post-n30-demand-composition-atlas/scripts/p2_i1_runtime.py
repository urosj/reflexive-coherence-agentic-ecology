"""Fail-closed PyGRC boundary for the P2-I1 runtime scaffold.

PyGRC is imported only inside explicit runtime functions.  This module builds
and validates the frozen fixture but deliberately does not execute candidate
cells before the registration and execution gates authorize them.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
import importlib
import importlib.metadata
from types import ModuleType
from typing import Any

from ae01_tooling import ContractError, digest_canonical_data


REQUIRED_MODEL_SYMBOLS = (
    "GRC9V3NodeState",
    "GRC9V3State",
    "LGRC9V3",
    "LGRC9V3RouteAspect",
    "LGRC9V3RouteAspectChannel",
    "LGRC9V3RouteAspectHop",
    "PortEdge",
    "slot_to_port_id",
    "validate_lgrc9v3_route_aspect",
)
REQUIRED_CORE_SYMBOLS = ("PortGraphBackend",)
OPERATION_CAPABILITY_PATHS = {
    "p2_i1_runtime_preflight": (
        "models.LGRC9V3.from_state",
        "models.LGRC9V3.get_state",
        "models.LGRC9V3.snapshot",
    ),
    "fixture_construction": ("models.LGRC9V3.from_state",),
    "route_aspect_validation": ("models.validate_lgrc9v3_route_aspect",),
    "snapshot_round_trip": (
        "models.LGRC9V3.snapshot",
        "models.LGRC9V3.load",
    ),
    "packet_queue_step": ("models.LGRC9V3.step",),
    "feedback_surface_emission": (
        "models.LGRC9V3.emit_feedback_eligibility_surface_row",
    ),
    "feedback_conditioned_packet_production": (
        "models.LGRC9V3.set_feedback_coupled_pulse_producer",
        "models.LGRC9V3.step",
    ),
}


def _import_module(name: str) -> ModuleType:
    return importlib.import_module(name)


def _read_version(name: str) -> str:
    return importlib.metadata.version(name)


def validate_runtime_operation_capabilities(
    runtime_modules: Mapping[str, ModuleType], operation_ids: list[str]
) -> dict[str, list[str]]:
    """Resolve every abstract operation class to concrete callable surfaces."""

    if operation_ids != list(OPERATION_CAPABILITY_PATHS):
        raise ContractError("P2-I1 operation-class order or set drifted")
    resolved: dict[str, list[str]] = {}
    for operation_id in operation_ids:
        paths = OPERATION_CAPABILITY_PATHS[operation_id]
        for path in paths:
            parts = path.split(".")
            value: Any = runtime_modules.get(parts[0])
            for part in parts[1:]:
                value = getattr(value, part, None)
            if not callable(value):
                raise ContractError(
                    f"P2-I1 operation capability is unavailable: {path}"
                )
        resolved[operation_id] = list(paths)
    return resolved


def bind_runtime(
    runtime_policy: Mapping[str, Any],
    realization_profile: Mapping[str, Any],
    *,
    importer: Callable[[str], ModuleType] = _import_module,
    version_reader: Callable[[str], str] = _read_version,
) -> dict[str, ModuleType]:
    """Bind the exact declared runtime or raise; never select a fallback."""

    if runtime_policy.get("execution_class") != "pygrc_runtime_with_rcae_producer":
        raise ContractError("P2-I1 execution class drifted")
    if runtime_policy.get("fallback_execution_class") is not None:
        raise ContractError("P2-I1 runtime policy must not declare a fallback")
    if runtime_policy.get("candidate_execution_authorized") is not False:
        raise ContractError("shared runtime policy cannot grant blanket candidate authority")
    if not (
        runtime_policy.get("candidate_execution_authorization_mode")
        == "explicit_cycle_exec_freeze_only"
        and runtime_policy.get("execution_freeze_required") is True
        and runtime_policy.get("execution_freeze_gate") == "P2-I1-EXEC-FREEZE"
        and runtime_policy.get("execution_close_gate") == "P2-I1-EXEC-GATE"
    ):
        raise ContractError("P2-I1 cycle authorization boundary drifted")
    profile = realization_profile.get("record", realization_profile)
    if not isinstance(profile, Mapping):
        raise ContractError("realization profile must be an object")
    if not (
        profile.get("availability") is True
        and profile.get("enabled") is True
        and profile.get("supported") is True
        and profile.get("validated") is True
    ):
        raise ContractError(
            "local realization must explicitly be available, enabled, supported, and validated"
        )
    expected_identity = runtime_policy["required_pygrc_identity"]
    if profile.get("required_pygrc_identity") != expected_identity:
        raise ContractError("local realization PyGRC identity differs from runtime policy")
    allowed_operations = profile.get("allowed_scheduling_operations", [])
    if runtime_policy["preflight_operation_id"] not in allowed_operations:
        raise ContractError("local realization does not authorize P2-I1 preflight")
    try:
        root = importer("pygrc")
        core = importer("pygrc.core")
        models = importer("pygrc.models")
        version = version_reader("pygrc")
    except (ImportError, ModuleNotFoundError, importlib.metadata.PackageNotFoundError) as exc:
        raise ContractError("PyGRC runtime is unavailable; no fallback is permitted") from exc
    if f"pygrc=={version}" != expected_identity:
        raise ContractError(
            f"PyGRC identity mismatch: expected {expected_identity}, observed pygrc=={version}"
        )
    advertised = getattr(root, "PUBLIC_API_SURFACES", {})
    for surface in runtime_policy["required_public_capabilities"]:
        if surface not in advertised:
            raise ContractError(f"PyGRC public capability missing: {surface}")
    for symbol in REQUIRED_CORE_SYMBOLS:
        if not hasattr(core, symbol):
            raise ContractError(f"PyGRC core symbol missing: {symbol}")
    for symbol in REQUIRED_MODEL_SYMBOLS:
        if not hasattr(models, symbol):
            raise ContractError(f"PyGRC model symbol missing: {symbol}")
    modules = {"pygrc": root, "core": core, "models": models}
    validate_runtime_operation_capabilities(
        modules,
        [runtime_policy["preflight_operation_id"], *runtime_policy["required_operations"]],
    )
    return modules


def resolve_node_coherences(
    fixture: Mapping[str, Any], seed: int, cell_id: str, cells: Mapping[str, Any]
) -> dict[str, float]:
    seed_rows = {int(row["seed"]): row for row in fixture["seeds"]}
    if seed not in seed_rows:
        raise ContractError(f"unregistered P2-I1 seed: {seed}")
    offset = float(seed_rows[seed]["offset"])
    values = {"P": 1.0 + offset, "W": 1.0 - offset, "A": 0.5, "B": 0.5}
    cell = next((row for row in cells["cells"] if row["cell_id"] == cell_id), None)
    if cell is None:
        raise ContractError(f"unregistered P2-I1 cell: {cell_id}")
    intervention = cell["intervention"]
    if intervention["kind"] == "absolute_environmental_support_scale":
        support_offset = float(intervention["support_offset"])
        values = {
            "P": values["P"],
            "W": values["W"] + 2.0 * support_offset,
            "A": 0.5 + support_offset,
            "B": 0.5 + support_offset,
        }
    return values


def resolve_reader_packet_amount(
    fixture: Mapping[str, Any], cells: Mapping[str, Any], cell_id: str
) -> float:
    """Resolve the registered reader load without changing node coherence."""

    cell = next((row for row in cells["cells"] if row["cell_id"] == cell_id), None)
    if cell is None:
        raise ContractError(f"unregistered P2-I1 cell: {cell_id}")
    intervention = cell["intervention"]
    if intervention["kind"] == "reader_packet_amount":
        return float(intervention["reader_packet_amount"])
    return float(fixture["packets"]["reader_amount"])


def _build_route_aspect(fixture: Mapping[str, Any], models: ModuleType) -> Any:
    route = fixture["route_aspect"]
    edges = {int(edge["edge_id"]): edge for edge in fixture["edges"]}
    channels = []
    for channel in route["channels"]:
        edge = edges[int(channel["edge_id"])]
        hop = models.LGRC9V3RouteAspectHop(
            source_node_id=int(edge["source_node_id"]),
            target_node_id=int(edge["target_node_id"]),
            edge_id=int(edge["edge_id"]),
        )
        channels.append(
            models.LGRC9V3RouteAspectChannel(
                channel_id=channel["channel_id"],
                source_pole_id=channel["source_pole_id"],
                target_pole_id=channel["target_pole_id"],
                expected_next_channel_id=channel["expected_next_channel_id"],
                route_hops=(hop,),
            )
        )
    return models.LGRC9V3RouteAspect(
        route_aspect_id=route["route_aspect_id"],
        direction=route["direction"],
        closed_loop=route["closed_loop"],
        pole_regions={key: tuple(value) for key, value in route["pole_regions"].items()},
        channels=tuple(channels),
        channel_sequence=tuple(route["channel_sequence"]),
    )


def build_fixture(
    fixture: Mapping[str, Any],
    cells: Mapping[str, Any],
    runtime_modules: Mapping[str, ModuleType],
    *,
    seed: int,
    cell_id: str,
) -> tuple[Any, Any]:
    """Construct one frozen initial fixture using only public PyGRC facades."""

    core = runtime_modules["core"]
    models = runtime_modules["models"]
    graph = core.PortGraphBackend()
    role_by_id = {int(row["node_id"]): row["role"] for row in fixture["nodes"]}
    for expected_id in sorted(role_by_id):
        observed = graph.add_node({"role": role_by_id[expected_id]})
        if observed != expected_id:
            raise ContractError("PyGRC node allocation differs from frozen fixture IDs")
    port_edges: dict[int, Any] = {}
    for edge in fixture["edges"]:
        observed = graph.connect_ports(
            int(edge["source_node_id"]),
            int(edge["source_port"]),
            int(edge["target_node_id"]),
            int(edge["target_port"]),
            {"role": edge["role"]},
        )
        edge_id = int(edge["edge_id"])
        if observed != edge_id:
            raise ContractError("PyGRC edge allocation differs from frozen fixture IDs")
        edge_policy = fixture["edge_policy"]
        port_edges[edge_id] = models.PortEdge(
            int(edge["source_node_id"]),
            models.slot_to_port_id(int(edge["source_port"])),
            int(edge["target_node_id"]),
            models.slot_to_port_id(int(edge["target_port"])),
            conductance=float(edge_policy["conductance"]),
            flux_uv=float(edge_policy["flux_coupling"]),
        )
    coherence_by_role = resolve_node_coherences(fixture, seed, cell_id, cells)
    node_states = {
        node_id: models.GRC9V3NodeState(coherence=coherence_by_role[role])
        for node_id, role in role_by_id.items()
    }
    edge_ids = sorted(port_edges)
    edge_policy = fixture["edge_policy"]
    state = models.GRC9V3State(
        topology=graph,
        nodes=node_states,
        port_edges=port_edges,
        base_conductance={edge_id: float(edge_policy["conductance"]) for edge_id in edge_ids},
        geometric_length={edge_id: float(edge_policy["geometric_length"]) for edge_id in edge_ids},
        temporal_delay={edge_id: float(edge_policy["temporal_delay"]) for edge_id in edge_ids},
        flux_coupling={edge_id: float(edge_policy["flux_coupling"]) for edge_id in edge_ids},
    )
    params = {
        "dt": float(fixture["runtime_parameters"]["dt"]),
        "causal_modes": {
            "causal_layer_mode": models.CAUSAL_LAYER_MODE_PACKETIZED_FIXED_TOPOLOGY,
            "lgrc_runtime_level": models.LGRC_RUNTIME_LEVEL_LGRC2,
            "lapse_policy": models.LAPSE_POLICY_UNIT,
            "edge_delay_policy": models.EDGE_DELAY_POLICY_CONSTANT_DELAY,
            "event_time_policy": "explicit_event_time_key",
            "proper_time_accumulation_policy": "local_event_frontier",
            "causal_pulse_substrate_surface_enabled": True,
            "causal_pulse_substrate_surface_policy": (
                models.LGRC9V3_CAUSAL_PULSE_SUBSTRATE_SURFACE_POLICY_EMIT_ROWS
            ),
            "causal_pulse_substrate_surface_validated": True,
        },
    }
    model = models.LGRC9V3.from_state(state, params)
    route_aspect = _build_route_aspect(fixture, models)
    models.validate_lgrc9v3_route_aspect(route_aspect, state=state)
    return model, route_aspect


def preflight_fixture(
    fixture: Mapping[str, Any],
    cells: Mapping[str, Any],
    runtime_policy: Mapping[str, Any],
    realization_profile: Mapping[str, Any],
    *,
    seed: int = 211,
    cell_id: str = "candidate-conditioning",
    importer: Callable[[str], ModuleType] = _import_module,
    version_reader: Callable[[str], str] = _read_version,
) -> dict[str, Any]:
    """Build and snapshot the fixture without executing a scientific cell."""

    modules = bind_runtime(
        runtime_policy,
        realization_profile,
        importer=importer,
        version_reader=version_reader,
    )
    model, route_aspect = build_fixture(
        fixture, cells, modules, seed=seed, cell_id=cell_id
    )
    snapshot = model.snapshot()
    queue = model.get_state().packet_ledger.event_queue_records
    surfaces = model.get_state().causal_pulse_substrate_surface_log
    if queue or surfaces:
        raise ContractError("preflight fixture must begin with empty queue and surface log")
    topology_projection = {
        "fixture_id": fixture["fixture_id"],
        "nodes": fixture["nodes"],
        "edges": fixture["edges"],
        "edge_policy": fixture["edge_policy"],
    }
    result = {
        "artifact_kind": "p2_i1_runtime_preflight",
        "schema_version": "1.0.0",
        "evidence_effect": "none_infrastructure_only",
        "execution_class": runtime_policy["execution_class"],
        "seed": seed,
        "cell_id": cell_id,
        "fixture_id": fixture["fixture_id"],
        "topology_digest": digest_canonical_data(topology_projection),
        "route_aspect": route_aspect.to_artifact(),
        "snapshot_family": snapshot["metadata"]["model_family"],
        "baseline_queue_empty": True,
        "baseline_surface_log_empty": True,
        "candidate_execution_authorized": False,
        "machine_local_runtime_path_recorded": False,
    }
    return {**result, "canonical_payload_digest": digest_canonical_data(result)}
