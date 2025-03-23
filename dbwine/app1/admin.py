from django.contrib import admin
from .models import *

class PessoaCustomizado(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'role', )

admin.site.register(Person, PessoaCustomizado)

class WinesCustomizado(admin.ModelAdmin):
    list_display = (
        'name', 'fixed_acidity', 'volatile_acidity', 'citric_acid', 
        'residual_sugar', 'chlorides', 'free_sulfur_dioxide', 
        'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 
        'alcohol', 'quality', 'bin_quality', 'train_set',
    )

admin.site.register(Wines, WinesCustomizado)
