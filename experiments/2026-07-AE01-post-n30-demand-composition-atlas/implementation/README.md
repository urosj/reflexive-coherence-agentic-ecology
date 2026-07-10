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
IDs, finite comparison groups, terminal rules, lane boundary ladders,
threshold interpretation, and a bounded P1-I5 handoff.

P1-I5 implements the minimum experiment infrastructure in the
[artifact, tooling, and reconstruction contract](P1-I5-tooling-contract.md).
It materializes finite comparison matrices, validates the P1-I3/P1-I4
contracts, produces reproducible manifests and bounded reports, and enforces
runtime/read-only boundaries. Revision 0.24 also implements first-class metric
sheets, candidate-blind resolution calibration, machine-derived threshold
relations, developmental-interpretation validation, and guarded next moves.

Phase 2 lane-specific directives begin with the
[P2-I1 minimal shared-medium niche formation brief](P2-I1-minimal-shared-medium-niche-brief.md).
It defines L01's theoretical, geometric, ecological, anti-subsumption,
observation, decision-timing, and registration boundaries without answering
the experiment in advance or changing the frozen hypothesis.

The corresponding
[P2-I1 detailed checklist](P2-I1-minimal-shared-medium-niche-checklist.md)
is the living execution surface. It may expand from evidence between probe
cycles, remains frozen within a cycle, preserves prior results, and feeds only
stable cover gates back to the master checklist. Its calibration
preregistration gate freezes response, orientation, opportunity, normalization,
window, matched-null, calibration-realization, analysis, and selectivity-policy
identities before any resolution margins are generated.

The implementation remains experiment-local under `scripts/`; it is not an
installable distribution, reusable ecology source surface, admitted mechanism,
or lane result.
