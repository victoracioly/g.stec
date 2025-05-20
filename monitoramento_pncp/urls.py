from django.urls import path
from . import views

urlpatterns = [
    path('atas/', views.monitoramento_atas_pncp, name='monitoramento_atas_pncp'),
    path('contratacoes/', views.monitoramento_contratacoes_pncp, name='monitoramento_contratacoes_pncp'),
    path('detalhes_ata/<str:numeroControle>/', views.detalhes_atas_pncp, name='detalhes_atas_pncp'),
    path('detalhes_contratacao/<str:numeroContrato>/', views.detalhes_contratacao_pncp, name='detalhes_contratacao_pncp'),
]
