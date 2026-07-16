# P2-I3 Trail or Stigmergic Field Checklist

**Status:** initial evidence-expandable governance package accepted;
`P2-I3-BRIEF-GATE` passed

**Iteration:** `P2-I3`

**Lane:** `AE01-L03`

**Current activity iteration:** `P2-I3-I00` complete; `P2-I3-I01` input-freeze
construction is open but unstarted, and audit activity remains unauthorized

**Current evidence effect:** none; no source capability, source admission,
realization, calibration, registration, execution, or scientific result

**Semantic authority:**
[accepted P2-I3 brief](P2-I3-trail-or-stigmergic-field-brief.md)

**Cumulative decisions:**
[P2-I3 decision record](P2-I3-decision-record.md)

**Frozen authorities:**
[L03 hypothesis](../hypotheses/lane-hypotheses.md),
[post-R3 ecology-discriminator amendment](../hypotheses/post-r3-ecology-discriminator-amendment.md),
[outcome and stopping contract](../hypotheses/outcome-and-stopping-contract.md),
[developmental interpretation contract](../hypotheses/developmental-interpretation-contract.md),
[common contract](../contracts/common-contract.md), and
[execution policy](../configs/p1_i5_execution_policy.json)

**Program cover:**
[Post-N30 master checklist](../../../implementation/PostN30-checklist.md)

## 1. How to use this checklist

This is the detailed planning, activity, evidence, and learning surface for
P2-I3. The master checklist carries stable program-level cover checks. This
file projects those checks into named lane-local iterations that may expand
from evidence without allowing an active scientific cycle to drift.

The operating rule is:

> No P2-I3 activity occurs off-ledger. Every audit, decision, implementation,
> conformance probe, calibration, registration, execution, control
> resolution, reconstruction, interpretation, or closeout is a named
> checklist iteration with an explicit evidence effect.

Before activity begins, its iteration declaration must fix:

```text
iteration_id
purpose
entry_authority
frozen_inputs_or_input_freeze_action
environment_prerequisites
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
- Creating or changing this checklist is recorded in the change ledger.
- Reading a source while designing an audit is preparation, not audit
  evidence, source admission, or capability proof.
- An iteration may prepare the next iteration's inputs but cannot silently
  perform or pass the next iteration.
- The checklist may expand between frozen candidate cycles. It is immutable
  within an active candidate cycle except for appending observations and
  terminal records required by that freeze.
- Evidence-triggered work receives a stable `P2-I3-CHG-*` identity, a reason,
  an affected iteration, and an explicit rerun scope.
- A failed or surprising result may motivate a new preregistered cycle; it may
  not be patched into the active cycle. Any new scientific question requires a
  separately preregistered cycle that preserves the original result.
- Numeric thresholds are resolution and interpretation ladders. They are not
  automatic accept/reject selectors, and narrow success or informative
  failure must receive developmental interpretation.
- Native, minimally producer-assisted, ecology-owned, constructed, missing,
  and unsuitable roles remain explicit. Transition to newly native behavior
  is deliberate and requires a new registered realization and rerun.
- The graph/PyGRC repository and the geometric-reflexive-coherence repository
  are read-only from this project.
- No terminal checkbox follows from a positive primary metric alone.
- `EXEC-FREEZE` is a one-shot authorization boundary: it first passes as an
  inactive accepted freeze, then activates explicitly, and is consumed at the
  first governed candidate operation. Other gates are not consumed.

### 1.1 Environment completeness rule

Every command-bearing iteration starts with a non-mutating preflight for:

```text
repository-local .venv
required interpreter identity
pinned required packages and versions
iteration-specific executable dependencies
```

If `.venv`, a package, or a required version is absent:

1. stop the affected work;
2. report the exact absence and the command that exposed it;
3. record whether any output or permanent claim was created;
4. ask the project owner to decide installation or repair; and
5. resume only after the accepted environment is verified.

The project must not adapt implementation, validation, scope, or scientific
meaning to an incomplete environment. Missing dependencies are infrastructure
state, never negative evidence or a missing substrate surface.

## 2. Local gate dashboard

| Gate | Meaning | Status | Exit evidence or current blocker |
| --- | --- | --- | --- |
| `P2-I3-BRIEF-GATE` | Accepted semantic brief is projected into an owner-accepted checklist and cumulative decision record | Passed | `P2-I3-DEC-014`; opens only I01 input-freeze construction and review |
| `P2-I3-SOURCE-AUDIT-GATE` | One frozen, source-current, read-only audit answers the accepted capability questions | Unopened | Requires accepted I01 input freeze and resolution of `P2-I3-Q-001` |
| `P2-I3-SOURCE-ADMISSION-GATE` | Exact theory and graph revisions, files, callables, roles, and digests are admitted | Unopened | Requires passed source audit and `P2-I3-Q-002` |
| `P2-I3-DISCRIMINATOR-GATE` | Field realization, dynamic, causal chain, observation boundary, mode family, and operational hypotheses are frozen | Unopened | Requires source admission and decisions resolving `P2-I3-Q-003` through `P2-I3-Q-008`, `Q-013`, and design part of `Q-015` |
| `P2-I3-CAL-PRE-GATE` | Response, comparator, matched null, controls, panels, windows, and candidate-blind calibration inputs are preregistered | Unopened | Requires passed discriminator gate and `P2-I3-Q-009` through `Q-012`, plus `Q-016` |
| `P2-I3-CAL-GATE` | Candidate-blind calibration freezes a reconstructable metric sheet and resolution delta | Unopened | Requires accepted CAL-PRE package and an explicitly authorized calibration invocation |
| `P2-I3-REG-GATE` | Exact topology, values, cells, schedules, controls, identities, resources, and reconstruction bundle are registered | Unopened | Requires passed CAL-GATE and `P2-I3-Q-014` through `Q-018` |
| `P2-I3-EXEC-FREEZE` | One exact inactive candidate cycle is accepted and then explicitly activated | Unopened | Requires passed REG-GATE, clean committed sources, runtime identity, and `P2-I3-Q-019` |
| `P2-I3-EXEC-GATE` | The finite frozen matrix completes or closes validly incomplete without interpretation inflation | Unopened | Candidate execution is unauthorized |
| `P2-I3-CONTROL-GATE` | Every common and L03 control has a compact retained disposition | Unopened | Requires terminal execution records |
| `P2-I3-RECON-GATE` | Artifacts, identities, continuations, reports, and results reconstruct independently | Unopened | Requires retained execution and control evidence |
| `P2-I3-INTERPRET-GATE` | Dynamic relation, rungs, strength, developmental reading, debts, and next move are interpreted | Unopened | Requires passed control and reconstruction gates |
| `P2-I3-CLOSE-GATE` | One bounded terminal classification and claim ceiling close the core lane | Unopened | Requires accepted interpretation and compact control index |

`P2-I3-GATE` in the master checklist is equivalent to
`P2-I3-CLOSE-GATE` here.

## 3. Stable entry and claim boundaries

- [x] `P1-GATE` passed. Evidence:
  [R2 closeout](../reports/R2-closeout.md).
- [x] Review R3 requires a compact lane-local control-resolution index before
  terminal closure. Evidence:
  [R3 review](../reports/R3-contract-adequacy-review.md).
- [x] Stable lane ID is `AE01-L03` and frozen hypothesis ID is
  `AE01-H-L03`.
- [x] The accepted prospective post-R3 D-039 amendment applies: reproducing a
  persistent trace is inherited substrate evidence, not sufficient ecology
  evidence.
- [x] The project owner accepted the P2-I3 brief on 2026-07-16 as semantic
  authority. Evidence: `P2-I3-DEC-001`.
- [x] L03 asks whether repeated costly formation creates an evolving,
  route-local field whose selected non-static dynamic causally changes later
  traversal.
- [x] Registered structure, geometric distance, functional distance,
  causal/proper-time distance, and experimental causal influence are five
  distinct surfaces. Evidence: `P2-I3-DEC-003`.
- [x] The core geometry is the two-route causal kernel; appendices A and B are
  dormant and Appendix C is deferred. Evidence: `P2-I3-DEC-004` and
  `P2-I3-DEC-009`.
- [x] Quantity matching, complete-state matching, current-state relocation,
  and active-history relocation are distinct operational relations. Evidence:
  `P2-I3-DEC-006`.
- [x] Exact frozen rungs remain R01 through R05; no R06 exists. Evidence:
  `P2-I3-DEC-008`.
- [x] Maximum claim remains a bounded trail or stigmergic field demand
  pattern, not a native trail primitive, communication, coordination,
  collective intelligence, agency, organism, motif, regime, or life claim.
- [x] A same-participant result cannot receive the stronger stigmergic-field
  interpretation tag. Evidence: `P2-I3-DEC-007`.
- [x] Brief and governance preparation create no source capability,
  realization, calibration, registration, or result evidence.
- [x] The initial decision record and checklist are accepted by the project
  owner and `P2-I3-BRIEF-GATE` passes. Evidence: `P2-I3-DEC-014`.

## 4. Activity-iteration ledger

| Iteration | Activity | Entry dependency | Status | Exit gate or effect |
| --- | --- | --- | --- | --- |
| `P2-I3-I00` | Accepted-brief projection, cumulative decision record, and evidence-expandable checklist | Owner-accepted semantic brief | Complete and owner-accepted | `P2-I3-BRIEF-GATE=passed`; no scientific evidence |
| `P2-I3-I01` | Source-current read-only capability audit | Passed brief gate | Open for input-freeze construction only; audit unstarted | I01 first constructs/accepts its input freeze; only then may audit activity begin and later pass `P2-I3-SOURCE-AUDIT-GATE` |
| `P2-I3-I02` | Exact theory and graph source admission | Passed source-audit gate | Unopened | May pass `P2-I3-SOURCE-ADMISSION-GATE`; no realization |
| `P2-I3-I03` | Field realization, dynamics, causal factorization, operational hypotheses, and bounded runtime conformance | Passed source-admission gate | Unopened | May pass `P2-I3-DISCRIMINATOR-GATE`; no calibration or candidate evidence |
| `P2-I3-I04` | Calibration preregistration | Passed discriminator gate | Unopened | May pass `P2-I3-CAL-PRE-GATE`; no calibration execution |
| `P2-I3-I05` | Candidate-blind calibration and metric-sheet freeze | Passed CAL-PRE gate and separately accepted invocation freeze | Unopened | May pass `P2-I3-CAL-GATE`; no candidate execution |
| `P2-I3-I06` | Exact implementation registration | Passed CAL-GATE | Unopened | May pass `P2-I3-REG-GATE`; no candidate execution |
| `P2-I3-I07` | Inactive candidate-cycle execution freeze and explicit activation | Passed REG-GATE and clean committed source anchor | Unopened | May pass/consume `P2-I3-EXEC-FREEZE`; no operation before activation |
| `P2-I3-I08` | Frozen finite matrix execution | Consumed active execution freeze | Unopened | May pass or validly close `P2-I3-EXEC-GATE`; no terminal interpretation |
| `P2-I3-I09` | Compact common and lane-control resolution | Retained I08 terminals | Unopened | May pass `P2-I3-CONTROL-GATE` |
| `P2-I3-I10` | Independent reconstruction and identity verification | Retained I08/I09 evidence | Unopened | May pass `P2-I3-RECON-GATE` |
| `P2-I3-I11` | Developmental interpretation, terminal classification, and lane closeout | Passed control and reconstruction gates | Unopened | May pass interpretation and close gates |

No later artifact retroactively completes an earlier iteration. Missing
iteration evidence fails closed and must be reconstructed or explicitly
classified.

## 5. `P2-I3-I00` — Governance bootstrap

**Purpose:** project the accepted semantic brief into stable decision and
activity authority before any source audit or implementation choice.

**Entry authority:** owner acceptance of the revised P2-I3 brief on
2026-07-16.

**Environment prerequisites:** none beyond read/write access to this
repository; no runtime dependency is exercised.

**Mutation boundary:** P2-I3 narrative governance and atlas navigation only.
The graph and theory repositories remain read-only.

**Required outputs:** accepted-status brief, one cumulative decision record,
one evidence-expandable checklist, and master/navigation projections.

**Evidence effect:** governance only.

- [x] The accepted brief records semantic authority without claiming a gate
  passage or scientific evidence.
- [x] One cumulative decision record exists and retains decisions
  `P2-I3-DEC-001` through `P2-I3-DEC-014`.
- [x] Open implementation questions have stable identities
  `P2-I3-Q-001` through `P2-I3-Q-020`.
- [x] This checklist defines named I00-I11 activities and stable cover gates.
- [x] The environment-completeness rule is explicit in the decision record
  and checklist.
- [x] The graph/PyGRC and theory repositories remain read-only.
- [x] No source audit, source admission, realization selection, operational
  hypothesis, calibration, registration, candidate execution, or result was
  inferred from brief preparation.
- [x] The project owner accepts the decision record and checklist as the
  controlling initial P2-I3 governance package.
- [x] `P2-I3-BRIEF-GATE` passes and opens construction of the I01 audit input
  freeze only.

### 5.1 I00 exit boundary

Brief-gate passage requires all of the following:

- [x] The brief clearly separates the inherited persistent-trace relation
  from the ecology-specific dynamic-field discriminator.
- [x] Five distance and causality surfaces are distinct.
- [x] The two-route causal kernel, minimum/strong/highest readings, rungs,
  interpretation tags, and claim ceiling are bounded.
- [x] Future implementation choices are assigned to legitimate decision
  points rather than answered by the brief.
- [x] Negative, missing-surface, constructed, redirective, and surprising
  outcomes remain valid.
- [x] Evidence-responsive expansion is allowed between cycles but cannot
  mutate an active cycle.
- [x] The project owner confirms that this checklist and decision record
  express the accepted operating boundary.

Passing I00 does not itself authorize the I01 audit. It authorizes only
construction and review of the exact I01 input freeze.

## 6. `P2-I3-I01` — Source-current capability audit

**Purpose:** establish what the current public PyGRC and admitted theory
surfaces can actually express before selecting a realization.

**Iteration entry authority:** passed brief gate. This permits construction
and review of the I01 input freeze only.

**Audit-activity entry authority:** accepted resolution of `P2-I3-Q-001` plus
a validated, owner-accepted I01 input freeze.

**Frozen inputs:** exact audit questions, source-revision candidates, path
scope, public-callable rule, allowed read-only commands, and output schema.

**Environment prerequisites:** repository-local `.venv` and every package
required by the accepted audit commands.

**Mutation boundary:** narrative and machine audit outputs in this repository
only. Source repositories are read-only. No candidate-shaped source changes.

**Evidence effect:** source-current capability evidence only; no source
admission and no scientific evidence.

### 6.1 Input freeze before audit activity

- [ ] Resolve `P2-I3-Q-001` through an accepted decision.
- [ ] Freeze the exact graph/PyGRC revision candidate and theory revision
  candidate to inspect.
- [ ] Freeze every in-scope path and capability question.
- [ ] Freeze the rule distinguishing public callable, internal helper,
  pre-existing test evidence, documentation, and inference.
- [ ] Freeze allowed static inspection and pre-existing test commands.
- [ ] Freeze whether any scientific-outcome-free synthetic conformance probe
  is necessary and quarantine it from candidate and capability claims unless
  separately reviewed.
- [ ] Freeze the exact evidence-class distinction:

  ```text
  public_source_fact:
    source-audit authority

  synthetic_probe:
    interface-conformance evidence only

  candidate_shaped_behavior:
    no capability upgrade and no scientific effect
  ```

- [ ] Complete environment preflight without installation.
- [ ] Record the input-freeze review and owner acceptance.

### 6.2 Required audit questions

- [ ] What registered topology can expose two structurally matchable
  alternative routes?
- [ ] Which route-local node, edge, corridor, pulse, feedback, eligibility,
  or state surfaces are publicly observable and alterable through declared
  public operations?
- [ ] For each of form, reinforce, withdraw, decay, maintain, saturate,
  relocate, snapshot, restore, and reset, record a separate native,
  producer-assisted, unsuitable, missing, or unknown disposition with exact
  source evidence.
- [ ] Which scheduler, packet, producer, feedback, and event-order surfaces
  are public and deterministic?
- [ ] Which geometric, functional, and causal/proper-time distances are
  actually exposed, and what runtime roles do they have?
- [ ] Which traversal-visible responses can be measured without a hidden
  controller or global route selector?
- [ ] Can complete continuation-relevant state be enumerated, saved, restored,
  branched, compared, and relocated?
- [ ] Can participant identity, depositor identity, fresh probe identity, and
  direct-address exclusion be represented?
- [ ] Which capabilities are native, producer-assisted by established
  extension patterns, unsuitable, missing, or unknown?
- [ ] Which claims depend only on static inspection, which on pre-existing
  tests, and which remain inference?

### 6.3 Audit outputs and exit

- [ ] Retain a machine-readable capability inventory with exact citations.
- [ ] Retain a human-readable audit report separating facts and inferences.
- [ ] Retain exact command, interpreter, package, revision, and digest
  provenance.
- [ ] Record every missing or unsuitable surface without treating it as a
  scientific null.
- [ ] Independently review the audit against only its frozen input scope.
- [ ] Resolve review findings in one bounded pass or record a new iteration;
  do not begin recursive review-of-review cycles absent a concrete new
  assumption.
- [ ] Owner accepts the audit and passes `P2-I3-SOURCE-AUDIT-GATE`.

## 7. `P2-I3-I02` — Exact source admission

**Purpose:** admit only the exact source surfaces that may constrain or
support P2-I3 realization work.

**Entry authority:** passed source-audit gate.

**Frozen inputs:** accepted I01 inventory and report.

**Environment prerequisites:** complete audit/admission validation environment.

**Mutation boundary:** admission records and validators in this repository;
source repositories remain read-only.

**Evidence effect:** source identity and role authority only.

- [ ] Resolve `P2-I3-Q-002` through an accepted decision.
- [ ] Admit the exact graph/PyGRC revision, files, public callables, and
  pre-existing tests by digest and evidence role.
- [ ] Admit the exact RC-Distance source revision and file, with its role
  bounded to theory/interpretation unless an operational source is separately
  demonstrated.
- [ ] Admit every other theory source by exact revision, path, digest, and
  role; reject vague directory-level authority.
- [ ] Distinguish inherited evidence, ecology interpretation, constructed
  mechanism, missing surface, and proposed discriminator.
- [ ] Record whether existing extension patterns permit RCAE-owned producers
  without changing PyGRC.
- [ ] Record any source transition from historical audit identity to current
  admitted identity.
- [ ] Validate source digests and public callable identities.
- [ ] Independently reconstruct the admission record.
- [ ] Owner accepts the source bundle and passes
  `P2-I3-SOURCE-ADMISSION-GATE`.

The admission bundle selects no field carrier, equation, realization, metric,
or candidate outcome.

## 8. `P2-I3-I03` — Realization, dynamics, and operational hypotheses

**Purpose:** choose and validate a falsifiable field realization that expresses
the accepted ecology discriminator without hiding the answer in a controller.

**Entry authority:** passed source-admission gate.

**Frozen inputs:** admitted sources and accepted brief/decisions.

**Environment prerequisites:** complete repository-local runtime and
validation environment for every accepted conformance command.

**Mutation boundary:** RCAE source, fixtures, schemas, validators, tests,
reports, and quarantined conformance artifacts. PyGRC remains read-only.

**Evidence effect:** implementation adequacy and operational semantics only;
no calibration or candidate evidence.

### 8.1 Decisions required before implementation selection

- [ ] Resolve field carrier `P2-I3-Q-003`.
- [ ] Resolve native/producer/constructed/missing ownership
  `P2-I3-Q-004`.
- [ ] Resolve the selected non-static dynamic `P2-I3-Q-005`.
- [ ] Resolve exact equation, units, order, and invariants `P2-I3-Q-006`.
- [ ] Resolve local traversal encounter and hidden-router exclusion
  `P2-I3-Q-007`.
- [ ] Resolve current-state versus active-history mode family
  `P2-I3-Q-008`.
- [ ] Assign separate quantity-matched and state-matched identities under
  `P2-I3-Q-013`.
- [ ] Specify restoration and equal-continuation design obligations from
  `P2-I3-Q-015`.
- [ ] Apply the `P2-I3-DEC-012` proportional default: one selected field
  realization plus one complete-state-matched formation-history
  discriminator. A multi-mode program requires demonstrated necessity and a
  separate owner decision.
- [ ] Apply the `P2-I3-DEC-013` repetition floor while deferring exact event
  count, timing, and quantity to I06.
- [ ] Record alternatives, reasoning, gate effect, and reopening condition for
  every accepted choice.

### 8.2 Realization and causal-factorization requirements

- [ ] The realization is structurally capable of exposing two alternative
  route surfaces under the complete baseline-matching contract, without a
  hidden preferred route. Exact numeric and parametric equality belongs to
  I06 registration.
- [ ] Field state is route-local and encountered during traversal.
- [ ] Formation is attributable, repeated, and has a nonzero declared cost.
- [ ] At least one selected non-static dynamic is operationally observable,
  independently intervenable where required, and capable of producing the
  registered measurements later frozen in I04. Scientific measurement belongs
  to I08, not I03 conformance.
- [ ] The selected dynamic either changes traversal directly or changes an
  independently intervenable mediator that changes traversal.
- [ ] Candidate, quantity-matched, state-matched, withdrawal/shuffle,
  false-trace, relocation, and no-field relations are separately addressable.
- [ ] The field-interface family supports a false-trace intervention without
  depositor history and without an outcome-writing path; I06 later freezes the
  exact operation before any execution.
- [ ] Relocation moves registered carrier state while excluding route,
  participant, and preference labels from the payload.
- [ ] Complete continuation-relevant current state is enumerated.
- [ ] Any claimed active history is causal, restorable, and independently
  intervenable rather than audit metadata.
- [ ] Fresh-traverser and direct-address boundaries can be represented.
- [ ] Geometric, functional, causal/proper-time, and experimental causal roles
  cannot be substituted for one another.
- [ ] Native and RCAE-owned paths have explicit ownership boundaries. Only
  declared, receipted state transitions are permitted; undeclared cross-owner
  mutation and producer-authored response or success are forbidden.
- [ ] A future native transition cannot silently replace the registered
  non-native realization.
- [ ] Any constructed mechanism justifies minimality against the added state
  and operations required by the accepted causal chain.

### 8.3 Operational hypotheses

- [ ] Create subordinate operational-hypothesis records only after the
  realization and dynamic decisions are accepted.
- [ ] Preserve `AE01-H-L03` as the frozen parent hypothesis.
- [ ] Map the repeated formation, persistence, selected dynamic, causal
  intervention, later traversal, specificity, variation, and interpretation
  relations to stable machine IDs.
- [ ] State what each relation can support, cannot support, and how it may
  redirect to another lane or a missing substrate surface.
- [ ] Keep direction, magnitude, and terminal outcome open.
- [ ] Bind minimum/strong/highest interpretations without inventing R06.

### 8.4 Bounded runtime conformance

- [ ] Freeze exact public runtime call requirements before conformance.
- [ ] Freeze a scientific-outcome-free, result-neutral conformance matrix. It
  may exercise a synthetic traversal-response interface when needed to prove
  the complete causal architecture, but its fixture values and outcomes are
  ineligible for calibration, registration values, and scientific evidence.
- [ ] Retain exact runtime identity, realization ownership, commands, seeds if
  any, artifacts, and reconstruction instructions.
- [ ] Demonstrate save/load/reset/branch and equal-input continuation where
  required.
- [ ] Demonstrate field update order, route-local access, invariants, and
  operation refusal boundaries.
- [ ] Keep conformance artifacts quarantined from calibration and candidate
  result inputs.
- [ ] Freeze the quarantine mechanism: separate artifact namespace and
  identities plus validator rejection of any downstream calibration,
  registration-value, or candidate-result reference to conformance outputs.
- [ ] Classify any failed binding as implementation or source evidence, never
  a scientific negative.

### 8.5 I03 exit

- [ ] Accepted realization and all load-bearing decisions have stable IDs.
- [ ] Operational hypotheses validate against their schemas/contracts.
- [ ] Runtime conformance reconstructs exactly or is validly classified
  missing/unsuitable.
- [ ] Alternative realization families remain visible with reopening
  conditions.
- [ ] Owner accepts the package and passes
  `P2-I3-DISCRIMINATOR-GATE`.

## 9. `P2-I3-I04` — Calibration preregistration

**Purpose:** freeze candidate-blind measurement semantics before any
calibration output or candidate response exists.

**Entry authority:** passed discriminator gate.

**Evidence effect:** measurement and calibration authority only.

- [ ] Resolve primary traversal response `P2-I3-Q-009`.
- [ ] Resolve all five surface dispositions and policies `P2-I3-Q-010`.
- [ ] Resolve comparator and estimator `P2-I3-Q-011`.
- [ ] Resolve matched-null generator and candidate-blind inputs
  `P2-I3-Q-012`.
- [ ] Resolve common and lane-control applicability `P2-I3-Q-016`.
- [ ] Freeze response units, sign, observation window, aggregation, missing
  values, ties, and normalization.
- [ ] Freeze an observation cadence that can resolve the selected dynamic and
  justify it relative to the declared field timescale.
- [ ] Freeze separate panels for primary response, selected field dynamics,
  distance surfaces, costs, and causal interventions.
- [ ] Freeze quantity-matched and complete-state-matched comparisons as
  distinct relations.
- [ ] Bind measurement semantics to the stable identities assigned in I03;
  I03 owns Q-013 identity and I04 owns its response/comparator binding.
- [ ] Freeze relocation, withdrawal/decay, shuffle/false-trace, hidden-router,
  producer-dependence, fixture-lock, and fresh-traverser controls as
  applicable.
- [ ] Freeze the candidate-blind input provenance and prove the null generator
  accepts no candidate-derived argument.
- [ ] Freeze deterministic calibration seeds disjoint from candidate seeds.
- [ ] Freeze the resolution ladder and interpretation obligations without
  turning a threshold into an automatic terminal gate.
- [ ] Retain exact reconstruction commands and expected artifacts.
- [ ] Owner accepts the package and passes `P2-I3-CAL-PRE-GATE`.

No calibration command runs in I04.

## 10. `P2-I3-I05` — Candidate-blind calibration

**Purpose:** execute only the frozen matched-null procedure and retain the
metric-resolution authority used by later registration.

**Entry authority:** passed CAL-PRE gate plus a separately accepted inactive
calibration invocation freeze.

**Evidence effect:** numeric measurement resolution only.

- [ ] Verify complete `.venv`, interpreter, and pinned packages before claim
  consumption.
- [ ] Verify clean committed calibration sources and exact authority hashes.
- [ ] Verify candidate artifacts, candidate seeds, PyGRC candidate runtime,
  realization responses, and candidate-shaped inputs are mechanically absent.
- [ ] Activate exactly one frozen calibration invocation.
- [ ] Run the complete finite null matrix once, subject only to a frozen
  infrastructure-retry rule.
- [ ] Retain raw null rows, metric calibration, metric sheet, receipts, logs,
  digests, and reconstruction instructions.
- [ ] Derive `delta` using the estimator in the
  [common contract](../contracts/common-contract.md) and
  [L03 metric sheet](../contracts/metric-sheets/AE01-L03.json), without
  candidate tuning.
- [ ] Reconstruct canonical payload and exact artifact bytes independently.
- [ ] Record narrow numeric resolution honestly; do not call it ecological
  support.
- [ ] Owner accepts calibration and passes `P2-I3-CAL-GATE`.

Calibration does not execute or evaluate the P2-I3 candidate.

## 11. `P2-I3-I06` — Exact implementation registration

**Purpose:** bind every scientific and operational choice before candidate
execution.

**Entry authority:** passed CAL-GATE.

**Evidence effect:** exact candidate/control authority only.

- [ ] Resolve exact topology, values, schedules, times, costs, seeds, and
  transfer/variation `P2-I3-Q-014`.
- [ ] Finalize restoration, reset, branch, and continuation identity
  `P2-I3-Q-015`.
- [ ] Preserve the Q-015 handoff: I03 owns the restoration and
  equal-continuation design obligations; I06 binds their exact fields,
  operations, policies, and identities.
- [ ] Finalize control evidence bindings `P2-I3-Q-016`.
- [ ] Resolve resources and artifact envelope `P2-I3-Q-017`.
- [ ] Resolve attempts, retries, failure classes, and one-shot rules
  `P2-I3-Q-018`.
- [ ] Register the exact two-route topology and baseline matching obligations.
- [ ] Register every field parameter, equation input, update order, dynamic,
  formation cost, traversal input, and observation window.
- [ ] Register candidate, reference, no-field, quantity-matched,
  complete-state-matched, withdrawal/decay, shuffle/false-trace, relocation,
  hidden-router, and other applicable control cells.
- [ ] Register distinct current-state and active-history variants only if both
  remain scientifically required.
- [ ] Register primary response, distance panels, field-dynamic panels,
  comparator, delta, relation ladder, rungs, and interpretation tags.
- [ ] Register exact deterministic seeds disjoint from calibration seeds.
- [ ] Register common-control applicability and every L03 control with exact
  evidence bindings.
- [ ] Register finite resources, attempts, infrastructure-only retries,
  expected artifacts, and terminal failure records.
- [ ] Register realization ownership and prevent silent native substitution.
- [ ] Register complete reconstruction instructions for every large or
  omitted artifact.
- [ ] Validate no appendix is present in the core matrix.
- [ ] Independently review the bundle for exact completeness, not for new
  hypothetical exploit resistance.
- [ ] Owner accepts registration and passes `P2-I3-REG-GATE`.

## 12. `P2-I3-I07` — Candidate-cycle execution freeze

**Purpose:** create one inactive, clean-source, exact execution authority and
activate it only through an explicit owner decision.

**Entry authority:** passed REG-GATE.

**Evidence effect:** operational authorization only; inactive freeze creation
runs no scientific response.

- [ ] Resolve clean-source execution authority `P2-I3-Q-019`.
- [ ] Verify the repository-local `.venv`, interpreter, and pinned packages.
- [ ] Require a clean committed RCAE source anchor; dirty previews are
  retention-ineligible and cannot enter activation.
- [ ] Bind exact admitted PyGRC revision and runtime package identity through
  an owner-supplied machine-local mechanism such as ignored local
  configuration or invocation environment. `P2-I3-Q-019` selects the exact
  mechanism; no machine-local path may enter retained artifacts.
- [ ] Validate every execution-specific public call as an explicit superset of
  registration-time conformance where necessary.
- [ ] Bind registration, calibration, policies, source admissions, controls,
  resources, seeds, attempts, restoration rules, and artifact identities.
- [ ] Materialize the complete finite matrix and expected terminal set.
- [ ] Prove no candidate operation occurred during freeze construction.
- [ ] Retain an inactive freeze record and independent validation.
- [ ] Obtain explicit owner acceptance before activation.
- [ ] Activate once and consume `P2-I3-EXEC-FREEZE` at the first governed
  candidate operation.

REG-GATE or an inactive freeze alone never authorizes candidate execution.

## 13. `P2-I3-I08` — Finite matrix execution

**Purpose:** run the exact activated matrix without scientific mutation.

**Entry authority:** activated, unconsumed execution freeze.

**Evidence effect:** mechanical candidate/control observations only; no
terminal classification.

- [ ] Consume the freeze atomically at the first governed operation.
- [ ] Run only exact registered cells, seeds, orders, inputs, and resource
  limits.
- [ ] Keep each arm isolated according to the registered fresh-runtime and
  restoration policy.
- [ ] Retain per-arm input identity, runtime identity, raw outputs, field
  trajectory, traversal response, distance panels, causal receipts, resource
  accounting, and terminal status.
- [ ] Retain formation cost and attribution evidence.
- [ ] Retain selected dynamic-to-traversal causal-chain records.
- [ ] Retain complete-state and history-mode witness records where applicable.
- [ ] Retain every exception, timeout, missing artifact, unsafe flag, and
  infrastructure retry without converting it to a scientific null.
- [ ] Make no threshold, estimator, equation, control, or matrix correction
  inside the active cycle.
- [ ] Close the exact matrix as complete, bounded-incomplete, invalid, or
  failed-closed under its frozen stopping rule.
- [ ] Pass or validly close `P2-I3-EXEC-GATE` without terminal interpretation.

Any scientifically motivated change creates a new registered cycle and keeps
this cycle as permanent history.

## 14. `P2-I3-I09` — Compact control resolution

**Purpose:** resolve all mandatory controls from retained execution evidence
before interpretation.

**Entry authority:** retained I08 terminal records.

**Evidence effect:** causal-control dispositions only.

- [ ] Resolve every applicable common control from explicit retained outcomes.
- [ ] Give each non-applicable common control a reviewed rationale.
- [ ] Resolve all L03 controls, including spatial specificity, selected
  dynamic mediation, withdrawal/shuffle/false-trace specificity,
  complete-state/history separation, hidden-router exclusion, and relevant
  transfer/variation.
- [ ] Resolve producer dependence, fixture lock, runtime substitution,
  restoration, and fresh-traverser identity.
- [ ] Distinguish missing opportunity, not applicable, blocked, invalid,
  passed, and failed statuses.
- [ ] Recompute numeric controls through the registered estimator and metric
  sheet.
- [ ] Derive causal-chain controls from registered masks, public calls,
  carrier and participant identities, event lineage, intervention receipts,
  forbidden-call guards, restoration identities, and runtime bindings.
- [ ] Require both numeric and causal-chain evidence for mixed controls; an
  authored boolean is never authoritative.
- [ ] Generate one compact lane-local control-resolution index as required by
  R3.
- [ ] Preserve failures and ambiguities for developmental interpretation.
- [ ] Independently reconstruct the index.
- [ ] Owner accepts the index and passes `P2-I3-CONTROL-GATE`.

## 15. `P2-I3-I10` — Reconstruction and identity verification

**Purpose:** prove that retained evidence, code, sources, runtime, and reports
support exact independent reconstruction.

**Entry authority:** retained I08 evidence and accepted I09 control package.

**Evidence effect:** evidence-integrity authority only.

- [ ] Reconstruct every retained machine artifact from documented relative
  commands and exact identities.
- [ ] Reconstruct large artifacts omitted from version control using complete
  instructions, expected sizes, and digests.
- [ ] Verify canonical payload and exact file digests where applicable.
- [ ] Verify clean source, environment, PyGRC, policy, registration,
  calibration, seed, and runtime receipt identities.
- [ ] Verify matrix completeness and one terminal per expected arm.
- [ ] Verify save/load/reset/branch and equal-input continuation identities.
- [ ] Verify current-state and active-history identities for every registered
  mode; a mode registered as inapplicable creates no vacuous identity check.
- [ ] Verify report machine facts derive from retained artifacts; authored
  text may interpret but cannot override them.
- [ ] Run reconstruction independently from result construction.
- [ ] Retain discrepancies as blockers or bounded debts rather than silently
  repairing source evidence.
- [ ] Owner accepts reconstruction and passes `P2-I3-RECON-GATE`.

## 16. `P2-I3-I11` — Developmental interpretation and closeout

**Purpose:** interpret what the result actually shows, including narrow,
unexpected, failed, redirective, and missing-surface outcomes, then close at
the strongest warranted boundary.

**Entry authority:** passed control and reconstruction gates.

**Evidence effect:** bounded L03 interpretation and terminal classification.

### 16.1 Result interpretation

- [ ] Interpret the selected field dynamic, not merely persistent trace or
  changed eligibility.
- [ ] Separate geometric, functional, causal/proper-time, and experimental
  causal findings.
- [ ] Classify R01-R05 independently from the minimum/strong/highest dynamic
  reading.
- [ ] Classify primary relations using the frozen metric sheet and preserve
  narrow, resolution-limited, mixed, counter-directional, or unexpected
  outcomes.
- [ ] Explain what every failed or narrowly passed control means structurally
  and behaviorally.
- [ ] Consider whether a local refinement, alternative realization, missing
  substrate surface, or lane redirect is the honest next move.
- [ ] Do not optimize locally merely to reach a desired class; any new probe
  requires a new preregistered cycle.
- [ ] Apply `trail_field_candidate` and, only if independently supported,
  `stigmergic_field_candidate`.
- [ ] Record realization dependence and any native-transition obligation.
- [ ] Record debts, limitations, perturbation/variation strength, and
  reproducibility confidence.

### 16.2 Terminal classification and closeout

- [ ] Produce exactly one valid terminal classification under the Phase 1
  outcome contract.
- [ ] Enforce that infrastructure absence, invalid execution, or failed
  reconstruction cannot become a scientific negative.
- [ ] Preserve valid negative outcomes such as static trace only, no dynamic
  mediation, generic route effect, hidden selection, state-only sufficiency,
  missing history surface, producer dependence, or missing substrate surface.
- [ ] Preserve redirects to other lanes without claiming L03 support.
- [ ] State the exact maximum claim and blocked vocabulary.
- [ ] State implications for the ecology atlas and possible future graph/LGRC
  experiments without changing the graph repository.
- [ ] Resolve whether any appendix has a falsifiable post-core rationale under
  `P2-I3-Q-020`; default remains closed.
- [ ] If an appendix is activated, open a separate `P2-I3-APP-*` work package
  with its own hypotheses or reuse decision, checklist authority, source and
  realization boundary, calibration or justified metric reuse, registration,
  attempt budget, execution freeze, reconstruction, controls, and bounded
  interpretation. This checkbox authorizes only opening that work package.
- [ ] Add an iteration-end interpretation of hypotheses and a concise
  implementation summary to this checklist.
- [ ] Owner accepts interpretation and passes
  `P2-I3-INTERPRET-GATE`.
- [ ] Owner accepts the terminal package and passes
  `P2-I3-CLOSE-GATE`.

## 17. Open-question and decision-timing ledger

The cumulative detail and alternatives live in the
[decision record](P2-I3-decision-record.md). This table prevents an answer
from appearing earlier than its evidence permits.

| Questions | Owning iteration | Current status |
| --- | --- | --- |
| `P2-I3-Q-001` | I01 audit input freeze | Open; blocks audit |
| `P2-I3-Q-002` | I02 source admission | Open; blocks realization |
| `P2-I3-Q-003`–`P2-I3-Q-008` | I03 realization and dynamics | Open; block discriminator gate |
| `P2-I3-Q-009`–`P2-I3-Q-012` | I04 calibration preregistration | Open; block CAL-PRE |
| `P2-I3-Q-013` | I03 assigns separate stable identities; I04 binds their measurement semantics | Open; blocks registration |
| `P2-I3-Q-014` | I06 exact numeric and topology registration | Open; blocks registration |
| `P2-I3-Q-015` | I03 fixes design obligations; I06 finalizes exact restoration and continuation identity | Open; blocks registration |
| `P2-I3-Q-016`–`P2-I3-Q-018` | I04/I06 control design and I06/I07 registration/execution boundaries as declared in the decision record | Open; block registration/execution freeze |
| `P2-I3-Q-019` | I07 execution freeze | Open; blocks candidate execution |
| `P2-I3-Q-020` | Post-core appendix decision | Open; no core blocker |

An open question becomes an accepted implementation boundary only through a
new `P2-I3-DEC-*` entry with alternatives, reasoning, gate effect, and
reopening condition.

## 18. Evidence-triggered checklist change control

The initial checklist is intentionally provisional about future evidence but
not about current authority.

For every expansion:

1. retain the observation or review that motivates it;
2. assign a stable `P2-I3-CHG-*` ID;
3. state whether it is semantic, scientific, implementation, infrastructure,
   reconstruction, or documentation work;
4. identify the affected active or future iteration;
5. state what remains frozen;
6. state rerun or no-rerun scope;
7. obtain owner acceptance when authority, implementation, or scientific
   meaning changes; and
8. append the new work before starting it.

A correction does not automatically require a review of the review. Targeted
revalidation is sufficient when the fix closes a concrete finding without a
new assumption. A broader review is required only when authority, scientific
meaning, or an unknown load-bearing choice changed.

### 18.1 Change ledger

This is a living ledger. Initial entries cover governance construction and are
appended as accepted evidence or review changes accumulate.

| Change ID | Trigger | Change | Status and effect |
| --- | --- | --- | --- |
| `P2-I3-CHG-001` | Owner acceptance of the revised P2-I3 semantic brief | Brief status and atlas navigation record accepted semantic authority | Complete; semantic authority only |
| `P2-I3-CHG-002` | Owner direction to create one cumulative decision record and an evidence-expandable checklist | Construct initial I00 governance package | Complete as construction; no gate or evidence effect |
| `P2-I3-CHG-003` | Initial governance projection | Add I00-I11 boundaries, gate dashboard, environment rule, decision timing, and change/evidence ledgers | Superseded by CHG-004 before brief-gate acceptance |
| `P2-I3-CHG-004` | Two independent governance review sets plus owner authorization | Correct R05 projection, I01 freeze authority, effect ownership, conformance quarantine, typed control evidence, split question handoffs, proportionality, repetition, and bounded review findings | Complete and owner-accepted; no evidence effect |
| `P2-I3-CHG-005` | Owner acceptance disposition after corrected-package review | Record DEC-014, pass BRIEF-GATE, and open only I01 input-freeze construction; clarify I01 evidence classes and I03 operational observability | Complete; no source audit or scientific evidence |

## 19. Evidence ledger

This is a living ledger. Entries are appended only when their named iteration
and evidence effect are retained.

| Evidence ID | Artifact | Iteration | Authority/evidence effect | Status |
| --- | --- | --- | --- | --- |
| `P2-I3-EV-001` | [Accepted semantic brief](P2-I3-trail-or-stigmergic-field-brief.md) | I00 | Lane-local semantic authority only | Accepted by owner 2026-07-16 |
| `P2-I3-EV-002` | [Cumulative decision record](P2-I3-decision-record.md) | I00 | Initial semantic/process decision history only | Accepted by owner 2026-07-16 |
| `P2-I3-EV-003` | This checklist | I00 | Activity/gate/change authority only | Accepted by owner 2026-07-16 |
| `P2-I3-EV-004` | Owner acceptance disposition | I00 | Passes BRIEF-GATE only; opens I01 input-freeze construction | Accepted 2026-07-16; retained as DEC-014/CHG-005 |

No source audit, admission, implementation, calibration, registration,
runtime, control, reconstruction, or scientific evidence exists yet for
P2-I3.

## 20. Current stop and next permitted action

Current stop:

```text
accepted semantic brief
+ accepted cumulative decision record
+ accepted evidence-expandable checklist
= passed P2-I3-BRIEF-GATE
+ I01 input-freeze construction open
!= source audit authorized
```

The next permitted action is construction and project-owner review of the exact
I01 capability-audit input freeze. The source audit itself remains a separate,
explicitly reviewed activity and may not begin until Q-001 and that freeze are
accepted.
