# aprendendopython/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestaodeatas.urls')),  # isso conecta as URLs do app
]
