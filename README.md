# Microplastics Detection Web Application

This web application helps users detect microplastics in water samples using computer vision and machine learning techniques.

## Overview

This project provides an accessible way for people to check their water for potential microplastic contamination. Users can upload images of water samples and get instant analysis results.

## Key Features

- Upload and analyze water sample images
- Real-time microplastics detection using YOLOv5
- Before/after visualization of detection results
- User-friendly web interface
- Detailed detection notes and analysis

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Machine Learning**: Roboflow (for model training/deployment), using YOLOv5 and ChatGPT
- **Frontend**: HTML, JavaScript, Bootstrap
- **Image Processing**: Base64 encoding/decoding

## How It Works

1. Users upload an image of their water sample
2. The application processes the image using computer vision techniques
3. A trained YOLOv5 model detects presence of microplastics
4. Results are displayed showing before/after images and detection notes

## Setup and Installation

1. Clone this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Access the web interface using localhost

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
