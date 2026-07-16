# P2-I3 I01 Source-Current Capability Audit

**Status:** accepted through `P2-I3-DEC-018`; `P2-I3-SOURCE-AUDIT-GATE` passed

**Iteration:** `P2-I3-I01`

**Lane:** `AE01-L03`

**Accepted input:**
[I01 capability-audit input freeze](../contracts/p2-i3/i01-capability-audit-input-freeze.json)
through `P2-I3-DEC-016`, plus owner-directed
[N29/N30 scope extension](../contracts/p2-i3/i01-n29-n30-scope-extension.json)
and [predecessor scope extension](../contracts/p2-i3/i01-predecessor-scope-extension.json)

**Evidence effect:** source-current capability evidence only

## 1. Outcome

The current PyGRC source is a strong substrate for P2-I3, but it does not
already contain the trail or stigmergic field relation.

The native shortlist is substantial:

- registered port topology and explicit route validation;
- route-exclusive node coherence as a plausible route-local carrier;
- deterministic, attributable, budget-conserving packet formation,
  reinforcement, and withdrawal;
- distinct geometric, functional, causal-delay, proper-time, and live response
  observations; and
- complete snapshot, load, reset, continuation, and restoration identity.

The missing causal kernel is equally precise:

```text
selected route-local carrier
  + non-static field lifecycle
  + state/history-specific interventions
  + local carrier-to-traversal encounter
  + participant-role separation
```

PyGRC does expose a public synchronous coherence-continuity dynamic through
`GRC9V3.apply_continuity()` and the full `GRC9V3.step()`. It is not integrated
with the LGRC event runtime: `LGRC9V3` explicitly owns a different queue-event
step and does not call the synchronous step. PyGRC has no native autonomous
decay, maintenance, saturation, or field-leakage operation. It also has no
native later-traversal operation that reads only local carrier state and
changes traversal without explicit route/edge addresses, route-order data,
global ranking, or a producer policy. Those are classified source boundaries,
not negative L03 evidence.

They are also not automatic execution blockers. `P2-I3-DEC-017` separates
native capability from producer-completion feasibility: a semantically
adequate native operation has priority, while a missing or unsuitable native
operation must be supplied by the smallest explicit RCAE-owned producer that
preserves the experiment. The remaining native gap is then recorded as an
LGRC naturalization demand rather than hidden or used to weaken P2-I3.

## 2. What was inspected

The audit was performed against clean, unchanged checkouts at the exact
revisions frozen in the input artifact:

| Checkout | Revision | Before | After |
| --- | --- | --- | --- |
| graph/PyGRC | `83e3a300426631ee4df71b661b67d4fcfdfed594` | clean | clean |
| distance theory | `e0d25bf69b8bf681eb8d092ba416497030e5d88e` | clean | clean |

The graph audit covered public model exports, GRC9V3 state and topology,
LGRC9V3 contracts, packet/runtime/timing/restoration surfaces, Phase 8
closeouts, and relevant pre-existing tests. The owner-directed extension first
examined N29/N30, then followed N29's index back to the load-bearing N05, N08,
N09, and N22 mechanism lineage and the supporting N06, N07, N10, N11, N25.2,
and N28 sources. RC-Distance v4 was inspected only for theory-role
consistency.

No synthetic probe, candidate fixture, source change, installed-package
substitution, calibration, or scientific execution was used.

## 3. Environment and conformance

The repository-local environment was used exclusively:

| Component | Identity |
| --- | --- |
| Python | `3.12.3` |
| pytest | `9.1.1` |
| jsonschema | `4.26.0` |
| networkx | `3.6.1` |
| matplotlib | `3.11.0` |
| pyvis | `0.3.2` |
| PyYAML | `6.0.3` |

Pytest was initially absent. Work stopped under `P2-I3-DEC-011`; the project
owner authorized installation into `.venv`, after which the resolved
`pytest==9.1.1`, `iniconfig==2.3.0`, and `pluggy==1.6.0` identities were
recorded and preflight reran successfully.

Six targeted pre-existing-test invocations passed:

```text
24 passed
333 deselected
0 failed
0 errors
```

The selected tests cover topology-route construction, route-aspect fail-closed
validation, deterministic multiple-packet ordering, packet debit/arrival
credit and conservation, separation of three distance surfaces, passive
pulse-surface behavior, producer scheduling boundaries, hidden route-input
rejection, native snapshot continuation, restoration fixed points, and
restoration sensitivity.

## 4. Capability interpretation

### 4.1 Native carrier and formation substrate

`GRC9V3State` exposes node coherence and edge-local conductance, geometric
length, temporal delay, and flux coupling. `LGRC9V3` exposes the state through
public methods and changes node coherence through committed packet debit and
arrival credit.

This makes route-exclusive intermediate-node coherence an adequate
source-current carrier candidate. Repeated arrivals can reinforce it, and
departures can withdraw it. Every event carries explicit time, scheduler,
packet, endpoint, amount, and optional lineage identities.

This is not a realization decision. An edge or corridor carrier may still be
preferable after source admission and I03 comparison.

### 4.2 Why the pulse-substrate surface is not the field

`LGRC9V3CausalPulseSubstrateSurfaceRow` is explicitly a passive evidence row.
It records before/after state, timing, contact, route-aspect, budget, and
lineage information but does not mutate coherence, support, topology, or claim
state. Its feedback and coupling producers schedule later native packet work;
only `step()` mutates runtime state.

That infrastructure is valuable for auditability and for a possible explicit
producer-assisted bridge. It is not a mutable persistent trail field and must
not be reclassified as one.

### 4.3 Why the landscape pheromone classifier is not the field

`inference_pheromone.py` classifies repeated paths from retained checkpoint
evidence and emits observed landscape seed markers. It is post-hoc inference,
not a live route-local carrier, update law, later traversal response, or
candidate execution surface. It is unsuitable as the primary L03 mechanism,
although its evidence vocabulary may later inform analysis.

### 4.4 Synchronous evolution and the missing integrated lifecycle

`GRC9V3.apply_continuity()` publicly updates node coherence by minus `dt`
times current flux divergence. The synchronous `GRC9V3.step()` rebuilds
transport, invokes that continuity update, and also performs the other hybrid
growth, boundary, choice, budget, and identity stages.

That is a genuine native dynamic and must not be erased by saying that PyGRC
has no dynamics. It is not, however, an LGRC event-time trail-field lifecycle.
The public `LGRC9V3` contract explicitly says that its deterministic
queue-event `step()` does not call synchronous `GRC9V3.step()`. Treating the
two as interchangeable would hide execution ownership, update ordering, and
the unrelated state effects of the full hybrid step.

I03 may therefore consider synchronous GRC continuity as a native source
candidate, but only through an explicit admission and composition decision
covering phase order, state effects, clocks, and restoration identity. I01
does not select or authorize that bridge.

Native packet transfer supports formation, repeated accumulation, and
conserved withdrawal. It does not support:

- autonomous decay after activity stops;
- costly maintenance against that decay;
- saturation or bounded field accumulation; or
- field-specific leakage with an explicit destination.

Budget overdraw checks and fixtures named for saturation do not implement
these operations. Multi-basin merge/leakage controls concern topology and
cannot be substituted.

### 4.5 Missing local traversal encounter

Native packet scheduling names source, target, and edge. Static causal routes
and route-aspect producers likewise contain declared route structure.
Feedback producers read committed surface evidence, but their configuration
still names the packet endpoints and edge to schedule. Native route
arbitration ranks topology-event candidates and explicitly does not establish
semantic choice.

Therefore the current source is inadequate for the defining response path:

```text
later probe
  -> encounters local carrier state
  -> local opportunity changes
  -> no route label, explicit outcome address, or global ranker carries result
```

A later RCAE bridge may be warranted, but only if it reads a registered local
carrier and hands an ordinary scheduling request back to PyGRC. It must not
duplicate the runtime or silently become the route selector whose outcome the
experiment claims to observe.

### 4.6 State, history, and controls

Native runtime state is broad: base state, packet ledger, clocks, routes,
event and update logs, surface rows, topology lineage, and producer state are
serialized and restoration-sensitive. But PyGRC has no field-specific public
operation for:

- complete-state-matched history substitution;
- trace shuffle;
- false-trace insertion;
- field clamp; or
- fixed-topology carrier relocation.

LGRC3 topology lineage is not the same operation as fixed-topology trace
relocation. A later RCAE intervention layer must use pure, registered
transformations over complete composite state and state exactly which fields
changed.

### 4.7 Matrix identity and meta-record boundary

`candidate_surface_id` names the exact capability or operation-family target
being audited; it does not assert that the target exists. The classification
field is authoritative. This matters for CAP-06, which audits the compound
withdrawal-plus-autonomous-evolution target, and CAP-07, which validly records
an absent maintenance/saturation/leakage family.

CAP-01 through CAP-13 concern runtime-capability targets. CAP-14 is an audit-
coverage meta-record and CAP-15 is the minimal-assistance demand synthesis;
neither is a PyGRC runtime surface. Likewise, the public callables listed for
OP-07 are the nearest inspected topology-lineage operations and are explicitly
nonqualifying for fixed-topology carrier relocation. The operation matrix
records an empty qualifying-callable set for that leg.

## 5. Geometry and distance interpretation

The source exposes distinct discrete roles:

| Surface | Source-current runtime role |
| --- | --- |
| Registered structure | live port topology and route membership |
| Geometric distance | shortest paths over `geometric_length` |
| Functional distance | shortest paths over inverse conductance or coupling |
| Causal/proper-time distance | shortest paths over explicit edge delays plus node/event clocks |
| Experimental causal influence | not a stored distance; must be estimated from registered intervention and live response |

The current shortest-path helper walks symmetric incident edges. Its causal
distance is therefore an edge-delay annotation, not directed packet influence
or a later-response result. Node proper time and packet event order remain
separate runtime surfaces.

RC-Distance v4 derives spatial support, induced geometry, geodesic distance,
and operational travel time from coherence and its dynamics. It supports the
discipline of separating geometric length from operational response. It does
not make PyGRC's current discrete labels identical to the continuum objects,
nor can it establish a runtime capability.

## 6. Restoration boundary

Native restoration is adequate and unusually complete. `snapshot`, `save`,
`load`, `from_state`, `reset`, and `rebase_reset_baseline` are public.
Restoration identity v1 covers current native state; v2 covers current state
and reset baseline. Pre-existing tests establish fixed points, continued
execution, and sensitivity to queue, clock, ledger, route, topology history,
producer, and source-current surface changes.

The boundary is strict: a future RCAE field law, carrier object, intervention,
participant manifest, or local encounter policy is not covered merely because
the PyGRC state is. Every external component must enter a composite identity.

## 7. What the predecessor lineage changes

N29 is a convergence index and debt atlas, not a substitute for the earlier
experiments it summarizes. Direct inspection establishes a staged
implementation lineage.

### 7.1 N05 and N09 — request producer, native transition

N05's repeated oscillator and N09's GPR4/GPR5 regulation loops show the
narrowest producer boundary. Experiment code reads declared runtime-visible
state, creates an auditable scheduling decision, and calls public packet
scheduling. `LGRC9V3.step()` owns the debit, queue, arrival, and state
transition.

That pattern is useful when PyGRC already has the required transition but not
the eligibility or orchestration policy. It is not automatically suitable for
P2-I3: N09 selects an explicit route to reduce a target-band error. Reusing
that decision would author the outcome. P2-I3 may reuse the typed-request and
ownership pattern, never the goal-directed route-selection semantics.

### 7.2 N08 — the exact trail-memory precursor and its limit

N08 Hypothesis A is the closest predecessor to the P2-I3 field lifecycle. It
maintains route-keyed `memory_strength`, orders decay before reinforcement,
bounds the value, retains route-use attribution, and lets later arbitration
consume the resulting state. This is a real constructed mechanism precedent,
but the field and arbitration are serialized producer/policy surfaces rather
than native PyGRC operations or local encounter.

N08 Hypothesis B demonstrates the complementary insufficiency. Positive
geometry can yield a persistent static route response, while zero-coherence
inserted structure can absorb rather than reinforce. No route-use-linked
conductance update or relaxation emerges. This is why P2-I3 requires a
non-static dynamic rather than replaying a static geometry result.

### 7.3 N22 — declared state producer, native runtime continuation

N22 supplies the strongest precedent for completing a missing native state
operation without editing PyGRC or abandoning the question. Its alternative
nonconsumptive carrier explicitly changes experiment-owned conductance state,
records `producer_mediated` ownership, invalidates derived diagnostics, and
then uses native snapshot, packet readback, replay, reentry, peer controls,
and stress variants. Its closeout never promotes the carrier to native
route-conductance memory.

This proves a load-bearing distinction:

```text
native operation absent
!=
scientifically unrealizable
```

P2-I3 may therefore use a declared state producer if no native operation
preserves the selected field dynamic. It must independently register the
equation, units, update order, state effects, local encounter, complete
identity, and controls.

### 7.4 Supporting and excluded mechanisms

- N06 contributes route-selection and hidden-router audit patterns, but its
  explicit arbitration cannot be the local traversal response.
- N07 contributes neutral-reservoir accounting for conserved withdrawal or
  decay destinations, but not a native decay operator.
- N10/N11 describe the graph-side demand precisely: route-use update,
  relaxation, scope, budget, policy identity, geometry update, and replayable
  state.
- N25.2 establishes native multi-basin runtime context behind N29 Prototype B,
  not a P2-I3 route-local field.
- N28 supplies artifact-level response and perturbation metrics, not fresh
  PyGRC dynamics.
- N29/N30 preserve composition, evidence, controls, and claim boundaries; they
  do not supersede these mechanism-level findings.

The exact findings and 44 predecessor source digests are retained in the
[predecessor mechanism lineage](../contracts/p2-i3/i01-predecessor-mechanism-lineage.json).

## 8. Resulting demand for I02/I03

The audit does not select an implementation. It narrows the legitimate future
comparison to a small set:

1. Admit the exact native topology, packet, synchronous-continuity, timing,
   and restoration surfaces that survived I01.
2. Compare route-node coherence against any justified edge/corridor carrier;
   do not presume the first working surface wins.
3. Select one non-static dynamic, not an all-purpose lifecycle framework, and
   decide explicitly whether synchronous GRC continuity is admissible within
   the LGRC execution boundary.
4. Compose or construct only the field operation and local encounter boundary
   demonstrated necessary by that selection. Missing native coverage is a
   producer requirement, not permission to weaken the question.
5. Prefer native PyGRC mutation, scheduling, and restoration when semantically
   adequate. Otherwise use a declared RCAE state producer with complete
   receipts and composite identity.
6. Bind state/history interventions and participant roles in RCAE with exact
   composite identity.
7. Export every selected non-native function as a precise naturalization-debt
   and proposed graph-experiment record.

## 9. Audit disposition

The machine matrices resolve all fifteen capability questions and all ten
operation requirements. They retain a bounded native shortlist and explicit
missing surfaces without source admission or realization selection.

Accepted review disposition:

```text
P2-I3-SOURCE-AUDIT-GATE = passed
```

The gate opens only I02 exact source admission and Q-002. It does not select a
carrier, dynamic, equation, response, conformance fixture, calibration,
execution, or scientific interpretation.
