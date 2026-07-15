# P2-I2 APP-B2 Runtime Result

**Status:** technically complete and closeout-validated; owner result review
pending; uncommitted

## Result

Appendix B supports the bounded three-operation composition claim in the
history-carried realization only.

```text
state_carried:   not supported in the frozen realization
history_carried: supported bounded composition
hybrid:          not supported in the frozen realization

terminal = supported_bounded_candidate
bounded claim = bounded P2-I2-grounded three-operation shared-pool
                composition candidate
```

This result comes from 99 newly executed fresh-process PyGRC models. It is not
an analysis of earlier P2-I2 or Appendix A simulations.

## Primary responses

Each mode used three seeds and the same eight-row proper-subset matrix. Results
were identical across the three frozen seeds:

| Mode | GEP response | Strongest proper subset | Proper-subset response | Normalized margin | Disposition |
| --- | ---: | --- | ---: | ---: | --- |
| state carried | 0 | GP | 0.125 | -1 | fails |
| history carried | 0.125 | reference (all proper subsets tie at zero) | 0 | 1 | passes |
| hybrid | 0.125 | P (P and GP tie) | 0.125 | 0 | fails |

In history-carried mode, `GEP` produces one native B response packet while
`reference`, `G`, `E`, `P`, `GE`, `GP`, and `EP` all produce valid scientific
zeros. Removing any operation changes the response. History clamp changes the
response; state-only C intervention does not; and equal final C with different
ordered history changes the response. Private partitions do not reproduce the
effect, while the controller-authored response is explicitly excluded.

State-carried mode fails because current P alone makes `GP` stronger than
`GEP`; the extraction operation suppresses rather than completes the response.
Hybrid mode reaches the response for `GEP`, but `P` and `GP` already reach the
same response, so E is not necessary and irreducibility fails. Its frozen C x
H discriminator nevertheless behaves as registered; this does not rescue the
primary proper-subset failure.

## Participant and implementation scope

One-source lineage, both cyclic lineage rotations, and label permutation
reproduce the history result. Thus participant-lineage plurality is not
load-bearing in this fixture; the physical G/E/P operation types are. The
operation reservoirs remain the fixed accepted P2-I2 reservoirs, so this does
not establish participant complementarity or cooperation.

History remains minimally producer-assisted: an external accepted-role adapter
owns ordered source-label-free H_C admission, while PyGRC owns every coherence
transition, M_H materialization packet, feedback evaluation, producer decision,
and B response packet. A fully native-history claim remains blocked.

## Runtime and reconstruction

```text
fresh replacement child processes/models = 99/99
child failures/retries = 0/0
operation packets = 297
history-materialization packets = 55
state-intervention packets = 6
neutral packets = 99
response packets = 27 (including 3 excluded controller controls)
total native packets = 484
native packet departure/arrival events = 968
final active-history tokens = 111
save/load/reset identity receipts = 99/99
unique child PIDs = 99
graph mutations = 0
```

The original reconstructor reproduced the aggregate's embedded analysis
byte-identically, but that embedded analysis was correctly withheld because
its operational validator was fail-open. The additive retained-only correction
uses native step-bookkeeping event identities and the frozen operation
route/amount registry. It changes no runtime byte, response, estimator value,
or control value. Corrected closeout validation confirms 99/99 valid arms and
reconstructs the history-only supported disposition with zero PyGRC, model,
producer, arm, or response regeneration.

## Claim boundary

The supported statement is fixture-, mode-, threshold-, and response-window-
bounded. It does not establish cross-appendix recurrence, generic participant
ecology, participant complementarity, cooperation, coalition, a fully native
history mechanism, unbounded irreducibility, or a revision of the accepted
main P2-I2 conclusion. Result acceptance and a result commit require owner
direction.
