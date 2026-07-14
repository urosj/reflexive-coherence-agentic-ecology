# P2-I2 I05 Single-Invocation Authorization Freeze

> Follow-up I05A safety audit passed only 3/8 checks and blocks acceptance of
> this candidate. See
> [P2-I2-I05A execution-safety audit](P2-I2-I05A-execution-safety-audit.md).

## Disposition

I05 has one identity-validated, unconsumed arithmetic-null authorization
candidate. It is not acceptance-ready after I05A. If the five safety blockers
were separately corrected, owner-accepted, and committed, it would permit one
governed invocation of the owner-accepted I04R2 entry point and no candidate
execution. It is not currently active or committed. The arithmetic null was
not invoked, no calibration output exists, and `P2-I2-CAL-GATE` remains closed.

## Authority and identities

The freeze is downstream of `P2-I2-DEC-026`, the passed CAL-PRE gate, and
accepted-I04 commit
`b7b008c402d837b529962a1a5edb062927939d28`. It binds:

| Surface | SHA-256 |
| --- | --- |
| I04R1 parent analysis policy | `91b8bd50633a19333935ec115bdd005697abdef5381ef59f4ceab21db08c090d` |
| I04R2 machine policy | `277dfc22c9e98268e950cb634ed1174b9ad4f0f654a72984b365655815c3a9ce` |
| I04R2 calibration policy | `57dc32d02b828bb21caf069c5690bf4fcfc240848faefcd8412a6505bba849fe` |
| I04R2 calibration entry point | `8a0ef5569705ea0619a628b3b5a25d9dc80448a273a68a92d131ce775793b61a` |
| I04R2 preregistration | `dee89df45b4a5ece93d1d7ce461d2c0cb8f028ff44aa32b3f4e45e88a1b09e9b` |
| I04R2 owner-acceptance record | `2ade4d6255c42044621489e1132d1030f48266e851bea614a11f1100c4f7dacf` |
| I05 execution freeze | `97a78f7f5e8b1119ec059b82a7a5b6c14c573efc55411ac4392ff6cf2703545a` |

The accepted commit contains the same I04R2 bytes as the working tree. I04R2
remains the sole progression authority; original I04 and I04R1 remain
immutable historical artifacts. The exact-tie `q1-only` provenance rule keeps
no scientific meaning.

## Static validation

The focused validator passed 12/12 checks and reconstructed its retained JSON
byte-identically. It called only
`p2_i2_i04r2_calibration.validate_execution_authorization`; it did not call
the calibration builder or CLI entry point. It also confirmed:

- one and only one governed invocation is authorized;
- candidate execution is false;
- all active identities match both the accepted commit and current files;
- the governed output is absent;
- no PyGRC module was imported;
- the graph checkout is clean at admitted revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594`; and
- no matched-null, PyGRC, candidate, or control invocation occurred.

Retained validation SHA-256:
`47b9e6c116684ba2d381d7f8640571a71f1733fd9d2a65862bedcbd6622fb0b6`.
The validation record binds validator SHA-256
`2765e479548132dd9c00802b80dfd85350299a1597af07150c41190e64fcb427`.

## Gate effect

This activity establishes proposed-permission integrity only. It assigns no
`analysis_arithmetic_delta`, does not populate or freeze a metric sheet, does
not pass CAL-GATE, and has no operational-hypothesis or scientific effect.
The next permitted operation is owner review. Only explicit acceptance and
commit authorization may activate the candidate; a later separately directed
single exact I04R2 arithmetic-null invocation would then be possible. I06 and
all candidate/control execution remain closed.
