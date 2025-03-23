from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("APP1.")

def home(request):
    return render(request, 'base_template.html')
