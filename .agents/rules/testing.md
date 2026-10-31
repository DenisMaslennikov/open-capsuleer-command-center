# testing — tests

When to read: before writing or editing tests, and before diagnosing a failing test.

## Where and how

- Backend: `backend/tests/unit/` (no database, no network) and `backend/tests/integration/`
  (ASGI application plus a real PostgreSQL).
- Frontend: `*.test.tsx` colocated with the unit under `frontend/src/`.
- End to end: `frontend/e2e/`, Playwright, run against the running stack — never against mocks.
- A test name states the behaviour (`test_me_10_reduces_materials`), not the function name.
- One test — one scenario; shared data goes to `tests/fixtures/`.

## Order

1. First a test that fails on the old code (`gate.py expect-fail`).
2. Then the implementation until green (`gate.py expect-pass`).
3. During the `Code` phase tests are frozen: editing `tests/**` is blocked by the
   `frozen-tests` gate.

## External systems

- ESI is mocked at the adapter boundary (`aioresponses`); unit tests never touch the network.
- Recorded payloads are kept outside the repository when they contain CCP data.
- Deterministic time: pass a clock or a timestamp into domain functions.

## Prohibitions

- Bending a test to fit the implementation (or the reverse) is a dispute for the arbiter, not a
  right of the code.
- Testing the implementation instead of the behaviour (private calls, call order).
- Asserting types or constants the language or library already guarantees.
