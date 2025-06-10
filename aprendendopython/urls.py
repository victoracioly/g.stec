# aprendendopython/urls.py

from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    # Página inicial do sistema - redireciona para o dashboard principal
    path('', home, name='home'),

    # Acesso ao painel administrativo padrão do Django
    path('admin/', admin.site.urls),

    # Rotas do aplicativo de usuários (autenticação, permissões, dashboards e gestão de hospitais)
    path('users/', include('users.urls', namespace='users')),

    # Funcionalidades relacionadas à consulta de dispositivos médicos registrados na ANVISA
    path('dispositivos-medicos-anvisa/', include('dispositivos_medicos_anvisa.urls')),

    # Funcionalidades de gestão das atas de registro de preços vigentes
    path('gestaodeatas/', include('gestaodeatas.urls')),

    # Monitoramento das publicações no PNCP (Portal Nacional de Contratações Públicas)
    path('monitoramento/', include(('monitoramento_pncp.urls', 'monitoramento_pncp'), namespace='monitoramento_pncp')),
]
