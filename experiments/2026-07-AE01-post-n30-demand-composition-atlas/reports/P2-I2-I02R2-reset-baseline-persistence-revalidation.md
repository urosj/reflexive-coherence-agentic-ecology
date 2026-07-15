# P2-I2-I02R2 Reset-Baseline Persistence Revalidation

**Iteration:** `P2-I2-I02R2`

**Status:** complete;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`

**Date:** 2026-07-14

**Evidence effect:** exact source/import/reset/provider conformance only. No
realization, dependence mode, calibration, candidate behavior, boundary rung,
or L02 result.

## 1. Result

Yes: updated PyGRC now preserves the declared `reset()` baseline across native
snapshot/save/load for the tested LGRC9V3 contract.

The correction is not a hidden checkpoint rebase:

```text
set_state(state)             -> changes current state only
rebase_reset_baseline()      -> explicitly adopts current state as baseline
reset()                      -> restores persisted or explicitly rebased baseline
save/load                    -> preserves current state and declared baseline
```

A legacy snapshot without baseline provenance still loads its current state,
but `reset()` and restoration identity v2 fail closed until explicit rebase.
That rebase is prospective; it does not recover historical construction state.

## 2. Frozen authority

The validated [I02R2 input freeze](../contracts/p2-i2/i02r2-reset-baseline-revalidation-input-freeze.json)
binds RCAE committed HEAD
`10c18fad2ba8ecac9ddacb0f0bc55813e6356c60` separately from this exact graph
transition:

| Role | Revision |
| --- | --- |
| Historical I02R1 admission | `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5` |
| Updated admitted graph | `83e3a300426631ee4df71b661b67d4fcfdfed594` |

The graph worktree was clean before and after source inspection, focused
upstream tests, and the retained validator. Imports were forced to the updated
checkout; no package installation or graph write occurred.

## 3. Exact source and callable transition

The [source transition](../contracts/p2-i2/i02r2-graph-source-transition.json)
records all 35 changed upstream paths with old/new/worktree SHA-256 values.
Seventeen changed paths supply direct reset-revalidation authority; the rest
are classified as cross-family implementation/regression, contract,
implementation, or documentation context rather than silently promoted to
P2-I2 runtime dependencies.

The effective [I02R2 admission manifest](../contracts/p2-i2/i02r2-admitted-source-and-reset-provider-manifest.json)
binds:

```text
31 exact source identities
31 complete public callable contracts
graph revision 83e3a300426631ee4df71b661b67d4fcfdfed594
```

All manifest, revision, and worktree digests match. Every callable resolves
under the updated checkout and retains its module, qualified name, signature,
implementation source/digest, supported boundary, causal relevance, and claim
ceiling.

## 4. Reset-baseline artifact

New snapshots retain the shared snapshot version and add a versioned group:

```text
reset_baseline_schema  = pygrc.reset_baseline
reset_baseline_version = 1
status                 = available | unavailable
```

An available group contains a complete same-family baseline snapshot with the
same parameter hash. Nested reset-baseline groups are forbidden, preventing
recursive serialization. An unavailable group contains only an explicit
reason.

Independent checks confirmed:

| Contract | Result |
| --- | --- |
| Same-family complete baseline | Pass |
| Same outer/baseline parameter hash | Pass |
| Recursive nesting absent/rejected | Pass |
| Original/restored current v1 identity equal | Pass |
| Original/restored reset-aware v2 identity equal | Pass |
| Original/restored `reset()` outcome equal | Pass |
| Three repeated save/load cycles preserve v2 and reset baseline | Pass |
| `set_state()` preserves baseline | Pass |
| Rebase requires explicit public call | Pass |

## 5. Restoration identity transition

PyGRC correctly preserves two different identities:

```text
lgrc9v3_restoration_identity_v1
  = current native state only; unchanged

lgrc9v3_restoration_identity_v2
  = current_state_restoration_identity_v1
  + reset_baseline_restoration_identity_v1
```

Two generic models were given equal current state but different explicitly
declared reset baselines. Their v1 digests were equal and their v2 digests were
different. This directly closes the I02R1 gap without redefining v1.

The v2 digest independently matched:

```text
SHA256(UTF8(pygrc.core.canonical_json_dumps(identity_v2)))
= 81644a930629776fbaddea4840784c85aa1f7b70d18e118a393443f12f63a1eb
```

## 6. Legacy and malformed-input policy

For a legacy snapshot lacking the group:

```text
current state load       = allowed
reset before rebase      = SnapshotCompatibilityError
identity v2 before rebase = SnapshotCompatibilityError
explicit rebase          = allowed prospectively
historical baseline recovered = false
```

After explicit rebase, v2 remained stable across save/load and reset restored
the adopted checkpoint baseline. RCAE must retain
`explicit_rebase_from_legacy_checkpoint` as external provenance if it ever
uses that route.

Malformed baseline snapshot, wrong family, wrong parameter hash, recursion,
and unsupported baseline version all failed explicitly with no fallback.

## 7. Verification

The retained [machine validation](../contracts/p2-i2/i02r2-reset-baseline-validation.json)
was generated by the generic
[validator](../scripts/p2_i2_i02r2_validate.py). It contains no P2-I2 source
set, pool, cell, control, comparator, or response behavior.

Focused upstream verification, with cache disabled and temporary files outside
the graph repository:

```text
68 passed
32 subtests passed
0 failed
```

The retained validator additionally rechecked 31 source identities, 31 public
callable contracts, save/load/reset equality, baseline-only v2 sensitivity,
three-cycle persistence, state/rebase semantics, legacy behavior, five
malformed cases, canonical digest recomputation, checkout imports, and graph
cleanliness.

## 8. Admission and claim boundary

Revision `83e3a300426631ee4df71b661b67d4fcfdfed594` and the reset-aware v2
provider are admitted for conditional later selection. Provider selection
remains configuration owned by I03/I06:

```text
selected_provider = null
```

The I02R1 blanket reset restriction no longer applies to new snapshots with a
valid persisted baseline when a later registered profile selects v2. It still
applies to legacy/unavailable baseline state until explicit rebase and external
rebase provenance are registered.

This establishes that PyGRC now handles its declared reset lifecycle correctly
under the tested contract. It does not select LGRC9V3 or v2 for P2-I2, cover
RCAE-owned pool/intervention/configuration state, prove unrestricted
continuation equivalence, or provide scientific evidence.

## 9. Gate disposition

| Gate condition | Disposition |
| --- | --- |
| Exact updated source/import identity | Pass |
| Complete affected and effective callable review | Pass |
| Reset baseline serialized without recursion | Pass |
| Save/load preserves reset behavior | Pass |
| Baseline-only difference changes v2 | Pass |
| Repeated cycles preserve baseline | Pass |
| State replacement/rebase semantics explicit | Pass |
| Legacy and malformed input fail closed | Pass |
| V1 unchanged; v2 separately versioned | Pass |
| Provider remains unselected | Pass |
| No I03 or scientific evidence | Pass |
| Graph repository read-only and clean | Pass |

`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`. I03 is ready
but not begun and still requires its own input freeze.
