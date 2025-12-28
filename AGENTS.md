# Repository Guidelines

## Project Structure & Module Organization
- `mecab_ko_dic_admin/config/` contains Django project settings, URLs, and ASGI/WSGI entrypoints.
- `mecab_ko_dic/` is the primary Django app (models, views, admin, migrations).
- `mecab_ko_dic/tests.py` holds app tests (currently a placeholder).
- `env/` is used for local environment data; keep generated files out of versioned code.
- `manage.py` is the main CLI entrypoint for Django tasks.

## Build, Test, and Development Commands
- `uv sync` installs dependencies from `pyproject.toml` into the local environment.
- `uv run python manage.py runserver` starts the local development server.
- `uv run python manage.py migrate` applies database migrations.
- `uv run python manage.py makemigrations` creates new migrations from model changes.
- `uv run pytest` runs the pytest test suite.
- `uv run python manage.py test` runs Django’s test runner (useful for app-level tests).

## Coding Style & Naming Conventions
- Indentation: 4 spaces; line length: 120.
- Formatter/Linter: `ruff` (`ruff format .`, `ruff check .`).
- Use double quotes for strings and follow Django naming conventions for apps and models.

## Testing Guidelines
- Primary framework: `pytest` (dependency listed in `pyproject.toml`).
- Django tests should live in `mecab_ko_dic/tests.py` or module-level `tests/` packages.
- Name tests with `test_` prefixes and keep unit tests isolated from external services.

## Commit & Pull Request Guidelines
- Commit history is short and descriptive; follow the same pattern (imperative, concise).
- Pull requests should include a clear summary, testing notes, and any relevant migration info.
- Link related issues and include screenshots only if UI changes are involved.

## Configuration Notes
- Update `mecab_ko_dic_admin/config/settings.py` for environment-specific settings.
- Keep secrets out of source control; use local environment files instead.
