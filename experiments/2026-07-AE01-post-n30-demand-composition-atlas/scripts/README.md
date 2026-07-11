# AE01 Scripts

This directory contains the experiment-local P1-I5 implementation. It is not a
reusable `rc_agentic_ecology` source package and does not change PyGRC.

## Entry point

All commands run from repository root with the pinned inspection dependency:

```text
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py <command>
```

### `validate-phase1`

Validates the P1-I3 schema and records, P1-I4/P1-I5 vocabulary and policy,
lane projections, valid fixtures, and expected-invalid fixtures. With no
`--output`, the deterministic non-evidential summary is printed to stdout.

### `resolve-policy`

Materializes all shared defaults: configuration IDs, seeds, attempt/retry
limits, resources, artifact roles, completion/failure criteria, and the
applicability/priority of all nineteen common controls for every lane.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py resolve-policy --output outputs/ae01-resolved-policy.json
```

### `digest`

Reports canonical semantic digest, exact-file SHA-256, and size without
modifying the artifact.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py digest --input outputs/ae01-resolved-policy.json
```

### `freeze-resolution`

Consumes a pending primary metric sheet and candidate-blind matched-null input.
It writes a schema-valid calibration record and frozen metric sheet with:

```text
delta = max(measurement resolution, maximum absolute matched-null margin)
```

The input seeds must exactly match the sheet's calibration seed profile. The
command fails if candidate blindness, seeds, or resolution status differ.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py freeze-resolution --metric-sheet experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/metric-sheets/AE01-L01.json --calibration-input experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/fixtures/inputs/l01-candidate-blind-calibration-input.json --calibration-output outputs/ae01-l01-metric-calibration.json --frozen-sheet-output outputs/ae01-l01-frozen-metric-sheet.json
```

### `classify-margin`

Derives the threshold relation from a frozen sheet while preserving every
seed margin. A pending sheet produces `resolution_unknown`, never intuitive
“narrow” or “robust” wording.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py classify-margin --metric-sheet outputs/ae01-l01-frozen-metric-sheet.json --margin 101:0.08 --margin 211:0.03 --margin 307:0.06
```

### `runtime-receipt`

Requires a lane-local `realization_profile` record, explicit live class, run
ID, operations, and receipt output. The profile must explicitly declare the
realization available and enabled, the class and operations must match it, and
PyGRC must already be available in the local Python environment. Its location
is not committed or recorded.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py runtime-receipt --profile outputs/local-realization-profile.json --run-id ae01-local-run --execution-class pygrc_runtime_with_rcae_producer --operation binding-check --receipt-output outputs/ae01-local-runtime-receipt.json
```

This command validates the binding requested for those operations; it does not
pretend that the future lane operation itself ran. A Phase 2 lane runner must
use the same receipt boundary around its actual state transition. Pass
`--graph-root` with the locally configured graph checkout when source-tree
fingerprint guarding is required. That machine-local argument never enters the
receipt. Missing/incompatible PyGRC writes a failed receipt and exits nonzero;
there is no fallback.

### `build-manifest`

Consumes a descriptor containing profile-registry path, source revisions,
artifact declarations, and optional realization-profile paths. Every declared
artifact must already exist and pass digest/profile/tier checks.

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py build-manifest --descriptor outputs/local-manifest-descriptor.json --output outputs/ae01-local-manifest.json
```

### `assemble-report`

Consumes a P1-I3 `report_projection` and optional separately authored Markdown.
Use `--preview-digest` first to calculate the deterministic digest fields for a
new projection without writing a report. Freeze those values in the projection,
then run the final assembly:

```bash
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py assemble-report --projection outputs/local-report-projection.json --preview-digest
uv run --with jsonschema==4.26.0 python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py assemble-report --projection outputs/local-report-projection.json --output outputs/ae01-local-report.md
```

For `assembled_interpretation`, also pass `--authored` with the portable path
to its tracked authored source.

## Reconstruction boundary

Commands write only to explicitly supplied RCAE-relative outputs. Disposable
products belong under ignored top-level `outputs/`. Only an explicit verified
manifest and retention decision can move selected evidence under the
experiment. No command writes into the graph/PyGRC repository.

## P2-I1 entry point

`p2_i1.py` is the thin file/CLI boundary. `p2_i1_analysis.py` contains pure
deterministic analysis and never imports PyGRC. `p2_i1_runtime.py` imports
PyGRC only inside an explicit runtime call and contains no candidate runner
while `P2-I1-REG-GATE` and `P2-I1-EXEC-GATE` remain closed.

Create the ignored local environment and install a non-editable build from the
locally configured PyGRC source plus the pinned validation dependency:

```bash
uv venv .venv
uv pip install --python .venv/bin/python LOCAL_PYGRC_SOURCE jsonschema==4.26.0
```

`LOCAL_PYGRC_SOURCE` is machine-specific and never enters shared records. A
retained runtime profile must instead record the installed `pygrc==0.1`
identity and source revision/digests.

Validate the five committed P2-I1 configs:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py validate-configs
```

Generate the CAL-PRE code, policy, fixture, cell, calibration, runtime, and
static-profile identity. The result records the current source revision and
therefore becomes a retained freeze artifact only after the implementation
commit is final:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py build-cal-pre-identity --output outputs/p2-i1-cal-pre-identity.json
```

The freeze command fails when the worktree is dirty. During implementation
review, an explicitly non-retainable preview may be generated with
`--allow-dirty-preview`; its artifact kind, identity ID, clean-state flag, and
retention eligibility prevent it from masquerading as the final freeze.

Generate the candidate-blind matched null through the same opportunity
aggregation and paired-margin functions later used for live records:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py generate-matched-null --output outputs/p2-i1-matched-null.json
```

Analyze retained raw opportunity records without authored recomputation:

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py analyze --input outputs/p2-i1-opportunities.json --output outputs/p2-i1-analysis.json
```

### Runtime preflight

Runtime preflight requires an ignored local `realization_profile` record whose
availability, enabled, supported, and validated fields are all true; whose
PyGRC identity is `pygrc==0.1`; and whose allowed operations contain
`p2_i1_runtime_preflight`. The local environment must already make that exact
PyGRC available. Its installation and checkout locations are arguments only
and never enter a shared record.

```bash
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py runtime-preflight --realization-profile outputs/p2-i1-local-realization-profile.json --run-id p2-i1-local-preflight --graph-root LOCAL_GRAPH_CHECKOUT --output outputs/p2-i1-runtime-preflight.json
```

Missing dependencies, an incompatible identity, a disabled local profile, or
an undeclared operation produces a failed binding receipt and no fallback.
The preflight builds and snapshots the baseline fixture only. It does not emit
a writer packet, medium row, opportunity, candidate result, or lane evidence.
