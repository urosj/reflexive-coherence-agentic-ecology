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
