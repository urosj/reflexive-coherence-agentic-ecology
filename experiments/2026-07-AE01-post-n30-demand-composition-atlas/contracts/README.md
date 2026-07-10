# AE01 Contracts

This directory owns the versioned experiment-local contracts frozen by P1-I3.
They govern AE01 records without becoming canonical project specifications.

## Frozen contract set

- [common-contract.md](common-contract.md) is the normative meaning contract.
- [schemas/ae01-contract.schema.json](schemas/ae01-contract.schema.json) is the
  JSON Schema Draft 2020-12 persisted-shape contract at version `1.0.0`.
- [lane-registry.json](lane-registry.json) is the controlling machine registry
  for the seven stable lanes.
- [source-inventory.md](source-inventory.md) is the accepted P1-I1 source
  admission record. Its content remains authoritative; the common schema now
  freezes the shape of a later machine materialization.

The one schema bundle uses a discriminated `record_type` envelope so common
vocabularies and compatibility rules do not drift across many independent
schema files. It defines these seventeen record shapes:

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

## Authority and validation boundary

Markdown controls meaning and cross-record claims. JSON Schema controls the
persisted envelope, required fields, types, enumerations, and closed extension
placement. Python semantic validators will be implemented in P1-I5; they may
enforce cross-record invariants but may not redefine either authority.

The registry currently records manual projection consistency as
`manual_review_passed_pending_automated_validation`. P1-I5 must replace that
status with validator-backed evidence and add negative/conformance fixtures,
canonical serialization, deterministic IDs, digests, and portable-path checks.
No live execution or reconstruction entry point exists yet.

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

This is a reproducible P1-I3 inspection command, not the Python semantic
validator or stable tooling interface deferred to P1-I5.

Contract completeness, schema validity, and registry consistency are not
positive atlas evidence. `AE01-C0` remains the highest assigned rung.
