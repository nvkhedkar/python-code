import math
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib import cm
import seaborn as sns
import json
import GeneticAlgorithm.test_functions as tf


def get_contours():
    with open('./anim/for_anim0.json', 'r') as fp:
        gdata = json.load(fp)
        p = int(gdata['n_pars'])

    # x = np.arange(-5., 5., 0.05)
    # y = np.arange(-5., 5., 0.05)
    x = np.arange(-2., 2., 0.01)
    y = np.arange(-2., 2., 0.01)
    [X, Y] = np.meshgrid(x, y)

    eval_func = None
    if gdata['eval_func_name'] == 'rastringin_gen':
        eval_func = tf.rastringin_gen
    elif gdata['eval_func_name'] == 'camel_hump_six':
        eval_func = tf.camel_hump_six

    Z = eval_func([X, Y])
    return X, Y, Z, x, y


def read_genetic_data(n):
    with open('./anim/for_anim0.json', 'r') as fp:
        gdata = json.load(fp)
        p = int(gdata['n_pars'])
        i = n % p
    with open('./anim/for_anim' + str(i) + '.json', 'r') as fp:
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
    elif gdata['eval_func_name'] == 'camel_hump_six':
        eval_func = tf.camel_hump_six
    # print(ranges)
    # x = np.arange(ranges[0][0]-1.,ranges[0][1]+2.,0.05)
    # y = np.arange(ranges[1][0]-1.,ranges[1][1]+2.,0.05)
    # X, Y = np.meshgrid(x, y)
    # Z = rastringin(X, Y)
    # gax1.contour(X,Y,Z,[x*x/32 for x in range(1,50)],linewidths=0.25)

    # xp = np.random.uniform(low=-5.11, high=4.11, size=(50,))
    # yp = np.random.uniform(low=-4.11, high=5.11, size=(50,))
    xp = gdata['parents'][0:p]
    yp = gdata['parents'][p:p * nv]
    zp = gdata['fitness_pars']
    return ranges, xp, yp, zp, eval_func


print(matplotlib.__version__)


class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""

    def __init__(self, numpoints=50, stream_func=None):
        self.numpoints = numpoints
        self.stream = self.data_stream()
        if stream_func:
            self.stream = stream_func

        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        self.fig.set_figheight(10)
        self.fig.set_figwidth(10)
        # self.fig = plt.figure() # figsize=(12, 12)
        # self.cx = self.fig.add_subplot(1, 2, 1)
        # self.ax = self.fig.add_subplot(1, 2, 1)
        # Then setup FuncAnimation.
        self.ani = FuncAnimation(self.fig, self.update, interval=1000,
                                 init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        CX, CY, CZ, cx, cy = get_contours()
        # gax1 = self.fig.add_subplot(1, 2, 1)
        self.ax.contour(CX, CY, CZ, [x * x / 16 for x in range(1, 50)], linewidths=0.15)

        x, y, s, c = next(self.stream).T
        self.scat = self.ax.scatter(x, y,
                                    # c=c, s=s,
                                    vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")
        # self.ax.axis([-5, 5, -5, 5])
        self.ax.axis([-2, 2, -2, 2])
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def data_stream(self):
        """Generate a random walk (brownian motion). Data is scaled to produce
        a soft "flickering" effect."""
        xy = (np.random.random((self.numpoints, 2)) - 0.5) * 10
        s, c = np.random.random((self.numpoints, 2)).T
        while True:
            xy += 0.03 * (np.random.random((self.numpoints, 2)) - 0.5)
            s += 0.05 * (np.random.random(self.numpoints) - 0.5)
            c += 0.02 * (np.random.random(self.numpoints) - 0.5)
            yield np.c_[xy[:, 0], xy[:, 1], s, c]

    def update(self, i):
        ranges, xp, yp, zp, eval_func = read_genetic_data(i % 100)
        self.scat = self.ax.scatter(xp, yp, s=40,
                                    # c=c, s=s,
                                    vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k", alpha=0.5)
        return self.scat,

    def update_(self, i):
        """Update the scatter plot."""
        data = next(self.stream)
        # Set x and y data...
        self.scat.set_offsets(data[:, :2])
        # Set sizes...
        self.scat.set_sizes(300 * abs(data[:, 2]) ** 1.5 + 100)
        # Set colors..
        self.scat.set_array(data[:, 3])

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,


if __name__ == '__main__':
    a = AnimatedScatter()
    plt.show()
