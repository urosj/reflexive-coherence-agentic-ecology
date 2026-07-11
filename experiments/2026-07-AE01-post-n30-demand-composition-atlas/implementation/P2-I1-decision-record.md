# P2-I1 Decision Record

**Status:** active cumulative lane decision record

**Lane:** `AE01-L01`

**Iteration:** `P2-I1`

**Evidence effect:** none; decisions constrain later work but are not results

**Controlling boundaries:**
[P2-I1 brief](P2-I1-minimal-shared-medium-niche-brief.md),
[P2-I1 checklist](P2-I1-minimal-shared-medium-niche-checklist.md),
[common contract](../contracts/common-contract.md), and
[execution policy](../configs/p1_i5_execution_policy.json)

## 1. Purpose and use

This is the single cumulative decision record for the P2-I1 niche experiment.
Every resolved or partially resolved research/design question receives a stable
decision ID here rather than a separate file. The checklist remains the gate
tracker; this file preserves the considered options, reasoning, ownership,
accepted boundary, rejected/deferred alternatives, remaining unknowns, and
reopening conditions.

A decision may constrain a gate without passing it. Later evidence may reopen a
decision only through its recorded reopening conditions and change control; it
may not silently rewrite the historical choice.

Each accepted decision selects the primary preregistered path; it does not
erase rejected or deferred options. An alternative combination may be tested
later when it has a stated discriminator or information gain. It must receive a
new linked probe cycle, name the decision IDs and alternative option IDs it
changes, preserve the primary result, and preferably vary one decision axis at
a time. Testing an alternative is not itself reopening: reopening changes the
controlling primary decision because a recorded reopening condition was met.

For the specific P2-I1 result, a numeric threshold crossing is a machine fact,
not an experiment-level verdict. Exact values, proximity, raw distributions,
causal controls, and unexpected properties remain visible in interpretation.
This does not soften runtime, identity, conservation, safety, provenance, or
reconstruction requirements.

## 2. Decision index

| Decision ID | Question | Status | Gate effect | Date |
| --- | --- | --- | --- | --- |
| `P2-I1-DEC-001` | Which realization family should produce fresh P2-I1 evidence? | Accepted: Option A | Constrains CAL-PRE; does not pass it | 2026-07-11 |
| `P2-I1-DEC-002` | What participant carrier and non-circular continuity criterion should Option A use? | Accepted | Resolves `L01-Q01`; does not pass CAL-PRE | 2026-07-11 |
| `P2-I1-DEC-003` | What non-private medium carrier and shared-access scope should Option A use? | Accepted | Resolves `L01-Q02`; does not pass CAL-PRE | 2026-07-11 |
| `P2-I1-DEC-004` | Which one primary response family should govern Option A? | Accepted: formation | Resolves `L01-Q03`; does not pass CAL-PRE | 2026-07-11 |
| `P2-I1-DEC-005` | How is formation measured without treating partial progress or operational missingness as formation? | Accepted: opportunity-level binary formation and per-seed formation fraction | Resolves `L01-Q15`; does not pass CAL-PRE | 2026-07-11 |
| `P2-I1-DEC-006` | How many later opportunities should each seed expose, and how should they relate temporally? | Accepted: four independent counterfactual branches | Resolves `L01-Q16`; does not pass CAL-PRE | 2026-07-11 |
| `P2-I1-DEC-007` | What participant-relative discriminator distinguishes selective conditioning from a generic formation main effect? | Accepted: matched polarity-susceptibility inversion | Resolves `L01-Q05`; profiles completed by `DEC-010` | 2026-07-11 |
| `P2-I1-DEC-008` | How should binary formation be oriented and normalized without mistaking sparse normalized effects for complete formation? | Accepted: identity orientation plus normalized paired margin with raw coverage retained | Resolves `L01-Q04`; does not pass CAL-PRE | 2026-07-11 |
| `P2-I1-DEC-009` | What native event windows separate baseline, writing, medium materialization, later opportunity, and response? | Accepted: bounded causal-event windows | Resolves `L01-Q07`; numeric base supplied by `DEC-011` | 2026-07-11 |
| `P2-I1-DEC-010` | What topology, ownership, and canonical identities should instantiate the two matched reader contexts? | Accepted: RCAE-owned symmetric four-node fixture and four canonical profiles | Resolves `L01-Q17`; generated digests remain implementation outputs | 2026-07-11 |
| `P2-I1-DEC-011` | What numeric base fixture instantiates the topology, and how should its threshold-relative result be read? | Accepted: dyadic base fixture plus proximity-aware result interpretation | Resolves `L01-Q18`; interprets P2-I1 numeric results | 2026-07-11 |
| `P2-I1-DEC-012` | How should the live seeds vary the numeric base fixture? | Accepted: three bounded balanced coherence offsets | Resolves `L01-Q19`; local robustness only | 2026-07-11 |
| `P2-I1-DEC-013` | What candidate-blind matched null should calibrate the formation metric? | Accepted: identical synthetic panels across the full fraction domain | Resolves `L01-Q06`; implementation artifacts remain open | 2026-07-11 |
| `P2-I1-DEC-014` | What portable code and policy boundary should own calibration and live-result analysis? | Accepted: thin CLI, pure analysis module, one projected policy | Resolves `L01-Q20`; hashes/digests remain implementation outputs | 2026-07-11 |
| `P2-I1-DEC-015` | Are participant and medium operationally separated, and what controls participant self-aftereffect? | Accepted: separated carriers with participant-mediated reading and state-matched medium absence | Resolves `L01-Q08`; history-content causality remains `L01-Q09` | 2026-07-11 |
| `P2-I1-DEC-016` | How do content, source lineage, and causal order make the medium historical rather than a row-presence gate? | Accepted: neutral-content reference, source-digest mismatch, and strict order verification | Resolves `L01-Q09`; remains configured-history evidence | 2026-07-11 |
| `P2-I1-DEC-017` | What support carries formation, and how should the parent-context cell test it without inventing a parent basin? | Accepted: score-preserving reduced-support contrast | Resolves `L01-Q10`; supplies no parent-basin evidence | 2026-07-11 |
| `P2-I1-DEC-018` | Which single carrier/timescale axis should the final contrast vary? | Accepted: double later reader-packet amount | Resolves `L01-Q21`; bounded carrier-load contrast only | 2026-07-11 |
| `P2-I1-DEC-019` | Which comparator owns the primary normalized margin, and which comparisons remain causal controls? | Accepted: reference is primary; row absence owns medium dependency and selectivity | Resolves `L01-Q22`; completes normalized-margin specialization | 2026-07-11 |
| `P2-I1-DEC-020` | Which gate authorizes candidate execution without making the post-execution gate circular? | Accepted: explicit cycle-scoped `EXEC-FREEZE` | Bounded v2 CAL-PRE/CAL refresh passed; REG-GATE resumed | 2026-07-11 |
| `P2-I1-DEC-021` | How should REG-GATE become machine-verifiable without prematurely adding a first-class registration schema? | Accepted: experiment-local policy plus existing records and manifest | Constrains REG-GATE; R3 retains schema-admission decision | 2026-07-11 |
| `P2-I1-DEC-022` | Should registration and execution use one retained realization profile or transition between profiles? | Accepted: one path-free, cycle-spanning conformance profile | Constrains REG-GATE and EXEC-FREEZE; grants no execution authority | 2026-07-11 |
| `P2-I1-DEC-023` | How should baseline/reset identity remain exact across seven cells and three seed transforms? | Accepted: per-configuration identity plus fresh worker isolation | Resolves REG-GATE reset/contamination policy; execution proof remains open | 2026-07-11 |
| `P2-I1-DEC-024` | How should registration distinguish control applicability, resolution stage, and observed outcome? | Accepted: three independent control-lifecycle fields | Constrains all REG-GATE control plans; R3 retains schema-admission decision | 2026-07-11 |
| `P2-I1-DEC-025` | Does the primary cycle require constructed-scaffold withdrawal? | Accepted: not applicable; no constructed scaffold carries the claimed relation | Resolves `AE01-L01-CTRL-05` applicability; guarded reopening only | 2026-07-11 |
| `P2-I1-DEC-026` | How should C01 bind native calls that are more specific than the REG-GATE operation-family receipt? | Accepted: execution-specific callable superset | Constrains EXEC-FREEZE and every live receipt; REG reopens only on concrete contradiction | 2026-07-11 |

## 3. `P2-I1-DEC-001` — Realization family

**Status:** accepted for calibration preregistration

**Question IDs:** `L01-Q00`

### 3.1 Decision question

The decision addressed two related ambiguities:

1. whether P2-I1 merely inspects N29/N30 artifacts or produces fresh evidence
   through a live PyGRC realization; and
2. which source-current PyGRC surface is the best first realization family for
   a participant-relative, historically produced niche-conditioning test.

N29/N30 remain frozen inherited evidence. They motivate the realization,
preserve claim ceilings, and carry debts, but are not rerun as P2-I1
simulations. P2-I1 must produce fresh evidence through the frozen L01 execution
class `pygrc_runtime_with_rcae_producer`.

### 3.2 Source-current audit finding

The read-only audit established:

- N30's accepted relation chain records `n30_fresh_runtime=false` and consumes
  inherited N28 source-current artifacts.
- N29 Prototype B extracts a source-current LGRC9V3 boundary/shared-medium
  surface from earlier native runtime evidence.
- N29 Prototype C's composed runtime rows are producer-computed numeric traces,
  not calls into the PyGRC runtime.
- N29 did not execute Prototype B and Prototype C as one composed runtime.
- Source-current PyGRC now exposes model-owned packet queues, causal
  pulse-substrate surface rows, feedback-eligibility rows,
  feedback-conditioned event production, packet-arrival eligibility,
  snapshots, digests, and surface-lineage validation.

This creates a legitimate P2-I1 opportunity: execute a new causal chain through
PyGRC while keeping the ecology interpretation and experimental orchestration
explicitly RCAE-owned.

### 3.3 Options considered

| Option | Realization | Strength | Main risk | Disposition |
| --- | --- | --- | --- | --- |
| Artifact-only reconstruction | Inspect or recombine N29/N30 records without a fresh runtime | Strong provenance and low cost | Cannot generate an `observed_ae01_result` or scientific negative | Rejected as P2-I1 execution; retained as inherited source use |
| A — feedback-conditioned packet opportunity | Native pulse-contact surface → state-derived feedback-eligibility surface → model-owned later packet production/arrival | Direct history-conditioned later possibility with native queue, lineage, and fail-closed behavior | Selectivity could collapse into a configured policy distinction unless separately controlled | **Accepted** |
| B — pulse-contact coupling | Native contact surface → thresholded later packet opportunity | Smallest live causal chain | Primarily demonstrates trace-mediated routing and risks subsumption by L03 | Deferred as an alternative or L03-oriented realization |
| C — child-basin/topology realization | Native child-basin/boundary state and transported surface → later route or basin formation | Strong participant continuity and geometric differentiation | Introduces parent-context, boundary-exchange, topology, and L05/L07 confounds too early | Deferred as a stronger later contrast |
| Native-only replay | Remove the RCAE experimental producer boundary and rerun through an admitted native realization | Tests naturalization directly | Premature before P2-I1 reveals a useful function; current L01 finite policy does not authorize it | Deferred to conditional `P2-I1-NAT` follow-up |

### 3.4 Accepted realization family

```text
registered source-side local differentiation
  -> participant-originated packet event processed by LGRC9V3
  -> native route-local pulse-contact surface
  -> native state-derived feedback-eligibility surface
  -> model-owned feedback producer schedules or blocks a later packet
  -> distinct target-side route/local differentiation receives or fails to
     receive the later packet-arrival opportunity
```

This selects a realization family, not an experimental result. It does not
select the participant carrier, continuity threshold, exact fixture, response
family, selectivity discriminator, opportunity count, windows, null generator,
or terminal classification.

### 3.5 Ownership boundary

| Owner | Owns in P2-I1 Option A | Must not be consumed as |
| --- | --- | --- |
| N29/N30 artifacts | Motivation, admitted source legs, original claim ceilings, controls, and inherited debts | Fresh P2-I1 runtime evidence |
| Source-current PyGRC | Runtime state and budget evolution; event queue and causal timing; pulse-contact surface emission; feedback-eligibility derivation; model-owned feedback scheduling/blocking; packet processing and arrival eligibility; snapshot and lineage semantics | Ecology interpretation, niche proof, or RCAE result by itself |
| RCAE experimental producer/harness | Portable fixture or landscape-seed definition; initial writer intervention; configuration of declared masks, thresholds, compatibility profiles, and opportunity windows; invocation of public PyGRC operations; seven-cell orchestration | Native LGRC mechanism or evidence that PyGRC already implements niche formation |
| RCAE analysis and records | Opportunity projection, matched comparisons, calibration, controls, rung classification, developmental interpretation, and demand extraction | Native substrate evidence or retroactive N29/N30 upgrade |
| Graph project | PyGRC implementation changes, source-current native admission, and later graph-experiment authority | Work that RCAE may modify from this repository |

The PyGRC feedback producer is model-owned runtime behavior. RCAE owns the
experimental adapter that configures and invokes it. The adapter may not
compute the later response, directly mutate coherence, inject a successful
surface, mark an event processed, bypass the event queue, or write claim labels
into runtime state.

### 3.6 Decision and consequences

```text
P2-I1-DEC-001 = option_A_feedback_conditioned_packet_opportunity
execution_class = pygrc_runtime_with_rcae_producer
```

- Artifact inspection remains source admission and calibration input work, not
  candidate execution.
- Missing or incompatible PyGRC blocks or leaves execution incomplete and
  never becomes a scientific negative.
- Native and RCAE-owned legs must be individually identified in the
  realization profile and runtime receipts.
- The graph/PyGRC repository remains read-only.
- Options B and C remain preregisterable alternatives if Option A exposes a
  specific limitation, not automatic retries.
- `P2-I1-NAT` is triggered only by an informative P2-I1 result and produces new
  evidence rather than upgrading the original run.

### 3.7 Reopening conditions

Reopen `P2-I1-DEC-001` if:

- the compatible local PyGRC lacks one of the required source-current
  operations;
- the feedback surface cannot be reconstructed as non-private runtime state;
- participant continuity cannot be represented without circularly reading the
  later outcome;
- selectivity can be expressed only as a label or configured accept/reject
  switch;
- the RCAE adapter must calculate the later response or bypass native queue
  processing; or
- the realization would require modifying the graph/PyGRC repository.

## 4. `P2-I1-DEC-002` — Participant carrier and continuity structure

**Status:** accepted

**Question IDs:** `L01-Q01`

### 4.1 Decision question

Which Option A object can count as the participant carrier without reducing
the participant to a transient event, importing an inherited artifact as a new
runtime participant, or defining continuity from the later outcome?

### 4.2 Options considered

| Option | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Packet lineage | Native, exact, and auditable | A packet/event lineage is too transient to be the local differentiation | Rejected as participant; retained as writer-event lineage |
| N30 mapped-basin signature | Accepted continuity method and replay recognizability | Belongs to inherited artifact geometry rather than the fresh Option A runtime | Retained as methodological precedent only |
| LGRC9V3 child basin | Strong native participant structure | Reintroduces the deferred topology realization and L05/L07 confounds | Deferred with Option C |
| Registered LGRC9V3 route-aspect source pole | Serializable native identity, stable node mask, explicit channels, and packet-lineage compatibility | Requires an RCAE-declared viability test over native state | **Accepted** |

### 4.3 Accepted participant carrier

```text
participant_carrier:
  source pole region of a registered LGRC9V3RouteAspect

participant_identity_projection:
  route_aspect_digest
  source_pole_id
  pole_region_digest
  fixed_topology_signature
  registered_source_lineage_id
```

The source pole is a bounded local differentiation, not an agent, organism,
self, or accepted identity. The `LGRC9V3RouteAspect` supplies a canonical
serializable route/pole contract; the registered source lineage attributes the
writer packet and its surface chain to that carrier.

### 4.4 Accepted continuity structure

Continuity is evaluated across the initial snapshot, post-writer snapshot, and
pre-reader snapshot. It passes only when:

- `route_aspect_digest`, `source_pole_id`, and `pole_region_digest` match
  exactly;
- every registered source-pole node remains live;
- source-pole membership and fixed topology remain unchanged;
- the writer packet and pulse-contact surface preserve the registered
  `source_lineage_id` through the machine-level relation chain;
- source-pole coherence mass remains above a preregistered viability floor; and
- no later response, feedback success, terminal class, or outcome-derived field
  participates in identity, continuity, or the viability threshold.

The same label, route name, or later successful response cannot rescue a
failed structural, lineage, liveness, or coherence check. Native PyGRC state
supplies all measured fields; RCAE owns the bounded participant interpretation
and the preregistered continuity predicate.

### 4.5 Viability-floor options

| Floor policy | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Absolute coherence floor | Simple | Fixture- and scale-dependent | Rejected |
| Fixed fraction of initial pole mass | Portable | Arbitrary fraction can hide differences in writer cost | Rejected as primary |
| Calibration-derived floor | Candidate-blind | Matched-null resolution does not define participant viability | Rejected |
| Budget-derived one-repeat reserve | Uses native conservation and the registered writer action | Requires strict debit and support accounting | **Accepted** |

### 4.6 Accepted viability rule

Definitions:

```text
M0 = source-pole coherence mass before the writer event
Dw = registered native coherence debit of one writer packet
Mt = source-pole coherence mass at a model-owned event boundary
epsilon_budget = 1e-9
```

Continuity requires at every model-owned event boundary from the initial
snapshot through the pre-reader snapshot:

```text
abs(native_budget_error) <= epsilon_budget
Mt >= M0 - Dw - epsilon_budget
Mt >= Dw - epsilon_budget
```

The first mass bound rejects unregistered depletion. The second retains enough
coherence for one further writer event at the same registered scale. Equality
within `epsilon_budget` passes. The `1e-9` tolerance is the source-current
PyGRC runtime validation default; it is not calibrated from candidate outcomes.

The base realization permits no inbound coherence reconstruction of the source
pole between writer and pre-reader boundaries. Inbound rescue, hidden support,
an extra debit, producer mutation, or any below-floor event boundary fails the
base continuity criterion and remains separately classifiable. Evaluation at
every model-owned event boundary prevents an endpoint-only recovery from
hiding participant loss and reconstruction.

The rule does not reuse N30's inherited `0.06` mapped-basin recognizability
threshold because that threshold measures cross-fixture signature distance,
not Option A source-pole viability. Participant identity and viability may not
use the later response, feedback success, candidate/control difference,
calibrated `delta`, or terminal class.

`L01-Q01` is resolved by the accepted route-aspect source-pole carrier,
structural/lineage criterion, and budget-derived one-repeat reserve.

### 4.7 Reopening conditions

Reopen `P2-I1-DEC-002` if:

- Option A cannot bind writer events to a route-aspect source pole through
  native lineage fields;
- route-aspect or pole-region identity is not stable across reconstruction;
- fixed-topology execution cannot supply a distinct target-side reader;
- coherence mass is shown to be an invalid or circular viability observable;
  or
- the carrier requires a topology-changing child-basin account to be
  scientifically meaningful.

## 5. `P2-I1-DEC-003` — Medium carrier and shared-access scope

**Status:** accepted

**Question IDs:** `L01-Q02`

### 5.1 Decision question

Which Option A state is the non-private medium that causally conditions the
later opportunity, and what access boundary makes it shared-local without
turning it into a global log, private participant state, or direct message?

### 5.2 Options considered

| Option | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Live node coherence field | Native and dynamically relevant | Too close to participant state and generic environmental condition; history is not explicit | Rejected as the medium carrier |
| Pulse-contact row alone | Native and auditable writer trace | Primarily a contact/routing trace and better aligned with L03 | Rejected as primary L01 medium; retained alternative |
| Feedback-eligibility row alone | Directly read by the later model-owned producer | Can look like a derived label without mandatory source history | Rejected as a standalone carrier |
| Narrow pulse-surface ledger with ordered contact→feedback lineage | Native, reconstructable, history-bearing, and causally load-bearing | Requires locality, branch identity, and anti-addressing controls | **Accepted** |

### 5.3 Accepted medium identity

```text
medium_carrier:
  LGRC9V3 model-owned causal_pulse_substrate_surface_log

focal_medium_state:
  exactly one feedback_eligibility row
  linked to exactly one preceding route_local_pulse_contact row

medium_history_digest:
  digest(
    pulse_contact_surface_digest,
    feedback_eligibility_surface_digest
  )

access_scope:
  shared_local
```

The runtime log is the native carrier, but P2-I1 does not treat the complete
global log as its medium state. The admissible state is the narrow ordered
two-row lineage registered for one local surface. The feedback row must retain
the pulse-contact predecessor digest, native event order, surface nodes, and
state digest; authored interpretation cannot join otherwise unrelated rows.

### 5.4 Shared-local access boundary

Shared-local access requires:

- both rows live in model-owned runtime state outside the participant identity
  projection;
- the rows survive participant-label removal and reconstruct from snapshot and
  event lineage;
- the writer event and feedback row contain no later reader ID, expected route
  ID, or expected next channel;
- `expected_next_route_id` and `expected_next_channel_id` remain unset in the
  feedback row;
- each reader owns its independently registered target route configuration;
- at least two distinct reader configurations can consume the same frozen
  `medium_history_digest` in counterfactual branches from one identical
  pre-reader snapshot;
- every reader lies within the registered surface-node/access region;
- the writer cannot privately select which reader succeeds; and
- simultaneous multi-source or multi-reader co-conditioning is not claimed,
  preserving the L02 boundary.

Reader-specific source/target/edge configuration may exist in the reader's
local runtime request. It is not written into the medium by the participant and
cannot serve as medium history. The later producer must read the committed
feedback row through model-owned policy rather than receive an RCAE-computed
success value.

### 5.5 Causal and control consequences

The load-bearing chain is:

```text
writer packet
  -> route-local pulse-contact row
  -> feedback-eligibility row
  -> model-owned producer reads the row
  -> later opportunity is scheduled or blocked
```

- Disabling, freezing, withdrawing, or substituting the registered surface
  lineage must change the later opportunity while preserving participant
  opportunity, baseline support, and reader configuration.
- A pulse row that changes only telemetry or authored interpretation cannot
  pass the medium-dependency control.
- A direct writer-to-reader address, copied private state, or global controller
  classifies the medium as absent or producer-carried.
- Counterfactual branches must begin from an identical frozen pre-reader
  snapshot and retain the same medium-history digest.

The native carrier is persistent ledger state and currently supplies no
natural decay law. Persistence, freeze, and withdrawal remain testable, but
P2-I1 cannot relabel the carrier as a naturalized environmental field, slow
medium memory, or native niche surface. This remains explicit medium and
naturalization debt.

### 5.6 Reopening conditions

Reopen `P2-I1-DEC-003` if:

- the feedback producer can consume the state only through reader identity or
  writer-supplied addressing;
- the two-row lineage cannot be reconstructed from native snapshots and event
  records;
- separate reader branches cannot preserve an identical medium-history digest;
- the surface log is telemetry-only rather than load-bearing runtime state;
- disabling the medium necessarily removes participant opportunity or baseline
  support; or
- a source-current native field supplies a less producer-dependent medium with
  the same registered function.

## 6. `P2-I1-DEC-004` — Primary response family

**Status:** accepted

**Question IDs:** `L01-Q03`

### 6.1 Decision question

Which one frozen response family should describe the later reader's outcome in
Option A without substituting medium persistence, a susceptibility proxy,
lower cost, or same-carrier re-entry for the niche-conditioning question?

### 6.2 Options considered

| Response family | Fit with Option A | Main problem | Disposition |
| --- | --- | --- | --- |
| Persistence | Measures whether participant or medium remains | Does not establish a changed later possibility | Secondary/control only |
| Re-entry | Strong for a returning carrier | Option A registers a distinct later reader, so the term would misclassify the relation | Deferred to a same-carrier alternative |
| Cost | Captures event, time, coherence, or packet-budget burden | Lower cost alone is not niche conditioning | Secondary response |
| Susceptibility | Close to feedback polarity and eligibility | Risks making a derived score the phenomenon and repeating the N29 proxy problem | Secondary discriminator/control |
| Formation | Directly measures whether a later native opportunity becomes admissible and completes | Must require processed arrival evidence rather than mere scheduling | **Accepted** |

### 6.3 Accepted primary response

```text
primary_response_family:
  formation

formed_object:
  later native packet-arrival opportunity
  for a registered distinct reader configuration
```

Formation requires the complete native chain:

```text
model-owned feedback producer reads the registered medium history
  -> schedules a native packet departure
  -> model-owned queue processes departure
  -> model-owned queue processes arrival
  -> native packet-arrival eligibility is emitted for the registered reader
```

A scheduled event alone is not formation. The machine relation chain must
connect the accepted medium-history digest to the feedback production record,
departure, arrival, and reader eligibility inside the registered response
window.

### 6.4 Non-formation outcomes

None of the following satisfies the primary response:

- a feedback or susceptibility score without later native processing;
- a scheduled but unprocessed event;
- an RCAE-computed response or direct success write;
- a report or runtime label asserting eligibility;
- an arrival outside the registered reader route or response window;
- an opportunity without the accepted medium-history digest;
- an infrastructure-missing or censored opportunity; or
- an opportunity blocked before scientific execution by a failed record guard.

`inadmissible` and `structurally_unavailable` may be scientific opportunity
outcomes when execution and controls are valid. They do not count as formed,
but they remain visible in the distribution and interpretation.

### 6.5 Secondary responses

The following may be preregistered as secondary and may not replace formation
after outcomes:

- medium persistence and lineage validity;
- feedback/susceptibility margin;
- event-time delay;
- coherence and packet-budget cost; and
- failure, inadmissibility, and missingness classifications.

### 6.6 Still unresolved

This decision selects semantics, not the numeric metric. The exact
opportunity-level raw formation formula, units, denominator, missingness
treatment, and opportunity-to-seed aggregation were deferred to `L01-Q15` and
are now resolved by `P2-I1-DEC-005`. Orientation was deferred to `L01-Q04` and
is now resolved by `P2-I1-DEC-008`.

### 6.7 Reopening conditions

Reopen `P2-I1-DEC-004` if:

- the registered reader becomes the same carrier and re-entry is the more
  accurate causal description;
- source-current PyGRC cannot emit or reconstruct arrival eligibility;
- native scheduling and processed arrival cannot be distinguished;
- formation cannot be separated from reader-local configuration or direct
  addressing; or
- an alternative response family yields a more direct L01 discriminator
  without moving the result into another lane.

## 7. `P2-I1-DEC-005` — Raw formation metric and aggregation

**Status:** accepted

**Question IDs:** `L01-Q15`

### 7.1 Decision question

How should the accepted formation response become a numeric primary response
without allowing a susceptibility score, partial causal-chain completion,
lower cost, or operational failure to masquerade as formation?

### 7.2 Options considered

| Metric family | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Binary opportunity formation | Matches the accepted formed object and has an auditable native completion boundary | Needs secondary records to explain near-formation and cost | **Accepted as primary** |
| Continuous susceptibility or feedback score | Sensitive to weak and narrow effects | Repeats the proxy risk and can report formation without native arrival eligibility | Secondary only |
| Time or cost to formation | Reveals efficiency and burden | Cannot represent formation independently of cost and censoring choices | Secondary only |
| Ordinal causal-chain completion depth | Locates the failed stage | Can make partial progress look like a fractional formed object | Secondary diagnostic only |

### 7.3 Opportunity-level response

For every preregistered later opportunity `o`:

```text
formation(o) = 1
  iff the registered medium-history digest is joined through the complete
      model-owned feedback-production, departure, arrival, and native
      packet-arrival-eligibility chain for the registered reader and window

formation(o) = 0
  iff scientific execution is valid but the opportunity does not form

formation(o) = null
  iff infrastructure, runtime censoring, or a failed control prevents a
      scientific observation
```

The opportunity-level `raw_response` is therefore `0` or `1` for a scientific
observation and `null` for a non-evaluable operational record. Its unit is one
formed opportunity per registered opportunity. `oriented_response` was
deferred to `L01-Q04` and is now resolved by `P2-I1-DEC-008`.

The status boundary is:

| `opportunity_status` | Primary value | Scientific denominator | Effect |
| --- | ---: | ---: | --- |
| `observed` with complete registered chain | `1` | included | formed opportunity |
| `observed` after valid scientific non-formation | `0` | included | observed non-formation |
| `inadmissible` | `0` | included | scientific non-formation with inadmissibility retained |
| `structurally_unavailable` | `0` | included | scientific non-formation and possible missing-surface signal |
| `censored_runtime` | `null` | excluded explicitly | seed response is non-evaluable |
| `missing_infrastructure` | `null` | excluded explicitly | seed response is non-evaluable |
| `blocked_by_control` | `null` | excluded explicitly | seed response is non-evaluable |

Operational records use `admissibility=not_evaluable`; they are not silently
encoded as scientifically inadmissible. The opportunity record vocabulary must
therefore admit `not_evaluable` before CAL-PRE closes.

### 7.4 Seed aggregation

For a seed `s` with its complete preregistered opportunity set `O_s`:

```text
formation_fraction(s) = sum(formation(o) for o in O_s) / |O_s|
```

This aggregate is defined only when:

- every registered opportunity in `O_s` has a scientific `0` or `1` value;
- the executed opportunity count equals the frozen planned count; and
- `|O_s| > 0`.

Any `null` opportunity makes the seed aggregate non-evaluable rather than
shrinking its denominator. The retained output must preserve the planned,
formed, observed-non-formed, inadmissible, structurally unavailable, and each
operational-status count behind the aggregate.

The seed response is a dimensionless fraction in `[0, 1]`. Candidate and
comparator fractions are paired within the same seed and frozen configuration,
then passed to the Phase 1 normalized paired-margin contract. Seeds remain
separate and are never pooled into a single formation rate.

### 7.5 Secondary diagnostics

The following remain visible but cannot replace the binary primary response
inside the cycle:

- causal-chain completion stage;
- feedback or susceptibility margin;
- departure and arrival delay;
- coherence and packet-budget cost; and
- detailed inadmissibility, structural-unavailability, and operational-failure
  reasons.

These diagnostics support developmental interpretation of narrow, negative,
or unexpected results without upgrading a non-formed opportunity.

### 7.6 Still unresolved

This decision does not select:

- the number of opportunities per seed;
- whether those opportunities are independent, sequential, or cumulative;
- the exact opportunity and response windows; or
- the orientation transform, which was later resolved by `P2-I1-DEC-008`.

### 7.7 Reopening conditions

Reopen `P2-I1-DEC-005` if:

- native arrival eligibility cannot supply an unambiguous completion event;
- the runtime cannot distinguish a scientifically observed non-formation from
  an operationally non-evaluable opportunity;
- the planned opportunities cannot share a meaningful denominator across
  candidate and comparator cells;
- binary completion discards a causal distinction necessary to answer L01
  rather than merely interpret it; or
- sequential dependence makes a fraction scientifically misleading even when
  the dependence is retained explicitly.

## 8. `P2-I1-DEC-006` — Opportunity count and temporal structure

**Status:** accepted

**Question IDs:** `L01-Q16`

### 8.1 Decision question

How many later opportunities should each seed expose, and should those
opportunities be independent counterfactual branches, sequential events in one
runtime history, or cumulative events whose results alter later opportunities?

The structure must make the formation fraction nontrivial without importing
persistence, depletion, or order effects into the first L01 realization.

### 8.2 Options considered

| Structure | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| One opportunity per seed | Smallest possible execution | Leaves three binary seed results and makes one-event success structurally prominent | Rejected for the primary cycle |
| Four independent counterfactual opportunities | Smallest panel that supports more than one reader configuration and a nontrivial within-seed fraction | Requires snapshot restoration and frozen profile matching | **Accepted** |
| Sequential opportunities | Tests whether conditioning persists across later events | Conflates L01 with depletion, self-aftereffect, and trace persistence | Deferred linked cycle; possible L03 relevance |
| Cumulative opportunities | Exposes ecology-like interference and adaptation | Makes every later response depend on prior reader outcomes | Deferred stronger composition cycle |
| Larger independent panel | Improves fractional resolution | Expands the fixture and runtime before the relevant distinctions are known | Deferred unless the four-profile panel is under-resolving |

### 8.3 Accepted opportunity panel

Each cell and seed has exactly four registered opportunities:

```text
opportunity_count_per_seed = 4
opportunity_indices = [0, 1, 2, 3]
opportunity_relation = independent_counterfactual_branches
seed_response_denominator = 4
possible_formation_fractions = [0.0, 0.25, 0.5, 0.75, 1.0]
```

For each cell/seed, all four opportunities restore the same frozen
post-writer, pre-reader branch-point snapshot. Each branch then applies exactly
one preregistered reader/opportunity profile and runs through its registered
response window. No branch outcome, queue residue, coherence debit, surface
row, idempotency key, or producer record may enter another branch.

The four `opportunity_profile_digest` values must be distinct. The panel must
contain at least two distinct `reader_configuration_digest` values so shared
access and later selectivity can be tested. Exact reader identities,
compatibility roles, and the allowed profile dimensions remain open under
`L01-Q05`; those policies are now resolved by `P2-I1-DEC-007`. Event-window
policy is now resolved by `P2-I1-DEC-009`; concrete profile identities and
times are now resolved by `P2-I1-DEC-010` and `P2-I1-DEC-011`, with generated
digests left to implementation.

### 8.4 Cross-cell matching

Corresponding opportunity indices across candidate and comparator cells must
share the same frozen reader/opportunity profile digest and all declared
non-medium fixture inputs. The intentional cell intervention may change medium
history or its causal availability; it may not silently change the reader,
route, timing profile, initial support, or opportunity count.

The four branches within a cell share that cell's registered
`medium_history_digest`. Candidate and comparator histories need not have the
same digest because producing, freezing, withdrawing, or nulling the medium is
the declared intervention. Their lineage role and all non-intervened inputs
must remain paired.

### 8.5 Why branching is required

Source-current PyGRC suppresses duplicate feedback production from an
identical committed feedback row through its native idempotency key. Replaying
one unchanged row inside a single history would therefore be duplicate
processing rather than an independent opportunity. Fresh branches allow four
distinct registered opportunity profiles to consume the same frozen history
without bypassing native duplicate suppression or carrying effects from one
reader into another.

This also fits the participant continuity decision: the one-repeat reserve is
tested once per independent branch instead of being silently multiplied into
a four-packet cumulative reserve.

### 8.6 Retained distribution

Every seed output must retain:

- the branch-point snapshot and medium-history digests;
- the four ordered opportunity/profile digests;
- every opportunity-level formation value and status;
- reader-configuration and later selectivity groupings;
- proof that every branch began from the registered branch point; and
- the derived formation fraction without dropping or replacing a branch.

The primary fraction aggregates the four opportunity values, but interpretation
must retain profile- and reader-stratified distributions. A positive fraction
cannot hide that only one reader or one opportunity profile formed.

### 8.7 Reopening conditions

Reopen `P2-I1-DEC-006` if:

- source-current snapshots cannot restore the branch point with exact native
  queue, surface, and lineage identity;
- four distinct opportunity profiles cannot be defined without changing the
  writer or medium intervention;
- the panel cannot include two reader configurations with comparable medium
  exposure;
- four branches cannot complete within the frozen resource envelope;
- the resulting quarter-step response is too coarse to distinguish the
  candidate-blind resolution band; or
- evidence shows that temporal persistence or composition, rather than an
  independent later possibility, is the necessary L01 discriminator.

## 9. `P2-I1-DEC-007` — Selectivity discriminator

**Status:** accepted for calibration preregistration; concrete profile identity
remains open

**Question IDs:** `L01-Q05`; opens `L01-Q17`

### 9.1 Decision question

What participant-relative discriminator can distinguish selective
niche-conditioning from a generic formation main effect while keeping the
medium history, opportunity, support, and baseline viability comparable?

The discriminator must be candidate-blind, mechanically evaluable, and
invertible. It may not use reader identity, a success label, or direct
addressing as a substitute for susceptibility.

### 9.2 Options considered

| Discriminator | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Registered polarity susceptibility | Uses source-current native `expected_polarity`, supports an exact inversion control, and interacts with the feedback surface | Susceptibility remains configured rather than participant-intrinsic | **Accepted with constructed-mechanism ceiling** |
| Threshold sensitivity | Provides graded susceptibility | A chosen threshold can manufacture the group distinction and lacks a clean symmetry | Deferred alternative |
| Route or location compatibility | Appears more geometric | Risks changing exposure, path burden, routing, or moving the result toward L03/L05 | Deferred until those confounds can be matched |
| Reader identity or label | Easy to configure | Directly embeds the answer and is not a causal discriminator | Rejected |
| Native participant-intrinsic receptor state | Would support a stronger claim | No accepted source-current surface has been established for Option A | Missing-surface demand, not the primary realization |

### 9.3 Four-profile allocation

The four independent opportunities form two matched context pairs:

```text
context A:
  opportunity 0 = history-aligned polarity susceptibility
  opportunity 1 = polarity-inverted susceptibility

context B:
  opportunity 2 = history-aligned polarity susceptibility
  opportunity 3 = polarity-inverted susceptibility
```

For each context, the two profiles differ only in the registered
`expected_polarity`. The aligned profile uses the preregistered writer/medium
polarity expectation; the inverted profile uses its opposite. Group assignment
is frozen before candidate execution. An unexpected observed polarity may
produce a counter-selective result but may not relabel the profiles.

The two contexts must be distinct through one or more candidate-blind
opportunity dimensions while remaining matched within each polarity pair. The
exact context dimensions, reader IDs, route IDs, timing profiles, and profile
identity rules are now resolved by `P2-I1-DEC-010`; their generated digests
remain implementation outputs.

### 9.4 Required matching

Within each pair, aligned and inverted profiles must have identical:

- branch-point snapshot and medium-history digest;
- source and target opportunity, route burden, and packet amount;
- baseline viability, participant reserve, and support;
- event and response windows;
- feedback threshold and front/rear masks; and
- all producer fields other than `expected_polarity`.

The feedback surface row may not contain the reader ID, selectivity group,
expected route, next channel, or later success. The same committed history is
therefore accessible to both counterfactual readers even though their
registered susceptibilities differ.

### 9.5 Selectivity interaction

For seed `s`, matched context `k`, and group `g`:

```text
medium_effect(k, g, s) =
  formation(candidate-conditioning, k, g, s)
  - formation(medium-freeze-withdrawal, k, g, s)

pair_interaction(k, s) =
  medium_effect(k, aligned, s)
  - medium_effect(k, inverted, s)

selectivity_margin(s) =
  mean(pair_interaction(A, s), pair_interaction(B, s))
```

The primary calibrated `delta` does not enter this calculation. With two
binary matched pairs, the smallest nonzero selectivity-margin step is `0.5`.
That combinatorial resolution is the frozen candidate-blind threshold source:

```text
selectivity_metric_uses_calibrated_delta = false
selectivity_threshold_candidate_blind = true
selectivity_threshold_source = binary_two_pair_combinatorial_resolution
minimum_selectivity_margin = 0.5
expected_interaction_direction = positive
```

Every pair interaction and raw opportunity remains visible; the mean cannot
erase pair disagreement.

### 9.6 Developmental ladder

The threshold is not a terminal accept/reject rule:

| Relation | Machine condition | Interpretation ceiling |
| --- | --- | --- |
| Strong constructed selectivity | Both pair interactions are positive | Constructed polarity-relative selectivity may satisfy this causal boundary if all other controls pass |
| Weak directionally resolved | One pair is positive, the other is zero, and margin is at least `0.5` | Bounded weak selectivity; stronger support remains blocked |
| Mixed | Pair signs disagree, regardless of positive mean | Mixed susceptibility relation requiring explanation |
| Generic main effect | Formation improves but selectivity margin is zero | Environmental conditioning below the niche-selectivity boundary |
| Counter-selective | Selectivity margin is negative | Opposite relation or incorrectly oriented realization |
| Non-evaluable | Either pair lacks valid scientific observations | No selectivity support or refutation |

A positive mean with a counter-direction pair is `mixed`, not weak support.
Magnitude cannot compensate for failed exposure matching, baseline viability,
medium dependence, or direct-address controls.

If both pair interactions are exactly zero, the result is
`generic_main_effect_or_no_effect`, not `weak_directionally_resolved`: the weak
branch requires at least one strictly positive pair interaction. Whether the
zero relation accompanies generic formation or no formation is read from the
retained raw opportunity coverage.

### 9.7 Susceptibility-inversion control

The `susceptibility-inversion` cell swaps `expected_polarity` between stable
reader slots while preserving their other registered fields. The formation
advantage must follow the susceptibility relation rather than the reader ID.
Failure to reverse classifies the apparent selectivity as reader-carried,
producer-carried, generic, or unresolved.

### 9.8 Claim boundary

`expected_polarity` is a configured native producer susceptibility, not a
demonstrated participant-intrinsic property. Even a strong result therefore
supports only bounded, constructed polarity-relative niche conditioning. It
does not establish native participant selectivity, an ecology motif, or
agency. A successful but configuration-dependent result may instead disclose
a precise demand for an intrinsic LGRC susceptibility or receptor surface.

### 9.9 Reopening conditions

Reopen `P2-I1-DEC-007` if:

- source-current PyGRC cannot preserve the same medium history while varying
  only `expected_polarity`;
- polarity roles cannot be assigned before candidate observation;
- the inversion cell cannot distinguish susceptibility from reader identity or
  direct addressing;
- the two matched contexts cannot maintain comparable baseline viability and
  medium exposure;
- the binary two-pair resolution proves too coarse for the causal question; or
- a source-current participant-intrinsic discriminator becomes available and
  can replace configured susceptibility without changing the lane question.

## 10. `P2-I1-DEC-008` — Orientation and normalized paired margin

**Status:** accepted

**Question IDs:** `L01-Q04`

### 10.1 Decision question

How should the binary opportunity and per-seed formation-fraction responses be
oriented and passed into the frozen Phase 1 normalized paired-margin contract
without allowing normalization to hide absolute opportunity coverage?

### 10.2 Options considered

| Orientation or transform | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Identity, higher formation aligned | Preserves the direct meaning and `[0, 1]` domain | Normalized margins can make sparse and complete effects look equal | **Accepted with mandatory raw coverage** |
| Lower formation aligned | None for the accepted response | Reverses the meaning of formation | Rejected |
| Logit/probit transform | Expands boundary resolution | Requires smoothing at `0` and `1` and obscures the four-opportunity scale | Rejected for the primary cycle |
| Selectivity-adjusted formation | Combines two causal demands in one number | Lets selectivity replace the primary medium-history comparison | Rejected; selectivity remains separate |
| Raw fraction-point difference only | Maximally interpretable | Would not instantiate the frozen Phase 1 normalized metric | Retained alongside, not instead of, the normalized margin |

### 10.3 Orientation

For each scientifically evaluable opportunity and seed:

```text
oriented_response(o) = raw_response(o)

raw_response(s) = formation_fraction(s)
oriented_response(s) = formation_fraction(s)

direction = higher_is_aligned
orientation_transform = identity
```

`null` remains `null`; orientation may not turn operational missingness into a
numeric value. Formation fractions remain dimensionless values in `[0, 1]`.

### 10.4 Paired responses

For a matched candidate response `C_s` and comparator response `K_s`:

```text
raw_paired_difference(s) = C_s - K_s

normalized_margin(s) =
  raw_paired_difference(s)
  / max(abs(C_s), abs(K_s), measurement_resolution)
```

The raw difference is measured in formation-fraction points and lies in
`[-1, 1]`. The normalized margin is dimensionless and also lies in `[-1, 1]`
for the accepted nonnegative response domain. Pairing remains by seed, frozen
configuration, and corresponding opportunity-profile panel.

The selectivity interaction from `P2-I1-DEC-007` is not part of `C_s`, `K_s`,
the numerator, or the denominator. It remains a separate causal/control gate
and does not consume calibrated `delta`.

### 10.5 Zero and unavailable responses

| Condition | Margin | Resolution relation | Scientific meaning |
| --- | --- | --- | --- |
| `C_s = 0` and `K_s = 0` | `0` using the resolution floor | `resolution_limited` | Valid observed non-formation on both sides; neither aligned nor counter evidence |
| Both numeric and unequal | Formula above | Derived against frozen `delta` | Directional result with raw coverage retained |
| Both numeric and equal above zero | `0` | Derived against frozen `delta` | Formation without a candidate/comparator difference |
| Either response operationally non-evaluable | `null` | `resolution_unknown` | No scientific paired margin |

An operationally missing response may not be replaced by zero, imputed, or
dropped so that the remaining side produces a margin.

### 10.6 Mandatory scale interpretation

Normalization establishes direction and scale relative to the paired observed
responses; it does not establish formation coverage or evidential strength by
itself. In particular:

```text
C_s = 0.25, K_s = 0.00 -> normalized_margin = 1.0
C_s = 1.00, K_s = 0.00 -> normalized_margin = 1.0
```

These are not equivalent results. Every machine observation and authored
interpretation must retain:

- `C_s` and `K_s`;
- `raw_paired_difference(s)`;
- all eight paired opportunity records behind the two fractions;
- `normalized_margin(s)` and its frozen-delta relation; and
- profile- and selectivity-stratified coverage.

The developmental ladder may describe sparse, partial, broad, or complete
coverage only from the raw distribution. A maximally normalized sparse effect
cannot be called maximal formation.

### 10.7 Reopening conditions

Reopen `P2-I1-DEC-008` if:

- the Phase 1 normalized denominator cannot be specialized to the `[0, 1]`
  formation domain without ambiguity;
- pairing cannot preserve identical seeds and opportunity-profile panels;
- the four-opportunity fraction is replaced by a response whose natural
  direction is not higher-aligned;
- calibration shows that the normalized representation is resolution-unknown
  for otherwise valid numeric responses; or
- downstream tooling cannot retain raw fractions and differences beside the
  normalized margin.

## 11. `P2-I1-DEC-009` — Native event windows

**Status:** accepted for calibration preregistration; fixture-specific event
times remain open

**Question IDs:** `L01-Q07`; constrains `L01-Q17`

### 11.1 Decision question

What event boundaries establish that the writer history is committed before a
later reader opportunity without importing arbitrary elapsed-time thresholds,
unbounded autonomous execution, or persistence claims into the minimal L01
realization?

### 11.2 Options considered

| Window policy | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Native causal-event boundaries | Follows queue ownership and gives each causal stage an auditable event/scheduler order | Establishes ordering but not extended persistence | **Accepted for the minimal cycle** |
| Fixed wall-clock or arbitrary `T_e` duration | Simple numeric cutoff | Can censor native edge delay or create unsupported temporal meaning | Rejected |
| Unbounded `run_autonomous(...)` | Lets all available work settle | May add undeclared producer cycles and obscure the causal chain | Rejected |
| Delayed or repeated reader window | Tests stronger persistence | Conflates minimal L01 with trace persistence, depletion, and L03-like questions | Deferred linked cycle |
| Multi-hop response window | Tests broader transfer | Adds routing and composition demands before the minimal relation is known | Deferred transfer variant |

### 11.3 Accepted window sequence

```text
W0 baseline
  require empty packet-event queue
  require no focal pulse-contact or feedback-eligibility rows
  retain baseline snapshot and participant/budget state

W1 writer
  schedule exactly one registered writer packet
  step() commits the writer departure
  step() commits the linked writer arrival
  require the packet-event queue to return to empty

W2 medium materialization
  select the writer-arrival route-local-pulse-contact row
  emit exactly one feedback-eligibility row linked to that source digest
  retain the post-writer, post-medium, pre-reader branch-point snapshot

W3 later opportunity
  restore the registered branch point
  configure exactly one registered reader/opportunity profile
  invoke the feedback producer exactly once

W4 response
  if the producer records a native scientific rejection, terminate the branch
  if it schedules, step() commits the linked reader-packet departure
  then step() commits the linked reader-packet arrival
  terminate after native arrival eligibility is recorded and the queue is empty
```

The four opportunities repeat `W3`–`W4` from independent restorations of the
same cell/seed branch point. `W0`–`W2` execute once per cell/seed, not once per
reader branch.

### 11.4 Native timing and ownership rules

- `arrival_event_time_key` remains unset for writer and reader packets unless a
  later registered variant explicitly reopens this decision. Native edge delay
  derives arrival time.
- `step()` consumes exactly one queued native event. The writer window
  therefore contains exactly two committed packet events, and a scheduled
  reader response contains exactly two.
- The producer may evaluate exactly once per branch. A negative native reason
  code ends that branch without manufacturing departure or arrival events.
- `run_autonomous(...)`, a second producer call, a second response packet, and
  unrelated queued work are outside the window.
- An unexpected event, non-empty required boundary queue, or extra focal row is
  an invalid fixture or control outcome; the harness may not silently extend
  the window to consume it.
- Exact event IDs, scheduler indices, `event_time_key` values, and native edge
  delays must be materialized in the concrete fixture/profile records according
  to `P2-I1-DEC-010` and `P2-I1-DEC-011`.

### 11.5 Causal-order assertions

Every branch must machine-verify:

```text
baseline checkpoint
  < writer departure
  < writer arrival
  < selected pulse-contact row
  < feedback-eligibility row
  < reader producer evaluation
  < scheduled reader departure, when any
  < committed reader departure, when any
  < committed reader arrival eligibility, when any
```

Ordering uses the applicable native checkpoint, scheduler-event, event-queue,
and lineage fields rather than authored timestamps. Each later record must
reference its immediate causal predecessor and the accepted medium-history
digest.

### 11.6 Response termination and missingness

A branch has a valid scientific `0` when the single producer evaluation returns
a registered scientific reason such as subthreshold, wrong polarity, or a
declared control-induced absence and all prerequisite/control checks remain
valid. It has a valid scientific `1` only after the linked native arrival
eligibility is committed.

A scheduled packet that fails to complete both native events inside `W4` is not
a scientific zero. It is operationally non-evaluable or structurally
unavailable according to the frozen failure classifier. Missing runtime,
failed restoration, unexpected queue work, or exhausted event bounds cannot
support or refute the lane.

### 11.7 Claim boundary

This policy establishes strict causal laterness: the medium history is
committed before the reader producer observes it, and reader arrival follows
that observation through native queue processing. It does not establish:

- persistence across an idle or externally chosen duration;
- decay or reinforcement;
- repeated access in one continuous history;
- multi-hop propagation; or
- an ecology regime.

Those are valid linked probes if the minimal cycle shows that temporal depth
rather than immediate causal ordering is the next discriminator.

### 11.8 Reopening conditions

Reopen `P2-I1-DEC-009` if:

- source-current native packet processing requires more or fewer committed
  events for the registered one-edge writer or reader route;
- the branch-point snapshot cannot preserve an empty queue plus the accepted
  medium history;
- producer rejection cannot be distinguished from operational failure;
- native edge-delay derivation cannot be reconstructed exactly;
- one producer evaluation cannot expose the accepted formation response; or
- evidence shows that an explicit persistence interval is necessary to answer
  L01 rather than a stronger trace-oriented question.

## 12. `P2-I1-DEC-010` — Fixture topology, ownership, and canonical identity

**Status:** accepted and complete at decision level; generated digests remain
implementation outputs

**Question IDs:** resolves `L01-Q17`; opened `L01-Q18`, now resolved by
`P2-I1-DEC-011`

### 12.1 Decision question

What is the smallest fixture topology that provides:

- one registered surviving participant source pole;
- one participant-originated writer event;
- two structurally symmetric, distinct later readers;
- one non-private medium history accessible to both reader branches; and
- a valid native route-aspect identity without importing an existing test
  helper as runtime code?

### 12.2 Options considered

| Fixture source | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| RCAE-owned symmetric four-node fixture | Satisfies source-pole identity, writer separation, two matched readers, and one shared history with minimal topology | Constructed and fixture-local until transfer | **Accepted** |
| Source-current three-node feedback test fixture | Demonstrates the native feedback API | Provides only one clean later-reader route and no adequate paired-reader symmetry | Design evidence only |
| Two-pole native packet-loop example | Supplies a registered route-aspect pattern | Provides one reader context and tests looping rather than shared reader access | Design evidence only |
| N29/N30-scale inherited fixture | Gives stronger continuity with prior experiments | Adds transfer and reconstruction complexity before the minimal relation is known | Deferred transfer contrast |
| Graph-project test-helper import | Minimizes local code | Makes private test layout a runtime dependency and violates portable ownership | Rejected |

### 12.3 Accepted logical topology

```text
                         writer channel
participant/source P  -------------------->  writer sink W
        ^                                      |
        |--------------- return ---------------|
        |
        |------------- reader route ----------> reader A
        |
        |------------- reader route ----------> reader B
```

The fixed topology contains four non-overlapping logical node roles:

```text
P = participant and source-pole region
W = writer sink and feedback front region
A = later reader context A
B = later reader context B
```

It contains four directed edge roles:

```text
P -> W = registered writer channel
W -> P = route-aspect return channel
P -> A = later reader route A
P -> B = later reader route B
```

The return channel exists only to close the source-current two-pole
`LGRC9V3RouteAspect` identity. It is not scheduled during the primary cycle and
must have no packet, producer, or surface activity in retained execution
records.

### 12.4 Participant route aspect

The registered route aspect has:

```text
source pole S = {P}
writer pole K = {W}
channel sequence = (participant_to_writer, writer_return)
closed_loop = true
```

The primary writer uses `participant_to_writer`. The route aspect and
source-pole region supply the participant identity projection accepted by
`P2-I1-DEC-002`. Reader routes remain declared fixed-topology edges but are not
added as extra route-aspect channels merely to make the participant identity
contain every later possibility.

### 12.5 Shared-medium geometry

The accepted feedback masks are:

```text
front_node_roles = {W}
rear_node_roles = {A, B}
```

The participant-originated writer changes the front region through native
packet arrival. Neither reader appears as a target, expected route, next
channel, selectivity label, or success field in the feedback row. Both
counterfactual reader contexts consume the same retained feedback-row digest.

Reader A and reader B must have matched topology burden: one direct edge from
`P`, equal declared edge-policy class, and equal baseline reader viability.
Their logical-role difference supplies contexts A and B; it may not create an
unrecorded exposure or support difference.

### 12.6 Four opportunity profiles

The logical allocation from `P2-I1-DEC-007` becomes:

```text
context A:
  P -> A with history-aligned expected polarity
  P -> A with inverted expected polarity

context B:
  P -> B with history-aligned expected polarity
  P -> B with inverted expected polarity
```

The four profiles remain independent branches. Within a context, polarity is
the only changed producer field. Across contexts, reader target identity is the
only intended distinction; numeric route, support, timing, and packet fields
must be matched unless a later decision explicitly declares a candidate-blind
context contrast.

### 12.7 Ownership and portability

RCAE owns a portable, experiment-local declarative fixture and its builder,
configuration, profile IDs, digests, and reconstruction instructions. The
builder may use only public surfaces from the locally configured PyGRC runtime.
It may not:

- import graph-project tests, examples, or private helpers at runtime;
- copy or patch PyGRC implementation code;
- write to the graph repository;
- treat source-current tests as P2-I1 execution evidence; or
- hide machine-local runtime location in a shared configuration.

Graph-project tests and examples remain read-only design evidence. PyGRC owns
native topology/state types, route-aspect validation, packet processing,
surface rows, feedback production, snapshots, and lineage validation.

### 12.8 Claim boundary

The four-node topology and polarity-susceptibility relation are constructed
RCAE mechanisms over native PyGRC surfaces. A positive primary result is
therefore fixture-local and constructed until transfer and admission gates say
otherwise. It cannot establish that PyGRC natively supplies niche formation,
participant-intrinsic selectivity, or a reusable ecology primitive.

The construction is nevertheless legitimate outbound evidence: if it exposes
a stable relation or tension, that can become a precise future LGRC demand.

### 12.9 Canonical topology and route identities

Canonical IDs remain fixed across every seed and cell:

```text
fixture_id = rcae_p2_i1_four_node_v1

nodes:
  0 = P
  1 = W
  2 = A
  3 = B

edges and ports:
  0 = P:0 -> W:0
  1 = W:1 -> P:1
  2 = P:2 -> A:0
  3 = P:3 -> B:0

route_aspect_id = rcae_p2_i1_participant_writer_loop_v1
direction = custom
pole_regions = {S: [0], K: [1]}
channel_sequence = [participant_to_writer, writer_return]
closed_loop = true
```

`participant_to_writer` uses edge `0`, and `writer_return` uses edge `1`.
Their `expected_next_channel_id` fields point to each other. Generated topology,
pole-region, and route-aspect digests are recorded from public PyGRC artifacts;
the decision record does not invent their values.

### 12.10 Canonical reader profiles and resolution

```text
ctx-a-aligned:
  source_node_id = 0
  target_node_id = 2
  edge_id = 2
  expected_polarity = positive

ctx-a-inverted:
  source_node_id = 0
  target_node_id = 2
  edge_id = 2
  expected_polarity = negative

ctx-b-aligned:
  source_node_id = 0
  target_node_id = 3
  edge_id = 3
  expected_polarity = positive

ctx-b-inverted:
  source_node_id = 0
  target_node_id = 3
  edge_id = 3
  expected_polarity = negative
```

All four use the packet, threshold, timing, and mask fields frozen by
`P2-I1-DEC-011`; `expected_next_route_id` and
`expected_next_channel_id` remain unset.

Each static `opportunity_profile_digest` includes a symbolic reference to the
accepted branch pulse-contact digest rather than a candidate-derived digest.
Each run also emits a `resolved_opportunity_profile_digest` containing the
actual accepted pulse-contact and medium-history digests. Cross-cell matching
uses the static digest; causal reconstruction uses the resolved digest.

Portable seed-specific lineage IDs are:

```text
rcae-p2-i1-seed-{seed}-participant-P
rcae-p2-i1-seed-{seed}-reader-A
rcae-p2-i1-seed-{seed}-reader-B
```

### 12.11 Writer-reader relation and claim boundary

```text
writer_reader_relation = distinct_carrier
read_mode = participant_mediated_configured_producer
sharedness_ceiling = shared_local_counterfactual_access
self_aftereffect_control = mandatory
```

The receiving carriers A and B are distinct from writer P, but P remains the
source of the later response packet and the configured producer reads the
medium on its behalf. This is not an autonomous reader consuming the medium.
Until the mandatory self-aftereffect control resolves, the maximum
interpretation is participant self-conditioning with a distinct recipient,
not shared niche conditioning.

### 12.12 Reopening conditions

Reopen `P2-I1-DEC-010` if:

- the four directed edge roles cannot be represented and replayed through
  public PyGRC topology/state surfaces;
- the two-pole route aspect cannot coexist with the two reader routes without
  hidden route activity;
- the return channel affects the primary cycle despite being unscheduled;
- A and B cannot maintain matched baseline viability and exposure;
- the feedback row cannot use `{W}` and `{A, B}` without reader addressing; or
- the static-versus-resolved profile digest split cannot preserve cross-cell
  matching and runtime lineage simultaneously;
- participant-mediated reading cannot be distinguished from autonomous reader
  access or participant self-aftereffect; or
- a smaller source-current fixture satisfies all accepted identities and
  controls without losing the two-context discriminator.

## 13. `P2-I1-DEC-011` — Numeric base fixture and result reading

**Status:** accepted

**Question IDs:** resolves `L01-Q18`; opens `L01-Q19`

### 13.1 Decision question

Which analytically defined numeric base state instantiates the accepted
four-node topology without consuming candidate outcomes, and how should the
specific result be read relative to its configured thresholds without turning
one crossing into a simplistic scientific verdict?

### 13.2 Accepted dyadic base state

```text
initial node coherence:
  P = 1.000
  W = 1.000
  A = 0.500
  B = 0.500

every fixed edge:
  conductance = 1.000
  geometric_length = 1.000
  temporal_delay = 1.000
  flux_coupling = 0.000

writer packet:
  amount = 0.250
  departure_event_time_key = 1.000
  arrival_event_time_key = unset

reader packet:
  amount = 0.125
  departure_event_time_key = native current frontier
  arrival_event_time_key = unset

feedback surface and producer:
  reference_delta = 0.000
  feedback_threshold = 0.125
  producer_threshold = 0.125

native budget tolerance:
  epsilon_budget = 1e-9
```

All selected coherence, packet, delay, and threshold values are dyadic
fractions except the inherited native budget tolerance. This reduces avoidable
representation ambiguity without claiming language-neutral canonicalization.

### 13.3 Candidate-blind derivation

The base-state polarity arithmetic is preregistered rather than learned from a
candidate run:

```text
baseline polarity = W - (A + B)
                  = 1.000 - 1.000
                  = 0.000

constructed post-writer polarity = (W + writer_amount) - (A + B)
                                 = 1.250 - 1.000
                                 = 0.250

configured mechanism threshold =
  midpoint(baseline polarity, constructed post-writer polarity)
  = 0.125
```

The expected values are fixture calculations, not P2-I1 evidence. Runtime
agreement must still be observed and reconstructed. Runtime disagreement is a
realization tension or implementation finding; it does not authorize threshold
tuning inside the cycle.

### 13.4 Participant viability and budget

```text
M0 = 1.000
Dw = 0.250
Mt = M0 - Dw = 0.750
Dr = 0.125

Mt >= M0 - Dw - epsilon_budget
Mt >= Dw - epsilon_budget
Mt >= Dr - epsilon_budget
```

The one-repeat reserve from `P2-I1-DEC-002` is therefore satisfied by the base
fixture with visible slack. Each independent reader branch pays at most one
reader-packet debit; the four branches never accumulate those debits in one
participant history.

Every event boundary retains native node-plus-packet budget before, after, and
error. The budget equation is not a measure of niche strength.

### 13.5 P2-I1 result-reading rule

The configured feedback threshold determines whether the native producer
schedules a packet. It does not, by itself, determine whether P2-I1 succeeds or
fails. Each evaluation retains:

```text
observed_signed_feedback
configured_threshold
signed_threshold_distance = observed_signed_feedback - configured_threshold
native_reason_code
native_transition_occurred
```

Interpretation considers threshold distance together with formation coverage,
per-seed margins, selectivity pairs, controls, lineage, support, and unexpected
properties. A narrow miss may still expose an adequate structural relation and
motivate a frozen local refinement or alternative realization. A narrow
crossing is not strong merely because scheduling occurred. Any refinement is a
new linked cycle and preserves the original result.

The same reading applies to the already selected `0.5` selectivity resolution,
strict positive primary direction, and calibrated `delta`: they locate the
specific result on a ladder rather than deciding the conclusion alone.

### 13.6 Integrity boundaries

Budget conservation, runtime identity, schema validity, causal lineage,
cross-branch isolation, unsafe-side-effect checks, provenance, reconstruction,
and repository boundaries remain fail-closed. Their failures are retained as
blocked, incomplete, unsafe, or implementation findings; they are not softened
by an otherwise interesting threshold-relative result.

### 13.7 Reopening conditions

Reopen the numeric base fixture if:

- public PyGRC construction or native packet processing cannot represent the
  values exactly enough for the declared tolerance;
- the source-current feedback score uses a different native formula;
- reader A and B do not remain baseline-matched under the declared state;
- native edge-delay derivation disagrees with the one-edge window assumptions;
  or
- seed realization cannot preserve participant reserve and polarity-role
  meaning across every registered seed.

Candidate success, failure, or proximity to the configured threshold is not by
itself a reopening condition.

## 14. `P2-I1-DEC-012` — Live-seed variation

**Status:** accepted

**Question IDs:** resolves `L01-Q19`

### 14.1 Decision question

How should seeds `101`, `211`, and `307` vary the base state enough to expose
local numeric sensitivity without turning seed machinery into a second
experiment?

### 14.2 Accepted balanced offsets

```text
seed 101: u = -1/32
seed 211: u =  0
seed 307: u = +1/32

P_s = 1 + u
W_s = 1 - u
A_s = 0.5
B_s = 0.5
```

All other fixture, packet, edge, threshold, mask, timing, and profile fields
remain unchanged. The offsets preserve total coherence `3.0`, exact A/B reader
matching, and the participant reserve.

The expected preregistration calculations are:

| Seed | Baseline polarity | Constructed post-writer polarity | Expected distance from `0.125` threshold |
| --- | ---: | ---: | ---: |
| `101` | `+0.03125` | `0.28125` | `+0.15625` |
| `211` | `0.00000` | `0.25000` | `+0.12500` |
| `307` | `-0.03125` | `0.21875` | `+0.09375` |

These calculations are fixture expectations, not candidate evidence. Observed
native values and threshold distances remain authoritative.

### 14.3 Seed meaning

The three seeds test deterministic reconstruction and local numeric robustness
around one constructed fixture. They are not independent ecological lineages
and cannot establish broad transfer or cross-lane recurrence. Exact reruns are
reconstruction checks rather than additional scientific seeds.

Numeric node, edge, and port identities stay canonical across seeds. Label
permutation is unnecessary for the scientific result and may be tested later
as ordinary implementation validation if a concrete label-dependence concern
appears.

### 14.4 Reopening conditions

Reopen `P2-I1-DEC-012` if any offset breaks participant reserve, reader
matching, medium geometry, native reconstruction, or the intended bounded
neighborhood. An observed narrow crossing or miss is interpreted as a result;
it does not authorize changing the offsets inside the cycle.

## 15. `P2-I1-DEC-013` — Candidate-blind matched null

**Status:** accepted; generator implementation and retained calibration
artifacts remain open

**Question IDs:** resolves `L01-Q06`

### 15.1 Decision question

What matched-null input measures the numerical resolution of the exact P2-I1
aggregation and normalization path without running PyGRC, inspecting candidate
outcomes, or creating a weakened candidate condition?

### 15.2 Options considered

| Null family | Strength | Main problem | Disposition |
| --- | --- | --- | --- |
| Identical synthetic panels spanning all formation fractions | Exercises the complete discrete response domain through the real analysis path | Measures analysis resolution, not runtime behavior | **Accepted** |
| Two live identical PyGRC reference branches | Exercises runtime construction | Adds runtime and registration dependencies to a resolution-only calibration and can resemble a scientific control | Rejected for metric calibration |
| No-history or weakened-writer runtime | Looks ecologically relevant | Is a scientific/null condition rather than matched numerical resolution | Rejected; belongs in the comparison matrix |
| Random synthetic noise | Can produce a nonzero band | Invents resolution not supplied by the measurement process | Rejected |
| Phase 1 hand-written example margins | Already accepted by tooling tests | Are illustrative fixtures without P2-I1 generator provenance | Rejected as P2-I1 calibration input |

### 15.3 Frozen synthetic panels

The calibration seeds map to two identical four-opportunity vectors:

| Seed | `null_a` and `null_b` | Formation fraction |
| --- | --- | ---: |
| `19` | `[0, 0, 0, 0]` | `0.00` |
| `43` | `[1, 0, 0, 0]` | `0.25` |
| `71` | `[1, 1, 0, 0]` | `0.50` |
| `109` | `[1, 1, 1, 0]` | `0.75` |
| `163` | `[1, 1, 1, 1]` | `1.00` |

The `0` and `1` values are synthetic analysis inputs. They are not observed
opportunities, runtime facts, candidate outcomes, or lane evidence.

For every seed, the frozen analysis code must derive:

```text
formation_fraction(null_a) = formation_fraction(null_b)
raw_paired_difference = 0
matched_null_margin = 0
```

The expected resolution freeze is therefore:

```text
delta = max(measurement_resolution, max(abs(matched_null_margin)))
      = max(1e-12, 0)
      = 1e-12
```

Expected zero margins and `delta` are preregistration calculations. Generated
artifacts remain authoritative. Any nonzero finite margin is retained and
enters `delta`; it is an analysis implementation finding, not candidate
evidence.

### 15.4 Execution and claim boundary

This generator is explicitly:

```text
runtime_execution = false
pygrc_imported = false
candidate_blind = true
evidence_effect = resolution_only_no_candidate_evidence
```

It exercises the same RCAE opportunity aggregation, identity orientation, raw
paired difference, normalized denominator, and margin serialization that later
analyze live results. It does not test PyGRC availability, native packet
processing, causal lineage, or runtime variability. Those remain execution and
control observations and may not be folded into metric `delta`.

### 15.5 Candidate-blind provenance

Before calibration, retain and digest:

- the portable generator/analysis script and exact command;
- the frozen panel specification above;
- calibration seeds `19`, `43`, `71`, `109`, and `163`;
- script, input, output, aggregation-policy, and metric-sheet digests;
- Python/dependency and command profiles;
- source revisions and resource envelope; and
- explicit absence of candidate artifacts, candidate seeds `101`, `211`, and
  `307`, PyGRC runtime inputs, and post-outcome tuning.

The current Phase 1 fixture containing illustrative nonzero margins remains a
tooling test fixture. P2-I1 must generate a new calibration input and may not
copy those hand-written margins into the resolution freeze.

### 15.6 Result reading

The frozen `delta` locates later observed margins on the existing robust,
narrow, resolution-limited, mixed, and counter-directional ladder. It does not
accept or reject P2-I1, compensate for failed controls, or erase raw formation
coverage.

### 15.7 Reopening conditions

Reopen `P2-I1-DEC-013` if:

- live-result analysis cannot use the same aggregation and normalization code
  as calibration;
- the primary response ceases to have the five discrete formation fractions;
- identical panel inputs cannot be distinguished from candidate evidence in
  retained artifacts;
- a deterministic analysis operation produces non-finite margins; or
- a genuine nonzero measurement-resolution source exists that this generator
  does not exercise.

## 16. `P2-I1-DEC-014` — Analysis identity boundary

**Status:** accepted; files, tests, hashes, and generated identity manifest
remain open implementation work

**Question IDs:** resolves `L01-Q20`

### 16.1 Decision question

What is the smallest portable code and policy boundary that lets the same
deterministic analysis process synthetic calibration panels and live
opportunity records while keeping PyGRC execution, file I/O, and scientific
logic visibly separate?

### 16.2 Accepted layout

```text
scripts/p2_i1.py
  thin command-line and file-I/O boundary

scripts/p2_i1_analysis.py
  pure deterministic P2-I1 analysis
  no PyGRC import, runtime construction, or machine-local path

configs/p2_i1_analysis_policy.json
  one frozen policy with separately digested projections
```

This follows the existing experiment-local script pattern without adding an
installable package or reusable `src/` surface before admission.

### 16.3 Responsibility split

The pure analysis module owns:

- opportunity status and missingness validation;
- binary formation and seed-fraction aggregation;
- identity orientation, raw paired difference, and normalized margin;
- feedback-threshold distance retention;
- matched polarity-pair selectivity interactions;
- candidate-blind matched-null panel generation;
- boundary-rung inputs; and
- terminal-classifier inputs.

It reuses existing Phase 1 calibration, resolution-relation, schema, and
canonical-digest functions where their frozen semantics already fit. It does
not copy the whole Phase 1 tooling API or silently change those semantics.

The CLI owns argument parsing, portable input/output paths, JSON loading and
writing, command-profile emission, and user-facing errors. It may not recompute
scientific values outside the analysis module.

The later runtime harness owns PyGRC binding and raw opportunity/causal records.
It may call neither a hidden alternative analyzer nor a success classifier.

### 16.4 One policy, three projections

`p2_i1_analysis_policy.json` contains at least:

```text
aggregation_policy
rung_classifier_policy
terminal_classifier_input_policy
```

The identity builder derives three canonical projection digests from that one
file:

```text
aggregation_policy_digest
rung_classifier_digest
terminal_classifier_digest
```

Separate policy files are unnecessary. Unknown fields fail closed, and one
projection cannot read fields owned only by another projection.

### 16.5 Generated analysis identity

Before matched-null calibration, generate and retain one identity manifest
containing:

```text
analysis_script_path = scripts/p2_i1_analysis.py
analysis_script_sha256
analysis_policy_path = configs/p2_i1_analysis_policy.json
analysis_policy_digest
aggregation_policy_digest
rung_classifier_digest
terminal_classifier_digest
cli_path = scripts/p2_i1.py
cli_sha256
```

The analysis-source hash plus policy projections form measurement identity.
The CLI hash and command profile remain reproducibility identity. This means a
help-text-only CLI edit does not change the scientific formulas, while any
input parsing or serialization edit remains visible and reviewable.

### 16.6 Shared calibration/live path

The matched-null generator from `P2-I1-DEC-013` and later live-result analysis
must call the same public functions in `p2_i1_analysis.py` for aggregation,
orientation, differences, normalization, and serialization-ready analysis
records. Calibration-only code may construct synthetic inputs but may not
maintain a second formula implementation.

### 16.7 Change control and evidence boundary

After CAL-PRE/CAL:

- changing the analysis module or any scientific policy projection requires a
  new CAL-PRE/CAL cycle and affected rerun;
- changing CLI behavior that affects parsing, serialization, commands, or
  artifacts requires updated reproducibility identity and review;
- changing comments or help text alone does not change measurement identity;
  and
- no analysis identity or passing test supplies lane evidence.

### 16.8 Reopening conditions

Reopen `P2-I1-DEC-014` if:

- synthetic calibration and live analysis cannot use the same functions;
- importing existing Phase 1 functions creates circular or side-effectful
  behavior;
- one policy file cannot keep its three projections unambiguous;
- runtime records cannot remain raw until the separate analysis step; or
- the two-file Python boundary becomes materially harder to reproduce than one
  self-contained script without improving auditability.

## 17. `P2-I1-DEC-015` — Participant/medium separation

**Status:** accepted; control implementation and execution remain open

**Question IDs:** resolves `L01-Q08`; constrains `L01-Q09`

### 17.1 Decision question

Are participant P and the accepted medium operationally separable, and what
comparison distinguishes a load-bearing medium history from P merely reacting
to its own writer debit or the post-writer node state?

### 17.2 Accepted relation

```text
participant_carrier = node P plus registered source-pole lineage
medium_carrier = model-owned pulse-contact -> feedback-eligibility history
carrier_relation = operationally_separated
read_mode = participant_mediated_configured_producer
co_constitution_claimed = false
```

P and the medium have distinct state, identity, lineage, and intervention
surfaces. However, P remains both the writer and the source of the later reader
packet. Operational separation therefore does not establish autonomous reader
access or eliminate participant self-aftereffect by definition.

### 17.3 State-matched medium-absent control

The primary comparison freezes two branches with identical:

- P/W/A/B post-writer coherence and total native budget;
- committed writer departure and arrival history;
- selected writer-arrival pulse-contact row;
- empty packet queue at the branch point;
- P continuity/reserve and reader A/B opportunity profiles; and
- topology, masks, timing, support, seeds, and producer configuration.

They differ only in feedback-medium materialization:

```text
candidate:
  emit exactly one accepted feedback-eligibility row

state-matched medium-absent control:
  do not emit the feedback-eligibility row
```

Both branches use public PyGRC construction and event surfaces. RCAE may not
obtain the control by deleting or editing a row in an existing runtime state.
The control preserves the committed pulse-contact row so it specifically tests
the accepted two-row medium rather than removing the writer event or its native
contact history.

The later producer is invoked once in both branches. In the control, a native
no-feedback-row reason is a valid scientific control outcome only when runtime,
participant opportunity, queue, state matching, and all control guards remain
valid.

### 17.4 What the control establishes

If candidate and control differ as expected, the feedback-medium row is
load-bearing beyond P's writer debit and the resulting node-coherence state. If
they do not differ, the apparent relation is state-carried, participant-carried,
producer-carried, or absent.

This control establishes row dependence, not history-content dependence.
`L01-Q09` must still show that the accepted source digest, ordering, and content
matter rather than the mere presence of any feedback row.

### 17.5 Self-aftereffect and claim ceiling

The state match controls P's private coherence change as a sufficient cause,
but P still performs the configured read and later production. Therefore, even
after a positive control difference:

```text
maximum_without_stronger_reader_control =
  participant-mediated conditioning with distinct recipients
```

The result may expose shared-local counterfactual accessibility of the medium
surface, but it may not claim autonomous reader consumption or a fully shared
niche. A later linked probe may introduce an independent response-source
carrier or native reader-susceptibility surface if that stronger discriminator
becomes necessary.

### 17.6 Outcome reading

| Observation | Interpretation |
| --- | --- |
| Candidate forms; state-matched control does not | Medium row is load-bearing; proceed to history-content controls and retain participant-mediated ceiling |
| Both form | Medium row is unnecessary or bypassed; intended niche-conditioning relation is not established |
| Neither forms | Realization is absent, narrow, blocked, or otherwise below the intended relation; use threshold proximity and failure records |
| Control cannot preserve state/opportunity | Separation remains blocked or missing-surface; do not infer a negative result |

### 17.7 Reopening conditions

Reopen `P2-I1-DEC-015` if:

- the feedback row cannot be withheld without changing writer/contact history;
- absence of the row cannot produce an auditable native reason;
- candidate and control cannot maintain identical post-writer node state,
  queue, budget, and later opportunity;
- P's private state influences the producer through an unrecorded path; or
- an independent response-source carrier becomes necessary for the minimum L01
  claim rather than a stronger follow-up.

## 18. `P2-I1-DEC-016` — History-content causality

**Status:** accepted; implementation and execution remain open

**Question IDs:** resolves `L01-Q09`

### 18.1 Decision question

What comparisons show that the accepted feedback medium depends on its
specific content, source contact, and causal order rather than merely the
presence of any feedback row or producer invocation?

### 18.2 Existing-cell allocation

No comparison cell is added. The existing finite matrix carries three distinct
tests:

| Cell or guard | Changed relation | Preserved relation |
| --- | --- | --- |
| `reference` | Writer contribution to feedback content is neutralized | Writer/contact history, one feedback row, node state, opportunity, and producer remain |
| `medium-freeze-withdrawal` | Feedback row is absent | Post-writer node state, writer/contact history, participant opportunity, and producer remain |
| `trace-shuffle` | Producer expects the writer-departure contact digest while the feedback row links writer arrival | Row quantity/content, node state, opportunity, timing envelope, and producer remain |
| causal-order guard | Reject any chain not ordered contact → feedback → producer → response | All valid candidate and control records |

### 18.3 Neutral-content reference

The reference cell uses:

```text
feedback_reference_delta = 0.250
```

This subtracts the analytically registered writer contribution from the
feedback score. With the three seed offsets from `P2-I1-DEC-012`, the retained
reference scores are the seed baseline polarities:

| Seed | Reference score after subtraction | Distance from positive `0.125` threshold |
| --- | ---: | ---: |
| `101` | `+0.03125` | `-0.09375` |
| `211` | `0.00000` | `-0.12500` |
| `307` | `-0.03125` | wrong polarity for the aligned profile |

The reference is therefore content-neutral relative to the writer
contribution, not numerically forced to zero for every seed. It retains one
feedback row and the same writer/contact/node history as the candidate.

### 18.4 Source-lineage mismatch

The candidate feedback row is natively linked to the writer-arrival
`route_local_pulse_contact` digest. In `trace-shuffle`, the producer's
`expected_source_surface_digest` is instead the earlier writer-departure
contact digest from the same runtime history.

This changes one declared relation without copying, injecting, or mutating a
surface row. It preserves row count, feedback content, masks, thresholds,
packet amounts, post-writer node state, and opportunity profiles. The expected
native outcome is the auditable feedback order/source mismatch reason.

This control tests a configured lineage guard. A positive result remains
constructed history dependence; it does not prove that native feedback content
would autonomously select its own historical source.

### 18.5 Causal order

Every valid chain must machine-verify:

```text
writer departure contact
  < writer arrival contact
  < accepted feedback row
  < single producer evaluation
  < response departure, when scheduled
  < response arrival eligibility, when scheduled
```

The ordering uses native scheduler, event, source-digest, and lineage fields.
An absent, reversed, duplicated, or authored-only link invalidates the causal
chain. The harness may not repair order by rerunning the producer after seeing
an outcome.

### 18.6 Joint interpretation

| Observation | Interpretation |
| --- | --- |
| Candidate differs from both neutral-content reference and row-absent control | Feedback materialization and writer-relative content are load-bearing; proceed subject to source/order controls |
| Candidate differs only from row-absent control | Row presence matters, but writer-relative content is not established |
| Trace-shuffle still forms | Exact source lineage is not load-bearing or the guard is bypassed |
| Trace-shuffle blocks with the registered native mismatch reason | Configured source-lineage binding is load-bearing |
| Causal order cannot be reconstructed | No history-conditioned claim, regardless of formation magnitude |

Threshold proximity and raw opportunity coverage remain visible. No single
comparison decides the terminal result alone.

### 18.7 Reopening conditions

Reopen `P2-I1-DEC-016` if:

- `reference_delta=0.250` does not isolate the registered writer contribution;
- the departure and arrival contact digests cannot be distinguished natively;
- `expected_source_surface_digest` does not produce an auditable mismatch;
- the trace-shuffle changes feedback content or opportunity fields beyond the
  declared source relation;
- native ordering fields cannot reconstruct the full chain; or
- a row-presence effect remains scientifically interesting but requires a
  different medium definition.

## 19. `P2-I1-DEC-017` — Support context and contrast

**Status:** accepted; implementation and execution remain open

**Question IDs:** resolves `L01-Q10`

### 19.1 Decision question

What support carries any observed formation, and how can the existing
`parent-context-contrast` cell vary support without pretending that the
four-node fixture contains a genuine parent basin?

### 19.2 Support account

Native PyGRC support consists of:

- live fixed-topology nodes and reader edges;
- P's coherence and packet budget;
- native queue, event, surface, snapshot, and lineage state;
- LGRC-2 causal-pulse surface availability; and
- native feedback-producer and packet-arrival processing.

Constructed RCAE support consists of the fixture, front/rear masks, feedback
emission parameters, configured producer profiles, independent branch
orchestration, controls, and analysis. That support remains explicit even when
the native runtime performs every registered transition.

No parent basin is present. `parent_context = absent_not_represented`; the
contrast may supply only support-scale information.

### 19.3 Score-preserving reduced-support contrast

For every seed, apply one scalar support offset:

```text
c = -0.250

P_support = P_seed
W_support = W_seed + 2c
A_support = 0.500 + c
B_support = 0.500 + c
```

Therefore:

```text
W_support = 0.500 - u_seed
A_support = 0.250
B_support = 0.250

post-writer W_support = 0.750 - u_seed
post-writer feedback score =
  (0.750 - u_seed) - (0.250 + 0.250)
  = 0.250 - u_seed
```

The feedback score and its threshold distance exactly match the candidate for
each seed, while the W/A/B support mass is reduced by `1.000`. P, participant
reserve, writer/reader packet amounts, topology, edge policies, masks, timing,
medium/source rules, and four reader profiles remain unchanged.

### 19.4 Single-axis meaning

The registered axis is `absolute_environmental_support_scale`. Although three
node values change, they are one score-preserving transformation controlled by
the single scalar `c`. No threshold, packet, delay, route, mask, or producer
field may be adjusted to rescue the contrast.

### 19.5 Outcome reading

| Observation | Interpretation |
| --- | --- |
| Formation and controls remain comparable | Bounded invariance to this reduced support scale |
| Formation or arrival changes while score remains matched | Support-dependent or fixture-locked relation; retain the changed stage and threshold proximity |
| Participant reserve or reader opportunity fails | Invalid support contrast or missing prerequisite, not scientific refutation |
| A parent/local distinction becomes necessary | Redirect the missing distinction to L07; do not promote this cell to parent-basin evidence |

This contrast does not naturalize the RCAE fixture, masks, producer
configuration, or branching scaffold. It only asks whether the observed
relation depends on the selected absolute support scale.

### 19.6 Reopening conditions

Reopen `P2-I1-DEC-017` if:

- the transformation fails to preserve candidate feedback score for every
  seed;
- A or B ceases to be a valid reader before the medium intervention;
- P reserve, edge policy, or packet opportunity changes unintentionally;
- more than the declared support-scale axis changes; or
- the lane requires an actual parent/local distinction rather than this active
  support null.

## 20. Decision-to-execution projection

This section is navigation, not a second authority. Accepted decisions govern
meaning; generated configs, manifests, and records will govern exact execution
identity once frozen.

```text
decision record
  -> fixture, cell, control, and analysis configs
  -> CAL-PRE review and generated identity hashes
  -> candidate-blind calibration
  -> PyGRC runtime registration
  -> seven cells x three seeds x four opportunities
  -> pure machine analysis
  -> developmental interpretation and next move
```

| Cell | Decision-derived intervention | Must remain matched | Authority/status |
| --- | --- | --- | --- |
| `reference` | Subtract writer contribution with `reference_delta=0.250`; retain one feedback row | Writer/contact/node state, opportunity, producer, masks, timing | `DEC-016`; decided |
| `candidate-conditioning` | Accepted writer-relative feedback history | Frozen fixture, seeds, profiles, runtime and analysis identity | `DEC-001`–`016`; decided |
| `medium-freeze-withdrawal` | Withhold feedback row from identical post-writer/contact state | Participant state/reserve, writer history, opportunity, producer | `DEC-015`; decided |
| `trace-shuffle` | Expect departure-contact digest while row links arrival contact | Feedback content/quantity, node state, opportunity, timing | `DEC-016`; decided |
| `parent-context-contrast` | Apply `c=-0.250` score-preserving reduced-support transform | P reserve, score, packet, topology, masks, timing, profiles | `DEC-017`; decided; no parent claim |
| `susceptibility-inversion` | Swap aligned/inverted expected polarity between stable reader slots | Reader identity, medium exposure, opportunity, threshold | `DEC-007`, `DEC-010`; decided |
| `carrier-timescale-contrast` | Double reader-packet amount from `0.125` to `0.250` | Writer, medium, threshold, delay, topology, profiles, seeds, analysis | `DEC-018`; decided |

The runtime harness emits raw native and causal records only. The analysis
boundary from `DEC-014` derives formation fractions, paired margins,
selectivity interactions, rung inputs, and terminal inputs. Interpretation
then asks what appeared, what carried it, what remained blocked, and which
single next move follows. Alternative combinations remain linked probe cycles
and never overwrite this primary projection.

## 21. `P2-I1-DEC-018` — Carrier-load contrast

**Status:** accepted; implementation and execution remain open

**Question IDs:** resolves `L01-Q21`

### 21.1 Decision question

Which one carrier or timescale axis gives the final comparison cell useful
information without turning it into an open transfer search or merely
retesting deterministic queue delay?

### 21.2 Options considered

| Axis | Information gained | Main limitation | Disposition |
| --- | --- | --- | --- |
| Double later reader-packet amount | Tests whether the formed opportunity survives a larger carrier burden within the accepted reserve | Remains one local fixture/load contrast | **Accepted** |
| Double reader-edge delay | Tests post-read arrival timing | Mostly rechecks queue timing after the medium has already been read | Deferred |
| Delay medium read | Would test persistence | No accepted native idle/decay mechanism exists in the minimal realization | Deferred linked persistence probe |
| Change reader topology | Tests transfer | Adds more than one route/geometry distinction | Deferred transfer cycle |

### 21.3 Accepted single-axis contrast

```text
changed_axis = reader_packet_amount

candidate reader_packet_amount = 0.125
contrast reader_packet_amount = 0.250
```

The contrast amount equals the writer debit and accepted one-repeat reserve.
For every seed, P retains sufficient post-writer coherence before the reader
opportunity:

```text
minimum P before reader = 0.71875
contrast reader debit = 0.25000
remaining P after scheduled departure = 0.46875
```

Writer packet, node/edge topology, medium history, feedback reference and
threshold, edge delays, masks, expected polarity, source/target reader roles,
seeds, opportunity count, windows, and analysis identity remain unchanged.
Both A and B and both aligned/inverted profiles use the contrast amount.

### 21.4 Interpretation

| Observation | Interpretation |
| --- | --- |
| Formation and controls persist | Bounded invariance to doubled carrier load |
| Producer schedules but arrival does not complete | Carrier-load or native capacity dependence at the failed stage |
| Producer becomes ineligible despite matched feedback | Packet-budget/availability dependence, not loss of medium history |
| Participant reserve or conservation fails | Invalid contrast or unsafe execution; retain as implementation/support finding |
| Load becomes the dominant discriminator | Record a possible L06 capacity/circulation redirect without relabeling L01 |

The cell supplies neither broad transfer nor timescale-persistence evidence.
Threshold proximity remains interpreted alongside the exact load and native
reason rather than as a binary conclusion.

### 21.5 Reopening conditions

Reopen `P2-I1-DEC-018` if:

- `0.250` exceeds source-current packet or participant budget constraints;
- doubling packet amount changes another producer, route, timing, or support
  field;
- A and B do not receive equal carrier exposure;
- the contrast cannot preserve all four opportunity-profile roles; or
- a carrier-load contrast proves irrelevant to L01 while one available
  timescale contrast has a clearer bounded discriminator.

## 22. `P2-I1-DEC-019` — Primary comparator and causal comparison roles

**Status:** accepted; implementation frozen in the analysis policy

**Question IDs:** resolves `L01-Q22`

### 22.1 Decision question

Which cell is the comparator in the primary normalized margin, and how should
that metric remain distinct from the row-presence and selectivity controls?

### 22.2 Options considered

| Primary comparator | What it isolates | Main problem | Disposition |
| --- | --- | --- | --- |
| `reference` | Writer-relative feedback content beyond the neutral-content row | Does not alone prove that the row is load-bearing | **Accepted as primary metric comparator** |
| `medium-freeze-withdrawal` | Presence of the accepted feedback row beyond matched participant/node state | Conflates primary content effect with medium-presence control | Retained as causal-control comparator |
| Composite of reference and withdrawal | Jointly rewards content and row dependence | Hides which causal relation carries the margin and creates an invented scale | Rejected |

### 22.3 Accepted comparison roles

```text
primary normalized margin:
  candidate-conditioning vs reference
  meaning = writer-relative history-content effect

medium-dependency control diagnostic:
  candidate-conditioning vs medium-freeze-withdrawal
  meaning = feedback-row presence is load-bearing

selectivity interaction:
  candidate-conditioning vs medium-freeze-withdrawal
  meaning = the medium effect differs by frozen polarity susceptibility
```

Only the first comparison instantiates the primary calibrated normalized
margin. The medium-dependency diagnostic preserves raw fractions and paired
differences but does not become a second primary metric or consume calibrated
`delta`. Selectivity remains the separately resolved two-context interaction
from `P2-I1-DEC-007` and likewise does not consume `delta`.

### 22.4 Joint interpretation

A primary aligned margin without row dependence remains insufficient: it may
reflect generic content, participant state, or another bypass. Row dependence
without a primary content effect shows that a feedback row matters but does
not establish writer-relative historical content. Both relations and the
separate selectivity result remain visible to rung and terminal interpretation;
they are never collapsed into one score.

This decision assigns metric roles, not accept/reject verdicts. Raw coverage,
threshold proximity, lineage, controls, support, and unexpected properties
still govern the developmental reading of the specific result.

### 22.5 Reopening conditions

Reopen `P2-I1-DEC-019` if:

- the neutral-content reference fails to isolate the registered writer
  contribution;
- candidate and reference cannot preserve their declared non-content fields;
- row absence proves to be the only scientifically meaningful comparator and
  the L01 question must be redescribed around medium presence;
- calibration and live analysis cannot use the same primary comparison; or
- a later cycle replaces the accepted medium definition or primary response.

## 23. `P2-I1-DEC-020` — Candidate-execution authorization boundary

**Status:** accepted; bounded v2 CAL-PRE/CAL refresh passed

**Question IDs:** registration and execution change control; no scientific lane
question changed

### 23.1 Decision question

Which gate may authorize the first candidate operation while preserving a
separate post-execution completion gate?

The CAL-GATE review exposed a circular statement in the frozen runtime policy:
it required `P2-I1-EXEC-GATE` to pass before candidate execution, while the
checklist defines that gate as the exit reached only after every registered
cell and seed has a terminal execution disposition.

### 23.2 Options considered

| Option | Advantage | Main problem | Disposition |
| --- | --- | --- | --- |
| Add a cycle-scoped `P2-I1-EXEC-FREEZE` before execution | Separates registration, exact-run authorization, and post-run closure | Requires one explicit authorization artifact and a bounded identity refresh | **Accepted** |
| Redefine `P2-I1-EXEC-GATE` as a pre-execution gate and add another close gate | Removes the literal cycle | Renames an already clear, widely referenced post-execution contract | Rejected |
| Let `P2-I1-REG-GATE` directly authorize execution | Minimal ceremony | Conflates a reusable registration bundle with one exact execution cycle | Rejected |
| Leave the old runtime-policy statement and supersede it only in prose | Avoids identity refresh | Preserves conflicting machine and narrative authorities | Rejected |

### 23.3 Accepted boundary

Candidate execution requires all of:

```text
P2-I1-CAL-GATE = passed
P2-I1-REG-GATE = passed
active candidate cycle = frozen
P2-I1-EXEC-FREEZE = passed for that exact cycle
```

`P2-I1-EXEC-FREEZE` binds the registration bundle, calibration, realization
profile, exact configuration IDs, seeds, attempt/retry limits, resources,
expected artifacts, control plans, claim boundary, stopping rule, candidate-
absence assertion, and source/configuration identities. Any mismatch or later
change invalidates that freeze and requires a new cycle-specific record.

The shared runtime policy retains
`candidate_execution_authorized=false`: it grants no blanket authority. A
future candidate runner must additionally consume a valid cycle-scoped freeze
record before it may schedule the first candidate operation. Registration
alone never supplies that record.

`P2-I1-EXEC-GATE` remains the post-execution exit gate. It records whether all
registered cells, controls, receipts, failures, and reconstructions reached a
valid completed, blocked, or incomplete disposition.

### 23.4 Change-control consequence

The incorrect authorization sentence participates in the retained runtime
configuration digest and therefore in the v1 CAL-PRE measurement identity.
The correction uses a bounded v2 refresh rather than a prose waiver:

- preserve the committed v1 identity, calibration, review, and source anchor;
- change only the authorization boundary and its validator/documentation;
- generate a v2 CAL-PRE identity from a clean source commit;
- rerun the candidate-blind matched null and resolution freeze;
- require the calibration-realization digest and all three calibration
  artifacts to remain identical;
- allow only the runtime-config and derived measurement identities to change;
  and
- close by exact deterministic verification after the semantic source change
  has been reviewed; require another review only if a new decision or unknown
  assumption appears, the declared scope expands, or a verification fails.

No candidate outcome exists, and this refresh cannot open candidate evidence.

### 23.5 Reopening conditions

Reopen `P2-I1-DEC-020` if:

- the runner cannot validate a cycle-scoped freeze before its first operation;
- authorization can drift after validation without changing the cycle identity;
- the freeze cannot bind all execution-affecting fields listed above;
- runtime failure occurs before a retained receipt can establish which freeze
  authorized the attempt; or
- the execution-close gate cannot remain distinct from terminal scientific
  interpretation.

## 24. `P2-I1-DEC-021` — Registration representation

**Status:** accepted; retained freeze and manifest materialized, REG-GATE
passed

**Question IDs:** REG-GATE representation and the deferred R3 contract-adequacy
question

### 24.1 Decision question

How should P2-I1 materialize a portable, machine-verifiable registration bundle
without either reducing registration to Markdown or prematurely revising the
common schema with a first-class `lane_registration` record?

### 24.2 Options considered

| Representation | Advantage | Main problem | Disposition |
| --- | --- | --- | --- |
| Experiment-local registration policy plus existing schema records and resolved manifest | Tests the accepted Phase 1 contract set in concrete use while keeping every relationship machine-verifiable | Requires an experiment-local validator and derived registration freeze | **Accepted** |
| Add first-class `lane_registration` and `control_outcome` schema records now | Makes registration and later control outcomes explicit core types | Reopens Phase 1 before concrete use demonstrates that existing records are insufficient | Deferred to R3 |
| Markdown checklist and authored registration report only | Low implementation cost | Cannot prove identity equality, exact controls, execution configuration, or candidate absence | Rejected |
| One opaque custom registration JSON replacing existing records | Simple single file | Creates an unreviewed parallel schema and hides record authority | Rejected |

### 24.3 Accepted bundle architecture

The registration bundle consists of:

1. one experiment-local `p2_i1_registration_policy.json` configuration that
   freezes operational identities, imported measurement fields, cells, seeds,
   order, reset/retry/resource policies, controls, expected artifacts,
   reconstruction, claim boundaries, and `EXEC-FREEZE` prerequisites;
2. existing schema-valid `realization_profile`, `runtime_binding_receipt`,
   `pattern_card`, `medium_surface`, `constructed_mechanism`, `claim_boundary`,
   and applicable debt records;
3. one derived experiment-local registration freeze that computes and compares
   the calibration and registration measurement/realization projections,
   separately digests registration-only policy, and records candidate absence;
   and
4. one resolved `artifact_manifest` that indexes the retained registration
   evidence and its reconstruction identities.

The derived freeze is an experiment artifact with an explicit
`artifact_kind`; it is not a new common record type, cannot replace any core
record, and cannot become positive lane evidence. Expected candidate outputs
that do not yet exist remain declarations in the registration policy rather
than fake manifest entries.

### 24.4 Authority and verification boundary

- Existing JSON Schema records retain their frozen meanings and shapes.
- The registration policy is a non-evidential experiment input validated by
  P2-I1 tooling.
- The registration freeze proves cross-record relationships and identity
  equality; it does not redefine core record semantics.
- The artifact manifest resolves only files that exist at registration time.
- Retained generated artifacts require a clean source anchor; dirty review
  previews are explicitly non-retainable and cannot enter the manifest.
- `validate-phase1` success alone cannot satisfy registration.
- No registration artifact grants candidate execution authority; a separate
  exact-cycle `P2-I1-EXEC-FREEZE` remains mandatory.
- R3 decides whether concrete friction justifies promoting registration or
  control outcomes into new first-class common records.

### 24.5 Reopening conditions

Reopen `P2-I1-DEC-021` if:

- existing records cannot express a required registration relationship without
  an authoritative `x_` extension or authored inference;
- the registration freeze must duplicate or redefine a core record meaning;
- the manifest cannot index the retained bundle without pretending future
  candidate artifacts already exist;
- control applicability cannot be made explicit and verifiable in the
  experiment-local policy; or
- R3 finds that the first completed lane cannot be audited cleanly without a
  first-class registration or control-outcome record.

## 25. `P2-I1-DEC-022` — Realization-profile scope

**Status:** accepted; retained path-free binding receipt passed conformance

**Question IDs:** REG-GATE realization identity and D-033/D-034 runtime-binding
discipline

### 25.1 Decision question

Should registration retain a preflight-only realization profile and transition
to another profile before execution, or should one exact profile span the
registered preflight and declared P2-I1 operation classes?

### 25.2 Options considered

| Profile scope | Advantage | Main problem | Disposition |
| --- | --- | --- | --- |
| One path-free profile spanning registration and the declared execution operation classes | Preserves realization identity from REG-GATE through EXEC-FREEZE while per-run receipts still verify use | Must distinguish conformance from scientific success and from authorization | **Accepted** |
| Registration-only profile followed by a separate execution profile | Narrow initial statement | Introduces a realization transition after registration and forces new identity review before execution | Rejected for the primary cycle |
| Keep the profile local and unretained | Avoids machine-specific availability claims in the repository | Makes the registered realization and reconstruction boundary unauditable | Rejected |
| Treat PyGRC availability as sufficient without a profile | Minimal ceremony | Permits silent version/capability/substitution drift | Rejected |

### 25.3 Accepted profile boundary

The retained profile:

- contains no machine-local runtime or checkout path;
- records the exact required and observed PyGRC identity, public capabilities,
  realization class, source/configuration identities, and claim ceiling;
- lists `p2_i1_runtime_preflight` plus the operation classes declared by the
  v2 runtime policy;
- resolves those operation classes to concrete callable PyGRC methods rather
  than treating an allowed name or public module namespace as conformance;
- uses `availability`, `enabled`, `supported`, and `validated` only for the
  exact binding, capability, and baseline-fixture conformance established at
  registration;
- does not claim that any writer, medium, reader opportunity, candidate cell,
  control, or scientific outcome succeeded;
- remains the referenced realization profile through the first exact-cycle
  `EXEC-FREEZE`; and
- requires one retained runtime receipt for every later live run.

The shared profile is a retained registration observation tied to its source
anchor, not a promise that another machine has the runtime installed. A
reproducer must perform the same local binding and emit a new receipt. Merely
listing operation classes never schedules them and never replaces the
cycle-scoped execution freeze from `P2-I1-DEC-020`.

### 25.4 Transition discipline

If PyGRC later implements an RCAE producer natively, the existing profile and
runner continue to use the registered constructed realization. Transition to
native functionality requires a new profile, explicit decision/change record,
new cycle freeze, and rerun. Neither repository may produce availability-driven
side effects in the other.

### 25.5 Reopening conditions

Reopen `P2-I1-DEC-022` if:

- registration preflight cannot verify the declared identity or capabilities;
- any listed operation class requires a different PyGRC build, realization
  class, producer implementation, or schema version;
- the profile would need a machine-local path to reproduce its identity;
- per-run receipts cannot prove which retained profile was used; or
- an explicit native-transition decision replaces the constructed producer.

## 26. `P2-I1-DEC-023` — Baseline, reset, and isolation identity

**Status:** accepted; all 21 retained W0 identities materialized and reconstructed

**Question IDs:** REG-GATE state isolation, reset, retry, and contamination
boundary

### 26.1 Decision question

How should registration freeze baseline state when the three seed transforms
and the parent-support intervention legitimately produce different initial
runtime states?

### 26.2 Options considered

| Reset model | Advantage | Main problem | Disposition |
| --- | --- | --- | --- |
| One expected baseline identity per exact cell/seed configuration, reconstructed in a fresh worker | Makes every intended initial difference explicit and prevents mutable state reuse | Produces 21 registered identities, including legitimate duplicate digest values | **Accepted** |
| One global baseline digest | Simple comparison | Incorrectly treats seed and support transforms as contamination | Rejected |
| Reuse one runtime and clear queue/log/state between runs | Lower construction cost | Reset correctness depends on mutation completeness and may preserve hidden state | Rejected |
| Reconstruct one runtime per seed and mutate cells in fixed order | Fewer constructions | Makes cell order a causal input and permits cross-cell history | Rejected |

### 26.3 Accepted baseline identity

Registration emits one ordered baseline-identity entry for each of the seven
cells and candidate seeds `101`, `211`, and `307`. Each entry binds:

```text
cell_id
seed
fixture_config_digest
cell_configuration_digest
resolved node coherences
topology and route-aspect identities
empty queue identity
empty focal-surface identity
runtime policy and realization profile refs
canonical initial snapshot digest
expected composite baseline digest
```

All 21 entries remain explicit even when several expected composite digests are
equal. Equality is an observed configuration relation, not a reason to drop an
entry.

### 26.4 Construction and retry boundary

Every cell/seed attempt starts in a fresh worker process and constructs a new
runtime from declarative inputs. It may not reset by clearing or mutating a
prior runtime. Before the writer operation, the observed composite baseline
must equal the registered expected identity.

An infrastructure retry reconstructs the same cell/seed/configuration in a
new worker, must reproduce the same baseline identity, and retains the failed
attempt. The lowest-seed-first cell retry allocation from the frozen cell
policy remains unchanged.

### 26.5 Opportunity branch boundary

Inside one valid cell/seed attempt, W2 creates exactly one branch-point
snapshot after writer history and medium materialization. Each of the four
opportunities restores that snapshot independently. Restoration equality is
separate from the W0 baseline identity: W0 proves attempt initialization; W2
proves equal later-opportunity exposure.

Fixed cell order remains retained for audit and operational reproducibility,
but intended scientific isolation comes from fresh workers and matching
identities rather than from assuming order has no effect.

### 26.6 Failure meaning and reopening conditions

A baseline mismatch, non-empty queue or surface, failed W2 restoration,
residual prior-run identity, or worker reuse is an infrastructure/integrity
failure. It cannot support or refute L01.

Reopen `P2-I1-DEC-023` if:

- source-current PyGRC cannot serialize a sufficient initial snapshot;
- the composite digest omits model-owned state that can affect later events;
- fresh workers cannot reproduce the same registered configuration identity;
- worker isolation changes the declared runtime or resource envelope; or
- W2 restoration cannot preserve every registered branch-point field.

## 27. `P2-I1-DEC-024` — Control lifecycle and registration meaning

**Status:** accepted; retained freeze resolves the exact evidence-bound
registration lifecycle

**Question IDs:** REG-GATE control applicability, planned evidence, and the
deferred R3 `control_outcome` contract question

### 27.1 Decision question

How should REG-GATE freeze every common and L01-specific control without
mistaking an applicable control or a planned artifact for a completed causal
outcome?

### 27.2 Accepted policy and result fields

The control lifecycle preserves three independent concepts without allowing an
input policy to declare its own successful outcome:

```text
registration policy:
applicability:
  applicable | not_applicable

resolution_stage:
  registration_guard | execution_comparison |
  terminal_report_guard | inherited_verification

required_evidence
fail_closed_effect

derived registration/execution/terminal freeze:
outcome_status:
  resolved | pending_execution | blocked | not_applicable
```

`not_applicable` always includes a control-specific causal or record-role
rationale in both policy and freeze. `blocked` is missing knowledge and cannot
masquerade as a negative result. A registration validator derives `resolved`
only when an applicable control's entire required check is deterministic,
outcome-independent, and satisfied by the declared evidence. The policy itself
never emits `resolved`.

The concrete P2-I1 materialization represents that boundary with exact
`evidence_binding_refs`. Both the descriptive obligation and its permitted
bindings are validator-frozen. Resolution requires every bound record, source,
profile, receipt, or baseline identity to pass its own validator; stage name
alone cannot resolve a leg.

### 27.3 Mixed and inherited controls

A control with both record-guard and causal/withdrawal meaning is represented
as separate legs under the same control ID. Resolving the registration leg does
not resolve its execution leg.

Every inherited-verification leg records:

```text
source artifact and digest
inherited role
identical-scope verification
must_not_consume_as
new lane execution required
```

Inheritance supplies only its declared method, schema, or fixed
runtime-invariant role unless identical carrier, mechanism, intervention, and
claim scope are demonstrated. A list of inherited IDs is not evidence.

### 27.4 Causal and withdrawal controls

Every causal or withdrawal leg names its exact registered cell or comparison,
preserved fields, broken relation, expected artifact role, and fail-closed
effect. The derived registration freeze records `pending_execution` through
REG-GATE. Registration cannot infer an outcome from a fixture, preflight,
expected result, or decision record.

Control IDs alone never satisfy terminal closure. Later outcome evidence must
remain linked through execution, developmental interpretation, terminal
classification, pattern card, debt, and report projections.

### 27.5 Representation and R3 boundary

The experiment-local registration policy carries applicability, stage, and
evidence obligations under `P2-I1-DEC-021`. Derived freezes carry outcome
status; no first-class `control_outcome` schema is added now. R3 may promote one
only if concrete execution cannot preserve these relationships without
authored inference, authoritative extensions, or duplicated meaning.

### 27.6 Reopening conditions

Reopen `P2-I1-DEC-024` if:

- one field cannot distinguish applicable-but-unexecuted from resolved;
- a mixed control cannot preserve separate registration and execution legs;
- inherited verification requires authored inference to determine scope;
- a causal outcome cannot link to its exact registered comparison artifact; or
- R3 finds that the first lane cannot audit control closure without a
  first-class record.

## 28. `P2-I1-DEC-025` — Constructed-scaffold withdrawal applicability

**Status:** accepted; `AE01-L01-CTRL-05` is not applicable to the primary cycle

**Question IDs:** L01 constructed-scaffold withdrawal applicability

### 28.1 Decision question

Does the accepted Option A realization contain a constructed scaffold whose
withdrawal would isolate whether the proposed medium or later response is
scaffold-carried?

### 28.2 Accepted applicability

```text
control_id = AE01-L01-CTRL-05
applicability = not_applicable
outcome_status = not_applicable
```

The accepted medium—native pulse-contact to feedback-eligibility history—and
the later feedback producer are model-owned PyGRC runtime surfaces. RCAE owns
the fixture, initial intervention, configuration, orchestration, and analysis,
but is prohibited from computing the later response, injecting a successful
surface, directly mutating coherence, marking native events processed, or
bypassing the event queue.

Removing the RCAE adapter would therefore remove the experiment and its
invocation boundary rather than withdraw a causal scaffold while preserving a
matched opportunity. Such a comparison would not discriminate the L01 claim.

### 28.3 Controls that remain applicable

This decision does not weaken:

- `AE01-L01-CTRL-01`, which freezes the accepted feedback-medium row while
  preserving participant state and opportunity;
- `AE01-CTRL-08`, which instruments every producer/handoff and blocks hidden
  constructed causality;
- `AE01-CTRL-15`, which preserves the RCAE-constructed role and prohibits
  native relabeling or silent substitution; or
- `AE01-CTRL-16`, which requires necessity, minimality, counterfactual,
  withdrawal meaning, debt, and discriminator fields for the constructed
  adapter/mechanism record.

Medium freeze and scaffold withdrawal remain distinct interventions. The
former is mandatory in this cycle; the latter is neither blended into it nor
treated as an unexecuted negative.

### 28.4 Reopening conditions

Reopen `P2-I1-DEC-025` before execution if implementation shows that:

- an RCAE-owned state surface carries medium history or later eligibility;
- an RCAE producer computes or schedules the later response outside the
  declared native producer;
- a constructed scaffold can be withdrawn while preserving the registered
  participant, native medium, and later opportunity; or
- source-current PyGRC lacks the declared native operation and the primary
  realization must introduce a constructed replacement.

If reopened after any candidate observation, preserve the primary result and
register a new linked cycle; never add scaffold withdrawal as a rescue variant.

## 29. `P2-I1-DEC-026` — Execution-specific runtime binding

**Status:** accepted for C01 EXEC-FREEZE

**Question IDs:** C01 runtime conformance and D-033/D-034 explicit-transition
discipline

### 29.1 Decision question

REG-GATE verified the registered operation family through fixture construction,
route validation, snapshot/load, stepping, feedback-row emission, and producer
configuration. The concrete C01 sequence also needs to schedule the writer
packet, invoke the configured native producer, persist the W2 branch point, and
inspect native state. How should those more specific calls be bound without
silently changing the retained REG receipt or pretending it authorized
execution?

### 29.2 Why this decision became necessary

REG-GATE and EXEC-FREEZE answer related but different questions.

REG-GATE asked:

> Does the selected PyGRC realization expose the native operation families
> required by the registered experiment?

Its receipt verified fixture construction, route validation, snapshot/load,
queue stepping, feedback-row emission, and feedback-producer configuration.
That was sufficient to establish that the proposed realization family and
registered native surfaces exist. It did not authorize candidate execution.

Writing the concrete W0-W4 runner exposed the narrower execution question:

> Which exact PyGRC methods does this executable sequence call, and are all of
> them present before the first candidate operation?

The distinction matters because configuration is not invocation. In
particular, `set_feedback_coupled_pulse_producer()` configures the native
producer, but source-current PyGRC requires `produce_events()` to ask that
producer to schedule eligible work. Likewise, the registered packet-step and
snapshot families do not by themselves state that C01 will call
`schedule_packet_departure()`, `save()`, `load()`, `get_state()`, and
`snapshot()` at its exact writer, branch, and audit boundaries.

The concrete roles are:

| Exact call | C01 role |
| --- | --- |
| `schedule_packet_departure()` | Schedule the single P-to-W writer packet at W1 |
| `produce_events()` | Invoke the configured native feedback producer at W3 |
| `save()` / `load()` | Persist W2 and restore four independent counterfactual branches |
| `get_state()` / `snapshot()` | Audit baseline, queue, medium, restoration, isolation, and retained identity without direct mutation |

This is not evidence that REG-GATE failed. It is evidence that registration
conformance was necessary but intentionally not identical to exact execution
conformance. The missing precision naturally appeared when the registered
design was turned into executable operations.

### 29.3 Options considered

| Option | Benefit | Cost | Disposition |
| --- | --- | --- | --- |
| Reopen REG-GATE and replace the retained receipt | One exhaustive receipt | Rewrites an accepted registration fact for detail only discoverable during executable materialization | Not recommended unless the added binding fails |
| Add a C01 execution-specific callable superset | Keeps registration and execution conformance distinct; fails before execution when any exact call is absent | Requires a second, narrower binding record in EXEC-FREEZE and every run | **Accepted** |
| Treat producer configuration plus `step()` as sufficient | No new record | False: source-current PyGRC requires explicit `produce_events()`, and writer setup requires `schedule_packet_departure()` | Rejected |
| Implement RCAE replacements for missing calls | Could keep the experiment runnable | Violates no-fallback and explicit-native-transition constraints | Rejected |

### 29.4 Accepted binding and layered contract

C01 imports every passed registration capability and adds exact callable
resolution for:

```text
LGRC9V3.schedule_packet_departure
LGRC9V3.produce_events
LGRC9V3.save
LGRC9V3.load
LGRC9V3.get_state
LGRC9V3.snapshot
```

The relation is:

```text
C01 execution binding
  = every capability already required by REG
  + the exact additional calls used by the C01 runner
```

It is a strict execution-specific superset, not a replacement public API and
not a monkey patch. The retained REG receipt remains evidence that the
registered family exists. The C01 binding receipt establishes that the exact
runner calls exist. EXEC-FREEZE binds those calls to one exact cycle, and only
the retained tracked freeze authorizes its 21 primary runs.

```text
REG receipt
  -> registered native operation family exists

C01 execution-binding receipt
  -> every exact C01 call is callable

P2-I1-EXEC-FREEZE
  -> those calls are bound to one exact candidate-free cycle

tracked P2-I1-EXEC-FREEZE
  -> only the exact cell/seed/attempt scope may run
```

The accepted binding is explicitly not:

- a duplicate RCAE implementation of PyGRC functionality;
- permission to monkey-patch or modify PyGRC;
- a fallback operation map;
- a transition to a newly native implementation;
- general candidate-execution authority; or
- scientific evidence for or against niche conditioning.

Missing, non-callable, or identity-drifting surfaces block execution as an
operational result. They cannot select a fallback, mutate PyGRC, or count as
scientific negative evidence. If PyGRC later provides a more native combined
operation, C01 continues to use this frozen realization until an explicit new
profile and rerun are accepted.

### 29.5 Failure and REG reopening boundary

An unavailable exact call stops C01 before scientific execution. The resulting
classification is operationally blocked or incomplete, never a negative niche
result. The next question would be whether:

- C01 selected the wrong public PyGRC call;
- the registered native-operation claim was too broad;
- the substrate is missing an operation surface; or
- a separately declared constructed realization and new cycle are warranted.

REG-GATE does not reopen merely because exact-call conformance belongs to the
next gate. It reopens only if the C01 binding exposes a concrete contradiction
with the retained REG claim—for example, if the supposedly available native
operation cannot be expressed by any admitted public call.

The candidate-free preview binding already resolved all six added methods in
the selected `pygrc==0.1` realization while leaving the graph worktree clean.
Therefore the accepted decision records a layered contract, not a workaround
for an observed missing runtime method.

Owner acceptance is recorded by the stable machine-readable marker:

```text
P2-I1-DEC-026 accepted for C01 EXEC-FREEZE
```

### 29.6 Reopening conditions

Reopen `P2-I1-DEC-026` if:

- one added call cannot be resolved in the retained `pygrc==0.1` realization;
- source inspection shows a different public call owns the registered
  operation;
- C01 would need a constructed replacement, direct state injection, or PyGRC
  modification;
- the execution-specific map duplicates a broad PyGRC API instead of the exact
  calls used; or
- the added binding changes the scientific fixture, cell, control, or claim
  semantics rather than merely making them executable.

## 30. `P2-I1-DEC-027` — Native branch-restoration identity

**Status:** accepted for a separately frozen C02 correction

**Question IDs:** C01 W2 restoration, `C01-OBL-07`, and exact native
save/load semantics

### 30.1 Why the decision became necessary

The exact C01 cycle attempted all 21 primaries and the seven deterministic
retries permitted by its freeze. Every attempt stopped before producer
invocation because the restored full snapshot digest differed from the W2
snapshot digest. C01 consequently closed bounded incomplete with no scientific
result and an exhausted attempt budget. The complete machine evidence and
reconstruction instructions are retained in the
[C01 bounded-incomplete record](../reports/P2-I1-C01-bounded-incomplete.md).

Bounded native round-trip diagnosis found exact preservation of the complete
`dynamics.lgrc9v3_runtime` artifact. The six differing leaves were confined to
the nested cached GRC9V3 snapshot: restoration materialized budget-source,
parameter-identity, and RNG defaults and canonicalized one undirected edge's
endpoint ordering. Outer geometry, events, observables, and the independently
reconstructed medium projection were equal.

The failure therefore exposed an RCAE equality-predicate decision. It did not
show that PyGRC lost the native LGRC runtime state, and it did not constitute
negative niche evidence.

### 30.2 Options considered

| Option | Benefit | Cost | Disposition |
| --- | --- | --- | --- |
| Declare a native restoration projection | Preserves the causal and geometric state C02 uses while excluding representation-only cache normalization | Requires a new cycle, explicit projection, raw-digest retention, and continuation tests | **Accepted** |
| Normalize the six observed cache differences before full comparison | Small local predicate change | Couples RCAE to internal cache normalization and risks silently expanding exclusions | Rejected |
| Continue requiring full snapshot equality | Maximum representational identity | Treats a public native load as unusable even though its LGRC runtime artifact is exact | Rejected for C02; reopen if cached identity is later shown scientifically necessary |
| Patch PyGRC or mutate the restored state | Could force byte equality | Violates graph read-only, no-fallback, and explicit-native-transition constraints | Rejected |

### 30.3 Accepted C02 contract

C02 preserves the C01 fixture, cells, seeds, metrics, controls, attempts, and
claim ceiling. It changes only branch-restoration identity:

```text
native branch-restoration identity
  = outer topology, basin attributes, and edge labels
  + exact native LGRC runtime artifact
  + event and observable state
  + separately verified medium reconstruction
```

The nested `caches.base_grc9v3_snapshot` remains present in the full raw native
snapshot but does not control restoration equality. Every opportunity retains:

- pre-save and post-load full raw snapshot digests;
- pre-save and post-load restoration-projection digests;
- whether raw normalization was observed;
- exact medium-reconstruction identity; and
- an equal-input continuation comparison between independently restored
  branches.

The projection must fail closed when any included geometry, runtime, event,
observable, or medium field drifts. Equal projections alone do not establish
full native equivalence: the continuation comparison is also mandatory before
the opportunity is evaluable.

This is an RCAE harness correction. It authorizes no PyGRC modification,
monkey-patch, state injection, fallback, candidate result, or scientific claim.
If projected state or equal-input continuation differs, C02 stops and the
native runtime question may reopen.

C01 remains immutable and cannot be rescued or rerun. C02 requires its own
source anchor, binding receipt, EXEC-FREEZE, paths, attempt scope, audit, and
manifest.

Owner acceptance is recorded by the stable machine-readable marker:

```text
P2-I1-DEC-027 accepted for C02 restoration correction
```

### 30.4 Reopening conditions

Reopen `P2-I1-DEC-027` if:

- a projected runtime, geometry, event, observable, or medium field differs;
- two independently restored equal-input branches continue differently;
- source inspection shows an excluded cached field carries scientific state
  used by P2-I1;
- the projection requires an expanding list of exception fields; or
- implementation would require PyGRC modification, direct state injection, or
  a constructed fallback.

## 31. Current decision boundary and next work

C01 is retained as `bounded_incomplete_operational` with no scientific result.
`P2-I1-DEC-027` authorizes materialization of C02 as a separately frozen
restoration correction. No C02 candidate operation is authorized until its
source, binding receipt, and tracked EXEC-FREEZE pass.

`L01-Q11` through `L01-Q13` remain open for terminal interpretation, and
`L01-Q14` remains reserved for R3 after a concrete scientific execution.
