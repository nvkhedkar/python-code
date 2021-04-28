import os, re, sys
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import math
import numpy as np
# from threading import Thread
import time
import json
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = os.path.basename(__file__)
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = f'{BASE_DIR}/data_pyworker/genetic_demo'
sys.path.insert(-1, SCRIPT_DIR)
sys.path.insert(-1, BASE_DIR)
print(BASE_DIR)
from GeneticAlgorithm.genetic import *
import copy

POPULATION = 50
GENERATIONS = 100
USE_STOPPING = 0
N_VARS = 2
LABELS = ['ref_vol_percent', 'redistribution']
RANGES = [-5.11, 4.2, -5.11, 4.2] # [10, 90, 5, 70, 0, 7, 20, 45]
# N_VARS = 3
# LABELS = ['ref_vol_percent', 'redistribution', 'material']
# RANGES = [10, 90, 5, 70, 0, 7]
# N_VARS = 2
# LABELS = ['ref_vol_percent', 'redistribution']
# RANGES = [10, 90, 5, 70]
OBJ_FUNC = 'stress'
EVAL_FUNC = tf.rastringin_gen


def function_eval_default(i_genr, gdata, population, np_vals_r, pop_size, n_vars):
    time.sleep(0.05)
    all_vals = [0. for i in range(pop_size)]
    for i, parent in enumerate(np_vals_r):
        all_vals[i] = EVAL_FUNC(parent)
    return all_vals


def evaluate_population_fitness(i_genr, population, population_fitness, pop_size, vals=None):
    gdata = read_json(genetic_data_json)
    p = int(gdata[pop_size])
    nv = gdata['n_vars']
    np_vals = np.array(gdata[population])
    np_vals_r = np_vals.reshape(p, nv, order='F')

    # function_eval_dummy, function_evaluation
    fitness_values = function_eval_default(i_genr, gdata, population, np_vals_r, p, nv)
    for i, fv in enumerate(fitness_values):
        gdata[population_fitness][i] = fv
        gdata[f'id_{population}'][i] = f'gen{i_genr}_{population}{i}'
    write_json(gdata, genetic_data_json)


best_results = {}


def write_to_result_file(i, gdata):
    with open('./results.txt', 'a') as f:
        p = gdata['n_pars']
        nv = gdata['n_vars']
        np_pars_r = np.array(gdata['parents']).reshape(p, nv, order='F')
        top_genes = gdata['fitness_pars'][0:5]
        f.write(f"Generation: {i}\n")
        print(f"Gen [{i}]: {np_pars_r[0]} val: {np.average(gdata['fitness_pars'][0:3])}")
        for i, fitness in enumerate(top_genes):
            vars = np_pars_r[i]
            var_str = ''
            # for j,var in enumerate(vars):
            #     var_str += f"{gdata['labels'][j]}: {var}, "
            # print(np_pars_r[i], fitness)
            f.write(f"\t{var_str} Value: {fitness}\n")
        f.write(f"{json.dumps(best_results, indent=2)}\n")
    return


def keep_best_results(i, gdata):
    p = gdata['n_pars']
    nv = gdata['n_vars']
    np_pars_r = np.array(gdata['parents']).reshape(p, nv, order='F')
    top_genes = gdata['fitness_pars'][0:2]
    locations = gdata['id_parents'][0:2]
    if not best_results:
        best_results['fitness_pars'] = gdata['fitness_pars'][0:2]
        best_results['id_parents'] = gdata['id_parents'][0:2]
        shaped_pars = np_pars_r[0:2]
        best_results['parents'] = list(shaped_pars.T.flatten())
    else:
        if best_results['fitness_pars'][0] > gdata['fitness_pars'][0]:
            best_results['fitness_pars'][1] = best_results['fitness_pars'][0]
            best_results['fitness_pars'][0] = gdata['fitness_pars'][0]
            best_results['id_parents'][1] = best_results['id_parents'][0]
            best_results['id_parents'][0] = gdata['id_parents'][0]
            shaped_pars = np.array(best_results['parents']).reshape(2, nv, order='F')
            shaped_pars[1] = shaped_pars[0]
            shaped_pars[0] = np_pars_r[0]
            best_results['parents'] = list(shaped_pars.T.flatten())
    return


def get_readable_gdata(gdata):
    np_pars_r = flat_array_to_nd_array(gdata, 'n_pars', 'n_vars', 'parents')
    np_off_r = flat_array_to_nd_array(gdata, 'n_offsp', 'n_vars', 'offspring')
    np_pool_r = flat_array_to_nd_array(gdata, 'n_pool', 'n_vars', 'pool')
    new_gdata = copy.deepcopy(gdata)
    new_gdata['parents'] = np_pars_r.tolist()
    new_gdata['offspring'] = np_off_r.tolist()
    new_gdata['pool'] = np_pool_r.tolist()
    return new_gdata


def process_results(i):
    gdata = read_json(genetic_data_json)
    # print('-' * 60)
    # print(i, gdata['fitness_pars'][0:5])
    # print('=' * 90)
    keep_best_results(i, gdata)
    gdata['best_results'] = best_results

    write_json(gdata, './anim/for_anim' + str(i) + '.json')
    write_json(get_readable_gdata(gdata), './anim/to_read_' + str(i) + '.json')

    write_to_result_file(i, gdata)
    return gdata


def run_genetic_algo():
    if os.path.exists('./results.txt'):
        os.unlink('./results.txt')
    population = POPULATION
    initialize_genetic_data(m=0.12, c=1, p=population, of=0.8, v=N_VARS, ps=0.8, ng=20,
                            ran=RANGES,
                            ev='rastringin_gen',
                            ev_func=function_eval_default,
                            labels=LABELS
                            # ran=[-5.1, 4, -5.1, 4],  # [-5.11,4.11,-4.11,5.11],
                            # ev='rastringin_gen'
                            )  # 'rastringin_gen') camel_hump_six
    conv = 0.0001
    last = 10
    diff = 0
    for i in range(GENERATIONS):
        if i == 0:
            generate_parents_np(i)
        else:
            mutate_population(i)
        evaluate_population_fitness(i, 'parents', 'fitness_pars', 'n_pars')
        sort_by_fitness('parents', 'fitness_pars', 'n_pars')
        crossover_parents()
        evaluate_population_fitness(i, 'offspring', 'fitness_off', 'n_offsp')
        combine(i)
        sort_by_fitness('pool', 'fitness_pool', 'n_pool')
        select_new_population()

        gdata = process_results(i)
        if USE_STOPPING:
            currav = np.average(gdata['fitness_pars'][0:int(0.05 * population)])
            if abs(currav - last) <= conv:
                diff += 1
            print(i, currav, currav - last, diff, gdata['fitness_pars'][0])
            last = currav
            if diff >= 5:
                break




run_genetic_algo()
