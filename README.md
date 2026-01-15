# Sign Language Detection System

A real-time sign language detection and interpretation system using computer vision and machine learning using advanced AI integration

## Features
- Real-time hand gesture detection
- Sign language interpretation
- Text-to-speech output
- Virtual assistant interface
- Multi-language support

## Files
- `cam.py` - Main application with full features and GUI
- `test.py` - Basic implementation for testing
- `wait.py` - Alternative implementation with different timing
- `Model/` - Contains trained model and labels

## Requirements
- Python 3.x
- See requirements.txt for all dependencies

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python cam.py
   ```
   Or for basic testing:
   ```
   python test.py
   ```

## Model
The system uses a trained Keras model (`keras_model.h5`) for sign language classification, along with corresponding labels in `labels.txt`.
