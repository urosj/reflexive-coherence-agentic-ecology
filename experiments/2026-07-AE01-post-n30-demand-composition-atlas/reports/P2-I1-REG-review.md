# P2-I1 REG-GATE Review

**Status:** passed

**Gate under review:** `P2-I1-REG-GATE`

**Frozen RCAE source revision:**
`6ca9391fff6daa82e3be4b42c11f431a961d35b8`

**Verified graph source revision:**
`1f42cb1d1e591159afc2ca54cc656b574d41c8d3`

**Evidence effect:** registration only; no candidate execution or lane evidence

## 1. Review target

This bounded review determines whether the L01 probe is registered as one
portable, internally constrained, PyGRC-bound candidate cycle without turning
registration facts into niche-conditioning evidence. It is the only REG-GATE
review required unless owner review identifies a concrete defect or an
unrecorded assumption.

Controlling retained artifacts:

- [registration policy](../configs/p2_i1_registration_policy.json)
- [registration profile registry](../configs/p2_i1_registration_profiles.json)
- [realization profile](../contracts/p2-i1/registration-realization-profile.json)
- [registration records](../contracts/p2-i1/registration-records/)
- [inherited verification](../contracts/p2-i1/inherited-control-verification.json)
- [runtime binding receipt](../contracts/p2-i1/registration-runtime-binding-receipt.json)
- [baseline identity registry](../contracts/p2-i1/baseline-identity-registry.json)
- [registration freeze](../contracts/p2-i1/registration-freeze.json)
- [registration manifest](../contracts/p2-i1/registration-manifest.json)
- [P2-I1 checklist](../implementation/P2-I1-minimal-shared-medium-niche-checklist.md)

## 2. Required review questions

1. Were all retained generated artifacts built from the clean source anchor,
   with preview artifacts mechanically excluded from retention?
2. Do calibration and registration measurement/realization identities match
   exactly, without silently reopening CAL-PRE or CAL?
3. Does the runtime receipt bind `pygrc==0.1` and all seven abstract operation
   classes to concrete callable PyGRC methods without recording a machine-local
   checkout or installation path?
4. Does the baseline registry retain all `7 cells x 3 seeds = 21` exact W0
   configurations, one fresh worker per entry, empty queue/surface state, and
   the intended geometric distinctions?
5. Are the five inherited N29/N30 sources digest-verified, read-only,
   non-identical in carrier/mechanism/intervention/claim scope, and prohibited
   from substituting for fresh L01 causal evidence?
6. Does every registration-time resolved control leg require its exact evidence
   bindings, while causal and terminal legs remain pending execution?
7. Are all selected files portable, digest-resolved, and exactly
   reconstructable under the declared command profiles?
8. Are candidate execution, positive and negative lane evidence, native niche
   claims, rung assignment, and terminal classification still closed?

## 3. Reproduction

From the repository root at the frozen RCAE source revision, use a local
environment containing the pinned repository dependencies and `pygrc==0.1`.
Supply the graph checkout through the local-only `LOCAL_GRAPH_CHECKOUT`
argument; never record its path in a shared artifact.

Run the five commands documented in the
[registration tooling instructions](../scripts/README.md), in this order:

```text
build-inherited-verification
build-runtime-receipt
build-baseline-registry
build-registration-freeze
build-registration-manifest
```

Then run:

```text
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/ae01.py validate-phase1
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1.py validate-configs
.venv/bin/python experiments/2026-07-AE01-post-n30-demand-composition-atlas/scripts/p2_i1_registration.py validate-policy
.venv/bin/python -m unittest discover -s experiments/2026-07-AE01-post-n30-demand-composition-atlas/implementation/tests -q
```

The freeze intentionally includes portable paths in its bundle-file records.
An alternate-output-directory reconstruction therefore reproduces the three
direct artifacts exactly but produces a different, correctly path-sensitive
freeze. Exact freeze and manifest reconstruction requires regenerating them at
their declared experiment-relative paths. This same-target regeneration was
performed after preserving the originals and reproduced both files byte for
byte.

## 4. Reconstruction findings

```text
validate-phase1 = passed
validate-configs = passed
registration-policy validation = passed
unit tests = 75 passed
direct artifact reconstruction = 3/3 exact
same-target derived reconstruction = freeze and manifest exact
machine-local path scan = passed
graph worktree before/after = clean
```

Retained digests:

| Artifact | Embedded canonical payload | Semantic-file digest | Exact-file SHA-256 |
| --- | --- | --- | --- |
| Inherited verification | `a0813aef3dd7ecd05adf37410732ec1100100e80174efbb1a731f88998fe2d6d` | `b57b6479df2e5128c17dffda60a7537385738a8bffdc3c6c9d5c1ffd3dbdaecb` | `4d291253167dd571d7337793081369907c3980366a19b07e08741b29ddd17e7d` |
| Runtime binding receipt | Not embedded; schema receipt uses `receipt_id` | `eac44b2d40f30dbaba44d2a46989ebff94fe7c9d6f263db269cc0947a4a3794c` | `823dd0c4e17fa4c05e257fffb3cf454674433fc1c1ae98ad8ac8a2cf79cfc32a` |
| Baseline registry | `a2fbd2b8ac86cc349e693b1665a420c39d8545fdac7dde540d97f8436f37464f` | `e412fb45b36dd074ac556381100490a4210b24080946593274147740e20d28cd` | `b886ee3a1f27ef08e75ca375470cab9eceddbfa9bc5d31afcd4c50a6aac83ac4` |
| Registration freeze | `1453eea6d096e8fb8eaf53960614440aebd9db0b8ab1b0b50e0387dad6aa5658` | `50de49e01008f5ca3949d62283701b0e59eeac5079466c15fa54b09f6a17644b` | `5b3bc38d85190e753f4acedf2510132f6d13fca404834588e11b566a58ecb593` |
| Registration manifest | Not embedded; schema manifest uses `manifest_id` | `47696658c79ddf4e942595b393601efd411c6fa4bbc7fcde55c06f2b8b662832` | `a091d71908e152e1e5ac9c89cd68c089ee978db26342c39e60bebda3bc493c47` |

The manifest resolves `15` selected artifacts totaling `139881` bytes. The
freeze digests `32` bundle files. Both imported identity comparisons are true:

```text
measurement identity = 853c5f10d33a1820b72cc3245e0612ff9024a7ae920833d44e81fcc22a7f2e5a
realization identity = 9b59988a0f5211cb32aaf531748f8a9b235540729d40544373e6ba3a04b769b8
```

The freeze's `reg_gate_disposition=pending_review_and_manifest` is a
pre-manifest boundary fact, not the current administrative gate status. The
manifest must be generated after the freeze to avoid a recursive digest, and
this review records the later gate disposition without rewriting the frozen
machine record.

## 5. Geometric and ecological interpretation

The retained W0 registry contains `21` unique composite identities, `6` native
snapshot identities, and one route-aspect identity. Every entry has the empty
queue and empty focal-surface digest. This verifies exact initial geometry and
fresh-worker construction, including the reduced-support contrast, without
preinstalling a medium row or candidate outcome.

The receipt verifies that the registered native operation family is callable;
it does not verify a writer-to-medium-to-reader causal sequence. The inherited
verification confirms five exact N29/N30 sources and keeps every source below
identical-scope inheritance. Together these artifacts register the proposed
participant, medium candidate, history relation, selectivity discriminator,
and claim ceiling while preserving the need for fresh execution.

The derived lifecycle contains `24` controls, `13` resolved registration legs,
`7` fully resolved registration controls, `16` pending-execution controls, one
accepted not-applicable control, and zero blocked legs. Pending execution is
not treated as passing, failing, or evidence absence.

## 6. Open execution questions

The following questions remain deliberately unresolved because REG-GATE
registers how to test them rather than answering them:

- whether written medium state can be reconstructed independently of the
  participant label;
- whether medium ablation differs from participant/private-state effects;
- whether later branches restore exactly and receive comparable exposure;
- whether support/budget matching and zero carryover hold during live runs;
- whether the result is selective, generic, producer-carried, missing-surface,
  redirected, or genuinely niche-conditioning.

None blocks registration because each has an explicit pending-execution leg,
expected artifact role, and claim boundary. No concrete representation
friction currently requires first-class `lane_registration` or
`control_outcome` schema records; that R3 question remains deferred.

## 7. Allowed dispositions

```text
pass
revise_before_execution_freeze
blocked_missing_registration_evidence
```

A pass closes registration only. It does not authorize candidate execution.
The exact candidate cycle must still be materialized and accepted through
`P2-I1-EXEC-FREEZE` before its first operation.

## 8. Disposition

The retained bundle is explicit, internally consistent, portable,
source-anchored, candidate-free, and exactly reconstructable. No concrete
registration blocker was found.

Owner disposition on 2026-07-11 accepted the unresolved independent-medium,
ablation, branch-restoration, exposure-comparability, support/budget, and
carryover questions as live-execution obligations. They remain mandatory and
unchecked; they do not convert absent candidate outcomes into a registration
blocker.

```text
P2-I1-REG-GATE = passed
```

This opens `P2-I1-EXEC-FREEZE` work only. Candidate execution remains closed
until one exact cycle-scoped authorization is retained.
