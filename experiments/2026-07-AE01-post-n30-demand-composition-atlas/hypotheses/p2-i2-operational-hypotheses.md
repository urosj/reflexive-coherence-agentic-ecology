# P2-I2 Operational Hypothesis Projections

**Status:** outcome-free; `P2-I2-I03A` and `P2-I2-I03B` are owner-accepted
for staged progression with their implementation-conformance results retained;
`P2-I2-I03C` has a frozen minimally producer-assisted hybrid causal design,
passed static validation, and `258/258` byte-reconstructed bounded runtime
conformance; `P2-I2-I03CR1` passed 26/26 review checks and 17/17 acceptance
conditions with zero blockers and eight fail-closed downstream obligations;
I03C is owner-accepted for progression and the zero-runtime `P2-I2-I03F`
compact umbrella family closeout passed 12/12 integration checks and 9/9
acceptance conditions with zero blockers and is owner-accepted; the
discriminator gate is passed and `P2-I2-I04` candidate-free measurement and
calibration preregistration passed its original static validation, but owner
review withheld `P2-I2-CAL-PRE-GATE` passage due a primary-comparator contract
conflict and additional null/window duties; candidate-free `P2-I2-I04R1`
corrected those duties and passed 19/19 focused static checks plus 15/15 pure
tests; conditional owner review accepted the conceptual correction but opened
candidate-free `P2-I2-I04R2`, which confirmed all eight machine invariants with
16/16 focused checks and 7/7 pure tests after correcting the future-I05 route
to use three raw arms through the live estimator; the project owner accepted
I04R2 as the sole progression authority and passed CAL-PRE under DEC-026;
original I04 and I04R1 remain immutable historical artifacts; proposed
DEC-027 remains failed-closed after I05A; I05B/I05C were owner-approved and
committed, and the single governed arithmetic null completed with one builder
call, zero retries, one readback, and a refused second start; its raw evidence
is retained at `c3eabf3`, but 10.4 closeout exposed forbidden persisted paths;
DEC-032 now retains the corrected P2-I2-wide I05D audit of 135 files with
312 value-redacted violations in 70 files; DEC-033 accepts that inventory, and
the first eleven-file I05E correction group is review-ready after 10/10 checks
with zero group violations; later corrections, metric freeze, CAL-GATE, I06,
and candidate execution remain closed pending review; all three profiles
remain distinct and retained downstream under
`P2-I2-DEC-011`

**Lane:** `AE01-L02`

**Frozen hypothesis authority:** `AE01-H-L02`

**Evidence effect:** subordinate projection plus quarantined realization
implementation-conformance; no calibration, control outcome, L02 support/
falsification, or scientific result

**Semantic authority:**
[accepted P2-I2 brief](../implementation/P2-I2-shared-pool-co-conditioning-brief.md)

**Activity and gate authority:**
[P2-I2 checklist](../implementation/P2-I2-shared-pool-co-conditioning-checklist.md)

**Decision authority:**
[P2-I2 decision record](../implementation/P2-I2-decision-record.md)

**Controlling contracts:**
[L02 hypothesis](lane-hypotheses.md),
[post-R3 ecology-discriminator amendment](post-r3-ecology-discriminator-amendment.md),
[outcome and stopping contract](outcome-and-stopping-contract.md),
[developmental interpretation contract](developmental-interpretation-contract.md), and
[L02 metric sheet](../contracts/metric-sheets/AE01-L02.json)

## 1. Authority and purpose

`AE01-H-L02` is already frozen and remains the only lane hypothesis authority.
This artifact does not create a competing hypothesis, alter a stable ID, add
schema vocabulary, or predetermine a terminal class. It projects the frozen
hypothesis and accepted brief into a realization-local family that can be
instantiated, preregistered, falsified, and resolved.

The local IDs `H-L02-OP-01` through `H-L02-OP-09` are navigation and
traceability identifiers only. They are not additions to the Phase 1 closed
hypothesis registry.

The operational family has this lifecycle:

```text
I00 scaffolded
  -> I03A state_carried_bound -> owner_review_A
      -> I03AR1 -> I03AR1R1_if_infrastructure_invalid
          -> state_carried_runtime_conformed_or_inadequate -> owner_review_AR1
        -> I03B_history_design_frozen
          -> I03B_history_runtime_conformed_or_inadequate -> owner_review_B
          -> I03C hybrid_bound -> owner_review_C
              -> I03 staged_family_bound -> I04 preregistered
                              -> I08 executed or validly incomplete
                              -> I09/I11 resolved and interpreted
  -> mode_specific_prerequisite_classified -> owner_review
      -> staged I09/I11 route when the umbrella gate cannot pass
```

An operational projection cannot be reworded after candidate outcomes. A
scientific change requires checklist change control, a new preregistration,
and a new cycle while preserving the earlier result.

## 2. Shared causal notation

The accepted generic factorization is:

```text
common carrier transition:
  C_P(k+1) = U(C_P(k), q(k), local_context(k))

audit lineage:
  L(k+1) = audit_append(L(k), source_id(k), q(k), time(k))

later continuation:
  Y = V(C_P(t3), opportunity_context)

forbidden bypass:
  Y = G(L, contributor_slots, contributor_count, success_labels)
```

`C_P` is the mode-relevant common encounter state, active carrier history, or
both. `L` preserves attribution for audit. An arbitrary source label may remain
in `L` but cannot enter `V`. Causal contribution properties such as amount,
location, timing, or registered type may enter `U` through `q`.

This notation does not by itself select a topology, exact carrier identity,
numerical update rule, scientific response, or registered implementation.
I03A's state-carried, I03B's history-carried, and I03C's hybrid causal mappings
are frozen below; exact scientific values remain later work.

## 3. Unbound realization variables

| Variable | Required meaning | Current state | Binding iteration |
| --- | --- | --- | --- |
| `graph_source_identity` | Exact admitted graph revision and relevant source digests | Bound by `P2-I2-DEC-009` and the I02R2 manifest at `83e3a300426631ee4df71b661b67d4fcfdfed594`; prior I02R1 identity remains historical authority and no realization is implied | I02R2 complete |
| `realization_class` | Native, producer-assisted, or constructed, separately dispositioned for each mode | I03A: `pygrc_native_candidate`; I03B/I03C: `minimally_producer_assisted` | I03A, then I03B, then I03C |
| `pool_dependence_mode` | Staged `state_carried`, `history_carried`, and admissible `hybrid` profiles | I03A: `state_carried`; I03B: `history_carried`; I03C: design-frozen `hybrid` | I03A, then owner review; I03B, then owner review; I03C |
| `source_set` | At least two distinguishable attributable source carriers/events | I03A/I03B/I03C: symbolic native roles S1 and S2 bound; exact node IDs pending I06 | I03A/I03B/I03C concept; I06 exact |
| `C_P` | One auditable non-private causal carrier identity | I03A: native P coherence; I03B: one RCAE-owned ordered `H_P` plus native output `M_H`, while P is excluded from V; I03C: separately causal native P plus active `H_P`, jointly read through P and `M_H` | I03A/I03B/I03C |
| `L` | Audit-only source lineage and attribution projection | All modes: native packet/event/surface/lineage records; I03B/I03C use row identity only for active-history admission/idempotency, never as a response input | I03A/I03B/I03C |
| `q` and `U` | Contribution properties and common-carrier transition | I03A: native arrival into P; I03B: source-label-free token append then native `M_H` materialization; I03C: the same physical contribution advances native P and the separately intervenable active history | I03A/I03B/I03C concept; I06 numeric/exact |
| `V` | Carrier-scoped read, susceptibility, or continuation path | I03A: native P/B_ref feedback; I03B: native M_H/B_ref feedback after adapter handoff; I03C: one native `[P,M_H]`/`[B_ref]` feedback path after adapter handoff; I04R1 freezes the shared downstream consequence as native B-target coherence gain over one fixed two-step response window | I03A/I03B/I03C causal read; corrected I04R1 response review-ready; I06 exact masks/policy |
| `access_witness` | Non-private carrier access without contributor addressing | I03A: one-node P mask; I03B: one common H_P/M_H path; I03C: one common P+H_P identity read through `[P,M_H]`, available to any registered eligible A-role responder | I03A/I03B/I03C concept; I06 exact |
| `primary_response` | One oriented raw later-continuation response | I04R1 freezes fixed-window native B-target coherence gain, identity-oriented with higher aligned and binary-like zero/one-packet semantics; shared extraction does not merge modes; owner review pending | I04R1 |
| `primary_comparator` | Closest insufficient-repetition alternative | I04R1 freezes the stronger of two symmetric carrier-changing leave-one-admitted branches within each mode/seed/physical order; repeated-S1/S2 is restored to an equivalence-permitted scope diagnostic; owner review pending | I04R1 |
| `control_relations` | Signed invariance/divergence and fail-closed effects | I03A/I03B/I03C qualitative relations plus corrected I04R1 numerical and evidence-derived causal-chain rules are frozen and review-ready; `analysis_arithmetic_delta` remains I05 | I03A/I03B/I03C, I04R1, then I05 resolution |
| `R05_contrast` | One capacity, contributor, or access-scope variation | All three modes select the access-scope axis; exact alternate responder pending | I03A/I03B/I03C concept; I06 exact |

No pending variable may be filled from candidate outcomes.

### 3.1 I02 source prerequisite

`P2-I2-I02`, as corrected and revalidated by I02R1, historically admits graph revision
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`, its exact relevant source and
public-callable identities, and makes the native
`lgrc9v3_restoration_identity_v1` provider available for conditional later
selection under the
[I02 manifest](../contracts/p2-i2/i02-admitted-source-and-restoration-manifest.json).
The historical P2-I1 RCAE projection is not an automatic fallback at this
revision. Native identity must later be composed with all selected RCAE-owned
state and followed by a separately frozen bounded equal-input continuation
check. Provider selection remains `null`. At that revision the private reset
baseline is not separately covered, so the historical restriction requires a
later continuation to forbid reset or compose an explicit reset-baseline
identity.

`P2-I2-I02R2` admits clean updated graph revision
`83e3a300426631ee4df71b661b67d4fcfdfed594`, the versioned
`pygrc.reset_baseline` group, and
`lgrc9v3_restoration_identity_v2` for conditional later selection. V1 remains
current-state-only; v2 adds reset-baseline identity. Provider selection remains
`null`. A valid persisted baseline no longer requires the historical blanket
reset prohibition under a later v2 registration. Legacy/unavailable baseline
state still blocks reset and v2 until explicit prospective rebase, whose
provenance remains externally composed and never recovers historical
construction state.

I02R2 re-closes only the `graph_source_identity` prerequisite. It does not bind
a realization class, carrier, dependence mode, operational projection,
response, comparator, or outcome. Those remain I03/I04 work.

### 3.2 Review-separated dependence-mode program

Owner direction dated 2026-07-14 requires all three dependence modes to be
implemented as separate, sequentially reviewed profiles:

```text
I03A / 8A = state_carried
I03B / 8B = history_carried
I03C / 8C = hybrid
```

I03A is owner-accepted for progression and I03B is active under its own
checklist declaration and immutable design/source-comparison freeze. I03B may
bind history-carried meanings in this artifact but must not pre-resolve the
hybrid profile. I03C requires a later checklist declaration, input freeze,
and owner review. The umbrella realization-bound status and I04 entry remain
unavailable until the staged family is complete and reviewed.

The project owner's later 2026-07-14 clarification, retained as
`P2-I2-DEC-011`, fixes the downstream scope: all three profiles continue
through preregistration, exact registration, finite execution, control
resolution, reconstruction, and interpretation. They are not alternatives in
a later winner-selection step. Native, minimally producer-assisted, or
missing-prerequisite selection occurs separately within each mode. I04 must
freeze whether measurement and calibration identities are validly shared or
mode-specific without dropping a mode, and I11 must preserve all three
mode-specific dispositions inside one bounded lane-level terminal
classification.

The project owner's subsequent acceptance of the stronger solution, retained
as `P2-I2-DEC-012`/`P2-I2-CHG-009`, inserts one bounded runtime-conformance
gate before each mode is accepted for calibration. I03AR1 applies that gate to
the already frozen state-carried design; I03B and I03C must include the same
design-first, freeze-before-runtime, review-separated structure. Conformance
may establish only whether declared interfaces, interventions, guards,
restoration, and equal-input continuation execute as specified. It cannot
select a scientific response, comparator, delta, seed matrix, or candidate
value and cannot support or falsify `AE01-H-L02`.

The first frozen I03AR1 evidence invocation produced no retained conformance
artifact. It stopped on strict equality between a derived binary floating-
point response delta (`0.09999999999999998`) and the frozen decimal literal
`0.1`. `P2-I2-I03AR1R1`/`P2-I2-CHG-010` classifies this as
`infrastructure_invalid`, not realization inadequacy. The only permitted
revision is an absolute-tolerance comparison of `1e-12` with zero relative
tolerance for derived response deltas. No fixture value, causal relation,
branch, native/producer ownership, hypothesis projection, or scientific
boundary changes, and the stopped invocation supplies no evidence.

The governed replacement invocation subsequently passed 136/136 frozen
assertions, and its sole reconstruction was byte-identical (conformance SHA-
256 `a7601bb1a7d335cfefc9d21aa365e3f5732ae0ebdfabe6bb7d168a7194ed0db0`).
This assigns `runtime_conformant` only to the bounded I03A state-carried native
candidate implementation. It does not assign truth, support, falsification,
effect size, calibration input, or a registered value to any operational
hypothesis. I03B remains behind explicit owner review.

The project owner's subsequent direction to move to 8B accepts the review-
ready I03A/I03AR1 package only for staged progression and activates
`P2-I2-I03B`. It assigns no scientific result and does not authorize I03C or
I04. I03B must independently freeze what active common history is causal,
what remains audit-only lineage, which response reads that history, and which
native/producer/missing-prerequisite realization is adequate. The I03AR1
fixture and observed values are prohibited selection inputs. Design must be
frozen before the first history-carried runtime call, followed by a separate
bounded conformance freeze under DEC-012.

#### 3.2.1 I03B history-carried design binding

Static admitted-source comparison under the I03B freeze found a precise
native boundary. PyGRC owns an ordered, restored packet/contact log, but its
surface rows are explicitly passive evidence. Native feedback derives from
the latest contact plus live node state; the expected-source digest compares
one configured row and is not a common multi-event history reducer. LGRC-0
history artifacts are annotation-only. Therefore I03B selects
`minimally_producer_assisted`, not a native history candidate.

The selected `RCAEActiveHistoryAdapterV1` owns one missing separable
operation: an active, independently intervenable, ordered common history
projection over admitted native contribution rows. It stores no source IDs or
lineage in causal tokens, computes no success field, reads no response target,
and stops after materializing a deterministic history readout at native node
`M_H` through public balancing packets. PyGRC owns every coherence mutation,
the `M_H`/`B_ref` feedback read, threshold evaluation, later packet schedule,
and packet processing. If runtime conformance requires the adapter to decide
or schedule success, the realization fails closed as a missing prerequisite.

The history-carried factorization is:

```text
native attributable arrivals to P
  -> source-label-free physical tokens q1, q2
  -> one ordered external H_P via RCAEActiveHistoryAdapterV1
  -> order-sensitive readout R_H(H_P)
  -> public native balancing packets materialize M_H
  -> native feedback mask(M_H, B_ref)
  -> model-owned producer and later native packet

native packet/event/surface/lineage records = L, audit-only for response
P.coherence = matched encounter state, excluded from history-mode V
```

`H_P` is an ordered token tuple rather than contributor-private slots. The
structural readout is a source-label-invariant left fold
`r_(j+1) = lambda * r_j + typed_amount_j`, with `0 < lambda < 1`; scientific
numeric values remain I04/I06 work. I03B runtime conformance must use a
separately frozen fixture-only coefficient and values that are prohibited as
later calibration inputs.

The mode-specific interventions are now qualitative authority:

- physical-token order shuffle: preserve marginal token multiset and final P
  while changing H_P, R_H/M_H, and the later response relation;
- active-history clamp: preserve native contributions, audit, P, support, and
  opportunity while explicitly replacing H_P and rematerializing M_H;
- state-only separation: change P through a native intervention while H_P and
  M_H remain fixed; the history-mode response remains invariant;
- native write diversion: preserve source activity but prevent arrival-to-P
  admission, leaving H_P at reference; and
- pure lineage-label permutation: change audit identity while H_P/M_H/V remain
  invariant.

The private competitor uses separate `H1_private` and `H2_private` adapter
instances. Each legitimate response may read one private readout only. No
component may concatenate, compare, sum, dispatch over, or choose between
both. The common access witness is the single H_P/M_H binding, available to
any registered eligible responder through the same one-node mask.

Native v2 identity covers the complete model, M_H, logs, producer config, and
native reset baseline. It does not cover H_P, the consumed-row cursor,
adapter configuration/interventions, or adapter reset baseline. I03B therefore
requires one versioned composite identity and paired save/load/reset operation
over native v2 plus the complete adapter current and reset state. One-sided or
implicit-rebase reset is forbidden.

This design is frozen by the
[I03B realization contract](../contracts/p2-i2/i03b-history-carried-realization-and-discriminator-contract.json).
Its exact runtime fixture, assertions, artifact paths, and conformance-only
values were retained in a second immutable freeze before the first history-
carried runtime call. The single evidence invocation passed `252/252` frozen
assertions, and the single reconstruction was byte-identical at SHA-256
`4465ff2174d285d26ffa8a6cb4bebaf644b150d24bea0d69563eb5f51d8c177d`.

This assigns only `runtime_conformant` to the bounded producer-assisted
implementation. It does not assign truth, effect size, support, falsification,
scientific response/comparator, calibration input, registration value, or a
mode ranking. The fixture-only order, amount, coefficient, threshold, and
response values are prohibited inputs to I04/I06. The adapter computed no
success and scheduled no later response; the native feedback producer owned
that transition. Paired native-v2/adapter composite save-load, reset, and
equal-input continuations passed. At I03B closeout, I03C and I04 remained
unauthorized; the later owner progression decision `P2-I2-DEC-015` opened
design-first I03C only and left I04 blocked.

#### 3.2.2 I03BR1 closeout-revalidation projection

The project owner's supplied I03B review activated `P2-I2-I03BR1` as a
separate zero-runtime acceptance audit before any progression decision. The
audit passed all twenty-one checks—fifteen directly and six with downstream
obligations—with zero blockers. The review and audit do not themselves accept
the history-carried realization and do not authorize I03C or I04.

I03BR1 must first exclude a hidden latest-contact path in which the adapter's
final materialization packet, rather than H_P's persistent materialized output
state, carries the native response difference. It must also confirm that the
functional pool identity is H_P plus its declared M_H output port: P remains
native intake, L remains audit, and M_H alone is not substituted for the
active ordered history.

The audit is limited to frozen-source/dataflow and retained-artifact evidence.
It must cover the exact P/H_P/L/U_H/R_H/M_H/V factorization; physical token
typing; admission and cursor isolation; continuation-state matching; clamp,
state-only, diversion, private, and access controls; producer minimality;
history lifecycle class; composite current/reset identity; branch isolation;
and mechanical scientific quarantine. The complete I03B harness, adapter,
runtime freeze, evidence invocation, and reconstruction remain immutable. No
new model, evidence, reconstruction, retry, rescue, calibration, candidate, or
control invocation is authorized.

The two priority boundaries passed. A neutral contact follows materialization;
across the order branches its route, endpoints, amount, event time, scheduler
index, event kind, and channel match. Only node-proper-time and derived row
digests differ, and native polarity/threshold evaluation does not read those
differences. `expected_source_surface_digest` remains null. Separately, H_P is
persistent and independently replaceable adapter state, while M_H is its
native output port. The clamp replaces H_P before readout recomputation and
native rematerialization; it does not clamp a precomputed scalar.

I03BR1 also freezes the claim and lifecycle qualifications. The bounded claim
is active ordered history retained and causally materialized through a
deterministic scalar readout, not irreducible raw-history necessity or
non-Markovianity. Normal H_P operation is run-bounded append-only; explicit
whole-history replacement is implemented, while autonomous depletion, fixed
capacity/saturation, leakage/decay, and maintenance are not selected for this
conformance realization.

The six downstream obligations do not change I03B's design or evidence: I06
must retain a unique source-to-P admission path or register an explicit route
key, resolve scientific access, bound lifecycle/event counts, expose only a
paired restoration interface with explicit manifest-hash validation, and
retain branch identity duties; I04/I06 validators must reject every
conformance fixture value and digest. Only the pre-runtime fold family and its
causal boundaries may be imported.

`P2-I2-I03BR1-CLOSEOUT-PASSED` makes I03B acceptance-ready. A later owner
progression decision may open I03C only; it cannot pass the umbrella
discriminator gate, assign R01-R05, compare modes, or open I04.

#### 3.2.3 I03C hybrid entry projection

The project owner's direction that 8C is next accepts the I03B causal design,
bounded runtime conformance, and I03BR1 closeout only for staged progression.
`P2-I2-DEC-015` retains `minimally_producer_assisted`, leaves the history-
carried scientific status unresolved, opens I03C under its own checklist and
input freeze, and keeps I04 blocked.

The native-first I03C source/dataflow comparison selects
`minimally_producer_assisted`. PyGRC can natively own the state component,
joint live-state read, threshold/polarity evaluation, response scheduling,
later packet transition, and graph-state restoration. Its multi-node feedback
front mask reads native `P` and the history output port `M_H` exactly once each
against `B_ref`. Complete native hybrid realization is nevertheless
inadequate because admitted PyGRC has no active, independently intervenable
multi-event common-history carrier.

I03C therefore reuses only the structural `RCAEActiveHistoryAdapterV1`
boundary selected before I03B runtime. The adapter owns one ordered,
source-label-free `H_P`, admission/idempotency, independent history
interventions, deterministic `R_H`, and public-packet materialization at
`M_H`. It must stop before the joint native read and may not read `P` as a
success input, add `P+M_H`, apply a threshold, schedule the later response, or
read response/success fields. This is a new hybrid composition, not a relabel
of I03A or I03B.

The design freezes independent state-only and history-only interventions plus
their joint contrast. A native P-only debit changes `P` while `H_P/R_H/M_H`
remain fixed; history replacement/clamp and rematerialization change
`H_P/R_H/M_H` while P remains fixed. Both must affect the same native joint
score/response under the later frozen resolution. Label permutation,
write-diversion, history order, private pairs, alternate access, and common
neutral-contact guards distinguish hybrid dependence from state-only,
history-only, latest-contact, source-label, mailbox, or controller shortcuts.
Nonlinearity is optional, but joint functional dependence is mandatory.

I03A and I03B are immutable prior-mode authorities. Their fixture values,
observed response branches, comparators, and evidence digests are prohibited
I03C selection inputs. Any realizable I03C design must receive a separate
validated runtime-conformance freeze under DEC-012 before one evidence
invocation and one reconstruction. The separate freeze validated before the
first model call; the one evidence invocation passed `258/258` frozen
assertions and the one reconstruction was byte-identical at SHA-256
`217c8972e8e1199409343fb72b0eca12b2ba24dceb6a1f213c97af9143f0e96c`.

The bounded result demonstrates implementation conformance only. Under the
same native `[P,M_H]` mask, the canonical branch responded while independent
P-only debit and H_P-only clamp branches did not; history order, label,
write-diversion, private-pair, alternate-access, neutral-contact, producer-
ownership, and paired restoration guards also passed. This cannot pass the
umbrella discriminator gate or open I04. The exact conformance values are new
fixture-only inputs and are prohibited I04/I06 inputs; exact scientific
component parameters, response, comparator, topology, and resolution remain
I04/I06 work.

#### 3.2.4 I03CR1 hybrid closeout projection

The owner-supplied I03C acceptance review activates a separate zero-runtime
closeout audit before owner acceptance or umbrella-family disposition. The
review does not authorize an I03C rewrite, rerun, new fixture, or I04. It asks
whether the retained package is causally well-formed as a hybrid architecture,
not merely executable.

I03CR1 must retain one exact composite carrier identity:

```text
hybrid common carrier =
  native current-state component P
  + authoritative independently persistent/intervenable H_P
  + declared native output-port binding M_H = R_H(H_P)
  + common [P,M_H]/[B_ref] access relation to one native V

L = separate native attribution/audit lineage
```

Neither P, H_P, M_H, the mask, adapter, nor feedback row alone may substitute
for that identity. The native response mechanism reads two current nodes; the
bounded hybrid architectural claim additionally depends on H_P persisting,
restoring, and accepting intervention independently of M_H. H_P is
authoritative, M_H must be rematerialized and verified before V, and this
assigns no irreducible-history or non-Markovian claim.

I03CR1 also freezes the qualitative future component factorial without
scientific values: P-reference/H-reference, P-candidate/H-reference,
P-reference/H-candidate, and P-candidate/H-candidate. Each uses the same
registered component constructions and V. The conformance run need not have
scientifically executed those four cells; it only demonstrated bounded
independent intervention feasibility. I04/I06 may operationalize but may not
invent or delete the factorial.

The audit must distinguish direct retained evidence from non-semantic
clarification and downstream registration obligations. Unique route keys,
atomic manifest APIs, private cross-load rejection, capacity/bounds, and later
mechanical I04/I06 rejection may remain downstream only when the bounded
fixture/source dataflow is already adequate and the duty is exact and fail-
closed. Any causal ambiguity, self-admission route, P/H redundancy, adapter
success computation, stale H_P/M_H use, hidden private aggregation, I03
artifact mismatch, scientific fixture reuse, or automatic I04 authorization
is a blocker.

The zero-runtime I03CR1 audit passed all twenty-six review checks and all
seventeen acceptance conditions with zero blockers. Seventeen checks are
direct retained-artifact passes, four are closure clarifications, and five
pass with exact downstream obligations. The immutable result retains eight
fail-closed duties across I04, I06, and the separate umbrella I03 family
closeout.

Three qualifications remain part of the hypothesis projection. First, the
complete qualitative P × H 2x2 is frozen for future science but was not fully
executed by I03C conformance. Second, composite restoration is a layered
native-plus-adapter-plus-binding package identity, not a new atomic native API.
Third, neutral contacts match in physical configuration and final relative
position, while absolute scheduler slots differ after explicit intervention
operations; those slots do not enter the native score or threshold, and I06
must still match or stratify every scientifically causal timing field. These
are downstream controls, not evidence for or against `AE01-H-L02`.

I03CR1 assigns no owner acceptance, mode rank, discriminator-gate passage,
scientific response, comparator, R01-R05 result, or L02 conclusion. I03C is
acceptance-ready. If accepted, only a separately declared checklist- and
hypothesis-governed umbrella I03 family closeout may begin; I04 cannot open
directly.

#### 3.2.5 I03F umbrella family-closeout projection

The project owner accepted I03C/I03CR1 for staged progression and directed
section 8.1 to begin. I03F is the separately declared umbrella closeout. It is
a compact zero-runtime composition of already accepted mode reviews, not a
repetition of their capability/source/dataflow audits, not a fourth dependence
mode, and not a scientific comparison.

I03F must retain the three profiles simultaneously:

```text
state-carried   = native P carrier; pygrc_native_candidate
history-carried = authoritative H_P with M_H = R_H(H_P);
                  minimally_producer_assisted
hybrid          = native P + authoritative H_P/M_H through one native V;
                  minimally_producer_assisted
```

These classes describe where missing implementation machinery resides. They
do not rank ecological adequacy, assign preference, or permit one mode to
stand in for another. Producer assistance may supply only the accepted missing
history carrier/readout bridge; it may not calculate success, improve an
outcome, collapse the modes, or revise a qualitative relation.

The family closeout trusts the accepted mode-level findings and indexes each
mode's exact carrier, update/write path, access mask, intervention,
common/private relation, operational-hypothesis mapping, restoration owner,
and producer prohibition without re-proving them. It may inspect only the
terminal authority identities and fields needed to detect omission,
substitution, semantic collapse, or cross-mode rewrite. Shared symbols are
mode-qualified: P is the complete state-carried causal pool, excluded from the
history-carried response, and only one component of the hybrid carrier. H_P
and M_H are causal in history and hybrid but do not retroactively alter the
accepted state-carried profile.

Every OP-01..OP-09 projection must remain usable in all three modes without
assigning R01-R05. The family registry must also consolidate, without
discharging, all six I03BR1 and eight I03CR1 downstream obligations; bind the
complete I03A/I03B/I03C fixture quarantine; and freeze an I04 import rule that
retains all three profiles unchanged and mode-indexed. Exact scientific
responses, comparators, calibration identities, parameters, topology, seeds,
and resolution remain I04/I06 work.

I03F may establish only discriminator-gate readiness. It instantiates no model
and produces no new implementation or scientific evidence. It performs no new
source-capability audit and cannot select a mode, reuse a conformance fixture,
pass `P2-I2-DISCRIMINATOR-GATE`, or open I04 without a later owner disposition
on the retained family-closeout package.

The compact composition passed all twelve integration checks and all nine
acceptance conditions with zero blockers. Eleven terminal authorities match
the accepted baseline commit. The retained family index contains exactly three
unranked required profiles, one pointer for each of nine OPs in each mode,
fourteen exact source obligations mapped once into nine consolidated duties,
the existing seven-source three-mode quarantine, and the mode-indexed I04
import boundary. No source obligation is discharged.

This result is family consistency and gate-readiness evidence only. It does
not revise or strengthen a mode-level finding, add implementation evidence,
assign a scientific response or comparator, pass the discriminator gate, or
authorize I04. Those final two effects remain with explicit owner review of
the I03F package.

The project owner subsequently accepted the I03F package and directed I04 to
begin. This passes only `P2-I2-DISCRIMINATOR-GATE`. It assigns no mode rank,
scientific response, comparator, calibrated resolution, control result, or L02
outcome.

#### 3.2.6 Historical I04 measurement and calibration-preregistration projection

This subsection records the original candidate-free construction. The owner
withheld CAL-PRE acceptance, and I04R1 below supersedes its comparator,
window, null-scope, and causal-analysis identities for progression. Nothing in
this historical subsection remains authority where it conflicts with 3.2.7.

I04 is the candidate-free scientific-choice boundary. It imports all three
accepted causal profiles unchanged and must decide, before matched-null or
candidate execution, exactly what later consequence is measured and which
closest insufficient-repetition alternative owns the primary margin in each
mode.

The initial choice-resolution work must compare admissible response and
comparator options against the accepted L02 semantic center. It may share a
response, aggregation rule, or matched-null identity across modes only after
showing equality of causal meaning, unit/orientation, observation window,
comparator role, missingness, and calibration population. Code convenience or
expected effect size is not semantic equivalence.

I04 must freeze:

- one exact raw substrate-visible later-continuation response and numerical
  orientation per mode;
- one closest primary insufficient-repetition comparator per mode, with other
  close alternatives retained as signed controls;
- seed pairing, aggregation, normalized margin, denominator floor, missingness,
  and raw-response retention shared by I05 and later live analysis;
- machine equality/resolution and pass/ambiguous/fail rules for every imported
  qualitative expectation without changing its direction;
- one candidate-blind matched-null design, shared only where semantic
  equivalence is demonstrated, with inputs/seeds/resources/reconstruction and
  stopping rule for later I05 execution; and
- complete rejection of every I03 conformance fixture value, observation,
  comparator, branch/topology identity, assertion outcome, and digest.

I04 performs neither matched-null calibration nor candidate execution. Its
result is a preregistered question and measurement procedure, not evidence for
an answer. I05 remains unauthorized until the complete candidate-free package
is validated and owner-accepted.

The candidate-free choice-resolution input selected the native receiving-
substrate consequence rather than the intermediate feedback score or a
scheduled/success flag:

```text
Y = native coherence at B after the one admitted A-to-B response window
    - native coherence at B immediately before the native producer evaluation
```

The window contains exactly one native feedback-producer evaluation and the
packet arrival it schedules, if any. A completed no-response window is
scientific zero; operational failure is null and makes that mode/seed's full
two-order panel not evaluable. Higher B gain is aligned. Packet identity,
producer decision, A debit, B arrival, masks, and window boundaries remain
chain evidence, not substitute response fields.

This response, unit, orientation, window, comparator role, aggregation,
missingness, and analysis-only calibration population are equal across modes,
so I04 freezes one shared response, pure analysis identity, and candidate-blind
null. The upstream causal carrier remains P, H_P/M_H with P excluded, or P plus
H_P/M_H according to mode; shared measurement neither merges nor ranks them.

The primary pairing is frozen separately in both source-role orders:

```text
candidate  = S1->S2 or S2->S1 two-source common-carrier constitution
comparator = same quantity/type/timing-class sequence repeated by the first
             source in that order
```

This comparator preserves the inherited one-source carrier relation while
removing multi-source constitution and is therefore the closest D-039
insufficient-repetition explanation. Outcome magnitude did not select it.
Contributor removal, marginal sources, shuffle/order, private partitions, and
controller substitutions remain mandatory signed or causal-chain controls.
All three seeds and both orders remain raw; the six primary margins per mode
cannot be averaged, selected, minimized, or maximized, and the top primary
signature requires every margin to exceed calibrated resolution.

Nine common and 3/3/5 state/history/hybrid rule sets now map the accepted
qualitative expectations into machine `pass`, `ambiguous`, or `fail` inputs.
State retains equal-P order invariance. History retains active-history order
divergence and P-only intervention invariance. Hybrid retains a complete
qualitative P-by-H_P four-cell factorial, separate P-only and H_P-only
divergence, and history-order divergence with P fixed; no interaction,
synergy, irreducibility, or nonlinearity condition was added.

The shared future I05 null is ten equal exact-rational response pairs: five
frozen calibration seeds by two orders. It imports no PyGRC, candidate/runtime,
I03 fixture, or P2-I1 calibration evidence. I04 froze but did not execute the
generator. The future entry point requires a separate I05 execution freeze
recording owner CAL-PRE acceptance, exactly one null invocation, exact I04
identities, and continued candidate prohibition, so `delta` remains pending.
Static validation passed 16/16 checks and the pure analysis suite passed 10/10
tests with zero model, null, or candidate invocations. The original package
reached `P2-I2-I04-REVIEW-READY`, but the project owner's critical review
withheld acceptance. I04R1 must resolve the comparator, analytic-null,
fixed-window, B-purity, mode-isolation, evidence-derived-chain, and rationale-
quarantine duties before the package can return for review.

#### 3.2.7 I04R1 critical-review projection

I04R1 is a candidate-free preregistration correction, not a calibration or
scientific retry. It retains the original I04 identities and the owner review
as historical inputs while reopening only the load-bearing measurement and
analysis choices identified by that review.

The quantity-matched one-source replacement must return to its accepted role as
a source-plurality scope diagnostic. Both repeated-S1 and repeated-S2 branches
must be retained over physical q1->q2 and q2->q1 order strata unless exact
source-role symmetry is independently demonstrated. Equality is valid when the
complete mode-relevant carrier is equal and cannot by itself fail R03; full
single-source explanation requires causal evidence, not output equality.

The revised primary comparator must change the common carrier while preserving
the nearest source activity, timing, support, opportunity, and response
conditions. Its identity cannot be selected from an observed margin. Per-order
relations remain independent: failure of the complete top signature is not
automatic falsification of a valid history- or hybrid-order relation.

I05 may calibrate only pure analysis-arithmetic resolution. It cannot assign a
runtime, save/load, queue, B-measurement, or mode-specific continuation
tolerance. I04R1 must therefore freeze a separate I06 numerical-admissibility
rule and keep every runtime/continuation tolerance explicitly registered.

The response window must be a fixed sequence and count of public native
operations whose endpoint is identical whether a response is scheduled,
unscheduled, delayed, blocked, or operationally invalid. B gain is valid only
when B starts matched and retained evidence proves that the registered response
packet is its sole permitted change; otherwise the response must use attributable
packet arrival or a matched-background subtraction.

Shared response/analysis identity covers extraction semantics only. Each mode
must retain its own primary margins, controls, metric relation, support, and
rung inputs. Private/controller control status must be derived from masks,
carrier/source identities, call provenance, lineage, guards, branch
configuration, and runtime receipts, never trusted from authored booleans.
Every corrected choice rationale must reconstruct from accepted theory and
pre-runtime causal contracts without importing conformance observations.

The corrected package now freezes the strongest symmetric leave-one common-
carrier admission comparison. Both source activities remain matched: in one
arm q1 enters the common carrier while q2 is debited and diverted to an inert
sink; the second arm reverses admission. Their maximum oriented response is
the predeclared comparator. Both raw arms remain visible. Repeated-S1 and
repeated-S2 remain a separate four-branch-per-mode/seed diagnostic over both
physical orders, and equal complete carriers may validly yield equal response.

The response protocol is now exact and outcome-independent: capture matched
`B_before` with empty queues, emit one feedback row, run the feedback producer
once, call `step` twice, and capture `B_after` plus queues and lineage. One
departure followed by one arrival is an observed response; two empty-queue
steps with unchanged B is scientific no-response. Any exception, delayed or
incomplete chain, residual queue, or other B change is operational null. B has
no causal flux route, background update, balancing operation, or topology
integration during this window.

Future I05 freezes only `analysis_arithmetic_delta`. I06 must independently
admit a response amount at least 1024 times both the `1e-12` floor and the
largest relevant ULP, require finite canonical-JSON roundtrip, and keep every
runtime/restoration/continuation tolerance below `r/1024`.

The corrected pure analyzer accepts one mode at a time and derives candidate,
private, and controller causal status from masks, source arrivals, call
provenance, native packet lineage, configurations, and receipts. It never
trusts authored pool/controller booleans. Focused validation passed 19/19
checks and 15/15 pure tests with zero PyGRC model, null, candidate/control, or
graph mutation. `P2-I2-I04-REVIEW-READY` is restored, but owner acceptance and
CAL-PRE passage remained pending at the historical I04R1 boundary. I04R2 and
DEC-026 now own progression and gate passage.

#### 3.2.8 I04R2 conditional machine-invariant projection

I04R2 is a candidate-free integrity closure, not another conceptual comparator
review and not an I05 execution. The conditional owner review accepts I04R1's
semantic correction subject to exact machine confirmation.

For every mode/seed/physical-order tuple, candidate, leave-q1, and leave-q2
must all be scientifically valid before the strongest-marginal comparator can
be selected. One invalid arm makes the tuple nonevaluable; no surviving arm may
stand in. Future I05 must exercise this same route from three raw synthetic
responses through max selection, pairing, denominator floor, normalized
margin, serialization, and reconstruction.

I06 must prove every diverted contribution preserves source debit/activity,
amount/type, timing and queue opportunity, support/capacity consequence, route
cost where applicable, responder opportunity, B baseline, and response policy.
The inert sink must be absent from P, H_P, M_H, B, B_ref, response masks,
producer eligibility, and every continuation-relevant state. A mode unable to
realize this boundary cannot register a weaker comparator.

The registered response gain must equal the expected native arrival gain
within a separately registered runtime tolerance. B_before and B_after must lie
inside a registered native coherence domain, and retained configuration/source
receipts must exclude clipping, saturation, projection, budget correction, or
other arrival transformation. The current admitted source semantics are
identity packet-amount addition; changing that semantic reopens I04.

Scientific zero remains available only after evaluation ID, producer
invocation, exact two step-event identities, empty pre/post queues, absence of
window contamination, unchanged B, and absent response lineage all validate.
Repeated-S1/S2 stays non-gating; non-top order panels stay independently
classifiable; and causal status remains receipt-derived. I04R2 performs only
static validation and pure tests and returns for explicit owner acceptance.

The focused I04R2 verification passed 16/16 checks and 7/7 pure tests, with a
byte-identical reconstruction and zero PyGRC, matched-null, candidate, or
control invocations. It confirmed all-or-none three-arm evaluability,
within-tuple maximum scope, diversion/noninterference duties, identity arrival
gain inside an I06-registered finite domain, window-before-zero receipts,
non-gating repetition, independent order classification, and receipt-derived
causal status. It also found and corrected one substantive implementation gap:
the I04R1 future calibration entry point had bypassed the strongest-marginal
path. The I04R2 entry point now builds raw candidate/q1-only/q2-only envelopes
and calls the exact primary analyzer, then enforces governed-output readback and
byte-identical JSON reconstruction. This is machine-preregistration integrity,
not a calibrated resolution or operational-hypothesis outcome.

#### 3.2.9 I05 single-invocation authorization projection

This projection governs permission construction only. The authorization must
bind accepted I04 commit
`b7b008c402d837b529962a1a5edb062927939d28`, DEC-026, the owner-acceptance
record, and the exact active I04R2 machine policy, analysis implementation,
calibration policy, calibration entry point, and machine preregistration
identities. It may authorize exactly one governed arithmetic-null invocation
and must keep candidate execution false.

Construction and validation have a zero-invocation budget. They may call only
the frozen I04R2 authorization validator, not the calibration builder or entry
point, PyGRC, a synthetic-null generator, or any candidate/control path. The
governed output must remain absent. A byte-reconstructed validation result can
establish only that one unconsumed permission is well formed; it cannot assign
`analysis_arithmetic_delta`, modify the metric sheet, pass CAL-GATE, or affect
any operational-hypothesis projection. Consuming the permission is a separate
future action.

#### 3.2.10 I05A execution-safety audit projection

I05A is a pre-acceptance, zero-null-execution audit prompted by the owner review
of the authorization candidate. It asks whether the existing machine path
already makes the permission genuinely single-use by consuming it atomically
before governed work, treating a failed attempt as consumed, and refusing
concurrent or later starts. It also asks whether immediate preflight binds the
new committed RCAE authority containing acceptance and the I05 freeze—not only
the earlier I04 commit—together with exact code, output, environment, command,
candidate-exclusion, and clean-authority identities.

Finally, I05A distinguishes output reconstruction from null regeneration. A
valid reconstruction path may only read, parse, canonicalize, and compare the
retained output. It must retain separate counts for one attempted null run,
zero reconstruction generations, one output readback, consumed authority, and
a refused second invocation. Absence of any mechanism blocks proposed DEC-027;
it cannot be inferred from authored booleans, repaired silently, or interpreted
as an operational-hypothesis result. Static audit passed only the existing
identity/output/candidate guards, one-build readback-only reconstruction, and
zero-execution boundary. It failed attempt consumption, concurrent exclusion,
retry identity, committed-I05 preflight, and retained consumption/count/refusal
receipts. Proposed DEC-027 therefore fails closed. I05A changes no execution
source and runs no null, PyGRC model, candidate, or control.

#### 3.2.11 I05B one-shot correction projection

DEC-028 authorizes only an I05-owned correction of the five I05A safety
blockers. I05B may add one governed wrapper, one one-shot policy, atomic
permanent claim/final receipts, and zero-null safety validation. Accepted I04R2
estimator, analysis, comparator, calibration-policy, preregistration, and test
bytes remain immutable.

The corrected path must consume exactly one attempt through exclusive creation
before calling the accepted builder, permit zero infrastructure retries, and
leave the claim present after success, ordinary failure, or crash. At runtime
it must accept the expected committed HEAD as a post-commit launch argument,
prove that HEAD contains owner acceptance plus every required I05/I04 authority
blob with current-byte equality, reject dirty index/worktree authority state,
and record interpreter and normalized-command identity. This binds the future
committed I05 authority without an impossible self-reference inside a file in
that commit.

The accepted builder may be called once only during a later separately
authorized invocation. I05B validation calls it zero times. Reconstruction is
retained-output read/parse/canonical comparison only, with distinct attempt,
generation, readback, consumption, and second-refusal facts. I05B creates no
null, PyGRC, candidate/control, calibration, or operational-hypothesis evidence
and returns uncommitted for owner review. The correction passed all ten focused
tests and 12/12 machine checks with byte-identical validation reconstruction;
the owner-acceptance record, claim/final receipts, and governed output remain
absent.

#### 3.2.12 I05B acceptance-and-launch authority projection

The project owner accepts I05B and authorizes retention of its complete
authority package, but does not thereby authorize the arithmetic-null
invocation. The committed package must therefore contain an immutable machine
owner-acceptance record with `owner_acceptance=true`,
`commit_authorized=true`, and `null_invocation_authorized=false`. A distinct
10.4 launch record with `null_invocation_authorized=true` is required before
the wrapper may create the permanent attempt claim or call the accepted I04R2
builder.

Both records must be committed in the exact runtime `HEAD`, byte-equal to the
clean working tree, and bound to the authorization, wrapper, policy, and
unchanged I04R2 identities. The split changes only execution authority
mechanics: it does not change the one-attempt/zero-retry rule, estimator,
comparator, calibration semantics, reconstruction route, or scientific
status. Acceptance/commit packaging executes zero builders, nulls, PyGRC
models, candidates, and controls; `P2-I2-CAL-GATE` remains closed.

#### 3.2.13 I05 governed arithmetic-null execution projection

After accepted I05B commit
`c1f821dfd543d10d8555ddf2b52dbd56dfa76c13`, the project owner separately
authorizes 10.4. The activity may add and commit only the exact launch record
already required by the accepted wrapper, then consume the permanent claim and
call the accepted I04R2 builder once. Infrastructure retries remain zero. The
claim, final receipt, and governed output are retained even when the result is
arithmetic-only and scientifically outcome-free.

The output may assign only the preregistered analysis/serialization resolution
and designated frozen metric-sheet fields. Reconstruction reads, parses,
canonicalizes, and compares that retained output without another null builder
call or response-envelope generation. No PyGRC model, candidate/control cell,
runtime tolerance, response measurement, R01-R05 result, L02 support status, or
mode ranking is authorized. Execution and deterministic validation return as
`P2-I2-I05-EXECUTION-REVIEW-READY`; CAL-GATE remains closed until owner review.

#### 3.2.14 I05C pre-claim interpreter-path correction projection

The first final 10.4 preflight failed before claim because the accepted wrapper
passed the repo-relative `.venv/bin/python` command path through the generic
repository-data resolver, which rejects its legitimate resolution to
`/usr/bin/python3.12`. This is an infrastructure-path validation defect, not a
governed attempt: no claim, builder call, null output, final receipt, PyGRC,
candidate, or control operation exists, so the one permitted attempt remains
unconsumed.

The project owner's explicit direction “always use venv” authorizes the bounded
DEC-031/CHG-024 correction. It separates lexical repo-relative command-path
validation from resolved executable identity while requiring an active venv at
the exact repository `.venv` prefix and preserving the exact target binary
digest, CPython version, normalized command, clean committed authority, one-
attempt/zero-retry rule, and every scientific exclusion. It cannot change the
I04R2 builder, estimator, null inputs, output path, or evidence effect.
Thirteen focused tests and 12/12 byte-reconstructed machine checks now pass
with the real active repository venv. Accepted I04R2 bytes remain exact and the
claim, final receipt, and governed output remain absent. I05C is uncommitted and
review-ready; no further preflight or invocation is authorized before review
and retention of the corrected authority.

#### 3.2.15 I05D persisted-path portability-audit projection

The committed I05 execution evidence exposed filesystem-absolute path values,
and the project owner clarified that absolute paths are never allowed. This is
not limited to the newly observed output: I05D must statically audit the entire
current-tree P2-I2 artifact and implementation surface under the AE01
experiment before any portability correction is accepted. Filesystem-absolute
POSIX paths, drive-prefixed paths, home-expanded paths, and machine-local
absolute tokens embedded in persisted commands, values, receipts, reports,
tests, or source literals are violations. Normalized repository-relative POSIX
identities, stable logical external-repository IDs, content digests, and
non-path URIs remain valid.

I05D is an audit iteration, not an implicit repair. It freezes its scanner and
classification policy before inspection, uses the repository `.venv`, and
retains only repository-relative affected-file identities, field/line
locations, violation classes, counts, and digests. It must not reproduce a
forbidden path value in the new audit artifacts. Git history is not rewritten;
historical bytes are referenced only by commit and SHA-256. The audit performs
no null-builder, one-shot-wrapper, PyGRC-model, conformance, candidate/control,
calibration, response-envelope, or scientific operation. Its result returns as
`P2-I2-I05D-PORTABILITY-AUDIT-REVIEW-READY`; CAL-GATE stays closed.

The corrected audit is now review-ready: it scans 135 files and retains 312
value-redacted violations across 70 files. The dependency order is I05 active
execution/closeout first (32 violations, 11 files), I04/I05 authority next
(30, 13), I03 realization/conformance (201, 30), I01/I02 source/identity
(35, 10), then governance/navigation/shared projections (14, 6). No affected
artifact was corrected and no runtime or scientific path was invoked.

During I05D construction, the first discovery pass showed that the recursive
contracts and outputs selectors selected directories rather than nested files.
The selector form and explicit nested-file coverage guards were corrected
inside I05D before the retained inventory was created. This was not a separate
iteration and changed no classification, value-redaction, correction-group,
historical-boundary, runtime, scientific, or gate rule.

#### 3.2.16 I05E bounded portable-path correction projection

After owner acceptance of the exact I05D inventory, I05E may correct one
dependency-frozen group at a time, starting with the active I05 execution and
closeout package and returning every group for review before the next begins.
Repository locations become normalized repository-relative POSIX identities.
External repositories, interpreters, mounts, and environments are represented
by stable logical IDs plus exact digest, version, filesystem-capability, or
admission facts, never by persisted absolute locations or prefixes.

The original governed attempt, arithmetic-null output, and final-receipt bytes
remain historical evidence in Git and are referenced only by commit and digest.
Any current-tree portable derivative must identify itself as a projection and
must not impersonate the raw receipt. The permanent consumed-attempt guard,
one-attempt/zero-retry result, exact accepted I04R2 estimator, three-arm values,
per-seed/order margins, arithmetic delta, and candidate/runtime/PyGRC exclusions
cannot change. No second null invocation, reconstruction generation, or
scientific execution is permitted. CAL-GATE remains closed until the required
correction groups and I05 post-run metric artifacts are separately reviewed.

The project owner accepts the I05D inventory as the right next move and opens
only the first I05 correction group. It binds the eleven affected I05 files
listed in checklist section 10.4C plus consequential I05 identity/projection
records. The correction may normalize persisted locations, remove hard-coded
machine paths and shebangs, and create an explicit historical-to-portable
lineage. It cannot change the retained scientific numbers, reopen authority,
or begin the next correction group before review.

The first group is owner-accepted and commit-authorized. An exact input freeze
binds its eleven historical source hashes and 32 I05D findings. The current
tree uses repository-relative artifact identities, digest-bound logical
interpreter identity, logical repository-worktree mount identity, sibling-
derived PyGRC lookup, and shebang-free `.venv` invocation. Explicit projection
metadata and a lineage manifest connect changed current records to historical
Git bytes. Validation passes 10/10 with zero corrected-group violations; the
focused helper suite passes 13/13. The historical final receipt remains byte-
unchanged, the consumed claim remains present and read-only, and I05E performs
no governed execution or scientific operation.

Owner acceptance authorizes retention of this exact package and progression to
the next bounded correction group only after the commit. It does not pass
CAL-GATE or authorize a later correction before retention.

### 3.3 I03A state-carried realization binding

The review-ready state-carried authority is the
[I03A realization and discriminator contract](../contracts/p2-i2/i03a-state-carried-realization-and-discriminator-contract.json),
SHA-256 `aab25571bb5faa71c3213d3c1a27fa5659c3d4d2427a9b3fad8d087df71cc473`.
It selects a `pygrc_native_candidate`, not a supported native ecology result.

```text
S1, S2 = distinct native source-node roles
P      = one native node-coherence scalar and the complete causal C_P
q_i    = registered positive native packet contribution
U      = schedule_packet_departure + step departure/arrival into P
L      = native packet/event attribution, audit-only in I03A
V      = emit feedback over mask(P, B_ref) + model-owned producer + later packet
```

RCAE defines the role/access registry, native-call schedule, branch pairing,
and no-common-read guard. It does not compute P, reduce L into P, author the
response, or retain an external causal pool variable. The selected response
configuration leaves `expected_source_surface_digest` unset so contribution-
history identity is not a response condition. A matched neutral contact
supplies the later opportunity immediately before the fresh state read.

The state-carried interventions are:

- native write diversion: preserve source debits/amounts/times but route writes
  to K so P remains at reference;
- native carrier debit: after both writes, send native P-to-K flux before the
  encounter so response follows post-debit P;
- audit-only label permutation: alter only source-lineage strings; P and V
  remain invariant; and
- state-preserving order shuffle: complete S1-S2 and S2-S1 before encounter;
  equal P implies invariant V.

PyGRC still lacks a byte-identical-audit state clamp and first-class atomic
pool-write gate. I03A does not relabel those general audit capabilities as
adequate. It selects bounded native diversion/debit operations whose changed
intervention records are explicit. Failure to realize their matched boundary
at I06 reopens I03A and its realization class.

The guarded private competitor routes q1 to P1 and q2 to P2. Each retained
response may read exactly one private node through the same one-node mask
shape. No code path may read, sum, concatenate, dispatch over, or choose between
both partitions. Such a read is a mailbox/controller bypass, not a pool.

I03A freezes the nine operational profiles as follows:

| Projection | State-carried qualitative relation | Principal held-fixed variables | Fail-closed scientific effect |
| --- | --- | --- | --- |
| `H-L02-OP-01` | Two attributable arrivals alter one P; private controls retain two distinct nodes | marginal amounts, opportunity, topology class | no one-node P or source-addressed access blocks R01 |
| `H-L02-OP-02` | Native eligibility follows encounter-time P; combined P differs from reference and each original marginal P | neutral encounter, B_ref, support, policy class | no state-dependent later relation blocks R03 |
| `H-L02-OP-03` | Pure lineage-label permutation changes audit identity but not P or V | physical source nodes/routes, amounts, times, opportunity | label-sensitive response blocks R04 |
| `H-L02-OP-04` | Native diversion/debit changes the response relation; audit-only label change does not | contributor activity/attribution, support, unrelated opportunity | no carrier-intervention separation blocks R03/R04 |
| `H-L02-OP-05` | Each original marginal/removal branch differs from complete combined P; quantity-matched one-source equivalence remains an allowed claim limiter | opportunity, support, policy class | full original-marginal/repetition explanation blocks supported closure |
| `H-L02-OP-06` | Neither legitimate one-node private read recreates the common P relation | marginal writes, timing, support, one-node access opportunity | legitimate private reproduction or hidden aggregation blocks R04 |
| `H-L02-OP-07` | Direct/controller output equivalence does not recreate independently intervenable P or U-to-V chain | nearest output opportunity and marginal inputs | no causal distinction from bypass blocks R04 |
| `H-L02-OP-08` | Equal-P S1-S2, S2-S1, and audit-shuffled variants have invariant V | complete P, marginals, B_ref, neutral encounter, policy class | unexplained divergence blocks state-carried R03/R04; no mode switch |
| `H-L02-OP-09` | Relation remains when another eligible responder uses the same P access class | P/B_ref, contributions, reserve adequacy, policy class | invalid/unretained contrast leaves R05 unavailable only |

All seven cells and five L02 controls are bound in the machine contract. Exact
node/edge IDs, amounts, times, raw response, orientation, primary comparator,
resolution, aggregation, threshold, and seeds remain pending at their proper
I04/I06 gates. No candidate or calibration behavior informed this profile.

## 4. `H-L02-OP-01` — Common-pool constitution

**Projection:** At least two attributable contributions enter one declared
common non-private carrier rather than source-specific private partitions.

**Required operational distinction:**

```text
multiple attributable writes -> one C_P
not
multiple attributable writes -> private slots queried separately
```

**Primary traceability:** L02 support signatures 1–2; R01–R02;
`reference-pool`, `individual-contributions`, and `combined-orders`.

**Fail-closed effect:** no single carrier or no non-private access witness
blocks R01. Private contributor slots block the pool claim even when a combined
output exists.

## 5. `H-L02-OP-02` — Combined-carrier dependence

**Projection:** The registered later response depends on the mode-relevant
common encounter state, active history, or both.

The relation need not be nonlinear and need not implement an AND gate. It must
be carried by `C_P`, survive the registered causal distinctions, and not be a
post-hoc presence label or authored success value.

**Primary traceability:** L02 support signature 3; R03; selected primary metric
pairing plus mode-appropriate freeze/clamp and jointness interventions.

**Fail-closed effect:** absence of a carrier-dependent later response prevents
R03 and `supported_bounded_candidate`.

## 6. `H-L02-OP-03` — Attribution-only invariance

**Projection:** Changing arbitrary source labels while holding contribution
physics and the complete causal carrier identity fixed does not change the
later response within the frozen equality/resolution rule.

Contribution-operation reassignment is not a pure label permutation. Amount,
location, timing, or type changes may alter `C_P` and must be classified
separately.

**Primary traceability:** `AE01-L02-CTRL-02`; R04; audit-lineage side of the
causal factorization.

**Fail-closed effect:** label-dependent response exposes a mailbox, lookup, or
controller bypass and blocks R04.

## 7. `H-L02-OP-04` — Common-carrier intervention dependence

**Projection:** Blocking, freezing, or clamping the mode-relevant common
carrier component changes the registered response relation while contributor
activity, attribution metadata, unrelated opportunity, and support remain
matched as frozen.

The complementary audit-only intervention holds complete `C_P` fixed while
changing `L`; the response must remain invariant.

**Primary traceability:** `AE01-L02-CTRL-05`; R03–R04; pool-write freeze and
candidate-state/active-history clamp subconfigurations.

**Fail-closed effect:** failure to distinguish carrier intervention from
matched activity blocks common-carrier causal dependence.

## 8. `H-L02-OP-05` — Insufficient-repetition exclusion

**Projection:** The candidate relation is not fully explained by either
contributor alone, repeated P2-I1-style writes, or the preserved inherited
single-source carrier relation.

At least one jointness counterfactual must retain the inherited single-source
relation while removing joint pool constitution.

**Primary traceability:** D-039 `insufficient_repetition_case`;
`individual-contributions`, `contributor-removal`, and the selected closest
primary comparator.

**Fail-closed effect:** if the preserved single-source relation fully explains
the combined consequence, P2-I2 cannot close as
`supported_bounded_candidate`.

## 9. `H-L02-OP-06` — Private-partition exclusion

**Projection:** Equivalent marginal writes into source-specific carrier
partitions do not reproduce the candidate through a legitimate carrier-scoped
response path.

The registered substitution must preserve contribution quantities, timing,
support, opportunity, and equivalent access opportunity while removing jointly
constituted common state. The responder may not recreate the combined outcome
by independently consulting both partitions.

**Primary traceability:** D-039 private-partition exclusion;
`global-state-exclusion`; `AE01-L02-CTRL-04`; R04.

**Fail-closed effect:** reproduction by independent partition reads is mailbox
dependence and blocks R04.

## 10. `H-L02-OP-07` — Controller and direct-path exclusion

**Projection:** A direct-address or controller-assembled substitute may
reproduce an output, but it does not reproduce the attributable
source-to-common-carrier-to-response causal chain.

A centrally executed native update is not disqualified merely by code
location. The forbidden alternative assembles a value from contributor-
addressed records and supplies it directly to the outcome path without a
separately intervenable carrier.

**Primary traceability:** `global-state-exclusion`;
`AE01-L02-CTRL-04`; common `AE01-CTRL-05` and `AE01-CTRL-08`; R04.

**Fail-closed effect:** if the candidate cannot be causally distinguished from
the bypass, R04 remains blocked even when output values match the candidate.

## 11. `H-L02-OP-08` — Mode-specific order and shuffle relation

**Projection:** The registered order/shuffle relation follows exactly one
dependence mode selected before calibration:

- `state_carried`: variants preserving complete common encounter state are
  invariant; a divergent primary contrast must alter state, constitution, or
  carrier access rather than merely reorder an inactive audit history;
- `history_carried`: a history-altering shuffle preserving registered marginal
  quantities changes the active carrier history and should change the later
  response under the frozen relation; or
- `hybrid`: independently registered state and active-history interventions
  show their separately frozen relations.

`hybrid` is admissible only when state and active history are separately
declared, each has at least one intervention that changes it while matching the
other as closely as possible, and failure to separate them closes lower or
mixed rather than causing a post-outcome mode change.

**Primary traceability:** `combined-orders`, `pooled-history-shuffle`,
`AE01-L02-CTRL-03`; R03–R04.

**Fail-closed effect:** a relation inconsistent with the preregistered mode
blocks R03 or forces a lower/mixed classification. The mode cannot be changed
after outcomes.

## 12. `H-L02-OP-09` — Bounded contrast retention

**Projection:** The controlled shared-pool relation remains under one
preregistered capacity, contributor, or access-scope contrast within the frozen
variation boundary.

This contrast tests only bounded R05 retention. It does not establish general
pooling, recurrence, a reusable primitive, coordination, or resource economy.

**Primary traceability:** `access-capacity-contrast`; R05.

**Outcome reading:**

```text
supported:
  the relation remains under the registered contrast, permitting R05

not_supported:
  the relation does not remain; R05 is unavailable while valid lower rungs
  remain classifiable

blocked_or_incomplete:
  the contrast cannot be validly executed or interpreted; R05 is unavailable
```

**Fail-closed effect:** without a valid retained contrast, R05 remains
unavailable; lower completed rungs and observations remain classifiable.

## 13. Scope diagnostic — quantity-matched single-source replacement

This diagnostic is not a tenth operational support hypothesis and is not an
automatic pass/fail gate.

Repeated-S1 and repeated-S2 each supply both registered q operations, and each
branch is retained separately in q1-then-q2 and q2-then-q1 physical order.
Contribution physics, source-side cost/depletion, support, encounter state,
opportunity, B baseline, and the complete mode-relevant carrier are matched
where source-role physics permits. I06 must prove each source can emit both q
operations under the frozen symmetry duties before this diagnostic registers:

- complete-carrier equivalence is valid under a source-label-free realization
  and cannot alone fail R03;
- divergence may support a bounded contribution-structure observation; and
- neither relation establishes source complementarity, cooperation, or
  coordination without separately authorized evidence.

The diagnostic and its interpretation must freeze before candidate outcomes.

## 14. Realization-binding and freeze gate

### 14.1 I03A state-carried review gate

- [x] I01R1 and I02R2 retain the corrected capability and source-admission
  prerequisites.
- [x] `pygrc_native_candidate` and `pool_dependence_mode = state_carried` are
  selected without opening the later modes.
- [x] S1, S2, P, B_ref, E, A, B, K, P1, and P2 role meanings are bound while
  exact node/edge IDs remain correctly deferred to I06.
- [x] `C_P`, `L`, `q`, `U`, `V`, access witness, label exclusion, native
  diversion/debit, and private no-common-read guard map to admitted public
  interfaces and explicit RCAE declarations.
- [x] OP-01 through OP-09 map to all seven cells, all five controls,
  qualitative relations, held-fixed variables, ambiguity boundaries, and
  fail-closed effects.
- [x] Native gaps remain explicit and no RCAE causal producer, external pool
  state, history-carried profile, or hybrid profile is silently introduced.
- [x] Raw response, primary comparator, numerical resolution, threshold,
  aggregation, seeds, exact fixture, and provider freeze remain deferred.
- [x] No candidate or matched-null behavior informed the state-carried profile.

These checks satisfy `P2-I2-I03A-REVIEW-READY` only. They do not pass the
umbrella gate.

### 14.2 Umbrella staged-family gate

I03 may change this artifact to umbrella `realization_bound` only after I03A,
I03B, and I03C are separately frozen and owner-reviewed, and when:

- [x] I01/I01R1 retain the corrected source-current capability audit. Evidence:
  [I01 audit](../reports/P2-I2-I01-source-current-capability-audit.md) and
  [capability matrix](../contracts/p2-i2/i01-capability-matrix.json), with the
  [I01R1 closeout revalidation](../reports/P2-I2-I01R1-capability-audit-closeout-revalidation.md).
  The custom candidate-shaped probe is quarantined, CAP-04 is inadequate, and
  this checks the audit prerequisite only; it does not bind a realization or
  dependence mode.
- [x] I02 retains exact source-admission or non-admission dispositions.
- [x] Each staged mode retains its realization class and source/runtime
  boundary. I03A is native; I03B and I03C are minimally producer-assisted,
  with distinct one-component and joint-response boundaries.
- [ ] `C_P`, `L`, `q`, `U`, `V`, sources, access witness, and contribution
  operations map to exact scientific runtime interfaces. All three I03 modes
  are runtime-conformant and owner-accepted, while exact topology,
  contribution values, routes, response configuration, and cell bindings
  remain I06 work.
- [x] All three owner-directed dependence-mode profiles are separately bound
  and owner-accepted without rewriting one another; compact I03F was accepted
  under DEC-020.
- [ ] Every projection maps to exact cells, controls, interventions, causally
  held-fixed variables, qualitative expected relations, allowed scientific
  ambiguity, and fail-closed effects.
- [x] The mode-specific jointness and private-partition counterfactuals are
  executable in bounded conformance; scientific resolution remains later.
- [ ] Producer necessity/minimality/withdrawal and external-state identity are
  complete when applicable. I03B freezes the minimal adapter and composite
  identity duty and passes bounded conformance; I03C freezes the same minimal
  missing operation inside a distinct joint P+H_P design, with runtime proof
  and later exact registration still pending.
- [x] I04R1 corrected and selected the primary response, symmetric carrier-
  changing comparator, non-failing scope diagnostic, and evidence-derived
  machine relations from frozen semantic authorities before any matched-null
  or candidate outcome; candidate outcomes remain absent.
- [x] I04R2 confirmed the complete machine projection 16/16 with 7/7 pure
  tests, corrected the future-I05 entry point to traverse the raw three-arm
  primary estimator, and retained zero calibration or scientific effect.

Umbrella I03 passed under DEC-020. I04R1 imports all three causal profiles
unchanged and freezes their corrected fixed-window measurement, analysis-only
resolution rule, numerical orientation, symmetric strongest-leave-one primary
comparator, non-failing quantity scope diagnostic, aggregation, missingness,
evidence-derived control evaluation, candidate-blind arithmetic null, and
stopping rule. Shared extraction identities preserve independently mode-
indexed expectations and dispositions. The corrected candidate-free package
is owner-accepted under DEC-026 as the sole I04 progression authority.
Original I04 and I04R1 remain immutable historical artifacts rather than
parallel active preregistrations. CAL-PRE passage opens only construction of a
separate exact one-invocation I05 arithmetic-null freeze. CHG-019 retains a
byte-reconstructed candidate for owner review under proposed DEC-027; no
authority is active, no null or candidate operation has occurred, no commit is
authorized, and CAL-GATE remains closed.

Neither status transition supplies evidence for any operational projection.

If no bounded realization can preserve one or more mode-specific
discriminators, I03 may instead set
the artifact status to `prerequisite_classified`. That status does not pass the
discriminator or calibration gates; it preserves which projections could not
be instantiated and supports only the reviewed earlier-stop path toward a
possible `blocked_missing_prerequisite` terminal classification.

## 15. Claim boundary

Passing every operational projection can support only the frozen
`AE01-H-L02` hypothesis within its boundary rungs, support status, metric
relation, realization class, terminal state, and maximum claim:

```text
bounded shared-pool co-conditioning demand pattern
```

The family cannot establish collective memory, communication, resource
economy, cooperation, coordination, agency, organism identity, a native shared
pool primitive, motif, regime, life, cross-lane recurrence, or N31+ selection.
