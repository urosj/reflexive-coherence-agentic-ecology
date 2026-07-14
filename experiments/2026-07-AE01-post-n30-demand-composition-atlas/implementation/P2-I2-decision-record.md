# P2-I2 Decision Record

**Status:** active cumulative lane decision record

**Lane:** `AE01-L02`

**Iteration:** `P2-I2`

**Evidence effect:** none; decisions constrain later work but are not results

**Controlling boundaries:**
[accepted P2-I2 brief](P2-I2-shared-pool-co-conditioning-brief.md),
[P2-I2 checklist](P2-I2-shared-pool-co-conditioning-checklist.md),
[operational hypothesis projections](../hypotheses/p2-i2-operational-hypotheses.md),
[common contract](../contracts/common-contract.md), and
[execution policy](../configs/p1_i5_execution_policy.json)

## 1. Purpose and use

This is the single cumulative decision record for P2-I2. Every resolved or
partially resolved semantic, audit, realization, measurement, control,
registration, execution, interpretation, or closure question receives a
stable decision ID here rather than a separate decision file.

The checklist is the activity and gate tracker. This record preserves the
question, considered options when alternatives exist, reasoning, accepted
boundary, remaining unknowns, gate effect, and reopening conditions.

A decision may constrain a gate without passing it. Later evidence may reopen
a decision only through its recorded reopening conditions and checklist change
control; it may not silently rewrite the historical choice. No decision may be
inferred from an activity performed outside its named checklist iteration.

## 2. Decision index

| Decision ID | Question | Status | Gate effect | Date |
| --- | --- | --- | --- | --- |
| `P2-I2-DEC-001` | Is the revised P2-I2 brief accepted as lane-local semantic authority, and which boundaries remain fixed? | Accepted by project owner | Passes `P2-I2-BRIEF-GATE`; grants no audit/calibration/execution authority | 2026-07-14 |
| `P2-I2-DEC-002` | How must P2-I2 activities be planned and retained? | Owner-directed and accepted: checklist-first named iterations; no off-ledger work | Constrains every P2-I2 activity and gate | 2026-07-14 |
| `P2-I2-DEC-003` | What authority and lifecycle do the operational hypothesis artifacts have? | Derived and accepted under DEC-001/002: subordinate scaffold now, realization binding after audit/admission | Constrains I00, I03, and I04; creates no second hypothesis | 2026-07-14 |
| `P2-I2-DEC-004` | How are I03 causal expectations separated from I04 machine rules, and how is calibrated resolution retained? | Derived and accepted from the common metric contract and I00R1 review | Constrains I03–I05; no calibration performed | 2026-07-14 |
| `P2-I2-DEC-005` | Which source-current public PyGRC surfaces are adequate or inadequate for the L02 discriminator? | Original I01 audit disposition; corrected by `P2-I2-DEC-006` | Historical gate pass reopened by I01R1 | 2026-07-14 |
| `P2-I2-DEC-006` | Does I01 satisfy the capability-audit closeout boundary after excluding candidate-shaped behavior? | I01R1 complete: probe quarantined; CAP-04 corrected to inadequate; package revalidated | Re-passes `P2-I2-SOURCE-AUDIT-GATE`; I02 ready but not begun | 2026-07-14 |
| `P2-I2-DEC-007` | Which exact graph sources and restoration provider may P2-I2 consume, and how does the P2-I1 provider transition? | Historical I02 disposition; clarified and revalidated by `P2-I2-DEC-008` | Original gate pass reopened by I02R1 | 2026-07-14 |
| `P2-I2-DEC-008` | Does I02 satisfy exact identity, import authority, callable/provider coverage, and conditional-transition closeout? | Historical I02R1 admission at graph revision `3d3d2ef`; reset limitation later updated by `P2-I2-DEC-009` | Historical gate pass reopened by I02R2 | 2026-07-14 |
| `P2-I2-DEC-009` | Does updated PyGRC preserve reset baseline across restoration and represent it in exact identity? | I02R2 complete: updated source admitted, reset persistence validated, v2 provider admitted but unselected | Re-passes `P2-I2-SOURCE-ADMISSION-GATE`; I03 ready but not begun | 2026-07-14 |

## 3. `P2-I2-DEC-001` — Brief acceptance and frozen boundaries

**Status:** accepted by project owner

**Question:** Is the revised P2-I2 shared-pool co-conditioning brief clear and
complete enough to govern lane-local artifact construction?

### 3.1 Accepted decision

The project owner explicitly confirmed on 2026-07-14 that the supplied
acceptance review constitutes owner acceptance: “yes, it is acceptance.” The
brief is accepted as the semantic authority for P2-I2 under the frozen Phase 1
contracts.

The acceptance retains:

```text
frozen lane hypothesis = AE01-H-L02
D-039 inherited/ecology distinction = binding
maximum claim = bounded shared-pool co-conditioning demand pattern
logical cells = seven frozen L02 cells
lane controls = five frozen L02 controls
one-pool factorization = required
non-private access witness = required
dependence mode = required before calibration
native-first audit = required
producer/constructed fallback = allowed only when explicit and bounded
restoration-provider transition = explicit admission required
candidate execution = closed
```

The accepted factorization separates the mode-relevant common causal carrier
from audit-only attribution metadata. The accepted dependence modes are
`state_carried`, `history_carried`, and admissible `hybrid`; none is selected
by this decision.

### 3.2 Gate and evidence effect

`P2-I2-BRIEF-GATE=passed`. This authorizes construction of the checklist,
cumulative decision record, subordinate operational-hypothesis scaffold, and
the later input freeze for the source-current capability audit.

It does not:

- admit graph revision `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`;
- select a native or producer realization;
- select a carrier, source set, dependence mode, response, comparator, or
  transfer axis;
- freeze calibration or registration;
- authorize candidate execution; or
- assign any boundary rung, support status, classification value, terminal
  state, or lane result.

### 3.3 Reopening conditions

Reopen this decision only if:

- a controlling Phase 1 contract is formally reopened or found inconsistent
  with the brief;
- the project owner withdraws or narrows acceptance; or
- a named later iteration demonstrates that the inherited relation and ecology
  discriminator cannot be operationally separated under the accepted brief,
  requiring formal aim redescription rather than a missing-prerequisite
  classification.

## 4. `P2-I2-DEC-002` — Checklist-first activity authority

**Status:** owner-directed and accepted

**Question:** How must P2-I2 work be sequenced and evidenced so that audits and
other preparatory actions do not occur without a retained iteration record?

### 4.1 Accepted decision

The checklist and operational hypothesis artifacts are constructed before the
source-current capability audit. Every P2-I2 activity is a named checklist
iteration with declared purpose, entry authority, frozen inputs or an explicit
input-freeze action, mutation boundary, outputs, evidence effect, and exit
gate.

This applies to:

- source-current capability audits;
- source admission and restoration-profile transitions;
- realization and discriminator decisions;
- operational hypothesis binding;
- calibration preregistration and calibration execution;
- implementation and registration construction;
- candidate-cycle freeze and live execution;
- control resolution and index generation;
- reconstruction; and
- interpretation and closeout.

Brief-preparation inspection of the graph checkout established only that a
candidate revision and restoration API exist. It is not retrospectively
treated as the I01 capability audit.

### 4.2 Consequences

- `P2-I2-I00` owns the authority bootstrap and may close after its artifacts
  and navigation validate.
- `P2-I2-I01` is the first capability-audit iteration. It remained pending
  until its input scope was frozen and is now complete under that retained
  freeze; see `P2-I2-DEC-005`.
- No unrecorded command, inspection, implementation, or run may satisfy a
  later checkbox or gate.
- A new evidence need expands the checklist through `P2-I2-CHG-NNN` before the
  work occurs, except for a bounded safety action needed to stop an active
  invalid run.

### 4.3 Reopening conditions

Reopen only if the owner changes the lane process or Review R4 admits a
different common activity-record mechanism that preserves or strengthens the
same traceability. Tool inconvenience is not a reopening condition.

## 5. `P2-I2-DEC-003` — Operational hypothesis authority and lifecycle

**Status:** derived and accepted under DEC-001/002; realization binding pending

**Question:** How can P2-I2 freeze realization-local falsifiable statements
without creating a second hypothesis that competes with `AE01-H-L02`?

### 5.1 Accepted decision

One artifact contains nine subordinate operational projections:

```text
H-L02-OP-01 common-pool constitution
H-L02-OP-02 combined-carrier dependence
H-L02-OP-03 attribution-only invariance
H-L02-OP-04 common-carrier intervention dependence
H-L02-OP-05 insufficient-repetition exclusion
H-L02-OP-06 private-partition exclusion
H-L02-OP-07 controller/direct-path exclusion
H-L02-OP-08 mode-specific order/shuffle relation
H-L02-OP-09 bounded contrast retention
```

These IDs are lane-local navigation and traceability IDs, not additions to the
closed hypothesis registry or schema vocabulary.

The artifact lifecycle is:

```text
I00 scaffolded and outcome-free
I03 realization_bound -> I04 preregistered -> I08 executed or incomplete
I03 prerequisite_classified -> I09/I11 earlier-stop interpretation
I09/I11 resolved and interpreted
```

The quantity-matched single-source replacement remains a scope diagnostic, not
a tenth support hypothesis or automatic gate.

### 5.2 Gate and evidence effect

The scaffold helps define I01 audit questions and I03 binding obligations. It
does not select any unbound realization variable and supplies no evidence.

`P2-I2-DISCRIMINATOR-GATE` cannot pass until each projection maps to actual
runtime interfaces, exact cells and controls, held-fixed variables, signed
qualitative relations, ambiguous scientific outcomes, and fail-closed effects.
`P2-I2-CAL-PRE-GATE` cannot pass until I04 imports those causal expectations
unchanged and freezes the response, comparator, numerical evaluation, metric
pairing, null, and stopping rule.

### 5.3 Reopening conditions

Reopen if the source audit shows that a projection combines causally distinct
questions that require separate preregistered tests, or that one projection
cannot be operationalized without changing `AE01-H-L02`. Any split or
redescription must preserve the original scaffold and receive checklist change
control.

## 6. `P2-I2-DEC-004` — Causal versus numerical freeze and metric artifacts

**Status:** derived and accepted from the common contract and I00R1 review

**Question:** Which meanings freeze in I03 versus I04, and how may I05 retain a
calibrated resolution without ambiguously mutating the frozen base L02 metric
sheet?

### 6.1 Accepted decision

I03 freezes realization-local causal semantics:

```text
intervention target and causal meaning
variables held fixed for causal interpretation
qualitative invariance, divergence, or direction
allowed scientific ambiguity
fail-closed rung/support consequence
```

I04 imports those meanings without revision and freezes their machine
operationalization:

```text
raw measurement and units
equality/resolution rule
numerical orientation
primary comparator
aggregation and missingness
machine-executable pass / ambiguous / fail evaluation
```

I05 follows the common metric contract and `freeze-resolution` artifact
pattern. The base `contracts/metric-sheets/AE01-L02.json` remains unchanged.
I05 retains:

1. a first-class lane-local metric-calibration record linked to the base metric
   sheet; and
2. a generated frozen metric-sheet artifact that copies the base semantic
   identity and populates only its designated resolution status, `delta`,
   rationale, and calibration-artifact reference fields.

The generated frozen artifact does not change the candidate/comparator,
formula, pairing, direction, threshold, estimator, measurement resolution, or
schema identity frozen before calibration.

### 6.2 Authority and gate effect

This decision derives from Section 16 of the common contract, the P1-I5
`freeze-resolution` tooling contract, and the retained P2-I1 separation between
the base and generated frozen metric sheets. It resolves wording only. No
matched null was generated and no calibration field was populated for L02.

I03 cannot defer a causal expectation to I04. I04 cannot numerically redefine
that expectation. I05 cannot mutate the base sheet or use candidate input.

### 6.3 Reopening conditions

Reopen only if the common metric-sheet contract or `freeze-resolution`
artifact semantics are formally revised before I04 closes, or if validation
shows that the designated frozen-sheet fields cannot represent the accepted
calibration without changing semantic identity.

## 7. `P2-I2-DEC-005` — Source-current native adequacy disposition

**Status:** historical audit-derived disposition; corrected by
`P2-I2-DEC-006`; not owner selection of a realization

**Question IDs:** `L02-Q00`, `L02-Q01`

**Question:** Which public surfaces at the exact source-current PyGRC revision
can carry the accepted L02 relation, which are inadequate, and what minimal
producer demands remain?

### 7.1 Audit basis

`P2-I2-I01` froze and audited the clean graph revision
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`. The package-root correction
`P2-I2-CHG-002` was recorded after the in-scope packaging manifest identified
`src/pygrc/**` and before package source inspection or classification.

Retained evidence:

- [narrative capability audit](../reports/P2-I2-I01-source-current-capability-audit.md);
- [capability matrix](../contracts/p2-i2/i01-capability-matrix.json);
- [source digests](../contracts/p2-i2/i01-source-digests.json); and
- [command provenance](../reports/P2-I2-I01-command-provenance.md).

### 7.2 Derived decision

Retain this bounded native shortlist for I02/I03 consideration:

```text
native common carrier candidate
  = one declared target node's GRC9V3 coherence

native joint contribution transition
  = at least two attributable LGRC9V3 packet paths credit that same node

native later response candidate
  = feedback-eligibility surface over current node coherence
    -> model-owned feedback producer
    -> native event-queue processing

native branch identity
  = lgrc9v3_restoration_identity_v1
    + digest_lgrc9v3_restoration_identity_v1
```

The source facts identify a composition-capable encounter-state candidate, not
an adequate complete realization and not a selected `state_carried` mode. The
packet ledger retains source attribution but is inadequate as the claimed pool
because it remains partitioned by source, target, edge, and lineage. The later
feedback path reads current carrier state rather than those lineage labels.

The audit-derived native gaps are:

```text
first-class pool role and access-scope identity
matched private-partition control and no-common-read guard
selective pooled-history shuffle/permutation
state/history intervention independent of native audit evidence
atomic pool-specific write freeze and value/history clamp
generic pool capacity/saturation, leakage/decay, and maintenance dynamics
```

Native route/producer withdrawal and distinct native topology nodes must be
tested first for the applicable controls. If they are inadequate, I03 may
authorize only the smallest explicit RCAE writer, registry, matched-control
harness, history projection, gate/clamp, or selected ecology-state transition.
No bundled resource economy or controller may be introduced by convenience.

### 7.3 Gate and authority effect

This decision originally passed `P2-I2-SOURCE-AUDIT-GATE`. I01R1 reopened that
gate after identifying the candidate-shaped custom probe and CAP-04
overclassification. `P2-I2-DEC-006` controls the current disposition. DEC-005
continues to record which surfaces were found and where native support is
inadequate. It does not:

- admit the graph revision or restoration helper;
- select the native shortlist as the realization;
- choose `state_carried`, `history_carried`, or `hybrid` dependence;
- authorize a producer or constructed control;
- freeze the response, comparator, calibration, or registration; or
- assign a lane result.

I02 must decide exact source admission and the restoration-profile transition.
I03 must then decide whether the bounded native core satisfies the complete
discriminator and which minimal producer/control boundaries are necessary.

### 7.4 Reopening conditions

Reopen this audit disposition if:

- I02 proposes a different graph revision;
- a cited public surface or digest does not match the admitted checkout;
- an I03 conformance check contradicts an I01 public-capability fact;
- the selected dependence mode requires a surface classified inadequate or
  absent here; or
- a scope defect is found that requires `audit_scope_correction` change
  control and explicit question reruns.

## 8. `P2-I2-DEC-006` — Capability-audit closeout correction

**Status:** I01R1 correction retained and validated

**Question IDs:** `L02-Q00`, `L02-Q01`

**Question:** Does the I01 package satisfy the capability-audit boundary when
candidate behavior is excluded, and what classifications change?

### 8.1 Trigger and correction

The owner-supplied closeout review requires executable I01 checks to remain
interface/capability conformance only. The custom I01 probe instantiated a
multi-source common-carrier fixture and compared combined, single-source, and
label-permuted later responses. I01R1 therefore:

- quarantines the probe source and output from capability and scientific
  evidence while retaining full historical provenance;
- reruns the audit judgments from static public-source contracts and
  pre-existing generic PyGRC tests only;
- changes CAP-04 from `adequate` to `inadequate` because persistence exists but
  no public state-only or active-history intervention independent of audit
  evidence was established; and
- replaces realization-suggestive `state_carried` adequacy wording with a
  mode-neutral composition-capable-candidate disposition.

Evidence:

- [I01R1 closeout revalidation](../reports/P2-I2-I01R1-capability-audit-closeout-revalidation.md);
- corrected [narrative audit](../reports/P2-I2-I01-source-current-capability-audit.md);
- corrected [capability matrix](../contracts/p2-i2/i01-capability-matrix.json);
  and
- corrected [command provenance](../reports/P2-I2-I01-command-provenance.md).

### 8.2 Retained source-current disposition

The exact revision still exposes a public, composition-capable native
candidate: multiple attributable packet paths can credit one node-coherence
carrier; a feedback surface and producer can read current node state and
schedule native work without consulting lineage labels; and native restoration
identity covers the supported PyGRC-owned branch state.

This is not complete native-realization adequacy. Public control gaps remain
for state/history intervention independent of audit evidence, atomic pool
freeze/clamp, matched private partition, selective pooled-history intervention,
access-role identity, and generic pool dynamics. I02 may consider source
admission only after I01R1 re-passes the source-audit gate. I03 alone may select
or reject a realization and dependence mode.

### 8.3 Gate effect

The corrected package re-passes `P2-I2-SOURCE-AUDIT-GATE`. I02 is ready but
not begun. No source admission, realization selection, calibration, candidate
evidence, control result, or lane result is assigned.

### 8.4 Reopening conditions

Reopen this correction if quarantined output reappears as capability evidence,
CAP-04 is upgraded without a public independent-intervention surface, the
admitted source differs from the audited revision, or a cited public contract,
digest, supported-input boundary, or graph worktree assertion fails validation.

## 9. `P2-I2-DEC-007` — Exact source admission and restoration transition

**Status:** historical I02 admission disposition; clarified and revalidated by
`P2-I2-DEC-008`

**Question ID:** `L02-Q02`

**Question:** Which exact graph source and public callable identities may later
P2-I2 iterations consume, which restoration provider governs supported native
branch identity, and what is the allowed relationship to the historical P2-I1
provider?

### 9.1 Admitted decision

Admit the clean graph revision
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5` and the exact seventeen source
identities in the
[I02 machine manifest](../contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json).
The manifest assigns separate package, runtime, restoration-provider,
supporting-boundary, and supporting-evidence roles and binds every public
symbol to both its stable export source and implementation source.

Admit the following native restoration provider for any later P2-I2 profile
that selects supported `LGRC9V3`:

```text
identity provider
  = pygrc.models.lgrc9v3_restoration_identity_v1

identity digest provider
  = pygrc.models.digest_lgrc9v3_restoration_identity_v1

accepted input
  = concrete LGRC9V3 model at the admitted revision
    or complete LGRC9V3 pygrc.snapshot version-1 mapping
```

Wrong-family, plain GRC9V3, raw digest, RCAE projection, partial, malformed,
and unsupported-version inputs are not accepted. The identity digest is a
digest of the versioned native identity document, not a raw snapshot digest.

The P2-I1 C02 `restoration_projection` is retained at RCAE source revision
`c2def54c3721c506c28fc9f14390b1ba683a98ec`, source SHA-256
`d09955bf48b986729dc01acd283fdbe14f7515e9b5e8785c404f34ea53effa07`.
It remains P2-I1 historical authority and is not admitted as an automatic
fallback for P2-I2 at the current graph revision. If a future proposed older
revision lacks the helper, I02 must reopen and explicitly admit a fallback
before use. The RCAE projection cannot be relabeled as native. Silent upgrade,
downgrade, or provider substitution is forbidden.

### 9.2 External-state and continuation consequence

Native identity covers only supported PyGRC-owned state. Every selected later
branch identity must compose, without duplication:

```text
native restoration identity and digest
  + RCAE role, access, matching, and control identity
  + any selected ecology-owned pool/history/constructed state
  + intervention, producer, configuration, and future-input identity
  + fixture, analysis, metric, calibration, registration, and policy identity
```

For every selected restorable branch point, equal native and external identity
must be followed by independently restored, exactly equal registered future
inputs and one bounded fail-closed continuation comparison. Identity equality
does not replace continuation, and neither establishes unrestricted behavioral
equivalence.

### 9.3 Gate and evidence effect

`P2-I2-SOURCE-ADMISSION-GATE=passed`. I03 may now decide whether the admitted
native surfaces are adequate for one complete discriminator-preserving
realization and which minimal explicit producer or constructed transitions are
needed.

This decision does not select a realization, carrier, pool, response,
dependence mode, producer, intervention, comparator, or measurement. It does
not authorize calibration, registration, or candidate execution and supplies
no P2-I2 scientific evidence or result. The graph restoration closeout's
negative claim boundary remains controlling.

### 9.4 Reopening conditions

Reopen if:

- the graph revision, worktree assertion, source digest, export, or callable
  definition changes or fails;
- I03 needs a source, callable, input family, or role outside the manifest;
- the native provider fails its admitted supported-input or identity boundary;
- a fallback provider is proposed; or
- the external-state composition or bounded-continuation obligation cannot be
  represented without changing this decision.

## 10. `P2-I2-DEC-008` — Admission closeout correction and revalidation

**Status:** accepted from retained I02R1 evidence

**Question ID:** `L02-Q02`

**Question:** Does the I02 package make every admitted dependency exact and
reproducible, tie executable imports to the admitted checkout, define complete
callable/provider/identity coverage, and preserve conditional authority without
turning admission into realization selection or restoration correctness?

### 10.1 Trigger and corrections

The owner-supplied closeout review reopened the source-admission gate. I02R1
found and corrected:

1. `P2-I2-CHG-004` used `audit_scope_correction`, which was not allowed after
   I01. Its corrected class is `source_admission_scope_correction`.
2. The untracked `1.0.0` freeze bytes were not retained before `1.0.1`
   replaced them. I02R1 retains an honest semantic reconstruction and digest,
   not a fabricated predecessor file SHA.
3. The provider covers current serialized native state but not private
   `_initial_state` as a separate reset baseline. A registered continuation
   must forbid reset or compose and compare an explicit reset-baseline
   identity.

Evidence:

- [I02R1 revalidation](../reports/P2-I2-I02R1-admission-closeout-revalidation.md);
- [identity/authority validation](../contracts/p2-i2/i02r1-identity-authority-validation.json);
- [CHG-004 transition](../contracts/p2-i2/i02r1-chg-004-freeze-transition.json);
  and
- corrected [admission manifest](../contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json).

### 10.2 Revalidated decision

Retain the exact graph revision, seventeen source identities, and twenty-four
public symbols admitted by DEC-007. Every source now has granular runtime,
public-API, contract/schema, evidence/closeout, test/conformance, or
documentation roles as applicable. Every symbol has an exact imported module,
qualified name, signature, implementation source/digest, argument boundary,
causal relevance, and claim ceiling.

The separate RCAE review-entry authority is committed HEAD
`10c18fad2ba8ecac9ddacb0f0bc55813e6356c60`, with the ten reviewed I02
worktree artifacts bound by exact SHA-256 values in the I02R1 input freeze.
That RCAE authority is not the graph revision and does not substitute for any
graph source identity.

Raw imported provenance establishes that `pygrc`, `pygrc.models`, and all
symbol implementation modules came from the admitted checkout, not an ambient
wheel, old editable install, or other checkout. All seventeen manifest,
revision, and worktree digests match and the graph worktree remained clean.

The native provider is **available for conditional later selection**; it is
not selected by I02:

```text
selected_provider = null

compatible I03 profile may propose provider
I06 must freeze provider ID/version as configuration
provider selection is not runtime recovery behavior
provider mismatch blocks branch comparison
exception or unsupported input cannot trigger fallback
```

The provider accepts an `LGRC9V3` model/subclass or complete supported
version-1 LGRC9V3 `Mapping`. Unsupported inputs fail with
`SnapshotCompatibilityError` and no fallback. Its identity is deterministic
under equal supported state and mapping reordering. Its digest is:

```text
SHA256(UTF8(pygrc.core.canonical_json_dumps(identity_document)))
```

This is distinct from raw snapshot digest and from bounded continuation.

### 10.3 Complete identity boundary

Current topology/allocation/tombstones, physical state, resolved parameter
identity, routes, pending queues, scheduler/checkpoint/event-time cursors, RNG,
native runtime logs/history, native attribution fields, events, observables,
and current native producer configuration are represented by native identity.

RCAE role/access semantics, derived evidence overlays, ecology-owned state,
interventions, controls/matching, future inputs, fixture/cycle, metric,
calibration, analysis, registration, and execution identity remain externally
composed. Private reset baseline is unsupported unless explicitly composed;
otherwise reset-dependent branching is blocked.

### 10.4 Gate and evidence effect

`P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`. I03 may use exact
admitted contracts to select or reject a realization, but it must itself decide
the realization class, carrier, dependence mode, composite identity, provider
configuration, response, and controls.

Source admission proves permitted dependency identity. Provider admission
proves an available identity contract. Digest agreement proves canonical
identity consistency. None proves restoration correctness, a pool, causal
adequacy, ecological support, a boundary rung, or an L02 result.

### 10.5 Reopening conditions

Reopen DEC-008 if:

- any admitted revision/path/digest/import/signature no longer reconstructs;
- a provider input is accepted or rejected outside the retained contract;
- any continuation-relevant component lacks native, external, or unsupported
  disposition;
- later work uses reset without the registered restriction/composite identity;
- provider choice changes without realization/registration configuration;
- fallback occurs after an exception or provider mismatch;
- identity equality is promoted to restoration correctness or continuation; or
- I03 meaning, candidate behavior, or scientific evidence is attributed to
  I02/I02R1.

## 11. `P2-I2-DEC-009` — Updated reset-baseline source and provider admission

**Status:** accepted from retained I02R2 evidence

**Question ID:** `L02-Q02`

**Question:** Does updated PyGRC preserve the declared `reset()` baseline
across snapshot/save/load, represent baseline-only differences in a distinct
restoration identity, and fail closed for legacy or malformed data without
opening I03 scientific choices?

### 11.1 Authority and validation

Admit clean graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594` under the exact 31-source and
31-public-callable scope in the
[I02R2 manifest](../contracts/p2-i2/i02r2-admitted-source-and-reset-provider-manifest.json).
The prior revision
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`, DEC-007/008, and the I02R1
reset restriction remain historical authority; they are not rewritten.

Evidence:

- [I02R2 revalidation](../reports/P2-I2-I02R2-reset-baseline-persistence-revalidation.md);
- [machine validation](../contracts/p2-i2/i02r2-reset-baseline-validation.json);
- [exact source transition](../contracts/p2-i2/i02r2-graph-source-transition.json);
  and
- [I02R2 input freeze](../contracts/p2-i2/i02r2-reset-baseline-revalidation-input-freeze.json).

Imports and every manifest callable resolve under the admitted checkout. All
manifest, revision, and worktree SHA-256 values match. Focused upstream checks
passed with 68 tests and 32 subtests; the independent validator retained no
candidate behavior and the graph repository remained clean.

### 11.2 Reset lifecycle decision

Admit the following native lifecycle contract:

```text
set_state(state)        preserves the existing baseline
rebase_reset_baseline() explicitly adopts current state as baseline
reset()                 restores the available declared baseline
save/load               preserves current state and declared baseline
```

The baseline is serialized as non-recursive `pygrc.reset_baseline` version 1
state with the same family and parameter hash as the outer snapshot. Original
and loaded models reset identically, and three repeated save/load cycles retain
the baseline.

Legacy absence is not silently converted into a checkpoint baseline. Current
state loads, but reset and v2 identity raise `SnapshotCompatibilityError`
until explicit rebase. Rebase begins a prospective declared lifecycle and does
not recover historical construction provenance. Any RCAE use of that route
must externally retain `explicit_rebase_from_legacy_checkpoint` and
`historical_construction_baseline_recovered=false`.

### 11.3 Provider transition

Retain v1 unchanged as current-state identity and admit v2 as available for
conditional later selection:

```text
v1 = current native state
v2 = current-state identity v1 + reset-baseline identity v1

selected_provider = null
```

Generic equal-current-state models with different reset baselines retained
equal v1 digests and different v2 digests. V2 fails closed when baseline state
is unavailable or malformed. Its digest is SHA-256 over UTF-8 PyGRC canonical
JSON and matched independent recomputation.

I03 may propose v2 only for a compatible realization. I06 must freeze exact
provider/schema, persisted-versus-rebased baseline provenance, and all RCAE
external identity before branch comparison. Provider choice remains
configuration, never exception recovery.

### 11.4 Gate and evidence effect

`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`. The I02R1
blanket reset prohibition is removed only for valid persisted-baseline state
under a later registered v2 policy. Legacy/unavailable state remains blocked
until explicit registered rebase.

This decision validates a native persistence and identity contract. It does
not select a realization, provider, carrier, dependence mode, response,
comparator, control, or branch point; does not cover RCAE-owned state; and does
not establish unrestricted continuation equivalence or scientific evidence.

### 11.5 Reopening conditions

Reopen if the updated revision/path/digest/import/signature fails, reset
diverges across save/load, v2 fails to distinguish reset baselines, v1 is
silently redefined, legacy/malformed data no longer fails closed, rebase is
treated as historical recovery, provider selection changes silently, or I03
meaning/scientific evidence is attributed to I02R2.

## 12. Pending decision queue

No item below is decided by this record yet:

| Proposed decision | Earliest iteration | Prerequisite |
| --- | --- | --- |
| Realization class and native/producer boundary | I03 | I01R1–I02 dispositions |
| Dependence mode and causal interfaces | I03 | Selected realization |
| Primary raw response and orientation | I04 | Discriminator gate |
| Closest primary comparator | I04 | Realization-bound insufficient-repetition alternatives |
| Candidate-blind matched null and analysis identity | I04 | Frozen response/comparator |
| Exact implementation and registration bundle | I06 | Frozen calibration |
| Candidate cycle authorization | I07 | Passed registration |
| Terminal classification and next move | I11 | Resolved controls and reconstruction |

Pending items may not be answered by convenience, code availability, or
candidate outcomes outside their named iteration.
