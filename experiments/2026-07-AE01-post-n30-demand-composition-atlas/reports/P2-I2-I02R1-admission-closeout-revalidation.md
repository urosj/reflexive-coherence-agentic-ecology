# P2-I2-I02R1 Admission Closeout Revalidation

**Iteration:** `P2-I2-I02R1`

**Lane:** `AE01-L02`

**Status:** complete; `P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`

**Trigger:** owner-supplied I02 identity, authority, and transition-boundary
closeout review received 2026-07-14

**Graph revision:**
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`

**Decision:** `P2-I2-DEC-008`

**Machine evidence:**
[I02R1 input freeze](../contracts/p2-i2/i02r1-closeout-review-input-freeze.json),
[CHG-004 transition](../contracts/p2-i2/i02r1-chg-004-freeze-transition.json),
[corrected admission manifest](../contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json),
and [identity/authority validation](../contracts/p2-i2/i02r1-identity-authority-validation.json)

**Evidence effect:** admission integrity and provider-contract authority only.
No realization, dependence mode, response, comparator, calibration, candidate,
control, boundary-rung, restoration-correctness, or L02 result.

## 1. Fail-closed review disposition

I02R1 found two retention defects and one newly explicit provider boundary:

1. `P2-I2-CHG-004` was labeled `audit_scope_correction`, although that class
   was allowed only before I01 completion. The correction itself occurred at
   the right time and changed the right scope, but its governance label was
   invalid. The checklist now admits and applies
   `source_admission_scope_correction`.
2. The original untracked freeze version `1.0.0` was overwritten before its
   byte-exact file was retained. I02R1 does not invent a file digest. It retains
   an exact semantic reconstruction rule and digest, the exact retained
   `1.0.1` file/semantic digests, the eight original and six added runtime
   methods, timing, and full-rerun obligation.
3. The provider covers current serialized native state, but not the model's
   private `_initial_state` as a separate reset baseline. Equal current native
   identity can therefore precede divergent `reset()` results after different
   construction/load histories. Later branching must forbid reset in the
   registered continuation window or compose and compare an explicit reset-
   baseline identity.

None is negative L02 evidence. With the governance correction, enriched exact
contracts, and reset limitation retained, the admission gate re-passes.

## 2. Frozen review and environment boundary

The I02R1 input freeze binds:

- RCAE committed entry revision
  `10c18fad2ba8ecac9ddacb0f0bc55813e6356c60` separately from ten exact
  reviewed worktree-artifact digests;
- the exact graph repository/revision and clean/read-only requirement;
- fourteen review areas and twelve gate conditions;
- source, symbol, provider, coverage, cross-artifact, and no-I03 checks;
- generic import/provider conformance only; and
- fail-closed effects and required outputs.

The user-authorized RCAE `.venv` was created with Python's standard-library
`venv` module and is ignored by Git. It intentionally received no installed
dependency. Its first forced-checkout import stopped on absent PyYAML and has
no admission effect. No dependency was downloaded or substituted.

The passing validation used the graph project's existing virtual-environment
interpreter with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH` forced to the
admitted checkout's `src`. Raw local paths are retained only in the validation
record as provenance. Stable identity remains `grc:<relative path>` at the
full revision plus SHA-256.

No multi-source pool, P2-I2 cell/control, combined-versus-single comparison,
label permutation, response, calibration, or candidate behavior ran.

## 3. Exact source and import identity

The independent validator established:

```text
graph revision exists as commit                         true
graph status before/after                              clean and equal
admitted source count                                  17
all repository-relative paths resolve at revision      true
all manifest/revision/worktree SHA-256 values match    true
dirty or untracked graph file contributed              false
imported pygrc root                                    grc:src/pygrc/__init__.py
imported models root                                   grc:src/pygrc/models/__init__.py
all imported callable modules under admitted checkout  true
ambient or other checkout used                         false
pyproject/distribution version when available          0.1 / 0.1
```

The manifest now carries the explicit invariant:

```text
all_admitted_file_sha256_match_file_contents = true
```

The seventeen admission roles remain disjoint. Each file also has one or more
orthogonal classifications:

```text
runtime_source
public_api_source
schema_or_contract_source
evidence_or_closeout_source
test_or_conformance_source
documentation_only
```

Executable source establishes implementation and import contracts. Generic
tests establish conformance only. Documentation and closeout establish
declared boundaries only. None establishes ecological adequacy.

Every manifest source is represented explicitly:

| Portable source | Admission role | Source classifications |
| --- | --- | --- |
| `grc:pyproject.toml` | package identity | contract/schema |
| `grc:src/pygrc/__init__.py` | package identity | public API |
| `grc:src/pygrc/models/__init__.py` | package identity | public API |
| `grc:src/pygrc/models/grc_9_v3_state.py` | runtime | runtime, public API, contract/schema |
| `grc:src/pygrc/models/lgrc_9_v3.py` | runtime | runtime, public API |
| `grc:src/pygrc/models/lgrc_9_v3_contract.py` | runtime | runtime, public API, contract/schema |
| `grc:src/pygrc/models/lgrc_9_v3_packets.py` | runtime | runtime, public API |
| `grc:src/pygrc/models/lgrc_9_v3_runtime.py` | runtime | runtime, public API |
| `grc:src/pygrc/models/lgrc_9_v3_runtime_state.py` | runtime | runtime, public API, contract/schema |
| `grc:src/pygrc/models/lgrc_9_v3_restoration.py` | restoration provider | runtime, public API, contract/schema |
| `grc:src/pygrc/models/lgrc_9_v3_timing.py` | supporting boundary | public API, contract/schema |
| `grc:docs/reference/LGRC9V3-CausalHistory-ReferenceGuide.md` | supporting evidence | documentation |
| `grc:tests/models/test_lgrc_9_v3_contract.py` | supporting evidence | test/conformance |
| `grc:tests/models/test_lgrc_9_v3_runtime.py` | supporting evidence | test/conformance |
| `grc:tests/models/test_lgrc_9_v3_restoration.py` | supporting evidence | test/conformance |
| `grc:tests/models/test_lgrc_9_v3_restoration_matrix.py` | supporting evidence | test/conformance |
| `grc:implementation/Phase-8-LGRC9-RestorationIdentityCloseout.json` | supporting evidence | evidence/closeout |

## 4. CHG-004 reconstruction and complete rerun

The [transition record](../contracts/p2-i2/i02r1-chg-004-freeze-transition.json)
preserves the following honest relation:

| Freeze | Retention | Digest |
| --- | --- | --- |
| `1.0.0` | Semantic predecessor reconstructible; original file bytes not retained and no file SHA claimed | reconstructed canonical semantic SHA-256 `e9c4a6f135724eccdd7713dfb40377cd72cfd1fff6fa5f069b52d123a42b2e9a` |
| `1.0.1` | Exact retained file | file SHA-256 `0ce2cbd8315faecdc9b433f767d95a7c34aa32386f84cda9c22c1d31b32760ca`; canonical semantic SHA-256 `7ba3446c412c705423547ba8de123f4cf6b493429a7ad65d5388a33f7ecb8296` |

The semantic reconstruction removes only the six added methods, changes the
version to `1.0.0`, and empties the correction list. The six added methods are
`from_state`, `step`, `run_event_queue`, `set_causal_flux_routes`, `reset`, and
`save`.

The source-completeness trigger preceded every admission role and provider
disposition. No graph path was added, no conclusion from the incomplete scope
was retained, and no desired realization drove expansion. I02R1 reran all
twenty-four symbol contracts, not only the six added rows.

## 5. Complete public-symbol contract

The validation record retains, for every one of twenty-four public symbols:

```text
public import path
module and qualified name
inspect.signature result
normalized implementation source
implementation SHA-256
admission role and contract profile
unsupported argument/input shape
causal relevance
claim boundary
```

The complete review confirms:

- queue state and bounded queue processing can affect later continuation and
  are native-current-state covered;
- route configuration can affect continuation and its current values are in
  `causal_flux_routes` inside the runtime artifact;
- scheduler/checkpoint/event-time cursors and pending packet/topology work are
  in the runtime artifact;
- current native producer configuration is in runtime `cached_quantities`;
- `snapshot()` supplies the supported complete input and `save()` serializes
  it; filesystem path is not stable identity;
- `load()` restores current native state but makes loaded current state the new
  private reset baseline; and
- `reset()` is public but is not fully governed by current-state restoration
  identity across different construction/load histories.

Constructor/resolved parameter identity appears through the embedded
`params_hash`. The identity document is a projection, not a restoration
payload; a complete supported snapshot remains necessary to load a model.

## 6. Provider input, document, and digest contract

The admitted provider remains available only for conditional later selection:

```text
identity = pygrc.models.lgrc9v3_restoration_identity_v1
digest   = pygrc.models.digest_lgrc9v3_restoration_identity_v1
kind     = lgrc9v3_restoration_identity
schema   = lgrc9v3_restoration_identity_v1
```

Generic conformance accepted:

- a concrete `LGRC9V3` model;
- an `LGRC9V3` subclass;
- a complete version-1 LGRC9V3 snapshot `dict`; and
- a complete version-1 LGRC9V3 `Mapping` wrapper.

Eight unsupported cases—arbitrary object, raw digest, partial mapping, wrong
family, unsupported version, missing runtime, malformed events, and RCAE
projection—each failed with `SnapshotCompatibilityError`. No fallback was
attempted. Plain GRC9V3 is outside the concrete-model input branch; a GRC9V3
snapshot is the tested wrong-family mapping case.

Repeated model evaluation, model-versus-snapshot evaluation, top-level mapping
reordering, and a `Mapping` wrapper produced the same identity document. The
provider adds no wall-clock time, filesystem path, memory address, or process
state. Simulation time and scheduler state remain included native state.

The exact digest relation independently reproduced is:

```text
identity_document = provider(supported_input)
canonical_text    = pygrc.core.canonical_json_dumps(identity_document)
identity_digest   = SHA256(UTF8(canonical_text))
```

The independent and provider digests both equal
`5ba5dd37cdaa11cdfbee1abf867c310ec560a854649bd3a752d3394d2e8fd41b`.
The same fixture's raw snapshot digest is
`7c2a4e4b8605808eb0d8aba7230ff90e3924615ceb1172f6ad96ef1d990b1df5`.
They remain distinct relations.

Generic sensitivity confirmed that changing route configuration, current
native producer configuration, or the scheduler cursor changes native identity
and that save/load preserves current native identity. These are provider-
contract checks only, not restoration correctness or P2-I2 continuation.

## 7. Complete identity coverage

The corrected manifest dispositioned every continuation-relevant class:

| Component | Native coverage | External duty or blocker |
| --- | --- | --- |
| Topology, allocation, tombstones | Embedded topology and stable allocation | None |
| Node/edge/basin/physical state | Embedded canonical GRC9V3 state | None |
| Resolved params | Embedded `params_hash` | Complete snapshot still required as load payload |
| Route configuration | Runtime `causal_flux_routes` | Semantic selection/config identity external |
| Packet ledger and pending queues | Runtime ledger, event queue, boundary-trial queue | None |
| Scheduler/operation cursors | Runtime scheduler, checkpoint, event-time, spark index | None |
| RNG state | Embedded GRC9V3 RNG state | External future random inputs/seeds remain registered inputs |
| Native logs/history, events, observables | Exact normalized runtime artifact plus events/observables | None |
| Native attribution lineage | Packet/surface runtime state | RCAE contributor roles and interpretation external |
| Derived causal-history overlay | Not active native runtime identity | External evidence identity when used |
| Current native producer config | Runtime cached quantities | Selection and semantic configuration identity external |
| Private reset baseline | **Not separately covered** | Forbid reset or externally compose/compare baseline; otherwise branching blocked |
| Ecology pool/history/access/dynamics | Not covered unless already native | External composite identity required |
| Intervention/control/future inputs | Not covered | External composite identity required |
| Candidate/fixture/metric/policy identity | Not covered | External composite identity required |

Anything later found capable of changing equal-input continuation must receive
one of the same three dispositions: native-covered, externally composed, or
unsupported with branching blocked.

## 8. Admission, provider selection, and fallback

I02R1 corrects ambiguous “transition/adopt” wording to conditional authority:

```text
I02R1 admits source and makes the native provider available.
selected_provider = null

if I03 selects compatible LGRC9V3 use:
  its realization profile may propose the provider
  and I06 must freeze provider ID/version before branch comparison

if external ecology state is selected:
  native identity must be composed with exact external identity

if input/provider/coverage is unsupported:
  fail closed; do not recover through fallback
```

Provider selection is configuration, not runtime recovery behavior. Exceptions
cannot trigger fallback. Provider mismatch blocks comparison, and branches
with different provider policies are not comparable.

The P2-I1 RCAE projection remains historical-only at this revision. A future
older graph revision or unavailable native helper must reopen source admission,
bind an exact provider, and update the realization profile before use. It may
not be relabeled native or applied outside its declared state coverage.

## 9. Identity versus continuation

Three relations remain separate:

```text
raw snapshot equality
restoration identity equality
bounded equal-input continuation equivalence
```

I02R1 executed only generic provider conformance. It did not run a P2-I2
continuation. A later registration must freeze the complete native plus
external branch identity, provider policy, reset disposition, equal external
configuration, equal intervention/future inputs, bounded window, compared
state/output projection, equality/tolerance rule, and failure consequence.

## 10. Cross-artifact and no-I03 review

The manifest, transition record, validation, report, source inventory,
DEC-007/008, checklist, hypothesis prerequisite, and navigation use the same
graph revision, RCAE entry boundary, seventeen sources, twenty-four symbols,
provider/schema, fallback rule, external-state duty, continuation separation,
and graph claim ceiling.

No artifact selects:

- a realization class or native pool;
- a common carrier, source/participant set, or access witness;
- `state_carried`, `history_carried`, or `hybrid`;
- `C_P`, `L`, `U`, or `V` interfaces;
- a response, comparator, signed control relation, or R05 contrast;
- a boundary rung, support status, or terminal outcome; or
- restoration correctness.

Admission proves exact permitted dependency identity. Provider admission proves
an available identity contract. Digest agreement proves canonical identity-
document consistency. None proves a pool, adequate restoration, causal
adequacy, shared-medium ecology, or L02 support.

## 11. Final gate test

| Gate condition | Disposition |
| --- | --- |
| Every source exact, portable, digest verified | Pass |
| Imports tied to admitted checkout | Pass |
| Source roles distinct | Pass |
| Complete post-CHG-004 callable review reconstructible | Pass with honest non-byte-exact predecessor boundary |
| Provider input/output/schema/digest limits exact | Pass |
| Native/external/unsupported coverage complete | Pass; reset limitation retained |
| Provider transition cannot change silently | Pass |
| Identity not continuation equivalence | Pass |
| Source inventory lane-scoped/non-retroactive | Pass |
| Admission conditional, not selection | Pass |
| No I03/scientific decision | Pass |
| Graph read-only and unchanged | Pass |

Reconstruction command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=${GRC}/src \
  ${GRC}/.venv/bin/python -B \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i2_i02r1_validate.py \
  --graph-root ${GRC} \
  --output ${TMPDIR}/p2-i2-i02r1-validation.json
```

The retained validation record file SHA-256 is
`243b82f3c108733320630de6d11584bd3a317d83ce1cd72a21075867323e3e7e`.
The graph worktree remained clean at the exact admitted revision.

Exit:

```text
exact identities + checkout-bound imports + complete symbol contracts
+ exact provider/digest boundary + complete identity coverage
+ configured no-silent transition + identity/continuation separation
+ conditional authority + no I03/scientific effect + graph unchanged
= P2-I2-SOURCE-ADMISSION-GATE passed_after_revalidation
```

I03 is ready but not begun.

I02R2 subsequently admits updated graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594`, validates native reset-baseline
persistence, and adds reset-aware identity v2 without redefining v1. The
[I02R2 report](P2-I2-I02R2-reset-baseline-persistence-revalidation.md) controls
the current prospective source/provider boundary; this I02R1 result remains
the historical record of the gap that triggered correction.

## I05H portability projection

This is a representation-only projection under `P2-I2-DEC-038` and
`P2-I2-CHG-031`. Raw bytes remain at commit
`62882efc5ecf3c131d21345ad89796f0b2ebccb7`, SHA-256
`3b48a26c0e7c95af4a3c9da19a6b04e6b9b67b72f625b5344edd2986e84b32a0`.
No source-admission, identity-authority, or scientific meaning changed.
