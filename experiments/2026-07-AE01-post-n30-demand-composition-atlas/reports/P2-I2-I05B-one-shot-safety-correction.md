# P2-I2 I05B One-Shot Safety Correction

## Disposition

The bounded I05-owned correction is owner-accepted. Twelve zero-null safety tests
and 12/12 machine checks pass, and the retained validation reconstructs byte-
identically. No accepted-builder/null, PyGRC, candidate, or control invocation
occurred.

The machine owner-acceptance record is retained with commit authorization true
and null-invocation authorization false. No attempt claim, final receipt, 10.4
launch record, or governed calibration output exists. The package is approved
for commit under DEC-029/CHG-022; null invocation remains separately gated and
CAL-GATE is closed.

Proposed DEC-027 remains the failed-closed historical disposition. DEC-028 and
CHG-021 own this correction only.

## I05-owned mechanics

The correction adds one governed wrapper and one one-shot policy. It does not
modify the accepted I04R2 estimator, analysis, comparator, calibration policy,
preregistration, validation, or tests.

The future governed path is:

```text
validate exact policy/paths
reject existing claim, governed output, or final receipt
validate expected runtime HEAD and clean index/worktree
validate exact interpreter binary and normalized command
prove every authority file is committed at HEAD and byte-equal locally
validate machine owner acceptance, separate 10.4 launch authority, permanent
claim storage, and complete frozen hashes
atomically create permanent attempt claim with O_CREAT|O_EXCL
call accepted I04R2 build_calibration_record exactly once
exclusively write governed output
read/parse/canonicalize/compare retained output exactly once
mechanically demonstrate second claim refusal
write final receipt
```

The accepted builder is imported only inside the post-claim adapter. The claim
is never deleted. If claim writing, import, validation, builder execution,
output writing, reconstruction, or final-receipt writing fails, the exclusive
claim path remains and every later start is refused. A hard crash after claim
therefore consumes the attempt even when no final receipt can be written.

The one-shot policy fixes:

```text
max_governed_attempts = 1
max_infrastructure_retries = 0
candidate_execution_authorized = false
claim_deletion_forbidden = true
builder_invocations_per_governed_attempt = 1
null_reconstruction_generation_count = 0
output_readback_reconstruction_count = 1
```

## Committed-authority binding

The wrapper requires a full `--expected-head` argument only after the future
owner-accepted authority commit exists. It requires actual HEAD equality, empty
Git porcelain, separately true index/worktree-clean facts, and current bytes
equal to every required blob in that commit.

The expected launch commit must contain the authorization freeze, wrapper,
policy, zero-null validation, governance records, immutable machine owner-
acceptance record, a separate 10.4 launch record, and all active I04R2 inputs/
validation. Acceptance binds wrapper, policy, authorization, and the complete
I04R2 hash set while setting owner acceptance and commit authorization true but
null-invocation authority false. Only the separate launch record may set the
latter true. Neither embeds its containing commit hash; the wrapper discovers
and records the exact launch HEAD at invocation time.

The permanent claim is repository-local under the experiment output tree, not
temporary storage. Preflight requires local `ext4`, rejects symlink path
components, and treats any existing directory entry—including an empty,
partial, or broken-symlink claim—as consumed. Atomic creation remains
`O_CREAT|O_EXCL|O_WRONLY`.

The exact interpreter contract is CPython 3.12 through `.venv/bin/python`,
binary SHA-256
`1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118`.
The claim records the resolved executable, binary digest, implementation,
version, exact HEAD, clean-state facts, normalized command, current/committed
authority hashes, policy/wrapper hashes, and unchanged I04R2 hashes.

## Zero-null safety matrix

| Required case | Result |
| --- | --- |
| Concurrent second start | Refused; exclusive claim has one winner |
| Start after claimed attempt | Refused |
| Start after simulated crash following claim | Refused; claim persists without final receipt |
| Dirty authority files or index | Refused |
| Wrong HEAD | Refused |
| Wrong interpreter or normalized command | Refused |
| Existing governed output | Refused |
| Accepted-builder invocation during safety validation | Zero |
| Existing empty, partial, or symlink claim | Refused as consumed |
| Owner acceptance without separate launch authority | Refused |

Two additional tests validate one-attempt/zero-retry plus complete I04R2 hashes,
and the exact final-receipt generation/readback/count shape. All 12/12 pass.

The final receipt contract requires:

```text
governed_attempt_count = 1
accepted_builder_invocation_count = 1
null_invocation_count = 1
null_reconstruction_generation_count = 0
output_readback_reconstruction_count = 1
authorization_consumed = true
second_invocation_refused = true
infrastructure_retries = 0
candidate_execution_authorized = false
```

## Exact correction identities

| Artifact | SHA-256 |
| --- | --- |
| I05B one-shot policy | `822f8b8e61e0de8ad53f8db80ed4fa4c3d8f8bcacf496a205c4f9ccda6d67098` |
| I05B governed wrapper | `c21af416c0ec20e928aa495533c09faffc0beffa144587d4ff4c173955d912f6` |
| I05B owner acceptance | `50b4ab21acb8e6d040639894ec2796e0b6fd92e7f5ddf34a55a1c16441d606c4` |
| I05B safety tests | `425f161ac49d6d143fcfe6b325c35cc81b76e3e8a4d0890b9453f7aae9009a9e` |
| I05B validator | `6f224c484ff6d66ecdd72629f1c1085f666693b5e30c3ed9b5578e090e2a3636` |
| I05B validation | `cbc618b019afcb6ee607810f4eb8dd4c3469a6242ee349b63c6bf660b810038b` |

The policy additionally binds authorization SHA-256
`97a78f7f5e8b1119ec059b82a7a5b6c14c573efc55411ac4392ff6cf2703545a`
and the complete accepted I04R2 identity set. Machine validation independently
compares those current bytes with accepted commit
`b7b008c402d837b529962a1a5edb062927939d28`.

## Review boundary

This accepted package demonstrates mechanics only. It does not create the
separate 10.4 launch record, consume authority, invoke the null, calculate a
delta, freeze a metric sheet, pass CAL-GATE, open I06, or assign scientific
evidence. DEC-029 authorizes its retention commit only; the project owner's
separate direction to proceed to 10.4 is governed there.
