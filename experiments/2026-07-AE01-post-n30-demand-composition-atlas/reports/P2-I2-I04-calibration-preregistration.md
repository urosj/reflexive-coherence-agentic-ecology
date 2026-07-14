# P2-I2 I04 Calibration Preregistration

**Status:** review-ready; `P2-I2-CAL-PRE-GATE` remains pending owner review

**Iteration:** `P2-I2-I04`

**Evidence effect:** candidate-free measurement and calibration authority only;
no matched-null result, candidate result, control outcome, rung, or L02 conclusion

## Outcome

I04 freezes one shared downstream response and analysis identity while retaining
all three causal modes separately:

```text
raw response = native coherence gain at registered response target B
window       = one native feedback-producer evaluation and its response arrival
orientation  = identity; higher is aligned
primary pair = two-source combined constitution
               versus quantity-and-timing-matched one-source repetition
strata       = S1->S2 and S2->S1, separately paired and never averaged
```

This response is shared because all three accepted `V` paths terminate in the
same native A-to-B continuation and receiving-substrate change. Their upstream
causes remain distinct: native P for state-carried, H_P/M_H with P excluded for
history-carried, and P plus H_P/M_H for hybrid.

The repeated-single-source comparator is intentionally demanding. It preserves
the inherited one-source carrier relation and total contribution while removing
multi-source joint constitution. It is therefore nearer than contributor
removal, shuffle, or controller substitution, even when it is likely to yield a
smaller or resolution-limited margin. Outcome magnitude did not select it.

## Measurement and decision boundary

- Each mode has three candidate seeds and two primary order strata, producing
  six preserved primary margins. Every margin must align for the top primary
  signature; one order or seed cannot carry the claim.
- A completed native window with no response is scientific zero. Operational
  failure leaves response null and makes that mode/seed's complete two-order
  panel not evaluable. Nothing is imputed or removed from a denominator.
- Nine common rules and 3/3/5 state/history/hybrid rules translate the accepted
  qualitative expectations into `pass`, `ambiguous`, or `fail`. The hybrid
  package includes the complete qualitative P-by-H_P four-cell factorial but
  imposes no interaction, synergy, or nonlinearity requirement.
- Private and controller substitutions are resolved by causal-chain exclusion,
  not by output inequality alone. All private raw responses remain separate.
- Exact topology, source routes, contribution values/types/times, feedback
  threshold, and response amount remain I06 work and cannot be selected here.

The exact policy is retained in
[p2_i2_analysis_policy.json](../configs/p2_i2_analysis_policy.json); the pure
analysis implementation is [p2_i2_analysis.py](../scripts/p2_i2_analysis.py).

## Candidate-blind calibration preregistration

One shared I05 null is justified because response meaning, unit, orientation,
window, comparator role, aggregation, missingness, and calibration population
are identical across modes. It contains ten equal exact-rational pairs: five
calibration seeds by two order strata. It imports no PyGRC/runtime/candidate
input. Its estimator remains the metric-sheet rule:

```text
delta = max(1e-12, maximum absolute matched-null normalized margin)
```

I04 froze the policy and future entry point but did not invoke them. The entry
point mechanically refuses to run until a future I05 execution freeze records
owner CAL-PRE acceptance, authorizes exactly one null invocation, keeps
candidate execution false, and binds the exact I04 identities. `delta` remains
pending I05. The exact policy is
[p2_i2_calibration_policy.json](../configs/p2_i2_calibration_policy.json).

## Static validation

The retained [validation record](../contracts/p2-i2/i04-calibration-preregistration-validation.json)
passed `16/16` checks and the pure analysis suite passed `10/10` tests. The
validation confirmed:

- exact accepted authorities and I03F baseline;
- three retained unranked modes;
- downstream substrate response, closest comparator, both-order distribution,
  missingness, margin, and control semantics;
- all seven shared-identity equivalence fields;
- the complete I03 fixture quarantine, including absence of null-value,
  branch-ID, and conformance-digest reuse;
- no PyGRC import, model instantiation, matched-null invocation, candidate
  invocation, or graph mutation; and
- an exact clean admitted PyGRC revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594`.

This was a focused CAL-PRE validation, not another review of accepted I03 mode
capability, source dataflow, restoration, or runtime conformance.

## Gate disposition

```text
P2-I2-I04 = REVIEW-READY
P2-I2-CAL-PRE-GATE = pending owner review
P2-I2-I05 = unauthorized
candidate execution = unauthorized
```

Owner acceptance may open only the governed I05 matched-null invocation. Any
change to response, comparator, order strata, analysis, control rules, or null
identity restarts I04/I05; I06 may later bind only the exact implementation
fields explicitly left open by this preregistration.
