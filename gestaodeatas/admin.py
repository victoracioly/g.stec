from django.contrib import admin
from .models import AtaRegistroPreco

# === Configuração para Visualização das Atas de Registro de Preço ===
class AtaRegistroPrecoAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na listagem
    list_display = [
        'numero_ata', 
        'hospital', 
        'vigencia_inicio', 
        'vigencia_fim', 
        'status',
        'data_assinatura', 
        'data_publicacao_pncp'
    ]

    # Campos pelos quais você pode buscar no admin
    search_fields = [
        'numero_ata', 
        'hospital', 
        'edital', 
        'numero_sei'
    ]

    # Adicionando filtro lateral para facilitar busca por status
    list_filter = [
        'status',
        'hospital',
        'vigencia_inicio',
        'vigencia_fim',
        'data_assinatura',
        'data_publicacao_pncp'
    ]

    # Ordenação padrão por vigência final
    ordering = ['vigencia_fim']

# === Registro dos modelos no admin ===
admin.site.register(AtaRegistroPreco, AtaRegistroPrecoAdmin)
