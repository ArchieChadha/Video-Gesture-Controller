import cv2
import mediapipe as mp
import time
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize variables
last_gesture_time = time.time()
cooldown_time = 2  # seconds
last_gesture = None

# Define the hand gesture actions
def check_gesture(landmarks):
    global last_gesture_time, last_gesture

    # Extract key landmarks (the tips of the fingers)
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Determine gestures
    if time.time() - last_gesture_time < cooldown_time:
        return None  # Ignore gesture if within cool-down period

    # Open Palm Gesture (All 5 fingers extended)
    if (index_tip.y < middle_tip.y and middle_tip.y < ring_tip.y and ring_tip.y < pinky_tip.y and thumb_tip.x < index_tip.x):
        action = 'Play'  # Open palm
        pyautogui.press('space')  # Simulate space bar press (play/pause)
        last_gesture = action
    # Fist Gesture (No fingers extended)
    elif (thumb_tip.y > index_tip.y and index_tip.y > middle_tip.y and middle_tip.y > ring_tip.y and ring_tip.y > pinky_tip.y):
        action = 'Pause'  # Fist
        pyautogui.press('space')  # Simulate space bar press (play/pause)
        last_gesture = action
    # Two Fingers Gesture (Index and middle up)
    elif (index_tip.y < middle_tip.y and abs(index_tip.x - middle_tip.x) < 0.03):
        action = 'Volume Up'  # Index and middle fingers extended
        pyautogui.press('up')  # Simulate arrow up (volume up)
        last_gesture = action
    # Ring and Pinky (Volume down)
    elif (ring_tip.y < pinky_tip.y and abs(ring_tip.x - pinky_tip.x) < 0.03):
        action = 'Volume Down'  # Ring and pinky fingers extended
        pyautogui.press('down')  # Simulate arrow down (volume down)
        last_gesture = action
    # All except Pinky Gesture (Previous Video)
    elif (index_tip.y < ring_tip.y and middle_tip.y < ring_tip.y and index_tip.x < ring_tip.x):
        action = 'Previous Video'  # All except pinky
        pyautogui.press('left')  # Simulate left arrow (previous video)
        last_gesture = action
    # All except Index Gesture (Next Video)
    elif (middle_tip.y < index_tip.y and abs(middle_tip.x - index_tip.x) > 0.05):
        action = 'Next Video'  # All except index
        pyautogui.press('right')  # Simulate right arrow (next video)
        last_gesture = action
    else:
        return None

    # Reset cool-down timer after gesture is recognized
    last_gesture_time = time.time()
    return action

# Video capture (use your webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later mirror view
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Draw the hand landmarks on the frame
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Draw landmarks and connections
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Check for gestures
            action = check_gesture(landmarks.landmark)
            if action:
                cv2.putText(frame, f'Action: {action}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the frame
    cv2.imshow("Hand Gesture Recognition", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

