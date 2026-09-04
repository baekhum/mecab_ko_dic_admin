# Phase 1 Test Coverage Completion Plan

**Status:** Completed on 2026-09-04. Implementation commits: `d71cff0`, `432df4d`.

**Goal:** Close the remaining Phase 1 test-evidence gaps without changing established behavior.

**Design:** `docs/superpowers/specs/2026-09-04-phase1-test-coverage-completion-design.md`

## Task 1: Protect dictionary identity

**Files:**
- Modify: `mecab_ko_dic/tests.py`

- [x] Add a direct test that a duplicate `(표층형, 품사_태그)` insert raises `IntegrityError`.
- [x] Run `uv run python manage.py test mecab_ko_dic.tests.MecabModelTest`.
- [x] Commit the focused test change.

## Task 2: Complete Django Admin coverage

**Files:**
- Modify: `mecab_ko_dic/tests_admin.py`
- Modify only if a test demonstrates a defect: `mecab_ko_dic/admin.py`

- [x] Add explicit search assertions for `표층형`, `품사_태그`, and `의미_부류`, retaining reading coverage.
- [x] Assert authorized staff can change and delete compound entries.
- [x] Run `uv run python manage.py test mecab_ko_dic.tests_admin`.
- [x] Commit the focused test change and any demonstrated minimal fix.

## Task 3: Verify and record completion

**Files:**
- Modify: `docs/superpowers/specs/2026-09-04-phase1-test-coverage-completion-design.md`
- Modify: `docs/superpowers/plans/2026-09-04-phase1-test-coverage-completion.md`

- [x] Run `uv run python manage.py migrate`.
- [x] Run `uv run python manage.py test`.
- [x] Run `uv run ruff check .`.
- [x] Run `uv run python manage.py check`.
- [x] Run `uv run python manage.py makemigrations --check --dry-run`.
- [x] Run `git diff --check` and inspect `git status --short`.
- [x] Mark this design and plan completed only after all checks pass.
- [x] Commit the completion record.
