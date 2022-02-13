import dramatiq
import requests, time, json
from dramatiq.brokers.rabbitmq import RabbitmqBroker

rabbitmq_broker = RabbitmqBroker(url="amqp://guest:pass@localhost:5672/dtq1")


@dramatiq.actor(broker=rabbitmq_broker, queue_name='easy1')
def simple_task(name):
    for i in range(3):
        time.sleep(1)
        print(f'{name}: Sleep for {i+1}')




