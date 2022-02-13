import redis

SHAPES = 'shapes'
redis_cache = redis.Redis(host='10.192.39.4', port=6379, db=0)


def set_shape(timestamp, shape):
  redis_cache.hset(SHAPES, timestamp, shape)


def show_shapes():
  try:
    print(f'Time to expire: {redis_cache.ttl(SHAPES)}')
    shapes_dict = redis_cache.hgetall(SHAPES)
    i = 0
    for k, v in shapes_dict.items():
      i += 1
      print(f"REDIS[{i}]: {k}, {v}")
  except Exception as e:
    print(f'Exception {e}')

def get_shapes_list(time_stamp=-1):
  # print(f'Time to expire: {redis_cache.ttl(SHAPES)}')
  shapes = []
  shapes_dict = redis_cache.hgetall(SHAPES)
  for timestamp, shape in shapes_dict.items():
    shape = shape.decode()
    if time_stamp >= int(timestamp.decode()):
      pass
    shapes.append(shape)
  # print(len(shapes))
  return shapes

def delete_shapes():
  try:
    redis_cache.delete(SHAPES)
    keys = redis_cache.hkeys(SHAPES)
    if not keys:
      return 'DELETED'
    return "ISSUE"
  except Exception as e:
    print(f'Already cleared {e}')

def get_shapes_all():
  shapes_list = []
  shapes = redis_cache.hgetall(SHAPES)
  for ts, shape in shapes.items():
    # print(shape.time_str + ',' + shape.shape)
    shapes_list.append(f"{ts}, {shape}")

  return shapes_list



# def set_shape_l(timestamp, shape):
#   redis_cache.lpush(SHAPES, f'{timestamp},{shape.decode()}')
#
# def show_shapes_l():
#   try:
#     print(f'Time to expire: {redis_cache.ttl(SHAPES)}')
#     print(f'Number of shapes: {redis_cache.llen(SHAPES)}')
#     for i in range(0, redis_cache.llen(SHAPES)):
#       print("REDIS:", redis_cache.lindex(SHAPES, i))
#   except Exception as e:
#     print(f'Exception {e}')
#
# def get_shapes_l():
#   print(f'Time to expire: {redis_cache.ttl(SHAPES)}')
#   for i in range(0, redis_cache.llen(SHAPES)):
#     yield redis_cache.lindex(SHAPES, i)
#
# def get_shapes_list_l(time_stamp=-1):
#   # print(f'Time to expire: {redis_cache.ttl(SHAPES)}')
#   shapes = []
#   for i in range(0, redis_cache.llen(SHAPES)):
#     # print(redis_cache.lindex(SHAPES, i))
#     shape_str = redis_cache.lindex(SHAPES, i)
#     timestamp, shape = shape_str.decode().split(',')
#     if time_stamp >= int(timestamp):
#       pass
#     shapes.append(shape)
#   print(len(shapes))
#   return shapes
#
# def get_num_shapes_l():
#   return redis_cache.llen(SHAPES)
#
# def delete_shapes_l():
#   try:
#     redis_cache.delete(SHAPES)
#     keys = redis_cache.keys(SHAPES)
#     if not keys:
#       return 'DELETED'
#     return "ISSUE"
#   except Exception as e:
#     print(f'Already cleared {e}')


def performance_test():
  import time
  start = time.perf_counter()
  for i in range(3_000):
    lst = get_shapes_all()
  end = time.perf_counter() - start
  print(f"CACHE finished in {end:0.2f} seconds.")

# performance_test()
