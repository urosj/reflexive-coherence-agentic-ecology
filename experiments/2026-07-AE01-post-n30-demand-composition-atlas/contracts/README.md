# AE01 Contracts

This directory owns the versioned experiment-local contracts frozen by P1-I3
and explicitly revised at revision 0.24.
They govern AE01 records without becoming canonical project specifications.

## Frozen contract set

- [common-contract.md](common-contract.md) is the normative meaning contract.
- [schemas/ae01-contract.schema.json](schemas/ae01-contract.schema.json) is the
  JSON Schema Draft 2020-12 persisted-shape contract at version `1.1.0`.
- [lane-registry.json](lane-registry.json) is the controlling machine registry
  for the seven stable lanes.
- [source-inventory.md](source-inventory.md) is the accepted P1-I1 source
  admission record. Its content remains authoritative; the common schema now
  freezes the shape of a later machine materialization.

The one schema bundle uses a discriminated `record_type` envelope so common
vocabularies and compatibility rules do not drift across many independent
schema files. It defines these twenty record shapes:

| Contract surface | Record type |
| --- | --- |
| source inventory | `source_inventory` |
| stable lane registry | `lane_registry` |
| pattern card | `pattern_card` |
| medium surface | `medium_surface` |
| requirement extraction | `requirement_extraction` |
| composition assessment | `composition_assessment` |
| debt | `debt_record` |
| claim boundary and unsafe flags | `claim_boundary` |
| constructed mechanism | `constructed_mechanism` |
| realization profile | `realization_profile` |
| runtime-binding receipt | `runtime_binding_receipt` |
| catalog/domain/applicability placement | `catalog_placement` |
| terminal classification and stopping | `terminal_classification` |
| N31+ ranking or non-selection | `n31_ranking` |
| reconstructed artifact manifest | `artifact_manifest` |
| shared-profile registry and resolution | `profile_registry` |
| generated or assembled report projection | `report_projection` |
| primary metric formula and resolution policy | `metric_sheet` |
| candidate-blind resolution calibration | `metric_calibration` |
| threshold, boundary-rung, and two-axis reading | `developmental_interpretation` |

Revision `1.1.0` requires every terminal classification to reference a
developmental interpretation. Existing retained `1.0.0` records remain
versioned history and do not migrate silently.

## Authority and validation boundary

Markdown controls meaning and cross-record claims. JSON Schema controls the
persisted envelope, required fields, types, enumerations, and closed extension
placement. The P1-I5 Python semantic validator enforces cross-record invariants
without redefining either authority.

The registry records validator-backed `validated` projection status. P1-I5
adds [conformance fixtures](fixtures/README.md), canonical serialization,
deterministic IDs and digests, portable-path checks, strict runtime receipts,
resolved manifests, metric calibration, threshold-relation derivation,
developmental-interpretation guards, and reconstruction commands. The
complete implementation boundary is in the
[P1-I5 tooling contract](../implementation/P1-I5-tooling-contract.md).

## Freeze verification

From the repository root, validate the Draft 2020-12 schema itself and the
controlling registry instance with the pinned inspection dependency:

```bash
uv run --with jsonschema==4.26.0 python -c 'import json; from jsonschema import Draft202012Validator; s=json.load(open("experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/schemas/ae01-contract.schema.json")); x=json.load(open("experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/lane-registry.json")); Draft202012Validator.check_schema(s); Draft202012Validator(s).validate(x); print("schema and lane registry valid")'
```

Expected output:

```text
schema and lane registry valid
```

This remains the narrow P1-I3 shape-only inspection command. The complete
P1-I5 schema, semantic, projection, policy, and fixture validation command is:

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py validate-phase1
```

Contract completeness, schema validity, and registry consistency are not
positive atlas evidence. Review R2 assigned `AE01-C2` for the accepted Phase 1
contract; no lane or higher scientific rung is assigned.

## P2-I3 B-R bounded-conformance freeze

`p2-i3/i03-br-bounded-conformance-input-freeze.json` is the accepted inactive
DEC-034 authority. It binds exact sources and public calls, a result-neutral two-route
fixture, eleven conformance cells, narrow RCAE ownership, Q-013/Q-015
addressability, and mechanical downstream quarantine. Its 85-check validation
performs no LGRC model operation and creates no conformance output. The freeze
cannot supply later scientific values. Harness construction and runtime wait
for the accepted freeze's clean source-anchor commit.

## P2-I3 B-R I04 calibration preregistration

`p2-i3/i04-br-calibration-preregistration.json` binds the accepted
DEC-036-through-DEC-040 authority to the exact machine policy, closed schema,
pure analysis path, validator, and focused tests.
`p2-i3/i04-br-machine-records.schema.json` defines a closed five-record root
union and eight response, pair/triplet, control-leg, terminal-overlay, and
component definitions. The retained
`p2-i3/i04-br-calibration-preregistration-validation.json` passes 485 static
checks and reconstructs byte-exactly.

This package runs no calibration builder and produces no `delta`. Its 22 pure
tests exercise response/estimator conformance, conditional schema closure, the
42-leg policy, and non-destructive reconstruction. The owner accepted the
corrected package and passed `P2-I3-CAL-PRE-GATE` on 2026-07-19, opening only
construction of a separate inactive I05 invocation freeze.

## P2-I3 B-R I05 inactive calibration freeze

`p2-i3/i05-br-calibration-invocation-freeze.json` binds DEC-041, accepted I04
source identities, the half-unit construction, one-shot envelope, candidate-
blindness, environment, outputs, and zero-execution gate boundary.
`p2-i3/i05-br-calibration-output.schema.json` is a closed root union for the
future matched-null, metric-calibration, frozen-metric-sheet, activation,
attempt-claim, and final-receipt records. A bound semantic validator resolves
nested response/triplet shapes against accepted I04 schema `1.0.1`, enforces
both-relation coverage, and recomputes identities and arithmetic. The retained
`p2-i3/i05-br-calibration-freeze-validation.json` passes 42 checks with 50
focused tests.

The owner accepted `1.0.2` for exact retention, and
`p2-i3/i05-br-retention-validation.json` binds clean retention commit
`d054c4df8491ea8f5cc3b13dcb10b222cf8973d5`, the accepted source digests,
50 passing tests, 42 passing checks, and byte-exact reconstruction. That record
has SHA-256
`f956eebe1695c62131f7b5cbc107f581eb5ee654a36ca5dcdf5c4f9668328e61`
and retention effect only. The separately schema-validated
`p2-i3/i05-br-calibration-launch-authorization.json` now binds the accepted
freeze and exact source/environment/path envelope for one invocation under the
owner's direction to complete I05 through the final acceptance boundary. Its
exact launch HEAD was runtime-supplied as
`7a58471a7ba680e67e11cb35037cb7a3fac9f3f2`. The sole invocation completed
successfully; the permanent claim, final receipt, three calibration outputs,
and 49-check independent validation are retained under `outputs/p2-i3/i05/`.
The shared `delta=1e-12` is numeric-resolution evidence only.

`p2-i3/i05-br-owner-acceptance-and-cal-gate.json` records that final
acceptance, binds the launch HEAD, activation, permanent claim, successful
receipt, three governed outputs, 49-check validation, exact shared `delta`, and
interpretation ceiling, and passes `P2-I3-CAL-GATE`. Its SHA-256 is
`16c820aaa2bba3ed2fa34604437f0c2202e194aa0db6c507a712dc30a09cdac0`. It
opens I06 exact implementation registration only.

## P2-I1 registration materialization

`p2-i1/registration-records/` applies the existing `1.1.0` record vocabulary
to the first concrete lane. It contains one registered-probe pattern card, one
candidate medium-surface account, one constructed orchestration boundary, one
registration-only claim boundary, and four explicit debts. These records test
the Phase 1 shapes in use; they do not add `lane_registration` or
`control_outcome` record types and do not contain candidate outcomes.

`p2-i1/registration-realization-profile.json` binds the path-free realization
identity used by registration. The derived registration freeze and manifest
are generated only after their source implementation is committed, so their
source revision and digests cannot accidentally identify an earlier commit.

## P2-I2 source-current audit controls

`p2-i2/i01-audit-input-freeze.json` preregisters the exact graph revision,
scope, questions, classifications, commands, package-identity rule, and output
paths before capability inspection. `P2-I2-CHG-002` records the manifest-led
addition of `src/pygrc/**` before package source was read.

`p2-i2/i01-capability-matrix.json` is the compact requirement-to-surface
projection. `p2-i2/i01-source-digests.json` binds its cited source-current
files. I01R1 excludes the historical custom probe from capability evidence,
classifies CAP-04 as inadequate, and adds the public causal-history
implementation/test digests needed to distinguish evidence overlays from
active runtime history. These are audit-control artifacts, not schema
instances, source admission, realization selection, calibration, or lane
evidence.

## P2-I2 I04 authority lineage

The original I04 and I04R1 contracts are immutable historical artifacts.
Owner-accepted I04R2 is the sole progression authority under DEC-026, with its
exact preregistration and 16/16 validation retained under `p2-i2/`. CAL-PRE is
passed. `i05-calibration-execution-freeze.json` is the separate exact
authorization candidate encoding a one-invocation ceiling, and
`i05-calibration-authorization-validation.json` validates it 12/12 with byte-
identical reconstruction. `i05a-execution-safety-audit.json` passed only 3/8
checks and blocks proposed DEC-027 historically. The DEC-028 I05B correction
then passes 12/12 in `i05b-zero-null-safety-validation.json` with twelve focused
tests and zero accepted-builder/null execution. DEC-029 retains exact
`i05b-owner-acceptance.json` with commit true and null authority false. A later
separate launch consumed the single attempt and retained raw claim/output/final
evidence at commit `c3eabf3`; CAL-GATE passage and candidate authority are not
implied.
`i05c-preclaim-interpreter-path-failure.json` retains the failed read-only
preflight at launch commit `98770ae` with zero attempts. The corrected
`i05c-zero-null-interpreter-validation.json` passed 12/12, was retained, and the
single governed null later completed. DEC-032 now governs I05D:
`i05d-portability-audit-input-freeze.json` binds the corrected recursive scope,
policy, scanner, and zero-runtime ceiling. The accepted inventory reports 312
value-redacted violations in 70 of 135 files. DEC-033 opens only its first I05
group. `i05e-portability-correction-input-freeze.json`,
`i05e-portable-projection-lineage.json`, and
`i05e-portability-correction-validation.json` retain the eleven-file portable
projection correction: 10/10 checks and zero remaining group violations. The
package is owner-accepted for commit; later groups remain closed until
retention, and CAL-GATE remains closed.
