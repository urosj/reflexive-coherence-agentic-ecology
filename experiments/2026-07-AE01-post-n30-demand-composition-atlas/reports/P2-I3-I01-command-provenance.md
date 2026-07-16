# P2-I3 I01 Command Provenance

**Status:** accepted as I01 provenance through `P2-I3-DEC-018`

**Iteration:** `P2-I3-I01`

**Working directory:** RCAE repository root

**Mutation boundary:** external checkouts read-only; retained files written
only in this repository; temporary test state directed to `${TMPDIR}`

## 1. Environment resolution

The initial preflight found `.venv/bin/python` present with Python 3.12.3 and
the declared PyGRC runtime dependencies present, but pytest absent. No audit
test ran in that state.

The project owner authorized:

```text
uv pip install --python .venv/bin/python pytest
```

The first sandboxed invocation could not access the uv cache. The same command
was rerun with the approved package-install permission and resolved:

```text
pytest==9.1.1
iniconfig==2.3.0
pluggy==1.6.0
```

No package was installed into either external checkout.

The successful environment verification was:

```text
test -x .venv/bin/python
.venv/bin/python --version
.venv/bin/python -B -c '<importlib.metadata version check>'
.venv/bin/python -B -m pytest --version
```

Recorded package identities:

```text
Python=3.12.3
matplotlib=3.11.0
networkx=3.6.1
pyvis=0.3.2
PyYAML=6.0.3
jsonschema=4.26.0
pytest=9.1.1
iniconfig=2.3.0
pluggy=1.6.0
```

The graph checkout declares Python `>=3.11`, `matplotlib>=3.8`,
`networkx>=3.2`, `pyvis>=0.3.2`, and `PyYAML>=6.0`. It does not declare a
pytest pin. The audit therefore records the exact resolved pytest identity
rather than inventing an upstream requirement.

## 2. Checkout identity and cleanliness

These commands ran before and after audit activity:

```text
git -C ../graph-reflexive-coherence rev-parse HEAD
git -C ../graph-reflexive-coherence branch --show-current
git -C ../graph-reflexive-coherence status --short
git -C ../geometric-reflexive-coherence rev-parse HEAD
git -C ../geometric-reflexive-coherence branch --show-current
git -C ../geometric-reflexive-coherence status --short
```

Results were unchanged:

```text
graph revision: 83e3a300426631ee4df71b661b67d4fcfdfed594
graph branch: main
graph worktree: clean
theory revision: e0d25bf69b8bf681eb8d092ba416497030e5d88e
theory branch: main
theory worktree: clean
```

## 3. Static source inspection

The audit used only frozen path scopes. Principal exact command forms were:

```text
git -C ../graph-reflexive-coherence show HEAD:pyproject.toml
git -C ../graph-reflexive-coherence ls-files \
  'src/pygrc/models/grc_9_v3*.py' \
  'src/pygrc/models/lgrc_9_v3*.py' \
  'tests/models/test_lgrc_9_v3*.py' \
  'examples/lgrc9v3/**' \
  'implementation/Phase-8*'
rg -n '^(class|def) |^    (def|@property)' \
  ../graph-reflexive-coherence/src/pygrc/models/lgrc_9_v3*.py \
  ../graph-reflexive-coherence/src/pygrc/models/grc_9_v3*.py
rg -n 'decay|leak|saturat|reinforc|withdraw|maintain|relocat|shuffle|clamp|false.trace|field' \
  ../graph-reflexive-coherence/src/pygrc/models/lgrc_9_v3*.py \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3*.py \
  ../graph-reflexive-coherence/implementation/Phase-8-LGRC9-*.md
rg -n '^    def test_.*(packet|arrival|departure|surface|feedback|route|proper_time|distance|snapshot|save|load|reset|restore|rebase)' \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3*.py \
  ../graph-reflexive-coherence/tests/models/test_grc_9_v3*.py
rg -n '^#|distance|proper time|causal|geometric|functional|influence|route|path|field|history|dynamic' \
  ../geometric-reflexive-coherence/investigations/2026-01-RC-Distance-v4.md
```

`sed -n` was then used over the frozen files to inspect the cited definitions,
docstrings, validation branches, serialization fields, and test bodies. No
command wrote into an external checkout.

The source digest command used exactly the 27 paths retained in
[the source inventory](../contracts/p2-i3/i01-source-digests.json):

```text
sha256sum <each retained frozen source path>
```

### 3.1 Owner-directed experiment-lineage extensions

After the source/public-interface audit, the owner directed a thorough N29/N30
inspection and clarified that N29 indexes earlier experiments. Read-only
`rg`, `sed`, and `sha256sum` inspection therefore followed the relevant
mechanism lineage through:

```text
N05, N06, N07, N08, N09, N10, N11,
N22, N25.2, N28, N29, and N30
```

The expansion did not execute an experiment, import a candidate fixture, or
change either external checkout. It retained:

- 32 exact N29/N30 source identities in
  `i01-n29-n30-mechanism-inventory.json`; and
- 44 exact predecessor source identities in
  `i01-predecessor-mechanism-lineage.json`.

The principal search and inspection forms were:

```text
rg --files ../graph-reflexive-coherence/experiments/<experiment>
rg -n '<mechanism terms>' ../graph-reflexive-coherence/experiments/<experiment>
sed -n '<bounded ranges>' ../graph-reflexive-coherence/experiments/<file>
sha256sum ../graph-reflexive-coherence/experiments/<exact retained file>
```

No earlier experiment test or runtime command was rerun. Its retained script,
report, and output relations were classified as source facts about that
experiment, never as fresh P2-I3 execution or native-capability upgrades.

## 4. Public import and callable introspection

The public introspection used the checkout directly, disabled bytecode, and
printed only checkout-relative module identities:

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../graph-reflexive-coherence/src \
.venv/bin/python -B -c '<read-only inspect.signature program>'
```

The program imported:

```text
pygrc
pygrc.models
pygrc.models.lgrc_9_v3_runtime
pygrc.models.lgrc_9_v3_timing
```

It verified callable public identities and signatures for:

```text
GRC9V3
GRC9V3.apply_continuity
GRC9V3.step
LGRC9V3
LGRC9V3.schedule_packet_departure
LGRC9V3.step
LGRC9V3.get_state
LGRC9V3.set_state
LGRC9V3.snapshot
LGRC9V3.save
LGRC9V3.load
LGRC9V3.reset
LGRC9V3.rebase_reset_baseline
LGRC9V3.emit_feedback_eligibility_surface_row
LGRC9V3.set_feedback_coupled_pulse_producer
compute_lgrc9v3_geometric_distances
compute_lgrc9v3_functional_distances
compute_lgrc9v3_causal_distances
LGRC9V3CausalPulseSubstrateSurfaceRow
prime_lgrc9v3_packet_departures
transport_lgrc9v3_packets_through_refinement
lgrc9v3_restoration_identity_v1
lgrc9v3_restoration_identity_v2
LGRC9V3.process_causal_collapse_reabsorption
```

Resolved modules were the expected tracked checkout modules under
`graph-reflexive-coherence/src/pygrc/`. No ambient `pygrc` installation was
consumed. A bounded follow-up callable check confirmed the five additional
construction, topology, restoration, and collapse identities above after the
operation matrix was assembled; all resolved as public callables. A final
source-boundary check also confirmed that `GRC9V3.apply_continuity`,
`GRC9V3.step`, and `LGRC9V3.step` are distinct public callables and that the
two model families resolve from the expected checkout modules.

## 5. Pre-existing generic tests

All commands used checkout imports, disabled bytecode and pytest cache, and
directed temporary files to `${TMPDIR}`. The portable rendering below replaces
the machine-local temporary-directory value with that variable.

### CMD-TEST-01 — packet, distance, ordering, and surface contracts

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../graph-reflexive-coherence/src \
TMPDIR=${TMPDIR} \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3_contract.py \
  -k 'causal_pulse_substrate_surface_row_round_trips or lgrc2_multiple_packets_on_one_edge_have_deterministic_order or lgrc2_packet_ledger_orders_queue_events_deterministically or lgrc2_packet_departure_debits_source_and_adds_in_flight or lgrc2_packet_arrival_credits_target_and_removes_in_flight or lgrc2_departure_arrival_cycle_round_trips_and_preserves_budget or three_distance_surfaces_are_not_conflated'
```

Result: `7 passed, 127 deselected`.

### CMD-TEST-02 — live runtime and producer boundaries

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../graph-reflexive-coherence/src \
TMPDIR=${TMPDIR} \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3_runtime.py \
  -k 'departure_arrival_lifecycle_preserves_budget or enabled_pulse_substrate_surface_emits_after_committed_packet_event or pulse_substrate_surface_snapshot_round_trip_and_continuation or feedback_surface_and_producer_schedule_via_packet_queue_only or native_route_candidate_emission_rejects_hidden_route_selection or snapshot_serializes_runtime_queue_and_events or native_runtime_snapshot_load_preserves_queue_and_continuation'
```

Result: `7 passed, 163 deselected`.

### CMD-TEST-03 — restoration identity and sensitivity

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../graph-reflexive-coherence/src \
TMPDIR=${TMPDIR} \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3_restoration.py \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3_restoration_matrix.py \
  -k 'component_is_stable_across_native_load or public_identity_is_stable_across_native_load or composite_fixed_point_and_raw_digest_cycle_across_three_loads or lgrc_queue_clock_ledger_route_topology_and_producer_sensitivity or source_current_surface_mutation_changes_identity'
```

Result: `5 passed, 27 deselected`.

### CMD-TEST-04 — library-owned topology routes

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../graph-reflexive-coherence/src \
TMPDIR=${TMPDIR} \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3_construction.py \
  -k 'route_generation_and_broad_seed_priming_are_library_owned'
```

Result: `1 passed, 3 deselected`.

### CMD-TEST-05 — route-aspect conformance

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../graph-reflexive-coherence/src \
TMPDIR=${TMPDIR} \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3_native_packet_loop_route_aspect.py \
  -k 'route_aspect_validates_against_state_and_compiles_to_routes or broken_return_route_is_rejected or route_aspect_state_validation_rejects_bad_edge'
```

Result: `3 passed, 8 deselected`.

### CMD-TEST-06 — static route is not self-rearm equivalence

```text
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=../graph-reflexive-coherence/src \
TMPDIR=${TMPDIR} \
.venv/bin/python -B -m pytest -q -p no:cacheprovider \
  ../graph-reflexive-coherence/tests/models/test_lgrc_9_v3_native_packet_loop_baseline.py \
  -k 'existing_static_route_autonomy_is_not_d2_3_equivalent'
```

Result: `1 passed, 5 deselected`.

## 6. Aggregate result and quarantine

```text
test invocations: 6
passed: 24
deselected: 333
failed: 0
errors: 0
synthetic probes: 0
candidate executions: 0
external source writes: 0
```

These tests establish source-current interface conformance only. They do not
constitute P2-I3 candidate behavior, source admission, realization evidence,
calibration, or support/refutation of `AE01-H-L03`.
