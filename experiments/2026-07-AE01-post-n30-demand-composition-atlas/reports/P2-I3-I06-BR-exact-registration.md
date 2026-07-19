# P2-I3-I06 B-R exact implementation registration

## Disposition

The B-R I06 package is complete and ready for one owner review of exact
registration completeness.

```text
P2-I3-I06 implementation:       owner-accepted and complete
P2-I3-REG-GATE:                 passed after owner acceptance
P2-I3-EXEC-FREEZE:              unopened
candidate execution:            not authorized and not performed
scientific/control execution:   not authorized and not performed
integrity-fault dispatch:        not authorized and not performed
C.2 work:                        unopened
scientific or ecology result:    none
```

I06 turns accepted DEC-042 through DEC-046 semantics into one closed inactive
execution registry. It does not test whether the registered B-R structure
works scientifically. It fixes what a later test would be allowed to run,
which comparisons must close, what artifacts must exist, and how failures may
propagate before any outcome is known.

This report describes corrected package `1.0.1`. Initial package `1.0.0` was
reviewed before acceptance and superseded. The bounded correction changed no
accepted decision, matrix population, resource envelope, or execution
authority. It corrected the DEC-038 estimator projection, restored the full
DEC-037 observation split and DEC-042 undirected-edge/request-whitelist
boundary, replaced heuristic control selectors with exact case-set bindings,
and separated the four DEC-040 control-lifecycle fields. `REG-GATE` remained
closed throughout.

## Why this registration matters for agentic ecology

P2-I3 is not asking merely whether LGRC9V3 can move coherence or whether an
RCAE producer can schedule packets. N31 already established a bounded
producer-mediated conservative-redistribution contract. The ecology question
is whether repeated attributable activity can compose that contract into a
route-local, non-static aftereffect which changes a later local possibility
without a hidden global selector.

The registration protects that question in four ways:

1. it separates formation, route-local carrier, isolated export reservoir,
   and later encounter roles geometrically;
2. it fixes W/O/E and targeted control comparisons before observing whether
   any route becomes easier or harder to traverse;
3. it makes complete current state, historical provenance, participant class,
   local route role, and future schedule distinct pairing dimensions; and
4. it records the exact native/RCAE ownership boundary and producer burden so
   a positive-looking result cannot be relabeled as a native LGRC primitive.

The registered result ceiling remains a bounded B-R trail-field or, only with
the conditional fresh-nondepositor evidence, stigmergic-field candidate. It
cannot establish a general decay law, autonomous native decay, communication,
coordination, motif, regime, agency, or selfhood.

## Authority and runtime boundary

The package consumes:

- RCAE source anchor `2e63a0dc6147bf124966374341c126f09b765cdd`;
- accepted `P2-I3-DEC-027` through `P2-I3-DEC-046`;
- the admitted N31 B-R contract
  `n31_B_R_conserved_redistribution_contract_v2`;
- clean graph revision
  `565706f8b7647f6b7638b9afbe52372e170bf724`; and
- the accepted I05 shared resolution `delta=1/1000000000000`.

PyGRC distribution metadata is not runtime authority. The local `.venv`
contains package metadata and an installed copy, but the exact graph `src`
files used by N31 are the governing runtime source. Every I06 command therefore
requires `PYTHONPATH=${RCAE_PYGRC_ROOT}/src`, verifies the admitted source
digests and clean graph revision, and refuses an ambient or installed fallback.
No machine-local absolute path is retained. The graph repository remains
read-only.

## Registered geometry

Each deterministic realization contains fourteen nodes and fourteen
structurally undirected native port edges. The only shared nodes are invariant
origin `O` and target `T`.

```text
                       A_d
                        |
O -- A_s -- A_m -- A_x -- T
     |       |
   A_z_s   A_z_m

                       B_d
                        |
O -- B_s -- B_m -- B_x -- T
     |       |
   B_z_s   B_z_m
```

The diagram is relational rather than a layout claim. `A_d` and `B_d` are
isolated export reservoirs with no outgoing registered edges. `z_s` and `z_m`
are explicit control destinations. There are no interior cross-route edges.
The two routes share no mutable field, packet, selector, or interior node.

Every edge machine record binds unit conductance, unit base conductance, unit
geometric length, zero initial flux, and zero flux coupling. Direction enters
only through a separate operation-role request whitelist: formation is
`s_e -> m_e`, encounter is `m_e -> x_e`, export is `m_e -> d_e`, and control
transfers target `z_s` or `z_m`. Shared boundary edges have no permitted
packet request. Every unregistered reverse request is prohibited. Constructor
endpoint order does not turn the native port edge into a directed topology.

For route `e`:

```text
s_e -> m_e      costly attributable formation transfer
m_e -> d_e      producer-authorized conservative export
m_e -> x_e      fixed branch-local native encounter request
```

Three realization IDs—`101`, `211`, and `307`—apply different raw node and
edge allocations while preserving those roles. They are deterministic
permutations, not random seeds or sampling replicates. Their role maps differ,
their semantic design does not, and producer code is forbidden from reading
raw identity as a route preference.

The six immutable substrate bases are:

```text
2 internal delay profiles (tau=1, tau=2)
x
3 raw-ID realizations (101, 211, 307)
=
6 substrate bases
```

I06 constructed each base using LGRC9V3, then verified native restoration-v2
identity across save/load and reset. That produced six model constructions,
six save/load pairs, and six resets with zero formation, lifecycle, encounter,
or control operations.

## Exact values and internal schedule

The dyadic baseline is:

```text
C(s_e)   = 7/8
C(m_e)   = 3/16
C(x_e)   = 1/4
C(d_e)   = 1/16
C(z_s)   = 1/16
C(z_m)   = 1/16
C(O)     = 1/2
C(T)     = 1/2

C_floor  = 3/16
q_cap    = 3/32
q_probe  = 15/64
```

Repeated formation is three transfers of `3/32` at internal times `0`, `4`,
and `8`. The quantity-matched one-pulse history is one `9/32` transfer at time
`8`. Lifecycle opportunities occur at `12`, `16`, `20`, and `24`. Clean
terminal encounter forks are registered at `j1=16`, primary `j2=20`, and
floor `j3=28`. `E3` is retained as an unprobed carrier checkpoint; `E4` is the
eligible-zero floor opportunity.

The registered `m_trace=2` and `m_export=4/5` values remain construction
targets, not pass thresholds. The shared `delta` applies only to derived
response arithmetic. Conservation, restoration, causal-projection, and
held-fixed equality remain exact. As elsewhere in the atlas, a narrow,
same-side, mixed, counterdirectional, or unexpectedly strong result requires
interpretation; a numeric crossing alone is not an accept/reject oracle.

The exact DEC-038 arithmetic is retained as:

```text
N(a,b)    = (mu_a - mu_b) / max(abs(mu_a), abs(mu_b), delta)
m_trace   = N(E,W)
m_export  = N(O,E)

mu_W = -3/64
mu_E =  3/64
mu_O = 15/64

m_trace  = (3/32) / (3/64)  = 2
m_export = (3/16) / (15/64) = 4/5
```

The validator recomputes these values from exact rationals and separately
checks formula text, numerator, denominator, and target. Float values are
projections only.

Observation surfaces also remain distinct. Native event/internal time is
measured from the event key, scheduler order, and local event frontier.
Shortest-path causal delay, geometric distance, and inverse-conductance
functional distance are derived annotations only. Experimental causal
influence is a mandatory estimate from measured intervention arms; no graph
annotation can satisfy it.

## Restoration and identity design

Every future checkpoint is one logical eight-file bundle:

```text
native.json
native-identity-v2.json
policy.json
execution.json
measurement.json
reset.json
audit.json
manifest.json
```

The package registers separate meanings for:

- original native bytes;
- native restoration-v2 semantic identity;
- complete exact native-plus-RCAE execution identity;
- closed causal-continuation projection;
- semantic branch key; and
- fresh branch/audit instance identity.

Later resaving need not reproduce native serializer bytes. Loading must
reproduce the native restoration-v2 semantic identity. A reset must reproduce
the same causal and cell semantics while issuing fresh evidence lineage and
therefore a distinct exact bundle identity.

The closed execution-record schema fixes machine shapes for checkpoint
manifests, attempt terminals, case resolutions, control-leg resolutions,
resource receipts, and cycle closeout. Unknown continuation-relevant fields
fail closed. No terminal record instance or observed disposition exists in
I06. A control-leg record keeps `execution_status`, `evidence_resolution`,
`control_resolution`, and `terminal_guard_status` separate under the exact
I04 enums.

The registration JSON Schema is deliberately described more narrowly: it is
a closed-root structural envelope, not complete experiment semantics. The
retained semantic validator is mandatory and reconstructs the topology,
estimators, observation roles, populations, exact case sets, pairings,
resources, attempts, dependencies, producers, and gate stops. Schema-only
acceptance is prohibited.

## Matrix closure

The exact top-level configuration families are:

| Family | Configurations |
| --- | ---: |
| W/O/E core | 18 |
| formation quantity/history | 6 |
| focal/reference role exchange | 18 |
| current-state relocation | 6 |
| carrier-matched false trace | 6 |
| causal-projection-matched false trace | 6 |
| equal-carrier clamp | 6 |
| reservoir clamp | 6 |
| export-mass/organization | 6 |
| export-policy omission | 6 |
| lifecycle-schedule omission | 6 |
| **Total** | **90** |

The 378 scientific branches close as:

```text
126  core: one unprobed trajectory + six terminal probes per cell
 60  formation/history and causal-projection false trace
180  remaining added control configurations
 12  conditional fresh-nondepositor terminal probes
---
378
```

The separate integrity population is exactly:

```text
18 cell envelopes
x
4 malformed request classes
  invalid load / reset / branch / continuation
=
72 quarantined integrity cases
```

These 72 cases are not native field-limited refusals and cannot produce a
scientific comparison. They later test only whether composite coordination
fails closed.

Every live branch must produce source/runtime identity, before/after composite
identity, causal receipts, formation-cost and conservation receipts, request
and native-disposition records, forbidden-read instrumentation, producer
receipts, reconstruction selectors, a resource receipt, and attempt/case
terminal records. No execution class may delete one of those obligations.

## Pairing, controls, and evidence ownership

The complete pairing key contains fourteen dimensions:

```text
delay profile
realization
role assignment
base arm or treatment
control family
checkpoint or encounter
participant class
route role
clean parent semantic identity
causal projection identity or match
request construction
request timing
future schedule
observation boundary
```

Only prospectively declared intervention fields may differ within a matched
comparison.

All 42 I04 control-leg identities are independently projected into I06 through
a central registry of 24 digest-bound exact case sets. Each leg now has
intervention fields, held-fixed fields, pairing exemption, scientific or guard
class, minimum artifact count, completion rule, exact case-set selectors, and
required evidence artifact roles.
Observed resolution and evidence references remain empty. A shared artifact
may satisfy several legs, but it cannot copy one leg's disposition into
another.

This keeps raw-ID permutation separate from focal/reference role exchange,
binds surface dependence to W/E withdrawal, relocation, role/raw-ID changes,
and both false-trace levels, and applies conservation, leakage, and the
participant/medium boundary across all 378 live scientific/control branches.
Every applicable scientific leg selects a nonempty exact case population.

The 14 supplemental discriminator, validity, and claim requirements have
their own exact populations and I09/I10/I11 ownership. In particular,
DISC-01 selects formation quantity/history, DISC-02 export
mass/organization, DISC-03 the repeated/one-pulse and causal-projection
state/history population, DISC-04 matched `tau-1`/`tau-2` core cases, and
DISC-05 exactly the twelve fresh-nondepositor probes. I06 does not prejudge
any requirement.

Case-set membership is stored as 1-based ordinals over the already frozen
`72 integrity + 378 scientific` matrix order, with exact case-ID and
configuration-ID membership digests. The validator reconstructs and checks
every selected identity. This removes repeated long IDs without weakening the
selector contract and keeps the 991,536-byte registration below the existing
1 MiB individual-artifact review boundary.

## Candidate-free timing and future resource envelope

The retained timing characterization used seven monotonic repetitions for:

- fresh Python startup;
- inert JSON load;
- a fixed two-event native packet operation on a two-node non-candidate model;
- eight-component generic serialization;
- schema validation; and
- eight-component reconstruction reads.

It consumed no candidate topology, values, artifact, producer result, control
disposition, or outcome. The raw observations and maximum-based reference
derivation are retained. Host memory, swap, cgroup, CPU count, platform, and
the distinction between identity versus observation-only resource fields are
also retained without a machine path.

Prospective class assignment is:

| Class | Cases | Timeout per case |
| --- | ---: | ---: |
| `probe_only` | 288 | 5 s |
| `standard_trajectory` | 48 | 20 s |
| `complex_construction_or_comparison` | 42 | 45 s |
| `integrity_fault` | 72 | 5 s |

The timeout is the maximum of a class minimum and eight times the measured
reference projection, bounded by the accepted 180-second scientific and
60-second integrity outer limits. In this characterization the class minima
remain controlling.

The complete future campaign ceiling is:

```text
primary child allowances       4,650 s
aggregation allowance          1,800 s
campaign overhead                600 s
four retry + grace reserves      115 s
retry administration               5 s
                              --------
exact registered ceiling        7,170 s = 1 h 59 m 30 s
outer campaign ceiling        108,000 s = 30 h
```

This is a maximum authorization envelope. It is neither estimated successful
runtime nor work performed by I06.

Storage closes separately:

```text
logical artifact maximum             7,147,094,016 bytes
prospective unique physical blobs     1,484,783,616 bytes
prospective retained logs               943,718,400 bytes
maximum active temporary work            33,554,432 bytes
incremental four-class retry reserve     109,051,904 bytes
governed physical projection           2,571,108,352 bytes
governed physical ceiling              8,589,934,592 bytes
```

Logical bytes intentionally may exceed the physical projection because exact-
byte SHA-256 deduplication can map several logical components to one immutable
blob. Semantic equivalence never permits deduplication. The retained I06 file
set is below both repository retention-review thresholds: the largest file is
871,585 bytes and the selected set is below 10 MiB.

No experiment `RLIMIT_AS` or RSS kill threshold exists. The future runner must
observe memory and classify OOM or native memory failure as infrastructure,
never negative L03 evidence.

## Attempts, failures, and fixed schedule

The registry contains 450 primary slots, zero scientific retries, and one
inactive pre-P5 retry position per case. Four class tokens may each be
allocated at most once to the first eligible pre-scientific failure in frozen
schedule order. Thus the maximum governed child-start count is 454.

The schedule places all 72 integrity cases first, then scientific cases in
fixed substrate/configuration/branch order. Each case names its immutable
baseline, trajectory, checkpoint, or cell-envelope parent. The validator
resolves every parent reference and freezes five failure-propagation classes.
Result-responsive reordering is forbidden.

P0 through P7, the supervisor-owned P5 boundary, campaign/case claims, one
bounded supervisor resume, retry allocation, closed attempt statuses, final
case resolution, and cycle precedence are all machine-retained. Nothing in
I06 creates a campaign claim or P5 token.

## Producer accounting

The static inventory contains seven non-overlapping items:

| ID | Class | Meaning |
| --- | --- | --- |
| `BR-PROD-01` | `contract_required` | export eligibility, amount/cap, time, destination |
| `BR-PROD-02` | `contract_required` | lifecycle state needed for mechanism continuation/reset |
| `BR-PROD-03` | `rcae_ecology_required` | fixed field-blind local encounter request |
| `BR-PROD-04` | `rcae_ecology_required` | atomic native-plus-RCAE composite coordination |
| `BR-PROD-05` | `evidence_only` | control construction |
| `BR-PROD-06` | `evidence_only` | restoration/reconstruction verification |
| `BR-PROD-07` | `evidence_only` | supervision, telemetry, and ledger governance |

Every item has expected counts across 90 configurations, 378 scientific
branches, and 72 integrity cases; causal position; state/schedule burden;
omission effect; restoration role; and naturalization debt. Mechanism
restoration and evidence-only verification are distinct items. Later realized
cost remains six unsummed dimensions; there is no scalar producer-cost score.

## Validation and reconstruction

Commands assume a locally chosen graph checkout:

```text
export RCAE_PYGRC_ROOT=../graph-reflexive-coherence
```

Build the retained candidate-free package:

```text
env PYTHONPATH=${RCAE_PYGRC_ROOT}/src \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -B \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i06_br_registration.py \
  build --graph-root ${RCAE_PYGRC_ROOT}
```

Read-only validation and non-destructive reconstruction use the same
environment with `validate` and `reconstruct`. Reconstruction writes to:

```text
outputs/reconstruction/p2-i3-i06-br-registration-validation.reconstructed.json
```

The retained and reconstructed validation files compare byte-exactly. Timing
observations are not expected to recur byte-exactly; a new timing run is a new
characterization. Reconstruction validates the retained observations and all
derived values without pretending host elapsed time is deterministic.

Focused results:

```text
registration validator:     25 / 25 passed
new adversarial tests:       36 / 36 passed
current I03/I04/I06 tests:   66 / 66 passed
I05 final closeout:          49 / 49 passed
```

One old I05 inactive-freeze test still asserts that the later accepted I05
launch authorization does not exist. That assertion is historical and stale
after completed I05; it is not used as a current-state gate.

A repository-wide atlas test run, with that one assertion deselected, produced
254 passes, 33 passing subtests, and five failures outside P2-I3 I06. They are
retained as existing-state diagnostics rather than repaired in this iteration:

- one P2-I1 conceptual-source digest has drifted from its historical registry;
- the local `.venv` has Matplotlib `3.11.0` while one P2-I2 test expects
  `3.10.9`;
- one P2-I2 pre-activation test requires an authorization that has since been
  created and consumed to remain absent; and
- two P2-I2 I05B tests detect historical I04R2 frozen-hash drift.

None of those files or authorities is consumed by the I06 validator. The
focused current-state P2-I3 and I05 closeout checks above are the relevant
regression boundary.

## Artifact identities

```text
registration policy
3db143f93f06246935d0665a5d53e4e2c729f0b4380b9a7e4a9eca0b212e590d

candidate-free timing
7644d54098cbbfe8c9b447b75500104cfcf5e28bfd9b3c4a54d724775af98973

exact registration
60f662965ce7c84c0b909a59b4826dbd8bb9cb400500dc14bb8b312790cc3af9

registration validation
531221f4eb15f30084584b8ac55dde2509db636ba588d2b995ba7d9ae39be597

registration schema
6efb99c60f468d857b5140f64897cdbca280ccc9272aba26694125fcf7519ac8

execution-record schema
de7887c9ad484caf973efe7fec8469243e29125c7a2065102decf988abedb1c1

builder/validator source
1b38247344b200f9398c2294ed5eb377ccc41a889d3853546899ff284a96ba6b

focused test source
295eddbcec96fcb62be6742d9ba10acd1fc9a8f5ff8883603f1061c54a681fb1
```

The exact registration's canonical payload digest is:

```text
9981d03df09f90d9507d038fc6581e35daa3fa085650c00db1144c968b581552
```

## Interpretation and next boundary

I06 demonstrates that the accepted B-R theory can be projected into a finite,
closed, source-bound experiment without selecting an outcome. It shows that
the geometric carrier/reservoir/encounter separation, state/history
discriminator, role permutation, exact restoration, control families,
producer attribution, and failure governance are implementable together.

It does **not** show that a trail field forms, that conservative export changes
later admissibility, that current state is sufficient, that perturbations are
stable, or that fresh participants respond. Those are future execution and
analysis questions.

## Owner acceptance and gate effect

The owner accepted corrected I06 package `1.0.1` on 2026-07-19. The
[acceptance record](../contracts/p2-i3/i06-br-owner-acceptance-and-reg-gate.json)
binds the policy, timing characterization, exact registration, retained
validation, both schemas, mandatory semantic validator, and focused
adversarial tests.

Acceptance-record SHA-256:
`3fdf921893083505fad6889567698b58dd7dbd5efdbbb1f5c32687947630faa1`.

Acceptance changes governance only:

```text
P2-I3-I06 = accepted and complete
P2-I3-REG-GATE = passed
next required boundary = clean retention commit
then = P2-I3-I07 inactive execution-freeze construction and Q-019
```

REG-GATE does not pass `P2-I3-EXEC-FREEZE` and authorizes no candidate,
control, or integrity-fault operation. I07 requires a separate clean committed
source anchor, inactive freeze, review, and explicit activation.
