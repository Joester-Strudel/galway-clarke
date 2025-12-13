#!/usr/bin/env bash

# Clear all Django migration files (except __init__.py) across project apps.
# Intended for disposable local SQLite workflows.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

find "$PROJECT_ROOT" \
  -path "$PROJECT_ROOT/venv" -prune -o \
  -path "$PROJECT_ROOT/.venv" -prune -o \
  -path "$PROJECT_ROOT/node_modules" -prune -o \
  -path "$PROJECT_ROOT/*/migrations" -type d -print | while read -r dir; do
    find "$dir" -type f ! -name "__init__.py" -name "*.py" -delete
done

echo "Migration files removed (kept __init__.py)."
