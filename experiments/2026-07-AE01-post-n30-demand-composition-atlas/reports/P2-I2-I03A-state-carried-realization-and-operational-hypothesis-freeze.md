# P2-I2-I03A State-Carried Realization and Operational-Hypothesis Freeze

**Iteration:** `P2-I2-I03A` / checklist section 8A

**Status:** review-ready; stop before I03B

**Dependence mode:** `state_carried`

**Realization class:** `pygrc_native_candidate`

**Evidence effect:** causal preregistration authority only; no calibration,
candidate execution, control outcome, L02 support result, or terminal class

**Owner-review boundary:** I03B history-carried work is unauthorized until the
project owner reviews and accepts or revises this I03A package.

## 1. Entry and scope

I03A ran under the
[state-carried input freeze](../contracts/p2-i2/i03a-state-carried-realization-freeze-input.json),
SHA-256 `34d0903c746fb67abff5a1c12bb252b5cb15933d2de75e56f1232fbe7dfd0845`.
Its fifteen entry-artifact digests match RCAE revision
`26811d395c0662473629d5710983e3c1fdb4f58f`; all twelve state-carried review
questions validated. The admitted graph revision is
`83e3a300426631ee4df71b661b67d4fcfdfed594`, and its worktree remained clean.

The project owner directed I03 to proceed sequentially:

```text
8A state_carried -> owner review
8B history_carried -> owner review
8C hybrid -> owner review
```

That direction arrived after the generic I03 freeze validated but before a
realization was compared or selected. `P2-I2-CHG-007` therefore narrowed this
iteration to state-carried work without undoing a scientific choice. This
report does not inspect or resolve history-carried or hybrid realizations.

## 2. Selected bounded realization

I03A selects a native candidate centered on one PyGRC node-coherence carrier:

```text
S1 --native packet q1--> P
S2 --native packet q2--> P
                           |
                           v
             encounter-time P.coherence = C_P
                           |
                           v
       native feedback state read + model-owned producer
                           |
                           v
                 later native packet opportunity
```

The exact topology, node IDs, amounts, times, thresholds, and raw response are
not selected here. I03A binds their causal roles and public interfaces; I04
owns response/comparator/numerical measurement and I06 owns exact fixture and
registration identity.

The complete machine-readable authority is the
[I03A realization/discriminator contract](../contracts/p2-i2/i03a-state-carried-realization-and-discriminator-contract.json),
SHA-256 `aab25571bb5faa71c3213d3c1a27fa5659c3d4d2427a9b3fad8d087df71cc473`.
The subordinate
[operational-hypothesis artifact](../hypotheses/p2-i2-operational-hypotheses.md)
retains the human-readable state-carried projection, SHA-256
`17d4db4af7d5a91814a88c2109b00df86d08a163e7918acba94d83f0bcb780f4`
at I03A freeze construction.

## 3. Why the realization is native

Every causal transition is an admitted public PyGRC operation:

| Causal role | Public native surface | I03A use |
| --- | --- | --- |
| Common carrier | `GRC9V3NodeState.coherence` | one scalar at role P |
| Attributable write | `LGRC9V3.schedule_packet_departure()` | S1 and S2 schedule positive q into P |
| Carrier update | `LGRC9V3.step()` packet departure/arrival | debit source and add amount to P |
| State read | `LGRC9V3.emit_feedback_eligibility_surface_row()` | front mask P, held-fixed rear reference B_ref |
| Native response policy | `LGRC9V3.set_feedback_coupled_pulse_producer()` | serialized state-derived response configuration |
| Later transition | `LGRC9V3.produce_events()` then `step()` | model-owned scheduling and packet processing |
| State intervention | native packet diversion and P-to-K debit | prevent P write or alter P before encounter |
| Branch identity proposal | `lgrc9v3_restoration_identity_v2()` and digest | current state plus persisted reset baseline |

RCAE supplies experiment orchestration: role/access declarations, registered
call order, branch pairing, intervention identity, and the private-control
guard. It does not compute the pool state, inspect source records to reduce a
pool, write an external causal pool, or author a success value. The native
feedback producer remains PyGRC-owned. Therefore the realization is a
`pygrc_native_candidate`, not producer-assisted or RCAE-constructed.

This is not a `pygrc_native_supported` classification. Only later frozen
candidate evidence and complete controls could establish support.

## 4. State-carried causal factorization

```text
C_P(t3) = model.get_state().base_state.nodes[P].coherence

q_i = registered positive packet amount plus physical source, P target,
      edge, timing, and registered contribution type

U = schedule_packet_departure(S_i -> P, q_i) + step(departure, arrival)

L = native packet/event records with source node, lineage, amount, edge,
    packet identity, and times

V = emit_feedback(mask=[P], rear=[B_ref])
    + model-owned feedback producer
    + later native packet processing
```

`L` is audit-only in I03A. `source_lineage_id` and `target_lineage_id` are not
inputs to deterministic packet identity, departure/arrival coherence mutation,
feedback mass, or the feedback producer's state score. The response config
leaves `expected_source_surface_digest` null so contribution-history identity
does not become a state-carried response condition.

A neutral, contributor-independent contact after pool constitution supplies
the later opportunity and enables a fresh feedback read. The feedback row is a
state-derived response intermediate at t3, not the active pool history. If the
later exact fixture cannot preserve that distinction, registration must reopen
I03A rather than silently adopting history dependence.

## 5. Non-private access witness

P is one fixed topology-node identity with no contributor slots. A registered
eligible responder encounters P through the same one-node feedback mask,
without a source address. I06 must prove:

- the front mask contains P exactly once;
- neither source node nor either private partition is in the mask;
- B_ref is matched and not a contributor lookup;
- the producer config contains no contributor-lineage field; and
- an alternate eligible responder can use the same P access class for the R05
  access-scope contrast.

Absent or source-addressed access blocks R01.

## 6. Native intervention decision

The broad I01R1 classifications remain unchanged: CAP-04 and CAP-06 are still
inadequate because PyGRC has no generic state-only clamp with independently
fixed audit state and no atomic pool-specific write gate.

For this bounded state-carried profile, admitted native operations suffice:

1. **Pool-write freeze by diversion.** Execute the same source debits,
   marginal amounts, lineage, and timing but route contributions to K rather
   than P. P remains at reference; neutral encounter and response opportunity
   remain.
2. **Carrier debit.** After both candidate writes arrive, send native P-to-K
   flux before encounter. Contributor history stays intact and V must follow
   the post-debit P state.
3. **Audit-only permutation.** Change only source-lineage strings. Native
   restoration identity honestly changes, but P and response remain invariant.
4. **State-preserving order shuffle.** Complete both positive additions in
   S1-S2 and S2-S1 order before encounter. Native ledger order differs; equal P
   must yield invariant V.

The intervention packet necessarily adds an intervention record. I03A does
not claim byte-identical audit state. Its matched causal requirement is fixed
contributor activity/attribution, opportunity, and support with an explicit
intervention identity. If later exact registration needs an RCAE gate or clamp
to make this boundary work, the native classification reopens before any
calibration or candidate execution.

## 7. Private-partition and bypass controls

The private competitor uses two native nodes:

```text
S1 -> P1_private
S2 -> P2_private
```

It preserves marginal writes, timing, support, and one-node access
opportunity. Each retained private response reads one partition only. No
feedback mask or RCAE helper may read, sum, concatenate, dispatch over, or
choose between both partitions. Doing so constructs a mailbox/controller
aggregate and blocks R04 rather than satisfying the control.

The direct/global substitute may reproduce an output. It remains a bypass
because it lacks the independently intervenable P and native U-to-V chain.
Output equivalence alone is explicitly non-diagnostic.

## 8. Frozen cell and control coverage

All seven logical cells are present:

| Cell | I03A state-carried role |
| --- | --- |
| `reference-pool` | baseline P plus native write-diversion subconfiguration |
| `individual-contributions` | S1-only, S2-only, and quantity-matched one-source diagnostic |
| `combined-orders` | S1-S2 and S2-S1 with equal complete P before encounter |
| `pooled-history-shuffle` | state-preserving order and pure-lineage shuffle; expected invariant |
| `contributor-removal` | remove/divert either marginal contribution under matched opportunity |
| `global-state-exclusion` | guarded P1/P2 reads and direct/controller bypasses |
| `access-capacity-contrast` | selected access-scope axis: alternate eligible responder, same P read class |

All five controls receive target, held-fixed variables, qualitative relation,
allowed ambiguity, and fail-closed effect in the machine contract:

```text
AE01-L02-CTRL-01 each contributor alone
AE01-L02-CTRL-02 deletion and label permutation
AE01-L02-CTRL-03 state-preserving pooled-history shuffle
AE01-L02-CTRL-04 direct/global and guarded private substitution
AE01-L02-CTRL-05 native pool-write freeze and carrier debit
```

## 9. Operational projections

OP-01 through OP-09 are now state-carried and falsifiable:

- OP-01: two attributable arrivals must alter the same one-node P.
- OP-02: the later native eligibility/response relation must follow
  encounter-time P.
- OP-03: pure lineage-label changes must leave P and response invariant.
- OP-04: native diversion/debit must change the response relation while the
  audit-only permutation does not.
- OP-05: neither original marginal or contributor-removal branch may fully
  explain the combined relation. Quantity-matched one-source equivalence is
  allowed but limits the claim to several contributors populating one pool.
- OP-06: neither legitimate one-node private read may reproduce the common P
  relation; reading both is a forbidden bypass.
- OP-07: a direct/controller output match does not recreate P or U-to-V.
- OP-08: equal-P order/shuffle variants must remain invariant; divergence
  blocks this mode and cannot cause a post-outcome mode switch.
- OP-09: the relation must remain for an alternate eligible responder using
  the same access class to reach R05.

Exact equality and resolution remain I04 work. None of these statements is an
observed outcome.

## 10. Pool-economy dispositions

| Property | I03A disposition |
| --- | --- |
| Reserve | native node coherence and conserved packet budget measured later |
| Accumulation | applicable: additive native arrivals into P |
| Mixing | applicable: scalar addition in one P state |
| Depletion | applicable: native P-to-K debit |
| Saturation | `not_applicable`: no capacity/saturation rule selected |
| Leakage | `not_applicable` within passive window: no autonomous decay selected |
| Maintenance | `not_applicable`: no maintenance transition selected |

These dispositions support no resource-economy, circulation, trail,
maintenance, or native-pool-primitive claim.

## 11. Native gaps retained for later synthesis

I03A exposes the following reusable implementation demands without attempting
to add them to PyGRC or LGRC now:

- first-class pool role and non-private access-scope registry;
- atomic pool-specific write gate preserving matched source activity;
- selective state clamp with independently controlled audit projection;
- private-partition identity, opportunity matcher, and no-common-read guard;
- generic capacity, saturation, leakage, and maintenance contracts; and
- composite identity for RCAE role, schedule, intervention, and branch-pair
  state alongside native v2 restoration identity.

The absence of these first-class surfaces does not force an RCAE causal
producer in I03A because the bounded candidate uses native transitions and
declarative external identity. It remains implementation debt and a later
cross-experiment synthesis input.

## 12. Restoration proposal

I03A proposes, but does not yet freeze, the reset-aware provider:

```text
pygrc.models.lgrc9v3_restoration_identity_v2
pygrc.models.digest_lgrc9v3_restoration_identity_v2
```

I06 must require a valid persisted `pygrc.reset_baseline` group and compose
RCAE role/access, call schedule, feedback config selection, interventions,
private-branch pairing/guard, and later analysis identity. Legacy fallback is
forbidden. Reset is permitted only under a registered valid-baseline v2
profile; explicit rebase, if ever selected, requires external prospective
provenance.

## 13. Deliberately unresolved

I03A does not select:

- the raw response or orientation;
- the primary insufficient-repetition comparator;
- amounts, event times, threshold, or response packet amount;
- equality/resolution, aggregation, missingness, or machine pass rules;
- matched-null generator, seeds, or `delta`;
- exact node/edge IDs and topology;
- exact branch point and matrix quantities; or
- final composite identity and continuation check.

Those decisions belong to I04–I06. No candidate or calibration operation ran
in I03A.

## 14. Static validation

The retained
[I03A validator](../scripts/p2_i2_i03a_validate.py) generated the
[machine validation](../contracts/p2-i2/i03a-state-carried-realization-validation.json),
version `1.1.0`, SHA-256
`6e5c9e33e596c372a7281cdda4811781711ceb23da55aad2cfbc79249c53a5bf`.

It passed twenty-one invariants:

- 15/15 entry-authority digests match the entry revision;
- the original I03A input freeze retains its exact frozen digest;
- all 31 admitted source digests match manifest, revision, and worktree;
- all eight selected public callables are admitted;
- packet identity excludes source/target lineage;
- native arrival adds packet amount to target coherence while retaining
  lineage in audit state;
- feedback reads declared coherence masks without lineage;
- the native producer reads the state-derived score without lineage;
- all seven cells, five controls, nine OPs, and eleven CAP dispositions are
  complete;
- all three dependence modes are retained downstream and realization
  selection occurs within each mode;
- later modes and I04 remain unauthorized;
- I04 measurement decisions remain deferred; and
- the graph revision/worktree is unchanged and clean.

The validator is static authority/source-dataflow/cross-artifact validation.
It constructed no candidate, ran no cell/control, and executed no calibration
or scientific response operation.

## 15. Review disposition

`P2-I2-I03A-REVIEW-READY` is satisfied. The umbrella
`P2-I2-DISCRIMINATOR-GATE` remains in progress. I03B, I03C, I04, calibration,
registration, and candidate execution are unauthorized.

### 15.1 Post-freeze owner scope clarification

After static design validation and before I03A acceptance, the project owner
accepted `P2-I2-DEC-011`/`P2-I2-CHG-008`: state-carried, history-carried, and
hybrid are all retained through downstream execution and interpretation.
Realization selection occurs within each mode, not among the modes. The
original I03A input freeze remains unchanged as historical entry authority.
This clarification does not accept or revise the state-carried mapping, open
I03B/I04, or add runtime or scientific evidence.

The next action is owner review of this state-carried package. No
history-carried analysis should begin until that review explicitly authorizes
8B.
