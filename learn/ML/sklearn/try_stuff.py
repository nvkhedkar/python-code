from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

df = pd.DataFrame()
df['col1'] = [x+1 for x in range(10)]
df['col2'] = [(x+1)/10 for x in range(10)]
print(df)
data = df.values
print(df.shape)
scaler = StandardScaler()
minmax = MinMaxScaler()

print(scaler)
# print(minmax.fit_transform(data))
