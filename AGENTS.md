# AGENTS.md — open-capsuleer-command-center

Operating rules for agents. Read automatically by OpenHands, Claude Code and Cursor.

> This file is an **index**. The rules live in `.agents/rules/<group>.md`.
> Read the file for the zone you are working in, not the whole set at once.

## Overview

EVE Online command center: skills and skill plans, industry jobs, assets across characters
and corporations, aggregated per account.

Stack: Python 3.14 + uv + FastAPI + SQLAlchemy 2 (async) + PostgreSQL 16 on the backend;
React 19 + Ant Design 6 + TypeScript + TanStack Query on the frontend; docker compose runs
both contours.

## Commands

```bash
make up        # docker compose up --build (db, backend, frontend dev server)
make test      # backend pytest + frontend vitest
make lint      # ruff + eslint + tsc --noEmit
make e2e       # Playwright against the running stack
make migrate   # alembic upgrade head
make sdk       # regenerate frontend API types from the backend OpenAPI
make sde       # download and import the current static data export
make schema-gate # compare models with the schema contract
```

## Layout

```
backend/src/app/     features/ (vertical slices), domain/, dbhelpers/, esi/, sde/, sync/
backend/tests/       unit/ and integration/
frontend/src/        pages/, common/, api/, theme/, i18n/, lib/
frontend/e2e/        Playwright specs against the running stack
.agents/rules/       rules: process, style, architecture, interface, testing, licensing, database
docs/adr/            decisions (adrkit)
docs/schema/         database schema contract (JSON) and ERD (DBML, generated)
```

## Project rules

| File | About | When to read |
|---|---|---|
| `.agents/rules/workflow.md` | branches, PRs, gates, limits, review and disputes | before any task and before a PR |
| `.agents/rules/code_style.md` | types, names, errors, comments, prohibitions | before editing `backend/**` or `frontend/src/**` |
| `.agents/rules/design.md` | layers, module boundaries, contracts, async rules | new feature, API or data change |
| `.agents/rules/ui.md` | design tokens, component placement, i18n, accessibility | any change under `frontend/` |
| `.agents/rules/testing.md` | where and how to write tests, fixtures, e2e | before writing or editing tests |
| `.agents/rules/licensing.md` | what may be licensed how, CCP data boundary | touching data, fixtures, images, licence files |
| `.agents/rules/database.md` | schema contract, table ownership, migrations, rules of the data model | before touching models, migrations or SQL |

A new rules group = a new file in `.agents/rules/` + a row in this table (through a PR).

## Language

Code, docstrings, comments, ADRs, rules and documentation are written in English. Interface
strings ship in both locales, `ru` and `en`, and catalogue keys stay identical between them.

## Comments and docstrings

- A comment exists only where the code cannot state its intent: a non-obvious workaround, a
  spec quirk, a deliberate deviation. Everything else belongs in a docstring or in `docs/`.
- A docstring describes behaviour, arguments, return value and raised errors. It never
  contains a call example.

## Hard prohibitions

- Do not touch files outside the task's `files_allowed`.
- Do not modify `tests/**` while the task is in the `Code` phase.
- Do not change a public API without an ADR.
- Do not commit secrets, `.env` files, or anything downloaded from CCP.
- Do not call ESI outside `backend/src/app/esi/`.
- Do not run SQL outside `backend/src/app/dbhelpers/`.

## Decisions

Before changing behaviour — `adr explain <path>`; a new decision — `adr new`.
