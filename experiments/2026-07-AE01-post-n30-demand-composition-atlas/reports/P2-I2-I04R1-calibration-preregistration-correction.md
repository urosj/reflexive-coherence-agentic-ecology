# P2-I2 I04-R1 Calibration-Preregistration Correction

**Iteration:** `P2-I2-I04R1`

**Disposition:** `P2-I2-I04-REVIEW-READY` pending explicit project-owner
acceptance

**Evidence effect:** corrected candidate-free measurement and calibration
authority only; no null, runtime, candidate/control, R01-R05, or L02 result

## Outcome

The critical-review blocker is resolved. The original I04 package remains
byte-exact historical evidence but is superseded for progression. The corrected
[preregistration](../contracts/p2-i2/i04r1-calibration-preregistration.json)
uses a carrier-changing primary comparator and restores quantity-matched
single-source repetition to its accepted scope-diagnostic role.

```text
candidate:
  q1 and q2 both enter the registered common carrier

primary comparator:
  max(
    response when q1 enters and q2 is activity-matched/diverted,
    response when q2 enters and q1 is activity-matched/diverted
  )

scope diagnostic:
  repeated-S1 and repeated-S2, each in q1->q2 and q2->q1 physical orders
  complete-carrier equivalence is allowed and cannot alone fail R03
```

Both leave-one branches remain raw. The maximum is a predeclared strongest-
marginal rule, not an outcome-selected arm. Source debit/activity, contribution
properties, timing, support, opportunity, response policy, and B baseline must
be matched; only common-carrier admission versus inert-sink diversion differs.

## Answers to the four load-bearing questions

1. A quantity-matched repeated source cannot be required to diverge when it
   preserves the complete source-label-free carrier. It is now a symmetric,
   mandatory scope diagnostic. Numerical equivalence has no automatic R03
   effect.
2. Future I05 `analysis_arithmetic_delta` calibrates exact-rational parsing,
   float conversion, normalized-margin arithmetic, serialization, and byte
   reconstruction only. It supplies no PyGRC, B-measurement, restoration, or
   continuation tolerance.
3. The response window has six outcome-independent slots: capture `B_before`,
   emit one feedback row, run the producer once, step twice, then capture
   `B_after` and lineage. Scheduled response must process departure then
   arrival; unscheduled/native block must process two empty-queue steps.
4. B may change only through the one registered response arrival. Registration
   requires matched B baselines, empty packet/birth queues, no B causal route,
   background update, balancing operation, topology integration, or unrelated
   B-targeting event. Any violation is operational null, not scientific zero.

The response is therefore explicitly binary-like: zero or one fixed registered
packet amount. It measures native response scheduling and arrival occurrence,
not a graded magnitude.

## Order, mode, and causal-control boundaries

Each mode retains three seeds by two physical orders. The top aligned signature
requires both three-seed order panels to be robustly aligned, but failure of
that signature is not itself a mode-hypothesis failure. History and hybrid may
retain an `order_conditioned_or_mixed` relation when OP-08 passes. Carrier-chain
and mandatory-control evidence, not the metric panel alone, decides causal
failure.

Shared identity covers response unit, fixed window, orientation, extraction,
pure analysis, and the analysis-arithmetic null. Primary margins, scope
diagnostics, controls, metric relation, support, R01-R05, and completeness
remain independently mode-indexed. Cross-mode pooling, averaging,
compensation, and dropping are forbidden.

The corrected pure analyzer derives candidate, private, and controller status
from actual masks, source arrivals, call provenance, producer/packet event
lineage, branch configuration, runtime-binding receipt, and call-trace
identities. It rejects authored causal-summary booleans as authority. Output
inequality alone proves no causal chain.

The corrected policy also retains the complete 9 common plus 3/3/5 state,
history, and hybrid machine-rule registry. Only the two necessary common roles
change: symmetric leave-one owns the primary relation, while quantity-matched
repetition becomes `scope_diagnostic`. No imported control was dropped.

## Numerical and execution boundary

I06 may register an exact response amount `r` only when:

```text
r >= 1024 * 1e-12
r >= 1024 * max(ulp(B_before), ulp(B_before + r))
runtime/restoration/continuation tolerance < r / 1024
```

`B_before`, `r`, and their sum must remain finite, canonical-JSON
round-trippable, and produce a positive recomputed gain. Runtime tolerances are
separate registrations and cannot be inferred from `analysis_arithmetic_delta`.

The future [calibration policy](../configs/p2_i2_i04r1_calibration_policy.json)
and entry point remain mechanically closed until an I05 freeze binds explicit
owner acceptance and the exact corrected identities. I04-R1 executed no null,
PyGRC model, candidate, or control.

## Focused validation

The [validation record](../contracts/p2-i2/i04r1-calibration-preregistration-validation.json)
passed 19/19 correction checks and the corrected pure analysis suite passed
15/15 tests. It additionally confirmed:

- all ten original I04 artifacts remain byte-exact history;
- all three modes remain retained and unranked;
- admitted public PyGRC source identities and the graph checkout are exact;
- all seven I03 conformance sources remain quarantined from scientific/null
  inputs;
- rationale reconstructs from accepted theory, pre-runtime causal contracts,
  and admitted public source semantics, without conformance observations; and
- no I05 authorization/output, PyGRC import/model, candidate/control
  invocation, or graph mutation exists.

Validation identity: `ba9e0bb8003f6f69ca21201db380de33f453f0f3a9c9107279413c798b73efa3`.

## Gate boundary

This package is ready for owner review. It does not pass
`P2-I2-CAL-PRE-GATE` by itself. Owner acceptance may authorize only the
checklist- and hypothesis-first I05 matched-null calibration. I06 registration,
I07 cycle authorization, I08 execution, R01-R05 assignment, mode ranking, and
L02 interpretation remain closed.
