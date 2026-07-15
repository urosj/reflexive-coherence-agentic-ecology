# P2-I2-I03B History-Carried Realization and Operational-Hypothesis Freeze

**Iteration:** `P2-I2-I03B` / checklist section 8B

**Status:** review-ready; design frozen and bounded runtime conformance passed

**Dependence mode:** `history_carried`

**Realization class:** `minimally_producer_assisted`

**Evidence effect:** causal-design authority plus quarantined realization
implementation-conformance only; no calibration, candidate/control outcome,
L02 support result, or terminal class

**Review boundary:** owner review is required before I03C. I03C and I04 remain
unauthorized.

## 1. Entry and activity boundary

I03B began only after the project owner accepted I03A/I03AR1 for staged
progression and directed the work to 8B. The checklist and operational
hypothesis were updated before source comparison. The immutable
[I03B design input freeze](../contracts/p2-i2/i03b-history-carried-realization-freeze-input.json),
SHA-256 `1d1ab37502b9138c5c98b3048bd854ac7ed17d5775c9fd34ad8475608a0bcc7f`,
binds RCAE entry revision `c13ccb74d3ddc7c6f8f3870a15e17e024c9200dd`,
clean graph revision `83e3a300426631ee4df71b661b67d4fcfdfed594`,
twenty admitted source IDs, the nine comparison questions, the three ordered
candidate dispositions, and a zero-runtime design policy.

I03A/I03AR1 artifacts were used only as fixed earlier-mode/governance
provenance. Their observed fixture values and branches did not select any
I03B carrier, intervention, value, or response.

No history-carried model was instantiated. No candidate, cell, control,
calibration, response, or conformance operation ran during this design phase.

## 2. Native-first comparison

PyGRC provides important native components:

- `LGRC9V3RuntimeState` owns the ordered packet ledger,
  `causal_pulse_substrate_surface_log`, native producer configuration, and
  scheduler state;
- committed packet events emit route-local contact rows with amount, physical
  endpoints, channel, event order, and time;
- the runtime artifact and those logs participate in native snapshot/load and
  restoration identity; and
- native feedback/producer/packet operations can own the later response.

Those components do not natively satisfy the history-carried discriminator:

1. `LGRC9V3CausalPulseSubstrateSurfaceRow` is explicitly passive evidence; a
   row does not update an active carrier.
2. `emit_feedback_eligibility_surface_row()` derives from only the latest
   route-local contact and current node coherence. It does not fold two or
   more registered contribution rows into common causal history.
3. The native feedback producer reads the latest feedback row. Its optional
   `expected_source_surface_digest` compares one configured source-row digest,
   not an independently intervenable, source-independent history. Treating
   that digest as authorization would make exact event/route identity a
   controller key.
4. LGRC-0 causal-history artifacts are documented and implemented as derived,
   annotation-only, and non-mutating.
5. No admitted public native method provides a history-only reorder/clamp
   while preserving contribution audit and encounter state.

The `pygrc_native_candidate` is therefore inadequate for 8B. The bounded
producer-assisted option is adequate in design and is selected ahead of a
missing-prerequisite disposition.

## 3. Selected realization

The complete authority is the
[I03B realization/discriminator contract](../contracts/p2-i2/i03b-history-carried-realization-and-discriminator-contract.json),
SHA-256 `8fc575089017c0e429f04bb221092493634bba4a6adcd4fc22ca36a5b238c38d`.

```text
S1 --native contribution q1-->
                                P -- matched encounter state, not read by V
S2 --native contribution q2-->

admitted native arrival rows
  -> RCAEActiveHistoryAdapterV1
  -> one ordered active history H_P
  -> deterministic order-sensitive readout R_H
  -> public native balancing packets
  -> native materialized readout node M_H
  -> native feedback mask(M_H, B_ref)
  -> model-owned producer
  -> later native A-to-B packet
```

`H_P` is one common ordered token tuple. It has no contributor-private slots
and stores no source node, lineage, packet/event ID, row digest, contributor
count, or success label as causal token data. Native source/route identity may
be used only to admit registered arrival-to-P rows and enforce exactly-once
consumption. Native packet/event/surface/lineage state remains the separate
audit projection `L`.

The structural readout is frozen as a source-label-invariant ordered fold:

```text
r_0 = 0
r_(j+1) = lambda * r_j + typed_amount_j
0 < lambda < 1
```

This freezes order sensitivity without choosing scientific values. I04/I06
remain responsible for scientific numeric values. I03B conformance must bind
its own fixture-only coefficient, token values, and native threshold in a
separate immutable freeze; those values cannot become calibration inputs.

## 4. Minimal producer boundary

`RCAEActiveHistoryAdapterV1` owns only the missing active-history operation:

- append canonical physical tokens to H_P from admitted rows;
- retain an exactly-once cursor/idempotency set;
- perform declared H_P reorder/replacement/clamp interventions;
- calculate the deterministic H_P readout; and
- request public native balancing packets that bring M_H to the readout.

The adapter may read `model.get_state().causal_pulse_substrate_surface_log`
without mutation and may call registered public packet scheduling/step
operations. It may not mutate `LGRC9V3RuntimeState`, node coherence, or
`cached_quantities` directly.

The adapter also may not read response target B, any success/claim field, or
the scientific output; apply the scientific response threshold; emit a
success value; call the feedback/producer path internally; or schedule the
later A-to-B response. It stops after M_H materialization. PyGRC owns every
coherence mutation, feedback-row derivation, threshold/polarity evaluation,
response scheduling decision, and response packet transition.

This separation is what keeps the design producer-assisted rather than a
controller-authored success path. If runtime conformance cannot preserve it,
I03B must stop as `missing_prerequisite`.

## 5. History/state separation and controls

The primary order contrast executes the same physical marginal token multiset
in two orders. Both native contributions reach P before encounter, so final P
is matched. H_P order, its readout, M_H, and the later response relation are
expected to differ under the later frozen measurement rule.

Four complementary interventions are frozen:

- **Active-history clamp:** preserve native contributions, attribution, P,
  support, and opportunity; explicitly replace H_P with reference/candidate
  history and rematerialize M_H. Response must track the clamp.
- **State-only separation:** freeze H_P/M_H, then alter P with a native
  intervention while keeping P outside V's mask. Response must remain
  invariant within the later resolution rule.
- **Pool-write freeze:** preserve source-side native activity but divert
  contributions away from P; the adapter admits no tokens and H_P remains at
  reference.
- **Pure label permutation:** alter only source-lineage strings; H_P, readout,
  M_H, and response remain invariant while audit identity changes honestly.

The private competitor uses separate H1 and H2 adapter instances. Each
legitimate response may read one private readout only. No adapter, mask,
helper, dispatcher, or analysis precursor may concatenate, sum, compare,
choose between, or otherwise jointly read both private histories. Such a path
is mailbox/controller dependence and blocks R04.

The common access witness is one H_P with one M_H output port. Any registered
eligible A-role responder may use the same one-node M_H/B_ref mask and native
policy class; no source address selects the response path.

## 6. Complete logical and operational coverage

All seven cells are mode-bound without rewriting I03A:

| Cell | History-carried role |
| --- | --- |
| `reference-pool` | reference H_P/M_H and contribution-diversion variant |
| `individual-contributions` | S1-only, S2-only, quantity-matched one-source histories |
| `combined-orders` | q1-q2 and q2-q1 in one H_P with matched final P |
| `pooled-history-shuffle` | active order shuffle, pure label permutation, H_P clamp |
| `contributor-removal` | remove/divert either admitted token |
| `global-state-exclusion` | H1/H2 private reads, state-only P contrast, direct/controller bypass |
| `access-capacity-contrast` | alternate eligible responder, same H_P/M_H access class |

All five lane controls retain a target, held-fixed variables, expected
relation, allowed ambiguity, and fail-closed effect. OP-01 through OP-09 bind
joint H_P constitution, history-dependent V, label invariance, H_P
intervention, insufficient repetition, private exclusion, controller
exclusion, history-order divergence, and access-scope retention respectively.
Exact equality/divergence resolution remains I04 work.

## 7. Restoration ownership

Native `lgrc9v3_restoration_identity_v2` covers the complete PyGRC current
runtime, M_H, packet/surface logs, producer configuration, scheduler state,
and valid persisted native reset baseline. It does not cover:

- H_P tokens;
- the consumed-row cursor/idempotency state;
- adapter bindings/readout/materialization configuration;
- last materialized readout and intervention provenance; or
- the adapter reset baseline.

I03B therefore requires a versioned composite identity over the complete
native v2 artifact, complete adapter current identity, complete adapter reset-
baseline identity, and experiment role/intervention binding. Save/load must
persist native and adapter artifacts under one manifest and validate both
before continuation. Reset must call native and adapter reset against their
paired registered baselines, then validate composite identity. One-sided
reset, implicit rebase, and legacy fallback are prohibited.

Runtime conformance must demonstrate original/load/reset composite identity
and equal-input continuation. This remains implementation-conformance only.

## 8. Native gaps retained for synthesis

I03B adds a concrete set of LGRC naturalization demands:

- an active common-history carrier spanning multiple committed contact rows;
- a source-label-free physical history-token schema and ordered reducer;
- public append, reorder, clamp, reset, and intervention-provenance methods;
- a native history-to-feedback readout bridge that does not depend on one
  controller-authored expected row digest;
- common/private history partition identity and no-common-read guards;
- native-plus-ecology composite current/reset identity; and
- generic history capacity, saturation, leakage, depletion, and maintenance
  contracts.

No native primitive or cross-experiment recurrence claim is assigned here.

## 9. Deliberately unresolved

I03B does not select a scientific raw response, orientation, primary
comparator, coefficient, token amount/type/time, native threshold, packet
amount, equality/divergence resolution, null generator, seed, delta, exact
topology, node/edge/carrier ID, or registered matrix. It also does not inspect
or resolve the hybrid realization.

## 10. Static design validation

The retained
[I03B static validator](../scripts/p2_i2_i03b_validate.py) generated the
[machine validation](../contracts/p2-i2/i03b-history-carried-realization-validation.json).
It passed every frozen invariant, including all twenty admitted source
digests, eleven public callables, seven cells, five controls, nine OPs, eleven
capability dispositions, passive/native-history boundaries, producer
minimality, composite restoration duty, no-runtime scope, and an unchanged
clean graph checkout.

The validator instantiated no model and performed no history-carried runtime
operation. It is design/source-dataflow authority only.

## 11. Frozen runtime conformance

The exact
[runtime-conformance freeze](../contracts/p2-i2/i03b-history-carried-runtime-conformance-input-freeze.json),
SHA-256 `dd0146f656f3f480d5ff3265696cacf39322fa5fe13991aed822614eee217720`,
validated without model instantiation before the first runtime call. It bound
the adapter/harness hashes, `.venv`, exact admitted checkout/import and source
digests, twelve branches, fixture-only values, 1e-12 absolute/zero-relative
implementation comparator, one evidence invocation, one reconstruction, zero
retries, and full quarantine.

The single retained
[runtime conformance](../contracts/p2-i2/i03b-history-carried-runtime-conformance.json)
passed `252/252` assertions:

| Conformance boundary | Frozen fixture observation | Meaning |
| --- | --- | --- |
| Order sensitivity | q1-q2 and q2-q1 retained the same marginal multiset and matched P, but H_P readouts were 0.5 and 0.4 and the native response branches differed | the declared ordered history path executed |
| Label invariance | lineage permutation changed native audit assignment while preserving H_P/readout/native response | arbitrary labels were outside the causal token/read path |
| History clamp | clamping H_P to reference preserved P at 1.6, rematerialized M_H to 0, and removed the fixture response | active history was independently intervenable |
| State-only separation | native P debit changed P from 1.6 to 1.3 while H_P/M_H and the fixture response remained | the history path did not silently read P |
| Write diversion | matched source debits reached K_P, no H_P token was admitted, and response remained reference | contribution admission was carrier-specific |
| Private partition | H1/H2 readouts were separately masked; no aggregation occurred and neither private branch produced the candidate fixture response | no mailbox/common-read bypass was used |
| Alternate access | A_alt used the same M_H/B_ref mask and retained the fixture relation | common access was not contributor-addressed |
| Producer ownership | every materialization used native balancing packets; the adapter computed/scheduled no success; the native producer owned later response | the frozen minimal boundary held |

These are conformance fixture observations, not candidate/control/scientific
results. Their amounts, coefficient, threshold, response packet, branch
values, and digests are forbidden I04/I06 inputs.

## 12. Restoration and reconstruction

Paired save/load preserved the complete composite identity. The pre-save and
loaded composite digest was
`4e8ae26852f0ac7cc953fde1e7ffa4bc0d02cee79b93e9d9cfb900d435a451dd`.
Paired native/adapter reset returned both original and loaded branches to the
initial composite digest
`01c5fce9e9da72888101c854c10663eb5831b892e4d55fac6037fac243f32850`.
Equal-input continuation matched after load and again after paired reset.

The sole reconstruction repeated all twelve branches and 252 assertions. Its
SHA-256 matched the retained evidence exactly:
`4465ff2174d285d26ffa8a6cb4bebaf644b150d24bea0d69563eb5f51d8c177d`.
The files were byte-identical. The
[reconstruction receipt](../contracts/p2-i2/i03b-runtime-reconstruction-receipt.json)
records the invocation accounting and claim boundary. The graph checkout
remained clean at the admitted revision.

## 13. Review disposition

`P2-I2-I03B-REVIEW-READY` is satisfied. The minimally producer-assisted
history-carried implementation is runtime-conformant within the frozen
synthetic fixture, pending owner review. This does not establish native
support, scientific support/falsification, effect size, calibration values,
registration values, a mode ranking, or a lane result.

The next governed action is owner review of I03B. I03C and I04 remain
unauthorized and no hybrid analysis has begun.
