# P2-I2 I07A Cross-Entry-Isolation Correction

**Iteration:** `P2-I2-I07A`

**Cycle:** `P2-I2-C01`

**Status:** owner-accepted, candidate-free, inactive, commit-authorized

**Gate under review:** `P2-I2-EXEC-FREEZE`

## Outcome

I07A closes all four CHG-041 cross-entry-isolation blockers without changing a
scientific matrix row or any accepted measurement, calibration, registration,
mode, branch, seed, value, or resource semantic.

The corrected package passes 15/15 focused tests and 17/17 final candidate-free
checks with zero blockers. Its three authorized `.venv/bin/python -B` starts
were exactly: derived refresh, focused tests, and final validation. There were
no failed starts or retries and zero PyGRC imports, models, adapters, packets,
candidate/control operations, response evaluations, or scientific windows.

## Four corrections

### 1. Physical artifact containment

Claims, outputs, and failure receipts now use normalized repository-relative
paths beneath the exact C01 output root. Every parent component is traversed by
directory descriptor with `O_DIRECTORY|O_NOFOLLOW`; every leaf uses
`O_NOFOLLOW`, and writes remain atomic `O_CREAT|O_EXCL`. Claim, output, and
failure leaves must all be absent before the permanent claim is created.

The complete 234-row matrix derives 1,404 distinct governed paths. Tests prove
that `..`, a symlink parent, and a second occupied claim fail closed without an
outside write.

### 2. Import-cache isolation

The frozen live command is now `.venv/bin/python -B`. Before any local
registration/PyGRC import, and again after execution, the runner scans only the
two exact import roots and rejects `__pycache__`, `.pyc`, `.pyo`, or symlinked
import-directory state. The exact interpreter digest remains bound.

Ignored caches left by earlier candidate-free development may still exist in
the working directories, but this is safe state: a live entry must refuse
before its claim until those caches are deliberately removed. With `-B`, a
clean import-root boundary remains clean across all later entry processes.

### 3. Current-entry-only retry reconstruction

The shared retry ledger is removed. Owner activation conditionally authorizes
attempt 2 only when the runner reads the same frozen row's exact unique
attempt-1 claim and failure receipt, verifies their hashes/HEAD/command/freeze,
confirms primary-output absence, and reconstructs all pre-construction zero-
state counters. Another entry's receipt fails identity validation and no other
entry path is opened.

The same committed HEAD is therefore retained without requiring a contradictory
post-failure ledger commit. Scientific/control outcomes cannot authorize a
retry, and the ceiling remains one conditional retry per entry.

### 4. Fail-closed matrix completion

The future `build-execution-manifest` command enumerates all 234 exact frozen
rows and their exact artifact paths; it never scans a result directory. Each
row must have exactly one claimed primary or eligible-retry terminal output,
with matching identity/HEAD, a valid response window, `operational_null=false`,
and a finite numeric raw response.

Any missing, dual, malformed, failed, or operationally-null row raises before
the execution manifest is written. Tests cover complete success and missing,
null, and duplicate failure states. An incomplete earlier entry still does not
alter later primary authorization, but it now necessarily prevents cycle
completion.

## Identity preservation

The additive [I07A input freeze](../contracts/p2-i2/c01/i07a-cross-entry-isolation-input-freeze.json)
retains every reviewed I07 hash. The [derived refresh receipt](../contracts/p2-i2/c01/i07a-derived-refresh-receipt.json)
confirms all 234 entry objects are byte-semantically unchanged and the
conditional-retry ceiling remains 234.

| Corrected artifact | SHA-256 |
| --- | --- |
| Effective policy | `773b9fc231942f59e7d5b74a49ad8ce722471badcc554afd74d5cfaadb4327d3` |
| Execution source | `9a92d90997ba80a0ae626fcfe3549fb77a49c108b9c4e84149aecf35fb1336fe` |
| Focused tests | `22df990af1d4d45729263e5740cc41b2990819fab8e3d64a2ed138eb19846420` |
| I07A validator | `e304b542a2e4d0b350c3605e376caaad306e7dfa878f65b97eaf8379cb54a162` |
| Run matrix | `5e9130bddb3fc888a8376100dcfccc4984a4435310cd0432e5096d29629cd427` |
| Execution binding | `99a474836b25014b31a887861c065e568a91d5ad2a0a58338cffc14aceb64479` |
| Inactive EXEC-FREEZE | `8e4533d37f3de3140dca84aaf3683989988d25a79fcc4aff4e88ca686a90ab22` |
| Focused-test receipt | `c59f96399569fcb8186bb74953e5f7b7809ab49a0dddf844c99eac0f262e4da6` |
| Derived refresh receipt | `17fa02851499cfaadb2837e933ca3bd1bd2f6f8e7406da28bc47724b0948d227` |
| Final I07A validation | `32f69dadc8cd10db3bb57fa7f837be921f91da2315369b2842e37d2737d9997c` |

## Gate disposition

```text
I07A focused tests:             15/15
I07A candidate-free checks:     17/17
remaining technical blockers:  0
matrix rows changed:            0/234
candidate execution performed:  false
candidate execution authorized: false
EXEC-FREEZE:                    passed for exact inactive I07A cycle
I08 authorized:                 false
commit authorized:              true
scientific evidence:            none
```

The owner accepts the package and authorizes its checkpoint commit under
[DEC-047/CHG-043 acceptance](../contracts/p2-i2/c01/i07a-owner-acceptance-and-exec-freeze.json).
Live I08 activation remains separate and must first satisfy the cache-free
preclaim boundary.
