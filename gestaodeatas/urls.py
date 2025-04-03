# gestaodeatas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_atas, name='lista_atas'),
    path('ata/<int:ata_id>/', views.detalhes_ata, name='detalhes_ata'),
    path('nova/', views.nova_ata, name='nova_ata'),
]
