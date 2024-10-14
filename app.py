from flask import *
import subprocess
import sys

app = Flask(__name__)

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
    # try:
    #     python_executable = sys.executable
    #     image_path = "yolov5/data/images/bus.jpg"
    #     result = subprocess.run([python_executable, 'yolov5/detect.py', '--source', image_path], capture_output=True, text=True)

    #     if result.returncode != 0:
    #         return jsonify({'result': 'Error running YOLO: ' + result.stderr})
        
    #     return jsonify({'result': result.stdout.strip()})
    
    # except Exception as e:
    #     return jsonify({'result': 'Error during backend detection: ' + str(e)})
    pass

if __name__ == "__main__":
    app.run(debug=True)