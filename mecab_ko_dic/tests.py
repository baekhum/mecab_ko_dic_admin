from django.test import TestCase
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

    def test_stopword(self):
        sw = Stopword.objects.create(word="그리고")
        self.assertEqual(sw.word, "그리고")
