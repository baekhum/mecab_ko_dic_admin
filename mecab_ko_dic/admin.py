from django.contrib import admin
from django.db import models
from .models import Mecab_Ko_Dic, SynonymGroup, SynonymWord, Stopword

@admin.register(Mecab_Ko_Dic)
class Mecab_Ko_Dic_Admin(admin.ModelAdmin):
    list_display = ('표층형', '품사_태그', '읽기', 'origin_type', 'is_active', '의미_부류', '종성_유무', '타입')
    list_filter = ('origin_type', '품사_태그', 'is_active')
    search_fields = ('표층형', '읽기', '품사_태그', '의미_부류')
    list_per_page = 50
    ordering = ['표층형']

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
