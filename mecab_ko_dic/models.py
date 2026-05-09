from django.db import models


class PosTag(models.TextChoices):
    NNG = "NNG", "일반 명사"
    NNP = "NNP", "고유 명사"
    NNB = "NNB", "의존 명사"
    NNBC = "NNBC", "단위를 나타내는 명사"
    NR = "NR", "수사"
    NP = "NP", "대명사"
    VV = "VV", "동사"
    VA = "VA", "형용사"
    VX = "VX", "보조 용언"
    VCP = "VCP", "긍정 지정사"
    VCN = "VCN", "부정 지정사"
    MM = "MM", "관형사"
    MAG = "MAG", "일반 부사"
    MAJ = "MAJ", "접속 부사"
    IC = "IC", "감탄사"
    JKS = "JKS", "주격 조사"
    JKC = "JKC", "보격 조사"
    JKG = "JKG", "관형격 조사"
    JKO = "JKO", "목적격 조사"
    JKB = "JKB", "부사격 조사"
    JKV = "JKV", "호격 조사"
    JKQ = "JKQ", "인용격 조사"
    JX = "JX", "보조사"
    JC = "JC", "접속 조사"
    EP = "EP", "선어말 어미"
    EF = "EF", "종결 어미"
    EC = "EC", "연결 어미"
    ETN = "ETN", "명사형 전성 어미"
    ETM = "ETM", "관형형 전성 어미"
    XPN = "XPN", "체언 접두사"
    XSN = "XSN", "명사 파생 접미사"
    XSV = "XSV", "동사 파생 접미사"
    XSA = "XSA", "형용사 파생 접미사"
    XR = "XR", "어근"
    SF = "SF", "마침표, 물음표, 느낌표"
    SE = "SE", "줄임표 …"
    SSO = "SSO", "여는 괄호 (, ["
    SSC = "SSC", "닫는 괄호 ), ]"
    SC = "SC", "구분자 , · / :"
    SY = "SY", "기호"
    SL = "SL", "외국어"
    SH = "SH", "한자"
    SN = "SN", "숫자"


class OriginType(models.TextChoices):
    SYSTEM = "SYSTEM", "시스템"
    USER = "USER", "사용자"
    COMPOUND = "COMPOUND", "복합명사"


class Mecab_Ko_Dic(models.Model):
    표층형 = models.CharField(max_length=100, db_column="surface_form")
    품사_태그 = models.CharField(max_length=4, choices=PosTag.choices, db_column="pos_tag")
    의미_부류 = models.CharField(max_length=100, blank=True, null=True, db_column="semantic_class")
    종성_유무 = models.CharField(max_length=1, db_column="final_consonant")
    읽기 = models.CharField(max_length=100, db_column="reading")
    타입 = models.CharField(max_length=100, blank=True, null=True, db_column="type")
    첫번째_품사 = models.CharField(max_length=100, blank=True, null=True, db_column="first_pos")
    마지막_품사 = models.CharField(max_length=100, blank=True, null=True, db_column="last_pos")
    표현 = models.CharField(max_length=255, blank=True, null=True, db_column="expression")
    origin_type = models.CharField(
        max_length=10,
        choices=OriginType.choices,
        default=OriginType.SYSTEM,
        db_column="origin_type",
    )
    is_active = models.BooleanField(default=True, db_column="is_active")

    def __str__(self):
        return self.표층형


class SynonymGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="그룹명", db_column="name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일", db_column="created_at")

    class Meta:
        db_table = "synonym_group"
        verbose_name = "동의어 그룹"
        verbose_name_plural = "동의어 그룹 목록"

    def __str__(self):
        return self.name


class SynonymWord(models.Model):
    group = models.ForeignKey(
        SynonymGroup,
        related_name="words",
        on_delete=models.CASCADE,
        db_column="group_id",
        verbose_name="동의어 그룹",
    )
    word = models.CharField(max_length=100, verbose_name="단어", db_column="word")

    class Meta:
        db_table = "synonym_word"
        verbose_name = "동의어 단어"
        verbose_name_plural = "동의어 단어 목록"
        unique_together = (("group", "word"),)

    def __str__(self):
        return self.word


class Stopword(models.Model):
    word = models.CharField(max_length=100, unique=True, verbose_name="불용어", db_column="word")

    class Meta:
        db_table = "stopword"
        verbose_name = "불용어"
        verbose_name_plural = "불용어 목록"

    def __str__(self):
        return self.word
