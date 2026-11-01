---
schemaVersion: 0.2.0
id: "0004"
title: "Two contours: backend and frontend, docker in dev and prod"
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
    pattern: "compose.yaml"
  - type: path
    pattern: "backend/Dockerfile"
  - type: path
    pattern: "frontend/Dockerfile"
provenance:
  authoredBy: human
---

# ADR-0004: Two contours: backend and frontend, docker in dev and prod

## Context

The application is an API plus a single-page interface. Development has to run on the owner's
machine and be reachable from the LAN at a stable address, and the production contour must
eventually be the same images with a different composition — otherwise "works in dev" stops
meaning anything.

## Decision

- Two contours at the repository root: `backend/` and `frontend/`, each with its own
  toolchain, Dockerfile and test runner. Neither is published as a package.
- `compose.yaml` runs three services: PostgreSQL 16, the backend with a reload server, and the
  frontend dev server bound to `0.0.0.0` and served at `http://localhost:5173/`.
- The dev server proxies `/api` to the backend service, so the browser sees one origin and
  cookies behave the same in every contour.
- `compose.prod.yaml` later reuses the same images: the backend as a multi-worker runtime
  stage, the frontend as static files behind nginx.

## Options considered

### Option A: monorepo, two contours, compose everywhere (chosen)

**Pros:** one pull request can change both sides of a contract; one command brings the stack
up; images are the same in dev and prod.
**Cons:** two toolchains in one CI run; a Node image and a Python image to maintain.

### Option B: two repositories

**Pros:** independent CI, independent versions.
**Cons:** a contract change becomes two pull requests with no atomic view, which is exactly
what an agent pipeline handles badly.

### Option C: single container with the backend serving built assets

**Pros:** one process, one image, no CORS or proxy questions.
**Cons:** every frontend change requires a backend rebuild; hot reload disappears, and the dev
loop — the thing that actually costs time here — gets worse.

## Trade-offs

- Two dev servers need a proxy rule, and a wrong proxy looks like a CORS bug.
- A monorepo means CI runs both suites even when only one contour changed; path filters can
  fix that later.
- The public development address is plain HTTP. CCP's OAuth redirect URI must match exactly,
  so it is registered as `http://localhost:5173/api/v1/auth/eve/callback`; if the
  portal rejects a non-HTTPS host, a TLS terminator is added for that path only.

## Consequences

- Easier: one-command start, identical images, no separate frontend deployment story.
- Harder: keeping the compose file honest as services are added (no mounts in the prod file).
- **How we would know this was wrong:** if the frontend rebuild starts dominating the dev
  loop, or if a change routinely needs two coordinated pull requests, the split is wrong.
- Revisit if: the product gets a second consumer of the API, where a versioned package helps.

## Action items

1. [x] `compose.yaml` with db, backend, frontend.
2. [ ] Add `compose.prod.yaml` when the first deployment target exists.
