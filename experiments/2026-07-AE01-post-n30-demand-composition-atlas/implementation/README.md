# AE01 Implementation Records

This directory owns AE01-specific implementation plans, checklists, and
handoffs. It does not contain canonical project architecture, experiment
evidence, or admitted reusable source.

Phase 1 may introduce only the tooling and experiment-local mechanisms required
by frozen contracts. Any constructed mechanism must declare its necessity,
minimality, counterfactual, withdrawal test, debt, claim ceiling, and proposed
graph-side discriminator. Placement here does not imply admission or LGRC
nativity.

P1-I4 now supplies the implementation semantics through the
[hypothesis index](../hypotheses/README.md): stable hypothesis/control/failure
IDs, finite comparison groups, terminal rules, and a bounded P1-I5 handoff.

P1-I5 is the next implementation iteration. It may add only the minimum
experiment infrastructure needed to materialize finite comparison matrices,
validate the P1-I3/P1-I4 contracts, produce reproducible manifests and reports,
and enforce runtime/read-only boundaries. No AE01 executable surface exists
yet.
