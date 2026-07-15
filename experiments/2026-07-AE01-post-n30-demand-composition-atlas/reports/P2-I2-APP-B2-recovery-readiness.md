# P2-I2 APP-B2 Recovery Readiness

**Status:** owner-authorized infrastructure correction passes candidate-free
validation; replacement campaign not yet started

The original claim and failed-start artifacts remain unchanged and permanent.
The recovery uses distinct replacement claim, runtime-output, and
reconstruction paths.

The runner now launches every scientific child lexically as:

```text
.venv/bin/python -B <runner> --worker ...
```

It does not resolve the launcher. Each worker verifies both its repository
venv prefix and lexical executable before `execute_arm` can import PyGRC or
construct a model.

Nonzero and malformed child results now become aggregate failure receipts with
arm identity, row digest, exit code, stdout/stderr digests, line counts, and a
path-free diagnostic class. The cumulative aggregate is atomically retained
after every child before the loop advances. Failures do not suppress later
frozen rows, and no row receives a retry.

Candidate-free validation confirms that all ten scientific runtime functions
are AST-identical to authority commit `40fd9be`. Operations, values, schedules,
thresholds, modes, arms, controls, estimator, response, and claim ceiling are
unchanged. One live model-free child probe confirms that lexical
`.venv/bin/python` activates the repository venv with `-B` before any campaign
claim exists.

```text
recovery validator starts = 4
validator-only live venv probes = 3
PyGRC imports = 0
models = 0
candidate/control arms = 0/0
response calls = 0
replacement claims = 0
replacement outputs = 0
final validation = 12 grouped checks passed
```

One clean-HEAD correction commit is necessary before the replacement preflight
can consume its sole claim. Result acceptance and result commit remain closed.
