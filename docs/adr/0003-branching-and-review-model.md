---
schemaVersion: 0.2.0
id: "0003"
title: "Branching and review model"
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
    pattern: ".agents/rules/workflow.md"
provenance:
  authoredBy: human
---

# ADR-0003: Branching and review model

## Context

Agents produce many small changes in parallel. The repository must stay reviewable by one
human, history must stay linear enough to bisect, and review must not become the bottleneck
while still keeping a human at the only irreversible step.

## Decision

- `main` is protected: pull requests only, squash merge, one human approval, linear history.
- `feat/<slug>` is the integration branch of one feature; it lives at most a week and is
  rebased daily.
- `task/<feat>/<id>` branches from `feat/*`; their pull requests target `feat/*`, never `main`.
- Two review modes on a card: `review:agent` (pr-agent comments, the executor fixes, merge into
  `feat/*` when green) and `review:human` (the same plus a filled description and a human
  approval).
- A disagreement between pr-agent and the executor goes to the arbiter; an unresolved one, or
  a verdict with `confidence < 0.6`, goes to the human.
- One pull request = one subtask = one `files_allowed`.

## Options considered

### Option A: feature branches plus a task branch per subtask (chosen)

**Pros:** parallel subtasks never conflict on `main`; the integration branch is the place where
the whole feature is tested together.
**Cons:** rebasing work, and a second merge step that a human must remember.

### Option B: trunk-based, every subtask straight to `main`

**Pros:** one branch, no accumulation.
**Cons:** a half-finished feature reaches the protected branch; with parallel agents the
conflict rate on hot files becomes the bottleneck.

### Option C: one branch per feature, no subtask branches

**Pros:** fewer branches.
**Cons:** parallel agents would share a working tree; `files_allowed` could be violated by a
race, not by a decision.

## Trade-offs

- Extra merges cost time; in exchange, review sees one subtask at a time.
- Squash merging discards individual commits inside a task, so the task description has to
  carry the reasoning.

## Consequences

- Easier: bisecting, reverting a single subtask, reviewing.
- Harder: keeping `feat/*` short-lived requires prompt integration, not patience.
- **How we would know this was wrong:** if `feat/*` branches routinely live past a week, the
  decomposition is producing features too large for one branch.
- Revisit if: pull requests stay under ~200 lines each, at which point direct-to-`main` with
  strict review could be revisited.

## Action items

1. [x] Branch protection on `main` (one approval, squash, linear history).
2. [ ] Add required status checks once CI is attached to the repository.
