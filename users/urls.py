# users/urls.py
from django.urls import path
from .views import (
    redirecionar_dashboard,
    dashboard_stec,
    dashboard_sec,
    dashboard_ceo,
    gerar_pdf_ceo,
    monitoramento_pncp,
    lista_atas,
    monitoramento_pncp,
    # Novas Views para Hospitais
    listar_hospitais,
    criar_hospital,
    editar_hospital,
    excluir_hospital,
    vincular_hospital
)

urlpatterns = [
    # Redirecionamento dinâmico para o dashboard correto
    path('dashboard/', redirecionar_dashboard, name='redirecionar_dashboard'),
    
    # Dashboards específicos
    path('dashboard/stec/', dashboard_stec, name='dashboard_stec'),
    path('dashboard/sec/', dashboard_sec, name='dashboard_sec'),
    path('dashboard/ceo/', dashboard_ceo, name='dashboard_ceo'),
    
    # Exportação de PDF do Dashboard do CEO
    path('dashboard/ceo/pdf/', gerar_pdf_ceo, name='gerar_pdf_ceo'),
    
    # Links para o Sidebar
    path('lista-atas/', lista_atas, name='lista_atas'),
    path('monitoramento-pncp/', monitoramento_pncp, name='monitoramento_pncp'),

    # CRUD de Hospitais
    path('hospitais/', listar_hospitais, name='listar_hospitais'),
    path('hospitais/novo/', criar_hospital, name='criar_hospital'),
    path('hospitais/editar/<int:id>/', editar_hospital, name='editar_hospital'),
    path('hospitais/excluir/<int:id>/', excluir_hospital, name='excluir_hospital'),
    path('hospitais/vincular/<int:id>/', vincular_hospital, name='vincular_hospital'),
]
