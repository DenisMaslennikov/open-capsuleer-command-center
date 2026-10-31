---
schemaVersion: 0.2.0
id: "0001"
title: "Stack: python 3.14 + uv + FastAPI + React 19 + AntD 6"
status: accepted
date: 2026-10-31
deciders: ["@denis"]
tags: []
scope: component
reversibility: one-way-door
blastRadius: component
relatesTo: []
affects:
  - type: path
    pattern: "backend/**"
  - type: path
    pattern: "frontend/**"
provenance:
  authoredBy: human
---

# ADR-0001: Stack: python 3.14 + uv + FastAPI + React 19 + AntD 6

## Context

The product is a data-heavy console: skills, skill plans, industry jobs, assets — with
aggregation across characters and corporations. The domain logic (training time, materials
with ME, job cost, valuation) is objective, so tests can check meaning rather than taste. The
code is written mostly by an agent pipeline, which rewards one toolchain per contour, fast
feedback loops and a type boundary between contours.

The owner fixed the stack: Python 3.14 with uv, FastAPI, SQLAlchemy with Alembic, PostgreSQL
16, React with Ant Design, pytest and vitest. `aiohttp` was chosen for all outbound HTTPS.

Versions below were verified by installing the stack on the target interpreter, not taken
from memory: FastAPI 0.162, Starlette 1.10, SQLAlchemy 2.1.6, psycopg 3.3.6, pydantic 2.14.2,
React 19.3.1, Ant Design 6.6.8, Vite 8.3.5, Vitest 5.0.5, TanStack Query 5.105.

## Decision

- Backend: Python 3.14, uv (`[tool.uv] package = false`, the project is an application, not a
  distributable), FastAPI, SQLAlchemy 2.1 async with psycopg 3, Alembic, pydantic 2.
- Outbound HTTP: `aiohttp`, one shared session created in the application lifespan.
- Database: PostgreSQL 16 in every contour, no SQLite fallback.
- Frontend: React 19, Ant Design 6, Vite 8, TanStack Query 5, zod, `openapi-fetch`, TypeScript
  5.9.
- Tests: pytest and vitest for units, Playwright for end to end against the running stack.

## Options considered

### Option A: FastAPI + React SPA (chosen)

**Pros:** the two halves evolve independently; the typed OpenAPI boundary gives the frontend
its types for free; Ant Design covers dense tables, trees and forms that this console needs.
**Cons:** two toolchains, two test runners, a Node runtime in CI.

### Option B: FastAPI + Jinja templates + HTMX

**Pros:** one language, one test runner, no API boundary to keep in sync.
**Cons:** the console needs client-side state (filters across linked tables, background
refresh of running jobs, per-character toggles) that HTMX pushes back to the server on every
interaction; the resulting handlers are harder for an agent to keep small.

### Option C: Django + DRF

**Pros:** admin out of the box, mature auth.
**Cons:** the async story is bolted on; the owner fixed FastAPI; the admin duplicates the
interface we actually need.

## Trade-offs

- TypeScript is pinned to 5.9, not 7.x. `openapi-typescript@7.13` and `typescript-eslint@8`
  declare a `^5` peer, and TypeScript 7 is the new native compiler; forcing it in produces an
  unsupported toolchain. Moving to TS 7 is a separate decision once the peers allow it.
- Async everywhere means no synchronous ORM shortcuts: a blocking call in a request path is a
  defect, which the rules state explicitly.
- A SPA needs its own i18n, formatting and error surfaces.

## Consequences

- Easier: generated API types, independent deploys, dense tables in Ant Design.
- Harder: keeping the OpenAPI schema stable, since the frontend compiles against it.
- **How we would know this was wrong:** if most pages need fewer than three client-side
  interactions, HTMX would have been enough — measure after the first release.
- Revisit if: TypeScript 7 support lands in the whole toolchain, or the SPA bundle passes the
  point where first paint on a slow connection hurts.

## Action items

1. [x] Pin versions in `backend/pyproject.toml` and `frontend/package.json`.
2. [ ] Record the upgrade to TypeScript 7 as its own ADR when peers allow.
