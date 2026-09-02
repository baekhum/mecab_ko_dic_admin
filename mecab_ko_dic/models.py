from django.core.exceptions import ValidationError
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
    NA = "NA", "미정의"
    UNA = "UNA", "해석불가"
    VSV = "VSV", "동사 파생 접미사(V)"


def validate_pos_tag(value):
    invalid_tags = [tag for tag in value.split("+") if tag not in PosTag.values]
    if invalid_tags:
        raise ValidationError(
            "Unsupported POS tag: %(tags)s",
            code="invalid_pos_tag",
            params={"tags": ", ".join(invalid_tags)},
        )


class OriginType(models.TextChoices):
    SYSTEM = "SYSTEM", "시스템"
    USER = "USER", "사용자"
    COMPOUND = "COMPOUND", "복합명사"


class SemanticClass(models.TextChoices):
    # 주요 분류
    NONE = "*", "*"
    PERSON = "인명", "인명"
    LOCATION = "지명", "지명"
    PLACE = "장소", "장소"
    NUMBER = "수", "수"
    ACTION = "행위", "행위"
    ULTRON = "울트론", "울트론"

    # 세부 분류 및 특수 태그 (시트 및 DB 분석 결과 반영)
    COINED = "쉬도록", "쉬도록"
    SENTENCE_ADV = "문장부사", "문장부사"
    STATUS_CHANGE = "상태변화", "상태변화"
    STATIC_STATE = "정적사태", "정적사태"

    # MeCab 특수 분류 (~로 시작)
    T_NOUN = "~명사", "~명사"
    T_NUMERAL = "~수사", "~수사"
    T_NUM_EXPR = "~수표현", "~수표현"
    T_COUNTABLE = "~가산명사", "~가산명사"
    T_PROPER = "~고유명사", "~고유명사"
    T_SPACE = "~공간명사", "~공간명사"
    T_INSTITUTION = "~기관명사", "~기관명사"
    T_GROUP = "~단체명사", "~단체명사"
    T_EVENT = "~사건명사", "~사건명사"
    T_DETERMINER = "~수관형사", "~수관형사"
    T_TIME = "~시간명사", "~시간명사"
    T_PERSON_NOUN = "~인명명사", "~인명명사"
    T_HUMAN = "~인성명사", "~인성명사"
    T_PLACE_NOUN = "~장소명사", "~장소명사"
    T_NON_HUMAN = "~비인성명사", "~비인성명사"
    T_QUANT_DET = "~양수관형사", "~양수관형사"
    T_ARTIFACT = "~인공물명사", "~인공물명사"
    T_DEP_COUNTABLE = "~의존가산명사", "~의존가산명사"

    # 복합 부류
    SENT_TIME = "문장부사|시간부사", "문장부사|시간부사"
    SENT_MODAL = "문장부사|양상부사", "문장부사|양상부사"
    SENT_CONN = "문장부사|접속부사", "문장부사|접속부사"
    SENT_DEGREE = "문장부사|정도부사", "문장부사|정도부사"
    COMP_SPACE = "성분부사|공간부사", "성분부사|공간부사"
    COMP_NEG = "성분부사|부정부사", "성분부사|부정부사"
    COMP_TIME = "성분부사|시간부사", "성분부사|시간부사"
    COMP_MODAL = "성분부사|양태부사", "성분부사|양태부사"
    COMP_DEGREE = "성분부사|정도부사", "성분부사|정도부사"
    PLACE_TIME = "~장소명사|시간명사", "~장소명사|시간명사"


class Mecab_Ko_Dic(models.Model):
    표층형 = models.CharField(max_length=100, db_column="surface_form", db_index=True)
    품사_태그 = models.CharField(max_length=50, db_column="pos_tag", db_index=True, validators=[validate_pos_tag])
    의미_부류 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=SemanticClass.choices,
        default=SemanticClass.NONE,
        db_column="semantic_class",
        verbose_name="의미 부류",
    )
    종성_유무 = models.CharField(max_length=1, db_column="final_consonant")
    읽기 = models.CharField(max_length=100, db_column="reading", db_index=True)
    타입 = models.CharField(max_length=100, blank=True, null=True, db_column="type")
    첫번째_품사 = models.CharField(max_length=100, blank=True, null=True, db_column="first_pos")
    마지막_품사 = models.CharField(max_length=100, blank=True, null=True, db_column="last_pos")
    표현 = models.CharField(max_length=255, blank=True, null=True, db_column="expression")
    origin_type = models.CharField(
        max_length=10,
        choices=OriginType.choices,
        default=OriginType.SYSTEM,
        db_column="origin_type",
        db_index=True,
        verbose_name="출처",
    )
    is_active = models.BooleanField(default=True, db_column="is_active", db_index=True, verbose_name="활성 여부")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["표층형", "품사_태그"],
                name="unique_surface_pos",
            ),
            models.CheckConstraint(
                condition=models.Q(origin_type__in=OriginType.values),
                name="mecab_origin_type_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(종성_유무__in=["T", "F", "*"]),
                name="mecab_final_consonant_valid",
            ),
        ]

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
