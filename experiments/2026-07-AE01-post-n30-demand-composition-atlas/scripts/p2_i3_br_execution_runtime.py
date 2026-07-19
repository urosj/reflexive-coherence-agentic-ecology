"""Pure execution-authority helpers for the P2-I3 B-R cycle.

This module deliberately imports neither PyGRC nor the I08 case implementation.
It defines portable identities, the exact finite run/terminal projection, governed
path rules, and durable JSON writes shared by I07 and the later I08 supervisor.
Importing it cannot construct a model or perform a candidate operation.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
from typing import Any, Mapping, Sequence


class ExecutionContractError(RuntimeError):
    """Raised when an execution authority or governed path fails closed."""


def repository_root(start: Path) -> Path:
    resolved = start.resolve()
    for candidate in (resolved.parent, *resolved.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root could not be discovered")


ROOT = repository_root(Path(__file__))
EXPERIMENT = Path("experiments/2026-07-AE01-post-n30-demand-composition-atlas")
POLICY_REL = EXPERIMENT / "configs/p2_i3_br_i07_execution_policy.json"
SCHEMA_REL = EXPERIMENT / "contracts/p2-i3/i07-br-execution-authority.schema.json"
REGISTRATION_REL = EXPERIMENT / "contracts/p2-i3/i06-br-exact-registration.json"

ENTRY_PHASES = (
    "P0_governed_entry_claim_durable",
    "P1_child_started",
    "P2_authorities_and_inputs_loaded",
    "P3_parent_restored_and_validated",
    "P4_entry_boundary_armed",
    "P5_entry_specific_dispatch_authorized",
    "P6_output_observed",
    "P7_terminal_receipt_complete",
)

RETRY_TOKEN_CLOSURE_STATES = (
    "unused",
    "allocated_before_attempt_2_claim",
    "attempt_2_failed",
    "attempt_2_valid_terminal",
)

LIVE_OPERATION_SYMBOLS = (
    "pygrc.core.PortGraphBackend",
    "pygrc.models.GRC9V3NodeState",
    "pygrc.models.GRC9V3State",
    "pygrc.models.PortEdge",
    "pygrc.models.LGRC9V3.from_state",
    "pygrc.models.LGRC9V3.get_state",
    "pygrc.models.LGRC9V3.schedule_packet_departure",
    "pygrc.models.LGRC9V3.step",
    "pygrc.models.LGRC9V3.run_event_queue",
    "pygrc.models.LGRC9V3.snapshot",
    "pygrc.models.LGRC9V3.save",
    "pygrc.models.LGRC9V3.load",
    "pygrc.models.LGRC9V3.reset",
    "pygrc.models.lgrc9v3_restoration_identity_v2",
    "pygrc.models.digest_lgrc9v3_restoration_identity_v2",
    "pygrc.models.compute_lgrc9v3_geometric_distances",
    "pygrc.models.compute_lgrc9v3_functional_distances",
    "pygrc.models.compute_lgrc9v3_causal_distances",
)

FORBIDDEN_SYMBOLS = (
    "pygrc.models.GRC9V3.step",
    "pygrc.models.GRC9V3.apply_continuity",
    "pygrc.models.LGRC9V3.set_state",
    "pygrc.models.LGRC9V3.rebase_reset_baseline",
)

CALL_SITE_REGISTRY: dict[str, list[str]] = {
    "pygrc.core.PortGraphBackend": ["p2_i3_i06_br_registration.build_baseline_model"],
    "pygrc.models.GRC9V3NodeState": ["p2_i3_i06_br_registration.build_baseline_model"],
    "pygrc.models.GRC9V3State": ["p2_i3_i06_br_registration.build_baseline_model"],
    "pygrc.models.PortEdge": ["p2_i3_i06_br_registration.build_baseline_model"],
    "pygrc.models.LGRC9V3.from_state": [
        "p2_i3_i06_br_registration.build_baseline_model",
        "p2_i3_i08_br_case.construct_registered_control_state",
    ],
    "pygrc.models.LGRC9V3.get_state": [
        "p2_i3_i08_br_case.native_state",
        "p2_i3_i08_br_case.native_observation",
    ],
    "pygrc.models.LGRC9V3.schedule_packet_departure": ["p2_i3_i08_br_case.schedule_registered_packet"],
    "pygrc.models.LGRC9V3.step": ["p2_i3_i08_br_case.run_registered_event"],
    "pygrc.models.LGRC9V3.run_event_queue": ["p2_i3_i08_br_case.drain_registered_queue"],
    "pygrc.models.LGRC9V3.snapshot": ["p2_i3_i08_br_case.native_observation"],
    "pygrc.models.LGRC9V3.save": ["p2_i3_i08_br_case.write_checkpoint_bundle"],
    "pygrc.models.LGRC9V3.load": ["p2_i3_i08_br_case.load_checkpoint_bundle"],
    "pygrc.models.LGRC9V3.reset": ["p2_i3_i08_br_case.verify_registered_reset"],
    "pygrc.models.lgrc9v3_restoration_identity_v2": ["p2_i3_i08_br_case.native_identity_record"],
    "pygrc.models.digest_lgrc9v3_restoration_identity_v2": [
        "p2_i3_i08_br_case.native_identity_digest",
        "p2_i3_i08_br_case.load_checkpoint_bundle",
    ],
    "pygrc.models.compute_lgrc9v3_geometric_distances": ["p2_i3_i08_br_case.distance_annotations"],
    "pygrc.models.compute_lgrc9v3_functional_distances": ["p2_i3_i08_br_case.distance_annotations"],
    "pygrc.models.compute_lgrc9v3_causal_distances": ["p2_i3_i08_br_case.distance_annotations"],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ExecutionContractError(message)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def payload_digest(value: Mapping[str, Any]) -> str:
    payload = {key: deepcopy(item) for key, item in value.items() if key != "canonical_payload_digest"}
    return hashlib.sha256(
        (
            json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
            + "\n"
        ).encode("utf-8")
    ).hexdigest()


def with_digest(value: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result["canonical_payload_digest"] = payload_digest(result)
    return result


def verify_digest(value: Mapping[str, Any]) -> None:
    require(value.get("canonical_payload_digest") == payload_digest(value), "canonical payload digest mismatch")


def validate_policy_command_environments(policy: Mapping[str, Any]) -> None:
    """Require each retained command to carry the complete normalized environment."""

    environment = policy["environment"]
    normalized = tuple(
        f"{key}={environment['required_environment'][key]}"
        for key in sorted(environment["required_environment"])
    ) + (f"PYTHONPATH={environment['normalized_pythonpath']}",)
    for command_id in (
        "build_inactive_freeze",
        "validate_inactive_freeze",
        "reconstruct_inactive_freeze",
    ):
        tokens = shlex.split(policy["commands"][command_id])
        require(tokens[0] == "env", f"{command_id} lacks explicit env boundary")
        interpreter_index = tokens.index(environment["interpreter"])
        require(
            tuple(tokens[1:interpreter_index]) == normalized,
            f"{command_id} normalized environment drifted",
        )
    launch = shlex.split(policy["commands"]["future_launch_prefix"])
    require(launch[0] == "env", "future launch lacks explicit env boundary")
    interpreter_index = launch.index(environment["interpreter"])
    require(
        tuple(launch[1:interpreter_index])
        == (
            f"{environment['graph_root_environment_variable']}={environment['retained_graph_root']}",
            *normalized,
        ),
        "future launch normalized environment drifted",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"JSON authority missing or symlinked: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON authority is not an object: {path}")
    return value


def identity(relative: str | Path, *, root: Path = ROOT) -> dict[str, str]:
    path = portable_path(relative)
    absolute = root / path
    require(absolute.is_file() and not absolute.is_symlink(), f"identity source missing: {path}")
    return {"path": path.as_posix(), "sha256": sha256_file(absolute)}


def portable_path(value: str | Path) -> PurePosixPath:
    raw = str(value).replace("\\", "/")
    path = PurePosixPath(raw)
    require(raw and not path.is_absolute(), f"path must be repository-relative: {raw!r}")
    require(".." not in path.parts and "." not in path.parts, f"path traversal is forbidden: {raw!r}")
    require(not re.match(r"^[A-Za-z]:", raw), f"drive-qualified path is forbidden: {raw!r}")
    return path


def entry_slug(entry_id: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", entry_id.lower()).strip("-")
    require(slug and len(slug) <= 180, f"invalid entry slug: {entry_id}")
    return slug


def entry_root(policy: Mapping[str, Any], entry: Mapping[str, Any], ordinal: int) -> PurePosixPath:
    template = str(policy["live_paths"]["entry_root_template"])
    return portable_path(
        template.format(
            schedule_ordinal=ordinal,
            entry_slug=entry_slug(str(entry["entry_id"])),
        )
    )


def governed_paths(policy: Mapping[str, Any], entry: Mapping[str, Any], ordinal: int) -> dict[str, str]:
    root = entry_root(policy, entry, ordinal)
    return {
        "primary_claim": (root / "attempt-1" / "claim.json").as_posix(),
        "primary_phase_ledger": (root / "attempt-1" / "phases.jsonl").as_posix(),
        "primary_ready": (root / "attempt-1" / "ready.json").as_posix(),
        "primary_failure": (root / "attempt-1" / "failure.json").as_posix(),
        "primary_p5": (root / "attempt-1" / "p5-authorization.json").as_posix(),
        "primary_p5_consumption": (root / "attempt-1" / "p5-consumption.json").as_posix(),
        "primary_stdout": (root / "attempt-1" / "stdout.bin").as_posix(),
        "primary_stdout_partial": (root / "attempt-1" / "stdout.bin.partial").as_posix(),
        "primary_stderr": (root / "attempt-1" / "stderr.bin").as_posix(),
        "primary_stderr_partial": (root / "attempt-1" / "stderr.bin.partial").as_posix(),
        "primary_terminal": (root / "attempt-1" / "terminal.json").as_posix(),
        "primary_resource": (root / "attempt-1" / "resource.json").as_posix(),
        "retry_claim": (root / "attempt-2" / "claim.json").as_posix(),
        "retry_phase_ledger": (root / "attempt-2" / "phases.jsonl").as_posix(),
        "retry_ready": (root / "attempt-2" / "ready.json").as_posix(),
        "retry_failure": (root / "attempt-2" / "failure.json").as_posix(),
        "retry_p5": (root / "attempt-2" / "p5-authorization.json").as_posix(),
        "retry_p5_consumption": (root / "attempt-2" / "p5-consumption.json").as_posix(),
        "retry_stdout": (root / "attempt-2" / "stdout.bin").as_posix(),
        "retry_stdout_partial": (root / "attempt-2" / "stdout.bin.partial").as_posix(),
        "retry_stderr": (root / "attempt-2" / "stderr.bin").as_posix(),
        "retry_stderr_partial": (root / "attempt-2" / "stderr.bin.partial").as_posix(),
        "retry_terminal": (root / "attempt-2" / "terminal.json").as_posix(),
        "retry_resource": (root / "attempt-2" / "resource.json").as_posix(),
        "entry_resolution": (root / "entry-resolution.json").as_posix(),
        "logical_manifest": (root / "logical-manifest.json").as_posix(),
    }


def expected_artifact_roles(entry: Mapping[str, Any]) -> list[str]:
    if entry["entry_kind"] == "operational_baseline_construction":
        return [
            "attempt_claim",
            "phase_ledger",
            "p5_authorization",
            "runtime_source_binding",
            "immutable_native_plus_rcae_baseline_bundle",
            "native_restoration_identity_v2",
            "resource_receipt",
            "operational_baseline_terminal",
            "entry_resolution",
        ]
    if entry["case_kind"] == "quarantined_integrity_fault":
        return [
            "attempt_claim",
            "phase_ledger",
            "p5_authorization",
            "integrity_refusal_receipt",
            "before_after_composite_identity",
            "resource_receipt",
            "attempt_terminal",
            "case_resolution",
        ]
    common = [
        "attempt_claim",
        "phase_ledger",
        "p5_authorization",
        "runtime_source_binding",
        "before_after_exact_composite_identity",
        "causal_chain_receipts",
        "formation_cost_and_budget_receipts",
        "global_conservation_receipt",
        "forbidden_read_attestation",
        "producer_operation_receipts",
        "resource_receipt",
        "attempt_terminal",
        "case_resolution",
    ]
    if entry.get("terminal_probe"):
        return common + [
            "clean_parent_checkpoint_reference",
            "fixed_encounter_request",
            "native_disposition",
            "signed_admissibility_margin",
            "distance_annotations",
        ]
    return common + [
        "substrate_baseline_reference",
        "trajectory_operation_ledger",
        "checkpoint_manifests",
        "future_probe_parent_selectors",
    ]


def build_entry_rows(registration: Mapping[str, Any], policy: Mapping[str, Any]) -> list[dict[str, Any]]:
    canonical_cases = (
        registration["matrix"]["integrity_fault_cases"]
        + registration["matrix"]["scientific_branches"]
    )
    cases = {row["case_id"]: row for row in canonical_cases}
    schedule = registration["schedule"]
    entries = schedule["entries"]
    resources = {
        row["entry_id"]: row for row in registration["resource_governance"]["assignments"]
    }
    slots = {row["entry_id"]: row for row in registration["attempt_governance"]["slots"]}
    require(len(canonical_cases) == len(cases) == 450, "I06 canonical case population is not closed")
    require(
        [row["case_id"] for row in canonical_cases]
        == schedule["canonical_case_registry_order"],
        "I06 canonical case registry order drifted",
    )
    require(len(entries) == len(resources) == len(slots) == 456, "I06 governed entry population is not closed")
    require(schedule["canonical_case_registry_count"] == 450, "I06 canonical case count drifted")
    require(schedule["operational_baseline_entry_count"] == 6, "I06 operational baseline count drifted")
    require(schedule["governed_entry_count"] == 456, "I06 governed entry count drifted")
    require(schedule["order"] == [row["entry_id"] for row in entries], "I06 schedule order drifted")
    require(
        schedule["dependency_dag"]
        == [
            {"entry_id": row["entry_id"], "parent_entry_ids": row["parent_entry_ids"]}
            for row in entries
        ],
        "I06 dependency DAG drifted",
    )
    rows: list[dict[str, Any]] = []
    for ordinal, scheduled in enumerate(entries, start=1):
        entry_id = str(scheduled["entry_id"])
        case_id = scheduled.get("case_id")
        source = cases.get(case_id) if case_id is not None else None
        require(scheduled["schedule_ordinal"] == ordinal, "entry schedule ordinal drift")
        require(resources[entry_id]["schedule_ordinal"] == ordinal, "resource schedule drift")
        require(slots[entry_id]["schedule_ordinal"] == ordinal, "attempt schedule drift")
        require(resources[entry_id]["entry_kind"] == scheduled["entry_kind"], "resource entry-kind drift")
        require(slots[entry_id]["entry_kind"] == scheduled["entry_kind"], "attempt entry-kind drift")
        if source is None:
            require(
                scheduled["entry_kind"] == "operational_baseline_construction"
                and case_id is None,
                "non-case entry is not an operational baseline",
            )
        else:
            require(str(source["case_id"]) == entry_id == case_id, "canonical case/schedule identity drift")
        parents = list(scheduled["parent_entry_ids"])
        row = {
            "schedule_ordinal": ordinal,
            "entry_id": entry_id,
            "entry_kind": scheduled["entry_kind"],
            "case_id": case_id,
            "case_kind": source["case_kind"] if source else None,
            "configuration_id": scheduled.get("configuration_id"),
            "substrate_base_id": scheduled["substrate_base_id"],
            "delay_profile_id": scheduled.get("delay_profile_id"),
            "realization_id": scheduled.get("realization_id"),
            "execution_class": scheduled["execution_class"],
            "branch_kind": source.get("branch_kind") if source else None,
            "fault_type": source.get("fault_type") if source else None,
            "checkpoint": source.get("checkpoint") if source else None,
            "participant_class": source.get("participant_class") if source else None,
            "route_role": source.get("route_role") if source else None,
            "parent_entry_ids": parents,
            "declared_parent_refs": list(scheduled.get("declared_parent_refs", [])),
            "produced_restoration_refs": list(scheduled.get("produced_restoration_refs", [])),
            "produced_checkpoint_refs": list(scheduled.get("produced_checkpoint_refs", [])),
            "fresh_runtime_load_ref": scheduled.get("fresh_runtime_load_ref"),
            "dependency_ids": parents,
            "scientific_evidence_effect": scheduled["scientific_evidence_effect"],
            "scientific_operation_counts": deepcopy(
                scheduled.get("scientific_operation_counts")
            ),
            "resource": deepcopy(resources[entry_id]),
            "attempt": deepcopy(slots[entry_id]),
            "phases": list(ENTRY_PHASES),
            "governed_paths": governed_paths(policy, scheduled, ordinal),
            "expected_artifact_roles": expected_artifact_roles(
                {**scheduled, **(source or {})}
            ),
            "expected_case_terminal": (
                "atomic_fail_closed_quarantined_no_scientific_continuation"
                if source and source["case_kind"] == "quarantined_integrity_fault"
                else (
                    "typed_operational_baseline_terminal_without_scientific_effect"
                    if source is None
                    else "typed_complete_or_registered_noncompletion_without_interpretation"
                )
            ),
        }
        rows.append(row)
    require(
        {row["case_id"] for row in rows if row["case_id"] is not None}
        == set(schedule["canonical_case_registry_order"]),
        "I06 scheduled case membership drifted",
    )
    return rows


def build_expected_terminal_set(rows: Sequence[Mapping[str, Any]], registration: Mapping[str, Any]) -> list[dict[str, Any]]:
    terminals: list[dict[str, Any]] = [
        {
            "terminal_id": "P2-I3-BR-C01-CAMPAIGN-CLAIM-CLOSURE",
            "root_class": "campaign_claim_closure",
            "required": True,
        }
    ]
    for row in rows:
        entry_id = str(row["entry_id"])
        terminals.extend(
            [
                {
                    "terminal_id": f"{entry_id}:primary-slot-closure",
                    "root_class": "attempt_slot_closure",
                    "entry_id": entry_id,
                    "case_id": row["case_id"],
                    "attempt": 1,
                    "required": True,
                    "allowed": ["attempt_terminal", "blocked_dependency", "not_started_campaign_stop"],
                },
                {
                    "terminal_id": (
                        f"{entry_id}:operational-baseline-terminal"
                        if row["entry_kind"] == "operational_baseline_construction"
                        else f"{entry_id}:case-resolution"
                    ),
                    "root_class": (
                        "operational_baseline_terminal"
                        if row["entry_kind"] == "operational_baseline_construction"
                        else "case_resolution"
                    ),
                    "entry_id": entry_id,
                    "case_id": row["case_id"],
                    "required": True,
                },
            ]
        )
    for token in registration["attempt_governance"]["class_retry_tokens"]:
        terminals.append(
            {
                "terminal_id": f"{token['token_id']}:closure",
                "root_class": "retry_token_closure",
                "required": True,
                "closure_model": "token_root_owns_optional_attempt_2_descendants",
                "allowed": list(RETRY_TOKEN_CLOSURE_STATES),
                "descendant_rule": "every_attempt_2_artifact_reachable_from_exactly_one_permanent_class_token_closure",
            }
        )
    terminals.extend(
        [
            {
                "terminal_id": "P2-I3-BR-C01-SUPERVISOR-RESUME-CLOSURE",
                "root_class": "resume_closure",
                "required": True,
                "allowed": ["unused", "used_once_and_closed"],
            },
            {
                "terminal_id": "P2-I3-BR-C01-CYCLE-CLOSEOUT",
                "root_class": "cycle_closeout",
                "required": True,
            },
        ]
    )
    require(len(terminals) == 919, "expected terminal-set population drift")
    require(
        len({row["terminal_id"] for row in terminals}) == 919,
        "expected terminal-set identity collision",
    )
    return terminals


def classify_retry_token_closure(
    *,
    token_present: bool,
    attempt_2_claim_present: bool,
    attempt_2_terminal_status: str | None,
    attempt_2_descendant_count: int,
) -> str:
    """Classify one permanent class-token closure without inventing a root.

    The token closure is one of the 919 closure roots.  A consumed token owns
    its attempt-2 claim, phases, terminal, logs, resource receipt, output, and
    final entry resolution as digest-bound descendants; those descendants are
    never additional terminal roots.
    """

    require(attempt_2_descendant_count >= 0, "negative retry descendant count")
    if not token_present:
        require(not attempt_2_claim_present, "attempt-2 claim exists without a class token")
        require(attempt_2_terminal_status is None, "attempt-2 terminal exists without a class token")
        require(attempt_2_descendant_count == 0, "retry output exists without a class token")
        return "unused"
    if not attempt_2_claim_present:
        require(attempt_2_terminal_status is None, "attempt-2 terminal exists before its claim")
        require(attempt_2_descendant_count == 0, "attempt-2 descendants exist before their claim")
        return "allocated_before_attempt_2_claim"
    require(attempt_2_terminal_status is not None, "claimed attempt-2 lacks a terminal")
    require(attempt_2_descendant_count > 0, "claimed attempt-2 lacks reachable descendants")
    return (
        "attempt_2_valid_terminal"
        if attempt_2_terminal_status == "valid_terminal"
        else "attempt_2_failed"
    )


def ensure_no_symlink_components(root: Path, relative: str | Path, *, leaf_may_be_absent: bool = True) -> Path:
    portable = portable_path(relative)
    current = root.resolve()
    for index, part in enumerate(portable.parts):
        current = current / part
        final = index == len(portable.parts) - 1
        if not current.exists() and final and leaf_may_be_absent:
            break
        if not current.exists():
            continue
        require(not current.is_symlink(), f"governed path contains symlink: {portable}")
    return root / Path(*portable.parts)


def write_exclusive_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        payload = canonical_bytes(value)
        os.write(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    parent_descriptor = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(parent_descriptor)
    finally:
        os.close(parent_descriptor)


__all__ = [
    "CALL_SITE_REGISTRY",
    "ENTRY_PHASES",
    "ExecutionContractError",
    "FORBIDDEN_SYMBOLS",
    "LIVE_OPERATION_SYMBOLS",
    "POLICY_REL",
    "REGISTRATION_REL",
    "RETRY_TOKEN_CLOSURE_STATES",
    "ROOT",
    "SCHEMA_REL",
    "build_entry_rows",
    "build_expected_terminal_set",
    "classify_retry_token_closure",
    "canonical_bytes",
    "ensure_no_symlink_components",
    "identity",
    "load_json",
    "payload_digest",
    "portable_path",
    "require",
    "sha256_file",
    "validate_policy_command_environments",
    "verify_digest",
    "with_digest",
    "write_exclusive_json",
]
