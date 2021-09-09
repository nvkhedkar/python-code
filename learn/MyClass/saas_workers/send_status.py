import json
from datetime import datetime
# SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# BASE_DIR = os.path.dirname(SCRIPT_DIR)
# sys.path.insert(-1, SCRIPT_DIR)
# sys.path.insert(-1, BASE_DIR)
# from dramatiq import get_broker
from kombu import Connection
import logging

logger = logging.getLogger(__name__)
result_conn = Connection("pyamqp://genuser:genpass@RABBIT_HOST:5673/mlpipe")

def send_status(task_id, status, time_req=0):
  message = {
    'task_id': task_id,
    'status': status,
    "time": datetime.strftime(datetime.now(), "%Y-%b-%d %H:%M:%S.%f")[:-2]
  }
  if time_req > 0:
    message['time'] += f'[{time_req}]'

  simple_queue = result_conn.SimpleQueue('cs-results-k1')
  simple_queue.put(json.dumps(message))
  simple_queue.close()

  # print(f'Sent: {message}')
