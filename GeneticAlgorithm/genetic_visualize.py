import math
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm
import json


def get_eval(e):
    if e == 'rastringin_gen':
        return rastringin_gen
    elif e == 'camel_hump_six':
        return camel_hump_six


def camel_hump_six(x1, x2):
    x1_2 = np.square(x1)
    x1_4 = np.square(x1_2)
    x2_2 = np.square(x2)
    term1 = (4.0 - 2.1*x1_2 + x1_4/3.0)*x1_2
    # term1 = term1*x1_2
    prod  = x1*x2
    term2 = (4.0*x2_2 - 4)*x2_2
    # term2 = term2*x2_2
    fx = term1 + prod + term2
    return fx

def sine_cosine(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

def rastringin(x1,x2,n=2.,A=5.):
    def calc(x):
        return np.square(x)-A*np.cos(2*np.pi*x)
    fx = A*n + calc(x1) + calc(x2)
    return fx

def rastringin_gen(xx,n=2,A=1):
    def calc(x):
        return np.square(x)-A*np.cos(2*np.pi*x)
    sum = 0
    for x in xx:
        sum += calc(x)
    fx = A*n + sum
    return fx


class ShowProgress(object):
    def __init__(self, ax, delta, eval):
        self.x = np.arange(-5.11, 4.11, delta)
        self.y = np.arange(-4.11, 5.11, delta)
        self.eval = eval
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.Z = self.eval(self.X,self.Y)
        self.contours = ax.contour(self.X, self.Y, self.Z, [x*x/8 for x in range(1,50)],linewidths=0.5)
        self.pnts = ax.scatter([],[], marker='.',s=1)
        self.ax = ax

    def init(self):
        # self.X, self.Y = np.meshgrid(self.x, self.y)
        # self.Z = self.eval(self.X,self.Y)
        # self.contours.set_data(self.X, self.Y, self.Z, [x*x/8 for x in range(1,50)])
        # self.ax.contour(self.X, self.Y, self.Z, [x*x/8 for x in range(1,50)],linewidths=0.5)
        return self.contours
        # self.ax.title('Minima '+str(self.eval(0,0)))

    def __call__(self, *args, **kwargs):
        xp = np.random.uniform(low=-5.11, high=4.11, size=(50,))
        yp = np.random.uniform(low=-4.11, high=5.11, size=(50,))
        self.pnts.set_data(xp,yp,marker='.',markersize=1)
        return self.pnts


def generte_contours(i=0):
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 2, 1)
    delta = 0.05#0.025
    x = np.arange(-5.,5.,delta)
    y = np.arange(-5.,5.,delta)
    X, Y = np.meshgrid(x, y)
    Z = rastringin(X,Y)
    print(Z)
    ax1.clear()
    ax1.contour(X,Y,Z,[x*x/8 for x in range(1,50)],linewidths=0.5)
    xp = np.random.uniform(low=-5.11, high=5.11, size=(50,))
    yp = np.random.uniform(low=-5.11, high=5.11, size=(50,))
    zp = rastringin(xp, yp)
    ax1.scatter(xp,yp,marker='.',s=9)
    # plt.scatter(np.random.random(),np.linspace(-2,2,20))
    # plt.title('Minima '+str(eval(0,0)))
    # plt.show()

    ax2 = fig1.add_subplot(1,2,2, projection='3d')
    ax2.plot_surface(X, Y, Z, cmap=cm.get_cmap('Spectral', 12),
                     linewidth=0, alpha=0.5, antialiased=False)
    ax2.scatter(xp,yp, zp, marker='.',s=9, alpha=1)
    plt.show()
    return


cont_flg = 0
def view_genetic(i, scat):
    gdata = None
    print(i)
    if(i==83):return
    with open('./anim/for_anim'+str(i)+'.json', 'r') as fp:
        gdata = json.load(fp)
    xr = gdata['ranges']
    p = gdata['n_pars']
    nv = gdata['n_vars']
    # print(gdata['ranges'])
    npranges = np.array(gdata['ranges'])
    ranges = npranges.reshape(int(nv),int(len(gdata['ranges'])/nv))

    np_pars = np.array(gdata['parents'])
    np_pars_r = np_pars.reshape(p, nv, order='F')
    eval = get_eval(gdata['eval_func_name'])
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
    for s in scat:
        s.clear()
    scat = [gax3.scatter(xp,yp,marker='.',s=15)]

    # XP,YP = np.meshgrid(xp,yp)
    # zp = rastringin(XP,YP)#gdata['fitness_pars']
    # gax2 = fig.add_subplot(1,2,2, projection='3d')
    # gax2.plot_surface(X, Y, Z, cmap=cm.get_cmap('Spectral', 12),
    #                   linewidth=0, alpha=0.5, antialiased=False)
    # gax2.scatter(XP,YP,zp, marker='.',s=15, alpha=1)
    return scat,

np.random.seed(19680801)


# generte_contours()
x = np.arange(-6., 6., 0.05)
y = np.arange(-6., 6., 0.05)
X, Y = np.meshgrid(x, y)
# Z = rastringin(X,Y)
Z = rastringin(X, Y)
# print(Z)

fig = plt.figure(figsize=(12,6))
gax1 = fig.add_subplot(1, 2, 1)
gax1.contour(X, Y, Z, [x * x / 32 for x in range(1, 50)], linewidths=0.25)
# gax2 = fig.add_subplot(1, 2, 2)
gax3 = fig.add_subplot(1, 2, 1)
scat1 = [gax3.scatter([0,0],[1,1])]
# gax4 = fig.add_subplot(1, 2, 2)
anim = FuncAnimation(fig,view_genetic,fargs=(scat1),interval=500,blit=False)
plt.show()

# ud = ShowProgress(ax, 0.025, rastringin)
# anim = FuncAnimation(fig, ud, init_func=ud.init, interval=100, blit=True)

