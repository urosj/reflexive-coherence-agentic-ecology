# AE01 P1-I5 Conformance Fixtures

These fixtures test the three-layer authority split without supplying atlas
evidence.

## Valid fixtures

- `valid/empty-ranking.json` proves an empty pre-synthesis ranking can remain
  explicitly `not_run`.
- `valid/artifact-inspection-receipt.json` proves non-runtime inspection has no
  live identity or state fields.
- `valid/conceptual-source-negative.json` proves a conceptual source can be
  admitted while both runtime and positive-evidence permissions remain false.
- `valid/empty-resolved-manifest.json` proves an empty resolved infrastructure
  manifest is deterministic and claim-free.
- `valid/unavailable-realization-profile.json` supplies a compatible shape for
  fail-closed missing-runtime tests without claiming runtime availability.
- `valid/candidate-blind-metric-calibration.json` proves resolution derives
  only from declared measurement resolution and matched-null margins.
- `valid/narrow-developmental-interpretation.json` proves a threshold-passing
  result can remain resolution-adjacent, scaffold-dependent, and bounded by a
  lower rung with a new probe rather than automatic promotion.

## Invalid fixtures

- `invalid/schema-missing-field.json` fails JSON Schema shape authority.
- `invalid/incompatible-version.json` fails exact-version compatibility.
- `invalid/constructed-native-role.json` passes basic shape but fails Python
  semantic authority because an RCAE construction is relabeled as inherited
  graph evidence.
- `invalid/threshold-relation-mismatch.json` passes shape but fails semantic
  authority because its asserted relation disagrees with the seed margins and
  frozen resolution band.

## Reconstruction inputs

- `inputs/l01-candidate-blind-calibration-input.json` is the exact non-record
  CLI input for reconstructing the Lane 1 calibration example. It contains no
  candidate outcome and has no evidence effect by itself.

The normative Markdown meaning remains in `../common-contract.md` and the
P1-I4 hypothesis/control/failure set. Fixtures cannot redefine it and cannot
support a lane, terminal classification, gate, or acceptance rung.

Run all fixture checks from the repository root through the command documented
in `../../scripts/README.md`.
