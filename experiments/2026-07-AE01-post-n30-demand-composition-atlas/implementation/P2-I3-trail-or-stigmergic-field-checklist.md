# P2-I3 Trail or Stigmergic Field Checklist

**Status:** I02 exact source admission accepted;
`P2-I3-SOURCE-ADMISSION-GATE` and `P2-I3-N31-RETURN-GATE` passed; bounded
DEC-025 return admission accepted; DEC-026 resolves Q-005 as staged B-R-first
and C.2-second evaluation; DEC-027 resolves B-R Q-008; DEC-028 resolves B-R
Q-006; DEC-029 resolves B-R Q-007; comparison-envelope, Q-013/Q-015 design,
operational-hypothesis, and bounded-conformance work are active

**Iteration:** `P2-I3`

**Lane:** `AE01-L03`

**Current activity iteration:** `P2-I3-I00` complete; `P2-I3-I01` audit
accepted and complete; `P2-I3-I02` exact source admission accepted and
complete; `P2-I3-I03` has reconstructed and admitted the N31 return and now
begins the B-R track's realization and common comparison-envelope work

**Current evidence effect:** source-current capability evidence, exact accepted
source-role authority, the N31 demand/handoff directive, and an accepted exact
N31 return/provider-option transition; no provider selection,
complete realization, calibration, registration, execution, or P2-I3
scientific result

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
- Native coverage has priority only when it preserves the registered causal
  meaning. Missing or inadequate native coverage creates an explicit
  RCAE-owned producer-completion obligation and graph-side naturalization
  debt; it does not authorize weakening or blocking the experiment. Evidence:
  `P2-I3-DEC-017`.
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
| `P2-I3-SOURCE-AUDIT-GATE` | One frozen, source-current, read-only audit answers the accepted capability questions | Passed | Owner-passed grounded artifact review; `P2-I3-DEC-018` |
| `P2-I3-SOURCE-ADMISSION-GATE` | Exact theory and graph revisions, files, callables, roles, and digests are admitted | Passed | Owner-accepted DEC-019, exact manifest, and reconstruction; opens only I03 realization questions |
| `P2-I3-N31-RETURN-GATE` | Exact N31 closeout and provider contracts reconstruct and are admitted without evidence transfer or automatic selection | Passed | Accepted DEC-025; 11 exact retained identities verified, 5 I12 artifacts byte-exact, and the other 3 bounded to an incorrect distribution-metadata value and dependent digests |
| `P2-I3-DISCRIMINATOR-GATE` | Both route-scoped field realizations, dynamics, causal chains, observation boundaries, mode families, and operational hypotheses are frozen or separately dispositioned | Pending staged I03 work | DEC-027/028/029 resolve B-R Q-008 mode, Q-006 law, and Q-007 encounter; common comparison, Q-013, design part of Q-015, operational hypotheses, and bounded conformance remain; C.2 is inactive until B-R closeout |
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
- [x] The core P2-I3 substrate is `LGRC9V3`. Synchronous `GRC9V3` behavior is
  comparative-only and cannot replace, bridge, or satisfy the core
  realization because its step/evolution/relaxation semantics differ.
  Evidence: `P2-I3-DEC-020`.
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
| `P2-I3-I01` | Source-current read-only capability audit | Passed brief gate plus accepted Q-001 freeze | Complete and owner-accepted | `P2-I3-SOURCE-AUDIT-GATE=passed` through DEC-018; no source admission or scientific evidence |
| `P2-I3-I02` | Exact theory and graph source admission | Passed source-audit gate | Complete and owner-accepted | `P2-I3-SOURCE-ADMISSION-GATE=passed` through DEC-019; no realization |
| `P2-I3-I03` | Route-scoped field realization, dynamics, causal factorization, operational hypotheses, bounded runtime conformance, and common comparison envelope | Passed source-admission and N31 return gates | B-R design active under DEC-026; C.2 queued | Each route remains separately gated; no calibration or candidate evidence |
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
  `P2-I3-DEC-001` through `P2-I3-DEC-017`.
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

**Status:** accepted and complete through `P2-I3-DEC-018`;
`P2-I3-SOURCE-AUDIT-GATE` passed.

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

- Accepted frozen artifact:
  [I01 capability-audit input freeze](../contracts/p2-i3/i01-capability-audit-input-freeze.json).
- [x] Resolve `P2-I3-Q-001` through an accepted decision. Evidence:
  `P2-I3-DEC-016`.
- [x] Freeze the exact graph/PyGRC revision candidate and theory revision
  candidate to inspect.
- [x] Freeze every in-scope path and capability question.
- [x] Freeze the rule distinguishing public callable, internal helper,
  pre-existing test evidence, documentation, and inference.
- [x] Freeze allowed static inspection and pre-existing test commands.
- [x] Freeze whether any scientific-outcome-free synthetic conformance probe
  is necessary and quarantine it from candidate and capability claims unless
  separately reviewed. Initial disposition: no synthetic probe is authorized.
- [x] Freeze the exact evidence-class distinction:

  ```text
  public_source_fact:
    source-audit authority

  synthetic_probe:
    interface-conformance evidence only

  candidate_shaped_behavior:
    no capability upgrade and no scientific effect
  ```

- [x] Complete environment preflight. Pytest was initially absent; work
  stopped under DEC-011, the owner authorized installation into `.venv`, and
  preflight then passed with Python 3.12.3 and `pytest==9.1.1` recorded.
- [x] Record the input-freeze review and owner acceptance. Evidence:
  owner direction to continue on 2026-07-16 under `P2-I3-DEC-015`, retained
  as `P2-I3-DEC-016`.

Input-freeze construction record — 2026-07-16:

- [x] Graph target is clean `main` at
  `83e3a300426631ee4df71b661b67d4fcfdfed594`.
- [x] Distance-theory target is clean `main` at
  `e0d25bf69b8bf681eb8d092ba416497030e5d88e`.
- [x] Fifteen capability questions and ten operation-disposition requirements
  are frozen in the candidate.
- [x] Theory-role consistency is separated from runtime-capability authority.
- [x] Public-source fact, synthetic interface conformance, and
  candidate-shaped behavior have distinct evidence effects.
- [x] Checkout-only inspection uses the RCAE `.venv`; global Python and
  ambient-package substitution are forbidden.
- [x] Construction inspected source identities and tracked filenames only; it
  performed no source classification, public API invocation, test,
  conformance probe, or candidate behavior.
- [x] Owner review accepts the freeze as the Q-001 resolution. Under
  `P2-I3-DEC-015`, a direction to continue with no concrete objection is
  sufficient and requires no separate acceptance formula. Evidence:
  `P2-I3-DEC-016`.

### 6.2 Required audit questions

- [x] What registered topology can expose two structurally matchable
  alternative routes?
- [x] Which route-local node, edge, corridor, pulse, feedback, eligibility,
  or state surfaces are publicly observable and alterable through declared
  public operations?
- [x] For each of form, reinforce, withdraw, decay, maintain, saturate,
  relocate, snapshot, restore, and reset, record a separate native,
  producer-assisted, unsuitable, missing, or unknown disposition with exact
  source evidence.
- [x] Which scheduler, packet, producer, feedback, and event-order surfaces
  are public and deterministic?
- [x] Which geometric, functional, and causal/proper-time distances are
  actually exposed, and what runtime roles do they have?
- [x] Which traversal-visible responses can be measured without a hidden
  controller or global route selector?
- [x] Can complete continuation-relevant state be enumerated, saved, restored,
  branched, compared, and relocated?
- [x] Can participant identity, depositor identity, fresh probe identity, and
  direct-address exclusion be represented?
- [x] Which capabilities are native, producer-assisted by established
  extension patterns, unsuitable, missing, or unknown?
- [x] Which claims depend only on static inspection, which on pre-existing
  tests, and which remain inference?
- [x] Which mechanisms N29 indexes from earlier experiments are actually
  load-bearing for P2-I3, and which are runtime, producer, constructed,
  artifact-only, control, accounting, or missing-pattern precedents?
- [x] For every native gap, distinguish absence of native support from
  producer-completion feasibility. Native absence alone is not an execution
  blocker under `P2-I3-DEC-017`.

### 6.3 Audit outputs and exit

- [x] Retain a machine-readable capability inventory with exact citations.
- [x] Retain a human-readable audit report separating facts and inferences.
- [x] Retain exact command, interpreter, package, revision, and digest
  provenance.
- [x] Record every missing or unsuitable surface without treating it as a
  scientific null.
- [x] Retain the N29/N30 mechanism audit and the predecessor-lineage audit as
  separate machine-readable records. N29 is an index into relevant earlier
  experiments, not a substitute for inspecting them.
- [x] Validate the package against its accepted input plus the two exact
  owner-directed scope extensions:
  [N29/N30 scope extension](../contracts/p2-i3/i01-n29-n30-scope-extension.json)
  (`P2-I3-CHG-012`) and
  [predecessor scope extension](../contracts/p2-i3/i01-predecessor-scope-extension.json)
  (`P2-I3-CHG-013`). Machine validation passes all 15
  capability and 10 operation records, 27 public/theory source identities,
  32 N29/N30 and 44 predecessor source identities, output digests, producer-
  feasibility/native-classification separation, quarantine flags, and
  checkout-integrity checks.
- [x] Owner reviews the audit against its accepted input and exact
  owner-directed scope extensions. Evidence: grounded eleven-artifact review
  passed on 2026-07-16.
- [x] Resolve review findings in one bounded pass or record a new iteration;
  do not begin recursive review-of-review cycles absent a concrete new
  assumption. Evidence: `P2-I3-CHG-014`; no classification or authority
  changed.
- [x] Owner accepts the audit and passes `P2-I3-SOURCE-AUDIT-GATE`.
  Evidence: `P2-I3-DEC-018`.

### 6.4 I01 implementation details and interpretation

Retained implementation:

- [x] Accepted one machine input freeze before classification.
- [x] Bound clean graph revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594` and clean distance-theory
  revision `e0d25bf69b8bf681eb8d092ba416497030e5d88e`.
- [x] Retained a 15-record
  [capability matrix](../contracts/p2-i3/i01-capability-matrix.json), a
  10-record
  [operation matrix](../contracts/p2-i3/i01-operation-dispositions.json),
  27 exact [source digests](../contracts/p2-i3/i01-source-digests.json),
  [command provenance](../reports/P2-I3-I01-command-provenance.md), and
  [machine validation](../contracts/p2-i3/i01-audit-validation.json).
- [x] Ran six targeted pre-existing-test invocations: 24 passed, 333
  deselected, zero failed/errors. The exact six `-k` filters and per-command
  deselection counts are retained in
  [command provenance §5](../reports/P2-I3-I01-command-provenance.md#5-pre-existing-generic-tests).
  No synthetic probe or candidate behavior ran.
- [x] Rechecked both external revisions and clean worktrees after the audit.
- [x] Expanded the read-only experiment audit from N29/N30 into the relevant
  predecessor lineage: N05 producer scheduling, N06 route-arbitration limits,
  N07 reservoir accounting, N08 serialized/dynamic trail-memory work, N09
  producer request/native transition, N10/N11 missing-pattern demand, N22
  producer-owned durable carrier, N25.2 native multi-basin context, and N28
  artifact-level metric projection.

Geometric and runtime interpretation:

```text
native registered topology
+ route-exclusive node coherence candidate
+ deterministic packet formation/reinforcement/withdrawal
+ separate synchronous GRC coherence continuity, comparative-only
+ distinct geometric/functional/causal timing surfaces
+ complete native restoration

does not yet provide

LGRC-integrated route-local field lifecycle
+ local field-to-traversal encounter
+ field-specific state/history controls
+ participant-role/direct-address exclusion
```

The strongest native carrier candidate is route-exclusive intermediate-node
coherence, updated by budget-conserving packet arrivals. Public synchronous
GRC continuity is a real native dynamic, but LGRC's queue-event step
explicitly does not invoke it; using it would require a later explicit
composition, ordering, state-effect, and restoration decision. These remain
shortlist results, not source admission or realization selection. The native
causal-pulse substrate is passive evidence and scheduling infrastructure, not
the field itself. The landscape pheromone classifier is post-hoc inference,
not live dynamics.

From the agentic-ecology side, I01 identifies where a graph relation stops and
the ecological discriminator begins. PyGRC can carry attributable route-local
history and can separately evolve coherence synchronously. I03 must decide
whether that dynamic can be integrated honestly or whether a bounded RCAE
dynamic is required. L03 still needs a later local encounter that changes
possibility without route labels, direct outcome addressing, or a global
selector.

That unresolved relation is a constructive demand for I03, not a negative
result or a reason to truncate the experiment. N08 states the missing native
route-memory pattern; N22 demonstrates that an explicitly producer-owned
carrier can be mutated, snapshotted, replayed, controlled, and read through
native runtime without being mislabeled native; N05/N09 demonstrate the
narrower request-producer pattern in which PyGRC owns the transition. Under
`P2-I3-DEC-017`, I03 must prefer semantically adequate native capability and
fill any remaining load-bearing gap with the smallest explicit producer path.
The unfilled native pattern remains a proposed LGRC expansion target.

The source-audit gate is passed. The proportional next move is I02 exact
source admission and Q-002. Only after its separate gate may I03 compare
carrier and dynamic options; it must not infer the first working source
surface as accepted.

## 7. `P2-I3-I02` — Exact source admission

**Purpose:** admit only the exact source surfaces that may constrain or
support P2-I3 realization work.

**Entry authority:** passed source-audit gate.

**Frozen inputs:** accepted I01 inventory and report.

**Environment prerequisites:** complete audit/admission validation environment.

**Mutation boundary:** admission records and validators in this repository;
source repositories remain read-only.

**Evidence effect:** source identity and role authority only.

- [x] Resolve `P2-I3-Q-002` through accepted `P2-I3-DEC-019`.
- [x] Admit the exact graph/PyGRC revision, files, public callables, and
  pre-existing tests by digest and evidence role.
- [x] Admit the exact RC-Distance source revision and file, with its role
  bounded to theory/interpretation unless an operational source is separately
  demonstrated.
- [x] Admit every other theory source by exact revision, path, digest, and
  role; reject vague directory-level authority.
- [x] Distinguish inherited evidence, ecology interpretation, constructed
  mechanism, missing surface, and proposed discriminator.
- [x] Record whether existing extension patterns permit RCAE-owned producers
  without changing PyGRC.
- [x] Record any source transition from historical audit identity to current
  admitted identity.
- [x] Validate source digests and public callable identities.
- [x] Independently reconstruct the admission record.
- [x] Owner accepts the source bundle and passes
  `P2-I3-SOURCE-ADMISSION-GATE`.

The admission bundle selects no field carrier, equation, realization, metric,
or candidate outcome.

### 7.1 I02 construction and review evidence

- [x] Construct one exact
  [source-admission manifest](../contracts/p2-i3/i02-source-admission-manifest.json)
  from the accepted I01 bundle without widening the graph audit scope.
- [x] Assign all 26 audited graph files exactly one bounded admission role.
- [x] Bind 40 public callable identities to their exact implementation source
  and classify them as later options, supporting implementation, or
  explicitly nonqualifying boundary references.
- [x] Bind all 24 accepted I01 generic-test definitions by exact file and
  name without rerunning them or consuming their fixture values.
- [x] Bind eight exact theory/method files: RC-Distance, four current RCAE
  conceptual sources, and three becoming/development sources.
- [x] Record four prospective RCAE-paper digest transitions from historical
  P1 admission to the current I02 entry revision without rewriting P1.
- [x] Admit the 32-source N29/N30 and 44-source predecessor inventories as
  exact grouped projections with inherited-evidence and constructed-
  precedent roles respectively.
- [x] Expose the predecessor experiment names and compact primary/supporting/
  projection-only roles in the manifest without copying source records or
  creating a second authority; validate both projections against the exact
  predecessor inventory.
- [x] Record the source-backed RCAE request/declared-state producer option,
  graph-repository non-mutation boundary, explicit native-transition rule,
  and graph-side naturalization debt.
- [x] Record `P2-I3-DEC-020` and reclassify synchronous `GRC9V3`,
  `apply_continuity()`, and `step()` as comparative-only. Preserve
  `GRC9V3State` solely as the public base-state type used by LGRC9V3.
- [x] Reconstruct source hashes, group inventories, callable identities, test
  definitions, role completeness, evidence classes, and external-checkout
  cleanliness with the retained
  [validator](../scripts/p2_i3_i02_validate.py).
- [x] Retain the [validation result](../contracts/p2-i3/i02-admission-validation.json)
  and [I02 report](../reports/P2-I3-I02-exact-source-admission.md).
- [x] Apply concrete owner-review corrections and accept DEC-019 under the
  correction-driven review convention.

Implementation interpretation:

```text
26 exact graph files
+ 40 public callable identities
+ 24 exact pre-existing tests
+ 8 exact theory/method files
+ 76 exact N29/N30 and predecessor sources through two digest-bound groups
= one accepted reconstructible later-use authority
!= one selected realization
```

The grouped projections avoid copying 76 path/digest records while remaining
fully dereferenceable: the validator verifies both inventory digests and every
underlying graph source at the admitted revision. Public imports are resolved
from the sibling graph checkout using the existing repository `.venv`; no
callable is invoked.

The eligible core substrate is narrower than the admitted PyGRC source set.
Only LGRC9V3 may carry the core realization. GRC9V3 source remains admitted so
its distinct dynamics can be understood and, if separately governed, compared;
it cannot rescue a missing LGRC9V3 lifecycle or produce a positive L03 core
classification.

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

- [x] Resolve field carrier `P2-I3-Q-003`: route-exclusive intermediate-node
  coherence under `P2-I3-DEC-021`, with edge and explicit-corridor alternatives
  retained for traceable future campaigns.
- [x] Resolve native/producer/constructed/unsuitable/missing ownership
  `P2-I3-Q-004` through the mixed native-LGRC/RCAE map in
  `P2-I3-DEC-022`.
- [x] Retain the originally three-way, now D0-first
  [Q-005 decay interpretation study](../reports/P2-I3-Q005-decay-interpretation-study.md)
  as pre-decision evidence. DEC-024 adds coherence-only derived decay as the
  first hypothesis, separates causal slow organization from a fading graph
  observable, and retains release attenuation, conserved leakage, and
  constructed susceptibility as later paths; it grants no implementation
  authority.
- [x] Resolve `P2-I3-Q-005` through DEC-026 as separate B-R-first and
  C.2-second candidate tracks followed by comparison; select no lane winner
  before branch evidence.
- [x] Replace the provisional two-RCAE-realization direction with the accepted
  DEC-023 cross-project spiral. Retain the
  [N31 handoff and return contract](P2-I3-N31-decay-primitive-handoff.md),
  defer Q-005 without answering it, and prohibit I03 implementation until the
  exact N31 result is reconstructed and admitted.
- [x] Record DEC-024: N31 tests D0 first; exact cache/recomputation and
  complete-field boundaries distinguish derived state from an effective
  closure or theory extension. Passed gates and the P2-I3 pause remain
  unchanged.
- [x] Freeze DEC-024's D0-versus-B classifier: ordinary native `C/J_C`
  redistribution remains D0; Candidate B requires a new field-specific
  emission eligibility, amount, timing, destination, or lifecycle policy.
- [x] Freeze the D0 producer guard: fixture, observation, admitted-native
  request, and receipt roles are permitted; no producer may author the
  load-bearing post-formation state or weakening transition.
- [x] Require N31 to classify D0a representation as native, exact projection,
  lossy, or missing before execution. Lossy/missing state closes D0a at the
  representation boundary and makes affected controls
  `unavailable_missing_representation`.
- [x] Separate cache recomputation from complete execution reconstruction and
  correct theory/substrate-source identity versus the future committed RCAE
  demand-source identity.
- [x] On return, admit the exact N31 revision through a bounded source
  transition, then explicitly retain or reopen DEC-021/022 before resolving
  Q-005. Follow the handoff's outcome-specific branch and return checklist.
- [x] Resolve the B-R exact equation, coherence units, serialized lifecycle,
  update order, receipt semantics, and invariants under DEC-028. Keep the C.2
  instance inactive and independent until the B-R branch closeout.
- [x] Resolve the B-R local traversal encounter and hidden-router exclusion
  through DEC-029 as paired independent fixed native departure requests whose
  adapter cannot read field state or compare routes. Keep C.2 independent.
- [x] Resolve the B-R current-state versus active-history mode family through
  DEC-027. Keep the C.2 instance inactive and independent.
- [ ] Assign separate quantity-matched and state-matched identities under
  `P2-I3-Q-013`.
- [ ] Specify restoration and equal-continuation design obligations from
  `P2-I3-Q-015`.
- [x] Apply and explicitly widen the `P2-I3-DEC-012` proportional default
  through DEC-026: N31's two distinct provider ontologies and the owner's
  request for evidence about both justify separate B-R and C.2 tracks. This
  does not authorize either track's later gates.
- [x] Apply the `P2-I3-DEC-013` repetition floor through DEC-028: require at
  least two attributable formation events and two serialized lifecycle
  opportunities while deferring counts beyond those minima, timing, and
  quantity to candidate-blind calibration and I06.
- [x] Record alternatives, reasoning, gate effect, and reopening condition for
  every accepted B-R Q-006/Q-008 choice; repeat this obligation for Q-007 and
  the later C.2 decisions.

### 8.1.1 N31 return transition

- [x] Verify N31 terminal closeout, clean merged graph checkout, closeout
  commit, source anchor, and committed RCAE demand source as distinct
  identities.
- [x] Verify the merged graph tree is identical to the N31 closeout tree and
  preserve the graph checkout as read-only during RCAE work.
- [x] Dereference all eleven N31 return-manifest roles from the exact closeout
  commit and verify exact-file plus internal output digests.
- [x] Install the source-declared graph package, build prerequisites, and
  declared runtime dependencies into the ignored graph `.venv` after owner
  authorization; verify
  `pygrc==0.1` and keep the tracked graph worktree clean.
- [x] Reconstruct I12 in a temporary local clone at the exact source anchor,
  using the exact closeout builder without modifying the graph checkout.
- [x] Retain the incorrect `0.0.0` closeout distribution metadata versus
  source-declared/reconstructed `0.1` instead of rewriting N31.
- [x] Prove both provider contracts, the candidate matrix, the claim/debt
  register, and the RCAE recommendation reconstruct byte-exactly.
- [x] Freeze the only three bounded non-exact artifacts and every permitted
  differing JSON pointer; classify them as distribution metadata and
  dependent digest differences only.
- [x] Admit B-R and C.2 as producer-mediated provider-contract options without
  selecting either; preserve B-R+C.2 only as a new composition requiring
  fresh attribution and interference controls.
- [x] Record that producer-mediated status is valid N-series evidence and
  nativity is an ownership/claim boundary, not an admission preference.
- [x] Record exact effects on DEC-020/023/024 and defer affected DEC-021/022
  changes until Q-005 selection.
- [x] Retain the
  [machine admission](../contracts/p2-i3/i03-n31-return-admission.json),
  [validation/reconstruction](../contracts/p2-i3/i03-n31-return-validation.json),
  [validator](../scripts/p2_i3_n31_return_validate.py), and
  [interpretive report](../reports/P2-I3-N31-return-admission.md).
- [x] Complete bounded correction-driven review and pass
  `P2-I3-N31-RETURN-GATE` under DEC-015.
- [x] Resolve Q-005 through DEC-026 and require each route to retain or reopen
  affected DEC-021/022 boundaries under separate identities before its Q-006
  work begins.

### 8.1.2 Staged B-R and C.2 comparison program

- [x] Record explicit owner authority to widen DEC-012's one-realization
  default because N31 returned two distinct causal ontologies and both are to
  receive fresh ecology evaluation.
- [x] Freeze the order as B-R first, C.2 second, comparison last; record that
  order is developmental and not a ranking.
- [x] Prohibit shared topology, carrier, equation, dynamic state, calibration,
  registration, or result identity unless equivalence is later demonstrated.
- [x] Permit reuse only of evidence-neutral schemas, validators, runner
  interfaces, telemetry shapes, reconstruction utilities, and report forms.
- [ ] Freeze the common ecology-result and producer-cost comparison envelope
  before B-R candidate work. Cost remains a vector, not a scalar gate, and
  separates contract-required, RCAE-ecology-required, and evidence-only work.
- [x] Bind the exact B-R provider contract and branch-specific DEC-021/022
  projection through DEC-028; resolve the B-R instance of Q-006 without
  transferring N31 evidence.
- [x] Resolve the B-R instance of Q-007 through DEC-029; carry its local-
  encounter, hidden-router, matched-mass readout, clamp, relocation,
  permutation, and atomic-refusal obligations into later gates without
  assigning outcomes.
- [x] Resolve the B-R instance of Q-008 through DEC-027 as current-composite-
  state carried with one mandatory complete-state-matched formation-history
  discriminator. Do not assign the discriminator outcome before execution.
- [ ] Complete separately gated B-R conformance, calibration, registration,
  execution, controls, reconstruction, and branch interpretation.
- [ ] Retain a B-R producer-cost record covering owned operations/state,
  invocation counts, producer-specific controls, restoration/replay burden,
  artifact/state footprint, omission dependence, and naturalization debt.
- [ ] Review the B-R branch closeout before opening C.2 design. Record every
  B-R-derived input used prospectively by C.2.
- [ ] Bind the exact C.2 provider contract under a separate carrier/topology
  identity; resolve C.2 instances of Q-006 through Q-008.
- [ ] Complete separately gated C.2 conformance, calibration, registration,
  execution, controls, reconstruction, and branch interpretation.
- [ ] Retain the corresponding C.2 producer-cost record under the same common
  ledger fields.
- [ ] Compare both branch results without scalar cost collapse or automatic
  winner selection; resolve Q-021 as B-R, C.2, both alternatives, a separately
  governed composition proposal, another justified route, or non-selection.
- [ ] Author one lane terminal record only after both branch closeouts and the
  comparison record exist, unless a later accepted decision stops the program
  with a classified bounded result.

### 8.1.3 Accepted B-R Q-006 law

- [x] Consume the exact B-R contract through DEC-025 admission rather than
  copying or reopening the complete N31 return identity.
- [x] Register `s_e` as route-support formation source/debit account, `m_e` as
  the sole native coherence carrier/export source, and `d_e` as an isolated
  explicit reservoir. Do not equate `s_e` with complete participant support or
  ecological budget.
- [x] Freeze settled carrier, mass, and contrast projections as
  `F=C(m)`, `M=C(s)+C(m)`, and `O=C(m)-C(s)`; keep `M` and `O` analysis-only.
- [x] Freeze conservative formation `s --p--> m`, with `Delta M=0` and
  `Delta O=2p`, through at least two attributable settled events.
- [x] Freeze eligible export as
  `q=min(q_cap,max(0,C(m)-C_floor))`, followed by native `m --q--> d`,
  `Delta M=-q`, and `Delta O=-q`; retain exact global conservation.
- [x] Separate eligible-positive, eligible-zero, invalid/ineligible, and
  duplicate-consumed receipt transitions. Eligible zero consumes and advances
  policy state without native mutation; invalid and duplicate operations are
  atomic no-ops.
- [x] Serialize receipts by route, sequence, native-event, predecessor-
  composite, policy, endpoint, and prior-settlement identities; permit at most
  one accepted-but-unsettled export per route.
- [x] Include lifecycle cursor, consumed/eligible receipts, pending
  reservation/export, policy, and endpoint bindings in complete composite
  restoration under DEC-027; prohibit raw-history producer reads.
- [x] Require producer omission to yield zero export and isolate the reservoir
  from return paths, route selection, producer inputs, and feedback into the
  candidate lifecycle or later traversal.
- [x] Freeze the quantity-matched control semantics as equal source/carrier
  removal with `Delta M=-q`, `Delta O=0`, and explicit conservation accounting;
  defer its exact intervention operation and numeric value.
- [x] Distinguish `single_positive_withdrawal_plus_floor`,
  `repeated_event_indexed_weakening`, and `terminal_floor_stability`; do not
  relabel two opportunities as two positive exports.
- [x] Classify DEC-028 as a repeated-lifecycle B-R realization and only the
  dynamic segment of a candidate ecology composition. Q-007 plus fresh RCAE
  execution are required to close the full formation-field-traversal chain.
- [x] Carry export-source `C(m)`, destination `C(d)`, matched-mass readout,
  and atomic rejected-readout obligations into Q-007 without assigning their
  outcome.

### 8.1.4 Accepted B-R Q-007 encounter

- [x] Add one matched continuation node `x_e` and edge `h_e=(m_e,x_e)` per
  route. Keep `m_e` as the field carrier/export source, `d_e` as an isolated
  reservoir, and `x_e` as a continuation target rather than a field,
  participant, or result carrier.
- [x] Compare fixed `m_e --q_probe--> x_e` requests in independent,
  complete-checkpoint-matched counterfactual branches. Do not implement a
  simultaneous runtime route selector or shared departure queue.
- [x] Restrict the RCAE encounter adapter to prospectively frozen local
  structural opportunity bindings. It may not read coherence, field/policy
  state, the other route, formation history, participant or route labels,
  outcome, rank, or result; numeric endpoint IDs are permitted only as frozen
  PyGRC structural bindings.
- [x] Leave admission and debit to the native LGRC9V3 step. Retain
  `mu=C(m_e)-q_probe` as analysis-only: `mu>=0` admits the fixed request and
  `mu<0` produces the exact insufficient-source-coherence refusal.
- [x] Type `admitted`, exact `field_limited_refusal`, and invalid or
  infrastructure failure separately. Verify atomic refusal against the
  pre-step native identity that already contains the scheduled request.
- [x] Treat an admitted probe as an invasive terminal branch. Delayed or
  repeated encounters must fork from clean unprobed checkpoints rather than
  continue from a debited branch.
- [x] Carry lifecycle intervention, source-`C(m)` clamp, reservoir-`C(d)`
  clamp, matched mass, DEC-027 state/history, current-state relocation,
  role/raw-ID permutation, fixed-route exclusion, atomic refusal/replay,
  no-export, and producer-omission controls into later design gates.
- [x] Keep the scientific interpretation graded. A native binary admission is
  not a binary lane gate: retain robust split, same-side margin, narrow split,
  no movement, matched-mass reproduction, state/history divergence, and
  invalid/resolution outcomes.
- [x] Bound the maximum encounter meaning to route-local continuation
  admissibility. It does not establish embodied movement, route choice,
  preference, planning, or a complete trail/stigmergic result.
- [x] Record opportunity manifest, structural guard, and blind adapter as
  `rcae_ecology_required`; native admission/debit/transport/refusal as native;
  and branching, margin derivation, and telemetry as `evidence_only`. Do not
  add this encounter adapter to N31's contract-required export residue.

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
| `P2-I3-Q-001` | I01 audit input freeze | Resolved by `P2-I3-DEC-016`; audit active |
| `P2-I3-Q-002` | I02 source admission | Resolved by `P2-I3-DEC-019`; no longer blocks I03 |
| `P2-I3-Q-003` | I03 carrier selection | Resolved by `P2-I3-DEC-021`; alternative carriers retained with rerun rules |
| `P2-I3-Q-004` | I03 operation ownership | Resolved by `P2-I3-DEC-022`; conformance may reopen affected rows |
| `P2-I3-Q-005` | I03 dynamic selection after graph return | Resolved by DEC-026 as separate B-R-first and C.2-second candidate tracks; no final provider selected |
| `P2-I3-Q-006` | Route-scoped I03 equation | B-R resolved by DEC-028 as serialized conservative redistribution; C.2 remains inactive and independent |
| `P2-I3-Q-007` | Route-scoped I03 encounter | B-R resolved by DEC-029 as paired branch-local fixed native departure admission; C.2 remains inactive and independent |
| `P2-I3-Q-008` | Route-scoped I03 current-state/history mode | B-R resolved by DEC-027 as current-composite-state primary plus mandatory history discriminator; C.2 remains open and inactive |
| `P2-I3-Q-009`–`P2-I3-Q-012` | I04 calibration preregistration | Open; block CAL-PRE |
| `P2-I3-Q-013` | I03 assigns separate stable identities; I04 binds their measurement semantics | Open; blocks registration |
| `P2-I3-Q-014` | I06 exact numeric and topology registration | Open; blocks registration |
| `P2-I3-Q-015` | I03 fixes design obligations; I06 finalizes exact restoration and continuation identity | Open; blocks registration |
| `P2-I3-Q-016`–`P2-I3-Q-018` | I04/I06 control design and I06/I07 registration/execution boundaries as declared in the decision record | Open; block registration/execution freeze |
| `P2-I3-Q-019` | I07 execution freeze | Open; blocks candidate execution |
| `P2-I3-Q-020` | Post-core appendix decision | Open; no core blocker |
| `P2-I3-Q-021` | Post-branch comparison and lane retention decision | Inactive until B-R and C.2 branch closeouts; blocks lane terminal and promotion |

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
| `P2-I3-CHG-006` | Owner direction on iteration review | Add DEC-015 correction-driven review: present every iteration, correct concrete comments, and treat unopposed reviewed progression as acceptance without a separate formula | Complete; review remains mandatory and gate status remains explicit |
| `P2-I3-CHG-007` | Passed brief gate and I01 entry | Construct the exact Q-001 input-freeze candidate with fifteen capability questions, ten operation dispositions, synthetic probes disabled, and source/audit evidence separated | Review-ready; no audit or capability evidence |
| `P2-I3-CHG-008` | Owner direction to continue after input-freeze review | Record DEC-016, resolve Q-001, accept the exact freeze, and open only its environment preflight and read-only audit | Complete; audit active with no output or capability classification yet |
| `P2-I3-CHG-009` | I01 preflight found pytest absent | Stop before tests under DEC-011; after owner authorization install pytest only into RCAE `.venv`, record exact resolved identities, and rerun preflight | Complete; `pytest==9.1.1`, `iniconfig==2.3.0`, and `pluggy==1.6.0`; no external checkout mutation |
| `P2-I3-CHG-010` | Accepted Q-001 audit scope and passed preflight | Execute the frozen source/public-interface audit, retain 15 capability and 10 operation dispositions, 27 source digests, six test invocations, narrative interpretation, and machine validation | Complete and review-ready; source-current capability effect only |
| `P2-I3-CHG-011` | Final I01 boundary check found the public synchronous GRC continuity operator inside the already frozen source scope | Clarify CAP-06 and the narrative: `GRC9V3.apply_continuity`/`step` are relevant native dynamics, while `LGRC9V3.step` deliberately remains a separate event runtime; retain existing classifications and expose the composition choice to I02/I03 | Complete after targeted source/callable revalidation; no test rerun, scope widening, source admission, realization choice, or scientific effect |
| `P2-I3-CHG-012` | Owner direction to examine the graph repository N29/N30 experiments thoroughly before I01 closure | Activate the exact [N29/N30 scope extension](../contracts/p2-i3/i01-n29-n30-scope-extension.json); inspect the roadmap and complete N29/N30 experiment trees for relevant native, producer-assisted, constructed, evidence-only, and debt mechanisms | Complete; no experiment rerun, source admission, realization choice, or P2-I3 scientific effect |
| `P2-I3-CHG-013` | Owner correction that N29 indexes earlier work, plus direction that missing native PyGRC support must not weaken or block correct execution | Record DEC-017; activate the exact [predecessor-lineage scope extension](../contracts/p2-i3/i01-predecessor-scope-extension.json); inspect relevant N05/N06/N07/N08/N09/N10/N11/N22/N25.2/N28 mechanisms; preserve native classifications while adding producer-completion feasibility and graph-side naturalization debt | Complete and validated; read-only source evidence only, no source admission, realization selection, experiment execution, or L03 result |
| `P2-I3-CHG-014` | Grounded artifact review identified low-risk machine-role and citation ambiguities | Clarify that candidate-surface IDs name audit targets rather than asserting existence; mark CAP-14/15 as meta roles; mark OP-07 callables as nonqualifying topology-lineage comparisons; add precedent legend and exact scope/filter citations | Complete after targeted structural/digest validation; no classification, authority, source scope, test, execution, or scientific-effect change |
| `P2-I3-CHG-015` | Project owner explicitly passed the grounded I01 review | Record DEC-018, accept the retained I01 package, pass SOURCE-AUDIT-GATE, and open only I02 exact source admission and Q-002 | Complete; governance status only, with no source admission, realization, execution, or scientific effect |
| `P2-I3-CHG-016` | Passed source-audit gate and owner direction to perform I02 | Construct DEC-019 proposal, exact source/callable/test/theory manifest, static reconstruction validator, validation result, and narrative report without widening I01 or selecting a realization | Review-ready; Q-002 and SOURCE-ADMISSION-GATE remain open pending correction-driven owner review |
| `P2-I3-CHG-017` | Owner clarified during I02 review that only LGRC9V3 is the target substrate and synchronous GRC9V3 has materially different per-step relaxation/evolution | Record DEC-020; reclassify GRC9V3 class/continuity/step identities as comparative-only; forbid substitution or bridge relabeling; rerun exact manifest reconstruction | Complete as bounded I02 correction; no source scope, realization, runtime, or scientific-effect change |
| `P2-I3-CHG-018` | Owner found that the compact manifest exposed N29/N30 but hid the exact earlier experiment lineage behind a generic predecessor group | Add a validator-bound `included_experiments` projection and compact role summary while retaining the digest-bound inventory as sole source-level authority | Complete as discoverability correction; no duplicated source records, admission widening, role change, realization, runtime, or scientific effect |
| `P2-I3-CHG-019` | Project owner accepts the corrected I02 manifest | Accept DEC-019, resolve Q-002, pass SOURCE-ADMISSION-GATE, and open only I03 realization questions | Complete; exact source-role authority only, with no realization, runtime conformance, calibration, execution, or scientific effect |
| `P2-I3-CHG-020` | Project owner accepts the recommended Q-003 carrier and requires alternatives to remain reusable | Record DEC-021 with route-exclusive intermediate-node coherence as the minimum core carrier; retain edge conductance and explicit corridor field as separately rerunnable alternatives | Complete as carrier choice only; Q-004 through Q-008 remain open and no equation, encounter, conformance, calibration, or scientific effect follows |
| `P2-I3-CHG-021` | Project owner accepts the Q-004 ownership classification | Record DEC-022 mixed ownership: retain native LGRC9V3 carrier/packet/time/restoration transitions, require explicit RCAE completion for missing lifecycle/encounter/control functions, reject nearby causal substitutions, and preserve naturalization debt | Complete as ownership authority only; Q-005 through Q-008 remain open and no implementation, conformance, calibration, or scientific effect follows |
| `P2-I3-CHG-022` | Owner requires a thorough record of all three decay interpretations and initially considers leakage plus constructed-susceptibility implementations; owner rejects assumed topology reuse | Retain the Q-005 interpretation study; separate attenuation, conserved leakage, and susceptibility relaxation; permit reuse only above demonstrated topology/carrier equivalence | Superseded prospectively by CHG-023 before implementation selection; report remains active evidence and no implementation occurred |
| `P2-I3-CHG-023` | Owner recognizes that the unresolved meaning of decay belongs first in graph/LGRC and accepts the N31 cross-project spiral | Record DEC-023; replace the local two-implementation plan with a detailed N31 demand/handoff/return contract; pause I03 at Q-005 | Complete as cross-project continuation authority; Q-005 remains unresolved and all P2-I3 implementation/scientific work stays closed pending N31 return |
| `P2-I3-CHG-024` | Owner accepts the core-theory evaluation, points to the LGRC substrate papers as the specification layer below core theory and above code, and supplies a grounded pre-freeze review of the amended package | Record DEC-024; add D0a slow causal coherence organization, D0b fading derived graph observable, D0c instantaneous comparator, seven theory/substrate authorities, explicit paper-to-code capability dispositions, ordinary-redistribution-versus-added-leakage classification, strict D0 producer limits, a pre-execution D0a representation gate, distinct cache-recomputation/execution-reconstruction statuses, corrected source identities, D0-first N31 outcomes, and return branches | Complete as bounded prospective theory/substrate correction; no passed gate, admitted I01/I02 artifact, implementation, or scientific state changes |
| `P2-I3-CHG-025` | N31 closes and merges with two exact provider contracts; RCAE reconstruction exposes incorrect retained `pygrc==0.0.0` distribution metadata against source-declared `0.1` | Construct and accept DEC-025, exact return admission, temporary-clone validator, bounded difference contract, reconstruction result, report, and checklist projection without selecting a provider | Complete; return gate passed with N31 graph/provider-option authority only and no P2-I3 evidence, realization, conformance, calibration, or execution effect |
| `P2-I3-CHG-026` | Owner requests empirical exploration of B-R first and C.2 second, including scientific results and producer cost, rather than pre-evidence provider selection | Record DEC-026; widen DEC-012 explicitly; create isolated route tracks plus a common comparison and producer-cost envelope; defer final provider retention to Q-021 | Accepted planning authority; opens B-R design only, with no conformance, calibration, execution, branch result, or lane result |
| `P2-I3-CHG-027` | Owner accepts the proposed B-R Q-008 current-state/history boundary | Record DEC-027; make complete native-plus-policy current state primary, require one matched-history discriminator, prohibit raw-history producer reads, and leave C.2 Q-008 independent | Accepted B-R mode authority only; Q-006/Q-007 and every conformance, calibration, execution, and result gate remain open |
| `P2-I3-CHG-028` | Owner accepts the proposed B-R Q-006 law plus bounded mechanical corrections from review | Record DEC-028; consume DEC-025 rather than re-admit N31; freeze route roles, coherence equations, floor/cap bound, four receipt outcomes, serialized lifecycle, native/producer ownership, matched-mass construction, reservoir isolation, and repetition classifications | Accepted B-R equation authority only; Q-007 and every conformance, calibration, registration, execution, and result gate remain open |
| `P2-I3-CHG-029` | Owner accepts the proposed B-R Q-007 local encounter | Record DEC-029; add matched continuation roles, freeze independent branch-local fixed requests, make native source-coherence admission load-bearing, prohibit adapter field reads and runtime route comparison, type refusal states, and carry clamp/mass/history/relocation/permutation controls forward | Accepted B-R encounter authority only; common comparison, Q-013/Q-015, operational hypotheses, conformance, calibration, registration, execution, and all results remain open |

## 19. Evidence ledger

This is a living ledger. Entries are appended only when their named iteration
and evidence effect are retained.

| Evidence ID | Artifact | Iteration | Authority/evidence effect | Status |
| --- | --- | --- | --- | --- |
| `P2-I3-EV-001` | [Accepted semantic brief](P2-I3-trail-or-stigmergic-field-brief.md) | I00 | Lane-local semantic authority only | Accepted by owner 2026-07-16 |
| `P2-I3-EV-002` | [Cumulative decision record](P2-I3-decision-record.md) | I00 | Initial semantic/process decision history only | Accepted by owner 2026-07-16 |
| `P2-I3-EV-003` | This checklist | I00 | Activity/gate/change authority only | Accepted by owner 2026-07-16 |
| `P2-I3-EV-004` | Owner acceptance disposition | I00 | Passes BRIEF-GATE only; opens I01 input-freeze construction | Accepted 2026-07-16; retained as DEC-014/CHG-005 |
| `P2-I3-EV-005` | [I01 capability-audit input freeze](../contracts/p2-i3/i01-capability-audit-input-freeze.json) | I01 | Frozen audit-input authority only | Accepted through DEC-016 before audit activity; supplies no capability evidence itself |
| `P2-I3-EV-006` | [I01 capability matrix](../contracts/p2-i3/i01-capability-matrix.json) | I01 | Source-current capability classifications only | Accepted; 15/15 questions resolved |
| `P2-I3-EV-007` | [I01 operation dispositions](../contracts/p2-i3/i01-operation-dispositions.json) | I01 | Source-current operation classifications only | Accepted; 10/10 operations resolved |
| `P2-I3-EV-008` | [I01 source digests](../contracts/p2-i3/i01-source-digests.json) and [command provenance](../reports/P2-I3-I01-command-provenance.md) | I01 | Exact source/environment/reproduction identity | Accepted; 27 sources and six test invocations retained |
| `P2-I3-EV-009` | [I01 narrative audit](../reports/P2-I3-I01-source-current-capability-audit.md) | I01 | Human interpretation of source facts and missing surfaces | Accepted; no source admission or scientific result |
| `P2-I3-EV-010` | [I01 audit validation](../contracts/p2-i3/i01-audit-validation.json) | I01 | Package-completeness and quarantine validation only | Accepted; machine validation and source-audit gate passed through DEC-018 |
| `P2-I3-EV-011` | [N29/N30 mechanism inventory](../contracts/p2-i3/i01-n29-n30-mechanism-inventory.json) and [predecessor mechanism lineage](../contracts/p2-i3/i01-predecessor-mechanism-lineage.json) | I01 | Source-current experiment-mechanism and producer-feasibility evidence only | Accepted under original claim ceilings; cannot upgrade native capability or select P2-I3 realization |
| `P2-I3-EV-012` | [I02 source-admission manifest](../contracts/p2-i3/i02-source-admission-manifest.json) | I02 | Exact accepted source and role authority only | Accepted; 26 graph files, 40 callables, 24 tests, 8 theory sources, and 76 grouped precedents |
| `P2-I3-EV-013` | [I02 validation](../contracts/p2-i3/i02-admission-validation.json) and [report](../reports/P2-I3-I02-exact-source-admission.md) | I02 | Reconstruction and human interpretation of the admission bundle | Passed reconstruction; SOURCE-ADMISSION-GATE passed with no realization, runtime, or scientific effect |
| `P2-I3-EV-014` | Owner substrate clarification retained as DEC-020/CHG-017 | I02 | Eligible-substrate and interpretation boundary only | Accepted: LGRC9V3 core, GRC9V3 comparative-only; no realization selected |
| `P2-I3-EV-015` | [Q-005 decay interpretation study](../reports/P2-I3-Q005-decay-interpretation-study.md) | I03 | D0-first coherence-only analysis plus comparison of three added-mechanism ontologies, source support, realization boundaries, and safe reuse | Retained as amended N31 demand input under DEC-023/024; later DEC-026/028 resolve staged provider work and B-R Q-006 without rewriting this evidence |
| `P2-I3-EV-016` | [N31 handoff and return contract](P2-I3-N31-decay-primitive-handoff.md) | I03 | D0-first graph-side demand selection, P2-I3 pause boundary, required N31 return roles, and exact resumption procedure | Accepted through DEC-023/024; no graph result, P2-I3 realization, or scientific effect |
| `P2-I3-EV-017` | Owner-accepted coherence-only theory/LGRC-substrate evaluation and grounded pre-freeze clarification retained as DEC-024/CHG-024 | I03 | Prospective N31 hypothesis ordering, theory/closure boundary, representation and producer guards, provenance split, and specification-to-code authority barrier only | Accepted 2026-07-16; no gate reopening, implementation, runtime, or scientific effect |
| `P2-I3-EV-018` | [N31 return-admission manifest](../contracts/p2-i3/i03-n31-return-admission.json) and [validation](../contracts/p2-i3/i03-n31-return-validation.json) | I03 return transition | Exact N31 graph evidence and unselected provider-contract option authority; bounded distribution-metadata error retained | Accepted; all 11 return roles verified, return gate passed, no provider or evidence transfer |
| `P2-I3-EV-019` | [N31 return report](../reports/P2-I3-N31-return-admission.md) | I03 return transition | Human interpretation of D0, B-R, C.2, topology/ownership effects, reconstruction debt, and next selection boundary | Accepted as return authority; DEC-026/028 later resolve staged work and B-R carrier/ownership projection without transferring N31 evidence |

No selected realization, calibration, registration, runtime conformance,
control, or scientific evidence exists yet for P2-I3. The N31 return adds
graph-side evidence and provider-contract options only.

## 20. Current stop and next permitted action

Current stop:

```text
accepted semantic brief
+ accepted cumulative decision record
+ accepted evidence-expandable checklist
= passed P2-I3-BRIEF-GATE
+ Q-001 resolved by P2-I3-DEC-016
+ I01 input freeze accepted
+ environment preflight passed after owner-authorized pytest installation
+ complete source-current audit package retained and validated
= P2-I3-SOURCE-AUDIT-GATE passed
+ exact I02 source/callable/test/theory authority retained
+ I02 source and public-identity reconstruction passed
+ LGRC9V3 core / GRC9V3 comparative-only boundary fixed by DEC-020
+ P2-I3-Q-002 resolved by DEC-019
= P2-I3-SOURCE-ADMISSION-GATE passed
+ Q-005 original three-way interpretation retained
+ DEC-023 selects N31 cross-project spiral
+ DEC-024 makes coherence-only D0 the first N31 hypothesis
+ amended N31 departure and return contract retained
+ N31 closes and merges with B-R and C.2 reusable contracts
+ exact return identities and all 11 artifact roles validate
+ I12 reconstruction passes with 5 byte-exact artifacts
+ 3 artifacts differ only in incorrect distribution metadata/dependent digests
= bounded DEC-025 return transition accepted
= P2-I3-N31-RETURN-GATE passed
+ DEC-026 resolves Q-005 as B-R-first / C.2-second evaluation
+ B-R design is the only active route track
+ DEC-027 resolves B-R Q-008 without assigning its outcome
+ DEC-028 resolves B-R Q-006 without assigning a traversal or result
+ DEC-029 resolves B-R Q-007 without assigning a primary metric or result
!= field realization or discriminator gate passed
```

The next permitted action is to freeze the common ecology-result and
producer-cost envelope, assign Q-013 comparison identities, specialize Q-015
restoration design, and project DEC-027 through DEC-029 into operational
hypotheses and bounded conformance. C.2 design and every calibration or
scientific execution remain unauthorized.
