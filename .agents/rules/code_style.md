# code_style — code style

When to read: before editing any file under `backend/**` or `frontend/src/**`.

## Comments and docstrings

- A comment exists only where the code cannot state its intent: a non-obvious workaround, a
  spec quirk, a deliberate deviation. Everything else belongs in a docstring or in `docs/`.
- A docstring describes behaviour, arguments, return value and raised errors. It never contains
  a call example — examples duplicate the signature and rot.
- Comments, docstrings and documentation are English.

## Python

- Types on every public boundary; `Any` only where an external payload is genuinely untyped,
  and then it is narrowed immediately.
- `ruff` decides formatting and lint (`backend/pyproject.toml` is the source of truth, currently
  line length 120); `ruff format` is the only formatter.
- Data crossing a boundary is a pydantic model, not a dict.
- `async def` on every I/O path; blocking calls are banned in request handlers.

## TypeScript

- Strict mode; no `any`, no non-null assertion to silence a real possibility of `null`.
- Server state through TanStack Query only; no `useEffect` fetching.
- Types describing the API come from the generated schema, never hand-written.

## Names

- Modules and functions are named after the action (`material_requirements`, `loadAssets`).
- No boolean flags in positional arguments — keyword-only parameters in Python, an options
  object in TypeScript.

## Imports

- Every import lives at module top. **Local (function-level) imports are forbidden.**
- If a change seems to need one — a circular import, a heavy optional dependency, a shortcut in
  tests — stop and raise it for a human decision with the options: move the shared symbol to a
  module both sides can import, invert the dependency (the lower module defines a protocol, the
  higher one implements it), or split the module.
- Breaking a cycle by moving an import inside a function is not a fix: it hides the cycle and the
  next reader pays for it. This list of forbidden workarounds grows — a pattern the owner forbids
  is added here in the same pull request that introduces the alternative.

## Prohibitions

- No local imports (see above).
- No public API change without an ADR.
- No secrets, `.env` files, downloaded game data or debug prints in commits.
