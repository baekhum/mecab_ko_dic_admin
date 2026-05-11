import csv
import io
import zipfile
from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.urls import path
from .models import Mecab_Ko_Dic, SynonymGroup, SynonymWord, Stopword, OriginType

class OriginTypeFilter(admin.SimpleListFilter):
    title = '출처/타입'
    parameter_name = 'origin_type_custom'

    def lookups(self, request, model_admin):
        return (
            ('SYSTEM', '시스템'),
            ('USER', '사용자'),
            ('COMPOUND', '복합명사'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'SYSTEM':
            return queryset.filter(origin_type='SYSTEM').exclude(타입='Compound')
        if self.value() == 'USER':
            return queryset.filter(origin_type='USER').exclude(타입='Compound')
        if self.value() == 'COMPOUND':
            return queryset.filter(models.Q(타입='Compound') | models.Q(origin_type='COMPOUND'))
        return queryset

@admin.register(Mecab_Ko_Dic)
class Mecab_Ko_Dic_Admin(admin.ModelAdmin):
    list_display = ('id', '표층형', '품사_태그', '읽기', 'origin_type', 'is_active', '의미_부류', '종성_유무', '타입')
    list_display_links = ('id', '표층형')
    list_filter = (OriginTypeFilter, '품사_태그', 'is_active')
    search_fields = ('표층형', '읽기', '품사_태그', '의미_부류')
    list_per_page = 50
    ordering = ['-id']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-user-dic-bundle/', self.admin_site.admin_view(self.export_user_dic_zip), name='mecab_ko_dic_export_user_dic_bundle'),
        ]
        return custom_urls + urls

    def export_user_dic_zip(self, request):
        """사용자 사전을 지명, 인명, 기타(NNP)로 분류하여 ZIP으로 다운로드"""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zf:
            # 1. 지명 (place)
            place_qs = Mecab_Ko_Dic.objects.filter(origin_type=OriginType.USER, 의미_부류__icontains='지명')
            zf.writestr('user-place.csv', self._generate_csv_content(place_qs))
            
            # 2. 인명 (person)
            person_qs = Mecab_Ko_Dic.objects.filter(origin_type=OriginType.USER, 의미_부류__icontains='인명')
            zf.writestr('user-person.csv', self._generate_csv_content(person_qs))
            
            # 3. 기타 (NNP 등 - 지명/인명 제외한 모든 사용자 사전)
            other_qs = Mecab_Ko_Dic.objects.filter(origin_type=OriginType.USER).exclude(의미_부류__icontains='지명').exclude(의미_부류__icontains='인명')
            zf.writestr('user-nnp.csv', self._generate_csv_content(other_qs))
            
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="user-dictionary-bundle.zip"'
        return response

    def _generate_csv_content(self, queryset):
        """Queryset을 MeCab CSV 형식의 문자열로 변환"""
        output = io.StringIO()
        writer = csv.writer(output)
        for entry in queryset:
            writer.writerow([
                entry.표층형,
                "0", "0", "0",
                entry.품사_태그,
                entry.의미_부류 or "*",
                entry.종성_유무 or "*",
                entry.읽기 or entry.표층형,
                entry.타입 or "*",
                entry.첫번째_품사 or "*",
                entry.마지막_품사 or "*",
                entry.표현 or "*"
            ])
        return output.getvalue()

    def get_readonly_fields(self, request, obj=None):
        # 시스템 사전인 경우 모든 필드를 읽기 전용으로 설정
        if obj and obj.origin_type == 'SYSTEM':
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def has_delete_permission(self, request, obj=None):
        # 시스템 사전인 경우 삭제 불가
        if obj and obj.origin_type == 'SYSTEM':
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        # 시스템 사전인 경우 수정 권한 제한 (조회는 가능)
        if obj and obj.origin_type == 'SYSTEM':
            return False
        return super().has_change_permission(request, obj)

class SynonymWordInline(admin.TabularInline):
    model = SynonymWord
    extra = 1

@admin.register(SynonymGroup)
class SynonymGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'words_count')
    search_fields = ('name', 'words__word')
    inlines = [SynonymWordInline]
    ordering = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            words_count=models.Count('words')
        )

    def words_count(self, obj):
        return obj.words_count
    words_count.short_description = '단어 수'
    words_count.admin_order_field = 'words_count'

@admin.register(Stopword)
class StopwordAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ('word',)
    ordering = ['word']
