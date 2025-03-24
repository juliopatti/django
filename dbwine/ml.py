import os
import django
import sys
import pandas as pd
# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dbwine.settings')  # Ajuste 'dbwine' se necessário
django.setup()
from app1.models import Wines

import numpy as np
from sklearn import svm
from sklearn.cluster import KMeans
from sklearn.model_selection import StratifiedShuffleSplit, StratifiedKFold
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from lightgbm import LGBMClassifier
from skopt import gp_minimize
from skopt.space import Real, Categorical, Integer
from imblearn.under_sampling import (
    CondensedNearestNeighbour, 
    TomekLinks, 
    OneSidedSelection, 
    EditedNearestNeighbours, 
    RepeatedEditedNearestNeighbours,
    AllKNN,
    NeighbourhoodCleaningRule,
    NearMiss,
    InstanceHardnessThreshold,
    RandomUnderSampler
    )
from imblearn.over_sampling import (
    RandomOverSampler,
    SMOTE,
    ADASYN,
    BorderlineSMOTE,
    SVMSMOTE,
    KMeansSMOTE,
)
import pickle

from tqdm import tqdm
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

random_state = 2025
skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=2025)

wines = Wines.objects.all() 
df_train = pd.DataFrame(list(wines.values()))
# Identificar e converter as colunas problemáticas
numeric_columns = [
    'fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',
    'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',
    'pH', 'sulphates', 'alcohol'
]
# Corrigir os tipos
for column in numeric_columns:
    df_train[column] = pd.to_numeric(df_train[column], errors='coerce')
df_test = df_train[df_train['train_set']==False].reset_index(drop=True).copy()
df_train = df_train[df_train['train_set']==True].reset_index(drop=True).copy()

# print(df_train.head(), df_train.shape)


feature_columns = df_train.drop(columns=['quality', 'id',
                                        'bin_quality', 
                                        'train_set', 'name']).columns.tolist()

class TqdmCallback:
    def __init__(self, total):
        self.pbar = tqdm(total=total)

    def __call__(self, res):
        self.pbar.update(1)
        
def calcular_estatisticas(lista, output=True):
    
    mean = round(np.mean(lista) * 100, 1)
    std = round(np.std(lista) * 100, 1)
    min = round(np.min(lista) * 100, 1)
    max = round(np.max(lista) * 100, 1)
    
    if output:
        output=f"Média da validação cruzada (std): {mean}% ({std}%)\n(Min/Máx): ({min}%/{max}%)"
        print(output)
    
    return mean, std, min, max


def sampling(df, sampling_type, feature_columns, label_column):
    if sampling_type=='cnn':
        sampler = CondensedNearestNeighbour(
            sampling_strategy='auto',
            random_state=random_state,
            n_neighbors=1,
        )
    
    if sampling_type=='tomeklinks_auto':
        sampler = TomekLinks(
            sampling_strategy='auto'
            )
        
    if sampling_type=='oss':
        sampler = OneSidedSelection(
            sampling_strategy='auto',
            random_state=random_state,
            n_neighbors=1 
        )
        
    if sampling_type=='enn':
        sampler = EditedNearestNeighbours(
            sampling_strategy='auto',
            n_neighbors=3,
            kind_sel='all'
        )
    
    if sampling_type=='renn':
        sampler = RepeatedEditedNearestNeighbours(
            sampling_strategy='auto',
            n_neighbors=3,
            kind_sel='all',
            max_iter=100
        )
        
    if sampling_type=='allknn':
        sampler = AllKNN(
            sampling_strategy='auto',
            n_neighbors=5,
            kind_sel='all'
        )
    
    if sampling_type=='ncr':
        sampler = NeighbourhoodCleaningRule(
            sampling_strategy='auto',
            n_neighbors=3,
            threshold_cleaning=0.5
        )
    
    if sampling_type in ['nm1', 'nm2', 'nm3']:
        nm_type = sampling_type[-1]
        sampler = NearMiss(
            sampling_strategy='auto',
            version = int(nm_type),
            n_neighbors=3
        )
        
    if sampling_type in ['iht_none', 'iht_lgbm']:
        estimator=None
        if sampling_type=='iht_lgbm':
            estimator = LGBMClassifier(class_weight='balanced', verbose=-1, random_state=random_state)
        sampler = InstanceHardnessThreshold(
            estimator=estimator,
            sampling_strategy='auto',
            random_state=random_state,
            cv=4
        )
    
    if sampling_type=='rus_std':
        sampler=RandomUnderSampler(
            sampling_strategy='auto',
            random_state=random_state,
        )
    
    ########### OVER 
    
    if sampling_type in ['ros_std', 'ros_sk05', 'ros_sk1', 'ros_sk10']:
        if sampling_type=='ros_std':
            sh = None
        elif sampling_type=='ros_sk05':
            sh=0.5
        else:
            sh = int(sampling_type.split('_sk')[-1])
        sampler=RandomOverSampler(
            sampling_strategy='auto',
            random_state=random_state,
            shrinkage=sh
        )
    
    if sampling_type in ['smt1', 'smt3', 'smt5']:
        k_neighbors = sampling_type.split('smt')[-1]
        sampler = SMOTE(
            sampling_strategy='auto',
            random_state=random_state,
            k_neighbors=int(k_neighbors)
        )
        
    if sampling_type in ['ada1', 'ada3', 'ada5']:
        k_neighbors = sampling_type.split('ada')[-1]
        sampler = ADASYN(
            sampling_strategy='auto',
            random_state=random_state,
            n_neighbors=int(k_neighbors)
        )
        
    if sampling_type in ['bsmt1', 'bsmt2']:
        kind=sampling_type[-1]
        sampler = BorderlineSMOTE(
            sampling_strategy='auto',
            random_state=random_state,
            k_neighbors=5,
            m_neighbors=10,
            kind=f'borderline-{kind}'
        )
        
    if sampling_type=='svm_smt':
        sampler = SVMSMOTE(
            sampling_strategy='auto',
            random_state=random_state,
            k_neighbors=5,
            m_neighbors=10,
            svm_estimator = svm.SVC(kernel='linear')
            )
        
    if sampling_type=='kms':
        sampler = KMeansSMOTE(
            sampling_strategy='auto',
            random_state=random_state,
            k_neighbors= 2,
            kmeans_estimator= KMeans(n_clusters=3, random_state=random_state),
            cluster_balance_threshold = 0.1,
            density_exponent='auto'
        )

    if sampling_type=='padrao':
        return df[feature_columns], df[label_column]
    
    x_res, y_res = sampler.fit_resample(df[feature_columns], df[label_column])
    return x_res, y_res


def get_model(params):

    model = LGBMClassifier(
        learning_rate     = params[0],
        num_leaves        = params[1],
        min_child_samples = params[2],
        max_bin           = params[3],
        subsample         = params[4],
        colsample_bytree  = params[5],
        n_estimators      = params[6],
        subsample_freq    = 1,
        class_weight      = 'balanced',
        random_state      = 2025,
        verbose=-1
    )
    
    return model



# sampling_type = 'padrao'
def train_eval_model(sampling_type):

    dict_folds = {}
    for c, (train_index_fold, val_index_fold) in enumerate(skf.split(df_train, df_train['quality'])):
        df_train_fold = df_train.loc[train_index_fold]
        # Undersample
        dict_folds[f'X_fold_{c}'], dict_folds[f'y_fold_{c}'] = sampling(
                                                                        df_train_fold, 
                                                                        sampling_type=sampling_type, 
                                                                        feature_columns=feature_columns, 
                                                                        label_column='bin_quality'
                                                                )
    def objective_minimize(params):
        # print(params)
        auc = []
        for c, (train_index_fold, val_index_fold) in enumerate(skf.split(df_train, df_train['quality'])):
            df_train_fold, df_val_fold = df_train.loc[train_index_fold], df_train.loc[val_index_fold]
            X_val = df_val_fold[feature_columns]
            y_val = df_val_fold['bin_quality']
            
            # Undersample
            X_fold, y_fold = dict_folds[f'X_fold_{c}'], dict_folds[f'y_fold_{c}']
            
            model = get_model(params)
            model.fit(X_fold, y_fold)
            # y_val_pred = model.predict(X_val)
            y_val_proba = model.predict_proba(X_val)[:,1]
            auc.append(roc_auc_score(y_val, y_val_proba))
        metric = float(np.mean(auc))
        
        return - metric

    #################################################   Otimização
    space = [Real(low=1e-4, high=3e-1, prior='log-uniform'),   # learning_rate     = params[0]
            Integer(low=2, high=128),                         # num_leaves        = params[1]
            Integer(low=1, high=200),                         # min_child_samples = params[2]
            Integer(low=100, high=500),                       # max_bin           = params[3]
            Real(low=0.05, high=1.0),                         # subsample         = params[4]
            Real(low=0.1, high=1.0),                          # colsample_bytree  = params[5]
            Integer(low=100, high=300)                        # n_estimators      = params[6]
            ]

    # Otimização de (hiper)parametros
    n_calls = 50

    result = gp_minimize(objective_minimize, space, random_state=2025, n_calls=n_calls, n_random_starts=15, callback=[TqdmCallback(total=n_calls)])

    # Melhores parâmetros
    best_params = result.x
    print(best_params)
    print(result.fun)

    # Validação cruzada
    auc = []
    for c, (train_index_fold, val_index_fold) in enumerate(skf.split(df_train, df_train['quality'])):
        df_train_fold, df_val_fold = df_train.loc[train_index_fold], df_train.loc[val_index_fold]
        X_val = df_val_fold[feature_columns]
        y_val = df_val_fold['bin_quality']
        
        # Undersample
        X_fold, y_fold = dict_folds[f'X_fold_{c}'], dict_folds[f'y_fold_{c}']
        
        model = get_model(best_params)
        model.fit(X_fold, y_fold)
        # y_val_pred = model.predict(X_val)
        y_val_proba = model.predict_proba(X_val)[:,1]
        auc.append(roc_auc_score(y_val, y_val_proba))
        
    # Calcular média, desvio padrão, mínimo e máximo
    print('AUC CROSS_VAL')
    mean, std, min, max = calcular_estatisticas(auc)


    # Modelo final
    X_train = df_train[feature_columns]
    y_train = df_train['bin_quality']

    if sampling_type:
        # Undersample
        X_train, y_train = sampling(df_train, 
                                    sampling_type=sampling_type, 
                                    feature_columns=feature_columns, 
                                    label_column='bin_quality')

    model = get_model(best_params)
    model.fit(X_train, y_train)

    ####################################### Teste
    # df_test = pd.read_csv('../data/df_test.csv')

    X_test = df_test[feature_columns]
    y_test = df_test['bin_quality']

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, y_pred_proba)
    report = classification_report(y_test, y_pred)

    path_result = f'ml_models/predict_model_{sampling_type}.txt'
    print(f'AUC: {round(100*auc,1)}%\n\n{report}')

    result_content = (
        "AUC Cross Val\n"
        f"Média da validação cruzada (std): {mean}% ({std}%)\n"
        f"(Min/Máx): ({min}%/{max}%)\n\n"
        "Resultados de Teste\n"
        f"AUC Test: {round(100 * auc, 1)}%\n\n"
        f"{report}"
    )

    # Salvar o conteúdo no arquivo
    with open(path_result, 'w', encoding='utf-8') as file:
        file.write(result_content)

    print(f"Resultados salvos em: {path_result}")

    ########## Out 
    df_test['proba'] = y_pred_proba
    df_test['pred'] = y_pred


    # Save model
    path_model = f'ml_models/predict_model_{sampling_type}.pkl'
    with open(path_model, 'wb') as arquivo:
        pickle.dump(model, arquivo)
        
    # Load test
    with open(path_model, 'rb') as arquivo:
        model = pickle.load(arquivo)

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    report = classification_report(y_test, y_pred)

    print(f'AUC: {round(100*auc,1)}%\n\n{report}')
    
    
# train_eval_model(sampling_type)

def eval(df, sampling_type):
    path_model = f'ml_models/predict_model_{sampling_type}.pkl'
    # print(df.head)
    # Load test
    with open(path_model, 'rb') as arquivo:
        model = pickle.load(arquivo)
        
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        
    X_test = df[feature_columns]
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    df['pred'] = y_pred
    df['proba'] = y_pred_proba
    
    if 'quality' in df.columns:
        df = df.rename(columns={'quality': 'quality (not feature)'})
    if 'bin_quality' in df.columns:
        df = df.rename(columns={'bin_quality': 'bin_quality (not feature)'})
    
    return df