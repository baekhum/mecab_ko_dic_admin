from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType, SynonymGroup, SynonymWord, Stopword

# Create your tests here.


class MecabModelTest(TestCase):
    def test_create_mecab_entry_with_origin(self):
        entry = Mecab_Ko_Dic.objects.create(
            표층형="테스트", 품사_태그="NNG", 종성_유무="T", 읽기="테스트", origin_type=OriginType.USER, is_active=True
        )
        self.assertEqual(entry.origin_type, "USER")
        self.assertTrue(entry.is_active)

    def test_rejects_invalid_origin_type(self):
        with self.assertRaises(IntegrityError):
            Mecab_Ko_Dic.objects.create(
                표층형="잘못된 출처",
                품사_태그="NNG",
                종성_유무="T",
                읽기="잘못된 출처",
                origin_type="INVALID",
            )

    def test_rejects_invalid_final_consonant(self):
        with self.assertRaises(IntegrityError):
            Mecab_Ko_Dic.objects.create(
                표층형="잘못된 종성",
                품사_태그="NNG",
                종성_유무="X",
                읽기="잘못된 종성",
            )

    def test_model_validation_rejects_invalid_pos_tag(self):
        entry = Mecab_Ko_Dic(
            표층형="잘못된 품사",
            품사_태그="INVALID",
            종성_유무="T",
            읽기="잘못된 품사",
        )

        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_model_validation_accepts_compound_pos_tag(self):
        entry = Mecab_Ko_Dic(
            표층형="복합 품사",
            품사_태그="NNG+NNG",
            종성_유무="T",
            읽기="복합 품사",
        )

        entry.full_clean()

    def test_search_and_filter_fields_are_indexed(self):
        indexed_fields = ["표층형", "품사_태그", "읽기", "origin_type", "is_active"]

        for field_name in indexed_fields:
            with self.subTest(field=field_name):
                self.assertTrue(Mecab_Ko_Dic._meta.get_field(field_name).db_index)


class SearchDicTest(TestCase):
    def test_synonym_group_and_words(self):
        group = SynonymGroup.objects.create(name="휴대폰 그룹")
        SynonymWord.objects.create(group=group, word="휴대폰")
        SynonymWord.objects.create(group=group, word="핸드폰")
        self.assertEqual(group.words.count(), 2)

    def test_synonym_group_unique_name(self):
        SynonymGroup.objects.create(name="유니크 그룹")
        with self.assertRaises(IntegrityError):
            SynonymGroup.objects.create(name="유니크 그룹")

    def test_synonym_word_unique_together(self):
        group = SynonymGroup.objects.create(name="그룹")
        SynonymWord.objects.create(group=group, word="단어")
        with self.assertRaises(IntegrityError):
            SynonymWord.objects.create(group=group, word="단어")

    def test_synonym_group_cascade_delete(self):
        group = SynonymGroup.objects.create(name="삭제그룹")
        SynonymWord.objects.create(group=group, word="삭제단어")
        word_id = SynonymWord.objects.get(word="삭제단어").id
        group.delete()
        self.assertFalse(SynonymWord.objects.filter(id=word_id).exists())

    def test_stopword(self):
        sw = Stopword.objects.create(word="그리고")
        self.assertEqual(sw.word, "그리고")

    def test_stopword_unique(self):
        Stopword.objects.create(word="불용어")
        with self.assertRaises(IntegrityError):
            Stopword.objects.create(word="불용어")
