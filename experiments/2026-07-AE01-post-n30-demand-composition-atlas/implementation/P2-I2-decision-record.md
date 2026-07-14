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
- `P2-I2-I01` is the first capability-audit iteration and remains pending until
  its input scope is frozen in the checklist and this record.
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

## 7. Pending decision queue

No item below is decided by this record yet:

| Proposed decision | Earliest iteration | Prerequisite |
| --- | --- | --- |
| I01 audit scope and exact source-current identity | I01 | I00R1 closure |
| Source admission and restoration-provider transition | I02 | I01 retained audit |
| Realization class and native/producer boundary | I03 | I01–I02 dispositions |
| Dependence mode and causal interfaces | I03 | Selected realization |
| Primary raw response and orientation | I04 | Discriminator gate |
| Closest primary comparator | I04 | Realization-bound insufficient-repetition alternatives |
| Candidate-blind matched null and analysis identity | I04 | Frozen response/comparator |
| Exact implementation and registration bundle | I06 | Frozen calibration |
| Candidate cycle authorization | I07 | Passed registration |
| Terminal classification and next move | I11 | Resolved controls and reconstruction |

Pending items may not be answered by convenience, code availability, or
candidate outcomes outside their named iteration.
