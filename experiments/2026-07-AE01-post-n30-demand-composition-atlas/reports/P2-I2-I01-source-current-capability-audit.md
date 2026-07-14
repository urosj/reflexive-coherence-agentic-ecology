# P2-I2-I01 Source-Current PyGRC Capability Audit

**Iteration:** `P2-I2-I01`

**Lane:** `AE01-L02`

**Status:** corrected and revalidated by `P2-I2-I01R1`;
`P2-I2-SOURCE-AUDIT-GATE=passed_after_revalidation`

**Audited revision:**
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`

**Worktree boundary:** clean before and after; graph repository read-only

**Evidence effect:** public capability, native adequacy, and missing-surface
classification only. This report does not admit the source revision, select a
realization, authorize calibration/execution, or assign an L02 result.

Controlling audit artifacts:

- [input freeze](../contracts/p2-i2/i01-audit-input-freeze.json), including the
  recorded `P2-I2-CHG-002` package-root correction;
- [capability matrix](../contracts/p2-i2/i01-capability-matrix.json);
- [source-digest inventory](../contracts/p2-i2/i01-source-digests.json); and
- [command provenance](P2-I2-I01-command-provenance.md).

Closeout correction:
[I01R1 capability-audit revalidation](P2-I2-I01R1-capability-audit-closeout-revalidation.md).

## 1. Disposition

The source-current revision has a bounded, composition-capable native
candidate for the central encounter-state form of the L02 discriminator:

```text
two attributable native packet paths
  -> additive arrivals into one declared target-node coherence carrier
  -> one native feedback-eligibility surface reads current carrier state
  -> one model-owned feedback producer schedules a later native packet
  -> native event queue processes the later response
```

Static public-source and pre-existing generic-test evidence shows that this
chain can compose without RCAE calculating the combined pool state or
authoring the later response. Source attribution remains in packet/lineage
evidence; the carrier holds the combined scalar state. The later feedback
calculation reads registered node masks and current coherence, not contributor
labels.

Native restoration is adequate for that entire PyGRC-owned chain. The new
versioned identity includes embedded GRC9V3 continuation state, the LGRC9V3
runtime artifact, queues, ledgers, causal routes, surface and topology logs,
cached producer configuration, events, and observables.

The native gaps are mostly experimental-control and ecology-role surfaces:

- no first-class pool role or access-scope identity;
- no matched private-partition control contract or no-common-read guard;
- no selective pooled-history shuffle/permutation API;
- no atomic pool-specific write-freeze and value/history-clamp API; and
- no generic pool capacity/saturation, leakage/decay, or maintenance dynamics.

These gaps include the absence of a public state-only intervention independent
of native audit evidence. They do not force a constructed pool, but they mean
that I01 does not classify the complete native realization as adequate. I03
must test native controls first and authorize only the smallest explicit RCAE
control or producer boundary where the native surface is inadequate.

I01R1 quarantined the original custom multi-source behavioral probe because it
crossed the I01 interface-conformance boundary. Its commands and outputs remain
historical provenance, but no capability classification or scientific claim
uses them.

I01R1 also rechecked the public causal-history helpers rather than inferring
absence from naming. They build or attach derived evidence overlays and
explicitly do not execute or mutate the LGRC runtime, so they do not supply an
active pool-history carrier or selective history intervention.

## 2. Bounded native shortlist

| Surface | Audit classification | Native role | Important boundary |
| --- | --- | --- | --- |
| One target node's `GRC9V3NodeState.coherence` plus the native packet ledger | `adequate` | Common encounter-state carrier with attributable native contributions | “Pool” and access scope are experiment declarations, not PyGRC semantics |
| `emit_feedback_eligibility_surface_row()` plus the feedback producer and queue | `adequate` | Combined-state read and bounded later response without contributor addressing | Front/rear masks, threshold, and opportunity remain registered inputs |
| `lgrc9v3_restoration_identity_v1()` and its digest | `adequate` | Exact native branch identity | RCAE control/role/intervention identity remains external |
| Packet ledger used as the claimed pool | `inadequate` | Per-packet attribution and budget audit only | It remains partitioned by source/target/edge/lineage and is an insufficient repetition case |
| Route replacement, producer enable/disable, topology branching, and state/reset APIs as a full control bundle | `inadequate` | Useful native control primitives | No complete pool-specific freeze/clamp or private-partition contract |
| Multi-basin merge/leakage evidence as a generic pool | `inadequate` | Topology-specific flow/control evidence | It is not a generic contribution/carrier/read surface |

This is a shortlist, not a realization decision. I02 must first decide source
admission and restoration-profile transition. I03 then selects or rejects the
native encounter-state realization against the full discriminator and control
obligations.

## 3. Capability-question results

| Question | Classification | Result |
| --- | --- | --- |
| `P2-I2-CAP-01` native non-private carrier | `adequate` | One topology node provides reconstructible scalar state; the fixture must declare and verify its shared access role |
| `P2-I2-CAP-02` two attributable contributions | `adequate` | Multiple native packets can debit distinct sources and add into the same target while retaining packet/lineage attribution |
| `P2-I2-CAP-03` contributor-independent later read | `adequate` | Native feedback eligibility reads current node coherence through registered masks; the producer does not consult contributor labels |
| `P2-I2-CAP-04` persistent/intervenable encounter state or history | `inadequate` | Node coherence persists, but native writes also change audit evidence; no public state-only clamp or selective aggregate-history intervention is established |
| `P2-I2-CAP-05` label and carrier interventions | `adequate` | Audit labels can be permuted without changing the causal response; carrier state can be altered through native contribution/debit paths |
| `P2-I2-CAP-06` write freeze and clamp | `inadequate` | Some producer/route withdrawal is public, but no atomic pool-specific write gate or carrier/history clamp preserves every unrelated activity |
| `P2-I2-CAP-07` private partition | `inadequate` | Separate native nodes are available, but matched marginal/opportunity semantics and the no-common-read guard are not native |
| `P2-I2-CAP-08` reserve and pool dynamics | `inadequate` beyond passive conserved mode | Reserve, accumulation/mixing, and depletion are observable; generic capacity, saturation, leakage, and maintenance are absent |
| `P2-I2-CAP-09` restoration coverage | `adequate` | Native identity covers the bounded native core and producer configuration; external experiment state must be composed separately |
| `P2-I2-CAP-10` complete classification | `adequate` | Six candidate-surface classes and all eleven questions have explicit dispositions and evidence |
| `P2-I2-CAP-11` minimal producer demand | `adequate` as audit output | Each inadequate surface has a bounded fallback description; none is authorized or selected here |

The machine-readable matrix contains the public facts, inference, evidence
references, missing distinction, minimal fallback, restoration coverage, and
open questions for every row.

## 4. Native causal factorization

The audited native core can instantiate the brief's factorization without
using the packet ledger as the response input:

```text
common carrier:
  C_P <- native packet arrivals credit one declared target node coherence

audit lineage:
  L <- native packet records retain source node and optional lineage ids

later response:
  Y <- native feedback row derives a score from current node coherence;
       native producer schedules work when the registered threshold is met

forbidden bypass avoided in the audited core:
  Y does not read source_lineage_id, contributor slots, or success labels
```

The response still cites the latest committed contact surface as its trigger.
I03 must ensure that the registered later opportunity is common-carrier based
and that the trigger does not become a source-specific shortcut. This is a
realization-bound discriminator decision, not an unresolved I01 source fact.

## 5. Conformance-evidence boundary

The original custom five-node probe compared combined, single-source, and
label-permuted response behavior. I01R1 classifies it as candidate-shaped and
therefore inadmissible at the capability-audit gate. Its full source, hash,
command, and outputs remain in command provenance so the process defect cannot
be erased. They support no row in the corrected matrix.

The admissible focused checkout suite passed:

```text
38 passed, 8 subtests passed
```

These are pre-existing generic PyGRC tests, not P2-I2 fixtures. They covered
restoration identity and sensitivity matrices plus packet
departure/arrival budget, feedback scheduling and subthreshold behavior,
arrival-triggered routing, snapshot serialization, and native continuation
after load.

## 6. Restoration boundary

Native identity covers:

- target-node coherence and the rest of embedded GRC9V3 state;
- packet queue, packet records, lineages, and conserved budget;
- scheduler/checkpoint/proper-time state;
- causal routes and producer configurations;
- contact/feedback surface rows, production records, and event history; and
- native events and observables.

If the native node-coherence carrier is later selected, that carrier state is
already native and must not be duplicated as an external pool component.

The following remain external and require their own stable identity when
selected:

- RCAE fixture-role and access-scope declarations;
- source/admission and intervention schedules;
- control-pairing and no-common-read assertions;
- analysis and metric identities; and
- any RCAE producer, selective history projection, gate, clamp, capacity,
  leakage, or maintenance state actually authorized by I03/I06.

I02 must explicitly admit the restoration helper and digest if selected. The
P2-I1 RCAE restoration projection cannot silently become the P2-I2 native
provider.

## 7. Minimal producer and missing-surface demands

The audit does not authorize these fallbacks. It constrains the smallest
later choice:

| Missing or inadequate native surface | Native-first action | Smallest fallback if native remains inadequate |
| --- | --- | --- |
| State/history intervention independent of audit evidence | Try native route/producer withdrawal while preserving the registered matched boundary | One RCAE carrier-write gate/projection clamp, or an explicitly producer-assisted active-history projection only if that mode is later selected |
| Initial arbitrary source activation | Try native upstream routes/producers where they preserve the selected discriminator | RCAE writer schedules initial native packets only; PyGRC computes carrier and response transitions |
| Pool role/access identity | Use topology and registered node masks as the witness | RCAE role/access registry with no causal state |
| Private partition | Use distinct native nodes and native packets | RCAE matched-branch harness that keeps responses separate and forbids aggregation |
| Label permutation | Swap native packet lineage strings | No causal producer; RCAE only compares the registered causal projection |
| Pooled-history shuffle | Use only if a native history surface adequate to the selected mode is found | RCAE projection over native logs, with the shuffled projection explicitly producer-assisted |
| Pool write freeze/clamp | First try route removal or producer disable while preserving source activity | One RCAE gate around pool-write calls or one declared carrier projection clamp, with withdrawal and construction debt |
| Capacity/leakage/maintenance | Prefer passive conserved-carrier mode and classify these inapplicable | Add only the selected scalar state/transition, never a bundled resource economy |

These are the graph-side demand fields to carry forward. They are not evidence
that PyGRC should immediately implement all of them; recurrence priority
belongs to P2-I8 after independent lanes close.

## 8. Gate evaluation

```text
frozen audit scope
+ complete eleven-question capability matrix
+ exact revision, source paths, source digests, and command provenance
+ native adequacy classifications and missing-surface distinctions
+ bounded native shortlist
+ no source admission, realization selection, or lane-result overclaim
+ unchanged clean graph worktree
= P2-I2-SOURCE-AUDIT-GATE passed
```

I01R1 re-passed the source-audit gate for this corrected package. I02 is ready
but not begun; I03 remains blocked until I02 resolves.
