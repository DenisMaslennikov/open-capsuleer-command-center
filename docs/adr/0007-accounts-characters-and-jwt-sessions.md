---
schemaVersion: 0.2.0
id: "0007"
title: "Accounts, characters and JWT sessions"
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
    pattern: "backend/src/app/features/auth/**"
  - type: path
    pattern: "backend/src/app/core/scopes.py"
provenance:
  authoredBy: human
---

# ADR-0007: Accounts, characters and JWT sessions

## Context

One person plays several characters, sometimes in different corporations. Data belongs to a
character (skills, jobs, assets) but the human wants one console. Corporation-scoped endpoints
additionally require corporation roles, which the character may or may not have.

The browser must never hold CCP tokens: a leaked access token is recoverable, a leaked refresh
token is a long-lived impersonation.

## Decision

- An account is local to this application: e-mail plus password (argon2), e-mail confirmation
  before first login.
- Characters attach to an account through EVE SSO; each character carries its own set of
  granted scopes, and therefore its own capabilities.
- Effective capability = scopes granted to that character ∩ scopes enabled in this instance.
  `GET /api/v1/me/capabilities` reports it per character.
- Between the contours: JWT. A short-lived access token is kept in memory by the frontend; a
  refresh token lives in an `HttpOnly`, `SameSite=Lax` cookie scoped to the auth path. No token
  in `localStorage`.
- CCP refresh tokens are stored server-side encrypted (Fernet, key from the environment) and
  never leave the backend.
- Aggregation endpoints accept `characters=all` or an explicit list and always return the
  characters they skipped together with the reason.

## Options considered

### Option A: local account, characters attached by SSO, JWT between contours (chosen)

**Pros:** one login for many characters; per-character consent is explicit; the browser holds
nothing long-lived; authorisation stays on the server.
**Cons:** an account system of our own (password reset, e-mail delivery), and a second
credential type to protect.

### Option B: log in as a character every time, no local account

**Pros:** no password storage, no e-mail infrastructure.
**Cons:** no place to keep several characters, and "aggregate across my characters" becomes a
session feature instead of a data model.

### Option C: server-side sessions with a cookie instead of JWT

**Pros:** revocation is immediate and trivial.
**Cons:** the SPA and the API would share a session store; JWT was an explicit requirement and
scales better across future consumers.

## Trade-offs

- Revocation with JWT is not immediate: the access token lives minutes, so a compromised token
  is bounded by that, and the refresh token is revoked at once.
- E-mail confirmation adds an SMTP dependency; development uses a local mail catcher, so the
  flow exists from day one instead of being retrofitted.
- Capability intersections mean a feature can be half-available; the interface has to state
  which character lacks which scope.

## Consequences

- Easier: multiple characters per person, honest partial data, small blast radius of a stolen
  browser token.
- Harder: two credential systems to reason about; tests need both a session token and a fake
  ESI token.
- **How we would know this was wrong:** if users routinely re-authorise the same character
  daily, refresh handling is broken.
- Revisit if: a second frontend or a public API consumer appears, where token lifetimes and
  scopes need their own policy.

## Action items

1. [x] Scope registry and capability resolution (`core/scopes.py`).
2. [ ] Account, character and token models with migrations.
