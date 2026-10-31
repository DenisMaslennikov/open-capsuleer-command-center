# OCCC · Dark theme tokens

Source of truth for the dark palette. It is a mapping, not a page: the same component tree, the
same `AppShell` layout, the same states — only the colour values change. The light theme stays the
default and is untouched; `dark` is an opt-in account setting. Every dark value below is a literal
hex or `rgba()` so it can be pasted into `src/theme/tokens.ts` as is. Contrast ratios are WCAG 2.x
measured against the named dark surface (canvas `#0f141a`, container `#161c24`, nav `#131a22`,
elevated `#202836`, tint wash `#1e2a3e` as the 12 % primary over container).

## Mapping table

| token | light value | dark value | use | contrast note |
|---|---|---|---|---|
| `colorBgLayout` | `#f7f8fa` | `#0f141a` | Canvas behind every screen — the page background that shows around panels. | Body text `#e6edf7` 15.70:1, secondary `#93a1b5` 7.05:1 on it. |
| `colorBgContainer` | `#ffffff` | `#161c24` | Cards, panels, top bar, inputs, popovers, dropdown menus. | Text 14.54:1, secondary 6.53:1, primary accent `#5b8ff9` 5.50:1. |
| `colorBgNav` (added) | `#eef4fc` | `#131a22` | Side rail and brand strip, recessed one step below the container. | Text 14.87:1, secondary 6.68:1 on it. Adjusted from the `#161c24` anchor: at 1.06:1 vs canvas the rail still reads as "set back", without a visible seam. |
| `colorBgElevated` (added) | `#ffffff` | `#202836` | Raised rows (character switcher hover/selected), floating panels. | Text 12.57:1, secondary 5.65:1 on it. Raised 1.16:1 above container — a step, not a jump. |
| `colorBgCard` (added) | `#ffffff` | `#1b222c` | Dense data cards (skill queues, job tables) sitting on the canvas. | Text ≈ 13.7:1 on it; kept between container and elevated so nested surfaces order correctly. |
| `colorBorder` | `#dde1e8` | `#273140` | Hairline strokes: card outlines, input borders, dividers on cards. | 1.31:1 vs container — intentionally below 3:1; it is decorative. Interactive boundaries are carried by the focus ring (`#5b8ff9`, 5.50:1). |
| `colorSplit` (added) | `rgba(31, 35, 40, 0.08)` | `rgba(230, 237, 247, 0.08)` | Table row dividers, list separators. | Renders as `#272d35` on container, 1.23:1 — a divider, not a boundary; non-text decorative. |
| `colorText` | `#1f2328` | `#e6edf7` | Primary text everywhere: names, numbers, values. | 15.70:1 on canvas, 14.54:1 on container, 12.57:1 on elevated. |
| `colorTextSecondary` | `#6b7280` | `#93a1b5` | Labels, captions, section subtitles, inactive nav labels. | 7.05:1 on canvas, 6.53:1 on container, 5.65:1 on elevated — comfortably above the 3:1 target. |
| `colorTextMuted` (added) | `#8b93a1` | `#6b7686` | Placeholders, timestamps, disabled text, "synced 4 min ago". | 3.72:1 on container, 3.22:1 on elevated, 4.02:1 on canvas. Below 4.5 by intent: it marks non-essential metadata; anything a user must act on uses `colorTextSecondary`. |
| `colorPrimary` | `#3b5bdb` | `#5b8ff9` | Links, selected nav item, primary button fill, focus ring, "queued" accent. | As text/accent: 5.94:1 on canvas, 5.50:1 on container, 4.75:1 on elevated. As a fill it keeps the algorithm's `#ffffff` label at 3.11:1 — the same trade-off as Ant Design's own dark seed; filled-button labels are large chrome text, and the dark hover state is the brighter `#7aa6ff`, inverting the light theme's darker hover. |
| `colorPrimaryHover` | `#2f49b0` | `#7aa6ff` | Hover of links, nav items and primary buttons. | 7.12:1 on container, 7.69:1 on canvas as text; direction reversed vs light (light hover darkens, dark hover brightens) because darkening a dark canvas would hide the change. |
| `colorPrimaryTint` (added) | `rgba(47, 111, 237, 0.10)` | `rgba(91, 143, 249, 0.12)` | Selected nav background, active character row, subtle accent washes. | Over container it renders `#1e2a3e`; primary text on that wash is 4.63:1, body text 12.24:1. Alpha raised from 10 % to 12 % because a 10 % blue wash on ink is nearly invisible — the wash must stay perceptible at low luminance. |
| `colorPrimaryTintHover` (added) | `rgba(47, 111, 237, 0.06)` | `rgba(91, 143, 249, 0.08)` | Hover wash on nav items and list rows. | Renders `#1c2535` on container, 1.11:1 — quiet feedback, paired with the text change to `colorPrimaryHover` (7.12:1) so hover is not colour-only. |
| `colorSuccess` | `#2f9e44` | `#3fbf6f` | Generic success: sync ok, API key valid, alerts. | 7.26:1 on container as dot/accent; 7.83:1 on canvas. |
| `colorSkillLearned` (added) | `#2f9e44` | `#3fbf6f` | "Learned" state dot and badge on skill rows. | 7.26:1 on container, 6.27:1 on elevated — well above the 3:1 status floor. |
| `colorSkillQueued` (added) | `#2f6fed` | `#5b8ff9` | "Queued" dot; aliases `colorPrimary` in both themes, as in the light artefact. | 5.50:1 on container, 4.75:1 on elevated. |
| `colorSkillNext` (added) | `#d98324` | `#e8a33d` | "Next to train" dot, stale-sync marker, soon-to-complete jobs. | 7.94:1 on container, 6.87:1 on elevated. |
| `colorSkillUnreachable` (added) | `#8a94a6` | `#8f9aab` | "Unreachable" state dot and scope-missing reason text. | 6.02:1 on container, 5.20:1 on elevated, 6.16:1 on nav. Brightened from the `#6b7686` muted anchor: unreachable is a state a user must notice, so it gets full secondary-level contrast, not muted contrast. |
| `colorSkillNoAccess` (added) | `#8a94a6` | `#8f9aab` | "No access" character state; aliases `colorSkillUnreachable`, as in the light artefact. | 6.02:1 on container; the row name additionally drops to `colorTextSecondary` (6.53:1), so the state is never carried by the dot alone. |
| `colorSkillStale` (added) | `#d98324` | `#e8a33d` | "Stale sync" dot; aliases `colorSkillNext`, as in the light artefact. | 7.94:1 on container, 6.87:1 on elevated. |
| `colorDanger` (added) | `#e03131` | `#e5534b` | Destructive buttons, sync failure, killmail accent; aliases `colorError`. | 4.63:1 on container, 4.99:1 on canvas, 4.00:1 on elevated — above the 3:1 status floor everywhere, and above 4.5 where it appears as text on container. |
| `colorError` | `#e03131` | `#e5534b` | Ant Design error semantics (alerts, form validation). | Same value as `colorDanger`: 4.63:1 on container, 4.99:1 on canvas. |
| `colorWarning` | `#e8a13a` | `#e8a33d` | Ant Design warning semantics (alerts, degraded state). | 7.94:1 on container, 6.87:1 on elevated. Nearly identical to the light value — the light amber already sits where a dark amber must. |
| `gray050` | `#f7f8fa` | `#0f141a` | Primitive behind `colorBgLayout`. | Dark literal of the canvas anchor. |
| `gray100` | `#eef0f4` | `#131a22` | Primitive behind `colorBgNav`. | Dark literal of the nav anchor. |
| `gray200` | `#dde1e8` | `#273140` | Primitive behind `colorBorder`. | Dark literal of the hairline anchor. |
| `gray500` | `#6b7280` | `#93a1b5` | Primitive behind `colorTextSecondary`. | 6.53:1 on container. |
| `gray900` | `#1f2328` | `#e6edf7` | Primitive behind `colorText`. | 14.54:1 on container. |
| `white` | `#ffffff` | `#161c24` | Primitive behind `colorBgContainer`. | The label colour on primary fills stays `#ffffff` in both themes; only the surface role flips. |
| `indigo600` | `#3b5bdb` | `#5b8ff9` | Primitive behind `colorPrimary`. | 5.50:1 on container. |
| `indigo700` | `#2f49b0` | `#7aa6ff` | Primitive behind `colorPrimaryHover`. | 7.12:1 on container. |
| `green600` | `#2f9e44` | `#3fbf6f` | Primitive behind `colorSuccess` / `colorSkillLearned`. | 7.26:1 on container. |
| `red600` | `#e03131` | `#e5534b` | Primitive behind `colorError` / `colorDanger`. | 4.63:1 on container. |
| `amber600` | `#e8a13a` | `#e8a33d` | Primitive behind `colorWarning` / `colorSkillNext`. | 7.94:1 on container. |
| `spaceXxs` … `spaceXxl` | 4 / 8 / 12 / 16 / 24 / 32 / 48 px | unchanged | Spacing scale — geometry, identical in both themes. | n/a — not a colour. |
| `radiusSm` / `radiusMd` / `radiusLg` | 4 / 8 / 12 px | unchanged | Corner radii, identical in both themes. | n/a — not a colour. |
| `fontFamily`, `fontSizeSm`…`fontSizeXxl`, font weights | Inter, 12–28 px, 400/500/600 | unchanged | Typography scale, identical in both themes. | n/a — not a colour. |
| `motionFast` / `motionBase` | 120 ms / 180 ms | unchanged | Transition durations, identical in both themes. | n/a — not a colour. |

Deliberate deviations from the anchor palette, with reasons: `colorSkillUnreachable` and
`colorSkillNoAccess` move from the muted `#6b7686` anchor to `#8f9aab` (an unreachable character is
information, not decoration, and must clear the 3:1 status floor on every surface); the primary
tint alpha rises from 10 % to 12 % (a 10 % wash vanishes on ink); `colorBgNav` becomes its own
`#131a22` instead of sharing the `#161c24` surface anchor (the rail must stay perceptibly recessed
without a visible seam). Everything else keeps the anchor values because they already clear their
contrast floors — see the measured column.

## Ant Design

Wire the dark theme through the algorithm, not by hand-tuning every Ant token:

```ts
import { theme } from "antd";
import { antdTheme } from "./antd"; // already derived from tokens.ts

<ConfigProvider
  theme={{
    algorithm: [theme.darkAlgorithm],
    ...antdTheme, // same shape as light: token + components overrides, now with dark values
  }}
>
```

- Override on top of the algorithm, in `token`, exactly the values the table pins: the brand and
  status seeds (`colorPrimary`, `colorPrimaryHover`, `colorSuccess`, `colorError`, `colorWarning`)
  and the pinned surfaces and text (`colorBgLayout`, `colorBgContainer`, `colorBgNav`,
  `colorBorder`, `colorSplit`, `colorText`, `colorTextSecondary`) — `tokens.ts` is the single
  source and `antd.ts` must derive from it, not from Ant's defaults.
- The domain states — `colorSkillLearned`, `colorSkillQueued`, `colorSkillNext`,
  `colorSkillUnreachable`, `colorSkillNoAccess`, `colorSkillStale`, `colorDanger`,
  `colorPrimaryTint` — stay in `tokens.ts` only and are consumed by markup and `common/`
  components; Ant has no slot for them, so the algorithm cannot know them.
- Do NOT override: sizing, spacing, radii, font family and sizes, motion durations, and everything
  the algorithm already derives from the seed — the neutral scale, hover/active variants of the
  overridden colours, `colorTextTertiary`/`colorTextQuaternary`, disabled states, and
  component-internal fills (table row hover, alert and tag backgrounds). Hand values there would
  drift from the algorithm.
- The seed colour changes: `#2f6fed` → `#5b8ff9`. In light theme the accent must be dark enough to
  carry `#ffffff` label text; in dark theme the accent must instead clear 4.5:1 against ink
  surfaces as text, links and focus rings, which forces a lighter blue. `theme.darkAlgorithm` seeds
  from `colorPrimary` and derives hover/active/background variants from it, so brightening the seed
  automatically produces the brightened variant set.

## Switching

- The theme is a user setting stored with the account (`settings.theme: "light" | "dark"`,
  light as default); the saved value is applied on load, before first paint.
- Switching applies `<body data-theme="dark">` for the token layer and `theme.darkAlgorithm` in
  `ConfigProvider` for Ant — both from one state, never set separately.
- No component reads a colour directly: markup references semantic tokens only, so a component
  never knows which theme is active.
