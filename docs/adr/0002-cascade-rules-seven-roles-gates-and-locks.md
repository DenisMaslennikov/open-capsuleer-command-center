---
schemaVersion: 0.2.0
id: "0002"
title: "Cascade rules: seven roles, gates and locks"
status: accepted
date: 2026-10-31
deciders: ["@denis"]
tags: []
scope: component
reversibility: two-way-door
blastRadius: component
relatesTo: []
affects:
  - type: path
    pattern: ".agents/rules/**"
  - type: path
    pattern: "docs/adr/**"
provenance:
  authoredBy: human
---

# ADR-0002: Cascade rules: seven roles, gates and locks

## Context

The code is produced by an agent pipeline whose failure mode is confident wrongness: a model
that both writes the tests and the implementation can make them agree on a mistake. Cost is
also real — an expensive model has to be spent only where it changes the outcome.

## Decision

Seven roles, each with its own process, context and model:

| Role | Input | Output |
|---|---|---|
| architect | feature description + repository map | JSON plan: subtasks, `files_allowed`, acceptance, dependencies, contracts |
| specifier | one subtask | failing tests plus the truth table |
| designer | UI specification + current tokens | design spec: grid, states, component list, token delta (no code) |
| executor | frozen tests + `files_allowed` | code until green |
| arbiter | dispute package | `{winner, rationale, action, confidence}` (no code) |
| reviewer | pull request | review report from pr-agent |
| vision | screenshots + acceptance criteria | matches / diverges |

Rules that make it hold:

1. Tests are written by one role and the code by another, and tests are frozen before coding.
2. Every subtask declares `files_allowed`; leaving it is a bad plan, not an exception.
3. Locks are enforced by a tool (the `check-diff` gate before push, branch protection on the
   host), never by a prompt.
4. The arbiter's vendor differs from the specifier's and the executor's; the reviewer's vendor
   differs from the arbiter's.
5. `designer` exists only in projects with an interface (`ui: true`); `designer` invents the
   interface, `vision` verifies what was rendered.
6. Every model call is written to the token ledger; a task is not closed without it.

## Options considered

### Option A: seven roles (chosen)

**Pros:** independent test authorship, a cheap implementer under strict tests, a separate
adjudicator for the residual disputes, a dedicated voice for design.
**Cons:** more orchestration, higher latency, more place where a bad prompt wastes money.

### Option B: one agent with a checklist

**Pros:** cheapest, fastest, least machinery.
**Cons:** the same context writes both sides of every contract; measured errors are
systematic, not random, and nothing catches them.

### Option C: three roles (architect, executor, reviewer)

**Pros:** half the moving parts.
**Cons:** no independent test authorship and no adjudicator, which are exactly the two things
the pipeline is built to provide.

## Trade-offs

- Latency: architect and designer run on the strongest model available and dominate cost.
- The arbiter is invoked only on disagreement, so its expense is bounded by disputes.
- The designer adds a phase to every UI subtask; the alternative is design decisions taken
  inside implementation, which are invisible to review.

## Consequences

- Easier: catching a wrong contract before code exists; parallel slices with disjoint files.
- Harder: the decomposer must produce subtasks small enough for a frozen `files_allowed`.
- **How we would know this was wrong:** if the arbiter's share of escalations approaches
  zero while defects still reach review, roles are being paid for nothing.
- Revisit if: executor pass rate on frozen tests exceeds ~90% on the first attempt, at which
  point the specifier or the arbiter can be thinned out.

## Action items

1. [x] Role contracts and temperatures in `~/.config/cascade/roles.yaml`.
2. [ ] Measure per-role cost share after the first three features.
