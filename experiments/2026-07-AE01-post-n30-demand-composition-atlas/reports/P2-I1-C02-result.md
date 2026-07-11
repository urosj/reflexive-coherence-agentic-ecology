# P2-I1 C02 Result and Interpretation

**Status:** complete validated result; owner interpretation accepted; retention
pending

**Lane:** `AE01-L01`

**Cycle:** `P2-I1-C02`

**Terminal recommendation:** `supported_bounded_candidate`

**Highest valid rung:** `AE01-L01-R05`

**Support status:** `explicit_constructed_support`

**Claim ceiling:** bounded niche-conditioning demand pattern

## 1. Outcome

C02 completed all 21 frozen primary runs with zero operational failures and
zero retries. All twelve structural obligations passed. Reconstruction and the
retained manifest resolve every registered cell/seed without fallback, graph
write, source drift, worker reuse, branch carryover, or missing evidence.

The observed response panels are seed-invariant:

| Cell | Response panel for each seed | Formation fraction | Interpretation role |
| --- | --- | --- | --- |
| `reference` | `[0,0,0,0]` | `0.0` | No later formation at reference feedback magnitude |
| `candidate-conditioning` | `[1,0,1,0]` | `0.5` | Aligned profiles form; inverted profiles do not |
| `medium-freeze-withdrawal` | `[0,0,0,0]` | `0.0` | Removing the feedback-medium row removes formation |
| `trace-shuffle` | `[0,0,0,0]` | `0.0` | Preserving row content but changing expected source order removes formation |
| `parent-context-contrast` | `[1,0,1,0]` | `0.5` | The relation survives the declared support-scale contrast |
| `susceptibility-inversion` | `[0,1,0,1]` | `0.5` | Local compatibility reverses which profiles form |
| `carrier-timescale-contrast` | `[1,0,1,0]` | `0.5` | The relation survives the frozen reader carrier-load contrast |

Each row above repeats exactly for seeds `101`, `211`, and `307`.

## 2. Metric and selectivity interpretation

Candidate formation is `0.5` and matched reference formation is `0.0` for
every seed. The frozen normalized-margin equation therefore yields:

```text
seed 101 = 1.0
seed 211 = 1.0
seed 307 = 1.0
delta = 1e-12
relation = robust_aligned
threshold_passed = true
```

Medium dependency has the same per-seed margins against the preserved-
opportunity freeze cell. This is a causal diagnostic, not a second primary
metric.

Selectivity does not use calibrated delta. In contexts A and B, for every
seed, the matched interaction is:

```text
(aligned candidate - aligned freeze)
- (inverted candidate - inverted freeze)
= (1 - 0) - (0 - 0)
= 1
```

The mean selectivity margin is `1.0`, classified
`strong_constructed_selectivity`. This distinguishes the result from generic
environmental improvement: the same medium history admits aligned profiles and
rejects inverted profiles, while susceptibility inversion reverses that
relation.

Threshold crossing alone does not select the result. The terminal
recommendation depends on the complete control and rung interpretation below.

## 3. Boundary ladder

| Rung | Status | Evidence meaning |
| --- | --- | --- |
| `AE01-L01-R01` — auditable medium history | Reached | Writer contact and feedback history are attributable and reconstruct independently without participant labels |
| `AE01-L01-R02` — later formation/susceptibility sign | Reached | Candidate later formation exceeds reference for every seed |
| `AE01-L01-R03` — medium-history-specific function | Reached | Preserved-opportunity medium freeze removes formation; selectivity is strong |
| `AE01-L01-R04` — withdrawal/source specificity | Reached | Withdrawal and the single-axis source-order shuffle both remove formation |
| `AE01-L01-R05` — carrier/timescale variation | Reached | The frozen reader-load contrast retains the selective response panel |

R05 is a limited contrast result. It does not establish general transfer or
upgrade the support to native expression.

The owner accepts R05 specifically as **bounded invariance to doubled carrier
load**. It is not timescale-persistence or broad-transfer evidence. Evidence:
[owner closeout review](P2-I1-closeout-review.md).

## 4. Geometric interpretation

The registered geometry remains `P-W-A-B`:

```text
P writes one native packet history into W
W retains an arrival-derived feedback eligibility surface
A and B are later reader profiles with different local compatibility
```

The result is not explained by the existence of W alone. It requires the
ordered relation between writer arrival contact, feedback-medium lineage, and
the later producer expectation:

- no emitted feedback row produces no formation;
- the same row content with shuffled expected source order produces no
  formation;
- aligned and inverted local profiles respond differently to the same retained
  medium history; and
- inverting local susceptibility reverses the profile response.

Thus the geometric object is a participant-written, lineage-sensitive,
non-private conditioning surface that changes later local possibility. It is
not merely an environment value, persistent trace, or global favorable state.

## 5. Agentic-ecology interpretation

What appeared is a bounded niche-conditioning relation:

> An attributable history produced through one participant changes which later
> local differentiations can form through a non-private shared medium, and the
> change depends on medium presence, source order, and reader susceptibility.

This reaches the L01 maximum because the relation survives the frozen
carrier-load contrast. It remains an explicitly constructed ecology-side
mechanism. The experiment configured the feedback surface, producer, profiles,
and support context; it did not observe endogenous niche formation or an
autonomous ecology.

The corresponding LGRC demand pattern is:

```text
attributable participant history
-> reconstructable non-private medium state
-> source/order-sensitive eligibility
-> selective later local formation
```

Future LGRC work seeking more native niche formation would need this relation
to arise, persist, be accessed, and possibly be maintained with less external
construction. That is a graph-side demand implication, not evidence that LGRC
already supplies a native niche abstraction.

The separately validated
[requirement extraction](../contracts/p2-i1/c02/requirement-extraction.json)
records this as an `apparently_adequate` building-block demand with
`pending_synthesis` ranking eligibility. Its three evidence roles remain
distinct: observed AE01 result, constructed ecology mechanism, and ecology
interpretation.

## 6. Becoming and development readings

The becoming reading is that selective later possibility genuinely appeared,
consistently across seeds and controls, at R05 under explicit constructed
support. The live boundary is not whether the local margin can be made larger;
it is whether comparable function recurs independently, supports multiple
writers, broadens transfer, or becomes less scaffold-dependent.

The development reading is to retain the implementation and stop local L01
patching. The result has `T3_operational_class` value: it defines a reusable
writer-medium-reader probe, reconstruction boundary, and causal-control suite.
Other lanes may reuse that method structure, but not these outcomes, margins,
delta, fixture bounds, or terminal classification.

The next move is therefore `retain_current_implementation`. P2-I1 closes at its
bounded claim ceiling; later lanes proceed independently, and P2-I8 may assess
cross-lane recurrence. Any renewed L01 naturalization or broader-transfer probe
requires a new preregistration.

## 7. Terminal disposition

The frozen decision procedure selects `supported_bounded_candidate` because:

- execution and reconstruction completed;
- every mandatory comparison and structural obligation passed;
- the primary relation is robust aligned for all seeds;
- medium withdrawal, source shuffle, selectivity, inversion, parent, and
  carrier-load controls resolve coherently; and
- the interpretation remains within explicit constructed support and the
  frozen maximum claim.

The result does not support native niche formation, multi-source
co-conditioning, autonomous shared access, coordination, agency, organism,
motif, regime, life, general transfer, or N31+ selection.

## 8. C01-to-C02 implementation record

C01 failed before producer invocation because RCAE compared the entire native
snapshot across save/load. PyGRC preserved the LGRC runtime artifact but
normalized nested cached GRC9V3 representation. C01 remained retained as
bounded incomplete with its retry scope exhausted.

C02 implemented accepted D-027 locally in RCAE:

- restoration equality covers outer geometry, exact LGRC runtime state,
  events, and observables;
- the full raw before/after snapshot digests remain retained;
- medium reconstruction remains a separate equality;
- each opportunity runs an independent continuation twin;
- scientific producer invocations and integrity-twin invocations are reported
  separately; and
- any projected-state or continuation drift fails closed.

All 84 opportunities record unequal full raw snapshots, equal restoration
projections, and equal independent continuations. The correction required no
PyGRC change, state injection, fallback, or graph write.

## 9. Reproduction

Validate the tracked freeze, rebuild the audit and execution manifest, rebuild
the scientific analysis, and validate authored closeout records with:

```bash
.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py \
  validate-exec-freeze \
  --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/exec-freeze.json \
  --require-tracked

.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py \
  build-cycle-audit \
  --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/exec-freeze.json \
  --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/cycle-audit.json

.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_execution.py \
  build-execution-manifest \
  --exec-freeze experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/exec-freeze.json \
  --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/execution-manifest.json

.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_closeout.py \
  build-analysis \
  --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/scientific-analysis.json

.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_closeout.py \
  validate-closeout \
  --analysis experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/scientific-analysis.json \
  --developmental experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/developmental-interpretation.json \
  --terminal experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/terminal-classification.json \
  --requirement experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/requirement-extraction.json \
  --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/closeout-validation.json

.venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_closeout.py \
  build-closeout-manifest \
  --analysis experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/scientific-analysis.json \
  --developmental experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/developmental-interpretation.json \
  --terminal experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/terminal-classification.json \
  --requirement experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/requirement-extraction.json \
  --validation experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/closeout-validation.json \
  --report experiments/2026-07-AE01-post-n30-demand-composition-atlas/reports/P2-I1-C02-result.md \
  --review experiments/2026-07-AE01-post-n30-demand-composition-atlas/reports/P2-I1-closeout-review.md \
  --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/c02/closeout-manifest.json
```

Machine artifact canonical digests:

```text
retry ledger       75231be9d8cef69368bb1c9ef1967c19638e007b24557d81e99d607c4c2137d2
cycle audit        8a535c6af06c96e1c93be9e6f3ef31a05af081f0fc14711388de9a937e6503ed
execution manifest c00252f235fb054624acf6d29c0be2df4f759b2eb63f14b3fdd7a59a78bb0dbb
scientific analysis df72d8e5813f7fdd159974dc23812af04c4f6697b7dcf645a11443b8e7e9fb38
```
