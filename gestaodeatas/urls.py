from django.urls import path
from .views import pagina_inicial, nova_ata, detalhes_ata

urlpatterns = [
    path('', pagina_inicial, name='pagina_inicial'),
    path('atas/nova/', nova_ata, name='nova_ata'),
    path('atas/<int:id>/', detalhes_ata, name='detalhes_ata'),
]
