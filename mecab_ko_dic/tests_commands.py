import os
import tempfile
from django.core.management import call_command, CommandError
from django.test import TestCase
from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType


class ImportMecabCsvTest(TestCase):
    def test_import_mecab_csv(self):
        # Create a sample CSV
        # 0:표층형, 1:LID, 2:RID, 3:Cost, 4:품사_태그, 5:의미_부류, 6:종성_유무, 7:읽기, 8:타입, 9:첫번째_품사, 10:마지막_품사, 11:표현
        csv_content = (
            "가나다,0,0,0,NNG,*,T,가나다,*,*,*,*\n"
            "라마바,0,0,0,NNP,인명,F,라마바,Preanalysis,NNP,NNP,라마/NNP/*+바/NNP/*\n"
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_content)
            tmp_file_path = f.name

        try:
            call_command("import_mecab_csv", tmp_file_path, type="USER")

            self.assertEqual(Mecab_Ko_Dic.objects.count(), 2)

            entry1 = Mecab_Ko_Dic.objects.get(표층형="가나다")
            self.assertEqual(entry1.품사_태그, "NNG")
            self.assertEqual(entry1.의미_부류, "*")
            self.assertEqual(entry1.종성_유무, "T")
            self.assertEqual(entry1.읽기, "가나다")
            self.assertEqual(entry1.타입, "*")
            self.assertEqual(entry1.origin_type, OriginType.USER)

            entry2 = Mecab_Ko_Dic.objects.get(표층형="라마바")
            self.assertEqual(entry2.품사_태그, "NNP")
            self.assertEqual(entry2.의미_부류, "인명")
            self.assertEqual(entry2.종성_유무, "F")
            self.assertEqual(entry2.읽기, "라마바")
            self.assertEqual(entry2.타입, "Preanalysis")
            self.assertEqual(entry2.표현, "라마/NNP/*+바/NNP/*")
            self.assertEqual(entry2.origin_type, OriginType.USER)

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_import_malformed_csv(self):
        # Line 1: Good
        # Line 2: Missing fields (less than 5)
        # Line 3: pos_tag too long (> 4 chars)
        # Line 4: Invalid pos_tag (not in PosTag choices)
        csv_content = (
            "정상,0,0,0,NNG,*,T,정상,*,*,*,*\n"
            "오류1,0,0,0\n"
            "오류2,0,0,0,TOOLONG,*,T,오류2,*,*,*,*\n"
            "오류3,0,0,0,ZZZ,*,T,오류3,*,*,*,*\n"
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_content)
            tmp_file_path = f.name

        try:
            with self.assertRaises(CommandError) as cm:
                call_command("import_mecab_csv", tmp_file_path)
            
            self.assertIn("Import failed with 3 errors", str(cm.exception))
            # Due to transaction.atomic, no records should be saved
            self.assertEqual(Mecab_Ko_Dic.objects.count(), 0)

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_import_with_encoding(self):
        # Test importing with EUC-KR encoding
        csv_content = "한글,0,0,0,NNG,*,T,한글,*,*,*,*\n"
        
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
            f.write(csv_content.encode("euc-kr"))
            tmp_file_path = f.name

        try:
            # Should fail with utf-8 (default)
            with self.assertRaises(CommandError):
                call_command("import_mecab_csv", tmp_file_path, encoding="utf-8")
            
            # Should succeed with euc-kr
            call_command("import_mecab_csv", tmp_file_path, encoding="euc-kr")
            self.assertEqual(Mecab_Ko_Dic.objects.count(), 1)
            self.assertEqual(Mecab_Ko_Dic.objects.get().표층형, "한글")

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
