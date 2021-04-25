import shortuuid as suid
import time, os
from datetime import datetime


def get_task_id():
    dt_obj = datetime.utcnow()
    curr_time = dt_obj.strftime("%Y%b%d-%H%M%S-%f")[:-3]
    num_digits = 32-len(curr_time)
    my_rn = suid.ShortUUID().random(num_digits)
    fr = f'{curr_time}-{my_rn}'
    print(fr, num_digits)
    print(str(dt_obj.timestamp()))

# full = "nvk.txt"
# filename = os.path.dirname(full)
# if not filename:
#     print('No directory')
# print(f'Filename: {filename}')

values = [x + 1 for x in range(10)]


def add(x, y):
    return x + y


# print(values[2:] + [66])

timestamp = int(time.mktime(datetime.utcnow().timetuple()))
print(timestamp)

import pandas as pd
import numpy as np

n_cols = 2
tarr = np.arange(3*n_cols).reshape(3, n_cols) # , order='F')
df = pd.DataFrame(tarr, columns=[f'col{x}' for x in range(n_cols)])
print(df)
adict = {
    "pars": tarr.tolist()
}
import json
# print(json.dumps(adict, indent=2))

# while len(values) > 1:
#     print(f'Values b: {values}')
#     values = values[2:] + [add(values[0], values[1])]
#     print(f'values: {values}')