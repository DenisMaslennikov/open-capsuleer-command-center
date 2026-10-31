---
schemaVersion: 0.2.0
id: "0008"
title: "Interface: design tokens and bilingual catalogue"
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
    pattern: "frontend/src/theme/**"
  - type: path
    pattern: "frontend/src/i18n/**"
  - type: path
    pattern: ".agents/rules/ui.md"
provenance:
  authoredBy: human
---

# ADR-0008: Interface: design tokens and bilingual catalogue

## Context

The console is dense: tables, cross-linked filters, numbers in ISK, durations in days. The
interface is bilingual (Russian and English) and will be built mostly by agents, which tend to
invent a colour, a spacing value and a hard-coded string every time they touch a component.
Design consistency has to be cheaper to follow than to violate.

## Decision

- `src/theme/tokens.ts` holds primitives (colour scale, spacing, radii, type, motion) and
  semantic aliases. Ant Design receives its theme only through `src/theme/antd.ts`, derived from
  those aliases. No component contains a literal colour, size, shadow or breakpoint.
- A component used by one page lives with that page; the second consumer moves it to `common/`.
  Pages compose, they do not re-implement layout.
- Every user-visible string goes through `t()`; `en.json` and `ru.json` stay key-for-key
  identical and a test fails on a missing key.
- Numbers, ISK and durations are formatted in `src/lib/format.ts`, never inline.
- Capability-driven visibility: the interface draws what `/me/capabilities` allows and states
  the missing scope instead of hiding a feature silently.

## Options considered

### Option A: design tokens plus a thin component layer (chosen)

**Pros:** one place to change the look; review can check a rule instead of a taste; the design
role produces a token delta rather than screenshots alone.
**Cons:** an extra indirection for every style; a component that needs something unusual has to
extend the token set first.

### Option B: Ant Design defaults, styles inline per component

**Pros:** fastest to write the first screen.
**Cons:** every screen looks slightly different; dark mode or a rebrand becomes a rewrite; no
reviewable artefact for design decisions.

### Option C: a separate CSS framework (Tailwind) alongside Ant Design

**Pros:** fine-grained control.
**Cons:** two styling systems and two sources of truth for colour and spacing — the exact
problem tokens exist to solve.

## Trade-offs

- The token layer costs a step for every new visual need, and an agent that does not read the
  rule will bypass it — which is why the rule is checked in review.
- Keeping two catalogues identical is mechanical work; a test enforces it instead of a habit.

## Consequences

- Easier: consistent look, a real design role, locale parity, accessibility defaults.
- Harder: one more layer to learn before the first component renders.
- **How we would know this was wrong:** if literal colours keep appearing in review, the token
  set is missing something — extend the set, do not relax the rule.
- Revisit if: the product needs a second visual theme (compact vs comfortable), which the token
  layer should absorb as another dimension.

## Action items

1. [x] `theme/tokens.ts`, `theme/antd.ts`, `i18n/{en,ru}.json`, layout with the legal footer.
2. [ ] Key-parity test for the catalogues.
