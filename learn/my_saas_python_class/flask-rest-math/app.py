from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_rest():
    return jsonify({
        "greeting": "Hello REST World"
    })


@app.route('/add/<a>/<b>', methods=['GET'])
def add(a, b):
    return jsonify({
        "a": a,
        "b": b,
        "addition": int(a) + int(b),
    })


@app.route('/mul/<a>/<b>', methods=['GET'])
def prod(a, b):
    return jsonify({
        "a": a,
        "b": b,
        "product": float(a) * float(b),
    })


@app.route('/pow/<a>/<b>', methods=['GET'])
def powered(a, b):
    return jsonify({
        "a": a,
        "b": b,
        "power": float(a) ** float(b)
    })


@app.route('/div/<a>/<b>', methods=['GET'])
def divide(a, b):
    return jsonify({
        "a": a,
        "b": b,
        "quotient": float(a) // float(b),
        "remainder": float(a) % float(b)
    })


if __name__ == '__main__':
    app.run()

