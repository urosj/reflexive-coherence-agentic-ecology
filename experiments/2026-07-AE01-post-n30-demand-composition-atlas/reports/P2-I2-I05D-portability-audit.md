# P2-I2 I05D persisted-path portability audit

## Disposition

`P2-I2-I05D-PORTABILITY-AUDIT-REVIEW-READY` is satisfied as an audit-only
disposition under DEC-032/CHG-025. The audit inspects 135 current-tree P2-I2
files and retains 312 value-redacted violations in 70 files. No affected
artifact has been corrected. I05E, the metric freeze, CAL-GATE, I06, and every
runtime or scientific path remain closed pending owner review.

## Authority and in-iteration selector correction

The checklist and operational hypothesis froze I05D before scanner
construction. During construction, the first discovery pass showed that two
recursive selectors selected directories rather than nested files. Their form
was corrected and explicit nested-file coverage guards were added inside I05D
before the retained inventory was created. This did not create a separate
iteration and changed no classification, redaction, correction-group,
historical, runtime, scientific, or gate rule. The discovery scratch inventory
is not retained.

## Corrected inventory

| Correction group | Violations | Affected files | Order |
| --- | ---: | ---: | ---: |
| I05 active execution and closeout | 32 | 11 | 1 |
| I04/I05 authority dependencies | 30 | 13 | 2 |
| I03 realization and conformance | 201 | 30 | 3 |
| I01/I02 source and identity | 35 | 10 | 4 |
| P2-I2 governance, navigation, and shared projections | 14 | 6 | 5 |
| **Total** | **312** | **70** | — |

The violation classes are:

- 199 filesystem-rooted persisted values;
- 113 machine-local absolute tokens embedded in commands, reports, tests, or
  source literals.

The I05-first correction group contains these eleven repository-relative
files:

- `contracts/p2-i2/i05c-preclaim-interpreter-path-failure.json`
- `contracts/p2-i2/i05c-zero-null-interpreter-validation.json`
- `implementation/tests/test_p2_i2_i05b_one_shot.py`
- `outputs/p2-i2/i05/complete-three-arm-analysis-arithmetic-calibration.json`
- `outputs/p2-i2/i05/i05b-attempt-claim.json`
- `reports/P2-I2-I05C-preclaim-venv-correction.md`
- `scripts/p2_i2_i05_authorization_validate.py`
- `scripts/p2_i2_i05a_safety_audit.py`
- `scripts/p2_i2_i05b_one_shot.py`
- `scripts/p2_i2_i05b_validate.py`
- `scripts/p2_i2_i05c_validate.py`

The machine inventory retains the complete 70-file list and every field/line
locator. It never stores a forbidden value: each finding retains only its
repository-relative file identity, locator, violation class, file digest, and
forbidden-value digest/length.

## Execution boundary

The audit used the repository `.venv`. Across its construction discovery,
corrected discovery, and final retained passes:

```text
static scan invocations:                 3
affected-artifact corrections:           0
null builder or one-shot invocations:    0
PyGRC model instantiations:               0
candidate/control invocations:            0
conformance/scientific invocations:       0
calibration or response generation:       0
```

The final scan performs six mechanical checks: frozen policy/scanner identity,
complete deterministic scope, value redaction, frozen group order,
zero-runtime/source-call boundary, and path-free generated report. It also
refuses to write an inventory containing a path violation. The known nested
I05 output and attempt artifacts are explicit coverage guards.

## Historical and correction boundary

Git history is not rewritten. Historical governed-attempt/output/final bytes
may be referenced only by commit and SHA-256. Future portable derivatives must
identify themselves as projections and cannot impersonate raw receipts. The
permanent consumed-attempt fact, one attempt, zero retries, accepted I04R2
estimator, three-arm values, ten margins, arithmetic delta, and all candidate/
runtime exclusions remain immutable. The null cannot run again.

Owner acceptance of this audit may open only the separately frozen first I05E
correction group. Every correction group remains uncommitted until its own
review and explicit commit authorization.
