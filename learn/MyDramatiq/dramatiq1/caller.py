import dramatiq
import json
from dramatiq1.base_case import simple_task

for i in range(2):
    msg = simple_task.send(name=f'Task-queue-{i+1}')
    print(json.dumps(msg, indent=2))

