# P2-I2-I03AR1 State-Carried Runtime Conformance

**Status:** `P2-I2-I03AR1-REVIEW-READY`

**Dependence mode:** `state_carried`

**Realization:** `pygrc_native_candidate`

**Evidence class:** quarantined realization implementation-conformance only

**Scientific effect:** none

## Result

The frozen state-carried realization is runtime-conformant on its bounded
synthetic fixture. The governed replacement evidence invocation passed all
136 assertions, and its one authorized reconstruction was byte-identical.

This establishes only that the accepted I03A realization can execute its
declared native causal path and lifecycle boundary. It does not calibrate or
support `AE01-H-L02`, resolve a scientific control, rank the three dependence
modes, or authorize I03B.

## Frozen identities

| Item | SHA-256 |
| --- | --- |
| Immutable base freeze | `d21cc390ab6655ce98c7dbf6827a73d9b3d537c9d90cb98b81f8e2da510a1d94` |
| I03AR1R1 revised freeze | `90929f30de7dec17e812dd98087b1ba8b497445439680fdbe50b2f70d1fa333c` |
| Revised harness | `616fd3b9c6a884ca785f60c075505e808c564f8975e3791fb21241f250024060` |
| Conformance record | `a7601bb1a7d335cfefc9d21aa365e3f5732ae0ebdfabe6bb7d168a7194ed0db0` |
| Admitted graph revision | `83e3a300426631ee4df71b661b67d4fcfdfed594` |

The RCAE `.venv` used CPython 3.12.3 and the graph lockfile's exact direct
dependency versions: matplotlib 3.10.9, networkx 3.6.1, pyvis 0.3.2, and
PyYAML 6.0.3. `pygrc` was imported directly from the admitted checkout's
`src/pygrc/__init__.py`; it was not installed into the environment.

## Conformance observations

| Boundary | Frozen observation | Disposition |
| --- | --- | --- |
| Reference | `P=1.0`, score `0.0`, response subthreshold | Passed |
| S1-only / S2-only | `P=1.25`, score `0.25`, response subthreshold | Passed |
| Combined S1+S2 | `P=1.5`, score `0.5`, native A-to-B response raised `B` from `0.5` to `0.6` | Passed |
| Reversed contribution order | Same P, score, and later response as canonical combined order | Passed |
| Lineage-only permutation | Audit lineage changed; P, score, and later response did not | Passed |
| Native write diversion | Source debits preserved; `P=1.0`, `K=1.0`, response returned to reference | Passed |
| Native carrier debit | Both contributions preserved; native P-to-K debit returned `P=1.0`, response returned to reference | Passed |
| Private competitor | P1 and P2 each reached `1.25`; reads were separate masks `[9]` and `[10]`; no aggregation occurred | Passed |
| Alternate responder | A_alt/B_alt used the same one-node P/B_ref access relation and produced the same response delta | Passed |
| Save/load | Reset-aware identity v2 remained `3cf2a3a2281987279b760f2ce80484b3fbdf06924d81ca12da7beea4ca763bf1` | Passed |
| Equal continuation | Original and loaded instances produced identical response, packets, state, queue, and identity | Passed |
| Reset | Original and loaded instances returned to the same persisted baseline, with `P=1.0`, empty queue, and empty packet ledger | Passed |

The model-owned feedback producer only enqueued native work. Frozen checks
confirmed that it did not directly mutate coherence or write a claim label.
The graph checkout remained clean at the admitted revision, and all ten bound
source digests remained unchanged.

## Native and missing-surface disposition

No RCAE causal producer was needed for the bounded state-carried realization.
All pool writes, diversion/debit transitions, carrier state, feedback read,
response scheduling, response packet processing, persistence, continuation,
and reset were PyGRC-owned. RCAE supplied only fixture construction, role and
access declarations, branch orchestration, matching, and assertions.

This does not erase the generic gaps recorded by I03A. PyGRC still has no
first-class atomic pool-write gate, byte-identical-audit state clamp, or native
private no-common-read role guard. The conformance fixture therefore used
explicit native route diversion/debit while retaining their changed audit
records, and RCAE verified each private mask separately. Those bounded
operations were adequate here; general promotion remains a later cross-
experiment question. History-carried and hybrid adequacy remain wholly
unresolved for I03B and I03C.

## Governed infrastructure correction

The original evidence invocation stopped before writing an output because
the harness compared a derived binary floating-point delta
`0.09999999999999998` to literal `0.1` with strict equality. This was recorded
as `P2-I2-I03AR1R1` / `P2-I2-CHG-010` before correction.

The revised freeze changed only that derived-delta comparator to
`math.isclose(..., abs_tol=1e-12, rel_tol=0)`. It retained all fixture values,
branches, native calls, causal assertions, source identities, run limits, and
quarantine rules. The stopped invocation is permanently classified
`infrastructure_invalid`; it produced no conformance or scientific evidence.

## Reconstruction and gate effect

The retained conformance artifact and the logical temporary-output reconstruction both have SHA-256
`a7601bb1a7d335cfefc9d21aa365e3f5732ae0ebdfabe6bb7d168a7194ed0db0`;
`cmp --silent` returned zero.

I03AR1 is ready for owner review. I03B, I03C, I04, calibration, registration,
candidate execution, and all scientific conclusions remain unauthorized.
