# P2-I3 I05 B-R Inactive Calibration Freeze

**Status:** retained and clean-commit validated; launch authorized; calibration
not yet invoked

**Iteration:** `P2-I3-I05`

**Lane/branch:** `AE01-L03` / `P2-I3-BR`

**Entry authority:** accepted I04 commit `1097547`; passed
`P2-I3-CAL-PRE-GATE`

**Evidence effect:** inactive invocation-integrity evidence only

**Owner disposition:** package `1.0.2` accepted on 2026-07-19 and retained at
`d054c4df8491ea8f5cc3b13dcb10b222cf8973d5`

## 1. Outcome

The package constructs—but does not activate—one exact candidate-blind
calibration invocation. It resolves the I04-to-I05 arithmetic handoff without
changing the accepted I04 response, estimator, schema, preregistration, or
validation bytes.

The selected construction is:

```text
q_probe = 1/2
C_pre(m_e) = 1/2 + registered_margin

C_pre(m_e) - q_probe = registered_margin
```

The frozen margins range from `-1/2` through `1/2`, so the constructed carrier
range is exactly `[0, 1]`. The request value and construction identity remain
the same across W/O/E and all five exact-null cases.

Fifty focused tests and 42 static checks pass. They call no complete
calibration builder, create no governed claim or output, import no PyGRC, and
assign no `delta`.

The same 50 tests and 42 checks passed again from the exact clean retention
commit. The retained validation reconstructed byte-exactly, the repository was
clean before and after verification, and no launch authorization, claim,
receipt, governed output, or `delta` existed.

The first bounded review correction makes the shared calibration explicit: every
one of the five entered cases contributes exactly one `m_trace` and one
`m_export` margin, for ten margins total. The same `delta` is frozen as the
arithmetic resolution of both relations. A digest-bound semantic validator
now recomputes identities, rational projections, W/O/E triplets, relation
coverage, the maximum null margin, and `delta` before writing and again after
readback. Closed activation, attempt-claim, and final-receipt record contracts
make partial output residue inadmissible without a successful receipt.

The launch-safety correction then derives every normalized margin and `delta`
input directly from exact rational response fields, requires deterministic
process variables, durably flushes both claim bytes and their directory entry,
and revalidates HEAD, committed authorities, activation, environment, exact
claim-only worktree state, and remaining output absence before builder import.
Thirteen injected transaction boundaries prove that any post-claim failure
retains consumption, produces no successful receipt, and admits no `delta`.

## 2. Why this construction

Three bounded choices were available:

| Choice | Benefit | Cost | Disposition |
| --- | --- | --- | --- |
| `q_probe=1`, `C_pre=1+mu` | Reuses the I04 unit-test helper unchanged | Produces carrier values through `3/2`; the helper's local fixture was never I05 authority | Not selected |
| `q_probe=1/2`, `C_pre=1/2+mu` | Exact, uniform, nonnegative, bounded in `[0,1]`, and keeps request semantics matched | Requires an I05-owned construction layer over the unchanged I04 envelope | Selected |
| Case-relative or candidate-relative request | Could tune the carrier range per case | Breaks one-request comparability or introduces candidate-shaped discretion | Prohibited |

The I04 helper's internal `q_probe=1` remains a test-envelope fixture. I05
does not modify it. The I05 builder replaces only the fields deliberately
deferred by I04 and then reuses I04's exact response validator and W/O/E
estimator. This keeps transition to the accepted analysis path explicit.

## 3. Package

| Artifact | Role | SHA-256 |
| --- | --- | --- |
| `configs/p2_i3_br_i05_one_shot_policy.json` | Exact construction, shared-estimator coverage, one-shot, environment, authority, path, and candidate-blind policy | `3e28501b1a2a4f6c148cb49694d69e4322fbf519b59c8eeea9bd7ae41f7b6282` |
| `contracts/p2-i3/i05-br-calibration-invocation-freeze.json` | Inactive invocation identity and gate boundary | `ce2bf6f479197d32009f8a5019a001172bda81db8099318c538030e60def1425` |
| `contracts/p2-i3/i05-br-calibration-output.schema.json` | Closed future output, activation, claim, and receipt shapes | `94a463ea820683d72742d05b2f9a8757619ee8da8a913b2b16978c9c7805f11a` |
| `scripts/p2_i3_i05_br_calibration.py` | Pure complete builder and exact-rational cross-record semantic validator, callable only after claim | `d9155c1a1f03c0543b86a47d7d1439c109dd17b71895493879dd6bb7fd6d687f` |
| `scripts/p2_i3_i05_br_one_shot.py` | Future preflight, durable claim, post-claim revalidation, one invocation, validation, exclusive writes, and readback | `083bc2cfa21553456c8d104e40979cfc0a7448c9346ab5b50ef9b8c66fd4e758` |
| `scripts/p2_i3_i05_br_freeze_validate.py` | Zero-calibration freeze validator | `6d419dd3101414d9807d14840d23a7e6a2af99f1e3c96e6f31fd6e076879b385` |
| `implementation/tests/test_p2_i3_i05_br_freeze.py` | Fifty construction, schema, exactness, durability, failure-boundary, and one-shot tests | `b9d266e581b5b0e3077ad3b718e4b52c31f28096bbe4a068927c9dbf35ecc081` |
| `contracts/p2-i3/i05-br-calibration-freeze-validation.json` | Retained 42-check validation | `763a9d6dac8f22117e19bd6d2e3ebf4411d7d476f56e7f5eea13b1413f866eed` |

The freeze also binds the unchanged accepted I04 policy, schema, analysis,
preregistration, retained validation, and L03 metric-sheet hashes.

## 4. Future governed invocation

If the freeze is accepted and committed, a separate launch-authorization
record must be created and committed. The one-shot command then receives the
full owner-authorized HEAD at invocation time. Before consuming the attempt it
must verify:

- the accepted I04 commit is an ancestor;
- current HEAD equals the supplied full HEAD;
- the index, tracked files, and untracked files are clean;
- every authority path is committed and byte-identical to that HEAD;
- the exact repository `.venv`, Python version, interpreter binary, and
  packages match, with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONHASHSEED=0`;
- the launch record authorizes one calibration and no candidate execution;
- the launch record names the full accepted-freeze commit and exact freeze
  digest, and those bytes remain ancestral to the launch HEAD;
- the permanent claim and all governed outputs are absent; and
- no path component is a symlink.

The activation record does not embed the hash of the commit that contains
itself. That would be circular. Instead it freezes every non-circular source,
command, environment, claim-path, and output-path binding; the exact clean
launch HEAD is supplied at runtime, verified twice, and retained in both claim
and final receipt.

The wrapper then atomically creates a permanent attempt claim before importing
the builder, flushes its file and containing directory, and repeats the
authority/environment/output checks after claim consumption. The accepted
envelope is:

```text
governed attempts             = 1
infrastructure retries        = 0
complete builder invocations  = 1
exact-null cases              = 5
response records              = 15
triplet results               = 5
reconstruction builder calls  = 0
readback outputs              = 3
```

Failure after the claim consumes the attempt. The claim is never deleted. A
second or concurrent start fails on exclusive claim creation.

## 5. Future outputs

One governed builder invocation will create:

1. `br-matched-null.json` — five W/O/E exact-null cases with complete typed
   response and triplet records;
2. `br-metric-calibration.json` — the maximum absolute null margin, the frozen
   measurement floor, an exact-rational ten-margin ledger, and derived `delta`;
3. `br-frozen-metric-sheet.json` — the L03 numeric-resolution projection.

The activation, attempt claim, and final receipt are separately typed closed
records. The claim binds its activation, launch HEAD, accepted freeze,
authority digests, command, environment, paths, and one-call ceiling. The
receipt binds the claim/activation digests, counts, output paths/digests,
shared relation scope, validations, readback, success, and second-start
refusal. Missing or failed receipt leaves the attempt consumed, quarantines
every partial output, admits no `delta`, and keeps CAL-GATE closed. The eight
intentionally nonzero I04 conformance cases cannot enter `delta` and are not
rerun by I05.

Reconstruction reads and canonically reserializes the three retained outputs.
It never calls the builder again.

## 6. Verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  .venv/bin/python -m pytest -q \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests/test_p2_i3_i05_br_freeze.py

50 passed
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 .venv/bin/python \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i3_i05_br_freeze_validate.py \
  --output outputs/reconstruction/p2-i3-i05-freeze-validation.reconstructed.json

cmp \
  experiments/2026-07-AE01-post-n30-demand-composition-atlas/contracts/p2-i3/i05-br-calibration-freeze-validation.json \
  outputs/reconstruction/p2-i3-i05-freeze-validation.reconstructed.json

42/42 checks
byte-exact reconstruction
```

The reconstruction target is non-retained and may be removed after comparison.

### 6.1 Clean-commit retention identity

The post-commit
[retention validation](../contracts/p2-i3/i05-br-retention-validation.json)
binds the complete source identity and reconstruction outcome:

```text
retention commit = d054c4df8491ea8f5cc3b13dcb10b222cf8973d5
tree             = ac40cd5002a2c2942b1afe4e99f234d9b7951ac6
parent           = 1097547ad30b77d4cf9312fb05753902f6d1cc81
retention record = f956eebe1695c62131f7b5cbc107f581eb5ee654a36ca5dcdf5c4f9668328e61
focused tests    = 50 passed
freeze checks    = 42 passed
reconstruction   = byte-exact
calibration calls = 0
```

This record completes retention identity only. It is not launch authority and
does not pass `P2-I3-CAL-GATE`.

### 6.2 Separate launch authorization

On 2026-07-19 the owner directed I05 to proceed through every remaining item
before final owner acceptance. The separate
[launch authorization](../contracts/p2-i3/i05-br-calibration-launch-authorization.json)
materializes that direction without modifying the accepted freeze:

```text
accepted freeze commit = d054c4df8491ea8f5cc3b13dcb10b222cf8973d5
launch-record SHA-256  = 8e55a0f65903d8735d6468f3fc3612a16115a0ad99f0ddb31755f01592e93c33
governed invocations  = 1
infrastructure retries = 0
candidate execution   = false
```

The exact clean commit containing this record is deliberately not embedded in
the record. It will be supplied as `--expected-head`, checked before and after
attempt consumption, and retained by the claim and final receipt. Until that
exact committed invocation occurs, no attempt is consumed and no `delta` is
admitted.

## 7. Review boundary

Review should confirm only:

1. the half-unit construction faithfully resolves the deferred I04 fields;
2. I04 response and estimator authority is reused without mutation;
3. candidate, PyGRC, candidate-seed, and scientific reuse boundaries are
   mechanical;
4. the one-shot claim precedes builder import and invocation;
5. authority, environment, outputs, and reconstruction are sufficiently exact;
   and
6. acceptance opens a retention commit, not calibration invocation.

The owner accepted the package for retention. It was committed without launch
authority or governed output, reconstructed from that exact clean source
commit, and retained through the full 40-character identity above. A separate
launch authorization and explicit direction have now been constructed for the
sole calibration invocation. The run and retained reconstruction remain to be
completed before final owner review.
`P2-I3-CAL-GATE`, I06, B-R candidate execution, C.2, and every scientific or
ecology result remain closed.
