from django.contrib import admin
from .models import Dashboard, Hospital

# Classe para customizar a visualização dos hospitais no Admin
@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uasg', 'cnpj')
    search_fields = ('nome', 'uasg', 'cnpj')
    list_filter = ('nome',)

#  Registrando o Dashboard no Admin
@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'role', 'hospital')
    search_fields = ('usuario__username', 'hospital__nome')
    list_filter = ('role',)
