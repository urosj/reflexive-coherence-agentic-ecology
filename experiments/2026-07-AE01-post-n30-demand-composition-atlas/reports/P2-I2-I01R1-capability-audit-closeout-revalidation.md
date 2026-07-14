# P2-I2-I01R1 Capability-Audit Closeout Revalidation

**Iteration:** `P2-I2-I01R1`

**Lane:** `AE01-L02`

**Status:** complete; `P2-I2-SOURCE-AUDIT-GATE=passed_after_revalidation`

**Trigger:** owner-supplied I01 capability-audit closeout review received
2026-07-14

**Graph revision:**
`3d3d2ef25903d4210a67980f11fdd3ec21e9b6e5`

**Evidence effect:** source-audit validity and process correction only. No
source admission, realization or dependence-mode choice, calibration,
candidate evidence, control outcome, or L02 result.

## 1. Fail-closed disposition

The review found one material process defect and one overclassification:

1. The custom I01 probe instantiated a candidate-shaped multi-source common-
   carrier chain and compared combined, single-source, and label-permuted
   responses. That exceeds the I01 interface-conformance boundary. Its source,
   hash, commands, and outputs remain in historical command provenance, but
   the probe is quarantined from all capability and scientific evidence.
2. `P2-I2-CAP-04` previously treated native encounter-state persistence and
   ordinary packet transitions as sufficient independent intervention. Native
   packet operations also change packet/event evidence, and no public state-
   only clamp or selective aggregate-history intervention was found. CAP-04 is
   corrected from `adequate` to `inadequate`.

The native source facts supporting CAP-01, CAP-02, CAP-03, CAP-05, and CAP-09
do not depend on the quarantined probe. They remain supported by public source
contracts and pre-existing generic PyGRC tests. The corrected result is a
composition-capable native candidate with incomplete control surfaces, not an
adequate or selected P2-I2 realization.

## 2. Scope and identity revalidation

| Check | Disposition | Evidence |
| --- | --- | --- |
| Exact revision | Pass | Input freeze, source digests, and final graph `HEAD` use the same full revision |
| Worktree before/after | Pass | Clean at entry and closure; rechecked during I01R1 |
| Inspected scope | Pass | Packaging manifest, `src/pygrc/**`, tracked tests/docs, and named closeout artifacts are all inside the frozen tracked-file scope |
| Scope correction | Pass | `P2-I2-CHG-002` added manifest-declared `src/pygrc/**` before package-source inspection or classification |
| Checkout/package identity | Pass | Successful imports and tests forced `${GRC}/src`; the ambient interpreter failure remains infrastructure provenance only |
| Brief-preparation separation | Pass | Preparatory observations remain explicitly non-evidential |
| Graph mutation boundary | Pass | No graph write, installation, generator, formatter, or Git mutation occurred |

The absolute checkout locator appears only as an observed local command/import
locator. Source identity is the repository name, full revision, repository-
relative path, and SHA-256; no machine-local path is an admitted source
identity.

## 3. Existing command and evidence admissibility

| Existing I01 activity | I01R1 classification | Permitted effect |
| --- | --- | --- |
| `CMD-001` through `CMD-006` identity/scope commands | Admissible | Exact checkout, worktree, package-root, and scope facts |
| Frozen static source/test/documentation reads | Admissible | Public contract facts, implementation behavior of public calls, missing-surface search |
| Failed ambient/RCAE/`uv` import attempts | Neutral provenance | Infrastructure facts only |
| Custom `/tmp` multi-source probe | **Quarantined** | Historical reconstructibility only; no capability or scientific support |
| Focused pre-existing PyGRC tests | Admissible | Generic public packet, feedback, restoration, serialization, and continuation conformance only |
| Digest and final Git checks | Admissible | File integrity and unchanged checkout |

No new dynamic probe was run in I01R1. The focused upstream tests are not
P2-I2 fixtures: they exercise generic public runtime and restoration
contracts already present at the frozen revision.

## 4. Complete native-composition check

The surviving source evidence supports the following composition in principle:

| Causal link | Public source fact | Audit judgment |
| --- | --- | --- |
| Multiple attributable contributions | `LGRC9V3.schedule_packet_departure()` accepts source, target, amount, timing, and optional lineage; arrival adds amount to target coherence | Multiple native packets may target the same carrier while retaining separate packet attribution |
| One common carrier | Exported `GRC9V3NodeState.coherence` is one scalar at one node identity | Adequate as a candidate encounter-state carrier; pool role/access semantics remain external declarations |
| Retained state/history | Node coherence and native packet/surface histories serialize in runtime state | State persistence is native; a mode-relevant active aggregate history is not established |
| Carrier-scoped later encounter | `emit_feedback_eligibility_surface_row()` derives a score from declared node masks and current coherence | The read need not address contributor lineage or private slots |
| Separately configurable response path | `set_feedback_coupled_pulse_producer(..., enabled=...)` and `produce_events()` schedule native packet work from a committed feedback row | The response path is public and separately enableable, but this does not supply pool freeze/clamp controls |
| Reconstructible branch identity | Public versioned restoration identity and digest accept an LGRC9V3 model or complete LGRC9V3 snapshot mapping | Adequate for supported native state; external experiment state must be composed later |

RCAE would invoke and configure these native calls, but it need not read
source-specific records, reduce them into a common value, or author the later
native response. This establishes composability of the native pieces. It does
not establish that the control-complete P2-I2 realization is native.

## 5. One-pool and public-support boundary

The node-coherence candidate is one causal scalar, not a container of private
records. Multiple packet arrivals alter that same node identity. Attribution
remains in packet records, while the feedback score reads declared node masks
and current coherence. The packet ledger itself remains inadequate as a pool
because it is partitioned by packet/source/target/edge/lineage.

Public-support inventory:

| Surface | Support class | Boundary |
| --- | --- | --- |
| `GRC9V3NodeState`, `GRC9V3State`, `LGRC9V3`, `LGRC9V3RuntimeState` | Public exports | Stable state/runtime contracts; ecology roles are not native |
| `LGRC9V3.schedule_packet_departure()` | Public non-private model method | Native contribution scheduling; arbitrary fixture activation may still be experiment-owned |
| `LGRC9V3.emit_feedback_eligibility_surface_row()` | Public non-private model method with tracked tests | Carrier-mask read; requires a committed contact row and registered masks |
| `LGRC9V3.set_feedback_coupled_pulse_producer()` / `produce_events()` | Public non-private model methods with tracked tests | Native response scheduling; does not prove pool-specific controls |
| `LGRC9V3.get_state()` / `set_state()` / `snapshot()` / `load()` | Public non-private model methods | Reconstruction/branching; arbitrary direct state mutation is excluded as native intervention evidence |
| `lgrc9v3_restoration_identity_v1()` and digest | Public exports with deterministic/fail-closed tests | Identity, not raw snapshot digest or unrestricted continuation proof |
| Private helper implementations behind the public methods | Internal implementation evidence | May explain public-call behavior; never counted as a callable intervention surface |
| Packet/event/surface logs | Publicly serializable native audit/runtime state | Not automatically an active functional pool or a selective history-control API |
| `annotate_lgrc9v3_causal_history()` and causal-history artifact helpers | Public exports with tracked contract tests | Explicitly derived evidence overlays; they do not execute or mutate the LGRC runtime and are not active pool history |

## 6. Intervention-readiness profile

These labels refine the four-value capability classification without selecting
a realization:

| Required intervention | Readiness | Reason |
| --- | --- | --- |
| Attribution-only label permutation | Native with bounded external orchestration | Public packet scheduling accepts lineage fields; packet ID, arrival mutation, feedback score, and producer decision do not use them as response inputs |
| Pool-write freeze with contributor activity preserved | Requires constructed transition unless a later registered native withdrawal proves adequate | Route/producer disabling exists, but no atomic pool-write gate preserves all unrelated activity |
| Carrier-state clamp | Requires constructed transition | `set_state()` is reconstruction, not an ecology-adequate selective clamp |
| Active-history clamp/shuffle | Requires ecology-owned state or constructed transition | No native aggregate pool-history projection with selective intervention exists |
| Contributor removal | Native with bounded external orchestration | Contribution scheduling can omit or withdraw one source, but matched opportunity semantics are experiment-owned |
| State/history/order variation | Unresolved until mode selection at I03 | Native state and ordered logs exist; separable mode-relevant interventions do not |
| Private-partition substitution | Native with bounded external orchestration plus an external guard | Distinct native nodes are available; matching and no-common-read assertions are not native |
| Direct/controller bypass comparison | Native with bounded external orchestration | Native branches/routes can expose a comparator; causal matching and exclusion semantics remain external |
| Equal-opportunity carrier read without source addressing | Native with bounded external orchestration | Declared node masks provide a common read path; access-scope identity and opportunity matching remain experiment declarations |

## 7. State/history mode-neutral profile

| Capability | Node-coherence candidate | Native log/history candidate |
| --- | --- | --- |
| Encounter-state persistence | Present | Not applicable |
| Ordered-history persistence | Packet/surface provenance accompanies state | Present as serialized packet, event, and surface logs; public causal-history artifacts are derived evidence overlays |
| History accessibility to continuation | Feedback uses the latest committed surface as a trigger but derives score from current node coherence | No generic ordered aggregate-history read was found |
| State-only interventionability | Inadequate: no public selective clamp independent of native audit evidence | Not applicable |
| History-only interventionability | Not established | Inadequate: no selective active-history clamp/shuffle |
| Match state while varying mode-relevant history | Not established | Inadequate beyond attribution-only label variation |
| Match history while varying state | Not established | Not established |

This table does not choose `state_carried`, `history_carried`, or `hybrid`.
The node-coherence route is only a candidate for later I03 evaluation.

## 8. Restoration and state ownership

The public identity and digest accept exactly a concrete `LGRC9V3` model or a
complete LGRC9V3 snapshot mapping in the supported `pygrc.snapshot` version-1
family. They reject a raw digest, an RCAE projection, the wrong family, missing
runtime state, and malformed events/observables. Tracked tests establish
deterministic identity generation, digest-of-identity correspondence, native
load stability, field sensitivity, and bounded equal-input continuation for
declared fixtures. They do not establish raw snapshot byte equality or
unrestricted continuation equivalence.

| State component | Owner | Included in native restoration identity? | Must be externally composed later? |
| --- | --- | --- | --- |
| Graph topology and GRC9V3 dynamic state | PyGRC | Yes | No |
| LGRC9V3 queues, packets, clocks, routes, histories, cached native producer configuration | PyGRC | Yes | No |
| Native events and observables | PyGRC | Yes | No |
| Source attribution fields retained in native packet/runtime state | PyGRC | Yes | No; RCAE interpretation/role mapping remains external |
| RCAE carrier role and access-scope declaration | RCAE | No | Yes |
| RCAE intervention schedule, matching, and control assertions | RCAE | No | Yes |
| Any constructed pool, history projection, gate, clamp, or added dynamics | RCAE | No | Yes |
| RCAE analysis, metric, and registration identity | RCAE | No | Yes |

Raw snapshot digest, restoration identity, identity digest, and bounded equal-
input continuation remain separate concepts. I02 decides whether to admit the
provider and how to compose external state.

## 9. Classification revalidation

All eleven rows retain exactly one frozen classification:

| ID | I01R1 classification | Surviving basis |
| --- | --- | --- |
| CAP-01 | `adequate` | Public scalar carrier and reconstruction surfaces; role/access metadata is non-causal external declaration |
| CAP-02 | `adequate` | Public packet scheduling and additive arrival transition support multiple attributed writes to one target |
| CAP-03 | `adequate` | Public feedback row and producer give a contributor-independent native read/response candidate |
| CAP-04 | `inadequate` | Persistence exists, but independent state/history intervention does not |
| CAP-05 | `adequate` | Static public-call dataflow separates arbitrary lineage labels from carrier/response inputs; no behavioral result is used |
| CAP-06 | `inadequate` | No complete pool-specific freeze/clamp surface |
| CAP-07 | `inadequate` | Native topology substrate lacks matched private-control semantics and guard |
| CAP-08 | `inadequate` | Passive reserve/accumulation/depletion exist; generic saturation/leakage/maintenance do not |
| CAP-09 | `adequate` | Public native identity covers supported PyGRC-owned state with explicit limits |
| CAP-10 | `adequate` | Complete four-value matrix with separated facts/inferences/gaps/questions |
| CAP-11 | `adequate` | Minimal missing transitions are described without authorization or selection |

No row is `unresolved`. The mode-specific intervention choice remains an I03
decision, not an unresolved source-presence question.

## 10. Fact, inference, and judgment separation

The corrected matrix preserves four levels:

```text
source fact:
  a public method, state field, serializer, or test-demonstrated call exists

audit inference:
  those public contracts can compose into a candidate causal path

adequacy judgment:
  one frozen capability question is adequate or fails a named distinction

open question:
  a later gate must select, bind, or test a realization-specific meaning
```

The custom probe is not present in any surviving evidence reference. A later
reviewer may disagree with an audit inference without disputing its source
facts.

## 11. Minimal-gap and shortlist review

The retained missing transitions are interface demands only:

- a selective carrier-write gate or clamp if native withdrawal is inadequate;
- a matched private-partition harness and no-common-read guard;
- an active-history projection/intervention only if a history-bearing mode is
  later selected;
- explicit access-role and opportunity-matching identity; and
- only the selected capacity, leakage, or maintenance transition if later
  required.

No producer implementation, pool algorithm, dependence mode, response,
comparator, control matrix, or scientific preference is selected. The
shortlist is advisory and non-selective.

## 12. Output-package cross-check

The corrected package contains the narrative audit, eleven-row matrix, exact
revision/worktree record, seventeen-file digest inventory, full command
provenance, public-call inventory above, classification rationale, missing-
surface list, bounded shortlist, decision-record correction, checklist/evidence
ledger, and graph read-only validation.

Every matrix runtime claim points to a repository-relative source/test
reference. Every narrative capability conclusion maps to a matrix row. Local
absolute paths remain observations only. `P2-I2-CHG-003` and
`P2-I2-DEC-006` retain the correction and reopening conditions.

Final dependency-free validation recorded:

```text
3 P2-I2 JSON artifacts parsed
11 unique CAP rows; required fields and classification values valid
CAP-04 = inadequate
0 surviving capability rows cite the quarantined probe
17 source digests matched the frozen checkout
11 cited source/test files and 32 symbol references resolved
historical probe source hash matched its quarantined record
13 I01R1 checks complete; 11 I02 checks untouched
master plan/checklist revision = 0.29
172 local Markdown targets resolved across 17 changed/new files
git diff --check = passed
graph revision unchanged; graph worktree clean
```

## 13. Final closeout conditions

| Condition | Disposition after correction |
| --- | --- |
| Frozen scope and source identity reconstructible | Pass |
| Public search sufficient for inadequacy/absence judgments | Pass |
| Every required capability evidenced | Pass |
| Composition assessed as a causal chain, not API inventory | Pass |
| Pool, attribution, intervention, access, and restoration distinguished | Pass |
| Source facts, inferences, judgments, and questions separated | Pass |
| Constructed needs remain minimal demands | Pass |
| Shortlist bounded without admission/selection | Pass |
| No candidate behavior supports the revalidated audit | Pass after quarantine; I01R1 itself executed no candidate probe |
| Graph repository unchanged | Pass |

The corrected package re-passes `P2-I2-SOURCE-AUDIT-GATE`. I02 is ready but
not begun. No source or restoration provider is admitted.
