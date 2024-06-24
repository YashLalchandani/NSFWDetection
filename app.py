from flask import Flask, render_template, Response, jsonify
from nudenet import NudeDetector
import cv2
import tempfile
import os
from datetime import datetime

app = Flask(__name__)
detector = NudeDetector()

# Store the results in a global variable
detection_results = []

def blur_frame(frame):
    return cv2.GaussianBlur(frame, (55, 55), 0)

def gen_frames():
    global detection_results
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera

    count = 0
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            count += 1

            # Detect NSFW elements in the frame
            if count % 30 == 0:  # Check every 1 second
                # Save the frame to a temporary file
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    temp_filename = temp_file.name
                    cv2.imwrite(temp_filename, frame)

                results = detector.detect(temp_filename)

                # Remove the temporary file
                os.remove(temp_filename)

                # Filter out gender-specific labels and scale scores from 1 to 10
                filtered_results = []
                for result in results:
                    if result['class'].startswith(('FEMALE_', 'MALE_')):
                        result['class'] = result['class'].split('_', 1)[1]
                    result['score'] = round(result['score'] * 10, 2)
                    filtered_results.append(result)

                detection_results = filtered_results

            # Blur the frame if NSFW content is detected
            if any(result['class'] in ['GENITALIA_EXPOSED', 'BREAST_EXPOSED', 'BUTTOCKS_EXPOSED'] for result in detection_results):
                frame = blur_frame(frame)

            # Encode the frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detection_results')
def get_detection_results():
    global detection_results
    return jsonify(detection_results)

if __name__ == '__main__':
    app.run(debug=True)
