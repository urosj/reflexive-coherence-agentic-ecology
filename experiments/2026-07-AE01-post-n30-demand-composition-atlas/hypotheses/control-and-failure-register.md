# AE01 Control and Failure Register

**Status:** frozen at P1-I4

**Register version:** `1.0.0`

**Evidence effect:** preregistration only

## 1. Control semantics

A control is fail-closed when its unsafe condition cannot produce a passing
lane, synthesis, ranking, report, or promotion record. Controls are either:

- `record_guard`: deterministic validation of roles, claims, identities, or
  ordering;
- `causal_control`: an executed comparison that breaks a proposed relation
  while preserving a nearby alternative; or
- `withdrawal_control`: removal of a producer, scaffold, carrier, or mechanism
  whose contribution must remain explicit.

A failed record guard invalidates the affected record. A failed causal or
withdrawal control downgrades or blocks only the claims it controls; it does
not erase lower-level valid observations.

## 2. Common fail-closed controls

| ID | Type | Unsafe path | Required check | Fail-closed effect |
| --- | --- | --- | --- | --- |
| `AE01-CTRL-01` | `record_guard` | Conceptual paper relabeled as runtime evidence | Every conceptual source retains `conceptual_motivation`, runtime permission false, and no observed-result role. | Reject the evidence reference and every dependent fact or gate. |
| `AE01-CTRL-02` | `record_guard` | N30 relabeled as coordination, agency, or ecology regime | Enforce the admitted P2/M2 ceiling and N30 blocked relabels. | Reject the stronger claim; preserve only the admitted trace-mediated eligibility leg. |
| `AE01-CTRL-03` | `record_guard` | N29 component success relabeled as composition success | Require a dedicated composition record with combined controls, handoff, budgets, leakage, and interference results. | Component observations remain separate; composition status cannot pass. |
| `AE01-CTRL-04` | `record_guard` plus lane causal control | Pre-given closed agent plus passive environment relabeled as RC ecology | Require participant/medium boundary account, attributable medium change, later functional dependence, and parent context where applicable. | Reject ecology/motif/regime labels; classify `AE01-F04` or `AE01-F08` as applicable. |
| `AE01-CTRL-05` | `causal_control` | Message bus, mailbox, database, or global variable disguised as medium | Remove private addressing/global routing and test dependence on an auditable non-private carrier state. | Reject medium support; classify `AE01-F04` or producer debt. |
| `AE01-CTRL-06` | `causal_control` | Surface annotation without functional dependence | Freeze, shuffle, or substitute the declared surface while preserving labels and nearby activity. | A label-only effect becomes `AE01-F05`; no medium-dependent support. |
| `AE01-CTRL-07` | `record_guard` plus combined comparison | Co-occurrence relabeled as composition | Require ordered dependency, interfaces, state/lineage handoff, interaction term, and combined controls beyond separate component presence. | Reject composition support and record `AE01-F07` when components interfere. |
| `AE01-CTRL-08` | `withdrawal_control` | Hidden producer or undeclared cross-prototype handoff | Instrument every transition and withdraw or neutralize the suspected producer/handoff. | Classify `AE01-F03`; retain producer/composition debt and block native claims. |
| `AE01-CTRL-09` | `causal_control` | Free trace, memory, movement, maintenance, or communication | Account for reserve, cost, leakage, and maintenance; run the frozen budget/leakage comparison. | Reject economy-dependent claims and record medium/measurement debt. |
| `AE01-CTRL-10` | `record_guard` plus causal contrast | Missing parent-basin context | Require a declared parent basin or explicit inapplicability; where causal, separate or hold parent context fixed. | Block parent modulation, motif, regime, and ecology claims. |
| `AE01-CTRL-11` | `record_guard` | Participant/medium boundary confusion | Require separate carrier IDs or an explicit co-constitution account with non-circular lineage and state fields. | Reject participant/medium relation claims until the boundary is resolved. |
| `AE01-CTRL-12` | `record_guard` | Premature communication, cooperation, intention, goal, care, or agency semantics | Match report terms against claim ceilings, unsafe flags, and blocked relabels. | Reject the semantic layer while preserving weaker substrate-visible observations. |
| `AE01-CTRL-13` | `record_guard` | Fixed N31+ selection before synthesis | Ranking requires seven terminal records, synthesis references, eligibility, thresholds, tie procedure, and sensitivity profiles. | Ranking remains `not_run` or closes as non-selection. |
| `AE01-CTRL-14` | `record_guard` | Agentic-ecology demand relabeled as substrate evidence | Demand and missing-surface records cannot occupy inherited or observed native-evidence roles. | Preserve demand only; block native-surface or graph-success claims. |
| `AE01-CTRL-15` | `record_guard` | Constructed ecology mechanism relabeled as native LGRC evidence | Enforce constructed evidence role, realization profile, producer transition discipline, and no silent native substitution. | Reject native claim; retain construction and naturalization debt. |
| `AE01-CTRL-16` | `record_guard` | Construction admitted without necessity, minimality, counterfactual, withdrawal, debt, or discriminator | Require every P1-I3 constructed-mechanism field before a probe may reference it. | Construction is invalid and cannot support execution, demand, or ranking. |
| `AE01-CTRL-17` | `record_guard` | Artifact inspection, mock behavior, or automatic fallback substitutes for requested live PyGRC execution | Validate requested class, local binding identity, conformance, before/after state, and per-run receipt; prohibit fallback. | Classify blocked or incomplete; never a negative lane result. |
| `AE01-CTRL-18` | `record_guard` | Domain fixture or conceptual example relabeled as reusable motif or admitted domain package | Enforce domain role, primary layer, maturity, promotion evidence, and blocked promotions. | Retain fixture/interpretation status; reject package or motif admission. |
| `AE01-CTRL-19` | `record_guard` | Incomplete or runtime-unavailable execution relabeled as a negative result or valid scientific closure | Require verified completed comparison for `not_supported`; require incomplete status and forced non-selection otherwise. | Reclassify as `incomplete_execution` and remove support/refutation and scores. |

Every lane inherits all applicable common controls. A lane must record an
explicit `not_applicable` rationale rather than silently omit a common control.

## 3. Detailed failure classifications

### `AE01-F01` — No primitive

**Signature:** a valid completed candidate comparison exposes no attributable
surface, state transition, eligibility effect, or bounded causal distinction
matching the lane hypothesis.

**Disposition:** normally `not_supported`. Preserve the null as catalog input
and record which proposed primitive was absent.

### `AE01-F02` — Primitive visible but unstable

**Signature:** the required distinction appears in some frozen cells but fails
replay, changes sign, exceeds its declared variance/stability bound, or cannot
survive the required persistence window.

**Disposition:** `partial_or_mixed`, with measurement and possibly transfer
debt. It cannot be promoted as controlled or transferable.

### `AE01-F03` — Producer-carried only

**Signature:** the result disappears under producer/scaffold withdrawal, or an
external transition supplies the relevant state, routing, support, or handoff.

**Disposition:** `partial_or_mixed` when the constructed behavior remains a
useful demand contrast; otherwise `blocked_missing_prerequisite`. Native and
naturalized claims remain blocked.

### `AE01-F04` — Medium absent

**Signature:** no auditable non-private carrier changes, the declared medium is
passive, or the effect resides only in private state, direct addressing, or a
global controller.

**Disposition:** `not_supported` if a valid medium comparison completed;
`blocked_missing_prerequisite` if the required surface cannot be instantiated.

### `AE01-F05` — Proxy success

**Signature:** a label, summary metric, trace annotation, or nearby activity
changes, but the required later formation, persistence, routing,
susceptibility, exchange, or capacity effect does not depend on it.

**Disposition:** `not_supported` for the proposed causal leg; weaker descriptive
observations may remain.

### `AE01-F06` — Fixture lock

**Signature:** the relation passes only in the reference fixture and fails the
frozen transfer/contrast cell, or depends on fixture-specific constants with no
declared substrate rationale.

**Disposition:** `partial_or_mixed` with transfer debt. A fixture-bound result
cannot be marked transferable, motif-level, or domain-general.

### `AE01-F07` — Composition interference

**Signature:** components pass separately but their combined execution breaks
ordered handoff, carrier/timescale/susceptibility compatibility, budget,
leakage, lineage, or the target effect.

**Disposition:** `partial_or_mixed` or `not_supported` for the composition.
Component results remain visible and do not discharge composition debt.

### `AE01-F08` — Claim inflation

**Signature:** a record or report names a stronger catalog layer, maturity,
semantic interpretation, nativity, domain status, or acceptance rung than its
controlling evidence permits.

**Disposition:** fail the claim/report projection. Preserve any valid weaker
record, add claim or semantic debt, and rerun affected projection validation.

### `AE01-F09` — Regime fragmentation

**Signature:** local candidate effects remain isolated, mutually incompatible,
or unable to sustain a coherent parent-level pattern across the declared
timescale and recovery conditions.

**Disposition:** retain primitive/building-block observations but block motif
or regime promotion. Within AE01 this is normally synthesis debt, not evidence
that a lower-level primitive failed.

### `AE01-F10` — Dormancy ambiguity

**Signature:** low or absent activity cannot distinguish persistent latent
organization from inert residue, exhausted capacity, frozen scheduling, or
unobserved producer state.

**Disposition:** `partial_or_mixed` when active observations remain valid;
otherwise `blocked_missing_prerequisite`. Record measurement debt and a future
reactivation discriminator.

## 4. Failure preservation rules

1. Every observed failure ID appears in the lane pattern card, terminal record,
   debt matrix, and cross-lane synthesis input.
2. A failure may recur across lanes without becoming positive substrate
   evidence; recurrence supports a demand only after independent lineage and
   alias controls.
3. Fixing an implementation defect does not delete the original failed cell.
   The rerun links the old and new artifacts and states why rerun was allowed.
4. Claim inflation never upgrades or erases the lower-level observation it
   attempted to relabel.
5. Failure classifications are eligible catalog inputs for requirements,
   controls, missing surfaces, and proposed discriminators.

## 5. P1-I4 boundary

The register specifies controls and failure meanings. No control result or
failure occurrence is assigned during P1-I4.
