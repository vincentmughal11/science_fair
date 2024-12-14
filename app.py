# Import required libraries
from flask import Flask, request, jsonify, render_template, make_response, send_from_directory
from inference_sdk import InferenceHTTPClient
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
import base64
from dotenv import load_dotenv


# Initialize Flask app
app = Flask(__name__)
load_dotenv()

# Load environment variables
api_key = os.getenv("API_KEY")
workspace_name = os.getenv("WORKSPACE_NAME")
workspace_id = os.getenv("WORKFLOW_ID")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
port = os.getenv("PORT")


# Initialize Roboflow client
client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=api_key,
)

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    """Homepage route that returns index.html.

    Returns:
        str: The rendered HTML of index.html
    """
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    """Handle image detection requests."""
    # Get the image file from form submission
    image_file = request.files["cameraInput"]

    # Save uploaded file with secure filename
    filename = secure_filename(image_file.filename)
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))

    # Process and encode image for Roboflow
    with open(os.path.join(UPLOAD_FOLDER, filename), "rb") as image_file:
        # Read image bytes
        image_bytes = image_file.read()

        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Convert PIL Image to byte stream
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")

        # Encode to base64 for API
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Send image to Roboflow for inference
    result = client.run_workflow(
        workspace_name=workspace_name,
        workflow_id=workspace_id,
        images={"image": img_base64, "data": img_base64},
    )

    # Clean up - remove uploaded file
    os.remove(os.path.join(UPLOAD_FOLDER, filename))

    # Extract results
    image = result[0]["label_visualization"]
    ai_response = result[0]["open_ai"]["output"]
    detected_count = result[0]["property_definition"]

    # Return JSON response with results
    return jsonify(
        {
            "ai_response": ai_response,
            "image": image,
            "detected_count": detected_count,
        }
    )


@app.route("/final_detect", methods=["POST"])
def final_detect():
    """Handle final detection requests."""
    # Get previous image and new image file
    before_img_base64 = request.form.get("before_image", "false")
    image_file = request.files["finalCameraInput"]

    # Validate that phase 1 detection was done
    if before_img_base64 == "false":
        return make_response(
            {"message": "You have to run the phase 1 detection first"}, 500
        )

    # Save uploaded file with secure filename
    filename = secure_filename(image_file.filename)
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))

    # Process and encode image for Roboflow
    with open(os.path.join(UPLOAD_FOLDER, filename), "rb") as image_file:
        # Read image bytes
        image_bytes = image_file.read()

        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Convert PIL Image to byte stream
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")

        # Encode to base64 for API
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Send image to Roboflow for inference
    result = client.run_workflow(
        workspace_name=workspace_name,
        workflow_id=workspace_id,
        images={"image": img_base64, "data": img_base64},
    )

    # Clean up - remove uploaded file
    os.remove(os.path.join(UPLOAD_FOLDER, filename))

    # Extract results
    image = result[0]["label_visualization"]
    ai_response = result[0]["open_ai"]["output"]
    detected_count = result[0]["property_definition"]

    # Return JSON response with results and previous image
    return jsonify(
        {
            "ai_response": ai_response,
            "image": image,
            "before_image": before_img_base64,
            "detected_count": detected_count,
        }
    )

@app.route("/download/<filename>")
def download_file(filename):
    # Specify the directory where your file is stored
    directory = os.path.join(app.root_path, 'files')
    return send_from_directory(directory, filename)


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
