# P2-I2-I05H I01/I02 source-and-identity portability correction

Date: 2026-07-14

Status: `P2-I2-I05H-I01-I02-GROUP-REVIEW-READY`

## Scope and authority

I05H is the fourth bounded group in the accepted I05D correction order. It is
owned by `P2-I2-DEC-038` and `P2-I2-CHG-031`, with source authority fixed at
commit `62882efc5ecf3c131d21345ad89796f0b2ebccb7`.

The exact scope is `i01_i02_source_and_identity`:

- 10 affected files;
- 35 accepted I05D findings;
- 24 embedded machine-local absolute tokens;
- 11 exact POSIX absolute values;
- 4 historical JSON artifacts, 3 historical reports, and 3 Python sources.

No fifth correction group is authorized by this closeout.

## Correction

The four JSON artifacts now use logical external-repository and temporary-
directory identities and declare their historical source commit/digest,
decision, change, projected-command non-executability, and zero scientific
change.

The three reports replace machine-local graph and temporary-directory tokens
with `${GRC}` and `${TMPDIR}` and append explicit historical lineage. The three
Python sources no longer select an interpreter through a shebang. Five I02R2
temporary-directory contexts now let `tempfile` select the system temporary
root instead of fixing one POSIX location.

The additive lineage binds every historical and projected byte identity. Raw
I01/I02 evidence remains unchanged at the source commit; current files are
portable projections, not replacement raw receipts.

## Scientific and runtime boundary

The correction does not alter any accepted I01 capability conclusion,
quarantine, I02 source admission, public-source digest, identity authority,
reset-baseline result, restoration boundary, downstream duty, or gate.

Validation is static and uses only `.venv/bin/python`. It imports no PyGRC,
instantiates no model, and invokes no historical validator, manifest builder,
conformance path, candidate/control path, calibration/null builder, one-shot
wrapper, or scientific operation.

## Validation disposition

The governed validator verifies the exact accepted group, reconstructs all
source bytes from the accepted commit, checks every lineage pair, reconstructs
all ten projections exactly, parses the three Python sources, scans the group
and I05H package for persisted absolute paths, checks prior I05G identities,
and enforces the zero-execution boundary.

The retained validation artifact is progression evidence for owner review.
I05H does not authorize a commit by itself and does not pass `CAL-GATE`.
