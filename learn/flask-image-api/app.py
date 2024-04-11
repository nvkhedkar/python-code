from flask import Flask, jsonify, request
from PIL import Image
from io import BytesIO

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
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


@app.route('/merge_images', methods=['POST'])
def merge_images():
    # Check if the request contains two images
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'error': 'Please provide two images.'}), 400

    image1 = request.files['image1']
    image2 = request.files['image2']

    # Read the images
    img1 = Image.open(BytesIO(image1.read()))
    img2 = Image.open(BytesIO(image2.read()))

    # Check if both images have the same dimensions
    if img1.size != img2.size:
        return jsonify({'error': 'Images must have the same dimensions.'}), 400

    # Merge the images (example: horizontally concatenate)
    merged_image = Image.new('RGB', (img1.width + img2.width, img1.height))
    merged_image.paste(img1, (0, 0))
    merged_image.paste(img2, (img1.width, 0))

    # Convert the merged image to bytes
    merged_image_bytes = BytesIO()
    merged_image.save(merged_image_bytes, format='JPEG')
    merged_image_bytes.seek(0)
    print('returning image')

    # Return the merged image
    return merged_image_bytes.getvalue(), 200, {'Content-Type': 'image/jpeg'}


