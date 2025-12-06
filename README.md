# Galway Clarke

## Frontend build shortcuts

Tailwind is compiled from `gc_static/input.css` to `gc_static/output.css`, which Django serves via `{% static 'output.css' %}`.

- `npm run tailwind:watch` — watches and rebuilds Tailwind during development.
- `npm run tailwind:build` — single build, useful for deployments or quick refreshes.

Both commands wrap `npx @tailwindcss/cli -i ./gc_static/input.css -o ./gc_static/output.css`.
