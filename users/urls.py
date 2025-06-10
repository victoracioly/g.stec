from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views.views_auth import registrar_usuario, login_usuario
from users.views.views_dashboard import (
    redirecionar_dashboard,
    dashboard_stec,
    dashboard_sec,
    dashboard_ceo,
    gerar_pdf_ceo,
    lista_atas,
    monitoramento_pncp,
)
from users.views.views_hospital import (
    listar_hospitais,
    criar_hospital,
    editar_hospital,
    excluir_hospital,
    vincular_hospital,
)
from users.views.views_htmx import (
    novo_usuario_inline,
    criar_usuario,
    pagina_usuarios,
    listar_usuarios,
)

app_name = 'users'  # Namespace obrigatório para uso com {% url 'users:name' %}

urlpatterns = [
    path('dashboard/', redirecionar_dashboard, name='redirecionar_dashboard'),
    path('dashboard/stec/', dashboard_stec, name='dashboard_stec'),
    path('dashboard/sec/', dashboard_sec, name='dashboard_sec'),
    path('dashboard/ceo/', dashboard_ceo, name='dashboard_ceo'),
    path('dashboard/ceo/pdf/', gerar_pdf_ceo, name='gerar_pdf_ceo'),

    path('lista-atas/', lista_atas, name='lista_atas'),
    path('monitoramento-pncp/', monitoramento_pncp, name='monitoramento_pncp'),

    path('hospitais/', listar_hospitais, name='listar_hospitais'),
    path('hospitais/novo/', criar_hospital, name='criar_hospital'),
    path('hospitais/editar/<int:id>/', editar_hospital, name='editar_hospital'),
    path('hospitais/excluir/<int:id>/', excluir_hospital, name='excluir_hospital'),
    path('hospitais/vincular/<int:id>/', vincular_hospital, name='vincular_hospital'),

    path('login/', login_usuario, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('cadastro/', registrar_usuario, name='cadastro'),

    # HTMX - Usuários
    path('usuarios/pagina/', pagina_usuarios, name='pagina_usuarios'),
    path('usuarios/listar/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/novo-inline/', novo_usuario_inline, name='novo_usuario_inline'),
    path('usuarios/criar/', criar_usuario, name='criar_usuario'),
]
