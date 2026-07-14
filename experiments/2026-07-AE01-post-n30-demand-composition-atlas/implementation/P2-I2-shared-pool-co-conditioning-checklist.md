# P2-I2 Shared-Pool Co-Conditioning Checklist

**Status:** active; authority bootstrap complete, source-current capability
audit not begun

**Iteration:** `P2-I2`

**Lane:** `AE01-L02`

**Current activity iteration:** `P2-I2-I01` — input-freeze construction
authorized; source inspection and capability audit not yet authorized or
performed

**Current local gate:** `P2-I2-BRIEF-GATE=passed`;
`P2-I2-SOURCE-AUDIT-GATE=pending`

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
| `P2-I2-SOURCE-AUDIT-GATE` | Source-current public PyGRC capability audit completed under one frozen audit scope | Pending; not begun | `P2-I2-I01` inputs and outputs remain unchecked |
| `P2-I2-SOURCE-ADMISSION-GATE` | Exact graph sources and any restoration-profile transition admitted for lane use | Blocked | Requires `SOURCE-AUDIT-GATE` |
| `P2-I2-DISCRIMINATOR-GATE` | Realization, dependence mode, factorization, access witness, and subordinate operational hypotheses frozen | Blocked | Requires source audit and admission dispositions |
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
- [x] Candidate graph revision
  `3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5` is only a proposed admission
  input, not an AE01 dependency.
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
| `P2-I2-I01` | Source-current PyGRC capability audit | I00R1 | Input-freeze construction authorized; source inspection not begun | `P2-I2-SOURCE-AUDIT-GATE` |
| `P2-I2-I02` | Source admission and restoration-profile transition disposition | I01 | Blocked | `P2-I2-SOURCE-ADMISSION-GATE` |
| `P2-I2-I03` | Realization, discriminator, dependence-mode, and operational-hypothesis freeze or missing-prerequisite classification | I01–I02 | Blocked | `P2-I2-DISCRIMINATOR-GATE` or retained earlier-stop route |
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

**Status:** input-freeze construction authorized; source inspection, API
invocation, conformance checks, and capability classification remain
unauthorized until Section 6.1 is retained as frozen.

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

- [ ] Record the exact graph repository revision and worktree state to audit.
- [ ] Freeze the repository-relative file/API scope and audit questions.
- [ ] Freeze allowed read-only commands and any non-mutating conformance checks.
- [ ] Declare whether installed-package inspection is needed and how package
  identity will be separated from checkout identity.
- [ ] Freeze output paths for the narrative audit, machine-readable capability
  matrix if needed, command provenance, and file-digest inventory.
- [ ] Record that audit failure or absence cannot become a negative L02 result.

### 6.2 Required capability questions

- [ ] Is there a public native non-private carrier with reconstructible
  identity and declared access scope?
- [ ] Can at least two attributable contribution paths alter one carrier
  without source-private response reads?
- [ ] Is there a carrier-scoped read, susceptibility, or eligibility path that
  does not require contributor addressing?
- [ ] Can encounter state, active history, or both persist and be intervened on
  independently of audit metadata?
- [ ] Can the audit-only label permutation and common-carrier intervention be
  expressed without causal bypass?
- [ ] Can pool write freeze and mode-relevant clamp interventions be expressed?
- [ ] Can a private-partition counterfactual preserve marginal contributions
  and opportunity without recreating a common state?
- [ ] Are reserve, accumulation, mixing, depletion, saturation, leakage, and
  maintenance observable or classifiably inapplicable?
- [ ] What native state is covered by restoration identity, and what ecology
  pool/intervention state would remain external?
- [ ] Does each candidate surface classify as `adequate`, `inadequate`,
  `absent`, or `unresolved`, with a precise reason and evidence reference?
- [ ] What is the smallest producer or constructed transition needed for each
  otherwise promising inadequate surface?

### 6.3 Audit outputs and exit

- [ ] Retain one narrative capability-audit report.
- [ ] Retain one compact requirement-to-surface matrix or explicitly justify
  why the report itself is the compact projection.
- [ ] Retain exact source revision, source paths, callable names, relevant file
  digests, and command provenance.
- [ ] Separate public API facts, inferred adequacy, missing surfaces, and open
  questions.
- [ ] Record a bounded shortlist or a classified absence without selecting the
  P2-I2 realization.
- [ ] Record all audit-derived decisions in the cumulative decision record.
- [ ] Validate that no graph-repository file changed.

Exit gate `P2-I2-SOURCE-AUDIT-GATE`:

```text
frozen audit scope + complete capability matrix + exact provenance
+ native adequacy classifications + missing-surface distinctions
+ no source admission or lane-result overclaim
= passed
```

## 7. `P2-I2-I02` — Source admission and restoration transition

**Status:** blocked on `P2-I2-SOURCE-AUDIT-GATE`.

**Purpose:** admit only the source identities relevant to the selected next
decision and define any explicit restoration-provider transition.

- [ ] Select the exact graph revision proposed for admission from I01 evidence.
- [ ] Recompute and retain admitted file digests from that revision.
- [ ] Bind repository revision, source files, runtime/package identity, and
  public callable identity without machine-local paths.
- [ ] Bind native restoration identity and digest callables when applicable.
- [ ] State accepted input scope and unsupported inputs.
- [ ] Declare ecology-owned pool, producer, intervention, and configuration
  state outside native identity.
- [ ] Declare the prior/fallback identity provider and its allowed scope.
- [ ] Forbid silent provider upgrade or downgrade.
- [ ] Define bounded equal-input continuation obligations separately from
  restoration-identity equality.
- [ ] Preserve the graph closeout claim boundary.
- [ ] Update the AE01 source inventory or retain a reviewed non-admission
  disposition.

Exit gate `P2-I2-SOURCE-ADMISSION-GATE` requires exact admitted identities or a
reviewed absence/inadequacy disposition. It grants no calibration or execution
authority.

## 8. `P2-I2-I03` — Realization and operational-hypothesis freeze

**Status:** blocked on I01 and the applicable I02 disposition.

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
| `L02-Q00` | Which public PyGRC surfaces could carry one pool? | I01 | Open | Source audit pending |
| `L02-Q01` | Is any native surface adequate to the L02 discriminator? | I01 | Open | Source audit pending |
| `L02-Q02` | Which graph sources and restoration provider are admitted? | I02 | Open | I01 required |
| `L02-Q03` | Which realization class is selected? | I03 | Open | I01–I02 required |
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

## 19. Evidence ledger

| Evidence ID | Iteration | Artifact or disposition | Evidence effect | Status |
| --- | --- | --- | --- | --- |
| `P2-I2-I00-BRIEF` | I00 | Accepted P2-I2 brief | Semantic authority only | Retained |
| `P2-I2-I00-CHECKLIST` | I00 | This checklist | Process and gate authority only | Retained |
| `P2-I2-I00-OPHYP` | I00 | [Operational-hypothesis scaffold](../hypotheses/p2-i2-operational-hypotheses.md) | Subordinate projection only | Retained |
| `P2-I2-I00-DECISIONS` | I00/I00R1 | Cumulative decision record, DEC-001 through DEC-004 | Decision authority only | Retained |
| `P2-I2-I00-VALIDATION` | I00R1 | [Compact validation provenance](../reports/P2-I2-I00-validation.md) | Integrity/process only | Retained |
| `P2-I2-I00R1-REVIEW` | I00R1 | Section 5.2 review disposition and `P2-I2-CHG-001` | Process correction only | Retained |
| `P2-I2-I01-PENDING` | I01 | No capability-audit artifact yet | None | Pending |

The ledger expands only when a named iteration retains evidence. It never
lists an intended artifact as though it already exists.
