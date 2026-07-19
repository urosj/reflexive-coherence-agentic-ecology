"""Mechanical provenance guard for quarantined P2-I3 conformance material.

The guard does not pretend it can recognize an unattributed copied number.
Instead, later record builders must retain declared provenance, and this guard
rejects the conformance namespace, artifact kinds, digests, value identities,
or provenance tags from every scientific consumer class.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any


CONFORMANCE_NAMESPACE = (
    "experiments/2026-07-AE01-post-n30-demand-composition-atlas/"
    "contracts/p2-i3/conformance/"
)
CONFORMANCE_ARTIFACT_PREFIX = "p2_i3_i03_br_conformance_"
CONFORMANCE_PROVENANCE_TAGS = frozenset(
    {
        "i03_conformance",
        "implementation_conformance",
        "synthetic_conformance_fixture",
        "conformance_only",
    }
)
FORBIDDEN_CONSUMER_CLASSES = frozenset(
    {
        "calibration_input",
        "calibration_output",
        "registration_value",
        "candidate_input",
        "candidate_output",
        "control_outcome",
        "scientific_result",
        "terminal_classification",
    }
)


class ConformanceQuarantineError(ValueError):
    """Raised when quarantined material enters a scientific consumer."""


def _walk(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield from _walk(child, f"{path}.{key}")
    elif isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def assert_no_conformance_import(
    payload: Any,
    *,
    consumer_class: str,
    blocked_output_digests: Iterable[str] = (),
    blocked_fixture_value_ids: Iterable[str] = (),
) -> None:
    """Reject declared conformance provenance from a scientific payload.

    Provenance-only gate references belong in authority metadata outside the
    scientific input/value/result payload passed to this function.
    """

    if consumer_class not in FORBIDDEN_CONSUMER_CLASSES:
        raise ConformanceQuarantineError(
            f"unknown or non-scientific consumer class: {consumer_class!r}"
        )
    blocked_digests = {str(value) for value in blocked_output_digests}
    blocked_value_ids = {str(value) for value in blocked_fixture_value_ids}
    failures: list[str] = []
    for path, value in _walk(payload):
        if not isinstance(value, str):
            continue
        normalized = value.strip()
        lowered = normalized.lower()
        if CONFORMANCE_NAMESPACE in normalized:
            failures.append(f"{path}:conformance_namespace")
        if CONFORMANCE_ARTIFACT_PREFIX in normalized:
            failures.append(f"{path}:conformance_artifact_kind")
        if lowered in CONFORMANCE_PROVENANCE_TAGS:
            failures.append(f"{path}:conformance_provenance")
        if "i03" in lowered and "conformance" in lowered:
            failures.append(f"{path}:conformance_reference")
        if normalized in blocked_digests:
            failures.append(f"{path}:conformance_output_digest")
        if normalized in blocked_value_ids:
            failures.append(f"{path}:conformance_fixture_value_id")
    if failures:
        raise ConformanceQuarantineError(
            f"{consumer_class} imports quarantined material: "
            + ", ".join(sorted(set(failures)))
        )


__all__ = [
    "CONFORMANCE_ARTIFACT_PREFIX",
    "CONFORMANCE_NAMESPACE",
    "CONFORMANCE_PROVENANCE_TAGS",
    "FORBIDDEN_CONSUMER_CLASSES",
    "ConformanceQuarantineError",
    "assert_no_conformance_import",
]
