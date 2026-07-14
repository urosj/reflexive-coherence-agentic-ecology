# P2-I2-I03C Hybrid Realization and Operational-Hypothesis Freeze

**Iteration:** `P2-I2-I03C` / checklist section 8C

**Status:** review-ready; design frozen, static validation retained, and
bounded runtime conformance passed with byte-identical reconstruction

**Dependence mode:** `hybrid`

**Realization class:** `minimally_producer_assisted`

**Evidence effect:** causal-design/source-dataflow authority plus quarantined
realization implementation-conformance only; no calibration, candidate/control
outcome, L02 support result, mode ranking, or terminal class

**Review boundary:** owner review is required before the umbrella discriminator
gate. Runtime completion does not authorize I04.

## 1. Entry and freeze boundary

I03C began only after the project owner accepted I03B/I03BR1 for staged
progression and directed that 8C was next. Checklist section 8C and the hybrid
operational-hypothesis projection were retained before source comparison.
`P2-I2-DEC-015` opened only design-first I03C.

The immutable
[I03C design input freeze](../contracts/p2-i2/i03c-hybrid-realization-freeze-input.json),
SHA-256 `1d69dedf481aba2ad996388d35e03e65e7a7e5cc39276feaf8d92b730208c353`,
binds RCAE entry revision `9332a67558764043d6f6adf67dc82a19187871db`,
clean graph revision `83e3a300426631ee4df71b661b67d4fcfdfed594`,
twenty admitted source IDs, ten comparison questions, three native-first
candidate dispositions, and zero design-phase runtime operations.

I03A and I03B were used only as immutable earlier-mode causal/governance
boundaries. Their fixture values, branches, comparators, and evidence digests
did not select I03C's realization or any future conformance value.

No hybrid model was instantiated. No candidate, cell, control, calibration,
response, or conformance operation ran during this design phase.

## 2. Native-first source/dataflow comparison

Admitted PyGRC already supplies most of a hybrid path:

- native packets can change common P while preserving exact audit lineage;
- `emit_feedback_eligibility_surface_row()` accepts a multi-node front mask
  and sums the live coherence of every front node;
- a front mask `[P, M_H]` against `[B_ref]` therefore gives one native joint
  state/history-output read without a contributor address;
- the native feedback producer owns polarity/threshold evaluation, response
  scheduling, idempotency, and the later packet transition; and
- native restoration identity v2 covers P, M_H, response configuration,
  scheduler/log state, and the persisted native reset baseline.

Complete native hybrid realization is still inadequate. Native contact rows
are passive evidence; feedback uses the latest contact plus live node state,
not an independently intervenable multi-event history fold. LGRC-0 history
artifacts are annotation-only. No admitted public native method appends,
reorders, clamps, or resets one active common history independently of P, and
native identity cannot include ecology-owned history by itself.

The minimally producer-assisted option is therefore selected ahead of
`missing_prerequisite`. The native gap is active history, not joint live-state
feedback.

## 3. Frozen hybrid factorization

The complete authority is the
[I03C realization/discriminator contract](../contracts/p2-i2/i03c-hybrid-realization-and-discriminator-contract.json),
SHA-256 `eed0a4a84fbcf3da35c222347d3dd913d6dd5bc8bc8e4906e0fb8eea5d1e3fc8`.

```text
S1, S2 -- native physical contributions --> P = causal state component
             same admitted rows
                    |
                    v
          RCAEActiveHistoryAdapterV1
          -> one source-label-free ordered H_P
          -> deterministic R_H(H_P)
          -> public native balancing packets -> M_H

common neutral contact after final interventions
  -> native feedback front [P, M_H], rear [B_ref]
  -> native score/polarity/threshold/producer
  -> later native A-to-B packet
```

The same physical admitted contribution advances native P and supplies one
canonical H_P token. Source/node/lineage IDs, packet/event/surface digests,
contributor count, and success labels never enter the token or joint response.
They remain audit or admission/idempotency fields only.

The hybrid family is `J(C_P,R_H) = C_P + R_H` at the native live-state mask.
Nonlinearity is not required, but both components must be functionally causal
in the same response. Exact scientific parameters and response resolution are
deferred to I04/I06.

## 4. Minimal producer and native ownership

The exact existing `RCAEActiveHistoryAdapterV1` structural implementation is
reused without importing its I03B fixture values. It owns only:

- the ordered H_P token tuple and its cursor/idempotency state;
- declared history append/reorder/replacement/clamp operations;
- the source-label-invariant deterministic R_H fold; and
- public-packet requests that materialize R_H at native M_H.

The adapter may not read P as a success input, calculate P+M_H, apply the
response threshold, emit feedback, configure or call the producer, schedule
A-to-B, read B/success/scientific fields, or directly mutate native state.
It stops after M_H materialization. PyGRC owns every coherence mutation and
the complete joint response transition. Any required widening reclassifies
the realization as `missing_prerequisite`.

## 5. Hybrid discriminators and controls

The design freezes both component interventions against the same joint path:

- a native P-only debit changes P while H_P/R_H/M_H remain fixed;
- an H_P-only replacement or clamp and rematerialization changes H_P/R_H/M_H
  while P remains fixed; and
- the fully constituted branch is compared with both one-component variants,
  requiring each intervention to affect the same native joint response under
  the later frozen resolution.

History-order reversal preserves marginal tokens and final P while allowing
H_P/R_H/M_H and the response to differ. Pure label permutation may change
audit identity only. Write diversion preserves source debits but prevents
both P accumulation and H_P admission. A common neutral contact follows every
final intervention, while `expected_source_surface_digest` remains null.

The private competitor has P1/H1 and P2/H2 with separate native nodes and
adapter instances. Each legitimate response sees one private pair only; no
shared reducer, mask, dispatcher, or analysis precursor may combine them. An
alternate eligible responder may use the same common `[P,M_H]/[B_ref]` mask.

All seven logical cells, five L02 controls, and OP-01 through OP-09 are bound
without rewriting the accepted state-carried or history-carried profiles.

## 6. Restoration and carried obligations

Native restoration identity v2 covers the complete graph current/reset state.
The external identity must additionally cover H_P, cursor/idempotency,
adapter configuration/code identity, last readout/materialization,
intervention provenance, and adapter reset baseline. One canonical composite
digest binds both layers plus P/H_P/M_H roles, `[P,M_H]/[B_ref]` masks,
private/common partition, admission/lifecycle rules, and fixture identity.

Save/load and reset must be registered paired procedures. One-sided reset,
implicit rebase, and continuation before complete manifest/hash validation are
forbidden. Original/load/reset branches must receive equal adapter and native
continuation inputs.

I03C carries all six I03BR1 downstream obligations: unique admission route or
explicit route key, later scientific access resolution, bounded lifecycle and
event counts, manifest-validating paired restoration, branch isolation, and
mechanical rejection of every conformance fixture value/digest from I04/I06.

## 7. Static validation and next boundary

The retained
[I03C static validator](../scripts/p2_i2_i03c_validate.py) generated the
[machine validation](../contracts/p2-i2/i03c-hybrid-realization-validation.json).
It validates the freeze/prior/source identities, multi-node native joint read,
passive-history limitation, minimal adapter boundary, seven cells, five
controls, nine OPs, separate interventions, layered restoration, six carried
obligations, zero-runtime policy, and unchanged clean graph checkout.

The validator instantiated no model and performed no hybrid runtime operation.
It authorized only construction and validation of the separate exact runtime-
conformance freeze under DEC-012/DEC-016. I04 remained blocked.

## 8. Frozen runtime conformance

The exact
[runtime-conformance freeze](../contracts/p2-i2/i03c-hybrid-runtime-conformance-input-freeze.json),
SHA-256 `e19be7110597252517f3531a1eddb82dc2e5fdf9a16fcb1c07ec1b9921ed6f5d`,
validated before the first model instantiation. It binds the RCAE `.venv`,
admitted checkout/source digests, exact I03C harness, unchanged structural
adapter, twelve branches, one evidence invocation, one reconstruction, zero
retries, and no search or rescue variants.

Its values are new fixture-only inputs: contributions `0.17` and `0.31`,
ordered-fold coefficient `0.65`, native joint threshold `0.88`, and response
packet `0.073`. Exact serialized I03A/I03B fixture signatures and evidence
digests are mechanically rejected. All I03C values and observations are in
turn prohibited I04/I06 inputs.

The single retained
[runtime conformance](../contracts/p2-i2/i03c-hybrid-runtime-conformance.json),
SHA-256 `217c8972e8e1199409343fb72b0eca12b2ba24dceb6a1f213c97af9143f0e96c`,
passed `258/258` frozen assertions:

| Boundary | Frozen fixture observation | Conformance meaning |
| --- | --- | --- |
| Joint hybrid path | P=`0.48`, M_H=`0.4205`, native `[P,M_H]` score=`0.9005`; native response scheduled | one native response read both components exactly once |
| P-only intervention | H_P/M_H remained `[0.17,0.31]`/`0.4205`; P fell to `0.32`, score to `0.7405`, response absent | native state independently affected the same joint path |
| H-only intervention | P remained `0.48`; H_P was explicitly clamped empty, M_H became `0`, score `0.48`, response absent | active history independently affected the same joint path |
| History order | reverse order preserved P=`0.48` and token multiset but changed M_H to `0.3715`, score to `0.8515`, and removed response | ordered history remained causal alongside native state |
| Label invariance | arbitrary source-lineage permutation changed audit assignment but not P/H_P/M_H/score/response | lineage remained outside the causal token and response |
| Write diversion | source debits were preserved while P and H_P/M_H remained at reference | both components depended on registered common writes |
| Private partition | two responses read only `[P1,M_H1]` and `[P2,M_H2]`; scores `0.34/0.62`, no aggregation or response | no common/private mailbox bypass occurred |
| Alternate access | A_alt used the same `[P,M_H]/[B_ref]` mask and retained the joint relation | access was common and not contributor-addressed |
| Ownership | adapter materialized M_H through native packets and computed no joint score/success; native producer scheduled the later packet | the minimal producer boundary held |

Every feedback row used the final common neutral contact and retained
`expected_source_surface_digest=null`. PyGRC remained the sole owner of
joint-score/threshold evaluation, response scheduling, and coherence
transition.

These observations are implementation-conformance evidence only. They do not
select the scientific response, comparator, resolution, parameter values,
topology, seed, or any R01-R05 outcome.

## 9. Restoration, reconstruction, and disposition

Paired native/adapter save-load preserved composite digest
`c1ff77baa3a6b9ec5ab917f431546a5923a024325a80e7cfa8090c893c6e5f8a`.
Paired reset returned original and loaded branches to initial composite digest
`6e673a89a73e40babe588c63c96eee8fccaa7e24c698e0ea187b0fcc786bed99`.
Equal post-reset inputs then produced matching continuation digest
`1401f981ea967542f752aab6f302bb96afa5b2487ff6cfd19864ca0b8d47d2f6`.
The paired manifest was validated before continuation; no one-sided reset or
implicit rebase occurred.

The sole reconstruction repeated all twelve branches and `258/258`
assertions. Its SHA-256 matched the evidence exactly and the files were byte-
identical. The
[reconstruction receipt](../contracts/p2-i2/i03c-runtime-reconstruction-receipt.json)
retains invocation accounting and restoration witnesses. The admitted graph
checkout remained clean and unchanged.

I03C is therefore `runtime_conformant` for the bounded minimally producer-
assisted hybrid realization and is review-ready. This does not pass the
umbrella discriminator gate or authorize I04. Owner acceptance, revision, or
an explicit earlier-stop disposition is required next.
