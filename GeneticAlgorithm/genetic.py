import os, re
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import math
import numpy as np
from threading import Thread
import time
import json

FILE_NAME = os.path.basename(__file__)
CURR_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(CURR_DIR)
import sys
sys.path.insert(-1, CURR_DIR)
sys.path.insert(-1, BASE_DIR)
import GeneticAlgorithm.test_functions as tf

class Visualization:
    def __init__(self):
        self.a = None


def generte_contours(eval=None):
    delta = 0.025  # 0.025
    x = np.arange(-5.11, 4.11, delta)
    y = np.arange(-4.11, 5.11, delta)
    X, Y = np.meshgrid(x, y)
    Z = eval(X, Y)
    print(Z)
    plt.contour(X, Y, Z, [x * x / 8 for x in range(1, 50)], linewidths=0.5)
    # plt.scatter(np.random.random(),np.linspace(-2,2,20))
    plt.title('Minima ' + str(eval(0, 0)))
    plt.show()
    return
    # plt.plot(X, Y, marker='.',linestyle='none')
    # print(len(X),len(Y))
    # print(y.__len__(), x.__len__())
    # print(x,y)

    points = np.zeros(shape=(len(x) * len(y), 2))
    vals = np.zeros(shape=(len(x) * len(y)))
    print(points)
    i = 0
    for xx in x:
        for yy in y:
            print(xx, yy)
            points[i] = [xx, yy]
            vals[i] = eval(xx, yy)
            i += 1
    print(points, np.min(vals), np.max(vals))


# plt.show()


class Genetic:
    def __init__(self, p, o, mutrate=0.05):
        self.a = None

    @staticmethod
    def generate_parents(self, xrange, yrange, p):
        return


def get_eval(e):
    if e == 'rastringin_gen':
        return tf.rastringin_gen
    elif e == 'camel_hump_six':
        return tf.camel_hump_six


def write_json(data, full):
    with open(full, 'w') as fp:
        json.dump(data, fp, indent=2)


def read_json(full):
    data = None
    with open(full, 'r') as fp:
        data = json.load(fp)
    return data


# gdj = 'h:/nikhil/Development/Python/Projects/Python3_Projects/Genetic/data/gdata.json'
genetic_data_json = f'{CURR_DIR}/gdata.json'


def initialize_genetic_data(m, c, p, of, v, ps, ng, ran, ev):
    """
    m: mutation rate
    c: crossover point
    p: initial population
    of: ratio of offspring to population
    ps: probability of parent selection
    ng: number of genes
    ran: Variable value ranges
    ev: evaluation function
    """
    n_pool = int(p * (1 + of))
    print('n_pool', n_pool)
    gdata = {
        'mutrate': m,
        'crossover_point': c,
        'n_pars': p,
        'n_offsp': of * p,
        'n_vars': v,
        'n_pool': int(p * (1 + of)),
        'parent_selection_prob': ps,
        'n_gens': ng,
        'parents': [0. for x in range(int(v * p))],
        'offspring': [0. for x in range(int(v * of * p))],
        'pool': [0. for x in range(int(v * n_pool))],
        'fitness_off': [0. for x in range(int(of * p))],
        'fitness_pool': [0. for x in range(n_pool)],
        'fitness_pars': [0. for x in range(int(p))],
        'ranges': [x for x in ran],
        'eval_func_name': ev
    }
    write_json(gdata, genetic_data_json)


def generate_parents_old():
    gdata = read_json(genetic_data_json)
    xr = gdata['ranges']
    p = gdata['n_pars']
    nv = gdata['n_vars']
    for i in range(nv):
        rng = gdata['ranges'][i]
        x = np.arange(rng[0], rng[1], (rng[1] - rng[0]) / p)
        gdata['parents'][i] = list(x)
    print(len(gdata['pool']))
    write_json(gdata, genetic_data_json)
    # y = np.arange(xr[2],xr[3],(xr[3]-xr[2])/p)
    return


def sort_by_fitness(population, population_fitness, population_size):
    gdata = read_json(genetic_data_json)
    p = gdata[population_size]
    nv = gdata['n_vars']
    np_vals = np.array(gdata[population])
    np_vals_r = np_vals.reshape(p, nv, order='F')
    np_fits = np.array(gdata[population_fitness])
    # np_full = np.concatenate((np_vals_r,np.array([np_fits]).T),axis=1)
    # print(np_full[np_full[:,-1].argsort()])
    arr_inds = np_fits.argsort()
    np_vals_sorted = np_vals_r[arr_inds]  # [::-1]
    np_fits_sorted = np_fits[arr_inds]
    gdata[population] = list(np_vals_sorted.T.flatten())
    gdata[population_fitness] = list(np_fits_sorted)
    # print(np_vals_sorted)
    # print(np_vals_sorted.T.flatten())
    write_json(gdata, genetic_data_json)


def evaluate_population_fitness(population, population_fitness, pop_size, vals=None):
    time.sleep(0.1)
    gdata = read_json(genetic_data_json)
    p = int(gdata[pop_size])
    nv = gdata['n_vars']
    np_vals = np.array(gdata[population])
    np_vals_r = np_vals.reshape(p, nv, order='F')
    # print(np_vals_r)
    eval = get_eval(gdata['eval_func_name'])
    # all_vals = []
    for i, parent in enumerate(np_vals_r):
        gdata[population_fitness][i] = eval(parent)
    # gdata[out] = all_vals[:]
    write_json(gdata, genetic_data_json)


def generate_parents_np():
    gdata = read_json(genetic_data_json)
    xr = gdata['ranges']
    p = gdata['n_pars']
    nv = gdata['n_vars']
    print(gdata['ranges'])
    npranges = np.array(gdata['ranges'])
    ranges = npranges.reshape(int(nv), int(len(gdata['ranges']) / nv))
    px1 = np.arange(ranges[0][0], ranges[0][1], (ranges[0][1] - ranges[0][0]) / p)
    px1 = np.random.uniform(ranges[0][0], ranges[0][1], p)
    fin = list(px1)
    # print('fin',fin)
    for r in ranges[1:]:
        px = np.arange(r[0], r[1], (r[1] - r[0]) / p)
        px = np.random.uniform(r[0], r[1], p)
        x = np.array(px)
        # print('x',x)
        fin.extend(list(x))
    gdata['parents'] = fin[:]
    write_json(gdata, genetic_data_json)


# print(ranges)

def crossover_parents():
    gdata = read_json(genetic_data_json)
    cp = gdata['crossover_point']
    n_pars = gdata['n_pars']
    nv = gdata['n_vars']
    n_off = int(gdata['n_offsp'])
    np_pars = np.array(gdata['parents'])
    np_pars_r = np_pars.reshape(n_pars, nv, order='F')
    par_indices = np.random.choice([a for a in range(n_pars)], int(gdata['n_offsp']), replace=False)

    coff = 0
    chosen = []
    offspr = np.zeros(shape=(n_off, nv))
    for i in range(n_pars):
        i_par1 = np.random.randint(0, n_pars)
        i_par2 = np.random.randint(0, n_pars)
        while i_par1 in chosen or i_par2 in chosen or i_par2 == i_par1:
            i_par1 = np.random.randint(0, n_pars)
            i_par2 = np.random.randint(0, n_pars)
        chosen.append(i_par1)
        chosen.append(i_par2)
        par1 = np_pars_r[i_par1]
        par2 = np_pars_r[i_par2]
        ch1 = np.zeros(nv)
        ch2 = np.zeros(nv)
        ch1[:cp] = par2[:cp]
        ch2[:cp] = par1[:cp]
        ch1[cp:] = par1[cp:]
        ch2[cp:] = par2[cp:]
        offspr[coff] = ch1
        offspr[coff + 1] = ch2
        # print('Pars', ip1,ip2,par1,par2)
        # print('Ch', ip1,ip2,ch1,ch2)
        coff += 2
        if coff == n_off:
            break

    gdata['offspring'] = list(offspr.T.flatten())
    write_json(gdata, genetic_data_json)


def combine():
    gdata = read_json(genetic_data_json)
    p = gdata['n_pars']
    nv = gdata['n_vars']
    gdata['pool'][:p * nv] = gdata['parents'][:]
    gdata['pool'][p * nv:] = gdata['offspring'][:]
    gdata['fitness_pool'][:p] = gdata['fitness_pars'][:]
    gdata['fitness_pool'][p:] = gdata['fitness_off'][:]
    write_json(gdata, genetic_data_json)


def select_new_population():
    """
    Selects new parents from combined parents and offspring
    :return:
    """
    gdata = read_json(genetic_data_json)
    p = gdata['n_pars']
    npool = gdata['n_pool']
    nv = gdata['n_vars']
    n_off = int(gdata['n_offsp'])
    np_pars = np.array(gdata['parents'])
    np_pars_r = np_pars.reshape(p, nv, order='F')
    np_pool = np.array(gdata['pool'])
    np_pool_r = np_pool.reshape(npool, nv, order='F')

    new_generation = np.zeros(shape=(p, nv))
    top_n_pars = int(0.75 * p)
    # print(0,topn)
    # select to best people from the group
    for i in range(top_n_pars):
        newpar = np.copy(np_pool_r[i])
        new_generation[i] = newpar

    chosen = []
    # print(topn,p)
    # Select some people from the bottom
    for i in range(top_n_pars, p):
        ni = np.random.randint(top_n_pars, npool)
        while ni in chosen:
            ni = np.random.randint(top_n_pars, npool)
        chosen.append(ni)
        newpar = np.copy(np_pool_r[ni])
        new_generation[i] = newpar
    # print(len(newgen.T.flatten()))
    gdata['parents'] = list(new_generation.T.flatten())
    write_json(gdata, genetic_data_json)


def mutate_population():
    gdata = read_json(genetic_data_json)
    write_json(gdata, './before.json')
    p = gdata['n_pars']
    nv = gdata['n_vars']
    mut_rate = int(gdata['mutrate'] * p)
    np_ranges = np.array(gdata['ranges'])
    np_ranges_r = np_ranges.reshape(int(nv), int(len(gdata['ranges']) / nv))

    chosen = []
    for i in range(mut_rate):
        rai = np.random.randint(0, p * nv)
        while rai in chosen:
            rai = np.random.randint(0, p * nv)
        chosen.append(rai)
        # print(rai, rai%nv)
        r_i = rai % nv
        mut = np.random.uniform(np_ranges_r[r_i][0], np_ranges_r[r_i][1], 1)
        # print(rai, rai%nv, mut)
        gdata['parents'][rai] = mut[0]
    write_json(gdata, genetic_data_json)
    return


# time.sleep(0.05)

# do_crossover()

def try_numpy():
    arr = np.arange(1, 13, 1)
    larr = list(arr)
    print(arr)
    ar = np.array(larr)
    r1 = ar.reshape(6, 2, order='F')
    print(r1)
    r2 = ar.reshape(6, 2)
    print(r2)
    print(list(r2), [[6, 8], [7, 9]])
# generte_contours(rastringin)
# print(rastringin(0,0))

# try_numpy()
