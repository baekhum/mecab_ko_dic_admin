from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from mecab_ko_dic.admin import Mecab_Ko_Dic_Admin, StopwordAdmin, SynonymGroupAdmin, SynonymWordInline
from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType, Stopword, SynonymGroup


class MecabDictionaryAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        cls.system_entry = Mecab_Ko_Dic.objects.create(
            표층형="시스템단어",
            품사_태그="NNG",
            종성_유무="T",
            읽기="시스템읽기",
            origin_type=OriginType.SYSTEM,
        )
        cls.user_entry = Mecab_Ko_Dic.objects.create(
            표층형="사용자단어",
            품사_태그="NNP",
            종성_유무="F",
            읽기="검색대상",
            의미_부류="사용자의미",
            origin_type=OriginType.USER,
        )
        cls.compound_entry = Mecab_Ko_Dic.objects.create(
            표층형="복합단어",
            품사_태그="NNG+NNG",
            종성_유무="T",
            읽기="복합단어",
            origin_type=OriginType.COMPOUND,
        )

    def setUp(self):
        self.client.force_login(self.staff_user)

    def changelist_results(self, **params):
        response = self.client.get(reverse("admin:mecab_ko_dic_mecab_ko_dic_changelist"), params)
        self.assertEqual(response.status_code, 200)
        return list(response.context["cl"].queryset)

    def test_filters_entries_by_origin(self):
        results = self.changelist_results(origin_type_custom=OriginType.USER)

        self.assertEqual(results, [self.user_entry])

    def test_filters_entries_by_pos_and_active_state(self):
        self.user_entry.is_active = False
        self.user_entry.save(update_fields=["is_active"])

        results = self.changelist_results(품사_태그="NNP", is_active="0")

        self.assertEqual(results, [self.user_entry])

    def test_searches_reading(self):
        results = self.changelist_results(q="검색대상")

        self.assertEqual(results, [self.user_entry])

    def test_searches_surface_form(self):
        results = self.changelist_results(q="사용자단어")

        self.assertEqual(results, [self.user_entry])

    def test_searches_pos_tag(self):
        results = self.changelist_results(q="NNP")

        self.assertEqual(results, [self.user_entry])

    def test_searches_semantic_class(self):
        results = self.changelist_results(q="사용자의미")

        self.assertEqual(results, [self.user_entry])

    def test_system_entry_is_read_only_and_cannot_be_deleted(self):
        model_admin = Mecab_Ko_Dic_Admin(Mecab_Ko_Dic, admin.site)
        request = RequestFactory().get("/admin/")
        request.user = self.staff_user

        self.assertFalse(model_admin.has_change_permission(request, self.system_entry))
        self.assertFalse(model_admin.has_delete_permission(request, self.system_entry))
        self.assertEqual(
            model_admin.get_readonly_fields(request, self.system_entry),
            [field.name for field in Mecab_Ko_Dic._meta.fields],
        )
        self.assertTrue(model_admin.has_change_permission(request, self.user_entry))
        self.assertTrue(model_admin.has_delete_permission(request, self.user_entry))

    def test_compound_entry_can_be_changed_and_deleted(self):
        model_admin = Mecab_Ko_Dic_Admin(Mecab_Ko_Dic, admin.site)
        request = RequestFactory().get("/admin/")
        request.user = self.staff_user

        self.assertTrue(model_admin.has_change_permission(request, self.compound_entry))
        self.assertTrue(model_admin.has_delete_permission(request, self.compound_entry))


class SearchDictionaryAdminTest(TestCase):
    def test_synonym_words_are_managed_inline(self):
        model_admin = SynonymGroupAdmin(SynonymGroup, admin.site)

        self.assertIn(SynonymWordInline, model_admin.inlines)

    def test_stopwords_are_searchable(self):
        stopword_admin = StopwordAdmin(Stopword, admin.site)

        self.assertEqual(stopword_admin.search_fields, ("word",))
