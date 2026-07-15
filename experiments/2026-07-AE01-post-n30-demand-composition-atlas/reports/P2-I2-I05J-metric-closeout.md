# P2-I2-I05J arithmetic-resolution and metric-sheet closeout

Date: 2026-07-14

Status: `P2-I2-I05J-METRIC-CLOSEOUT-REVIEW-READY`

## Scope reconciliation

I05C/10.4A is already complete. It corrected the pre-claim venv interpreter
guard, retained the sole governed attempt for later use, and was committed at
`9d81f15`. The remaining work consists of the three deferred 10.4 obligations:
freeze `analysis_arithmetic_delta`, retain the lane-local metric-calibration and
frozen metric-sheet records, and preserve narrow/robust language as a relation
to the frozen resolution.

I05J enters from owner-accepted I05I commit `b5d0acb`. It does not rerun the
consumed arithmetic null or alter any I04/I05 execution evidence.

## Input projection and native generation

The first frozen native entry-point start failed closed before either output
was created because the repository `.venv` lacked the common tooling contract's
pinned `jsonschema==4.26.0` dependency. I05JA preserves that failure and the
original I05J freeze, installs and verifies only that dependency, and admits one
unchanged retry. The retained accounting is therefore two native starts: one
failed closed before output and one successful generation.

The accepted I04R2 arithmetic null retains ten margins: five calibration seeds
by two physical orders. The common native `freeze-resolution` interface accepts
one matched-null margin for each unique calibration seed. I05J therefore uses a
bounded input projection that takes the maximum absolute margin across both
required orders for each seed.

All ten source margins are zero, so every projected seed envelope is zero. More
generally, the maximum over the five projected envelopes is identically the
maximum over all ten source margins. The projection therefore preserves the
registered estimator without treating either order as optional and without
replacing the authoritative order-stratified provenance.

The native interface generates:

- `contracts/p2-i2/metric-calibration.json`; and
- `contracts/p2-i2/frozen-metric-sheet.json`.

The base `contracts/metric-sheets/AE01-L02.json` remains unchanged. Only the
designated resolution status and delta fields differ in the frozen projection.

## Resolution and interpretation

The maximum absolute matched-null margin is `0.0`; the registered arithmetic
floor and base measurement resolution are both `1e-12`. The frozen
`analysis_arithmetic_delta` is therefore `1e-12`.

This is analysis/serialization resolution only.
It is not a runtime or measurement tolerance and supplies no restoration,
continuation, candidate, control, mode-selection, support, or falsification
evidence.

Narrow and robust are future relations to the frozen resolution, not
calibration outcomes. The metric closeout is not a terminal scientific verdict.

## Validation and gate boundary

Static validation reconstructs the ten-row input projection, both native
outputs, schema validity, exact bytes, estimator equality, and the five allowed
metric-sheet resolution-path changes. One failed-closed native start and one
successful native generation are retained. No null builder/wrapper, PyGRC,
candidate/control, conformance, runtime, or scientific operation occurs.

## Closure amendment and process accounting

A later read-only closure audit found no metric or scientific defect. It did
find that the generated validation did not itself retain the complete process
history and that current navigation lagged behind I05J. Because I05J remained
uncommitted and unaccepted, the project owner directed an in-iteration
amendment rather than another I05 iteration.

The additive closeout records the actual preparation and execution history:

- two dependency-install process starts: one sandbox-blocked package-index
  attempt that changed no environment, followed by one successful installation
  and verification of `jsonschema==4.26.0`;
- two native entry-point starts: the retained missing-dependency failure before
  output, followed by one unchanged successful retry;
- two validator starts: one failed closed before output because a required
  report phrase crossed a Markdown line break, followed by the retained 11/11
  validation; and
- zero null, PyGRC, candidate/control, conformance, runtime, or scientific
  reruns during the amendment.

These process facts are explicitly identified as an authored reconstruction
from the observed activity and retained artifacts, not as newly invented
machine-generated execution receipts. The original freezes, native outputs,
validator script, and generated validation remain byte-identical. The additive
closeout binds this final report and the complete non-self I05J package
inventory.

The project owner subsequently accepts the complete amended I05J/I05JA package
and authorizes its commit. `P2-I2-CAL-GATE` is passed and I06 registration
construction is authorized but not begun. No candidate, control, runtime, or
scientific operation is authorized by this acceptance.
