# P2-I2 APP-B3 Implication-Boundary Audit

**Status:** technically complete; owner result review pending; uncommitted

## Disposition

Three critical validations pass. The fourth identifies one real claim boundary:
APP-B2 did not register a quantity- and cardinality-matched repeated-operation
three-admission control.

```text
fail-open correction isolation = passed
exact H_C admission reconciliation = passed
mode-/support-specific claim projection = passed
matched three-admission alternative = absent

APP-B2 proper-subset composition result = retained
operation complementarity = unresolved / not claimed
```

No APP-B2 arm or output was changed or regenerated.

## Cardinality and quantity boundary

The frozen 99-arm registry contains 19 three-admission history rows. Every one
contains the three distinct operations G, E, and P, in GEP or GPE order. There
is no GGG, EEE, PPP, GGE, GPP, or other repeated-operation sequence matched on
cardinality, total quantity, timing, and history length.

Therefore APP-B2 distinguishes GEP from every proper subset but not from a
generic matched three-event alternative. This does not invalidate its bounded
proper-subset irreducibility or composition result. It does block the stronger
phrase `operation complementarity`. A separately frozen repeated-operation
three-admission panel is the highest-priority possible next discriminator; it
was not retrofitted into APP-B2 and is not authorized by this audit.

## Fail-open correction isolation

Source/dataflow and retained process evidence establish:

- The parent completes the fixed 99-row child loop before its only call to the
  analysis function.
- Neither the child worker nor the campaign loop calls the analysis function.
- All 99 frozen rows completed in exact order in 99 unique fresh processes.
- No arm was retried, removed, adaptively selected, or outcome-reclassified.
- The original reconstructor reproduces the embedded analysis byte-identically.
- The corrected closeout is bound to the unchanged retained runtime hash.
- Primary responses, estimator values, and control values are identical before
  and after correction.
- Corrected validity reads native receipts rather than an authored `valid`
  field, and the original embedded terminal is explicitly quarantined.

The defect was therefore purely post-run analysis projection. It did not
affect execution, continuation, scientific-zero acceptance, or later arms.

## Exact active-history reconciliation

Across all 99 retained arms:

```text
expected physical G/E/P admission rows = 123
actual physical G/E/P admission rows = 123
G / E / P admissions = 41 / 41 / 41
unexpected admission rows = 0
duplicate admissions = 0
route/amount/event provenance mismatches = 0

admissions cleared by frozen history interventions = 12
expected final active-history tokens = 111
actual final active-history tokens = 111
final token-provenance mismatches = 0
```

The adapter admits only native arrival surface rows that exactly match one
registered G/E/P source, target, edge, and amount, and refuses duplicate
surface digests. Ingestion occurs only immediately after each of the three
physical operation packets. There is no later ingestion call after history
materialization, history/state intervention, neutral contact, feedback,
response/controller activity, or save/load/reset.

Consequently materialization, neutral, response, controller, diversion,
state-intervention, private-partition, and restoration activity each have zero
admissions. The history path is not recursively self-supporting.

## Correct claim projection

The appendix-wide terminal remains `supported_bounded_candidate`. The strongest
scientific statement is:

> Bounded history-carried P2-I2-grounded three-operation shared-pool
> composition candidate.

```text
support_status = scaffold_dependent

state_carried = not supported in the frozen realization
history_carried = supported bounded composition
hybrid = not supported in the frozen realization
```

The hybrid negative is causal, not operational: its carrier and factorial
discriminator work, but P and GP already reproduce GEP at the registered
response boundary, so E is nonessential. State and hybrid are not claimed
generally impossible.

The supported interpretation is that, in this bounded fixture, carrier
temporality changes the composition structure: E suppresses the state-carried
response, is necessary in active ordered history, and becomes nonessential in
the registered hybrid path. This remains scaffold-dependent because ordered
active-history admission is adapter-owned.

## Execution boundary

APP-B3 used one pure repository `.venv` validator implementation across six
process starts: two check-only starts and four artifact-generation starts. The
first three generated artifacts were superseded uncommitted while the receipt-
predicate and process-ledger checks were tightened; no scientific byte or
disposition changed. All six starts imported no PyGRC, constructed no model,
invoked no producer, and generated no arm or response. Owner result acceptance,
result commit, and any matched-cardinality runtime test remain closed.
