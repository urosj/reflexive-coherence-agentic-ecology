# P2-I1 Minimal Shared-Medium Niche Formation Checklist

**Status:** active provisional lane checklist; registration completed, no
candidate execution completed

**Iteration:** `P2-I1`

**Lane:** `AE01-L01`

**Current probe cycle:** `P2-I1-C01` — execution-freeze preparation

**Current local gate:** `P2-I1-EXEC-FREEZE`

**Acceptance ceiling:** `AE01-C2`; no lane result assigned

**Theory and observation directive:**
[P2-I1 brief](P2-I1-minimal-shared-medium-niche-brief.md)

**Cumulative lane decision record:**
[P2-I1 cumulative decision record](P2-I1-decision-record.md)

**Frozen authorities:**
[L01 hypothesis](../hypotheses/lane-hypotheses.md),
[outcome and stopping contract](../hypotheses/outcome-and-stopping-contract.md),
[developmental interpretation contract](../hypotheses/developmental-interpretation-contract.md),
[L01 metric sheet](../contracts/metric-sheets/AE01-L01.json),
[execution policy](../configs/p1_i5_execution_policy.json), and
[P1-I5 tooling contract](P1-I5-tooling-contract.md)

**Program cover:** [Post-N30 master checklist](../../../implementation/PostN30-checklist.md)

## 1. How to use this checklist

This file is the detailed execution and learning surface for P2-I1. The master
checklist records only stable cover gates. This checklist projects the common
lane completion contract into L01-specific work and may expand as retained
evidence exposes new needs.

The operating rule is:

> The checklist is living between probe cycles and frozen within a probe cycle.

Before a cycle runs, its implementation, inputs, controls, attempts, resources,
artifacts, claim boundary, and stopping rule are frozen. After a valid result,
the checklist may add work that improves discrimination, exposes a missing
condition, redirects the question, or closes the lane. It must not add variants
merely to obtain a positive result.

Checkbox convention:

```text
[ ] pending, unresolved, or not yet demonstrated
[x] completed with cited evidence or explicitly dispositioned
```

Rules:

- A checked evidential item cites a retained artifact, reconstruction, report,
  or accepted review record.
- Infrastructure success never checks a scientific result item.
- Negative, narrow, mixed, counter-directional, blocked, and incomplete results
  may legitimately add, redirect, or close work.
- Every evidence-triggered addition receives a change ID and preserves the
  result that triggered it.
- Scientific changes require a new preregistration and a new probe cycle.
- Each registered cell's one infrastructure retry cannot be used for
  scientific refinement.
- A conflict with a frozen Phase 1 authority reopens the affected contract; it
  cannot be resolved inside this checklist.
- Review is gate-bounded, not recursive. Review a semantic or architectural
  decision once; close its deterministic retention and reconstruction work by
  machine verification. Require another review only when later work introduces
  a new decision or unresolved assumption, expands the accepted scope, or
  fails a required comparison.

## 2. Local gate dashboard

| Gate | Meaning | Status | Exit evidence |
| --- | --- | --- | --- |
| `P2-I1-THEORY-GATE` | L01 meaning, distinctions, open questions, and decision timing accepted | Passed | Accepted brief and owner review disposition dated 2026-07-10 |
| `P2-I1-CAL-PRE-GATE` | Measurement, opportunity, null, calibration realization, selectivity policy, and analysis identity frozen before margins exist | Passed | v2 identity refresh passed; v1 remains retained history |
| `P2-I1-CAL-GATE` | Candidate-blind resolution band frozen from reconstructable matched-null provenance | Passed | D-020 regeneration is byte-identical to retained calibration |
| `P2-I1-REG-GATE` | Exact probe and registration evidence bundle accepted | Passed | Retained bundle and owner-accepted REG-GATE review dated 2026-07-11 |
| `P2-I1-EXEC-FREEZE` | One exact registered candidate cycle authorized before its first operation | Pending | Cycle-scoped freeze with candidate outcomes absent |
| `P2-I1-EXEC-GATE` | Frozen comparison matrix completed or validly bounded as blocked/incomplete | Pending | Cell artifacts, receipts, control outcomes, reconstruction |
| `P2-I1-CLOSE-GATE` | Developmental interpretation and terminal classification complete | Pending | Terminal record, report, retained manifest, R3 handoff |

`P2-I1-GATE` in the master checklist is equivalent to
`P2-I1-CLOSE-GATE` here.

The two calibration gates passed at v1. `P2-I1-DEC-020` briefly reopened only
their runtime-policy/measurement identity chain so the circular execution
boundary could be corrected in machine policy. The bounded v2 refresh passed:
the committed v1 records remain valid history, the calibration realization is
unchanged, and all calibration artifacts are byte-identical.

## 3. Stable entry and claim boundaries

- [x] `P1-GATE` passed. Evidence: [R2 closeout](../reports/R2-closeout.md).
- [x] Stable lane ID is `AE01-L01`.
- [x] Frozen hypothesis is `AE01-H-L01`.
- [x] Frozen maximum claim is `bounded niche-conditioning demand pattern`.
- [x] `AE01-C2` is the program acceptance ceiling; it is not boundary rung
  `AE01-L01-R02`.
- [x] Positive ecology, coordination, agency, organism, motif, regime, life,
  or N31+ claims remain blocked.
- [x] Graph/PyGRC repository remains read-only from RCAE.
- [x] No calibration, lane registration, candidate cell, or terminal result is
  inferred from Phase 1 fixtures or validation.
- [x] P2-I1 may not consume another lane's conclusion as evidence.

## 4. Theory gate

### 4.1 Brief and concept distinctions

- [x] Draft P2-I1 theory/geometry/ecology/observation brief exists.
- [x] Project-owner review accepts the brief or records required revisions.
- [x] `niche medium state`, `niche-conditioning relation`, and `niche
  formation` remain distinct.
- [x] Historically produced conditioning is distinguished from occupancy or
  pre-existing environmental suitability.
- [x] `local differentiation` has a bounded operational meaning without agent
  or organism promotion.
- [x] Niche is not reducible to spatial location, passive surroundings,
  resource count, role, label, or correlation alone.
- [x] Selectivity is required beyond uniform environmental improvement or
  degradation.
- [x] Co-constitution requires separable causal roles under intervention.
- [x] Sharedness requires a surface outside private state that is accessible in
  principle to a later local differentiation.
- [x] Niche formation names the search direction while the claim ceiling
  remains niche conditioning.
- [x] Ecology-side observed relation and LGRC demand implication remain
  separate.

### 4.2 Minimum, strong, and maximum interpretation

- [x] Minimum observation is bounded to rungs `AE01-L01-R01`–`R02`.
- [x] Strong bounded result requires rungs through `AE01-L01-R04` plus the
  applicable causal controls.
- [x] Maximum L01 result requires `AE01-L01-R05` without implying native
  support, general niche theory, coordination, agency, motif, or regime.
- [x] Metric relation, boundary rung, support status, classification value, and
  terminal state remain orthogonal.
- [x] One event cannot satisfy a distributional niche-conditioning claim.

### 4.3 Anti-subsumption and reuse

- [x] L01 does not subsume L02 source-plurality or contribution-structure
  effects.
- [x] L01 does not subsume L03 route/trace function.
- [x] L01 does not subsume L04 provisioning/support admissibility.
- [x] L01 does not subsume L05 selective boundary exchange.
- [x] L01 does not subsume L06 audited capacity circulation.
- [x] L01 does not manufacture the missing L07 parent/local distinction.
- [x] A more specific lane owns the stronger interpretation when its causal
  discriminator explains the result.
- [x] Reusable method structure is distinguished from non-reusable L01 evidence,
  deltas, bounds, and conclusions.

Exit gate `P2-I1-THEORY-GATE`:

- [x] Brief accepted with all requested revisions dispositioned.
- [x] Open research questions remain explicitly open at their legitimate
  decision points rather than answered in advance.
- [x] No frozen P1 contract was changed by interpretation.

Theory-gate owner review — 2026-07-10:

> The brief and checklist define a bounded search for historically produced,
> participant-relative niche conditioning through a non-private shared medium.
> They preserve selectivity, causal lineage, sharedness, distributional
> evidence, anti-subsumption, and claim-boundary discipline while leaving
> realization and scientific outcome open.

Disposition: `P2-I1-THEORY-GATE=passed`. The review selects no participant,
medium, response family, selectivity discriminator, realization mechanism, or
terminal class. Generic environmental conditioning, occupancy/suitability,
self-aftereffect, producer-carried appearance, missing selectivity, lane
redirection, missing substrate surface, and no reusable/generative value remain
valid outcomes.

## 5. Open-question and decision-timing ledger

| Question ID | Question | Decision point | Current status | Evidence or disposition |
| --- | --- | --- | --- | --- |
| `L01-Q00` | Which realization family will produce fresh P2-I1 evidence? | Calibration preregistration | Decided | `P2-I1-DEC-001`: Option A feedback-conditioned packet opportunity |
| `L01-Q01` | What calibration participant carrier and continuity criterion will be used? | Calibration preregistration | Decided | `P2-I1-DEC-002`: route-aspect source pole with structural/lineage continuity and budget-derived one-repeat reserve |
| `L01-Q02` | What calibration medium carrier and access scope will be used? | Calibration preregistration | Decided | `P2-I1-DEC-003`: narrow ordered pulse-contact→feedback lineage with shared-local counterfactual access |
| `L01-Q03` | Which one response family is primary? | Calibration preregistration | Decided | `P2-I1-DEC-004`: formation of a later native packet-arrival opportunity |
| `L01-Q15` | What opportunity-level raw formation formula, units, and aggregation are primary? | Calibration preregistration | Decided | `P2-I1-DEC-005`: binary opportunity formation aggregated as a per-seed formation fraction; operational missingness invalidates rather than shrinks the seed denominator |
| `L01-Q16` | How many later opportunities occur per seed, and are they independent, sequential, or cumulative? | Calibration preregistration | Decided | `P2-I1-DEC-006`: four distinct-profile independent counterfactual branches restored from one cell/seed branch point |
| `L01-Q04` | What orientation transform makes positive margin aligned? | Calibration preregistration | Decided | `P2-I1-DEC-008`: identity orientation; higher formation fraction is aligned, with raw paired coverage retained beside the normalized margin |
| `L01-Q05` | What participant/compatibility discriminator tests selectivity? | Calibration preregistration and registration import | Decided | `P2-I1-DEC-007`: two matched context pairs compare history-aligned with polarity-inverted configured susceptibility |
| `L01-Q17` | Which exact reader, route, timing, and opportunity-profile identities instantiate the two polarity pairs? | Calibration preregistration | Decided | `P2-I1-DEC-010`: fixed node/edge/port, route-aspect, lineage, and four static/resolved profile identities; hashes remain generated outputs |
| `L01-Q18` | What initial coherence, packet amounts, delays, feedback reference/threshold, and resulting viability values instantiate that topology? | Calibration preregistration | Decided | `P2-I1-DEC-011`: dyadic base state, analytically derived mechanism threshold, and proximity-aware reading of the specific result |
| `L01-Q19` | How do deterministic seeds vary the base fixture, and what recurrence claim may they support? | Calibration preregistration | Decided | `P2-I1-DEC-012`: balanced `P/W` offsets `{-1/32, 0, +1/32}`; local numeric robustness only |
| `L01-Q06` | How are matched-null margins generated reproducibly? | Calibration preregistration | Decided | `P2-I1-DEC-013`: analysis-only identical synthetic panel pairs span formation fractions `0`, `.25`, `.5`, `.75`, and `1`; expected margins are zero |
| `L01-Q07` | What baseline and later-response windows define a margin? | Calibration preregistration | Decided | `P2-I1-DEC-009`: bounded W0–W4 native causal-event sequence, completed numerically by `P2-I1-DEC-011` |
| `L01-Q20` | What portable analysis/generator boundary and digest surfaces freeze aggregation, rung classification, and terminal inputs? | Calibration preregistration | Decided | `P2-I1-DEC-014`: thin CLI, pure no-PyGRC analysis module, and one policy with three canonical projections; generated hashes remain implementation work |
| `L01-Q08` | Are participant and medium separated or co-constituted? | Controls and interpretation | Decided | `P2-I1-DEC-015`: operationally separated carriers with participant-mediated reading; state-matched feedback-row absence controls private-state sufficiency |
| `L01-Q09` | Does medium history cause the later response? | Execution and controls | Decided | `P2-I1-DEC-016`: neutral-content reference, row-absent control, departure/arrival source-digest mismatch, and strict native ordering distinguish content, presence, lineage, and order |
| `L01-Q10` | What support carries any appearance? | Withdrawal and interpretation | Decided | `P2-I1-DEC-017`: `parent-context-contrast` is a score-preserving reduced-support active null; no actual parent basin or parent claim |
| `L01-Q11` | Does the observed geometry justify niche-conditioning language? | Terminal interpretation | Open | — |
| `L01-Q12` | Is another lane the better causal home? | Terminal interpretation or R3 | Open | — |
| `L01-Q13` | Is the result reusable or generative beyond the fixture? | Classification-value reading and R3 | Open | — |
| `L01-Q14` | Are first-class registration or control-outcome records necessary? | R3 | Open | — |
| `L01-Q21` | Which one carrier or timescale axis does `carrier-timescale-contrast` vary, and what can it establish? | Calibration preregistration | Decided | `P2-I1-DEC-018`: double reader-packet amount from `.125` to `.25`; bounded carrier-load invariance only |
| `L01-Q22` | Which comparator owns the primary normalized margin, and which comparisons remain causal controls? | Calibration preregistration | Decided | `P2-I1-DEC-019`: candidate versus neutral-content reference is primary; candidate versus row absence controls medium dependency and selectivity |

An open question blocks only the gate named by its decision point. It is not a
defect merely because the answer is unknown earlier.

## 6. Calibration preregistration gate

This gate prevents calibration from defining its response, orientation, or
opportunity structure after margins are known. Its fields are measurement
identity, not positive lane evidence.

Entry condition:

- [x] `P2-I1-THEORY-GATE` passed.

### 6.1 Response and realization identity

- [x] Select the live realization family and separate native PyGRC,
  RCAE-producer, and inherited-artifact ownership. Evidence:
  [`P2-I1-DEC-001`](P2-I1-decision-record.md).
- [x] Select the participant carrier and non-circular structural continuity
  fields. Evidence: [`P2-I1-DEC-002`](P2-I1-decision-record.md).
- [x] Freeze the participant viability floor as a budget-derived one-repeat
  reserve evaluated at every model-owned event boundary with native
  `epsilon_budget=1e-9`. Evidence:
  [`P2-I1-DEC-002`](P2-I1-decision-record.md).
- [x] Select exactly one primary response family from `formation`,
  `persistence`, `re-entry`, `cost`, or `susceptibility`. Evidence:
  [`P2-I1-DEC-004`](P2-I1-decision-record.md).
- [x] Freeze the raw response formula, units, valid domain, and missing-value
  semantics. Evidence: [`P2-I1-DEC-005`](P2-I1-decision-record.md).
- [x] Freeze higher-is-aligned orientation and identity transformation from raw
  to oriented response. Evidence:
  [`P2-I1-DEC-008`](P2-I1-decision-record.md).
- [x] Freeze the calibration participant carrier and continuity criterion.
  Evidence: [`P2-I1-DEC-002`](P2-I1-decision-record.md).
- [x] Freeze the medium carrier and shared-access scope. Evidence:
  [`P2-I1-DEC-003`](P2-I1-decision-record.md).
- [x] Freeze the RCAE-owned four-node logical fixture topology, participant
  route aspect, shared-medium masks, and two symmetric reader-route roles.
  Evidence: [`P2-I1-DEC-010`](P2-I1-decision-record.md).
- [x] Freeze the dyadic numeric base state, packet amounts, native delay policy,
  feedback reference/threshold, and budget projections. Evidence:
  [`P2-I1-DEC-011`](P2-I1-decision-record.md).
- [x] Materialize the exact declarative fixture and calibration-realization
  identity projection. Evidence:
  [`p2_i1_fixture.json`](../configs/p2_i1_fixture.json),
  [`p2_i1_calibration_policy.json`](../configs/p2_i1_calibration_policy.json),
  and the clean-commit identity builder in
  [`p2_i1.py`](../scripts/p2_i1.py).
- [x] Retain the final fixture and calibration-realization digests from the
  clean follow-up implementation commit. Evidence:
  [CAL-PRE identity](../contracts/p2-i1/cal-pre-identity.json) and
  [freeze record](../contracts/p2-i1/cal-pre-freeze.json), anchored to
  `134b66cf6adf50e9f1e773454be25bbea53938d2`.
- [x] Freeze baseline, writer, medium-materialization, later-opportunity, and
  response windows as bounded native causal-event stages. Evidence:
  [`P2-I1-DEC-009`](P2-I1-decision-record.md). Numeric event-time policy is
  completed by [`P2-I1-DEC-011`](P2-I1-decision-record.md); concrete event IDs
  remain generated outputs.
- [x] Freeze primary-response aggregation, scientific versus operational
  denominator semantics, and the normalized candidate/comparator denominator,
  including zero and unavailable behavior. Evidence:
  [`P2-I1-DEC-005`](P2-I1-decision-record.md) and
  [`P2-I1-DEC-008`](P2-I1-decision-record.md).
- [x] Identify secondary responses in advance and prohibit them from replacing
  the primary response inside the cycle. Evidence:
  [`P2-I1-DEC-005`](P2-I1-decision-record.md).
- [x] Adopt selectivity Policy A: calibrated `delta` applies only to the primary
  candidate-versus-comparator margin; selectivity is a separate causal/control
  gate and does not consume `delta`. Evidence:
  [`P2-I1-DEC-007`](P2-I1-decision-record.md).
- [x] Freeze `selectivity_metric_uses_calibrated_delta=false`, the independent
  `selectivity_threshold_source`, and
  `selectivity_threshold_candidate_blind=true` before calibration. Evidence:
  [`P2-I1-DEC-007`](P2-I1-decision-record.md).
- [x] Preserve threshold proximity and developmental interpretation for the
  specific P2-I1 result rather than treating one crossing as the conclusion.
  Evidence:
  [`P2-I1-DEC-011`](P2-I1-decision-record.md).

### 6.2 Unit of analysis and opportunity structure

Every opportunity-level record must contain:

```text
opportunity_id
seed
cell_id
relation_chain_id
writer_carrier_id
writer_event_id
medium_surface_id
medium_change_event_id
medium_history_digest
later_opportunity_event_id
reader_or_local_differentiation_id
raw_response
oriented_response
admissibility: admissible | inadmissible | not_evaluable
opportunity_status: observed | inadmissible | structurally_unavailable |
  censored_runtime | missing_infrastructure | blocked_by_control
```

Every feedback-threshold evaluation additionally retains observed value,
configured threshold, signed distance, native reason, and whether the native
transition occurred.

- [x] Freeze live-seed variation as the three balanced `P/W` coherence offsets
  in [`P2-I1-DEC-012`](P2-I1-decision-record.md), with no broad recurrence
  claim.

- [x] Freeze exactly four later opportunities per seed. Evidence:
  [`P2-I1-DEC-006`](P2-I1-decision-record.md).
- [x] Freeze the opportunities as independent counterfactual branches restored
  from one registered cell/seed branch point. Evidence:
  [`P2-I1-DEC-006`](P2-I1-decision-record.md).
- [x] Freeze aggregation from opportunity records to the seed-level formation
  fraction and specialize the primary normalized margin as
  `candidate-conditioning` versus `reference`. Preserve
  `candidate-conditioning` versus `medium-freeze-withdrawal` as the separate
  medium-dependency and selectivity comparison. Evidence:
  [`P2-I1-DEC-005`](P2-I1-decision-record.md),
  [`P2-I1-DEC-019`](P2-I1-decision-record.md).
- [x] Freeze treatment of missing, censored, and structurally unavailable
  opportunities without silently removing them from the denominator.
  Evidence: [`P2-I1-DEC-005`](P2-I1-decision-record.md).
- [x] Freeze the consistency mapping between `admissibility` and
  `opportunity_status`, and how every status enters the scientific denominator
  and seed aggregate. Terminal interpretation remains a later gate. Evidence:
  [`P2-I1-DEC-005`](P2-I1-decision-record.md).
- [x] Require `structurally_unavailable` to remain potentially scientific while
  `censored_runtime` and `missing_infrastructure` remain operational and cannot
  support or refute the lane. Evidence: status validation and fixed-denominator
  aggregation in [`p2_i1_analysis.py`](../scripts/p2_i1_analysis.py).
- [x] Require opportunity counts and admissibility distributions in retained
  outputs so a seed aggregate cannot conceal one-event success or unequal
  exposure. Evidence: `planned_count`, `formed_count`, `status_counts`, and
  ordered opportunity/profile IDs emitted by
  [`p2_i1_analysis.py`](../scripts/p2_i1_analysis.py).
- [x] Require every relation chain to record `causal_order_verified` and exact
  `medium_dependency_control_refs`, joining writer, medium perturbation,
  persisted/decayed history, later opportunity, and response in machine data
  rather than authored interpretation. Evidence: closed opportunity-record
  validation in [`p2_i1_analysis.py`](../scripts/p2_i1_analysis.py). Actual
  runtime records remain an execution obligation.
- [x] Freeze `writer_reader_relation` as `distinct_carrier` with
  `participant_mediated_configured_producer` read mode. Evidence:
  [`P2-I1-DEC-010`](P2-I1-decision-record.md).
- [x] Freeze the four static opportunity-profile identities, canonical
  node/edge/port mapping, portable lineage pattern, and static-versus-resolved
  digest rule. Evidence: [`P2-I1-DEC-010`](P2-I1-decision-record.md).
- [x] Materialize four static profile digests with exactly two reader identities
  and freeze per-run resolved-digest construction, exact cross-cell static
  matching, branch-point restoration equality, and no cross-branch state
  carryover. Evidence: identity functions and negative tests in
  [`p2_i1_analysis.py`](../scripts/p2_i1_analysis.py) and
  [`test_p2_i1.py`](tests/test_p2_i1.py).
- Actual resolved digest values are produced only by registered live branches
  and are tracked under registration/execution, not CAL-PRE.
- [x] Freeze whether the selected relation permits a sharedness claim, whether
  a self-aftereffect control is mandatory, and the maximum claim available.
  Evidence: [`P2-I1-DEC-010`](P2-I1-decision-record.md): shared-local
  counterfactual access is the ceiling, and participant-mediated reading
  requires the self-aftereffect control.

### 6.3 Frozen analysis identity

- [x] Freeze the thin-CLI, pure-analysis-module, and one-policy responsibility
  boundary plus portable paths. Evidence:
  [`P2-I1-DEC-014`](P2-I1-decision-record.md).
- [x] Freeze portable `analysis_script_path` and `analysis_script_sha256`.
  Evidence: [CAL-PRE identity](../contracts/p2-i1/cal-pre-identity.json).
- [x] Freeze `aggregation_policy_digest`, `rung_classifier_digest`, and
  `terminal_classifier_digest` before calibration or candidate outcomes.
  Evidence: [CAL-PRE identity](../contracts/p2-i1/cal-pre-identity.json).
- [x] Verify the analysis identity converts opportunity records into seed
  aggregates, frozen-role margins, selectivity results, rung inputs, and
  terminal inputs without authored recomputation. Evidence: analysis and
  caller-override tests in [`test_p2_i1.py`](tests/test_p2_i1.py).
- [x] Require a new CAL-PRE/CAL cycle if analysis code or scientific policy
  identity changes after calibration. Evidence:
  [`P2-I1-DEC-014`](P2-I1-decision-record.md).

### 6.4 Matched-null preregistration

- [x] Declare the matched-null generator, exact null configuration, and why it
  measures resolution rather than acting as a weakened candidate. Evidence:
  [`P2-I1-DEC-013`](P2-I1-decision-record.md).
- [x] Freeze portable calibration command, environment, dependency, resource,
  source/input identity, and expected-artifact policies. Evidence:
  [`p2_i1_cal_pre_provenance.json`](../configs/p2_i1_cal_pre_provenance.json).
- [x] Materialize the final clean source revision, source hashes, configuration
  and projection digests, and reconstruction identity after the follow-up
  implementation commit. Evidence:
  [CAL-PRE identity](../contracts/p2-i1/cal-pre-identity.json) and
  [freeze record](../contracts/p2-i1/cal-pre-freeze.json).
- [x] Freeze calibration seeds `19`, `43`, `71`, `109`, and `163`. Evidence:
  [`P2-I1-DEC-013`](P2-I1-decision-record.md).
- [x] Verify calibration seeds are disjoint from candidate seeds `101`, `211`,
  and `307`. Evidence: [`P2-I1-DEC-013`](P2-I1-decision-record.md).
- [x] Declare that no candidate-derived input, candidate outcome, PyGRC
  runtime input, or post-outcome tuning enters the null generator or
  preregistration. Evidence:
  [`P2-I1-DEC-013`](P2-I1-decision-record.md).

Exit gate `P2-I1-CAL-PRE-GATE`:

- [x] Response, orientation, unit, opportunity, normalization, window, null,
  calibration-realization, selectivity-policy, and analysis identities are
  complete and internally consistent. Evidence: retained CAL-PRE records,
  passing config validation, and the P2-I1 test suite.
- [x] Candidate outcomes were absent at freeze. Evidence: candidate-absence
  projection in [CAL-PRE freeze](../contracts/p2-i1/cal-pre-freeze.json).
- [x] Independent review accepts the calibration preregistration. Evidence:
  [P2-I1 CAL-PRE review](../reports/P2-I1-CAL-PRE-review.md).
- [x] Freeze the requirement that these fields import unchanged into lane
  registration; any change restarts calibration in a new probe cycle.
  Evidence: retained measurement and calibration-realization identities.

CAL-PRE implementation progress — 2026-07-11:

- [x] Materialize the decision-derived fixture, seven cells, W0-W4 windows,
  seed transforms, four profiles, calibration panels, analysis projections,
  and runtime boundary as portable configuration surfaces. Evidence:
  [P2-I1 configs](../configs/README.md#p2-i1-configuration-surfaces).
- [x] Implement one pure opportunity-analysis path for scientific versus
  operational missingness, fixed-denominator seed aggregation, raw paired
  coverage, normalized margins, selectivity interactions, and
  serialization-ready rung/terminal inputs. Evidence:
  [`p2_i1_analysis.py`](../scripts/p2_i1_analysis.py).
- [x] Implement deterministic static opportunity-profile and reader-identity
  digests, with four distinct profile identities and exactly two reader
  configurations. Evidence: [`p2_i1.py`](../scripts/p2_i1.py) config
  validation and identity builder.
- [x] Implement a thin CLI for config validation, CAL-PRE identity generation,
  matched-null generation, and later raw-record analysis.
  Evidence: [P2-I1 commands](../scripts/README.md#p2-i1-entry-point).
- [x] Implement a fail-closed PyGRC preflight boundary with a schema-validated
  local realization profile, runtime-binding receipt, graph-tree read-only
  guard, no recorded local path, and no fallback. Evidence:
  [`p2_i1_runtime.py`](../scripts/p2_i1_runtime.py).
- [x] Keep candidate execution mechanically unauthorized in the shared runtime
  policy and runtime scaffold.
  Evidence: [`p2_i1_runtime_policy.json`](../configs/p2_i1_runtime_policy.json).
- [x] Verify the baseline fixture against a local non-editable `pygrc==0.1`
  installation: native route-aspect validation and snapshot construction pass,
  the baseline queue and surface log are empty, and the graph repository
  remains unchanged. Evidence: ignored local preflight output reconstructed by
  the [runtime-preflight command](../scripts/README.md#runtime-preflight). This
  is infrastructure evidence only.
- [x] Add deterministic tests for policy, aggregation, missingness, coverage,
  null generation, selectivity, profile identities, portable identity, and
  runtime binding boundaries. Evidence:
  [`test_p2_i1.py`](tests/test_p2_i1.py).
- [x] Generate the retained CAL-PRE identity from the final implementation
  commit and record its canonical, semantic-file, and exact-file digests.
- [x] Obtain independent CAL-PRE review. Review record:
  [P2-I1 CAL-PRE review](../reports/P2-I1-CAL-PRE-review.md).

CAL-PRE gate disposition — 2026-07-11:

> The retained CAL-PRE identity correctly anchors the reviewed implementation,
> its declared digests and candidate-absence boundaries are consistent, and
> runtime-dependent evidence remains deferred.

Disposition: `P2-I1-CAL-PRE-GATE=passed`. This opens candidate-blind
calibration only. Candidate execution, registration, L01 rungs, and ecology
claims remain closed.

CAL-PRE implementation details and interpretation — 2026-07-11:

- Scientific structure is declarative and digest-bound across six separate
  surfaces: fixture, cells, analysis, calibration, provenance, and runtime.
  This keeps scientific policy reviewable without importing machine-local
  runtime location or state.
- The seven-cell matrix has closed roles. The primary normalized margin is
  `candidate-conditioning` versus `reference`; medium dependency and
  selectivity separately compare `candidate-conditioning` with
  `medium-freeze-withdrawal`. Callers cannot substitute other comparison roles
  during analysis.
- Each cell/seed run defines one branch point and four independently restored
  later opportunities. Static opportunity-profile identities are frozen now;
  live registration must add resolved contact, history, and restoration
  identities while proving exact cross-cell matching and no branch carryover.
- One pure analysis path validates opportunity records, preserves scientific
  versus operational missingness, aggregates over the fixed planned
  denominator, retains raw paired coverage, and emits serialization-ready
  margin, selectivity, rung, and terminal inputs. The thin CLI does not carry a
  second scientific policy.
- Matched-null generation is deterministic and candidate-blind: its five
  seeds are disjoint from the three candidate seeds, and it accepts neither
  candidate artifacts nor PyGRC runtime inputs. The implementation-time null
  output tested the generator only; it was not retained as calibration
  evidence.
- Runtime binding fails closed against an explicitly selected, machine-local
  PyGRC realization profile. There is no fallback or silent transition from an
  RCAE-owned producer to later native functionality, and candidate execution
  remains mechanically disabled.
- The clean source anchor and later retention commit avoid circular identity.
  Canonical-payload, semantic-file, and exact-file digests distinguish three
  kinds of drift. Independent clean-worktree reconstruction reproduced all
  three and passed the 25 P2-I1 plus 32 Phase 1 tests.

Interpretation: CAL-PRE freezes how P2-I1 asks and measures the niche question;
it does not observe an answer. Calibration still must retain the candidate-
blind null lineage and freeze the resolution sheet before registration. The
eventual `delta` is a resolution/proximity guide for interpreting the specific
result, not a substitute for examining narrow success, near misses, structural
quality, or alternative realizations. Selectivity remains a separate causal
question. Runtime preflight is narrower still: it shows only that the declared
fixture constructs against the selected local PyGRC and cannot support or
refute L01.

## 7. Calibration gate

Entry condition:

- [x] `P2-I1-CAL-PRE-GATE` passed. Evidence:
  [P2-I1 CAL-PRE review](../reports/P2-I1-CAL-PRE-review.md).

Required calibration work:

- [x] Retain generator command/profile, dependencies, source revisions,
  configuration identity, input digests, and resource envelope. Evidence:
  [CAL-GATE freeze](../contracts/p2-i1/calibration-freeze.json).
- [x] Verify the generator and input lineage contain no candidate-derived
  outcome or post-outcome tuning. Evidence: candidate-blindness projection in
  the [CAL-GATE freeze](../contracts/p2-i1/calibration-freeze.json); independent
  review remains the exit condition below.
- [x] Generate and retain all per-seed matched-null margins. Evidence:
  [matched null](../contracts/p2-i1/matched-null.json).
- [x] Run `freeze-resolution` once on the registered calibration input.
- [x] Verify `delta` equals the maximum of measurement resolution and absolute
  matched-null margins. Observed values: maximum absolute null margin `0.0`,
  measurement resolution `1e-12`, and frozen `delta=1e-12`.
- [x] Produce schema-valid `metric_calibration` and frozen `metric_sheet`
  records. Evidence: [metric calibration](../contracts/p2-i1/metric-calibration.json)
  and [frozen metric sheet](../contracts/p2-i1/frozen-metric-sheet.json).
- [x] Reconstruct calibration independently and compare canonical and file
  digests. Evidence: reconstruction projection in the
  [CAL-GATE freeze](../contracts/p2-i1/calibration-freeze.json).
- [x] Record calibration evidence effect as resolution-only, never lane
  support or refutation. Evidence: all retained CAL-GATE records.

Exit gate `P2-I1-CAL-GATE`:

- [x] Matched-null provenance is complete and reconstructable.
- [x] Candidate blindness is reviewed rather than merely self-declared.
- [x] Frozen sheet references the retained calibration artifact.
- [x] Calibration opened no candidate outcome or lane claim.

CAL-GATE implementation progress — 2026-07-11:

- [x] Retain five matched-null panels spanning every possible four-opportunity
  formation fraction through the same aggregation and margin functions used by
  later analysis.
- [x] Retain zero margins for seeds `19`, `43`, `71`, `109`, and `163`, all
  disjoint from candidate seeds `101`, `211`, and `307`.
- [x] Freeze `delta=1e-12` from the numeric measurement floor because the
  maximum absolute matched-null margin is `0.0`.
- [x] Reproduce the matched null, metric calibration, and frozen metric sheet
  byte-for-byte in a detached clean worktree with no PyGRC installed; all 57
  tests and both validators pass.
- [x] Obtain independent review and record the gate disposition. Review
  packet: [P2-I1 CAL review](../reports/P2-I1-CAL-review.md).

Implementation interpretation: the five equal null pairs show that the pure
analysis path introduces no detectable difference anywhere in the discrete
formation-fraction domain. Consequently `delta` is the numeric floor, not an
empirical runtime-noise estimate and not a substantive effect-size boundary.
It supports later proximity classification but cannot make a candidate result
scientifically sufficient. Raw coverage, seed distribution, dependency,
selectivity, causal controls, and alternate realizations remain decisive.
Calibration consumed no PyGRC state and therefore says nothing about runtime
formation behavior.

CAL-GATE disposition — 2026-07-11:

> The retained candidate-blind calibration is reconstructable, its zero null
> margins freeze only the declared numeric resolution floor, and no candidate
> or lane claim was opened.

Disposition: `P2-I1-CAL-GATE=passed`. This opens registration work only.
Candidate execution, selectivity evaluation, L01 rungs, and ecology claims
remain closed.

D-020 bounded refresh — 2026-07-11:

- [x] Record the accepted separation between cycle-scoped
  `P2-I1-EXEC-FREEZE` authorization and post-execution `P2-I1-EXEC-GATE`
  closure. Evidence: [`P2-I1-DEC-020`](P2-I1-decision-record.md).
- [x] Preserve the committed v1 CAL-PRE/CAL identities, artifacts, reviews,
  and source anchors as versioned history.
- [x] Change only the runtime authorization boundary and its direct
  validator, tests, and documentation.
- [x] Commit the bounded-refresh source anchor with candidate outcomes absent.
  Source revision: `1c9736dee165d44ed1d837f673f03a9a69bba113`.
- [x] Generate and independently reconstruct the v2 CAL-PRE identity. Evidence:
  [v2 identity](../contracts/p2-i1/cal-pre-identity-v2.json) and
  [bounded-refresh freeze](../contracts/p2-i1/d020-bounded-refresh-freeze-v2.json).
- [x] Verify the calibration-realization digest is unchanged while the runtime
  configuration and derived measurement identities change as declared.
- [x] Regenerate the matched null, metric calibration, and frozen metric sheet
  and prove byte-for-byte equality with v1. Evidence:
  [bounded-refresh freeze](../contracts/p2-i1/d020-bounded-refresh-freeze-v2.json).
- [x] Close the refresh by deterministic verification because the semantic
  source correction was already reviewed and no new decision or unknown
  assumption appeared afterward. Verification record:
  [D-020 bounded refresh closeout](../reports/P2-I1-D020-bounded-refresh-review.md).

## 8. Registration gate

Entry conditions:

- [x] `P2-I1-THEORY-GATE` passed.
- [x] `P2-I1-CAL-PRE-GATE` passed. Evidence:
  [P2-I1 CAL-PRE review](../reports/P2-I1-CAL-PRE-review.md).
- [x] `P2-I1-CAL-GATE` passed. Evidence:
  [P2-I1 CAL review](../reports/P2-I1-CAL-review.md).
- [x] `P2-I1-DEC-020` bounded v2 CAL-PRE/CAL refresh passed. Evidence:
  [D-020 bounded refresh closeout](../reports/P2-I1-D020-bounded-refresh-review.md).

### 8.1 Operational identities

- [x] Participant carrier and continuity criterion frozen. Evidence:
  [registration policy](../configs/p2_i1_registration_policy.json) and
  [pattern card](../contracts/p2-i1/registration-records/pattern-card.json).
- [x] Medium carrier, access scope, and non-private/sharedness account frozen.
  Evidence: [medium surface](../contracts/p2-i1/registration-records/medium-surface.json).
- [x] Participant writing event and attributable lineage frozen. Evidence:
  [registration policy](../configs/p2_i1_registration_policy.json) and
  [medium surface](../contracts/p2-i1/registration-records/medium-surface.json).
- [x] Persistence/decay and later-response windows frozen with rationale.
  Evidence: [medium surface](../contracts/p2-i1/registration-records/medium-surface.json)
  and the accepted window/config authorities imported by the registration
  policy.
- [x] Parent context and support context declared separately from the candidate
  medium and assigned controls. Evidence: [pattern card](../contracts/p2-i1/registration-records/pattern-card.json)
  and [parent-context debt](../contracts/p2-i1/registration-records/parent-context-debt.json).
- [x] Freeze participant/medium separation with a state-matched
  feedback-row-absent intervention; no co-constitution claim is made. Evidence:
  [`P2-I1-DEC-015`](P2-I1-decision-record.md).

The accepted plan controls private participant state as a sufficient cause but
retains a participant-mediated reading ceiling. It does not claim autonomous
reader access.

If co-constitution is claimed, the plan must produce distinct outcomes for:

```text
participant_ablation_control
medium_ablation_control
independent_medium_reconstruction
writer_event_removal_control
private_state_only_control
```

- [ ] Medium state can be reconstructed independently of the participant
  label.
- [x] Participant continuity is not inferred from the later medium outcome.
  Evidence: [medium surface](../contracts/p2-i1/registration-records/medium-surface.json).
- [ ] Medium ablation changes the later response while participant and medium
  ablations have distinguishable effects.
- [x] Writing and reading are frozen as temporally and interventionally
  separable; execution must still verify the registered causal chain. Evidence:
  [medium surface](../contracts/p2-i1/registration-records/medium-surface.json)
  and [registration policy](../configs/p2_i1_registration_policy.json).
- [ ] If these checks cannot be implemented, registration limits the possible
  result to producer-carried or missing participant/medium separation.

### 8.2 Measurement and selectivity

- [x] Response family, raw formula/units, orientation, opportunity structure,
  aggregation, windows, normalization, and calibration realization import
  unchanged from the accepted calibration preregistration. Evidence:
  [registration validator](../scripts/p2_i1_registration.py).
- [x] Registration identifies the imported fields and proves one-to-one
  identity; any change starts a new calibration and probe cycle.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json)
  and [registration validator](../scripts/p2_i1_registration.py).
- [x] Produce `calibration_measurement_identity_digest` and
  `registration_measurement_identity_digest` over response formula/units,
  orientation, unit of analysis, opportunity structure, aggregation, windows,
  normalization, participant/medium fixture identity, and matched-null
  realization, writer-reader relation, and frozen analysis identity. Evidence:
  [registration validator](../scripts/p2_i1_registration.py).
- [x] Produce `calibration_realization_digest` and
  `registration_realization_digest`, then require machine-derived
  `measurement_identity_match=true` and `realization_identity_match=true`.
  Evidence: [registration validator](../scripts/p2_i1_registration.py).
- [x] Both realization digests hash the same calibration-relevant identity
  projection rather than their entire bundles; registration-only controls and
  execution details remain separately digested and cannot mask projection
  drift. Evidence: [registration validator](../scripts/p2_i1_registration.py).
- [x] Any digest mismatch fails closed and reopens CAL-PRE/CAL; prose review
  cannot waive it. Evidence: [registration tests](tests/test_p2_i1_registration.py).
- [x] Freeze configured polarity susceptibility as the compatibility-relative
  selectivity discriminator. Evidence:
  [`P2-I1-DEC-007`](P2-I1-decision-record.md).
- [x] Freeze the `selectivity_axis`, aligned/inverted groups, positive expected
  interaction direction, `0.5` minimum selectivity margin, and
  main-effect-versus-interaction test. Concrete group profiles are fixed by
  `P2-I1-DEC-010`; verified baseline viability remains registration work.
  Evidence:
  [`P2-I1-DEC-007`](P2-I1-decision-record.md).
- [x] Import Policy A fields unchanged, demonstrate that the minimum
  selectivity margin derives from the frozen candidate-blind threshold source,
  and prohibit use of calibrated `delta` for selectivity classification.
  Policy authority: [`P2-I1-DEC-007`](P2-I1-decision-record.md); import proof
  remains a registration artifact.
- [ ] Verify matched baseline opportunity and support for every selectivity
  group before the medium-history intervention.
- [x] Freeze `medium_history_match_fields`, exposure digest per group, trace
  quantity/timing tolerances, and surface-access tolerance.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json).
- [ ] Verify comparable medium history across selectivity groups before
  attributing their different later responses to the discriminator.
- [x] Generic main effects that change all groups similarly cannot pass the
  selectivity gate; the declared medium-history-by-discriminator interaction
  must resolve. Evidence: imported selectivity analysis identity in the
  [registration policy](../configs/p2_i1_registration_policy.json).
- [x] Magnitudes across response families declared non-comparable. Evidence:
  `measurement_scope` in the
  [registration policy](../configs/p2_i1_registration_policy.json).

### 8.3 State isolation, order, and matching

- [x] Freeze one expected baseline identity for every exact cell/seed
  configuration, fresh worker construction for every attempt/retry, and W2
  branch restoration as a separate identity boundary. Evidence:
  [`P2-I1-DEC-023`](P2-I1-decision-record.md).
- [x] Freeze cell execution order and declare fixed or randomized order policy.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json).
- [x] If randomized, freeze the order-randomization seed before execution; if
  fixed, record order effects as an explicit control or debt.
  Evidence: [fixed-order debt](../contracts/p2-i1/registration-records/fixed-order-debt.json).
- [x] Freeze one baseline identity per exact cell/seed configuration, the
  fresh-worker reset procedure, and the expected W0 queue/surface state.
  Evidence: [baseline identity registry](../contracts/p2-i1/baseline-identity-registry.json)
  and [registration policy](../configs/p2_i1_registration_policy.json).
- [ ] Every independent cell/seed starts from that baseline unless cumulative
  history is an explicit registered feature.
- [ ] Cross-cell and cross-seed contamination audits prove no trace from one
  run remains available to another.
- [ ] Every registered live branch emits its resolved opportunity-profile
  digest from the frozen static profile, actual pulse-contact and medium-history
  digests, and an exactly restored branch-point digest; cross-cell static-panel
  matching and zero cross-branch carryover validate before interpretation.
- [x] Freeze support/budget matching variables and tolerances across reference,
  candidate, freeze/withdrawal, shuffle, and inversion cells.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json).
- [ ] Require a retained support/budget matching audit before scientific
  interpretation.

### 8.4 Realization, retry, and reproducibility

- [x] Freeze one retained, path-free realization profile across registration
  and the declared P2-I1 operation classes; distinguish binding/baseline
  conformance from scientific success and execution authorization. Evidence:
  [`P2-I1-DEC-022`](P2-I1-decision-record.md).
- [x] Exact PyGRC-compatible execution class selected. Evidence:
  [realization profile](../contracts/p2-i1/registration-realization-profile.json).
- [x] Realization profile records local availability/enabled state without a
  machine-local path.
  Evidence: [realization profile](../contracts/p2-i1/registration-realization-profile.json).
- [x] Any constructed mechanism declares necessity, minimality, counterfactual,
  withdrawal, implementation identity, debts, and claim ceiling.
  Evidence: [constructed mechanism](../contracts/p2-i1/registration-records/constructed-mechanism.json).
- [x] Exact cells, candidate seeds `101`, `211`, and `307`, attempt limits,
  resources, and expected artifacts frozen.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json).
- [x] Preserve the resolved Phase 1 scope: at most one infrastructure retry per
  comparison cell, shared across that cell's three seeds; never one retry per
  seed or one pool silently shared by the whole cycle.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json).
- [x] Freeze the deterministic seed-allocation rule used if more than one seed
  in a cell encounters an infrastructure failure; outcome inspection cannot
  choose which seed receives the retry.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json).
- [x] An infrastructure retry uses the same seed, configuration, initial-state
  digest, and scientific parameters; begins from the reset baseline; is never
  outcome-dependent; and retains the failed attempt and infrastructure-only
  reason.
  Evidence: [registration policy](../configs/p2_i1_registration_policy.json).
- [x] Runtime receipt requirement exists for every live run. Evidence:
  [registration policy](../configs/p2_i1_registration_policy.json).
- [x] Reconstruction commands and retention roles frozen. Evidence:
  [registration tooling instructions](../scripts/README.md).
- [x] Graph read-only fingerprint guard configured for live use. Evidence:
  [registration tooling](../scripts/p2_i1_registration.py).
- [x] Freeze candidate authorization as an exact cycle-scoped
  `P2-I1-EXEC-FREEZE`, distinct from the post-execution `P2-I1-EXEC-GATE`.
  Evidence: [`P2-I1-DEC-020`](P2-I1-decision-record.md).

Local artifact-validity rules:

- [x] Every manifest-selected artifact's SHA-256 matches its file contents and
  resolved manifest declaration. Evidence:
  [registration manifest](../contracts/p2-i1/registration-manifest.json) and
  [REG-GATE review](../reports/P2-I1-REG-review.md).
- [ ] Positive-evidence rows identify source-current inputs and their digests.
- [x] Portable registration inputs and existing-schema records contain no
  machine-local or absolute paths; the derived freeze revalidates this rule.
  Evidence: [registration tooling](../scripts/p2_i1_registration.py).
- [x] Canonical payload digest and file-content SHA-256 are both retained where
  the record contract provides them; existing-schema receipt and manifest
  records retain their schema IDs plus semantic and exact-file digests rather
  than adding out-of-schema fields. Evidence:
  [REG-GATE review](../reports/P2-I1-REG-review.md).
- [ ] `derived_report_only=true` artifacts cannot support a positive boundary
  rung.
- [x] Reconstruction regenerates canonical machine content, not merely a
  semantically similar authored report. The three direct records and the
  same-target freeze/manifest reconstruction compare byte-for-byte. Evidence:
  [REG-GATE review](../reports/P2-I1-REG-review.md).

### 8.5 Registration evidence bundle

- [x] Freeze the bundle representation as one experiment-local registration
  policy plus existing schema records, a derived registration freeze, and a
  resolved manifest; defer first-class `lane_registration` and
  `control_outcome` records to R3 unless concrete friction satisfies the
  reopening conditions. Evidence:
  [`P2-I1-DEC-021`](P2-I1-decision-record.md).
- [x] Bundle resolves the brief, hypothesis, lane registry, execution policy,
  metric sheet, calibration, pattern card, medium surface, realization profile,
  constructions, controls, claims, debts, profiles, and expected manifest.
  Evidence: [registration freeze](../contracts/p2-i1/registration-freeze.json)
  and [registration manifest](../contracts/p2-i1/registration-manifest.json).
- [x] Every common control has an explicit applicability disposition and
  resolution stage; the retained freeze derives its lifecycle only from exact
  evidence bindings. Evidence:
  [registration policy](../configs/p2_i1_registration_policy.json) and
  [registration freeze](../contracts/p2-i1/registration-freeze.json).
- [x] Every L01 control has a planned outcome artifact or the accepted D-025
  inapplicability. Evidence:
  [registration policy](../configs/p2_i1_registration_policy.json).
- [x] Every inherited control records source artifact, source digest, inherited
  role, identical-scope verification, `must_not_consume_as`, and whether new
  lane execution is required. Evidence:
  [inherited control verification](../contracts/p2-i1/inherited-control-verification.json).
- [x] Inheritance supplies only method, schema, or fixed runtime-invariant
  evidence unless identical carrier, mechanism, intervention, and claim scope
  are demonstrated; it never substitutes for lane-specific causal evidence.
  Evidence: [registration tooling](../scripts/p2_i1_registration.py).
- [x] The bundle contains no candidate outcome. The retained freeze records
  `candidate_outcomes_absent=true`, candidate execution closed, and no positive
  or negative lane evidence. Evidence:
  [registration freeze](../contracts/p2-i1/registration-freeze.json).
- [x] Independent review confirms `validate-phase1` success alone was not
  treated as registration. Evidence: [REG-GATE review](../reports/P2-I1-REG-review.md).
- [x] Registration review records unresolved execution questions and why none
  blocks registration. Evidence: [REG-GATE review](../reports/P2-I1-REG-review.md).

Focused source-safety corrections required by the REG-GATE implementation
review:

- [x] Retained registration generation fails when source files differ from the
  source revision; only the five expected generated outputs are ignored while
  assembling the post-anchor bundle. Dirty review artifacts require
  `--allow-dirty-preview`, carry a preview-specific kind and
  `retention_eligible=false`, and cannot enter the manifest. Evidence:
  [registration tooling](../scripts/p2_i1_registration.py) and
  [registration tests](tests/test_p2_i1_registration.py).
- [x] Every registration-time `resolved` leg has exact
  `evidence_binding_refs`; both its evidence description and bindings are
  validator-frozen, and missing or substituted evidence yields `blocked` or
  policy rejection rather than resolution. Evidence:
  [registration policy](../configs/p2_i1_registration_policy.json),
  [registration tooling](../scripts/p2_i1_registration.py), and
  [registration tests](tests/test_p2_i1_registration.py).
- [x] Runtime conformance resolves all seven operation classes to concrete
  callable PyGRC methods; version and namespace checks alone cannot pass the
  registration receipt. Evidence:
  [runtime boundary](../scripts/p2_i1_runtime.py) and
  [runtime tests](tests/test_p2_i1.py).

### 8.6 REG-GATE implementation record and interpretation — 2026-07-11

**Record status:** retained post-anchor bundle complete, exactly reconstructed,
and accepted at REG-GATE. Everything described here has `registration-only`
or infrastructure effect. It is not candidate execution, positive or negative
L01 evidence, or a niche result.

#### 8.6.1 What was implemented

The registration source layer now contains four mutually constrained parts:

1. [The registration policy](../configs/p2_i1_registration_policy.json)
   imports the frozen v2 CAL-PRE/CAL identities and freezes operational
   carrier identities, seven cells, three seeds, fixed order, fresh-worker
   reset, retry allocation, matching fields and tolerances, resources,
   expected artifacts, claims, and every common/L01 control plan.
2. [The reconstruction profile registry](../configs/p2_i1_registration_profiles.json)
   freezes path-free environment, dependency, resource, generation, and
   verification commands. The exact PyGRC and graph checkout locations remain
   local command arguments.
3. Eight existing-schema records under
   [`registration-records/`](../contracts/p2-i1/registration-records/) define
   one pattern card, one medium-surface candidate, one constructed
   orchestration boundary, one registration claim boundary, and four debts.
   No new `lane_registration` or `control_outcome` common record was added.
4. [`p2_i1_registration.py`](../scripts/p2_i1_registration.py) validates and
   joins those inputs, verifies inherited sources, binds native runtime
   capabilities, constructs W0 baseline identities in fresh workers, derives
   evidence-sensitive control status, freezes the bundle, and builds the
   non-recursive resolved manifest. [`p2_i1_runtime.py`](../scripts/p2_i1_runtime.py)
   owns the fail-closed PyGRC binding and concrete operation-capability map.

The deterministic generation path is:

```text
frozen CAL-PRE/CAL identities
  -> registration policy and existing-schema record validation
  -> exact N29/N30 inherited-source verification
  -> path-free PyGRC binding receipt plus concrete method conformance
  -> 21 fresh-worker W0 baseline identities
  -> exact evidence-binding resolution for registration controls
  -> derived registration freeze
  -> resolved manifest over files that actually exist
```

The manifest is deliberately last: it may digest the freeze, while the freeze
can only declare the expected manifest path. This avoids a recursive identity.

The post-anchor generation step retained five machine artifacts under
`contracts/p2-i1/`:

| Artifact | Registration role |
| --- | --- |
| `inherited-control-verification.json` | Exact N29/N30 paths, file/output digests, inherited roles, non-identical scope, blocked consumption, and fresh-execution requirement |
| `registration-runtime-binding-receipt.json` | Observed PyGRC identity, public capabilities, concrete callable operation surfaces, source state, and graph read-only result |
| `baseline-identity-registry.json` | All 21 ordered W0 cell/seed identities, native snapshots, route identity, empty queue/surface checks, and composite digests |
| `registration-freeze.json` | Imported identity equality, 32-file bundle digests, exact evidence resolution, control lifecycle, reconstruction commands, and closed claims |
| `registration-manifest.json` | Non-recursive resolved retention index over the 15 selected registration artifacts and their shared/realization profiles |

#### 8.6.2 Geometric and runtime artifacts materialized

The registered geometry is a four-node fixed-topology fixture:

```text
P --participant_to_writer--> W
P <--writer_return---------- W
P --reader_a---------------> A
P --reader_b---------------> B
```

- `P` is the participant/source-pole carrier and `W` the writer/return pole.
  Their two directed edges form one validated closed route aspect.
- `A` and `B` are distinct later-reader contexts. Four opportunity profiles
  cross these two contexts with aligned/inverted configured susceptibility;
  the four profiles retain distinct identities while resolving to exactly two
  reader carrier configurations.
- Seeds `101`, `211`, and `307` apply balanced coherence offsets
  `{-1/32, 0, +1/32}`: `P=1+offset`, `W=1-offset`, and `A=B=0.5`.
- The parent-context contrast is not a parent basin. It is a declared
  reduced-support geometry with `W=0.5-offset` and `A=B=0.25`, preserving the
  registered feedback-score relation while changing absolute support.
- The carrier-timescale contrast changes reader packet amount from `0.125` to
  `0.25`; it does not silently alter W0 node coherence.

The retained candidate-free W0 registry constructed all
`7 cells x 3 seeds = 21`
configurations in separate worker processes. It produced:

| Geometric identity observation | Retained result | Meaning |
| --- | ---: | --- |
| Explicit cell/seed entries | `21` | No legitimate configuration was collapsed |
| Composite baseline digests | `21` unique | Cell configuration remains part of identity even when native state coincides |
| Native snapshot digests | `6` unique | Three ordinary seed states plus three reduced-support seed states |
| Route-aspect digests | `1` unique | All cells retain the same participant-writer route geometry |
| Initial queue states | all empty | No scheduled packet contaminates W0 |
| Initial focal surfaces | all empty | No medium row or outcome is preinstalled at W0 |

The runtime binding also verified concrete callable PyGRC surfaces for fixture
construction, route validation, snapshot/load, queue stepping,
feedback-eligibility surface emission, and feedback-conditioned packet
production. This demonstrates that the registered operation family exists in
the selected `pygrc==0.1` realization. It does not demonstrate that the
candidate sequence succeeds.

What the geometric materialization shows:

- the declared initial topology, coherences, route aspect, profiles, and cell
  transforms are constructible and distinguish intended from unintended W0
  differences;
- each exact configuration can begin from an auditable fresh native state;
- no queue, medium row, candidate outcome, or cross-cell history is smuggled
  into the baseline; and
- the calibration and registration measurement/realization projections remain
  identical (`853c5f10...f2e5a` and `9b59988a...769b8`).

What it does **not** show:

- an attributable writer event or committed feedback row;
- independent medium reconstruction after writing;
- persistence from writing to the later branch point;
- branch restoration, comparable exposure, or zero carryover after W2;
- later opportunity formation, medium dependency, selectivity, or causal
  source-lineage dependence; or
- niche conditioning, niche formation, agency, coordination, motif, or regime.

Those remain execution comparisons in Sections 9-14.

#### 8.6.3 Agentic-ecology materialization

The registration turns the L01 theory into a bounded ecology-side object
without claiming its result:

- **Participant:** structural source-pole identity, lineage identity, and a
  budgeted one-repeat reserve; continuity is defined before and independently
  of the later outcome.
- **Medium candidate:** a native model-owned pulse-contact to
  feedback-eligibility row, outside participant identity and available under
  bounded shared-local counterfactual access. Reading remains
  participant-mediated, which is retained as explicit debt.
- **Historical relation:** participant write/contact, attributable row source,
  bounded W1-to-W2 persistence, and a later configured opportunity are
  separately named so that mere environmental improvement cannot satisfy L01.
- **Selectivity:** aligned and inverted susceptibility groups must receive
  comparable medium history and differ through the frozen interaction; a
  generic main effect remains below the niche boundary.
- **Support context:** no parent basin exists in the primary fixture. Absolute
  support is visible through one bounded contrast and parent-context debt,
  blocking parent-modulation and higher ecology claims.
- **Construction/native boundary:** RCAE configures and orchestrates the
  experiment but may not compute the later response or inject native state.
  The medium and feedback producer remain native PyGRC surfaces; RCAE remains
  constructed, and any future native transition requires a new profile,
  cycle, and rerun.
- **Catalog placement:** the pattern remains a `registered_probe`,
  `building_block` candidate with `candidate` maturity and `absent` domain
  role. It is not a reusable motif or admitted ecology.

The N29/N30 spiral is also made operational rather than rhetorical. Five exact
graph-side sources are digest-verified under a read-only guard, but all four
identical-scope dimensions—carrier, mechanism, intervention, and claim
scope—remain false. Inheritance supplies method, debt, control patterns, and
the P2/M2 evidence ceiling only; fresh L01 execution remains mandatory.

#### 8.6.4 Control and claim result at registration time

The retained freeze resolves `13` outcome-independent legs. Seven controls are
fully resolved because all their exact evidence bindings validate:

```text
AE01-CTRL-01  conceptual/source-role boundary
AE01-CTRL-02  N30 claim ceiling
AE01-CTRL-03  N29 component versus composition boundary
AE01-CTRL-07  composition-scope guard
AE01-CTRL-11  participant/medium carrier separation record
AE01-CTRL-15  constructed-role and no-silent-transition guard
AE01-CTRL-16  constructed-mechanism completeness
```

Sixteen controls remain `pending_execution`. These include mixed controls
whose registration leg resolved but whose causal leg did not (`04`, `05`,
`08`, `09`, `10`, and `17`), causal/withdrawal comparisons (`06` and L01
controls `01`-`04`), and terminal report guards (`12`, `13`, `14`, `18`, and
`19`). `AE01-L01-CTRL-05` alone is `not_applicable` under D-025. No control is
blocked, but pending is not passing.

The registration claim ceiling is therefore:

```text
portable, internally constrained registered probe candidate
```

It is not:

```text
positive lane evidence
negative lane evidence
candidate execution authorization
native niche formation
agentic ecology success
```

#### 8.6.5 Reproducibility, safety, and remaining work

The five artifacts were generated from clean source anchor `6ca9391`, record
`retention_eligible=true` and `preview_only=false` where those fields are
provided, and retain no machine-local path. The graph checkout remained clean
at verified revision `1f42cb1`.

Independent regeneration reproduced the inherited verification, runtime
receipt, and baseline registry byte-for-byte. Because the freeze deliberately
digests portable bundle paths, an alternate-output-directory freeze correctly
changes those paths and its canonical digest. Regeneration at the declared
experiment-relative paths reproduced both the freeze and manifest
byte-for-byte. The retained semantic and exact-file digests are recorded in the
[REG-GATE review](../reports/P2-I1-REG-review.md).

The retained implementation passes all `75` tests, Phase 1 validation, P2-I1
config validation, registration-policy validation, portable-path checks, exact
reconstruction, and graph read-only checks. The manifest resolves `15`
selected artifacts totaling `139881` bytes; the freeze digests `32` bundle
files. Both imported measurement and realization identities match exactly.
The freeze retains its pre-manifest
`reg_gate_disposition=pending_review_and_manifest`; the non-recursive manifest
and this review close those later administrative facts without rewriting the
frozen record.

The remaining Section 8 checks concern either live causal execution or the
owner's bounded gate disposition. The independent-medium, ablation,
branch-restoration, exposure-comparability, support/budget, and carryover
questions remain explicit pending-execution obligations rather than being
promoted into registration facts. Candidate execution stays closed until a
separate exact-cycle `P2-I1-EXEC-FREEZE` is retained after REG-GATE passes.

Exit gate `P2-I1-REG-GATE`:

- [x] Registration bundle is explicit, internally consistent, and portable.
- [x] Measurement and realization digest equality verifies calibration and
  registration identities one-to-one.
- [x] Candidate execution configuration cannot drift without a new cycle.
- [x] No registration fact is promoted into positive lane evidence.

## 9. Frozen comparison-cell readiness

All applicable common record guards govern the bundle and each affected
artifact. The table names the exact direct causal/withdrawal IDs for each cell;
`none` means a registered baseline, not absence of controls.

| Cell | Group | Exact direct controls | Implementation frozen | Expected artifacts frozen | Ready |
| --- | --- | --- | --- | --- | --- |
| `reference` | reference | none; registered matched baseline | [x] | [x] | [ ] |
| `candidate-conditioning` | candidate | `AE01-CTRL-04`, `AE01-CTRL-05`, `AE01-CTRL-11` | [x] | [x] | [ ] |
| `medium-freeze-withdrawal` | withdrawal | `AE01-CTRL-06`, `AE01-CTRL-08`, `AE01-L01-CTRL-01` | [x] | [x] | [ ] |
| `trace-shuffle` | lineage/source | `AE01-CTRL-06`, `AE01-L01-CTRL-02` | [x] | [x] | [ ] |
| `parent-context-contrast` | active null | `AE01-CTRL-10`, `AE01-L01-CTRL-04` | [x] | [x] | [ ] |
| `susceptibility-inversion` | budget/leakage and selectivity | `AE01-CTRL-09`, `AE01-L01-CTRL-03` | [x] | [x] | [ ] |
| `carrier-timescale-contrast` | transfer/contrast | none; registered single-axis transfer contrast | [x] | [x] | [ ] |

Cell-specific freeze requirements:

- [x] Freeze the logical `reference`, `medium-freeze-withdrawal`, and
  `trace-shuffle` interventions plus causal-order guard. Evidence:
  [`P2-I1-DEC-015`](P2-I1-decision-record.md) and
  [`P2-I1-DEC-016`](P2-I1-decision-record.md). Concrete C01 operations and
  artifact fields and retained-eligible EXEC-FREEZE identities are
  materialized; tracked authorization remains pending.
- [x] Freeze `parent-context-contrast` as the single-axis, score-preserving
  reduced-support transform in
  [`P2-I1-DEC-017`](P2-I1-decision-record.md), with no parent-basin claim.
  The C01 support/budget auditor treats it as one declared exception.

- [x] `medium-freeze-withdrawal` declares exactly one `intervention_kind` per
  probe cycle: `medium_freeze` or `scaffold_withdrawal`, plus whether
  participant opportunity, baseline support, and parent context are preserved.
  The primary C01 realization is `medium_freeze`, preserves native producer
  invocation and participant opportunity, and sets scaffold withdrawal false.
  Evidence: [C01 execution policy](../configs/p2_i1_c01_execution_policy.json).
- [x] `intervention_kind=both` is prohibited: it would create two undeclared
  configurations inside one frozen comparison cell and obscure seed, attempt,
  retry, and artifact accounting. Evidence:
  [C01 policy validator](../scripts/p2_i1_execution.py).
- [x] If both interventions are scientifically mandatory, preregister a later
  probe cycle with the other realization of the same logical cell, preserve
  both cycle results, and do not close a claim that requires the unresolved
  control. This remains a change-control rule, not an authorized C01 variant.
- [x] Record constructed-scaffold withdrawal as not applicable to the primary
  cycle because no constructed scaffold carries the accepted native medium or
  later response; preserve producer/construction guards and reopen before
  execution if implementation contradicts this account. Evidence:
  [`P2-I1-DEC-025`](P2-I1-decision-record.md).
- [x] `trace-shuffle` freezes preserved quantity, cost, write count, timing
  distribution, carrier size/spatial support, parent/support context, and
  coherence/resource input where applicable. Evidence:
  [C01 execution policy](../configs/p2_i1_c01_execution_policy.json) and
  [cycle auditor](../scripts/p2_i1_execution.py).
- [x] `trace-shuffle` freezes only the source, lineage, ordering, or geometry
  relation to break, plus pre/post digests and quantity-match tolerance.
  C01 changes only the producer's expected source from the writer-arrival
  contact digest to the writer-departure contact digest while retaining the
  arrival-derived row. Evidence:
  [C01 execution policy](../configs/p2_i1_c01_execution_policy.json).
- [x] Freeze `carrier-timescale-contrast` as exactly one axis—reader-packet
  amount `0.125` → `0.250`—with all other fields matched and no broad
  transfer/timescale claim. Evidence:
  [`P2-I1-DEC-018`](P2-I1-decision-record.md) and
  [C01 execution policy](../configs/p2_i1_c01_execution_policy.json).

No additional cell may be introduced inside a frozen cycle. Evidence may
motivate a later preregistered cycle with a new cell, alternative, or revised
question.

Navigation: [decision-to-execution projection](P2-I1-decision-record.md#20-decision-to-execution-projection).
All seven cells now have decision-level definitions; readiness boxes remain
open until their configs, identities, artifacts, and reviews exist.

## 10. Control disposition and outcome tracking

The [control and failure register](../hypotheses/control-and-failure-register.md)
governs meaning. This checklist records local applicability, execution, and
evidence only.

### 10.1 Common controls

- [x] Freeze applicability, resolution stage, and outcome status as independent
  lifecycle concepts: policy declares obligations, derived freezes record
  outcomes, mixed controls split into legs, and inherited controls require full
  provenance. Evidence: [`P2-I1-DEC-024`](P2-I1-decision-record.md).

| Control | L01 priority | Applicability reviewed | Planned evidence | Outcome resolved |
| --- | --- | --- | --- | --- |
| `AE01-CTRL-01` | direct | [x] | [x] | [x] |
| `AE01-CTRL-02` | direct | [x] | [x] | [x] |
| `AE01-CTRL-03` | inherited | [x] | [x] | [x] |
| `AE01-CTRL-04` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-05` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-06` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-07` | inherited | [x] | [x] | [x] |
| `AE01-CTRL-08` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-09` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-10` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-11` | direct | [x] | [x] | [x] |
| `AE01-CTRL-12` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-13` | inherited | [x] | [x] | [ ] |
| `AE01-CTRL-14` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-15` | direct | [x] | [x] | [x] |
| `AE01-CTRL-16` | direct | [x] | [x] | [x] |
| `AE01-CTRL-17` | direct | [x] | [x] | [ ] |
| `AE01-CTRL-18` | inherited | [x] | [x] | [ ] |
| `AE01-CTRL-19` | direct | [x] | [x] | [ ] |

### 10.2 L01-specific controls

| Control | Meaning | Applicability reviewed | Planned evidence | Outcome resolved |
| --- | --- | --- | --- | --- |
| `AE01-L01-CTRL-01` | Medium freeze with participant opportunity preserved | [x] | [x] | [ ] |
| `AE01-L01-CTRL-02` | Matched trace shuffle | [x] | [x] | [ ] |
| `AE01-L01-CTRL-03` | Susceptibility/selectivity inversion | [x] | [x] | [ ] |
| `AE01-L01-CTRL-04` | Parent-context separation | [x] | [x] | [ ] |
| `AE01-L01-CTRL-05` | Constructed-scaffold withdrawal when applicable | [x] | [x] | [x] |

Applicability rules:

- “Not applicable” requires a specific causal or record-role rationale.
- Non-empty prose alone does not prove the rationale is sound.
- A causal or withdrawal control cannot be made inapplicable merely because it
  is difficult or unfavorable.
- Control ID references alone do not satisfy terminal closure; retained outcome
  evidence must resolve.
- An inherited control must resolve all locally required inheritance fields and
  cannot substitute for a lane-specific causal or withdrawal result.
- `AE01-L01-CTRL-01` is medium freeze with opportunity preserved; it is not
  interchangeable with the `AE01-L01-R02` persistence boundary rung.
- `AE01-L01-CTRL-05` is explicitly not applicable in the primary cycle under
  [`P2-I1-DEC-025`](P2-I1-decision-record.md); the checked outcome means
  `not_applicable`, not a successful withdrawal result.

## 11. Current frozen probe cycle

### `P2-I1-C00` — registration preparation

**Status:** closed design-only cycle; never frozen for candidate execution

**Evidence effect:** resolution only; no candidate evidence

- [x] Dedicated brief drafted.
- [x] Dedicated provisional checklist drafted.
- [x] Brief review completed.
- [x] `P2-I1-THEORY-GATE` passed.
- [x] Calibration preregistration accepted and
  `P2-I1-CAL-PRE-GATE` passed.
- [x] Candidate-blind calibration independently reviewed and
  `P2-I1-CAL-GATE` passed.
- [x] D-020 bounded v2 refresh completed without changing calibration
  realization or artifacts.
- [x] Cycle closed as design-only and handed to `P2-I1-C01`. Evidence:
  [REG-GATE review](../reports/P2-I1-REG-review.md).

### `P2-I1-C01` — candidate-execution freeze preparation

**Status:** active; freeze generated but not tracked, so no candidate operation
is authorized at runtime

**Evidence effect:** none; pre-execution materialization only

- [x] Predecessor cycle is `P2-I1-C00`.
- [x] `P2-I1-REG-GATE` passed without resolving live causal outcomes.
- [x] Exact executable cell configurations and expected artifact contracts are
  materialized in candidate-free source. Evidence:
  [C01 execution policy](../configs/p2_i1_c01_execution_policy.json) and
  [execution boundary](../scripts/p2_i1_execution.py).
- [x] One cycle-scoped freeze proves candidate outcomes were absent at freeze.
  Evidence: [C01 EXEC-FREEZE](../contracts/p2-i1/c01/exec-freeze.json).
- [ ] `P2-I1-EXEC-FREEZE` passed.

### C01 source materialization and live-obligation interpretation — 2026-07-11

**Record status:** executable source and candidate-free policy materialized;
`P2-I1-DEC-026` accepted with its layered REG-to-EXEC rationale recorded. The
clean source anchor, retained-eligible binding receipt, and retained-eligible
EXEC-FREEZE reconstruct exactly. Tracking, final gate passage, and candidate
execution remain pending.

The C01 source adds one bounded layer above the passed registration bundle:

1. [The C01 execution policy](../configs/p2_i1_c01_execution_policy.json)
   imports the registered seven cells and three seeds unchanged, freezes exact
   W0-W4 native operations, binds twelve live obligations to machine fields,
   and declares every primary, retry, audit, ledger, and manifest path.
2. [The execution boundary](../scripts/p2_i1_execution.py) builds a
   candidate-free cycle authorization, refuses preview or untracked freezes,
   validates an execution-specific PyGRC callable superset, and runs every
   primary in a fresh worker.
3. The same boundary records deterministic infrastructure failures and permits
   only the lowest failed seed's single same-configuration retry per cell.
4. A cross-run auditor resolves structural obligations without converting a
   magnitude or threshold crossing into a terminal verdict.

The execution-specific PyGRC superset is governed by
[`P2-I1-DEC-026`](P2-I1-decision-record.md). That decision records why exact
execution calls became visible only while materializing W0-W4, why the
retained REG receipt remains valid, what each added call owns, and the concrete
failure condition that alone would justify reopening REG.

The native sequence for each cell/seed is:

```text
W0  construct and match the retained cell/seed baseline
W1  schedule one P->W writer packet and drain departure/arrival events
W2  emit or freeze the arrival-derived feedback row and persist one branch point
W3  restore four independent branches and invoke the native feedback producer
W4  drain scheduled reader work and retain the raw opportunity relation
```

The geometry remains the registered `P-W-A-B` fixture. C01 does not add a
participant, medium carrier, parent basin, reader edge, or comparison cell.
The medium-freeze cell keeps the post-writer base state, arrival contact,
producer call, and opportunity panel while omitting only the feedback row. The
trace-shuffle cell keeps the arrival-derived row but asks the producer to
expect the departure-contact digest. The parent and carrier contrasts retain
their already declared support-scale and reader-load exceptions.

The live obligations split across two evidence levels:

- **per run/opportunity:** W0 identity, empty start, native binding, writer and
  contact lineage, participant-label-free medium reconstruction, four-profile
  viability, common medium exposure, W2 restoration, no branch carryover,
  producer invocation, support/budget projection, raw response, runtime
  receipt, and reconstruction command;
- **cross run:** unique worker scopes, candidate-versus-freeze state matching,
  producer parity, trace-shuffle single-axis matching, ordinary-cell
  support/budget equality, and declared parent/load exceptions.

Independent medium reconstruction is deliberately bounded: the restored W2
snapshot locates and reconstructs the native feedback surface by surface kind
and native lineage without accepting or reading a participant label. This
supports a separable recorded carrier under the participant-mediated reading
ceiling; it does not claim autonomous reader access or co-constitution.

Source validation currently passes `88` tests. Dirty-worktree construction
produces only `p2_i1_c01_exec_freeze_preview`, with retention and candidate
authority both false. No writer packet, feedback row, reader opportunity, or
candidate result has been executed during source materialization.

Post-anchor generation produced a path-free execution-binding receipt and one
exact C01 freeze from source `606bc27`. Both regenerated byte-for-byte in a
separate clean clone. The receipt binds `pygrc==0.1`, the six D-026 methods,
graph revision `1f42cb1`, no fallback, and no graph write. The freeze binds 21
primary run specifications, twelve live obligations, twelve authority records,
nine source files, deterministic retry allocation, every expected artifact,
and the bounded claim ceiling. Detailed digests and reconstruction commands are
recorded in the
[EXEC-FREEZE review](../reports/P2-I1-EXEC-FREEZE-review.md).

Untracked freeze validation passes, but tracked validation fails as intended.
The runtime cannot schedule a candidate operation until both generated records
are committed byte-for-byte and `--require-tracked` passes.

### Candidate-execution freeze template

Every execution cycle records before running:

```text
cycle_id:
predecessor_cycle_id:
change_ids_applied:
question_and_falsifier:
registration_bundle_ref:
calibration_ref:
calibration_preregistration_ref:
resolved_policy_digest:
realization_profile_ref:
configuration_ids:
seeds:
attempt_limit:
infrastructure_retry_limit_per_cell: 1
infrastructure_retry_seed_allocation_rule:
resource_profile_ref:
expected_artifacts:
control_plan_refs:
claim_boundary_ref:
stopping_rule:
frozen_at:
candidate_outcomes_absent_at_freeze:
```

Exit gate `P2-I1-EXEC-FREEZE`:

- [x] `P2-I1-CAL-GATE` and `P2-I1-REG-GATE` passed for the referenced
  identities.
- [x] One active candidate cycle imports the reviewed registration and
  calibration records without drift.
- [x] Exact configurations, seeds, attempts, retry allocation, resources,
  expected artifacts, controls, claim boundary, stopping rule, source
  identities, and realization profile are machine-bound.
- [x] Candidate outcomes were absent when the cycle freeze was retained.
- [x] Runtime authorization applies only to the exact frozen cycle; any change
  invalidates it before another operation can be scheduled.
- [ ] Execution-binding receipt and EXEC-FREEZE match their tracked `HEAD`
  bytes; `--require-tracked` validation passes.

## 12. Execution gate

Entry conditions:

- [x] `P2-I1-CAL-GATE` passed. Evidence:
  [P2-I1 CAL review](../reports/P2-I1-CAL-review.md).
- [x] `P2-I1-REG-GATE` passed. Evidence:
  [P2-I1 REG review](../reports/P2-I1-REG-review.md).
- [ ] `P2-I1-EXEC-FREEZE` passed for the active candidate-execution cycle.

Execution tracking for the active candidate cycle:

| Cell | Seed 101 | Seed 211 | Seed 307 | Receipt/reconstruction | Scientific disposition |
| --- | --- | --- | --- | --- | --- |
| `reference` | [ ] | [ ] | [ ] | [ ] | [ ] |
| `candidate-conditioning` | [ ] | [ ] | [ ] | [ ] | [ ] |
| `medium-freeze-withdrawal` | [ ] | [ ] | [ ] | [ ] | [ ] |
| `trace-shuffle` | [ ] | [ ] | [ ] | [ ] | [ ] |
| `parent-context-contrast` | [ ] | [ ] | [ ] | [ ] | [ ] |
| `susceptibility-inversion` | [ ] | [ ] | [ ] | [ ] | [ ] |
| `carrier-timescale-contrast` | [ ] | [ ] | [ ] | [ ] | [ ] |

Opportunity-level execution requirements:

- [ ] Every run emits the frozen opportunity schema and preserves raw records
  behind each seed aggregate.
- [ ] Opportunity counts, admissibility, aggregation, missingness, and
  structural unavailability match the preregistration.
- [ ] Every opportunity resolves one machine-level causal relation chain from
  writer through medium history to later response, including causal-order and
  medium-dependency-control verification.
- [ ] Writer-reader relation, self-aftereffect control, and sharedness claim
  remain within the registered boundary.
- [ ] Initial-state and post-reset digests match the frozen baseline before
  every independent cell/seed.
- [ ] Cross-cell and cross-seed contamination audits resolve before any causal
  result is interpreted.
- [ ] Execution order matches its frozen order or frozen randomization seed.
- [ ] Support/budget matching and all cell-specific invariant audits resolve.

Infrastructure retry ledger:

| Failure ID | Cell/seed | Failure class | Retry authorized | Retry result | Scientific effect |
| --- | --- | --- | --- | --- | --- |
| — | — | — | — | — | None |

Retry authorization requires the same seed, configuration, initial digest,
scientific parameters, and reset baseline. It is never outcome-dependent, the
failed attempt remains retained, no cell receives more than one retry, and the
registered seed-allocation rule controls any contention within a cell.

Exit gate `P2-I1-EXEC-GATE`:

- [ ] Every registered cell/seed has a valid completed, blocked, or incomplete
  disposition.
- [ ] No undeclared attempt, seed, fallback, or configuration was used.
- [ ] Runtime receipts and graph read-only checks resolve for every live run.
- [ ] Every mandatory control outcome resolves through retained evidence.
- [ ] Reconstruction status is known for every candidate and control artifact.
- [ ] Operational failures remain distinct from scientific negative evidence.

## 13. Developmental interpretation and terminal closure

### 13.1 Machine-derived observation

- [ ] Preserve every raw and oriented primary response.
- [ ] Preserve every per-seed normalized margin.
- [ ] Derive the exact threshold relation from the frozen `delta`.
- [ ] Record response distribution/admissibility rather than one-event success.
- [ ] Record all rungs `AE01-L01-R01` through `R05` with `rung_id`, `status`,
  `required_evidence`, `evidence_refs`, `failed_or_blocked_reason`, and
  `claim_enabled`.
- [ ] Use only `passed`, `failed_closed`, `blocked`, or `not_applicable` as rung
  status and record the honest highest-valid rung.
- [ ] Never skip a rung; a higher rung cannot pass when a lower prerequisite is
  blocked, and metric magnitude cannot compensate for a failed causal rung.
- [ ] `R05` transfer never upgrades support nativity, and a positive terminal
  class does not automatically establish `R04` or `R05`.
- [ ] Record expected, adjacent, and unexpected expressed properties.
- [ ] Record support status and T0–T4 classification value.

### 13.2 Two-axis interpretation

- [ ] Becoming reading states what appeared, where, under what support, and at
  what claim ceiling.
- [ ] Development reading states what condition was disclosed and what should
  be retained, varied, withdrawn, redirected, redescribed, or stopped.
- [ ] Niche medium state, niche-conditioning relation, and niche formation
  remain separate in authored interpretation.
- [ ] Uniform environmental conditioning is not relabeled as selective niche
  conditioning.
- [ ] Occupancy/suitability is not relabeled as historically produced niche
  formation.
- [ ] More specific lane interpretations take precedence when their causal
  discriminator explains the result.
- [ ] Strongest valid claim and every blocked stronger claim are explicit.
- [ ] One next move and its falsifier are recorded.

### 13.3 Terminal-to-claim mapping

| Terminal/rung state | Maximum report wording |
| --- | --- |
| Below `R01` or missing surface | Missing prerequisite or unsuitable realization |
| `R01`–`R02` | Medium-history conditioning observation |
| `R03` | Causal medium-history conditioning candidate |
| `R04` | Bounded niche-conditioning relation candidate |
| `R05` | Limited-transfer bounded niche-conditioning relation candidate |
| `R04`/`R05` plus separately recorded LGRC demand | Bounded niche-conditioning demand pattern |
| Any producer-carried result | Scaffolded observation with explicit debt |

No terminal label licenses stronger wording than its highest valid rung and
support status.

### 13.4 Observed relation and demand implication

The frozen schema is not reopened. Existing authoritative records carry the
distinction as follows:

- [ ] Terminal classification and same-lane developmental interpretation state
  the observed relation and reference only observation/control evidence.
- [ ] `requirement_extraction` records state LGRC demand implications and use
  distinct demand-basis references.
- [ ] Demand records explicitly state that demand is not runtime or native
  substrate evidence.
- [ ] The authored report projects both authorities without merging the demand
  implication into the observed relation.

### 13.5 Terminal classification

- [ ] Complete exactly one terminal record:
  `supported_bounded_candidate`, `partial_or_mixed`, `not_supported`,
  `blocked_missing_prerequisite`, or `incomplete_execution`.
- [ ] Terminal record references the same-lane developmental interpretation.
- [ ] Positive or negative scientific closure uses completed verified retained
  evidence rather than missing runtime or reconstruction.
- [ ] Every failure and debt remains visible.
- [ ] Non-selection effect is applied when required.
- [ ] Human report agrees with controlling machine records.

Exit gate `P2-I1-CLOSE-GATE`:

- [ ] `P2-I1-EXEC-GATE` passed or a complete valid blocked/incomplete closure
  exists.
- [ ] Developmental interpretation is complete and claim-safe.
- [ ] Terminal record, retained manifest, reconstruction, and report agree.
- [ ] New requirements, debts, redirects, and missing surfaces are recorded.
- [ ] No claim exceeds the bounded niche-conditioning demand-pattern ceiling.
- [ ] R3 handoff is prepared without tuning the completed result.

## 14. Evidence-triggered checklist change control

Checklist expansion is expected. It becomes unsafe only when it hides why work
was added, rewrites a previous result, or changes a frozen execution slice
after candidate outcomes.

Allowed change classes:

```text
infrastructure_correction
bounded_local_refinement
alternative_realization
new_boundary_or_naturalization_probe
revise_working_class_or_hypothesis
redescribe_aim
stop_no_reusable_or_generative_value
```

Every change record contains:

```text
change_id
date
triggering_cycle_id
triggering_evidence_refs
observed_limitation_or_new_need
new_checklist_requirement
change_class
target_function
prior_result_preserved
affected_controls_and_artifacts
new_preregistration_required
rerun_scope
claim_and_debt_impact
falsifier
status
```

Change ledger:

| Change ID | Trigger | Change class | New requirement | Rerun scope | Claim impact | Status |
| --- | --- | --- | --- | --- | --- | --- |
| — | Initial provisional checklist | — | No evidence-triggered additions yet | None | None | Empty |

Rules:

- An infrastructure correction repairs the registered run path without
  changing the scientific question, metric, control, or interpretation.
- A bounded local refinement must satisfy the D-038 function-not-proxy guard.
- An alternative or new probe starts a new cycle and preserves the predecessor
  result.
- A hypothesis/class revision or aim redescription records why the previous
  frame was insufficient; it cannot retroactively rescue the prior result.
- Stopping is a valid evidence-driven disposition.

## 15. Probe-cycle history

| Cycle | Purpose | Frozen status | Execution status | Result | Successor reason |
| --- | --- | --- | --- | --- | --- |
| `P2-I1-C00` | Theory, calibration, and registration preparation | Design-only; closed | REG-GATE passed; no candidate execution | Registration-only bundle; no scientific result | Handed exact probe boundary to `P2-I1-C01` |
| `P2-I1-C01` | First exact candidate-execution cycle | Freeze preparation active | Not authorized or executed | None | Materialize exact cells and pass EXEC-FREEZE |

Completed and superseded cycles remain in this table. Their records and
artifacts are never replaced by the successor cycle.

## 16. Evidence ledger

| Evidence ID | Cycle | Artifact role | Path or manifest ref | Reconstruction | Evidential use | Evidence effect | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P2-I1-REG-INHERITED` | `P2-I1-C00` | Inherited-source verification | `registration-manifest.json` | Exact | Method and scope boundary | `registration-only` | Retained |
| `P2-I1-REG-RUNTIME` | `P2-I1-C00` | Runtime binding receipt | `registration-manifest.json` | Exact | Native operation conformance | `registration-only` | Retained |
| `P2-I1-REG-BASELINE` | `P2-I1-C00` | W0 baseline registry | `registration-manifest.json` | Exact | Initial geometry and isolation identity | `registration-only` | Retained |
| `P2-I1-REG-FREEZE` | `P2-I1-C00` | Registration freeze | `registration-manifest.json` | Exact at declared paths | Control lifecycle and claim closure | `registration-only` | Retained |
| `P2-I1-REG-MANIFEST` | `P2-I1-C00` | Resolved manifest | `rcae-p2-i1-registration-manifest-v1` | Exact at declared paths | Retention and reconstruction index | `reconstruction` | Retained |

Allowed evidence effects are `method`, `resolution-only`, `registration-only`,
`positive`, `negative`, `control`, `reconstruction`, and `interpretation`.

Phase 1 fixtures and validation outputs are infrastructure references only and
must not be entered as P2-I1 scientific evidence.

## 17. Review R3 handoff

R3 occurs after the first completed lane. For P2-I1 it must review the result
without tuning its conclusion and decide:

- whether the brief and checklist preserved what actually appeared;
- whether calibration provenance and registration evidence were sufficient;
- whether control outcomes resolved without a first-class record;
- whether first-class `lane_registration` or `control_outcome` records are now
  justified by concrete use;
- whether checklist growth improved discrimination or drifted toward a desired
  answer;
- whether the L01 boundary against L02–L07 remained clear; and
- whether to continue, redirect, revise, redescribe, or stop.

## 18. Current next actions

1. [x] Review and accept the P2-I1 brief.
2. [x] Pass `P2-I1-THEORY-GATE` while preserving open research questions.
3. [x] Freeze the response, orientation, opportunity, normalization, windows,
   realization, Policy A selectivity boundary, analysis identity, and
   matched-null inputs; pass `P2-I1-CAL-PRE-GATE`.
4. [x] Run candidate-blind calibration and pass `P2-I1-CAL-GATE`.
5. [x] Complete the D-020 bounded v2 identity/calibration refresh.
6. [x] Materialize the exact L01 registration evidence bundle and pass
   `P2-I1-REG-GATE` before any candidate execution.
7. [ ] Freeze one exact candidate cycle and pass `P2-I1-EXEC-FREEZE` before
   its first operation.
