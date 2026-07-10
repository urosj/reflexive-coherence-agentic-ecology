# AE01 Cross-Lane and Non-Selection Hypotheses

**Status:** frozen at P1-I4

**Hypothesis-set version:** `1.0.0`

**Evidence effect:** synthesis and ranking have not run

## 1. Synthesis entry boundary

These hypotheses may be evaluated only after all seven lane terminal records
exist. A complete negative or blocked lane remains an input. An incomplete lane
forces N31+ non-selection and prevents a complete recurrence claim, but its
missing information remains visible.

Candidate names, conceptual enthusiasm, inherited N31/N32 ordering, and shared
implementation code do not establish recurrence.

## 2. `AE01-H-S01` — Recurring operational requirement

**Hypothesis:** after independent lane classification, at least one normalized
primitive or building-block requirement will recur across two or more lanes as
the same operational causal demand, composition bottleneck, or controlled
missing-surface tension.

Two rows are the same requirement only when they share:

- the requested operational distinction and catalog layer;
- compatible input/output and state-handoff meaning;
- the same causal role rather than merely similar ecology vocabulary;
- compatible counterfactual and future graph discriminator;
- independent lane evidence lineage; and
- compatible claim ceilings and debt path.

### Required synthesis comparisons

- lane-to-requirement incidence matrix over all seven terminal records;
- alias/synonym normalization with original lane wording retained;
- source-lineage and shared-fixture dependency check;
- constructed-mechanism reuse check;
- prerequisite and composition-dependency graph; and
- leave-one-lane-out recurrence sensitivity.

### Support signature

`AE01-H-S01` is supported when one normalized requirement is independently
required by at least two complete lanes and survives alias, shared-source,
shared-construction, and fixture controls. Leave-one-lane-out sensitivity is
reported as robustness information rather than used to erase valid two-lane
recurrence.

Support records recurrence count and affected lanes but does not assign a high
D-029 score automatically. Four or more independent lanes is the fixed score-3
anchor for cross-lane recurrence; two-lane recurrence merely supports the
existence of a recurring demand.

### Negative, partial, blocked, and incomplete outcomes

- `not_supported`: every normalized requirement occurs in only one independent
  lane after controls.
- `partial_or_mixed`: apparent recurrence depends on shared wording, one reused
  construction, one fixture, or an unresolved alias; record the cluster but do
  not count it as independent recurrence.
- `blocked_missing_prerequisite`: all lane records are complete, but required
  interfaces or source lineage are too underspecified to decide whether rows
  are the same requirement.
- `incomplete_execution`: at least one required lane terminal record or the
  synthesis reconstruction is incomplete. Descriptive counts may be retained,
  but the full hypothesis is not supported or refuted.

### Fail-closed controls

- `AE01-S01-CTRL-01`: do not count conceptual-source repetition;
- `AE01-S01-CTRL-02`: do not count repeated names without shared operational
  semantics;
- `AE01-S01-CTRL-03`: detect correlation caused by a shared fixture or copied
  construction;
- `AE01-S01-CTRL-04`: preserve independent lane lineage and leave-one-out
  sensitivity; and
- `AE01-S01-CTRL-05`: prohibit recurrence from discharging producer,
  naturalization, composition, or claim debt.

Common controls `AE01-CTRL-03`, `07`, `08`, and `13` through `19` also apply.

### Stopping condition

Stop after every lane-to-requirement row is normalized once under the frozen
rules, dependency and source controls complete, and every cluster has exactly
one supported, partial, negative, blocked, or incomplete disposition. Do not
merge clusters after seeing ranking scores without reopening synthesis.

## 3. `AE01-H-S02` — Explicit N31+ non-selection

**Hypothesis:** if no post-synthesis candidate satisfies every D-029
eligibility gate, threshold, tie rule, and sensitivity requirement—or if any
forced non-selection condition applies—AE01 can close honestly with an
explicit non-selection and a bounded information-gathering step.

This is a governance and inference hypothesis. Non-selection is a valid result,
not evidence that no useful future graph experiment can ever exist.

### Support signature

`AE01-H-S02` is supported when at least one frozen non-selection condition is
present and the machine ranking record:

1. keeps ineligible candidates unscored;
2. records every failed eligibility gate or threshold;
3. applies the one-point tie band and fixed tie order;
4. runs all four sensitivity profiles for every scored candidate;
5. preserves the independent qualitative rationale and any declared prior;
6. selects no candidate;
7. records non-selection reasons and one applicable information-gathering
   step; and
8. leaves graph-side experiment authority unchanged.

Forced non-selection conditions are:

```text
no candidate clears every eligibility gate
eligible candidates exist but none clears every threshold
tie remains after the declared procedure
sensitivity profiles change the winner
any required lane or synthesis record is incomplete
conceptual demand is the primary support
reconstruction cannot be bounded
an unnamed stronger prerequisite is required
```

### Negative, blocked, and incomplete outcomes

- `not_supported`: exactly one eligible candidate passes all fixed thresholds,
  wins every sensitivity profile or declared tie procedure, and no forced
  non-selection condition applies. Selection is then permitted, not mandatory
  evidence of graph-side acceptance.
- `partial_or_mixed`: the ranking can order some candidates but a required
  qualitative rationale, prior-disagreement report, or information-gathering
  step is incomplete; no selection is allowed.
- `blocked_missing_prerequisite`: ranking inputs are complete but an eligibility
  discriminator or bounded reconstruction contract needed to evaluate a
  candidate is missing; close as non-selection with the missing requirement.
- `incomplete_execution`: ranking assembly or validation itself does not
  complete. This is not a valid scientific non-selection record and prevents a
  ranking closeout; the program may retain a lower-rung incomplete disposition.

### Fail-closed controls

- `AE01-S02-CTRL-01`: candidate IDs and inherited roadmap order cannot break a
  tie;
- `AE01-S02-CTRL-02`: ineligible candidates cannot receive scores;
- `AE01-S02-CTRL-03`: intuition cannot override a gate, threshold, tie, or
  sensitivity result;
- `AE01-S02-CTRL-04`: conceptual demand and constructed behavior cannot be
  counted as native LGRC evidence;
- `AE01-S02-CTRL-05`: no candidate or failed lane may be omitted to improve the
  ordering; and
- `AE01-S02-CTRL-06`: an incomplete lane forces non-selection but cannot be
  scored as a negative or recurrence result.

Common controls `AE01-CTRL-01` through `03`, `07`, `08`, and `12` through `19`
also apply.

### Stopping condition

Stop after the frozen candidate set has one eligibility disposition per
candidate and, for every eligible candidate, one complete score, tie,
sensitivity, and qualitative-rationale record. The result is either one
permitted unique recommendation or explicit non-selection. No post-hoc
candidate, weight, threshold, or tie-breaker change is allowed.

## 4. Claim boundary

Recurrence supports an ecology-side demand pattern only. Selection or
non-selection is guidance to the graph/ecology spiral, not LGRC evidence,
assignment of graph experiment N31, or authorization to modify the graph
repository.
