# P2-I2 Operational Hypothesis Projections

**Status:** evidence-bearing through owner-accepted I09; review-ready I09A
corrects the I10-found estimator bypass at 24/24 with no raw-evidence or
control-disposition change. CONTROL-GATE awaits owner reconciliation and
RECON-GATE remains closed; no scientific interpretation is assigned.
The accepted C02 manifest retains 234/234 evaluable mode-indexed terminals.
I09 resolves only the already-frozen common and L02 control relations from
those retained receipts. The three modes remain separate and unranked;
`R01`–`R05`, the lane support status, and terminal interpretation remain
unassigned until their later declared stages.

**Lane:** `AE01-L02`

**Frozen hypothesis authority:** `AE01-H-L02`

**Evidence effect:** subordinate projection plus retained realization
conformance, candidate-blind arithmetic resolution, registered I08 raw
evidence, and I09 control resolution; no L02 support/falsification, mode
ranking, terminal interpretation, or lane scientific result

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
| `source_set` | At least two distinguishable attributable source carriers/events | Owner-accepted I06 registration binds exact native S1/S2 node and route IDs while preserving source-attributable receipts | I03A/I03B/I03C concept; accepted DEC-042 exact registration |
| `C_P` | One auditable non-private causal carrier identity | I03A: native P coherence; I03B: one RCAE-owned ordered `H_P` plus native output `M_H`, while P is excluded from V; I03C: separately causal native P plus active `H_P`, jointly read through P and `M_H` | I03A/I03B/I03C |
| `L` | Audit-only source lineage and attribution projection | All modes: native packet/event/surface/lineage records; I03B/I03C use row identity only for active-history admission/idempotency, never as a response input | I03A/I03B/I03C |
| `q` and `U` | Contribution properties and common-carrier transition | I03A: native arrival into P; I03B: source-label-free token append then native `M_H` materialization; I03C: the same physical contribution advances native P and the separately intervenable active history | I03A/I03B/I03C concept; I06 numeric/exact |
| `V` | Carrier-scoped read, susceptibility, or continuation path | I03A: native P/B_ref feedback; I03B: native M_H/B_ref feedback after adapter handoff; I03C: one native `[P,M_H]`/`[B_ref]` feedback path after adapter handoff; owner-accepted I04R2 retains the shared downstream consequence as native B-target coherence gain over one fixed two-step response window | I03A/I03B/I03C causal read; I04R2 accepted response authority; I06 exact masks/policy |
| `access_witness` | Non-private carrier access without contributor addressing | I03A: one-node P mask; I03B: one common H_P/M_H path; I03C: one common P+H_P identity read through `[P,M_H]`, available to any registered eligible A-role responder | I03A/I03B/I03C concept; I06 exact |
| `primary_response` | One oriented raw later-continuation response | Owner-accepted I04R2 freezes fixed-window native B-target coherence gain, identity-oriented with higher aligned and binary-like zero/one-packet semantics; shared extraction does not merge modes | I04R2 accepted; I06 exact registration |
| `primary_comparator` | Closest insufficient-repetition alternative | Owner-accepted I04R2 freezes the stronger of two symmetric carrier-changing leave-one-admitted branches within each mode/seed/physical order; repeated-S1/S2 remains an equivalence-permitted non-gating scope diagnostic | I04R2 accepted; I06 exact registration |
| `control_relations` | Signed invariance/divergence and fail-closed effects | I03A/I03B/I03C qualitative relations plus I04R2 numerical and evidence-derived causal-chain rules are frozen; I05J retains `analysis_arithmetic_delta = 1e-12` as arithmetic/serialization resolution only | I03A/I03B/I03C, I04R2, and I05J resolution complete; I06 exact controls |
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
`system-interpreter:python3.12`. This is an infrastructure-path validation defect, not a
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

#### 3.2.17 I05F I04/I05 authority-dependency portability projection

After the accepted I05D/I05E package is retained at `6dd6898`, I05F may correct
only the audit group `i04_i05_authority_dependencies`: 30 findings in 13 files.
The group includes I04, I04R1, and I04R2 preregistration/policy/validation
records plus their experiment-local validators and calibration-source
surfaces. It does not reopen any accepted scientific choice or execution
authority.

Historical I04/I04R1/I04R2 bytes remain authoritative provenance identified by
commit and SHA-256. Any changed current-tree JSON must declare itself as a
portable projection and be mechanically reconstructable from its historical
source through frozen path-only transformations. Repository sources become
repository-relative POSIX identities; PyGRC sources become sibling-derived
logical repository identities plus admitted revision/digest facts; scripts
lose machine-selecting shebangs and remain `.venv`-invoked.

The accepted I04R2 estimator, comparator, complete-arm rule, fixed response
window, B-gain rule, calibration inputs, candidate quarantine, and CAL-PRE
meaning cannot change. Existing raw I05 claim/output/final hashes are not
rewritten. Consequential lineage may identify the historical I04 hashes and
their current projections, but cannot silently substitute new hashes into raw
receipts. I05F performs no calibration builder, arithmetic null, one-shot
wrapper, PyGRC model, candidate/control, conformance, or scientific operation.
It returns uncommitted for review with CAL-GATE and later groups closed.

I05F is technically complete and uncommitted, but process-blocked. Its final
`.venv` validation passes 10/10: all 13 source/current identities are bound,
all eight JSON projections reconstruct mechanically, all five Python
corrections are confined to frozen path-portability surfaces, current PyGRC
source digests match, accepted I04R2 historical bytes remain addressable, and
the I05 output projection, consumed claim projection, and raw final receipt
remain byte-unchanged from `6dd6898`. The exact group moves from 30 findings to
zero.

However, the freeze allowed three static-validation invocations and actual
preparation used 13 `.venv` Python starts: eight JSON syntax checks, one compile
check, three validator starts, and one scanner diagnostic. Two validator starts
failed closed and wrote no artifact; the third alone retained the passing
technical result. Every start remained zero-builder and zero-runtime, but the
numeric process ceiling was exceeded. The original freeze is not rewritten,
and I05F requires explicit owner disposition before acceptance or commit. This
has no operational-hypothesis or scientific effect.

Under DEC-035, the project owner's `+1` authorizes one additive I05F-owned
closeout record accepting this process-only deviation in place. The record
must retain both the ceiling and the complete 13-start ledger; it cannot
rewrite the freeze or trigger any Python/validator rerun. This authorization
has no operational-hypothesis effect, does not accept the complete I05F
package, and does not authorize commit or a later correction group.

After the closeout record was retained, the project owner further directed
that completion also constitutes full I05F acceptance and commit authorization
under DEC-036. This changes only retention authority: the 13-versus-three
deviation remains explicit, the original freeze remains immutable, no
technical validation is rerun, no later group opens, and no scientific or
operational-hypothesis conclusion follows.

#### 3.2.18 I05G third bounded portability correction

After accepted I05F is retained at `99c64dd`, the project owner directs the
third bounded portability group to begin. I05G initially authorizes only a
read-only resolution of the exact third correction group from the accepted
I05D inventory and construction of its immutable input freeze. No affected
file may change before the group name, paths, counts, source digests, allowed
transformations, historical boundary, invocation ceilings, outputs, and review
stop are retained.

The accepted policy order resolves the group as
`i03_realization_and_conformance`, with 201 findings across exactly 30 files.
Its slash-leading I03F authority and operational-projection values are JSON
pointers rather than filesystem locations. Their portable projection must use
explicit segment arrays with byte-equivalent target resolution. Historical
checkout, environment, command, temporary-output, attachment, report, and
script identities become repository-relative or logical identities while the
raw I03 conformance bytes remain addressable at parent commit `99c64dd`.

I05G is representation-only. It cannot change an accepted realization,
restoration identity, estimator, comparator, response, calibration value,
gate, evidence meaning, operational profile, or scientific status. Any current
changed artifact must remain mechanically linked to accepted historical bytes.
No builder, arithmetic null, one-shot wrapper, PyGRC model, candidate/control,
conformance, or scientific operation is authorized. The fourth correction
group, metric-sheet freeze, CAL-GATE, and I06 remain closed.

The completed uncommitted I05G projection passes 10/10 static checks. It binds
all 30 accepted source files to 30 portable projections, closes the 201
accepted path findings to zero, reconstructs the 20 JSON and 10 text changes
exactly, converts 105 pointer occurrences to ordered segment structures, and
proves identical resolution for all 44 indexed contract targets. The raw I03
bytes remain at commit `99c64dd`; no accepted realization or conformance
meaning is rewritten.

Two of the three allowed `.venv` validator starts were used. The first failed
closed before output on an incomplete validator-only attachment mapping; the
second passed and alone retained a result. Every other Python, PyGRC, model,
conformance, candidate/control, calibration, null/wrapper, and scientific
count is zero. These are portability-process facts only and have no
operational-hypothesis or L02 evidentiary effect. I05G now stops uncommitted for
explicit owner review; it does not authorize its own commit or a fourth group.

The project owner subsequently accepted I05G, authorized its commit, and
directed progression to the fourth bounded group. The accepted package is
retained at `62882ef`. This changes only progression authority; it does not
turn I05G portability validation into scientific evidence or pass CAL-GATE.

#### 3.2.19 I05H fourth bounded portability correction

After accepted I05G is retained at `62882ef`, the project owner directs the
fourth accepted-audit portability group to begin. I05H initially authorizes
only checklist/hypothesis-first read-only resolution of the exact fourth group
and construction of its immutable input freeze. No affected file may change
before the group identity, source paths and digests, finding classes and
counts, transformations, historical boundary, invocation ceiling, expected
outputs, and uncommitted review stop are retained.

The accepted I05D order resolves the fourth group as
`i01_i02_source_and_identity`: 35 findings across exactly 10 files, comprising
24 embedded machine-local absolute tokens and 11 exact POSIX absolute values.
The scope contains four historical I01/I02 input or validation JSON artifacts,
three historical reports, and three I02 validation/manifest Python sources.

I05H is representation-only. Raw accepted bytes remain addressable at the
accepted parent commit and by SHA-256. Portable projections may alter only
checkout, interpreter, command, attachment, or other machine-local location
representation and the corresponding static path-resolution machinery. They
cannot change an I01 capability conclusion, I02 source-admission or identity
authority, reset-baseline result, PyGRC source meaning, restoration boundary,
later mode realization, estimator, response, calibration, gate, or evidence
status.

No builder, arithmetic null, one-shot wrapper, PyGRC model, candidate/control,
conformance, or scientific operation is authorized. Any Python validation must
use `.venv/bin/python` under a separately frozen ceiling. The fifth correction
group, metric-sheet freeze, CAL-GATE, and I06 remain closed.

The completed uncommitted I05H projection passes 10/10 static checks. It binds
all ten accepted source files to ten portable projections, closes the 35
accepted findings to zero, and reconstructs the four JSON, three report, and
three Python changes exactly. The only active-source changes are three
machine-selecting shebang removals and five substitutions from a fixed POSIX
temporary root to `tempfile`'s system-selected temporary directory. Raw I01/
I02 bytes remain at commit `62882ef`; all source-admission, identity-authority,
reset-baseline, capability, and quarantine meanings are unchanged.

One of the three allowed `.venv` validator starts was used and passed on its
first attempt. Every other Python, PyGRC import/model, historical validator or
manifest-builder, candidate/control, calibration, null/wrapper, conformance,
and scientific count is zero. These are portability-process facts only and
have no operational-hypothesis or L02 evidentiary effect. I05H stops
uncommitted for explicit owner review; it does not authorize its own commit or
a fifth group.

The project owner subsequently accepts I05H, authorizes its commit, and asks
for an exact remaining-file check before deciding whether two residual groups
should be combined. The accepted package is retained at `1279e17`.

#### 3.2.20 I05I fifth/final portability correction

The accepted I05D order and current P2-I2 audit boundary agree that only one
residual group exists: `p2_i2_governance_navigation_and_shared_projections`,
with 14 embedded machine-local tokens across six files. There are not two
residual groups to combine. The project owner directs that this check be folded
into the fifth/final correction instead of creating a standalone review.

Before the first I05I validator start, owner inspection identifies two more
source files that the literal-token scanner could not classify:
`p2_i2_i05g_validate.py` reconstructs the historical RCAE and graph roots, and
`p2_i2_i05h_validate.py` reconstructs the historical graph root. These three
constructed-root surfaces are equally forbidden. They are added to the same
final correction, not a new iteration. The second failed-closed I05I start then
shows that the expanded guard also detects a constructed historical shebang in
`p2_i2_i05f_validate.py`. That ninth source is admitted before the final
validator start. I05I therefore binds nine historical sources at commit
`1279e17`. The three
self-governance files necessarily receive checklist/hypothesis/decision
declaration before freeze, but their correction source remains the accepted
commit bytes and no non-governance affected file may change before the exact
freeze. The final projections may change only absolute-path, interpreter,
temporary-output, graph-checkout, command, or portable path-resolution
representation plus additive lineage/governance needed to describe the
correction.

I05I cannot change any hypothesis, decision, calibration, gate, source,
realization, reset, restoration, evidence, or navigation meaning. It cannot
import PyGRC, execute a model, invoke a historical validator, run a candidate/
control/conformance/scientific path, freeze the metric sheet, pass CAL-GATE, or
edit older P2-I1/shared AE01 files outside the accepted P2-I2 boundary. Static
validation must use `.venv/bin/python` under a frozen ceiling. The completed
correction must stop uncommitted for owner review.

The completed uncommitted I05I projection passes 10/10 static checks. It binds
the six accepted-audit sources plus three validator constructor sources to
nine portable projections, closes the terminal 14 literal findings and four
constructed absolute surfaces to zero, and scans the complete current P2-I2 audit
scope to zero findings. The three ordinary non-governance projections
reconstruct exactly; all three validator sources contain no constructed absolute
binding; the three
self-governance diffs are bounded to the I05H acceptance, DEC-039/CHG-032/I05I
declaration/closeout, and frozen path substitutions. Raw source bytes remain
at commit `1279e17`.

All three allowed `.venv` validator starts are used. The first fails
closed before output because the initial policy carried three stale pre-I05H
governance digests instead of the exact `1279e17` source bytes; the policy,
freeze, and lineage are corrected in place. The second fails closed at I05I-04
after finding the I05F constructed shebang; that source is added and corrected.
The third passes. Every
other Python, PyGRC import/model, historical validator/manifest-builder,
candidate/control, calibration, null/wrapper, conformance, and scientific count
is zero. These facts have no operational-hypothesis or L02 evidentiary effect.
I05I stops uncommitted for owner review and does not itself pass CAL-GATE.

The project owner subsequently accepts I05I and authorizes its retention at
commit `b5d0acb`, then directs work to return to 10.4 and 10.4A.

#### 3.2.21 I05J arithmetic-resolution and metric-sheet closeout

I05J distinguishes the already completed I05C/10.4A interpreter correction
from the three still-open 10.4 metric obligations. It may close only the
candidate-blind analysis-arithmetic resolution produced by the consumed I05
attempt. It cannot rerun the null, import PyGRC, execute a candidate or control,
infer a runtime/restoration/measurement tolerance, rank a dependence mode, or
change the base `AE01-L02` metric sheet.

The accepted governed output contains five seeds by two physical-order strata.
The common native `freeze-resolution` interface requires exactly one matched-
null margin for each unique calibration seed. I05J therefore freezes a bounded
input projection: for each seed, take the maximum absolute normalized margin
across its two required physical orders. The projection preserves the exact
global estimator because the maximum of those five per-seed envelopes equals
the maximum across all ten retained margins. The full order-stratified output
remains the authoritative provenance; the projection has no scientific effect.

After checklist/hypothesis declaration, I05J must bind the base sheet, accepted
I04R2 estimator policy, portable I05 output and lineage, I05I closeout, native
tooling/schema identities, exact output paths, and invocation ceilings before
generation. One `.venv` native `freeze-resolution` start may generate a
schema-valid lane-local metric-calibration record and frozen metric sheet.
Static validation must reconstruct the projection and both generated artifacts,
verify that only designated resolution fields differ from the unchanged base
sheet, and preserve narrow/robust language solely as a relation to the frozen
resolution. The result returns uncommitted for owner review; CAL-GATE and I06
remain closed until that review.

#### 3.2.22 I05JA native dependency correction

The first and only start admitted by the original I05J freeze fails closed
before output because the repository `.venv` lacks the common tooling contract's
pinned `jsonschema==4.26.0` dependency. Neither metric artifact exists, and the
null, PyGRC, candidate, control, conformance, runtime, and scientific counts
remain zero.

I05JA preserves the original freeze and failed start rather than silently
rewriting its one-start ceiling. It may install only `jsonschema==4.26.0` into
the repository `.venv`, verify that exact version, and authorize one native
`freeze-resolution` retry with unchanged inputs, outputs, and semantics. The
later static validator must bind the original freeze, failure record, correction
freeze, installed dependency identity, two total native starts, and one failed-
closed pre-output start. I05JA adds no null retry and does not alter CAL-GATE or
I06 authority.

Before owner acceptance, a read-only closure audit finds no scientific or
metric defect but identifies incomplete process accounting and stale current-
status projections. Because I05J remains uncommitted and unaccepted, the owner
directs that this be amended inside I05J rather than opened as another
iteration. The amendment must preserve the original I05J and I05JA freezes,
native outputs, and generated 11/11 validation. It may add one explicitly
authored process/package closeout that records the two dependency-install
process starts, native and validator attempt history, final report and package
hashes, and the distinction between machine-validated artifacts and reconstructed
process history. It may also synchronize current-status projections through
the experiment and master navigation surfaces. No null, dependency install,
native generation, validator, PyGRC, candidate/control, conformance, runtime,
or scientific rerun is admitted by this amendment.

The owner subsequently accepts the complete amended I05J/I05JA package and
authorizes its commit. That acceptance passes `P2-I2-CAL-GATE` and authorizes
only the construction of I06 registration artifacts; it does not begin I06 or
authorize any candidate, control, conformance, runtime, or scientific execution.

#### 3.2.23 I06 exact three-mode registration declaration

The owner now directs I06 under the passed CAL-GATE. I06 must retain and
register state-carried, history-carried, and hybrid as three distinct required
modes. It may select no winner, drop no mode, import no conformance outcome, and
collapse no mode-specific causal or restoration identity into a shared scalar.

I06 begins with a read-only source/runtime preflight. It must bind the current
clean PyGRC checkout, active repository `.venv`, imported package source,
accepted I02R2 restoration providers, and the exact structural active-history
adapter before selecting or materializing registration values. Source drift,
dirty state, unavailable public calls, or an inadequate restoration boundary
fails closed for review rather than silently changing the admitted realization.

That preflight is complete. One initial diagnostic start omitted the already
declared external-checkout `PYTHONPATH` and therefore failed to import PyGRC;
it changed no environment and instantiated no model. The corrected declared
binding passes at admitted revision `83e3a3...` with a clean checkout, 31/31
source hashes, 31/31 public callables, active `.venv`, and exact locked direct
dependencies. PyGRC remains source-bound from the admitted checkout rather than
installed into the environment.

The structural adapter audit finds one prohibited implementation carryover:
`RCAEActiveHistoryAdapterV1` hardcodes the I03 fixture comparator
`math.isclose(..., abs_tol=1e-12)` in readout materialization. I03 quarantine
explicitly rejects that comparator, while I04 requires every runtime tolerance
to be independently registered rather than inferred from analysis delta. I06
therefore may create one minimal adapter revision that adds an explicit
materialization-tolerance configuration/restoration field. The revision must
otherwise preserve the accepted token schema, fold, intervention, native packet
handoff, and no-response-production boundary. Any broader causal change reopens
I03 rather than entering registration silently.

The compact I06 artifact stack is one policy/input freeze, one exact three-mode
registration bundle, one manifest, one control-resolution-index template, one
validator/validation artifact, and one report. The bundle must bind per-mode
roles, topology, carrier/write/read mapping, exact seven-cell/five-control
matrix, response/comparator, numeric domain and runtime tolerance, contribution
physics, timing/opportunity matching, pool-economy dispositions, seeds,
attempts/resources, contamination checks, branch points, and complete native-v2
or native-v2-plus-adapter restoration identity.

Native PyGRC owns every adequate state, packet, feedback-response, scheduling,
and restoration transition. Only the already accepted minimal active-history
adapter may produce the missing common-history carrier and native readout for
history-carried and hybrid. If exact registration requires that adapter to read
success/response state, compute the joint response, schedule the later response,
or hide a one-sided restoration operation, the affected realization fails
closed and I03 must be reopened.

Every exact I03 conformance value, branch/topology identity, response
observation, outcome, comparator, and evidence/restoration digest is prohibited
as I06 registration input, including trivial serialized reuse. Structural code,
causal form, public APIs, and accepted producer/restoration obligations may be
imported. I06 may perform only baseline-only composite restoration binding and
negative mismatch checks after its exact freeze; it may not admit an S1/S2
contribution, active-history token, neutral encounter, response evaluation,
candidate/control cell, comparator window, or scientific operation.

I06 initially returns uncommitted for explicit owner review. Its exact package retains
all three unranked modes on one matched 23-node/16-edge opportunity topology,
with separate carriers/masks, seven cells, 26 exact subconfigurations, five lane
controls, complete response/comparator identities, and an outcome-free control
index. The I06-owned history-adapter revision changes only the quarantined
hardcoded materialization comparator: tolerance is an explicit configuration
and restoration-identity field, while the accepted token fold, intervention,
native handoff, and no-response-production boundary remain unchanged.

The sole output-producing baseline-only validation passes 14/14. Original,
loaded, and reset composite digests agree independently for state-carried,
history-carried, and hybrid, and all nine registered mismatch/one-sided/repeat
cases refuse. The run admits no contribution, active-history token, neutral
contact, response evaluation, candidate/control cell, comparator, or scientific
window. A terminal scan then corrects only the validator's portability guard,
replacing literal rejection patterns with generic absolute-token and `*_ROOT`
placeholder detection; one no-model static check passes and the consumed
baseline validation is not rerun. It therefore changes no OP/R01–R05
disposition and supplies no L02 result. REG-GATE remains closed and I07 remains
unauthorized until explicit owner acceptance.

#### 3.2.24 I06A registration review-closeout declaration

Owner review of the uncommitted I06 package identifies two potential blockers:
the registered AdapterV2 requires conformance authority relative to I03-tested
AdapterV1, and the final manifest must preserve exact two-stage provenance
across the portability-guard correction rather than imply that current source
produced the historical 14/14 output.

I06A may retain source/AST equivalence, pure no-model adapter tests, exact
historical-byte reconstruction, static manifest transition proof, and bounded
confirmation of tolerance domain, diversion/admission purity, mode isolation,
and retry semantics. It may add only provenance/validation artifacts and
clarifying bundle fields that do not change I06 causal or numeric semantics. It
may not construct a PyGRC model, rerun baseline validation, admit a contribution
or history token, evaluate a response, execute any cell/control/comparator, or
assign scientific evidence. REG-GATE remains closed and I07 unauthorized until
the complete I06/I06A package receives explicit owner acceptance.

The first I06A no-model validation start subsequently fails closed before any
output. The frozen retry policy correctly names six byte-identical retry-input
classes, but the authored validator asserts seven. Before that assertion it
uses eight fake packet-interface instances and imports no PyGRC; it reaches no
candidate, control, baseline rerun, response, comparator, or scientific work.
The failure and output absence are retained, infrastructure retries remain zero,
and the one-line corrected validator remains unexecuted. REG-GATE stays closed;
one replacement static start requires explicit owner direction.

After retaining that failed-closed checkpoint at commit `7761d3e`, the owner
explicitly directs I06A to continue. One separately bound replacement no-model
validation start is therefore authorized against the corrected validator and
the retained failure record. It is not an infrastructure retry, permits no
PyGRC import/model or candidate/scientific operation, and is consumed by any
failure. REG-GATE remains closed pending the retained result and later owner
review.

That replacement passes 14/14. AdapterV2 inherits 13 tested V1 members exactly;
its normalized materialization AST is equal, nine pure cases pass, and response
reads/schedules remain absent. The historical execution manifest and validator
reconstruct byte-exactly, while only `_assert_portable` and two required imports
differ in current source; all 24 remaining validation functions are unchanged.
The registered tolerance domain, twelve comparator arm tuples, two unique H_P
admission edges/seven excluded traffic classes, positive mode isolation, and
per-entry outcome-independent retry semantics all pass. Final manifest v1.1.1
binds historical producer and current reconstruction roles separately. No
scientific disposition changes. The owner accepts the complete I06/I06A package,
authorizes amendment into the retained checkpoint, passes REG-GATE, and opens
only I07 candidate-cycle freeze construction. Candidate execution remains
unauthorized until the exact cycle receives its own authority.

#### 3.2.25 I07 exact candidate-cycle freeze declaration

The owner directs I07 after accepted I06/I06A as the final preparation before
actual runs. I07 must assign one cycle identity and bind the accepted tracked
source/runtime, all three registered modes, exact cell/subconfiguration/seed/
attempt/resource matrix, I04R2 response/comparator authority, I05J arithmetic
resolution, I06 registration/restoration identities, retry eligibility, stop
conditions, output/receipt schema, graph read-only guard, and candidate-effect
boundary. Missing mode-specific prerequisites must remain explicit matrix
entries rather than silently shrinking the cycle.

I07 may perform only read-only authority inspection and candidate-free static,
schema, hash, matrix, and refusal validation under the repository `.venv`. It
may not construct a PyGRC candidate/control model, admit a contribution or
history token, evaluate a response, open a comparator/scientific window, tune a
value, rank modes, or assign OP/R01–R05 evidence. The one eligible
infrastructure retry is scoped independently per matrix entry; failed
scientific or control outcomes are never retryable. I07 returns its exact
package uncommitted for explicit owner review and cannot pass EXEC-FREEZE or
authorize I08 by its own output.

The I07 authority audit assigns cycle ID `P2-I2-C01` and projects 78 applicable
mode/branch/order combinations across three registered seeds, yielding 234
primary entries. It then stops before execution-source construction. The
accepted schedule has q1/q2 contribution slots 0/1, history materialization at
slot 2, neutral contact at slot 3, and fixed response arrival 15.625, but the
hybrid state-component branches require a native P debit after M_H
materialization and before neutral contact. I06 registers neither that debit's
event/index position nor a full reference-P amount: its `0.4375` diagnostic
debit is not the derived `q1+q2 = 1.5` needed to return candidate P to reference.
PyGRC exposes no public state-only intervention that bypasses this schedule.

The audit also finds that direct-address and output-matched controller bypasses
have accepted causal-exclusion meanings but no exact frozen call primitives.
Choosing contributor masks or controller-authored A-to-B scheduling inside I07
would therefore revise rather than instantiate I06. These are registration-
readiness findings only. No PyGRC import/model, contribution/history admission,
response, comparator, or scientific operation occurred. The owner subsequently
authorized bounded I06B; EXEC-FREEZE remains closed pending I06B acceptance and
later completion/acceptance of the resumed I07 freeze.

#### 3.2.26 I06B execution-readiness registration correction declaration

The owner accepts DEC-043's recommendation to pause I07 and open one bounded
I06B correction. The exact correction scope is only: (1) a native P-debit slot
after history materialization and before neutral contact, (2) the full
reference-P debit amount derived exactly as registered `q1 + q2`, and (3)
public-call primitives for the already registered direct-address and
controller-assembled bypass exclusions. These are implementation-registration
obligations, not new operational hypotheses or scientific contrasts.

I06B must preserve accepted I06/I06A bytes and bind its changes through an
additive overlay. It may move only the downstream neutral/response absolute
times needed to reserve a matched intervention slot; contribution order,
amounts, spacing, arrival delay, response-window lag, mode thresholds,
response amount, cells, controls, seeds, retry semantics, restoration, and all
OP/R01–R05 meanings remain unchanged. A branch that does not use the
intervention slot records a no-op rather than receiving a different opportunity
schedule.

Validation may read and hash accepted artifacts and source, inspect public-call
signatures, derive exact binary arithmetic, validate schemas/matrices, and test
refusal predicates under `.venv`. It may not import or construct a PyGRC model,
schedule or process a packet, admit a contribution/history token, evaluate a
response, execute a cell/control/comparator, tune any value, or assign
scientific evidence. I06B returns uncommitted for explicit owner review.
REG-GATE remains reopened and I07/EXEC-FREEZE/I08 remain closed until acceptance.

The constructed overlay satisfies that declaration without changing its
boundary. It reserves slot 3 for native P intervention, moves the matched
neutral contact to slot 4, and preserves the `1.0` neutral-arrival-to-response-
arrival lag. It separates accepted diagnostic debit `0.4375` from exact full
reference debit `0.625 + 0.875 = 1.5`; maps the latter only to the two hybrid
reference-P branches; freezes contributor-front-mask native feedback for the
direct-address exclusion; and freezes receipt-derived, carrier-blind direct
native scheduling for the controller exclusion. Public PyGRC is adequate for
all three primitives, so I06B identifies no new native implementation gap.

One `.venv` candidate-free validation start passes 15/15 with zero blockers,
zero retries, immutable accepted I06/I06A bytes, exact source-current public
signatures, and zero PyGRC imports/models, packet, candidate/control/response,
comparator, or scientific operations. This supplies registration-readiness
evidence only. The owner subsequently accepts I06B and restores REG-GATE;
commit, I07 acceptance, EXEC-FREEZE, and live execution remain separate and
ungranted.

#### 3.2.27 I06B acceptance and I07 resumption declaration

The owner explicitly accepts the complete review-ready I06B package. That
acceptance supplies registration progression authority only: REG-GATE is
restored and the already-declared I07 freeze resumes from its retained blocked
audit and `P2-I2-C01` projection. Accepted I06/I06A and I06B scientific and
causal meanings remain unchanged.

I07 may bind the accepted I06B overlay, correct its non-authoritative draft
schedule/call surfaces, construct the exact finite cycle policy and receipts,
and run candidate-free static validation under `.venv`. It may not import or
construct a PyGRC candidate/control model, schedule/process a packet, evaluate a
response, open a comparator/scientific window, pass EXEC-FREEZE, authorize I08,
or assign OP/R01–R05 evidence. Commit authority is absent. The completed I07
package must return uncommitted for separate owner review.

#### 3.2.28 I07 candidate-free validation failed-closed declaration

The first authorized I07 `.venv` start generated the exact 234-primary-entry
matrix, 20-file execution binding, and inactive cycle freeze without importing
PyGRC or performing any candidate/control operation. The second authorized
start stopped before test collection because the repository `.venv` has no
`pytest` module. This is an environment/tooling failure only; it supplies no
result about any OP projection, realization, control, or scientific claim.

The I07 input freeze allows zero infrastructure retries and requires a stop for
owner direction after any failed construction/validation start. Therefore the
third validator start remains unused, no dependency is installed, and no
replacement validation is inferred. EXEC-FREEZE, I08, candidate execution,
commit authority, and OP/R01–R05 evidence all remain closed. Any correction
must be separately checklist/hypothesis-frozen and must preserve the already
generated inactive scientific/execution semantics byte-exact.

The owner subsequently directs that the missing `pytest` installation and
continuation remain within I07 rather than opening I07A. This changes only the
candidate-free environment/process boundary: retain the failed start, install
into the repository `.venv`, record the resolved dependency, update honest
process accounting, refresh derived binding/freeze hashes, then permit one
replacement focused-test start and one final validator start. Policy, run
matrix, tests, accepted upstream authorities, causal semantics, candidate
prohibition, and scientific evidence remain unchanged. Any further failure
stops again for owner direction.

The authorized continuation completes without further failure. The repository
`.venv` retains `pytest 9.1.1`; the candidate-free binding refresh preserves the
policy, execution source, focused tests, and 234-entry matrix byte-exact; the
unchanged suite passes 7/7; and the final validator passes 25/25 with zero
blockers. All six Python starts, including the original pre-collection failure
and dependency installation, are retained in the process ledger. No PyGRC
import, model, adapter, packet, candidate/control operation, response,
comparator, or scientific window occurred. I07 is review-ready only;
EXEC-FREEZE, I08, commit authority, and all OP/R01–R05 evidence remain closed.

#### 3.2.29 I07 cross-entry-isolation audit declaration

Before I07 acceptance, the owner requests a stronger audit of whether earlier
C01 artifacts can influence later entries. The audit is read-only and must
separately check: fixed-row/accepted-authority reads; fresh process and registered
baseline construction; absence of earlier-result scans or outcome-conditioned
branch/retry logic; unique non-shadowing claim/output/failure paths; adapter,
cache, temporary-file, queue, and RNG isolation; entry-local preflight; later
authorization after an incomplete earlier entry; and fail-closed matrix
completion when any required entry is missing or nonevaluable.

Passing path uniqueness alone is insufficient. Parent-component symlinks,
Python bytecode/import caches, shared retry ledgers, and completion-manifest
logic are explicitly in scope. The audit may classify a blocker but may not
change the frozen source, policy, matrix, binding, validation, or activation
boundary without subsequent owner direction. It performs no PyGRC import,
model/packet/candidate/control operation, response, comparator, or scientific
window.

The audit finds that ordinary entry dataflow is row-local: the live function
selects exactly one frozen row; reads only fixed authority paths; seeds the
process from that row; constructs a new model and registered mode/branch
adapter; derives branch, schedule, and parameters from frozen authorities; and
does not enumerate or parse prior run, claim, or failure trees. The normalized
CLI plus the process-local one-start guard requires a fresh process, and an
incomplete earlier primary does not participate in a later primary's
authorization. Across 234 entries, the 1,404 derived primary/retry output,
claim, and failure paths are all distinct, relative, and textually confined to
the declared C01 output root.

That is not yet a complete isolation guarantee. `_exclusive_json` checks only
the leaf and follows unchecked parent components, while the clean-tree rule
admits any untracked object beneath the C01 output root; a parent symlink can
therefore alias distinct textual paths or redirect an artifact toward authority
or import locations. Both the experiment scripts and external PyGRC source
trees contain ignored shared `__pycache__` directories, and the normalized
command does not bind an entry-local bytecode-cache policy. Attempt 2 accepts a
committed `retry_eligible: true` ledger row without reconstructing that value
from the same entry's retained attempt-1 failure receipt and zero-state
counters. Finally, `execution_manifest_path` is declared only as an absent
future path: no implementation currently enumerates all 234 rows and fails
closed on a missing or `operational_null`/nonevaluable terminal record.

Therefore fixed-row semantics, fresh construction, and ordinary cross-entry
dataflow pass, but strict C01 isolation does not. I07 remains review-blocked on
four execution-safety corrections; the audit itself authorizes none of them and
produces no candidate or scientific evidence.

#### 3.2.30 I07A cross-entry-isolation correction declaration

The owner assigns the four CHG-041 blockers to `P2-I2-I07A`. The correction is
mechanical and candidate-free. It may change only the live execution source,
effective successor policy, focused tests, candidate-free validator, the exact
completion surface, and consequential matrix/binding/freeze identities. The
reviewed I07 hashes and audit disposition remain historical inputs. Accepted
I04R2 measurement semantics, I05J resolution, I06/I06A/I06B registration,
three-mode retention, branch/value identities, resource envelopes, retry
ceiling, and scientific interpretation boundaries are immutable.

The corrected path must satisfy four stronger hypotheses. First, a governed
artifact is addressable only by a normalized relative path below the C01 output
root, and every parent component is opened as a real directory without
following symlinks before an exclusive leaf creation. Second, every live entry
runs under the repository `.venv` with bytecode writes disabled and refuses any
pre-existing project or PyGRC bytecode/import cache before local runtime import;
the same cache boundary is rechecked after execution. Third, attempt 2 has no
shared ledger: its only entry-specific predecessor inputs are its exact unique
attempt-1 claim and failure receipt, from which pre-construction eligibility is
reconstructed mechanically under unchanged common authority. Fourth, the cycle
manifest enumerates exact matrix paths, never scans result directories, and is
not created unless all 234 rows have exactly one valid evaluable terminal
output; missing, duplicate, malformed, or operational-null rows fail closed.

I07A permits at most three `.venv/bin/python -B` starts: derived refresh,
focused tests, and final validation. It imports no PyGRC during construction or
validation, constructs no model or adapter, schedules no packet, evaluates no
candidate/control response, and produces no scientific evidence. Completion
returns uncommitted for explicit review; EXEC-FREEZE and I08 remain closed.

The correction completes within that exact boundary. All 234 entry objects and
the 234 conditional-retry ceiling are unchanged. Governed I/O now traverses
every directory component by descriptor without following symlinks and creates
each claim/output/failure leaf exclusively. The live `.venv/bin/python -B`
surface rejects project/PyGRC cache state before local imports and after an
entry. Attempt 2 reconstructs only its own exact claim/failure predecessor and
the shared ledger is absent. Completion reads the exact two frozen terminal
paths per row and refuses to create a manifest for missing, duplicate,
malformed, invalid-window, non-finite, or operational-null evidence.

The three authorized starts pass without replacement: derived refresh, 15/15
focused tests, and 17/17 final validation. Negative tests cover path escape,
ancestor symlink, occupied claim, cache presence, other-entry retry receipt,
and missing/null/duplicate terminal states. There are zero PyGRC imports,
models, packets, candidate/control operations, response evaluations, or
scientific windows. I07A is review-ready but not self-accepted; EXEC-FREEZE,
I08, commit authority, and scientific evidence remain closed.

The owner subsequently states `ok, time to commit`. DEC-047/CHG-043 accept the
exact zero-blocker I07A package, pass EXEC-FREEZE only for the inactive cycle,
and authorize its retention with the accumulated I06B/I07 checkpoint. This
acceptance does not remove ignored caches, create the activation record, open
I08, run a matrix entry, create the execution manifest, or assign scientific
evidence; those actions remain separately governed.

#### 3.2.31 I08 activation and finite-execution declaration

After the accepted I06B/I07/I07A checkpoint is retained at `5c2c248`, the owner
states `ok, let's do I08`. DEC-048/CHG-044 treats this as the separate direction
needed to open I08 activation-package construction. It authorizes the
checklist/hypothesis-first activation preparation and the frozen import-cache
cleanup prerequisite, but it cannot accept activation bytes that do not yet
exist and does not authorize an uncommitted matrix entry.

The activation candidate must initially remain inactive. It binds the exact
committed inactive freeze, policy, execution source, validator, tests,
resumption freeze, I07A input and validation, matrix, binding receipt, graph
revision/source, repository `.venv` interpreter, and relative normalized
command surface. It records `owner_acceptance=false`,
`candidate_execution_authorized=false`, and `I08_authorized=false` until the
complete candidate-free package returns for explicit review. The eventual live
HEAD is supplied only after the accepted activation is committed, through the
normalized command argument, so the activation record contains no
self-referential commit identity.

Preparation may remove only ignored Python bytecode/import-cache artifacts
beneath the two frozen import roots and must retain the before/after inventory.
It performs no PyGRC import, model or adapter construction, packet operation,
candidate/control response, comparator, or scientific window. Validation must
fail closed on an authority/hash/revision/interpreter/command mismatch, dirty
tracked repository, remaining import cache, pre-existing governed artifact, or
non-unique/incomplete 234-row matrix.

If the activation is later explicitly accepted and committed, each primary row
runs in ascending frozen `sequence_index` in its own `.venv/bin/python -B`
process with a fresh/restored registered composite baseline. No parallel worker,
shared mutable process state, earlier outcome read, parameter derivation, or
outcome-conditioned branch is allowed. Attempt 2 exists only when the same
entry's permanent attempt-1 claim and exact pre-construction failure receipt
mechanically establish the already-frozen infrastructure eligibility. A
scientific/control outcome is never retried. Missing, ambiguous, malformed, or
nonevaluable terminal evidence remains incomplete and prevents creation of the
execution manifest; it is not converted into negative evidence.

The bounded preparation completes without opening that live boundary. The
cleanup start retains an exact 207-item before inventory and zero-item after
inventory across the two frozen import roots, while both tracked repositories
remain unchanged. The second and final preparation start passes 18/18 checks
with zero blockers. All 234 matrix rows and accepted technical hashes match;
the output root and execution manifest remain absent; and PyGRC imports, models,
packets, candidate/control operations, and scientific windows all remain zero.
The activation candidate is therefore review-ready but still records all three
acceptance/authorization booleans as false and remains uncommitted.

The owner then states `+1 and make a commit`. DEC-049/CHG-045 accept the exact
inactive candidate at SHA-256 `52d420b49029e32f007119a3f888ca9fc05ca545a4a75b3e775f8c69c23eac6b`
and authorize its declared transition and retention. The accepted activation
has SHA-256 `f46ebd323499423715107c3b337963c3787404ed257c56be880808617cb09cc3`;
all accepted scientific, matrix, policy, source, and runtime identities remain
unchanged. The activation becomes live only from the resulting committed full
HEAD and an exact post-commit preflight. Acceptance and commit do not themselves
create a claim, execute an entry, build the manifest, or assign evidence.

#### 3.2.32 I08 C01 bounded-incomplete and I08A successor declaration

The exact post-commit preflight passes at full HEAD `c265279`. The first frozen
entry then consumes its permanent attempt-1 claim and terminates in the common
registration/PyGRC import path with an OpenBLAS memory-allocation error. No
governed output or failure receipt is created. Attempt 2 is mechanically
unauthorized because the exact same-entry failure receipt and zero-state
counters do not exist; source-level phase inference cannot replace them.

This event supplies no response, comparison, control, mode, OP/R01–R05, or L02
evidence and is not a negative result. C01 is retained bounded incomplete with
one claimed, zero evaluable, and 233 unattempted entries. No later C01 claim is
consumed.

The owner states that a 512 MiB space limit is unnecessary on the 128 GB host.
DEC-050/CHG-047 therefore open I08A construction of C02. C02 must preserve the
234 scientific entry projections byte-semantically while assigning new cycle
and artifact identities. It removes only `RLIMIT_AS` enforcement and retains the
180-second runtime ceiling, 512 MiB file-size ceiling, single-local-CPU rule,
`.venv/bin/python -B`, graph read-only/cache isolation, restoration, and retry
semantics.

C02 must place native worker termination outside the evidence-loss boundary:
an external supervisor owns the permanent claim and final success/failure
receipt. A missing child attestation or unknown failure phase is conservatively
non-retryable. Construction and candidate-free native-exit tests cannot import
PyGRC, execute a registered entry, assign evidence, pass C02 EXEC-FREEZE, or
authorize commit without separate review.

I08A construction now satisfies that candidate-free projection. C02 contains
the exact 234 C01 scientific rows under new cycle/governed paths with zero
scientific projection changes. The worker applies no `RLIMIT_AS` cap while
retaining the 180-second runtime and 512 MiB file-size ceilings. A fresh
external supervisor owns claims and terminal receipts, and unknown/native
termination remains non-retryable. Focused tests pass 8/8, including actual
child native-exit observation; final validation passes 18/18 with zero blockers,
PyGRC imports, models/adapters, candidate/control operations, or scientific
windows. This is implementation-authority evidence only. C02 remains inactive,
uncommitted, and unauthorized for candidate execution pending owner review.

The owner now accepts I08A and rejects a duplicate activation-review step.
DEC-051/CHG-048 authorize a deterministic activation record bound to the
reviewed I08A hashes, one candidate-free activation validation, one complete
package commit, one exact read-only post-commit preflight, and corrected I08
entry 1. Activation and commit do not supply evidence. Entry 1 may supply only
its registered raw/control receipts; it cannot assign OP/R01–R05, L02 support,
or a terminal result before the complete registered matrix and later gates.
Execution must stop after entry 1 for retained-outcome review before entry 2.

The first post-commit preflight start does not pass: the command supplies
`12ff83b30…`, while the resulting committed authority is `12ff83be7…`. The
exact HEAD guard fails before any C02 claim, PyGRC import, model/adapter,
candidate/control operation, or scientific window. Entry 1 remains unstarted.
The failed start cannot be rewritten as a successful preflight or silently
retried; one corrected read-only preflight requires explicit owner authority.
The owner supplies that authority immediately, classifies the mismatch as an
operator fault unrelated to the experiment, and authorizes one corrected
preflight using the actual resulting full HEAD. This changes no scientific,
matrix, activation, retry, or evidence rule.

The corrected preflight passes, but entry-001 attempt 1 then produces a
supervised, attested pre-model failure. `.venv` already contains
`matplotlib==3.10.9`; the C02 launcher instead resolved `sys.executable` to the
host binary before spawning its child, so the child had no active repository
venv. Claim and failure receipt are retained, output is absent, all model/
adapter/candidate counters are zero, and the frozen retry predicate is true.

The owner directs no I08B or new scientific rerun authority: this is an in-place
I08A/I08 infrastructure regression correction. The accepted I05C invariant is
projected to every governed Python subprocess: invoke lexical
`.venv/bin/python`, require repository-venv `sys.prefix`, and use the resolved
host binary only for digest identity. Only the already-frozen eligible
same-entry retry may cross the exact committed correction bridge; no matrix,
hypothesis, response, control, or evidence rule changes.

The in-place correction passes 8/8 focused tests, including an actual child
dependency import under the lexical repository-venv command, and 18/18 final
candidate-free checks. The retained attempt-1 bytes and all zero-state counters
remain exact; no PyGRC, model, candidate, control, or scientific-window
operation occurs. This is infrastructure conformance evidence only.

Commit `6b920fb` binds that correction. The exact attempt-2 preflight passes,
and the sole same-entry retry completes under `.venv/bin/python -B`. The
retained state-carried `reference_pool_empty`, seed-101 terminal is evaluable:
the response window is valid, queues are empty, measured B gain equals the
registered native packet gain at `0.0`, and the record assigns scientific zero.
This is one registered row of evidence, not a mode or hypothesis conclusion;
`R01`–`R05` and scientific interpretation remain unassigned until the frozen
downstream stages.

The owner accepts this terminal and directs that narrative reporting be
cumulative rather than one file per entry. Because acceptance precedes the
continuation commit, the existing manifest's one-global-HEAD equality must be
corrected without broadening scientific authority. Existing I08 may admit only
this exact checkpoint by entry, attempt, old HEAD, claim/output hashes, source,
and policy; entries 2–234 must share the next committed authority HEAD. Any
unlisted historical head or byte mismatch remains nonevaluable and fails
closed. No further checkpoint commit occurs before the cumulative manifest.
The exact admission and historical retry-provenance path pass 9/9 focused
tests through `.venv`, including fail-closed rejection of an unlisted old HEAD.
Commit `180a1bf` binds the continuation. Entries 2–234 all complete on primary
attempt 1 through fresh repository-venv processes, and the cumulative manifest
accepts exactly 234/234 evaluable terminals. This closes I08 execution only;
scientific interpretation remains null and `R01`–`R05` remain unassigned.
The raw registered response inventory contains 132 scientific-zero rows and
102 rows at gain 0.125. All matched configurations are invariant across the
three seeds. State-carried is invariant across both registered physical orders;
history-carried and hybrid retain an order-conditioned 0.125/0.0 split. These
are mechanical I08 observations only, not control resolution or L02 support.
The owner accepts the complete I08 mechanical package and authorizes its
cumulative commit. This acceptance freezes the raw evidence and manifest; it
does not assign `R01`–`R05`, resolve a control, or begin I09 interpretation.

#### 3.2.33 I09 retained-evidence control-resolution declaration

The owner directs I09 after accepting and retaining the complete I08 package.
I09 is a deterministic projection stage, not a new hypothesis, execution
cycle, calibration, or terminal interpretation. Before constructing its
machine index, it must bind the exact accepted I04R2 analysis rules, I06
registration and fifteen-entry lane-control template, I08 run matrix and
234/234 manifest, all nineteen program-common control meanings, the OP-01
through OP-09 fail-closed effects, and the R3 compact-index requirement.

The index must retain three distinct layers without conflating them:

1. every program-common `AE01-CTRL-01` through `AE01-CTRL-19` guard, with an
   explicit applicability and outcome for each mode;
2. every frozen common and mode-specific comparison rule, with exact
   subconfiguration, seed, response, causal-status, and relation provenance;
3. every `AE01-L02-CTRL-01` through `AE01-L02-CTRL-05` disposition separately
   for state-carried, history-carried, and hybrid.

`pass` means only that retained evidence satisfies the frozen control rule. It
does not mean the primary scientific margin is positive or that a boundary
rung is supported. `not_applicable`, `ambiguous`, `fail`, `blocked`, and
`not_run` remain first-class fail-closed outcomes. Raw-visibility and scope-
diagnostic rules may pass through complete, uncontaminated retention even when
their response relation is zero or non-gating. Direct/controller branches are
resolved by receipt-derived causal exclusion rather than numerical inequality.

I09 may not alter a response, regenerate an entry, import or run PyGRC, select
among modes, collapse mode-specific results, assign `R01`–`R05`, determine L02
support, or create schema authority. Program-common terminal/report guards are
resolved only against the artifact set that exists at I09 and must be
revalidated against the eventual I11 closeout. Any missing registered branch,
invalid window, seed variation, causal-receipt mismatch, or changed frozen
identity fails the affected control closed rather than being repaired or
interpreted away.

The resulting retained-evidence projection is review-ready. It passes 21/21
deterministic checks and byte-identical reconstruction: all 38 frozen
comparison rules and all 15 mode-local L02 controls pass, while all 19 program-
common controls resolve separately by mode to 56 passes and one explicit
state-carried `AE01-CTRL-16` not-applicable. No matched branch varies across
seeds. State-carried retains order-invariant responses and primary margins of
`0.125/0.125`; history-carried and hybrid retain order-conditioned responses
and primary margins of `0.125/0.0`. This is control evidence, not a rung or
terminal interpretation. At the construction handoff, CONTROL-GATE remains
pending owner acceptance; every frozen terminal/report guard remains subject
to I11 revalidation.

The owner subsequently states `please commit`, accepting this exact projection
and its 21/21 validation. DEC-054 passes CONTROL-GATE and authorizes the
containing retention commit. The acceptance adds no rung or terminal meaning;
I10 remains unstarted, and the I11 revalidation duty is unchanged.

#### 3.2.34 I09A normalized-estimator correction declaration

The owner responds `+1` to the bounded DEC-056 proposal. DEC-057/CHG-056
therefore authorize only an additive I09A correction over retained evidence.
Accepted I09 remains immutable history, and I04R2, I05, I06, I08, their raw
responses, scientific zeros, causal receipts, rules, registration, and matrix
cannot change.

I09A must first prove the accepted I09 projection reconstructs byte-exactly.
It then replaces only the derived raw-difference `primary_margin` path in
memory with the accepted I04R2 exact three-arm estimator for all eighteen
mode/order/seed tuples. Candidate, q1-only, and q2-only envelopes must be
complete and scientifically valid, the maximum must remain within each tuple,
and exact ties retain deterministic `q1-only` provenance without scientific
meaning. Every comparison, lane-control, and program-control disposition must
be recomputed from the corrected projection rather than copied.

This is a correction to derived control evidence, not a candidate execution or
new scientific input. I09A imports no PyGRC, constructs no model, regenerates
no C02 entry, assigns no mode ranking, rung, support, or terminal class, and
persists no absolute path. Its outputs remain uncommitted and CONTROL-GATE
remains reopened until explicit owner review. I10 remains paused and may later
receive only an additive v2 freeze after accepted I09A retention.

The first I09A build start fails closed before output or estimator evaluation:
the builder supplied the I04R2 machine-verification preregistration document
where `primary_margin` requires the separately accepted machine-policy JSON.
CHG-057 retains the failure and corrects only that input binding in place,
without creating another iteration. The start reconstructed accepted I09 bytes
and read retained evidence but imported no PyGRC and performed no model,
candidate/control, matrix-regeneration, or scientific-runtime operation.

The corrected generation and independent reconstruction then each pass 24/24.
All eighteen retained tuples traverse the accepted I04R2 entrypoint: the twelve
positive normalized margins are `1.0`, and the six zero margins are `0.0`.
State-carried retains an order-invariant `1.0/1.0` relation; history-carried
and hybrid retain their order-conditioned `1.0/0.0` relation. The underlying
responses remain `0.125/0.0`. Recomputing all dependent layers leaves every
disposition unchanged: 38 comparison passes, 15 lane-control passes, and 56
program-mode passes plus one not-applicable. This is review-ready corrected
control evidence only; owner acceptance, CONTROL-GATE passage, commit, and I10
resumption remain pending.

#### 3.2.35 I10 reconstruction and identity-verification declaration

After accepted I09 commit `cfa19fe`, the owner directs I10. DEC-055/CHG-054
open only independent retained-evidence reconstruction and registered identity
verification. I10 introduces no new operational hypothesis and may not alter
an OP-01 through OP-09 projection, response, control, mode, or scientific
input.

I10 must freeze exact accepted I05J calibration, I06/I06A/I06B registration,
I08/C02 execution, and I09 control identities before its first governed start.
It reconstructs derived bytes only from those retained inputs, using memory or
temporary paths and refusing to overwrite accepted artifacts. C02 execution is
reconstructed from the frozen matrix and retained claims, failures, and
terminal outputs; no matrix-entry worker or scientific branch may run.

Restoration identity and raw snapshots remain distinct witnesses. The bounded
runtime allowance is one check per retained mode in each declared pass: build
the exact registered baseline, pair-save/load every owned component, verify
the composite restoration identity, apply one identical no-packet native step
to both branches, compare continuation result, composite identity, and raw
observations within the separately registered runtime tolerance, then reset
both branches and reverify the registered baseline. This is candidate-free
identity conformance. It admits no contribution, history token, neutral
contact, response evaluation, comparator window, seed, or L02 evidence.

Any missing input, digest/path/schema drift, unsafe claim, graph mutation,
restoration mismatch, continuation mismatch, margin mismatch, or non-byte-
identical deterministic projection fails RECON-GATE closed. It cannot become a
scientific null and cannot be repaired by regenerating a C02 entry or selecting
new inputs. I10 may return only a compact reconstruction manifest, validation,
and cumulative report for explicit review. `R01` through `R05`, support,
terminal classification, mode ranking, I11, and CLOSE-GATE remain unopened.

The first exact I10 pass fails at that boundary before output or PyGRC import.
I09 computes `candidate - strongest` directly, whereas the accepted I04R2
estimator divides that difference by the maximum absolute candidate,
comparator, and arithmetic floor. Thus the twelve positive mode/order/seed
rows reconstruct as normalized margin `1.0`, while I09 records `0.125`; the six
zero rows remain `0.0`. This is a derived-control projection defect, not a
change in I08 raw responses. I04R2, I05, I06, and I08 remain immutable. A
bounded I09A correction is now complete and review-ready under DEC-057 but
remains unaccepted and uncommitted; I10 cannot resume from technical completion
alone.

The owner then directs that I10 must be finished or have its tasks properly
marked done. DEC-058/CHG-058 resume I10 without inventing an I10A or inferring
commit authority. A v2 freeze may bind the exact local I09A hashes alongside
the immutable committed lineage, and I10 may complete its previously frozen
reconstruction/restoration passes for one combined review. CONTROL-GATE and
RECON-GATE remain pending that review; I11 and scientific interpretation stay
closed.

The first v2 generation then fails closed before I10 output or continuation
checks because the live accepted I06 validator result is not byte-identical to
its retained validation. It had already verified all 47 frozen inputs,
reconstructed calibration, C02, and the 18 corrected margins, and invoked only
the candidate-free six-model I06 validation. CHG-059 permits one exact-field
diagnostic before any criterion change or replacement generation.

The diagnostic finds one field only: retained `I06-12.bound_file_count` is `5`
while the live current validator reports `15`. Accepted I06A already classifies
this exact provenance transition: the retained validation was produced by the
historical five-file execution manifest/validator, whereas the final 15-file
manifest binds both historical and current roles and explicitly does not claim
the current validator as historical producer. CHG-060 therefore requires both
witnesses—live current 14/14 validation and byte-exact reconstruction of the
historical five-file projection. No semantic check, baseline digest, refusal,
or gate field may differ.

The provenance-corrected replacement then reaches the intended restoration
boundary. State-carried composite identity matches after paired save/load, but
the separately required raw snapshot does not, before any no-packet step.
CHG-061 retains failed start 003 and permits one state-only structural diff.
Neither composite identity nor raw observation may be waived or redefined from
the failure alone.

That diagnostic resolves the ambiguity before any further runtime. All 20
differences are the duplicated current/reset-baseline instances of four native
normalizations: deterministic budget-source, parameter-identity, and RNG-state
materialization, plus canonical orientation of three undirected zero-flux
edges. At the admitted revision, PyGRC's restoration matrix explicitly
requires restoration-identity and equal-input-continuation stability while
expecting the raw full-snapshot digest not to be a fixed point. CHG-062
therefore corrects only unaccepted I10 v2: adapter raw state must remain exact,
native raw state remains a separately retained witness with an exact closed
normalization set, every unexpected native difference fails closed, and
identity, equal-input continuation, and paired reset remain mandatory in all
three modes. No raw witness is erased, no PyGRC byte is changed, and no
scientific claim or input is introduced.

The exact CHG-062 replacement generation and independent byte reconstruction
now each pass 24/24 with zero blockers. In all three modes, load, post-step,
and reset comparisons contain exactly the same 20 admitted native
normalization differences and zero unexpected differences; adapter state is
exact, restoration identities match, equal-input no-packet continuation
matches, and paired reset returns to the registered identity. Each pass uses
six candidate-free native no-packet steps and zero contribution, history-token,
neutral-contact, response/comparator, C02-worker, or new scientific operation.
All 18 corrected margins, 234 terminals, 470 governed paths, calibration,
registration provenance, historical I09, and corrected I09A bytes reconstruct.
This makes I09A/I10 review-ready together but does not pass CONTROL-GATE or
RECON-GATE, accept/commit either package, authorize I11, or interpret L02.

The owner then states `commit all`. DEC-059/CHG-063 accept the exact combined
I09A/I10 hashes, pass CONTROL-GATE and RECON-GATE, and authorize one containing
retention commit. This acceptance changes no technical byte and assigns no
`R01`–`R05` disposition, support status, mode ranking, terminal classification,
or scientific interpretation. I11 becomes ready only after retention and must
still revalidate the program-common guards before assigning terminal meaning.

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
