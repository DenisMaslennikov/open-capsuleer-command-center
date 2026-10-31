# ui — interface

When to read: any change under `frontend/` — components, styles, user-visible strings.

## Design tokens

- One source: `src/theme/tokens.ts` — primitives (colour scale, spacing, radii, type, motion)
  plus semantic aliases built on them.
- Ant Design receives its theme only through `src/theme/antd.ts`, derived from the semantic
  aliases.
- No literal colour, pixel size, shadow, radius or breakpoint inside a component. Tokens only.

## Component placement

- A component used by one page lives next to that page (`pages/<page>/components/`).
- As soon as a second page needs it, it moves to `common/`. Not before.
- Pages compose; they do not re-implement layout primitives.

## Localisation

- Every user-visible string goes through `t()`; no literals in markup.
- `src/i18n/ru.json` and `src/i18n/en.json` stay key-for-key identical; a test fails on a
  missing key.
- Numbers, ISK amounts and durations go through `src/lib/format.ts`, never `toFixed` in a
  component.

## Access control

- The interface draws only what the capabilities response allows; a hidden button is not a
  permission.
- A disabled feature states the reason (`requires scope X`), it does not silently disappear.

## States and accessibility

- Every interactive element is keyboard reachable and has a visible focus state.
- Empty, loading and error states belong to the component, not to the caller.
