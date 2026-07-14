# P2-I2 Shared-Pool Co-Conditioning Checklist

**Status:** active; staged `P2-I2-I03`; I03A/I03AR1 state-carried package is
owner-accepted for progression, I03B/I03BR1 is owner-accepted for staged
progression, and I03C hybrid passed 258/258 byte-reconstructed runtime
conformance; I03CR1 passed its 26/26, 17/17 zero-runtime closeout revalidation
with zero blockers and is owner-accepted for progression; the separately
declared I03F compact family closeout passed 12/12 integration checks and 9/9
acceptance conditions with zero blockers and is owner-accepted; the
discriminator gate is passed; I04R2 confirmed all conditional machine
invariants with 16/16 focused checks and 7/7 pure tests after correcting the
future I05 estimator route; the project owner accepted I04R2 as the sole
progression authority and passed CAL-PRE; original I04 and I04R1 are immutable
historical artifacts; the I05B/I05C authority was owner-approved and committed;
the single governed arithmetic null completed once with zero retries; DEC-032
retains the corrected I05D portability audit of 135 files with 312
value-redacted violations in 70 files; DEC-033 now has the first eleven-file
I05 portability group review-ready with 10/10 checks and zero remaining group
violations; DEC-034 retains that group at `6dd6898`; I05F has a 10/10
technical result and zero remaining group violations; DEC-035 accepts its
13-versus-three process deviation in place without rewriting the freeze or
rerunning validation; DEC-036 accepts the complete package and authorizes its
commit without opening a later group

**Iteration:** `P2-I2`

**Lane:** `AE01-L02`

**Current activity iteration:** `P2-I2-I05F`; the owner-accepted first I05
correction group is retained at `6dd6898`; the exact second I04/I05
authority-dependency correction group is owner-accepted and commit-authorized
under DEC-036 with 10/10 checks, zero remaining group findings, and an
owner-accepted additive process-deviation closeout under DEC-035; no later
group is open, and metric-sheet freeze, CAL-GATE, I06, and every scientific or
candidate operation remain closed

**Current local gate:** `P2-I2-BRIEF-GATE=passed`;
`P2-I2-SOURCE-AUDIT-GATE=passed_after_revalidation`;
`P2-I2-SOURCE-ADMISSION-GATE=passed_after_i02r2_revalidation`;
`P2-I2-DISCRIMINATOR-GATE=passed`;
`P2-I2-CAL-PRE-GATE=passed_after_explicit_owner_acceptance_of_I04R2`;
`P2-I2-CAL-GATE=closed_pending_portability_correction_and_review`

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
| `P2-I2-BRIEF-GATE` | L02 semantic center, D-039 delta, dependence modes, causal factorization, controls, timing, and claim ceiling accepted | Passed after mode-family scope clarification | Owner acceptance dated 2026-07-14; `P2-I2-DEC-001`; owner-accepted three-mode retention correction `P2-I2-DEC-011`; accepted brief |
| `P2-I2-SOURCE-AUDIT-GATE` | Source-current public PyGRC capability audit completed under one frozen audit scope | Passed after revalidation | I01R1 quarantines the custom probe, corrects CAP-04, and revalidates all claims from admissible evidence |
| `P2-I2-SOURCE-ADMISSION-GATE` | Exact graph sources and any restoration-profile transition admitted for lane use | Passed after I02R2 revalidation | Updated revision `83e3a300426631ee4df71b661b67d4fcfdfed594`, 31 sources/callables, persisted reset baseline, v1/v2 provider boundary, legacy fail-closed policy, and `P2-I2-DEC-009` |
| `P2-I2-DISCRIMINATOR-GATE` | Realization, dependence mode, factorization, access witness, and subordinate operational hypotheses frozen | Passed after owner acceptance of compact I03F | DEC-020; opens I04 construction only; all three modes remain retained and unranked |
| `P2-I2-CAL-PRE-GATE` | Candidate-blind null, response, comparator, signed controls, and analysis identity preregistered | Passed after explicit owner acceptance of I04R2 | DEC-026 accepts I04R2 as sole progression authority after 16/16 checks and 7/7 pure tests; opens only separately frozen single-invocation I05 arithmetic calibration; no null/runtime/candidate execution occurred at passage |
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
- [x] State-carried, history-carried, and hybrid are retained as three
  mode-specific realizations through registration, execution, control
  resolution, and interpretation. Selection is among native, minimally
  producer-assisted, or missing-prerequisite dispositions within each mode;
  the three modes are not candidates in a winner-selection step. Evidence:
  owner acceptance dated 2026-07-14 and `P2-I2-DEC-011`.
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
| `P2-I2-I03` | Staged realization, discriminator, dependence-mode, and operational-hypothesis program | I01R1–I02R2 plus owner staging direction | Complete and owner-accepted through compact I03F under DEC-020 | `P2-I2-DISCRIMINATOR-GATE=passed`; opened only I04 |
| `P2-I2-I03A` | 8A state-carried realization and operational-hypothesis freeze | I02R2 plus owner staging direction | Causal design accepted as I03AR1 baseline; runtime adequacy unassigned | `P2-I2-I03A-REVIEW-READY`; opened only I03AR1 under DEC-012 |
| `P2-I2-I03AR1` | 8A-R1 quarantined state-carried realization runtime conformance | Owner acceptance of stronger conformance path after I03A review | Owner accepted for progression on 2026-07-14; scientific effect remains none | Opens I03B only under its own declaration/freeze; does not open I03C/I04 |
| `P2-I2-I03B` | 8B history-carried realization, operational-hypothesis freeze, and bounded runtime conformance | Owner acceptance/progression direction after I03AR1 | Owner accepted for staged progression on 2026-07-14; minimally producer-assisted design and 252/252 runtime conformance retained | Opens I03C only under DEC-015; no scientific or I04 effect |
| `P2-I2-I03BR1` | I03B closeout revalidation of latest-contact dataflow, active-history identity, producer minimality, lifecycle, restoration, and quarantine | I03B plus owner-supplied validation review | Complete and owner accepted for progression; 21/21 checks, six downstream obligations, zero blockers | `P2-I2-I03BR1-CLOSEOUT-PASSED`; obligations retained for I04/I06 |
| `P2-I2-I03C` | 8C hybrid realization, operational-hypothesis freeze, and bounded runtime conformance | Owner acceptance of I03B/I03BR1 under DEC-015 | Owner accepted for staged progression on 2026-07-14; minimally producer-assisted design and 258/258 byte-reconstructed runtime conformance retained | Opens I03F only under its own declaration/freeze; no scientific or direct I04 effect |
| `P2-I2-I03CR1` | 8C-R1 zero-runtime hybrid causal-well-formedness and acceptance closeout revalidation | I03C plus owner-supplied twenty-six-point/seventeen-condition review | Complete and owner accepted for progression; 26/26 review checks, 17/17 acceptance conditions, eight downstream obligations, zero blockers | `P2-I2-I03CR1-CLOSEOUT-PASSED`; opened I03F only |
| `P2-I2-I03F` | 8.1 compact zero-runtime umbrella three-mode family closeout | Owner acceptance/progression direction after I03C/I03CR1 | Complete and owner accepted; 12/12 integration checks and 9/9 acceptance conditions passed with zero blockers | `P2-I2-DISCRIMINATOR-GATE=passed`; opens I04 construction only |
| `P2-I2-I04` | Three-mode calibration preregistration construction | Passed discriminator gate under owner-accepted I03F | Static package validated, but owner review withheld CAL-PRE passage and reopened the comparator/window/null boundary | Superseded for progression by I04R1; retained history only |
| `P2-I2-I04R1` | I04-R1 comparator, order, analytic-null, fixed-window, B-purity, mode-isolation, and evidence-derived-chain correction | Owner-supplied critical review of I04 | Complete immutable historical correction; 19/19 focused checks and 15/15 pure tests | Superseded for progression by owner-accepted I04R2; no independent execution authority |
| `P2-I2-I04R2` | Conditional two-arm estimator, diversion, response-gain, window, diagnostic, order, and causal-receipt machine verification | Owner-supplied conditional I04R1 acceptance review | Complete and owner-accepted; 16/16 focused checks and 7/7 pure tests; future I05 bypass and reconstruction enforcement corrected | Sole I04 progression authority; `P2-I2-CAL-PRE-GATE=passed`; opens only separately frozen I05 authorization |
| `P2-I2-I05` | Matched-null calibration execution and metric-sheet freeze under the preregistered shared/mode-specific rule | Owner-accepted I04R2 and passed CAL-PRE | Single arithmetic-null attempt completed with one builder call and zero retries; metric-sheet closeout remains blocked on portability review | `P2-I2-CAL-GATE` |
| `P2-I2-I05A` | Pre-acceptance one-shot consumption, committed-authority revalidation, and readback-only reconstruction safety audit | Owner-supplied three-item execution-safety review of the I05 candidate | Complete: 3/8 passed, five blockers, zero governed execution; no source correction | Proposed DEC-027 blocked; cannot open I05 execution or CAL-GATE |
| `P2-I2-I05B` | I05-owned one-shot wrapper, policy, claim/final receipt, committed-authority preflight, and zero-null safety correction | Explicit owner authorization after I05A | Owner-accepted: 12/12 tests, 12/12 checks, byte reconstruction; I04R2 immutable; commit authorized, null launch separate | Accepted authority package committed under DEC-029/CHG-022 |
| `P2-I2-I05C` | Pre-claim active-repository-venv command/target identity correction | Final 10.4 preflight failure plus owner direction “always use venv” | Owner-approved and committed at `9d81f15`; 13/13 tests and 12/12 checks preceded the later single attempt | Historical authority; current portable projections governed by I05E |
| `P2-I2-I05D` | P2-I2-wide persisted-path portability audit | Owner rule that absolute paths are never allowed | Accepted exact inventory: 312 value-redacted findings in 70 of 135 files | Opens one reviewed I05E correction group at a time |
| `P2-I2-I05E` | First bounded historical-to-portable correction group | Owner acceptance of I05D and authorization of the I05 group | Complete and retained at `6dd6898`: 10/10 checks, zero group violations, 13/13 focused helper tests | Opens only I05F under DEC-034; CAL-GATE remains closed |
| `P2-I2-I05F` | I04/I05 authority-dependency historical-to-portable correction | Owner acceptance/commit of I05E and direction to continue | Owner-accepted and commit-authorized: 10/10, 30 to zero findings, original freeze retained, and 13-versus-three process deviation accepted additively under DEC-035/036 | Retain complete package; no later group or CAL-GATE passage |
| `P2-I2-I06` | Exact three-mode implementation registration and evidence-bundle construction | I05 | Blocked | `P2-I2-REG-GATE` |
| `P2-I2-I07` | Mode-indexed candidate-cycle execution freeze | I06 | Blocked | `P2-I2-EXEC-FREEZE` |
| `P2-I2-I08` | Finite live three-mode candidate/control matrix execution | I07 | Blocked | `P2-I2-EXEC-GATE` |
| `P2-I2-I09` | Mode-specific control resolution and compact index generation | I08 or valid earlier stop | Blocked | `P2-I2-CONTROL-GATE` |
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

## 8. `P2-I2-I03` — Staged realization and operational-hypothesis program

**Status:** in progress through three review-separated mode sub-iterations.

**Purpose:** instantiate the subordinate operational hypotheses for all three
declared dependence modes without changing `AE01-H-L02`, resolving only one
mode per owner-reviewed sub-iteration.

Owner direction dated 2026-07-14 fixes this order and boundary:

```text
8A / P2-I2-I03A = state_carried
owner review
8B / P2-I2-I03B = history_carried
owner review
8C / P2-I2-I03C = hybrid
owner review
```

No later mode may be inspected, bound, or resolved inside an earlier mode's
sub-iteration. The umbrella discriminator gate remains open until the staged
program is complete and reviewed. This staging direction arrived after the
generic I03 input freeze validated but before realization comparison or
selection; `P2-I2-CHG-007` narrows that freeze to 8A without undoing a
scientific choice.

### 8.0 Owner-accepted mode-family retention correction

`P2-I2-CHG-008` records the project owner's 2026-07-14 acceptance of the
following scope rule before further I03A work:

```text
P2-I2 retains and tests state_carried, history_carried, and hybrid.
No later iteration selects one of those modes as the winner.
Within each mode, native is preferred when adequate; otherwise the smallest
adequate producer-assisted realization or a reviewed missing prerequisite is
retained.
```

- [x] Record the clarification in this active I03 checklist before editing the
  brief, hypothesis projection, decision record, or downstream iteration
  descriptions.
- [x] Preserve the original I03A input freeze and its entry digests; the
  clarification is a later owner-authorized scope transition, not a
  retrospective rewrite of what preceded state-carried comparison.
- [x] Correct the brief's singular `selected dependence mode` and `selected
  realization` language under `P2-I2-DEC-011`.
- [x] Require I04–I11 artifacts to remain mode-indexed and prohibit
  convenience-, availability-, calibration-, or outcome-based mode dropping.
- [x] Retain one bounded lane-level terminal classification while preserving
  separate realization, calibration, execution, control, and interpretation
  dispositions for all three modes.
- [x] Revalidate the current I03A package after the scope correction without
  executing a candidate, cell, control, matched null, or calibration action.

This accepted correction changes downstream scope but does not accept or
revise `P2-I2-DEC-010`, authorize I03B/I04, or assign scientific evidence.

### 8A. `P2-I2-I03A` — State-carried realization freeze

**Status:** causal design accepted by the project owner as the immutable
I03AR1 baseline; runtime adequacy and scientific support remain unassigned.

#### 8A.1 I03A activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03A
purpose = freeze one bounded state-carried realization, discriminator,
          interventions, and state-carried OP-01..OP-09 profile
entry_authority = RCAE 26811d395c0662473629d5710983e3c1fdb4f58f;
                  admitted PyGRC 83e3a300426631ee4df71b661b67d4fcfdfed594;
                  I01R1 and I02R2 passed
frozen_inputs_or_input_freeze_action = construct and validate the scoped
                  contracts/p2-i2/i03a-state-carried-realization-freeze-input.json
                  before implementation-surface comparison
mutation_and_repository_boundary = RCAE I03A contracts, hypotheses, decisions,
                  report, checklist, and navigation only; graph/PyGRC read-only;
                  no candidate, calibration, or matched-null execution
required_outputs = I03A input freeze; state-carried realization/discriminator
                   contract; state-carried operational-hypothesis profile;
                   I03A report; DEC-010; checklist disposition
evidence_effect = causal preregistration authority only; no calibration,
                  candidate evidence, control result, or L02 support result
exit_gate = P2-I2-I03A-REVIEW-READY; stop for owner review without starting
            I03B or opening I04
```

- [x] Record the I03A activity declaration before realization work.
- [x] Revise and parse the scoped I03A input freeze; retain exact entry
  revisions and authority digests while binding state-carried-only questions,
  the review stop, native-first selection rule, mutation boundary, required
  outputs, and failure effects. Evidence:
  [`i03a-state-carried-realization-freeze-input.json`](../contracts/p2-i2/i03a-state-carried-realization-freeze-input.json),
  SHA-256 `34d0903c746fb67abff5a1c12bb252b5cb15933d2de75e56f1232fbe7dfd0845`;
  15/15 entry digests and all 12 state-carried questions validated.
- [x] Confirm the graph/PyGRC worktree is clean at the admitted revision before
  reading admitted implementation sources for I03A. Evidence: exact revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594`, clean after scoped-freeze
  validation.

The initial generic I03 freeze validated before the owner's staging direction:

- [x] Fifteen of fifteen entry-revision authority digests and all twelve
  generic questions validated in the same turn. Its pre-staging SHA-256 was
  `fb96012b3d353a0e0f8d69827317f0610d60a69f2b1b1bf16a167119ef9b51d2`.
- [x] The graph/PyGRC worktree was clean at admitted revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594` before the staging direction.

I03A freezes causal meaning for `state_carried`: intervention targets,
causally held-fixed variables, qualitative invariance/divergence or direction,
and fail-closed scientific interpretation. It does not define numerical
resolution or a machine pass rule.

Evidence for every checked I03A design item below is
[`i03a-state-carried-realization-and-discriminator-contract.json`](../contracts/p2-i2/i03a-state-carried-realization-and-discriminator-contract.json),
[`P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md`](../reports/P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md),
`P2-I2-DEC-010`, and the
[static validation](../contracts/p2-i2/i03a-state-carried-realization-validation.json).

- [x] Select and justify one state-carried realization class—native,
  producer-assisted, or constructed—or retain why no bounded state-carried
  realization can preserve the discriminator.
- [x] Record every state-carried native-adequacy and producer-minimality
  consequence.
- [x] Bind `pool_dependence_mode = state_carried`; do not compare or bind
  `history_carried` or `hybrid` profiles in I03A.
- [x] Bind the common encounter-state carrier identity, non-private access
  witness, sources, contribution operations, and audit lineage.
- [x] Bind the state-carried `C_P`/`L`/`V` causal factorization to actual
  runtime interfaces.
- [x] Demonstrate from admitted dataflow that arbitrary attribution labels do
  not enter the response path.
- [x] Bind a state-changing common-carrier intervention and a state-preserving
  order/shuffle invariance; audit history remains non-causal in this profile.
- [x] Map all nine operational projections to state-carried cells, controls,
  expected qualitative relations, causally held-fixed variables, and
  fail-closed scientific effects.
- [x] Preserve all seven logical cells and five L02 controls.
- [x] Freeze the private-partition competitor and non-private access witness.
- [x] Record unresolved measurement choices for I04 rather than silently
  selecting them here.
- [x] Retain an I03A contract, report, DEC-010, hypothesis-profile update,
  validation evidence, and explicit owner-review stop.

Exit state `P2-I2-I03A-REVIEW-READY` is satisfied by the complete state-carried
package. It neither passes the umbrella `P2-I2-DISCRIMINATOR-GATE` nor
authorizes I03B, I04, calibration, or candidate execution.

### 8A-R1. `P2-I2-I03AR1` — State-carried runtime conformance

**Status:** `P2-I2-I03AR1-REVIEW-READY`; replacement evidence and its one
reconstruction passed 136/136 assertions after governed I03AR1R1 correction.

#### 8A-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03AR1
purpose = determine whether the accepted I03A state-carried native candidate
          actually executes its declared writes, interventions, invariances,
          private guard, response path, restoration, and continuation
entry_authority = accepted I03A causal design; owner-accepted DEC-012/CHG-009;
                  admitted PyGRC 83e3a300426631ee4df71b661b67d4fcfdfed594
frozen_inputs_or_input_freeze_action = construct and validate a separate
          I03AR1 conformance freeze before the first mode-specific runtime call
mutation_and_repository_boundary = RCAE I03AR1 contracts, harness, reports,
          decisions, checklist, hypotheses, and navigation only; graph/PyGRC
          read-only; temporary artifacts permitted under /tmp
required_outputs = immutable input freeze; deterministic harness; runtime
          receipt; raw conformance record; reconstruction; narrative report;
          DEC-012/CHG-009 disposition; explicit owner-review stop
evidence_effect = realization implementation-conformance only; no calibration,
          L02 support/falsification, control result, boundary rung, or terminal
          effect
exit_gate = P2-I2-I03AR1-REVIEW-READY or reviewed realization-inadequate stop;
            never automatic I03B authorization
```

- [x] Record I03AR1 in the checklist before new conformance design,
  implementation inspection, or runtime execution.
- [x] Project the owner-accepted conformance boundary into the hypothesis
  artifact before runtime work.
- [x] Complete the ignored RCAE `.venv` with exact direct dependency versions
  from the admitted graph `uv.lock`, retain the environment receipt, and
  prohibit ambient/system-package substitution.
- [x] Retain and parse an exact I03AR1 input freeze before the first runtime
  operation.
- [x] Bind one deterministic fixture, exact values, assertions, run/attempt
  count, environment, admitted imports, outputs, and reconstruction command.
- [x] Prohibit parameter search, rescue variants, scientific response/
  comparator selection, delta/calibration input, and use as L02 evidence.
- [x] Exercise the accepted native write, carrier intervention, lineage-label
  invariance, state-preserving order invariance, private-partition guard,
  later response, save/load/reset, and equal-input continuation boundaries.
- [x] Retain exact runtime/import/source identities and graph read-only guards.
- [x] Reconstruct the conformance record byte-for-byte and stop for owner
  review without beginning I03B.

### 8A-R1-R1. `P2-I2-I03AR1R1` — Frozen scalar-comparison correction

**Status:** complete; original invocation retained as `infrastructure_invalid`;
revised evidence and reconstruction passed; I03B remains unauthorized.

#### 8A-R1-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03AR1R1
trigger = the one authorized I03AR1 evidence invocation stopped at
          combined_s1_s2.response_delta because native 0.5 + 0.1 was observed
          as 0.09999999999999998 after subtraction and the harness required
          strict equality with literal 0.1
classification = infrastructure_invalid; floating-point representation in the
                 assertion harness, not realization_inadequate and not an L02
                 result
retained_failed_attempt = freeze SHA-256 d21cc390ab6655ce98c7dbf6827a73d9b3d537c9d90cb98b81f8e2da510a1d94;
          harness SHA-256 3d2a12345343cd71e830a7dad6fc02bd6665cda60712f937d0ace4ce58fb5332;
          exit 1; no conformance output written
authorized_correction = compare only derived response deltas with frozen
          absolute tolerance 1e-12 and zero relative tolerance; retain every
          fixture value, branch, native call, causal assertion, run boundary,
          quarantine, and graph/source identity
run_effect = original invocation is permanently invalid; revised freeze may
          authorize one replacement evidence invocation and one reconstruction
          invocation; no additional retry
evidence_effect = none from the stopped invocation; replacement remains
          implementation-conformance only
exit_gate = return to P2-I2-I03AR1 review-ready work or stop fail-closed;
            never automatic I03B authorization
```

- [x] Record the stopped invocation, exact failure, absent output, and
  `infrastructure_invalid` classification before revising code or freeze.
- [x] Project the correction into the operational-hypothesis artifact before
  revising code or freeze.
- [x] Revise only the derived response-delta comparator and freeze its exact
  absolute/relative tolerances.
- [x] Retain a revised freeze and harness identity before the replacement
  runtime invocation.
- [x] Execute exactly one replacement evidence invocation and one
  reconstruction invocation; retain the original failed-attempt provenance.
- [x] Return to the I03AR1 owner-review stop without beginning I03B.

Exit state `P2-I2-I03AR1-REVIEW-READY` is satisfied by the immutable base
freeze, governed I03AR1R1 freeze revision, 136/136 replacement conformance,
byte-identical reconstruction, retained failed-attempt provenance, clean graph
guards, and scientific-evidence quarantine. It does not authorize I03B.

### 8B. `P2-I2-I03B` — History-carried realization freeze

**Status:** owner-accepted for staged progression under `P2-I2-DEC-015`. The
causal design and exact runtime sub-freeze were retained before execution;
bounded conformance passed and reconstructed byte-identically. At I03B close,
only I03C opened under its own freeze; DEC-020 later opened I04 after the
complete family closeout.

#### 8B.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03B
purpose = independently select and freeze the history-carried realization,
          causal factorization, interventions, private/access guards, and
          operational-hypothesis profile; then determine bounded runtime
          conformance under a second freeze
entry_authority = owner acceptance of the review-ready I03A/I03AR1 package and
                  explicit direction to move to 8B; DEC-011/DEC-012; admitted
                  PyGRC 83e3a300426631ee4df71b661b67d4fcfdfed594
frozen_inputs_or_input_freeze_action = first retain an I03B design/source-
          comparison freeze; select native, minimally producer-assisted, or
          missing-prerequisite disposition within history_carried mode; only
          then retain a separate exact runtime-conformance freeze before the
          first history-carried runtime call
mutation_and_repository_boundary = RCAE I03B contracts, harness, reports,
          decisions, checklist, hypotheses, and navigation only; graph/PyGRC
          read-only; temporary artifacts permitted under /tmp
required_outputs = immutable design input freeze; source/dataflow comparison;
          history-carried realization and operational-hypothesis contract;
          static validation; if realizable, immutable runtime input freeze,
          deterministic harness, runtime receipt, raw conformance record,
          byte reconstruction, narrative report, decision/change disposition,
          and explicit owner-review stop
evidence_effect = causal-design authority plus quarantined realization
          implementation-conformance only; no calibration, L02 support/
          falsification, control result, boundary rung, or terminal effect
exit_gate = P2-I2-I03B-REVIEW-READY or reviewed history-carried missing-
            prerequisite/inadequate stop; never automatic I03C authorization
```

- [x] Record I03B in the checklist before history-carried source comparison,
  design selection, harness construction, or runtime execution.
- [x] Project I03B's active/unbound and no-scientific-evidence status into the
  operational-hypothesis artifact before design work.
- [x] Retain and validate an I03B design input freeze before comparing history-
  carried realization candidates.
- [x] Prohibit I03A/I03AR1 observed outputs from selecting the I03B carrier,
  values, interventions, response, or realization class.
- [x] Define active causal history versus audit-only lineage, including the
  exact response read path and forbidden state-only/controller shortcuts.
- [x] Apply native-first selection within `history_carried`: use admitted
  native machinery when adequate, otherwise the minimal explicit RCAE
  producer, or retain a missing-prerequisite disposition.
- [x] Freeze source roles, common non-private access, contribution/history
  constitution, history intervention, state-preserving history contrast,
  private-partition competitor, restoration ownership, and producer boundary.
- [x] Preserve all seven logical cells, five L02 controls, and OP-01..OP-09
  without rewriting the accepted state-carried profile.
- [x] Retain a machine contract, static validator/result, narrative design
  report, and decision disposition before any history-carried runtime call.
- [x] If the design is realizable, retain and validate a separate exact runtime
  fixture, assertions, import/source identities, one evidence invocation, one
  reconstruction invocation, zero retries, and full scientific quarantine.
- [x] Exercise only the frozen history-carried causal path, interventions,
  guards, restoration/reset, and equal-input continuation boundaries.
- [x] Reconstruct byte-for-byte and stop for owner review without beginning
  I03C or I04.

#### 8B.2 Frozen design disposition

`P2-I2-DEC-014` selects `minimally_producer_assisted` after static comparison
of the three frozen dispositions. PyGRC's ordered packet/contact history is
native, restored, and useful as audit/input authority, but its rows are
passive evidence. Native feedback reads the latest contact plus live node
state; neither that path nor LGRC-0 annotations supplies an active,
independently intervenable multi-event history.

The selected `RCAEActiveHistoryAdapterV1` owns one missing separable
operation: one ordered, source-label-free, independently intervenable history
carrier `H_P` over admitted physical contribution rows. It materializes a
deterministic order-sensitive readout at native node `M_H` through public
native balancing packets. It stops there. It may not mutate PyGRC state
directly, retain source identity in causal tokens, inspect response state,
apply the response threshold, write success, or schedule the later response.
PyGRC owns native coherence mutation and the complete M_H-to-feedback-to-later-
packet response path.

The design freezes active-history reorder/clamp, state-only separation,
native write diversion, pure-label invariance, separate H1/H2 private
carriers with no common read, and one H_P/M_H access scope. Native v2 identity
must be composed with adapter current state, cursor/configuration,
interventions, and adapter reset baseline. Save/load/reset are paired
composite operations; no one-sided reset or implicit rebase is permitted.

Machine authority:
[I03B contract](../contracts/p2-i2/i03b-history-carried-realization-and-discriminator-contract.json),
SHA-256 `8fc575089017c0e429f04bb221092493634bba4a6adcd4fc22ca36a5b238c38d`.
No history-carried model was instantiated and no runtime operation occurred
during this design selection.

#### 8B.3 Runtime-conformance freeze

The separate
[I03B runtime freeze](../contracts/p2-i2/i03b-history-carried-runtime-conformance-input-freeze.json),
SHA-256 `dd0146f656f3f480d5ff3265696cacf39322fa5fe13991aed822614eee217720`,
validated without model instantiation. It binds the adapter and harness,
environment/import/source identities, twelve exact fixture branches,
history/order and label guards, active-history clamp, state-only separation,
private partitions, alternate access, paired composite save/load/reset,
equal-input continuation, one evidence invocation, one reconstruction, zero
retries, and the full scientific-evidence quarantine.

The exact conformance values are fixture-only and prohibited from I04/I06 or
scientific reuse. The next permitted action is the sole evidence invocation;
failure follows the frozen realization/missing-prerequisite/infrastructure
classification and cannot trigger tuning or a rescue branch.

#### 8B.4 Runtime-conformance disposition and review stop

The sole evidence invocation passed `252/252` frozen assertions. The sole
reconstruction produced the same SHA-256
`4465ff2174d285d26ffa8a6cb4bebaf644b150d24bea0d69563eb5f51d8c177d`
and was byte-identical to the retained
[runtime conformance](../contracts/p2-i2/i03b-history-carried-runtime-conformance.json).
The
[reconstruction receipt](../contracts/p2-i2/i03b-runtime-reconstruction-receipt.json)
records one evidence invocation, one reconstruction, zero retries, twelve
branches per invocation, clean graph identity, and paired composite
save/load/reset/continuation witnesses.

The fixture demonstrated only implementation conformance: equal-marginal and
equal-P physical order variants produced different H_P/readout/native-response
branches; lineage permutation was causally invariant; active-history clamp
changed the response with P retained; state-only P debit preserved the
H_P/M_H response; private histories remained separately readable only; and
alternate access used the same M_H/B_ref path. The adapter never computed or
scheduled success, and PyGRC owned every native mutation and later response.

`P2-I2-I03B-REVIEW-READY` is satisfied. No fixture value, branch outcome, or
digest may enter I04/I06 or scientific evidence. I03C and I04 remain
unauthorized pending explicit owner review/acceptance.

No history-carried surface comparison or binding occurred during I03A/I03AR1.
I03B may cite those artifacts only as fixed earlier-mode and governance
boundaries, never as history-carried selection evidence.

### 8B-R1. `P2-I2-I03BR1` — I03B closeout revalidation

**Status:** complete; zero-runtime closeout revalidation passed with no
blocking finding. Owner acceptance remains pending. I03C/I04 remain
unauthorized.

#### 8B-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03BR1
purpose = independently revalidate I03B against the owner-supplied twenty-one-
          point acceptance review, prioritizing exclusion of a hidden latest-
          contact response path and confirmation that H_P plus its M_H output
          port is the functional active-history pool
entry_authority = review-ready I03B package plus project-owner request for the
                  supplied validation suggestions to be checked
frozen_inputs_or_input_freeze_action = retain a machine-readable review/input
          freeze before inspecting the frozen harness, native source dataflow,
          conformance branches, identities, and control mappings
mutation_and_repository_boundary = RCAE I03BR1 checklist, hypothesis,
          validation contract/result, report, decision/change record, and
          navigation only; graph/PyGRC read-only; I03B freezes, harness,
          adapter, and retained runtime evidence immutable
runtime_policy = zero model instantiations and zero new evidence,
          reconstruction, retry, rescue, calibration, candidate, or control
          invocations; exhausted I03B invocation accounting is preserved
evidence_effect = source/dataflow and retained-artifact acceptance validation
          only; no scientific evidence, calibration input, registration value,
          R01-R05 assignment, mode ranking, or terminal effect
exit_gate = P2-I2-I03BR1-CLOSEOUT-PASSED or explicit blocking finding; never
            automatic I03C/I04 authorization
```

- [x] Record I03BR1 in the checklist before revalidation activity.
- [x] Project I03BR1's active, zero-runtime, no-scientific-effect status into
  the operational hypotheses before revalidation activity.
- [x] Retain a machine-readable input freeze mapping all twenty-one review
  sections and twelve concise acceptance statements to exact audit tests.
- [x] Trace every field consumed by native feedback emission and production;
  establish a matched neutral latest contact or prove differing contact fields
  are outside V.
- [x] Verify H_P is persistent, independently intervenable active state and
  M_H is its declared native output port, including clamp semantics.
- [x] Revalidate the complete P/H_P/L/U_H/R_H/M_H/V factorization, physical
  token typing, exact admission rule, cursor/idempotency isolation, order-state
  matching, and bounded history claim.
- [x] Revalidate stable history clamp, state-only debit exclusion, matched
  write diversion, private no-common-read, and alternate-access eligibility.
- [x] Revalidate adapter forbidden/allowed operations and counterfactual
  producer minimality against all admitted native candidates.
- [x] Classify H_P capacity, saturation, leakage, depletion, maintenance, and
  replacement semantics without selecting scientific numeric values.
- [x] Revalidate complete composite current/reset identity, paired operations,
  partial-load failure, no implicit rebase, and cursor continuation.
- [x] Verify mechanical scientific quarantine and the complete isolated
  twelve-branch matrix using only retained artifacts.
- [x] Confirm I03A remains independently retained, I03C remains untouched, and
  any later owner acceptance can authorize only I03C while I04 stays blocked.
- [x] Retain machine validation, narrative closeout report, and governance
  disposition; stop for owner review without beginning I03C.

#### 8B-R1.2 Closeout disposition

The frozen
[I03BR1 machine revalidation](../contracts/p2-i2/i03br1-closeout-revalidation.json)
passed all twenty-one review checks: fifteen directly and six with explicit
downstream obligations. There were zero blockers, zero model instantiations,
and zero runtime, reconstruction, retry, rescue, candidate, control,
calibration, or scientific invocations. The
[closeout report](../reports/P2-I2-I03BR1-history-carried-closeout-revalidation.md)
retains the full source/dataflow reasoning.

The two priority findings are:

1. A common neutral contact follows materialization. Across the order branches
   its physical route/contact/schedule fields match. Only node-proper-time and
   derived digests differ; native feedback does not use those differences in
   the polarity/threshold decision, and `expected_source_surface_digest` is
   null. The response difference is carried by M_H.
2. H_P is persistent adapter state and the clamp replaces H_P itself before
   R_H recomputation and native M_H rematerialization. The functional pool is
   H_P plus its M_H output-port binding, never P or M_H alone.

The selected lifecycle is run-bounded append-only under normal admission,
with explicit whole-history replacement and no autonomous depletion,
saturation, leakage, or maintenance transition. The bounded claim is active
ordered history causally materialized through a scalar readout; irreducible
raw-history and non-Markovian claims remain prohibited.

Six non-blocking duties remain explicit for later stages: I06 must preserve a
unique source-to-P path or register a route key, resolve scientific access,
bound lifecycle/event counts, make paired restoration the only registered
continuation interface with manifest-hash validation, and retain branch
identity obligations; I04/I06 validators must reject every conformance fixture
value/digest while importing only the pre-runtime structural family.

`P2-I2-I03BR1-CLOSEOUT-PASSED` is satisfied. At that review boundary it made
I03B acceptance-ready but did not itself accept I03B, authorize I03C/I04, pass
the umbrella gate, assign R01-R05, or create scientific evidence. The later
owner decisions remain separate authority.

### 8C. `P2-I2-I03C` — Hybrid realization freeze

**Status:** owner-accepted for progression under `P2-I2-DEC-018`; design/static
validation and the separately frozen 258/258 byte-reconstructed runtime
conformance passed. No hybrid source comparison, design selection, or runtime
operation preceded this declaration/freeze sequence. I04 opened only later
under DEC-020 after compact family closeout.

#### 8C.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03C
purpose = independently select and freeze the hybrid realization, separable
          state/history factorization, interventions, private/access guards,
          restoration ownership, and operational-hypothesis profile; then
          determine bounded runtime conformance under a second freeze
entry_authority = owner acceptance of I03B/I03BR1 for staged progression and
                  explicit direction that 8C is next; DEC-011, DEC-012, and
                  DEC-015; admitted PyGRC revision
                  83e3a300426631ee4df71b661b67d4fcfdfed594
frozen_inputs_or_input_freeze_action = first retain an I03C design/source-
          comparison freeze; compare native, minimally producer-assisted, and
          missing-prerequisite dispositions within hybrid mode; only then may
          a separate exact runtime-conformance freeze authorize one bounded run
mutation_and_repository_boundary = RCAE I03C contracts, adapter/harness if
          selected, reports, decisions, checklist, hypotheses, and navigation
          only; graph/PyGRC read-only; I03A/I03B artifacts immutable
required_outputs = immutable design input freeze; native-first source/dataflow
          comparison; hybrid realization and operational-hypothesis contract;
          static validation; if realizable, immutable runtime input freeze,
          deterministic harness, runtime receipt, raw conformance record,
          byte reconstruction, narrative report, and owner-review stop
evidence_effect = hybrid causal-design authority plus quarantined realization
          implementation-conformance only; no calibration, L02 support/
          falsification, control result, boundary rung, mode ranking, or
          terminal effect
exit_gate = P2-I2-I03C-REVIEW-READY or reviewed hybrid missing-prerequisite/
            inadequate stop; never automatic discriminator-gate or I04 pass
```

- [x] Record I03C in the checklist before hybrid source comparison, design
  selection, harness construction, or runtime execution.
- [x] Project I03C's active/unbound and no-scientific-evidence status into the
  operational hypotheses before design work.
- [x] Retain and validate an I03C design input freeze before comparing hybrid
  realization candidates.
- [x] Import I03A and I03B only as fixed earlier-mode causal/governance
  boundaries; prohibit their fixture observations from selecting I03C values,
  response, factorization, or realization class.
- [x] Define a genuinely hybrid factorization with separately identified
  state and active-history causal components, one joint response read, and no
  relabeling of either earlier mode as hybrid.
- [x] Freeze independent history-only, state-only, joint, write-diversion,
  label-invariance, private-partition, and alternate-access interventions that
  distinguish hybrid dependence from state-only or history-only shortcuts.
- [x] Apply native-first selection within `hybrid`: use admitted native
  machinery where adequate, otherwise the minimal explicit RCAE producer, or
  retain a missing-prerequisite disposition.
- [x] Freeze exact ownership and permitted/forbidden inputs for native state,
  active history, readout/materialization, joint V, audit lineage, adapter or
  producer, and later native response.
- [x] Preserve all seven logical cells, five L02 controls, and OP-01..OP-09
  without rewriting the accepted state-carried or history-carried profiles.
- [x] Freeze composite current/reset identity and paired continuation duties
  for every external state component; retain all I03BR1 admission,
  restoration, lifecycle, branch-identity, and quarantine obligations.
- [x] Retain a machine contract, static validator/result, narrative design
  report, and decision disposition before any hybrid runtime call.
- [x] If realizable, retain and validate a separate exact runtime fixture,
  assertions, import/source identities, one evidence invocation, one
  reconstruction invocation, zero retries, and full scientific quarantine.
- [x] Exercise only the frozen hybrid causal path, independent interventions,
  guards, paired restoration/reset, and equal-input continuation boundaries.
- [x] Reconstruct byte-for-byte and stop for owner review without beginning
  I04 or passing the umbrella discriminator gate.

Exit state `P2-I2-I03C-REVIEW-READY` is satisfied by the immutable design and
runtime freezes, passed static validation, one `258/258` evidence invocation,
one `258/258` byte-identical reconstruction, complete P-only/H-only joint-path
guards, paired save/load/reset and equal-input continuation, clean graph
guards, and scientific quarantine. Runtime SHA-256:
`217c8972e8e1199409343fb72b0eca12b2ba24dceb6a1f213c97af9143f0e96c`.
This does not pass the umbrella discriminator gate or authorize I04.

No hybrid surface comparison or binding occurred during I03A, I03B, or
I03BR1. I03C may cite those artifacts only as immutable prior-mode and
governance boundaries.

### 8C-R1. `P2-I2-I03CR1` — Hybrid closeout revalidation

**Status:** `P2-I2-I03CR1-CLOSEOUT-PASSED`; 26/26 review checks and 17/17
acceptance conditions passed with zero blockers. Eight fail-closed downstream
obligations are retained. I03C is acceptance-ready but not owner-accepted by
this audit; the umbrella closeout and I04 remain unauthorized.

#### 8C-R1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03CR1
purpose = revalidate the bounded hybrid package against the exact twenty-six
          review areas and seventeen acceptance conditions; retain explicit
          carrier/authority/factorial/admission/neutral-contact/restoration/
          lifecycle/quarantine meanings and classify every non-blocking
          registration duty without rewriting or rerunning I03C
entry_authority = owner-supplied review at attachment SHA-256
                  df1e823f2ff640713638b2b08266de45b99c5410bdd880f4380e75016e7a0298;
                  DEC-011, DEC-012, DEC-015, DEC-016; exact retained I03C hashes
frozen_inputs_or_input_freeze_action = retain an immutable I03CR1 input that
          binds the review digest, I03C artifacts/source identities, all audit
          questions, zero-runtime policy, and direct-pass/clarification/
          downstream-obligation/blocker classification rules before audit
mutation_and_repository_boundary = RCAE I03CR1 freeze, static validator,
          closeout result/report, checklist, hypotheses, decision/change
          records, and a machine quarantine/obligation registry only; no I03C
          artifact rewrite; graph/PyGRC read-only
required_outputs = exact review input freeze; machine-readable hybrid carrier,
          qualitative 2x2, admission exclusion, layered identity, lifecycle,
          and fixture-quarantine registry; static validator/result; closeout
          report; explicit blocker count and next-authority boundary
runtime_budget = zero model instantiations, zero candidate/control/conformance
          branches, zero reruns, zero reconstructions, zero parameter search
evidence_effect = retained-artifact causal-well-formedness and acceptance
          validation only; no new implementation or scientific evidence
exit_gate = P2-I2-I03CR1-CLOSEOUT-PASSED with owner acceptance still pending,
            or explicit retained blocker; never automatic umbrella/I04 pass
```

- [x] Record I03CR1 and its zero-runtime boundary before auditing the review.
- [x] Project the active closeout review and no-I04 effect into the operational
  hypotheses before audit.
- [x] Freeze the exact review digest, retained I03C artifact identities,
  twenty-six review areas, seventeen acceptance tests, and classification
  rules before source/evidence inspection.
- [x] Establish one stable hybrid carrier identity over P, authoritative H_P,
  M_H output-port binding, `[P,M_H]/[B_ref]` access, V, and separate L; reject
  P/H_P/M_H/mask/adapter/feedback-row substitutions.
- [x] Retain the bounded architectural distinction between native current-
  state response mechanics and independently persistent/intervenable H_P;
  explicitly reject irreducible-history or non-Markovian overclaim.
- [x] Verify P and H_P each enter the same native V independently, neither is
  encoded in the other, and both intervention chains preserve held-fixed
  components rather than acting through scheduler/contact/configuration side
  effects.
- [x] Freeze the complete qualitative P reference/candidate × H reference/
  candidate 2x2 for I04/I06 without importing fixture values or requiring all
  four cells to have been executed during conformance.
- [x] Retain raw P, R_H/M_H, native joint score/polarity, schedule decision, and
  later continuation; prohibit threshold crossing from defining hybrid and
  prohibit nonlinear interaction/synergy/irreducibility claims.
- [x] Prove from exact filter/dataflow identities that only registered
  physical S-role-to-common-P arrivals are admissible exactly once and that
  materialization, neutral contact, debit, response, feedback, reset/load,
  private, and diversion traffic cannot self-admit.
- [x] Resolve unique-route adequacy for the conformance fixture and retain the
  I06 explicit route/channel-key duty without using arbitrary labels or row/
  packet/event digests as causal authorization.
- [x] Validate the neutral contact's common configuration, final relative
  position, causal neutrality, admission exclusion, empty-queue boundary,
  latest-row role, and null digest requirement; classify absolute audit time/
  digest differences only after proving they do not enter score/threshold.
- [x] Validate exact-once distinct P/M_H masks, fixed B_ref, no aliases/extra
  nodes, live-state rather than stale-cache reads, order-insensitive native
  summation, and private-pair-only masks.
- [x] Retain one common P/H_P/M_H pool binding and verify private native nodes,
  adapters, cursors, baselines, masks, and no-dispatch/no-cross-pair guards;
  carry exact cross-load rejection into I06 if not executable in conformance.
- [x] Retain a complete layered identity over native v2, adapter current/reset,
  code/schema/filter/readout, joint/private bindings, masks, neutral/intervention
  policy, fixture/freeze, snapshot manifest, and evidence identities; distinguish
  demonstrated composite equality from the still-deferred registered atomic
  load/reset interface.
- [x] Verify H_P is authoritative, M_H must equal registered R_H(H_P) before V,
  and disagreement fails closed; cover pre-response, clamp/order, save/load,
  reset, and equal-input continuation boundaries.
- [x] Classify history length/overflow/window/truncation/saturation/leakage/
  clamp/reset/maintenance and P/M_H bounds as implemented, fixture-bounded,
  deferred, not applicable, or construction debt with rationale.
- [x] Audit all nine OPs for hybrid-specific meanings without rewriting I03A
  or I03B and without assigning R01-R05.
- [x] Retain a machine rejection registry for every I03A/I03B/I03C fixture
  coefficient, amount, threshold, topology/branch identity, observation,
  comparator, assertion result, and evidence digest; require later I04/I06
  validators to reject direct or trivial serialized reuse.
- [x] Verify 258/258 remains machine-classified as implementation conformance
  only, all three modes remain retained/unranked, and owner acceptance can open
  only a separately declared umbrella I03 family closeout—not I04 directly.
- [x] Produce a direct-pass/clarification/downstream-obligation/blocker matrix,
  run zero-runtime validation, and stop for owner review without opening the
  umbrella gate or I04.

#### 8C-R1.2 Closeout disposition — 2026-07-14

The immutable input and machine registry validated all twenty-six review areas
and all seventeen acceptance conditions. Classification counts are seventeen
direct passes, four closure clarifications, five downstream-obligation passes,
and zero blockers. The audit instantiated no model, ran no retained branch,
and left the single I03C evidence invocation and single reconstruction
unchanged.

The closeout explicitly records three bounded qualifications: I03C did not
execute the complete future scientific 2x2; restoration authority is a
layered package rather than one new native atomic API; and neutral-contact
absolute scheduler slots differ after explicit intervention operations even
though those slots do not enter the native score or threshold. Eight exact
fail-closed I04/I06/family-closeout obligations retain the corresponding
future work.

Exit state `P2-I2-I03CR1-CLOSEOUT-PASSED` is satisfied by the
[input freeze](../contracts/p2-i2/i03cr1-closeout-revalidation-input.json),
[hybrid closeout registry](../contracts/p2-i2/i03cr1-hybrid-closeout-registry.json),
[machine revalidation](../contracts/p2-i2/i03cr1-closeout-revalidation.json),
[validator](../scripts/p2_i2_i03cr1_validate.py), and
[closeout report](../reports/P2-I2-I03CR1-hybrid-closeout-revalidation.md).
This makes I03C acceptance-ready only. Owner acceptance may authorize a new
checklist-first umbrella I03 family closeout; it may not authorize I04
directly.

### 8.1 Umbrella I03 exit boundary

**Iteration:** `P2-I2-I03F`

**Status:** complete and owner accepted; compact composition passed 12/12
integration checks and 9/9 acceptance conditions with zero blockers. No mode
review was repeated. `P2-I2-DISCRIMINATOR-GATE=passed`; I04 construction is
authorized under its own declaration.

#### 8.1.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I03F
purpose = close the staged I03 family without choosing among modes by composing
          the already accepted mode closeouts into one lossless index over
          retained profiles, OP-01..OP-09, obligations, quarantine, restoration
          ownership, and unchanged mode-indexed I04 import
entry_authority = owner direction "we can move to 8.1 next" after
                  P2-I2-I03CR1-CLOSEOUT-PASSED; DEC-011, DEC-012, DEC-013,
                  DEC-015, DEC-016, DEC-017; all retained I03 mode artifacts
frozen_inputs_or_input_freeze_action = retain an immutable I03F input binding
          the accepted terminal authority for each mode, exact closeout/evidence
          identities, graph revision, compact integration checks, zero-runtime
          policy, and gate/owner-review effect before family composition
mutation_and_repository_boundary = RCAE I03F input, compact machine family
          index, static index validator/result, report, checklist, hypotheses,
          and decision/change records only; no reopening of accepted mode
          capability/source/dataflow findings, no I03 rewrite, graph read-only
required_outputs = exact compact family-closeout input; lossless three-mode OP,
          restoration-owner, obligation, quarantine, and I04-import index;
          static index validation; closeout report; explicit blocker count and
          owner-review boundary
runtime_budget = zero model instantiations, zero conformance/reconstruction/
          candidate/control branches, zero retries, zero parameter search
evidence_effect = accepted-authority composition and discriminator-gate
          readiness only; no repeated mode review, new implementation evidence,
          or scientific evidence
exit_gate = P2-I2-I03F-REVIEW-READY or explicit retained blocker; only a later
            owner disposition may pass P2-I2-DISCRIMINATOR-GATE and open I04
```

- [x] Record I03C/I03CR1 owner acceptance for progression and declare I03F in
  the checklist before any family audit.
- [x] Project I03F's zero-runtime, no-ranking, no-I04 boundary into the
  operational hypotheses before audit.
- [x] Freeze the accepted terminal decision/closeout authority for each mode
  plus exact evidence identities needed to prevent substitution; do not replay
  already accepted mode reviews.
- [x] Retain state-carried, history-carried, and hybrid as three required
  downstream modes with realization classes `pygrc_native_candidate`,
  `minimally_producer_assisted`, and `minimally_producer_assisted`; perform no
  selection, rank, preference, or supersession.
- [x] Cross-check only the accepted contract identities needed to show that
  I03B/I03C do not replace I03A, I03C does not replace I03B, and shared symbols
  retain mode-qualified rather than collapsed meanings.
- [x] Index, without re-proving, each accepted mode's carrier, write/update
  relation, access mask, intervention family, private/common binding, producer
  prohibition, and realization class.
- [x] Build a complete OP-01..OP-09 × three-mode pointer index and verify no OP
  or mode is absent; do not reassess the accepted mode-level causal evidence.
- [x] Retain the accepted native-first/producer-minimality boundary and index
  restoration ownership as native v2 for state-carried versus paired native-v2/
  adapter identity for history-carried and hybrid.
- [x] Consolidate every I03BR1 and I03CR1 downstream obligation without loss,
  duplication ambiguity, premature discharge, or transfer to the wrong owner
  iteration.
- [x] Consolidate the complete I03A/I03B/I03C fixture quarantine and require
  mechanical I04/I06 rejection of exact and trivially serialized reuse.
- [x] Freeze the I04 import boundary: all three profiles enter unchanged and
  mode-indexed; I04 may select measurements/comparators/calibration identities
  but cannot alter I03 causal semantics, remove a mode, or inherit fixture
  values/outcomes.
- [x] Verify the admitted graph revision remains clean/unchanged and that no
  source-capability re-audit, model/runtime, or reconstruction execution occurred
  in I03F.
- [x] Produce a machine blocker/gate-readiness result and family closeout report,
  then stop for owner review without passing the discriminator gate or opening
  I04 automatically.

#### 8.1.2 Compact family-closeout disposition — 2026-07-14

The compact validator matched all eleven terminal authorities to accepted
baseline commit `fc3fb0f638eb0b180cb05d081e6dc447f24af66b` and passed all
twelve integration checks and nine acceptance conditions with zero blockers.
It did not repeat any mode-level capability, source, dataflow, restoration, or
runtime review.

The retained index contains three unranked required modes, 27 exact OP pointers,
fourteen losslessly copied source obligations mapped exactly once into nine
consolidated duties, the complete seven-source fixture quarantine, mode-specific
restoration ownership, and an unchanged mode-indexed I04 import rule. At I03F
freeze no source obligation was discharged and the family-gate duty remained
pending; DEC-020 subsequently supplied that owner disposition without rewriting
the immutable index.

Exit state `P2-I2-I03F-REVIEW-READY` is satisfied by the
[input freeze](../contracts/p2-i2/i03f-family-closeout-input.json),
[family index](../contracts/p2-i2/i03f-family-closeout-index.json),
[machine validation](../contracts/p2-i2/i03f-family-closeout-validation.json),
[validator](../scripts/p2_i2_i03f_validate.py), and
[compact report](../reports/P2-I2-I03F-family-closeout.md). DEC-020 subsequently
accepted this package, passed the discriminator gate, and opened only I04.

Exit gate `P2-I2-DISCRIMINATOR-GATE` requires the complete reviewed staged
family and opens calibration preregistration only. If no bounded realization
can preserve one or more mode-specific discriminators, I03 may instead retain
a reviewed missing-prerequisite disposition without treating it as a negative
L02 result.

## 9. `P2-I2-I04` — Calibration preregistration construction

**Status:** original candidate-free package retained as validated history after
owner review withheld CAL-PRE passage. I04R1 resolved the primary-comparator
conflict and response/null correctness duties and passed focused validation;
I04R2 is the owner-accepted sole progression authority under DEC-026. No
matched-null or candidate execution occurred during I04–I04R2.

### 9.1 Activity declaration — 2026-07-14

```text
iteration_id = P2-I2-I04
purpose = freeze before any calibration or candidate outcome the exact
          mode-indexed scientific response, orientation, closest insufficient-
          repetition comparator, aggregation/missingness, signed control rules,
          candidate-blind matched-null design, analysis identity, and stopping
          policy imported unchanged from the accepted I03 family
entry_authority = owner direction "in that case, let's continue with I04";
                  owner-accepted I03F under DEC-020; accepted P2-I2 brief,
                  L02 metric sheet, I03F family index, and all frozen common
                  outcome/stopping/interpretation contracts
frozen_inputs_or_input_freeze_action = first retain an I04 choice-resolution
          input binding accepted semantic authorities, candidate/runtime/null
          absence, complete I03 fixture quarantine, available response/
          comparator options, and decision criteria; freeze the final
          preregistration only after those choices are justified
mutation_and_repository_boundary = RCAE I04 input, measurement/calibration
          preregistration, pure analysis/null-generation policy or code only
          if required, static validators/results, report, checklist,
          hypotheses, and decisions; graph/PyGRC read-only
required_outputs = exact per-mode response/comparator/control matrix; shared-
          versus-mode-specific equivalence decisions; aggregation/missingness/
          resolution rules; candidate-blind null freeze for I05; fixture-reuse
          rejection; analysis identity; machine validation; I04 report
execution_budget = zero candidate operations and zero matched-null calibration
          executions; static validation and candidate-free config construction
          only
evidence_effect = scientific measurement and calibration-method preregistration
          only; no resolution result, implementation registration, control
          outcome, R01-R05 assignment, or L02 support/falsification
exit_gate = P2-I2-CAL-PRE-GATE after owner review, or explicit retained blocker;
            never automatic I05 execution or candidate authority
```

- [x] Record owner acceptance of I03F, pass only the discriminator gate, and
  declare I04 before resolving any measurement choice.
- [x] Project I04's candidate-free choice boundary into the operational
  hypotheses before studying response/comparator options.

I04 imports all three reviewed I03 causal profiles unchanged. It freezes their
exact raw measurement, equality/resolution rule, numerical orientation,
primary comparator, aggregation, missingness, and machine-executable
pass/ambiguous/fail evaluation. It must preregister whether any measurement,
comparator, or calibration identity is validly shared or must be mode-specific;
it may not drop a mode. Numerical operationalization may not revise an I03
qualitative causal expectation.

- [x] Freeze an exact raw later-response family and orientation for each mode,
  sharing a definition only where semantic comparability is justified.
- [x] Freeze each mode's primary candidate response and closest registered
  insufficient-repetition comparator with rationale.
- [x] Freeze aggregation, pairing, normalized-margin, denominator-floor, and
  missingness policies shared by calibration and live analysis.
- [x] Freeze the candidate-blind matched-null generator(s), explicitly decide
  shared versus mode-specific calibration identity, and prove candidate and
  runtime exclusion.
- [x] Freeze calibration inputs, seeds, resource limit, expected artifacts,
  reconstruction command, and stopping rule.
- [x] Convert every imported qualitative expectation and fail-closed effect
  into an exact measurement, equality/resolution rule, and machine-executable
  pass/ambiguous/fail evaluation.
- [x] Freeze raw-response retention for all cells and subconfigurations.
- [x] Freeze analysis code/policy identity and change-control boundary.
- [x] Reject every I03A/I03B/I03C conformance-fixture coefficient, amount,
  type, time, threshold, packet amount, branch ID, response observation,
  implementation comparator, and evidence digest as calibration or scientific
  input; import only each pre-runtime frozen structural family and causal
  boundary.
- [x] Validate the preregistration without running the candidate or matched
  null.
- [x] Prove that no retained mode was removed or demoted by convenience,
  expected margin, or anticipated implementation cost.

### 9.2 Frozen substantive choices and validation

The [choice-resolution input](../contracts/p2-i2/i04-choice-resolution-input.json)
binds the accepted I03F baseline, ten controlling authorities, complete
fixture quarantine, candidate/null absence, admissible response/comparator
options, and decision criteria before the final choices.

The frozen [calibration preregistration](../contracts/p2-i2/i04-calibration-preregistration.json)
and [analysis policy](../configs/p2_i2_analysis_policy.json) select:

```text
response = native B-target coherence gain across one native response window
orientation = identity; higher is aligned
candidate = two-source combined constitution in both source-role orders
comparator = quantity-and-timing-matched repeated contribution by one source
primary panel = 3 seeds x 2 separately retained orders per mode
```

The response/analysis/null identity is validly shared because causal response
meaning, unit/orientation, window, comparator role, aggregation, missingness,
and calibration population are equal. Upstream carrier causes and controls
remain mode-specific. State retains equal-P order invariance, history retains
active-order divergence with P exclusion, and hybrid retains the complete
qualitative P-by-H_P four-cell factorial without imposing synergy.

Scientific no-response is zero. Operational failure leaves the complete
mode/seed two-order primary panel not evaluable; no imputation or denominator
removal is allowed. Every seed/order/cell/subconfiguration response remains
raw. Nine common and 3/3/5 mode-specific rules are frozen as numerical or
causal-chain `pass`/`ambiguous`/`fail` evaluations.

The [candidate-blind calibration policy](../configs/p2_i2_calibration_policy.json)
freezes five calibration seeds by two equal exact-rational order pairs and the
base metric estimator. I04 froze but did not invoke the future I05 entry point;
the entry point refuses to run without a future owner-authorized I05 freeze
binding all I04 identities and exactly one null invocation. `delta` remains
pending.

The retained [validation](../contracts/p2-i2/i04-calibration-preregistration-validation.json)
passed 16/16 static checks and 10/10 pure analysis tests. It confirmed all
seven semantic-equivalence fields, all seven I03 quarantine sources, no
fixture-value/branch/digest reuse, no PyGRC import/model, no matched-null or
candidate invocation, and an exact clean graph checkout. The compact
[I04 report](../reports/P2-I2-I04-calibration-preregistration.md) records the
review surface without reopening accepted I03 mode reviews.

Historical disposition: original `P2-I2-I04-REVIEW-READY` construction was not
owner-accepted and is superseded for progression under DEC-022/DEC-023. Its
artifacts remain byte-exact history; I05 and all candidate execution remained
unauthorized.

### 9.3 `P2-I2-I04R1` — Critical-review correction

**Status:** corrected candidate-free package review-ready; owner acceptance
pending

```text
iteration_id = P2-I2-I04R1
purpose = correct the I04 contract conflict that promoted an equivalence-
          permitted quantity-matched one-source scope diagnostic into a
          required-divergence primary comparator; harden source symmetry,
          order-conditioned interpretation, analytic-null scope, fixed
          response window, B-purity, per-mode isolation, evidence-derived
          causal-chain controls, and choice-rationale quarantine
entry_authority = owner-supplied critical I04 review withholding
                  P2-I2-CAL-PRE-GATE passage
frozen_inputs_or_input_freeze_action = retain original I04 package and review
          verbatim as historical inputs; revise only through a new I04R1
          choice/correction freeze before replacing preregistration identities
mutation_and_repository_boundary = RCAE I04R1 contracts, policies, pure
          analysis/future-null code, validators/tests/results, report,
          checklist, hypotheses, and decisions; admitted graph source may be
          read for public operation semantics but remains unmodified
required_outputs = corrected primary comparator and symmetric quantity-matched
          diagnostic; per-order/mode disposition rules; analysis-only delta
          meaning and I06 numeric admissibility; exact outcome-independent
          native operation window; B-purity guards; per-mode evidence boundary;
          evidence-derived causal-chain evaluation; quarantine provenance;
          static validation and revised report
execution_budget = zero PyGRC model instantiations, zero matched-null
          invocations, and zero candidate/control invocations; static source,
          policy, code, and pure unit validation only
evidence_effect = correction of candidate-free measurement/calibration
          authority only; no resolution result, control result, R01-R05,
          L02 support/falsification, or terminal classification
exit_gate = revised P2-I2-I04-REVIEW-READY for explicit owner review or a
            retained blocker; never automatic CAL-PRE passage or I05 authority
```

- [x] Freeze the owner review and original I04 identities before correction.
- [x] Restore quantity-matched repeated-S1 and repeated-S2 conditions to a
  symmetric scope diagnostic whose valid equivalence cannot fail R03.
- [x] Select a primary comparator that changes the mode-relevant common carrier
  without outcome-based choice and resolve source-role symmetry.
- [x] Separate failure of the full top signature from valid order-conditioned
  or mixed history/hybrid relations.
- [x] State that I05 calibrates analysis arithmetic only, keep runtime/
  continuation tolerances separate, and freeze I06 numeric-domain admission.
- [x] Freeze an exact outcome-independent native operation window for scheduled,
  unscheduled, delayed, blocked, and operationally invalid responses.
- [x] Require B-baseline matching and prove that only the registered response
  packet may change B, or use an attributable/subtracted response instead.
- [x] Keep primary margins, controls, metric relations, support, and rung inputs
  independent per mode with no cross-mode compensation.
- [x] Derive private/controller causal-chain control status from retained masks,
  identities, calls, lineage, guards, configuration, and receipts rather than
  authored booleans.
- [x] Reconstruct every I04 choice rationale from pre-runtime causal contracts
  and accepted theory without conformance observations.
- [x] Validate the revised package without executing PyGRC, the matched null,
  or any candidate/control cell, then return for owner review.

The [correction input](../contracts/p2-i2/i04r1-critical-review-correction-input.json)
binds the owner review, all ten original I04 identities, three pre-runtime mode
contracts, and two admitted public-source identities. The corrected
[preregistration](../contracts/p2-i2/i04r1-calibration-preregistration.json)
selects the strongest symmetric leave-one common-carrier admission comparator;
repeated-S1/S2 in both physical orders is a separate equivalence-permitted
scope diagnostic.

The response is fixed-window B gain with one feedback-row emission, one
producer evaluation, and exactly two step calls. Scientific zero requires two
empty-queue steps, unchanged B, and no packet. B purity, binary-like response
semantics, per-mode isolation, evidence-derived causal status, analytic-only
I05 delta, and I06 floor/ULP/tolerance admission are machine-frozen in the
corrected analysis policy.

The focused [validation](../contracts/p2-i2/i04r1-calibration-preregistration-validation.json)
passed 19/19 checks and 15/15 pure tests. It repeated no I03 mode review and
executed zero PyGRC models, matched nulls, candidates, or controls. The compact
[correction report](../reports/P2-I2-I04R1-calibration-preregistration-correction.md)
is the owner-review surface.

Historical disposition: `P2-I2-I04-REVIEW-READY` under DEC-023. I04R1 is now
immutable history superseded for progression by owner-accepted I04R2; it has no
parallel calibration or execution authority.

### 9.4 `P2-I2-I04R2` — Conditional machine-invariant closure

**Status:** complete and explicitly owner-accepted; sole I04 progression
authority under DEC-026

```text
iteration_id = P2-I2-I04R2
purpose = verify and, where required, correct the machine implementation of
          I04R1's complete two-arm comparator evaluability, exact I05 primary-
          estimator route, I06 diversion and response-gain admissibility,
          window-before-zero validation, non-gating scope diagnostic, order-
          conditioned classification, and receipt-derived causal controls
entry_authority = owner-supplied conditional I04R1 acceptance review,
                  SHA-256 78a49384609cdc4198a2dbce359c21d03694822fb7da96d1c2ff5f3333741d5d
frozen_inputs_or_input_freeze_action = retain the complete I04/I04R1 package
          and conditional review as exact history; freeze an I04R2 verification
          input before changing any corrected policy/code identity
mutation_and_repository_boundary = RCAE I04R2 contracts, corrected policy/
          pure analysis/future-I05 code, tests, focused validator/result,
          report, checklist, hypotheses, and decisions; admitted PyGRC public
          source may be inspected but graph repository remains unmodified
required_outputs = all-or-none primary tuple rule; future I05 three-arm route;
          exact diversion noninterference duties; B-domain/identity-gain guard;
          step-event/evaluation contamination guards; explicit non-gating and
          order/causal derivations; focused validation and review surface
execution_budget = zero matched-null invocations, zero PyGRC models, and zero
          candidate/control invocations; static inspection and pure unit tests
          only
evidence_effect = conditional candidate-free machine-preregistration integrity
          only; no resolution, runtime, control, R01-R05, or L02 result
exit_gate = I04R2 acceptance-readiness confirmation for explicit owner review,
            or retained blocker; never automatic CAL-PRE or I05 execution
```

- [x] Freeze the conditional review and exact I04R1 identities before machine
  verification.
- [x] Prove candidate, leave-q1, and leave-q2 are all required before `max`,
  and that `max` is computed only within one mode/seed/physical-order tuple.
- [x] Route the future I05 arithmetic null through raw candidate, leave-q1,
  and leave-q2 records and the exact live strongest-marginal estimator path.
- [x] Freeze I06 diversion matching and inert-sink noninterference over every
  continuation-relevant carrier, mask, policy, eligibility, and B surface.
- [x] Require measured B gain to equal the registered native arrival gain
  within a separate runtime tolerance, remain inside the registered native
  coherence domain, and exclude clipping/projection/budget corrections.
- [x] Validate evaluation, producer, exact step-event, queue, and contamination
  identities before assigning scientific zero.
- [x] Confirm repeated-S1/S2 equivalence has no primary, top-signature, R03, or
  lowering effect.
- [x] Confirm non-top order panels remain independently classifiable from raw
  order/control/causal evidence and never imply hypothesis failure directly.
- [x] Confirm candidate/private/controller status remains derived from exact
  masks, arrivals, calls, lineage, guards, configurations, and receipts.
- [x] Run only focused static validation and pure tests, reconstruct the result,
  and return the package for explicit owner acceptance.

The [I04R2 input freeze](../contracts/p2-i2/i04r2-conditional-machine-verification-input.json)
binds the conditional review and all ten I04R1 identities. Focused inspection
found one real machine gap: the I04R1 future calibration entry point fed an
already paired response directly into normalized-difference arithmetic. The
corrected [future I05 entry point](../scripts/p2_i2_i04r2_calibration.py) now
builds raw candidate, q1-only, and q2-only response envelopes and invokes the
same all-or-none [primary analyzer](../scripts/p2_i2_i04r2_analysis.py) used by
the preregistered live route, then writes, reads, parses, and byte-reconstructs
the governed output before successful exit.

The [machine policy](../configs/p2_i2_i04r2_machine_policy.json) freezes
diversion noninterference, native identity-gain/domain admission,
window-before-zero receipts, repeated-source non-gating scope, independent
order classification, and receipt-derived causal status. The focused
[validation](../contracts/p2-i2/i04r2-machine-verification-validation.json)
passed 16/16 checks and 7/7 pure tests and reconstructed byte-identically. It
executed zero matched nulls, PyGRC models, candidate/control cells, or graph
mutations. Its retained test receipt excludes wall-clock timing so an
independent validator run is byte-stable. The compact
[verification report](../reports/P2-I2-I04R2-conditional-machine-verification.md)
is the owner-review surface.

Owner disposition: accepted under DEC-026. I04R2 is the sole progression
authority; original I04 and I04R1 remain immutable historical artifacts with
no parallel execution authority. `P2-I2-CAL-PRE-GATE` is passed and authorizes
only construction of a separate, exact, single-invocation I05 arithmetic-null
freeze. It does not invoke I05 or open I06, candidate execution, or a result.

Exit gate `P2-I2-CAL-PRE-GATE` authorizes only I05 matched-null calibration.

## 10. `P2-I2-I05` — Candidate-blind calibration

**Status:** one exact authorization candidate passed identity validation; I05A
found five execution-safety blockers and failed proposed DEC-027 closed; I05B
resolved them and is owner-accepted for retention under DEC-029. The authority
remains unconsumed, null launch is separate, no I05 invocation occurred, and
CAL-GATE remains closed.

### 10.1 Single-invocation authorization-freeze construction

```text
activity_id = P2-I2-I05-AUTHORIZATION-FREEZE
purpose = construct and statically validate authority for exactly one I05
          analysis-arithmetic matched-null invocation
entry_authority = DEC-026 + passed CAL-PRE + accepted I04 lineage commit
accepted_I04_commit = b7b008c402d837b529962a1a5edb062927939d28
mutation_boundary = I05 authorization contract, focused zero-invocation
                    validator/result, report, and navigation/governance records
governed_invocations_during_construction = 0
PyGRC_invocations_during_construction = 0
candidate_or_control_invocations_during_construction = 0
graph_repository = read_only
evidence_effect = permission/integrity only; no calibrated delta, metric-sheet
                  result, operational-hypothesis evidence, or scientific result
exit = one validated, unconsumed authorization candidate returned for owner
       review; activation and commit each require explicit owner authorization,
       and P2-I2-CAL-GATE remains closed
```

- [x] Bind the authority to accepted I04 commit
  `b7b008c402d837b529962a1a5edb062927939d28`, DEC-026, the owner-acceptance
  record, and the exact active I04R2 machine/analysis/calibration/preregistration
  identities.
- [x] Encode a ceiling of exactly one governed invocation and set candidate
  execution to false; this becomes active only after owner acceptance and the
  separately authorized retention commit.
- [x] Validate only through the frozen I04R2 authorization validator; do not
  call the calibration builder, calibration entry point, or PyGRC.
- [x] Verify that the governed I05 output is absent and record zero
  matched-null, PyGRC, candidate, and control invocations.
- [x] Reconstruct the authorization-validation result byte-identically.
- [x] Obtain owner review and explicit acceptance/commit authorization.
- [x] Commit the accepted, unconsumed authorization before any request to
  execute it; do not pass `P2-I2-CAL-GATE` during this activity.

### 10.2 `P2-I2-I05A` — Pre-acceptance execution-safety audit

**Status:** complete and blocked; 3/8 checks passed, five execution-safety
blockers retained, with zero governed-null, PyGRC, candidate, or control
invocation and no source correction.

```text
entry = review-ready uncommitted I05 authorization candidate + owner review
scope = existing entry point, freeze, validation, reconstruction policy, and
        commit/environment/command bindings only
mutation_boundary = checklist, hypothesis projection, audit result/report,
                    and navigation records; no execution-source correction
governed_null_invocations = 0
reconstruction_generations = 0
candidate_or_control_invocations = 0
acceptance_effect = none until owner review of the audit disposition
```

- [x] Inspect atomic attempt-time consumption and concurrent exclusion: failed;
  no consumption token, exclusive claim, or lock exists before governed work.
- [x] Inspect immediate preflight binding: failed; it binds only accepted I04
  commit/identities, not a committed I05 authority, exact launch interpreter/
  command, or clean RCAE authority files.
- [x] Inspect reconstruction generation: passed; the existing main path calls
  the builder once, then reads, parses, canonicalizes, and compares retained
  output without a second envelope generation.
- [x] Inspect separate retained counts and refusal witness: failed; no
  consumption receipt, generation/readback counts, or refused-second-start fact
  is emitted.
- [x] Inspect failure/retry semantics: failed; one governed invocation and one
  infrastructure retry are configured without an attempt-token distinction.
- [x] Fail proposed DEC-027 closed and return a precise
  correction scope for owner authorization; do not implement it in I05A.

### 10.3 `P2-I2-I05B` — I05-owned one-shot safety correction

**Status:** owner-accepted for retention under DEC-029/CHG-022; 12/12 zero-null
tests and 12/12 machine checks passed with byte-identical reconstruction.

```text
allowed_scope = one I05 governed wrapper + one I05 one-shot policy + atomic
                claim/final receipt mechanics + zero-null tests/validation
I04R2_scientific_bytes = immutable
max_governed_attempts = 1
max_infrastructure_retries = 0
claim_timing = atomic and before accepted builder call
claim_lifecycle = survives every success/failure/crash; deletion forbidden
committed_authority_binding = runtime expected-HEAD argument + committed-blob
                              equality + owner-acceptance presence; no
                              self-referential hash inside the freeze
null_invocations_during_I05B = 0
commit_authorized = true
CAL_GATE = closed
exit = accepted, committed correction and byte-reconstructed zero-execution
       validation; null launch remains a distinct 10.4 authority
```

- [x] Add one I05-owned governed wrapper and one one-shot policy without
  changing accepted I04R2 estimator, analysis, comparator, calibration policy,
  preregistration, or test bytes.
- [x] Atomically create an exclusive claim receipt before any builder call;
  never delete or reuse it, and make every later/concurrent start fail closed.
- [x] Require one governed attempt and zero retries; a failure or crash after
  claim remains consumed.
- [x] Bind runtime `HEAD` supplied after the future authority commit, prove all
  required authority/code blobs are in that commit and equal working bytes,
  require clean index/worktree authority state, and bind interpreter plus
  normalized command.
- [x] Bind the existing authorization candidate, wrapper/policy identities, and
  unchanged I04R2 hashes in the claim receipt.
- [x] Make the future governed path call the accepted I04R2 builder exactly
  once and reconstruct only by retained-output read/parse/canonical comparison.
- [x] Retain final counts/status for one attempt, zero reconstruction
  generations, one readback, consumed authority, and mechanical second-start
  refusal.
- [x] Demonstrate all eight owner-required refusal cases with zero accepted-
  builder invocations during safety validation.
- [x] Reconstruct the validation byte-identically; retain zero null/PyGRC/
  candidate/control execution and return uncommitted for owner review.

#### 10.3.1 I05B owner acceptance and commit packaging

```text
activity_id = P2-I2-I05B-ACCEPTANCE-COMMIT
entry_authority = explicit project-owner approval of I05B and authorization
                  to commit, dated 2026-07-14
purpose = retain immutable owner acceptance and commit the complete reviewed
          I05/I05A/I05B authority package without authorizing or invoking the
          arithmetic null
authority_split = I05B owner acceptance + commit authorization now;
                  null-launch authorization only in separately directed 10.4
mutation_boundary = I05B acceptance/launch authority split, machine acceptance
                    record, zero-null validation, governance/navigation, and
                    digest consequences only; accepted I04R2 bytes immutable
null_invocations = 0
candidate_or_control_invocations = 0
CAL_GATE = closed
exit = accepted committed I05B authority package; 10.4 remains blocked on a
       separate explicit null-launch authorization
```

- [x] Record I05B owner acceptance and commit authorization under a new
  decision/change identity without rewriting DEC-027 or DEC-028.
- [x] Split immutable package acceptance (`null_invocation_authorized=false`)
  from the future 10.4 launch authority; require both exact records before any
  attempt claim can be created.
- [x] Retain the permanent claim on a repository-local non-temporary path and
  preserve `O_CREAT|O_EXCL` refusal for empty, partial, symlink, concurrent,
  crashed, or earlier claim-path occupation.
- [x] Recompute affected wrapper/policy/acceptance/validation identities and
  rerun focused plus combined zero-execution tests.
- [x] Verify accepted I04R2 bytes, graph/PyGRC cleanliness, absent claim/final/
  governed output, zero builder/null/candidate/control operations, and closed
  CAL-GATE immediately before retention.
- [x] Commit the complete accepted package; do not create the separate launch
  record or execute the null in this activity.

### 10.4 Authorized arithmetic-null execution and metric-sheet freeze

**Status:** the single governed attempt completed at historical commit
`c3eabf3` with one builder call, zero retries, one readback, zero reconstruction
generations, and a refused second start. Metric-sheet closeout remains paused
on portability correction review.

```text
activity_id = P2-I2-I05-ARITHMETIC-NULL-EXECUTION
entry_authority = owner direction "after commit" to proceed with 10.4;
                  accepted I05B authority commit
                  c1f821dfd543d10d8555ddf2b52dbd56dfa76c13
purpose = consume the single governed arithmetic-null permission, retain and
          reconstruct its exact output, and freeze only the preregistered
          analysis-arithmetic resolution fields
launch_authority = exact P2-I2-I05-NULL-LAUNCH-AUTHORIZATION under DEC-030/
                   CHG-023, committed before the attempt and bound by the
                   accepted I05B wrapper/policy
max_governed_attempts = 1
max_infrastructure_retries = 0
accepted_builder_invocations = 1
null_reconstruction_generation_count = 0
output_readback_reconstruction_count = 1
candidate_or_control_invocations = 0
PyGRC_model_instantiations = 0
mutation_boundary = exact launch record/commit; governed attempt/final/output;
                    deterministic readback validation; designated frozen
                    metric-sheet fields; checklist/hypothesis/decision/report
evidence_effect = arithmetic/serialization resolution only; no runtime
                  tolerance, candidate/control evidence, R01-R05 assignment,
                  L02 support/falsification, or mode selection/ranking
exit = P2-I2-I05-EXECUTION-REVIEW-READY with CAL-GATE still closed pending
       owner review of exact receipts, reconstruction, and metric-sheet freeze
```

- [x] Record DEC-030/CHG-023 and create the exact separate launch record bound
  to accepted commit `c1f821d`, owner acceptance, authorization, wrapper,
  policy, and unchanged I04R2 hashes.
- [x] Validate the launch record without calling the accepted builder, null,
  PyGRC, candidate, or control path; require absent claim/final/output.
- [x] Commit the exact launch authority and revalidate exact HEAD, clean
  index/worktree, committed/local byte equality, interpreter, command, local
  ext4 claim storage, and accepted I04R2 identities immediately before start.
- [x] Invoke the accepted one-shot wrapper exactly once; treat any post-claim
  failure as consumed and perform no infrastructure retry.
- [x] Retain the permanent claim, final receipt, and governed output with the
  required attempt/builder/generation/readback/consumption/refusal counts.
- [x] Reconstruct only from retained output and require byte identity; do not
  invoke the builder or regenerate response envelopes during validation.

#### 10.4A `P2-I2-I05C` — Pre-claim venv-interpreter path correction proposal

**Status:** correction was owner-approved and committed at `9d81f15` under the
explicit direction “always use venv”; 13/13 tests and 12/12 zero-null checks
passed before the later single governed attempt.

```text
trigger = accepted wrapper validates expected .venv/bin/python through the
          generic repository-data-path resolver
observed_resolution = .venv/bin/python -> digest-bound host Python target
failure = OneShotError: path escapes repository root: .venv/bin/python
claim_created = false
accepted_builder_invocations = 0
governed_null_invocations = 0
output_or_final_receipt_created = false
authority_consumed = false
proposed_scope = distinguish the frozen repo-relative command path from its
                 resolved executable target; retain exact target digest,
                 implementation/version, command, and all other preflight
                 guards; update consequential wrapper/policy/acceptance/launch
                 identities and add a direct real-venv preflight test
scientific_change = none
```

- [x] Stop on the preflight failure without creating the permanent claim or
  calling the builder.
- [x] Identify the direct cause as reuse of the repository-data `_path()` guard
  for an intentionally external-resolving venv interpreter symlink.
- [x] Obtain explicit owner authorization before changing the accepted I05B
  wrapper, policy hash, acceptance record, launch record, tests, or committed
  authority.
- [x] Freeze the exact correction under DEC-031/CHG-024, prove
  the real `.venv` interpreter passes while wrong command/path/digest fail,
  rerun zero-null validation, and return for review. The sole governed attempt
  remains available because no claim exists; infrastructure retries remain
  zero.
- [x] Obtain owner review and explicit commit authorization, commit the complete
  corrected authority together, and require a clean exact-HEAD preflight before
  the one-shot attempt.

- [x] Execute only the frozen shared pure analysis-arithmetic matched-null
  structure.
- [x] Retain reconstructable generator provenance and all per-seed margins.
- [x] Verify candidate/runtime exclusion and absence of post-hoc inputs.
- [ ] After portability corrections are accepted, freeze the preregistered shared
  `analysis_arithmetic_delta`
  disposition under the metric-sheet estimator without selecting a mode or
  inferring any runtime/measurement tolerance.
- [ ] Retain a lane-local metric-calibration record and generated frozen
  metric-sheet artifact linked to the unchanged base L02 metric sheet;
  populate only the frozen artifact's designated resolution-status,
  `analysis_arithmetic_delta`, rationale, and calibration-reference fields.
- [x] Retain schema-valid raw calibration/provenance and exact portable
  projection lineage records.
- [x] Reconstruct the calibration independently and verify semantic digests.
- [ ] Preserve narrow/robust language as relation to frozen resolution, not a
  terminal verdict.

#### 10.4B `P2-I2-I05D` — P2-I2-wide persisted-path portability audit

**Status:** corrected full-scope audit accepted under DEC-032/DEC-033;
312 value-redacted violations are retained across 70 of 135 scanned files, and
the owner authorized only the first I05 correction group.

```text
activity_id = P2-I2-I05D-PERSISTED-PATH-PORTABILITY-AUDIT
trigger = committed I05 execution closeout exposed filesystem-absolute paths;
          project owner states that absolute paths are never allowed
scope = current-tree P2-I2 contracts, configs, outputs, reports,
        implementation/governance, tests, and scripts under the AE01
        experiment; historical Git objects are immutable provenance only
invalid_path = any persisted filesystem-absolute POSIX path, drive-prefixed
               path, home-expanded path, or machine-local absolute path token
               embedded in a persisted command/value/literal
allowed_path = normalized repository-relative POSIX identity, stable logical
               external-repository ID, content digest, or non-path URI
mutation_boundary = checklist/hypothesis/decision audit authority; exact audit
                    policy, scanner, input freeze, inventory, and validation
                    only; no affected artifact correction in I05D
runtime_boundary = static current-tree inspection only; always use repository
                   .venv; no null builder, PyGRC model, candidate/control,
                   conformance, calibration, or response-envelope operation
historical_boundary = do not rewrite Git history and do not copy forbidden
                      path strings into new audit/governance artifacts; retain
                      historical lineage by commit and SHA-256 only
exit = P2-I2-I05D-PORTABILITY-AUDIT-REVIEW-READY with CAL-GATE closed
```

During I05D construction, the first discovery pass showed that two recursive
selectors selected directories rather than nested files. The selectors and
coverage guards were corrected inside I05D before the retained inventory was
created; this changed no classification, redaction, grouping, or gate rule and
does not constitute a separate iteration.

- [x] Record the owner-authorized audit under a new decision/change identity
  without weakening the project-wide no-absolute-path rule.
- [x] Freeze a deterministic scanner scope and classification policy before
  scanning affected files.
- [x] Correct the in-iteration recursive selector form, bind the final policy/
  scanner freeze, and require explicit nested contract/output coverage before
  retaining the audit.
- [x] Scan every in-scope current-tree P2-I2 persisted artifact and relevant
  source literal; reject filesystem-absolute paths regardless of whether they
  occur in JSON values, commands, receipts, reports, tests, or code.
- [x] Distinguish filesystem paths from non-path URIs and mathematical slash
  notation without permitting machine-location exceptions.
- [x] Retain a portable inventory containing only repository-relative affected
  file identities, field/line locations, violation classes, counts, and file
  digests; never reproduce the forbidden path values.
- [x] Group the inventory into dependency-aware correction batches with I05
  active execution/closeout first and earlier accepted lineages afterward.
- [x] Prove the audit itself imports/calls no null builder, one-shot wrapper,
  PyGRC, candidate/control, conformance, or scientific path.
- [x] Return the audit uncommitted for owner review; do not correct affected
  artifacts, reopen the one-shot attempt, freeze delta, or pass CAL-GATE.

#### 10.4C `P2-I2-I05E` — Bounded portable-path correction groups

**Status:** first I05 correction group owner-accepted and commit-authorized
after 10/10 machine checks, zero remaining violations across the exact eleven-
file scope, and 13/13 focused helper tests. The next group remains inactive
until this package is committed.

```text
activity_id = P2-I2-I05E-BOUNDED-PORTABLE-PATH-CORRECTION
entry = owner-accepted I05D inventory and exact correction-group freeze
group_order = I05 active execution/closeout first; dependency-ordered upstream
              P2-I2 groups afterward; one reviewed group at a time
path_rule = current-tree persisted filesystem identities are normalized
            repository-relative POSIX strings or stable logical external IDs;
            machine identity is retained by digest/version/capability facts,
            never by an absolute location
execution_evidence = original governed-attempt/output/final bytes remain
                     immutable in Git history and are referenced only by commit
                     and digest; active portable projections must declare their
                     derivation and cannot impersonate original raw receipts
null_invocations = 0
infrastructure_retries = 0
candidate_or_control_invocations = 0
PyGRC_model_instantiations = 0
scientific_change = none; accepted I04R2 estimator, three-arm values, margins,
                    delta arithmetic, and candidate/runtime exclusions immutable
gate_effect = CAL-GATE remains closed until all required corrections and I05
              post-run metric artifacts pass review
```

The first correction group binds these eleven affected files plus only the
consequential I05 authority/projection identities required to keep their
historical and current meanings explicit:

- `contracts/p2-i2/i05c-preclaim-interpreter-path-failure.json`
- `contracts/p2-i2/i05c-zero-null-interpreter-validation.json`
- `implementation/tests/test_p2_i2_i05b_one_shot.py`
- `outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json`
- `outputs/p2-i2/i05/i05b-attempt-claim.json`
- `reports/P2-I2-I05C-preclaim-venv-correction.md`
- `scripts/p2_i2_i05_authorization_validate.py`
- `scripts/p2_i2_i05a_safety_audit.py`
- `scripts/p2_i2_i05b_one_shot.py`
- `scripts/p2_i2_i05b_validate.py`
- `scripts/p2_i2_i05c_validate.py`

- [x] Accept and bind the exact I05D audit before editing an affected artifact.
- [x] Freeze the first I05 correction group's exact files, fields, upstream
  hashes, derived-historical lineage, allowed transformations, and validators.
- [x] Replace absolute repository locations with normalized repository-relative
  identities and external machine locations with stable logical IDs plus exact
  digests/version facts; never persist resolved absolute targets or prefixes.
- [x] Preserve the permanent consumed-attempt guard and one-attempt/zero-retry
  fact without rerunning, regenerating, or fabricating the governed null.
- [x] Preserve original raw execution identities by historical commit/digest,
  create explicitly labelled portable projections, and update only downstream
  identities authorized by the correction freeze.
- [x] Rerun the portability scanner and bounded semantic/integrity validation;
  require zero absolute-path violations in the completed correction group.
- [x] Return the first correction group uncommitted for owner review and explicit
  commit authorization before beginning the next group.
- [x] Record owner acceptance and commit authorization; begin no later group
  until the accepted package is retained.

#### 10.4D `P2-I2-I05F` — I04/I05 authority-dependency portability correction

**Status:** owner-accepted and commit-authorized under DEC-036 after bounded
in-place process-deviation closeout under DEC-035. The exact group remains
technically 10/10 with zero findings; the original freeze and complete
13-start ledger are retained, and no technical-validator rerun occurred.

```text
activity_id = P2-I2-I05F-I04-I05-AUTHORITY-DEPENDENCY-PORTABILITY-CORRECTION
entry = owner-accepted I05D/I05E commit 6dd6898 plus DEC-034/CHG-027
baseline_group = i04_i05_authority_dependencies
baseline_findings = 30 across 13 files
path_rule = repository artifacts use normalized repository-relative POSIX
            identities; external repositories use stable logical IDs plus
            admitted revision/digest facts; no persisted machine location
historical_boundary = accepted I04/I04R1/I04R2 bytes remain Git evidence by
                      commit and SHA-256; current changed artifacts declare
                      portable projection lineage and cannot impersonate raw
                      preregistrations or validations
scientific_boundary = accepted I04R2 estimator, comparator, window, response,
                      calibration policy, and CAL-PRE meaning are immutable
runtime_boundary = .venv static validation only; zero calibration builder,
                   null, one-shot wrapper, PyGRC model, candidate/control,
                   conformance, or scientific invocation
gate_effect = CAL-GATE remains closed; no I06 or later correction group opens
exit = P2-I2-I05F-I04-I05-GROUP-REVIEW-READY, uncommitted
```

The exact affected files are:

- `configs/p2_i2_i04r2_machine_policy.json`
- `contracts/p2-i2/i04-calibration-preregistration.json`
- `contracts/p2-i2/i04r1-calibration-preregistration-validation.json`
- `contracts/p2-i2/i04r1-calibration-preregistration.json`
- `contracts/p2-i2/i04r1-critical-review-correction-input.json`
- `contracts/p2-i2/i04r2-conditional-machine-verification-input.json`
- `contracts/p2-i2/i04r2-machine-verification-preregistration.json`
- `contracts/p2-i2/i04r2-machine-verification-validation.json`
- `scripts/p2_i2_i04_validate.py`
- `scripts/p2_i2_i04r1_calibration.py`
- `scripts/p2_i2_i04r1_validate.py`
- `scripts/p2_i2_i04r2_calibration.py`
- `scripts/p2_i2_i04r2_validate.py`

- [x] Retain the accepted first correction group at `6dd6898` before opening
  this group.
- [x] Bind the exact I05D group identity: 13 files and 30 findings.
- [x] Freeze every source hash, allowed field transformation, historical
  authority identity, consequential downstream identity, and validator before
  editing an affected file.
- [x] Replace repository and external-source locations with repository-relative
  or stable logical identities; remove machine-selecting shebangs.
- [x] Preserve exact historical I04/I04R1/I04R2 semantics and reconstruct every
  changed JSON projection mechanically from its historical bytes.
- [x] Preserve accepted I04R2 and I05 arithmetic identities by explicit
  historical-to-current lineage; do not silently update raw receipt hashes.
- [ ] Require zero path findings across the exact group, parseable corrected
  source, and bounded semantic/integrity validation under `.venv`.
- [x] Return the group uncommitted for owner review; do not begin I03 or another
  correction group, freeze the metric sheet, or pass CAL-GATE.
- [x] Record the owner's `+1` authorization for an I05F-owned in-place
  process-deviation closeout under DEC-035/CHG-028; do not reinterpret or
  rewrite the original freeze.
- [x] Retain one additive closeout record binding the frozen ceiling, actual
  13-start ledger, technical 10/10 result, zero-runtime boundary, and exact
  owner-authorized disposition.
- [x] Restore I05F to uncommitted owner-review readiness without any Python,
  technical-validator, builder, null, wrapper, PyGRC, candidate/control,
  conformance, or scientific rerun.
- [x] Record the owner's instruction that completed closeout also constitutes
  full I05F acceptance and commit authorization under DEC-036/CHG-029.
- [x] Retain a separate owner-acceptance artifact so the earlier deviation
  closeout remains an accurate pre-acceptance record.
- [x] Confirm with non-Python precommit checks that both new authority records
  parse, the diff has no whitespace errors, HEAD is the accepted `6dd6898`
  parent on `p2-i2-experiment`, and the closeout/navigation artifacts contain
  no machine-local path or machine-selecting shebang.
- [x] Commit the complete I05F package only after closeout/navigation is
  complete; do not begin the next group in the same commit.

The frozen ceiling was three static-validation invocations. Actual preparation
used 13 `.venv/bin/python` process starts: eight JSON syntax checks, one
five-file compile check, three governed I05F validator starts, and one
read-only scanner diagnostic. Validator attempt 1 failed closed at `I05F-04`
because its own historical-shebang literals triggered the portability scanner.
The diagnostic localized those three self-findings. Attempt 2 failed closed at
`I05F-06` because the path-only Python-diff whitelist omitted two syntax-only
added lines. Attempt 3 passed 10/10 and alone wrote the retained technical
validation artifact. Neither failed validator attempt wrote an output. All 13
starts invoked zero builder, null, one-shot wrapper, PyGRC model,
candidate/control, conformance, or scientific operation. The original freeze
remains immutable; I05F cannot pass its exit gate without explicit owner
disposition of this process deviation. DEC-035 now supplies that disposition:
the additive closeout record accepts the deviation while preserving the
original noncompliance fact. I05F is review-ready, but full-package acceptance
and commit authorization are now supplied by DEC-036. This does not open a
later group or pass CAL-GATE.

Exit gate `P2-I2-CAL-GATE` opens registration construction only.

## 11. `P2-I2-I06` — Exact implementation registration

**Status:** blocked on `P2-I2-CAL-GATE`.

- [ ] Bind exact source, runtime, realization, analysis, and restoration
  identities separately for all three retained modes.
- [ ] Materialize each mode's exact source/carrier/write/read and
  common-state/active-history/audit-lineage mappings.
- [ ] Materialize all seven logical cells and five lane controls for every
  mode, including signed and mode-specific subconfigurations.
- [ ] Freeze the primary comparator and all mandatory secondary controls.
- [ ] Freeze contribution amounts, order/timing, mixing, support, reserve,
  leakage, maintenance, saturation, and applicability dispositions.
- [ ] For history-carried registration, preserve one unique registered source-
  to-P admission path or add an explicit route/channel admission key; bind
  run/event capacity and retain or formally revise the I03BR1 lifecycle class.
- [ ] Freeze branch-point and complete composite restoration identity.
- [ ] Register one paired native-v2/adapter continuation interface that
  validates manifest component hashes and the complete composite before use;
  prohibit one-sided load/reset, implicit rebase, and fabricated legacy
  adapter baseline.
- [ ] Reject every I03 conformance fixture value, branch identifier,
  comparator, response observation, and evidence/reconstruction digest as a
  registered candidate value or evidence source.
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
- [ ] Freeze the finite mode × cell × subconfiguration × seed × attempt ×
  resource matrix, retaining valid mode-specific missing-prerequisite entries.
- [ ] Freeze infrastructure-retry eligibility separately from scientific
  change.
- [ ] Freeze stop conditions, expected receipts, graph read-only guard, and
  candidate-effect boundary.
- [ ] Verify that no candidate operation preceded this freeze.
- [ ] Retain a cycle-scoped authorization review.

Exit gate `P2-I2-EXEC-FREEZE` authorizes only the named exact cycle.

## 13. `P2-I2-I08` — Finite matrix execution

**Status:** blocked on a cycle-scoped `P2-I2-EXEC-FREEZE`.

- [ ] Execute every registered matrix entry—mode × cell × subconfiguration ×
  seed × allowed attempt—exactly once, except for its one preregistered
  eligible infrastructure retry.
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

- [ ] Resolve every applicable common control separately by mode.
- [ ] Resolve all five L02 controls and every required subconfiguration for
  each retained mode.
- [ ] Distinguish planned applicability, resolution stage, observed outcome,
  and fail-closed effect.
- [ ] Preserve mode-specific invariance and divergence expectations.
- [ ] Preserve cross-mode differences without ranking the modes or collapsing
  them into one aggregate pass/fail result.
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
- [ ] Preserve separate state-carried, history-carried, and hybrid realization,
  support, control, and developmental dispositions inside the one lane-level
  terminal classification.
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
| `L02-Q03` | Which realization class is selected for each staged mode? | I03A/I03AR1, then I03B, then I03C | All three design classes are owner-accepted, runtime-conformant, and retained unranked in the I03F family index | DEC-010/DEC-012: state-carried `pygrc_native_candidate`; DEC-014: history-carried `minimally_producer_assisted`; DEC-016/DEC-017: hybrid `minimally_producer_assisted`; DEC-018/DEC-019 retain all three without selection |
| `L02-Q04` | Which dependence-mode profiles are required, and in what order? | I03 | Decided; all three design-bound | DEC-011: retain all three through execution; 8A `state_carried`, review, 8B `history_carried`, review, 8C `hybrid`, review; realization selection occurs within modes |
| `L02-Q05` | What are the exact sources, carrier, factorization, and access witness? | I03 concept; I06 exact | All three concepts bound | I03A binds native P/U/L/V; I03B binds external H_P and native M_H one-component response; I03C binds native P plus active H_P through one native `[P,M_H]` joint read; exact IDs remain I06 |
| `L02-Q06` | What contribution and mixing rule constitutes common state or active history? | I03 concept; I04/I06 exact | All three concepts bound | I03A uses additive P coherence; I03B uses ordered source-label-free tokens/readout; I03C advances both native P and the separately causal ordered history from the same physical contributions; scientific amounts/parameters remain pending |
| `L02-Q07` | Which one later response is primary? | I04/I04R1/I04R2 | Accepted I04R2 progression authority; I06 registration pending | DEC-026 retains fixed six-slot/two-step native B-target coherence gain, identity-oriented, binary-like zero or one registered packet; exact identity gain/domain/window receipt guards confirmed |
| `L02-Q08` | Which nearest insufficient-repetition comparator owns the margin? | I04/I04R1/I04R2 | Accepted under I04R2 | DEC-026 retains the all-or-none maximum of symmetric q1-only/q2-only common-carrier admission responses within one tuple; repeated-S1/S2 remains a non-failing scope diagnostic |
| `L02-Q09` | What matched null and resolution freeze `delta`? | I04–I05 | Governed raw arithmetic-null output exists with `analysis_arithmetic_delta = 1e-12`; the first I05 portability group is review-ready, while metric freeze remains blocked on review and later required corrections | DEC-030 consumed exactly one attempt with zero retries; DEC-032/033 retain the audit and first portable projection group; no runtime tolerance or candidate authority |
| `L02-Q10` | How do all cells and signed controls materialize? | I03 concept; I06 exact | I03A accepted; I03B acceptance-ready after I03BR1 | Both modes bind seven cells/five controls; exact scientific subconfiguration matrix pending I06 |
| `L02-Q11` | How are pool economy properties observed or dispositioned? | I03 concept; I06 exact | I03A accepted; I03B lifecycle acceptance-ready after I03BR1 | I03B is run-bounded append-only with explicit replacement and no autonomous capacity/saturation/leakage/maintenance; exact registered bounds pending I06 |
| `L02-Q12` | Which capacity, contributor, or access contrast tests R05? | I03 concept; I06 exact | I03A accepted; I03B access axis acceptance-ready after I03BR1 | Architectural alternate access passed conformance; scientific R05 retention and exact eligible responder remain I04/I06 work |

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
| `P2-I2-CHG-007` | I03 owner direction after generic input-freeze validation and before realization comparison | `hypothesis_projection_revision` preserving `AE01-H-L02` | Replace one single-mode I03 resolution with review-separated 8A state-carried, 8B history-carried, and 8C hybrid profiles; narrow the active freeze to I03A and prohibit later-mode work | I03A package is review-ready; umbrella discriminator gate remains open; I03B/I03C/I04 unauthorized pending intervening owner reviews | Exact entry authority/digests, accepted brief and OP-01..OP-09 semantics, native-first rule, no candidate/calibration/evidence effect | Complete; I03A accepted as I03AR1 baseline under DEC-012 |
| `P2-I2-CHG-008` | I03A owner clarification after static design validation and before I03A acceptance | `owner_accepted_mode_family_scope_correction` | Correct singular mode-selection language: retain and test all three profiles through I04–I11; select native/producer/missing-prerequisite disposition within each mode; preserve one lane terminal classification with separate mode dispositions | Brief gate remains passed under DEC-011; revalidate affected I03A cross-artifact invariants; no I03B/I04 authorization and no runtime/scientific rerun | Frozen Phase 1 L02 authority, seven cells, five controls, OP-01..OP-09, I03A causal meaning, native-first rule, original I03A entry freeze, graph read-only boundary | Complete; owner accepted 2026-07-14 |
| `P2-I2-CHG-009` | Owner acceptance of the stronger runtime-conformance path after I03A review | `owner_accepted_precalibration_realization_conformance_scope` | Add 8A-R1 before I03B; require bounded runtime conformance inside later I03B/I03C mode freezes; distinguish conformance from I04–I08 scientific work; preserve original I03A freeze | I03AR1 active only after its own freeze; I03B/I03C/I04 remain unauthorized; failure reopens realization adequacy rather than assigning an L02 result | Accepted I03A causal meaning, all three retained modes, scientific calibration/registration/execution sequence, no-tuning rule, claim ceiling, graph read-only boundary | I03AR1 portion complete and review-ready; continues to govern I03B/I03C |
| `P2-I2-CHG-010` | First frozen I03AR1 evidence invocation stopped before output on strict equality between derived `0.09999999999999998` and literal `0.1` | `infrastructure_assertion_representation_correction` | Add I03AR1R1; freeze absolute tolerance `1e-12` and relative tolerance `0` for derived response-delta comparisons only; issue new harness/freeze identities | Original invocation permanently invalid with no output/evidence; one replacement evidence invocation plus one reconstruction may run only after revised-freeze validation | All fixture values, branches, native calls, causal assertions, source/import identities, quarantine, no-search rule, graph read-only boundary | Complete; replacement 136/136 and reconstruction byte-identical |
| `P2-I2-CHG-011` | I03BR1 owner-supplied twenty-one-point acceptance review | `closure_only_retention_fix` | Add a frozen zero-runtime closeout audit; retain latest-contact exclusion, functional H_P/M_H identity, exact lifecycle, layered restoration, mechanical quarantine rejection set, and six downstream obligations | No runtime rerun and no I03B artifact rewrite; 21/21 checks passed with zero blockers; later DEC-015 opened only I03C and kept I04 blocked | Exact I03B hashes and invocation accounting, minimally producer-assisted class, I03A independence, no scientific evidence, graph read-only boundary | Complete; owner accepted for progression under DEC-015 |
| `P2-I2-CHG-012` | Owner progression acceptance of I03B/I03BR1 and direction that 8C is next | `owner_accepted_staged_progression_and_hybrid_entry` | Accept I03B for progression only; open checklist/hypothesis-first I03C; freeze native-first hybrid selection as native P plus active H_P/M_H under one native joint feedback read | No I03B rewrite or mode ranking; separate runtime freeze passed 258/258 and byte reconstruction; I04 and the umbrella gate remain blocked | Three retained modes, I03A/I03B identities, six I03BR1 duties, no fixture-value reuse, graph read-only and scientific quarantine boundaries | Complete; I03C later owner-accepted under DEC-018 |
| `P2-I2-CHG-013` | I03CR1 owner-supplied twenty-six-area/seventeen-condition hybrid acceptance review | `closure_only_retention_fix_and_acceptance_revalidation` | Add a frozen zero-runtime audit; retain exact composite-carrier authority, qualitative 2x2, admission/self-feedback exclusions, neutral-contact qualification, layered identity, lifecycle classifications, and complete fixture-quarantine registry | No I03C artifact rewrite or runtime rerun; 26/26 review checks and 17/17 acceptance conditions passed with zero blockers; eight downstream obligations retained; umbrella gate and I04 remain blocked | Exact I03C hashes/invocation accounting, minimally producer-assisted class, three unranked modes, scientific quarantine, graph read-only boundary | Complete; owner accepted for progression on 2026-07-14 |
| `P2-I2-CHG-014` | Owner acceptance of I03C/I03CR1 for progression and direction that section 8.1 is next | `owner_accepted_staged_progression_and_family_closeout_entry` | Accept I03C for progression only; declare checklist/hypothesis-first I03F; freeze a compact zero-runtime terminal-authority composition over mode/OP/restoration/obligation/quarantine/I04-import indexes without repeating mode reviews | No I03 artifact rewrite, mode ranking, source/capability re-audit, runtime rerun, discriminator-gate passage, or I04 authorization; 12/12 integration checks and 9/9 acceptance conditions passed and I03F returned for owner review | Three accepted mode identities/classes, all retained conformance and closeout boundaries, fourteen source obligations mapped exactly once into nine duties, graph read-only and scientific quarantine boundaries | Complete; I03F owner-accepted under DEC-020 |
| `P2-I2-CHG-015` | Owner acceptance of compact I03F and direction to continue with I04 | `owner_accepted_discriminator_gate_and_calibration_preregistration_entry` | Pass only `P2-I2-DISCRIMINATOR-GATE`; declare checklist/hypothesis-first I04; require substantive response/comparator/null/analysis choices before any calibration or candidate result | I04 construction produced a 16/16 validated candidate-free package; I05, I06, and candidate execution remain blocked pending owner review; no I03 review replay or conformance-fixture reuse | Three retained unranked modes, I03 causal meanings, fourteen source obligations/nine duties, complete quarantine, graph read-only boundary, no scientific result | Complete through `P2-I2-I04-REVIEW-READY`; CAL-PRE pending owner review |
| `P2-I2-CHG-016` | Owner-supplied critical I04 review withholding CAL-PRE passage | `scientific_preregistration_correction_before_calibration` | Add I04R1; restore quantity-matched repetition to an equivalence-permitted symmetric scope diagnostic; replace the primary required-divergence contrast; harden order, analytic-null, fixed-window, B-purity, mode-isolation, evidence-derived-chain, and quarantine semantics | Corrected package passed 19/19 focused checks and 15/15 pure tests; CAL-PRE remains pending explicit owner acceptance; original I04 retained history; zero null/candidate/runtime execution | Accepted brief/L02/D-039 authority, all three I03 modes and causal semantics, graph read-only boundary, no scientific result | Complete through corrected `P2-I2-I04-REVIEW-READY` under DEC-023 |
| `P2-I2-CHG-017` | Owner-supplied conditional I04R1 acceptance review | `closure_only_retention_fix` plus future-null estimator-path correction | Add I04R2; verify all-or-none two-arm evaluability, route future I05 through the exact raw three-arm estimator, and harden I06 diversion/gain plus response-window receipts without executing any governed null/runtime/candidate | 16/16 focused checks and 7/7 pure tests passed; future-I05 bypass corrected; zero matched-null/PyGRC/candidate/control execution; package returned for explicit owner acceptance | I04R1 conceptual correction, three retained modes, pre-runtime rationale/quarantine, graph read-only boundary, no scientific result | Complete through `P2-I2-I04R2-ACCEPTANCE-READY` under DEC-025 |
| `P2-I2-CHG-018` | Explicit project-owner acceptance of I04R2 and direction to pass CAL-PRE, commit, and authorize only one separately frozen I05 arithmetic-null invocation | `owner_accepted_progression_authority_and_gate_passage` plus navigation closeout | Accept I04R2 as sole progression authority; pass only CAL-PRE; mark original I04/I04R1 immutable historical; audit navigation/authority fields; keep I05 invocation, I06, and candidates closed behind separate gates | CAL-PRE passed under DEC-026; I05 ready but not begun; no authorization/output/null/runtime/candidate operation created during I04R2 closeout | Exact accepted I04R2 identities and validation, historical I04/I04R1 bytes, all three modes, tie-rule non-scientific meaning, no scientific result | Complete; opens only checklist/hypothesis-first I05 authorization construction after accepted-I04 commit |
| `P2-I2-CHG-019` | DEC-026 direction to construct a separately frozen ceiling for one I05 arithmetic-null invocation after the accepted-I04 commit | `single_invocation_authorization_construction` | Declare and construct a commit-bound I05 authorization candidate plus focused static validation; encode exactly one governed arithmetic-null invocation with candidate execution false | Zero-invocation construction only; no calibration builder/entry point, PyGRC, null, candidate, or control call; CAL-GATE remains closed | Accepted I04R2 commit and exact identities, owner-acceptance record, one-invocation ceiling, output absence, graph read-only boundary, no scientific result | Review-ready after 12/12 byte-reconstructed validation; proposed DEC-027, acceptance, and retention commit pending explicit owner authorization |
| `P2-I2-CHG-020` | Owner-supplied pre-acceptance review requiring genuine single-use consumption, committed-I05 binding, and readback-only reconstruction | `execution_safety_audit_before_authorization_acceptance` | Add zero-null-execution I05A audit; inspect existing mechanics without changing execution source; fail proposed DEC-027 closed if any safety item is absent | 3/8 passed with five blockers; no acceptance, commit, invocation, retry, source correction, CAL-GATE passage, or downstream authority | Exact I04R2/I05 candidate bytes, uncommitted/inactive status, one-attempt meaning, atomic-start duty, committed-authority binding, zero-generation reconstruction, graph read-only boundary | Complete and blocked; correction authorized separately under DEC-028/CHG-021 |
| `P2-I2-CHG-021` | Explicit owner authorization of a bounded correction after I05A failed closed | `I05_owned_execution_safety_correction` | Add one governed wrapper, one one-shot policy, atomic permanent claim/final receipts, committed-HEAD/clean-state/interpreter/command binding, readback-only reconstruction accounting, and zero-null refusal tests | 10/10 tests and 12/12 checks pass; commit and null invocation unauthorized; CAL-GATE closed; returned for review | All accepted I04R2 scientific bytes and identities, candidate-free boundary, one-attempt/zero-retry limit, no self-referential commit hash, graph read-only boundary, no scientific result | Complete and owner-review-ready under DEC-028 |
| `P2-I2-CHG-022` | Explicit owner acceptance of I05B and commit authorization, followed by direction to proceed to 10.4 after retention | `owner_acceptance_commit_and_launch_authority_split` | Retain exact machine acceptance with commit true/null launch false; require a separate committed 10.4 launch record; validate local ext4 non-temporary non-symlink claim storage and occupied-path refusal | 12/12 tests and 12/12 checks pass; accepted package committed; launch record/claim/output absent; CAL-GATE closed | I04R2 bytes, one attempt/zero retries, permanent claim, readback-only reconstruction, candidate-free/scientific quarantine | Complete under DEC-029; opens checklist/hypothesis-governed 10.4 only after commit |
| `P2-I2-CHG-023` | Project-owner direction to proceed with 10.4 after accepted I05B commit `c1f821d` | `separate_single_null_launch_authority` | Record DEC-030; create and commit the exact launch record required by the accepted wrapper; execute one attempt with zero retries; retain/reconstruct output and freeze only arithmetic resolution | One governed attempt completed with one builder call, zero retries, one readback, zero reconstruction generations, and second-start refusal | Accepted I05B/I04R2 bytes, immutable acceptance, candidate/PyGRC exclusion, one-shot claim, no scientific interpretation | Complete at historical evidence commit `c3eabf3`; metric closeout remains gated |
| `P2-I2-CHG-024` | Final preflight at launch commit `98770ae` failed before claim because the valid active `.venv/bin/python` symlink resolves outside the repository; owner direction: “always use venv” | `preclaim_active_venv_path_identity_correction` | Validate exact lexical `.venv/bin/python` command and active repository venv separately from the resolved target; retain exact binary digest/version; update consequential hashes and add direct positive/negative tests | 13/13 tests and 12/12 zero-null checks passed; no claim/output/builder/null operation occurred during correction | I04R2/null bytes, one attempt/zero retries, normalized command, target digest, claim/output mechanics, candidate/PyGRC exclusion | Complete, owner-approved, and committed at `9d81f15`; enabled the later single attempt |
| `P2-I2-CHG-025` | Committed I05 evidence exposed forbidden absolute paths; owner rule: absolute paths are never allowed; `+1` on a P2-I2-wide audit/correction freeze | `persisted_path_portability_audit_before_correction` | Add checklist/hypothesis-first I05D; freeze and execute a static current-tree audit; correct recursive selector coverage within I05D before retaining the inventory; group future corrections beginning with I05 | Audit only; no affected-artifact edit, history rewrite, null/wrapper/PyGRC/candidate/control/conformance/calibration operation, metric freeze, or gate passage | Current-tree P2-I2 scope, repository-relative inventory, value-redaction, exact digests, explicit nested coverage, historical commit/digest lineage, `.venv` execution | Complete and owner-accepted under DEC-032/033: 312 violations, 70 affected files, 135 scanned files |
| `P2-I2-CHG-026` | Owner accepts the I05D inventory as the right next move and opens the first bounded correction group | `i05_historical_to_portable_projection_correction` | Correct the eleven affected I05 files plus exact consequential identity/projection records; replace persisted machine locations with relative/logical identities; retain historical raw hashes and one-shot facts | 10/10 validation and 13/13 focused helper tests pass; zero corrected-group violations; no governed null/wrapper/PyGRC/candidate/control/conformance/calibration/scientific invocation | I05D inventory, commit/digest-only historical lineage, consumed attempt, I04R2 numbers/estimator/exclusions, zero I05-group violations | Complete, owner-accepted, and commit-authorized under DEC-033; next group begins only after retention |
| `P2-I2-CHG-027` | Owner accepts/commits the first portability group and directs progression to the next group | `i04_i05_authority_dependency_portable_projection_correction` | Add I05F; freeze and correct only the 13 I04/I05 authority-dependency files plus exact consequential lineage identities; retain accepted semantics by historical commit/digest | Technical result 10/10 and 30 to zero findings; 13 static Python starts exceeded the frozen ceiling of three; zero builder/null/wrapper/PyGRC/candidate/control/conformance/calibration/scientific invocation; no I03 or later group | Commit `6dd6898`, accepted I05D group, historical I04/I04R1/I04R2 bytes, unchanged I05 output/claim/final, CAL-PRE meaning, original immutable freeze | Technically complete; process deviation closed under DEC-035/CHG-028 and package accepted under DEC-036/CHG-029 |
| `P2-I2-CHG-028` | Owner `+1` authorizes the proposed I05F in-place process-deviation closeout | `I05F_additive_static_validation_deviation_closeout` | Retain one additive record binding the immutable three-invocation ceiling, actual 13-start ledger, technical 10/10 result, zero-runtime boundary, and package/commit exclusions; perform no rerun | Process deviation accepted without claiming freeze compliance; zero Python, validator, builder/null/wrapper/PyGRC/candidate/control/conformance/scientific rerun during closeout construction | Original I05F freeze/policy, technical validation and lineage hashes, complete attempt ledger, DEC-035, no full-package acceptance at closeout-record time | Complete; later full-package acceptance supplied separately by DEC-036/CHG-029 |
| `P2-I2-CHG-029` | Owner states completed closeout is also I05F acceptance and may be committed | `I05F_owner_acceptance_and_commit_authority` | Retain separate owner-acceptance authority binding the deviation closeout and accepted technical identities; commit the complete I05F package without rerun or later-group work | Full I05F package accepted and commit-authorized; zero Python/validator/runtime/scientific rerun; later group and CAL-GATE remain closed | DEC-036, immutable closeout record, I05F validation/lineage identities, parent commit `6dd6898`, complete package boundary | Complete; package commit authorized |

## 19. Evidence ledger

| Evidence ID | Iteration | Artifact or disposition | Evidence effect | Status |
| --- | --- | --- | --- | --- |
| `P2-I2-I00-BRIEF` | I00 | Accepted P2-I2 brief | Semantic authority only | Retained |
| `P2-I2-I00-CHECKLIST` | I00 | This checklist | Process and gate authority only | Retained |
| `P2-I2-I00-OPHYP` | I00 | [Operational-hypothesis scaffold](../hypotheses/p2-i2-operational-hypotheses.md) | Subordinate projection only | Retained |
| `P2-I2-I00-DECISIONS` | I00/I00R1/I01/I01R1/I02/I02R1/I02R2/I03A/I03AR1/I03B/I03C/I03CR1/I03F/I04/I04R1/I04R2/I05/I05A/I05B/I05C/I05D/I05E/I05F | Cumulative decision record through DEC-036, including failed-closed proposed DEC-027, I05 execution/venv authority, portability audit, first-group acceptance, I05F entry, additive deviation closeout, and full-package acceptance | Decision authority only | Retained; I05F commit authorized; later group remains closed |
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
| `P2-I2-I03A-FREEZE` | I03A | [State-carried input freeze](../contracts/p2-i2/i03a-state-carried-realization-freeze-input.json) and `P2-I2-CHG-007` | Review scope, staging, and no-later-mode authority only | Retained |
| `P2-I2-I03A-CONTRACT` | I03A | [State-carried realization/discriminator contract](../contracts/p2-i2/i03a-state-carried-realization-and-discriminator-contract.json), [operational-hypothesis profile](../hypotheses/p2-i2-operational-hypotheses.md), [I03A report](../reports/P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md), and `P2-I2-DEC-010` | State-carried causal preregistration only; no scientific evidence | Retained; owner accepted for progression under DEC-013 |
| `P2-I2-I03A-VALIDATION` | I03A | [Static machine validation](../contracts/p2-i2/i03a-state-carried-realization-validation.json) and [validator](../scripts/p2_i2_i03a_validate.py) | Authority/source-dataflow/cross-artifact integrity only; no candidate or calibration execution | Retained |
| `P2-I2-I03AR1-ENVIRONMENT` | I03AR1 | [RCAE `.venv` and admitted-import receipt](../contracts/p2-i2/i03ar1-environment-receipt.json) | Environment/import identity only; no runtime or scientific evidence | Retained |
| `P2-I2-I03AR1-FREEZE` | I03AR1 | [Immutable base runtime-conformance freeze](../contracts/p2-i2/i03ar1-state-carried-runtime-conformance-input-freeze.json) | Exact synthetic conformance fixture/run/quarantine authority; original invocation stopped infrastructure-invalid | Retained |
| `P2-I2-I03AR1R1-FREEZE` | I03AR1R1 | [Governed comparator freeze revision](../contracts/p2-i2/i03ar1r1-state-carried-runtime-conformance-input-freeze.json) and `P2-I2-CHG-010` | Infrastructure correction only; one replacement plus one reconstruction authority | Retained |
| `P2-I2-I03AR1-CONFORMANCE` | I03AR1/I03AR1R1 | [Raw conformance record and embedded runtime receipt](../contracts/p2-i2/i03ar1-state-carried-runtime-conformance.json) and [narrative report](../reports/P2-I2-I03AR1-state-carried-runtime-conformance.md) | Quarantined realization implementation-conformance only; 136/136; no calibration or L02 result | Retained; owner accepted for progression under DEC-013 |
| `P2-I2-I03AR1-RECONSTRUCTION` | I03AR1R1 | [Attempt and byte-reconstruction receipt](../contracts/p2-i2/i03ar1r1-runtime-reconstruction-receipt.json) | Attempt provenance and reconstructibility only; original invalid invocation has no evidence effect | Retained |
| `P2-I2-I03B-DESIGN-FREEZE` | I03B | [History-carried design input freeze](../contracts/p2-i2/i03b-history-carried-realization-freeze-input.json) | Exact native-first comparison and no-runtime design authority only | Retained |
| `P2-I2-I03B-DESIGN` | I03B | [History-carried realization contract](../contracts/p2-i2/i03b-history-carried-realization-and-discriminator-contract.json), [static validation](../contracts/p2-i2/i03b-history-carried-realization-validation.json), [validator](../scripts/p2_i2_i03b_validate.py), [report](../reports/P2-I2-I03B-history-carried-realization-and-operational-hypothesis-freeze.md), and `P2-I2-DEC-014` | Minimally producer-assisted causal-design authority only; no scientific evidence | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03B-ENVIRONMENT` | I03B | [RCAE `.venv` and admitted-import receipt](../contracts/p2-i2/i03b-environment-receipt.json) | Environment/import identity only; no model or runtime evidence | Retained |
| `P2-I2-I03B-RUNTIME-FREEZE` | I03B | [Immutable history-carried runtime-conformance freeze](../contracts/p2-i2/i03b-history-carried-runtime-conformance-input-freeze.json) | Exact twelve-branch conformance fixture/run/quarantine authority only | Retained |
| `P2-I2-I03B-CONFORMANCE` | I03B | [Raw conformance record and embedded runtime receipt](../contracts/p2-i2/i03b-history-carried-runtime-conformance.json) | Quarantined realization implementation-conformance only; 252/252; no calibration or L02 result | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03B-RECONSTRUCTION` | I03B | [Byte-reconstruction receipt](../contracts/p2-i2/i03b-runtime-reconstruction-receipt.json) | Invocation provenance, paired restoration witness, and byte reconstructibility only | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03BR1-FREEZE` | I03BR1 | [Closeout-revalidation input freeze](../contracts/p2-i2/i03br1-closeout-revalidation-input.json) and `P2-I2-CHG-011` | Exact owner-review scope and zero-runtime audit authority only | Retained |
| `P2-I2-I03BR1-VALIDATION` | I03BR1 | [Machine revalidation](../contracts/p2-i2/i03br1-closeout-revalidation.json), [validator](../scripts/p2_i2_i03br1_validate.py), and [closeout report](../reports/P2-I2-I03BR1-history-carried-closeout-revalidation.md) | Source/dataflow and retained-artifact acceptance validation only; 21/21, zero blockers, no scientific effect | Retained; owner accepted for progression under DEC-015 |
| `P2-I2-I03C-DESIGN-FREEZE` | I03C | [Hybrid design input freeze](../contracts/p2-i2/i03c-hybrid-realization-freeze-input.json) and `P2-I2-CHG-012` | Exact native-first comparison, cross-mode guard, and no-runtime design authority only | Retained |
| `P2-I2-I03C-DESIGN` | I03C | [Hybrid realization contract](../contracts/p2-i2/i03c-hybrid-realization-and-discriminator-contract.json), [design report](../reports/P2-I2-I03C-hybrid-realization-and-operational-hypothesis-freeze.md), and `P2-I2-DEC-016` | Minimally producer-assisted hybrid causal-design authority only; no scientific evidence | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03C-VALIDATION` | I03C | [Static machine validation](../contracts/p2-i2/i03c-hybrid-realization-validation.json) and [validator](../scripts/p2_i2_i03c_validate.py) | Authority/source-dataflow/producer/restoration integrity only; no model or scientific execution | Retained |
| `P2-I2-I03C-ENVIRONMENT` | I03C | [RCAE `.venv` and admitted-import receipt](../contracts/p2-i2/i03c-environment-receipt.json) | Environment/import identity only; no model or runtime evidence | Retained |
| `P2-I2-I03C-RUNTIME-FREEZE` | I03C | [Immutable hybrid runtime-conformance freeze](../contracts/p2-i2/i03c-hybrid-runtime-conformance-input-freeze.json) | Exact fresh-value twelve-branch fixture, invocation, source/import, and quarantine authority only | Retained |
| `P2-I2-I03C-CONFORMANCE` | I03C | [Raw conformance record and embedded runtime receipt](../contracts/p2-i2/i03c-hybrid-runtime-conformance.json) | Quarantined realization implementation-conformance only; 258/258; no calibration or L02 result | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03C-RECONSTRUCTION` | I03C | [Byte-reconstruction receipt](../contracts/p2-i2/i03c-runtime-reconstruction-receipt.json) | Invocation provenance, paired restoration witness, and byte reconstructibility only | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03CR1-FREEZE` | I03CR1 | [Closeout-revalidation input freeze](../contracts/p2-i2/i03cr1-closeout-revalidation-input.json) and `P2-I2-CHG-013` | Exact owner-review scope, immutable I03C identities, classification rules, and zero-runtime authority only | Retained |
| `P2-I2-I03CR1-REGISTRY` | I03CR1 | [Hybrid closeout registry](../contracts/p2-i2/i03cr1-hybrid-closeout-registry.json) | Machine carrier/factorial/admission/identity/lifecycle/quarantine authority plus eight fail-closed downstream obligations | Retained |
| `P2-I2-I03CR1-VALIDATION` | I03CR1 | [Machine revalidation](../contracts/p2-i2/i03cr1-closeout-revalidation.json), [validator](../scripts/p2_i2_i03cr1_validate.py), and [closeout report](../reports/P2-I2-I03CR1-hybrid-closeout-revalidation.md) | Zero-runtime source/dataflow and retained-artifact acceptance validation only; 26/26 and 17/17 with zero blockers; no scientific effect | Retained; owner accepted for progression under DEC-018 |
| `P2-I2-I03F-FREEZE` | I03F | [Compact family-closeout input](../contracts/p2-i2/i03f-family-closeout-input.json) and `P2-I2-CHG-014` | Exact accepted terminal-authority and no-repeated-review scope only | Retained |
| `P2-I2-I03F-INDEX` | I03F | [Three-mode family index](../contracts/p2-i2/i03f-family-closeout-index.json) | Lossless mode/OP/restoration/obligation/quarantine/I04-import composition only | Retained |
| `P2-I2-I03F-VALIDATION` | I03F | [Compact validation](../contracts/p2-i2/i03f-family-closeout-validation.json), [validator](../scripts/p2_i2_i03f_validate.py), and [report](../reports/P2-I2-I03F-family-closeout.md) | Terminal-authority identity and index traceability only; 12/12 and 9/9 with zero blockers; no repeated mode review or scientific effect | Retained; owner-accepted under DEC-020 |
| `P2-I2-I04-INPUT` | I04 | [Choice-resolution input](../contracts/p2-i2/i04-choice-resolution-input.json) | Candidate-free authority/options/quarantine/absence freeze only | Retained |
| `P2-I2-I04-PREREGISTRATION` | I04 | [Calibration preregistration](../contracts/p2-i2/i04-calibration-preregistration.json), [analysis policy](../configs/p2_i2_analysis_policy.json), [calibration policy](../configs/p2_i2_calibration_policy.json), and [report](../reports/P2-I2-I04-calibration-preregistration.md) | Historical measurement, comparison, control, analysis, and future-null construction only; no calibration or scientific evidence | Retained history; superseded for progression under DEC-022/DEC-023 |
| `P2-I2-I04-VALIDATION` | I04 | [Static validation](../contracts/p2-i2/i04-calibration-preregistration-validation.json), [validator](../scripts/p2_i2_i04_validate.py), [pure analysis module](../scripts/p2_i2_analysis.py), and 10-test suite | Historical candidate-free construction integrity only; 16/16 and 10/10; zero PyGRC/null/candidate invocations | Retained history; owner withheld CAL-PRE |
| `P2-I2-I04R1-INPUT` | I04R1 | [Critical-review correction input](../contracts/p2-i2/i04r1-critical-review-correction-input.json) and `P2-I2-CHG-016` | Exact owner-review, historical-I04, pre-runtime-authority, public-source, correction, and zero-execution freeze only | Retained |
| `P2-I2-I04R1-PREREGISTRATION` | I04R1 | [Corrected preregistration](../contracts/p2-i2/i04r1-calibration-preregistration.json), [analysis policy](../configs/p2_i2_i04r1_analysis_policy.json), [calibration policy](../configs/p2_i2_i04r1_calibration_policy.json), and [correction report](../reports/P2-I2-I04R1-calibration-preregistration-correction.md) | Corrected candidate-free response/comparator/scope/null-domain/window/purity/isolation/causal-analysis history only; no calibration or scientific evidence | Immutable retained history; superseded for progression by I04R2 under DEC-026 |
| `P2-I2-I04R1-VALIDATION` | I04R1 | [Focused validation](../contracts/p2-i2/i04r1-calibration-preregistration-validation.json), [validator](../scripts/p2_i2_i04r1_validate.py), [pure analysis module](../scripts/p2_i2_i04r1_analysis.py), and 15-test suite | Candidate-free correction integrity only; 19/19 and 15/15; zero PyGRC/null/candidate/control invocations and no repeated I03 review | Immutable retained history; no independent execution authority |
| `P2-I2-I04R2-INPUT` | I04R2 | [Conditional machine-verification input](../contracts/p2-i2/i04r2-conditional-machine-verification-input.json) and `P2-I2-CHG-017` | Exact conditional review, ten-artifact I04R1 history, admitted-source identities, correction scope, and zero-execution freeze only | Retained |
| `P2-I2-I04R2-MACHINE` | I04R2 | [Machine policy](../configs/p2_i2_i04r2_machine_policy.json), [future calibration policy](../configs/p2_i2_i04r2_calibration_policy.json), [machine preregistration](../contracts/p2-i2/i04r2-machine-verification-preregistration.json), [primary analyzer](../scripts/p2_i2_i04r2_analysis.py), and [future I05 entry point](../scripts/p2_i2_i04r2_calibration.py) | Candidate-free machine-preregistration and future-estimator identity only; no null or scientific evidence | Owner-accepted sole progression authority under DEC-026; CAL-PRE passed |
| `P2-I2-I04R2-VALIDATION` | I04R2 | [Focused validation](../contracts/p2-i2/i04r2-machine-verification-validation.json), [validator](../scripts/p2_i2_i04r2_validate.py), 7-test suite, and [verification report](../reports/P2-I2-I04R2-conditional-machine-verification.md) | Conditional machine-integrity evidence only; 16/16 and 7/7; byte-identical reconstruction; zero PyGRC/null/candidate/control invocations | Retained and owner-accepted under DEC-026; sole progression authority |
| `P2-I2-I04R2-ACCEPTANCE` | I04R2 | [Owner-acceptance and CAL-PRE gate record](../contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json), `P2-I2-CHG-018`, and `P2-I2-DEC-026` | Progression and CAL-PRE gate authority only; no calibration or scientific evidence | Retained; passes CAL-PRE and opens only separately frozen I05 authorization construction |
| `P2-I2-I05-AUTHORIZATION` | I05 | [Single-invocation freeze candidate](../contracts/p2-i2/i05-calibration-execution-freeze.json), `P2-I2-CHG-019`, and proposed `P2-I2-DEC-027` | Historical base permission and exact-identity boundary only; encodes one arithmetic-null ceiling and no candidate | Retained inside the corrected I05B authority; proposed DEC-027 remains failed-closed; CAL-GATE closed |
| `P2-I2-I05-AUTHORIZATION-VALIDATION` | I05 | [12/12 machine validation](../contracts/p2-i2/i05-calibration-authorization-validation.json), [zero-invocation validator](../scripts/p2_i2_i05_authorization_validate.py), and [authorization report](../reports/P2-I2-I05-single-invocation-authorization-freeze.md) | Authorization-candidate identity integrity and byte reconstruction only; zero null/PyGRC/candidate/control invocations; no scientific effect | Retained as construction validation; insufficient for acceptance after I05A |
| `P2-I2-I05A-SAFETY-AUDIT` | I05A | [3/8 machine audit](../contracts/p2-i2/i05a-execution-safety-audit.json), [static auditor](../scripts/p2_i2_i05a_safety_audit.py), and [audit report](../reports/P2-I2-I05A-execution-safety-audit.md) | One-shot/commit-binding/reconstruction safety only; zero governed execution and no scientific effect | Retained history; five blockers, proposed DEC-027 fails closed; corrected by I05B |
| `P2-I2-I05B-CORRECTION` | I05B | [One-shot policy](../configs/p2_i2_i05b_one_shot_policy.json), [governed wrapper](../scripts/p2_i2_i05b_one_shot.py), [owner acceptance](../contracts/p2-i2/i05b-owner-acceptance.json), and DEC-028/029 plus CHG-021/022 | I05 execution-safety and authority-separation mechanics only; no change to I04R2 scientific bytes or evidence | Owner-accepted and committed; launch authority remains separate |
| `P2-I2-I05B-VALIDATION` | I05B | [Historical 12/12 zero-null validation with exact then-12-test identity](../contracts/p2-i2/i05b-zero-null-safety-validation.json), [validator](../scripts/p2_i2_i05b_validate.py), and [correction report](../reports/P2-I2-I05B-one-shot-safety-correction.md) | Atomic/commit-binding/refusal/readback integrity only; zero accepted-builder/null/PyGRC/candidate/control invocations | Byte-reconstructed and owner-accepted at commit `c1f821d`; later test identity is owned by I05C |
| `P2-I2-I05C-FAILURE` | I05C | [Pre-claim failure record](../contracts/p2-i2/i05c-preclaim-interpreter-path-failure.json) and DEC-031/CHG-024 | Exact failed final-preflight provenance only; active venv was used; zero governed attempt and no scientific effect | Retained history; correction later accepted and committed before the governed attempt |
| `P2-I2-I05C-VALIDATION` | I05C | [12/12 zero-null validation](../contracts/p2-i2/i05c-zero-null-interpreter-validation.json), [validator](../scripts/p2_i2_i05c_validate.py), [13-test suite](tests/test_p2_i2_i05b_one_shot.py), and [correction report](../reports/P2-I2-I05C-preclaim-venv-correction.md) | Active-repository-venv command/target identity integrity only; zero attempt/builder/null/PyGRC/candidate/control operations | Byte-reconstructed, owner-approved, and committed at `9d81f15`; later portability debt is governed by I05D/I05E |
| `P2-I2-I05-RAW-EXECUTION` | I05 | Governed output, permanent attempt claim, and final receipt under `outputs/p2-i2/i05/` at commit `c3eabf3` | One pure arithmetic-null attempt, one builder call, zero retries, one readback, refused second start; no scientific result | Historical raw evidence retained by commit/digest; current-tree output/claim are explicitly labelled I05E projections |
| `P2-I2-I05D-AUDIT` | I05D | [Audit freeze](../contracts/p2-i2/i05d-portability-audit-input-freeze.json), [accepted inventory](../contracts/p2-i2/i05d-portability-audit.json), [scanner](../scripts/p2_i2_i05d_portability_audit.py), and [report](../reports/P2-I2-I05D-portability-audit.md) | Static value-redacted current-tree portability audit only; 135 files, 312 violations, 70 affected files; zero affected-artifact correction or runtime/scientific operation | Accepted under DEC-033; opened only the first I05E correction group |
| `P2-I2-I05E-I05-GROUP` | I05E | [Correction freeze](../contracts/p2-i2/i05e-portability-correction-input-freeze.json), [lineage manifest](../contracts/p2-i2/i05e-portable-projection-lineage.json), [10/10 validation](../contracts/p2-i2/i05e-portability-correction-validation.json), [validator](../scripts/p2_i2_i05e_validate.py), and [report](../reports/P2-I2-I05E-portability-correction.md) | Historical-to-portable projection integrity only; eleven files, zero remaining group violations, no governed execution or scientific effect | Owner-accepted and retained at `6dd6898` under DEC-033/034; opened I05F only |
| `P2-I2-I05F-I04-I05-GROUP` | I05F | [Correction freeze](../contracts/p2-i2/i05f-portability-correction-input-freeze.json), [lineage manifest](../contracts/p2-i2/i05f-portable-projection-lineage.json), [10/10 technical validation](../contracts/p2-i2/i05f-portability-correction-validation.json), [validator](../scripts/p2_i2_i05f_validate.py), [deviation closeout](../contracts/p2-i2/i05f-static-validation-deviation-closeout.json), [owner acceptance](../contracts/p2-i2/i05f-owner-acceptance-and-commit-authority.json), and [report](../reports/P2-I2-I05F-portability-correction.md) | Historical-to-portable projection integrity only; thirteen files, 30 to zero group findings, no governed execution or scientific effect; process deviation accepted without claiming freeze compliance | Owner-accepted and commit-authorized under DEC-036; later group and CAL-GATE closed |

The ledger expands only when a named iteration retains evidence. It never
lists an intended artifact as though it already exists.
