# %%
# import os
FILE_NAME = os.path.basename(__file__)
CURR_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(CURR_DIR)
DATA_DIR = f'{CURR_DIR}/data'
import sys
sys.path.insert(-1, CURR_DIR)
sys.path.insert(-1, BASE_DIR)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
df = pd.read_csv(f'{DATA_DIR}/train.csv')

#%%
print(df.head(5))

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


def encode(dfin, feature, target):
    """
    Looks like target encoding
    target is mean of column "target"
    """
    ordering = pd.DataFrame()
    ordering['val'] = dfin[feature].unique()
    print('1--'*30)
    print(ordering)
    ordering.index = ordering.val
    print('2--'*30)
    print(ordering)
    ordering['spmean'] = dfin[[feature, target]].groupby(feature).mean()[target]
    print('3--'*30)
    print(ordering)
    ordering = ordering.sort_values('spmean')
    print('4--'*30)
    print(ordering)
    ordering['ordering'] = range(1, ordering.shape[0] + 1)
    print('5--'*30)
    print(ordering)
    ordering = ordering['ordering'].to_dict()
    print('6--'*30)
    print(ordering)

    for cat, o in ordering.items():
        dfin.loc[dfin[feature] == cat, feature + '_E'] = o


def encode_try_1():
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df1['size'] = ['s' for i in range(5)]
    df1['value'] = np.random.randint(10, 20, size=(5, 1)).astype(float)

    df2 = pd.DataFrame()
    df2['size'] = ['m' for i in range(7)]
    df2['value'] = np.random.randint(15, 25, size=(7, 1)).astype(float)

    df3 = pd.DataFrame()
    df3['size'] = ['l' for i in range(9)]
    df3['value'] = np.random.randint(25, 35, size=(9, 1)).astype(float)
    df = pd.concat([df1, df3, df2])
    encode(df, 'size', 'value')
    print(df)
    return


# %%
encode_try_1()
# df2 = drop_too_many_nan_columns(df, nan_threshold=0.3, cols_to_drop=['Id'])


# %%
