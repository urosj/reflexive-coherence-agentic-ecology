# P2-I2-I08 activation preflight

**Status:** owner-accepted and commit-authorized; execution not started

**Cycle:** `P2-I2-C01`

**Scientific execution:** not started

## Disposition

The owner accepts the exact I08 activation candidate and authorizes its commit
under DEC-049/CHG-045. Candidate-free validation passed 18/18 with zero
blockers. All accepted I07A technical bytes and all 234 matrix entries remain
unchanged.

The reviewed candidate deliberately remained inactive:

```text
owner_acceptance = false
candidate_execution_authorized = false
I08_authorized = false
commit_authorized = false
activation_commit_head = null
```

No matrix command could pass the frozen live validator in that state. The
accepted transition changes only the prereviewed authorization surface; live
use still requires the resulting committed full HEAD.

## Preparation evidence

- Accepted inactive authority commit: `5c2c248647e78526474210649c0a7ba84fcef13d`.
- Cleanup scope: only ignored `__pycache__`, `.pyc`, and `.pyo` artifacts under
  `experiment_scripts` and `pygrc_source`.
- Exact cleanup: 207 inventory items before, zero after.
- Tracked RCAE/PyGRC bytes changed: zero.
- Preactivation validation: 18/18 passed, zero blockers.
- Preparation process: two `.venv/bin/python -B` starts, zero retries.
- PyGRC imports, models/adapters, packets, candidate/control operations, and
  scientific windows: zero.
- Governed C01 output root and execution manifest: absent.

## Bound identities

| Artifact | SHA-256 |
| --- | --- |
| I08 activation input freeze | `931be4ecb70fb1bfa4b4cd10382a98558987a54509f27e809e7722318b5780ef` |
| Import-cache cleanup receipt | `3030cae7af90f0c0eae312b0f54c77238f582e5987af094177aaddb362ae7466` |
| Inactive activation candidate | `52d420b49029e32f007119a3f888ca9fc05ca545a4a75b3e775f8c69c23eac6b` |
| Owner-accepted activation | `f46ebd323499423715107c3b337963c3787404ed257c56be880808617cb09cc3` |
| Preactivation validation | `47e7463b39f057d57140b49c711dc5385e0b7c8bbb7beb17de027d835b473f0f` |

The activation candidate also binds the exact inactive freeze, policy,
execution source, I07A validator/tests, resumption freeze, I07A validation and
input freeze, run matrix, and binding receipt hashes required by the frozen
live validator.

## Required activation transition

Owner acceptance authorizes exactly the following transition before commit:

```text
artifact_version:                  1.0.0-candidate -> 1.0.0
status:                            inactive_candidate_for_owner_review
                                   -> owner_accepted_activation
owner_acceptance:                  false -> true
candidate_execution_authorized:    false -> true
I08_authorized:                    false -> true
commit_authorized:                 false -> true
```

`activation_commit_head` remains null and `expected_head_source` remains the
separately owner-authorized normalized command argument. After that exact
activation package is committed, every entry command must use the resulting
full HEAD. The activation commit itself contains no candidate execution; the
first claim requires exact post-commit preflight.
