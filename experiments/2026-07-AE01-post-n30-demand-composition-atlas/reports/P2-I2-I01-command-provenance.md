# P2-I2-I01 Command Provenance

**Iteration:** `P2-I2-I01`

**Status:** complete historical command provenance; corrected by
`P2-I2-I01R1`

**Audit target:** clean `graph-reflexive-coherence` checkout at
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`

**Evidence effect:** audit mechanics and public-capability conformance only;
not source admission, calibration, a control outcome, or an L02 result. The
custom probe in Section 4 is candidate-shaped and quarantined from capability
and scientific evidence by I01R1.

The audit followed the frozen command boundary in
[the I01 input freeze](../contracts/p2-i2/i01-audit-input-freeze.json). `${GRC}`
below denotes the logical sibling checkout `${GRC}`.

## 1. Identity and scope commands

| ID | Exact command | Exit/result |
| --- | --- | --- |
| `CMD-001` | `git -C ${GRC} rev-parse HEAD` | `0`; frozen revision returned |
| `CMD-002` | `git -C ${GRC} branch --show-current` | `0`; `main` observed |
| `CMD-003` | `git -C ${GRC} status --short` | `0`; empty output / clean |
| `CMD-004` | `git -C ${GRC} ls-files pyproject.toml setup.py setup.cfg 'pygrc/**' 'implementation/**/pygrc/**' 'tests/**' 'docs/**' 'examples/**' 'implementation/Phase-8-LGRC9-RestorationIdentityCloseout.json'` | `0`; packaging manifest, tests, docs, examples, and closeout enumerated |
| `CMD-005` | `sed -n '1,240p' ${GRC}/pyproject.toml` | `0`; discovered `package-dir = { "" = "src" }` |
| `CMD-006` | `git -C ${GRC} ls-files 'src/pygrc/**'` | `0`; executed only after `P2-I2-CHG-002` added the manifest-declared package root |

`CMD-005` was the only source-like read before the scope correction. It was
already inside the original packaging-manifest scope. No `src/pygrc` source was
read and no capability was classified before `P2-I2-CHG-002` was recorded.

## 2. Static inspection commands

The material public-surface reads were:

```bash
sed -n '1,260p' ${GRC}/src/pygrc/models/__init__.py
sed -n '1,260p' ${GRC}/src/pygrc/models/lgrc_9_v3.py
sed -n '1,300p' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime_state.py
rg -n '^class LGRC9V3|^    def [^_]' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime.py
sed -n '1980,2245p' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime.py
sed -n '630,850p' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime_state.py
sed -n '38,184p' ${GRC}/src/pygrc/models/lgrc_9_v3_packets.py
sed -n '620,745p' ${GRC}/src/pygrc/models/lgrc_9_v3_packets.py
sed -n '1260,1555p' ${GRC}/src/pygrc/models/lgrc_9_v3_packets.py
sed -n '1680,1895p' ${GRC}/src/pygrc/models/lgrc_9_v3_packets.py
sed -n '5240,5408p' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime.py
sed -n '6350,7365p' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime.py
sed -n '7710,8145p' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime.py
sed -n '8630,8750p' ${GRC}/src/pygrc/models/lgrc_9_v3_runtime.py
sed -n '270,455p' ${GRC}/src/pygrc/models/lgrc_9_v3_restoration.py
sed -n '1,280p' ${GRC}/implementation/Phase-8-LGRC9-RestorationIdentityCloseout.json
sed -n '1,260p' ${GRC}/src/pygrc/models/grc_9_v3_state.py
sed -n '250,380p' ${GRC}/docs/reference/LGRC9V3-CausalHistory-ReferenceGuide.md
sed -n '540,635p' ${GRC}/docs/reference/LGRC9V3-CausalHistory-ReferenceGuide.md
sed -n '980,1080p' ${GRC}/docs/reference/LGRC9V3-CausalHistory-ReferenceGuide.md
```

Targeted discovery used `rg -n` over only the frozen `src/pygrc`, tracked test,
example, documentation, and closeout scopes for these terms and definitions:

```text
pool shared common carrier reserve accumulation mixing depletion saturation
leakage maintenance freeze clamp partition contributor source lineage history
snapshot restoration digest eligibility susceptibility capacity support surface
class/def declarations; public LGRC9V3 methods; restoration exports; feedback,
packet, arrival, route, lineage, and snapshot tests
```

All static-inspection commands exited `0`. Broad discovery output was used only
to locate the smaller cited reads. The retained source facts and digests are in
[the capability matrix](../contracts/p2-i2/i01-capability-matrix.json) and
[source-digest inventory](../contracts/p2-i2/i01-source-digests.json).

## 3. Dynamic-probe infrastructure attempts

The first attempts did not reach a PyGRC capability check:

| ID | Exact command | Exit/result |
| --- | --- | --- |
| `CMD-007` | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=${GRC}/src python -B ${TMPDIR}/p2_i2_i01_native_pool_probe.py` | `1`; ambient Python lacked declared dependency `matplotlib` |
| `CMD-008` | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=${GRC}/src ./venv/bin/python -B ${TMPDIR}/p2_i2_i01_native_pool_probe.py` | `127`; no RCAE `./venv/bin/python` |
| `CMD-009` | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=${GRC}/src uv run --project ${GRC} --no-sync python -B ${TMPDIR}/p2_i2_i01_native_pool_probe.py` | `127`; `uv` unavailable |
| `CMD-010` | `test -x ${GRC}/.venv/bin/python` | `0`; existing graph-project interpreter available |

These failures are infrastructure observations only. No installed-package fact
was merged into the checkout audit, no package was installed, and no network
or graph-repository mutation was attempted.

## 4. Quarantined candidate-shaped native-composition probe

**I01R1 admissibility:** excluded from capability and scientific evidence.

This custom probe instantiated a multi-source common-carrier chain and compared
combined, single-source, and label-permuted response behavior. That exceeds the
I01 interface-conformance boundary. The source, hash, command, and outputs are
retained below only so the process defect and executed activity remain fully
reconstructible. No corrected capability-matrix row cites this probe.

The successful exact command was:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=${GRC}/src \
${GRC}/.venv/bin/python -B ${TMPDIR}/p2_i2_i01_native_pool_probe.py
```

It exited `0` and recorded the imported model facade as:

```text
${GRC}/src/pygrc/models/__init__.py
```

The final probe source SHA-256 was
`f6a421e3b3190a9c6b164b1baecde350085d188746f73ce2912ad4b97bb10384`.
Its full source is retained here because the executed file existed only under
`${TMPDIR}`:

```python
from __future__ import annotations

import json

from pygrc import core, models


def build_model() -> models.LGRC9V3:
    graph = core.PortGraphBackend()
    source_a = graph.add_node({"role": "source_a"})
    source_b = graph.add_node({"role": "source_b"})
    pool = graph.add_node({"role": "pool"})
    response = graph.add_node({"role": "response"})
    reference = graph.add_node({"role": "reference"})
    edge_a = graph.connect_ports(source_a, 0, pool, 0, {"role": "a_to_pool"})
    edge_b = graph.connect_ports(source_b, 0, pool, 1, {"role": "b_to_pool"})
    edge_y = graph.connect_ports(pool, 2, response, 0, {"role": "pool_to_response"})
    state = models.GRC9V3State(
        topology=graph,
        nodes={
            source_a: models.GRC9V3NodeState(coherence=1.0),
            source_b: models.GRC9V3NodeState(coherence=1.0),
            pool: models.GRC9V3NodeState(coherence=0.2),
            response: models.GRC9V3NodeState(coherence=1.0),
            reference: models.GRC9V3NodeState(coherence=0.1),
        },
        port_edges={
            edge_a: models.PortEdge(source_a, 1, pool, 1, conductance=1.0, flux_uv=0.0),
            edge_b: models.PortEdge(source_b, 1, pool, 2, conductance=1.0, flux_uv=0.0),
            edge_y: models.PortEdge(pool, 3, response, 1, conductance=1.0, flux_uv=0.0),
        },
        base_conductance={edge_a: 1.0, edge_b: 1.0, edge_y: 1.0},
        geometric_length={edge_a: 1.0, edge_b: 1.0, edge_y: 1.0},
        temporal_delay={edge_a: 1.0, edge_b: 1.0, edge_y: 1.0},
        flux_coupling={edge_a: 0.0, edge_b: 0.0, edge_y: 0.0},
    )
    params = {
        "dt": 1.0,
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
    return models.LGRC9V3.from_state(state, params)


def run_case(contributions: tuple[tuple[int, float, str], ...]) -> dict[str, object]:
    model = build_model()
    for packet_index, (source, amount, lineage) in enumerate(contributions):
        model.schedule_packet_departure(
            source_node_id=source,
            target_node_id=2,
            edge_id=source,
            amount=amount,
            departure_event_time_key=1.0 + (0.1 * packet_index),
            arrival_event_time_key=2.0 + (0.1 * packet_index),
            scheduler_event_index=1 + packet_index,
            packet_index=packet_index,
            source_lineage_id=lineage,
            target_lineage_id="pool-lineage",
        )
    model.run_event_queue(max_events=2 * len(contributions))
    pool_after_contributions = model.get_state().base_state.nodes[2].coherence
    row = model.emit_feedback_eligibility_surface_row(
        front_node_ids=(2,),
        rear_node_ids=(4,),
        feedback_threshold=0.5,
    )
    model.set_feedback_coupled_pulse_producer(
        source_node_id=2,
        target_node_id=3,
        edge_id=2,
        threshold=0.5,
        packet_amount=0.1,
        expected_polarity="positive",
    )
    production = model.produce_events(
        policy=(
            models.LGRC9V3_AUTONOMOUS_PRODUCER_POLICY_PACKET_DEPARTURE_FROM_FEEDBACK_ELIGIBILITY
        )
    )
    if production.scheduled_event_count:
        model.run_event_queue(max_events=2)
    state = model.get_state()
    identity = models.lgrc9v3_restoration_identity_v1(model)
    return {
        "pool_after_contributions": pool_after_contributions,
        "boundary_polarity_score": row.surface_values_after[
            "boundary_polarity_score"
        ],
        "scheduled_event_count": production.scheduled_event_count,
        "producer_reason": production.production_records[0].reason_code,
        "response_coherence": state.base_state.nodes[3].coherence,
        "pool_after_response": state.base_state.nodes[2].coherence,
        "source_lineage_ids": [
            packet.source_lineage_id
            for packet in sorted(
                (
                    packet
                    for packet in state.packet_ledger.packet_records
                    if packet.target_node_id == 2
                ),
                key=lambda packet: packet.source_node_id,
            )
        ],
        "restoration_kind": identity["artifact_kind"],
        "restoration_digest": models.digest_lgrc9v3_restoration_identity_v1(model),
    }


combined_ab = run_case(((0, 0.2, "alpha"), (1, 0.3, "beta")))
combined_ba = run_case(((0, 0.2, "beta"), (1, 0.3, "alpha")))
single_a = run_case(((0, 0.2, "alpha"),))
single_b = run_case(((1, 0.3, "beta"),))

causal_keys = (
    "pool_after_contributions",
    "boundary_polarity_score",
    "scheduled_event_count",
    "producer_reason",
    "response_coherence",
    "pool_after_response",
)
result = {
    "probe_kind": "P2-I2-I01 audit-only native composition conformance",
    "module_file": models.__file__,
    "combined_ab": combined_ab,
    "combined_ba": combined_ba,
    "single_a": single_a,
    "single_b": single_b,
    "label_permutation_causal_projection_equal": all(
        combined_ab[key] == combined_ba[key] for key in causal_keys
    ),
    "label_permutation_identity_differs": (
        combined_ab["restoration_digest"] != combined_ba["restoration_digest"]
    ),
    "combined_only_schedules_response": (
        combined_ab["scheduled_event_count"] == 1
        and single_a["scheduled_event_count"] == 0
        and single_b["scheduled_event_count"] == 0
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
```

Compact successful output:

```text
combined pool after contributions = 0.7
combined boundary-polarity score = 0.6
combined scheduled response = 1
single-A score = 0.30000000000000004; scheduled response = 0
single-B score = 0.4; scheduled response = 0
label-permutation causal projection equal = true
label-permutation restoration identity differs = true
combined-only response = true
restoration artifact kind = lgrc9v3_restoration_identity
```

The historical differing restoration digests reflected the probe inputs. No
causal, adequacy, control, or restoration judgment is carried forward from
this output.

## 5. Focused source-current tests

Exact command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=${GRC}/src \
${GRC}/.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=${TMPDIR}/p2-i2-i01-pytest \
  tests/models/test_lgrc_9_v3_restoration.py \
  tests/models/test_lgrc_9_v3_restoration_matrix.py \
  tests/models/test_lgrc_9_v3_runtime.py::LGRC9V3RuntimeTest::test_departure_arrival_lifecycle_preserves_budget \
  tests/models/test_lgrc_9_v3_runtime.py::LGRC9V3RuntimeTest::test_feedback_surface_and_producer_schedule_via_packet_queue_only \
  tests/models/test_lgrc_9_v3_runtime.py::LGRC9V3RuntimeTest::test_feedback_coupled_pulse_subthreshold_and_wrong_polarity_are_negative \
  tests/models/test_lgrc_9_v3_runtime.py::LGRC9V3RuntimeTest::test_arrival_local_update_can_schedule_outbound_causal_flux \
  tests/models/test_lgrc_9_v3_runtime.py::LGRC9V3RuntimeTest::test_native_runtime_snapshot_load_preserves_queue_and_continuation \
  tests/models/test_lgrc_9_v3_runtime.py::LGRC9V3RuntimeTest::test_snapshot_serializes_runtime_queue_and_events
```

Result:

```text
38 passed, 8 subtests passed in 2.66s
```

The graph checkout remained read-only; cache creation was disabled and test
temporaries were directed to `${TMPDIR}`. I01R1 classifies these pre-existing
generic PyGRC tests as admissible interface/restoration conformance; they do
not instantiate a P2-I2 multi-source candidate fixture.

## 6. Digest and closure commands

I01 originally ran `sha256sum` over fifteen tracked files listed in
[the source-digest inventory](../contracts/p2-i2/i01-source-digests.json) and
the `${TMPDIR}` probe source. I01R1 added exact digests for the in-scope public
causal-history implementation and its contract test, bringing the corrected
inventory to seventeen tracked files. Final closure repeated:

```bash
git -C ${GRC} rev-parse HEAD
git -C ${GRC} status --short
```

The revision remained
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`; status output remained empty.

## 7. I01R1 closeout-revalidation commands

I01R1 executed no dynamic probe and did not rerun candidate-shaped behavior.
It used read-only source/package checks under the already frozen `src/pygrc`,
tracked tests/docs/examples, and closeout scope. Material added reads were:

```bash
sed -n '250,470p' ${GRC}/src/pygrc/models/lgrc_9_v3_restoration.py
sed -n '620,1095p' ${GRC}/src/pygrc/models/lgrc_9_v3_timing.py
rg -n 'lgrc9v3_restoration_identity_v1|digest_lgrc9v3_restoration_identity_v1' \
  ${GRC}/src/pygrc/models/__init__.py \
  ${GRC}/src/pygrc/models/lgrc_9_v3_restoration.py \
  ${GRC}/tests/models/test_lgrc_9_v3_restoration.py \
  ${GRC}/tests/models/test_lgrc_9_v3_restoration_matrix.py
rg -n 'annotate_lgrc9v3_causal_history|build_lgrc9v3_causal_history_artifact|attach_lgrc9v3_causal_history_artifact|extract_lgrc9v3_causal_history_artifact' \
  ${GRC}/src/pygrc/models/__init__.py \
  ${GRC}/src/pygrc/models/lgrc_9_v3_runtime.py \
  ${GRC}/src/pygrc/models/lgrc_9_v3_runtime_state.py \
  ${GRC}/tests/models/test_lgrc_9_v3_contract.py \
  ${GRC}/docs/reference/LGRC9V3-CausalHistory-ReferenceGuide.md
rg -n '^    def [a-zA-Z0-9_]*(pool|clamp|freeze|partition|shuffle|history)|^def [a-zA-Z0-9_]*(pool|clamp|freeze|partition|shuffle|history)|pool_write|pool_specific|private_partition|history_clamp|history_shuffle' \
  ${GRC}/src/pygrc ${GRC}/tests ${GRC}/docs ${GRC}/examples
sha256sum \
  ${GRC}/src/pygrc/models/lgrc_9_v3_timing.py \
  ${GRC}/tests/models/test_lgrc_9_v3_contract.py
git -C ${GRC} rev-parse HEAD
git -C ${GRC} status --short
```

Dependency-free local validators then parsed all P2-I2 JSON, verified the
eleven unique CAP IDs and required fields, resolved every repository-relative
matrix source/callable reference, recomputed every source digest, checked that
no surviving matrix row cited the quarantined probe, validated local Markdown
links, and ran `git diff --check`. The exact outcomes are retained in the
[I01R1 report](P2-I2-I01R1-capability-audit-closeout-revalidation.md).

## I05H portability projection

This is a representation-only projection under `P2-I2-DEC-038` and
`P2-I2-CHG-031`. Historical commands are non-executable provenance. Raw bytes
remain at commit `62882efc5ecf3c131d21345ad89796f0b2ebccb7`, SHA-256
`f30cb5cf99e9088cc8f669b716b1481fd6d55022179bdd6fc6c4dd80fe2185af`.
No capability or scientific meaning changed.
