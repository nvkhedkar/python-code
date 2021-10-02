import numpy as np
import pandas as pd
# https://1drv.ms/u/s!AtAAGckP_LuV3Wyf08BipNyOJAnm?e=CZE1qS
df = pd.read_csv('./dataset/dataset.csv')
# for col in df.columns:
#     print(col)
print(df.shape)
df1 = df.dropna()
print(df1.shape)
# print(df.describe())
print(df1.Age.min())
ans = {
    "1.1": df.Age.min(),
    "1.3": int(df1.sem(axis = 0, skipna = False)["BasePay"]),
    "1.4": [0.0, 43291.990000, 84278.515000, 122807.782500, 567595.430000]
}
cdf = df1.corr()
print(cdf.shape)
print(cdf.BasePay)
print(ans)
# print(df1.TotalPayBenefits.describe())
# print(df1.TotalPayBenefits.median())





