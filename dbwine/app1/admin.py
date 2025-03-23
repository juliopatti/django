from django.contrib import admin
from .models import *

class PessoaCustomizado(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'role', )

admin.site.register(Person, PessoaCustomizado)
