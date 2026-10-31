---
schemaVersion: 0.2.0
id: "0009"
title: "Data model baseline and schema contract enforcement"
status: accepted
date: 2026-10-31
deciders: ["@denis"]
tags: []
scope: component
reversibility: one-way-door
blastRadius: component
relatesTo: ["0006", "0007"]
affects:
  - type: path
    pattern: "docs/schema/**"
  - type: path
    pattern: "backend/src/app/dbhelpers/**"
  - type: path
    pattern: "backend/src/app/db/schema_gate.py"
  - type: path
    pattern: ".agents/rules/database.md"
provenance:
  authoredBy: agent
  ratifiedBy: "@denis"
---

# ADR-0009: Data model baseline and schema contract enforcement

## Context

Every feature of this application touches the same entities: an account holding several characters,
game data imported from the static export, per-character state, hangars, mail, industry, market,
killmails, notifications. If each task designs the tables it needs, the same concept ends up in
three caches under three names, the migration graph forks, and the right to be forgotten reaches
half of the rows.

A schema can only be a contract if something enforces it. A document without a gate is advice:
the first executor with a deadline adds a column that the contract does not declare, and nobody
notices until the data is already wrong.

The repository is the place for the contract — it is part of the product, not of the pipeline that
happens to generate it. That is a deliberate exception to the pipeline rule that every gate lives
next to the pipeline scripts: this gate imports the application metadata, so it must live where the
application lives.

## Decision

### A. Baseline of the data model

- Every aggregate owns its tables and has exactly one module `backend/src/app/dbhelpers/<aggregate>.py`.
  A table belongs to one aggregate; two parallel tasks never touch the same table.
- Three lifetimes: `user` (dies with the account), `reference` (imported from the static data
  export), `cache` (disposable). The lifetime decides the deletion rule and the reachability rule.
- Game identifiers inside user and cache tables (`type_id`, `character_id`, `corporation_id`,
  `structure_id`, `alliance_id`) are `bigint` **without** a foreign key. Foreign keys **inside** the
  SDE aggregate are allowed and required. A reimport of static data must never lock or rewrite user
  rows, so a user or cache table never references `sde` by foreign key.
- Ownership has three shapes only: account-owned (`account_id`), character-owned, corporation-owned;
  the last two are nullable pairs guarded by `CHECK num_nonnulls(...) = 1`. Where an account context
  and a character appear in one row, the character must belong to that account: composite foreign
  key `(account_id, character_id) -> characters (account_id, id)`. Polymorphic `entity_id`, EAV and
  a universal `attributes` column are banned.
- Money is `numeric(20,2)`, quantities and skill points are `numeric(20,0)` or `bigint`; floating
  point is banned for money, quantity and price. Time is `timestamptz` in UTC.
- `jsonb` is allowed only for opaque external payloads. Secrets are `bytea` columns named
  `*_encrypted`.
- Every synchronised table has a unique key for upsert (owner plus game id). Synchronisation is
  idempotent: upsert, then delete the owner's rows the response no longer contains.
- Missing access is a row in `sync_states` with `skip_reason`, not a missing row: "no access" must be
  distinguishable from "no data".
- Corporate data is stored per account, never in shared rows.
- Time partitioning applies only to `market_data`.

### B. The contract is the source of truth, and a gate enforces it

- `docs/schema/schema.json` holds the contract; `docs/schema/schema.dbml` is the same contract as a
  diagram. Both are generated from the contract, never edited in the other direction.
- `backend/src/app/db/schema_gate.py` compares SQLAlchemy metadata with the contract and fails the
  build on: an undeclared table or column; a type, nullability or primary-key mismatch; a forbidden
  type (float money, misplaced `jsonb`, non-`bytea` secret, non-`timestamptz` timestamp); a foreign
  key that does not resolve, differs in `ON DELETE`, or points from a user/cache table into `sde`;
  a model living outside its aggregate's module; a user table that does not reach `accounts` by
  cascading foreign keys.
- The gate runs in CI on every pull request. A pre-commit hook is allowed for speed but is not the
  guarantee: an executor can bypass it with `--no-verify`, CI cannot.
- The completeness check in the reverse direction (declared but not implemented) fails only for
  aggregates whose module already exists, otherwise the gate would be red from day one.
- Changing the contract is a human-reviewed change: contract, model and migration land in one pull
  request, and a pull request that edits `schema.json` is `review:human`.

## Consequences

- A new column starts in the contract. That costs one extra step per schema change and buys a
  single place where the model of the data is visible.
- The gate is red until the model implements a declared table once its aggregate module exists. That
  is intended: an aggregate appears together with its tables, not ahead of them.
- Migrations stay linear: one revision per task, one head, no `alembic merge`.
- Some decisions become expensive to reverse: copying corporate data into each account, the ban on
  foreign keys into `sde`, and the composite tenant keys. They are one-way doors and would need a
  migration that rewrites rows.
- `alembic heads` and the autogenerate diff are not part of this gate yet: there are no models and no
  migrations to compare. They join in the first schema task (DB1), where the comparison becomes
  meaningful.

## Alternatives considered

- Contract as a document only, enforcement by convention. Rejected: nothing detects drift, and drift
  is only found by a wrong number in the interface.
- Contract generated from the models instead of the other way round. Rejected: then the model is the
  design, every task decides the design on its own, which is the problem this ADR exists to solve.
- Gate as a pre-commit hook in the pipeline scripts. Rejected: it imports the application metadata,
  so it belongs to the application repository; and a hook is bypassable by the agent it constrains.
- Separate ADRs for the baseline and for the gate. Rejected: they would duplicate the change process
  and cross-reference each other for no gain.
