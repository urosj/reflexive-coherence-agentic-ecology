# P2-I2-I06B Execution-Readiness Registration Correction

**Status:** explicitly owner-accepted; 15/15 candidate-free checks pass with
zero blockers. The package remains uncommitted, REG-GATE is restored, and the
existing I07 freeze resumes candidate-free. EXEC-FREEZE and candidate execution
remain unauthorized.

## Purpose and authority

The I07 authority audit correctly stopped before runner construction because
accepted I06/I06A did not freeze three exact execution primitives. The owner
authorized DEC-043's bounded I06B recommendation with `+1`. I06B therefore
adds one overlay and does not modify or reinterpret any accepted I06/I06A byte.

The correction ceiling is exactly:

1. native P-debit timing after history materialization and before neutral
   contact;
2. full reference-P debit identity; and
3. exact native calls for the already registered direct-address and
   controller-assembled diagnostic bypasses.

No fourth primitive, scientific value, mode, cell, comparator, seed, or
candidate-cycle source is admitted.

## Exact correction

The matched schedule retains contribution slots 0/1 and history materialization
slot 2, reserves native-intervention slot 3, and moves neutral contact to slot
4. Contribution spacing and arrival offset are unchanged. Neutral arrival moves
from `14.625` to `15.875`; response arrival moves from `15.625` to `16.875`,
preserving the exact `1.0` neutral-arrival-to-response-arrival lag. Unused
materialization/intervention slots receive explicit no-op dispositions, so
branches retain identical absolute opportunities without scheduling fake work.

The exact full reference-P debit is:

```text
q1 + q2 = 0.625 + 0.875 = 1.5
candidate P = 0.75 + 1.5 = 2.25
post-debit P = 2.25 - 1.5 = 0.75
```

It is distinct from the accepted `0.4375` diagnostic P debit. Both use the
public native `P_TO_K_P` packet route at the reserved intervention slot. The
overlay maps all five applicable mode/subconfiguration pairs exactly and makes
every other pair an explicit slot-3 no-op.

The direct-address bypass now calls the public feedback-surface method over
front mask `[S1, S2]` and rear mask `[B_REF]`, then uses the existing native
feedback producer with the registered mode threshold, reference delta, packet
amount, and corrected response arrival. It is contributor-addressed by design
and remains outside the candidate causal chain.

The controller bypass derives its boolean only from exact retained q1/q2
arrival receipts, reads no P, M_H, active history, or native feedback surface,
and directly calls public `schedule_packet_departure` on `A_PRIMARY_TO_B` only
when the receipt predicate is true. Its source, target, amount, departure,
arrival, scheduler, and packet-index rule are frozen to match the native
response opportunity. Its authored aggregation remains a diagnostic causal
exclusion, never candidate evidence.

## Native-first disposition

No new RCAE causal producer is needed. Public PyGRC packet scheduling is
adequate for both P debits and the controller diagnostic, while the public
feedback-surface and native feedback-producer path is adequate for the
direct-address diagnostic. The prior absence was exact experiment registration,
not missing PyGRC machinery.

## Validation

The single authorized `.venv` validation start passed 15/15:

- all nine accepted I06/I06A authority inputs reconstruct byte-exactly;
- both blocked I07 drafts reconstruct and remain non-authoritative;
- the graph checkout is clean at admitted revision
  `83e3a300426631ee4df71b661b67d4fcfdfed594`;
- the source-current runtime hash and all three public method signatures match;
- the freeze, overlay, and validator reconstruct through the manifest;
- overlay precedence, schedule arithmetic, both debit identities, branch
  applicability, topology, bypass calls, inherited mode/cell/control/seed
  identities, bounds, restoration duties, portability, and gate closure pass;
- canonical output reconstruction and retained readback are byte-identical.

Process accounting is one output-producing validation start, zero retries, two
read-only source-control subprocesses, and zero PyGRC imports, models, packet
operations, candidate operations, control operations, response evaluations, or
comparator/scientific windows.

## Retained package

- [input freeze](../contracts/p2-i2/i06b-execution-readiness-correction-input-freeze.json),
  SHA-256 `4ada5141c550d478ee36d8a3be069bcbb0a040bddff235ad65bd707e74fc685c`;
- [additive overlay](../contracts/p2-i2/i06b-execution-readiness-overlay.json),
  SHA-256 `72d70a4c3e2a8b1dd8186a0b4de74a2212d33956c1e89f5d35bccc9f42e05694`;
- [manifest](../contracts/p2-i2/i06b-execution-readiness-manifest.json),
  SHA-256 `9bf6bf64d2072cb96b0ea2bb9fb58fc169bd821480b1a10a06c07e3979379323`;
- [validator](../scripts/p2_i2_i06b_validate.py), SHA-256
  `ae0b5d3b52b1f66749031d5f49fe61e4f7ee23f24da04ba1a590e275799b670c`;
- [15/15 validation](../contracts/p2-i2/i06b-execution-readiness-validation.json),
  SHA-256 `2bbffec5c72d78f565ac9830ed2b236bb934aa76042d7f8d67911681ac261857`.

## Disposition

```text
three missing primitives:             frozen
accepted I06/I06A byte changes:       0
candidate-free validation:            15/15 passed
remaining I06B correctness blockers:  0
scientific evidence:                  none
package acceptance:                   explicit owner acceptance
commit authority:                     absent
REG-GATE:                              passed
I07:                                   resumed candidate-free
EXEC-FREEZE:                           closed
I08/candidate execution:              unauthorized
```

The owner explicitly accepts I06B, restoring REG-GATE and authorizing resumption
of I07 from its retained blocked audit. Acceptance does not accept an I07 cycle,
pass EXEC-FREEZE, authorize a commit, or authorize any live run.
