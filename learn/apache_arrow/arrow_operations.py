import pandas as pd
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/allisonhorst/"
                 "palmerpenguins/47a3476d2147080e7ceccef4cf70105c808f2cbf/"
                 "data-raw/penguins_raw.csv")
                 # Increase dataset to 1m rows and reset index
df = df.sample(1_000_000, replace=True).reset_index(drop=True)


# Update sample number (0 to 999'999)
df["Sample Number"] = df.index
# Add some random variation to numeric columns
df[["Culmen Length (mm)", "Culmen Depth (mm)",
    "Flipper Length (mm)", "Body Mass (g)"]] = df[["Culmen Length (mm)", "Culmen Depth (mm)",
                                                   "Flipper Length (mm)", "Body Mass (g)"]] \
                                               + np.random.rand(df.shape[0], 4)

# Create dataframe where missing numeric values are filled with zero
df_nonan = df.copy()
df_nonan[["Culmen Length (mm)", "Culmen Depth (mm)",
          "Flipper Length (mm)", "Body Mass (g)"]] = df[["Culmen Length (mm)", "Culmen Depth (mm)",
                                                         "Flipper Length (mm)", "Body Mass (g)"]].fillna(0)


#=======================================================================================================


import pyarrow as pa
df.to_csv("penguin-dataset.csv")

# Write to parquet
df.to_parquet("penguin-dataset.parquet")

# Write to Arrow
# Convert from pandas to Arrow
table = pa.Table.from_pandas(df)
# Write out to file
with pa.OSFile('penguin-dataset.arrow', 'wb') as sink:
    with pa.RecordBatchFileWriter(sink, table.schema) as writer:
        writer.write_table(table)

# Convert from no-NaN pandas to Arrow
table_nonan = pa.Table.from_pandas(df_nonan)
# Write out to file
with pa.OSFile('penguin-dataset-nonan.arrow', 'wb') as sink:
    with pa.RecordBatchFileWriter(sink, table_nonan.schema) as writer:
        writer.write_table(table_nonan)


#===============================================================================================
# Write to csv
df.to_csv("penguin-dataset.csv")

# Write to parquet
df.to_parquet("penguin-dataset.parquet")

# Write to Arrow
# Convert from pandas to Arrow
table = pa.Table.from_pandas(df)
# Write out to file
with pa.OSFile('penguin-dataset.arrow', 'wb') as sink:
    with pa.RecordBatchFileWriter(sink, table.schema) as writer:
        writer.write_table(table)

# Convert from no-NaN pandas to Arrow
table_nonan = pa.Table.from_pandas(df_nonan)
# Write out to file
with pa.OSFile('penguin-dataset-nonan.arrow', 'wb') as sink:
    with pa.RecordBatchFileWriter(sink, table_nonan.schema) as writer:
        writer.write_table(table_nonan)




# %%timeit
pd.read_csv("penguin-dataset.csv")["Flipper Length (mm)"].mean()


# Read parquet and calculate mean
# %%timeit
pd.read_parquet("penguin-dataset.parquet", columns=["Flipper Length (mm)"]).mean()


# Read Arrow using file API and calculate mean
# %%timeit
with pa.OSFile('penguin-dataset.arrow', 'rb') as source:
    table = pa.ipc.open_file(source).read_all().column("Flipper Length (mm)")
result = table.to_pandas().mean()


# Read Arrow with memory-mapped API with missing values
# %%timeit
source = pa.memory_map('penguin-dataset.arrow', 'r')
table = pa.ipc.RecordBatchFileReader(source).read_all().column("Flipper Length (mm)")
result = table.to_pandas().mean()


# Read Arrow with memory-mapped API without missing values (zero-copy)
# %%timeit
source = pa.memory_map('penguin-dataset-nonan.arrow', 'r')
table = pa.ipc.RecordBatchFileReader(source).read_all().column("Flipper Length (mm)")
result = table.to_pandas().mean()


import psutil, os

# Measure initial memory consumption
memory_init = psutil.Process(os.getpid()).memory_info().rss >> 20


# Read csv
col_csv = pd.read_csv("penguin-dataset.csv")["Flipper Length (mm)"]
memory_post_csv = psutil.Process(os.getpid()).memory_info().rss >> 20


# Read parquet
col_parquet = pd.read_parquet("penguin-dataset.parquet", columns=["Flipper Length (mm)"])
memory_post_parquet = psutil.Process(os.getpid()).memory_info().rss >> 20


# Read Arrow using file API
with pa.OSFile('penguin-dataset.arrow', 'rb') as source:
    col_arrow_file = pa.ipc.open_file(source).read_all().column("Flipper Length (mm)").to_pandas()
memory_post_arrowos = psutil.Process(os.getpid()).memory_info().rss >> 20


# Read Arrow with memory-mapped API with missing values
source = pa.memory_map('penguin-dataset.arrow', 'r')
table_mmap = pa.ipc.RecordBatchFileReader(source).read_all().column("Flipper Length (mm)")
col_arrow_mapped = table_mmap.to_pandas()
memory_post_arrowmmap = psutil.Process(os.getpid()).memory_info().rss >> 20


# Read Arrow with memory-mapped API without missing values (zero-copy)
source = pa.memory_map('penguin-dataset-nonan.arrow', 'r')
table_mmap_zc = pa.ipc.RecordBatchFileReader(source).read_all().column("Flipper Length (mm)")
col_arrow_mapped_zc = table_mmap_zc.to_pandas()
memory_post_arrowmmap_zc = psutil.Process(os.getpid()).memory_info().rss >> 20


# Display memory consumption
print(f"csv memory consumption: {memory_post_csv - memory_init}\n"
      f"Parquet memory consumption: {memory_post_parquet - memory_post_csv}\n"
      f"Arrow file memory consumption: {memory_post_arrowos - memory_post_parquet}\n"
      f"Arrow mapped (no zero-copy) memory consumption: {memory_post_arrowmmap - memory_post_arrowos}\n"
      f"Arrow mapped (zero-copy) memory consumption: {memory_post_arrowmmap_zc - memory_post_arrowmmap}\n")


