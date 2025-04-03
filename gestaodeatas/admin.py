from django.contrib import admin
from .models import AtaRegistroPreco, ItemDaAta

class ItemDaAtaInline(admin.TabularInline):
    model = ItemDaAta
    extra = 1

class AtaRegistroPrecoAdmin(admin.ModelAdmin):
    inlines = [ItemDaAtaInline]
    list_display = ['numero_ata', 'hospital', 'vigencia_inicio', 'vigencia_fim']
    search_fields = ['numero_ata', 'hospital', 'edital', 'numero_sei']

admin.site.register(AtaRegistroPreco, AtaRegistroPrecoAdmin)
