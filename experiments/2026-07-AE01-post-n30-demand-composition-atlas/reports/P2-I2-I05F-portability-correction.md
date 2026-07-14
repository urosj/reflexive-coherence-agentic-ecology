# P2-I2 I05F I04/I05 Authority-Dependency Portability Correction

## Disposition

I05F technically removes all 30 accepted I05D portability findings from the
exact thirteen-file `i04_i05_authority_dependencies` group. The correction
changes only path representation and script portability. It does not revise
accepted I04R2 scientific, estimator, comparator, measurement-window,
calibration, or gate semantics. I05F is not process-clear, however: its frozen
static-validation invocation ceiling was exceeded.

The source bytes remain available at commit `6dd6898`, and the accepted I04R2
authority remains available at commit `b7b008c`. Every changed JSON artifact
declares its source commit and digest. The additive lineage manifest binds all
thirteen source and current digests without embedding a checkout location.

## Portable identity model

- PyGRC sources use repository ID `graph-reflexive-coherence`, a
  source-relative POSIX path, and the unchanged source SHA-256.
- The owner-review attachment uses its stable attachment ID, relative artifact
  name, and unchanged content SHA-256.
- JSON field authorities use an artifact path plus explicit field identities;
  embedded slash-form pseudo-pointers are removed.
- Validators derive the PyGRC checkout as the logical sibling repository and
  never persist the resolved location.
- Calibration record builders normalize all RCAE input identities to
  repository-relative POSIX paths. Their arithmetic and input hashes are
  unchanged.
- Python files have no machine-selecting shebang and are invoked only through
  `.venv/bin/python`.

## Historical and execution boundary

The I05F validator reconstructs all eight JSON projections from the frozen Git
blobs and admits only the frozen path-related source edits in the five Python
files. It separately checks current PyGRC source digests, accepted I04R2
historical identities, and byte equality of the I05 output projection,
permanent claim projection, and raw final receipt at commit `6dd6898`.

No calibration builder, arithmetic-null wrapper, PyGRC model, candidate,
control, conformance run, or scientific run is invoked. I05F produces no
scientific result and does not change CAL-GATE status.

The freeze allowed three static-validation invocations. Actual preparation
used 13 `.venv/bin/python` process starts: eight JSON syntax checks, one
five-file compile check, three governed validator starts, and one read-only
scanner diagnostic. The first validator attempt failed closed on findings
caused by validator-local historical-shebang literals. The diagnostic localized
those literals. The second validator attempt failed closed because the
source-diff whitelist omitted two syntax-only additions. Neither failed attempt
wrote an output. The third attempt passed 10/10 and alone wrote the technical
validation artifact. All 13 starts remained inside the zero-builder,
zero-runtime boundary.

DEC-035 accepts this process-only deviation through the additive
`i05f-static-validation-deviation-closeout.json` record. The original freeze
is unchanged, the 13-start ledger remains explicit, and no Python or technical
validation was rerun during closeout construction.

## Review boundary

The project owner subsequently confirmed under DEC-036 that completed closeout
also constitutes full I05F acceptance and commit authorization. The accepted
package therefore includes exact group closure, historical-to-portable
reconstruction, unchanged I04R2/I05 semantics, zero runtime execution, and the
explicit 13-versus-three deviation without claiming original-freeze
compliance. No I03 or later portability group is authorized by I05F.
