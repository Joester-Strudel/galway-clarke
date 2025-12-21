## Workspace Build Pattern (Generic)

Use this as a recipe to build a CRUD workspace (list + drawer + tabs) for any app/model.

### 1) Model & Defaults
- Define your core model and any lookup models (e.g., statuses/tags/categories/geography).
- If you need per-team/per-tenant defaults, add a `post_save` signal on the tenant (e.g., Team) to seed a few starter lookup records.

### 2) Admin
- Create a `model_admins/<model>_admin.py`, import from `admin.py`.
- Set `list_display`, `search_fields`, `ordering`, and `list_select_related` for performance.
- Keep filters minimal unless you have proven, performant filters.

### 3) Views & URLs
- List view: renders the workspace shell (table + drawer placeholder), HTMX-friendly.
- Drawer views:
  - GET to open existing record (edit) or new record (create).
  - POST to save; return the drawer partial with updated context.
- Delete view: POST to delete; the drawer triggers a table refresh.
- Select endpoints for remote selects (search + pagination); return option partials.
- Wire URLs for list/edit/create/delete and select endpoints.

### 4) Templates Structure
- Workspace page (`templates/cotton/app/<app>/pages/<model_plural>.html`):
  - Table tools (search/sort/add), HTMX table container, drawer shell.
- Drawer partial (`partials/<model>_drawer.html`):
  - Alpine data factory (e.g., `modelDrawer`) manages `activeTab`, delete confirm, delete call.
  - Tabs: use `c-app.components.tabs.changeform_tab`.
  - Error: `c-app.components.errors.form_error`.
  - Tab content split into components:
    - General tab component: core fields + remote selects.
    - Address tab component (if needed): address lines + geo selects.
    - Notes/extra tab component: rich text or other fields.
  - Footer: `c-app.components.changeforms.changeform_footer_controls` (timestamp, delete confirm, save button).
  - OOB row: render row via a Cotton component for table swaps.
- Row partial (`partials/<model>_row.html`): structured cells, used both in initial table render and OOB updates.
- Generic components leveraged:
  - `components/tabs/changeform_tab.html`
  - `components/errors/form_error.html`
  - `components/changeforms/changeform_footer_controls.html`

### 5) Frontend Field Patterns
- Remote select (`components/fields/remote_pill_select.html`):
  - HTMX options endpoint (`?search=&page=`), sentinel for infinite scroll.
  - Supports single/multiple; renders pills; accepts help text.
- Rich text (`components/fields/rich_text_field.html`):
  - WYSIWYG toolbar, sanitization, hidden input sync.

### 6) JavaScript Helpers
- Alpine factory for the drawer (e.g., `modelDrawer({ activeTab, deleteUrl, listRefreshUrl })`).
- Optionally move JS into `gc_static/js/<name>.js` and load via `{% static %}`.

### 7) E2E Tests (Playwright + pytest-django + pytest-playwright)
- Fixtures:
  - `user_and_team` (or tenant) + session cookie login for authenticated flows.
  - Any required lookup/geo seeds (e.g., states/cities/zips) so selects have data.
- Helpers:
  - Remote select chooser with wait + scroll + collapse.
  - Save wait (expect response on POST).
  - Delete wait (expect response on delete POST).
  - Drawer open/close helpers, row open by name, formatted notes filler.
- Flows to cover:
  - List renders; drawer opens from row and add button.
  - Search narrows rows and combined filters (e.g., status/tag/org) isolate expected records.
  - Create: fill required fields, selects, notes; save; row appears.
  - Edit: change fields; save; row updates.
  - Tab persistence: save while on a non-default tab.
  - Delete: confirm and verify row removal.
  - (If applicable) auth flows: signup/signin/select-tenant/signout.
- Run examples:
  - `pytest <app>/tests/test_<model>_e2e.py --headed --browser chromium -s --slowmo 200`
  - Ensure `pytest.ini` sets `DJANGO_SETTINGS_MODULE` and Playwright browsers are installed.

### 8) Repeatable Checklist
1. Model + lookups + optional seed signal.
2. Admin with display/search/ordering/select_related.
3. Views: list, drawer edit/create, delete, select endpoints.
4. URLs wired for list/edit/create/delete/selects.
5. Workspace page + drawer partial + row partial.
6. Componentize tabs, errors, footer, and tab content.
7. JS helper for drawer state; static file optional.
8. Remote selects + rich text fields as needed.
9. E2E tests for create/edit/delete/tab persistence/selects/auth; seed data fixtures.
10. Tune timeouts/slowmo for visibility; keep helpers reusable.

## Codex Notes – CRM Individuals Workspace Fixes
- Prevent reversing edit URLs with empty IDs: when rendering the individuals drawer for “add”, do not include the OOB row swap or any `crm-individual-edit` URL; pass explicit `save_url`/`delete_url` into the drawer context and forward `edit_url` to the row partial.
- Avoid showing “None” error banners: wrap `form_error` with `error|default_if_none:''` so the alert is hidden when no error is present (applied to both individuals and organizations drawers).
- Remote selects: close the dropdown immediately after selecting an option (single or multi) so it doesn’t intercept subsequent clicks (e.g., checkboxes near the field); implemented in `remote_pill_select` toggle.
