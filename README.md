YouTube Gesture Controller 

Control YouTube videos using your hand gestures — no mouse or keyboard needed!

Overview
The YouTube Gesture Controller is an innovative computer vision project that enables users to control YouTube playback with intuitive hand gestures using a webcam. This hands-free interface enhances accessibility and offers a futuristic way to interact with media.

Features
1. Play/Pause with open or closed palm.
2. Next/Previous video by swiping hand right or left.
3. Volume Control using vertical hand motion.
4. Seek Video by horizontal hand movement.
5. Real-time gesture recognition using a webcam.
6. Integrates directly with YouTube through browser automation.

Tech Stack
1. Python
2. OpenCV – for real-time video capture and image processing
3. Mediapipe – for accurate hand gesture detection
4. PyAutoGUI – to simulate keyboard/mouse actions
5. Webbrowser module / Selenium – to launch and interact with YouTube
 
Demo
<img width="1470" alt="youtube-gesture-controller" src="https://github.com/user-attachments/assets/fcf0b59d-920a-4f2b-acb7-5e112a033609" />

How It Works

1. Mediapipe tracks and maps your hand landmarks in real time.
2. Gestures are mapped to specific YouTube controls.
3.PyAutoGUI simulates the appropriate keystroke or action on the YouTube window.

Setup
git clone https://github.com/yourusername/youtube-gesture-controller.git
cd youtube-gesture-controller
pip install -r requirements.txt
python gesture_controller.py

Requirements
a. Python 3.7+
b. Webcam
c. Google Chrome browser

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
