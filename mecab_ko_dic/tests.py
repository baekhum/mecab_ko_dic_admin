from django.test import TestCase
from django.db.utils import IntegrityError
from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType, SynonymGroup, SynonymWord, Stopword

# Create your tests here.

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
