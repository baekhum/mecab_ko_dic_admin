# Phase 1 Test Coverage Completion Design

**Status:** Completed on 2026-09-04. Implementation commits: `d71cff0`, `432df4d`.

## Context

Phase 1 dictionary management is functionally implemented and its full verification suite passes. A final requirements audit found three behaviors that are implemented but not directly protected by tests:

- duplicate `Mecab_Ko_Dic` rows with the same `(표층형, 품사_태그)` pair must be rejected;
- Django Admin search must cover `표층형`, `읽기`, `품사_태그`, and `의미_부류`;
- authorized staff must be able to change and delete both user and compound entries, while system entries remain protected.

This follow-up closes those evidence gaps without expanding Phase 1 behavior.

## Goals

- Add a direct database-boundary regression test for the dictionary identity constraint.
- Add explicit Admin search coverage for every promised search field.
- Add explicit Admin permission coverage for compound entries.
- Re-run the complete Phase 1 verification suite and record completion.

## Non-goals

- No model, migration, import-command, or Admin refactor unless a new test demonstrates a defect.
- No new dictionary feature, UI behavior, or search semantics.
- No change to the `(표층형, 품사_태그)` identity contract.

## Design

### Dictionary identity coverage

Create one dictionary entry and assert that inserting another entry with the same `표층형` and `품사_태그` raises `IntegrityError`. Keep the assertion at the database boundary so it verifies the existing `UniqueConstraint`, not duplicated validation logic.

### Admin search coverage

Use the existing Admin changelist helper and fixture entries. Exercise each configured search field with a value that selects exactly one record. Preserve the existing reading-search assertion and add surface-form, POS-tag, and semantic-class cases.

### Admin permission coverage

Extend the existing system-entry permission test or add a focused companion test. Assert that the compound fixture has both change and delete permission for the authorized staff user, matching the existing user-entry behavior.

### Verification and status

Run focused tests after each test-only change, then run migrations, the full Django suite, Ruff, Django system checks, migration drift checks, and diff checks. Once all checks pass, mark this design and its implementation plan completed. The original Phase 1 documents remain completed; this document is a narrowly scoped follow-up.

## Commit boundaries

1. Add this design and its execution plan.
2. Add dictionary uniqueness coverage.
3. Complete Django Admin search and permission coverage.
4. Record verified completion in the follow-up documents.
