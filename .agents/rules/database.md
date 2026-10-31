# database — schema contract, ownership and migrations

When to read: before any change to models, migrations or the database schema, and before writing
SQL in `dbhelpers/`.

## The contract comes first

- `docs/schema/schema.json` is the declared schema. `docs/schema/contract/<aggregate>.json` is the
  slice a single task implements; `docs/schema/schema.dbml` is the diagram.
- A change starts in the contract, then the SQLAlchemy model, then the Alembic migration — all in
  one PR. Adding a column that the contract does not declare is a defect, not a shortcut.
- The contract edits are `review:human`. Models and migrations that follow an already declared
  table are ordinary `review:agent` work.
- One aggregate = one module in `backend/src/app/dbhelpers/`; a table belongs to exactly one
  aggregate. Two tasks working in parallel never touch the same table.

## Rules the contract encodes

- `bigint identity` primary keys for our tables; SDE tables are keyed by the game id.
- Game ids (`type_id`, `character_id`, `corporation_id`, `structure_id`, `alliance_id`) inside user
  and cache tables are `bigint` without a foreign key: reimporting static data must not lock or
  rewrite user rows. Foreign keys inside the SDE aggregate are allowed and required.
- Where one row carries an account and a character, the character must belong to that account:
  composite foreign key `(account_id, character_id) -> characters (account_id, id)`.
- Ownership of a row is two nullable foreign keys plus `CHECK num_nonnulls(...) = 1`. No polymorphic
  `entity_id`, no EAV, no universal `attributes` column.
- Money `numeric(20,2)`; quantities and skill points `numeric(20,0)` or `bigint`. Float is banned
  for money, quantity and price.
- Timestamps are `timestamptz` in UTC; `created_at` always, `updated_at` on mutable rows.
- `jsonb` only for opaque external payloads (`esi_responses.body`, `notification_events.payload`).
- Secrets are `bytea` columns named `*_encrypted`; the key comes from the environment, never from
  the database.
- Every synchronised table has a unique key for upsert (owner plus game id). Synchronisation is
  upsert-then-delete-what-disappeared, never truncate-and-reload.
- "No access" is recorded as `sync_states.skip_reason`, not as an absence of rows.
- Corporate rows belong to the account that authorised them (`corporations.account_id`).

## Migrations

- One revision per task, chained on the current head. `alembic merge` is banned: it hides a
  conflict instead of resolving it. A second head is a planning defect, not a migration problem.
- `alembic upgrade head` must succeed from an empty database, not only from the current one.
- Autogenerate must produce no diff: a model that the migration does not match is a broken task.
- Never edit an applied migration; write the next one.

## Holds

- `make schema-gate` is green: models match `docs/schema/schema.json`.
- `alembic heads` returns exactly one head, and its parent is the head recorded when the task was
  created.
- The models match the contract table by table, column by column.
- Every user-lifetime table reaches `accounts.id` through cascading foreign keys; deleting an
  account leaves no user row, no cache row and no notification history behind.

## Prohibitions

- No SQL outside `backend/src/app/dbhelpers/`.
- No schema change in a PR that is about behaviour only.
- No `SELECT *` in `dbhelpers/` — a column added by a migration must not silently change a payload.
- No index without a query that needs it.
