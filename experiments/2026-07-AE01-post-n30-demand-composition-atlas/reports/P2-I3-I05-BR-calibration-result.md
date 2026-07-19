# P2-I3 I05 B-R Calibration Result

**Status:** owner-accepted; `P2-I3-CAL-GATE` passed

**Iteration:** `P2-I3-I05`

**Lane/branch:** `AE01-L03` / `P2-I3-BR`

**Launch HEAD:** `7a58471a7ba680e67e11cb35037cb7a3fac9f3f2`

**Evidence effect:** numeric measurement resolution only

## 1. Outcome

The sole authorized candidate-blind calibration attempt completed
successfully. One builder invocation evaluated five exact-null W/O/E cases,
producing 15 typed response records, five triplets, and ten entered margins
across `m_trace` and `m_export`.

All ten exact matched-null margins were zero. The resulting shared resolution
is therefore the preregistered arithmetic floor:

```text
maximum absolute matched-null margin = 0
measurement resolution               = 1/1000000000000
delta                                = 1/1000000000000
```

This is a narrow numeric-resolution result, not support for a trace, trail,
field, niche, or other ecological claim. It shows that the exact registered
arithmetic introduces no detectable matched-null offset above the frozen
floor. It does not establish empirical robustness at that scale, and later
near-threshold candidate margins still require structural and developmental
interpretation.

No candidate artifact, candidate seed, PyGRC runtime input, or candidate-
shaped value entered calibration.

## 2. One-shot execution

The committed launch authorization bound accepted freeze commit
`d054c4df8491ea8f5cc3b13dcb10b222cf8973d5`, exact source digests, the pinned
repository `.venv`, deterministic process environment, normalized command,
and all governed paths. Exact preclaim validation passed from a clean worktree
without consuming the attempt.

The governed command was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  .venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_one_shot.py \
  --policy experiments/2026-07-AE01-post-n30-demand-composition-atlas/configs/p2_i3_br_i05_one_shot_policy.json \
  --activation experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-launch-authorization.json \
  --expected-head 7a58471a7ba680e67e11cb35037cb7a3fac9f3f2
```

The permanent claim was created before builder import. Post-claim source,
environment, activation, worktree, and output-absence validation passed. The
final receipt records one builder invocation, zero retries, successful schema
and semantic validation, exact canonical readback, and an actual refused
second start with unchanged claim bytes.

## 3. Retained artifacts

| Artifact | Role | SHA-256 |
| --- | --- | --- |
| `outputs/p2-i3/i05/br-attempt-claim.json` | Permanent attempt consumption and exact launch/source binding | `5b0208f3b54953d801297f191f7cb5712ddaf223e5910cb313abb0c35f76da90` |
| `outputs/p2-i3/i05/br-final-receipt.json` | Successful closeout, counts, output bindings, validation, and second-start refusal | `8b979000286f467537c06f80531003ae719d07c3b27f81a3fa9f427562ad2a44` |
| `outputs/p2-i3/i05/br-matched-null.json` | Five exact-null cases and 15 typed responses | `fa8de40ecba373fe7b3969a0cb76f8b6745de2a1d482fee18d80f7a934e25b79` |
| `outputs/p2-i3/i05/br-metric-calibration.json` | Ten-margin ledger and exact `delta` derivation | `b5715991b6ade786d28863b52e4021d304de4407655be157f7e27d7685ef80b9` |
| `outputs/p2-i3/i05/br-frozen-metric-sheet.json` | Shared `m_trace`/`m_export` numeric-resolution authority | `206de69c252e9cfbd82eeae4ef7ebe255f77b72e7b15ac44de6e9afa8a8d9319` |
| `outputs/p2-i3/i05/br-result-validation.json` | Independent 49-check readback and reconstruction record | `725f5bcea59288c9e5872f8598e16105918f9f500c2ce1371125304c8d24bfee` |

The claim is permanent. None of these files may be deleted and the governed
calibration may not be rerun.

## 4. Independent reconstruction

The read-only validator imports the accepted semantic validation function but
never imports or calls `build_calibration_outputs`. It schema-validates the
activation, claim, receipt, and three scientific outputs; resolves every
receipt digest; repeats cross-record semantic and closeout validation; then
parses and canonically reserializes only the retained outputs.

```text
validator = experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_result_validate.py
SHA-256  = 7dbb72b421949065b41a246357145a42552f367be46313209f1d7299dc28c320
```

Reproduce into absent non-retained paths with:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  .venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_result_validate.py \
  --reconstruction-dir outputs/reconstruction/p2-i3-i05-results-rerun \
  --output experiments/2026-07-AE01-post-n30-demand-composition-atlas/outputs/reconstruction/p2-i3-i05-result-validation.reconstructed.json
```

Both reconstruction destinations must be absent before the command. The three
reconstructed bytes and SHA-256 digests must equal the retained matched-null,
metric-calibration, and frozen-metric-sheet artifacts. The completed run passed
49/49 checks and all three comparisons byte-exactly.

## 5. Claim boundary

The result authorizes no ecological interpretation. It establishes only the
numeric resolution to be consumed by future exact registration:

```text
delta(m_trace)  = 1e-12
delta(m_export) = 1e-12
scope           = shared arithmetic resolution
```

I06 exact registration is opened by owner acceptance. Still closed:

- B-R candidate and control execution;
- C.2 design or execution;
- R01-R05 assignment;
- trail, stigmergic-field, or ecology classification; and
- any native LGRC promotion claim.

## 6. Owner acceptance and gate effect

The owner accepted the final I05 calibration result on 2026-07-19. The
[acceptance record](../contracts/p2-i3/i05-br-owner-acceptance-and-cal-gate.json)
binds the launch HEAD, permanent activation and claim, successful receipt,
three governed outputs, independent result validation, exact shared `delta`,
and the interpretation ceiling.

Acceptance-record SHA-256:
`16c820aaa2bba3ed2fa34604437f0c2202e194aa0db6c507a712dc30a09cdac0`.
The owner separately authorized retention of the complete accepted package.

```text
P2-I3-I05 = accepted and complete
P2-I3-CAL-GATE = passed
opened = P2-I3-I06 exact implementation registration
```

This progression opens registration construction only. Candidate/control
execution, C.2, R01-R05 assignment, trail or stigmergic-field classification,
and every ecology or native-mechanism claim remain closed.
