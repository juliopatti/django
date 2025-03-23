import os
import django
import csv
import sys
sys.path.append(r'C:\Users\julio\Documents\pos agentes\projetos\framework\django\dbwine')

# Configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbwine.settings')  # Aponta para o arquivo settings.py correto
django.setup()

from app1.models import Wines  # Importa o modelo Wines da pasta 'app1'

# Caminho do arquivo CSV
csv_path = r'C:\Users\julio\Documents\pos agentes\projetos\framework\django\raw_data\data_not_dup.csv'

def carregar_dados():
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Lê o CSV como dicionário
        registros = []

        for row in reader:
            registros.append(Wines(
                name=row['name'],
                fixed_acidity=row['fixed_acidity'],
                volatile_acidity=row['volatile_acidity'],
                citric_acid=row['citric_acid'],
                residual_sugar=row['residual_sugar'],
                chlorides=row['chlorides'],
                free_sulfur_dioxide=row['free_sulfur_dioxide'],
                total_sulfur_dioxide=row['total_sulfur_dioxide'],
                density=row['density'],
                pH=row['pH'],
                sulphates=row['sulphates'],
                alcohol=row['alcohol'],
                quality=row['quality'],
                bin_quality=row['bin_quality'],
                train_set=row['train_set'].lower() == 'true'  # Converte para booleano
            ))
        
        # Insere os registros em massa
        Wines.objects.bulk_create(registros)
        print("Dados carregados com sucesso!")

if __name__ == '__main__':
    carregar_dados()