import dramatiq
import requests, time, json
from dramatiq.brokers.rabbitmq import RabbitmqBroker

rabbitmq_broker = RabbitmqBroker(url="amqp://guest:pass@localhost:5672/dtq1")


@dramatiq.actor(broker=rabbitmq_broker, queue_name='easy1')
def simple_task(name):
    for i in range(3):
        time.sleep(1)
        print(f'{name}: Sleep for {i+1}')


# @dramatiq.actor
# def count_words(url):
#      response = requests.get(url)
#      count = len(response.text.split(" "))
#      print(f"There are {count} words at {url!r}.")

# Synchronously count the words on example.com in the current process
# count_words("http://example.com")

# or send the actor a message so that it may perform the count
# later, in a separate process.
# count_words.send("http://example.com")

# print(f'{json.dumps(msg, indent=2)}')


