from django.contrib import admin
from .models import Mecab_Ko_Dic, SynonymGroup, SynonymWord, Stopword

@admin.register(Mecab_Ko_Dic)
class Mecab_Ko_Dic_Admin(admin.ModelAdmin):
    list_display = ('표층형', '품사_태그', '읽기', 'origin_type', 'is_active', '의미_부류', '종성_유무', '타입')
    list_filter = ('origin_type', '품사_태그', 'is_active')
    search_fields = ('표층형', '읽기', '품사_태그', '의미_부류')
    list_per_page = 50

class SynonymWordInline(admin.TabularInline):
    model = SynonymWord
    extra = 1

@admin.register(SynonymGroup)
class SynonymGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'get_words_count')
    search_fields = ('name', 'words__word')
    inlines = [SynonymWordInline]

    def get_words_count(self, obj):
        return obj.words.count()
    get_words_count.short_description = '단어 수'

@admin.register(Stopword)
class StopwordAdmin(admin.ModelAdmin):
    list_display = ('word',)
    search_fields = ('word',)
