# design — architecture

When to read: a new feature, a new module, a change to a public API or the data model.

## Layers

- `domain/` — pure functions, no I/O, no framework imports; fully unit-tested.
- `features/<feature>/` — one vertical slice: `router.py`, `schemas.py`, `service.py`.
- `dbhelpers/` — every SQL statement in the project. A `select()` anywhere else is a defect.
- `esi/` — the single outbound boundary to CCP. A call to `esi.evetech.net` anywhere else is a
  defect.
- `sde/` — bulk import of static data; `sync/` — scheduling of background refresh.

Dependencies point one way: `features → domain`, `features → dbhelpers`, `features → esi`.
`domain` imports none of them.

## Database layer

- One module per aggregate (`dbhelpers/characters.py`, `dbhelpers/assets.py`); the module owns
  its models and its statements.
- A helper needed by a second module moves to `dbhelpers/common.py`. Modules never import each
  other sideways.
- Everything is async: `AsyncSession`, `create_async_engine`, `await session.execute(...)`.

## Contracts

- Public functions carry explicit types and a docstring stating what and why, never how.
- A data-model change goes through an Alembic migration plus an ADR.
- Outbound third-party payloads are validated into pydantic models at the boundary; features
  never see raw dictionaries.

## Boundaries

- A feature never imports another feature. Shared behaviour belongs to `domain/` or `common/`.
- Cyclic imports are forbidden.
- Shared helpers live where they were born, not in a default `utils/`.

## When a decision is required

A library, a storage shape, a protocol or a service boundary is chosen by an ADR, not by a
comment in the code.
