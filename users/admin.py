from django.contrib import admin
from .models import PerfilUsuario, Hospital

# Classe para customizar a visualização dos hospitais no Admin
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uasg', 'cnpj')
    search_fields = ('nome', 'uasg', 'cnpj')
    list_filter = ('nome',)

# Classe para visualizar os Perfis de Usuário no Admin
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_nome_completo', 'get_email', 'role', 'cargo', 'hospital')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__email', 'hospital__nome')
    list_filter = ('role', 'cargo')

    def get_nome_completo(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip() or obj.usuario.username
    get_nome_completo.short_description = 'Nome Completo'

    def get_email(self, obj):
        return obj.usuario.email
    get_email.short_description = 'E-mail'
