from flask import Flask, jsonify
from flask import request
from flask_caching import Cache
import time, datetime

import saas_training.server_ex1.caching as rc
import saas_training.server_ex1.db_shapes as dbs
from saas_training.saas_workers.saas_job import simple_task

config = {
    # "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache", #"FileSystemCache",  # Flask-Caching related configs
    "CACHE_TYPE": "FileSystemCache", #"FileSystemCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 3000,
    "CACHE_DIR": "d:/temp/flask-cache"
}

app = Flask(__name__)
app.config.from_mapping(config)
# cache = Cache(app)

# def add_flask_cache(shape):
#     cache.add(str(), f'{str(get_int_timestamp())},{shape}')
#     all_shapes = cache.get('shapes')
#     print(f'Shapes: {type(all_shapes)} {len(all_shapes)}')
#     print(f'Shapes: {all_shapes}')

def get_int_timestamp(t_str=0):
    if t_str:
        return int(t_str)
    return int(time.mktime(datetime.datetime.now().timetuple()))


@app.route('/', methods=['GET'])
def hello_rest():
    print("Flask hello world")
    return jsonify({
        "greeting": "Hello FLASK REST World"
    })


@app.route('/draw', methods=['POST'])
def create_shape_info():
    shape = request.data.decode()
    time_stamp = get_int_timestamp()
    print(f"Shape: {shape}")

    rc.set_shape(time_stamp, shape)
    rc.show_shapes()

    dbs.si.add_shape(time_stamp, shape)
    dbs.si.show_shapes()

    # send worker task
    simple_task.send(time_stamp, shape)
    return jsonify({"shape": shape})


@app.route('/get_shapes/<ts>', methods=['GET'])
def get_shape_info(ts):
    shapes_list = rc.get_shapes_list(int(ts))
    curr_time = get_int_timestamp()
    # print(f'DRAW_GET_EMPTY {ts} {len(shapes_list)} {time.time()}')
    return jsonify({"timestamp": str(curr_time), "shapes": shapes_list})


@app.route('/clr', methods=['POST'])
def clear_cache():
    stat = rc.delete_shapes()
    return jsonify({"stat": stat})

@app.route('/shapes', methods=['GET'])
def get_cache_shapes():
    all_shapes = rc.get_shapes_list()
    return jsonify({"shapes": all_shapes})


if __name__ == '__main__':
    app.run(debug=True)
