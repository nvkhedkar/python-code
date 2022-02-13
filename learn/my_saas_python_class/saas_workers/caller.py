import json, uuid, os, sys
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
print(SCRIPT_DIR)
print(BASE_DIR)
# sys.path.insert(-1, SCRIPT_DIR)
# sys.path.insert(-1, BASE_DIR)
sys.path.insert(-1, os.path.dirname(BASE_DIR))
from creo_saas.csdramatiq.base_case import simple_task

# num = 10
# for i in range(num):
#     cid = uuid.uuid4()
#     task_config = {
#         "name": "Node-Task",
#         "task_id": str(cid),
#         "batch": num,
#         "blob_info": {
#             "container": "simple-test-container",
#             "path": "test1/inputs",
#             "app_zip": "app_small.zip"
#         },
#         "run_task": False
#     }
#     msg = simple_task.send(task_config=task_config)
#     print(json.dumps(msg, indent=2))

def simple_send():
    return