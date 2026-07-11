# P2-I1 CAL Independent Review

**Status:** passed

**Gate under review:** `P2-I1-CAL-GATE`

**Frozen source revision:**
`ae955a3ddc651d2f89c0a1e288bfbe72be22f60e`

**Evidence effect:** resolution only; no candidate evidence

## 1. Review target

The review determines whether the P2-I1 matched-null lineage is genuinely
candidate-blind and reconstructable, whether the retained calibration and
metric sheet freeze exactly the preregistered numeric resolution, and whether
the result remains outside every L01 support or refutation claim.

Controlling records:

- [CAL-PRE identity](../contracts/p2-i1/cal-pre-identity.json)
- [CAL-PRE freeze](../contracts/p2-i1/cal-pre-freeze.json)
- [CAL-GATE freeze](../contracts/p2-i1/calibration-freeze.json)
- [matched null](../contracts/p2-i1/matched-null.json)
- [metric calibration](../contracts/p2-i1/metric-calibration.json)
- [frozen L01 metric sheet](../contracts/p2-i1/frozen-metric-sheet.json)
- [P2-I1 checklist](../implementation/P2-I1-minimal-shared-medium-niche-checklist.md)

The retained artifact root is
`experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i1/`.

## 2. Required review questions

1. Does the generator lineage resolve only to the frozen calibration and
   analysis policies, without candidate artifacts, candidate seeds, PyGRC
   runtime input, or post-outcome tuning?
2. Do the five panels cover formation fractions `0`, `0.25`, `0.5`, `0.75`,
   and `1` through the same aggregation and paired-margin functions used by
   later analysis?
3. Are both sides identical in every panel, with five retained margins of
   `0.0`, and is `delta=1e-12` exactly the maximum of the declared measurement
   resolution and absolute matched-null margins?
4. Are the `metric_calibration` and frozen `metric_sheet` schema-valid, and
   does the sheet reference the retained calibration record exactly?
5. Does independent clean-source reconstruction reproduce exact bytes and
   semantic digests for all three retained artifacts?
6. Are candidate execution, selectivity evaluation, registration, lane
   support/refutation, and native-niche claims still closed?

## 3. Reproduction

From a clean checkout of the frozen source revision, create a local Python
environment satisfying Python `>=3.11` and `jsonschema==4.26.0`. PyGRC is not
installed or consumed for this calibration.

The test result is explicitly environment-bound: running the suite from a
shell without the pinned `jsonschema==4.26.0` dependency is expected to produce
dependency errors and is not a reconstruction of the frozen profile.

Run:

```text
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py validate-phase1
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py validate-configs
.venv/bin/python -m unittest discover -s experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests -q
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py generate-matched-null --output outputs/p2-i1-matched-null.json
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py freeze-resolution --metric-sheet experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/metric-sheets/AE01-L01.json --calibration-input outputs/p2-i1-matched-null.json --calibration-output outputs/p2-i1-metric-calibration.json --frozen-sheet-output outputs/p2-i1-frozen-metric-sheet.json
```

Compare the three outputs with their retained counterparts and verify the
semantic and exact-file digests in `calibration-freeze.json`.

## 4. Reconstruction findings available to the reviewer

A detached clean-worktree reconstruction with a fresh environment and no
PyGRC installation produced:

```text
validate-phase1 = passed
validate-configs = passed
unit tests = 57 passed
matched null exact comparison = identical
metric calibration exact comparison = identical
frozen metric sheet exact comparison = identical
```

The reconstructed digests were:

| Artifact | Embedded canonical payload digest | Semantic-file digest | Exact-file SHA-256 |
| --- | --- | --- | --- |
| Matched null | `6b95026850da740fa1bcf286200a6ccda0363beae8613e0ab8bcb52d72f1873a` | `a9cbe5e7449091c3c6f6a395a9c8db5f8e3d05890b985975c97550e1572b9629` | `2188529b520466aabee5baa86750f1376ae5172d2be07b11192747f9e8c1cc2f` |
| Metric calibration | Not embedded; schema record uses `calibration_id` | `8c734e4e43131842917e423170584cf53b8c657ed3302544d5805a29f645cde9` | `ebd6c62c8a5920c681b8e91810a4788e7dcd5591e98d0313a7225f0e63635e5a` |
| Frozen metric sheet | Not embedded; schema record uses `metric_sheet_id` | `68ed80f6455ec2e4ab8dc18d3a385d8d6bc9781483c90dbf1b1a9b3c5c80f043` | `fdd2a0d78140edbe6383661804c2928f5a1ae63ef501e1aed6ca296994514563` |

The matched-null embedded canonical payload digest was explicitly verified.
The calibration and metric-sheet records correctly rely on their schema IDs
plus retained semantic and exact-file digests rather than adding an
out-of-schema canonical digest field.

## 5. Result interpretation

The null panels agree exactly across the complete five-point formation-fraction
domain, so the matched-null contribution to the resolution band is zero. The
frozen `delta=1e-12` therefore records only the declared numeric floor.

This does not mean that any later positive margin is scientifically strong or
that a margin at the floor is automatically uninteresting. `delta` describes
numeric resolution and supports the threshold-relation ladder; later
interpretation must still preserve raw formation coverage, seed distribution,
threshold proximity, medium dependency, selectivity, causal controls, and
possible alternative realizations.

## 6. Allowed dispositions

```text
pass
revise_before_registration
blocked_missing_review_evidence
```

A pass opens registration work only. It does not authorize candidate
execution, assign an L01 rung, or support/refute a niche-conditioning claim.

## 7. Disposition

Review completed 2026-07-11. The retained panels, seed separation, frozen
estimator, dependency profile, reconstruction chain, and claim boundaries were
verified. No implementation defect was found.

```text
P2-I1-CAL-GATE = passed
```

This opens `P2-I1-REG-GATE` work only. Candidate execution, L01 rung
assignment, selectivity evaluation, and niche-conditioning claims remain
closed.
