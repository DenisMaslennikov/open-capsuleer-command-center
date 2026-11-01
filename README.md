# OpenCapsuleerCommandCenter (OCCC)

A command center for capsuleers: character skills and skill plans, active and planned
industry jobs, and assets across personal and corporation hangars — aggregated over every
character attached to one account, filtered down to a single character when needed.

Interface is bilingual (English / Russian). Code, documentation and agent rules are English.

## Status

Early development. The repository is the product: application contours, agent rules and
architecture decisions. No production deployment exists yet.

## Stack

| Contour | Stack |
|---|---|
| Backend | Python 3.14, uv, FastAPI, SQLAlchemy 2 (async), Alembic, psycopg 3, aiohttp |
| Database | PostgreSQL 16 |
| Frontend | React 19, Ant Design 6, Vite, TypeScript, TanStack Query, zod, i18next |
| Tests | pytest, vitest, Playwright (end to end against the running stack) |
| Runtime | docker compose, development and production contours |

## Quick start

```bash
cp .env.example .env          # fill in the EVE application credentials
docker compose up --build     # db + backend + frontend dev server
```

Then open <http://localhost:5173/>. The backend is on port 8000, PostgreSQL on 5433.

## Accounts, characters and scopes

A user registers on the site, then attaches one or more EVE characters through EVE SSO.
Each character carries its own set of granted scopes, so capabilities differ per character.
Endpoints answer for `characters=all` or a chosen subset, and always report which characters
were skipped and why (missing scope, missing corporation role) instead of returning a
silently incomplete total.

## Licensing

- Application code: **AGPL-3.0-or-later** (`LICENSE`).
- EVE game data, static data exports, images and CCP Marks: **not** covered by that licence,
  see `LICENSE-CCP-DATA`. Nothing from CCP is committed to this repository; it is fetched at
  runtime into `data/`, which is ignored by git.
- This application has been created under the EVE Developer License Agreement. It is
  non-commercial: no paid access, no premium tiers. Donations and general advertising are
  permitted by that agreement; selling the application is not.
- © 2014 CCP hf. All rights reserved. "EVE", "EVE Online", "CCP", and all related logos and
  images are trademarks or registered trademarks of CCP hf.

## Repository layout

```
backend/    FastAPI service: features (vertical slices), domain, dbhelpers, esi adapter, sde import
frontend/   React application: pages, common components, api client, theme tokens, i18n
docs/adr/   architecture decisions
.agents/rules/  operating rules for agents (index in AGENTS.md)
compose.yaml
```

## Contributing

See `CONTRIBUTING.md`. In short: contributors must have signed the EVE Developer License
Agreement (required to use ESI at all), changes arrive through pull requests into `feat/*`
branches, and merges into `main` are performed by a human.
