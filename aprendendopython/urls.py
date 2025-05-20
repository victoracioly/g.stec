# aprendendopython/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), #responsável por acessar o painel administrativo do Django.
    path('', include('gestaodeatas.urls')),  # Todas as rotas do app gestaodeatas.
    path('users/', include('users.urls')), # Todas as rotas do app users.
    path('', include('monitoramento_pncp.urls')),
]