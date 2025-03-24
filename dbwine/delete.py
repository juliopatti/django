import os
import django
from django.db import connection

# Configure o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbwine.settings')  # Substitua 'nome_do_projeto' pelo nome real do seu projeto
django.setup()

def delete_person_table():
    with connection.cursor() as cursor:
        # Comando SQL para deletar a tabela Person
        cursor.execute("DROP TABLE IF EXISTS app1_person;")  # Substitua 'app_person' pelo nome real da tabela
        print("Tabela Person deletada com sucesso!")

# Executar a função
delete_person_table()


# import os
# import django
# from django.db import connection

# # Configurar o ambiente do Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbwine.settings')  # Substitua pelo nome do seu projeto
# django.setup()

# def listar_tabelas():
#     with connection.cursor() as cursor:
#         # Esse comando funciona na maioria dos bancos de dados suportados pelo Django
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  # Para SQLite
#         # Para outros bancos, como PostgreSQL ou MySQL, use:
#         # cursor.execute("SHOW TABLES;")
#         tabelas = cursor.fetchall()
#         print("Tabelas no banco de dados:")
#         for tabela in tabelas:
#             print(tabela[0])  # Cada tabela está em um tuple
            
# listar_tabelas()