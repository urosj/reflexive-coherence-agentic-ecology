# P2-I2 Shared-Pool Co-Conditioning Checklist

**Status:** active; I02R2 reset-baseline source/provider revalidation passed;
I03 ready but not begun

**Iteration:** `P2-I2`

**Lane:** `AE01-L02`

**Current activity iteration:** none; `P2-I2-I02R2` complete and
`P2-I2-I03` ready but not begun

**Current local gate:** `P2-I2-BRIEF-GATE=passed`;
`P2-I2-SOURCE-AUDIT-GATE=passed_after_revalidation`;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`

**Acceptance ceiling:** `AE01-C2`; no P2-I2 result, cross-lane recurrence, or
N31+ effect assigned

**Semantic authority:**
[accepted P2-I2 brief](P2-I2-shared-pool-co-conditioning-brief.md)

**Operational hypothesis projections:**
[P2-I2 operational hypotheses](../hypotheses/p2-i2-operational-hypotheses.md)

**Cumulative lane decisions:**
[P2-I2 decision record](P2-I2-decision-record.md)

**Frozen authorities:**
[L02 hypothesis](../hypotheses/lane-hypotheses.md),
[post-R3 ecology-discriminator amendment](../hypotheses/post-r3-ecology-discriminator-amendment.md),
[outcome and stopping contract](../hypotheses/outcome-and-stopping-contract.md),
[developmental interpretation contract](../hypotheses/developmental-interpretation-contract.md),
[L02 metric sheet](../contracts/metric-sheets/AE01-L02.json),
[execution policy](../configs/p1_i5_execution_policy.json), and
[P1-I5 tooling contract](P1-I5-tooling-contract.md)

**Program cover:** [Post-N30 master checklist](../../../implementation/PostN30-checklist.md)

## 1. How to use this checklist

This is the detailed planning, activity, evidence, and learning surface for
P2-I2. The master checklist records stable cover gates. This file projects the
common lane contract and the accepted P2-I2 brief into named lane-local
iterations.

The operating rule is:

> No P2-I2 activity occurs off-ledger. Every audit, decision campaign,
> artifact-construction step, calibration, registration action, execution,
> control resolution, reconstruction, interpretation, or closeout is a named
> checklist iteration with retained evidence.

An activity iteration must declare before work begins:

```text
iteration_id
purpose
entry_authority
frozen_inputs_or_input_freeze_action
mutation_and_repository_boundary
required_outputs
evidence_effect
exit_gate
```

Checkbox convention:

```text
[ ] pending, blocked, unresolved, or not yet demonstrated
[x] completed with cited retained evidence or explicit disposition
```

Rules:

- A checked evidential item cites an accepted decision, retained artifact,
  reconstruction, report, or owner disposition.
- Creating or editing this checklist is itself recorded in the active
  iteration before the iteration closes.
- Reading a source to design an audit does not count as completing the audit.
  Preparatory observations carry no capability, source-admission, realization,
  calibration, or result authority.
- An iteration may prepare the next iteration's inputs, but it cannot silently
  perform or pass that next iteration.
- The checklist is living between candidate probe cycles and frozen within a
  probe cycle.
- Every evidence-triggered addition receives a change ID and names the
  affected iteration and rerun scope.
- Scientific changes after calibration require a new preregistration and a
  separately frozen candidate cycle; infrastructure retries cannot carry
  scientific refinement.
- Native, producer-assisted, constructed, and ecology-owned state roles remain
  explicit throughout.
- The graph/PyGRC repository remains read-only from RCAE.
- A conflict with a frozen Phase 1 authority reopens that authority; it cannot
  be resolved inside this checklist.
- No terminal checkbox can be inferred from a positive metric alone.

## 2. Local gate dashboard

| Gate | Meaning | Status | Exit evidence or blocker |
| --- | --- | --- | --- |
| `P2-I2-BRIEF-GATE` | L02 semantic center, D-039 delta, dependence modes, causal factorization, controls, timing, and claim ceiling accepted | Passed | Owner acceptance dated 2026-07-14; `P2-I2-DEC-001`; accepted brief |
| `P2-I2-SOURCE-AUDIT-GATE` | Source-current public PyGRC capability audit completed under one frozen audit scope | Passed after revalidation | I01R1 quarantines the custom probe, corrects CAP-04, and revalidates all claims from admissible evidence |
| `P2-I2-SOURCE-ADMISSION-GATE` | Exact graph sources and any restoration-profile transition admitted for lane use | Passed after I02R2 revalidation | Updated revision `83e3a300426631ee4df71b661b67d4fcfdfed594`, 31 sources/callables, persisted reset baseline, v1/v2 provider boundary, legacy fail-closed policy, and `P2-I2-DEC-009` |
| `P2-I2-DISCRIMINATOR-GATE` | Realization, dependence mode, factorization, access witness, and subordinate operational hypotheses frozen | Ready; not begun | I01R1 audit and I02R2 source/provider admission passed; requires named I03 input freeze and disposition |
| `P2-I2-CAL-PRE-GATE` | Candidate-blind null, response, comparator, signed controls, and analysis identity preregistered | Blocked | Requires `DISCRIMINATOR-GATE` |
| `P2-I2-CAL-GATE` | Reconstructable matched-null calibration freezes `delta` without candidate input | Blocked | Requires `CAL-PRE-GATE` |
| `P2-I2-REG-GATE` | Exact realization, cells, controls, identities, artifacts, and reconstruction bundle accepted | Blocked | Requires `CAL-GATE` |
| `P2-I2-EXEC-FREEZE` | One exact candidate cycle authorized before its first operation | Blocked | Requires `REG-GATE` and a cycle-specific freeze |
| `P2-I2-EXEC-GATE` | Frozen finite matrix completes or closes validly blocked/incomplete | Blocked | Requires `EXEC-FREEZE` |
| `P2-I2-CONTROL-GATE` | Every mandatory common and L02 control receives a retained fail-closed disposition | Blocked | Requires the relevant registered executions |
| `P2-I2-RECON-GATE` | Retained evidence, identities, and reports reconstruct independently | Blocked | Requires execution/control artifacts or a valid earlier blocked bundle |
| `P2-I2-INTERPRET-GATE` | Boundary rungs, metric relation, support, two-axis reading, debts, and next move resolve | Blocked | Requires reconstruction |
| `P2-I2-CLOSE-GATE` | One terminal classification and compact control-resolution index close the lane | Blocked | Requires all applicable prior gates |

`P2-I2-GATE` in the master checklist is equivalent to
`P2-I2-CLOSE-GATE` here.

## 3. Stable entry and claim boundaries

- [x] `P1-GATE` passed. Evidence: [R2 closeout](../reports/R2-closeout.md).
- [x] Review R3 passed and requires a compact lane-local control-resolution
  index before P2-I2 terminal closure. Evidence:
  [R3 review](../reports/R3-contract-adequacy-review.md).
- [x] Stable lane ID is `AE01-L02`.
- [x] Frozen hypothesis authority is `AE01-H-L02`.
- [x] The accepted post-R3 D-039 amendment applies before calibration.
- [x] The P2-I2 brief is accepted as lane-local semantic authority. Evidence:
  `P2-I2-DEC-001`.
- [x] The operational hypotheses are subordinate projections, not new lane
  hypotheses or schema vocabulary.
- [x] Frozen maximum claim is
  `bounded shared-pool co-conditioning demand pattern`.
- [x] The seven Phase 1 L02 logical cells and five L02 controls remain fixed.
- [x] Nonlinearity is optional; joint functional dependence is mandatory.
- [x] Native support is preferred when adequate; a minimal explicit producer
  or constructed mechanism remains allowed when native support is absent or
  inadequate.
- [x] Graph revision
  `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5` is the exact historical I02R1
  admission and remains retained provenance.
- [x] Updated graph revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594` is the exact I02R2 admission;
  this source identity alone selects no provider or realization.
- [x] No source audit, source admission, realization selection, calibration,
  registration, candidate execution, control outcome, or P2-I2 result is
  inferred from brief preparation.
- [x] Collective memory, communication, resource economy, cooperation,
  coordination, agency, organism, native pool primitive, motif, regime, life,
  cross-lane recurrence, and N31+ selection remain blocked.

## 4. Activity-iteration ledger

| Iteration | Activity | Entry dependency | Status | Exit gate/effect |
| --- | --- | --- | --- | --- |
| `P2-I2-I00` | Authority bootstrap: brief acceptance, checklist, operational-hypothesis scaffold, and cumulative decision record | Owner acceptance | Complete | `P2-I2-BRIEF-GATE=passed`; no scientific evidence |
| `P2-I2-I00R1` | Post-bootstrap artifact review, provenance correction, and compact validation retention | I00 plus external review | Complete | `P2-I2-CHG-001`; brief gate remains passed |
| `P2-I2-I01` | Source-current PyGRC capability audit | I00R1 | Complete as executed; corrected by I01R1 | Historical audit disposition retained; current gate effect owned by I01R1 |
| `P2-I2-I01R1` | Capability-audit closeout revalidation and candidate-probe quarantine review | I01 plus owner-supplied closeout review | Complete; probe quarantined, CAP-04 corrected, static audit revalidated | `P2-I2-SOURCE-AUDIT-GATE=passed_after_revalidation` |
| `P2-I2-I02` | Source admission and restoration-profile transition disposition | I01R1 | Complete | `P2-I2-SOURCE-ADMISSION-GATE=passed`; no scientific evidence |
| `P2-I2-I02R1` | Admission closeout revalidation: identity, authority, imported-package provenance, callable/provider contract, and transition boundary | I02 plus owner-supplied closeout review | Complete; governance/import/provider/coverage package revalidated | `P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`; no scientific evidence |
| `P2-I2-I02R2` | Updated PyGRC reset-baseline persistence and restoration-identity revalidation | I02R1 plus updated graph revision supplied by project owner | Complete; reset persistence and v2 identity validated, updated source admitted | `P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`; no scientific evidence |
| `P2-I2-I03` | Realization, discriminator, dependence-mode, and operational-hypothesis freeze or missing-prerequisite classification | I01R1–I02R2 | Ready; not begun | `P2-I2-DISCRIMINATOR-GATE` or retained earlier-stop route |
| `P2-I2-I04` | Candidate-blind calibration preregistration construction | I03 | Blocked | `P2-I2-CAL-PRE-GATE` |
| `P2-I2-I05` | Matched-null calibration execution and metric-sheet freeze | I04 | Blocked | `P2-I2-CAL-GATE` |
| `P2-I2-I06` | Exact implementation registration and evidence-bundle construction | I05 | Blocked | `P2-I2-REG-GATE` |
| `P2-I2-I07` | Candidate-cycle execution freeze | I06 | Blocked | `P2-I2-EXEC-FREEZE` |
| `P2-I2-I08` | Finite live candidate/control matrix execution | I07 | Blocked | `P2-I2-EXEC-GATE` |
| `P2-I2-I09` | Control resolution and compact index generation | I08 or valid earlier stop | Blocked | `P2-I2-CONTROL-GATE` |
| `P2-I2-I10` | Retained-evidence reconstruction and identity verification | I08–I09 or valid earlier stop | Blocked | `P2-I2-RECON-GATE` |
| `P2-I2-I11` | Developmental interpretation, terminal classification, and lane closeout | I09–I10 | Blocked | `P2-I2-INTERPRET-GATE`, then `P2-I2-CLOSE-GATE` |

No iteration may be marked complete merely because a later iteration produced
an artifact that should have been created earlier. Missing iteration evidence
fails closed and must be reconstructed or explicitly classified.

## 5. `P2-I2-I00` — Authority bootstrap

**Purpose:** establish accepted semantic authority and the lane-local process
surfaces before any capability or realization work begins.

**Evidence effect:** none; authority and process only.

**Mutation boundary:** P2-I2 narrative artifacts and stable navigation only;
no graph-repository writes, runtime probes, calibration, registration, or
candidate execution.

- [x] Project owner explicitly accepted the revised P2-I2 brief on
  2026-07-14.
- [x] Brief status records owner acceptance without assigning evidence.
- [x] This evidence-expandable checklist exists and makes every later activity
  a named iteration.
- [x] Subordinate operational-hypothesis projections reside under the
  experiment's `hypotheses/` authority surface and are indexed there without
  selecting a realization, dependence mode, response, comparator, or outcome.
- [x] One cumulative P2-I2 decision record exists.
- [x] `P2-I2-DEC-001` retains the accepted semantic and claim boundaries.
- [x] `P2-I2-DEC-002` retains the checklist-first, no-off-ledger activity rule.
- [x] `P2-I2-DEC-003` retains the subordinate operational-hypothesis lifecycle.
- [x] Brief-preparation inspection is explicitly not counted as I01 audit
  evidence.
- [x] Capability audit, source admission, realization selection, calibration,
  registration, and execution remain unopened.

### 5.1 I00 construction and validation record — 2026-07-14

- [x] P2-I1's accepted checklist and cumulative-decision conventions plus R3's
  proportionality constraints were inspected only to scaffold P2-I2 process;
  no P2-I1 conclusion or realization was reused as evidence.
- [x] All local Markdown links from the brief, checklist, decision record,
  operational hypotheses, and lane indexes resolve to existing files.
- [x] The checklist contains exactly the declared I00–I11 activity sequence,
  and the hypothesis artifact contains OP-01 through OP-09.
- [x] Required Phase 1 L02 cell, control, rung, metric, and D-039 identities
  remain present in the accepted brief and linked artifacts.
- [x] `git diff --check` and trailing-whitespace scans passed for the complete
  I00 documentation change.
- [x] The graph/PyGRC worktree remained clean after I00 validation.
- [x] The validation did not execute the I01 capability questions, admit the
  candidate graph revision, or run PyGRC candidate behavior.

Compact reconstructable evidence for these checks is retained in the
[I00 validation provenance](../reports/P2-I2-I00-validation.md).

### 5.2 `P2-I2-I00R1` — Post-bootstrap review correction

**Status:** complete

**Trigger:** the owner-supplied artifact-stack review received after I00.

**Change ID:** `P2-I2-CHG-001`

**Evidence effect:** integrity and process clarification only; no capability,
source-admission, calibration, or lane evidence.

- [x] Acceptance provenance was checked against the actual conversation and
  workspace. The explicit owner statement “yes, it is acceptance” supports
  DEC-001 and the accepted brief; the review's stale draft-status premise does
  not reopen `P2-I2-BRIEF-GATE`.
- [x] DEC-002 is identified as an explicit owner-directed process decision;
  DEC-003 is identified as derived and accepted under the I00 package rather
  than a separate owner statement.
- [x] I01 now distinguishes authorized input-freeze construction from
  unauthorized source inspection, API invocation, and conformance checks.
- [x] I03 owns causal intervention meaning, held-fixed variables, qualitative
  expected relations, and fail-closed scientific interpretation.
- [x] I04 owns exact measurement and machine evaluation without revising I03's
  causal expectations.
- [x] I05 retains a separate metric-calibration record and generated frozen
  metric-sheet artifact rather than mutating the base L02 sheet.
- [x] I08 now quantifies exact matrix-entry execution and explicitly retains
  `reference-pool` responses.
- [x] OP-09 is a falsifiable bounded-retention projection with supported,
  not-supported, and blocked/incomplete readings.
- [x] Compact validation provenance retains commands, exit codes, checked
  files, graph status, and authority-package digests.
- [x] No I01 source inspection occurred during I00R1.

Exit gate `P2-I2-BRIEF-GATE`:

```text
accepted brief + checklist + subordinate hypothesis scaffold
+ cumulative decision record + no evidence overclaim
= passed
```

Disposition: `P2-I2-I00=complete` and `P2-I2-BRIEF-GATE=passed`.
This opens only the input-freeze work for I01.

## 6. `P2-I2-I01` — Source-current capability audit

**Status:** complete; Section 6.1 input freeze preceded source inspection, all
questions and outputs are retained, and the graph checkout remained unchanged.

**Purpose:** determine which public surfaces of one exact source-current PyGRC
revision can natively express the accepted L02 discriminator and which are
absent or inadequate.

**Evidence effect:** capability and missing-surface classification only; no
source admission, realization selection, calibration, or lane result.

Writing and reviewing the audit scope, permitted commands, identity boundary,
and output contract is authorized now. Reading additional graph/PyGRC source
files for capability classification, invoking public APIs, or running
conformance checks begins only after every Section 6.1 input-freeze item is
checked with retained evidence.

### 6.1 Input freeze before audit activity

Frozen artifact:
[I01 audit-input freeze](../contracts/p2-i2/i01-audit-input-freeze.json).

- [x] Record the exact graph repository revision and worktree state to audit.
  Evidence: clean `main` checkout at
  `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`.
- [x] Freeze the repository-relative file/API scope and audit questions.
- [x] Freeze allowed read-only commands and any non-mutating conformance checks.
- [x] Declare whether installed-package inspection is needed and how package
  identity will be separated from checkout identity.
- [x] Freeze output paths for the narrative audit, machine-readable capability
  matrix if needed, command provenance, and file-digest inventory.
- [x] Record that audit failure or absence cannot become a negative L02 result.

The freeze fixes eleven question IDs (`P2-I2-CAP-01` through
`P2-I2-CAP-11`), the `adequate` / `inadequate` / `absent` / `unresolved`
classification contract, checkout-only package identity, graph read-only
boundaries, fixed output paths, and the change-control rule for any audit-scope
correction. Its entry-authority digests bind the accepted state at RCAE commit
`430f77206790c2d27b8283e58d4b8a58737a7ad3` before this checklist advanced
I01 to source inspection.

The first in-scope packaging-manifest read showed that the checkout package
root is `src/pygrc/**`. `P2-I2-CHG-002` added that exact tracked path and fixed
checkout import root before any package source file was read or any capability
was classified. No rerun was required.

### 6.2 Required capability questions

- [x] Is there a public native non-private carrier with reconstructible
  identity and declared access scope? Disposition: one declared node-coherence
  carrier is `adequate`; pool role/access semantics remain RCAE declarations.
- [x] Can at least two attributable contribution paths alter one carrier
  without source-private response reads? Disposition: `adequate` through
  multiple native packets crediting one target while lineage stays in the
  separate packet ledger.
- [x] Is there a carrier-scoped read, susceptibility, or eligibility path that
  does not require contributor addressing? Disposition: `adequate` through the
  native feedback-eligibility surface and feedback producer.
- [x] Can encounter state, active history, or both persist and be intervened on
  independently of audit metadata? Disposition: `adequate` for encounter-state
  mode; no native aggregate pool-history object was established.
- [x] Can the audit-only label permutation and common-carrier intervention be
  expressed without causal bypass? Disposition: `adequate`; the audit probe
  retained invariant causal projections under swapped lineage labels.
- [x] Can pool write freeze and mode-relevant clamp interventions be expressed?
  Disposition: `inadequate` as a complete native surface; route/producer
  withdrawal is available, but no atomic pool-specific gate/clamp exists.
- [x] Can a private-partition counterfactual preserve marginal contributions
  and opportunity without recreating a common state? Disposition: native
  topology primitives exist, but the matched-control/no-common-read contract
  is `inadequate` and remains RCAE-orchestrated.
- [x] Are reserve, accumulation, mixing, depletion, saturation, leakage, and
  maintenance observable or classifiably inapplicable? Disposition: reserve,
  accumulation/mixing, and depletion are native; generic capacity/saturation,
  leakage, and maintenance are `inadequate` beyond passive conserved mode.
- [x] What native state is covered by restoration identity, and what ecology
  pool/intervention state would remain external? Disposition: native node,
  queue, ledger, routes, histories, producer configuration, events, and
  observables are covered; RCAE roles, controls, schedules, and any constructed
  state remain external.
- [x] Does each candidate surface classify as `adequate`, `inadequate`,
  `absent`, or `unresolved`, with a precise reason and evidence reference?
  Evidence: [capability matrix](../contracts/p2-i2/i01-capability-matrix.json).
- [x] What is the smallest producer or constructed transition needed for each
  otherwise promising inadequate surface? Evidence: CAP-06 through CAP-11 and
  the narrative audit's minimal-demand table; no fallback is selected.

### 6.3 Audit outputs and exit

- [x] Retain one [narrative capability-audit report](../reports/P2-I2-I01-source-current-capability-audit.md).
- [x] Retain one compact requirement-to-surface matrix or explicitly justify
  why the report itself is the compact projection.
- [x] Retain exact source revision, source paths, callable names, relevant file
  digests, and command provenance.
- [x] Separate public API facts, inferred adequacy, missing surfaces, and open
  questions.
- [x] Record a bounded shortlist or a classified absence without selecting the
  P2-I2 realization.
- [x] Record all audit-derived decisions in the cumulative decision record.
  Evidence: `P2-I2-DEC-005`.
- [x] Validate that no graph-repository file changed. Evidence: frozen revision
  unchanged and final `git status --short` empty.

Exit gate `P2-I2-SOURCE-AUDIT-GATE`:

```text
frozen audit scope + complete capability matrix + exact provenance
+ native adequacy classifications + missing-surface distinctions
+ no source admission or lane-result overclaim
= passed
```

Disposition: `P2-I2-I01=complete` and
`P2-I2-SOURCE-AUDIT-GATE=passed` at original closeout. I01R1 has since
reopened that gate for fail-closed review; this historical disposition is not
the current gate state.

## 6A. `P2-I2-I01R1` — Capability-audit closeout revalidation

**Status:** complete; this subsection was frozen before any revalidation
inspection or classification beyond reading the owner-supplied review that
triggered the iteration.

**Iteration ID:** `P2-I2-I01R1`

**Purpose:** test the I01 package against the supplied capability-audit
closeout standard, quarantine any inadmissible candidate behavior from I01
evidence, and determine whether the source-audit gate can be re-passed from
admissible source-current evidence alone.

**Entry authority:** accepted P2-I2 brief, I01 input freeze and retained
outputs, cumulative decisions through `P2-I2-DEC-005`, and the owner-supplied
I01 closeout review received 2026-07-14.

**Frozen inputs and scope:** exact graph revision
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`; the retained I01 freeze,
narrative, matrix, provenance, source digests, decision, checklist, and
operational-hypothesis projection; and the thirteen review sections plus ten
final closeout conditions in the supplied review. Static read-only inspection
may revisit only the I01-frozen graph scope. No new dynamic candidate,
combined-versus-single, response, calibration, or boundary-rung probe is
authorized.

**Mutation and repository boundary:** RCAE P2-I2 governance, audit, matrix,
provenance, and revalidation-report artifacts only. The graph repository
remains read-only. Existing commands and outputs may be retained for
historical provenance while being explicitly excluded from capability or
scientific evidence.

**Required outputs:** one retained I01R1 revalidation report; an admissibility
disposition for every I01 command/evidence class; corrected audit, matrix,
decision, checklist, hypotheses, and navigation where required; exact
integrity validation; and either a re-passed source-audit gate or a retained
precise blocker.

**Evidence effect:** capability-audit validity and process correction only.
No source admission, realization or dependence-mode choice, calibration,
candidate evidence, control outcome, or L02 result.

### 6A.1 Frozen revalidation checks

- [x] Verify exact revision/worktree, path/callable/command scope, package
  identity, scope corrections, and the separation from brief preparation.
- [x] Validate the complete native causal composition without treating a bag
  of APIs or ecology-side reduction/injection as adequate.
- [x] Recheck the one-pool, attribution-only, public-support, intervention,
  and active-runtime-versus-audit-log boundaries.
- [x] Recheck state/history-mode neutrality without binding a realization or
  dependence mode.
- [x] Recheck restoration callable/digest/input/ownership/continuation
  boundaries and retain a state-ownership table.
- [x] Revalidate all eleven classifications under exactly the four frozen
  values and distinguish source facts, audit inferences, adequacy judgments,
  and open questions.
- [x] Revalidate minimal producer/constructed demands without selecting a
  design, response, comparator, or control matrix.
- [x] Confirm the shortlist remains bounded and non-selective.
- [x] Classify every executable I01 check as admissible interface evidence or
  quarantined candidate behavior; candidate behavior cannot support I01.
- [x] Cross-check narrative/matrix/provenance/digests/decisions/checklist,
  portable identities, stable IDs, reopening conditions, and graph status.

### 6A.2 Exit disposition

- [x] Retain the [I01R1 revalidation report](../reports/P2-I2-I01R1-capability-audit-closeout-revalidation.md)
  and all required corrections.
- [x] Demonstrate that every surviving capability claim is supported without
  quarantined candidate behavior.
- [x] Re-pass `P2-I2-SOURCE-AUDIT-GATE` or record the exact failed condition
  and keep I02 blocked.

Exit rule:

```text
all thirteen review areas + all ten final closeout conditions
+ candidate-behavior quarantine
+ capability matrix support from admissible evidence alone
+ no later-gate decision or evidence
+ unchanged graph worktree
= source-audit gate re-passed; otherwise fail closed
```

## 7. `P2-I2-I02` — Source admission and restoration transition

**Status:** complete as executed; corrected and revalidated by I02R1;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`.

**Purpose:** admit only the source identities relevant to the selected next
decision and define any explicit restoration-provider transition.

**Iteration ID:** `P2-I2-I02`

**Entry authority:** accepted P2-I2 brief; corrected I01/I01R1 audit package;
`P2-I2-DEC-006`; RCAE entry revision
`10c18fad2ba8ecac9ddacb0f0bc55813e6356c60`.

**Frozen-input action:** construct and validate
[the I02 source-admission input freeze](../contracts/p2-i2/i02-source-admission-input-freeze.json)
from retained I01R1 evidence before recomputing a graph digest, rereading a
graph source/callable for admission, importing PyGRC, or writing an admission
disposition.

**Mutation and repository boundary:** RCAE P2-I2 contract, report, decision,
checklist, hypothesis-prerequisite, source-inventory, navigation, and master-
governance artifacts only. The graph repository remains read-only. Generated
temporary validation output may exist only under `/tmp`.

**Required outputs:** frozen I02 input contract; admitted-source digest and
callable manifest or reviewed non-admission record; narrative source-admission
and restoration-transition report; source-inventory update; cumulative
decision; checklist/evidence/change ledgers; integrity validation.

**Evidence effect:** exact source and provider admission only. No realization,
dependence-mode, response, comparator, calibration, candidate, control,
boundary-rung, or L02-result effect.

### 7.1 Input freeze before admission activity

- [x] Bind the exact RCAE entry revision, proposed graph revision, clean
  worktree requirement, and repository-relative identity rule.
- [x] Freeze the I01R1-derived proposed runtime-source, evidence-source, and
  public-callable scopes without treating them as admitted.
- [x] Freeze native-provider inputs, unsupported inputs, identity/digest
  distinction, external-state boundary, and prior/fallback-provider question.
- [x] Freeze the bounded equal-input continuation obligation separately from
  identity equality; do not execute it in I02.
- [x] Freeze read-only commands, output paths, classification values, change
  control, and fail-closed/non-evidence rules.
- [x] Validate the input-freeze JSON and record that only the freeze may be
  constructed before all preceding checks are complete.

Passing Section 7.1 authorizes only the exact read-only source-admission review
frozen there. It does not itself admit a source or provider.

The first in-scope runtime read exposed omitted public construction, queue-
processing, save, reset, and route-configuration callables before any admission
role or provider decision was assigned. `P2-I2-CHG-004` updates the freeze to
version `1.0.1`; the complete callable review was rerun before admission
closure.

### 7.2 Admission and provider disposition

- [x] Select the exact graph revision proposed for admission from I01 evidence.
- [x] Recompute and retain admitted file digests from that revision.
- [x] Bind repository revision, source files, runtime/package identity, and
  public callable identity without machine-local paths.
- [x] Bind native restoration identity and digest callables when applicable.
- [x] State accepted input scope and unsupported inputs.
- [x] Declare ecology-owned pool, producer, intervention, and configuration
  state outside native identity.
- [x] Declare the prior/fallback identity provider and its allowed scope.
- [x] Forbid silent provider upgrade or downgrade.
- [x] Define bounded equal-input continuation obligations separately from
  restoration-identity equality.
- [x] Preserve the graph closeout claim boundary.
- [x] Update the AE01 source inventory or retain a reviewed non-admission
  disposition.

### 7.3 Outputs and exit

- [x] Retain the admitted-source digest/callable manifest or reviewed non-
  admission record.
- [x] Retain the narrative source-admission and restoration-transition report.
- [x] Record all I02 decisions and evidence/change-ledger additions.
- [x] Validate JSON, portable paths, callable/source references, digests,
  Markdown links, graph revision/status, and no-I03-overreach.

Exit gate `P2-I2-SOURCE-ADMISSION-GATE` requires exact admitted identities or a
reviewed absence/inadequacy disposition. It grants no calibration or execution
authority.

## 7A. `P2-I2-I02R1` — Admission closeout revalidation

**Status:** complete;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_revalidation`.

**Trigger:** owner-supplied I02 closeout review received 2026-07-14.

**Change ID:** `P2-I2-CHG-005`

**Purpose:** independently revalidate I02 as an exact identity, authority, and
provider-transition result; correct any retention/governance defects without
selecting an I03 realization or treating restoration identity as restoration
correctness.

**Entry authority:** accepted P2-I2 brief; I01R1 audit package; I02 freeze,
manifest, report, source-inventory update, `P2-I2-DEC-007`, and checklist state
at review entry; owner-supplied I02 closeout review.

**Frozen-input action:** retain and validate an I02R1 closeout-review input
freeze that binds all entry artifact digests, the exact graph revision, the
review's fourteen areas and twelve gate conditions, read-only commands,
environment-bootstrap boundary, required outputs, and no-I03/no-evidence
rules before inspecting new graph source ranges, importing PyGRC, or running a
provider conformance check.

**Mutation and repository boundary:** RCAE P2-I2 contracts, reports,
validation script, decisions, checklist, hypothesis prerequisite, source
inventory, navigation, master governance, ignored local `.venv`, and `/tmp`
validation artifacts only. The graph repository remains read-only.

**Required outputs:** frozen I02R1 input contract; CHG-004 predecessor/current
freeze transition record; corrected admitted-source/provider manifest;
retained generic validator plus import-provenance and provider-contract
validation record; complete identity-coverage table; I02R1 narrative
revalidation; corrected source inventory, decision/checklist/change/evidence
ledgers, and navigation; integrity validation.

**Evidence effect:** admission integrity and provider-contract authority only.
No realization, dependence mode, response, comparator, calibration, candidate,
control, boundary-rung, restoration-correctness, or L02-result effect.

### 7A.1 Input freeze

- [x] Bind exact RCAE review-entry artifact digests separately from graph
  revision and graph file digests.
- [x] Freeze all review questions, source/callable/provider/coverage checks,
  CHG-004 governance checks, cross-artifact checks, and I03-leakage scan.
- [x] Freeze a generic imported-package provenance check that cannot execute
  candidate behavior.
- [x] Authorize ignored RCAE `.venv` creation only if needed for the frozen
  generic checks; forbid dependency substitution and graph-repository writes.
- [x] Freeze outputs, classification values, failure effects, and change
  control.
- [x] Parse and validate the I02R1 input contract before new review activity.

### 7A.2 Identity, authority, and provider checks

- [x] Reconstruct exact source identity, revision existence, clean/unchanged
  worktree, repository-relative paths, digests, and separate RCAE entry state.
- [x] Classify every source by runtime, public API, contract/schema, evidence/
  closeout, test/conformance, or documentation role as applicable.
- [x] Tie raw imported `pygrc` and callable provenance to the admitted checkout
  and normalize only the stable manifest identity.
- [x] Reconstruct CHG-004's predecessor scope, correct its governance class,
  retain predecessor/current semantic and file digests, and rerun the complete
  callable review without retaining an incomplete-scope conclusion.
- [x] Bind every public symbol's signature/accepted shape, source digest,
  supported/unsupported scope, causal relevance, and claim boundary.
- [x] Independently validate restoration-provider input rejection, identity
  determinism/canonicality, digest algorithm/encoding/recomputation, and raw-
  snapshot distinction without claiming restoration correctness.
- [x] Retain complete continuation-relevant native/external/unsupported
  identity coverage and block later branching on any unresolved component.
- [x] Revalidate conditional admission, configured provider selection,
  no-silent-fallback, provider-match, and identity-versus-continuation rules.
- [x] Revalidate lane-scoped non-retroactive source inventory and cross-
  artifact agreement.
- [x] Confirm no I03 scientific choice or positive evidence leaked into I02.

### 7A.3 Outputs and exit

- [x] Retain all required corrected machine and narrative artifacts.
- [x] Record `P2-I2-DEC-008`, CHG-005, evidence-ledger additions, and any
  exact correction to DEC-007 without erasing its historical disposition.
- [x] Run final JSON, digest, import/callable, provider, path/link, checklist,
  claim-boundary, graph-read-only, and `git diff --check` validation.
- [x] Re-pass `P2-I2-SOURCE-ADMISSION-GATE` or retain the exact failed
  condition and keep I03 blocked.

## 7B. `P2-I2-I02R2` — Reset-baseline persistence revalidation

**Status:** complete;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`.

**Trigger:** project owner reports that PyGRC has been updated to correct the
reset-baseline persistence gap retained by I02R1.

**Change ID:** `P2-I2-CHG-006`

**Purpose:** determine whether updated PyGRC preserves the public `reset()`
baseline across native snapshot/save/load restoration and covers that baseline
in the restoration identity, without selecting an I03 realization or treating
generic restoration conformance as scientific evidence.

**Entry authority:** accepted P2-I2 brief; I01R1 audit; I02/I02R1 admission
package and `P2-I2-DEC-008`; clean updated graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594`; owner request dated 2026-07-14.

**Frozen-input action:** before inspecting changed graph source or executing a
reset check, retain and validate an I02R2 input freeze binding the old and new
graph revisions, clean/read-only worktree, RCAE entry authority, changed-path
discovery rule, reset/snapshot/save/load/provider contract questions, generic
fixtures, legacy-compatibility checks, required outputs, and no-I03/no-evidence
boundary.

**Mutation and repository boundary:** RCAE P2-I2 contracts, validator, report,
decision, checklist, hypothesis prerequisite, source inventory, navigation,
and master governance only. PyGRC remains read-only. Generated validation
artifacts may be retained in RCAE or written temporarily under `/tmp`.

**Required outputs:** I02R2 input freeze; exact old-to-new graph source and
public-contract transition; checkout-bound reset/provider validator and
machine record; narrative revalidation; updated or failed admission manifest;
source inventory, decision, checklist/change/evidence ledgers, hypothesis
prerequisite, navigation, and integrity checks.

**Evidence effect:** source/provider restoration conformance only. No
realization, carrier, dependence mode, response, comparator, calibration,
candidate, control, restoration correctness beyond the tested generic reset
contract, boundary rung, or L02 result.

### 7B.1 Input freeze

- [x] Bind exact RCAE entry authority and old/new graph revisions separately.
- [x] Require graph worktree cleanliness before and after every check.
- [x] Freeze changed-path discovery plus affected source/callable/provider
  scope before reading changed implementation ranges.
- [x] Freeze generic reset-baseline fixtures and prohibit P2-I2 candidate
  behavior.
- [x] Freeze output paths, failure effects, change control, and I03 blocking.
- [x] Parse and validate the I02R2 freeze before source inspection or runtime
  validation.

### 7B.2 Reset and identity validation

- [x] Verify exact changed source/test/contract identities and checkout-bound
  imports at the updated revision.
- [x] Determine the declared reset-baseline serialization schema, provider
  schema/version transition, and legacy snapshot policy.
- [x] Show that a model and its native save/load restoration have equal current
  identity and equal `reset()` outcomes.
- [x] Show that reset-baseline-only differences change restoration identity or
  otherwise fail closed before branch comparison.
- [x] Show that repeated save/load cycles preserve the reset baseline.
- [x] Verify `set_state()` and any explicit rebasing operation follow their
  declared baseline semantics without silent rebasing.
- [x] Verify malformed or unsupported reset-baseline payloads fail according
  to the declared compatibility contract, with no fallback.
- [x] Confirm the old I02R1 reset restriction is removed only if every affected
  contract passes and the new source revision is admitted.

### 7B.3 Outputs and exit

- [x] Retain machine and narrative validation with exact source/import/test
  provenance and no candidate behavior.
- [x] Record `P2-I2-DEC-009`, CHG-006, source-inventory/manifest transition,
  and all affected hypothesis/checklist/navigation updates.
- [x] Run JSON, digest, import/provider, link/path, claim-boundary,
  graph-read-only, and `git diff --check` validation.
- [x] Re-pass `P2-I2-SOURCE-ADMISSION-GATE` or retain the exact failed
  condition and keep I03 blocked.

## 8. `P2-I2-I03` — Realization and operational-hypothesis freeze

**Status:** ready but not begun; requires its own recorded input freeze before
realization work.

**Purpose:** choose one bounded realization and instantiate the subordinate
operational hypotheses without changing `AE01-H-L02`.

I03 freezes causal meaning: intervention targets, causally held-fixed
variables, qualitative invariance/divergence or direction, and the fail-closed
scientific interpretation. It does not define numerical resolution or a
machine pass rule.

- [ ] Select and justify one realization class—native, producer-assisted, or
  constructed—or retain why no bounded realization can preserve the
  discriminator.
- [ ] Record every native-adequacy and producer-minimality consequence.
- [ ] Select exactly one `pool_dependence_mode`: `state_carried`,
  `history_carried`, or admissible `hybrid`.
- [ ] If `hybrid`, separately declare encounter state and active history,
  register one intervention for each while matching the other, freeze both
  expected relations, and fail lower/mixed if separation cannot be obtained.
- [ ] Bind the common carrier identity, non-private access witness, sources,
  contribution operations, and audit lineage.
- [ ] Bind the `C_P`/`L`/`V` causal factorization to actual runtime interfaces.
- [ ] Demonstrate that arbitrary attribution labels do not enter the response
  path.
- [ ] Bind the mode-appropriate common-carrier intervention and jointness
  counterfactual.
- [ ] Map all nine operational projections to cells, controls, expected
  qualitative relations, causally held-fixed variables, and fail-closed
  scientific effects.
- [ ] Preserve all seven logical cells and five L02 controls.
- [ ] Freeze the private-partition competitor and non-private access witness.
- [ ] Record unresolved measurement choices for I04 rather than silently
  selecting them here.

Exit gate `P2-I2-DISCRIMINATOR-GATE` requires a complete realization-bound
operational hypothesis family and opens calibration preregistration only. If
no bounded realization can preserve the discriminator, I03 may instead retain
a reviewed missing-prerequisite disposition and route to I09–I11 without
passing this gate or opening calibration.

## 9. `P2-I2-I04` — Calibration preregistration construction

**Status:** blocked on `P2-I2-DISCRIMINATOR-GATE`.

I04 imports I03's causal expectations unchanged. It freezes their exact raw
measurement, equality/resolution rule, numerical orientation, primary
comparator, aggregation, missingness, and machine-executable
pass/ambiguous/fail evaluation. Numerical operationalization may not revise an
I03 qualitative causal expectation.

- [ ] Freeze one raw later-response family and orientation.
- [ ] Freeze the primary candidate response and closest registered
  insufficient-repetition comparator with rationale.
- [ ] Freeze aggregation, pairing, normalized-margin, denominator-floor, and
  missingness policies shared by calibration and live analysis.
- [ ] Freeze a candidate-blind matched-null generator and prove candidate and
  runtime exclusion.
- [ ] Freeze calibration inputs, seeds, resource limit, expected artifacts,
  reconstruction command, and stopping rule.
- [ ] Convert every imported qualitative expectation and fail-closed effect
  into an exact measurement, equality/resolution rule, and machine-executable
  pass/ambiguous/fail evaluation.
- [ ] Freeze raw-response retention for all cells and subconfigurations.
- [ ] Freeze analysis code/policy identity and change-control boundary.
- [ ] Validate the preregistration without running the candidate or matched
  null.

Exit gate `P2-I2-CAL-PRE-GATE` authorizes only I05 matched-null calibration.

## 10. `P2-I2-I05` — Candidate-blind calibration

**Status:** blocked on `P2-I2-CAL-PRE-GATE`.

- [ ] Execute only the frozen matched-null calibration.
- [ ] Retain reconstructable generator provenance and all per-seed margins.
- [ ] Verify candidate/runtime exclusion and absence of post-hoc inputs.
- [ ] Compute and freeze `delta` under the metric-sheet estimator.
- [ ] Retain a lane-local metric-calibration record and generated frozen
  metric-sheet artifact linked to the unchanged base L02 metric sheet;
  populate only the frozen artifact's designated resolution-status, `delta`,
  rationale, and calibration-reference fields.
- [ ] Retain schema-valid calibration and provenance records.
- [ ] Reconstruct the calibration independently and verify semantic digests.
- [ ] Preserve narrow/robust language as relation to frozen resolution, not a
  terminal verdict.

Exit gate `P2-I2-CAL-GATE` opens registration construction only.

## 11. `P2-I2-I06` — Exact implementation registration

**Status:** blocked on `P2-I2-CAL-GATE`.

- [ ] Bind exact source, runtime, realization, analysis, and restoration
  identities.
- [ ] Materialize exact source/carrier/write/read and common-state/audit-lineage
  mappings.
- [ ] Materialize all seven logical cells and five lane controls, including
  signed subconfigurations.
- [ ] Freeze the primary comparator and all mandatory secondary controls.
- [ ] Freeze contribution amounts, order/timing, mixing, support, reserve,
  leakage, maintenance, saturation, and applicability dispositions.
- [ ] Freeze branch-point and complete composite restoration identity.
- [ ] Freeze seeds, attempts, one infrastructure-retry scope, resources,
  isolation, and contamination checks.
- [ ] Freeze expected artifacts, manifests, reconstruction commands, report
  assembly, and claim boundary.
- [ ] Retain an explicit registration evidence bundle and compact summary.
- [ ] Prepare the lane-local control-resolution-index template as a projection,
  not evidence.
- [ ] Validate registration without executing a candidate operation.

Exit gate `P2-I2-REG-GATE` does not itself authorize execution.

## 12. `P2-I2-I07` — Candidate-cycle execution freeze

**Status:** blocked on `P2-I2-REG-GATE`.

- [ ] Assign a unique candidate cycle ID.
- [ ] Bind the exact tracked source/runtime, registration, calibration, policy,
  code, and manifest identities.
- [ ] Freeze the finite cell/seed/attempt/resource matrix.
- [ ] Freeze infrastructure-retry eligibility separately from scientific
  change.
- [ ] Freeze stop conditions, expected receipts, graph read-only guard, and
  candidate-effect boundary.
- [ ] Verify that no candidate operation preceded this freeze.
- [ ] Retain a cycle-scoped authorization review.

Exit gate `P2-I2-EXEC-FREEZE` authorizes only the named exact cycle.

## 13. `P2-I2-I08` — Finite matrix execution

**Status:** blocked on a cycle-scoped `P2-I2-EXEC-FREEZE`.

- [ ] Execute every registered matrix entry—cell × subconfiguration × seed ×
  allowed attempt—exactly once, except for its one preregistered eligible
  infrastructure retry.
- [ ] Retain per-run runtime receipts, raw responses, state identities,
  operation order, costs, leakage, and failures.
- [ ] Preserve every `reference-pool`, individual-source, combined-order,
  shuffle, label-permutation, removal, freeze/clamp, private-partition,
  controller/direct-path, quantity-matched, and transfer-contrast response.
- [ ] Stop under the frozen rule without adding rescue variants.
- [ ] Retain incomplete or blocked evidence without converting it into a
  negative scientific result.
- [ ] Generate and validate the execution manifest.

Exit gate `P2-I2-EXEC-GATE` records completion state only; it does not assign
the terminal class.

## 14. `P2-I2-I09` — Control resolution

**Status:** blocked on registered control evidence or a valid earlier stop.

- [ ] Resolve every applicable common control.
- [ ] Resolve all five L02 controls and every required subconfiguration.
- [ ] Distinguish planned applicability, resolution stage, observed outcome,
  and fail-closed effect.
- [ ] Preserve mode-specific invariance and divergence expectations.
- [ ] Preserve ambiguous outcomes rather than forcing pass/fail.
- [ ] Generate one compact lane-local control-resolution index from retained
  evidence.
- [ ] Verify that the index introduces no new evidence or schema authority.

Exit gate `P2-I2-CONTROL-GATE` fails closed on every unresolved mandatory
control.

## 15. `P2-I2-I10` — Reconstruction and identity verification

**Status:** blocked on retained evidence.

- [ ] Reconstruct calibration, registration, execution, controls, and reports
  from the resolved manifest.
- [ ] Verify semantic digests, portable paths, schema, unsafe-claim flags, and
  graph read-only evidence.
- [ ] Verify restoration identity separately from raw snapshot observations.
- [ ] Run bounded equal-input continuation checks where registered.
- [ ] Recompute every per-seed margin and threshold relation.
- [ ] Verify no missing artifact is silently replaced or regenerated with new
  scientific inputs.

Exit gate `P2-I2-RECON-GATE` requires an independently auditable retained
bundle or a valid earlier blocked/incomplete bundle.

## 16. `P2-I2-I11` — Interpretation and closeout

**Status:** blocked on control resolution and reconstruction.

- [ ] Assign all five L02 boundary-rung dispositions.
- [ ] Preserve every per-seed metric relation without scalar collapse.
- [ ] Assign support status, T0–T4 classification value, realization class,
  and one terminal state independently.
- [ ] Record expected, adjacent, unexpected, null, mixed, and counter-
  directional observations.
- [ ] Record separate becoming and development readings.
- [ ] Preserve native, producer, construction, medium, leakage, transfer,
  measurement, composition, semantic, and claim debts as applicable.
- [ ] Separate the observed relation from the LGRC demand implication.
- [ ] State the strongest valid claim and every blocked relabel.
- [ ] Record one next move with a falsifier under D-038.
- [ ] Retain a human-readable report, machine terminal records, updated atlas
  projections, and the compact control-resolution index.
- [ ] Stop P2-I2 after one complete terminal classification.

Exit gate `P2-I2-CLOSE-GATE`:

```text
valid terminal classification + reconstructed evidence
+ resolved mandatory controls + lowest honest boundary
+ bounded next move + claim ceiling preserved
= passed
```

## 17. Open-question and decision-timing ledger

| Question ID | Question | Earliest iteration | Status | Decision/evidence |
| --- | --- | --- | --- | --- |
| `L02-Q00` | Which public PyGRC surfaces could carry one pool? | I01/I01R1 | Decided for audit | `P2-I2-DEC-006`: node coherence + native packet contribution + feedback response composition candidate |
| `L02-Q01` | Is any native surface adequate to the L02 discriminator? | I01/I01R1 | Decided for audit | `P2-I2-DEC-006`: composition-capable native surfaces exist; complete realization adequacy is not assigned and control gaps remain |
| `L02-Q02` | Which graph sources and restoration provider are admitted? | I02/I02R1/I02R2 | Decided after reset revalidation | `P2-I2-DEC-009`: updated checkout-bound identities admitted; v1 current-only and v2 reset-aware providers available but unselected; legacy rebase provenance remains external; P2-I1 projection historical-only |
| `L02-Q03` | Which realization class is selected? | I03 | Open | I01R1–I02 required |
| `L02-Q04` | Which dependence mode applies? | I03 | Open | Realization required |
| `L02-Q05` | What are the exact sources, carrier, factorization, and access witness? | I03 | Open | Realization required |
| `L02-Q06` | What contribution and mixing rule constitutes common state or active history? | I03 | Open | Realization required |
| `L02-Q07` | Which one later response is primary? | I04 | Open | Discriminator gate required |
| `L02-Q08` | Which nearest insufficient-repetition comparator owns the margin? | I04 | Open | Discriminator gate required |
| `L02-Q09` | What matched null and resolution freeze `delta`? | I04–I05 | Open | Calibration only |
| `L02-Q10` | How do all cells and signed controls materialize? | I03 concept; I06 exact | Open | Registration pending |
| `L02-Q11` | How are pool economy properties observed or dispositioned? | I03 concept; I06 exact | Open | Registration pending |
| `L02-Q12` | Which capacity, contributor, or access contrast tests R05? | I03 concept; I06 exact | Open | Registration pending |

Questions may move only through cumulative decisions. A later answer must not
rewrite an earlier retained decision without its reopening condition.

## 18. Evidence-triggered checklist change control

Every addition after I00 receives an ID:

```text
P2-I2-CHG-NNN
triggering_iteration
triggering_evidence
change_class
added_or_revised_items
affected_gate
rerun_scope
preserved_result_or_boundary
status
```

Allowed change classes are:

- `audit_scope_correction` before I01 completion;
- `source_admission_scope_correction` before the affected admission closes or
  during a named admission revalidation;
- `source_admission_revision_update` during a named revalidation when an
  upstream admitted dependency revision changes;
- `audit_evidence_quarantine` preserving historical provenance;
- `infrastructure_correction` with no scientific change;
- `scientific_refinement` requiring new preregistration/cycle;
- `control_or_measurement_expansion` with explicit gate/rerun effect;
- `hypothesis_projection_revision` preserving `AE01-H-L02` authority;
- `aim_redescription_or_redirect`; or
- `closure_only_retention_fix`.

No change may erase a null, negative, blocked, incomplete, or inconvenient
result. No checklist expansion may serve only to obtain support.

### 18.1 Change ledger

| Change ID | Triggering iteration/evidence | Class | Revision | Gate/rerun effect | Preserved boundary | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `P2-I2-CHG-001` | I00R1 owner-supplied artifact-stack review | `closure_only_retention_fix` plus pre-execution clarification | Acceptance provenance/status roles; I01 authorization wording; I03/I04 boundary; I05 metric artifact policy; I08 matrix quantification; OP-09 falsifiability; compact validation evidence | No gate reopened; no rerun; `BRIEF-GATE` remains passed and I01 source inspection remains unopened | Accepted brief, frozen L02/D-039 authorities, no P2-I2 evidence, graph read-only boundary | Complete |
| `P2-I2-CHG-002` | I01 in-scope `pyproject.toml` package-root declaration | `audit_scope_correction` | Add tracked `src/pygrc/**`; bind checkout-only imports to `${GRC}/src` | No gate reopened; no rerun because no package source or capability classification preceded the correction | Exact graph revision, read-only boundary, public-surface/classification/output contracts, no-evidence effect | Complete |
| `P2-I2-CHG-003` | I01R1 owner-supplied capability-audit closeout review | `audit_evidence_quarantine` plus `closure_only_retention_fix` | Quarantine candidate-shaped custom probe; rerun classifications from admissible static/generic-test evidence; correct CAP-04 to inadequate; add mode-neutral, public-support, intervention, causal-history, and restoration-ownership checks | Source-audit gate reopened during I01R1 and re-passed after corrected static revalidation; no candidate rerun | Full historical probe provenance, exact graph revision, graph read-only boundary, no source admission/realization/calibration/result | Complete |
| `P2-I2-CHG-004` | I02 first in-scope LGRC9V3 runtime read | `source_admission_scope_correction` (corrected by I02R1 before re-passing the admission gate) | Add public construction, queue-processing, save, reset, and route-configuration methods omitted from the frozen callable list; no source path added | Complete 24-symbol review rerun before original disposition and enriched I02R1 review; predecessor semantics/current file retained under explicit limits | Exact revisions/source paths, graph read-only and no-candidate rules, output/classification contracts, no-realization/no-evidence effect | Complete after I02R1 revalidation |
| `P2-I2-CHG-005` | I02R1 owner-supplied identity/authority/transition closeout review | `closure_only_retention_fix` plus `source_admission_scope_correction` | Reopen admission gate; correct CHG-004 governance; retain imported-package provenance, granular roles/callable contracts, provider validation, identity coverage, explicit invariants, and cross-artifact/no-I03 checks | All fourteen review areas and twelve gate conditions passed; source-admission gate re-passed; I03 ready | Historical I02 provenance and DEC-007, exact graph revision, read-only boundary, conditional authority, no restoration-correctness/scientific evidence | Complete |
| `P2-I2-CHG-006` | I02R2 owner-reported upstream PyGRC reset-baseline correction at revision `83e3a300426631ee4df71b661b67d4fcfdfed594` | `source_admission_revision_update` | Reopen exact graph source/provider admission; validate reset-baseline persistence, identity coverage, schema transition, and compatibility policy before re-admission | Full affected/effective source/import/callable/provider review, 68 tests plus 32 subtests, and generic reset-conformance rerun passed; I03 readiness restored | Historical I02/I02R1 provenance, graph read-only boundary, provider remains unselected, no realization/scientific evidence | Complete |

## 19. Evidence ledger

| Evidence ID | Iteration | Artifact or disposition | Evidence effect | Status |
| --- | --- | --- | --- | --- |
| `P2-I2-I00-BRIEF` | I00 | Accepted P2-I2 brief | Semantic authority only | Retained |
| `P2-I2-I00-CHECKLIST` | I00 | This checklist | Process and gate authority only | Retained |
| `P2-I2-I00-OPHYP` | I00 | [Operational-hypothesis scaffold](../hypotheses/p2-i2-operational-hypotheses.md) | Subordinate projection only | Retained |
| `P2-I2-I00-DECISIONS` | I00/I00R1/I01/I01R1/I02/I02R1/I02R2 | Cumulative decision record, DEC-001 through DEC-009 | Decision authority only | Retained |
| `P2-I2-I00-VALIDATION` | I00R1 | [Compact validation provenance](../reports/P2-I2-I00-validation.md) | Integrity/process only | Retained |
| `P2-I2-I00R1-REVIEW` | I00R1 | Section 5.2 review disposition and `P2-I2-CHG-001` | Process correction only | Retained |
| `P2-I2-I01-FREEZE` | I01 | [Audit-input freeze](../contracts/p2-i2/i01-audit-input-freeze.json) | Preregistered capability-audit scope and process only | Retained |
| `P2-I2-I01-AUDIT` | I01 | [Narrative audit](../reports/P2-I2-I01-source-current-capability-audit.md) | Public capability and missing-surface classification only | Retained |
| `P2-I2-I01-MATRIX` | I01 | [Capability matrix](../contracts/p2-i2/i01-capability-matrix.json) | Compact native adequacy and producer-demand projection only | Retained |
| `P2-I2-I01-PROVENANCE` | I01 | [Command provenance](../reports/P2-I2-I01-command-provenance.md) and [source digests](../contracts/p2-i2/i01-source-digests.json) | Reconstructibility and integrity only | Retained |
| `P2-I2-I01R1-REVALIDATION` | I01R1 | [Capability-audit closeout revalidation](../reports/P2-I2-I01R1-capability-audit-closeout-revalidation.md), `P2-I2-CHG-003`, and `P2-I2-DEC-006` | Audit validity/process correction only; quarantined probe has no capability or scientific effect | Retained |
| `P2-I2-I02-FREEZE` | I02 | [Source-admission input freeze](../contracts/p2-i2/i02-source-admission-input-freeze.json) version 1.0.1 and `P2-I2-CHG-004` | Preregistered source/provider review scope and scope correction only | Retained |
| `P2-I2-I02-ADMISSION` | I02 | [Admitted-source and restoration manifest](../contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json), [transition report](../reports/P2-I2-I02-source-admission-and-restoration-transition.md), source-inventory update, and `P2-I2-DEC-007` | Exact source/provider admission only; no realization or scientific evidence | Retained |
| `P2-I2-I02R1-FREEZE` | I02R1 | [Closeout-review input freeze](../contracts/p2-i2/i02r1-closeout-review-input-freeze.json) | Preregistered identity/authority/provider review only | Retained |
| `P2-I2-I02R1-VALIDATION` | I02R1 | [CHG-004 transition](../contracts/p2-i2/i02r1-chg-004-freeze-transition.json), [validator output](../contracts/p2-i2/i02r1-identity-authority-validation.json), and [revalidation report](../reports/P2-I2-I02R1-admission-closeout-revalidation.md) | Admission integrity/provider-contract authority only; reset boundary retained; no restoration correctness or scientific evidence | Retained |
| `P2-I2-I02R2-FREEZE` | I02R2 | [Reset-baseline revalidation input freeze](../contracts/p2-i2/i02r2-reset-baseline-revalidation-input-freeze.json) | Preregistered updated-source/reset/provider review only | Retained |
| `P2-I2-I02R2-SOURCE` | I02R2 | [Exact graph source transition](../contracts/p2-i2/i02r2-graph-source-transition.json) and [updated admission manifest](../contracts/p2-i2/i02r2-admitted-source-and-reset-provider-manifest.json) | Exact updated source/provider authority only | Retained |
| `P2-I2-I02R2-VALIDATION` | I02R2 | [Machine reset validation](../contracts/p2-i2/i02r2-reset-baseline-validation.json), [validator](../scripts/p2_i2_i02r2_validate.py), and [revalidation report](../reports/P2-I2-I02R2-reset-baseline-persistence-revalidation.md) | Generic reset/provider conformance only; no realization or scientific evidence | Retained |

The ledger expands only when a named iteration retains evidence. It never
lists an intended artifact as though it already exists.
