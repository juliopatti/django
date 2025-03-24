from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Wines
import os
import json
import sys
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import pandas as pd
from django.http import FileResponse
import shutil
import csv


# Adiciona o diretório raiz ao caminho de pesquisa do Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

# Agora importe a função corretamente
from ml import train_eval_model, eval
from django.views.decorators.csrf import csrf_exempt


# def index(request):
#     return HttpResponse("APP1.")

def home(request):
    return render(request, 'base_template.html')

def criar_wine(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        # Verifica se o nome já existe no banco de dados
        if Wines.objects.filter(name=name).exists():
            return render(request, 'criar_wine.html', {
                'error': f'Já existe um vinho com o nome "{name}". Escolha outro nome.'
            })

        Wines.objects.create(
            name=name,
            fixed_acidity=request.POST['fixed_acidity'],
            volatile_acidity=request.POST['volatile_acidity'],
            citric_acid=request.POST['citric_acid'],
            residual_sugar=request.POST['residual_sugar'],
            chlorides=request.POST['chlorides'],
            free_sulfur_dioxide=request.POST['free_sulfur_dioxide'],
            total_sulfur_dioxide=request.POST['total_sulfur_dioxide'],
            density=request.POST['density'],
            pH=request.POST['pH'],
            sulphates=request.POST['sulphates'],
            alcohol=request.POST['alcohol'],
            quality=request.POST['quality'],
            bin_quality=request.POST['bin_quality'],
            train_set=request.POST['train_set']
        )
        return redirect('home')  # Redireciona após criar
    return render(request, 'criar_wine.html')

def buscar_wines(request):
    search_query = request.GET.get('search_query', '').strip()  # Captura a consulta de busca
    wines = []  # Inicialmente vazio; só popula se houver resultados na pesquisa

    if search_query:
        if search_query.isdigit():  # Busca por ID se a consulta for um número
            wines = Wines.objects.filter(id=int(search_query))
        else:  # Busca por nome
            wines = Wines.objects.filter(name__icontains=search_query)

    return render(request, 'buscar_wines.html', {'wines': wines})



def atualizar_wine(request):
    wine = None  # Inicialmente nenhum vinho está selecionado
    if request.method == 'POST':
        if 'search_query' in request.POST:  # Etapa de busca
            search_query = request.POST.get('search_query', '').strip()

            # Verificar se o input é numérico para buscar por ID, caso contrário buscar por nome
            if search_query.isdigit():
                wine = Wines.objects.filter(id=search_query).first()
            else:
                wine = Wines.objects.filter(name__icontains=search_query).first()

            if not wine:
                return render(request, 'atualizar_wine.html', {'error': 'Vinho não encontrado.'})

        elif 'update_wine' in request.POST:  # Etapa de atualização
            wine_id = request.POST.get('wine_id')

            # Validar se o ID é numérico
            if not wine_id.isdigit():
                return render(request, 'atualizar_wine.html', {'error': 'ID inválido.', 'wine': None})

            wine = get_object_or_404(Wines, id=wine_id)

            # Atualizar os campos
            new_name = request.POST.get('name', wine.name)

            # Verificar se o novo nome já existe
            if Wines.objects.filter(name=new_name).exclude(id=wine_id).exists():
                return render(request, 'atualizar_wine.html', {
                    'wine': wine,
                    'error': f'Já existe um vinho com o nome "{new_name}". Escolha outro nome.'
                })

            wine.name = new_name
            wine.fixed_acidity = request.POST.get('fixed_acidity', wine.fixed_acidity)
            wine.volatile_acidity = request.POST.get('volatile_acidity', wine.volatile_acidity)
            wine.citric_acid = request.POST.get('citric_acid', wine.citric_acid)
            wine.residual_sugar = request.POST.get('residual_sugar', wine.residual_sugar)
            wine.chlorides = request.POST.get('chlorides', wine.chlorides)
            wine.free_sulfur_dioxide = request.POST.get('free_sulfur_dioxide', wine.free_sulfur_dioxide)
            wine.total_sulfur_dioxide = request.POST.get('total_sulfur_dioxide', wine.total_sulfur_dioxide)
            wine.density = request.POST.get('density', wine.density)
            wine.pH = request.POST.get('pH', wine.pH)
            wine.sulphates = request.POST.get('sulphates', wine.sulphates)
            wine.alcohol = request.POST.get('alcohol', wine.alcohol)
            wine.quality = request.POST.get('quality', wine.quality)
            wine.bin_quality = request.POST.get('bin_quality', wine.bin_quality)
            wine.train_set = request.POST.get('train_set', wine.train_set)
            wine.save()
            return redirect('home')  # Redireciona após salvar

    return render(request, 'atualizar_wine.html', {'wine': wine})



def deletar_wine(request):
    wine = None  # Inicialmente não há vinho selecionado
    if request.method == 'POST':  # Recebe a busca ou a confirmação
        if 'search_query' in request.POST:  # Etapa de busca
            search_query = request.POST.get('search_query', '').strip()
            # Busca por nome ou ID
            wine = Wines.objects.filter(name__icontains=search_query).first() or Wines.objects.filter(id=search_query).first()
            if not wine:
                return render(request, 'deletar_wine.html', {'error': 'Vinho não encontrado.'})
        elif 'confirm_delete' in request.POST:  # Confirmação da exclusão
            wine_id = request.POST.get('wine_id')
            wine = get_object_or_404(Wines, id=wine_id)
            wine.delete()
            return redirect('home')

    return render(request, 'deletar_wine.html', {'wine': wine})




@csrf_exempt
def treinar_modelo(request):
    if request.method == 'POST':
        # Obter o tipo de amostragem do formulário
        sampling_type = request.POST.get('sampling_type')

        if sampling_type:
            # Chamar a função para treinar o modelo
            train_eval_model(sampling_type)
            return HttpResponse(f"Modelo treinado com sucesso para o tipo: {sampling_type}")

    # Se for GET ou não houver dados POST
    return render(request, 'treinar_modelo.html')

def informacoes_modelos(request):
    return render(request, 'informacoes_modelos.html')

def escolher_modelo(request):
    # Caminho do arquivo JSON
    json_path = os.path.join(os.path.dirname(__file__), 'sampling_types.json')

    # Carrega os dados do arquivo JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        sampling_types = json.load(file)

    # Ordena os modelos: "padrao" em primeiro lugar, seguido dos demais em ordem alfabética
    modelos = [{"tipo": "padrao", "nome": sampling_types["padrao"]["name"], "sampling_type": "padrao"}]
    modelos += sorted(
        [
            {
                "tipo": key,
                "nome": value["name"],
                "info": value,
                "sampling_type": key  # Adiciona a chave 'sampling_type'
            }
            for key, value in sampling_types.items() if key != "padrao"
        ],
        key=lambda x: x["nome"]
    )

    # Renderiza o template, passando todos os modelos e informações
    return render(request, 'escolher_modelo.html', {'modelos': modelos, 'sampling_data': sampling_types})

@csrf_exempt
def treinar_modelo(request):
    if request.method == 'POST':
        # Obter o tipo de amostragem do formulário
        sampling_type = request.POST.get('sampling_type')

        if sampling_type:
            # Chamar a função para treinar o modelo
            train_eval_model(sampling_type)
            
            # Renderizar o template com sucesso
            return render(request, 'modelo_treinado.html', {'sampling_type': sampling_type})

    # Se for GET ou não houver dados POST, redirecionar para outro lugar
    return render(request, 'treinar_modelo.html')


def listar_modelos_treinados(request):
    # Caminho da pasta ml_models
    ml_models_path = os.path.join(os.path.dirname(__file__), '..', 'ml_models')

    # Lista de modelos treinados
    modelos_treinados = []
    if os.path.exists(ml_models_path):
        for file_name in os.listdir(ml_models_path):
            if file_name.endswith('.txt'):
                # Extrai o sampling_type do nome do arquivo
                sampling_type = '_'.join(file_name.split('_')[2:]).split('.')[0]
                modelos_treinados.append({
                    "nome": file_name,
                    "sampling_type": sampling_type,
                })

    return render(request, 'informacoes_modelos.html', {'modelos_treinados': modelos_treinados})


def exibir_informacoes_modelo(request, sampling_type):
    json_path = os.path.join(os.path.dirname(__file__), 'sampling_types.json')

    # Carrega os dados do arquivo JSON
    with open(json_path, 'r', encoding='utf-8') as file:
        sampling_types = json.load(file)
    info_model = ''
    for k, v in sampling_types[sampling_type].items():
        info_model += f'{k}: {v}\n'
    
    # Configurar o caminho absoluto para a pasta ml_models
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Caminho raiz do projeto
    ml_models_path = os.path.join(base_dir, 'ml_models')  # Caminho para ml_models
    file_name = f'predict_model_{sampling_type}.txt'  # Gera o nome do arquivo
    file_path = os.path.join(ml_models_path, file_name)  # Caminho completo do arquivo

    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            conteudo = file.read()  # Lê o conteúdo do arquivo
        conteudo += '\n\n'+ str(info_model)
        return render(request, 'informacoes_modelo.html', {
            'conteudo': conteudo,
            'sampling_type': sampling_type
        })
    else:
        return render(request, 'informacoes_modelo.html', {
            'conteudo': f"Arquivo não encontrado: {file_name}",
            'sampling_type': sampling_type
        })

def avaliacao(request):
    # Renderiza a tela principal de avaliação com os dois botões
    return render(request, 'avaliacao.html')

def avaliacao_1_amostra(request):
    # Lógica para avaliar uma única amostra
    return HttpResponse("Página de Avaliação - 1 Amostra")

def avaliacao_varias_amostras(request):
    # Lógica para avaliar várias amostras a partir de um CSV
    return HttpResponse("Página de Avaliação - Várias Amostras (CSV)")



def avaliacao(request):
    # Renderiza a tela principal de avaliação com os dois botões
    return render(request, 'avaliacao.html')

def avaliacao_1_amostra(request):
    # Lógica para avaliar uma única amostra
    return HttpResponse("Página de Avaliação - 1 Amostra")

def avaliacao_varias_amostras(request):
    # Lógica para avaliar várias amostras a partir de um CSV
    return HttpResponse("Página de Avaliação - Várias Amostras (CSV)")

def upload_csv(request):
    if request.method == 'POST':
        try:
            # Obtendo o arquivo enviado
            csv_file = request.FILES['csv_file']

            # Salvando no diretório 'media'
            BASE_DIR = Path(__file__).resolve().parent.parent
            media_path = os.path.join(BASE_DIR, 'media')

            # Esvaziando a pasta 'media' antes do upload
            if os.path.exists(media_path):
                for file_name in os.listdir(media_path):
                    file_path = os.path.join(media_path, file_name)
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove o arquivo
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)  # Remove subpastas vazias, se necessário

            # Cria a pasta 'media' caso ela não exista
            if not os.path.exists(media_path):
                os.makedirs(media_path)

            # Salvando o novo arquivo CSV na pasta 'media'
            file_path = os.path.join(media_path, csv_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Salvando o caminho na sessão
            request.session['csv_path'] = file_path
            print(f"CSV salvo em: {file_path}")

            # Listar modelos
            models_path = os.path.join(BASE_DIR, 'ml_models')
            modelos_treinados = []
            for file_name in os.listdir(models_path):
                if file_name.startswith("predict_model_") and file_name.endswith(".pkl"):
                    sampling_type = file_name.replace("predict_model_", "").replace(".pkl", "")
                    modelos_treinados.append({'nome': sampling_type, 'sampling_type': sampling_type})

            # Marcar CSV como carregado e renderizar com a lista de modelos
            return render(request, 'upload.html', {
                'modelos_treinados': modelos_treinados,
                'csv_carregado': True  # Adiciona a flag ao contexto
            })
        except Exception as e:
            print(f"Erro ao carregar CSV: {e}")
            return HttpResponse(f"Erro ao carregar o CSV: {e}")

    # Renderiza a página inicial se for GET
    return render(request, 'upload.html', {'csv_carregado': False})


def executar_modelo(request, sampling_type):
    BASE_DIR = Path(__file__).resolve().parent.parent
    model_path = os.path.join(BASE_DIR, 'ml_models', f'predict_model_{sampling_type}.pkl')

    if not os.path.exists(model_path):
        return HttpResponse(f"Erro: Modelo não encontrado no caminho {model_path}")

    try:
        # Recuperar o arquivo CSV carregado previamente
        csv_path = request.session.get('csv_path', None)
        if not csv_path or not os.path.exists(csv_path):
            return HttpResponse("Erro: Nenhum arquivo CSV foi carregado previamente.")

        # Processar o arquivo CSV
        df = pd.read_csv(csv_path)
        df_result = eval(df, sampling_type)  # Função de predição
        print(f"Resultados gerados:\n{df_result.head()}")  # Debug no terminal

        # Salvar o resultado em CSV
        result_path = os.path.join(BASE_DIR, 'media', 'resultado.csv')
        df_result.to_csv(result_path, index=False)
        request.session['resultado_path'] = result_path  # Salva o caminho do arquivo na sessão

        # Renderizar a página com botão de download
        return render(request, 'resultado.html', {
            'preview': df_result.head().to_html(index=False)  # Mostra apenas o preview na tela
        })

    except Exception as e:
        return HttpResponse(f"Erro ao processar o modelo: {e}")
    

def download_csv(request):
    # Recuperar o caminho do arquivo salvo na sessão
    resultado_path = request.session.get('resultado_path', None)
    if not resultado_path or not os.path.exists(resultado_path):
        return HttpResponse("Erro: Nenhum resultado disponível para download.")

    # Enviar o arquivo como resposta para download
    with open(resultado_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="resultado.csv"'
        return response
    

def avaliacao_1_amostra(request):
    if request.method == 'POST':
        # Captura os dados enviados via POST (dados da amostra)
        name = request.POST.get('name')
        fixed_acidity = request.POST.get('fixed_acidity')
        volatile_acidity = request.POST.get('volatile_acidity')
        citric_acid = request.POST.get('citric_acid')
        residual_sugar = request.POST.get('residual_sugar')
        chlorides = request.POST.get('chlorides')
        free_sulfur_dioxide = request.POST.get('free_sulfur_dioxide')
        total_sulfur_dioxide = request.POST.get('total_sulfur_dioxide')
        density = request.POST.get('density')
        pH = request.POST.get('pH')
        sulphates = request.POST.get('sulphates')
        alcohol = request.POST.get('alcohol')
        quality = request.POST.get('quality')
        bin_quality = request.POST.get('bin_quality')

        # Caminho da pasta `ml_models`
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ml_models_path = os.path.join(BASE_DIR, 'ml_models')

        # Carregar os modelos treinados dinamicamente a partir dos arquivos na pasta
        modelos_treinados = []
        try:
            for file_name in os.listdir(ml_models_path):
                if file_name.startswith("predict_model_") and file_name.endswith(".pkl"):
                    sampling_type = file_name.replace("predict_model_", "").replace(".pkl", "")
                    modelos_treinados.append({'nome': sampling_type, 'sampling_type': sampling_type})
        except Exception as e:
            return HttpResponse(f"Erro ao carregar modelos: {e}")

        # Redireciona para o template individual de seleção de modelos
        return render(request, 'selecionar_modelo_1_amostra.html', {
            'modelos_treinados': modelos_treinados,
            'amostra': {
                'name': name,
                'quality': quality,
                'bin_quality': bin_quality,
                'fixed_acidity': fixed_acidity,
                'volatile_acidity': volatile_acidity,
                'citric_acid': citric_acid,
                'residual_sugar': residual_sugar,
                'chlorides': chlorides,
                'free_sulfur_dioxide': free_sulfur_dioxide,
                'total_sulfur_dioxide': total_sulfur_dioxide,
                'density': density,
                'pH': pH,
                'sulphates': sulphates,
                'alcohol': alcohol,
            },
        })

    # Caso seja GET, exibe o formulário para 1 Amostra
    return render(request, 'avaliacao_1_amostra.html')


import shutil

def executar_modelo_amostra(request, sampling_type):
    BASE_DIR = Path(__file__).resolve().parent.parent
    media_dir = os.path.join(BASE_DIR, 'media')
    model_path = os.path.join(BASE_DIR, 'ml_models', f'predict_model_{sampling_type}.pkl')

    # Verificar se o diretório 'media' existe e, se existir, deletar seu conteúdo
    if os.path.exists(media_dir):
        shutil.rmtree(media_dir)  # Remove todo o conteúdo da pasta 'media'

    # Criar o diretório 'media' novamente
    os.makedirs(media_dir)

    if not os.path.exists(model_path):
        return HttpResponse(f"Erro: Modelo não encontrado no caminho {model_path}")

    try:
        # Recuperar os dados da amostra enviados via POST
        amostra = {
            'name': request.POST.get('name'),
            'fixed_acidity': request.POST.get('fixed_acidity'),
            'volatile_acidity': request.POST.get('volatile_acidity'),
            'citric_acid': request.POST.get('citric_acid'),
            'residual_sugar': request.POST.get('residual_sugar'),
            'chlorides': request.POST.get('chlorides'),
            'free_sulfur_dioxide': request.POST.get('free_sulfur_dioxide'),
            'total_sulfur_dioxide': request.POST.get('total_sulfur_dioxide'),
            'density': request.POST.get('density'),
            'pH': request.POST.get('pH'),
            'sulphates': request.POST.get('sulphates'),
            'alcohol': request.POST.get('alcohol'),
            'quality': request.POST.get('quality'),  # Opcional
            'bin_quality': request.POST.get('bin_quality')  # Opcional
        }

        # Verificar se algum campo obrigatório está vazio
        required_fields = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
                           'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
                           'pH', 'sulphates', 'alcohol']
        for field in required_fields:
            if amostra[field] is None:
                return HttpResponse(f"Erro: O campo {field} é obrigatório.")

        # Converter os valores para um DataFrame para o modelo
        import pandas as pd
        df_amostra = pd.DataFrame([amostra])

        # Certifique-se de que os campos opcionais (quality e bin_quality) sejam preenchidos com None
        df_amostra['quality'] = df_amostra['quality'].fillna('None')
        df_amostra['bin_quality'] = df_amostra['bin_quality'].fillna('None')

        # Processar a amostra com o modelo
        df_result = eval(df_amostra, sampling_type)  # Função `eval` para predição
        print(f"Resultado gerado:\n{df_result}")  # Debug no terminal

        # Salvar o resultado em CSV
        result_path = os.path.join(media_dir, 'resultado_amostra.csv')
        df_result.to_csv(result_path, index=False)

        # Salvar o caminho do CSV na sessão
        request.session['resultado_amostra_path'] = result_path

        # Renderizar o template de resultados
        return render(request, 'resultado_1_amostra.html', {
            'preview': df_result.to_html(index=False)  # Exibir o resultado como preview
        })

    except Exception as e:
        return HttpResponse(f"Erro ao processar o modelo: {e}")

    
def baixar_resultado_amostra(request):
    result_path = request.session.get('resultado_amostra_path')
    if not result_path or not os.path.exists(result_path):
        return HttpResponse("Erro: Nenhum resultado de amostra foi encontrado.")
    return FileResponse(open(result_path, 'rb'), as_attachment=True, filename='resultado_amostra.csv')


def download_wines(request):
    # Cria uma resposta HTTP com o cabeçalho do tipo de conteúdo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wines.csv"'

    # Obtém os campos dinamicamente
    fields = [field.name for field in Wines._meta.get_fields()]

    # Cria um writer para o arquivo CSV
    writer = csv.writer(response)
    # Escreve o cabeçalho automaticamente
    writer.writerow(fields)

    # Escreve os valores para cada instância
    for wine in Wines.objects.all():
        writer.writerow([getattr(wine, field) for field in fields])

    return response