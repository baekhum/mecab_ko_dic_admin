# Phase 1: Dictionary Management Active Implementation Plan

> **Execution rule:** Work task-by-task using test-driven development. Do not recreate existing models, commands, or migrations merely because they appear in the historical Phase 1 scope. Verify the current baseline first and implement only demonstrated gaps.

**Goal:** Verify and complete the Phase 1 dictionary-management contract for MeCab entries, synonyms, stopwords, CSV import, and Django Admin.

**Architecture:** Keep the unified `Mecab_Ko_Dic` model and dedicated synonym/stopword models. Treat `(표층형, 품사_태그)` as the global import identity, use transactional UPSERT for CSV ingestion, and enforce behavior through database constraints and focused tests.

**Tech Stack:** Python 3.12, Django 5.2 LTS, PostgreSQL 17, uv, Django test runner, Ruff.

**Design:** `docs/superpowers/specs/2026-05-09-phase1-dictionary-management-design.md`

---

### Task 0: Satisfy runtime prerequisite

**Files:**
- Follow: `docs/superpowers/plans/2026-08-30-python-django-version-alignment.md`
- Verify: `.python-version`, `pyproject.toml`, `uv.lock`

- [ ] **Step 1: Verify the selected runtime**

Run:

```bash
uv run python --version
uv run python -m django --version
```

Expected: Python 3.12.x and Django 5.2.x.

- [ ] **Step 2: Resolve a failed prerequisite**

If either version is outside the required range, stop this plan and execute `docs/superpowers/plans/2026-08-30-python-django-version-alignment.md`. Resume Phase 1 only after both version checks pass.

### Task 1: Establish the verified implementation baseline

**Files:**
- Verify: `mecab_ko_dic/models.py`
- Verify: `mecab_ko_dic/admin.py`
- Verify: `mecab_ko_dic/management/commands/import_mecab_csv.py`
- Verify: `mecab_ko_dic/tests.py`
- Verify: `mecab_ko_dic/tests_commands.py`
- Verify: `mecab_ko_dic/migrations/`

- [ ] **Step 1: Verify Django model and migration consistency**

Run:

```bash
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py showmigrations mecab_ko_dic
```

Expected: no model changes are missing from migrations; all expected app migrations are listed.

- [ ] **Step 2: Run the focused baseline tests**

Run:

```bash
uv run python manage.py test mecab_ko_dic.tests mecab_ko_dic.tests_commands
```

Expected: the existing model and import tests pass. A failure becomes the first gap to fix; do not proceed by assuming the baseline is valid.

- [ ] **Step 3: Record the baseline result**

In the implementation change description, record the commands, pass/fail result, and any gap mapped to the design section it violates. Do not create a source-code commit when verification produces no changes.

### Task 2: Complete model validation and database guarantees

**Files:**
- Modify if required: `mecab_ko_dic/models.py`
- Create if required: the next migration reported by `makemigrations`
- Modify: `mecab_ko_dic/tests.py`

- [ ] **Step 1: Add failing tests for uncovered invariants**

Cover at minimum:

- invalid `origin_type` rejection at the database or model-validation boundary;
- invalid `종성_유무` rejection for values outside `T`, `F`, `*`;
- duplicate `(표층형, 품사_태그)` rejection;
- unique synonym group names and group-local synonym words;
- synonym cascade deletion and unique stopwords;
- required indexes on `표층형`, `품사_태그`, `읽기`, `origin_type`, and `is_active`.

Run the new tests and confirm they fail for the missing behavior rather than an unrelated setup error.

- [ ] **Step 2: Implement only the missing constraints or validators**

Prefer database constraints for finite-value and uniqueness rules. Keep validation definitions close to the owning model and use stable, descriptive constraint names.

- [ ] **Step 3: Generate and inspect the migration**

Run:

```bash
uv run python manage.py makemigrations mecab_ko_dic
git diff -- mecab_ko_dic/migrations
uv run python manage.py migrate
```

Inspect the SQL for unintended table rebuilds, dropped constraints, or destructive data conversions.

- [ ] **Step 4: Verify and commit the complete schema change**

Run:

```bash
uv run python manage.py test mecab_ko_dic.tests
uv run python manage.py makemigrations --check --dry-run
```

Commit `models.py`, its tests, and every generated migration in the same commit. If no implementation gap exists, make no commit for this task.

### Task 3: Complete the CSV import contract

**Files:**
- Modify if required: `mecab_ko_dic/management/commands/import_mecab_csv.py`
- Modify: `mecab_ko_dic/tests_commands.py`
- Add: `mecab_ko_dic/testdata/mecab_sample.csv`

- [ ] **Step 1: Add failing contract tests**

Use temporary files except for the committed representative fixture. Cover:

- a valid 12-column UTF-8 import;
- `--encoding=euc-kr`;
- invalid column count, POS tag, final-consonant value, empty required values, type, and batch size;
- file-not-found and decode failures;
- all-or-nothing rollback when any row is invalid;
- duplicate keys inside one batch, across batches, and against existing rows;
- last-row-wins semantics for duplicates within a file;
- UPSERT updates dictionary attributes and `origin_type` while preserving `is_active`;
- a second import of the same file does not increase row count;
- actionable summary and error output.

Run each new test before implementation and confirm the expected contract failure.

- [ ] **Step 2: Implement the smallest changes needed**

Retain `transaction.atomic()` around the complete file import. Validate rows before committing, deduplicate by `(표층형, 품사_태그)`, and use Django bulk UPSERT with explicit `unique_fields` and `update_fields`. Do not include `is_active` in `update_fields`.

- [ ] **Step 3: Run focused command tests**

Run:

```bash
uv run python manage.py test mecab_ko_dic.tests_commands
```

Expected: all normal, duplicate, encoding, and rollback paths pass.

- [ ] **Step 4: Verify a representative import**

Run the committed fixture twice against the test or disposable development database:

```bash
uv run python manage.py import_mecab_csv mecab_ko_dic/testdata/mecab_sample.csv --type SYSTEM
uv run python manage.py import_mecab_csv mecab_ko_dic/testdata/mecab_sample.csv --type SYSTEM
```

Confirm the second run does not increase the number of rows for the fixture keys. Do not use the full external MeCab corpus as an automated completion test.

- [ ] **Step 5: Commit the import contract**

Commit the command, tests, and fixture together. If all contract tests already pass without implementation changes, commit only newly added tests and the fixture.

### Task 4: Verify and complete Django Admin behavior

**Files:**
- Modify if required: `mecab_ko_dic/admin.py`
- Add or modify: `mecab_ko_dic/tests_admin.py`

- [ ] **Step 1: Add failing Admin tests**

Cover:

- filters for origin, POS tag, and active state;
- searches over surface form, reading, POS tag, and semantic class;
- system entries cannot be changed or deleted through Admin;
- user and compound entries remain editable for authorized staff;
- synonym words are managed through `SynonymGroupAdmin` inline;
- stopwords are searchable.

- [ ] **Step 2: Implement only demonstrated gaps**

Keep custom filters and permission logic isolated in named Admin classes. Avoid changing model behavior from Admin code.

- [ ] **Step 3: Verify and commit**

Run:

```bash
uv run python manage.py test mecab_ko_dic.tests_admin
```

Commit `admin.py` and `tests_admin.py` together. If existing behavior already satisfies the contract, add the missing tests without rewriting the Admin implementation.

### Task 5: Full verification and completion record

**Files:**
- Verify only unless a failure demonstrates an in-scope defect

- [ ] **Step 1: Apply migrations and run all checks**

Run:

```bash
uv run python manage.py migrate
uv run python manage.py test
uv run ruff check .
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
```

Expected: every command exits successfully, all tests pass, and Django reports no pending model changes.

- [ ] **Step 2: Review the final diff**

Run:

```bash
git diff --check
git status --short
```

Confirm that only Phase 1 files and pre-existing unrelated changes appear. Do not stage unrelated files.

- [ ] **Step 3: Update document status after verified completion**

Only after every check above passes, change the design status from `Active` to `Completed`, add the completion date and implementation commit references, and mark this plan's completed checkboxes. Until then, keep both documents active.
