import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import numpy as np
import json
import GeneticAlgorithm.test_functions as tf


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='interval-component',
            interval=1000,
            n_intervals=0
        ),
    ]
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    lon = n % 100
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Longitude: {0:.2f}'.format(n), style=style),
    ]


def read_genetic_data(n):
    with open('./anim/for_anim0.json', 'r') as fp:
        gdata = json.load(fp)
        p = int(gdata['n_pars'])
        i = n % p
    with open('./anim/for_anim'+str(i)+'.json', 'r') as fp:
        gdata = json.load(fp)

    p = int(gdata['n_pars'])
    nv = int(gdata['n_vars'])
    np_ranges = np.array(gdata['ranges'])
    ranges = np_ranges.reshape(nv, int(len(gdata['ranges']) / nv))

    np_pars = np.array(gdata['parents'])
    # np_pars_r = np_pars.reshape(p, nv, order='F')

    eval_func = None
    if gdata['eval_func_name'] == 'rastringin_gen':
        eval_func = tf.rastringin_gen
    # print(ranges)
    # x = np.arange(ranges[0][0]-1.,ranges[0][1]+2.,0.05)
    # y = np.arange(ranges[1][0]-1.,ranges[1][1]+2.,0.05)
    # X, Y = np.meshgrid(x, y)
    # Z = rastringin(X, Y)
    # gax1.contour(X,Y,Z,[x*x/32 for x in range(1,50)],linewidths=0.25)

    # xp = np.random.uniform(low=-5.11, high=4.11, size=(50,))
    # yp = np.random.uniform(low=-4.11, high=5.11, size=(50,))
    xp = gdata['parents'][0:p]
    yp = gdata['parents'][p:p*nv]
    zp = gdata['fitness_pars']
    return ranges, xp, yp, zp, eval_func


def get_contours():
    with open('./anim/for_anim0.json', 'r') as fp:
        gdata = json.load(fp)
        p = int(gdata['n_pars'])

    x = np.arange(-6., 6., 0.05)
    y = np.arange(-6., 6., 0.05)
    [X, Y] = np.meshgrid(x, y)

    eval_func = None
    if gdata['eval_func_name'] == 'rastringin_gen':
        eval_func = tf.rastringin_gen

    Z = eval_func([X, Y])
    return X, Y, Z


X, Y, Z = get_contours()
print(X.shape, Y.shape, Z.shape)

@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_scatter(n):
    ranges, xp, yp, zp, eval_func = read_genetic_data(n)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xp,
        y=yp,
        mode='markers',
        marker=dict(size=10, opacity=0.5,
                    line=dict(width=1, color='grey'))
    ))
    fig.add_trace(go.Contour(
        z=Z,
        # x=X,
        # y=Y
    ))
    fig.update_layout(width=750, height=750)

    return fig


if __name__ == '__main__':
    app.run_server()
