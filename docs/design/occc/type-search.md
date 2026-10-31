# Type Search Control

## Component Information

- **Component Name**: TypeSearch
- **Placement**: `common/` (used across multiple pages)
- **States**: idle, focused, loading, results, no-results, error, no-access
- **Tokens Used**: All tokens from `src/theme/tokens.ts`

## Catalogue Keys

### English
- `search.placeholder`: "Search for a skill or type..."
- `search.clear`: "Clear search"
- `search.no-results`: "No results found"
- `search.error`: "Search failed. Please try again."
- `search.no-access`: "Requires scope: {scope}"

### Russian
- `search.placeholder`: "Поиск навыка или типа..."
- `search.clear`: "Очистить поиск"
- `search.no-results`: "Результатов не найдено"
- `search.error`: "Поиск не удался. Пожалуйста, попробуйте снова."
- `search.no-access`: "Требуется разрешение: {scope}"

## Keyboard Behavior

- **Up/Down arrows**: Navigate through results
- **Enter**: Select highlighted result
- **Escape**: Close dropdown
- **Tab**: Move to next focusable element
- **Space**: Toggle dropdown (when focused)

## Accessibility Checklist

- [x] All interactive elements have proper focus states
- [x] Clear button has aria-label for screen readers
- [x] Dropdown content is properly announced by screen readers
- [x] Keyboard navigation works correctly
- [x] Focus management within dropdown
- [x] Proper labeling of all form controls
- [x] Semantic HTML structure
- [x] Color contrast meets WCAG standards

## Implementation Notes

The coding agent should implement the following:

1. The component must be self-contained with no external dependencies
2. All styling must use the provided design tokens exclusively
3. The dropdown should show/hide based on input focus and interaction
4. Results should be grouped by category (skills, items, etc.)
5. Each result item should include an icon, name, and group
6. Long names should truncate with ellipsis and show full name in tooltip
7. All states must be handled properly with appropriate visual feedback
8. The component should handle keyboard navigation for results
9. The clear button should reset the input and close dropdown
10. Error and no-access states should display appropriate messages

The component should be designed to integrate seamlessly with the existing skill plan interface.
