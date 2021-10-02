
def pallindrome(word):
    middle = int(len(word)/2)
    print(word[0:middle], word[-1*middle:])
    return word[0:middle] == word[-1*middle:][::-1]

import pandas as pd
import requests
x = requests.get(url='https://query.data.world/s/vBDCsoHCytUSLKkLvq851k2b8JOCkF', verify=False).content
df = pd.read_csv(x.decode('utf8'))
df_2 = df.loc[2:20, :]
print(df_2)
