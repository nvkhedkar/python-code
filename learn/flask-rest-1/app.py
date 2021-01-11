from flask import Flask
from flask_restful import Api
# import os, sys
# SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(-1, SCRIPT_DIR)
from api import api

app = Flask(__name__)
restapi = Api(app)

restapi.add_resource(api.HelloWorld, '/')
restapi.add_resource(api.TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run()
