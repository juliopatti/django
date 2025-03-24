# import pickle

# path_model = r'C:\Users\julio\Documents\pos agentes\projetos\framework\django\dbwine\ml_models\predict_model_ros_sk1.pkl'

# try:
#     with open(path_model, 'rb') as arquivo:
#         model = pickle.load(arquivo)
#     print("Modelo carregado com sucesso:", model)
# except Exception as e:
#     print("Erro ao carregar o modelo:", e)


import pandas as pd
import pickle

numeric_columns = [
    'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
    'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
    'pH', 'sulphates', 'alcohol'
]



df = pd.read_csv(r'C:\Users\julio\Documents\pos agentes\projetos\framework\django\raw_data\data_not_dup.csv')
feature_columns = df.drop(columns=['quality',
                                        'bin_quality', 
                                        'train_set', 'name']).columns.tolist()
cols = ['name', 'fixed_acidity', 'volatile_acidity', 'citric_acid',
       'residual_sugar', 'chlorides', 'free_sulfur_dioxide',
       'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol']

if 'quality' in df.columns.tolist():
    cols += ['quality']
df = df[df['train_set']==False].reset_index(drop=True)[cols]

df.to_csv('sample_test_csv.csv', index=False)
print(df.shape)
print(df.columns)

