import os
FILE_NAME = os.path.basename(__file__)
CURR_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(CURR_DIR)
import sys
sys.path.insert(-1, CURR_DIR)
sys.path.insert(-1, BASE_DIR)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(f'{CURR_DIR}/train.csv')


def show_general_info():
    for col in df.columns:
        percent_nan = df[col].isnull().sum(axis = 0)/len(df[col])
        print(f"{col} \t{df[col].dtype}, \t{df[col].nunique()}, \t{percent_nan}")
        if df[col].nunique() < 10 and df[col].dtype == object:
            print(f'{df[col].unique()}')
        print(f"{df[col].isnull().sum(axis = 0)}/{len(df[col])}")

    print(df.info())


def drop_too_many_nan_columns(dfin:pd.DataFrame, nan_threshold : float = 0.3, cols_to_drop : list = None):
    """
    df[column].count() -> counts only non-nan values
    """
    dfl2 = dfin[[column for column in dfin if dfin[column].count() / len(df) >= nan_threshold]]
    print(f'New df: {dfl2.shape}')
    if cols_to_drop:
        dfl2 = dfl2.drop(columns=cols_to_drop)
    print("List of dropped columns:", end=" ")
    for c in dfin.columns:
        if c not in dfl2.columns:
            print(c, end=", ")
    print('')
    print(dfl2.shape)
    return dfl2


df2 = drop_too_many_nan_columns(df, nan_threshold=0.3, cols_to_drop=['Id'])

