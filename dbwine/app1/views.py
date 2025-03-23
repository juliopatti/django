from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Wines

# def index(request):
#     return HttpResponse("APP1.")

def home(request):
    return render(request, 'base_template.html')

def criar_wine(request):
    # Lógica para criar um registro na tabela Wines
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

def atualizar_wine(request, wine_id):
    wine = get_object_or_404(Wines, id=wine_id)  # Busca o objeto ou retorna 404
    if request.method == 'POST':
        wine.name = request.POST.get('name', wine.name)
        wine.save()
        return redirect('home')  # Redireciona para a página inicial
    return render(request, 'atualizar_wine.html', {'wine': wine})

def deletar_wine(request, wine_id):
    wine = get_object_or_404(Wines, id=wine_id)  # Busca o objeto ou retorna 404
    wine.delete()  # Deleta o registro
    return redirect('home')  # Redireciona para a página inicial