import time, re
from datetime import datetime
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import CurrentMessage
import logging

logger = logging.getLogger(__name__)

broker = RabbitmqBroker(url="amqp://genuser:genpass@localhost:5673/test1")
broker.add_middleware(CurrentMessage())


def get_area(shape):
    if "circle" in shape:
        radius = float(re.search("r=\"([\d]+)\"", shape).group(1))
        return "circle", (22./7.)*radius*radius
    elif "rect" in shape:
        width = float(re.search("\s+width=\"([\d]+)\"", shape).group(1))
        height = float(re.search("height=\"([\d]+)\"", shape).group(1))
        return "rect", width * height
    return "line", 0.0

@dramatiq.actor(broker=broker, queue_name='cs-easy-1', max_retries=3)
def simple_task(ts, shape):
    shape_type, area = get_area(shape)
    time.sleep(5)
    time_str = datetime.fromtimestamp(int(ts)).strftime("%Y-%b-%d %H:%M:%S")
    logger.info(f"====> FinishLong Job: Area [{shape_type}]: {area:0.2f}")

