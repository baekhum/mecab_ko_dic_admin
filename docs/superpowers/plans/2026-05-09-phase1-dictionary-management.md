# Phase 1: Dictionary Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust dictionary management system that handles MeCab system/user dictionaries, synonyms, and stopwords.

**Architecture:** Use a unified Django model for MeCab entries with origin type flags, dedicated models for synonym groups and words, and a management command for high-speed CSV imports.

**Tech Stack:** Python 3.12, Django 5.1, PostgreSQL 17.

---

### Task 1: Extend MeCab Dictionary Model

**Files:**
- Modify: `mecab_ko_dic/models.py`
- Test: `mecab_ko_dic/tests.py`

- [ ] **Step 1: Write test for new model fields**
```python
from django.test import TestCase
from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType

class MecabModelTest(TestCase):
    def test_create_mecab_entry_with_origin(self):
        entry = Mecab_Ko_Dic.objects.create(
            표층형="테스트",
            품사_태그="NNG",
            종성_유무="T",
            읽기="테스트",
            origin_type=OriginType.USER,
            is_active=True
        )
        self.assertEqual(entry.origin_type, "USER")
        self.assertTrue(entry.is_active)
```

- [ ] **Step 2: Run test to verify failure**
Run: `uv run python manage.py test mecab_ko_dic.tests.MecabModelTest.test_create_mecab_entry_with_origin`
Expected: FAIL (ImportError or AttributeError)

- [ ] **Step 3: Implement model changes**
```python
class OriginType(models.TextChoices):
    SYSTEM = "SYSTEM", "시스템"
    USER = "USER", "사용자"
    COMPOUND = "COMPOUND", "복합명사"

class Mecab_Ko_Dic(models.Model):
    # ... existing fields ...
    origin_type = models.CharField(max_length=10, choices=OriginType.choices, default=OriginType.SYSTEM)
    is_active = models.BooleanField(default=True)
```

- [ ] **Step 4: Run migrations and verify test passes**
Run: `just makemigrations && just migrate && uv run python manage.py test mecab_ko_dic.tests.MecabModelTest.test_create_mecab_entry_with_origin`
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add mecab_ko_dic/models.py
git commit -m "feat: add origin_type and is_active to Mecab_Ko_Dic"
```

---

### Task 2: Implement Synonym and Stopword Models

**Files:**
- Modify: `mecab_ko_dic/models.py`
- Test: `mecab_ko_dic/tests.py`

- [ ] **Step 1: Write tests for Synonym and Stopword**
```python
from mecab_ko_dic.models import SynonymGroup, SynonymWord, Stopword

class SearchDicTest(TestCase):
    def test_synonym_group_and_words(self):
        group = SynonymGroup.objects.create(name="휴대폰 그룹")
        SynonymWord.objects.create(group=group, word="휴대폰")
        SynonymWord.objects.create(group=group, word="핸드폰")
        self.assertEqual(group.words.count(), 2)

    def test_stopword(self):
        sw = Stopword.objects.create(word="그리고")
        self.assertEqual(sw.word, "그리고")
```

- [ ] **Step 2: Run tests to verify failure**
Run: `uv run python manage.py test mecab_ko_dic.tests.SearchDicTest`
Expected: FAIL

- [ ] **Step 3: Implement models**
```python
class SynonymGroup(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class SynonymWord(models.Model):
    group = models.ForeignKey(SynonymGroup, related_name='words', on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    def __str__(self): return self.word

class Stopword(models.Model):
    word = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.word
```

- [ ] **Step 4: Run migrations and verify tests pass**
Expected: PASS

- [ ] **Step 5: Commit**
```bash
git add mecab_ko_dic/models.py
git commit -m "feat: add Synonym and Stopword models"
```

---

### Task 3: CSV Import Management Command

**Files:**
- Create: `mecab_ko_dic/management/commands/import_mecab_csv.py`
- Test: `mecab_ko_dic/tests.py`

- [ ] **Step 1: Write test for import command**
```python
from django.core.management import call_command
import io

class ImportCommandTest(TestCase):
    def test_import_csv(self):
        csv_content = "테스트,0,0,0,NNG,*,T,테스트,*,*,*,*\n"
        with open("test_import.csv", "w") as f: f.write(csv_content)
        call_command('import_mecab_csv', 'test_import.csv', '--type', 'USER')
        self.assertTrue(Mecab_Ko_Dic.objects.filter(표층형="테스트").exists())
```

- [ ] **Step 2: Implement command logic**
Use `csv` module and `Mecab_Ko_Dic.objects.bulk_create` for performance.

- [ ] **Step 3: Verify with real MeCab source**
Run: `just run-import-system` (Add this recipe to Justfile later or run manually).

---

### Task 4: Advanced Django Admin UI

**Files:**
- Modify: `mecab_ko_dic/admin.py`

- [ ] **Step 1: Enhance Mecab_Ko_Dic Admin**
Add `list_filter` for `origin_type`, `품사_태그`, `is_active`.
Add `search_fields` for `표층형`, `읽기`.

- [ ] **Step 2: Add Synonym Inline**
Use `TabularInline` to manage `SynonymWord` inside `SynonymGroupAdmin`.

- [ ] **Step 3: Commit**
```bash
git add mecab_ko_dic/admin.py
git commit -m "feat: enhance Django Admin for dictionary management"
```
