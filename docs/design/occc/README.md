# Skill Plan Screen Design

## Overview

This document describes the design of the skill plan screen for the OCCC interface.

## Component Inventory

- `SkillPlanScreen` - Main screen component, located in `pages/skills/`
- `CharacterSwitcher` - Global character selector, located in `common/`
- `SkillGroupTree` - Left panel showing skill groups, located in `pages/skills/components/`
- `PlanList` - Right panel showing planned levels, located in `pages/skills/components/`
- `ProgressIndicator` - Progress bars for skill groups, located in `pages/skills/components/`
- `StatusIndicator` - Status indicators for plan items, located in `pages/skills/components/`
- `TotalsPanel` - Summary statistics, located in `pages/skills/components/`
- `StateLoader` - Loading skeleton, located in `pages/skills/components/`
- `EmptyState` - Empty plan state, located in `pages/skills/components/`
- `ErrorState` - Error state, located in `pages/skills/components/`
- `NoAccessState` - No access state, located in `pages/skills/components/`
- `StaleState` - Stale data state, located in `pages/skills/components/`

## Tokens Used

### Semantic Tokens

- `--color-bg-layout`: Background color for layout areas
- `--color-bg-container`: Background color for containers
- `--color-border`: Border color for elements
- `--color-text`: Primary text color
- `--color-text-secondary`: Secondary text color
- `--color-primary`: Primary action color
- `--color-primary-hover`: Hover state for primary actions
- `--color-success`: Success color
- `--color-error`: Error color
- `--color-warning`: Warning color
- `--color-learned`: Color for learned skills
- `--color-queued`: Color for queued skills
- `--color-next`: Color for next skills
- `--color-unreachable`: Color for unreachable skills
- `--color-no-access`: Color for no access state
- `--color-stale`: Color for stale data

### Primitive Tokens

- `--space-xxs`: 4px spacing
- `--space-xs`: 8px spacing
- `--space-sm`: 12px spacing
- `--space-md`: 16px spacing
- `--space-lg`: 24px spacing
- `--space-xl`: 32px spacing
- `--space-xxl`: 48px spacing
- `--radius-sm`: 4px border radius
- `--radius-md`: 8px border radius
- `--radius-lg`: 12px border radius
- `--font-family`: Inter font family
- `--font-size-sm`: 12px font size
- `--font-size-md`: 14px font size
- `--font-size-lg`: 16px font size
- `--font-size-xl`: 20px font size
- `--font-size-xxl`: 28px font size
- `--motion-fast`: 120ms animation duration
- `--motion-base`: 180ms animation duration

## Tokens to Add

### New Semantic Tokens

| Name | Value | Meaning |
|------|-------|---------|
| `--color-learned` | `#2f9e44` | Color for learned skills |
| `--color-queued` | `#3b5bdb` | Color for queued skills |
| `--color-next` | `#e8a13a` | Color for next skills |
| `--color-unreachable` | `#6b7280` | Color for unreachable skills |
| `--color-no-access` | `#9ca3af` | Color for no access state |
| `--color-stale` | `#9ca3af` | Color for stale data |

## Catalogue Keys Needed

### English

- `skillPlan.title`: "Skill Plan"
- `skillPlan.characterSwitcher.all`: "All Characters"
- `skillPlan.characterSwitcher.select`: "Select Character"
- `skillPlan.syncBadge.lastSync`: "Last sync: {time}"
- `skillPlan.skillGroups.title`: "Skill Groups"
- `skillPlan.plannedLevels.title`: "Planned Levels"
- `skillPlan.totals.totalTime`: "Total Time"
- `skillPlan.totals.totalSp`: "Total SP"
- `skillPlan.totals.totalIsk`: "Total ISK"
- `skillPlan.actions.mergePlans`: "Merge Plans"
- `skillPlan.actions.planForShip`: "Plan for Ship"
- `skillPlan.state.loading.title`: "Loading..."
- `skillPlan.state.empty.title`: "No Skill Plan Yet"
- `skillPlan.state.empty.description`: "You haven't created a skill plan yet. Start by selecting skills to learn."
- `skillPlan.state.error.title`: "Failed to Load Plan"
- `skillPlan.state.error.description`: "There was an error loading your skill plan. Please try again later."
- `skillPlan.state.noAccess.title`: "Access Denied"
- `skillPlan.state.noAccess.description`: "You don't have permission to view this skill plan. You need the 'skills.read' scope."
- `skillPlan.state.stale.title`: "Data Stale"
- `skillPlan.state.stale.description`: "Your skill plan data is {days} days old. Refresh to get the latest information."
- `skillPlan.state.retry`: "Retry"
- `skillPlan.state.grantScope`: "Grant Scope"
- `skillPlan.state.refresh`: "Refresh"
- `skillPlan.createPlan`: "Create New Plan"

### Russian

- `skillPlan.title`: "План навыков"
- `skillPlan.characterSwitcher.all`: "Все персонажи"
- `skillPlan.characterSwitcher.select`: "Выбрать персонажа"
- `skillPlan.syncBadge.lastSync`: "Последняя синхронизация: {time}"
- `skillPlan.skillGroups.title`: "Группы навыков"
- `skillPlan.plannedLevels.title`: "Запланированные уровни"
- `skillPlan.totals.totalTime`: "Общее время"
- `skillPlan.totals.totalSp`: "Общие ОП"
- `skillPlan.totals.totalIsk`: "Общий ISK"
- `skillPlan.actions.mergePlans`: "Объединить планы"
- `skillPlan.actions.planForShip`: "Запланировать для корабля"
- `skillPlan.state.loading.title`: "Загрузка..."
- `skillPlan.state.empty.title`: "План навыков отсутствует"
- `skillPlan.state.empty.description`: "Вы еще не создали план навыков. Начните с выбора навыков для изучения."
- `skillPlan.state.error.title`: "Не удалось загрузить план"
- `skillPlan.state.error.description`: "Произошла ошибка при загрузке вашего плана навыков. Пожалуйста, попробуйте позже."
- `skillPlan.state.noAccess.title`: "Доступ запрещен"
- `skillPlan.state.noAccess.description`: "У вас нет разрешения на просмотр этого плана навыков. Вам нужна область 'skills.read'."
- `skillPlan.state.stale.title`: "Устаревшие данные"
- `skillPlan.state.stale.description`: "Ваши данные плана навыков устарели на {days} дней. Обновите, чтобы получить последние данные."
- `skillPlan.state.retry`: "Повторить"
- `skillPlan.state.grantScope`: "Предоставить область"
- `skillPlan.state.refresh`: "Обновить"
- `skillPlan.createPlan`: "Создать новый план"

## What to Reproduce

The coding agent should implement:

1. The main skill plan screen with:
   - Top bar with character switcher and sync badge
   - Left panel with skill groups and progress
   - Right panel with planned levels
   - Totals section with summary statistics
   - Action buttons

2. All state blocks:
   - Loading state with skeleton UI
   - Empty state
   - Error state with retry option
   - No access state with grant scope option
   - Stale data state with refresh option

3. Components:
   - SkillGroupTree
   - PlanList
   - ProgressIndicator
   - StatusIndicator
   - TotalsPanel
   - StateLoader
   - EmptyState
   - ErrorState
   - NoAccessState
   - StaleState

4. Proper use of design tokens throughout
5. Responsive layout
6. Keyboard accessibility with focus rings
7. Tabular number formatting for SP and ISK
8. Human-readable duration formatting

## Accessibility Checklist

- [x] All interactive elements have keyboard focus indication
- [x] Focus order is logical
- [x] All images have appropriate alt text
- [x] Sufficient color contrast for text and UI elements
- [x] Semantic HTML structure
- [x] Proper labeling of form controls
- [x] Screen reader friendly content
- [x] All state indicators are accessible
- [x] Color is not the only means of conveying information
- [x] Landmark regions properly defined
- [x] Skip links available if needed
