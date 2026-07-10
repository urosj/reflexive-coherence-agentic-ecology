"""Experiment-local infrastructure for the AE01 Phase 1 contract freeze.

This module intentionally has no packaging metadata and no import-time PyGRC
dependency. Artifact inspection is local and non-runtime. Live binding is an
explicit function that fails closed and always returns a receipt.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import AbstractContextManager
from copy import deepcopy
import hashlib
import importlib
import importlib.metadata
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
from types import MappingProxyType, ModuleType
from typing import Any


SCHEMA_VERSION = "1.0.0"
TOOLING_VERSION = "1.0.0"
DIGEST_ALGORITHM = "sha256"

LANE_IDS = tuple(f"AE01-L0{index}" for index in range(1, 8))
HYPOTHESIS_IDS = tuple(
    [f"AE01-H-L0{index}" for index in range(1, 8)]
    + ["AE01-H-S01", "AE01-H-S02"]
)
COMMON_CONTROL_IDS = tuple(f"AE01-CTRL-{index:02d}" for index in range(1, 20))
FAILURE_IDS = tuple(f"AE01-F{index:02d}" for index in range(1, 11))
LANE_CONTROL_IDS = {
    lane_id: tuple(f"{lane_id}-CTRL-{index:02d}" for index in range(1, 6))
    for lane_id in LANE_IDS
}

COMPARISON_GROUPS = (
    "reference",
    "candidate",
    "withdrawal",
    "active_null",
    "lineage_or_source",
    "budget_or_leakage",
    "transfer_or_contrast",
)
EXPECTED_ARTIFACT_ROLES = (
    "comparison_record",
    "control_record",
    "runtime_binding_receipt_for_every_live_run",
    "terminal_classification_input",
)
EXPECTED_NON_SELECTION_CONDITIONS = (
    "no_candidate_clears_every_eligibility_gate",
    "eligible_candidates_exist_but_none_clears_every_threshold",
    "tie_remains_after_declared_procedure",
    "sensitivity_profiles_change_winner",
    "required_lane_or_synthesis_record_incomplete",
    "conceptual_demand_is_primary_support",
    "reconstruction_cannot_be_bounded",
    "unnamed_stronger_prerequisite_required",
)

EVIDENCE_TIERS = (
    "exploratory_scratch",
    "registered_probe",
    "retained_evidence",
)
LIVE_EXECUTION_CLASSES = (
    "pygrc_runtime_with_rcae_producer",
    "pygrc_native_runtime",
)
TERMINAL_CLASSIFICATIONS = (
    "supported_bounded_candidate",
    "partial_or_mixed",
    "not_supported",
    "blocked_missing_prerequisite",
    "incomplete_execution",
)

INDIVIDUAL_RETENTION_REVIEW_BYTES = 1024 * 1024
SET_RETENTION_REVIEW_BYTES = 10 * 1024 * 1024


class ContractError(ValueError):
    """One or more contract checks failed."""

    def __init__(self, issues: str | Iterable[str]):
        if isinstance(issues, str):
            values = [issues]
        else:
            values = list(issues)
        self.issues = tuple(values)
        super().__init__("; ".join(self.issues))


def canonicalize_json_value(value: Any) -> Any:
    """Return the PyGRC-compatible deterministic JSON-safe form."""

    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ContractError("canonical JSON rejects non-finite floats")
        return value
    if isinstance(value, MappingProxyType):
        value = dict(value)
    if isinstance(value, Mapping):
        bad_keys = [key for key in value if not isinstance(key, str)]
        if bad_keys:
            raise ContractError(
                f"canonical JSON requires string keys; got {bad_keys!r}"
            )
        return {
            key: canonicalize_json_value(inner)
            for key, inner in sorted(value.items())
        }
    if isinstance(value, (list, tuple)):
        return [canonicalize_json_value(item) for item in value]
    if isinstance(value, (set, frozenset)):
        canonical_items = [canonicalize_json_value(item) for item in value]
        return sorted(canonical_items, key=canonical_json_dumps)
    raise ContractError(
        "canonical JSON does not support " f"{type(value).__name__}"
    )


def canonical_json_dumps(value: Any) -> str:
    """Encode compact canonical JSON used for semantic digests."""

    return json.dumps(
        canonicalize_json_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def pretty_json_dumps(value: Any) -> str:
    """Encode the deterministic tracked-file representation."""

    return (
        json.dumps(
            canonicalize_json_value(value),
            indent=2,
            sort_keys=True,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )


def digest_canonical_data(value: Any) -> str:
    """Return the SHA-256 digest of canonical JSON data."""

    return hashlib.sha256(canonical_json_dumps(value).encode("utf-8")).hexdigest()


def digest_file(path: Path) -> str:
    """Return the exact-file SHA-256 digest."""

    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def semantic_file_digest(path: Path) -> str:
    """Digest JSON canonically and other files by exact bytes."""

    if path.suffix.lower() == ".json":
        return digest_canonical_data(load_json(path))
    return digest_file(path)


def deterministic_id(kind: str, identity: Any) -> str:
    """Build a stable AE01 ID from a declared identity payload."""

    slug = re.sub(r"[^a-z0-9]+", "-", kind.casefold()).strip("-")
    if not slug:
        raise ContractError("deterministic ID kind must contain a letter or number")
    return f"ae01:{slug}:{digest_canonical_data(identity)[:16]}"


def validate_portable_path(value: str) -> str:
    """Require a normalized repository-relative POSIX path."""

    if not isinstance(value, str) or not value:
        raise ContractError("portable path must be a non-empty string")
    if value == ".":
        return value
    if "\\" in value or "\x00" in value:
        raise ContractError(f"non-portable path syntax: {value!r}")
    if value.startswith(("/", "~")) or re.match(r"^[A-Za-z]:", value):
        raise ContractError(f"path must be repository-relative: {value!r}")
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ContractError(f"path must be normalized and traversal-free: {value!r}")
    normalized = PurePosixPath(value).as_posix()
    if normalized != value:
        raise ContractError(f"path is not normalized: {value!r}")
    return value


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(pretty_json_dumps(value), encoding="utf-8")


def find_repository_root(start: Path | None = None) -> Path:
    """Find the RCAE checkout without persisting its machine-local location."""

    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (
            (candidate / "implementation/PostN30-plan.md").is_file()
            and (candidate / "experiments/README.md").is_file()
        ):
            return candidate
    raise ContractError("unable to locate the RCAE repository root")


def _jsonschema_validator(schema: Mapping[str, Any]) -> Any:
    try:
        module = importlib.import_module("jsonschema")
    except ModuleNotFoundError as exc:
        raise ContractError(
            "jsonschema is required; use the pinned repository command"
        ) from exc
    validator_class = module.Draft202012Validator
    validator_class.check_schema(schema)
    return validator_class(schema)


def validate_schema_record(
    record: Mapping[str, Any], schema: Mapping[str, Any]
) -> None:
    """Validate one common record against the P1-I3 schema."""

    validator = _jsonschema_validator(schema)
    issues = [
        f"schema:{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: "
        f"{error.message}"
        for error in sorted(
            validator.iter_errors(record),
            key=lambda item: tuple(str(part) for part in item.absolute_path),
        )
    ]
    if issues:
        raise ContractError(issues)


PATH_FIELDS = frozenset(
    {
        "path",
        "working_directory",
        "expected_path",
        "implementation_path",
        "output_path",
    }
)


def _validate_embedded_paths(value: Any, *, context: str = "record") -> list[str]:
    issues: list[str] = []
    if isinstance(value, Mapping):
        for key, inner in value.items():
            child = f"{context}.{key}"
            if key in PATH_FIELDS and isinstance(inner, str):
                try:
                    validate_portable_path(inner)
                except ContractError as exc:
                    issues.append(f"{child}: {exc}")
            issues.extend(_validate_embedded_paths(inner, context=child))
    elif isinstance(value, list):
        for index, inner in enumerate(value):
            issues.extend(
                _validate_embedded_paths(inner, context=f"{context}[{index}]")
            )
    elif isinstance(value, str):
        machine_path = re.search(
            r"(?:^|[\s\"'(])(?:file://|/(?:home|Users|tmp|private/tmp)/|[A-Za-z]:\\)",
            value,
        )
        if machine_path:
            issues.append(f"{context}: machine-local path is not persistable")
    return issues


def _profile_map(profile_registry: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    profiles = profile_registry.get("record", profile_registry).get("profiles", [])
    result: dict[str, Mapping[str, Any]] = {}
    for profile in profiles:
        profile_id = profile.get("profile_id")
        if profile_id in result:
            raise ContractError(f"duplicate profile ID: {profile_id}")
        result[profile_id] = profile
    return result


def _validate_source_inventory(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    source_ids: set[str] = set()
    for source in payload.get("sources", []):
        source_id = source.get("source_id", "<missing>")
        if source_id in source_ids:
            issues.append(f"duplicate source ID: {source_id}")
        source_ids.add(source_id)
        role = source.get("evidence_role")
        runtime_allowed = source.get("runtime_evidence_permission")
        positive_allowed = source.get("positive_evidence_permission")
        if role == "conceptual_motivation" and runtime_allowed is not False:
            issues.append(f"{source_id}: conceptual source cannot be runtime evidence")
        if role == "conceptual_motivation" and positive_allowed is not False:
            issues.append(f"{source_id}: conceptual source cannot be positive evidence")
        if source.get("mutable"):
            if not source.get("current_sha256") or not source.get("historical_sha256"):
                issues.append(
                    f"{source_id}: mutable source requires current and historical digests"
                )
    return issues


def _validate_claim_boundary(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    flags = payload.get("unsafe_flags", {})
    if not flags:
        issues.append("claim boundary requires unsafe flags")
    for flag, value in flags.items():
        if value is not False:
            issues.append(f"unsafe claim flag must be false: {flag}")
    return issues


def _validate_realization_profile(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    availability = bool(payload.get("availability"))
    enabled = bool(payload.get("enabled"))
    validated = bool(payload.get("validated"))
    supported = bool(payload.get("supported"))
    if enabled and not availability:
        issues.append("enabled realization must be available")
    if validated and not enabled:
        issues.append("validated realization must be enabled")
    if supported and not validated:
        issues.append("supported realization must be validated")
    if (
        payload.get("realization_class") == "rcae_constructed"
        and payload.get("evidence_role") != "constructed_ecology_mechanism"
    ):
        issues.append("RCAE-constructed realization must retain constructed role")
    return issues


def _validate_runtime_receipt(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    execution_class = payload.get("execution_class")
    conformance = payload.get("conformance_status")
    failure_status = payload.get("failure", {}).get("status")
    if execution_class == "artifact_inspection":
        if conformance != "not_applicable_non_runtime":
            issues.append("artifact inspection must be explicitly non-runtime")
    elif execution_class in LIVE_EXECUTION_CLASSES:
        if conformance == "passed" and failure_status != "not_applicable":
            issues.append("passed live binding cannot carry an applicable failure")
        if conformance == "failed" and failure_status != "applicable":
            issues.append("failed live binding must carry an applicable failure")
    else:
        issues.append(f"unknown execution class: {execution_class}")
    if payload.get("graph_repository_write_observed") is not False:
        issues.append("runtime receipt must preserve graph read-only boundary")
    return issues


def _validate_pattern_card(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    lane_id = payload.get("lane_id")
    if lane_id not in LANE_IDS:
        issues.append(f"unknown lane ID: {lane_id}")
        return issues
    allowed_controls = set(COMMON_CONTROL_IDS) | set(LANE_CONTROL_IDS[lane_id])
    control_refs = set(payload.get("control_refs", []))
    unknown_controls = control_refs - allowed_controls
    if unknown_controls:
        issues.append(f"unknown or cross-lane controls: {sorted(unknown_controls)}")
    missing_lane_controls = set(LANE_CONTROL_IDS[lane_id]) - control_refs
    if missing_lane_controls:
        issues.append(f"missing mandatory lane controls: {sorted(missing_lane_controls)}")
    unknown_failures = set(payload.get("failure_modes", [])) - set(FAILURE_IDS)
    if unknown_failures:
        issues.append(f"unknown failure IDs: {sorted(unknown_failures)}")
    return issues


def _validate_terminal(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    classification = payload.get("classification")
    execution_status = payload.get("execution_status")
    reconstruction = payload.get("reconstruction_status")
    evidence_refs = payload.get("retained_evidence_refs", [])
    lane_id = payload.get("lane_id")
    if lane_id not in LANE_IDS:
        issues.append(f"unknown lane ID: {lane_id}")
    else:
        control_refs = set(payload.get("control_refs", []))
        required_controls = set(COMMON_CONTROL_IDS) | set(LANE_CONTROL_IDS[lane_id])
        if control_refs != required_controls:
            missing = sorted(required_controls - control_refs)
            unknown = sorted(control_refs - required_controls)
            if missing:
                issues.append(f"terminal record omits mandatory controls: {missing}")
            if unknown:
                issues.append(f"terminal record has unknown or cross-lane controls: {unknown}")
    if classification in (
        "supported_bounded_candidate",
        "partial_or_mixed",
        "not_supported",
    ):
        if execution_status != "completed":
            issues.append(f"{classification} requires completed execution")
        if reconstruction != "verified":
            issues.append(f"{classification} requires verified reconstruction")
        if not evidence_refs:
            issues.append(f"{classification} requires retained evidence")
        if payload.get("stopping_condition_reached") is not True:
            issues.append(f"{classification} requires its stopping condition")
        if payload.get("record_complete") is not True:
            issues.append(f"{classification} requires a complete terminal record")
    if classification in ("supported_bounded_candidate", "partial_or_mixed"):
        if not payload.get("positive_signatures"):
            issues.append(f"{classification} requires a bounded positive signature")
    if classification == "not_supported" and not payload.get("negative_signatures"):
        issues.append("not_supported requires a scientific negative signature")
    if classification == "blocked_missing_prerequisite" and execution_status != "blocked":
        issues.append("blocked classification requires blocked execution status")
    if classification == "incomplete_execution":
        if payload.get("positive_signatures"):
            issues.append("incomplete execution cannot carry positive signatures")
        if payload.get("forces_n31_non_selection") is not True:
            issues.append("incomplete execution must force N31+ non-selection")
    return issues


SCORE_GROUPS = {
    "demand": (
        "cross_lane_recurrence",
        "prerequisite_centrality",
        "composition_leverage",
        "transfer_value",
    ),
    "experimental_readiness": (
        "gap_tension_specificity",
        "future_discriminator_quality",
        "control_feasibility",
        "naturalization_debt_path",
    ),
    "safety_feasibility": ("claim_safety", "cost_feasibility"),
}


def _validate_ranking(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    candidates_by_id: dict[str, Mapping[str, Any]] = {}
    scored_candidate_ids: set[str] = set()
    for candidate in payload.get("candidates", []):
        candidate_id = candidate.get("candidate_id", "<missing>")
        if candidate_id in candidates_by_id:
            issues.append(f"duplicate candidate ID: {candidate_id}")
        candidates_by_id[candidate_id] = candidate
        all_gates = all(candidate.get("eligibility_gates", {}).values())
        if candidate.get("eligible") is not all_gates:
            issues.append(f"{candidate_id}: eligible must equal all eligibility gates")
        if candidate.get("scoring_status") != "scored":
            continue
        scored_candidate_ids.add(candidate_id)
        scores = candidate.get("scores", {})
        calculated_groups = {
            group: sum(scores.get(name, 0) for name in names)
            for group, names in SCORE_GROUPS.items()
        }
        if candidate.get("group_totals") != calculated_groups:
            issues.append(f"{candidate_id}: group totals do not match scores")
        overall = sum(calculated_groups.values())
        if candidate.get("overall_total") != overall:
            issues.append(f"{candidate_id}: overall total does not match scores")
        checks = {
            "every_dimension": all(value >= 1 for value in scores.values()),
            "demand": calculated_groups["demand"] >= 7,
            "experimental_readiness": calculated_groups["experimental_readiness"] >= 8,
            "safety_feasibility": calculated_groups["safety_feasibility"] >= 4,
            "overall": overall >= 20,
            "critical_dimensions": all(
                scores.get(name, 0) >= 2
                for name in (
                    "gap_tension_specificity",
                    "future_discriminator_quality",
                    "control_feasibility",
                    "claim_safety",
                )
            ),
        }
        if candidate.get("threshold_checks") != checks:
            issues.append(f"{candidate_id}: threshold checks do not match scores")
        if candidate.get("threshold_passed") is not all(checks.values()):
            issues.append(f"{candidate_id}: threshold result does not match checks")
        profiles = [item.get("profile") for item in candidate.get("sensitivity_profiles", [])]
        if len(profiles) != len(set(profiles)):
            issues.append(f"{candidate_id}: duplicate sensitivity profiles")
        expected_profile_totals = {
            "equal": overall,
            "doubled_demand": overall + calculated_groups["demand"],
            "doubled_readiness_safety": (
                overall
                + calculated_groups["experimental_readiness"]
                + calculated_groups["safety_feasibility"]
            ),
        }
        for profile in candidate.get("sensitivity_profiles", []):
            profile_name = profile.get("profile")
            if (
                profile_name in expected_profile_totals
                and profile.get("total") != expected_profile_totals[profile_name]
            ):
                issues.append(
                    f"{candidate_id}: {profile_name} sensitivity total is inconsistent"
                )
            if profile.get("wins_or_ties") is not (profile.get("rank") == 1):
                issues.append(
                    f"{candidate_id}: {profile_name} wins_or_ties must match rank one"
                )
    selected = payload.get("selected_candidate", {})
    if scored_candidate_ids and not payload.get("synthesis_refs"):
        issues.append("candidate scoring requires completed synthesis references")
    selected_result_ids = {
        candidate_id
        for candidate_id, candidate in candidates_by_id.items()
        if candidate.get("candidate_result") == "selected"
    }
    if payload.get("selection_result") == "selected":
        selected_id = selected.get("candidate_id")
        candidate = candidates_by_id.get(selected_id)
        if candidate is None:
            issues.append("selected candidate does not resolve")
        else:
            if candidate.get("scoring_status") != "scored":
                issues.append("selected candidate must be scored")
            if candidate.get("eligible") is not True:
                issues.append("selected candidate must be eligible")
            if candidate.get("threshold_passed") is not True:
                issues.append("selected candidate must pass every frozen threshold")
            if candidate.get("tie_result") == "shortlisted_unresolved":
                issues.append("unresolved tie requires non-selection")
            if candidate.get("tie_breaker_reached") == "unresolved":
                issues.append("unresolved tie procedure requires non-selection")
            if not all(
                item.get("wins_or_ties") is True
                for item in candidate.get("sensitivity_profiles", [])
            ):
                issues.append("selected candidate must remain robust in every profile")
        if selected_result_ids != {selected_id}:
            issues.append("candidate_result selection must match selected candidate")
    elif selected_result_ids:
        issues.append("non-selection or not-run record cannot mark a candidate selected")
    return issues


def _validate_profile_registry(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    seen: set[str] = set()
    for profile in payload.get("profiles", []):
        profile_id = profile.get("profile_id", "<missing>")
        if profile_id in seen:
            issues.append(f"duplicate profile ID: {profile_id}")
        seen.add(profile_id)
    return issues


def _validate_manifest(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    profiles = {
        item.get("profile_id"): item
        for item in payload.get("resolved_shared_profiles", [])
    }
    realization_profiles: dict[str, Mapping[str, Any]] = {}
    for profile in payload.get("resolved_realization_profiles", []):
        profile_id = profile.get("profile_id")
        if profile_id in realization_profiles:
            issues.append(f"duplicate resolved realization profile: {profile_id}")
        realization_profiles[profile_id] = profile
    profile_type_by_ref = {
        "command_profile_ref": "command",
        "environment_profile_ref": "environment",
        "dependency_profile_ref": "dependency",
        "resource_profile_ref": "resource",
        "verification_command_profile_ref": "command",
    }
    total_size = 0
    seen_artifacts: set[str] = set()
    seen_paths: set[str] = set()
    for artifact in payload.get("artifacts", []):
        artifact_id = artifact.get("artifact_id", "<missing>")
        if artifact_id in seen_artifacts:
            issues.append(f"duplicate artifact ID: {artifact_id}")
        seen_artifacts.add(artifact_id)
        artifact_path = artifact.get("expected_path")
        if artifact_path in seen_paths:
            issues.append(f"duplicate artifact path: {artifact_path}")
        seen_paths.add(artifact_path)
        total_size += int(artifact.get("expected_size_bytes", 0))
        for field, expected_type in profile_type_by_ref.items():
            profile = profiles.get(artifact.get(field))
            if profile is None:
                issues.append(f"{artifact_id}: unresolved profile {field}")
            elif profile.get("profile_type") != expected_type:
                issues.append(f"{artifact_id}: wrong profile type for {field}")
        tier = artifact.get("evidence_use_tier")
        verified = artifact.get("last_verified_status")
        if tier == "retained_evidence" and verified != "passed":
            issues.append(f"{artifact_id}: retained evidence must be verified")
        if artifact.get("claim_dependency_refs"):
            if tier != "retained_evidence":
                issues.append(f"{artifact_id}: claim dependency requires retained evidence")
            if verified != "passed" or payload.get("fully_resolved") is not True:
                issues.append(f"{artifact_id}: claim dependency requires resolved verification")
        realization = artifact.get("realization_profile", {})
        if artifact.get("execution_class") in LIVE_EXECUTION_CLASSES:
            if realization.get("status") != "applicable":
                issues.append(f"{artifact_id}: live execution requires realization profile")
            else:
                realization_id = realization.get("reference_id")
                resolved_realization = realization_profiles.get(realization_id)
                if resolved_realization is None:
                    issues.append(
                        f"{artifact_id}: unresolved realization profile {realization_id}"
                    )
                elif not (
                    resolved_realization.get("availability")
                    and resolved_realization.get("enabled")
                    and resolved_realization.get("validated")
                ):
                    issues.append(
                        f"{artifact_id}: retained live realization is not available, enabled, and validated"
                    )
        elif realization.get("status") != "not_applicable":
            issues.append(f"{artifact_id}: artifact inspection has no realization profile")
        if (
            int(artifact.get("expected_size_bytes", 0))
            > INDIVIDUAL_RETENTION_REVIEW_BYTES
            and artifact.get("size_review", {}).get("status") != "applicable"
        ):
            issues.append(f"{artifact_id}: large file requires retention review")
    if payload.get("artifact_set_size_bytes") != total_size:
        issues.append("artifact-set size does not match entries")
    if (
        total_size > SET_RETENTION_REVIEW_BYTES
        and payload.get("retention_review", {}).get("status") != "applicable"
    ):
        issues.append("large artifact set requires retention review")
    if payload.get("fully_resolved") and not profiles:
        issues.append("fully resolved manifest requires embedded shared profiles")
    return issues


def _validate_report_projection(payload: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("mode") == "generated_projection" and payload.get("authored_sections"):
        issues.append("generated projection cannot contain authored sections")
    if payload.get("consistency_status") == "passed" and not payload.get(
        "controlling_machine_record_refs"
    ):
        issues.append("passed report requires controlling machine records")
    return issues


def validate_semantics(record: Mapping[str, Any]) -> None:
    """Apply semantic checks without redefining Markdown or schema authority."""

    record_type = record.get("record_type")
    payload = record.get("record", {})
    issues = _validate_embedded_paths(record)
    validators: dict[str, Callable[[Mapping[str, Any]], list[str]]] = {
        "source_inventory": _validate_source_inventory,
        "claim_boundary": _validate_claim_boundary,
        "lane_registry": lambda value: _validate_claim_boundary(
            value.get("claim_boundary", {})
        ),
        "pattern_card": _validate_pattern_card,
        "terminal_classification": _validate_terminal,
        "n31_ranking": _validate_ranking,
        "profile_registry": _validate_profile_registry,
        "artifact_manifest": _validate_manifest,
        "realization_profile": _validate_realization_profile,
        "runtime_binding_receipt": _validate_runtime_receipt,
        "report_projection": _validate_report_projection,
    }
    validator = validators.get(str(record_type))
    if validator is not None:
        issues.extend(validator(payload))
    if issues:
        raise ContractError(issues)


def validate_record(record: Mapping[str, Any], schema: Mapping[str, Any]) -> None:
    validate_schema_record(record, schema)
    validate_semantics(record)


def _extract_projection_rows(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    table_rows = re.findall(
        r"^\| `(AE01-L0[1-7])` \| ([^|]+?) \|", text, flags=re.MULTILINE
    )
    if table_rows:
        return [(lane_id, name.strip()) for lane_id, name in table_rows]
    list_rows = re.findall(
        r"^\d+\. `(AE01-L0[1-7])` — ([^;\n]+)", text, flags=re.MULTILINE
    )
    return [(lane_id, name.strip()) for lane_id, name in list_rows]


def validate_lane_projections(
    registry: Mapping[str, Any], repository_root: Path
) -> None:
    """Validate stable IDs, order, names, and all declared narrative projections."""

    payload = registry.get("record", {})
    lanes = payload.get("lanes", [])
    ids = [lane.get("lane_id") for lane in lanes]
    orders = [lane.get("order") for lane in lanes]
    issues: list[str] = []
    if ids != list(LANE_IDS):
        issues.append(f"lane IDs/order must be {list(LANE_IDS)!r}; got {ids!r}")
    if orders != list(range(1, 8)):
        issues.append(f"lane order values must be 1..7; got {orders!r}")
    if len(ids) != len(set(ids)):
        issues.append("lane registry contains duplicate IDs")
    for target in payload.get("projection_targets", []):
        relative = target.get("path", "")
        try:
            validate_portable_path(relative)
        except ContractError as exc:
            issues.append(f"projection target {relative!r}: {exc}")
            continue
        path = repository_root / relative
        if not path.is_file():
            issues.append(f"missing projection target: {relative}")
            continue
        rows = _extract_projection_rows(path)
        row_ids = [lane_id for lane_id, _ in rows]
        if row_ids != list(LANE_IDS):
            issues.append(f"{relative}: missing, duplicate, stale, or reordered lane IDs")
            continue
        document = " ".join(
            path.read_text(encoding="utf-8").casefold().split()
        )
        for lane, (_, projected_name) in zip(lanes, rows, strict=True):
            current_name = lane.get("current_display_name", "")
            if path.name != "PostN30-plan.md" and projected_name != current_name:
                issues.append(
                    f"{relative}: stale name for {lane.get('lane_id')}: {projected_name!r}"
                )
            if " ".join(current_name.casefold().split()) not in document:
                issues.append(
                    f"{relative}: current name missing for {lane.get('lane_id')}"
                )
        if target.get("consistency_status") != "validated":
            issues.append(f"{relative}: projection status is not validated")
    if issues:
        raise ContractError(issues)


def validate_execution_policy(policy: Mapping[str, Any]) -> None:
    """Validate the finite P1-I4-to-P1-I5 comparison materialization."""

    issues: list[str] = []
    if policy.get("policy_id") != "ae01-p1-i5-execution-policy":
        issues.append("execution policy ID mismatch")
    if policy.get("policy_version") != "1.0.0":
        issues.append("execution policy version must be 1.0.0")
    if policy.get("evidence_effect") != "none_configuration_only":
        issues.append("execution policy cannot claim evidence")
    global_policy = policy.get("global_policy", {})
    seeds = global_policy.get("deterministic_seeds")
    if seeds != [101, 211, 307]:
        issues.append("deterministic seed set must remain [101, 211, 307]")
    if global_policy.get("max_attempts_per_seed") != 1:
        issues.append("max attempts per seed must remain one")
    if global_policy.get("max_infrastructure_retries") != 1:
        issues.append("infrastructure retry limit must remain one")
    if global_policy.get("resource_envelope") != {
        "max_disk_mb": 256,
        "max_memory_mb": 512,
        "max_runtime_seconds": 120,
    }:
        issues.append("resource envelope does not match the P1-I5 freeze")
    if tuple(global_policy.get("expected_artifact_roles", [])) != EXPECTED_ARTIFACT_ROLES:
        issues.append("expected artifact roles do not match the P1-I5 freeze")
    if global_policy.get("support_thresholds") != {
        "mandatory_control_pass_fraction": 1.0,
        "mandatory_signature_pass_fraction": 1.0,
        "minimum_directional_seed_fraction": 1.0,
        "minimum_transfer_contrast_pass_fraction": 2 / 3,
        "unsafe_flag_count_maximum": 0,
    }:
        issues.append("support thresholds do not match the P1-I5 freeze")
    for criteria_name in (
        "success_criteria",
        "invalid_run_criteria",
        "infrastructure_failure_criteria",
    ):
        criteria = global_policy.get(criteria_name, [])
        if not criteria or len(criteria) != len(set(criteria)):
            issues.append(f"{criteria_name} must be a non-empty unique list")
    common_default = global_policy.get("common_control_default", {})
    if common_default.get("status") != "required" or not common_default.get(
        "rationale"
    ):
        issues.append("global common-control default must be required with rationale")
    lanes = policy.get("lanes", [])
    if [item.get("lane_id") for item in lanes] != list(LANE_IDS):
        issues.append("execution-policy lanes must be complete and ordered")
    for index, lane in enumerate(lanes, 1):
        lane_id = f"AE01-L0{index}"
        if lane.get("hypothesis_id") != f"AE01-H-L0{index}":
            issues.append(f"{lane_id}: hypothesis mapping mismatch")
        cells = lane.get("comparison_cells", [])
        if len(cells) != 7:
            issues.append(f"{lane_id}: exactly seven frozen comparison cells required")
        cell_ids = [cell.get("cell_id") for cell in cells]
        if len(cell_ids) != len(set(cell_ids)):
            issues.append(f"{lane_id}: comparison cell IDs must be unique")
        represented_groups: set[str] = set()
        for cell in cells:
            groups = [cell.get("group"), *cell.get("additional_groups", [])]
            unknown_groups = set(groups) - set(COMPARISON_GROUPS)
            if unknown_groups:
                issues.append(
                    f"{lane_id}/{cell.get('cell_id')}: unknown groups {sorted(unknown_groups)}"
                )
            represented_groups.update(group for group in groups if group)
            if cell.get("seed_policy") not in ("global", "deterministic_no_seed"):
                issues.append(f"{lane_id}/{cell.get('cell_id')}: invalid seed policy")
        inapplicable_groups = lane.get("inapplicable_comparison_groups", {})
        for group, rationale in inapplicable_groups.items():
            if group not in COMPARISON_GROUPS or not str(rationale).strip():
                issues.append(f"{lane_id}: invalid inapplicable comparison group")
            if group in represented_groups:
                issues.append(f"{lane_id}: group cannot be represented and inapplicable: {group}")
        if represented_groups | set(inapplicable_groups) != set(COMPARISON_GROUPS):
            missing_groups = set(COMPARISON_GROUPS) - represented_groups - set(inapplicable_groups)
            issues.append(f"{lane_id}: comparison groups are unresolved: {sorted(missing_groups)}")
        if set(lane.get("lane_control_ids", [])) != set(LANE_CONTROL_IDS[lane_id]):
            issues.append(f"{lane_id}: five lane controls do not match freeze")
        direct_controls = set(lane.get("direct_common_control_ids", []))
        if not direct_controls or not direct_controls <= set(COMMON_CONTROL_IDS):
            issues.append(f"{lane_id}: direct common-control priority is invalid")
        threshold = lane.get("primary_threshold", {})
        if threshold.get("operator") != "greater_than":
            issues.append(f"{lane_id}: primary threshold must be strict greater-than")
        if threshold.get("normalized_margin") != 0.0:
            issues.append(f"{lane_id}: normalized margin boundary must remain zero")
        expected_classes = (
            ["artifact_inspection", "pygrc_runtime_with_rcae_producer"]
            if lane_id == "AE01-L07"
            else ["pygrc_runtime_with_rcae_producer"]
        )
        if lane.get("execution_classes") != expected_classes:
            issues.append(f"{lane_id}: execution classes do not match the freeze")
        if lane.get("registration_status") != "frozen_not_executed":
            issues.append(f"{lane_id}: registration must remain frozen and unexecuted")
    synthesis = policy.get("synthesis_entry", {})
    if synthesis.get("required_terminal_lane_ids") != list(LANE_IDS):
        issues.append("synthesis lane set must match the stable lane registry")
    if synthesis.get("terminal_record_count") != len(LANE_IDS):
        issues.append("synthesis terminal count must remain seven")
    if tuple(policy.get("non_selection_conditions", [])) != EXPECTED_NON_SELECTION_CONDITIONS:
        issues.append("non-selection conditions do not match the D-029 freeze")
    if issues:
        raise ContractError(issues)


def resolve_execution_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    """Return a canonical fully explicit comparison-policy view."""

    validate_execution_policy(policy)
    resolved = deepcopy(policy)
    global_policy = resolved["global_policy"]
    for lane in resolved["lanes"]:
        direct_controls = set(lane["direct_common_control_ids"])
        lane["common_control_applicability"] = {
            control_id: {
                "status": global_policy["common_control_default"]["status"],
                "priority": "direct" if control_id in direct_controls else "inherited",
                "rationale": (
                    "P1-I4 identifies this control as especially direct for the lane"
                    if control_id in direct_controls
                    else global_policy["common_control_default"]["rationale"]
                ),
            }
            for control_id in COMMON_CONTROL_IDS
        }
        for cell in lane["comparison_cells"]:
            if cell.get("seed_policy") == "global":
                cell["resolved_seeds"] = list(global_policy["deterministic_seeds"])
            elif cell.get("seed_policy") == "deterministic_no_seed":
                cell["resolved_seeds"] = []
            else:
                raise ContractError(
                    f"{lane['lane_id']}/{cell.get('cell_id')}: invalid seed policy"
                )
            cell["max_attempts_per_seed"] = global_policy["max_attempts_per_seed"]
            cell["max_infrastructure_retries"] = global_policy[
                "max_infrastructure_retries"
            ]
            cell["resource_envelope"] = deepcopy(global_policy["resource_envelope"])
            cell["configuration_id"] = (
                f"{lane['lane_id'].casefold()}-{cell['cell_id']}-v1"
            )
            cell["required_artifact_roles"] = list(
                global_policy["expected_artifact_roles"]
            )
            cell["success_criteria"] = list(global_policy["success_criteria"])
            cell["invalid_run_criteria"] = list(
                global_policy["invalid_run_criteria"]
            )
            cell["infrastructure_failure_criteria"] = list(
                global_policy["infrastructure_failure_criteria"]
            )
    resolved["resolved_policy_digest"] = digest_canonical_data(resolved)
    return canonicalize_json_value(resolved)


def assert_synthesis_entry(terminal_records: Sequence[Mapping[str, Any]]) -> None:
    """Block synthesis until every stable lane has exactly one terminal record."""

    if any(item.get("record_type") != "terminal_classification" for item in terminal_records):
        raise ContractError("synthesis accepts only terminal-classification records")
    if any(item.get("record", {}).get("record_complete") is not True for item in terminal_records):
        raise ContractError("synthesis requires complete terminal records")
    lane_ids = [item.get("record", {}).get("lane_id") for item in terminal_records]
    if sorted(lane_ids) != sorted(LANE_IDS) or len(lane_ids) != len(set(lane_ids)):
        raise ContractError(
            "synthesis requires exactly one terminal record for every AE01 lane"
        )


def build_runtime_binding_receipt(
    realization_profile: Mapping[str, Any],
    *,
    run_id: str,
    execution_class: str,
    requested_operations: Sequence[str],
    importer: Callable[[str], ModuleType] | None = None,
    version_reader: Callable[[str], str] | None = None,
) -> dict[str, Any]:
    """Attempt a strict PyGRC binding and return a receipt even on failure."""

    if execution_class not in LIVE_EXECUTION_CLASSES:
        raise ContractError("live binding requires an explicit live execution class")
    importer = importer or importlib.import_module
    version_reader = version_reader or importlib.metadata.version
    required_identity = realization_profile.get("required_pygrc_identity")
    required_capabilities = set(realization_profile.get("required_capabilities", []))
    conformance = "failed"
    observed_identity = "pygrc:unavailable"
    observed_capabilities: list[str] = []
    failure_rationale = "PyGRC import was not attempted"
    try:
        if not realization_profile.get("availability"):
            raise ContractError("realization profile declares the runtime unavailable")
        if not realization_profile.get("enabled"):
            raise ContractError("realization profile is not explicitly enabled")
        expected_execution_class = (
            "pygrc_runtime_with_rcae_producer"
            if realization_profile.get("realization_class") == "rcae_constructed"
            else "pygrc_native_runtime"
        )
        if execution_class != expected_execution_class:
            raise ContractError(
                "execution class does not match the explicit realization class"
            )
        allowed_operations = set(
            realization_profile.get("allowed_scheduling_operations", [])
        )
        if not requested_operations:
            raise ContractError("at least one explicit runtime operation is required")
        undeclared_operations = set(requested_operations) - allowed_operations
        if undeclared_operations:
            raise ContractError(
                f"runtime operations are not allowed by profile: {sorted(undeclared_operations)}"
            )
        module = importer("pygrc")
        version = version_reader("pygrc")
        observed_identity = f"pygrc=={version}"
        surfaces = getattr(module, "PUBLIC_API_SURFACES", {})
        if not isinstance(surfaces, Mapping):
            raise ContractError("pygrc.PUBLIC_API_SURFACES is unavailable")
        observed_capabilities = sorted(str(item) for item in surfaces)
        if observed_identity != required_identity:
            raise ContractError(
                f"runtime identity mismatch: required {required_identity}, "
                f"observed {observed_identity}"
            )
        missing = required_capabilities - set(observed_capabilities)
        if missing:
            raise ContractError(f"runtime capabilities missing: {sorted(missing)}")
        conformance = "passed"
        failure_rationale = "binding conformance passed"
    except ContractError as exc:
        failure_rationale = str(exc)
    except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
        failure_rationale = f"{type(exc).__name__}: PyGRC runtime unavailable"
    except Exception as exc:  # a receipt is required even for unexpected binding failure
        failure_rationale = f"{type(exc).__name__}: PyGRC binding failed"

    receipt_payload = {
        "receipt_id": deterministic_id(
            "runtime-receipt",
            {
                "run_id": run_id,
                "profile_id": realization_profile.get("profile_id"),
                "execution_class": execution_class,
                "requested_operations": list(requested_operations),
            },
        ),
        "run_id": run_id,
        "execution_class": execution_class,
        "profile_id": realization_profile.get("profile_id"),
        "observed_runtime_identity": observed_identity,
        "observed_capabilities": observed_capabilities,
        "conformance_status": conformance,
        "before_state_identity": "binding-check:not-started",
        "after_state_identity": "binding-check:not-started",
        "requested_operations": list(requested_operations),
        "transition_receipt_ids": [],
        "failure": {
            "status": "not_applicable" if conformance == "passed" else "applicable",
            "rationale": failure_rationale,
        },
        "graph_repository_write_observed": False,
        "extensions": {},
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "record_type": "runtime_binding_receipt",
        "record": canonicalize_json_value(receipt_payload),
    }


def build_artifact_inspection_receipt(*, run_id: str) -> dict[str, Any]:
    payload = {
        "receipt_id": deterministic_id(
            "artifact-inspection-receipt", {"run_id": run_id}
        ),
        "run_id": run_id,
        "execution_class": "artifact_inspection",
        "conformance_status": "not_applicable_non_runtime",
        "failure": {
            "status": "not_applicable",
            "rationale": "artifact inspection requested no live runtime",
        },
        "graph_repository_write_observed": False,
        "extensions": {},
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "record_type": "runtime_binding_receipt",
        "record": payload,
    }


def build_artifact_manifest(
    *,
    manifest_id: str,
    profile_registry: Mapping[str, Any],
    declarations: Sequence[Mapping[str, Any]],
    repository_root: Path,
    source_revisions: Mapping[str, str],
    resolved_realization_profiles: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Materialize a verified manifest from declared artifact files."""

    profiles = _profile_map(profile_registry)
    artifact_entries: list[dict[str, Any]] = []
    total_size = 0
    for declaration in declarations:
        relative = validate_portable_path(str(declaration["expected_path"]))
        path = repository_root / relative
        if not path.is_file():
            raise ContractError(f"declared artifact does not exist: {relative}")
        size = path.stat().st_size
        total_size += size
        size_review_required = size > INDIVIDUAL_RETENTION_REVIEW_BYTES
        artifact_entries.append(
            canonicalize_json_value(
                {
                    "artifact_id": declaration["artifact_id"],
                    "expected_path": relative,
                    "command_profile_ref": declaration["command_profile_ref"],
                    "working_directory": declaration.get("working_directory", "."),
                    "environment_profile_ref": declaration["environment_profile_ref"],
                    "dependency_profile_ref": declaration["dependency_profile_ref"],
                    "source_revisions": dict(source_revisions),
                    "configuration_id": declaration["configuration_id"],
                    "input_digests": dict(declaration.get("input_digests", {})),
                    "random_seeds": list(declaration.get("random_seeds", [])),
                    "execution_class": declaration["execution_class"],
                    "realization_profile": deepcopy(declaration["realization_profile"]),
                    "artifact_kind": declaration["artifact_kind"],
                    "schema_version": declaration["schema_version"],
                    "expected_output_digest": semantic_file_digest(path),
                    "expected_file_sha256": digest_file(path),
                    "expected_size_bytes": size,
                    "retention_mode": declaration["retention_mode"],
                    "size_review": {
                        "status": "applicable" if size_review_required else "not_applicable",
                        "rationale": (
                            "individual artifact exceeds retention review threshold"
                            if size_review_required
                            else "individual artifact is below retention review threshold"
                        ),
                    },
                    "resource_profile_ref": declaration["resource_profile_ref"],
                    "verification_command_profile_ref": declaration[
                        "verification_command_profile_ref"
                    ],
                    "last_verified_status": "passed",
                    "evidence_use_tier": declaration["evidence_use_tier"],
                    "claim_dependency_refs": list(
                        declaration.get("claim_dependency_refs", [])
                    ),
                    "extensions": {},
                }
            )
        )
    resolved_profiles = [profiles[key] for key in sorted(profiles)]
    set_review_required = total_size > SET_RETENTION_REVIEW_BYTES
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "artifact_manifest",
        "record": {
            "manifest_id": manifest_id,
            "experiment_id": "AE01",
            "profile_registry_ref": profile_registry.get("record", profile_registry).get(
                "profile_registry_id"
            ),
            "artifacts": artifact_entries,
            "fully_resolved": True,
            "resolved_shared_profiles": resolved_profiles,
            "resolved_realization_profiles": [
                item.get("record", item) for item in resolved_realization_profiles
            ],
            "artifact_set_size_bytes": total_size,
            "retention_review": {
                "status": "applicable" if set_review_required else "not_applicable",
                "rationale": (
                    "artifact set exceeds retention review threshold"
                    if set_review_required
                    else "artifact set is below retention review threshold"
                ),
            },
            "extensions": {},
        },
    }
    validate_semantics(manifest)
    return canonicalize_json_value(manifest)


def assemble_report(
    projection: Mapping[str, Any], *, authored_markdown: str = ""
) -> str:
    """Deterministically assemble generated facts and bounded interpretation."""

    payload = projection.get("record", projection)
    mode = payload.get("mode")
    if mode == "generated_projection" and authored_markdown.strip():
        raise ContractError("generated projection cannot accept authored interpretation")
    for blocked in payload.get("blocked_statements", []):
        if blocked.casefold() in authored_markdown.casefold():
            raise ContractError(f"authored interpretation contains blocked statement: {blocked}")
    lines = [f"# {payload.get('report_id')}", "", "## Generated facts", ""]
    lines.extend(f"- {fact}" for fact in payload.get("facts_projection", []))
    if mode == "assembled_interpretation":
        lines.extend(["", "## Authored interpretation", "", authored_markdown.strip()])
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            f"Controlling claim boundary: `{payload.get('claim_boundary_ref')}`.",
            "",
        ]
    )
    return "\n".join(lines)


def _tree_fingerprint(root: Path) -> str:
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if relative == ".git" or relative.startswith(".git/"):
            continue
        if path.is_symlink():
            entries.append({"path": relative, "symlink": os.readlink(path)})
        elif path.is_file():
            entries.append(
                {"path": relative, "size": path.stat().st_size, "sha256": digest_file(path)}
            )
    return digest_canonical_data(entries)


class ReadOnlyTreeGuard(AbstractContextManager["ReadOnlyTreeGuard"]):
    """Detect any worktree file mutation across an RCAE live operation."""

    def __init__(self, root: Path):
        self.root = root
        self.before = ""

    def __enter__(self) -> "ReadOnlyTreeGuard":
        if not self.root.is_dir():
            raise ContractError("read-only source root does not exist")
        self.before = _tree_fingerprint(self.root)
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> bool:
        after = _tree_fingerprint(self.root)
        if after != self.before:
            raise ContractError("read-only source tree changed during operation")
        return False
