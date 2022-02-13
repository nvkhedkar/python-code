# import shortuuid as suid
import time, os
from datetime import datetime


def get_task_id():
    dt_obj = datetime.utcnow()
    curr_time = dt_obj.strftime("%Y%b%d-%H%M%S-%f")[:-3]
    num_digits = 32-len(curr_time)
    my_rn = suid.ShortUUID().random(num_digits)
    fr = f'{curr_time}-{my_rn}'
    print(fr, num_digits)
    print(str(dt_obj.timestamp()))


full = "nvk.txt"


def add(x, y):
    return x + y


print(add('nv-', 'khed'))
print(add(2, 3))
print(add(2.3, 3.2))


def get_epoch_int_time():
    timestamp = int(time.mktime(datetime.utcnow().timetuple()))
    print(timestamp)

# while len(values) > 1:
#     print(f'Values b: {values}')
#     values = values[2:] + [add(values[0], values[1])]
#     print(f'values: {values}')