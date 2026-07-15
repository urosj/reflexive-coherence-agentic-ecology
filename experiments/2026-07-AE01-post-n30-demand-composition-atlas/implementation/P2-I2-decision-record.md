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
| `P2-I2-DEC-010` | Which state-carried realization, factorization, interventions, controls, and producer boundary should 8A freeze? | Accepted by project owner as the causal-design baseline for I03AR1; bounded runtime conformance later completed under DEC-012; scientific support unassigned | Authorizes only separately frozen I03AR1 conformance; umbrella gate remains open; I03B/I04 unauthorized | 2026-07-14 |
| `P2-I2-DEC-011` | Are state-carried, history-carried, and hybrid alternatives for later selection or three retained mode-specific realizations? | Accepted by project owner: retain and test all three; select native/producer/missing-prerequisite disposition within each mode | Corrects brief/downstream singular scope; brief gate remains passed; did not itself accept DEC-010 or authorize I03B/I04 | 2026-07-14 |
| `P2-I2-DEC-012` | May each I03 mode receive bounded runtime conformance before calibration, and what evidence boundary applies? | Accepted by project owner: I03AR1 now, then design-first conformance inside I03B/I03C | Authorizes only freeze-governed realization conformance; no I04–I08 or scientific authority | 2026-07-14 |
| `P2-I2-DEC-013` | Does the review-ready I03A/I03AR1 package satisfy the progression boundary, and may 8B begin? | Accepted by project owner: move to 8B next | Opens design-first I03B only; I03C/I04 and scientific authority remain closed | 2026-07-14 |
| `P2-I2-DEC-014` | Which history-carried realization and producer boundary should I03B freeze before runtime conformance? | Design-frozen minimally producer-assisted adapter; bounded runtime conformance and I03BR1 closeout revalidation passed; accepted for progression under DEC-015 | I03B retained; later progression remains governed separately | 2026-07-14 |
| `P2-I2-DEC-015` | Does I03B/I03BR1 satisfy the staged-progression boundary, and may 8C begin? | Accepted by project owner: 8C is next; retain I03B as minimally producer-assisted implementation evidence only | Opens design-first I03C under a new freeze; I04 and scientific authority remain closed | 2026-07-14 |
| `P2-I2-DEC-016` | Which hybrid realization, separable components, joint response, and producer boundary should I03C freeze before runtime conformance? | Minimally producer-assisted hybrid frozen; static validation and 258/258 byte-reconstructed bounded runtime conformance passed; accepted for progression under DEC-018 | I03C retained; umbrella gate and I04 remain governed separately | 2026-07-14 |
| `P2-I2-DEC-017` | Does I03C satisfy the owner-supplied causal-well-formedness and acceptance closeout checks, and what may follow? | I03CR1 audit passed 26/26 review checks and 17/17 acceptance conditions with zero blockers and eight downstream obligations; accepted for progression under DEC-018 | I03C acceptance-ready boundary satisfied; opened only I03F under DEC-018 | 2026-07-14 |
| `P2-I2-DEC-018` | Does I03C/I03CR1 satisfy staged progression, and what scope should section 8.1 use? | Accepted by project owner: move to 8.1; compose prior full reviews compactly rather than repeating them | Opens checklist/hypothesis-first I03F terminal-authority composition only; I04 remains closed | 2026-07-14 |
| `P2-I2-DEC-019` | Does the compact three-mode family composition satisfy discriminator-gate readiness? | I03F passed 12/12 integration checks and 9/9 acceptance conditions with zero blockers; subsequently owner-accepted under DEC-020 | Historical `P2-I2-I03F-REVIEW-READY` disposition retained | 2026-07-14 |
| `P2-I2-DEC-020` | Does the owner accept compact I03F and which downstream scope may open? | Accepted: pass only the discriminator gate and continue with I04 | Opens candidate-free I04 construction; I05 and candidate execution remain closed | 2026-07-14 |
| `P2-I2-DEC-021` | Which response, comparator, order, analysis, controls, and candidate-blind null should original I04 freeze? | Historical candidate-free package validated 16/16 with 10/10 pure tests; superseded for progression after critical review | Historical construction only; CAL-PRE was withheld | 2026-07-14 |
| `P2-I2-DEC-022` | What effect does the owner-supplied critical I04 review have? | Accepted as correction authority: preserve original I04 as history, withhold CAL-PRE, and open only checklist/hypothesis-first I04R1 | Reopens preregistration construction; no null/runtime/candidate authority | 2026-07-14 |
| `P2-I2-DEC-023` | Does I04R1 resolve the comparator, null-domain, fixed-window, B-purity, mode-isolation, causal-evidence, and quarantine duties? | Historical readiness: 19/19 focused checks and 15/15 pure tests; superseded for progression by DEC-026 | Immutable I04R1 correction history only; no parallel calibration authority | 2026-07-14 |
| `P2-I2-DEC-024` | What effect does the owner-supplied conditional I04R1 review have? | Accepted as an I04R2 verification/correction trigger, not as automatic owner acceptance | Opens focused candidate-free I04R2 only; CAL-PRE and I05 remain closed | 2026-07-14 |
| `P2-I2-DEC-025` | Does I04R2 confirm the complete two-arm/I05 estimator path and remaining machine invariants? | Acceptance-ready: 16/16 focused checks and 7/7 pure tests passed; one future-I05 bypass corrected; subsequently accepted under DEC-026 | Historical readiness disposition; gate effect now owned by DEC-026 | 2026-07-14 |
| `P2-I2-DEC-026` | Does the project owner accept I04R2, which I04 lineage governs progression, and what gate may pass? | Accepted: I04R2 is sole progression authority; original I04/I04R1 are immutable history; exact tie has no scientific meaning | Passes CAL-PRE; opens only separately frozen single-invocation I05 authorization construction | 2026-07-14 |
| `P2-I2-DEC-027` | Is the separately frozen I05 authorization candidate exact and bounded enough to accept and commit? | Proposed but blocked: I05A passed 3/8 safety checks and found five one-shot/commit-binding/receipt blockers | No active invocation authority; acceptance, commit, CAL-GATE, I06, and candidates remain closed | 2026-07-14 |
| `P2-I2-DEC-028` | May the five I05A execution-safety blockers be corrected, and under what scope? | Owner-authorized: I05-owned mechanics only; I04R2 immutable; zero-null validation; return uncommitted | Opens I05B construction/tests only; commit, null invocation, CAL-GATE, I06, and candidates remain closed | 2026-07-14 |
| `P2-I2-DEC-029` | Does the project owner accept I05B, and which authority is committed? | Accepted: commit the complete I05/I05A/I05B package with immutable acceptance; null launch remains separate | Authorizes package retention only; 10.4 launch requires its own exact record and committed HEAD | 2026-07-14 |
| `P2-I2-DEC-030` | After the accepted I05B commit, may 10.4 consume the single arithmetic-null attempt? | Accepted: create and commit the exact separate launch record, then execute the one-shot with zero retries | Opens one I05 arithmetic-null attempt only; CAL-GATE and I06 remain pending review | 2026-07-14 |
| `P2-I2-DEC-031` | How must the pre-claim `.venv` path-resolution failure be corrected? | Accepted and committed: always use the active repository `.venv`; separate invoked command identity from resolved binary identity | Historical I05C correction enabled the later single attempt; its portability debt is now governed by DEC-032 | 2026-07-14 |
| `P2-I2-DEC-032` | How must the newly exposed absolute-path violations be audited and corrected? | Owner-authorized audit now review-ready: 135 files scanned, 312 value-redacted violations in 70 files; an in-iteration selector correction ensures nested coverage; correction order begins with I05 | I05E correction, metric freeze, CAL-GATE, I06, and all execution remain closed pending audit acceptance | 2026-07-14 |
| `P2-I2-DEC-033` | Does the owner accept the I05D inventory and which correction group may begin? | Accepted as the right next move: open only the exact first I05 portability correction group and return it uncommitted for review | Opens I05E group 1 only; no null rerun, later correction group, metric freeze, CAL-GATE, I06, or candidate execution | 2026-07-14 |
| `P2-I2-DEC-034` | Does the owner accept the first correction group and which group follows its commit? | Accepted and committed at `6dd6898`; open only the exact 13-file/30-finding I04/I05 authority-dependency group under I05F | Opens I05F only; no I03/later group, metric freeze, CAL-GATE, I06, or execution | 2026-07-14 |
| `P2-I2-DEC-035` | May the I05F static-validation ceiling deviation be closed in place without rewriting the freeze or rerunning validation? | Owner-authorized `+1`: retain an additive I05F deviation closeout accepting the process-only 13-versus-three variance | Opens closeout-record construction only; no full-package acceptance, commit, rerun, later group, CAL-GATE, I06, or execution | 2026-07-14 |
| `P2-I2-DEC-036` | Does completed DEC-035 closeout also constitute full I05F acceptance and commit authorization? | Owner-confirmed: “when done, it is also acceptance, can be committed” | Accepts and authorizes commit of the complete I05F package after closeout; no next group, CAL-GATE, I06, or execution | 2026-07-14 |
| `P2-I2-DEC-037` | Which portability work may begin after accepted I05F commit `99c64dd`? | Owner direction: “third group is next”; declare I05G, resolve/freeze the exact third accepted-audit group before edits, and return its bounded correction uncommitted | I05G is 10/10 review-ready with 201 to zero findings; no owner acceptance/commit authority, fourth group, CAL-GATE, I06, or execution | 2026-07-14 |
| `P2-I2-DEC-038` | What follows owner review of I05G? | Accept and commit I05G, then open I05H for the exact fourth accepted-audit group under checklist/hypothesis-first freeze discipline | I05G retained at `62882ef`; opens I05H scope resolution/freeze only; no affected edit before freeze, fifth group, CAL-GATE, I06, or execution | 2026-07-14 |
| `P2-I2-DEC-039` | What follows owner review of I05H? | Accept and commit I05H; reconcile the remaining inventory; fold the one six-file/14-finding group plus three validator constructor sources into the fifth/final I05I correction | I05H retained at `1279e17`; opens exact nine-file terminal correction only; no P2-I1 scope expansion, CAL-GATE, I06, or execution | 2026-07-14 |
| `P2-I2-DEC-040` | What may proceed after owner acceptance and commit of I05I? | Retain I05I at `b5d0acb`; distinguish completed I05C/10.4A from the three deferred 10.4 metric obligations; open bounded I05J native metric closeout | Authorizes one frozen native `freeze-resolution` generation plus static validation only; no null rerun, runtime/candidate work, CAL-GATE passage, I06, or commit | 2026-07-14 |
| `P2-I2-DEC-041` | What follows the first I05J native start failing before output because the repo `.venv` lacks the pinned schema dependency? | Preserve the original freeze and failed start; add I05JA; install only `jsonschema==4.26.0` into `.venv`; authorize one unchanged native retry; amend the still-uncommitted I05J package with honest process accounting | Complete package owner-accepted and commit-authorized; CAL-GATE passed; I06 registration construction authorized but not begun; zero candidate/runtime/scientific authority | 2026-07-14 |
| `P2-I2-DEC-042` | Which exact three-mode implementations, identities, cells, controls, and continuation boundary should I06 register? | Owner-accepted after I06A: retain all three unranked modes; native PyGRC owns adequate transitions; AdapterV2 conformance and exact historical/current provenance are machine-closed; I06 and I06A each pass 14/14 | Authorizes amendment into checkpoint `7761d3e`, passes REG-GATE, and opens I07 freeze construction only; candidate-cycle execution remains unauthorized and candidate/scientific counts remain zero | 2026-07-15 |
| `P2-I2-DEC-043` | May I07 invent missing hybrid intervention timing/value and direct/controller primitives, or must exact registration reopen? | Owner accepts the recommended bounded checklist/hypothesis-first I06B correction; I07 may not invent the missing primitives | I06B construction completes at 15/15 with zero blockers; package acceptance/commit remain pending, REG-GATE remains reopened, and I07/EXEC-FREEZE/I08/candidate execution remain closed | 2026-07-15 |
| `P2-I2-DEC-044` | Does the review-ready I06B package restore registration progression authority? | Owner explicitly accepts I06B; retain exact accepted overlay and validation, restore REG-GATE, and resume the existing I07 freeze from its paused audit | Opens only candidate-free I07 construction/validation; commit, EXEC-FREEZE, I08, and candidate execution remain unauthorized | 2026-07-15 |
| `P2-I2-DEC-045` | Does missing `pytest` require I07A or an in-place I07 environment correction? | Owner directs no I07A: install into `.venv`, preserve failed start, update I07 process accounting, refresh derived bindings, and continue once | Opens only bounded candidate-free I07 continuation; commit, EXEC-FREEZE, I08, and candidate execution remain unauthorized | 2026-07-15 |
| `P2-I2-DEC-046` | Do the four cross-entry-isolation blockers belong to I07A, and what may that correction change? | Owner directs one bounded I07A correction for safe governed I/O, import-cache isolation, same-entry retry reconstruction, and fail-closed completion | I07A passes 15/15 tests and 17/17 checks; acceptance, commit, EXEC-FREEZE passage, I08, and candidate execution remain separately governed | 2026-07-15 |
| `P2-I2-DEC-047` | Does the owner accept I07A and pass the exact inactive execution freeze? | Accepted: retain the zero-blocker I07A package and accumulated I06B/I07 checkpoint | Passes inactive `P2-I2-EXEC-FREEZE` and authorizes commit; live activation, cache cleanup, I08, and candidate execution remain closed | 2026-07-15 |
| `P2-I2-DEC-048` | May I08 activation preparation and its required import-cache cleanup begin? | Owner opens checklist/hypothesis-first inactive activation construction, exact cache cleanup, and candidate-free validation | Produces an 18/18 review-ready inactive activation candidate; no commit, claim, matrix entry, or scientific effect | 2026-07-15 |
| `P2-I2-DEC-049` | Does the owner accept and authorize commit of the exact I08 activation? | Accepted: bind candidate `52d420b`, retain accepted activation `f46ebd3`, and commit the complete activation package | Opens live I08 only from the resulting committed full HEAD after exact preflight; the activation commit contains no matrix claim or result | 2026-07-15 |

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
- an applicable retained dependence mode requires a surface classified inadequate or
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

## 12. `P2-I2-DEC-010` — I03A native state-carried realization

**Status:** accepted by project owner as the causal-design baseline for
`P2-I2-I03AR1`; bounded runtime conformance is review-ready under DEC-012;
scientific support remains unassigned

**Question IDs:** `L02-Q03`–`L02-Q06`, `L02-Q10`–`L02-Q12`

**Question:** Which bounded state-carried realization preserves one common
non-private carrier, attribution-only lineage, native later dependence, and the
complete control structure with the least producer involvement?

### 12.1 Staged mode authority

The project owner directed the dependence-mode program to proceed in three
review-separated sub-iterations:

```text
8A / P2-I2-I03A = state_carried
8B / P2-I2-I03B = history_carried
8C / P2-I2-I03C = hybrid
```

Only I03A is in scope here. I03B requires owner review/acceptance of I03A, and
I03C requires the corresponding I03B review. The umbrella discriminator gate
cannot pass in I03A.

### 12.2 Review-ready selection

Select for review:

```text
candidate_id = p2-i2-state-carried-native-node-pool-v1
realization_class = pygrc_native_candidate
brief_class = native
pool_dependence_mode = state_carried
RCAE causal producer = none
RCAE external role = orchestration, declarations, matching, and guards only
```

Two distinct native source-node roles S1/S2 use admitted public packet calls to
contribute positive amounts to one native node-coherence carrier P. Native
departure/arrival processing implements additive U. Native packet/event state
retains L for audit. A fresh native feedback row reads P against held-fixed
B_ref; the model-owned feedback producer schedules the later native packet.
`expected_source_surface_digest` remains null so contribution-history identity
does not enter the state-carried response condition.

The later responder accesses P through the same one-node feedback mask without
source addressing. Exact node/edge IDs and numerical policy values remain I06
work; raw response, comparator, equality/resolution, and calibration rules
remain I04/I05 work.

Authority:

- [I03A input freeze](../contracts/p2-i2/i03a-state-carried-realization-freeze-input.json);
- [I03A realization/discriminator contract](../contracts/p2-i2/i03a-state-carried-realization-and-discriminator-contract.json);
- [I03A report](../reports/P2-I2-I03A-state-carried-realization-and-operational-hypothesis-freeze.md);
  and
- [state-carried operational-hypothesis profile](../hypotheses/p2-i2-operational-hypotheses.md).

### 12.3 Native intervention and control decision

Use admitted native transitions rather than add an RCAE causal clamp:

- pool-write freeze diverts the same source debits/amounts/times to K instead
  of P;
- carrier intervention sends native P-to-K flux after both contributions and
  before the neutral encounter;
- pure source-lineage permutation varies audit-only L while preserving P; and
- S1-S2 versus S2-S1 completes to equal P and therefore freezes response
  invariance for the state-carried profile.

CAP-04 and CAP-06 remain inadequate as broad generic capabilities. PyGRC still
lacks a byte-identical-audit state clamp and first-class atomic pool-write
gate. The selected native intervention is narrower: intervention identity may
differ, while contributor activity/attribution, support, and later opportunity
remain matched. If I06 cannot realize that boundary natively, reopen DEC-010
and the realization class before calibration or execution.

The private competitor uses P1/P2 native nodes and separately retained
one-node reads. Reading or aggregating both partitions is forbidden and
classifies the branch as mailbox/controller bypass. The R05 concept selects
the access-scope axis: an alternate eligible responder must use the same P read
class.

### 12.4 Producer and restoration boundary

RCAE schedules registered native operations and owns role/access declarations,
branch pairing, intervention identity, and the no-common-read guard. These are
externally composed identities, not an RCAE-computed pool or response.

Propose reset-aware native v2 for later registration:

```text
provider = pygrc.models.lgrc9v3_restoration_identity_v2
selection_status = proposed_by_I03A_not_frozen_until_I06
```

I06 must require a valid persisted reset baseline, forbid legacy fallback, and
compose every RCAE role/schedule/control component. Reset may be used only
under that later registered profile.

### 12.5 Gate and evidence effect

The state-carried package binds all seven cells, all five L02 controls, and
OP-01 through OP-09 with qualitative relations, held-fixed variables,
ambiguity boundaries, and fail-closed effects. It selects no raw response,
primary comparator, numerical threshold, resolution, aggregation, seeds,
exact fixture, or candidate outcome.

Therefore:

```text
P2-I2-I03A-REVIEW-READY = satisfied
P2-I2-DISCRIMINATOR-GATE = in_progress
P2-I2-I03B = unauthorized_pending_owner_review
P2-I2-I04 = blocked
scientific evidence = none
```

### 12.6 Reopening conditions

Reopen if owner review rejects or revises the state-carried mapping; an exact
fixture cannot realize native diversion/debit and private matching; V consumes
contributor history or labels; P is not one independently intervenable node;
private controls aggregate both partitions; any mandatory cell/control is
missing; v2 cannot cover the selected native state/reset lifecycle; an RCAE
causal pool/response transition becomes necessary; or I04/I06 numerical and
registration choices revise rather than instantiate this causal meaning.

## 13. `P2-I2-DEC-011` — Retain all three dependence modes

**Status:** accepted by project owner on 2026-07-14

**Question IDs:** `L02-Q03`, `L02-Q04`, and downstream I04–I11 scope

**Question:** After I03A, I03B, and I03C separately bind state-carried,
history-carried, and hybrid profiles, does P2-I2 select one mode for later
work, or retain all three?

### 13.1 Decision

P2-I2 retains and tests all three dependence modes. They are distinct causal
profiles, not competing candidates in a winner-selection stage:

```text
state_carried   -> mode-specific realization and controls
history_carried -> mode-specific realization and controls
hybrid          -> mode-specific realization and controls
```

Selection occurs within each profile. Native PyGRC is preferred when it is
adequate. When it is absent or inadequate, the smallest explicit producer-
assisted realization may be selected. If neither preserves the discriminator,
that mode retains a reviewed missing-prerequisite disposition rather than
being silently removed or converted into a negative L02 result.

### 13.2 Downstream effect

I04 through I11 remain mode-indexed:

- I04 must preregister each mode's response, comparator, controls, and whether
  measurement/calibration identity is validly shared or mode-specific;
- I05 must calibrate only that frozen structure without selecting a mode;
- I06 must register exact identities and implementations for all three modes
  or their reviewed missing prerequisites;
- I07/I08 must freeze and execute the retained mode-indexed finite matrix;
- I09/I10 must resolve controls and reconstruction separately by mode; and
- I11 must preserve all three mode dispositions inside one bounded lane-level
  terminal classification and developmental interpretation.

Convenience, code availability, anticipated cost, calibration behavior, and
candidate outcomes may not select or drop a mode. A shared response,
comparator, calibration identity, or implementation component is permitted
only when I04/I06 explicitly justify semantic equivalence; sharing cannot
erase mode-specific causal expectations.

### 13.3 Authority, preservation, and gate effect

This owner-accepted decision corrects the accepted brief's original singular
`selected dependence mode` and `selected realization` language. It preserves
`AE01-H-L02`, D-039, all seven logical cells, all five L02 controls, OP-01
through OP-09, the native-first rule, claim ceiling, and one lane-level
terminal classification.

It also preserves the original I03A input freeze as historical entry
authority. `P2-I2-CHG-008` carries the later scope transition and affected
cross-artifact revalidation.

This decision did not itself accept or revise DEC-010's state-carried
realization, authorize I03B or I04, perform runtime or calibration action, or
assign scientific evidence. DEC-010 was subsequently accepted as the causal-
design baseline for the separately governed DEC-012/I03AR1 path.

### 13.4 Reopening conditions

Reopen if a controlling Phase 1 contract prohibits mode-indexed execution; a
later owner decision explicitly returns to one-mode selection; I04 shows that
the stable metric contract cannot represent the three profiles without a
controlling-authority change; or resource limits require a scientific scope
reduction. Resource pressure alone cannot silently remove a mode.

## 14. `P2-I2-DEC-012` — Precalibration realization runtime conformance

**Status:** accepted by project owner on 2026-07-14

**Question:** Should the three I03 mode realizations remain static/source-
dataflow designs until I08, or receive bounded runtime conformance before
calibration?

### 14.1 Decision

Use the stronger, review-separated conformance path:

```text
I03A accepted causal design
  -> I03AR1 frozen state-carried runtime conformance -> owner review
  -> I03B design freeze + frozen history-carried runtime conformance -> review
  -> I03C design freeze + frozen hybrid runtime conformance -> review
  -> I04 only after the complete reviewed family
```

The original I03A input freeze remains immutable. I03AR1 receives a new input
freeze and separate conformance identities. I03B and I03C must freeze their
causal design before their first mode-specific runtime call and may not use an
earlier mode's output to resolve their realization.

### 14.2 Permitted evidence

Realization conformance may determine only whether the frozen implementation:

- executes declared native and producer-owned interfaces;
- preserves the declared causal state/history and audit factorization;
- realizes its frozen interventions and access/private guards;
- restores the complete continuation-relevant state;
- resets to the persisted baseline; and
- produces equal registered continuation under equal composite input.

This is candidate-shaped implementation behavior and must be named honestly.
It is not capability-audit evidence, calibration input, a lane control result,
or scientific support/falsification.

### 14.3 Mandatory quarantine

Each conformance iteration must freeze before execution:

- one deterministic fixture and exact values derived without runtime search;
- exact assertions, invocation count, one evidence run, one reconstruction
  replay, and no retry unless a separately classified infrastructure failure
  occurs;
- exact source/import/runtime identities and graph read-only guards;
- separate output and fixture IDs that cannot enter I04/I05 calibration or the
  I06/I07/I08 candidate bundle;
- prohibition of parameter search, rescue variants, scientific response/
  comparator selection, delta/threshold calibration, and mode ranking; and
- failure classification as `realization_inadequate`, `missing_prerequisite`,
  or `infrastructure_invalid`, never as an L02 result.

Observed conformance values may be retained for audit but cannot choose later
scientific values. Later registration must independently bind its exact
fixture, and I08 must execute the complete registered mode × cell × control
matrix.

### 14.4 Gate and reopening effect

DEC-012 authorizes only construction/validation of the I03AR1 freeze and then
its exact bounded run. I03B remains unauthorized until owner review of the
I03AR1 result. I04 remains blocked until the complete I03A/I03AR1/I03B/I03C
family is reviewed.

Reopen if conformance output is proposed as calibration or scientific
evidence; the fixture is tuned after observation; run limits change without a
new freeze; a graph write or unadmitted import occurs; or a later scientific
step is treated as already satisfied.

### 14.5 I03AR1 implementation disposition

The I03AR1 state-carried portion of DEC-012 is implemented and review-ready.
The immutable base freeze has SHA-256
`d21cc390ab6655ce98c7dbf6827a73d9b3d537c9d90cb98b81f8e2da510a1d94`.
Its original invocation stopped without output on a strict floating-point
representation assertion and is retained as `infrastructure_invalid` under
`P2-I2-I03AR1R1`/`P2-I2-CHG-010`.

The governed freeze revision changed only derived response-delta comparison
to absolute tolerance `1e-12`, relative tolerance `0`. Its replacement run
passed 136/136 assertions, and the sole reconstruction was byte-identical at
conformance SHA-256
`a7601bb1a7d335cfefc9d21aa365e3f5732ae0ebdfabe6bb7d168a7194ed0db0`.
This assigns bounded realization implementation-conformance only. Owner
acceptance/revision remains pending; I03B and I04 remain unauthorized.

## 15. `P2-I2-DEC-013` — I03AR1 progression acceptance and I03B entry

**Status:** accepted by project owner on 2026-07-14

**Question:** Does the review-ready I03A/I03AR1 state-carried package satisfy
its staged review boundary, and may the history-carried 8B iteration begin?

### 15.1 Decision

Accept the I03A causal design and quarantined I03AR1 runtime-conformance
package for staged progression. Begin `P2-I2-I03B` under its own checklist and
hypothesis declaration.

This is progression acceptance, not scientific support. The state-carried
profile remains fixed; its observed fixture values and outcomes may not select
the history-carried realization. I03B must independently:

- freeze its design/source-comparison inputs before comparing candidates;
- define active common causal history separately from encounter state and
  audit-only lineage;
- apply native-first selection within `history_carried` mode;
- freeze its causal design before the first mode-specific runtime call;
- if realizable, retain a second exact runtime-conformance freeze and bounded
  reconstruction under DEC-012; and
- stop for owner review before I03C.

### 15.2 Gate effect

DEC-013 closes the I03AR1 owner-review stop and opens I03B design work only.
It does not pass the umbrella discriminator gate, authorize I03C/I04, select a
history-carried realization, choose scientific values, or assign an L02
result.

Reopen if I03B uses I03AR1 outputs as selection evidence, rewrites the accepted
state-carried profile, runs before its own freezes, or is treated as permission
for later-mode or scientific work.

## 16. `P2-I2-DEC-014` — History-carried realization and producer boundary

**Status:** design-frozen; bounded runtime conformance passed; owner review
pending

**Question:** Can admitted PyGRC machinery natively realize one active,
independently intervenable common history, or what is the smallest adequate
producer-assisted boundary for 8B?

### 16.1 Source-current comparison

The native runtime owns an ordered packet/contact surface log, packet ledger,
producer configuration, snapshots, and reset-aware v2 identity. Those are
valuable source facts and audit/restoration surfaces. They do not by
themselves instantiate the required history-carried path:

- native contact rows are explicitly passive evidence;
- native feedback derives from the latest contact row and live node state,
  not a registered fold over several contribution events;
- `expected_source_surface_digest` compares one configured latest-row digest
  and would become a controller-addressed exact-event key if treated as the
  common history; and
- LGRC-0 causal-history artifacts are annotation-only and non-mutating.

The native option is therefore inadequate for `history_carried`. This does
not revise I01's audit classifications or the accepted I03A native
state-carried design.

### 16.2 Selected realization

Select `minimally_producer_assisted` with one bounded
`RCAEActiveHistoryAdapterV1` component:

```text
native arrivals to P
  -> source-label-free ordered physical tokens
  -> one external, independently intervenable H_P
  -> deterministic order-sensitive readout
  -> public native balancing packets materialize M_H
  -> native feedback/producer owns the later A-to-B transition
```

The adapter owns only the missing active-history carrier, its cursor,
history-only interventions, readout calculation, and the request for native
balancing packets. It may inspect admitted surface rows read-only. It may not
mutate PyGRC state directly, retain contributor identities in causal tokens,
read success/response state, apply the scientific response threshold, emit a
success field, or schedule the later response. PyGRC owns every coherence
mutation and the complete response evaluation/transition.

`H_P` is one ordered token tuple, not source-private mailboxes. The readout
family is a source-label-invariant left fold
`r_(j+1) = lambda * r_j + typed_amount_j` with `0 < lambda < 1`. Exact
scientific values remain I04/I06 work. A separate conformance freeze may bind
fixture-only values that are prohibited as later calibration inputs.

### 16.3 Discriminators and restoration

I03B freezes:

- a physical-token order shuffle that preserves marginal quantities and P at
  encounter while changing H_P/readout/response;
- an explicit active-history clamp with native contribution/audit/P matched;
- a state-only P intervention with H_P/M_H fixed and expected response
  invariance;
- native contribution diversion that prevents H_P admission while preserving
  source activity;
- audit-only lineage permutation with H_P/M_H/response invariance;
- separate H1/H2 private carriers with a strict prohibition on reading both;
  and
- one common H_P/M_H access scope usable by alternate eligible responders.

Native v2 identity covers the model, M_H, native logs/configuration, and native
reset baseline. It does not cover H_P, the consumed-row cursor, adapter
configuration/interventions, or adapter reset baseline. The realization must
therefore compose native v2 with complete current and baseline adapter
identity. Save/load/reset are paired composite operations; one-sided reset or
implicit rebase is forbidden.

### 16.4 Gate effect and reopening

DEC-014 authorizes construction and validation of one separate immutable
I03B runtime-conformance freeze under DEC-012. It does not authorize a runtime
call before that freeze validates, select a scientific response/comparator or
numeric value, assign an L02 result, or open I03C/I04.

Reclassify to `missing_prerequisite` before accepting runtime conformance if
the adapter must compute/schedule success, if H_P cannot be independently
intervened and restored, if the response path must consult contributor/audit
identity, if private histories must be combined, or if paired composite
save/load/reset and continuation cannot be demonstrated.

### 16.5 Runtime-conformance disposition

The separate freeze validated before runtime at SHA-256
`dd0146f656f3f480d5ff3265696cacf39322fa5fe13991aed822614eee217720`.
The sole evidence invocation passed `252/252` frozen assertions. The sole
reconstruction was byte-identical to the retained conformance artifact at
SHA-256
`4465ff2174d285d26ffa8a6cb4bebaf644b150d24bea0d69563eb5f51d8c177d`.
There were zero retries, rescue variants, searches, or graph mutations.

The bounded implementation demonstrated the declared separations: order
changed H_P/readout/native response with marginal quantities and P matched;
lineage-only permutation was invariant; active-history clamp changed the
response with P retained; state-only P intervention preserved H_P/M_H and the
response; private carriers remained separate; alternate access used the same
M_H/B_ref path; and paired native-v2/adapter save-load-reset plus equal-input
continuation matched. The adapter never computed or scheduled success. The
native feedback producer owned the later response transition.

This establishes implementation conformance only. It supplies no scientific
effect, response/comparator, calibration input, registered value, L02 support
or falsification, or inter-mode ranking. I03B is now review-ready. DEC-014
does not authorize I03C/I04; explicit owner acceptance/revision is required.

### 16.6 I03BR1 closeout-revalidation note

The project owner's twenty-one-point acceptance review was handled under a
separate checklist-first `P2-I2-I03BR1` audit and `P2-I2-CHG-011`; it does not
rewrite DEC-014. The exact I03B harness, adapter, freezes, evidence invocation,
and reconstruction remained immutable. No model or runtime operation ran.

The revalidation passed all twenty-one checks with zero blockers. In
particular:

- the common neutral contact follows materialization; the two order branches
  match its physical route/contact/schedule fields, while the remaining node-
  proper-time and digest differences do not enter native polarity/threshold
  evaluation and `expected_source_surface_digest` remains null; and
- H_P is persistent independently intervenable state, R_H reads H_P, and M_H
  is its native output port. The clamp replaces H_P before recomputation and
  native rematerialization.

Six downstream obligations are retained without changing the I03B
disposition: unique registered source-to-P admission or an explicit route key;
scientific access resolution; bounded lifecycle/event counts; an I06 paired-
restoration interface with explicit manifest-component validation; branch
identity retention; and I04/I06 rejection of every conformance fixture value
and digest. The active-history claim remains bounded to an ordered history
causally materialized through a deterministic scalar readout; no irreducible-
history or non-Markovian claim is assigned.

`P2-I2-I03BR1-CLOSEOUT-PASSED` makes I03B acceptance-ready. It grants no
progression authority. Consistent with the owner's review, any acceptance must
be a new decision after DEC-014 that opens I03C only, retains
`minimally_producer_assisted`, leaves history-carried scientific status
unresolved, and keeps I04 blocked.

## 17. `P2-I2-DEC-015` — I03B progression acceptance and I03C entry

**Status:** accepted by the project owner

**Question:** Does the I03B/I03BR1 package satisfy the staged-progression
boundary, and may I03C/8C begin?

**Decision:** Yes. The project owner's direction that 8C is next:

- accepts the I03B causal design for staged progression;
- accepts the 252/252, byte-reconstructed runtime result as implementation-
  conformance evidence only;
- accepts the I03BR1 21/21 zero-blocker closeout and carries its six downstream
  obligations forward;
- retains `minimally_producer_assisted` for history-carried mode;
- leaves history-carried scientific status unresolved;
- authorizes I03C design work only after its checklist/hypothesis declaration
  and design input freeze; and
- keeps I04, R01-R05, calibration, registration, candidate/control execution,
  and scientific interpretation unauthorized.

I03C must apply native-first selection independently within `hybrid`. It must
not use I03A/I03B observed fixture values or outcomes to choose its
realization. If a realizable design is selected and statically validated, one
separate immutable conformance freeze may authorize the bounded evidence and
reconstruction invocations already governed by DEC-012.

DEC-015 does not pass `P2-I2-DISCRIMINATOR-GATE`. I03C must return for owner
review after design and any bounded runtime conformance; I04 remains blocked
until the complete three-mode family has been reviewed and explicitly
accepted under the umbrella gate.

## 18. `P2-I2-DEC-016` — Hybrid realization and producer boundary

**Status:** design-frozen, statically validated, and runtime-conformant;
owner review pending

**Question:** Which native-first hybrid realization, separately causal state
and history components, joint response path, and restoration boundary should
I03C retain?

**Decision:** Select `minimally_producer_assisted` for hybrid mode.

- `C_P` is live native P coherence.
- `H_P` is one ordered source-label-free active history owned by the exact
  pre-runtime `RCAEActiveHistoryAdapterV1` structural component.
- `R_H(H_P)` is materialized through public native balancing packets at
  native output node `M_H`.
- Native PyGRC feedback reads P and M_H exactly once each in one common front
  mask, against B_ref; the native producer owns score, threshold/polarity,
  response scheduling, and the later packet transition.
- A native P-only debit and an adapter history-only replacement/clamp must
  independently affect the same joint path while holding the other component
  fixed.
- `expected_source_surface_digest` remains null, and a common neutral contact
  follows all final component interventions; audit lineage cannot authorize
  or enter the response.

Complete native realization is inadequate only because admitted PyGRC has no
active independently intervenable multi-event common-history carrier. The
existing adapter supplies exactly that missing operation and may not read P
for success, compute P+M_H, apply the response threshold, configure/execute
feedback, schedule A-to-B, or inspect response/success fields. If runtime
conformance requires any such expansion, the realization stops as
`missing_prerequisite` rather than silently widening the producer.

I03C reuses no I03A/I03B conformance coefficient, amount, timing, threshold,
branch outcome, comparator, or evidence digest. Its separate runtime freeze
must use new fixture-only values, one evidence invocation, one reconstruction,
and zero retries. Native v2 and the complete adapter current/reset identity
must be bound in one composite identity; native and adapter reset are one
paired registered procedure.

DEC-016 freezes causal-design authority only. It assigns no scientific
response, comparator, resolution, R01-R05 outcome, mode rank, L02 support, or
terminal class. A successful static validation authorizes construction of the
separate conformance freeze under DEC-012; only owner review after bounded
runtime conformance may address the umbrella gate. I04 remains blocked.

The separate runtime freeze validated before the first model call. Its single
evidence invocation and single reconstruction each passed `258/258` frozen
assertions with byte-identical SHA-256
`217c8972e8e1199409343fb72b0eca12b2ba24dceb6a1f213c97af9143f0e96c`.
Both state-only and history-only interventions changed the same native joint
response relation while holding the other component fixed; order, label,
write-diversion, private/access, producer-ownership, neutral-contact, paired
restoration/reset, and equal-input continuation guards passed. This adds only
quarantined realization implementation-conformance. I03C is review-ready;
the umbrella gate and I04 remain blocked pending owner disposition.

## 19. `P2-I2-DEC-017` — Hybrid closeout revalidation disposition

**Status:** zero-runtime closeout passed; owner acceptance pending

**Question:** Does the retained I03C package satisfy the exact twenty-six
owner-review areas and seventeen acceptance conditions, and what progression
authority follows from that audit?

**Disposition:** `P2-I2-I03CR1-CLOSEOUT-PASSED`.

The immutable I03CR1 review input and closeout registry bind one composite
P/H_P/M_H carrier, independent component interventions through the same
native V, complete future qualitative P × H factorization, exact admission
and self-feedback exclusions, neutral-contact qualifications, common/private
bindings, layered restoration identity, lifecycle dispositions, hybrid OP
meanings, and complete machine fixture quarantine. The zero-runtime validator
passed all 26 review checks and all 17 acceptance conditions with zero
blockers. It classified 17 checks as direct passes, four as closure
clarifications, and five as passes carrying downstream duties.

Eight fail-closed obligations remain: register the full qualitative 2x2;
bind physical admission route/type identity; match or stratify causal neutral-
contact timing/support fields; expose and failure-test one paired restoration
boundary; bound lifecycle/capacity semantics; mechanically reject every
fixture value/identity/observation/outcome/digest; reject common/private
cross-load; and perform a separate three-mode family closeout before the
discriminator gate.

The closeout retains three explicit limits. I03C did not execute the complete
scientific 2x2. Restoration completeness is layered across native v2,
adapter, joint binding, freeze, manifest, evidence, and reconstruction rather
than supplied by one new atomic native API. Neutral-contact absolute scheduler
slots differ after explicit intervention operations, although those slots do
not enter the native score or threshold and remain an I06 matching duty.

DEC-017 records acceptance readiness only. It does not assign project-owner
acceptance, authorize the umbrella family closeout, pass
`P2-I2-DISCRIMINATOR-GATE`, or open I04. If the project owner accepts I03C,
the next permissible step is to declare the umbrella I03 family closeout in
the checklist and hypotheses before performing it.

## 20. `P2-I2-DEC-018` — I03C acceptance and compact family-closeout entry

**Status:** accepted by project owner

**Question:** May the staged program move from the accepted hybrid package to
section 8.1, and must that closeout repeat the prior mode reviews?

**Decision:** Accept I03C/I03CR1 for staged progression and open only the
separately checklist- and hypothesis-declared `P2-I2-I03F` family closeout.

The project owner directed “we can move to 8.1 next,” then clarified that many
full reviews had already been completed and another should occur only if
critical. I03F therefore trusts the accepted A/B/C mode-level findings. It may
check terminal authority identity, omission/substitution, cross-mode rewrite,
OP coverage, obligation/quarantine loss, restoration-owner indexing, no
ranking, and the I04 import boundary. It may not repeat capability, source,
dataflow, restoration, or runtime conformance reviews.

DEC-018 assigns no scientific status and does not pass the discriminator gate
or open I04. I03F must freeze its compact scope first and return a retained
gate-readiness package for owner review.

## 21. `P2-I2-DEC-019` — Compact family-closeout readiness

**Status:** validation passed; subsequently owner-accepted under DEC-020

**Question:** Do the three accepted mode packages compose losslessly enough to
place `P2-I2-DISCRIMINATOR-GATE` before the owner?

**Disposition:** `P2-I2-I03F-REVIEW-READY`.

Eleven terminal authorities match accepted baseline commit
`fc3fb0f638eb0b180cb05d081e6dc447f24af66b`. The compact family index retains
exactly three required and unranked profiles, all 27 OP-mode pointers, each
mode's accepted carrier/intervention/access/producer/restoration summary, all
six I03BR1 and eight I03CR1 obligations copied exactly, nine consolidated
duties covering each source obligation once, the complete three-mode fixture
quarantine, and an unchanged mode-indexed I04 import rule.

The validator passed 12/12 integration checks and 9/9 acceptance conditions
with zero blockers. It performed no repeated source/capability review, model
execution, runtime conformance, reconstruction, scientific selection, or
mode ranking. No downstream obligation is discharged; the family-gate duty
remains pending owner acceptance.

DEC-019 establishes gate readiness only. It cannot pass
`P2-I2-DISCRIMINATOR-GATE` or authorize I04 without an explicit project-owner
disposition.

That later owner disposition is retained in DEC-020 and does not retroactively
turn DEC-019's validation into owner authority.

## 22. `P2-I2-DEC-020` — I03F acceptance and I04 entry

**Status:** accepted by project owner

**Question:** Does the compact three-mode family package satisfy the owner gate,
and what downstream work may begin?

**Decision:** Accept I03F without selecting or ranking a mode, pass only
`P2-I2-DISCRIMINATOR-GATE`, and open checklist- and hypothesis-governed I04
calibration-preregistration construction.

The project owner's direction “in that case, let's continue with I04” follows
the explicit discussion of why I04 is the substantive measurement-choice gate
and why I05–I07 should remain compact but separate. It constitutes acceptance
of the already review-ready I03F package, not acceptance of any later
measurement, calibration, registration, or cycle.

All three accepted modes remain retained and unranked. DEC-020 assigns no raw
response, comparator, calibrated resolution, control outcome, R01–R05 rung, or
L02 conclusion. It authorizes no matched-null or candidate execution. I04 must
first freeze and validate those choices under the complete I03 fixture
quarantine and return for owner review.

## 23. `P2-I2-DEC-021` — I04 measurement and calibration preregistration

**Status:** historical candidate-free validation retained; superseded for
progression under DEC-022/DEC-023

**Question:** What exact scientific measurement and analysis should all three
retained modes use, which insufficient-repetition alternative owns the primary
margin, and what candidate-blind null may I05 execute?

**Disposition:** `P2-I2-I04-REVIEW-READY`.

I04 selects native B-target coherence gain across one bounded native response
window as the raw later-continuation response. Identity orientation makes
higher gain aligned. The downstream response, unit, window, aggregation,
missingness, comparator role, and analysis-only calibration population are
semantically equal across modes, so one response, analysis, and matched-null
identity are shared. Upstream carrier causes and controls remain mode-specific.

The primary candidate is two-source common-carrier constitution in both frozen
source-role orders. Each order is separately paired against a quantity- and
timing-matched repetition by one source. This is the closest D-039
insufficient-repetition explanation because it preserves total contribution and
the inherited single-source relation while removing multi-source constitution.
Contributor removal, order/shuffle, private partitions, and controller
substitutions remain mandatory signed or causal-chain controls. Neither order
nor seed margins may be scalar-collapsed.

Scientific no-response is retained as zero; operational failure leaves the
complete mode/seed two-order panel not evaluable. The frozen analysis converts
nine common and 3/3/5 mode-specific rule sets into machine `pass`, `ambiguous`,
or `fail` inputs. Hybrid retains its complete qualitative P-by-H_P factorial
without requiring synergy or nonlinearity.

The shared candidate-blind null contains five disjoint calibration seeds by two
order strata, with equal exact-rational response pairs. It exercises only the
shared paired-margin analysis. Its estimator remains
`max(1e-12, max(abs(null_margin)))`; no null was executed and `delta` remains
pending I05. The entry point refuses to run without a later I05 freeze that
records owner CAL-PRE acceptance, authorizes exactly one null invocation,
retains candidate prohibition, and binds the exact I04 identities.

Static validation passed 16/16 checks and 10/10 pure unit tests. It found no
I03 fixture-value/branch/digest reuse, no PyGRC import or model instantiation,
no matched-null or candidate invocation, and no graph mutation. Exact
scientific topology, contributions, thresholds, routes, and response amount
remain I06 fields.

The project owner's later critical review withheld acceptance because this
primary comparator could preserve a source-label-free complete carrier while
being required to diverge. DEC-021 remains exact historical construction but
cannot pass CAL-PRE or govern progression. DEC-022 opens the correction and
DEC-023 records its revised review-ready disposition.

## 24. `P2-I2-DEC-022` — Critical-review authority and I04R1 entry

**Status:** accepted as the controlling correction trigger

**Question:** What gate and artifact effect follows from the project owner's
critical I04 review?

**Decision:** Withhold `P2-I2-CAL-PRE-GATE`, preserve the complete original I04
package as historical evidence, and open only the checklist- and hypothesis-
declared `P2-I2-I04R1` candidate-free correction.

The load-bearing conflict is semantic rather than cosmetic. Quantity-matched
repeated-source constitution was accepted as an equivalence-permitted scope
diagnostic, but original I04 required it to be the divergent primary
comparison. A source-label-free additive P, H_P/M_H, or hybrid carrier can be
identical under those conditions, so equality cannot decide absence of a
shared pool.

I04R1 must choose a carrier-changing primary comparison, retain repeated-S1
and repeated-S2 over physical q orders, separate top metric signature from
causal failure, limit I05 to analysis arithmetic, freeze an outcome-independent
window and B-purity boundary, keep mode evidence independent, derive causal
status from provenance, and reconstruct choice rationale without I03
conformance observations.

DEC-022 authorizes static source inspection, corrected policies/code/tests,
and focused candidate-free validation only. It authorizes no matched-null,
PyGRC model, candidate/control cell, calibration value, or scientific result.

## 25. `P2-I2-DEC-023` — Corrected I04R1 preregistration readiness

**Status:** historical focused-validation readiness; superseded for progression
by owner-accepted I04R2 under DEC-026

**Question:** Does the corrected package resolve every load-bearing review duty
without importing candidate or conformance outcomes?

**Disposition:** `P2-I2-I04-REVIEW-READY` under the corrected I04R1 identities.

The primary margin now compares combined common-carrier admission against the
maximum oriented response of two predeclared symmetric leave-one arms:
q1 admitted/q2 activity-matched and diverted, and q2 admitted/q1 activity-
matched and diverted. Both raw arms remain visible. Repeated-S1 and repeated-S2
remain mandatory scope diagnostics in q1-then-q2 and q2-then-q1 physical
orders; complete-carrier equivalence cannot by itself fail R03.

Native B-target coherence gain remains the shared downstream response but now
has an exact six-slot, two-step outcome-independent protocol and binary-like
zero/one-packet semantics. Empty queues, matched B baseline, no B causal route
or background/topology update, and one response arrival as B's sole permitted
change are registration duties. Exceptions, incomplete/delayed chains,
residual queues, or unrelated B changes are operational null rather than
scientific zero.

Future I05 `analysis_arithmetic_delta` covers only rational parsing, float
conversion, margin arithmetic, serialization, and reconstruction. I06 must
admit `r >= 1024*1e-12` and `r >= 1024*max(ulp(B_before),
ulp(B_before+r))`, require finite JSON roundtrip, and register every runtime/
restoration/continuation tolerance separately below `r/1024`.

The pure analyzer accepts one mode at a time and derives candidate/private/
controller status from masks, source arrivals, call provenance, native packet
lineage, configuration, and receipts. Shared extraction never pools or
compensates modes. A non-top history/hybrid order panel is not automatic causal
failure.

Focused validation passed 19/19 checks and 15/15 pure tests. Original I04
remains byte-exact history; all seven I03 conformance sources remain
quarantined; no PyGRC model, null, candidate/control invocation, I05 artifact,
or graph mutation occurred. DEC-023 is readiness, not owner acceptance.
CAL-PRE, I05, registration, execution, R01-R05, and interpretation remain
closed.

## 26. `P2-I2-DEC-024` — Conditional-review authority and I04R2 entry

**Status:** accepted as the controlling machine-verification trigger

**Question:** What gate and artifact effect follows from the project owner's
conditional I04R1 review?

**Decision:** Preserve the complete I04/I04R1 packages as exact history and
open only checklist- and hypothesis-declared `P2-I2-I04R2` candidate-free
machine verification. The supplied review resolves the conceptual comparator
blocker but conditions acceptance readiness on eight exact machine invariants:
all-or-none two-arm evaluability, the full raw three-arm I05 estimator route,
matched diversion, exact native response gain, window validity before zero,
non-gating repeated-source diagnostics, independent order classification, and
receipt-derived causal status.

DEC-024 authorizes exact-source inspection, compositional machine policies,
pure analysis/future-I05 code, focused unit/static verification, and a compact
owner-review surface. It authorizes no matched-null invocation, PyGRC model,
candidate/control execution, calibration value, I06 registration, R01-R05
effect, or L02 result. The conditional review is not itself inferred to be the
project owner's explicit CAL-PRE acceptance.

## 27. `P2-I2-DEC-025` — I04R2 machine-verification readiness

**Status:** historical acceptance-readiness disposition; subsequently accepted
under DEC-026

**Question:** Does I04R2 enforce every conditional invariant exactly while
preserving the candidate-free and historical-identity boundaries?

**Disposition:** `P2-I2-I04R2-ACCEPTANCE-READY`.

The primary analyzer requires candidate, q1-only, and q2-only scientific
records for one identical mode/seed/physical-order/pairing/opportunity/window/
B-baseline tuple before selecting the within-tuple maximum. Any invalid arm
makes the complete tuple nonevaluable; no surviving-arm or cross-tuple maximum
is permitted.

Focused verification found one substantive implementation gap. The I04R1
future calibration entry point called normalized-difference arithmetic on an
already paired response, bypassing the new strongest-marginal comparator. The
I04R2 entry point now builds raw candidate, q1-only, and q2-only response
envelopes and calls the exact `primary_margin` route, then writes, reads,
parses, and byte-reconstructs the governed output. This preserves I05 as
arithmetic-only while exercising selection, pairing, floor, normalization,
serialization, retained-output readback, and reconstruction through the same
estimator path.

The machine overlay also freezes the complete I06 diversion/noninterference
receipt set; requires measured B gain to equal current native packet-amount
addition within an independent runtime tolerance and an I06-registered finite
closed domain; validates evaluation, producer, queues, exact step events, and
contamination before scientific zero; keeps repeated-source equivalence
non-gating; keeps non-top order panels independently classifiable; and derives
causal status from eight receipt classes rather than authored summaries.

Validation passed 16/16 focused checks and 7/7 pure tests and reconstructed
byte-identically. All ten I04R1 identities remained exact; all seven I03
conformance sources remained quarantined; graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594` remained clean. No PyGRC model,
matched null, candidate/control invocation, I05 authorization/output, or graph
mutation occurred.

DEC-025 records readiness, not owner acceptance. DEC-026 subsequently records
that acceptance, passes CAL-PRE, and makes I04R2 the sole progression
authority. DEC-025 itself remains immutable historical readiness evidence.

Reopen DEC-025 if any validated identity changes; either leave-one arm can be
dropped; a maximum can cross mode/seed/order strata; future I05 bypasses the
raw three-arm route; native arrival semantics change; or I06 cannot register
the frozen diversion, domain, gain, window, order, or causal-receipt duties.

## 28. `P2-I2-DEC-026` — I04R2 owner acceptance and CAL-PRE passage

**Status:** accepted by project owner

**Question:** Does the project owner accept I04R2, which I04 lineage governs
progression, and what exact downstream authority follows?

**Decision:** Accept I04R2 without further scientific revision, pass
`P2-I2-CAL-PRE-GATE`, and designate I04R2 as the sole progression authority.
Original I04 and I04R1 remain immutable historical artifacts documenting the
superseded comparator and correction path; neither is a parallel active
preregistration or an independently executable calibration route.

Machine gate record:
[I04R2 owner acceptance and CAL-PRE passage](../contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json).

The owner found no remaining correctness blocker and explicitly confirmed the
complete-arm, within-tuple maximum, arithmetic-only null, fail-closed diversion,
fixed-window scientific-zero, separate runtime-tolerance, non-gating repeated-
source, order-conditioned, receipt-derived causal, fixture-quarantine, and
candidate-free boundaries. The deterministic q1-only exact-tie rule carries
comparator provenance only and must never acquire scientific meaning.

CAL-PRE passage authorizes only checklist- and hypothesis-first construction of
one separately frozen I05 authorization permitting exactly one arithmetic-null
invocation. It does not itself create that freeze or invoke the null. I06,
PyGRC runtime, candidate/control execution, R01-R05, L02 interpretation, and
mode selection/ranking remain closed.

The accepted I04 lineage must be committed before the I05 authorization freeze
is constructed, so that the latter can name the accepted source commit while
binding the exact I04R2 parent-analysis, machine-policy, calibration-policy,
entrypoint, and preregistration identities.

Reopen DEC-026 only on contradictory evidence or drift in an accepted I04R2
identity or invariant. Navigation correction that preserves those bytes is
housekeeping, not another scientific I04 revision.

## 29. `P2-I2-DEC-027` — Proposed I05 single-invocation authorization freeze

**Status:** proposed but blocked by I05A; owner acceptance and commit are not
authorized

**Question:** Has the separately required I05 execution freeze bound the exact
accepted I04R2 lineage, limited authority to one arithmetic-null invocation,
and remained unconsumed during construction?

**Proposed decision:** Accept the execution-freeze candidate at
`contracts/p2-i2/i05-calibration-execution-freeze.json` has SHA-256
`97a78f7f5e8b1119ec059b82a7a5b6c14c573efc55411ac4392ff6cf2703545a`.
It binds DEC-026, owner-acceptance record digest
`2ade4d6255c42044621489e1132d1030f48266e851bea614a11f1100c4f7dacf`,
accepted-I04 commit `b7b008c402d837b529962a1a5edb062927939d28`, and
the exact parent-analysis, machine-policy, calibration-policy, calibration-
entrypoint, and I04R2-preregistration identities.

The frozen I04R2 authorization validator accepts the candidate. A focused
zero-invocation audit passed 12/12 checks and reconstructed byte-identically.
The validator imported only `validate_execution_authorization`; it never
called the arithmetic-null builder or entry point and never imported PyGRC.
The governed calibration output remains absent. Construction accounting is
zero matched-null, PyGRC, candidate, and control invocations.

I05A subsequently tested the owner's three execution-safety conditions without
running the null. Only 3/8 checks passed. The current path has no attempt-time
consumption token, atomic concurrent-start exclusion, unambiguous failed-attempt
retry identity, committed-I05/environment/command/clean-worktree preflight, or
retained consumption/count/refused-second-start receipt. Its one-build,
readback-only reconstruction path is valid but insufficient by itself.

Until a separately authorized correction closes all five blockers, this
decision cannot be accepted or committed and makes no future invocation
mechanically permissible. It does not currently activate
or consume that invocation, compute or freeze
`analysis_arithmetic_delta`, update the metric sheet, pass CAL-GATE, open I06,
or assign operational-hypothesis/scientific evidence. Candidate execution
remains false. No commit may occur before explicit owner review and commit
authorization.

Reject or revise proposed DEC-027 if the authorization bytes or any bound I04R2 identity drift;
the accepted commit or acceptance record cannot be reconstructed; the
governed output appears without the exact authorized call; more than one
invocation is attempted; candidate authority becomes true; or retained-output
reconstruction fails after the future invocation.

## 30. `P2-I2-DEC-028` — I05-owned execution-safety correction authority

**Status:** accepted by project owner for bounded correction construction

**Decision:** Correct the five I05A blockers strictly inside I05. Add one
governed wrapper, one one-shot policy, and atomic attempt/final receipt
mechanics. Governed attempts equal one, infrastructure retries equal zero, and
an atomic claim must precede any accepted-builder call and survive every
failure or crash. Concurrent, later, and simulated-post-crash starts must be
refused.

Runtime preflight must bind the expected committed I05 authority through an
explicit post-commit HEAD argument, committed-blob equality, owner acceptance,
clean authority/index state, exact interpreter/normalized command, wrapper and
policy identities, and unchanged I04R2 hashes. No file inside the authority
commit may attempt to embed that same commit's self-referential hash.

The future governed path may invoke the accepted I04R2 builder exactly once.
Reconstruction may only read, parse, canonicalize, and compare retained output.
Attempt/final receipts must retain one attempted null invocation, zero
reconstruction generations, one output readback, consumed authority, and
mechanical refusal of a second start.

I05B safety validation must exercise all eight owner-required refusal cases
with zero accepted-builder invocations. This decision does not authorize the
null, a commit, CAL-GATE passage, I06, candidates/controls, or any scientific
result. The correction returns uncommitted for owner review. Accepted I04R2
scientific bytes are immutable. Proposed DEC-027 remains failed-closed history
and is not rewritten.

**Construction result:** I05B adds exactly one governed wrapper and one one-shot
policy. Ten focused zero-null tests cover all eight owner-required refusal
cases plus policy/hash and final-receipt shape. Machine validation passes 12/12
and reconstructs byte-identically with zero accepted-builder/null, PyGRC,
candidate, or control invocations. The future owner-acceptance record, attempt/
final receipts, and governed output are absent. The correction is uncommitted,
inactive, and returned for owner review; this result does not expand DEC-028's
gate effect.

Reopen DEC-028 if implementation would require changing accepted I04R2 bytes,
more than one attempt, a retry, deletion/reuse of a claim, a self-referential
commit identity, null execution during validation, or broader scientific scope.

## 31. `P2-I2-DEC-029` — I05B owner acceptance and retention authority

**Status:** accepted by project owner; commit authorized

**Decision:** Accept the complete I05B one-shot correction and commit the
I05/I05A/I05B authority package. DEC-027 remains failed-closed historical
evidence and DEC-028 remains the bounded correction authority.

Acceptance and launch are distinct. The immutable machine acceptance record
sets owner acceptance and commit authorization true while retaining
`null_invocation_authorized=false`. A separately directed 10.4 machine launch
record must set that field true before the permanent attempt claim can be
created. Both records, the wrapper/policy, the authorization freeze, validation,
governance, and unchanged I04R2 authorities must be committed and byte-equal at
the exact launch HEAD.

The accepted package additionally confirms repository-local non-temporary
claim storage on local `ext4`, rejects symlink path components, and treats an
empty, partial, broken-symlink, concurrent, crashed, or earlier claim as
consumed. Twelve focused tests and 12/12 zero-null checks pass with no builder,
null, PyGRC, candidate, or control operation. CAL-GATE remains closed.

DEC-029 authorizes the acceptance-package commit. It does not itself invoke the
null, assign `analysis_arithmetic_delta`, freeze the metric sheet, pass
CAL-GATE, or open I06. The owner's subsequent explicit direction to proceed
with 10.4 after this commit is recorded separately under that activity.

Reopen DEC-029 if acceptance and launch are conflated; the accepted package is
not committed together; the claim location becomes temporary, symlinked, or
non-atomic; accepted I04R2 bytes drift; or any execution occurs before exact
committed launch authority and clean preflight.

## 32. `P2-I2-DEC-030` — Single arithmetic-null launch authority

**Status:** accepted by project owner after I05B commit

**Decision:** The project owner's clarification “after commit that is”
explicitly directs execution of 10.4 after accepted authority commit
`c1f821dfd543d10d8555ddf2b52dbd56dfa76c13`. Create the exact separate machine
launch record already frozen by the accepted I05B wrapper, commit that record
together with this checklist/hypothesis/decision authority, and then invoke the
one-shot wrapper exactly once against that clean launch HEAD.

The launch retains one governed attempt, zero infrastructure retries, candidate
authority false, unchanged I04R2 hashes, exact interpreter/command identity,
local ext4 permanent claim storage, and the immutable owner-acceptance digest.
The wrapper must atomically claim before the accepted builder and retain one
claim, one final receipt, one governed output, zero reconstruction generations,
one readback, and a refused second start. A post-claim failure consumes the
attempt and cannot be retried.

DEC-030 authorizes only the pure analysis-arithmetic matched null and subsequent
readback/metric-freeze validation. It does not authorize PyGRC, candidate or
control execution, runtime/measurement tolerance, R01-R05 assignment, L02
support/falsification, mode ranking, CAL-GATE passage, or I06. The completed
package returns as `P2-I2-I05-EXECUTION-REVIEW-READY` for owner review.

Reopen DEC-030 only before claim if the launch record, accepted authority,
clean HEAD, interpreter/command, filesystem, or immutable I04R2 identities fail
preflight. After claim, retain failure and do not reopen authority for a retry.

## 33. `P2-I2-DEC-031` — Active `.venv` pre-claim correction

**Status:** correction owner-approved and committed; historical authority for
the later single governed attempt

**Decision:** Preserve the project owner's rule “always use venv.” The exact
governed command remains `.venv/bin/python`; the process must report an active
venv whose prefix is the repository `.venv`; and `sys.base_prefix` must differ.
The wrapper must validate that lexical command path without following its final
symlink, then separately resolve the target binary and require the already
frozen CPython version and SHA-256 digest.

The accepted wrapper incorrectly reused its repository-data `_path()` guard for
the interpreter. Because the valid `.venv/bin/python` chain resolves to
`system-interpreter:python3.12`, final preflight at launch commit `98770ae` failed with
`OneShotError` before claim. This created no attempt claim, builder/null call,
output, final receipt, PyGRC model, candidate/control action, or scientific
result. The one governed attempt remains unconsumed and infrastructure retries
remain zero.

I05C may change only interpreter path/identity validation and consequential
wrapper, policy, acceptance, launch, test, validation, governance, and report
hashes. It must add a direct positive test using the real active repository
venv and retain negative wrong-command/path/digest/inactive-venv checks. I04R2,
the null builder and inputs, one-shot claim/output mechanics, estimator,
candidate exclusion, and evidence effect are immutable.

Return the zero-null correction uncommitted for review. No further preflight or
governed invocation may occur until the corrected authority is reviewed,
explicitly authorized for commit, committed together, and cleanly revalidated.

Reopen DEC-031 if correction would permit a direct system-Python command,
accept an inactive or different venv, weaken the target digest/version, change
scientific bytes, or create/reuse a governed attempt.

## 34. `P2-I2-DEC-032` — P2-I2-wide persisted-path portability audit

**Status:** audit review-ready; correction blocked on owner acceptance of the
exact inventory

**Decision:** The project owner states that absolute paths are never allowed
and accepts the proposed P2-I2-wide portability audit/correction freeze. I05D
must first audit the complete current-tree P2-I2 artifact and implementation
surface under the AE01 experiment using a deterministic policy frozen before
inspection. The audit must classify filesystem-absolute, drive-prefixed,
home-expanded, and embedded machine-local path tokens as violations wherever
they are persisted in data, commands, receipts, reports, tests, or source.

The inventory may retain only repository-relative affected-file identities,
field or line locations, violation classes, counts, and digests. It must not
copy a forbidden value into its own records. Non-path URIs and mathematical
slash notation are not filesystem paths. Historical Git objects remain
immutable and are referenced only by commit and SHA-256; history is not
rewritten.

I05D authorizes static audit construction and execution with the repository
`.venv` only. It authorizes no affected-artifact correction, null builder,
one-shot wrapper, PyGRC model, candidate/control, conformance, calibration,
response-envelope, or scientific operation. The audit must group violations
into dependency-aware correction batches beginning with the active I05 package
and return uncommitted for review.

I05E remains blocked until the owner accepts that exact inventory. Future
correction groups must preserve historical execution lineage by commit/digest,
label portable projections honestly, preserve the consumed one-attempt/
zero-retry fact, and never rerun the null. Every group returns for review before
the next begins. CAL-GATE and I06 remain closed.

Reopen DEC-032 if the audit scope omits a P2-I2 persisted surface, reproduces a
forbidden value, treats machine provenance as an exception, edits an affected
artifact before audit acceptance, rewrites history, or invokes any runtime or
scientific path.

**Audit result:** The corrected scanner inspected 135 files and retained 312
value-redacted violations in 70 files. The frozen correction order is I05
active execution/closeout first, followed by I04/I05 authority dependencies,
I03 realization/conformance, I01/I02 source/identity, and governance/navigation/
shared projections. No affected artifact was corrected and every runtime or
scientific invocation count is zero.

During I05D construction, the first discovery pass showed that two recursive
selectors selected directories rather than nested files. Their form and
explicit nested-file coverage guards were corrected inside I05D before the
review inventory was retained. This was not a separate iteration and changed
no classification, redaction, grouping, historical, runtime, scientific, or
gate rule.

## 35. `P2-I2-DEC-033` — I05D acceptance and first I05 correction group

**Status:** accepted by project owner; first I05 correction group accepted and
commit-authorized

**Decision:** The project owner's statement that proceeding is the right move
accepts the exact I05D inventory and opens only the first I05E correction
group. The group is the eleven affected I05 files listed in checklist section
10.4C plus consequential I05 authority/projection identities required to keep
historical raw evidence and current portable derivatives explicit.

The group may replace persisted repository locations with normalized relative
identities, replace external locations with stable logical IDs plus existing
digest/version/capability facts, remove hard-coded machine paths and shebangs,
and create a portable-lineage manifest. Original raw execution bytes remain
historical Git evidence referenced only by commit and SHA-256. Current portable
derivatives must identify themselves as projections and cannot impersonate the
raw receipts.

The correction must preserve the permanent consumed-attempt guard, one
attempt, one builder call, zero retries, one readback, refused second start,
accepted I04R2 estimator, three-arm values, ten margins, arithmetic delta, and
candidate/runtime/PyGRC exclusions. It may invoke no null builder, one-shot
wrapper, PyGRC model, candidate/control, conformance, calibration, or scientific
path. Return the group uncommitted for owner review. Later correction groups,
metric freeze, CAL-GATE, I06, and candidate execution remain closed.

Reopen DEC-033 if the group expands beyond exact consequential identities,
changes scientific or one-shot facts, loses historical lineage, leaves an I05
absolute-path violation, invokes a prohibited path, or begins a later group
before review.

**Outcome:** The exact group passed review and is commit-authorized. Its frozen
validator passes 10/10 with zero path violations across all eleven corrected
files; the focused helper suite passes 13/13 under `.venv`. The raw execution
output, claim, and final receipt reconstruct at `c3eabf3`; the current output
and claim identify themselves as portable projections; the final receipt is
byte-unchanged; the read-only consumed claim remains present. No governed null,
wrapper entry point, builder, PyGRC, candidate/control, conformance,
calibration, or scientific operation occurred in I05E.

The project owner explicitly accepts this result, authorizes its commit, and
directs progression to the next bounded group after retention. That direction
does not itself begin or mutate the next group before this package is
committed.

## 36. `P2-I2-DEC-034` — First correction acceptance and I05F entry

**Status:** accepted by project owner; I05F technically complete but
process-blocked and uncommitted after commit `6dd6898`

**Decision:** The project owner accepts the first I05E correction group,
authorizes and completes its commit, and directs progression to the next group.
The retained commit is `6dd689811949b51ef9a2e9e0d0d14c06bf7346ba`.
Only the I05D group `i04_i05_authority_dependencies` may now begin: 30
findings across the exact 13 files listed in checklist section 10.4D.

I05F must freeze the exact historical source hashes and path-only
transformations before editing an affected file. Accepted I04/I04R1/I04R2
scientific and calibration semantics remain immutable historical authority.
Current changed records must declare portable projection lineage and cannot
impersonate raw preregistrations or validations. Raw I05 execution receipts
retain their original I04 hashes; any current linkage is additive lineage, not
silent substitution.

No calibration builder, arithmetic null, one-shot wrapper, PyGRC model,
candidate/control, conformance, or scientific operation is authorized. I03
and later correction groups, metric freeze, CAL-GATE, I06, and candidate
execution remain closed. Return I05F uncommitted for owner review.

The authorized I05F group is technically complete and remains uncommitted. The
exact thirteen-file group moves from 30 findings to zero and passes 10/10
focused checks. Eight JSON artifacts reconstruct exactly from their `6dd6898`
source bytes, five Python diffs are confined to the frozen portability
surfaces, current external-source digests match, accepted I04R2 bytes remain
addressable at `b7b008c`, and the current I05 output/claim/final bytes are
unchanged from `6dd6898`.

I05F nevertheless fails its frozen process ceiling. The freeze allowed three
static-validation invocations; actual preparation used 13 `.venv` Python
starts: eight JSON syntax checks, one compile check, three validator starts,
and one scanner diagnostic. Two validator starts failed closed without output;
the third alone wrote the passing technical result. All 13 starts were static
and invoked no builder, null, wrapper, PyGRC model, candidate/control,
conformance, or scientific path. The original freeze remains immutable. This
is a process-blocked execution disposition under DEC-034, not owner acceptance
of I05F and not commit authorization; the required process disposition was
subsequently supplied by DEC-035, with package acceptance supplied separately
by DEC-036.

Reopen DEC-034 if the scope differs from the 13 I05D files, a transformation
changes accepted semantics, raw receipt hashes are rewritten, a prohibited
operation occurs, a later group begins before review, or any group finding
remains.

## 37. `P2-I2-DEC-035` — I05F in-place process-deviation closeout

**Status:** complete; process deviation accepted by project owner; full-package
acceptance supplied separately by DEC-036

**Question:** May the I05F validation-count deviation be accepted as a bounded
process-only deviation without rewriting the original freeze or rerunning the
technical validator?

**Decision:** The project owner responded `+1` to the proposed bounded
correction. I05F may retain one additive closeout record that binds:

- the immutable original ceiling of three static-validation invocations;
- the actual 13 `.venv` Python starts: eight JSON syntax checks, one compile
  check, three I05F validator starts, and one scanner diagnostic;
- the two failed-closed validator starts and sole final 10/10 output;
- zero builder, null, wrapper, PyGRC model, candidate/control, conformance, and
  scientific operations; and
- the unchanged historical I04R2 and I05 authority/evidence boundary.

The closeout accepts only the process deviation. It does not reinterpret the
freeze as though the ceiling had been met, authorize a Python or validator
rerun, accept the complete I05F package, authorize commit, open a later
portability group, freeze the metric sheet, pass CAL-GATE, open I06, or
authorize candidate execution.

After the additive record and navigation are internally consistent, I05F may
return to uncommitted owner-review readiness. Full-package acceptance and
commit authorization remain separate owner decisions.

The additive closeout is retained as
`contracts/p2-i2/i05f-static-validation-deviation-closeout.json`, SHA-256
`b1473dbcd4784040f91e026b2ba9d809398bf69d6cbc4b3b533921ea6151f6a7`.
It remains an accurate pre-package-acceptance record; DEC-036 does not rewrite
its then-current package/commit exclusions.

Reopen DEC-035 if the original freeze is edited, the actual invocation ledger
is reduced or reclassified, another validation/runtime operation occurs, the
technical result changes, or the closeout is treated as package acceptance or
commit authority.

## 38. `P2-I2-DEC-036` — I05F package acceptance and commit authority

**Status:** accepted by project owner; commit authorized after completed
DEC-035 closeout

**Question:** Once the bounded I05F deviation closeout is complete, does that
also constitute acceptance of the full I05F package and authorize its commit?

**Decision:** The project owner stated: “when done, it is also acceptance, can
be committed.” Completed DEC-035 closeout therefore authorizes:

- full acceptance of the exact I05F thirteen-file portability correction;
- acceptance of the additive deviation record without claiming the original
  three-invocation ceiling was met;
- retention of the 10/10 technical result and 30-to-zero group finding result;
  and
- one commit containing the complete I05F authority, correction, lineage,
  technical-validation, deviation-closeout, acceptance, report, hypothesis,
  decision, and checklist package.

The earlier deviation record remains an accurate pre-acceptance artifact and
is not rewritten. No Python or technical-validator rerun is authorized or
needed. This decision does not select or open the next portability group,
freeze the metric sheet, pass CAL-GATE, open I06, authorize candidate/control
execution, or assign a scientific result.

The separate acceptance authority is retained as
`contracts/p2-i2/i05f-owner-acceptance-and-commit-authority.json`, SHA-256
`4c5804ebe2c531145be40170c5832a59ecbe347092ee0760e68aa83e77cf7cb4`.

Reopen DEC-036 if the committed package omits an I05F authority/correction/
closeout artifact, changes the retained technical identities, rewrites the
freeze or deviation ledger, includes a later group, or performs a prohibited
operation before commit.

## 39. `P2-I2-DEC-037` — Third bounded portability-group entry

**Status:** owner-directed activity complete; I05G review-ready and
uncommitted pending explicit owner acceptance/commit authority

**Question:** Which bounded portability activity may begin after the accepted
I05F package is retained at `99c64dd`?

**Decision:** The project owner directs: “third group is next.” P2-I2 may open
I05G only. Before editing any affected file, I05G must:

- read the accepted I05D ordered correction-group inventory;
- resolve the exact third group name, affected paths, file/finding counts, and
  source digests;
- retain an immutable input freeze binding parent commit `99c64dd`, allowed
  path-only transformations, historical and consequential identities,
  invocation ceilings, outputs, and the uncommitted review stop; and
- update checklist/hypothesis/decision navigation with the resolved scope.

Until that freeze exists, only the I05G governance scaffold and read-only scope
resolution are authorized. I05G cannot change scientific/runtime semantics,
rewrite historical evidence, invoke a builder/null/wrapper/PyGRC/candidate/
control/conformance/scientific path, begin a fourth correction group, freeze
the metric sheet, pass CAL-GATE, or open I06.

Reopen DEC-037 if the selected group is not the exact next accepted I05D group,
an affected file changes before freeze, the parent commit differs, a
transformation exceeds path representation, a later group begins, or a
prohibited operation occurs.

**Resolved scope:** The accepted I05D policy order identifies the third group
as `i03_realization_and_conformance`, with 201 findings across exactly 30
files. The read-only resolution also distinguishes slash-leading I03F JSON
pointers from filesystem paths; they must become structured segment arrays
with identical target resolution. No affected file changed during resolution.

**Completion:** The exact group now passes 10/10 static checks with 201 to zero
findings. The additive lineage binds all 30 source/projection pairs; all 20
JSON and 10 text projections reconstruct exactly; 105 pointer occurrences
retain ordered-segment identity; and all 44 indexed targets resolve
identically. Historical I03 evidence remains addressable at `99c64dd`, and no
scientific/runtime semantics changed.

Two of the three admitted `.venv/bin/python` validator starts were used. The
first failed closed before output because the validator-only projector omitted
one admitted owner-attachment identity; the second passed and alone retained
the result. All other Python starts and every builder/null/wrapper/PyGRC/model/
candidate/control/conformance/scientific operation remain zero. I05G stops
uncommitted for review. DEC-037 does not accept or authorize committing the
package, select the fourth group, freeze the metric sheet, or pass CAL-GATE.

## 40. `P2-I2-DEC-038` — I05G acceptance and fourth-group entry

**Status:** owner-directed I05G progression complete; I05H review-ready and
uncommitted pending explicit owner acceptance/commit authority

**Question:** What may proceed after owner review of the complete I05G
correction package?

**Decision:** The project owner directs: “ok, commit, move to fourth group.”
This accepts the complete I05G package, authorizes and results in commit
`62882ef`, and opens I05H only. Before editing any fourth-group affected file,
I05H must:

- read the accepted I05D ordered correction-group inventory;
- resolve the exact fourth group name, affected paths, file/finding counts,
  violation classes, and source digests;
- retain an immutable input freeze binding parent commit `62882ef`, allowed
  path-only transformations, historical and consequential identities,
  invocation ceilings, outputs, and the uncommitted review stop; and
- update checklist/hypothesis/decision navigation with the resolved scope.

Until that freeze exists, only the I05H governance scaffold and read-only scope
resolution are authorized. I05H cannot change scientific/runtime semantics,
rewrite historical evidence, invoke a builder/null/wrapper/PyGRC/candidate/
control/conformance/scientific path, begin a fifth correction group, freeze the
metric sheet, pass CAL-GATE, or open I06.

**Resolved scope:** The accepted I05D policy order identifies the fourth group
as `i01_i02_source_and_identity`, with 35 findings across exactly 10 files:
24 embedded machine-local absolute tokens and 11 exact POSIX absolute values.
No affected file changed during the eight-command read-only scope resolution
and freeze preparation.

**Completion:** The exact group now passes 10/10 static checks with 35 to zero
findings. The additive lineage binds all ten source/projection pairs, and the
four JSON, three report, and three Python projections reconstruct exactly. The
only active-source differences are three shebang removals and five changes from
a fixed POSIX temporary root to `tempfile`'s system-selected temporary
directory. Historical I01/I02 evidence remains addressable at `62882ef`; all
capability, source-admission, identity-authority, reset-baseline, quarantine,
and gate meanings remain unchanged.

One of the three admitted `.venv/bin/python` validator starts was used and
passed on its first attempt. All other Python starts and every PyGRC import or
model, historical validator/manifest builder, builder/null/wrapper, candidate/
control/conformance/scientific operation remain zero. I05H stops uncommitted
for review. DEC-038 does not accept or authorize committing I05H, select the
fifth group, freeze the metric sheet, or pass CAL-GATE.

Reopen DEC-038 if the selected group is not the exact fourth accepted I05D
group, an affected file changes before freeze, the parent commit differs, a
transformation exceeds path representation, a fifth group begins, or a
prohibited operation occurs.

## 41. `P2-I2-DEC-039` — I05H acceptance and remaining-inventory reconciliation

**Status:** owner-directed I05H progression complete; exact fifth/final I05I
review-ready and uncommitted pending explicit owner acceptance/commit authority

**Question:** What may proceed after owner review of I05H, and should two
remaining groups be combined?

**Decision:** The project owner directs: “accept and commit, then I think we
should check how many files have left, maybe combine the two groups as one.”
This accepts I05H, authorizes and results in commit `1279e17`, and initially
opens a read-only comparison of:

- the accepted I05D correction-group order and remaining group/file/finding
  inventory; and
- the actual current P2-I2 files still carrying an absolute-path finding after
  I05E–I05H.

The comparison resolves one residual accepted group, not two: six files and 14
findings under `p2_i2_governance_navigation_and_shared_projections`. The
current P2-I2 boundary identifies the same six files. The owner's follow-up—
“don't overcomplicate with I05I ... there's no need for just a review”—directs
the comparison to become the entry step of the fifth/final I05I correction.
No group combination is needed or possible.

Before I05I validation begins, owner inspection identifies constructed
machine-specific repository roots in `p2_i2_i05g_validate.py` and
`p2_i2_i05h_validate.py`: two historical graph-root constructors and one RCAE-
root constructor across the two files. The accepted audit did not report them
because it scans persisted literal tokens rather than dynamically assembled
paths. Absolute paths remain forbidden regardless of representation, so these
two sources are admitted to I05I before validation. This corrects the same
final portability boundary; it does not create I05I-A or another group.

Before any non-governance affected file changes, I05I must retain an immutable
freeze binding commit `1279e17`, all six source hashes, permitted
representation-only transformations, the self-governance declaration
boundary, invocation ceilings, outputs, and the uncommitted review stop. The
three governance files necessarily carry this checklist/hypothesis/decision
declaration before freeze, but their historical correction source remains the
accepted commit bytes. The freeze additionally binds the two owner-identified
validator source hashes and the I05F source identified by the expanded
constructor guard, for nine correction sources in total.

I05I cannot expand into older P2-I1/shared AE01 files, change scientific or
governance meaning, import PyGRC, invoke a historical validator or manifest
builder, run any runtime/scientific path, freeze the metric sheet, pass
CAL-GATE, or open I06.

**Completion:** The terminal correction passes 10/10 static checks with 14
literal findings and four constructed absolute surfaces reduced to zero. All
nine source/projection pairs are retained; the three ordinary non-governance
projections reconstruct exactly; all three validator projections contain no
constructed absolute binding; the three self-governance
diffs are bounded to I05H acceptance, DEC-039/CHG-032/I05I declaration and
closeout, and frozen path substitutions. The complete current P2-I2 audit
scope has zero findings. Historical source bytes remain addressable at
`1279e17`, and no hypothesis, decision, gate, calibration, source,
realization, evidence, or navigation meaning changes.

All three admitted `.venv/bin/python` validator starts are used. The
first fails closed at I05I-02 before output because three governance source
digests predate I05H; the exact `1279e17` digests are corrected in the policy,
freeze, and lineage. The second fails closed at I05I-04 before output because
the expanded guard finds a constructed I05F historical shebang; that ninth
source is frozen and corrected, and the third start passes. All other Python starts and every PyGRC import/model, historical
validator/manifest builder, builder/null/wrapper, candidate/control/
conformance/scientific operation remain zero. I05I stops uncommitted for
review. DEC-039 does not accept or authorize committing I05I or pass CAL-GATE.

Reopen DEC-039 if a non-governance subject changes before freeze, the frozen
nine-file boundary expands, source identity differs from `1279e17`, a process
count becomes scientific evidence, or a prohibited operation occurs.

## 42. `P2-I2-DEC-040` — I05I acceptance and I05J metric-closeout authority

**Status:** historical I05J preparation authority; complete package accepted
and CAL-GATE passed later under DEC-041

**Question:** After accepted I05I portability closeout, what remains in 10.4
and 10.4A, and how may it be completed without rerunning the consumed null?

**Decision:** The project owner confirms there are no remaining machine-local
absolute paths, accepts and authorizes commit of I05I at `b5d0acb`, and then
directs: “let's now deal with 10.4 and 10.4A.” I05C/10.4A is already complete:
its pre-claim venv correction was accepted at `9d81f15`, and the later single
governed attempt succeeded. The three unchecked items following that subsection
are deferred 10.4 metric-closeout obligations rather than unresolved I05C work.

I05J may freeze only `analysis_arithmetic_delta` from the retained candidate-
blind I05 output and generate the two artifacts required by DEC-004: one
lane-local metric-calibration record and one frozen projection of the unchanged
base `AE01-L02` metric sheet. The accepted I04R2 estimator takes the maximum of
the arithmetic floor and all ten absolute order-stratified null margins. The
native common freeze interface accepts one margin per unique seed, so a frozen
input projection takes the maximum absolute margin across both registered
orders for each seed. This is estimator-preserving because the global maximum
over the five seed envelopes equals the global maximum over all ten rows.

Before generation, I05J must bind exact input/tool/schema/output identities and
ceilings. It may invoke the existing native `freeze-resolution` entry point once
through `.venv` and then run bounded static reconstruction validation. The base
metric sheet, I04R2, governed output, one-shot receipts, and portability lineage
remain immutable. No null regeneration, PyGRC import/model, candidate/control,
runtime tolerance, mode selection, scientific conclusion, CAL-GATE passage, or
I06 work is authorized by this decision. I05J returns uncommitted for explicit
owner review, which is later supplied under DEC-041.

Reopen DEC-040 if the per-seed envelope does not reconstruct all ten retained
margins, native generation changes a non-resolution metric field, any frozen
identity differs, or a prohibited operation occurs.

## 43. `P2-I2-DEC-041` — I05JA native dependency correction

**Status:** correction and in-iteration closure amendment complete; complete
I05J/I05JA package owner-accepted and commit-authorized; CAL-GATE passed

**Question:** How may I05J continue after its single frozen native start fails
before output because the repository `.venv` lacks `jsonschema`?

**Decision:** Preserve the original I05J input freeze and its one-start ceiling.
Retain a failure record showing that both governed metric outputs remained
absent and no null, PyGRC, candidate/control, runtime, or scientific operation
occurred. I05JA may install exactly `jsonschema==4.26.0`, the dependency already
required by the accepted common tooling contract, into the repository `.venv`.
It may then authorize one retry of the exact frozen native command.

The correction cannot change the calibration projection, base metric sheet,
I04R2 estimator, governed output, native entry point or implementation, schema,
output paths, or result interpretation. Validation must record two total native
starts, one failed-closed pre-output start, one successful generation, and zero
other Python/null/PyGRC/candidate/runtime/scientific operations. I05JA remains
part of the uncommitted I05J review package and supplies no CAL-GATE or I06
authority.

The later read-only closure audit identifies one process-accounting deviation:
the pinned install command had two process starts, not the correction freeze's
declared one. The first was blocked at package-index DNS by the execution
sandbox and changed no environment; the network-enabled second start installed
and verified `jsonschema==4.26.0`. The original correction freeze is not
rewritten. Because I05J remains uncommitted and unaccepted, the project owner
directs an in-iteration amendment rather than a new I05 iteration. One additive
closeout must distinguish this authored process reconstruction from generated
machine receipts; bind both native starts, both validator starts, successful
outputs, generated validation, final report, and non-self package inventory;
and synchronize stale current-status projections. It authorizes no install,
null, native generation, validator, PyGRC, candidate/control, conformance,
runtime, or scientific rerun.

The project owner subsequently accepts the complete amended I05J/I05JA package
and authorizes its commit. That acceptance passes `P2-I2-CAL-GATE` and opens
only unstarted I06 registration construction; it authorizes no candidate,
control, runtime, or scientific operation.

Reopen DEC-041 if either output exists before the retry, dependency identity is
not exactly `jsonschema==4.26.0`, any frozen command/input differs, the retry
fails, or a prohibited operation occurs.

## 44. `P2-I2-DEC-042` — Exact three-mode implementation registration

**Status:** accepted by project owner; checkpoint amendment authorized

**Question:** Which exact implementations, numeric identities, cells, controls,
and restoration boundary should I06 register for the three retained modes?

**Decision:** Retain `state_carried`, `history_carried`, and `hybrid`
as three required, unranked execution modes on one matched physical-opportunity
topology. Public PyGRC owns every adequate native state, packet, scheduling,
feedback-response, and reset-aware restoration transition. State-carried is
native. History-carried and hybrid use the accepted minimal active-history
producer only for source-label-free token state and native `M_H`
materialization; it may not read response state, decide success, or schedule the
later response.

The I03 adapter's hardcoded `1e-12` materialization comparator is prohibited by
fixture quarantine and cannot be registered. The I06-owned revision therefore
makes the independently derived runtime tolerance an explicit configuration and
restoration-identity field without changing the accepted causal dataflow. The
exact package freezes 23 nodes, 16 edges, seven cells, 26 subconfigurations,
five lane controls, complete comparator/diversion receipts, numeric domain,
seeds/resources, pool-economy bounds, and paired composite continuation.

The sole output-producing validation is baseline-only and passes 14/14. Three
fresh plus three loaded models preserve mode-specific composite identity across
save/load/reset; nine mismatch, cross-pair, one-sided, repeated-reset, wrong-
binding, and stale-readout cases refuse. No contribution, history admission,
neutral contact, response, cell, comparator, or scientific window occurs.

A terminal portability scan finds one source-only defect: the validator's own
rejection guard contains literal absolute/legacy-root patterns. Manifest v1.0.1
retains the pre/post validator hashes and replaces only that guard with generic
POSIX/Windows absolute-token and `*_ROOT` placeholder detection. Two no-model
static starts pass the corrected document/hash/refusal checks and the accepted
I05D scanner over all eight I06 package files at zero findings. The consumed
baseline validation is not rerun, and its projected 14/14 result is unchanged.

Owner review then identifies AdapterV2 conformance authority and exact
historical/current validator-manifest provenance as potential blockers. I06A
freezes those two questions plus tolerance-domain, diversion/H_P-admission,
positive mode-isolation, and retry-semantics confirmations. The first no-model
start stops on an authored seven-versus-six cardinality assertion before output
and is retained at checkpoint `7761d3e`. The owner separately authorizes one
corrected replacement, not an infrastructure retry; it passes 14/14.

I06A proves 13 inherited AdapterV1 members exact, normalized materialization AST
equality, nine pure adapter cases, eight decoy admission exclusions, and zero
response authority. It reconstructs the exact five-file execution manifest and
historical validator hash, identifies only `_assert_portable` plus two imports
as changed, and confirms all 24 other validation functions exact. Final
manifest v1.1.1 binds historical producer and current reconstruction roles
separately. All four confirmation groups pass. I06A imports/instantiates no
PyGRC and performs no baseline rerun, candidate/control operation, or scientific
work.

This decision supplies registration-integrity evidence only. It does not assign
R01–R05 or select a mode. The owner accepts the complete I06/I06A package and
authorizes the successful closeout to amend the failed-closed checkpoint at
`7761d3e`. That acceptance passes REG-GATE and opens only checklist/hypothesis-
first I07 candidate-cycle freeze construction. It does not authorize candidate-
cycle execution; candidate and scientific operation counts remain zero.

Reopen DEC-042 if any registered identity drifts, a mode is collapsed or
ranked, the adapter acquires response authority, a fixture value/identity is
reused, a composite component can be restored one-sidedly, or any prohibited
candidate/scientific operation is found.

## 45. `P2-I2-DEC-043` — I07-found exact-registration blocker

**Status:** decided; owner authorizes the bounded I06B correction

**Question:** May I07 choose execution semantics that I06 did not freeze, or
must exact registration reopen before candidate-cycle source is constructed?

The I07 authority audit assigns `P2-I2-C01`, binds sixteen accepted authority
inputs, and projects 78 applicable mode/branch/order combinations across three
seeds for 234 primary entries. It then identifies three blockers:

1. hybrid P-only/reference-P branches require a native P debit after M_H
   materialization and before the neutral contact, but I06 freezes no event
   time or scheduler/packet index for that operation;
2. full reference P requires a derived `q1+q2 = 1.5` debit, while I06 registers
   only the distinct `0.4375` diagnostic debit; and
3. direct-address and controller-assembled bypasses have accepted exclusion
   semantics but no exact call primitives.

PyGRC exposes no public state-only intervention that removes the first gap; the
accepted native mechanism is packet debit. Choosing an interstitial packet
time, full debit, contributor mask, or controller-authored response schedule in
I07 would revise I06 rather than instantiate it.

**Decision:** open one bounded checklist/hypothesis-first `P2-I2-I06B`
registration correction. Freeze only the missing intervention amount/schedule
and bypass primitives, candidate-free revalidate their compatibility with the
accepted I06/I06A package, and return uncommitted for review. Preserve accepted
I06/I06A bytes, all modes, other values, response semantics, comparators,
seeds, controls, and scientific boundaries. Resume I07 only after corrected
REG-GATE acceptance.

The owner explicitly accepts this recommendation with `+1`. This supplies
construction authority only: it does not accept an eventual I06B package, pass
REG-GATE, resume I07, authorize a commit, or authorize candidate execution.

The resulting additive overlay freezes one matched five-slot schedule, exact
diagnostic `0.4375` and full-reference `q1+q2=1.5` native P debits, and exact
public PyGRC call primitives for both already registered bypass exclusions.
The single `.venv` validation start passes 15/15 with zero blockers, reconstructs
all nine accepted I06/I06A inputs and both blocked I07 drafts, and records zero
PyGRC imports/models, packet operations, candidate/control/response/comparator/
scientific operations, or retries. Accepted I06/I06A bytes are unchanged.

This is a review candidate, not self-acceptance. REG-GATE remains reopened and
I07 remains paused until explicit owner acceptance; commit authority is absent.

No PyGRC import/model, contribution/history admission, response, comparator, or
scientific operation occurred in this audit. The drafted I07 policy is marked
non-authoritative and blocked; EXEC-FREEZE and I08 remain closed.

Reopen DEC-043 if I06B needs any fourth primitive, changes accepted scientific
semantics, or static validation cannot show exact compatibility with I06/I06A.

## 46. `P2-I2-DEC-044` — I06B acceptance and I07 resumption

**Status:** decided by explicit owner acceptance

The owner states `sure, i accept` after reviewing the complete I06B result and
confirming that acceptance permits return to I07. This accepts the exact I06B
input freeze, additive overlay, manifest, validator, 15/15 validation, report,
and their zero-execution boundary. Accepted I06/I06A bytes remain unchanged.

REG-GATE is restored. The already-declared I07 iteration resumes from its
retained authority audit and exact `P2-I2-C01`/234-entry projection; it does not
restart or discard the blocked drafts. I07 may correct and complete those drafts
only by binding accepted I06B, then perform candidate-free static validation and
return uncommitted for separate owner review.

This acceptance does not authorize a commit, pass EXEC-FREEZE, accept an I07
cycle, open I08, or authorize any model, packet, candidate, control, response,
comparator, or scientific operation.

Reopen DEC-044 if any accepted I06B byte changes, the acceptance record fails to
bind the exact package, or I07 requires registration semantics beyond I06B.

## 47. `P2-I2-DEC-045` — Missing test dependency remains an I07 correction

**Status:** decided by explicit owner direction

The first I07 construction start completed, while the second `.venv` start
failed before test collection solely because `pytest` was absent. The owner
states: `installing pytest doesnt need I07A, just install it and udate I07 after
it is installed`.

**Decision:** do not open I07A. Preserve the CHG-039 failed-start receipt and
continue inside I07 under CHG-040. Install `pytest` only into the repository
`.venv`; record the exact resolved dependency; update the validator's process
accounting honestly; candidate-free refresh only the derived binding/freeze
hashes; then allow one replacement focused-test start and one final validator
start. Any additional failure stops for owner direction.

The continuation completes as authorized: `pytest 9.1.1` is installed only in
`.venv`, the derived refresh preserves policy/source/tests/matrix identities,
the unchanged focused suite passes 7/7, and final candidate-free validation
passes 25/25 with zero blockers. Six starts are retained honestly and no PyGRC,
model, packet, candidate/control, response, comparator, or scientific operation
occurs.

The accepted upstream authorities, execution policy and causal semantics,
234-entry matrix, focused tests, candidate prohibition, and scientific-evidence
boundary remain unchanged. This decision does not authorize a commit, pass
EXEC-FREEZE, open I08, or execute a candidate/control operation.

## 48. `P2-I2-DEC-046` — Cross-entry-isolation blockers belong to I07A

**Status:** decided by explicit owner direction

After the CHG-041 audit identifies four substantive execution-safety gaps, the
owner states: `These can actually be I07A`.

**Decision:** open `P2-I2-I07A` for only the four audited corrections: safe
beneath-root no-symlink artifact creation; project/PyGRC bytecode-cache
isolation; current-entry-only mechanical retry reconstruction without a shared
ledger; and exact-path fail-closed 234-entry completion. Preserve the reviewed
I07 identities in an additive input freeze before changing consequential bytes.

I07A may refresh the effective policy, runner, focused tests, validator,
matrix, binding, inactive freeze, and related reports only as required by those
mechanics. Accepted I04R2/I05J/I06–I06B semantics, three-mode retention,
registered values, retry ceiling, candidate prohibition, and scientific
boundaries remain immutable. Use at most three candidate-free
`.venv/bin/python -B` starts. Return uncommitted for review.

This direction does not accept the eventual I07A package, pass EXEC-FREEZE,
authorize a commit, open I08, or authorize model, packet, candidate/control,
response, comparator, or scientific execution.

The authorized candidate completes with all 234 entry objects unchanged, 15/15
focused tests, and 17/17 final candidate-free checks. Exactly three `-B` starts
pass with zero retries and no PyGRC/model/packet/candidate/scientific activity.
All four audited blockers are mechanically closed. This result remains
uncommitted and awaits explicit owner acceptance; the gate boundary above is
unchanged.

Reopen DEC-046 if a fifth semantic or execution correction is required, any
accepted upstream authority must change, or a candidate-free start fails.

## 49. `P2-I2-DEC-047` — I07A acceptance, inactive EXEC-FREEZE passage, and commit

**Status:** decided by explicit owner acceptance and commit direction

After receiving the complete I07A result—15/15 focused tests, 17/17 final
candidate-free checks, zero blockers, all 234 entry objects unchanged, and zero
PyGRC/model/packet/candidate/scientific activity—the owner states: `ok, time to
commit`.

**Decision:** accept the exact I07A package, pass `P2-I2-EXEC-FREEZE` for its
inactive cycle only, and authorize committing the complete accumulated
I06B/I07/I07A checkpoint on `p2-i2-experiment`. The machine acceptance record
binds the exact technical artifacts and their hashes.

This acceptance does not create or authorize the live activation record, open
I08, execute a matrix entry, remove ignored import caches, build the execution
manifest, or assign scientific evidence. Each remains subject to a separate
owner direction after the accepted commit.

Reopen DEC-047 if a committed technical hash differs from the acceptance
record, an activation/candidate artifact enters this commit, or EXEC-FREEZE is
treated as live execution authority.

## 50. `P2-I2-DEC-048` — Open I08 activation-package construction

**Status:** decided by separate owner direction

After commit `5c2c248` retains the accepted inactive I06B/I07/I07A authority,
the owner states: `ok, let's do I08`.

**Decision:** open I08 only far enough to freeze and validate its exact
activation candidate. This includes the previously withheld cleanup of ignored
`__pycache__`, `.pyc`, and `.pyo` artifacts beneath the two frozen live import
roots, with before/after accounting. The activation candidate must remain
inactive and uncommitted while under review. No matrix claim, PyGRC import,
model, packet, candidate/control response, or scientific window is authorized.

Explicit review must precede setting `owner_acceptance`,
`candidate_execution_authorized`, and `I08_authorized` true. The resulting live
activation must then be committed before any normalized entry command may bind
that commit's full HEAD. No commit is authorized by this decision.

The bounded preparation completes as declared: 207 ignored cache artifacts are
retained in the before inventory and zero remain; no tracked graph or RCAE byte
changes; and preactivation validation passes 18/18 with two candidate-free
`.venv/bin/python -B` starts, zero retries, and zero PyGRC/model/packet/
candidate/scientific activity. The activation candidate remains inactive and
uncommitted for owner review.

Reopen DEC-048 if preparation changes an accepted I07A technical byte, touches
a tracked graph byte, creates a governed claim/output/failure/manifest, leaves
an import cache in either live root, or requires a scientific change.

## 51. `P2-I2-DEC-049` — Accept and commit the exact I08 activation

**Status:** decided by explicit owner acceptance and commit direction

After the inactive I08 activation package passes 18/18 checks with zero
blockers and returns uncommitted, the owner states: `+1 and make a commit`.

**Decision:** accept candidate SHA-256
`52d420b49029e32f007119a3f888ca9fc05ca545a4a75b3e775f8c69c23eac6b`,
apply only its prereviewed activation transition, and authorize committing the
complete I08 activation package. The accepted activation SHA-256 is
`f46ebd323499423715107c3b337963c3787404ed257c56be880808617cb09cc3`.
It binds the preparation artifacts and unchanged live-validator hashes while
retaining `activation_commit_head=null` and the normalized-command full-HEAD
source, avoiding self-reference.

This decision opens live I08 only after the activation is committed and the
exact resulting full HEAD passes the frozen repository, graph, interpreter,
cache, command, and current-entry preflight. It does not authorize a claim or
matrix entry inside the activation commit itself. No additional activation
review is required if those exact preconditions pass.

Reopen DEC-049 if the commit changes an accepted live technical hash, includes
a governed claim/output/failure/manifest, or the first normalized preflight
does not reproduce the accepted authority and clean-runtime boundary.

## 52. Pending decision queue

No item below is decided by this record yet:

| Proposed decision | Earliest iteration | Prerequisite |
| --- | --- | --- |
| Terminal classification and next move | I11 | Resolved controls and reconstruction |

Pending items may not be answered by convenience, code availability, or
candidate outcomes outside their named iteration.
