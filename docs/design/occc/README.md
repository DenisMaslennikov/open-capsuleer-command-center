# OCCC · Skill plan — design s5-t1 (revision)

Standalone mock: `skill-plan.html` (open directly in a browser, no build). Dark theme is the
default (`<body data-theme="dark">`); removing the attribute shows the light token map.

## Screen inventory

| Screen | Where in the file | Notes |
|---|---|---|
| Skill plan (default, populated, stale banner visible) | top `AppShell` block | Tree left (`--layoutTreeWidth`), plan right |
| State gallery | section "States · Состояния" | One rendered block per state, labelled with `figcaption` |

## Component inventory

| Component | Role | Rebuild notes |
|---|---|---|
| `AppShell` | Grid: top bar + nav + main | Existing layout; only the main area is new |
| `TopBar`, `SideNav`, `CharacterSwitcher` | Existing shell | `SideNav` item "Skill plan" gets `aria-current="page"` |
| `SkillTree` | Catalogue of skill groups | Width `--layoutTreeWidth`, own scroll |
| `SearchField` | Filters the tree | Focus ring on the wrapper via `:focus-within` |
| `StatusLegend` | Explains pip colours | Static |
| `SkillGroup` | Collapsible group | `<button aria-expanded aria-controls>`; chevron rotates `-90deg` when collapsed |
| `SkillRow` | Selectable skill | `<button aria-pressed>`; selected = inset 2px `--colorPrimary` bar |
| `LevelPips` | 5 level squares | `role="img"` + `aria-label` describing levels; states learned / queued / next / empty |
| `ImportPlanButton`, `AddSkillButton` | Plan actions | Primary = `AddSkillButton` |
| `StaleBanner` | Sync age warning | `role="status"`, shown when last sync > 1 h |
| `RefreshButton` | Re-sync skills | Inside banner |
| `PlanSummary` | 4 stat tiles (`<dl>`) | Total time, SP, book cost, finish date |
| `SkillPlanQueue` | Ordered plan table | Real `<table>` with visually hidden caption |
| `PlanRow` | One planned level | Move up/down/remove; first row "up" and last row "down" are `disabled` |
| `StatusBadge` | learned / queued / next / unreachable | Unreachable uses hollow dot so it is not colour-only |
| `EmptyState`, `ErrorState`, `NoAccessState` | State blocks | Shared layout `.state` |

## Formatting rules (reproduce exactly)

- All numbers use `--fontFamilyMono` + `font-variant-numeric: tabular-nums`.
- Thousands separator: narrow no-break space U+202F (`27 648 000`), via the product's number formatter.
- ISK: `1 312 500 000 ISK` (suffix, no decimals in the plan).
- Durations: `38d 07h 41m` / `38д 07ч 41м`; hours and minutes zero-padded; days omitted only in the stale banner when < 1 d.
- Skill level: Roman numerals I–V in monospace bold.
- Absent value: em dash `—`, right-aligned.

## Tokens used

Colours: `colorBgLayout`, `colorBgNav`, `colorBgContainer`, `colorSplit`, `colorText`,
`colorTextSecondary`, `colorPrimary`, `colorPrimaryHover`, `colorError`, `colorWarning`.
Spacing: `spaceXxs`…`spaceXl`. Radius: `radiusSm`, `radiusMd`, `radiusLg`. `shadowCard`.
Type: `fontFamily`, `fontSizeSm`, `fontSizeTable`, `fontSizeMd`, `fontSizeXl`.
Layout: `layoutTopBarHeight`, `layoutNavWidth`, `layoutTreeWidth`. `iconSize`, `motionBase`.

## Tokens to add

| Token | Light | Dark | Purpose |
|---|---|---|---|
| `colorStatusLearned` | `#2f9e44` | `#51cf66` | Learned level / badge |
| `colorStatusQueued` | `#2f6fed` | `#5b8ff9` | Queued level / badge |
| `colorStatusNext` | `#d98324` | `#f0a04b` | Next level in training order |
| `colorStatusUnreachable` | `#868e96` | `#6c757d` | Unreachable level (hollow dot, never colour-only) |
| `colorStatusEmpty` | `#dee2e6` | `#343a40` | Empty pip background / border |
| `colorFocusRing` | `#2f6fed` | `#8cb4ff` | 2px outline for all focusable elements |

Add them to the tokens file and to both theme maps (light and dark). No other new colours appear in the HTML. Every other colour resolves to an existing token. Status colours must not be reused for anything except level status.

## States per component

| Component | Default | Loading | Empty | Error | No access | Stale |
|---|---|---|---|---|---|---|
| `SkillTree` | Groups collapsed except the one holding the selected skill | 6 skeleton rows (`aria-busy="true"`) | "No skills match" plus a button that clears the search | — | Hidden; `NoAccessState` replaces the whole main area | Rendered normally; banner sits above the plan |
| `SearchField` | Placeholder | Disabled | Clear button visible when the field has a value | — | — | — |
| `SkillGroup` | Expanded / collapsed | — | Hidden when the filter leaves 0 rows | — | — | — |
| `SkillRow` | Rest / hover / focus / selected (`aria-pressed="true"`) | Skeleton | — | — | — | — |
| `LevelPips` | learned / queued / next / empty | Grey skeleton bar | All five empty | — | — | Values from the last sync |
| `StaleBanner` | Hidden | — | — | — | — | Visible: "Skills synced 3h 12m ago" + `RefreshButton` |
| `RefreshButton` | Rest | Spinner, `aria-busy="true"`, label "Refreshing…" | — | Banner switches to `colorError` and shows "Refresh failed" | — | — |
| `PlanSummary` | 4 tiles | 4 skeleton tiles | All values `—` | — | — | Values shown, finish date marked "approx." |
| `SkillPlanQueue` | Rows | 5 skeleton rows, caption announces loading | `EmptyState` with `AddSkillButton` | `ErrorState` with retry | `NoAccessState` | Rows shown |
| `PlanRow` | Rest / hover / focus-within | — | — | — | — | — |
| `StatusBadge` | learned / queued / next / unreachable | — | — | — | — | — |
| `EmptyState` | Icon + title + text + primary action | — | — | — | — | — |
| `ErrorState` | Icon in `colorError` + message + "Try again" button | — | — | — | — | — |
| `NoAccessState` | Lock icon + "Grant the skills scope" + link to the character's ESI settings | — | — | — | — | — |

## Accessibility checklist

- [x] Every interactive element is a native `<button>`, `<a>` or `<input>`. No clickable `div`s.
- [x] Visible focus ring: `outline: 2px solid var(--colorFocusRing); outline-offset: 2px` via `:focus-visible`. `SearchField` uses `:focus-within` on its wrapper.
- [x] Tab order follows reading order: top bar → nav → tree search → tree → plan actions → banner → table.
- [x] Collapsible groups use `aria-expanded` and `aria-controls`. Selected skill uses `aria-pressed`.
- [x] Status is never colour-only. Every state has a different shape (filled / outlined / striped / hollow) plus a text label in `StatusBadge`.
- [x] `LevelPips` has `role="img"` and a full `aria-label`, e.g. "Level 3 of 5 learned, level 4 queued".
- [x] Icon-only buttons (move up/down/remove) have `aria-label` with the skill name and level.
- [x] `StaleBanner` uses `role="status"`. `ErrorState` uses `role="alert"`.
- [x] Loading containers carry `aria-busy="true"`. Skeletons are `aria-hidden="true"`.
- [x] The table has a `<caption>` (visually hidden), `<th scope="col">` headers and right-aligned numeric columns.
- [x] Contrast: text ≥ 4.5:1 and status glyphs ≥ 3:1 against `colorBgContainer` in both themes.
- [x] `prefers-reduced-motion: reduce` disables the chevron rotation, skeleton shimmer and spinner animation.
- [x] Layout holds at 200 % zoom. Below 1100px the tree collapses above the plan.

## Catalogue keys

| Key | en | ru |
|---|---|---|
| `skillPlan.title` | Skill plan | План навыков |
| `skillPlan.search.placeholder` | Search skills | Поиск навыков |
| `skillPlan.search.clear` | Clear search | Очистить поиск |
| `skillPlan.legend.learned` | Learned | Изучено |
| `skillPlan.legend.queued` | Queued | В очереди |
| `skillPlan.legend.next` | Next | Следующий |
| `skillPlan.legend.unreachable` | Unreachable | Недоступно |
| `skillPlan.actions.import` | Import plan | Импорт плана |
| `skillPlan.actions.add` | Add skill | Добавить навык |
| `skillPlan.summary.totalTime` | Total time | Общее время |
| `skillPlan.summary.sp` | Skill points | Очки навыков |
| `skillPlan.summary.books` | Skillbook cost | Стоимость книг |
| `skillPlan.summary.finish` | Finishes | Завершение |
| `skillPlan.summary.approx` | approx. | прибл. |
| `skillPlan.table.caption` | Planned skill levels in training order | Запланированные уровни навыков в порядке изучения |
| `skillPlan.table.skill` | Skill | Навык |
| `skillPlan.table.level` | Level | Уровень |
| `skillPlan.table.duration` | Duration | Длительность |
| `skillPlan.table.status` | Status | Статус |
| `skillPlan.row.moveUp` | Move {skill} {level} up | Переместить {skill} {level} выше |
| `skillPlan.row.moveDown` | Move {skill} {level} down | Переместить {skill} {level} ниже |
| `skillPlan.row.remove` | Remove {skill} {level} | Удалить {skill} {level} |
| `skillPlan.pips.label` | Level {learned} of 5 learned, {queued} queued | Изучено уровней: {learned} из 5, в очереди: {queued} |
| `skillPlan.stale.text` | Skills synced {age} ago | Навыки синхронизированы {age} назад |
| `skillPlan.stale.refresh` | Refresh | Обновить |
| `skillPlan.stale.refreshing` | Refreshing… | Обновление… |
| `skillPlan.stale.failed` | Refresh failed | Не удалось обновить |
| `skillPlan.empty.title` | Your plan is empty | План пуст |
| `skillPlan.empty.text` | Pick a skill in the tree or import a plan. | Выберите навык в дереве или импортируйте план. |
| `skillPlan.tree.noMatch` | No skills match | Навыки не найдены |
| `skillPlan.error.title` | Could not load the plan | Не удалось загрузить план |
| `skillPlan.error.retry` | Try again | Повторить |
| `skillPlan.noAccess.title` | Grant the skills scope | Предоставьте доступ к навыкам |
| `skillPlan.noAccess.text` | This character has not shared skill data. | Персонаж не предоставил данные о навыках. |
| `skillPlan.noAccess.link` | Open ESI settings | Открыть настройки ESI |
| `duration.units` | d / h / m | д / ч / м |

All plural-sensitive strings go through the product's ICU formatter. Do not concatenate them.

## Rebuild order for the coding agent

1. Add the new tokens to both theme maps. Add `LevelPips` and `StatusBadge`, because every other part depends on them.
2. Build `SkillPlanQueue` / `PlanRow` with the formatting rules above. Use the product formatter for numbers, ISK and durations.
3. Build `SkillTree` with `SkillGroup`, `SkillRow` and `SearchField`.
4. Build `PlanSummary` and `StaleBanner`.
5. Add the shared `.state` blocks and wire the loading, empty, error and no-access states.
6. Check the result against the HTML in both themes, at 1440px and 1024px, and with keyboard only.
