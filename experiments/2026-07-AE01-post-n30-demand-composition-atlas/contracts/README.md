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
placement. The P1-I5 Python semantic validator enforces cross-record invariants
without redefining either authority.

The registry records validator-backed `validated` projection status. P1-I5
adds [conformance fixtures](fixtures/README.md), canonical serialization,
deterministic IDs and digests, portable-path checks, strict runtime receipts,
resolved manifests, and reconstruction commands. The complete implementation
boundary is in the
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
positive atlas evidence. `AE01-C0` remains the highest assigned rung.
