# P2-I2-I02 Source Admission and Restoration Transition

**Iteration:** `P2-I2-I02`

**Lane:** `AE01-L02`

**Status:** complete as executed; corrected and revalidated by I02R1;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`

**Graph revision:**
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`

**Decision:** `P2-I2-DEC-007`

**Controlling closeout correction:**
[I02R1 admission closeout revalidation](P2-I2-I02R1-admission-closeout-revalidation.md)
and `P2-I2-DEC-008`

**Machine admission record:**
[I02 admitted-source and restoration manifest](../contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json)

**Evidence effect:** exact source and restoration-provider admission only. No
realization, dependence mode, response, comparator, calibration, candidate,
control, boundary-rung, or L02 result.

## 1. Disposition

I02 admits the clean source-current graph revision and the exact P2-I2-
relevant package, runtime, restoration-provider, boundary, and supporting-
evidence identities listed in the machine manifest. The public native
restoration identity and digest are admitted for a later realization profile
that selects supported `LGRC9V3`.

This is a source/provider decision, not a realization decision. In particular:

```text
admitted now
  = exact graph source identities
  + exact public runtime callable identities
  + native restoration identity provider and digest
  + provider limits, external-state boundary, and later continuation duty

not selected now
  = native carrier or response
  + realization class
  + state/history/hybrid dependence mode
  + producer or constructed transition
  + response, comparator, calibration, registration, or candidate operation
```

I03 may consume the admitted identities when it decides whether a native-first
realization preserves the complete L02 discriminator. Mere admission supplies
no evidence that it does.

## 2. Frozen entry and scope correction

The [I02 input freeze](../contracts/p2-i2/i02-source-admission-input-freeze.json)
bound RCAE entry revision
`10c18fad2ba8ecac9ddacb0f0bc55813e6356c60`, the candidate graph revision,
seventeen graph paths, the public callable families, provider questions,
external-state boundary, continuation obligation, commands, outputs, and no-
evidence effect before the admission review began.

The first in-scope read of `lgrc_9_v3_runtime.py` showed that the callable list
omitted the public construction, queue-processing, route-configuration, reset,
and save counterparts already bounded by the I01R1 audit. `P2-I2-CHG-004`
corrected the freeze to version `1.0.1` before any callable received an
admission role and before the provider transition was decided. No source path
was added. The complete public-callable review was rerun over the corrected
scope.

## 3. Repository and source identity

Admission identity is portable:

```text
graph-reflexive-coherence
  + full Git revision
  + grc:<repository-relative path>
  + SHA-256
```

The local checkout location is command provenance only. It does not appear in
the admitted manifest. The graph checkout was on `main`, at the exact frozen
revision, and clean before and after review. RCAE made no graph-repository
write and did not import or execute PyGRC in I02.

The manifest assigns exactly one role to every frozen path:

| Role | Count | Meaning |
| --- | ---: | --- |
| `admitted_package_identity` | 3 | Package root and public export identity |
| `admitted_runtime_source` | 6 | P2-I2-relevant public state/runtime source |
| `admitted_restoration_provider_source` | 1 | Native versioned identity provider |
| `supporting_boundary_only` | 1 | Derived causal-history helpers, not active history |
| `supporting_evidence_only` | 6 | Generic tests, documentation, and graph closeout |

These seventeen files are the relevant I02 admission set, not a complete
transitive dependency lock. Any later executable registration must bind the
complete execution source and dependency identity it actually uses.

## 4. Public callable disposition

The corrected scope resolves twenty-four public symbols:

| Callable group | Count | Role |
| --- | ---: | --- |
| Public state/runtime types | 4 | `admitted_runtime_callable` |
| Public `LGRC9V3` construction, queue, contribution, feedback, routing, state, persistence, and reset methods | 14 | `admitted_runtime_callable` |
| Native restoration identity and digest | 2 | `admitted_restoration_callable` |
| Causal-history annotation/artifact helpers | 4 | `supporting_boundary_only` |

Every symbol has both a stable `pygrc.models` export source and an
implementation source in the manifest. Admission does not turn reconstruction
methods such as `set_state()` into adequate ecology interventions, and it does
not turn derived causal-history helpers into active causal history.

## 5. Native restoration provider

The admitted provider is:

```text
identity = pygrc.models.lgrc9v3_restoration_identity_v1
digest   = pygrc.models.digest_lgrc9v3_restoration_identity_v1
kind     = lgrc9v3_restoration_identity
schema   = lgrc9v3_restoration_identity_v1
```

It accepts only:

- a concrete `LGRC9V3` model at the admitted revision; or
- a complete `LGRC9V3` `pygrc.snapshot` version-1 mapping at that revision.

It does not accept a plain `GRC9V3` model/snapshot, a raw snapshot digest, an
RCAE projection, or a wrong-family, partial, malformed, or unsupported-version
snapshot.

The identity contains canonical embedded GRC9V3 state, the normalized exact
LGRC9V3 runtime artifact, events, observables, and source snapshot schema and
version. Its digest is the canonical digest of that identity document. Neither
the identity nor its digest is raw snapshot byte identity.

Identity equality is necessary at a registered branch point, but it does not
establish bounded equal-input continuation by itself and cannot establish
unrestricted behavioral equivalence.

## 6. Explicit P2-I1 to P2-I2 provider transition

P2-I1 C02 used an RCAE-owned provider:

```text
symbol:
  restoration_projection

portable source:
  rcae:experiments/2026-07-AE01-post-n30-demand-composition-atlas/
       scripts/p2_i1_execution.py

frozen C02 source revision:
  c2def54c3721c506c28fc9f14390b1ba683a98ec

source SHA-256:
  d09955bf48b986729dc01acd283fdbe14f7515e9b5e8785c404f34ea53effa07
```

That provider remains the immutable historical P2-I1 C02 identity under
`P2-I1-DEC-027`. It is not admitted as an automatic P2-I2 fallback at the
current graph revision, because the native helper is present and admitted.

The graph closeout recognizes an RCAE C02 projection fallback only for an
older graph revision or an unavailable helper, and forbids relabeling it as
native. I02 makes that boundary operational: such a future condition must
reopen I02, bind and admit an exact fallback provider, and update the selected
realization profile. Silent native upgrade, fallback downgrade, or provider
substitution is forbidden.

This transition changes neither P2-I1 evidence nor its result.

## 7. Native and external state ownership

The native identity owns the supported PyGRC state represented by its versioned
contract. A complete P2-I2 branch identity must separately compose all
selected RCAE state and semantics, without double-counting native state:

| External identity class | Examples |
| --- | --- |
| Realization and roles | realization class, dependence mode, carrier/pool/contributor roles, access scope |
| Causal guards | access witness, held-fixed variables, matching assertions, private-partition and no-common-read guards |
| Intervention | targets, gates, clamps, write freeze, history transforms, intervention and future-input schedules |
| Producer/configuration | semantic identity of selected native producer configuration; any RCAE producer or constructed transition |
| Ecology-owned state | only selected pool/history/access/capacity/leakage/maintenance state not already native |
| Experiment identity | fixture, sources, contribution operations, ordering, seeds, resources, metric, calibration, analysis, registration, and execution policy |

The minimum complete later identity is therefore:

```text
admitted native restoration identity and digest
  + selected external-state identity and digest
  + intervention / producer / configuration identity and digest
```

Whether any external producer or constructed state is needed is an I03
native-adequacy decision. I02 does not authorize one.

## 8. Bounded continuation obligation

I02 defines but does not execute the continuation check. Every later selected
restorable branch point must:

1. establish equal admitted native identity and equal separately composed
   external identity;
2. independently restore the branches;
3. apply exactly equal registered future inputs for one bounded registered
   horizon; and
4. compare the registered continuation projection under a fail-closed rule.

The later freeze must identify the fixture, branch point, identity projections,
future inputs, horizon, continuation projection, tolerance/equality rule, and
failure effect. Raw snapshot digests remain diagnostic unless a later
registration explicitly makes them an additional requirement.

## 9. Graph closeout boundary

The graph restoration closeout supports the versioned native provider and
bounded equal-input continuation only for its declared fixtures. I02 preserves
all of its negative boundaries. Source/provider admission does not support:

- raw snapshot byte identity;
- unrestricted continuation equivalence;
- native shared medium or ecology;
- identity acceptance or RC identity;
- agency or selfhood;
- organism or life; or
- Phase 8 completion.

It also supplies no P2-I2 boundary rung, support status, classification value,
terminal state, cross-lane recurrence, or N31+ selection.

## 10. Static validation and exit

I02 used only the frozen read-only source and validation operations. No dynamic
import, upstream test, custom probe, candidate fixture, calibration, or control
operation was needed or permitted.

The retained validation checks cover:

```text
input-freeze JSON and entry-artifact digests
exact graph revision, branch observation, and clean worktree
17 of 17 frozen graph file SHA-256 values
17 unique source paths with allowed roles
24 unique public symbols with allowed roles
public export and implementation definition for every symbol
historical P2-I1 provider source at its frozen source revision and SHA-256
portable grc:/rcae: identities and absence of machine-local paths in manifest
local Markdown targets
checklist/decision/hypothesis/source-inventory/master/navigation agreement
git diff --check
no I03 realization or scientific field assigned
```

Exit disposition:

```text
exact source identities admitted
+ native provider and digest admitted with supported-input limits
+ explicit prior/fallback transition
+ complete external-state ownership classes
+ bounded later continuation obligation
+ graph closeout ceiling preserved
+ no later-gate decision or evidence
= P2-I2-SOURCE-ADMISSION-GATE passed
```

I03 is ready but not begun.

I02R1 subsequently clarified that the provider is available for conditional
later selection (`selected_provider = null`), corrected CHG-004 governance,
bound imported-package provenance and complete callable/coverage contracts,
and retained the uncovered private reset-baseline limitation. The I02R1 report
controls wherever this original report's transition wording could be read as
provider adoption rather than admission.

I02R2 later supersedes the prospective graph dependency with revision
`83e3a300426631ee4df71b661b67d4fcfdfed594`, validates persisted reset
baseline, and admits reset-aware v2 as conditionally available. The
[I02R2 report](P2-I2-I02R2-reset-baseline-persistence-revalidation.md) controls
current P2-I2 source/provider admission; this report remains historical I02
provenance.
