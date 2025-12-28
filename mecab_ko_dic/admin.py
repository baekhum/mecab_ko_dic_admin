from django.contrib import admin
from .models import Mecab_Ko_Dic

@admin.register(Mecab_Ko_Dic)
class Mecab_Ko_Dic_Admin(admin.ModelAdmin):
    list_display = ('표층형', '품사_태그', '의미_부류', '종성_유무', '읽기', '타입', '첫번째_품사', '마지막_품사', '표현')
    search_fields = ('표층형', '품사_태그', '의미_부류', '읽기')
