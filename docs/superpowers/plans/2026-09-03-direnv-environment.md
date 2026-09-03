# direnv Local Environment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Load local `.env` variables and reuse the uv-managed `.venv` whenever a developer enters the repository.

**Architecture:** A tracked root `.envrc` uses direnv's standard library to load `.env` when present, then prepends the existing `.venv/bin` to `PATH`. The configuration never installs dependencies automatically; it prints an actionable message when `.venv` is absent. The local `.env` stays on disk but is removed from Git tracking and ignored.

**Tech Stack:** direnv 2.37, uv, Python 3.12, Zsh/Bash-compatible `.envrc` syntax.

---

### Task 1: Protect local secrets and configure direnv

**Files:**
- Create: `.envrc`
- Modify: `.gitignore`
- Untrack while preserving locally: `.env`

- [ ] **Step 1: Verify the current security state**

Run:

```bash
git ls-files --error-unmatch .env
git check-ignore -q .env
```

Expected before implementation: the first command succeeds because `.env` is tracked, and the second command fails because `.env` is not ignored.

- [ ] **Step 2: Ignore `.env`**

Add this entry to the Environments section of `.gitignore`:

```gitignore
.env
```

- [ ] **Step 3: Stop tracking `.env` without deleting the local file**

Run:

```bash
git rm --cached .env
test -f .env
```

Expected: Git stages removal of `.env`, while `test -f .env` succeeds because the local file remains.

This does not remove `.env` from existing Git history. If the file has ever contained real shared credentials, rotate them separately; do not rewrite repository history as part of this task.

- [ ] **Step 4: Create `.envrc`**

Create `.envrc` with exactly:

```bash
dotenv_if_exists .env

if [[ -d "$PWD/.venv" ]]; then
    export VIRTUAL_ENV="$PWD/.venv"
    PATH_add "$VIRTUAL_ENV/bin"
else
    echo "direnv: .venv is missing; run: uv sync" >&2
fi
```

- [ ] **Step 5: Allow and evaluate the configuration**

Run:

```bash
direnv allow .
direnv exec . sh -c 'test "$VIRTUAL_ENV" = "$PWD/.venv"'
direnv exec . sh -c 'test "$(command -v python)" = "$PWD/.venv/bin/python"'
direnv exec . sh -c 'test -n "${DJANGO_SECRET_KEY:-}"'
```

Expected: every command exits successfully. The checks expose no secret values.

- [ ] **Step 6: Verify Git and project state**

Run:

```bash
git check-ignore -q .env
test -f .env
git diff --check
uv run python manage.py check
```

Expected: `.env` is ignored but still exists locally, the diff has no whitespace errors, and Django reports no issues.

- [ ] **Step 7: Commit the configuration**

Run:

```bash
git add .envrc .gitignore
git commit -m "chore: configure direnv environment"
```

The staged `.env` removal must remain in the same commit so the repository no longer contains the local secret file.
