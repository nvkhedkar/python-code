from __future__ import absolute_import, unicode_literals
from kombu import Exchange, Queue

broker_url='pyamqp://guest:pass@localhost:5672/genetic'
result_backend = 'redis://localhost/0'

imports = ('geneticapp.tasks',)

result_expires = 3600
result_persistent = True
task_result_expires = None
task_protocol = 1
send_events = True

default_exchange = Exchange('default', type='direct')
population_exchange = Exchange('genetic.populate', type='direct')
evaluation_exchange = Exchange('genetic.eval', type='direct')
common_exchange = Exchange('genetic.common', type='direct')

task_queues = [
	Queue('genetic.populate', population_exchange, routing_key='genetic.populate'),
	Queue('genetic.eval', evaluation_exchange, routing_key='genetic.eval'),
	Queue('genetic.common', common_exchange, routing_key='genetic.common')]

task_default_queue = 'default'
task_default_exchange = 'default'
task_default_routing_key = 'default'

# celery -A nvkproject.tasks worker --loglevel=info -Q gaapp.manage -n w1@ubuntu1
