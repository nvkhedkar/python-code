from flask import Flask, jsonify
# import os, sys
# SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(-1, SCRIPT_DIR)
# from api import api

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_rest():
    return jsonify({
        "greeting": "Hello REST World"
    })


if __name__ == '__main__':
    app.run()


shapes = dict()


@app.route('/shape', methods=['GET'])
def get_shape_info():
    return


@app.route('/', methods=['POST'])
def create_shape_info():
    return


