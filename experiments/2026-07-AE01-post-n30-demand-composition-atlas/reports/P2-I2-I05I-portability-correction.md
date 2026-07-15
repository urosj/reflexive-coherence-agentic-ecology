# P2-I2-I05I terminal portability correction

Date: 2026-07-14

Status: `P2-I2-I05I-TERMINAL-GROUP-REVIEW-READY`

## Scope and combination disposition

The accepted I05D order and current P2-I2 audit boundary identify only one
residual group, not two. The fifth/final group is
`p2_i2_governance_navigation_and_shared_projections`:

- 6 affected files;
- 14 embedded machine-local absolute tokens;
- 3 self-governance Markdown files;
- 1 historical I00 report;
- 1 script README; and
- 1 calibration Python source.

There is no second accepted residual group to combine. Older P2-I1/shared AE01
files found by a broader experiment-directory text search are outside the
accepted P2-I2 audit boundary and are not changed by I05I.

Before the first validator start, owner inspection identified a defect class
the literal-token scanner missed. `p2_i2_i05g_validate.py` constructed both a
historical RCAE root and a graph root; `p2_i2_i05h_validate.py` constructed a
graph root. These two files and three constructor surfaces are included in the
same final correction. I05I therefore has eight source files, not a new
correction group or suffixed iteration.

The second failed-closed validation start applies the expanded constructor
guard to the complete P2-I2 Python scope and identifies one more surface:
`p2_i2_i05f_validate.py` constructs a historical interpreter shebang. That
ninth source is added to I05I and now derives the expected removed shebang from
the retained historical file itself.

## Correction

Historical system-interpreter, graph-checkout, and temporary-output locations
are represented by logical identities. The calibration script no longer
selects an interpreter through a shebang. The I00 report and script README
retain explicit historical source lineage. DEC-039, CHG-032, the checklist,
and the hypothesis record the self-governance boundary and terminal closeout.
The I05G/I05H validators now discover retained historical roots from semantic
markers instead of embedding or reconstructing machine-specific locations;
the I05F validator discovers its historical shebang from retained source.

All nine raw sources remain unchanged at commit
`1279e177d6691417a1d692dd8fdfc5cf50060e11`. The additive lineage binds each
raw source digest to its portable current projection.

## Validation boundary

The static validator:

- reconstructs the exact accepted six-file/14-finding group, the two owner-
  identified root-constructor validators, and the guard-identified shebang-
  constructor validator;
- reconstructs every historical source from the accepted commit;
- checks all nine lineage pairs;
- verifies the three non-governance projections exactly;
- parses all three validator projections and rejects constructed absolute
  bindings;
- bounds self-governance changes to I05H acceptance, DEC-039/CHG-032/I05I
  declaration/closeout, and the frozen path substitutions;
- parses the calibration source without importing it; and
- scans the complete current P2-I2 audit scope to zero literal and constructed-
  root findings.

All three frozen `.venv/bin/python` validator starts are used. The first
fails closed at I05I-02 before output because the initial correction policy
mistook three pre-I05H governance digests for the exact `1279e17` source bytes.
The policy, freeze, and lineage are corrected in place. The second fails closed
at I05I-04 before output after finding the I05F constructed shebang; that source
is added and corrected. The third start passes 10/10. Validation performs no PyGRC import, model
instantiation, historical validator or manifest-builder invocation,
candidate/control/conformance/scientific execution, calibration/null builder,
one-shot wrapper, or retry.

I05I remains uncommitted for owner review. It does not itself pass `CAL-GATE`.
