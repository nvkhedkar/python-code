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
import GeneticAlgorithm.genetic_data as gd


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


def get_eval(e):
    if e == 'rastringin_gen':
        return tf.rastringin_gen
    elif e == 'camel_hump_six':
        return tf.camel_hump_six


def flat_array_to_nd_array(gdata, rows, cols, population, order='F'):
    n_p = int(gdata[rows])
    nv = gdata[cols]
    np_vals = np.array(gdata[population])
    return np_vals.reshape(n_p, nv, order=order)


def evaluate_parents(i_genr, gdata, population_fitness, np_vals_r, pop_size, n_vars):
    eval = get_eval(gdata['eval_func_name'])
    all_vals = [0. for i in range(pop_size)]
    for i, parent in enumerate(np_vals_r):
        all_vals[i] = eval(parent)
    return all_vals


eval_function = evaluate_parents
read_data_function = gd.read_genetic_data
write_data_function = gd.write_genetic_data


def initialize_genetic_data(m, c, p, of, v, ps, ng, ran, ev, labels=None, ev_func=None):
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
    if ev_func:
        eval_function = ev_func
    if not labels:
        labels = [f'var{x+1}'for x in range(v)]
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
        'id_offspring': [0. for x in range(int(of * p))],
        'id_pool': [0. for x in range(n_pool)],
        'id_parents': [0. for x in range(int(p))],
        'ranges': [x for x in ran],
        'labels': labels,
        'eval_func_name': ev
    }
    write_data_function(gdata)


def generate_parents_old():
    gdata = read_data_function()
    xr = gdata['ranges']
    p = gdata['n_pars']
    nv = gdata['n_vars']
    for i in range(nv):
        rng = gdata['ranges'][i]
        x = np.arange(rng[0], rng[1], (rng[1] - rng[0]) / p)
        gdata['parents'][i] = list(x)
    print(len(gdata['pool']))
    write_data_function(gdata)
    # y = np.arange(xr[2],xr[3],(xr[3]-xr[2])/p)
    return


def sort_by_fitness(population, population_fitness, population_size):
    gdata = read_data_function()
    p = gdata[population_size]
    nv = gdata['n_vars']
    np_vals = np.array(gdata[population])
    np_vals_r = np_vals.reshape(p, nv, order='F')
    np_fits = np.array(gdata[population_fitness])
    np_locs = np.array(gdata[f'id_{population}'])
    # np_full = np.concatenate((np_vals_r,np.array([np_fits]).T),axis=1)
    # print(np_full[np_full[:,-1].argsort()])
    arr_inds = np_fits.argsort()
    np_vals_sorted = np_vals_r[arr_inds]  # [::-1]
    np_fits_sorted = np_fits[arr_inds]
    np_locs_sorted = np_locs[arr_inds]
    gdata[population] = list(np_vals_sorted.T.flatten())
    gdata[population_fitness] = list(np_fits_sorted)
    gdata[f'id_{population}'] = list(np_locs_sorted)
    # print(np_vals_sorted)
    # print(np_vals_sorted.T.flatten())
    write_data_function(gdata)


def evaluate_population_fitness(i_genr, population, population_fitness, pop_size, vals=None):
    gdata = read_data_function()
    p = int(gdata[pop_size])
    nv = gdata['n_vars']
    np_vals = np.array(gdata[population])
    np_vals_r = np_vals.reshape(p, nv, order='F')

    fitness_values = eval_function(i_genr, gdata, population_fitness, np_vals_r, p, nv)
    for i, fv in enumerate(fitness_values):
        gdata[population_fitness][i] = fv
    write_data_function(gdata)


def generate_parents_np(i=0):
    gdata = read_data_function()
    # xr = gdata['ranges']
    p = gdata['n_pars']
    nv = gdata['n_vars']
    print(gdata['ranges'])
    npranges = np.array(gdata['ranges'])
    ranges = npranges.reshape(int(nv), int(len(gdata['ranges']) / nv))
    # ranges = npranges.reshape(int(len(gdata['ranges']) / nv), int(nv))
    # px1 = np.arange(ranges[0][0], ranges[0][1], (ranges[0][1] - ranges[0][0]) / p)
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
    write_data_function(gdata)


def crossover_parents():
    gdata = read_data_function()
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
        coff += 2
        if coff == n_off:
            break

    gdata['offspring'] = list(offspr.T.flatten())
    write_data_function(gdata)


def mutate_population_readable(i_gen=0):
    gdata = read_data_function()
    gd.write_json(gdata, './before.json')
    p = gdata['n_pars']
    nv = gdata['n_vars']
    n_mutate = int(gdata['mutrate'] * p)
    np_pars = np.array(gdata['parents'])
    np_pars_r = np_pars.reshape(p, nv, order='F')
    np_ranges = np.array(gdata['ranges'])
    np_ranges_r = np_ranges.reshape(int(nv), int(len(gdata['ranges']) / nv))

    chosen = []
    for i in range(n_mutate):
        rai = np.random.randint(0, p * 0.8)
        while rai in chosen:
            rai = np.random.randint(0, p * 0.8)
        chosen.append(rai)
        # print(rai, rai%nv)
        r_i = np.random.randint(0, nv) # int(rai / p)
        mut = np.random.uniform(np_ranges_r[r_i][0], np_ranges_r[r_i][1], 1)
        # print(rai, rai%nv, mut)
        before = np_pars_r[rai]
        # print(f'before {i_gen}: {before}')
        np_pars_r[rai][r_i] = mut[0]
        # print(f'after {i_gen}: {np_pars_r[rai]}')
        # print(f'{i_gen} aft:{np_pars_r[rai]} mut:{mut[0]}, rai:{rai}, r_i:{r_i} [{np_ranges_r[r_i][0]}, {np_ranges_r[r_i][1]}]')
    gdata['parents'] = list(np_pars_r.T.flatten())
    write_data_function(gdata)


def combine(i=0):
    gdata = read_data_function()
    p = gdata['n_pars']
    n_off = int(gdata['n_offsp'])
    nv = gdata['n_vars']
    np_pars_r = np.array(gdata['parents']).reshape(p, nv, order='F')
    np_off_r = np.array(gdata['offspring']).reshape(n_off, nv, order='F')

    np_pool = np.concatenate((np_pars_r, np_off_r), axis=0)
    gdata['pool'] = list(np_pool.T.flatten())
    gdata['fitness_pool'][:p] = gdata['fitness_pars'][:]
    gdata['fitness_pool'][p:] = gdata['fitness_off'][:]
    gdata['id_pool'][:p] = gdata['id_parents'][:]
    gdata['id_pool'][p:] = gdata['id_offspring'][:]
    write_data_function(gdata)


def select_new_population():
    """
    Selects new parents from combined parents and offspring
    :return:
    """
    gdata = read_data_function()
    p = gdata['n_pars']
    npool = gdata['n_pool']
    nv = gdata['n_vars']
    n_off = int(gdata['n_offsp'])
    np_pars_r = np.array(gdata['parents']).reshape(p, nv, order='F')
    np_pool_r = np.array(gdata['pool']).reshape(npool, nv, order='F')
    np_pool_fitness = np.array(gdata['fitness_pool'])
    np_pars_fitness = np.array(gdata['fitness_pars'])

    new_generation = np.zeros(shape=(p, nv))
    top_n_pars = int(0.7 * p)
    # print(0,topn)
    # select to best people from the group
    for i in range(top_n_pars):
        newpar = np.copy(np_pool_r[i])
        new_generation[i] = newpar
        np_pars_fitness[i] = np_pool_fitness[i]

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
        np_pars_fitness[i] = np_pool_fitness[ni]
    # print(len(newgen.T.flatten()))
    gdata['parents'] = list(new_generation.T.flatten())
    gdata['fitness_pars'] = list(np_pars_fitness)
    write_data_function(gdata)


def mutate_population(i_gen=0):
    gdata = read_data_function()
    gd.write_json(gdata, './before.json')
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
        r_i = int(rai / p)
        mut = np.random.uniform(np_ranges_r[r_i][0], np_ranges_r[r_i][1], 1)
        # print(rai, rai%nv, mut)
        before = gdata['parents'][rai]
        gdata['parents'][rai] = mut[0]
        # print(f'{i_gen} bef:{before}, aft:{mut[0]}, rai:{rai}, r_i:{r_i} [{np_ranges_r[r_i][0]}, {np_ranges_r[r_i][1]}]')
    write_data_function(gdata)
    return


def mutate_population_keep_top(i_gen, top=2, exclude_bottom=0.8):
    gdata = read_data_function()
    gd.write_json(gdata, './before.json')
    p = gdata['n_pars']
    nv = gdata['n_vars']
    mut_rate = int(gdata['mutrate'] * p)
    np_ranges = np.array(gdata['ranges'])
    np_ranges_r = np_ranges.reshape(int(nv), int(len(gdata['ranges']) / nv))

    chosen = []
    for i in range(mut_rate):
        rai = np.random.randint(0, p * nv)
        while (rai in chosen) or (rai % p < top):
            rai = np.random.randint(0, p * nv)
        chosen.append(rai)
        # print(rai, rai%nv)
        r_i = int(rai / p)
        mut = np.random.uniform(np_ranges_r[r_i][0], np_ranges_r[r_i][1], 1)
        # print(rai, rai%nv, mut)
        before = gdata['parents'][rai]
        gdata['parents'][rai] = mut[0]
        print(f'{i_gen} bef:{before}, aft:{mut[0]}, rai:{rai}({rai % p}), r_i:{r_i} [{np_ranges_r[r_i][0]}, {np_ranges_r[r_i][1]}]')
    write_data_function(gdata)
    return
