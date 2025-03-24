from django.http import HttpResponseForbidden
from django.shortcuts import render

PROHIBITED_ENDPOINTS = [
    '/escolher_modelo/',
    '/criar/',
    '/atualizar/',
    '/deletar/',
]

class RestrictEndpointsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.groups.filter(name='usuario_comum').exists():
            if request.path in PROHIBITED_ENDPOINTS:
                # Renderiza a página de acesso negado
                return render(request, 'acesso_negado.html')  # Certifique-se de salvar o HTML como acesso_negado.html em templates
        return self.get_response(request)

