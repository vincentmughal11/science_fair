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

    pass

if __name__ == "__main__":
    app.run(debug=True)