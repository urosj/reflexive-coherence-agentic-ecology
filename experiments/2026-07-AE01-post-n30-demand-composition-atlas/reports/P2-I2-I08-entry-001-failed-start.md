# P2-I2-I08 entry 001 failed-start review

**Status:** C01 bounded incomplete; I08A/C02 construction authorized

**Cycle:** `P2-I2-C01`

**Scientific result:** none

## Disposition

The exact post-commit preflight passed at full HEAD `c265279`. Sequence entry 1
then created its permanent attempt-1 claim and terminated during the common
runtime import path with:

```text
OpenBLAS error: Memory allocation still failed after 10 retries, giving up.
```

The process emitted neither its governed success output nor its required
failure receipt. Attempt 1 is consumed. Attempt 2 is not authorized because the
frozen retry predicate requires the exact attempt-1 failure receipt and its
zero-state counters.

```text
claimed entries:       1
evaluable entries:     0
unattempted entries:   233
eligible retries:      0
scientific results:    0
```

## Bounded diagnosis

The runner applies a 512 MiB `RLIMIT_AS` ceiling before importing the I06
registration/PyGRC stack. The observed native OpenBLAS termination occurs in
that shared import path, before the Python runner can establish or serialize
its model/candidate counters. This identifies two coupled infrastructure
problems:

- the address-space ceiling is not compatible with the native numerical import
  path in this environment; and
- the in-process exception handler cannot retain a receipt for native process
  termination.

That phase diagnosis is not a substitute failure receipt and cannot authorize
a retry.

## Boundary

No later C01 entry was claimed. Repeating the unchanged common import path
would risk stranding additional permanent claims without producing additional
scientific evidence.

The owner states that a 512 MiB space limit is unnecessary on the 128 GB host.
C01 is therefore retained as historical bounded incomplete, and I08A may
construct C02 without applying `RLIMIT_AS`. C02 must add an external per-entry
supervisor receipt boundary so native termination cannot strand another claim
without evidence. Runtime and file-size ceilings, the scientific matrix, and
every registered value remain unchanged. Construction and candidate-free
validation do not themselves authorize C02 execution or commit.
