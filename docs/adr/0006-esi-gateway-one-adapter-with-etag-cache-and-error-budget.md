---
schemaVersion: 0.2.0
id: "0006"
title: "ESI gateway: one adapter with ETag cache and error budget"
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
    pattern: "backend/src/app/esi/**"
  - type: path
    pattern: "backend/src/app/dbhelpers/cache.py"
provenance:
  authoredBy: human
---

# ADR-0006: ESI gateway: one adapter with ETag cache and error budget

## Context

ESI is a shared, rate-limited, cache-friendly HTTP API. It reports a per-character error budget
(`X-ESI-Error-Limit-Remain`, `X-ESI-Error-Limit-Reset`), answers `304` with `Expires` and
`ETag`, paginates large collections and changes shape behind a compatibility date. A user with
five characters and corporation scopes can easily fan out into hundreds of requests per refresh.

## Decision

- All ESI traffic goes through `backend/src/app/esi/`; nothing else may call the host. Cache,
  retries, limits and token refresh live there once.
- Conditional requests: `If-None-Match` with the stored ETag, honouring `Expires`; a `304` is a
  normal answer and means the stored payload is reused.
- The cache is persistent (PostgreSQL), keyed by route, character and parameters, so restarts
  and background syncs share it.
- The client stops issuing requests when the remaining error budget approaches the floor and
  backs off on `420`/`429`; both surface as `EsiUnavailable`, never as a silent empty list.
- `X-Compatibility-Date` is set deliberately in one place and bumped by an ADR.
- The interface never calls ESI: features read the database, the sync layer fills it, so a page
  view is O(1) requests and pages cannot be used to amplify traffic.

## Options considered

### Option A: one adapter, database cache, background sync (chosen)

**Pros:** one place to enforce limits, a page view never depends on ESI latency, syncs are
resumable, and tests mock a single boundary.
**Cons:** data is as fresh as the last sync; the sync loop has to be scheduled and observable.

### Option B: call ESI from the request path

**Pros:** always fresh, no cache invalidation.
**Cons:** latency and rate limits leak into the interface; a slow ESI becomes a broken page,
and the error budget is spent by page views.

### Option C: community snapshot services for static data only

**Pros:** no ESI load for static data at all.
**Cons:** still needs the adapter for character data, and adds a second source of truth for the
same entities.

## Trade-offs

- Freshness trades against ESI load: the sync interval is a product decision, currently 15
  minutes, adjustable per deployment.
- The persistent cache adds a table and a key scheme to maintain; getting the key wrong is a
  correctness bug (one character's data served for another).

## Consequences

- Easier: testing, rate-limit safety, resumable syncs.
- Harder: "why is this number stale" questions, which need a visible last-synced timestamp.
- **How we would know this was wrong:** ESI error budget exhausted, or `420` responses in the
  logs, means the sync schedule is too aggressive.
- Revisit if: ESI introduces server-side subscriptions for the data the console needs.

## Action items

1. [x] Adapter skeleton with conditional GET and budget guard.
2. [ ] Cache table and key scheme (`dbhelpers/cache.py`) in the first sync slice.
