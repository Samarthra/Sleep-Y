
# Import necessary libraries
import torch
import numpy as np
import cv2
import random
import pygame.mixer
from flask import Flask, render_template, jsonify
from flask_cors import CORS
# Initialize Pygame mixer
pygame.mixer.init()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize drowsy detection variables
counter = 0
drowsy_duration = 0
drowsy_threshold = 15

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt', force_reload=True)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Function to play alarm
def play_alarm():
    # filechoice = random.choice(["beep2.mp3"])
    filechoice = "beep2.mp3"
    pygame.mixer.music.load('beep2.mp3')
    pygame.mixer.music.play()

    print("Playing alarm:", filechoice)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(1)
    print("Alarm playback complete")

# Route for starting drowsy detection
# Add a global flag to track whether detection has started
detection_started = False

@app.route('/start_detection', methods=['GET'])
def start_detection():
    global detection_started,cap
    
    if cap.isOpened():
        cap.release()

    # Initialize a new video capture object
    cap = cv2.VideoCapture(0)
    # Start the detection only if it hasn't already started
    if not detection_started:
        detection_started = True
        detect()

    return jsonify({'status': 'success', 'message': 'Drowsy detection started successfully'})

# ...

# Route for stopping drowsy detection
@app.route('/stop_detection', methods=['GET'])
def stop_detection():
    global detection_started

    # Stop the detection by setting the flag to False
    detection_started = False

    cap.release()

    return jsonify({'status': 'success', 'message': 'Drowsy detection stopped successfully'})

# ...

# Function to detect drowsiness
def detect():
    global counter, drowsy_duration,detection_started
    # detection_started = True
    while detection_started: 
         # Continue detection while the flag is True
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = model(frame)

        if len(results.xyxy[0]) > 0:
            dconf = results.xyxy[0][0][4]
            dclass = results.xywh[0][0][5]
            # print(results.xyxy[0])
            
            if dclass == 16.0 and dconf.item() > 0.30:
                counter += 1
                drowsy_duration += 1
                print(drowsy_duration, drowsy_threshold)
                if drowsy_duration > drowsy_threshold and not pygame.mixer.music.get_busy():
                    play_alarm()
                    counter = 0  # Reset the counter to zero after the alarm is played
                    drowsy_duration = 0  # Reset drowsy_duration to zero as well
                    
            else:
                drowsy_duration = 0
        


# Route for the home page
# @app.route('/')
# def index():
#     return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

