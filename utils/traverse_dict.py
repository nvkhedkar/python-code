
my_test_dict = {
  "_id": {
    "oid": "5fc8ec"
  },
  "mainId": "1e5a84e4",
  "thisDate": {
    "date": "2020-12-03T13:46:57Z"
  },
  "details": [
    {
      "detlName": "Detail_Name_1",
      "dtlId": "fc9631b2-aed3",
      "dblValue1": 0.925,
      "intValue1": 715,
      "customJSON": {
        "accelAvg": 0.0,
        "accelMax": 0.0,
        "max": [
          200.0,
          40.0
        ],
        "gmInf": [
          {
            "bX": 30.297,
            "bY": 53.648,
            "pnt": [
              110.0,
              259.999,
            ],
          },
          {
            "bX": 30.297,
            "bY": 53.648,
            "pnt": [
              110.0,
              259.999,
            ],
          },
        ],
        "intPath": [
          {
            "type": "Type One",
            "name": "Some Name"
          },
          {
            "type": "Type Two",
            "name": "AnotherName1"
          },
        ],
        "teleData": {
          "userId": "5f31dcf7ca5",
          "companyId": "5f198226",
        }
      },
      "mcInfo": [
        {
          "osInfo": "Ubuntu 18.04.5 LTS",
          "osKernelVersion": "5.4.0",
          "cpuInfo": "Intel(R) Xeon(R)",
          "machineRamGb": "59",
        },
      ],
    },
  ]
}

class DictEntity:
  def __init__(self):
    self.final_name = ''
    self.name = ''
    self.path = []
    self.type = ''
    self.data = None
    self.data_type = ''
    self.size = 0
    self.cnt = -1
    self.parent_type = 'list'

  def to_string(self):
    return f"{self.path}, name: {self.name}, value: {self.data}, " \
      f"par:{self.parent_type}, cnt: {self.cnt}, {self.data_type}"

  def path_string(self):
    return '_'.join(self.path)

  def path_name_string(self):
    return self.path_string() + ":" + self.name

  def level(self):
    return len(self.path)

def flatten_data(dct, root_label='root', level=-1):
  flat_data = []
  all_keys = {}
  def add_key(k, path):
    fp = '_'.join(path)
    if k in all_keys.keys():
      if f'{fp}_{k}' in all_keys.keys():
        all_keys[f'{fp}_{k}'] += 1
      else:
        all_keys[f'{fp}_{k}'] = 1
    else:
      all_keys[k] = 1

  def add_data(k_dict, v_dict, path, j=-1):
    ee = DictEntity()
    ee.path = path.copy()
    ee.name = k_dict
    ee.data = v_dict
    ee.data_type = str(type(v_dict))
    ee.cnt = j
    if j == -1:
      ee.parent_type = 'dict'
    flat_data.append(ee)
    # print(len(flat_data), ee.to_string())
    return

  def add_array_data(k_dict, v_dict, path, j=-1):
    ee = DictEntity()
    ee.path = path.copy()
    ee.name = f'{k_dict}_{j+1}'
    ee.data = v_dict
    ee.data_type = str(type(v_dict))
    ee.cnt = j
    flat_data.append(ee)
    # print(len(flat_data), ee.to_string())
    return

  def travel_further(path):
    if level == -1:
      return True
    elif level > len(path):
      return True
    else:
      return False

  def traverse_dict(d, path, cnt=-1):
    for k, v in d.items():
      # add_key(k, path)
      if isinstance(v, dict):
        if travel_further(path):
          path.append(k)
          traverse_dict(v, path)
          path.pop()
      elif isinstance(v, list):
        for i, m in enumerate(v):
          if isinstance(m, dict):
            if travel_further(path):
              path.append(k)
              traverse_dict(m, path, i)
              path.pop()
          else:
            add_array_data(k, m, path, i)
      else:
        add_data(k, v, path, cnt)

  traverse_dict(dct, [root_label])
  return flat_data

# flat_data = []
# flatten_data(my_dict)
# for i, fd in enumerate(flat_data):
#   print(i, fd.to_string())

