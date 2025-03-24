# Projeto Django: Predição de Qualidade do Vinho

Este projeto utiliza **machine learning** para modelar preferências de vinhos com base em propriedades físico-químicas, seguindo a pesquisa de Cortez et al., 2009. A aplicação foi desenvolvida com Django e permite treinamento, avaliação e predição de modelos de classificação.

---

## 📜 Créditos
O dataset utilizado está disponível no Kaggle: **Red Wine Quality - Cortez et al. (2009)**.

Este projeto está baseado na pesquisa:
> P. Cortez, A. Cerdeira, F. Almeida, T. Matos e J. Reis. *Modeling wine preferences by data mining from physicochemical properties*. Decision Support Systems, Elsevier, 47(4):547-553, 2009.

---

## 🔎 Considerações sobre o Projeto
- **Preparo dos dados:** Para melhor generalização dos modelos, duplicados foram desconsiderados.
- **Divisão de dados:** 
  - 80% dos dados são destinados ao treino e validação por **validação cruzada**.
  - 20% dos dados são utilizados para teste, garantindo comparação de desempenho com os resultados da validação cruzada.
- **Otimização de hiperparâmetros:** A métrica alvo no treinamento é **AUC**, mas outras métricas também são exibidas para análise de desempenho.
- **Sampleamento:** 
  - Métodos como **oversampling** e **undersampling** são usados na maioria dos casos.
  - Não ocorre sampleamento nos conjuntos de teste e validação para evitar vazamento de dados e preservar a distribuição real dos dados.
  - Para garantir a integridade, os splits foram manualmente configurados. Mais detalhes no [wine_api repository](https://github.com/juliopatti/wine_api).

# Créditos
O dataset está disponível no Kaggle: **Red Wine Quality - Cortez et al. (2009)**.  
Corresponde à pesquisa de Cortez et al., 2009:  
P. Cortez, A. Cerdeira, F. Almeida, T. Matos e J. Reis. *Modeling wine preferences by data mining from physicochemical properties*. Decision Support Systems, Elsevier, 47(4):547-553, 2009.

# Considerações
- Os dados aqui utilizados desconsideram os duplicados para uma melhor ideia sobre a generalização dos modelos.
- O processo de treinamento consiste em uma validação cruzada sobre 80% dos dados que são destinados a treino e validação. 20% dos dados são designados a teste e comparação de desempenho com a validação cruzada.
- A otimização de hiperparâmetros e a métrica alvo no treinamento é a **AUC**, porém outras métricas são apresentadas para o desempenho sobre o conjunto de treinamento.
- O processo de treinamento conta, em sua maioria dos casos, com o procedimento de sampleamento, podendo ser **over** ou **undersample**, e diversas outras técnicas da literatura. É preciso atentar-se ao não sampleamento em conjuntos de teste e validação, pois essa prática consiste em vazamento de dados, além de não preservar a distribuição real dos dados. Deste modo, os splits foram manualmente confeccionados para se garantir que tal deslize não ocorresse.  
  Um trabalho correlato pode ser visto em: [Wine API Repository](https://github.com/juliopatti/wine_api).

# Django
Você pode iniciar por:
git clone https://github.com/juliopatti/django.git  
cd django  

## É necessário ter Python 3.11. Para criar um ambiente no Windows:
python3.11 -m venv venv  

## Para ativá-lo:
.\venv\Scripts\activate  

## Atualizar o pip:
python.exe -m pip install --upgrade pip  

## Instalar as demais dependências:
pip install -r requirements.txt  

### Crie um arquivo `.env` com suas secret keys. Exemplo: `....../django/.env`
DJANGO_SECRET_KEY=sua_senha  
DJANGO_DEBUG=True  
DJANGO_ALLOWED_HOSTS=['*']  

## Entre no projeto Django:
cd dbwine  

## No terminal:
python .\manage.py runserver  

## Na porta local pode-se realizar o login:
http://127.0.0.1:8000/admin  

## Home app:
http://127.0.0.1:8000/


### OBS ##
como é uma aplicação informal, compactarei tambem a pasta com todos arquivos, inclusos os do gitignore

por facilidade, os acesssos dos usuários meramente ilustrativos são

Username: admin
Email address: juliopatti@discente.ufg.br
Password: ronaldofenomeno

user: usuario_comum@gmail.com
senha: menosacesso

user: cientista@gmail.com
fenomenoronaldo
