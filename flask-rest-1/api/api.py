from flask_restful import Resource
from flask import request


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


todos = {'todo1': 'todo1'}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = todo_id
        return {todo_id: todos[todo_id]}
