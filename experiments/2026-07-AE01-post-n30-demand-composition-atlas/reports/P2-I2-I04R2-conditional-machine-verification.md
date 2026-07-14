# P2-I2 I04-R2 Conditional Machine Verification

**Iteration:** `P2-I2-I04R2`

**Disposition:** owner-accepted under `P2-I2-DEC-026`; sole I04 progression
authority; `P2-I2-CAL-PRE-GATE=passed`

**Evidence effect:** candidate-free machine-preregistration integrity only; no
matched-null, PyGRC model, candidate/control, calibration value, or scientific
result

## Outcome

All eight conditional machine requirements are now confirmed. One substantive
future-I05 path gap was found and corrected: the I04-R1 future calibration
entry point called the normalized-difference function on an already paired
equal response, and reconstruction was named as a downstream duty rather than
forced by that entry point. The I04-R2 entry point instead builds three raw
response envelopes, invokes the same all-or-none strongest-marginal estimator
that future live analysis must use, writes and reads the governed output, and
requires byte-identical JSON reconstruction before successful exit.

The focused [validation](../contracts/p2-i2/i04r2-machine-verification-validation.json)
passed 16/16 checks and 7/7 pure tests. The output reconstructed byte-identically
under the frozen inputs. No accepted I03 or I04-R1 review was replayed.

## Conditional invariants

### Complete two-arm evaluability

For one exact mode/seed/physical-order/pairing/opportunity/window/B-baseline
tuple:

```text
candidate scientific
and leave-q1 scientific
and leave-q2 scientific
  -> comparator = max(leave-q1, leave-q2)

otherwise
  -> comparator = null
  -> primary margin = null
  -> tuple = nonevaluable
```

No arm can be removed, and no maximum can cross a mode, seed, or order. The
predeclared exact-tie rule selects q1-only.

### Exact I05 estimator route

The future I05 path is now:

```text
raw candidate envelope
raw q1-only envelope
raw q2-only envelope
-> p2_i2_i04r2_analysis.primary_margin
-> strongest-arm selection
-> pairing and denominator floor
-> normalized margin
-> serialization
-> retained-output readback and reconstruction
```

The future entry point contains three raw-envelope builder calls and one
`primary_margin` call. It neither accepts a precollapsed comparator nor calls
`normalized_paired_difference` directly. It contains the governed write/read,
parse, reserialize, and byte-equality guard. The null remains arithmetic-only.

### I06 diversion boundary

I06 must match source debit/activity, contribution amount/type, timing slot,
queue opportunity, support/capacity consequences, route cost where relevant,
responder opportunity, B baseline, and response policy. The inert sink must be
absent from P, H_P, M_H, B, B_ref, feedback masks, producer eligibility, and
every continuation-relevant state. Five exact configuration/comparison receipts
are required. Failure blocks that mode's registration; a weaker or surviving-
arm comparator is forbidden.

### Arrival gain and native domain

Exact admitted source inspection confirms the current arrival transition is:

```text
B_after = B_before + packet.amount
```

There is no native arrival clipping, saturation, projection, or correction.
I06 must register a finite closed coherence interval, and both B values must
fall inside it. The analyzer requires:

```text
expected_native_arrival_gain = response_packet_amount
abs(measured_B_gain - expected_native_arrival_gain) <= runtime_tolerance
runtime_tolerance < expected_native_arrival_gain / 1024
arrival_adjustment_event_ids = []
```

A change to native arrival semantics reopens I04 rather than silently changing
the response.

### Window validity before zero

The response envelope now adds exact feedback-evaluation, policy, producer-
invocation, producer-receipt, pre/post queue-identity, step-event, and
contamination receipts. Observed response requires the step IDs to equal the
registered departure then arrival. Scientific zero requires two null step IDs
paired with two explicit empty-queue step kinds. Any contamination or identity
mismatch is operational null.

### Retained semantic rules

- Repeated-S1/S2 equivalence has no primary, top-signature, R03-failure, or
  automatic-lowering effect.
- A non-top order panel does not map directly to operational-hypothesis
  failure; raw orders, OP-08, interventions, mode controls, and causal evidence
  govern classification.
- Candidate/private/controller status remains derived from eight receipt
  sources. Authored booleans and output difference remain non-authoritative.

## Validation and execution boundary

Validation additionally confirmed:

- the conditional review and all ten I04-R1 artifacts remain byte-exact;
- all seven I03 conformance sources remain excluded from the arithmetic null;
- I04-R2 analysis/calibration code imports no PyGRC;
- admitted graph revision `83e3a300426631ee4df71b661b67d4fcfdfed594`
  is clean; and
- no I05 authorization/output, matched-null invocation, PyGRC model,
  candidate/control invocation, or graph mutation occurred.

The validation receipt retains deterministic command/status/count evidence
rather than unittest wall-clock duration. A second validator run reconstructed
the complete retained output byte-identically.

Validation identity:
`637c07cc7d31824f4806459f7b4e8ddd1262eec3c5cc874b009ea7767b59d361`.

## Gate boundary

The project owner explicitly accepted this package under DEC-026 and passed
CAL-PRE. I04R2 is the sole progression authority; original I04 and I04R1 are
immutable historical artifacts and not parallel active preregistrations. This
opens only checklist/hypothesis-first construction of a separately frozen
single I05 arithmetic-null invocation. It does not itself create that freeze,
invoke I05, or open I06, candidate/control execution, R01-R05, L02
interpretation, or mode ranking. The q1-only exact-tie rule is deterministic
provenance only and has no scientific meaning.

Retained gate record:
[I04R2 owner acceptance and CAL-PRE passage](../contracts/p2-i2/i04r2-owner-acceptance-and-cal-pre-gate.json).
