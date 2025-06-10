from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_dispositivos, name='lista_dispositivos_anvisa'),
    path('exportar_dispositivos_pdf/', views.exportar_dispositivos_pdf, name='exportar_dispositivos_pdf'),

]
