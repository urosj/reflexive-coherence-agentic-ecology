# P2-I3 B-R I03 Operational-Conformance Review

**Review date:** 2026-07-19

**Disposition:** accepted; `P2-I3-DISCRIMINATOR-GATE` passed

**Evidence effect:** implementation adequacy and operational expressibility
only

## 1. Accepted conclusion

> At the exact admitted RCAE and PyGRC source identities, the producer-mediated
> B-R realization is operationally expressible. Repeated native formation,
> serialized conservative export, fixed local encounter, native admission and
> refusal, composite restoration, control addressability, and conformance
> quarantine can be composed without an RCAE producer reading or authoring the
> later native disposition.

This is the I03 ceiling. It does not support `AE01-H-L03`, pass an operational
hypothesis, assign R01–R05, validate a scientific control, select B-R over C.2,
or establish a trail or stigmergic field candidate.

## 2. Verified semantic result

B-R is realized as conservative redistribution:

```text
m_e --q--> d_e

Delta C(m_e) = -q
Delta C(d_e) = +q
Delta global node-plus-packet coherence = 0
```

The retained fixture begins with total coherence `2.2`. Native formation
debits sources by exactly the amounts credited to route-local carriers. One
producer-authorized native export moves `0.1` from one carrier to its isolated
reservoir. The global total remains `2.2` at every retained checkpoint.

The later equal requests ask for `0.45`. Native source-coherence admission
accepts the request from the carrier retaining `0.5` and atomically refuses the
request from the carrier reduced to `0.4`. This is a deliberately constructed
admissibility boundary for conformance. It is not a measured decay rate,
calibrated margin, registered value, or scientific effect.

The precise interpretation is:

> A producer-authorized conservative export reduced the coherence locally
> available at the registered carrier.

## 3. Corrected ownership statement

The conformance review corrects any wording that assigns the complete event
schedule to PyGRC.

```text
RCAE owns:
  lifecycle eligibility
  receipt serialization and consumption
  export floor/cap policy
  source, destination, and route bindings
  construction and scheduling of native packet requests
  structural encounter opportunities
  branch and composite-manifest coordination
  control identities and quarantine

PyGRC owns:
  coherence state
  source debit and destination credit
  packet creation and ledger
  native ordering and event-queue progression
  transport
  source-coherence admission
  typed native refusal
  settlement
  native snapshot, save, load, and reset surfaces
```

Therefore:

> RCAE owns the lifecycle and request schedule; PyGRC owns the native ordering,
> admission, progression, refusal, and settlement of each scheduled native
> operation.

Composite restoration is factored similarly: PyGRC restores native state;
RCAE validates and restores the complete native-plus-policy composition.

The export policy causally constructs the weakened-carrier condition. The
encounter adapter does not read carrier value, history, competing-route state,
participant or route labels, rank, or expected outcome. It therefore does not
manufacture the later native disposition through an outcome-aware selector.
Any later positive B-R result remains producer-mediated and retains
naturalization debt.

## 4. Section 8.2 closure crosswalk

All fifteen realization requirements close at I03, but through distinct
evidence types rather than one undifferentiated runtime proof.

| Item | Requirement | I03 closure basis |
| --- | --- | --- |
| 1 | Two alternative route surfaces | Runtime-conformed synthetic fixture |
| 2 | Route-local encountered field | Runtime-conformed fixed local encounter |
| 3 | Repeated attributable costly formation | Runtime-conformed native transfers and debits |
| 4 | Selected non-static dynamic | Runtime-conformed conservative export; no scientific measurement |
| 5 | Dynamic-to-traversal architecture | Runtime-conformed synthetic branch split |
| 6 | Separate comparison/control relations | Constructor and identity addressability |
| 7 | False-trace interface | Design and constructor addressability |
| 8 | Relocation without semantic labels | Addressability plus forbidden-label exclusion |
| 9 | Complete continuation state | Composite identity and fail-closed restoration conformance |
| 10 | Active history | Explicitly not claimed; audit history remains noncausal |
| 11 | Fresh/direct-address boundaries | Representable identity and access boundary only |
| 12 | Distinct distance/causal surfaces | Public-interface callability and separate identities |
| 13 | Native/RCAE ownership | Dataflow and forbidden-read conformance |
| 14 | No silent native substitution | Source, provider, and realization binding |
| 15 | Constructed-mechanism minimality | Accepted design argument plus narrow-producer conformance |

Formation withdrawal and no-field are constructible interfaces, not passed
scientific controls. Fresh/direct address is a representable boundary, not
second-participant evidence. OP-13 remains interpretation-only.

## 5. Exact retained identities

The reviewer did not receive the generated receipt/result bytes. They were
therefore checked directly in the repository before gate passage.

| Identity | Exact value |
| --- | --- |
| RCAE implementation commit | `ce9701c436f9ed39fa2db5323c5f4bac8c55d931` |
| PyGRC revision | `565706f8b7647f6b7638b9afbe52372e170bf724` |
| PyGRC import origin | `src/pygrc/__init__.py` in the admitted graph checkout |
| Input-freeze exact-file SHA-256 | `0a255d21605c2a1cbf00a3467562fc08dd73a32505d4d435b6eb6f140f16a243` |
| Runtime-module exact-file SHA-256 | `e8496bf5af9c8fc297f569c127c7193e238f562063e10a71a94cae2c87b5d7f7` |
| Harness exact-file SHA-256 | `63ff0086bda4e92aec375153a37293e313845005839edea1e2b07efaeadb306e` |
| Quarantine-guard exact-file SHA-256 | `deeb969d5d5a0b29b0d4c95441a5769be8b4d9002fede8e889a96b3b92deaff7` |
| Binding-receipt exact-file SHA-256 | `9f26ccecde072420c53ff1b46aa00693ea63f302c726deb03be62e02c3cf0b69` |
| Binding-receipt canonical digest | `abdbcd1078511284e6e64d1646593ffaa4bdca8cd80fcca8011183134a7ede7e` |
| Conformance-output exact-file SHA-256 | `2baf7ba5782bcab686123ac004dafbbe6f993cd29ebfb9da53e9da5126de5e4c` |
| Conformance-output canonical digest | `4696e9d6c054c22f9770e9790eb991a255c7454cbcc465ed207aa0ab673fddee` |
| Reconstructed-output exact-file SHA-256 | `2baf7ba5782bcab686123ac004dafbbe6f993cd29ebfb9da53e9da5126de5e4c` |
| Attempt policy | one attempt, zero retries, parallelism one |
| Conformance totals | 11/11 cells; 36/36 checks; 109 required public-call invocations; zero blocked calls |

The retained output and independent reconstruction are both 48,395 bytes and
byte-identical. Both retained artifacts' canonical-payload digests validate.
The RCAE and graph worktrees were clean before the retained invocation, and the
graph checkout remains unmodified.

## 6. Downstream reuse and gate effect

Only this conclusion may be reused downstream:

> The accepted I03 B-R conformance gate passed.

The fixture's `0.1`, `0.45`, `0.4`, and `0.5` values, topology, observed split,
output digest, and any derived margin are prohibited as I04 calibration inputs
and I06 registration values. Conformance provenance remains mechanically
ineligible for calibration, candidate, control-outcome, scientific-result, or
terminal-result records.

```text
P2-I3 B-R realization:       accepted as operationally expressible
P2-I3-DISCRIMINATOR-GATE:    passed
I04 calibration prereg:     opened
calibration execution:       unauthorized
I06 registration:           unauthorized
candidate/control execution: unauthorized
B-R scientific result:      unassigned
AE01-H-L03 and R01-R05:      unassigned
C.2 work:                    unauthorized by this gate
```

No rerun is required. Reopen I03 only if an exact identity fails
reconstruction; an RCAE producer requires a forbidden read or authors the
native response; composite restoration ceases to be complete and fail-closed;
the source/provider identity changes; quarantine admits conformance provenance
downstream; or later evidence demonstrates that one of the operational
interfaces cannot support its registered scientific role.
