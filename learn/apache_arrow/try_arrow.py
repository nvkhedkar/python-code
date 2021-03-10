import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pac
import datetime as dt

data_dir = 'd:/nikhil/data/ml/occupancy_data'
data_file = f'{data_dir}/datatraining.txt'

df = pd.read_csv(data_file, float_precision='%.8f')
print(df.shape, df.columns)

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S') # "2015-02-04 17:51:00"
print(df['date'].min(), df['date'].max())

df['pd_timestamp'] = df['date'].apply(lambda x: pd.Timestamp(x).value)
pd_timestamp = pd.Timestamp(year=2015, month=2, day=7).value
ndf = df[df['pd_timestamp'] <= pd_timestamp]
print(ndf.shape)

table = pa.Table.from_pandas(df)
print(table.shape)
# print(pd.Timestamp('2001-01-01').value)

stable = table.filter(pac.less_equal(table['pd_timestamp'], pd_timestamp))

print(stable.shape)
