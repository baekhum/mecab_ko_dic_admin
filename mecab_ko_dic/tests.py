from django.test import TestCase
from mecab_ko_dic.models import Mecab_Ko_Dic

# Create your tests here.

class MecabModelTest(TestCase):
    def test_create_mecab_entry_with_origin(self):
        # Note: OriginType and the new fields don't exist yet, so this should fail.
        from mecab_ko_dic.models import OriginType
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
