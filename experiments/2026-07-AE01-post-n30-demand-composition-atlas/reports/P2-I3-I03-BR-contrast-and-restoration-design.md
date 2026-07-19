# P2-I3 I03 B-R Contrast and Restoration Design

**Status:** accepted prospective design

**Iteration:** `P2-I3-I03`

**Branch:** `P2-I3-BR`

**Controlling decisions:** `P2-I3-DEC-031` and `P2-I3-DEC-032`

**Evidence effect:** stable contrast and restoration semantics only. No
response, comparator, numeric registration, conformance result, calibration,
execution, control outcome, or scientific result is assigned.

## 1. Q-013 conclusion: three contrasts, not two

The earlier brief distinguished quantity matching from complete-state
matching. DEC-028 later introduced a second scientifically different quantity
match. B-R therefore requires three non-substitutable identities:

| Stable identity | Matched relation | Scientific purpose |
| --- | --- | --- |
| `P2-I3-BR-Q13-FORMATION-QUANTITY-MATCH-001` | Equal total formation transfer and cost; repeated events versus one pulse | Temporal formation structure versus accumulated quantity |
| `P2-I3-BR-Q13-EXPORT-MASS-MATCH-001` | Equal `Delta M=-q`; candidate `Delta O=-q`, control `Delta O=0` | Organization loss versus generic route-mass loss |
| `P2-I3-BR-Q13-COMPLETE-STATE-HISTORY-MATCH-001` | Equal complete causal continuation state and future inputs; different histories | Current-state sufficiency versus active-history or missing-state dependence |

The first quantity comparison does not require equal complete current state.
The second does not compare formation timing. Neither can establish history
dependence. Relocation, false trace, clamps, withdrawal, and hidden-router
controls retain their own identities.

I03 fixes these meanings and IDs. I04 binds their response and comparator
semantics; I06 freezes exact amounts, operations, times, and topology.

## 2. Q-015 conclusion: exact identity and causal equivalence differ

One identity cannot honestly serve both byte-exact reconstruction and the
different-history state-match. Different valid formation histories must remain
visible in exact audit state, so their full snapshots need not be identical.

Q-015 therefore distinguishes:

```text
exact composite execution identity
  all native state + all RCAE policy/branch state + audit lineage
  -> exact save/load/reset/replay and reconstruction

causal continuation-equivalence projection
  every field capable of changing registered continuation
  - only prospectively validated audit-only fields
  -> state-matched history and equal-input continuation
```

Each history arm must restore exactly to itself. The two arms may differ in
exact execution identity, but their causal projections must match before the
same future receipts, schedules, requests, interventions, and observations are
applied. Projection equality is necessary and is not itself continuation
evidence.

## 3. Composite restoration contents

The manifest-coordinated identity covers:

- full native LGRC9V3 topology, coherence, conductance, packet, event, clock,
  phase, scheduler, budget, and reset state;
- B-R policy, cursor, receipts, pending reservation/export, settlement, and
  source/destination bindings;
- route, reservoir, continuation, edge, and role bindings;
- encounter opportunity, parent checkpoint, request schedule, and branch;
- intervention/control identity and participant audit provenance;
- distance-surface policy inputs and dispositions; and
- native plus RCAE reset baselines and audit lineage.

Load must either return a fully validated composite or fail closed before any
scientific continuation. Partial, stale, one-sided, cross-route, cross-policy,
or cross-branch loads are invalid. Reset restores native and RCAE baselines
together and cannot silently rebase.

## 4. Branch and continuation behavior

Every scientific branch forks from a validated clean parent. An admitted Q-007
probe is invasive and terminal. Delayed or repeated probes require clean
unprobed forks.

Equal-input continuation compares original/load, initial/reset, each history
arm restored to itself, paired state-matched histories, and atomic-refusal
replay. It later binds native event/packet sequences, lifecycle receipts,
admission or typed refusal, state/projection digests, and the I04 response over
an I06-frozen horizon.

For field-limited refusal, the post-attempt native identity must equal the
pre-step identity that already contains the scheduled request. Other failures
remain infrastructure or invalid-operation evidence.

## 5. Deferred exactness

I06 still owns exact schemas and component hashes, topology values, commands,
continuation horizon, output-specific equality/tolerance rules, reset values,
branch counts, and runtime binding. Q-015 design is resolved at I03, but its
registration finalization is not complete.

## 6. Reopening conditions

Reopen the relevant decision if a contrast cannot be constructed without
conflation; a continuation-relevant component is missing; an audit-only field
must become causal; complete restore/reset cannot fail closed; conformance
finds unequal continuation after a verified restore; native refusal cannot be
replayed atomically; or new graph evidence changes the admitted provider or
restoration boundary.
