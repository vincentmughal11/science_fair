from flask import *
from inference_sdk import InferenceHTTPClient
import os
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
import base64
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

api_key = os.getenv("API_KEY")
workspace_name = os.getenv("WORKSPACE_NAME")
workspace_id = os.getenv("WORKFLOW_ID")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
port = os.getenv("PORT")

print(workspace_name, workspace_id)


client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=api_key
)

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
        workspace_name=workspace_name,
        workflow_id=workspace_id,
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
    app.run(host='0.0.0.0', port=port, debug=True)