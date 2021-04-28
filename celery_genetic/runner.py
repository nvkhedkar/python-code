import geneticapp.tasks as ga
from kombu import Connection, Exchange, Producer, Queue, binding
import json,uuid

class RabbitMq:
  server_host = 'localhost'
  server_port = '5672'
  queue_name = 'genetic.common'
  queue_routing_key = 'genetic.common'
  exchange_name = 'genetic.common'
  exchange_type = 'direct'
  server_user = 'guest'
  server_passwd = 'guest'
  server_vhost = 'genetic'

  url = 'pyamqp://guest:guest@localhost:5672/genetic'

def get_msg(task,retries ):
  msg = {}
  msg['id'] = str(uuid.uuid4())
  msg['task'] = task
  msg['args'] = []
  msg['kwargs'] = {}
  msg['retries'] = str(retries)

  meta = {'genetic': 'Hello_Genetic'}
  ka = {}
  ka['meta'] = meta
  msg['kwargs'] = ka
  return msg

def send_kombu_message(ex_name='', ex_type = '', rkey= '', msg=None):
  send_msg = msg
  if msg:
    send_msg = msg
  conn = Connection(RabbitMq.url)
  channel = conn.channel()
  exchange = Exchange(RabbitMq.exchange_name, type=RabbitMq.exchange_type)
  producer = Producer(exchange=exchange, channel=channel, routing_key=RabbitMq.queue_routing_key)

  # queue = Queue(name=”example - queue”, exchange = exchange, routing_key =”BOB”)
  # queue.maybe_bind(conn)
  # queue.declare()
  json_msg = json.dumps(get_msg('init',0), indent=2).encode('utf-8')
  print(json_msg)
  # print('sending', json.dumps(send_msg, indent=2))
  producer.publish(json_msg, content_type='application/json', content_encoding='utf-8')
  print('sent')
  return

send_kombu_message()
# meta = {'genetic': 'Hello_genetic'}
# ga.init.delay()

