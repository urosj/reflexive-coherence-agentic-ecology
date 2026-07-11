# P2-I1 CAL-PRE Independent Review

**Status:** passed

**Gate under review:** `P2-I1-CAL-PRE-GATE`

**Frozen source revision:** `134b66cf6adf50e9f1e773454be25bbea53938d2`

**Evidence effect:** none; this review does not itself create or admit
calibration or candidate evidence. A pass authorizes candidate-blind
calibration work only.

## 1. Review target

The review determines whether the P2-I1 measurement, opportunity, comparison,
selectivity, calibration-null, identity, and provenance surfaces were frozen
before candidate outcomes and are sufficient to authorize candidate-blind
calibration.

Controlling retained records:

- [CAL-PRE identity](../contracts/p2-i1/cal-pre-identity.json)
- [CAL-PRE freeze](../contracts/p2-i1/cal-pre-freeze.json)
- [P2-I1 checklist](../implementation/P2-I1-minimal-shared-medium-niche-checklist.md)
- [P2-I1 decision record](../implementation/P2-I1-decision-record.md)
- [calibration provenance](../configs/p2_i1_cal_pre_provenance.json)

The matched null generated during implementation was a deterministic
verification output only. This review does not admit it as calibration
evidence, create a `metric_calibration` record, or freeze the metric sheet.

## 2. Required review questions

1. Does the retained identity resolve to the clean frozen source revision and
   match its declared source, configuration, projection, and profile digests?
2. Are formation, fixed-denominator aggregation, primary comparison,
   medium-dependency comparison, selectivity, missingness, and threshold
   proximity complete and mutually consistent?
3. Does the calibration generator remain candidate-blind, non-runtime, and
   free of candidate seeds, candidate artifacts, PyGRC inputs, and
   post-outcome tuning?
4. Are commands, dependencies, resources, expected artifacts, and
   reconstruction instructions portable and sufficiently bounded?
5. Are static versus resolved profile identity, cross-cell matching, and
   cross-branch isolation correctly divided between CAL-PRE contracts and
   later registration/execution evidence?
6. Do all records preserve the claim ceiling and keep candidate execution,
   calibration evidence, positive lane evidence, and native-niche claims
   closed?

## 3. Reproduction

In a clean checkout of the frozen source revision, create the documented local
environment and run the command profiles in
`configs/p2_i1_cal_pre_provenance.json`. Generate the identity into ignored
`outputs/`, then compare its canonical content with the retained identity and
the file/semantic digests in `cal-pre-freeze.json`.

Expected implementation checks:

```text
validate-phase1 = pass
validate-configs = pass
unit tests = pass
identity source_tree_clean = true
identity retention_eligible = true
candidate_execution_authorized = false
candidate_outcomes_absent = true
```

## 4. Allowed dispositions

```text
pass
revise_before_calibration
blocked_missing_review_evidence
```

A `pass` opens only `P2-I1-CAL-GATE` work. It does not authorize candidate
execution, pass registration, assign an L01 rung, or open an ecology claim.

## 5. Review findings

Review date: 2026-07-11.

The final review confirmed that:

- source revision `134b66cf6adf50e9f1e773454be25bbea53938d2`
  exists and is the clean source anchor;
- the identity and freeze records are materialized through the intentional
  source-anchor/retention two-commit structure;
- the six configuration surfaces, 25 P2-I1 tests, 32 Phase 1 tests, and frozen
  `unittest discover` command are correctly represented;
- `DEC-019` comparison roles match the frozen analysis policy;
- post-anchor changes are limited to freeze, checklist, and review artifacts;
  no script, config, or test source drifted; and
- candidate execution, calibration evidence, positive lane evidence, and
  native-niche claims remain closed.

## 6. Independent reconstruction

A separate clean worktree at the frozen source revision was given a fresh
local environment with `jsonschema==4.26.0`. The frozen commands produced:

```text
validate-phase1 = passed
validate-configs = passed
unit tests = 57 passed
identity source_tree_clean = true
identity retention_eligible = true
working_tree_change_count = 0
```

The reconstructed identity was byte-for-byte identical to the retained
identity. All three digest layers matched:

```text
canonical_payload_digest = ababf1196b664e174cf182238432a6a4fbaf6a4d925c7780dc48dc1956f1655e
semantic_file_digest = 1eece72127dbac9d4d6999962baf4776f01e3f1f4ce1f38bd654032461ec86fc
file_sha256 = 7f87b018b397d515329d6b559d268ae54e3d6cef6b5a3cf27aaf77214ca4ffaf
```

## 7. Disposition

```text
P2-I1-CAL-PRE-GATE = passed
```

The retained CAL-PRE identity correctly anchors the reviewed implementation,
its declared digests and candidate-absence boundaries are consistent, and
runtime-dependent evidence remains deferred. This authorizes
candidate-blind calibration only. It does not authorize candidate execution,
pass registration, assign an L01 rung, or open an ecology claim.
