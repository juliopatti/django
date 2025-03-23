import pandas as pd
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