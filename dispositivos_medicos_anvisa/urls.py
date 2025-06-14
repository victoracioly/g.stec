from django.urls import path
from . import views

app_name = 'dispositivos_medicos_anvisa'

urlpatterns = [
    path('', views.lista_dispositivos, name='lista_dispositivos'),
    path('exportar_dispositivos_pdf/', views.exportar_dispositivos_pdf, name='exportar_dispositivos_pdf'),
]
