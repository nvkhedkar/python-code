from __future__ import absolute_import, unicode_literals
from .celery import app
from celery import Task, group, chord, chain
from celery.task.control import revoke
import time,re,random,sys, json
import numpy as np
import os
sys.path.insert(0, os.getenv(GENETIC_ROOT_PATH, '.'))
import genetic as ga


class TaskHelper(Task):
	def on_success(self, retval, task_id, args, kwargs):
		print('SUCCESS '+ self.request.task)
		return
	def run_init(self,meta):
		return


@app.task(base=TaskHelper, bind=True, name='init')
def init(self, meta=None):
	print('INIT_GENETIC',meta)
	population = 10
	ga.initialize_genetic_data(m=0.12,c=1,p=population,of=0.8,v=2,ps=0.8,ng=20,
													ran=[-3.1,3,-2.1,2],#[-5.11,4.11,-4.11,5.11],
													ev = 'camel_hump_six')#'rastringin_gen') camel_hump_six

	ga.generate_parents_np()

	for i in range(2):
		meta['curr_iteration'] = i
		res = app.send_task('evaluate_all_sort', kwargs={'meta':meta},
												queue='genetic.common')
		while not res.ready():
			time.sleep(0.1)

	# fullga = []
	# fullga.append(populate.s(meta).set(queue='genetic.common'))
	# fullga.append(evaluate_all.s(meta).set(queue='genetic.common'))
	# fullga.append(evaluate.s(meta).set(queue='genetic.common'))
	# res = chain(fullga)()
# app.send_task(new_task, (x, y, meta),
#               queue='gaapp.' + new_task,
#               routing_key=new_key)
	return


@app.task(base=TaskHelper, bind=True, name='populate')
def populate(self, meta=None):
	print('POPULATE_GENETIC',meta)
	return


@app.task(base=TaskHelper, bind=True, name='evaluate')
def evaluate(self, meta=None):
	print('POPULATE_GENETIC',meta)
	cp = meta['eval_curr_parent']
	par_num = meta['eval_curr_i']
	fitness = meta['eval_fitness']
	eval_func = ga.get_eval(meta['eval_func'])
	f = eval(cp)

	return #{'par_num':par_num, 'fitness': f}


@app.task(base=TaskHelper, bind=True, name='evaluate_all')
def sort_by_fitness(self, meta=None):
	return


@app.task(base=TaskHelper, bind=True, name='evaluate_all_sort')
def evaluate_all_sort(self, meta=None):
	print('evaluate_all_sort'.upper(),self.request)
	print('meta'.upper(),meta)
	gdata = ga.read_json(ga.gdj) # 'parents'
	p = int(gdata['n_pars'])
	nv = gdata['n_vars']
	np_vals = np.array(gdata['parents'])
	np_vals_r = np_vals.reshape(p, nv, order='F')
	# print(np_vals_r)
	eval = ga.get_eval(gdata['eval'])
	fitness = gdata['fitness_pars']
	loop = []
	for i,parent in enumerate(np_vals_r):
		meta['eval_curr_parent'] = parent
		meta['eval_curr_i'] = i
		meta['eval_fitness'] = fitness
		meta['eval_func'] = gdata['eval']
		loop.append(evaluate.s(meta).set(queue='genetic.eval'))

	meta['after_eval'] = 'sort'
	# loop = [evaluate.s(meta).set(queue='genetic.eval') for i in range(4)]
	cb = gather.s(meta).set(queue='genetic.common')
	res = chord(loop)(cb)
	while not res.ready():
		time.sleep(0.25)
	return


@app.task(base=TaskHelper, bind=True, name='looper')
def looper(self, meta=None):
	print('looper'.upper(),meta)
	time.sleep(2)
	return


@app.task(base=TaskHelper, bind=True, name='gather')
def gather(self, meta=None):
	print('gather'.upper(),meta)
	return


@app.task(base=TaskHelper, bind=True, name='evaluate_all')
def evaluate_all(self, meta=None):
	print('evaluate_all'.upper(),self.request)
	print('meta'.upper(),meta)
	loop = [looper.s(meta).set(queue='genetic.eval') for i in range(4)]
	cb = gather.s(meta).set(queue='genetic.common')
	res = chord(loop)(cb)
	# res = ch.apply_async(kwargs={'meta':meta})
	# while not res.ready():
	# 	print('WAITING')
	# 	time.sleep(1)
	# app.send_task('gather', kwargs={'meta':meta},
	# 							queue='genetic.common',
	# 							routing_key='genetic.common')
	# (gather.s().apply_async(kwargs={'meta':meta},queue='genetic.common'))
	return
