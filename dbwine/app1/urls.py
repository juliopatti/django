from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('criar/', views.criar_wine, name='criar_wine'),
    # path('listar/', views.listar_wines, name='listar_wines'), 
    path('buscar/', views.buscar_wines, name='buscar_wines'),
    path('atualizar/<int:wine_id>/', views.atualizar_wine, name='atualizar_wine'),
    path('deletar/<int:wine_id>/', views.deletar_wine, name='deletar_wine'),    
    
]