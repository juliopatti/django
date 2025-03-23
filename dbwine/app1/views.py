from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Wines

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
