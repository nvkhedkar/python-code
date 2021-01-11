from flask import Flask
from flask_restful import Resource, Api

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    

def create_app(testing=True):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return f"Hello World<br>Testing: {testing}"
    
    return app
