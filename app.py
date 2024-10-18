from flask import *
from inference_sdk import InferenceHTTPClient

app = Flask(__name__)

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
    result = client.infer_from_workflow(
        workspace_name="practiceproject-kutwd",
        workflow_id="custom-workflow",
        images={
            "image": "YOUR_IMAGE.jpg"
        }
    )

if __name__ == "__main__":
    app.run(debug=True)