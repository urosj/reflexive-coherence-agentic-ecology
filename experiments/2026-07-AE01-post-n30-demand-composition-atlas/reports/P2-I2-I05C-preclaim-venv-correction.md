# P2-I2 I05C Pre-Claim Active-Venv Correction

This current-tree report is a portability projection under DEC-033/CHG-026.
Its historical source is retained at commit `c3eabf3` with SHA-256
`da49ff8a7c430dcc1a8568fe00d698ddd2af7a771625f029a3b2500ecc2b1f3c`;
no scientific or execution fact changes here.

## Disposition

The first final 10.4 preflight failed closed before claim creation because the
accepted wrapper treated the valid `.venv/bin/python` symlink as a repository
data file. The command did use the active repository venv; only its resolved
digest-bound host Python 3.12 target is outside the repository.

DEC-031/CHG-024 correct only this identity distinction. Thirteen focused tests
and 12/12 machine checks pass with zero governed attempt, accepted-builder/null,
PyGRC, candidate, or control operation. The correction is uncommitted and
returns for review. CAL-GATE remains closed.

## Failed-closed boundary

The retained failure record binds launch HEAD
`98770ae4860ddc269a9ed21bb4803ec75682fc34`, the exact invoked venv path, active
venv/base prefixes, resolved target, exception, and zero execution counts.

```text
normalized command interpreter = .venv/bin/python
sys.executable = <repository>/.venv/bin/python
sys.prefix = <repository>/.venv
sys.base_prefix = separated host base runtime; location not persisted
venv active = true
resolved target identity = sha256:1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118
failure stage = read-only final preflight before claim
attempt claim = absent
authority consumed = false
builder/null invocations = 0
```

Because the permanent claim was not created, this was not a governed attempt
or infrastructure retry. The single authorized attempt remains available.

## Corrected identity model

The wrapper now requires all of the following independently:

- normalized command path exactly `.venv/bin/python`;
- `sys.executable` exactly the repository `.venv/bin/python` path;
- active venv with `sys.prefix` equal to repository `.venv`;
- `sys.prefix != sys.base_prefix`;
- lexical command containment checked without following the final symlink;
- resolved target recorded separately;
- resolved target digest equal to the frozen Python binary SHA-256;
- CPython major/minor version remains 3.12.

This does not permit direct host-Python invocation. The target is admitted only
by the frozen digest behind the active venv command; its location is not
persisted.

The accepted I04R2 builder, estimator, calibration inputs, output path,
one-attempt/zero-retry policy, atomic claim, reconstruction, and scientific
boundaries are unchanged.

## Validation

The focused suite now has thirteen tests. It adds a direct positive assertion
against the real active repository venv and retains refusal of wrong command,
wrong invoked path, inactive venv, wrong binary digest, wrong HEAD, dirty
authority, concurrent/later/crashed claims, existing output, and acceptance
without launch authority.

Machine validation confirms:

```text
I05C checks = 12/12
active repository venv = exact
accepted I04R2 bytes = immutable
attempt claim/final/output = absent
governed attempts = 0
infrastructure retries = 0
accepted builder/null invocations = 0
PyGRC/candidate/control operations = 0
graph revision = 83e3a300426631ee4df71b661b67d4fcfdfed594, clean
CAL-GATE = closed
```

## Exact identities

| Artifact | SHA-256 |
| --- | --- |
| Corrected one-shot policy | `71dddb9f89a1d195e84899555ebdadbda45041405d04cbcbe03628ab536b932a` |
| Corrected governed wrapper | `b6cf5e3129821660fb77b2f7c3591a66d859d18930cc28681fa8096d7462220c` |
| Updated owner acceptance | `fb1eedf30a477e938339366d380f30e263b19b73efc7881c41df97170cd3acb3` |
| Updated launch authority | `a8f1434190e875d39569c2a6b2ed670d606a98717950e0b8707f083a7823bb7a` |
| Failed preflight record | `0a1bff47797a23e18ef143b2418d3d0b697615c88ac121a547450e7234ce3fed` |
| Thirteen-test suite | `12f890e622772b9d5d0d6e61fef33c8f9fef3cbcba8a66e4e11b3bec23ec53d8` |
| I05C validator | `ef933f921d1feda1000aa41ecedc1e7b4ea59dbfdae184c54e182aa60f8246b7` |
| I05C validation | `71cc9d8b32448cc228259e166f03888cdb771e92f3be229a4c8823189030e8b7` |

## Review boundary

Review should confirm that direct system-Python invocation remains impossible,
the active repository venv is positively required, the resolved binary is still
digest-bound, the failed preflight consumed no attempt, and no I04R2 or
scientific byte changed. Commit and another final preflight remain unauthorized
until explicit owner review.
