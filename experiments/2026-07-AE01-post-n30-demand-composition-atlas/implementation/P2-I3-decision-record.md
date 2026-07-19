# P2-I3 Decision Record

**Status:** active cumulative lane decision record; initial governance package
accepted, `P2-I3-BRIEF-GATE`, `P2-I3-SOURCE-AUDIT-GATE`, and
`P2-I3-SOURCE-ADMISSION-GATE` passed; N31 has returned and the bounded
DEC-025 source transition is accepted and `P2-I3-N31-RETURN-GATE` passed; I03
now begins a staged B-R-first, C.2-second evaluation under DEC-026; neither
provider is selected as the lane result; DEC-027 resolves only the B-R
instance of Q-008; DEC-028 resolves only the B-R instance of Q-006; DEC-029
resolves only the B-R instance of Q-007; DEC-030 is the accepted common
comparison-envelope authority; DEC-031 resolves B-R Q-013; DEC-032 resolves
the I03 design portion of B-R Q-015; DEC-033 is the accepted B-R
operational-hypothesis projection; DEC-034 is the accepted inactive bounded-
conformance input freeze; DEC-035 accepts the exact B-R operational-
conformance package and passes `P2-I3-DISCRIMINATOR-GATE`; I04 calibration
preregistration is open but calibration execution remains unauthorized

**Lane:** `AE01-L03`

**Iteration:** `P2-I3`

**Evidence effect:** none; decisions constrain later work but are not results

**Controlling boundaries:**
[accepted P2-I3 brief](P2-I3-trail-or-stigmergic-field-brief.md),
[P2-I3 checklist](P2-I3-trail-or-stigmergic-field-checklist.md),
[common contract](../contracts/common-contract.md),
[post-R3 amendment](../hypotheses/post-r3-ecology-discriminator-amendment.md),
[developmental interpretation contract](../hypotheses/developmental-interpretation-contract.md), and
[execution policy](../configs/p1_i5_execution_policy.json)

## 1. Purpose and use

This is the single cumulative decision record for P2-I3. Every resolved or
partially resolved semantic, source, realization, dynamics, measurement,
control, registration, execution, interpretation, appendix, or closure
question receives a stable `P2-I3-DEC-*` identity here rather than a separate
file per decision.

The checklist is the activity and gate tracker. This record preserves:

```text
question
status
considered alternatives
reasoning
accepted boundary
remaining unknowns
gate effect
reopening condition
```

A decision may constrain a gate without passing it. Later evidence may reopen
a decision only through its recorded reopening condition and checklist change
control. It may not silently rewrite the historical choice.

Open questions use stable `P2-I3-Q-*` identities. An open question is not a
decision and supplies no implementation authority. When resolved, it receives
a new decision ID that points back to the question; the original question and
alternatives remain visible.

No decision may be inferred from:

- an activity performed outside its named checklist iteration;
- the first working implementation;
- a current PyGRC API name;
- a candidate result;
- an absent `.venv` or missing package;
- another AE01 lane's result; or
- an unreviewed appendix idea.

## 2. Decision index

| Decision ID | Question | Status | Gate effect | Date |
| --- | --- | --- | --- | --- |
| `P2-I3-DEC-001` | Is the P2-I3 semantic brief accepted as lane-local authority? | Accepted by project owner | Fixes semantic scope; does not pass the checklist-governed brief gate | 2026-07-16 |
| `P2-I3-DEC-002` | How must P2-I3 activities and decisions be planned and retained? | Owner-directed: one cumulative decision record and one evidence-expandable checklist | Requires checklist-first named iterations; initial package remains pending review | 2026-07-16 |
| `P2-I3-DEC-003` | How are registered structure, geometric distance, functional distance, causal/proper-time distance, and experimental causal influence related? | Accepted as five distinct surfaces | Constrains source audit through interpretation; no surface selected | 2026-07-16 |
| `P2-I3-DEC-004` | What is the core causal kernel? | Accepted two-route kernel with matched baseline opportunities and result-neutral post-formation observation | Constrains realization and registration; no topology values selected | 2026-07-16 |
| `P2-I3-DEC-005` | What dynamics are required and how do they relate to later traversal? | Accepted repeated costly formation, at least one non-static dynamic, and causal connection from that selected dynamic to traversal | Constrains realization, operational hypotheses, and support; no equation selected | 2026-07-16 |
| `P2-I3-DEC-006` | How are quantity matching, complete-state matching, history sufficiency, and relocation separated? | Accepted as distinct mode-aware contrasts with complete continuation-state equality | Requires separate operational IDs and controls before registration | 2026-07-16 |
| `P2-I3-DEC-007` | How are trail-field and stigmergic-field interpretations separated? | Accepted as bounded interpretation tags, not terminal classes or rungs | Same-participant evidence cannot alone receive the stronger stigmergic tag | 2026-07-16 |
| `P2-I3-DEC-008` | How are minimum/strong/highest interpretations related to thresholds and R01-R05? | Accepted without adding R06 or renaming frozen rungs | Constrains interpretation; thresholds remain ladders, not terminal selectors | 2026-07-16 |
| `P2-I3-DEC-009` | What is the appendix scope? | Appendices A/B dormant; Appendix C deferred | No appendix construction or execution authority | 2026-07-16 |
| `P2-I3-DEC-010` | Which implementation choices require explicit later decisions? | Runtime carrier, realization ownership, equation, observation, numeric registration, source admission, gates, and execution authority all require recorded decisions | Prevents implicit implementation authority from brief acceptance | 2026-07-16 |
| `P2-I3-DEC-011` | What happens when `.venv` or a required package is absent? | Stop and report exact absence; owner decides installation before work continues | Missing environment cannot redefine scope, validation, or scientific state | 2026-07-16 |
| `P2-I3-DEC-012` | What realization breadth is the proportional default? | One selected field realization plus one complete-state-matched formation-history discriminator | Multiple full modes require demonstrated necessity and explicit owner acceptance | 2026-07-16 |
| `P2-I3-DEC-013` | What is the logical floor for repeated formation? | More than one attributable formation event; exact cardinality remains an I06 decision | Prevents one event from satisfying repetition without freezing a premature numeric design | 2026-07-16 |
| `P2-I3-DEC-014` | Is the corrected initial governance package accepted? | Accepted; `P2-I3-BRIEF-GATE` passes | Opens only I01 input-freeze construction and review | 2026-07-16 |
| `P2-I3-DEC-015` | How are iteration packages reviewed and accepted without unnecessary ceremony? | Review is correction-driven; absent a concrete objection, progression treats the presented package as accepted | Preserves owner review without requiring a separate acceptance formula | 2026-07-16 |
| `P2-I3-DEC-016` | What exact scope resolves Q-001 and authorizes I01 audit activity? | Accept the review-ready I01 input freeze without correction | Opens only the frozen read-only capability audit | 2026-07-16 |
| `P2-I3-DEC-017` | Does missing native PyGRC coverage block a scientifically correct P2-I3 realization? | No: use semantically adequate native capability first and complete missing functions through explicit RCAE-owned producers | Converts native gaps into producer requirements and graph-side naturalization demands without weakening the experiment | 2026-07-16 |
| `P2-I3-DEC-018` | Does the complete grounded I01 package pass the source-audit gate? | Accepted by project owner after grounded artifact review and bounded CHG-014 clarification | Passes source-audit gate and opens only I02 exact source admission and Q-002 | 2026-07-16 |
| `P2-I3-DEC-019` | Which exact theory, graph, callable, test, and precedent identities resolve Q-002? | Accepted exact I02 bundle after bounded substrate and visibility corrections | Passes source-admission gate and opens only I03 realization questions | 2026-07-16 |
| `P2-I3-DEC-020` | May synchronous GRC9V3 evolution replace or bridge the required LGRC9V3 substrate? | No; LGRC9V3 is the core substrate and GRC9V3 is comparative-only | Corrects I02 roles and prevents a GRC result from satisfying or substituting for the L03 core | 2026-07-16 |
| `P2-I3-DEC-021` | Which route-local surface carries the minimum core field under Q-003? | Route-exclusive intermediate-node coherence, with edge and external-corridor alternatives retained | Fixes the carrier only; opens Q-004 ownership comparison without selecting a dynamic, equation, encounter, or result | 2026-07-16 |
| `P2-I3-DEC-022` | Which required functions are native, producer-assisted, constructed, unsuitable, or missing under Q-004? | Mixed ownership: native LGRC state/packet/restoration core plus explicit RCAE completion and controls | Fixes ownership truth and naturalization debt; opens Q-005 without selecting the dynamic or equation | 2026-07-16 |
| `P2-I3-DEC-023` | Should RCAE choose a decay implementation locally or return the missing primitive question to graph/LGRC? | Pause P2-I3 at Q-005 and select an N31 decay-semantic/native-primitive experiment through the cross-project spiral | Replaces the local two-implementation proposal with a graph handoff and exact P2-I3 return contract; Q-005 remains unresolved | 2026-07-16 |
| `P2-I3-DEC-024` | Must N31 first test whether ordinary coherence evolution already supplies bounded decay without an additional state? | Yes; D0 coherence-only derived decay is first, with causal slow organization separated from a fading graph observable | Amends the N31 demand and return paths, binds the theory/substrate/code authority split, and does not reopen gates or authorize P2-I3 implementation | 2026-07-16 |
| `P2-I3-DEC-025` | Can the exact N31 return and its two provider contracts be admitted despite incorrect retained PyGRC distribution metadata, without selecting a P2-I3 provider? | Accepted by project owner: admit B-R and C.2 as exact unselected options; retain the `0.0.0`/`0.1` distribution-metadata error and require fresh RCAE evidence | Passes `P2-I3-N31-RETURN-GATE` and opens only Q-005 plus affected DEC-021/022 comparison | 2026-07-19 |
| `P2-I3-DEC-026` | Should Q-005 select one N31 provider before evidence, or evaluate both and compare their ecology results and producer cost? | Accepted by project owner: execute separate B-R-first and C.2-second tracks, then compare without automatic winner selection | Resolves Q-005 as a two-route candidate program; opens only B-R realization decisions first and keeps C.2 execution inactive until B-R branch closeout | 2026-07-19 |
| `P2-I3-DEC-027` | For the B-R track, is complete current state or active formation history the primary continuation mode under Q-008? | Accepted by project owner: current composite state is primary, with one mandatory complete-state-matched formation-history discriminator | Resolves only B-R Q-008; Q-006/Q-007 and all conformance or later gates remain open | 2026-07-19 |
| `P2-I3-DEC-028` | What exact B-R field equation, units, update order, receipt lifecycle, and invariants resolve Q-006? | Accepted by project owner: repeated event-indexed conservative redistribution from a registered route source through the native carrier to an isolated reservoir | Resolves only B-R Q-006; Q-007, conformance, calibration, registration, execution, and all result gates remain open | 2026-07-19 |
| `P2-I3-DEC-029` | How does a later B-R probe encounter the local field without a hidden global selector under Q-007? | Accepted by project owner: paired independent branch-local fixed native departure requests, with LGRC9V3 alone deciding admission from local carrier coherence | Resolves only B-R Q-007; common comparison, Q-013/Q-015, conformance, calibration, registration, execution, and all result gates remain open | 2026-07-19 |
| `P2-I3-DEC-030` | Which common scientific and producer-cost fields can compare B-R and C.2 without collapsing their mechanisms or choosing a winner? | Accepted by correction-free progression: common semantic axes plus an unsummed three-class producer-cost vector and prospective C.2 influence register | Freezes comparison semantics only and leaves Q-013/Q-015, metrics, conformance, calibration, execution, and results open | 2026-07-19 |
| `P2-I3-DEC-031` | Which separate stable identities resolve B-R Q-013 after DEC-028 introduces a second quantity-matched relation? | Accepted by project owner: formation-quantity match, export-mass match, and complete-state/history match remain three non-substitutable contrasts | Resolves B-R Q-013 meaning/IDs only; I04 binds responses and I06 binds exact constructions | 2026-07-19 |
| `P2-I3-DEC-032` | What B-R restoration and equal-continuation design resolves the I03 portion of Q-015? | Accepted by project owner: one manifest-coordinated composite restoration interface with separate exact-execution and causal-continuation identities | Resolves B-R Q-015 design only; I06 must finalize schemas, fields, hashes, commands, horizon, and equality rules | 2026-07-19 |
| `P2-I3-DEC-033` | Does the B-R operational projection faithfully specialize `AE01-H-L03` and DEC-027 through DEC-032 without pre-answering metrics or results? | Accepted by project owner: thirteen operational hypotheses covering formation through bounded interpretation | Opens only bounded conformance-freeze construction; no runtime or scientific effect | 2026-07-19 |
| `P2-I3-DEC-034` | Which exact inactive input freeze may authorize one scientifically quarantined B-R conformance implementation and run? | Accepted by project owner: exact source/call bindings, two-route synthetic fixture, eleven cells, narrow RCAE interfaces, restoration/refusal, mechanical quarantine, and evidence-responsive stronger alternatives | Opens committed-source harness construction and one bounded conformance run only | 2026-07-19 |

## 3. `P2-I3-DEC-001` — Semantic authority

### Question

Is the P2-I3 brief accepted as the lane-local theory, geometry, ecology,
distance, observation, and claim-boundary directive?

### Selected resolution

The project owner accepted the brief on 2026-07-16. It binds:

- the D-039 inherited-relation/ecology-discriminator separation;
- the two-route causal kernel;
- the five-surface distance boundary;
- route-field ontology and identity-basin restraint;
- non-static dynamics causally connected to later traversal;
- minimum, strong, and highest interpretations;
- the exact frozen R01-R05 meanings;
- trail-versus-stigmergic interpretation discipline;
- dormant Appendix A/B and deferred Appendix C; and
- the bounded trail or stigmergic claim ceiling.

### Gate effect

Semantic meaning is accepted. Source audit, source admission, realization,
calibration, registration, runtime conformance, candidate execution, and
scientific interpretation remain unauthorized. `P2-I3-BRIEF-GATE` also
requires owner acceptance of this decision record and the checklist.

### Reopening condition

The checklist or source audit demonstrates a conflict with a frozen Phase 1
authority, or the two-route kernel cannot operationally separate the inherited
trace relation from the ecology-specific dynamic-field discriminator.

## 4. `P2-I3-DEC-002` — Checklist-first cumulative governance

### Question

How should P2-I3 retain decisions and evidence-triggered iteration changes?

### Considered alternatives

1. One file per decision.
2. Decisions embedded only in implementation reports.
3. One cumulative decision record plus one evidence-expandable checklist.
4. A complete immutable plan that cannot expand from results.

### Selected resolution

Use option 3. Every activity is a named checklist iteration declared before it
begins. Decisions remain cumulative in this file. Evidence may expand future
work between frozen cycles, but never within an active scientific cycle.

The initial checklist is provisional in content but strict in authority:

- pending future details may be added through change control;
- the currently active iteration boundary cannot drift silently;
- previous results and failed attempts remain retained;
- scientific refinements are new preregistrations, not retries; and
- stable cover gates project to the master checklist.

### Gate effect

No P2-I3 activity may occur off-ledger after this governance package is
accepted. Initial package construction itself is `P2-I3-I00` and carries no
capability or scientific effect.

### Reopening condition

The cumulative record becomes unable to express competing realization
families or evidence-triggered branches without ambiguity, or one checklist
becomes too large to preserve clear active-cycle authority. Any split must
preserve stable IDs and one unambiguous controlling index.

## 5. `P2-I3-DEC-003` — Five-surface distance and causality boundary

### Question

May registered structure or a computed distance surface substitute for
experimental causal influence?

### Selected resolution

No. P2-I3 separates:

```text
registered structure
geometric distance
functional distance
causal/proper-time distance
experimental causal influence
```

The first four may be measured, computed, annotation-only, inapplicable with
rationale, or unavailable as a missing surface. Experimental causal influence
must be measured and reconstructed for a positive result.

Later machine projection must map each semantic disposition through existing
vocabulary or an explicitly reviewed pre-freeze extension. The project must
not invent an artificial distance surface to complete a panel.

### Gate effect

Source audit must classify public PyGRC distance and timing surfaces by actual
runtime role. Calibration preregistration must select the primary response and
applicability of every panel. Registration must bind exact policies and inputs.

### Reopening condition

An admitted source exposes a distinct load-bearing distance or causal surface
not representable by the five roles, or two roles prove operationally
inseparable while preserving claim safety.

## 6. `P2-I3-DEC-004` — Two-route causal kernel

### Question

What is the smallest core geometry that can separate route structure, field
location, temporal dynamics, and later traversal?

### Selected resolution

Use two alternative route surfaces between one origin and target. Before
formation, match or account for registered structure and every applicable
baseline distance and traversal surface. After formation, observe every
surface without presuming equality, divergence, or direction.

The later traversal must encounter route-local field state. A global
trace-table `argmax`, route-label lookup, or controller-written preference
cannot carry the result.

### Alternatives preserved

- One-route dynamics remain a possible source-audit or component-conformance
  diagnostic but cannot close the core spatial-specificity relation.
- Three-or-more-route transfer remains dormant Appendix A.
- Shared-corridor transfer remains dormant Appendix B.
- Network reorganization remains deferred Appendix C.

### Gate effect

Realization must show local encounter. Registration must freeze baseline
matching, field location, route relocation, and hidden-router controls.

### Reopening condition

No admitted or bounded constructed realization can express two matched local
route surfaces, or a smaller topology proves capable of the same relocation
and route-specificity discriminator without weakening it.

## 7. `P2-I3-DEC-005` — Dynamic-field causal requirement

### Question

What distinguishes L03 from static persistent trace plus later eligibility?

### Selected resolution

Minimum positive support requires:

```text
repeated attributable formation at nonzero declared cost
+ at least one measured non-static field dynamic
+ causal connection from that selected dynamic to later traversal
+ later fresh traversal dependence
+ field-specific causal controls
```

The selected dynamic may be reinforcement, decay, maintenance, or saturation.
It must change traversal directly or change an independently intervenable
mediator that changes traversal. A co-occurring dynamic cannot carry support.

Strong interpretation adds reinforcement, withdrawal/decay, quantity-matched
pulse comparison, and maintenance. Highest within the lane adds saturation
and one registered variation or transfer.

### Gate effect

Realization and operational hypotheses must identify the selected dynamic and
its causal chain before calibration. No equation or numeric value is assigned
by this decision.

### Reopening condition

Source audit shows no realization can isolate any accepted non-static dynamic,
or a different non-static relation provides a more direct and falsifiable L03
discriminator while preserving the post-R3 amendment.

## 8. `P2-I3-DEC-006` — Matching, history, and relocation

### Question

How are temporal quantity, complete present state, formation history, and
field location compared without hidden unmatched state?

### Selected resolution

Use distinct operational identities:

```text
quantity_matched:
  equal total deposited quantity; current field may differ

state_matched:
  equal complete continuation-relevant current field; history differs

current_state_relocation:
  move complete registered current field from route A to route B

active_history_relocation:
  move or reconstruct complete current state and active causal history
```

Complete current state includes every registered continuation-relevant field,
pending update, phase, reserve/capacity, leakage, producer, scheduler, support,
and distance-policy input. An omitted component must be demonstrated
irrelevant.

Active-history relocation is valid only when history is causal, restorable,
and independently intervenable. Copying audit lineage does not qualify.

### Gate effect

Operational hypotheses and registration require separate cell/control IDs and
interpretation rules. A quantity-matched pulse cannot establish history
dependence unless complete current causal state is also matched.

### Reopening condition

The selected realization has no meaningful distinction between current state
and active history, or its continuation identity requires an additional
registered component.

## 9. `P2-I3-DEC-007` — Trail versus stigmergic interpretation

### Question

When may the stronger stigmergic interpretation be used?

### Selected resolution

```text
trail_field_candidate:
  evolving route-local field alters later traversal

stigmergic_field_candidate:
  one participant's attributable activity alters the field and thereby
  changes another eligible participant's later activity without direct
  addressing
```

These are interpretation tags, not terminal classes or rungs. A
same-participant probe can support only the trail-field tag. A fresh
nondepositor probe supports the stronger tag only when identity, mediation,
and direct-address exclusion resolve independently.

### Gate effect

Interpretation must record the applicable tag. Neither tag permits
communication, coordination, learning, colony, or agency language.

### Reopening condition

The eventual realization exposes a different participant/field relation that
cannot be classified honestly by the two tags.

## 10. `P2-I3-DEC-008` — Rungs, strength, and thresholds

### Question

Do richer dynamics create new rungs, and do numeric thresholds select the
result?

### Selected resolution

No R06 is added and no frozen rung is renamed:

```text
R01 costly attributable deposition
R02 persistent trace
R03 trace-dependent route function
R04 withdrawal/shuffle/false-trace specificity
R05 geometry/timescale variation
```

Minimum positive L03 support normally reaches through R04 because causal
specificity is mandatory. Stronger dynamic trajectories enrich the
interpretation within reached rungs. R05 requires one preregistered geometry
or timescale variation. Participant or susceptibility variation may inform
robustness but cannot independently assign R05.

The Phase 1 threshold, candidate-blind `delta`, and relation vocabulary remain
fixed anchors. They classify strength and resolution; they do not select the
terminal class. Narrow, resolution-limited, mixed, counter-directional, and
unexpected results remain scientific information.

### Gate effect

Calibration and registration still require explicit response, comparator,
matched-null generator, numeric inputs, and resolution artifacts. Candidate
outcomes cannot tune them.

### Reopening condition

A valid result exposes an important relation not representable by the frozen
metric relations, rung ladder, or developmental interpretation vocabulary.

## 11. `P2-I3-DEC-009` — Dormant and deferred appendices

### Question

Do topology extensions belong to the core P2-I3 authority?

### Selected resolution

- Appendix A, multi-route topology transfer, is dormant.
- Appendix B, shared-carrier overlap transfer, is dormant.
- Appendix C, network reorganization, is deferred until after core closeout
  and a separate semantic review.

Appendices cannot rescue, strengthen, or alter the core terminal result.
Activation requires a new named iteration and complete source, measurement,
registration, execution, and interpretation authority.

### Reopening condition

The core closes and its result supplies a falsifiable reason to activate one
extension, or a core result demonstrates that an extension was actually
load-bearing and therefore requires explicit redesign rather than relabeling.

## 12. `P2-I3-DEC-010` — Explicit implementation decisions

### Question

Which implementation choices may be inherited from the semantic brief or
filled by developer discretion?

### Selected resolution

None of the following may be implicit:

```text
exact theory and PyGRC source admission
runtime field carrier and access scope
native, producer-assisted, or missing-prerequisite status
selected non-static dynamic
field equation or update law
current-state/history causal mode
primary traversal response
distance-surface applicability and policy
metric comparator and matched-null generator
topology and every numeric value
cost, budget, leakage, and maintenance accounting
restoration and equal-continuation identity
control applicability
seeds, resources, attempts, and retries
clean-source runtime binding
candidate-cycle execution authority
appendix activation
```

Each is resolved at its checklist-defined decision point. More than one
realization may be retained when the scientific question requires comparison;
“primary” never means alternatives are erased.

### Gate effect

Every later gate must cite accepted decisions for its load-bearing choices.
Passing a validator cannot substitute for owner acceptance when the checklist
requires an explicit decision.

### Reopening condition

The selected implementation exposes a new load-bearing choice not represented
above or shows that two listed choices must be decided in a different order.

## 13. `P2-I3-DEC-011` — Environment completeness

### Question

How should work proceed when `.venv`, an interpreter, a required package, or a
pinned version is absent?

### Selected resolution

Stop and report:

```text
missing component
required version or identity
command that exposed the absence
affected iteration and gate
whether any permanent claim or output was created
```

The project owner decides whether to install or otherwise repair the
environment before work continues. Do not adapt the code, contract, command,
scope, or interpretation to treat an incomplete environment as correct.

Environment absence is infrastructure state. It is never:

- a scientific null;
- a missing PyGRC capability;
- evidence that a field surface is unavailable;
- authority to weaken validation;
- authority to use global Python; or
- an infrastructure retry unless the active freeze explicitly permits one
  after the owner-approved repair.

### Gate effect

Every command-bearing iteration begins with an environment preflight. The
preflight must not install packages. Any installation is a separate explicit
owner decision and retained process event.

### Reopening condition

The repository adopts a separately accepted reproducible environment manager
that can materialize the exact environment without an owner decision while
preserving installation accounting and network authority.

## 14. `P2-I3-DEC-012` — Proportional realization breadth

### Question

Should P2-I3 retain one bounded field realization or automatically expand into
parallel current-state, history-carried, and hybrid realization programs?

### Considered alternatives

1. Retain one selected realization only and do not test formation history.
2. Retain one selected realization plus one complete-state-matched
   formation-history discriminator.
3. Require full current-state, history-carried, and hybrid realization
   programs as the default.
4. Let the first working implementation determine the program breadth.

### Selected resolution

Use option 2 by default:

```text
one selected field realization
+ one complete-state-matched formation-history discriminator
```

The discriminator tests whether complete present causal state suffices without
recreating the P2-I2 mode program. More than one full realization mode is
permitted only when the source audit and causal design demonstrate that one
realization cannot answer the state/history question without changing its
semantics, and the project owner accepts that expansion explicitly.

This decision constrains the breadth of `P2-I3-Q-008`; it does not answer
whether current state or active history will prove load-bearing.

### Gate effect

I03 must begin from the proportional default. Any proposed multi-mode program
requires a new decision that cites the source/design necessity, added work,
control consequences, and downstream rerun scope.

### Reopening condition

The admitted runtime exposes irreducibly different current-state and
history-carried mechanisms whose comparison cannot be represented by one
realization and a complete-state-matched discriminator.

## 15. `P2-I3-DEC-013` — Logical repetition floor

### Question

What must “repeated attributable formation” mean before the exact finite event
count is registered?

### Considered alternatives

1. Leave repetition entirely undefined until registration.
2. Define repetition as more than one attributable formation event while
   deferring the exact cardinality.
3. Freeze an arbitrary universal count such as three or five events now.
4. Permit one event with a large quantity to count as repeated formation.

### Selected resolution

Use option 2. A repeated-formation history contains at least two temporally
distinguishable attributable formation events. A single pulse or event cannot
satisfy repetition regardless of quantity.

The exact finite count, timing, quantity per event, cost, and matched pulse
belong to I06 registration after source admission, realization, and
calibration. The post-R3 requirement for at least two trace-history conditions
is separate: it governs contrasted histories, while this decision governs the
minimum event cardinality inside a history described as repeated.

### Gate effect

I03 operational hypotheses must preserve event-level attribution and temporal
ordering. I06 must freeze the exact repeated-event count and cannot reduce it
to one after candidate outcomes.

### Reopening condition

The selected runtime represents formation as a continuous registered process
for which event cardinality is not meaningful. Reopening must replace the
event floor with an equally falsifiable non-single-exposure duration or update
criterion before calibration.

## 16. `P2-I3-DEC-014` — Initial governance acceptance

### Question

Do the corrected brief, cumulative decision record, and evidence-expandable
checklist form an adequate initial authority stack for P2-I3?

### Selected resolution

Yes. The project owner accepted the package after review confirmed:

- separate I01 freeze-construction and audit-activity authorities;
- exact R05 geometry/timescale scope;
- declared-effect ownership and scientific conformance quarantine;
- typed numeric, causal-chain, and mixed control evidence;
- proportional realization breadth and the repetition floor;
- distinct quantity/state matching and relocation handoffs; and
- separately governed post-core appendices.

The remaining I03 wording is clarified so operational observability cannot be
misread as scientific measurement. I01 must also preserve public-source fact,
synthetic interface-conformance, and candidate-shaped behavior as distinct
evidence classes.

### Gate effect

`P2-I3-BRIEF-GATE` passes. This opens construction and owner review of the
exact I01 capability-audit input freeze only. `P2-I3-Q-001` remains open, and
no audit activity, source admission, realization, conformance run,
calibration, registration, execution, or L03 evidence is authorized.

### Reopening condition

A concrete conflict appears between this package and a controlling Phase 1
authority, or I01 input-freeze construction exposes a semantic ambiguity that
cannot be resolved under the existing brief and decisions.

## 17. `P2-I3-DEC-015` — Correction-driven iteration review

### Question

Must every P2-I3 iteration receive a separate ceremonial acceptance statement
after its package is presented and reviewed?

### Selected resolution

No. Every iteration package is still presented for owner review, but review is
correction-driven:

```text
concrete owner comment:
  affected scope remains open and is corrected before progression

no concrete objection + direction to continue:
  presented package is treated as accepted

review reports no blocker + owner proceeds:
  reviewed package is treated as accepted
```

An explicit phrase such as “I accept” is not required. Silence by itself while
work is paused does not authorize progression; the owner's next instruction to
continue supplies the operational acceptance. Unaffected portions of a package
do not reopen merely because one bounded correction is requested.

Gate and checklist status must still be recorded before dependent activity.
This decision removes redundant ceremony, not review, evidence, validation,
or authorization boundaries.

### Gate effect

Future review-ready iterations may advance on an owner direction to continue
when no unresolved concrete objection remains. Candidate execution, package
installation, external mutation, and other separately explicit authorities
retain their existing rules.

### Reopening condition

The convention makes it ambiguous whether a load-bearing correction was
resolved, or a future iteration requires a legally, operationally, or
scientifically distinct explicit authorization.

## 18. `P2-I3-DEC-016` — I01 capability-audit input freeze

### Question

Does the review-ready I01 input freeze adequately resolve `P2-I3-Q-001`, and
what activity does its acceptance authorize?

### Considered alternatives

1. Accept the exact frozen scope and begin only its read-only audit.
2. Revise the capability questions, source identities, path scope, command
   envelope, evidence classes, or required outputs before inspection.
3. Authorize a synthetic conformance probe with the source audit.
4. Treat freeze acceptance as source admission or realization authority.

### Selected resolution

Option 1. The project owner reviewed the input-freeze package, raised no
concrete correction, and directed the work to continue. Under
`P2-I3-DEC-015`, this accepts the exact freeze and resolves
`P2-I3-Q-001`.

The accepted scope fixes:

- the clean graph/PyGRC and distance-theory checkout identities;
- fifteen capability questions and ten separately classified operation
  dispositions;
- the tracked path scope and public-callable boundary;
- allowed read-only static inspection, import/introspection, and
  pre-existing-test commands;
- public-source fact, synthetic interface-conformance, and candidate-shaped
  behavior as distinct evidence classes;
- synthetic probes as disabled unless a later concrete gap is separately
  reviewed;
- exact environment, mutation, checkout-integrity, provenance, output, and
  exit requirements; and
- the claim boundary that the audit creates capability evidence only.

Options 3 and 4 remain prohibited. The audit may identify a source as
adequate, inadequate, absent, unsuitable, or unresolved, but it cannot admit
that source, select a field carrier or equation, execute candidate-shaped
behavior, or create L03 scientific evidence.

### Gate effect

I01 audit activity is authorized after the frozen environment preflight
passes. `P2-I3-SOURCE-AUDIT-GATE` remains open until all frozen outputs are
retained, validated, reviewed, and accepted. I02 and every later iteration
remain unopened.

### Reopening condition

The preflight or audit exposes a concrete mismatch in a frozen revision,
tracked path, required public-interface question, command assumption, evidence
class, or output requirement that prevents the exact audit from answering
Q-001 honestly. Reopening must record the bounded correction before the
affected audit activity continues.

## 19. `P2-I3-DEC-017` — Native priority and producer completion

### Question

Does an absent or semantically inadequate native PyGRC operation block P2-I3,
or force the experiment to test only what the current runtime already exposes?

### Considered alternatives

1. Require every load-bearing operation to be native and block the realization
   when one is missing.
2. Reduce or redirect the scientific question until it fits current native
   coverage.
3. Prefer a semantically adequate native operation, but implement any missing
   load-bearing function as an explicit RCAE-owned producer or constructed
   operation without weakening the causal question.
4. Build the whole realization outside PyGRC even when adequate native
   operations already exist.

### Selected resolution

Use option 3. Naturalization depth is subordinate to scientific adequacy:

```text
semantically adequate native PyGRC capability exists:
  use it as the first realization candidate

native capability is absent or changes the intended causal relation:
  retain the scientific requirement
  + implement the smallest explicit RCAE-owned producer completion
  + keep ownership, state effects, identity, and controls visible
  + record the missing native pattern as graph-side naturalization debt
```

“Native priority” is not “native at any cost.” A public operation receives
priority only when it realizes the same registered causal function without
hidden route selection, outcome writing, unmatched state, or additional
state effects that change the experiment. The experiment must not be reduced,
redirected, or declared impossible merely because current PyGRC lacks a trail
field, decay law, local encounter, relocation, or another selected operation.

Two producer-completion forms are allowed for later I03 consideration:

1. **Request producer:** RCAE reads immutable, registered runtime-visible
   state and emits a typed request; PyGRC performs the native transition. N05
   and N09 are precedents for producer scheduling followed by native queue
   processing. The producer may not author the scientific response.
2. **Declared state producer:** when no native transition can express the
   required state change, RCAE performs the smallest typed, reconstructable,
   explicitly receipted transition over the registered composite state. N22's
   experiment-owned conductance carrier is the controlling precedent: the
   mutation remained producer-mediated, entered replay and controls, and was
   never promoted to native route-conductance memory.

Any producer completion must freeze:

- why every nearby native operation is absent, inadequate, or unsuitable;
- exact read inputs, write targets, units, equation, ordering, and invariants;
- whether PyGRC or RCAE owns each state transition;
- composite snapshot, restoration, reset, branch, and continuation identity;
- producer-absence/dependence and hidden-controller controls;
- a failure boundary that distinguishes implementation failure from a valid
  scientific negative; and
- the precise missing LGRC pattern that the graph project could later test or
  naturalize.

Later native coverage cannot silently replace a frozen producer path. Such a
transition requires a new realization profile, explicit provider change, and
rerun. Conversely, producer success cannot upgrade a constructed operation to
native capability or authorize a graph-repository change from RCAE.

### Source-lineage rationale

N29 is an index rather than the full authority for this rule. Its relevant
predecessors show a staged path:

```text
N05/N09:
  producer decision/request -> native PyGRC packet transition

N08:
  serialized trail-memory scaffold exposes the missing route-memory law;
  static positive geometry does not close the dynamic gap

N22:
  explicit producer-owned carrier mutation -> native snapshot/readback/reentry
  -> controls and durability, without a false native claim

N29/N30:
  preserve composition debt, evidence boundaries, and inherited relation
```

This is the intended graph/ecology spiral: RCAE may construct a missing
pattern honestly, test what ecological relation it enables, and hand the
result back as a proposed graph discriminator. Lack of native runtime support
therefore creates an implementation obligation and naturalization debt, not a
scientific veto.

### Gate effect

I01 native classifications remain unchanged: a native operation may still be
`adequate`, `inadequate`, `absent`, or `unsuitable`. I01 must now record a
separate producer-completion feasibility and precedent where evidence exists.
I02 may admit exact producer-pattern sources by role. I03 resolves Q-004 by
assigning each selected function to native, request-producer, declared-state-
producer, constructed, or unsuitable ownership.

An absent native operation does not block `P2-I3-DISCRIMINATOR-GATE` when a
bounded producer completion can preserve the accepted causal kernel and pass
conformance. A missing operation blocks later execution only when neither a
semantically adequate native path nor a reconstructable producer completion
can express the requirement honestly.

### Reopening condition

A source-current native operation proves semantically equivalent to a frozen
producer completion, or the proposed producer boundary cannot preserve local
encounter, reconstructable state, causal attribution, and hidden-controller
exclusion. Reopening changes provider selection through a new recorded
realization; it does not retroactively change the ownership of earlier runs.

## 20. `P2-I3-DEC-018` — I01 source-audit acceptance

### Question

Does the complete I01 package answer the accepted capability-audit question
with adequate source, ownership, producer-feasibility, provenance, and
quarantine discipline?

### Selected resolution

Yes. The project owner explicitly passed the review after a grounded reviewer
read all eleven retained artifacts. The review confirmed:

- all fifteen capability and ten operation dispositions against their actual
  machine records;
- 27 public/theory, 32 N29/N30, and 44 predecessor source identities;
- exact environment, command, test-filter, revision, and digest provenance;
- 24 passing targeted pre-existing tests with 333 filtered deselections;
- no synthetic probe, candidate execution, source mutation, admission, or
  scientific effect;
- unchanged native classifications plus separate producer-completion
  feasibility under DEC-017; and
- narrative-to-matrix consistency.

The six non-blocking review refinements were closed in one bounded CHG-014
pass. Candidate-surface IDs now explicitly name audit targets rather than
assert existence, CAP-14/15 have machine-readable meta roles, OP-07 separates
nearest nonqualifying callables from its empty qualifying-callable set, and
the missing scope/filter cross-references are explicit. No classification,
source scope, scientific meaning, test result, or execution authority changed.

### Gate effect

`P2-I3-SOURCE-AUDIT-GATE` passes. I01 is accepted and complete. Only I02 exact
source admission and `P2-I3-Q-002` open. Gate passage does not itself admit a
theory or runtime source, select a carrier, dynamic, equation, producer,
response, or realization, run conformance or calibration, or create L03
scientific evidence.

### Reopening condition

An exact retained digest fails reconstruction, an admitted I02 source cannot
be traced to the accepted I01 classification, or a later public-source check
shows that a load-bearing I01 fact was classified from the wrong revision or
evidence class. A new implementation preference or producer alternative does
not reopen I01.

## 21. `P2-I3-DEC-019` — Exact I02 source admission

### Question

Which exact theory and graph revisions, files, public callables, pre-existing
tests, producer precedents, and evidence roles may P2-I3 realization work
consume?

### Accepted resolution

Admit the exact
[I02 source manifest](../contracts/p2-i3/i02-source-admission-manifest.json)
after correction-driven owner review. The accepted bundle binds:

- graph/PyGRC revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594`, all 26 graph files in the
  accepted I01 source-digest inventory, 40 public callable identities, and 24
  exact pre-existing generic tests;
- geometric-theory revision
  `e0d25bf69b8bf681eb8d092ba416497030e5d88e` with the exact RC-Distance and
  three becoming/development files named by the brief;
- RCAE revision `8f09ae2f9abf734829f8f046b9be2015ae007458` with the four
  current conceptual/method papers named by the brief;
- the exact 32-source N29/N30 inventory as inherited evidence and orientation
  only; and
- the exact 44-source predecessor inventory as constructed-producer/control
  precedent only.

Every graph source receives exactly one package, interface, runtime-option,
measurement-option, restoration-option, conformance, claim-boundary, or
comparative/exclusion role. Public callables are admitted only as later options,
supporting implementation identities, or explicitly nonqualifying boundary
references. Their presence does not select or prove a complete realization.

DEC-020 further constrains the bundle: P2-I3 targets `LGRC9V3`. The
`GRC9V3` class, `apply_continuity()`, and synchronous `step()` are retained
only as comparative-substrate identities. Their distinct full-step evolution
and relaxation semantics cannot replace an LGRC9V3 realization or discharge
an LGRC9V3 missing surface. `GRC9V3State` remains admitted because it is the
public base-state type used by LGRC9V3, not because synchronous GRC execution
is an eligible core path.

The four RCAE conceptual files have changed since their historical P1-I1
admission. I02 therefore records both the P1 digest and the current committed
I02 digest. This prospective lane-local transition neither rewrites the P1
inventory nor changes an earlier claim.

Under DEC-017, the admitted predecessor sources establish that an RCAE-owned
request or declared-state producer is a permissible later option without any
PyGRC-repository change. Such a producer remains constructed, may invoke only
admitted public native operations, may not author the desired outcome or hide
a global selector, and exports every load-bearing missing native pattern as
naturalization debt. Native replacement later requires an explicit source and
realization transition plus rerun.

The five evidence classes remain distinct: graph and prior-experiment facts
are inherited evidence; theory sources constrain ecology interpretation;
producer precedents support only a constructed mechanism; I01 gaps remain
missing surfaces; and the brief remains a proposed discriminator rather than
evidence.

### Gate effect

The project owner accepted the corrected manifest on 2026-07-16. DEC-019
therefore resolves Q-002 and passes `P2-I3-SOURCE-ADMISSION-GATE`, opening only
I03 questions Q-003 through Q-008. It does not select a source combination for
execution, carrier, dynamic, equation, producer, response, metric, or result.

### Reopening condition

A later realization needs an unadmitted source or callable; a new graph
revision changes a load-bearing operation, restoration identity, or missing-
surface classification; a theory-source change alters lane meaning; an
admitted producer pattern cannot be reconstructed from the exact inventory;
or a native transition is proposed for a retained RCAE producer.

## 22. `P2-I3-DEC-020` — LGRC9V3 substrate authority

### Question

May P2-I3 use synchronous `GRC9V3` evolution as a replacement, bridge, or
equivalent implementation of the required `LGRC9V3` substrate?

### Selected resolution

No. The project owner clarified that P2-I3 is interested in the `LGRC9V3`
substrate. `GRC9V3` and `LGRC9V3` have different step ownership and different
per-step evolution/relaxation semantics. In particular, the public LGRC9V3
runtime processes one deterministic queue event and explicitly does not call
synchronous `GRC9V3.step()`.

Therefore:

- the core P2-I3 realization must execute over `LGRC9V3`;
- native-priority under DEC-017 means semantically adequate native LGRC9V3
  capability, not any operation exported by the broader PyGRC package;
- an RCAE producer may complete missing LGRC9V3 functions but may not call a
  GRC9V3 step and relabel the result as LGRC9V3 behavior;
- a separately described GRC9V3 result may be retained as interesting
  comparative evidence; and
- a GRC9V3-only positive result leaves the L03 core unsupported or blocked by
  a missing LGRC9V3 surface, according to the registered execution state.

This decision does not choose a route-local carrier, field dynamic, equation,
producer, response, or metric. It fixes only the eligible substrate family
and interpretation boundary.

### Gate effect

I02 must classify `GRC9V3`, `GRC9V3.apply_continuity()`, and
`GRC9V3.step()` as `supporting_comparative_substrate_only`. I03 cannot select
them as the core realization or use them to close Q-004. A future GRC9V3
comparative study requires a separately governed scope and cannot pass the
core P2-I3 discriminator or lane gate.

### Reopening condition

The project owner explicitly changes the primary substrate, or a future
source-current LGRC9V3 implementation natively incorporates an operation with
the required semantics. The latter changes LGRC9V3 capability classification;
it does not make a historical GRC9V3 result equivalent retroactively.

## 23. `P2-I3-DEC-021` — Minimum core field carrier

### Question

Which route-local surface carries the minimum P2-I3 core field under
`P2-I3-Q-003`?

### Considered alternatives

#### Option A — route-exclusive intermediate-node coherence

Each matched route contains one exclusive intermediate node. Its public
LGRC9V3 node-coherence value is the route-local carrier. Native packet arrivals
can form and repeatedly accumulate the carrier through attributable,
budget-conserving transfers; departures can withdraw quantity. Native runtime
state, events, clocks, packet lineage, and continuation are restorable.

This option has the smallest current ownership gap, but node coherence is not
a native trail abstraction. RCAE must still declare the carrier-node mask,
field interpretation, lifecycle boundary, interventions, and local encounter.
Q-005/Q-006 decide whether coherence is the complete field value or the native
substrate beneath an additional RCAE-owned law. Q-007 decides how a later
traverser consumes it without a route label or global ranker.

#### Option B — edge-local base conductance

Edge conductance is geometrically intuitive and closest to a conventional
trail-support surface. N22 provides a strong precedent for a declared-state
producer that changes experiment-owned conductance while preserving native
snapshot, replay, reentry, and controls.

The source-current LGRC9V3 event runtime does not natively update conductance
as a consequence of traversal. Selecting it would therefore make formation,
reinforcement, and other chosen dynamics producer-owned from the beginning,
with more composite-state and naturalization debt than Option A.

#### Option C — explicit RCAE corridor field

A corridor-owned scalar or structured field would make route extent, equation,
relocation, false-trace insertion, and lifecycle semantics explicit without
overloading node coherence or conductance. It is also the most constructed
option: RCAE would own the carrier state, update law, serialization,
restoration wrapper, intervention surface, and graph-side naturalization debt.
It is retained for a later campaign if native-state coupling proves
scientifically distorting or too restrictive.

#### Option D — passive pulse/evidence surface

Rejected as a carrier. Pulse-surface rows record contact, timing, lineage, and
before/after evidence but do not carry mutable persistent field state. Their
producer configurations also name explicit packet endpoints and edges. They
may support receipts or conformance, never the causal field itself.

A node-plus-edge or other composite carrier was not selected. Under
`P2-I3-DEC-012`, added carrier breadth requires demonstrated necessity rather
than convenience.

### Selected resolution

Select Option A: route-exclusive intermediate-node coherence is the minimum
core carrier.

The core topology will later register two baseline-matched routes with one
exclusive intermediate carrier node per route. Formation may use explicit
addresses to deliver native packet work, but formation addresses, route names,
packet lineage, and success labels are excluded from the later traversal
input. The later encounter may consume only the registered local carrier state
and other inputs explicitly admitted by Q-007.

LGRC9V3 owns node-coherence storage and every native packet transition. RCAE
owns only the role/mask declaration and any later lifecycle, intervention, or
encounter operation explicitly selected under Q-004 through Q-007. Calling
the carrier a field is an ecology-side operational interpretation until the
complete causal chain is implemented and tested.

### Why this option was selected

- It maximizes semantically adequate native LGRC9V3 ownership.
- Attributable costly formation and repeated accumulation already have public,
  source-backed native transitions.
- Carrier and formation history enter native restoration and causal receipts.
- It confines construction to the operations I01 actually found missing:
  lifecycle, intervention, participant roles, and local encounter.
- It gives a strict test of whether an existing LGRC surface can support the
  ecology discriminator before introducing a wholly external field object.

This is a proportional starting choice, not a claim that node coherence is the
universally best or most natural trail carrier.

### Gate effect

Q-003 is resolved. Q-004 may now classify ownership for the selected node
carrier and its still-missing operations. No dynamic, equation, field units,
encounter policy, dependence mode, conformance fixture, calibration value, or
scientific outcome is selected. `P2-I3-DISCRIMINATOR-GATE` remains open.

### Reopening and alternative-campaign rule

Reopen Q-003 before the discriminator gate if Q-005 through Q-007 or bounded
conformance demonstrates that node coherence cannot express an independently
intervenable field lifecycle and local encounter without changing LGRC9V3
semantics, hiding a route selector, conflating participant capacity with field
state, or preventing complete restoration and relocation controls.

An edge-conductance or explicit-corridor alternative may also be executed
later even if the node realization succeeds. Such work must receive a new
realization and campaign identity, restart every affected I03-and-later
contract and gate, and retain the node realization rather than silently
replacing it. A different candidate outcome or aesthetic preference alone
does not rewrite this decision; it motivates a separately traceable
alternative experiment.

## 24. `P2-I3-DEC-022` — Realization ownership map

### Question

For every function required by the node-carried realization, is the operation
native LGRC9V3, minimally producer-assisted, explicitly constructed,
unsuitable, or scientifically missing under `P2-I3-Q-004`?

### Considered ownership strategies

#### Option A — call the complete realization native

Rejected. Public LGRC9V3 owns node coherence, packet transfers, queue/event
time, and native restoration, but it does not own a trail-field lifecycle,
fixed-topology field interventions, participant roles, or a compliant local
carrier-to-traversal response. Calling the composition native would erase the
main graph-side demand exposed by the experiment.

#### Option B — construct the whole realization in RCAE

Rejected as disproportionate. It would duplicate adequate LGRC9V3 state,
packet, timing, accounting, and restoration functions and weaken the test of
what the admitted substrate can already carry.

#### Option C — mixed native core with explicit RCAE completion

Selected. Adequate public LGRC9V3 operations retain transition ownership.
RCAE owns only the missing eligibility, lifecycle, intervention, role, and
composite-identity functions demonstrated necessary by later decisions.
Producer assistance never upgrades the underlying native capability class.

#### Option D — silently bridge nearby operations

Rejected. Synchronous GRC9V3 evolution, global route arbitration,
topology-lineage transport, passive pulse rows, and post-hoc pheromone
inference answer different causal questions and cannot be relabeled as the
missing LGRC9V3 field operations.

### Accepted ownership map

| Function | Accepted ownership/disposition | Boundary |
| --- | --- | --- |
| Node-coherence carrier storage and readback | native LGRC9V3 | RCAE supplies only the declared route-node role/mask and interpretation |
| Costly attributable deposition | native LGRC9V3 packet departure/arrival | formation addresses and lineage cannot enter the later response |
| Repeated node accumulation | native LGRC9V3 repeated arrivals | adequate only for node-state accumulation; Q-005 decides whether it is the selected dynamic |
| Conserved withdrawal | native LGRC9V3 departure debit | control or transfer only; it is not autonomous decay |
| Queue ordering, event time, packet budget, and causal receipts | native LGRC9V3 | evidence and accounting do not become field state |
| Decay | native operation absent; RCAE producer required if selected | prefer a request producer plus native transfer when Q-006 semantics permit; otherwise declare the exact non-native transition |
| Costly maintenance | native operation absent; RCAE producer required if selected | must respond to the selected loss dynamic and cannot rename ordinary deposits |
| Saturation or field-response cap | native operation absent; RCAE policy/producer required if selected | source-budget rejection is not field saturation |
| Later local carrier-to-traversal encounter | native path inadequate; bounded RCAE request producer required | producer may read only registered local opportunity/carrier inputs and must hand transition work back to LGRC9V3; Q-007 fixes factorization |
| False-trace insertion, clamp, state/history shuffle | constructed RCAE controls | typed interventions only; never hidden candidate tuning |
| Fixed-topology carrier relocation | constructed RCAE control | topology refinement/reabsorption is unsuitable; Q-013/Q-015 fix equality and identity |
| Native snapshot, load, and reset | native LGRC9V3 | covers only native state |
| Complete save/load/reset/branch/equal continuation | native restoration plus RCAE composite wrapper | every selected producer, policy, intervention, and external state must be included or the operation fails closed |
| Participant roles, access, depositor/probe episodes, and direct-address exclusion | constructed RCAE manifests and guards | orchestration metadata cannot author the traversal response |

No required function is yet classified `scientifically_missing`. Native
decay, maintenance, saturation, fixed-topology relocation, and local encounter
surfaces are absent or inadequate, but admitted producer/control precedents
make bounded completion plausible. Q-005 through Q-007 and conformance must
still demonstrate that the selected completion preserves the experiment. A
failed adequate binding may later become a precise missing-surface result; it
must not be disguised as a scientific negative.

### Naturalization debt

The initial graph-side debt is:

- an LGRC-integrated route-local field lifecycle if a non-native dynamic is
  selected and remains load-bearing;
- a local carrier-to-traversal opportunity interface without explicit outcome
  addresses, route labels, or global ranking;
- fixed-topology field intervention and relocation surfaces if they remain
  essential controls; and
- composite restoration support for any producer/policy state that cannot be
  reduced to native LGRC9V3 identity.

Debt is specialized after Q-005 through Q-007; this decision does not claim
that every possible optional operation must be naturalized.

### Gate effect

Q-004 is resolved. Q-005 may now select one non-static dynamic from this
ownership map. Q-006 still owns the exact law, units, ordering, invariants,
and any request-versus-declared-state producer choice. Q-007 still owns the
local encounter. No implementation, conformance, calibration, registration,
or scientific execution is authorized. `P2-I3-DISCRIMINATOR-GATE` remains
open.

### Reopening condition

Reopen the affected ownership row if an admitted or later explicitly
transitioned PyGRC revision adds a semantically adequate native operation; if
Q-005/Q-006 requires a state effect that cannot be expressed through the
recorded ownership path; if Q-007 cannot avoid an outcome-writing producer; or
if complete composite restoration cannot be demonstrated. A native transition
requires a new source/realization identity and rerun; it never silently
replaces retained RCAE behavior.

### Pre-decision Q-005 interpretation evidence

The owner-directed
[Q-005 decay interpretation study](../reports/P2-I3-Q005-decay-interpretation-study.md)
retains three non-equivalent meanings:

```text
release-efficacy attenuation
coherence-conserving source leakage
constructed route-susceptibility relaxation
```

It corrects one unsafe early reuse assumption: the leakage and susceptibility
realizations may share semantic protocol and artifact infrastructure, but they
must not be presumed to share a concrete topology. Leakage likely requires a
closed receiver/reservoir relation around the node carrier; susceptibility
likely requires edge/corridor coupling and a different complete-state and
local-encounter contract.

The report originally recommended leakage as the DEC-021-compatible core
direction and susceptibility as a separate RCAE-constructed realization.
DEC-023 supersedes that local implementation direction before either
realization was selected or built. The three meanings now serve as N31 input,
and Q-005 remains intentionally unresolved pending the graph-side return.

## 25. `P2-I3-DEC-023` — N31 decay-primitive spiral handoff

### Question

Should P2-I3 select and implement decay locally from the three Q-005
interpretations, or should it return the unresolved primitive to the graph
project before continuing ecology composition?

### Trigger

The Q-005 study established:

```text
release-efficacy attenuation
!= coherence-conserving source leakage
!= route-susceptibility relaxation
```

Current RC theory, LGRC specification, and PyGRC implementation do not select
one of these as the decay primitive. Native packet mechanics strongly support
conserved transfer, but not an autonomous leak law. RC-Distance supports
instantaneous state/flux-derived geometry, but not slow susceptibility
relaxation. N08 records native route-conductance memory as missing, and N22
retains a producer-mediated susceptibility candidate with naturalization debt.

### Considered paths

#### Option A — implement leakage and susceptibility inside P2-I3

This would preserve ecology momentum and permit two explicit constructed
realizations. It would also make RCAE responsible for resolving a substrate-
level semantic distinction before graph/LGRC had tested or specified it.
Different carrier, topology, invariant, restoration, and encounter contracts
would create two full scientific programs rather than a small lifecycle
choice.

#### Option B — select only conserved leakage inside P2-I3

This is the smallest path consistent with DEC-021 and current native packet
mechanics. It still requires RCAE to invent the autonomous source-emission law
and might prematurely naturalize “decay” as redistribution without comparing
the relational alternative at graph level.

#### Option C — return the primitive question to graph/LGRC as N31

N30's closeout explicitly established a cross-project spiral:

```text
N30 graph result
-> agentic-ecology demand pass
-> selected N31+ primitive/building-block probe
```

The N30+ direction catalog already includes slow-memory conductance trace but
leaves N31 unfixed pending ecology demand. P2-I3 now supplies a concrete demand
that is broader than conductance: discriminate decay semantics and naturalize
the best warranted LGRC9V3 primitive, permitting plurality or non-selection.

### Selected resolution

Select Option C.

Pause P2-I3 at Q-005. Preserve all three interpretations as the input to a
small graph-side experiment provisionally titled:

```text
N31 — LGRC9V3 Decay Semantics and Native Primitive
```

N31 should use candidate-specific minimal fixtures, source-current evidence,
internal-time and invariant audits, local causal readout, restoration, and
controls. It may select one primitive, distinct multiple primitives, a
producer-only candidate, no primitive, or a new taxonomy.

The exact departure, graph return bundle, outcome branches, RCAE source
transition, and resumption order are fixed in the
[N31 handoff and return contract](P2-I3-N31-decay-primitive-handoff.md).

### What remains frozen

- All historical decisions and admitted source classifications remain intact.
- The graph and geometric-theory repositories remain read-only in RCAE scope.
- Q-005 is deferred, not answered.
- Q-006 through Q-008 and all I04-and-later work remain unopened.
- No P2-I3 implementation or conformance may proceed during N31.
- N31 demand is not evidence and cannot support L03.

### Return boundary

P2-I3 resumes only after:

1. N31 closes with a committed, reconstructable return bundle;
2. RCAE admits the exact N31 revision through a bounded source transition;
3. affected DEC-021 carrier and DEC-022 ownership rows are explicitly retained
   or reopened;
4. Q-005 is resolved from the graph result and unchanged ecology need; and
5. Q-006 through Q-008 continue under the handoff's ordered procedure.

N31 does not discharge the P2-I3 topology, local ecology encounter,
calibration, lane controls, execution, or terminal interpretation.

### Gate effect

`P2-I3-DISCRIMINATOR-GATE` remains pending. I03 is intentionally paused at a
cross-project dependency, not invalidated and not scientifically negative.
Only completion and retention of the RCAE handoff package is authorized before
the workspace switches to graph-project N31 work.

### Reopening condition

Reconsider this handoff if the graph project rejects or indefinitely defers
N31; N31 closes without a return bundle usable by RCAE; a source-current
native primitive appears independently and is admitted through a new
transition; or the owner explicitly chooses an RCAE-constructed exploration
despite the unresolved native surface. Any such path receives a new decision
and does not erase the handoff history.

## 26. `P2-I3-DEC-024` — Coherence-only D0 priority

### Question

After admitting the coherence-only core theory and the LGRC substrate papers
explicitly, should N31 still begin by choosing among release attenuation,
conserved leakage, and relaxing susceptibility, or must it first test whether
ordinary `C/J_C` evolution already produces the bounded decay relation without
additional state?

### Trigger

Owner-directed evaluation of these theory and substrate sources:

```text
geometric-reflexive-coherence:core/2025-11-ReflexiveCoherence.md
geometric-reflexive-coherence:core/2025-11-RC-IdentityChoiceAbundance.md
geometric-reflexive-coherence:core/2025-11-Coherence.md
geometric-reflexive-coherence:investigations/2026-01-RC-Distance-v4.md
geometric-reflexive-coherence:substrates/2026-05-LGRC-9.md
geometric-reflexive-coherence:substrates/2026-05-LGRC9V3-Native-Packet-Loops.md
geometric-reflexive-coherence:substrates/2026-05-LGRC9V3-Causal-Pulse-Substrate-Surfaces.md
```

Their clean repository revision and exact file digests are retained in the
handoff's required-theory-and-substrate-authority table. This is a prospective
DEC-024 theory/substrate-source record, not the future committed RCAE
demand-source identity and not a rewrite of historical I02 admission.
The evaluation established a stricter ontology than the original three-way
Q-005 comparison:

- coherence is the only primitive dynamical field;
- the strict formulation makes `C(x,t)` the only dynamical variable and
  treats flux, geometry, graph, and memory as derived;
- slow/low-pass coherence modes may carry memory without a second field;
- a finite-window flux graph relation is derived but is not automatically a
  causal mediator of later transport;
- an independently causal susceptibility, release-age cursor, or other memory
  state is an effective closure or theory extension even if stored natively;
- LGRC requires operational causal order and exact node-plus-packet or
  equivalent pending-budget accounting while leaving final lifecycle laws
  open;
- validated native packet self-rearm is conserved causal handoff, not evidence
  of trail decay; and
- the proposed pulse-substrate history surface is specification precedent,
  not proof of native code or a relaxation primitive.

The existing Q-005 report had honestly classified slow `S_e` as constructed,
but it had not made the no-additional-state explanation a positive first
hypothesis.

### Considered paths

#### Option A — leave the three-way N31 handoff unchanged

This preserves the accepted document but biases N31 toward inventing or
selecting a decay state before testing the theory's own closed loop. A later
"no primitive" result would also conflate successful coherence-only decay with
failure to find any relation.

#### Option B — reject susceptibility and retain leakage as the sole candidate

This respects conservation but still assumes that decay requires an added
emission law. It also discards useful closure/extension evidence prematurely.

#### Option C — add D0 first and retain the three mechanisms as later paths

This tests the strongest theory-faithful explanation first while preserving
release attenuation as an expression boundary, leakage as the first native-
mechanics-aligned fallback, and susceptibility as a declared closure or
theory-extension candidate.

### Selected resolution

Select Option C.

N31 first tests:

```text
D0a — slow causal C/J_C organization weakens under ordinary evolution
D0b — a finite-window derived graph relation fades as an observable/closure
D0c — instantaneous current-derived geometry as the lower comparator
```

D0a may support a positive bounded coherence-only decay result. D0b alone is
below causal trail support unless later local transport actually consumes the
underlying coherence/flux relation. D0c alone is below durable decay.

Only after D0 is classified may N31 require or compare an additional release,
leakage, susceptibility, or newly exposed mechanism. An independently causal
`S_e` must be described as an effective LGRC closure or explicit theory
extension, not silently naturalized as coherence-only.

### State and cache boundary

N31 must distinguish:

```text
same complete spatial/spectral C plus laws and continuation
-> same coherence-only future

same complete C/J_C trajectory over a declared history functional
-> same derived history value
```

Node-coherence scalar equality is not complete-field equality. A cached
history value is derived only if it is exactly recomputable, cannot diverge,
and does not create independent continuation. A causally active history value
that is not fixed by current complete coherence state is at least an effective
non-Markovian closure.

### D0 redistribution, runtime state, and producer boundary

Conserved outward flux remains D0 when it follows entirely from the already
admitted ordinary `C/J_C` evolution and native LGRC event dynamics. Candidate
B begins only when N31 introduces a new route-field-specific emission
eligibility, amount, timing, destination, or lifecycle policy. The observation
that local coherence moved outward is insufficient to classify leakage.

`Coherence-only` does not reduce legitimate LGRC continuation state to node
scalars. Queues, in-flight coherence, event ordering, scheduler state, node
proper time, and frozen boundary/constitutive policies remain admitted. What
D0 excludes is additional route-memory, susceptibility, age, decay, or
causally independent history state.

A D0 producer may build fixtures, initiate formation through admitted native
operations, compute derived observations, request already admitted native
transitions, and collect receipts. It may not author a load-bearing
post-formation update, relaxation, future-affecting history cursor, D0-specific
decay schedule, retained-history conductance update, or causal diagnostic
feedback. Any such role makes the result a producer-mediated closure or
added-mechanism candidate.

### D0a representation gate

Before D0a executes, N31 must classify its claimed slow coherence organization
as:

```text
represented_natively
represented_by_exact_projection
represented_only_by_lossy_coarse_state
missing
```

An exact projection freezes its basis, decomposition/recomposition, overlap
policy, temporal support, intervention semantics, error bound, and independent
state status. Lossy or missing representation closes D0a at that boundary.
It must not be repaired by constructing a persistent `C_slow` scalar solely
to satisfy the controls. Unavailable D0a controls receive
`unavailable_missing_representation`, not an artificial approximation.

Cache recomputation and complete execution/artifact reconstruction are
separate statuses. Conditional return-manifest roles may be
`not_applicable_with_reason`; empty placeholder artifacts are not required.

### Source identity correction

The clean `geometric-reflexive-coherence` revision and seven file digests are
the theory/substrate-source identity. The RCAE demand-source identity is the
future clean RCAE commit containing this accepted amendment and its projected
documents. N31 must retain both identities without conflating them.

### Gate and evidence effect

- DEC-023 remains accepted: P2-I3 stays paused and N31 remains the selected
  cross-project step.
- Passed brief/source gates and I01/I02 artifacts remain unchanged.
- Q-005 remains unresolved.
- No P2-I3 implementation, conformance, calibration, execution, or scientific
  authority follows.
- The exact PyGRC source/callable/test freeze remains the executable-capability
  barrier; substrate-paper statements cannot promote an absent operation to
  native support.
- The Q-005 study, N31 handoff, lane checklist, and master directives receive
  a bounded prospective amendment before N31 begins.

### Reopening condition

Reopen this ordering only if exact N31 source analysis shows that the admitted
core theory does not govern LGRC9V3, that D0 cannot be operationalized even as
a classified missing-surface probe, or that a newly admitted theory explicitly
requires an additional primitive. Failure of current PyGRC representation
alone does not invalidate D0; it receives a distinct missing-surface result.

## 27. `P2-I3-DEC-025` — Bounded N31 return admission

### Question

Can RCAE admit N31's exact graph-side classifications and reusable provider
contracts when closeout reconstruction exposes incorrect installed PyGRC
distribution metadata, while preserving the rule that provider adoption and
positive ecology evidence must be generated afresh?

### Evidence inspected

The bounded return pass inspected:

- the graph `main` merge tree, N31 closeout commit, I11 source anchor, and the
  committed RCAE demand-source lineage;
- the exact N31 closeout, all eleven source-artifact-manifest entries, and
  their internal output digests;
- the B-R and C.2 reusable contracts, candidate disposition matrix,
  claim/debt register, and RCAE recommendation;
- the source-anchor `pyproject.toml` and installed reconstruction package
  identity; and
- a fresh I12 builder run in a temporary clone at the exact source anchor.

The retained closeout records `pygrc_version=0.0.0`, while the exact source
declares and installs `0.1`. All N31 builder checks pass under `0.1`. Five
return artifacts, including both provider contracts, reconstruct byte-exactly.
Only the source-authority record, top-level closeout, and trace differ, and
only in the version field or its dependent digests.

### Considered dispositions

#### Option A — reject the complete N31 return

This would treat inconsistent environment metadata as if it invalidated exact
provider semantics and controls. It is too strong because no scientific or
provider-contract byte differs.

#### Option B — silently regenerate N31 artifacts with version `0.1`

This would rewrite graph evidence from RCAE and destroy the exact historical
closeout identity. It is forbidden.

#### Option C — bounded admission with explicit metadata error

Admit the committed graph result and exact provider contracts, retain both
historical and reconstructed environment identities, enumerate every allowed
reconstruction difference, and prohibit provider selection or evidence
transfer in this transition.

### Accepted resolution

Select Option C. The exact machine authority is the
[N31 return-admission manifest](../contracts/p2-i3/i03-n31-return-admission.json),
its [validation result](../contracts/p2-i3/i03-n31-return-validation.json), and
the [interpretive report](../reports/P2-I3-N31-return-admission.md).

The project owner classifies the retained `pygrc_version=0.0.0` value as a
distribution-metadata error. The source has always declared `0.1`, the current
editable import resolves directly to the admitted graph source, protected
runtime code is unchanged across the admitted source/closeout boundary, and
both provider contracts reconstruct byte-exactly. The historical value and
its digest cascade remain retained rather than rewritten.

The transition admits:

- B-R conservative coherence redistribution at
  `DR5_producer_mediated`, with reusable semantics at
  `DR6_contract_only`; and
- C.2 exact packet-history-derived susceptibility at relation `DR2`,
  producer extension `DR5`, native constitutive surface `DR0`, and reusable
  semantics at `DR6_contract_only`.

Both remain `admitted_option_not_selected`. Their producer-mediated status is
valid graph evidence and is not a reason to prefer or reject either option.
Nativity remains implementation-ownership and claim-boundary metadata. P2-I3
must choose by ecology semantics, carrier, topology, encounter, controls, and
restoration adequacy.

The B-R+C.2 possibility is retained only as a new composition candidate. It
cannot inherit either individual DR5 result and requires separate attribution
and interference controls.

### Effect on existing decisions

- DEC-020 remains fixed: every executable route is LGRC9V3-based.
- DEC-021 is neither retained nor reopened by admission alone. B-R adds an
  explicit destination topology; C.2 makes a history-derived relational
  carrier load-bearing.
- DEC-022 is neither retained nor reopened until selection. The two contracts
  provide the exact ownership rows that the selected route must consume.
- DEC-023's return-bundle condition is satisfied.
- DEC-024's D0-first question is answered: native D0a organization reaches
  DR2, but ordinary autonomous weakening was not found in the tested domain.

### Gate and evidence effect

`P2-I3-N31-RETURN-GATE` has passed. It opens only the Q-005 semantic/provider
decision and its affected DEC-021/022 comparison. It does
not pass `P2-I3-DISCRIMINATOR-GATE`, authorize I03 conformance, admit N31
positive evidence as P2-I3 evidence, or open calibration, registration, or
execution.

### Reopening condition

Reopen the source transition if the admitted graph merge no longer contains
the exact closeout tree, any provider contract or source-manifest artifact
fails its exact identity, reconstruction differences exceed the frozen JSON
pointer envelope, or new graph evidence changes a load-bearing semantic or
ownership boundary. Do not reopen it merely because one option is
producer-mediated or later remains unselected.

## 28. `P2-I3-DEC-026` — Staged B-R and C.2 evaluation

### Question

Should Q-005 select one returned provider from graph evidence alone, or should
P2-I3 generate fresh ecology evidence for both B-R and C.2 and evaluate their
results together with the cost of their producer residue?

### Considered paths

1. Select B-R immediately because it is closer to the provisional
   node-coherence carrier.
2. Select C.2 immediately because it gives history a direct relational role.
3. Construct both simultaneously under one shared topology and implementation.
4. Evaluate B-R first and C.2 second under separate realization identities,
   then compare ecology evidence, producer burden, and naturalization debt.
5. Select neither provider without executing either.

Options 1 and 2 would turn N31's conditional graph result into premature
ecology selection. Option 3 would assume the topology equivalence already
rejected during the original Q-005 study and could hide which mechanism caused
the result. Option 5 remains a legitimate final outcome, but it would discard
the owner's requested opportunity to learn from both returned contracts.

### Accepted resolution

Select Option 4:

```text
P2-I3-BR
  B-R realization, conformance, calibration, registration, execution,
  controls, reconstruction, and branch interpretation

then

P2-I3-C2
  C.2 realization, conformance, calibration, registration, execution,
  controls, reconstruction, and branch interpretation

then

P2-I3-COMPARE
  ecology-result and producer-cost comparison
  -> retain B-R, retain C.2, retain both as alternatives,
     propose a separately governed composition, or select none
```

The order is developmental, not a ranking. B-R goes first because its
conservative redistribution semantics can initially retain node coherence as
the local source carrier while making its destination/reservoir topology and
producer-owned export lifecycle explicit. C.2 follows because it more deeply
reopens the carrier boundary: packet history becomes a load-bearing relational
surface and the producer applies the history functional, effective
conductance, and scheduling.

DEC-012's proportional one-realization default is explicitly widened for this
lane. N31 demonstrated that B-R and C.2 are distinct causal ontologies, and the
owner has requested evidence about both rather than a pre-evidence selection.
This is the demonstrated necessity and explicit owner authority DEC-012
requires for multiple full realization tracks.

### Independence and permitted reuse

B-R and C.2 MUST have separate:

- realization, topology, carrier, equation, and ownership identities;
- calibration and registration artifacts;
- execution activation and retained evidence;
- controls, reconstruction, branch interpretation, and producer-cost record;
- terminal branch disposition.

They MAY reuse evidence-neutral infrastructure:

- schemas, validators, runner interfaces, telemetry event shapes;
- common causal-obligation and claim-boundary vocabulary;
- reconstruction utilities and report templates; and
- the producer-cost ledger defined below.

No shared topology, field state, causal equation, runtime adapter, threshold,
or result may be presumed. Reuse requires demonstrated semantic equivalence;
code convenience is not evidence of equivalence.

### Common comparison envelope

Before B-R candidate work, freeze the common comparison questions without
freezing C.2's concrete design:

1. Does repeated costly activity create an attributable non-static route-local
   aftereffect?
2. Does that aftereffect causally change later local traversal under the
   registered controls?
3. What rung, stability/perturbation profile, failure class, and claim ceiling
   does the branch support?
4. Which topology, carrier, and history assumptions are load-bearing?
5. Which functions and state remain producer-owned, and what would native
   naturalization require?
6. What new controls and reconstruction obligations exist only because of the
   producer?

C.2's detailed design may learn from the completed B-R branch, but every
B-R-derived design input MUST be recorded prospectively before C.2 calibration.
The final comparison must label this as a sequential developmental comparison,
not a blind symmetric contest.

### Producer-cost ledger

Producer cost is a vector, not one scalar score or a pass/fail gate. Each
branch MUST retain at least:

- exact producer-owned operations and their place in the causal chain;
- producer-owned state, topology, schedules, and serialized continuation
  state;
- native calls versus producer decisions and runtime invocation counts;
- producer-specific controls, restoration checks, replay checks, and failure
  modes;
- normalized artifact/state footprint and supplementary runtime/resource
  measurements;
- implementation surface size as descriptive metadata, never as the primary
  scientific metric;
- naturalization debt and the explicit graph-side surfaces that would remove
  the producer residue; and
- producer-omission or neutralization evidence showing whether the claimed
  relation depends on that residue.

Every cost item MUST also distinguish:

```text
contract_required
  residue required by the admitted N31 provider contract

rcae_ecology_required
  additional producer work required by the L03 topology or local encounter

evidence_only
  harness, telemetry, control, and reconstruction work that observes or
  verifies the mechanism but does not produce it
```

This prevents experimental rigor from being miscounted as mechanism cost and
prevents RCAE-specific topology work from being attributed to the N31 contract.

A cheaper producer does not automatically win, and a stronger ecology result
does not erase producer debt. Scientific adequacy and producer burden remain
separate comparison axes.

### Effect on DEC-021 and DEC-022

- B-R reopens DEC-021 only enough to add an explicit destination/reservoir
  topology while retaining node coherence as the provisional local source
  carrier. It reopens DEC-022 to bind the exact B-R export eligibility,
  amount/cap, time, and destination producer residue.
- C.2 remains inactive during B-R. When its track opens, it reopens DEC-021
  under a new branch identity for a packet-history-derived relational carrier
  and reopens DEC-022 for history-functional application, effective-conductance
  insertion, and packet scheduling.
- Neither branch silently replaces the historical DEC-021/022 choice, and a
  later native implementation cannot silently replace retained producer code.

### Gate and evidence effect

Q-005 is resolved as a two-route candidate-family decision, not as provider
adoption or an L03 result. Only `P2-I3-BR` realization work may begin. C.2
construction, any B-R or C.2 candidate execution, the final comparison, and
the top-level `P2-I3-DISCRIMINATOR-GATE` remain separately gated.

Each track must traverse the existing I03–I11 obligations under route-scoped
identities. A branch closeout is branch evidence, not the lane terminal record.
The lane terminal may be authored only after both branch closeouts and the
comparison record exist, unless a later owner decision explicitly stops the
program with a classified bounded result.

### Reopening condition

Reopen DEC-026 if a provider contract cannot express the required L03 causal
chain, branch isolation proves impossible, the common producer-cost ledger
systematically favors one ontology, new graph evidence changes a provider's
load-bearing semantics, or the owner explicitly stops after a classified
branch outcome. Do not skip C.2 merely because B-R succeeds, or reject B-R
merely because its producer burden is higher, without such a recorded change.

## 29. `P2-I3-DEC-027` — B-R current-state/history mode

### Question

For the B-R branch, should later export and traversal depend on native node
coherence alone, on a complete current native-plus-policy state, on active
formation history, or on several full realization modes?

### Considered paths

1. **Native coherence only.** Treat carrier-node `C` as the entire
   continuation state.
2. **Current composite state plus one history discriminator.** Treat the
   complete native LGRC state and current export-policy closure as causal;
   retain formation history as audit lineage and test state sufficiency.
3. **Active history primary.** Make a formation-history functional a direct
   producer input.
4. **Multiple full B-R modes.** Execute current-state and active-history B-R
   campaigns independently.

Option 1 omits load-bearing packet, event, receipt, and policy state. Option 3
adds a history functional not required by conservative redistribution and
begins to overlap C.2's ontology. Option 4 is disproportionate before the
bounded discriminator shows that complete current state is insufficient.

### Accepted resolution

Select Option 2 under the branch-local identity:

```text
P2-I3-BR-Q008
  primary_mode = current_composite_state_carried
  mandatory_discriminator = complete_state_matched_formation_history
  active_history_primary = false
  multiple_full_B_R_modes = false
```

The complete continuation state includes at least:

- the full native LGRC9V3 restoration identity rather than one projected
  carrier value;
- all continuation-relevant node coherence, conductance, packet-ledger,
  pending-event, event-time, phase, and native scheduling state;
- the registered B-R export-policy identity;
- eligible and consumed lifecycle receipts;
- pending exports and their exact source, amount, time, destination, and
  lineage;
- route boundary, explicit reservoir, and later-probe continuation state; and
- every current input later admitted by Q-006 and Q-007.

Route mass and route organization are derived measurements, not separately
stored causal variables. Immutable audit lineage may differ between matched
arms only after validation proves that neither native runtime nor any producer
reads it.

### Mandatory discriminator

Construct two arms with:

```text
same complete continuation state at t*
+ different attributable formation histories
+ identical future lifecycle receipts and probe opportunity
-> compare future export and traversal trajectories
```

The formed arm is the only arm that may satisfy costly attributable formation.
A false-installed or differently formed arm may test state sufficiency but
cannot inherit the formation claim.

Interpret outcomes as follows:

- matching futures support current-composite-state sufficiency at the tested
  boundary;
- a difference caused by audit-only lineage exposes an invalid hidden-history
  read;
- a difference caused by an omitted packet, queue, phase, receipt, cursor, or
  schedule means the state match was incomplete;
- a difference after a verified complete match reopens Q-008 as a genuine
  active-history or missing-state result rather than automatically promoting
  B-R; and
- inability to construct the matched state is a classified realization or
  restoration limitation, not negative L03 evidence.

### Producer-cost effect

Current policy receipts and their consumed/pending state count as
`contract_required` or `rcae_ecology_required` producer state according to
their exact origin. Audit-only history and comparison harness work count as
`evidence_only`. A producer that reads the raw formation trajectory would
change the accepted mode and must reopen this decision.

### Gate and evidence effect

This resolves only the B-R instance of Q-008. It does not resolve B-R Q-006 or
Q-007, open B-R conformance, make the state-sufficiency outcome positive,
authorize calibration, or constrain the later C.2 instance of Q-008.

### Reopening condition

Reopen DEC-027 if Q-006 or Q-007 adds continuation-relevant state omitted
above; bounded conformance cannot restore the native-plus-policy identity; the
state-matched discriminator cannot be constructed; verified complete-state
matches diverge; or a producer must read formation history to implement B-R.

## 30. `P2-I3-DEC-028` — B-R conservative repeated-lifecycle law

### Question

What exact field equation, units, update order, receipt lifecycle, and
invariants resolve the B-R branch instance of Q-006 without destroying
coherence, importing C.2 history semantics, or treating one N31 export as a
completed ecology result?

### Consumed authority

This decision consumes the already accepted
[DEC-025 return admission](../contracts/p2-i3/i03-n31-return-admission.json)
rather than re-admitting or restating the complete N31 closeout identity. Its
selected semantic contract is the admitted B-R provider option:

```text
contract_id = n31_B_R_conserved_redistribution_contract_v2
contract_output_digest = 7b8d171835eccf70df8debc0732eed0704867e1d7893ef955415d6c105e20873
executed_graph_rung = DR5_producer_mediated
reusable_semantics_rung = DR6_contract_only
```

DEC-025 remains the sole authority for graph revision, contract file digest,
producer residue, naturalization debt, consumer controls, forbidden claims,
and the bounded distribution-metadata error. No N31 positive result transfers
into this branch.

### Considered laws

1. **Wall-clock attenuation or direct carrier decrement.** Rejected because it
   either introduces external time or destroys coherence without a destination.
2. **Release-efficacy attenuation.** Rejected for this branch because it is
   Candidate A semantics: later release changes while the field carrier need
   not weaken.
3. **Raw-history-derived weakening.** Rejected for B-R because it imports a
   C.2-like functional and contradicts DEC-027's audit-only formation history.
4. **One N31-style export only.** Semantically valid B-R, but insufficient for
   the P2-I3 demand for an evolving field with repeated lifecycle
   opportunities.
5. **Serialized conservative redistribution.** Formation conservatively moves
   coherence into the route carrier; distinct internal lifecycle receipts may
   later authorize bounded conservative exports to an isolated destination.

Select Option 5 for the B-R branch only.

### Registered roles and units

For each matched route `e`, register three distinct node roles:

```text
s_e  route-local formation source and physical deposition debit account
m_e  route-exclusive intermediate-node coherence carrier and export source
d_e  explicit isolated reservoir outside later traversal and readout
```

`s_e` belongs to the registered route support. Its debit makes deposition
physically costly in the native coherence account, but `s_e` is not thereby
the depositor's complete support, participant identity, ecological fitness,
or total budget. Those participant-role and cost mappings remain later
registration questions.

Only native node coherence `C` carries the B-R field. Coherence is the unit for
formation amount `p`, export amount `q`, carrier value, route mass, and route
contrast. At settled checkpoints define the analysis-only projections:

```text
F_e = C(m_e)
M_e = C(s_e) + C(m_e)
O_e = C(m_e) - C(s_e)
```

`F_e` is the carrier value. `M_e` and `O_e` separately expose mass and spatial
contrast; neither may be stored as a hidden causal variable or read by the
producer. In-flight packets are included in global conservation accounting
but the displayed `M_e`/`O_e` equations apply only at declared settled
checkpoints.

### Formation law

Each attributable formation event `j` requests a positive native transfer
`p_{e,j}` from `s_e` to `m_e`:

```text
s_e --p_{e,j}--> m_e
C(s_e)' = C(s_e) - p_{e,j}
C(m_e)' = C(m_e) + p_{e,j}

Delta M_e = 0
Delta O_e = 2 * p_{e,j}
```

LGRC9V3 performs source debit, packet creation, transport, and destination
credit. Each event has a distinct attributable receipt and settles before its
registered checkpoint. DEC-013's logical floor applies: at least two
attributable formation events are required, while exact amounts, count beyond
that floor, and event schedule remain for candidate-blind calibration and I06
registration.

### Export law

After registered formation stops and a complete checkpoint exists, an exact
eligible internal lifecycle receipt `k` may authorize at most one export from
`m_e` to `d_e`. For nonnegative policy values `q_cap` and `C_floor`, evaluate:

```text
E_{e,k} in {0, 1}

q_{e,k} = E_{e,k} * min(
  q_cap,
  max(0, C(m_e) - C_floor)
)
```

For every eligible receipt:

```text
0 <= q_{e,k} <= max(0, C(m_e) - C_floor)
```

If `C(m_e) <= C_floor`, then `q_{e,k}=0`. Every positive export satisfies
`C(m_e)' >= C_floor`. `C_floor` is an export floor, not a universal lower bound
on every admissible initial carrier state.

For `q_{e,k}>0`, the producer requests native transfer
`m_e --q_{e,k}--> d_e`. At the settled post-credit checkpoint:

```text
Delta M_e = -q_{e,k}
Delta O_e = -q_{e,k}

source debit = in-flight amount = destination credit = q_{e,k}
```

Global node-plus-packet coherence remains conserved. The B-R weakening is
local redistribution, never coherence destruction, autonomous native decay,
or organization transferred to the reservoir.

### Receipt states and serialized lifecycle

The lifecycle distinguishes four outcomes:

```text
eligible positive
  consume receipt; reserve q > 0; schedule native export

eligible zero
  consume receipt; create no packet; leave native state unchanged;
  advance the producer-policy cursor

ineligible or invalid
  consume nothing; leave complete composite state unchanged

duplicate consumed receipt
  refuse atomically; leave complete composite state unchanged
```

Every lifecycle receipt binds:

```text
route identity
sequence index
qualifying native event identity
exact predecessor composite identity
policy identity
source and destination identities
prior receipt-settlement status
```

At most one accepted-but-unsettled export may exist per route. Receipt
acceptance and `q` reservation form one atomic producer-policy transition; the
next receipt becomes eligible only after the prior native export and complete
checkpoint settle. A validation or scheduling refusal must restore the exact
predecessor native-plus-policy identity rather than leave a consumed receipt,
reservation, or partial packet.

The restorable producer-policy identity therefore includes the lifecycle
cursor, eligible and consumed receipt sets, pending reservation or scheduled
export, policy values, and source/destination binding. This specializes rather
than reopens DEC-027's complete-current-state contract. The producer still may
not read raw formation history.

### Update order and ownership

The registered causal order is:

```text
1.  attributable formation request
2.  native source debit
3.  native formation packet transport
4.  native carrier credit and settled checkpoint
5.  repeat formation through the logical floor
6.  stop formation and retain complete checkpoint
7.  receive next exact internal lifecycle receipt
8.  validate receipt and current composite identity
9.  read current C(m_e) and compute/reserve q from frozen policy
10. request native export when q > 0, or settle eligible zero
11. native carrier debit
12. native export packet transport
13. native reservoir credit
14. retain complete native-plus-policy checkpoint
15. admit the next lifecycle opportunity or later Q-007 traversal probe
```

LGRC9V3 owns coherence state, debit, packets and ledger, event progression,
transport, credit, and native restoration. RCAE owns lifecycle eligibility,
the internal event schedule, floor/cap policy, receipt serialization and
consumption, source/destination binding, request construction, and composite
policy restoration.

The producer may read only current `C(m_e)`, the exact current receipt, frozen
policy values, and frozen source/destination identity. It may not read raw
formation history, participant or route labels, global route rank, destination
state, future outcomes, semantic success labels, or wall-clock time. Time is
internal event and checkpoint order generated by the system.

### Invariants, controls, and reservoir isolation

Every later realization and conformance package must preserve:

- exact global node-plus-packet coherence conservation;
- source debit equals packet amount equals destination credit;
- the export floor and cap bounds above;
- separate route-mass and route-contrast reporting;
- producer omission yields zero export;
- eligible-zero, invalid, duplicate, and rejected-operation semantics above;
- complete native-plus-policy restoration and branch replay; and
- B-R producer-mediated attribution and its N31 forbidden-claim ceiling.

The matched route-mass-loss control must decrease `M_e` by the candidate's
matched amount while leaving `O_e` unchanged. Its semantic transform removes
equal coherence from `s_e` and `m_e` and accounts for the removed quantity at
an explicit isolated control destination:

```text
C(s_e)' = C(s_e) - q/2
C(m_e)' = C(m_e) - q/2
Delta M_e = -q
Delta O_e = 0
```

Both debited nodes must satisfy the registered `q/2` availability bound.
The exact admissible intervention operation and numeric amount freeze later,
but no control may destroy or hide coherence. Q-007 must require that this
matched mass loss does not reproduce the candidate traversal effect. It must
also carry forward the admitted N31 export-source `C(m_e)` clamp, destination
`C(d_e)` clamp, and atomic rejected-readout obligations. Q-006 defines their
dynamic inputs; it assigns no readout outcome.

The candidate reservoir `d_e` is excluded from the later route and readout and
must remain causally isolated from the lifecycle:

- no automatic or scheduled return packet;
- no outgoing registered path into either candidate route;
- no reservoir-dependent export eligibility, amount, route choice, or global
  producer decision;
- no reservoir-triggered topology, pressure, or scheduler effect that can
  feed back into the candidate conclusion; and
- destination-state clamps must leave export and later traversal conclusions
  unchanged once Q-007 supplies the encounter.

A role-preserving reservoir permutation may be added later as a registered
control, but is not made mandatory by this equation decision alone.

### Repetition and composition classification

Register at least two sequential lifecycle opportunities. One positive export
followed by an eligible zero at the floor is a valid multi-opportunity
lifecycle but not repeated positive export. Later evidence must distinguish:

```text
one positive plus one zero
  single_positive_withdrawal_plus_floor

two or more sequential positive exports
  repeated_event_indexed_weakening

additional eligible zeros after the floor
  terminal_floor_stability
```

Exact opportunity count beyond the logical minimum is deferred. This is an
RCAE repeated-lifecycle realization of the admitted B-R contract, not a
B-R+C.2 semantic composition and not inherited N31 DR5 evidence. At Q-006 it
is only the dynamic segment of a candidate ecology composition. The full L03
causal composition requires Q-007's local traversal encounter and fresh RCAE
execution:

```text
costly repeated formation
  -> route-local native carrier
  -> serialized conservative weakening
  -> later local traversal encounter
```

### Deferred numeric and observational choices

This decision freezes the equation family, coherence units, role topology,
event order, receipt state machine, ownership, and invariants. It does not
freeze:

- `C_floor`, `q_cap`, formation amounts, initial coherence, or exact times;
- event and opportunity counts beyond their logical minima;
- the later traversal request or primary response family;
- candidate-blind resolution, interpretation bands, or ladder placement;
- exact fixture, seeds, attempts, controls, or resource envelope; or
- a scientific, ecological, provider-selection, or naturalization result.

Those choices remain assigned to Q-007, I04 calibration, I06 registration, and
later gated iterations. Numeric thresholds remain interpretive guides whose
near, narrow, failed, and exceeded outcomes require developmental analysis;
they are not automatic accept/reject selectors.

### Gate and evidence effect

This resolves only the B-R instance of Q-006. It binds the exact B-R contract
and the affected DEC-021/022 carrier/topology/ownership projection. B-R Q-007
is now the next realization decision. B-R Q-008 remains resolved by DEC-027;
C.2 Q-006 through Q-008 remain inactive and independent until the B-R branch
closeout.

No conformance, candidate-blind calibration, registration, candidate
execution, control result, branch evidence, trail/stigmergic interpretation,
or lane result follows. `P2-I3-DISCRIMINATOR-GATE` remains pending.

### Reopening condition

Reopen DEC-028 if bounded conformance cannot serialize and restore the complete
lifecycle; an eligible export cannot use native conservative packet transfer;
the reservoir cannot be causally isolated; Q-007 requires producer access to
forbidden history, labels, global rank, or outcome state; the matched-mass
control cannot preserve contrast and conservation; a verified complete-state
match exposes omitted load-bearing state; or new graph evidence changes the
admitted B-R contract. A narrow or unexpected later scientific result does not
silently rewrite the law; it is interpreted through the registered ladders and
may motivate an explicit alternative campaign.

## 31. `P2-I3-DEC-029` — B-R paired local native-departure encounter

### Question

How does a fresh later B-R probe encounter route-local carrier state and
produce a substrate-visible continuation consequence without a runtime route
ranker, field-reading outcome producer, participant-label decision, or global
comparison?

### Considered encounter paths

1. **Global route choice.** Compare both carrier values and schedule work on
   the preferred route. Rejected as the exact hidden-router pattern Q-007 must
   exclude.
2. **Field-reading outcome producer.** Let RCAE read `C(m_e)` and emit an
   accepted/refused traversal result or field-conditioned request. Rejected as
   unnecessary outcome authorship for the B-R minimum.
3. **Field-to-participant support transfer.** Conservatively transfer carrier
   coherence into separate participant support before movement. Retained only
   as a possible later realization because the extra transfer can make support
   provisioning or budget circulation, rather than the route field, carry the
   result and redirect interpretation toward L04 or L06.
4. **Conductance or susceptibility modulation.** Retained for the later C.2
   branch or a separately governed alternative; it is not B-R's selected
   coherence-carried encounter.
5. **Paired branch-local native departure admission.** At one frozen local
   continuation opportunity per branch, schedule the same role-matched request
   from the carrier to its continuation node. The adapter never reads field
   state; LGRC9V3 alone admits or refuses native processing from local source
   coherence.

Select Option 5 for the B-R branch.

### Encounter topology

Add one matched continuation role `x_e` and one fixed continuation edge
`h_e=(m_e,x_e)` to each route:

```text
s_e -> m_e -> x_e
       |
       -> d_e
```

`m_e` remains DEC-028's sole field carrier and export source. `d_e` remains
the isolated B-R reservoir and is not on the continuation path. `x_e` is a
route-local continuation target, not field state, participant state, or a
result label. The two routes must have role-matched continuation topology,
edge properties, causal delay, initial state, and opportunity policy before
any field intervention.

Adding `x_e` specializes the anticipated Q-007 encounter topology. It does not
reopen DEC-028's field law, but `x_e`, `h_e`, their runtime state, and every
pending encounter request become continuation-relevant state under DEC-027.

### Local opportunity and fixed request

For each route `e` and probe branch `k`, preregister one immutable local
opportunity record:

```text
o_{e,k} = (
  role-preserving source binding m_e,
  continuation target x_e,
  continuation edge h_e,
  fixed q_probe,
  internal departure and arrival event positions,
  generic fresh-probe role,
  exact parent checkpoint identity
)
```

The exact numeric `q_probe`, event positions, edge values, and branch set are
deferred to candidate-blind calibration and I06. They must match across paired
route roles and freeze before candidate execution.

An RCAE blind request adapter validates the already frozen local opportunity
and invokes one native request:

```text
m_e --q_probe--> x_e
```

The adapter may read only the immutable opportunity record, its exact parent
checkpoint identity, and branch-local structural endpoint bindings. It may
not read:

- `C(m_e)`, `M_e`, `O_e`, the other route, or any derived field score;
- formation or lifecycle history;
- semantic route labels, participant identity, or preferred-route metadata;
- expected classification, candidate arm, or future outcome; or
- any global rank, comparison matrix, or wall-clock value.

Numeric source, target, and edge IDs are required by the public PyGRC call.
They are permitted only as prospectively frozen structural bindings. They may
not be chosen or changed as a function of field state or result.

### Native encounter relation

The fixed adapter authors a request, not its outcome. LGRC9V3 processing owns
the state-dependent boundary. Once all non-field validity conditions are
verified, retain the analysis-only signed local margin:

```text
mu_{e,k} = C(m_e) - q_probe
```

The native relation is:

```text
mu_{e,k} >= 0
  -> departure admitted; native debit, packet transport, and x_e credit

mu_{e,k} < 0
  -> native insufficient-source-coherence refusal
```

`mu` is measured from retained state and request facts. Neither the request
adapter nor any runtime producer may consume it. Equality belongs to native
admission because source coherence is rejected only when it is smaller than
the requested amount.

An admitted row must close:

```text
C(m_e) debit = in-flight amount = C(x_e) credit = q_probe
global node-plus-packet coherence change = 0
```

This is a local continuation-admission response. It is not a native route
choice, embodied participant trajectory, preference, or abstract organization
mediator.

### Paired branch factorization

No runtime invocation may offer both routes to a selector. Starting from one
verified matched complete checkpoint, create independent counterfactual probe
branches:

```text
branch A
  -> invoke only o_A with the frozen role-matched request

branch B
  -> invoke only o_B with the frozen role-matched request
```

The branch plan is frozen before field values or outcomes are consumed. A
later analysis may compare the retained branch results; that comparison is
not runtime causal input. Scheduling both requests in one shared queue is not
the primary encounter because queue order and shared continuation state could
create an unregistered interaction.

Accepted probes debit the carrier and are therefore invasive. Each probe is
terminal within its scientific branch. A delayed or repeated probe must fork
from a clean, unprobed checkpoint with its own registered opportunity rather
than continue after an earlier readout changed the carrier.

### Outcome typing and atomic refusal

Retain three distinct terminal encounter states:

```text
admitted
  native departure and arrival complete with exact conservation

field_limited_refusal
  exact native insufficient-source-coherence refusal after every other
  request and state condition validates

invalid_or_infrastructure_failure
  malformed endpoint, unexpected exception, queue/restoration mismatch,
  missing runtime, or other non-scientific failure
```

Only the exact insufficient-source-coherence condition is a valid field-
limited refusal. Other failures cannot be counted as a scientific negative or
silently mapped to `admitted=false`.

For a field-limited refusal, the complete native identity after the attempted
processing step must equal the pre-step identity that already contains the
scheduled request, including queue, packet ledger, clocks, checkpoint,
scheduler index, node coherence, budget, topology, and restoration digest.
The probe branch then terminates. Replay from the same clean parent checkpoint
must reproduce the disposition and state projection exactly.

The immutable branch/attempt ledger is evidence-only orchestration, not a
hidden producer cursor or causal field. Duplicate execution within one branch
is invalid; duplicate replay uses a fresh branch from the same parent identity.

### Required causal and hidden-router controls

Q-007 carries the following design obligations into conformance,
calibration, registration, and execution without assigning their outcomes:

1. **Lifecycle intervention.** B-R export changes `C(m_e)` and therefore may
   change native encounter margin or admission under the frozen request.
2. **Export-source clamp.** A registered `C(m_e)` clamp must reverse the
   encounter relation where its frozen intervention predicts reversal.
3. **Reservoir clamp.** Changing `C(d_e)` must not alter request construction,
   native encounter disposition, or continuation outcome.
4. **Matched mass loss.** DEC-028's same-`Delta M`, zero-`Delta O` control must
   not reproduce the candidate traversal effect required by the admitted B-R
   contract. Its actual outcome remains scientific evidence.
5. **Complete-state-matched history.** DEC-027's different formation histories
   must produce matching future encounter trajectories when complete current
   state is truly equal.
6. **Current-state relocation.** Moving the complete registered carrier and
   continuation state between matched route roles must move the encounter
   relation with that state rather than with a route label.
7. **Role and raw-ID permutation.** A role-preserving node/edge permutation
   must yield the correspondingly permuted request and outcome.
8. **Fixed-route exclusion.** Every retained route receives its own
   prospectively frozen local branch; no adapter may select which route to
   invoke after inspecting state.
9. **Atomic refusal and replay.** Every field-limited refusal is native-state
   neutral at the exact pre-step boundary and every retained branch replays.
10. **No-export and producer-omission controls.** Static/no-export and omitted
    B-R lifecycle branches remain distinct from encounter-adapter omission.

The matched-mass control can change `C(m_e)` while preserving `O_e`; therefore
its result must be interpreted at the registered margin rather than presumed
from its label. B-R's inherited evidence ceiling remains bounded partial
mediation by local source `C(m_e)`, not full route-distribution or abstract
organization mediation.

### Participant and interpretation boundary

The probe manifest may identify a fresh eligible probe episode, but participant
identity is audit and eligibility provenance only. It cannot affect endpoint,
request amount, timing, or outcome. The core may use the same participant in a
later episode or a different matched participant; only the latter can support
the stronger `stigmergic_field_candidate` interpretation after its own role
controls pass.

The maximum Q-007 operational meaning is:

> bounded route-local continuation admissibility conditioned by current
> carrier coherence after an evolving B-R lifecycle.

It does not establish embodied movement, free route choice, preference,
planning, learning, communication, or persistent participant identity. A
participant-coupled support-transfer or field-conditioned producer remains a
separately governed alternative if this bounded readout later proves too weak;
it cannot silently replace the retained branch.

### Interpretation is not a binary gate

Native processing is binary, but the scientific result is not. Later metric
and ladder design must separately classify at least:

```text
robust admission split
graded margin movement without a binary split
narrow or boundary-sensitive split
no encounter-relevant movement
matched-mass reproduction
state/history divergence
invalid, censored, or resolution-limited encounter
```

Candidate-blind calibration and Q-009 decide the primary response projection,
resolution bands, and exact margin treatment. A same-side margin movement is
not automatically failure; a narrow split is not automatically strong
evidence; and values may not be retuned after candidate outcomes merely to
create a binary difference.

### Producer-cost and naturalization effect

The local opportunity manifest, structural binding guard, and blind request
adapter are `rcae_ecology_required` producer work. Native source-coherence
admission, debit, transport, arrival, and refusal remain LGRC9V3-owned.
Branch comparison, margin calculation, telemetry, and replay harnesses are
`evidence_only`. None is added to N31's `contract_required` export residue.

The specialized naturalization debt is a native local-opportunity interface
that can bind a carrier-local continuation without experiment-owned numeric
addresses while preserving the same no-ranking and restoration boundaries.
The retained RCAE adapter is not silently replaced if such an interface later
appears.

### Gate and evidence effect

This resolves only the B-R instance of Q-007. Together, DEC-027 through
DEC-029 fix the B-R Q-008 mode, Q-006 lifecycle law, and Q-007 encounter
factorization. The common comparison envelope, Q-013 comparison identities,
the design portion of Q-015 restoration, operational hypotheses, and bounded
conformance still remain before `P2-I3-DISCRIMINATOR-GATE` can pass.

No `q_probe`, fixture, calibration value, primary metric, threshold, seed,
attempt, registration, conformance result, candidate execution, control
outcome, trail/stigmergic interpretation, branch result, or lane result is
assigned.

### Reopening condition

Reopen DEC-029 if bounded conformance shows that a fixed local request cannot
be generated and restored without field-reading or route-selecting producer
logic; native refusal is not atomic at the registered boundary; paired branches
cannot exclude queue or shared-state interference; the request topology makes
the reservoir causal; the local departure readout cannot support even bounded
continuation-admissibility meaning; Q-013/Q-015 exposes omitted load-bearing
state; or new graph evidence changes the admitted B-R readout contract. A
narrow, same-side, or contrary candidate outcome is interpreted under the
frozen ladder and does not silently rewrite this decision.

## 32. `P2-I3-DEC-030` — Common branch-comparison envelope

### Question

Which common result and producer-cost fields can compare the sequential B-R
and C.2 branches without forcing distinct mechanisms into one realization,
making raw magnitudes falsely commensurable, or computing an automatic winner?

### Considered comparison forms

1. **One shared implementation and metric.** Rejected because DEC-026 requires
   separate topology, carrier, equation, calibration, registration, execution,
   and evidence identities unless equivalence is demonstrated.
2. **One scalar benefit-minus-cost score.** Rejected because it would collapse
   scientific adequacy, producer dependence, naturalization debt, and
   evidence-only rigor into discretionary weights.
3. **Narrative comparison after both results.** Rejected because outcome-aware
   selection of comparison criteria would defeat the pre-B-R freeze.
4. **Raw side-by-side artifacts only.** Retained as necessary evidence but
   insufficient: unlike structures would remain difficult to compare and the
   sequential C.2 learning boundary would be implicit.
5. **Prospective semantic envelope plus unsummed producer-cost vector.** Each
   branch answers the same ecology questions and R01-R05 ladder while keeping
   its own mechanism, metric, and numeric scale. Producer residue is classified
   by causal role, and all B-R-derived C.2 inputs are recorded prospectively.

Select Option 5.

### Proposed scientific envelope

Every branch closeout must answer eight common questions:

1. Did at least two attributable costly events form the route-local
   aftereffect?
2. Did a registered non-static dynamic occur beyond static persistence?
3. Did a later local opportunity encounter it without hidden selection,
   label reading, or outcome-writing production?
4. Did intervention on the dynamic or its mediator change continuation?
5. Did withdrawal, shuffle or relocation, false-trace, and no-field controls
   establish mechanism specificity?
6. Was continuation carried by complete current state, active history, or an
   honestly unresolved distinction?
7. How stable, perturbation-sensitive, narrow, transferable, or regime-limited
   was the relation?
8. What R01-R05 rung, claim ceiling, developmental value, and next move are
   justified?

The questions are mandatory; positive answers are not. Valid static-trace,
generic-quantity, narrow, counter-directional, unresolved, producer-dependent,
missing-surface, redirective, or non-selection results remain visible.
Infrastructure failure remains separate from scientific evidence.

Each branch retains its own primary response, comparator, resolution band,
and raw effect magnitude. Cross-branch numeric comparison is prohibited unless
a later prospective record demonstrates equivalent response meaning, units,
timing, comparator, aggregation, missingness, and calibration population.
Common normalization alone is not semantic equivalence.

Thresholds remain interpretive reference bands, not universal pass/fail gates.
The comparison preserves per-seed or per-attempt relations, controls,
perturbations, unexpected properties, and developmental readings.

### Proposed producer-cost envelope

Every producer item receives exactly one role class:

```text
contract_required
rcae_ecology_required
evidence_only
```

Classification precedence is provider-contract duty first, additional
ecology-composition duty second, and non-causal evidence work third. Reuse does
not duplicate one item across cost classes.

Within those classes, each branch reports six unsummed dimensions:

1. causal operations, ownership, chain position, and registered invocation
   counts;
2. causal state, topology, schedules, lifecycle, and serialization;
3. producer-specific controls, failure surfaces, omission dependence, and
   atomicity/refusal guards;
4. restoration, cross-load protection, replay, and reconstruction burden;
5. descriptive implementation, state/artifact, runtime, memory, disk, and
   process footprint; and
6. naturalization debt and the exact graph-side surface that would remove it.

Counts, source lines, bytes, or runtime measurements are descriptive and may
not be summed into a winner. Evidence-only work is not causal mechanism cost;
contract-required and RCAE-ecology-required residue remain separate. Missing
native coverage is debt rather than automatic scientific failure, while a
strong scientific result cannot erase producer dependence.

### Sequential-development boundary

Before C.2 calibration, retain one prospective influence-register entry for
every B-R result, artifact, or observation used in C.2 design:

```text
source B-R input
-> adopted / rejected / not applicable
-> prospective C.2 design effect and reason
-> comparison or independence consequence
```

The register permits learning. It prohibits importing B-R candidate values as
C.2 calibration, retuning C.2 to outperform B-R, claiming a blind symmetric
contest, or silently reusing B-R topology, carrier, equation, adapter, or
threshold.

### Q-021 and gate effect

The final Q-021 disposition remains one of: retain B-R, retain C.2, retain both
as alternatives, propose a separately governed composition, retain another
justified route, or select none. No envelope field computes that decision.

DEC-030 freezes comparison semantics and the producer-cost ledger before B-R
candidate work. It does not accept the B-R realization, resolve
Q-013 or Q-015, select a metric or numeric value, authorize conformance or
calibration, or assign any branch/provider/lane result.

The complete accepted projection is retained in the
[machine envelope](../contracts/p2-i3/i03-common-comparison-envelope.json) and
[interpretive report](../reports/P2-I3-I03-common-comparison-envelope.md).

### Reopening condition

Reopen DEC-030 if the common axes systematically privilege one provider
ontology rather than L03's causal question; a branch cannot be represented
without erasing its mechanism; cross-branch numeric comparison becomes
necessary and prospective semantic equivalence can be shown; the cost classes
mix evidence rigor with causal residue; C.2 cannot preserve prospective B-R
input provenance; or new graph evidence changes a provider contract.

A weak, narrow, surprising, or negative branch outcome is interpreted inside
the envelope and does not itself reopen it.

## 33. `P2-I3-DEC-031` — B-R Q-013 contrast identities

### Question

Which separate stable identities bind B-R quantity-matched and complete-state-
matched contrasts without conflating temporal formation, route-mass loss, and
history sufficiency?

### Accepted resolution

DEC-028 introduced a second quantity relation beyond the brief's original
repeated-formation versus one-pulse comparison. A generic `quantity_matched`
identity would now be ambiguous. Register three non-substitutable contrasts:

```text
P2-I3-BR-Q13-FORMATION-QUANTITY-MATCH-001
  equal total formation transfer, debit, and cost
  repeated attributable formation versus one formation pulse
  complete current state is not required equal

P2-I3-BR-Q13-EXPORT-MASS-MATCH-001
  candidate and control both have Delta M = -q
  candidate has Delta O = -q
  control removes q/2 from s_e and q/2 from m_e, so Delta O = 0

P2-I3-BR-Q13-COMPLETE-STATE-HISTORY-MATCH-001
  equal complete causal continuation state at t*
  different attributable formation histories
  identical future receipts, schedule, opportunity, and probe inputs
```

The formation-quantity contrast tests temporal structure versus accumulated
quantity. The export-mass contrast tests organization loss versus generic mass
loss. The complete-state/history contrast tests current-state sufficiency
versus active history or omitted causal state. None may substitute for another.

Only a validly formed arm can satisfy costly attributable formation. Matching
future trajectories after a verified state match support state sufficiency at
the tested boundary; divergence from an omitted state component invalidates
the match; verified divergence reopens active history or missing state without
automatically supporting B-R.

Relocation, false trace, clamp, withdrawal, and hidden-router controls retain
separate identities. I03 owns contrast meaning and IDs; I04 owns response and
comparator binding; I06 owns exact values, operations, timing, and topology.

### Gate and evidence effect

This resolves B-R Q-013 only. It assigns no response, metric, amount, control
outcome, conformance result, calibration, execution, or L03 evidence.

### Reopening condition

Reopen DEC-031 if one contrast cannot be constructed without collapsing into
another; exact B-R mechanics expose another load-bearing matching relation; or
I04/I06 cannot preserve the three meanings under separate identities.

## 34. `P2-I3-DEC-032` — B-R Q-015 restoration and continuation design

### Question

What complete restoration, reset, branch, and equal-input continuation design
is required for B-R, especially when different-history arms cannot be byte-
identical yet must have equal causal continuation state?

### Accepted resolution

Use one manifest-coordinated composite restoration interface with two distinct
identity layers:

```text
P2-I3-BR-Q15-EXACT-COMPOSITE-RESTORATION-001
  exact native + RCAE + branch + audit execution identity

P2-I3-BR-Q15-CAUSAL-CONTINUATION-PROJECTION-001
  every field capable of changing registered continuation
  excluding only prospectively validated audit-only fields
```

The exact identity includes full native LGRC9V3 restoration state, topology,
roles, coherence/conductance, packet/event/scheduler/time/budget state, B-R
policy and lifecycle receipts, reservations and pending work, source/carrier/
reservoir/continuation bindings, encounter opportunity and parent checkpoint,
intervention identity, participant audit provenance, distance-policy inputs,
reset baselines, and audit lineage.

Different-history arms restore exactly to themselves and may retain different
exact execution identities. Their causal continuation projections must match
before identical future native inputs, lifecycle receipts, probe opportunity,
request, interventions, and observation calls are applied. Projection equality
is necessary but cannot replace bounded equal-input continuation.

Load returns one fully validated composite or fails closed before scientific
continuation. Missing, partial, stale, one-sided, cross-route, cross-policy,
cross-branch, or mismatched components are invalid. Reset restores native and
RCAE baselines together and cannot silently rebase. Each scientific branch
forks from a clean validated parent; an admitted Q-007 probe is invasive and
terminal, so delayed or repeated probes require fresh unprobed forks.

Equal-input continuation must later compare original/load, initial/reset,
each history arm restored to itself, paired state-matched histories, and
atomic-refusal replay. For field-limited refusal, the post-attempt native
identity must equal the pre-step identity that already contains the scheduled
request.

The accepted machine and narrative projection is retained in the
[B-R contrast/restoration design](../contracts/p2-i3/i03-br-contrast-and-restoration-design.json)
and its [report](../reports/P2-I3-I03-BR-contrast-and-restoration-design.md).

### Gate and evidence effect

This resolves only the I03 design portion of B-R Q-015. I06 still owns exact
component schemas and hashes, topology values, commands, reset values,
continuation horizon, output-specific equality/tolerance rules, branch counts,
and runtime binding. No conformance, calibration, execution, or result follows.

### Reopening condition

Reopen DEC-032 if a continuation-relevant component is absent; an audit-only
field must become causal; complete save/load/reset cannot fail closed;
conformance finds unequal continuation after verified restoration; native
refusal cannot replay atomically; or new graph evidence changes the admitted
restoration or B-R provider boundary.

## 35. `P2-I3-DEC-033` — B-R operational-hypothesis projection

### Question

Does the B-R operational projection faithfully specialize `AE01-H-L03`, the
post-R3 non-static-dynamic discriminator, and DEC-027 through DEC-032 without
selecting a metric, numeric direction, control outcome, or result?

### Considered projection granularity

1. **One monolithic B-R statement.** Rejected because formation, field
   dynamics, local encounter, causal mediation, and controls could not fail or
   redirect independently.
2. **Mechanism steps only.** Rejected because quantity/history specificity,
   restoration, hidden-router exclusion, variation, and interpretation would
   remain implicit.
3. **One hypothesis per matrix cell.** Rejected as premature because I04 and
   I06 still own the exact finite matrix and numeric registration.
4. **Thirteen semantic operational hypotheses.** Project the causal chain,
   three Q-013 contrasts, restoration-aware state/history, required control
   meanings, R05 variation, and interpretation tags while leaving every exact
   value and outcome open.

Select Option 4.

### Accepted projection

```text
OP-01  costly attributable repeated formation
OP-02  route-local persistent carrier
OP-03  conservative non-static export lifecycle
OP-04  fixed local native encounter
OP-05  dynamic-to-encounter causal mediation
OP-06  formation-quantity temporal discriminator
OP-07  export-mass organization discriminator
OP-08  complete-state/history discriminator
OP-09  field locality, relocation, and permutation
OP-10  withdrawal, false trace, and producer dependence
OP-11  hidden-router and participant exclusion
OP-12  geometry or internal-timescale variation
OP-13  trail versus stigmergic interpretation boundary
```

The projection maps OP-01 to R01, OP-02 through OP-03 to R02, OP-03 through
OP-05 to R03, OP-06 through OP-11 to the branch-specific R04 specificity
package, and OP-12 to R05. OP-13 supplies bounded interpretation tags and adds
no rung. The overlap preserves the frozen R02 meaning: persistence plus the
selected decaying or reinforced dynamic precedes its later route function.

A positive B-R non-static-dynamic interpretation requires at least one
positive conservative export after the repetition floor. An eligible-zero
policy transition with no carrier change remains a valid lifecycle observation
but does not by itself satisfy the dynamic-beyond-persistence boundary.
Repeated positive export is not required: one positive export followed by
eligible-zero floor stability remains addressable under DEC-028.

Direction, magnitude, binary split, perturbation strength, state-sufficiency
outcome, interpretation tag, and terminal class remain open. Same-side, narrow,
generic-mass, static, producer-dependent, missing-surface, redirective, and
negative results are retained rather than forced into acceptance/rejection.

The exact machine and narrative projection is retained in the
[operational-hypothesis contract](../contracts/p2-i3/i03-br-operational-hypotheses.json)
and [subordinate hypothesis record](../hypotheses/p2-i3-br-operational-hypotheses.md).

### Gate and evidence effect

DEC-033 freezes the B-R operational meanings and opens only
construction of a bounded, scientifically quarantined conformance freeze. It
does not run conformance, pass `P2-I3-DISCRIMINATOR-GATE`, select I04 metrics,
authorize calibration or execution, or assign any control or scientific
outcome.

### Reopening condition

Reopen DEC-033 if an OP cannot be addressed without changing DEC-027 through
DEC-032; the projection implicitly chooses an I04 metric or numeric direction;
the controls cannot distinguish the causal relation; bounded conformance finds
omitted state, operation, refusal, restoration, or hidden selection; B-R cannot
represent the parent ecology discriminator; or new graph evidence changes the
provider contract.

## 36. `P2-I3-DEC-034` — Inactive bounded-conformance input freeze

### Question

Which exact inactive input freeze can test whether the accepted B-R operation
chain is expressible without turning a synthetic fixture into calibration,
registration, control, or scientific evidence?

### Accepted resolution

Freeze one deterministic two-route LGRC9V3 fixture with eleven conformance
cells. Bind the clean merged N31 graph revision, the unchanged I02-admitted
PyGRC provider sources, eighteen exact public symbols, locally resolved PyGRC,
one attempt, zero retries, and no network or external-repository writes.

The fixture exposes two native formation events, a positive B-R export followed
by eligible zero, an admitted and refused fixed encounter, all four lifecycle
states, all three Q-013 constructor identities, composite save/load/reset/
fork/replay, cross-bound refusal, control/variation addressability, forbidden-
read exclusion, and downstream quarantine. Fixture values deliberately span
both native encounter paths but are result-neutral and ineligible downstream.

RCAE owns only the serialized export policy, blind structural request adapter,
composite restoration coordination, and quarantine guard. LGRC9V3 owns every
coherence and packet transition plus native admission/refusal. The export
policy receives one declared carrier value rather than a model/global-state
object; the encounter adapter receives no field value.

The exact proposed freeze, zero-runtime validator, quarantine module, and
interpretive record are:

- [machine input freeze](../contracts/p2-i3/i03-br-bounded-conformance-input-freeze.json);
- [zero-runtime validator](../scripts/p2_i3_i03_br_freeze_validate.py);
- [quarantine guard](../scripts/p2_i3_conformance_quarantine.py); and
- [freeze report](../reports/P2-I3-I03-BR-bounded-conformance-input-freeze.md).

The validator passes 85 checks while constructing no model and producing no
conformance output. Quarantine is mechanical for declared provenance, paths,
kinds, digests, and fixture value identities; it does not claim to recognize
an unattributed copied number.

The owner explicitly retains the recurring evidence-responsive development
rule: results may motivate a stronger topology, narrower producer, more native
realization, or more discriminating structure later. Such work receives new
realization/freeze/execution/artifact identities, preserves this structure and
result as history, and reruns every affected comparison. It may not tune this
fixture retrospectively or claim that the stronger structure already ran.

### Gate and evidence effect

DEC-034 authorizes construction of the exact source-bound runtime module and
harness followed by the one bounded conformance run after this accepted freeze
is committed as a clean source anchor. It does not
pass the discriminator gate, open I04, or assign any OP/control/scientific
outcome.

### Reopening condition

Reopen DEC-034 if a public call is unavailable; the producer needs a forbidden
input or direct native mutation; the encounter needs a field read or selector;
a Q-013 interface is conflated; composite restoration or atomic refusal cannot
be expressed; quarantine does not reject declared conformance provenance; or
new graph evidence changes the admitted provider boundary.

## 37. `P2-I3-DEC-035` — Accept B-R operational conformance

### Question

Does the retained B-R package establish the accepted realization's operational
adequacy strongly enough to pass `P2-I3-DISCRIMINATOR-GATE`, and which wording
and evidence boundaries must govern that acceptance?

### Alternatives considered

1. reject the package and reopen the realization;
2. require a second conformance run or stronger fixture before gate passage;
3. accept the runtime result without correcting ownership and section 8.2
   wording; or
4. accept the exact package, correct the two ledger meanings without rerun, and
   preserve all scientific questions for later gates.

### Accepted resolution

Accept alternative 4. At the exact retained RCAE and PyGRC identities, the
producer-mediated B-R realization is operationally expressible. Repeated native
formation, serialized conservative export, fixed local encounter, native
admission/refusal, composite restoration, control addressability, and
conformance quarantine compose without an RCAE producer reading or authoring
the later native disposition.

Correct the ownership statement as follows: RCAE owns lifecycle eligibility
and the request schedule; PyGRC owns native ordering, admission, progression,
refusal, and settlement of each scheduled native operation. RCAE causally
constructs the export opportunity and weakened-carrier condition but does not
manufacture the later result through an outcome-aware encounter selector.

Close all fifteen section 8.2 requirements at I03 through their individually
typed bases: bounded runtime conformance, constructor/interface addressability,
accepted design, explicit nonclaim/non-applicability, restoration evidence, or
source/provider binding. Do not describe them as one empirical proof. In
particular, active history is not claimed; fresh/direct address is only
representable; false-trace and no-field are only addressable; and no scientific
control or OP-13 interpretation has passed.

Retain the complete review, exact source/artifact identities, crosswalk,
reconstruction evidence, and downstream prohibition in the
[I03 operational-conformance review](../reports/P2-I3-I03-BR-operational-conformance-review.md).
No runtime artifact changes and no rerun are required.

### Gate and evidence effect

`P2-I3-DISCRIMINATOR-GATE` passes. This opens only I04 candidate-blind
calibration preregistration. Calibration execution, I06 registration,
candidate/control execution, C.2 work, every OP and R01–R05 disposition,
`AE01-H-L03`, provider comparison, and all scientific or lane results remain
unassigned or unauthorized.

Only the statement that the accepted I03 B-R conformance gate passed may be
consumed downstream. Fixture values, topology, admission/refusal split,
artifact digest, and derived margins are prohibited I04/I06 inputs.

### Reopening condition

Reopen DEC-035 if an exact source or artifact identity fails reconstruction; a
producer needs a forbidden read or authors the native response; composite
restoration is incomplete or not fail-closed; the admitted source/provider
identity changes; quarantine admits conformance provenance downstream; or
later work demonstrates that an operational interface cannot support its
registered scientific role.

## 38. Open decision register

These questions are intentionally unresolved. Their order is part of the
governance contract; answers cannot be taken from candidate outcomes.

| Question ID | Question | Earliest decision point | Blocking effect |
| --- | --- | --- | --- |
| `P2-I3-Q-001` | What exact read-only capability-audit scope examines route-local field, timing, distance, packet, route, intervention, and restoration surfaces? | I01 input freeze | Resolved by `P2-I3-DEC-016`; no longer blocks audit |
| `P2-I3-Q-002` | Which exact theory and graph revisions, files, public callables, and evidence roles are admitted? | I02 source admission | Resolved by `P2-I3-DEC-019`; no longer blocks I03 |
| `P2-I3-Q-003` | Is the field carrier edge-, node-, corridor-, or another route-local surface? | I03 realization selection | Resolved by `P2-I3-DEC-021`; alternative campaigns remain permitted under new identities |
| `P2-I3-Q-004` | Is each required function native, minimally producer-assisted, constructed, unsuitable, or missing? | I03 after I01/I02 | Resolved by `P2-I3-DEC-022`; conformance may reopen affected rows |
| `P2-I3-Q-005` | Which non-static dynamic carries the minimum candidate? | I03 realization freeze after N31 return | Resolved by DEC-026 as separate B-R-first and C.2-second candidate tracks; no final provider is selected |
| `P2-I3-Q-006` | What exact field equation/update law, units, update order, and invariants apply? | Route-scoped I03 realization freeze | B-R instance resolved by DEC-028 as serialized conservative B-R redistribution; C.2 instance remains inactive until B-R branch closeout |
| `P2-I3-Q-007` | How does traversal encounter the local field without a hidden global selector? | Route-scoped I03 causal factorization | B-R instance resolved by DEC-029 as paired branch-local fixed native departure admission; C.2 remains inactive and independent |
| `P2-I3-Q-008` | Is current field state sufficient, is active history load-bearing, or must multiple modes remain? | Route-scoped I03 discriminator freeze | B-R instance resolved by DEC-027 as current-composite-state primary plus mandatory history discriminator; C.2 instance remains open and inactive |
| `P2-I3-Q-009` | What primary substrate-visible traversal response is measured? | I04 calibration preregistration | Blocks CAL-PRE |
| `P2-I3-Q-010` | Which of the five surfaces are measured, annotation-only, inapplicable, or unavailable, and which policies derive them? | I04 | Blocks CAL-PRE |
| `P2-I3-Q-011` | What comparator and estimator preserve the dynamic-to-traversal causal question? | I04 | Blocks CAL-PRE |
| `P2-I3-Q-012` | What candidate-blind matched-null generator and inputs calibrate resolution without consuming candidate structure? | I04 | Blocks calibration |
| `P2-I3-Q-013` | Which separate IDs bind quantity-matched and complete-state-matched contrasts? | I03/I04 | B-R resolved by DEC-031 as three distinct contrast identities; C.2 remains inactive and independent |
| `P2-I3-Q-014` | What exact topology, field values, costs, schedules, times, seeds, and transfer contrast are registered? | I06 after calibration | Blocks REG-GATE |
| `P2-I3-Q-015` | What complete restoration, reset, branch, and equal-input continuation identity is required? | I03 design; finalized I06 | B-R I03 design resolved by DEC-032; exact I06 finalization remains open and blocks REG-GATE |
| `P2-I3-Q-016` | Which common controls apply and what evidence must resolve every lane-specific control? | I04/I06 | Blocks REG-GATE and CONTROL-GATE |
| `P2-I3-Q-017` | What time, memory, disk, process, and artifact-size envelope applies? | I06 | Blocks REG-GATE |
| `P2-I3-Q-018` | What finite attempts, infrastructure-only retries, failure classes, and one-shot claims apply? | I06/I07 | Blocks EXEC-FREEZE |
| `P2-I3-Q-019` | Which clean committed sources, commands, runtime identities, and activation record authorize the candidate cycle? | I07 | Blocks candidate execution |
| `P2-I3-Q-020` | Does any appendix activate after core closeout, and under what separate hypothesis? | Post-core decision only | No core blocker; appendix remains closed |
| `P2-I3-Q-021` | After both branch closeouts, which provider, alternative set, composition proposal, or non-selection should the lane retain? | P2-I3-COMPARE after B-R and C.2 branch closeouts | Blocks the single lane terminal record and any specification promotion |

## 39. Decision protocol for subsequent work

For each open question:

1. Record the exact question and alternatives before implementation selection.
2. Inspect only evidence authorized by the active checklist iteration.
3. Distinguish source fact, inference, preference, and missing information.
4. Propose one bounded resolution with gate effect and reopening condition.
5. Obtain owner acceptance when the choice is load-bearing or the checklist
   names an owner decision.
6. Add a stable decision ID without deleting the open-question history.
7. Update the checklist and every affected prospective artifact before work
   continues.

A review correction receives its own decision and change entry when it changes
authority, semantics, or rerun scope. Cosmetic corrections may remain in the
containing iteration when they introduce no unknown assumption.

## 40. Current boundary

Accepted decisions `P2-I3-DEC-001` through `P2-I3-DEC-024` retain the semantic,
source, LGRC9V3-only, N31 handoff, and theory/substrate/code authority chain.
DEC-025 admits the exact N31 return without transferring its evidence or
selecting B-R/C.2. DEC-026 defines the staged B-R-first/C.2-second program.
DEC-027 through DEC-032 fix the B-R mode, conservative redistribution law,
blind local encounter, comparison, contrast, and restoration meanings.
DEC-033 fixes the operational hypotheses without assigning outcomes. DEC-034
freezes the exact result-neutral conformance input and quarantine.

The accepted freeze is retained at source anchor `94bfe01`; the exact runtime
module, harness, and focused tests are retained at implementation anchor
`ce9701c`. The sole conformance attempt passes 11/11 cells and 36/36 checks,
uses no blocked public call, remains scientifically quarantined, and
reconstructs byte-exactly. DEC-035 accepts this as B-R operational
expressibility, corrects complete-schedule ownership to the factored RCAE/
PyGRC statement, and closes all fifteen section 8.2 requirements through their
individual operational/design/nonclaim bases rather than one empirical claim.

`P2-I3-DISCRIMINATOR-GATE` is passed. I04 candidate-blind calibration
preregistration is the only newly opened activity. It must resolve Q-009
through Q-012 and Q-016 prospectively without consuming conformance fixture
values, topology, observed split, digest, or derived margins.

Calibration execution, exact I06 registration, candidate/control execution,
C.2 work, every OP and R01–R05 result, `AE01-H-L03`, provider comparison,
appendix activation, and every branch/lane/specification result remain
unauthorized or unassigned until their named gates pass.
