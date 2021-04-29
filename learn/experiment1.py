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

import numpy as np
def numpy_cols():
    import pandas as pd


    n_cols = 2
    tarr = np.arange(3*n_cols).reshape(3, n_cols) # , order='F')
    df = pd.DataFrame(tarr, columns=[f'col{x}' for x in range(n_cols)])
    print(df)
    adict = {
        "pars": tarr.tolist()
    }

cp = 1
a = [1, 2]
b = [3, 4]
c = [0, 0]
c[:cp] = a[:cp]
c[cp:] = b[cp:]
print(c, [np.random.randint(1,3) for x in range(10)])
import json
# print(json.dumps(adict, indent=2))

# while len(values) > 1:
#     print(f'Values b: {values}')
#     values = values[2:] + [add(values[0], values[1])]
#     print(f'values: {values}')

import plotly.graph_objects as go


def rastringin_gen(xx, n=2, A=1):
    def calc(xv):
        return np.square(xv) - A * np.cos(2 * np.pi * xv)

    summation = 0
    for x in xx:
        summation += calc(x)
    fx = A * n + summation
    return fx


feature_x = np.arange(-5.11, 5.11, 0.05)
feature_y = np.arange(-5.11, 5.11, 0.05)

# Creating 2-D grid of features
[X, Y] = np.meshgrid(feature_x, feature_y)

# Z = np.cos(X / 2) + np.sin(Y / 4)
Z = rastringin_gen([X, Y])

print(X.shape)
print(Y.shape)
print(Z.shape)
fig = go.Figure()
# fig.add_trace(
#     go.Contour(
#         z=Z1, x=feature_x, y=feature_y,
#         autocontour=False, contours=dict(coloring='lines', size=1, start=0, end=2),
#         # colorscale='rainbow'
#         ))
fig.add_trace(go.Surface(z=Z, x=feature_x, y=feature_y, opacity=0.2))
fig.update_layout(title='Rastringin', autosize=False,
                  width=750, height=750,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()
