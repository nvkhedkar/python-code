# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# %%
nums = np.random.uniform(100, 200, 1_000_000).astype(np.float32)
print(nums)
n = 100
samples = np.array([np.random.choice(nums, 100) for x in range(200)], np.float32)
print(samples.shape)



