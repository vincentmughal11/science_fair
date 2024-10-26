from flask import *
from inference_sdk import InferenceHTTPClient
import os
from PIL import Image
import io
import requests
import json
import os
from werkzeug.utils import secure_filename
import base64
import numpy as np

app = Flask(__name__)


client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="r5nDcPfmL8cZWXu4Jg8v"
)

UPLOAD_FOLDER = 'detect_imgs'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')  # Homepage
def home():
    """
    Homepage route that returns index.html

    Returns:
        str: The rendered HTML of index.html
    """
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
     # Get the image file
    image_file = request.files['cameraInput']

    filename = secure_filename(image_file.filename)
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    # Send the processed image to Roboflow
    with open(os.path.join(UPLOAD_FOLDER, filename), 'rb') as image_file:
       # Assume `image_bytes` contains your image data in bytes
        image_bytes = image_file.read()

        # Convert bytes to a PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Convert the PIL Image to a byte stream
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")  # or 'PNG', depending on your image

        # Encode the byte stream to base64
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")


    result = client.run_workflow(
        workspace_name="practiceproject-kutwd",
        workflow_id="custom-workflow",
        images={
            "image": img_base64,
            "data": img_base64
        }
    )

    os.remove(os.path.join(UPLOAD_FOLDER, filename))

    image = result[0]["label_visualization"]
    ai_response = result[0]['open_ai']['output']

    return jsonify({
        "ai_response": ai_response,
        "image": image
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)