from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('criar/', views.criar_wine, name='criar_wine'),
    # path('listar/', views.listar_wines, name='listar_wines'), 
    path('buscar/', views.buscar_wines, name='buscar_wines'),
    path('atualizar/', views.atualizar_wine, name='atualizar_wine'),
    path('deletar/', views.deletar_wine, name='deletar_wine'),   
    path('treinar_modelo/<str:tipo>/', views.treinar_modelo, name='treinar_modelo'),
    path('informacoes_modelos/', views.informacoes_modelos, name='informacoes_modelos'),
    path('escolher_modelo/', views.escolher_modelo, name='escolher_modelo'),
]