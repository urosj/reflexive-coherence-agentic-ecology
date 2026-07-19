# P2-I3 I04 B-R Calibration Preregistration

**Status:** accepted by the project owner on 2026-07-19;
`P2-I3-CAL-PRE-GATE` passed

**Iteration:** `P2-I3-I04`

**Lane/branch:** `AE01-L03` / `P2-I3-BR`

**Source authority anchor:** `4c5b49153cf42ea4893f4bf42538bce79138a7b4`

**Evidence effect:** candidate-blind measurement, calibration, and control-
governance integrity only

## 1. Outcome

DEC-036 through DEC-040 are materialized as one coherent machine package.
The corrected package passes 22 focused pure tests and 485 zero-calibration validation
checks. Its retained validation artifact reconstructs byte-for-byte with
SHA-256:

```text
153d187c988f8802c674977f07d872c28798cdda78d5296321c55c8eb74a1862
```

This is readiness evidence, not calibration or ecology evidence. No matched-
null population was invoked, no `delta` was generated, and no PyGRC model,
candidate, control, B-R runtime, C.2 path, rung, tag, or terminal class was
executed or assigned.

## 2. Retained package

| Artifact | Role |
| --- | --- |
| `configs/p2_i3_br_i04_machine_policy.json` | Complete response, observation, W/O/E estimator, arithmetic-panel, control, and I09-I11 policy |
| `contracts/p2-i3/i04-br-machine-records.schema.json` | Closed root union plus response, pair, triplet, control-leg, terminal-overlay, and component shapes |
| `scripts/p2_i3_i04_br_analysis.py` | Pure typed response and W/O/E estimator path; no PyGRC import or calibration builder |
| `scripts/p2_i3_i04_br_validate.py` | Authority, policy, schema, applicability, provenance, and reconstruction validator |
| `implementation/tests/test_p2_i3_i04_br.py` | Twenty-two pure tests over sign, pairing, estimator, missingness, root/conditional schema closure, control lifecycle, safe reconstruction, and terminal overlay |
| `contracts/p2-i3/i04-br-calibration-preregistration.json` | Review-ready package identity and exact future boundary |
| `contracts/p2-i3/i04-br-calibration-preregistration-validation.json` | 485-check retained readiness validation |

The preregistration file has SHA-256
`d6ffb7fc1604b529ba23cf2574bb17128019749f405df878b32b22819bfb40fc`.

Corrected machine identities are:

| Machine file | SHA-256 |
| --- | --- |
| policy | `9877154766ab9ea26a11c426a8feb8666df1a3f146efb188006a5e0f26a77bf1` |
| schema | `2e8f3cc72e588b45a641a04a16bf0287f703ee4d91880af6102692553d968e72` |
| analysis | `e8292c7fbe0f3cb8521e15de354dd8a0a36b9ade80c38b2c8b733858e197bb46` |
| validator | `637978b743a6935b0c7ae748866b5e6466bc3e66996450b9ff48ebebd1766b82` |
| focused tests | `0dc5761f0dd87b130f4cee194f61d84039310d5e1d688a83950020964e968e82` |

## 3. DEC-036 response realization

The machine response is:

```text
mu[e,j] = C_pre(m_e) - q_probe
```

It is not a free scalar. Every valid response retains:

- exact unrounded carrier and request inputs;
- native coherence units;
- encounter index `j`;
- the complete pre-next-event observation boundary;
- native `admitted` or exact `field_limited_refusal` disposition; and
- the full pairing projection.

`mu >= 0` must agree with native admission and `mu < 0` with the exact field-
limited refusal. A structurally invalid or infrastructure-failed encounter
has a null primary margin. A sign/disposition mismatch is invalid evidence,
not a scientific value.

The schema and analysis module share the same typed record. Candidate-blind
arithmetic records add exact rational source fields and explicit negative
declarations for candidate artifacts, PyGRC inputs, and execution.

## 4. DEC-037 observation realization

The five surfaces remain epistemically separate:

| Surface | Machine role |
| --- | --- |
| Native topology/state | Measured native structure and state |
| RCAE role bindings | Integrity-checked registered metadata |
| Geometric distance | Derived annotation only |
| Functional distance | Derived annotation only |
| Native event/internal time | Measured native time |
| Causal shortest path | Derived annotation only |
| Experimental causal influence | Estimated from measured intervention arms; never a direct-observation claim |

A later geometry or internal-timescale variation may be a real registered
factor. No distance annotation can substitute for its measured consequence.

## 5. DEC-038 estimator realization

The exact three arms remain:

```text
W = deposition withdrawn
O = lifecycle retained but designated B-R export neutralized
E = B-R export lifecycle enabled
```

The pure analysis path computes:

```text
m_trace  = N(E,W;epsilon_mu)
m_export = N(O,E;epsilon_mu)

N(a,b;epsilon_mu) =
  (mu_a - mu_b) / max(abs(mu_a), abs(mu_b), epsilon_mu)
```

`m_trace` is the primary complete-trace relation and `m_export` the mandatory
B-R mediation relation. Only raw deltas retain the additive identity.
Normalized relations are neither additive nor percentages and are not clipped.

An invalid W affects the trace pair without invalidating the independent O/E
pair. An invalid E affects both. No surviving-arm substitution, averaging,
or imputation exists. Pairing binds all eleven accepted dimensions, including
clean parent, causal continuation projection, request, schedule, and
observation identity.

## 6. DEC-039 calibration realization

The policy freezes one denominator floor and two distinct roles:

```text
epsilon_mu = 1e-12
delta_N    = future metric-sheet delta field
```

Five exact-equality W/O/E cases are the only future inputs to the Phase 1
delta rule. Seeds `19`, `43`, `71`, `109`, and `163` are inert case aliases;
randomness is false. Candidate seeds `101`, `211`, and `307` are disjoint and
excluded.

Eight deliberately nonzero cases cover trace/export orientation, first/second
arm denominators, floor dominance/equality, cross-zero magnitude `2`, and a
non-dyadic round trip. The focused test suite exercised these as pure estimator
conformance. They are mechanically excluded from `delta` and have no runtime
or scientific effect.

The five exact-null cases were statically validated for complete W/O/E
equality, exact rational form, seed identity, and exclusivity. They were not
iterated through a calibration builder, no calibration artifact was produced,
and the expected `1e-12` remains a preregistered consequence rather than a
retained calibration result.

## 7. DEC-040 control realization

The policy contains:

- all 19 common parent controls and all five L03 parent controls;
- 29 common and 13 lane-specific independently resolvable legs;
- partial applicability only for `AE01-CTRL-10`;
- four producer/handoff legs under `CTRL-08`;
- five cost/conservation/leakage/isolation/specificity legs under `CTRL-09`;
- two false-trace strengths;
- five independently resolvable L03 dynamic-family legs;
- fourteen stable scientific, validity, and claim requirements; and
- three preserved producer-cost classes.

Every one of the 42 legs now has a keyed machine policy fixing its target
relation IDs, owning iteration, allowed evidence resolutions, claim effect,
invalidity effect, unavailability effect, and terminal-guard role. These are
I04 meanings rather than I06 operations or outcomes. In particular:

- conservation or unregistered leakage invalidates the affected execution;
- formation-cost failure blocks R01 and higher while preserving weaker
  observations;
- producer omission classifies constructed dependence without automatically
  invalidating the observation;
- reservoir dependence blocks isolated-carrier mediation but remains an
  interpretable dependence;
- `generic_effect` under export-mass matching blocks organization-specific
  interpretation without invalidating the comparison; and
- terminal-language failures reject only the I11 overlay and cannot alter I09
  scientific facts.

Control-leg schema fields keep applicability, execution, evidence resolution,
control resolution, and terminal-guard status separate. A valid generic or
counterdirectional result may resolve a diagnostic control. Invalid execution
cannot receive a scientific resolution.

The false-trace contract keeps carrier matching below causal-projection
matching. Carrier reproduction supports only carrier-value sufficiency;
carrier divergence leaves omitted state versus history unresolved. Only a
verified causal-projection match may bear on complete-current-state
sufficiency, and no false installation establishes costly formation.

`not_supported` requires valid completion of every claim-mandatory scientific
leg. Blocked, incomplete, and missing-surface closeouts may retain explicitly
unavailable scientific legs without turning absence into support or
refutation. I09 resolves scientific/pre-terminal facts, I10 reconstructs
them, and I11 may add only a terminal guard overlay that leaves I09 facts
unchanged.

## 8. Implementation corrections retained

The initial focused run produced 12 passes and four schema-test errors because
the test helper extracted a `$defs` fragment without preserving the root
reference context. No policy or analysis assertion failed. The helper was
corrected to validate through a root wrapper containing the complete `$defs`
registry. The replacement run passed 16 tests; adding complete coverage of all
eight non-delta estimator-conformance cases brought the pre-review result to
17/17.

This was a test-harness correction only. No calibration case, estimator
formula, response meaning, control applicability, or authority changed.

The final checklist projection then exposed an authority-verification cycle:
the policy correctly bound the accepted checklist bytes at source anchor
`4c5b491`, but the validator compared that digest with the necessarily updated
working-tree checklist. The validator now reads every authority artifact from
the exact source-anchor Git object and continues to verify newly materialized
machine files from the current package. This preserves both immutable decision
authority and an evolvable checklist; it changes no scientific or calibration
meaning.

The bounded I04 review then found three real machine-contract gaps. Version
`1.0.1` closes them without reopening DEC-036 through DEC-040:

1. the schema root is now a closed union of the five top-level record classes;
   pair evaluability, response validity/source class, unique arm IDs, and the
   raw additive identity are conditionally closed;
2. all 42 control legs now retain their own outcome and fail-closed policy;
   and
3. reconstruction writes only to a separate repository-relative scratch path,
   followed by explicit `cmp`. The validator refuses the retained path unless
   explicit artifact-construction mode is selected.

The closure tests also exposed that the estimator validated rational/value
equality but subtracted the float projections. The shared path now derives
raw numerators, denominators, normalized margins, and the additive identity
from exact rational fields before projecting final numeric values. All eight
non-delta cases assert that exact path.

Five focused tests cover those corrections, bringing the final suite to
22/22. The future I05 boundary also requires one exact candidate-blind
`c_pre_m_e`/`q_probe` construction with nonnegative carrier coherence, matched
request semantics, and a mechanical prohibition on I06/I08 scientific reuse.
No values or construction are selected in I04.

## 9. Reproduction

From the repository root, use only the repository-local environment:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  .venv/bin/python -m pytest -q \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests/test_p2_i3_i04_br.py

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  .venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i04_br_validate.py \
  --output outputs/reconstruction/p2-i3-i04-validation.reconstructed.json

cmp \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i04-br-calibration-preregistration-validation.json \
  outputs/reconstruction/p2-i3-i04-validation.reconstructed.json
```

Expected results:

```text
22 passed
485 validation checks
byte-exact validation reconstruction
validation SHA-256:
153d187c988f8802c674977f07d872c28798cdda78d5296321c55c8eb74a1862
```

No external repository write, network access, PyGRC import, or global Python
interpreter is required.

## 10. Review boundary

The bounded review should determine whether:

1. DEC-036 through DEC-040 are represented without semantic loss;
2. the pure response/estimator path is suitable for later I05 and live I08
   reuse;
3. the exact-null versus non-delta-conformance separation is mechanical;
4. root and conditional schema closure reject contradictory machine records;
5. all 42 controls have sufficient target/outcome/ownership/fail-closed
   semantics for later I06 exact binding;
6. reconstruction cannot overwrite retained evidence;
7. the I05 construction obligation is exact while its values remain deferred;
   and
8. candidate blindness and all gate boundaries remain explicit.

The project owner accepted the corrected `1.0.1` package on 2026-07-19 and
passed `P2-I3-CAL-PRE-GATE`. This opens only construction of a separate
inactive I05 calibration invocation freeze. Acceptance did not invoke
calibration or authorize registration, candidate/control execution, C.2, or
a scientific result.
