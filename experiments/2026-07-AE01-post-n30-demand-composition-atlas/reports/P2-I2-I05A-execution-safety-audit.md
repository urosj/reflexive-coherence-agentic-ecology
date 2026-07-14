# P2-I2 I05A Execution-Safety Audit

## Disposition

The I05 authorization candidate is not ready for owner acceptance. Static,
zero-execution audit passed 3/8 checks and found five execution-safety
blockers. The scientific measurement design remains unchanged; the blockers
are one-shot authority and provenance mechanics.

No null, PyGRC model, candidate, control, or reconstruction generation ran.
The governed output remains absent, the authorization candidate remains
uncommitted and inactive, and CAL-GATE remains closed.

## Findings

| Check | Result | Finding |
| --- | --- | --- |
| Attempt-time consumption | Failed | The entry point validates reusable authorization JSON but creates no consumed-attempt marker before calling the builder. A crash leaves the same permission reusable. |
| Concurrent-start exclusion | Failed | Output absence is checked non-atomically before work. No exclusive claim or lock prevents two processes from starting. |
| Failure/retry semantics | Failed | Policy contains `max_governed_invocations=1` and `max_infrastructure_retries=1`, but there is no attempt token distinguishing the governed attempt from a retry. |
| Committed-I05 binding | Failed | Preflight binds accepted I04 commit `b7b008c`, not a future commit containing accepted I05 authority. It does not validate the exact launch command/interpreter or a clean RCAE authority worktree immediately before execution. |
| Existing identity/output/candidate guards | Passed | The entry point validates the five I04R2 identities, refuses an existing output, and keeps candidate authority false. |
| Readback-only reconstruction | Passed | Within the current invocation, the builder is called once, output is written once, then read/parsed/reserialized once. No second envelope generation occurs. |
| Retained counts/refusal witness | Failed | No machine receipt retains invocation/reconstruction counts, consumed status, or a refused second start. |
| Zero-execution audit boundary | Passed | Audit parsed source/contracts only and created no governed output. |

Machine audit SHA-256:
`cb0c2f6275febdcbe92e8b64cd6ac2bba71531e4ecdee3812811c4d8347e4ed8`.
The result binds audit-validator SHA-256
`8fc8155ba914150f926813038c5e92b761c9ff546fde07e0e86d0decfd745fd7`.
Its reconstruction is byte-identical.

## Important partial satisfaction

The current reconstruction code does not rerun the null builder. That part of
the review is sound. The missing part is a retained post-attempt receipt that
separates generation from readback and proves the authorization was consumed
and a second start was refused.

## Bounded correction scope for owner consideration

A correction can preserve the accepted I04R2 bytes by adding an I05-owned
governed wrapper and companion one-shot policy rather than editing the accepted
I04R2 estimator module. The correction would need to:

1. Atomically create an exclusive attempt/consumption receipt before any null
   generation. The marker must survive failure and reject concurrent/later
   starts.
2. Resolve the current committed RCAE revision at invocation time, prove that
   it contains the owner-accepted I05 freeze and unchanged I04R2 blobs, require
   clean authority files/index, and bind the exact interpreter and normalized
   command in the attempt receipt. This avoids an impossible self-referential
   commit hash inside a file belonging to that same commit.
3. Make retry semantics explicit. The narrowest implementation sets governed
   attempts to one and infrastructure retries to zero; any different retry
   allowance requires its own frozen token policy.
4. Call the accepted I04R2 builder path once, then perform reconstruction only
   from the retained output and retain these derived facts:

   ```text
   null_invocation_count = 1
   null_reconstruction_generation_count = 0
   output_readback/reconstruction_count = 1
   authorization_consumed = true
   second_invocation_refused = true
   ```

5. Bind the new I05 wrapper/policy/receipt identities alongside—not by
   rewriting—the accepted I04R2 identities.

This audit authorizes no correction, acceptance, commit, or execution. Proposed
DEC-027 fails closed pending owner direction.
