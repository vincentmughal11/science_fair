from flask import *
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="r5nDcPfmL8cZWXu4Jg8v"
)

@app.route('/')  # Homepage
def home():
    """
    Homepage route that returns index.html

    Returns:
        str: The rendered HTML of index.html
    """
    return render_template('index.html')

@app.route('/run-yolo', methods=['POST'])
def run_yolo():
    result = client.run_workflow(
        workspace_name="practiceproject-kutwd",
        workflow_id="custom-workflow",
        images={
            "image": "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg"
        }
    )

    image = result[0]["label_visualization"]
    ai_response = result[0]['open_ai']['output']

    return jsonify({
        "ai_response": ai_response,
        "image": image
    })

if __name__ == "__main__":
    app.run()