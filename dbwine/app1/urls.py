# from django.contrib import admin
# from django.urls import path
# from . import views

# urlpatterns = [
#     # path('', views.index, name='index'),
#     path('', views.home, name='home'),
#     path('criar/', views.criar_wine, name='criar_wine'),
#     # path('listar/', views.listar_wines, name='listar_wines'), 
#     path('buscar/', views.buscar_wines, name='buscar_wines'),
#     path('atualizar/', views.atualizar_wine, name='atualizar_wine'),
#     path('deletar/', views.deletar_wine, name='deletar_wine'),   
#     path('treinar-modelo/', views.treinar_modelo, name='treinar_modelo'),
#     path('informacoes-modelos/', views.listar_modelos_treinados, name='informacoes_modelos'),
#     path('escolher_modelo/', views.escolher_modelo, name='escolher_modelo'),
#     path('modelos-treinados/', views.listar_modelos_treinados, name='modelos_treinados'),
#     path('modelo/<str:sampling_type>/', views.exibir_informacoes_modelo, name='informacoes_modelo'),
#     path('avaliacao/', views.avaliacao, name='avaliacao'),
#     path('avaliacao/1-amostra/', views.avaliacao_1_amostra, name='avaliacao_1_amostra'),
#     path('avaliacao/varias-amostras/', views.avaliacao_varias_amostras, name='avaliacao_varias_amostras'),
#     path('upload_csv/', views.upload_csv, name='upload_csv'),
#     path('executar_modelo/<str:sampling_type>/', views.executar_modelo, name='executar_modelo'),
# ]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),

    # Operações relacionadas a "Wine"
    path('criar/', views.criar_wine, name='criar_wine'),
    path('buscar/', views.buscar_wines, name='buscar_wines'),
    path('atualizar/', views.atualizar_wine, name='atualizar_wine'),
    path('deletar/', views.deletar_wine, name='deletar_wine'),   
    
    # Modelos treinados
    path('treinar-modelo/', views.treinar_modelo, name='treinar_modelo'),
    path('informacoes-modelos/', views.listar_modelos_treinados, name='informacoes_modelos'),
    path('escolher_modelo/', views.escolher_modelo, name='escolher_modelo'),
    path('modelos-treinados/', views.listar_modelos_treinados, name='modelos_treinados'),
    path('modelo/<str:sampling_type>/', views.exibir_informacoes_modelo, name='informacoes_modelo'),
    
    # Avaliações
    path('avaliacao/', views.avaliacao, name='avaliacao'),
    path('avaliacao_1_amostra/', views.avaliacao_1_amostra, name='avaliacao_1_amostra'),
    path('avaliacao/varias-amostras/', views.avaliacao_varias_amostras, name='avaliacao_varias_amostras'),

    # Upload de CSV e execução de modelo
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('executar_modelo/<str:sampling_type>/', views.executar_modelo, name='executar_modelo'),
    path('executar_modelo_amostra/<str:sampling_type>/', views.executar_modelo_amostra, name='executar_modelo_amostra'),

    # Download do CSV
    path('baixar_resultado_amostra/', views.baixar_resultado_amostra, name='baixar_resultado_amostra'),
    path('download_csv/', views.download_csv, name='download_csv'),  
    path('download-wines/', views.download_wines, name='download_wines'),
]
