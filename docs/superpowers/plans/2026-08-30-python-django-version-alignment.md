# Python and Django Version Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standardize the local development environment on Python 3.12 and Django 5.2 LTS with reproducible dependencies and current documentation.

**Architecture:** Project metadata defines compatible minor-version ranges while `uv.lock` pins exact transitive versions. `.python-version` selects Python 3.12 locally, and the README plus existing Phase 1 documents record the supported stack and workflow.

**Tech Stack:** Python 3.12, Django 5.2 LTS, uv, PostgreSQL, pytest, Ruff

---

### Task 1: Runtime version policy

**Files:**
- Create: `.python-version`
- Modify: `pyproject.toml:7-16`

- [ ] **Step 1: Set the Python selector**

Create `.python-version` containing exactly:

```text
3.12
```

- [ ] **Step 2: Constrain supported runtime versions**

Set the project metadata to:

```toml
requires-python = ">=3.12,<3.13"
dependencies = [
    "django>=5.2,<5.3",
]
```

Keep the existing non-Django dependencies unchanged.

- [ ] **Step 3: Confirm uv selects Python 3.12**

Run: `uv run python --version`

Expected: output starts with `Python 3.12.`

### Task 2: Lock dependencies

**Files:**
- Modify: `uv.lock`

- [ ] **Step 1: Regenerate the lock file**

Run: `uv lock --python 3.12`

Expected: successful resolution with `requires-python = ">=3.12,<3.13"` and a Django 5.2.x package.

- [ ] **Step 2: Synchronize the environment**

Run: `uv sync --python 3.12`

Expected: dependencies install successfully without building the Python 3.14-incompatible `pyzmq` path encountered previously.

### Task 3: Update developer documentation

**Files:**
- Modify: `README.md`
- Modify: `docs/superpowers/specs/2026-05-09-phase1-dictionary-management-design.md`
- Modify: `docs/superpowers/plans/2026-05-09-phase1-dictionary-management.md`

- [ ] **Step 1: Replace the placeholder README**

Document:

- Python 3.12 and Django 5.2 LTS as the supported stack.
- `uv sync`, PostgreSQL environment variables, migrations, server startup, tests, and Ruff commands.
- MeCab CSV import and export command examples.
- `/admin/` as the current user interface.

- [ ] **Step 2: Record the stack in the Phase 1 design**

Add a technology stack section specifying:

```text
Python 3.12
Django 5.2 LTS
PostgreSQL
uv
```

- [ ] **Step 3: Record the prerequisite in the Phase 1 plan**

Add an environment prerequisite stating that all commands assume Python 3.12 and Django 5.2 LTS as locked by `uv.lock`.

### Task 4: Verification

**Files:**
- Verify only; no application code changes expected

- [ ] **Step 1: Verify selected versions**

Run: `uv run python --version && uv run python -m django --version`

Expected: Python 3.12.x and Django 5.2.x.

- [ ] **Step 2: Run tests**

Run: `uv run pytest -q`

Expected: all tests pass.

- [ ] **Step 3: Run static and Django checks**

Run: `uv run ruff check . && uv run python manage.py check`

Expected: both commands exit successfully. If Ruff reports pre-existing style issues, report them separately rather than changing unrelated application code.

- [ ] **Step 4: Review the diff**

Run: `git diff --check && git status --short`

Expected: no whitespace errors; only the planned files and the pre-existing `.antigravitycli/` entry appear.
