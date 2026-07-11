# P2-I1 C01 Bounded-Incomplete Execution Record

**Status:** retained operational result; no scientific result

**Cycle:** `P2-I1-C01`

**Execution authority:** tracked `P2-I1-EXEC-FREEZE` retained in `fff1690`

**Frozen source revision:**
`606bc2714bce5c6086e0c92ea363a070481b0ca8`

**Graph source revision:**
`1f42cb1d1e591159afc2ca54cc656b574d41c8d3`

**Evidence effect:** control and integrity only

## 1. What executed

After tracked EXEC-FREEZE validation passed, the runner attempted the exact
frozen matrix:

```text
7 cells x 3 seeds = 21 primary attempts
1 deterministic infrastructure retry per cell at its lowest failed seed
scientific configuration changes = 0
fallbacks = 0
graph writes = 0
```

The exact command was:

```bash
.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py \
  run-cycle \
  --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/exec-freeze.json \
  --graph-root ../graph-reflexive-coherence \
  --summary-output outputs/p2-i1-c01-execution-summary.json
```

Every primary reached native W2 save/load and stopped before producer
invocation with the same diagnostic:

```text
C01 branch restoration differs from W2 snapshot
```

The frozen retry ledger then authorized seed 101 once in each cell. All seven
retries stopped at the same boundary and diagnostic. C01 has therefore used
its complete declared attempt scope and cannot be rerun.

## 2. Retained machine evidence

| Artifact | Canonical payload digest | Exact-file SHA-256 |
| --- | --- | --- |
| [Retry ledger](../contracts/p2-i1/c01/retry-ledger.json) | `cacaffa051e1d5fb613e063831eb6178a71cbc9c29c913db9917ed3073caaf0d` | `8ea6c323857db5ac58bb7d4a46945d25f285520e747f2491383a674eac4b43fe` |
| [Cycle audit](../contracts/p2-i1/c01/cycle-audit.json) | `763bb080470290b4aebe8f05fa9f680385cdaa97a587e123ea7339f269941b28` | `1073b28c3c60741b2196f9d80c42ab66d6c669f4c364d38eec0ccb316585b123` |

The ledger records:

```text
primary failures = 21
retry authorizations = 7
retry failures = 7
unique diagnostic digests = 1
diagnostic digest = cafffec3f98ecdcb1a2070c0e5f383cf3e5586a86cbf1a7c8671a68784f17e15
candidate scientific effect = none_operational_only
```

The audit records:

```text
effective runs = 0
missing frozen run IDs = 21
blocked-or-incomplete live obligations = 12
audit complete = false
candidate outcomes present = false
scientific rung assigned = false
terminal classification opened = false
```

Regenerate the audit from the retained retry ledger and absent run paths with:

```bash
.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py \
  build-cycle-audit \
  --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/exec-freeze.json \
  --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c01/cycle-audit.json
```

Run that reconstruction at the C01 result commit or its declared source state;
later successor decisions intentionally change the current authority digest.

The complete 88-test suite passes in the clean C01 reconstruction clone. When
the same suite is invoked in the post-execution checkout, five freeze-builder
tests stop at the intentional `candidate outcomes must be absent at freeze`
guard because the C01 audit and retry ledger now exist at their frozen paths.
This is not a failed scientific control or a C01 source regression. It exposes
a test-isolation requirement for C02: freeze-construction tests must use
temporary result paths or an injected absence predicate rather than depending
on the repository never having executed a cycle.

## 3. Bounded failure diagnosis

A source-current native round-trip comparison reproduced the failing reference
branch at W2 and recursively compared `model.snapshot()` before save with
`LGRC9V3.load(...).snapshot()` after load. It found six differing leaves, all
inside `caches.base_grc9v3_snapshot`:

| Cached field | Before save | After native load | Observed relation |
| --- | --- | --- | --- |
| `dynamics.state.cached_quantities.budget_target_source` | absent | `explicit_state` | default materialized |
| `dynamics.state.params_identity` | `null` | resolved digest | identity materialized |
| `dynamics.state.port_edges.1.node_u` | `1` | `0` | undirected endpoints canonicalized |
| `dynamics.state.port_edges.1.node_v` | `0` | `1` | undirected endpoints canonicalized |
| `dynamics.state.rng_state` | `null` | deterministic Python RNG state | state materialized |
| `metadata.rng_state` | absent | deterministic Python RNG state | metadata materialized |

The following compared equal:

- the complete native `dynamics.lgrc9v3_runtime` artifact;
- outer topology, basin attributes, and edge labels;
- event history and observables; and
- the independently reconstructed feedback-medium projection.

This diagnosis is narrower than a claim that native restoration is fully
equivalent under all continuations. It establishes that C01's failing predicate
included cached representation details not changed by its scientific design.
C02 must additionally test equal continuation from independently restored
branches before the correction can pass its execution gate.

## 4. Why C02 is required

C01 cannot be patched or retried because its frozen attempt scope is exhausted.
The failure exposed a new experiment-side choice about which native state owns
branch-restoration identity. That choice is not a threshold adjustment and
does not alter the niche hypothesis, fixture, cells, seeds, metrics, or claim
ceiling.

Accepted `P2-I1-DEC-027` assigns restoration identity to a declared projection:

```text
outer geometry
+ exact native LGRC runtime artifact
+ event and observable state
+ separately verified medium reconstruction
```

Full raw snapshot digests remain observations, while the nested cached base
snapshot no longer controls equality. C02 must be separately implemented,
tested, source-anchored, bound, and frozen. Any projected-state difference or
equal-input continuation divergence fails closed and may reopen the native
runtime question. No PyGRC change, state injection, or fallback is authorized.

## 5. Disposition

```text
P2-I1-C01 = bounded_incomplete_operational
scientific result = none
retry budget = exhausted
successor = P2-I1-C02
successor reason = correct an over-broad RCAE restoration predicate under D-027
```
