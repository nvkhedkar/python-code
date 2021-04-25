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
print(BASE_DIR)
from GeneticAlgorithm.genetic import *


def do_genetic():
    population = 50
    initialize_genetic_data(m=0.12, c=1, p=population, of=0.8, v=3, ps=0.8, ng=20,
                            ran=[0, 5, 6, 10, 11, 15],
                            ev='rastringin_gen'
                            # ran=[-5.1, 4, -5.1, 4],  # [-5.11,4.11,-4.11,5.11],
                            # ev='rastringin_gen'
                            )  # 'rastringin_gen') camel_hump_six
    generate_parents_np()
    conv = 0.0001
    last = 10
    diff = 0
    for i in range(100):
        evaluate_population_fitness('parents', 'fitness_pars', 'n_pars')
        sort_by_fitness('parents', 'fitness_pars', 'n_pars')
        crossover_parents()
        evaluate_population_fitness('offspring', 'fitness_off', 'n_offsp')
        combine()
        sort_by_fitness('pool', 'fitness_pool', 'n_pool')
        select_new_population()
        mutate_population()
        gdata = read_json(genetic_data_json)
        currav = np.average(gdata['fitness_pars'][0:int(0.05 * population)])
        if abs(currav - last) <= conv:
            diff += 1

        print(i, currav, currav - last, diff, gdata['fitness_pars'][0])
        last = currav
        write_json(gdata, './anim/for_anim' + str(i) + '.json')
        if diff >= 5:
            break


do_genetic()
