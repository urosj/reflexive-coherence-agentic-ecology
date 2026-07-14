# P2-I2 Operational Hypothesis Projections

**Status:** outcome-free; `P2-I2-I03A` causal design and quarantined I03AR1
runtime conformance are review-ready after completed `P2-I2-I03AR1R1`
infrastructure correction; I03B history-carried and I03C hybrid profiles
remain unauthorized pending the required owner reviews; all three profiles
are retained downstream under `P2-I2-DEC-011`

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
        -> I03B history_carried_bound_and_runtime_conformed_or_inadequate -> owner_review_B
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

This notation does not by itself select a topology, carrier, update rule,
response, or implementation architecture. I03A's state-carried mapping is
frozen below; I03B and I03C remain deliberately unbound.

## 3. Unbound realization variables

| Variable | Required meaning | Current state | Binding iteration |
| --- | --- | --- | --- |
| `graph_source_identity` | Exact admitted graph revision and relevant source digests | Bound by `P2-I2-DEC-009` and the I02R2 manifest at `83e3a300426631ee4df71b661b67d4fcfdfed594`; prior I02R1 identity remains historical authority and no realization is implied | I02R2 complete |
| `realization_class` | Native, producer-assisted, or constructed, separately dispositioned for each mode | I03A: `pygrc_native_candidate`; I03B/I03C unauthorized | I03A, then I03B, then I03C |
| `pool_dependence_mode` | Staged `state_carried`, `history_carried`, and admissible `hybrid` profiles | I03A: `state_carried`; later modes deliberately unopened | I03A, then owner review; I03B, then owner review; I03C |
| `source_set` | At least two distinguishable attributable source carriers/events | I03A: symbolic native roles S1 and S2 bound; exact node IDs pending I06 | I03A concept; I06 exact |
| `C_P` | One auditable non-private causal carrier identity | I03A: one native `GRC9V3NodeState.coherence` at role P at encounter | I03A |
| `L` | Audit-only source lineage and attribution projection | I03A: native packet/event records; excluded from V | I03A |
| `q` and `U` | Contribution properties and common-carrier transition | I03A: positive native packet amount and schedule/step departure-arrival chain into P | I03A concept; I04/I06 numeric/exact |
| `V` | Carrier-scoped read, susceptibility, or continuation path | I03A: native feedback P/B_ref mask, model-owned feedback producer, and later packet path | I03A concept; I04 response and I06 exact |
| `access_witness` | Non-private carrier access without contributor addressing | I03A: one-node P feedback mask available to any registered eligible A-role responder | I03A concept; I06 exact |
| `primary_response` | One oriented raw later-continuation response | Pending | I04 |
| `primary_comparator` | Closest insufficient-repetition alternative | Pending | I04 |
| `control_relations` | Signed invariance/divergence and fail-closed effects | I03A qualitative relations bound; numerical equality/resolution pending | I03A, then I04 |
| `R05_contrast` | One capacity, contributor, or access-scope variation | I03A selects access-scope axis; exact alternate responder pending | I03A concept; I06 exact |

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

Only I03A is active. I03A may bind state-carried meanings in this artifact but
must not pre-resolve the history-carried or hybrid profile. I03B and I03C each
require a later checklist declaration, input freeze, and owner review. The
umbrella realization-bound status and I04 entry remain unavailable until the
staged family is complete and reviewed.

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

One contributor supplies the combined registered quantity while support,
encounter state, and opportunity remain matched where possible:

- equivalence may support only the bounded statement that several contributors
  can populate a common pool;
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
- [ ] Each staged mode retains its realization class and source/runtime
  boundary.
- [ ] `C_P`, `L`, `q`, `U`, `V`, sources, access witness, and contribution
  operations map to actual runtime interfaces.
- [ ] All three owner-directed dependence-mode profiles are separately bound
  without rewriting one another.
- [ ] Every projection maps to exact cells, controls, interventions, causally
  held-fixed variables, qualitative expected relations, allowed scientific
  ambiguity, and fail-closed effects.
- [ ] The jointness and private-partition counterfactuals are executable or the
  prerequisite is classified missing.
- [ ] Producer necessity/minimality/withdrawal and external-state identity are
  complete when applicable.
- [ ] No primary response, comparator, or expected relation was selected from
  candidate outcomes.

I04 may change the artifact to `preregistered` only after umbrella I03 passes.
It must import all three I03 causal profiles unchanged, then freeze each
profile's raw measurement, equality/resolution rule, numerical orientation,
closest primary comparator, aggregation, missingness, machine
pass/ambiguous/fail evaluation, candidate-blind null, and stopping rule through
the calibration preregistration. Shared identities require explicit semantic
justification and may not erase mode-specific expectations.

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
