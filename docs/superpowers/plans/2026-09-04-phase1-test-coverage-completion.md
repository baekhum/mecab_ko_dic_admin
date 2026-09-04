# Phase 1 Test Coverage Completion Plan

**Status:** Active

**Goal:** Close the remaining Phase 1 test-evidence gaps without changing established behavior.

**Design:** `docs/superpowers/specs/2026-09-04-phase1-test-coverage-completion-design.md`

## Task 1: Protect dictionary identity

**Files:**
- Modify: `mecab_ko_dic/tests.py`

- [ ] Add a direct test that a duplicate `(표층형, 품사_태그)` insert raises `IntegrityError`.
- [ ] Run `uv run python manage.py test mecab_ko_dic.tests.MecabModelTest`.
- [ ] Commit the focused test change.

## Task 2: Complete Django Admin coverage

**Files:**
- Modify: `mecab_ko_dic/tests_admin.py`
- Modify only if a test demonstrates a defect: `mecab_ko_dic/admin.py`

- [ ] Add explicit search assertions for `표층형`, `품사_태그`, and `의미_부류`, retaining reading coverage.
- [ ] Assert authorized staff can change and delete compound entries.
- [ ] Run `uv run python manage.py test mecab_ko_dic.tests_admin`.
- [ ] Commit the focused test change and any demonstrated minimal fix.

## Task 3: Verify and record completion

**Files:**
- Modify: `docs/superpowers/specs/2026-09-04-phase1-test-coverage-completion-design.md`
- Modify: `docs/superpowers/plans/2026-09-04-phase1-test-coverage-completion.md`

- [ ] Run `uv run python manage.py migrate`.
- [ ] Run `uv run python manage.py test`.
- [ ] Run `uv run ruff check .`.
- [ ] Run `uv run python manage.py check`.
- [ ] Run `uv run python manage.py makemigrations --check --dry-run`.
- [ ] Run `git diff --check` and inspect `git status --short`.
- [ ] Mark this design and plan completed only after all checks pass.
- [ ] Commit the completion record.
