# P2-I1 D-020 Bounded Refresh Verification Closeout

**Status:** complete

**Decision:** `P2-I1-DEC-020`

**Source anchor:** `1c9736dee165d44ed1d837f673f03a9a69bba113`

**Evidence effect:** none; identity correction only

## 1. Closeout scope

The D-020 semantic and source-policy change was reviewed and accepted before
commit. Everything after that review was deterministic retention work. Its
complete verification scope is:

1. verify the v2 runtime policy separates cycle-scoped
   `P2-I1-EXEC-FREEZE` authorization from post-execution
   `P2-I1-EXEC-GATE` closure;
2. verify the v2 identity explicitly supersedes v1 and anchors the reviewed
   clean source revision; and
3. verify that only the declared runtime/measurement identities changed while
   the calibration realization and all three calibration artifacts remained
   identical.

Controlling records:

- [D-020 decision](../implementation/P2-I1-decision-record.md#23-p2-i1-dec-020--candidate-execution-authorization-boundary)
- [v1 CAL-PRE identity](../contracts/p2-i1/cal-pre-identity.json)
- [v2 CAL-PRE identity](../contracts/p2-i1/cal-pre-identity-v2.json)
- [bounded-refresh freeze](../contracts/p2-i1/d020-bounded-refresh-freeze-v2.json)
- [runtime policy v2](../configs/p2_i1_runtime_policy.json)
- [P2-I1 checklist](../implementation/P2-I1-minimal-shared-medium-niche-checklist.md)

## 2. Required closeout checks

1. Does the runtime policy keep blanket candidate authorization false and
   require an exact active-cycle `EXEC-FREEZE` after CAL-GATE and REG-GATE?
2. Does it preserve `EXEC-GATE` exclusively as post-execution closure?
3. Does the v2 identity name v1 as its superseded identity, record the D-020
   reason, resolve to the clean source anchor, and remain candidate-free?
4. Are the runtime configuration, derived measurement identity, CLI source,
   and runtime-harness source the only declared changes?
5. Are fixture, cells, analysis, calibration, provenance, analysis code, and
   calibration-realization identities unchanged?
6. Are regenerated matched-null, metric-calibration, and frozen-sheet files
   byte-for-byte identical to the retained v1 files?
7. Did independent reconstruction reproduce the v2 identity and all three
   calibration artifacts without PyGRC or candidate input?

## 3. Identity comparison

| Identity | v1 | v2 | Expected |
| --- | --- | --- | --- |
| Runtime config | `0d3c70fef545ce0371448ef2637b7a2b265152b8769013dfe7e07a8925aa141a` | `85574006a8ebb912e2a211b9a591bda7d1a4bdff13c3ff330c7bf4228b355793` | changed |
| Measurement | `eff89329d93d2addd05c27e72706da59c6f96c7ad813dceb90452a37bc46fd70` | `853c5f10d33a1820b72cc3245e0612ff9024a7ae920833d44e81fcc22a7f2e5a` | changed |
| Calibration realization | `9b59988a0f5211cb32aaf531748f8a9b235540729d40544373e6ba3a04b769b8` | `9b59988a0f5211cb32aaf531748f8a9b235540729d40544373e6ba3a04b769b8` | identical |

Fixture, cells, analysis, calibration, and provenance configuration digests
are identical between versions. The pure analysis script digest is also
identical. CLI and runtime-harness digests changed because they enforce the
new policy fields and v2 identity chain.

## 4. Calibration artifact comparison

| Artifact | Semantic-file digest | Exact-file SHA-256 | v2 result |
| --- | --- | --- | --- |
| Matched null | `a9cbe5e7449091c3c6f6a395a9c8db5f8e3d05890b985975c97550e1572b9629` | `2188529b520466aabee5baa86750f1376ae5172d2be07b11192747f9e8c1cc2f` | byte-identical |
| Metric calibration | `8c734e4e43131842917e423170584cf53b8c657ed3302544d5805a29f645cde9` | `ebd6c62c8a5920c681b8e91810a4788e7dcd5591e98d0313a7225f0e63635e5a` | byte-identical |
| Frozen metric sheet | `68ed80f6455ec2e4ab8dc18d3a385d8d6bc9781483c90dbf1b1a9b3c5c80f043` | `fdd2a0d78140edbe6383661804c2928f5a1ae63ef501e1aed6ca296994514563` | byte-identical |

The v2 refresh therefore reuses the content-addressed retained calibration
artifacts. It does not duplicate or rewrite them.

## 5. Reconstruction

A fresh detached worktree at the source anchor, with
`jsonschema==4.26.0` and without PyGRC, produced:

```text
validate-phase1 = passed
validate-configs = passed
unit tests = 57 passed
v2 identity exact comparison = identical
matched null exact comparison = identical
metric calibration exact comparison = identical
frozen metric sheet exact comparison = identical
```

## 6. Claim boundary

The refresh creates no candidate result and grants no execution authority.
REG-GATE remains blocked until this review passes. Even afterward, candidate
execution requires a separate exact-cycle `P2-I1-EXEC-FREEZE`.

## 7. Completion rule

The refresh closes mechanically when every declared identity comparison and
exact-file comparison passes. Another review is required only if the
post-review implementation introduces a new decision or unresolved assumption,
the refresh exceeds its declared scope, or any comparison fails.

## 8. Disposition

The semantic fix was already reviewed. No new assumption was introduced after
that review, all required identity relations matched, and the v2 identity plus
all three calibration artifacts reconstructed byte-for-byte.

```text
P2-I1 D-020 bounded refresh = passed
```

CAL-PRE-GATE and CAL-GATE return to passed. REG-GATE may resume. Candidate
execution remains blocked pending REG-GATE and a separate cycle-scoped
EXEC-FREEZE.
