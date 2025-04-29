YouTube Gesture Controller 

Control YouTube videos using your hand gestures — no mouse or keyboard needed!

Overview
The YouTube Gesture Controller is an innovative computer vision project that enables users to control YouTube playback with intuitive hand gestures using a webcam. This hands-free interface enhances accessibility and offers a futuristic way to interact with media.

Features
Play/Pause with open or closed palm.
Next/Previous video by swiping hand right or left.
Volume Control using vertical hand motion.
Seek Video by horizontal hand movement.
Real-time gesture recognition using a webcam.
Integrates directly with YouTube through browser automation.
Tech Stack

Python
OpenCV – for real-time video capture and image processing
Mediapipe – for accurate hand gesture detection
PyAutoGUI – to simulate keyboard/mouse actions
Webbrowser module / Selenium – to launch and interact with YouTube
 
Demo
<img width="1470" alt="youtube-gesture-controller" src="https://github.com/user-attachments/assets/fcf0b59d-920a-4f2b-acb7-5e112a033609" />

How It Works

Mediapipe tracks and maps your hand landmarks in real time.
Gestures are mapped to specific YouTube controls.
PyAutoGUI simulates the appropriate keystroke or action on the YouTube window.

Setup
git clone https://github.com/yourusername/youtube-gesture-controller.git
cd youtube-gesture-controller
pip install -r requirements.txt
python gesture_controller.py

Requirements
Python 3.7+
Webcam
Google Chrome browser

Note
Ensure the YouTube tab is active when running the controller.
Lighting conditions may affect gesture detection accuracy.

Future Improvements
Support for custom gestures
Multi-platform browser compatibility
Dark mode hand detection enhancements

Contact
Created by Archie Chadha — feel free to reach out! 
Linkedin: https://www.linkedin.com/in/archie-chadha-1869ba281/ 
