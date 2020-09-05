from flask import Flask


def create_app(testing=True):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return f"Hello World<br>Testing: {testing}"
    return app
