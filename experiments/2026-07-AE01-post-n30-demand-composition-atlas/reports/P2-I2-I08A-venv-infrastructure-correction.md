# P2-I2-I08A Repository-Venv Infrastructure Correction

**Status:** candidate-free correction passed; exact commit and attempt-2
preflight remain before the authorized same-entry retry

## Disposition

C02 entry-001 attempt 1 is retained as an attested, pre-model infrastructure
failure. Its claim and failure receipt are immutable, its success output is
absent, every construction/candidate counter is zero, and the frozen retry
predicate is true.

The cause was a nested-process regression: the active repository-venv command
was resolved before child launch, so the worker entered the host interpreter
environment. The required dependency was already installed in `.venv`.

CHG-050 corrects this inside existing I08A/I08 and C02. It creates no I08B or
new cycle and changes no scientific row, value, response, estimator, control,
or evidence rule. Governed Python launches now preserve lexical
`.venv/bin/python`; the resolved target remains binary-digest identity only.

## Candidate-free evidence

| Surface | Result |
| --- | --- |
| Focused tests | 8/8 passed |
| Child command identity | Exact repository `.venv/bin/python` |
| Child venv identity | Repository venv prefix active |
| Child dependency check | `matplotlib==3.10.9` imported |
| P2-I2 resolved-host command launch sites | 3 before; 0 after |
| Final validation | 18/18 passed; zero blockers |
| PyGRC/model/candidate/control/scientific operations | 0 |
| Infrastructure retries during correction | 0 |
| Scientific projection changes | 0 of 234 rows |

## Live boundary

The correction package must be committed together with the permanent attempt-1
claim/failure and exact updated authority. A clean post-commit attempt-2
preflight must then bind that full HEAD. Only the already-frozen same-entry
attempt 2 is authorized; entry 2 and manifest construction remain closed.
