# Publication Checklist

This checklist tracks the finite work required to make this repository ready
for a public GitHub publication pass.

## README

- [x] Add a concise project description near the top.
- [x] State current maturity: conceptual paper/specification repository, no
      runnable implementation package.
- [x] Add a four-paper reading path for current papers.
- [x] Add core translation, intended-reader, practical-use, and maturity-ladder
      orientation sections.
- [x] Link the related theory and implementation repositories.
- [x] Add repository map, claim boundary, citation, and license sections.

## Repository Metadata

- [x] Add `CONTRIBUTING.md`.
- [x] Add `CODE_OF_CONDUCT.md`.
- [x] Add `CITATION.cff`.
- [x] Add `CHANGELOG.md`.
- [x] Add `RELEASE-NOTES.md`.
- [x] Add `.gitignore` for local caches, tool state, scratch output, virtual
      environments, and secret-bearing config.

## Claim and License Review

- [x] Confirm the README does not imply runnable code or native implementation
      claims.
- [x] Confirm paper headers declare CC BY-SA 4.0.
- [x] Confirm shared-medium coordination is framed as conceptual/specification
      work unless future implementation evidence is linked.
- [x] Confirm message scaffolds and medium debt are distinguished from native
      shared-medium coordination.
- [x] Confirm repository metadata documents the mixed-license boundary:
      `papers/` are CC BY-SA 4.0, while non-paper support files are
      GPL-2.0-only unless a file states otherwise.

## Pre-Publication Scan

- [x] Review current repository file inventory.
- [x] Search for obvious secrets, tokens, private keys, passwords, and
      machine-local absolute paths.
- [x] Review `git status --short` before publication.

## Deferred Until After Publication

- [ ] Add issue templates after the public repository workflow is clear.
- [ ] Add a pull request template after first external contribution patterns are
      known.
- [ ] Add GitHub repository description and topics after publication.
- [ ] Add archive DOI metadata to `CITATION.cff` if assigned.
