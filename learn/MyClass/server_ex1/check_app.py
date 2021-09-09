import requests
import datetime

url = 'http://localhost:8080/'

def clear_shapes():
  x = requests.post(url + 'clr')
  print(x.json())

def get_shapes_info():
  x = requests.get(url + 'shapes')
  shapes = x.json()
  print(f"Number of shapes found: {len(shapes['shapes'])}")
  for k, v in shapes.items():
    for shape in v:
      print(f"type: {type(shape)}, {shape}")

# get_shapes_info()
# clear_shapes()

# x = requests.get(url + 'draw/' + str(12345))
# print(x.json())



def check_db():
  shapes = [
    b'1622903272,\t<circle stroke="black" stroke-width="1" fill="black" r="45" cx="100" cy="58" />\n',
    b'1622900583,\t<circle stroke="black" stroke-width="1" fill="white" r="35" cx="240" cy="103" />\n',
    b'1622900493,\t<circle stroke="black" stroke-width="1" fill="black" r="36" cx="64" cy="70" />\n',
  ]
  for shape in shapes:
    ss = shape.decode('utf-8')
    ts, msg = ss.split(',')
    print(ts, datetime.datetime.fromtimestamp(int(ts)).strftime('%c'), msg)


import saas_training.server_ex1.caching as rc
import saas_training.server_ex1.db_shapes as dbs


def compare_performance():
  rc.performance_test()
  dbs.performance_test()

def delete_data():
  print(rc.delete_shapes())
  print('Deleted data')

# delete_data()

