import os
import cv2
import base64
import logging
import threading
from flask import Flask, render_template, Response, jsonify
from gesture_controller import GestureRecognizer
from youtube_controller import YouTubeController

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "gesture_controller_secret")

# Initialize gesture recognizer and YouTube controller
gesture_recognizer = GestureRecognizer()
youtube_controller = YouTubeController()

# Global variables
camera = None
camera_lock = threading.Lock()
processing_active = False
last_gesture = "None"
cooldown_active = False

def get_camera():
    """Get or initialize the camera"""
    global camera
    with camera_lock:
        if camera is None:
            # Try to open the camera
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                logging.error("Could not open webcam")
                return None
            # Set camera properties
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return camera

def release_camera():
    """Release the camera resource"""
    global camera
    with camera_lock:
        if camera is not None:
            camera.release()
            camera = None

def process_frame():
    """Process frames from the webcam"""
    global last_gesture, cooldown_active
    
    camera = get_camera()
    if camera is None:
        return
    
    while processing_active:
        success, frame = camera.read()
        if not success:
            break
            
        # Flip the frame horizontally for a more intuitive mirror view
        frame = cv2.flip(frame, 1)
        
        # Process the frame to detect gestures
        processed_frame, detected_gesture = gesture_recognizer.process_frame(frame)
        
        # If a gesture is detected and cooldown is not active
        if detected_gesture != "None" and detected_gesture != last_gesture and not cooldown_active:
            last_gesture = detected_gesture
            
            # Process the detected gesture to control YouTube
            threading.Thread(
                target=youtube_controller.execute_command,
                args=(detected_gesture,)
            ).start()
            
            # Set cooldown
            cooldown_active = True
            threading.Timer(1.5, lambda: setattr(app, 'cooldown_active', False)).start()
        
        # Encode the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        # Convert to base64 for sending to the client
        encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', last_gesture=last_gesture)

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    global processing_active
    processing_active = True
    return Response(process_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_processing')
def start_processing():
    """Start the gesture processing"""
    global processing_active
    processing_active = True
    return jsonify({"status": "started"})

@app.route('/stop_processing')
def stop_processing():
    """Stop the gesture processing"""
    global processing_active
    processing_active = False
    release_camera()
    return jsonify({"status": "stopped"})

@app.route('/get_status')
def get_status():
    """Get the current gesture status"""
    return jsonify({
        "gesture": last_gesture,
        "cooldown": cooldown_active
    })

# Clean up resources on shutdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    release_camera()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
