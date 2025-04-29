import cv2
import mediapipe as mp
import pyautogui
import time
import logging

logging.basicConfig(filename='gesture_control.log', level=logging.INFO)

# Function to detect which fingers are up
def get_finger_states(hand_landmarks):
    finger_states = []

    # Thumb (use x axis for thumb)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        finger_states.append(1)
    else:
        finger_states.append(0)

    # For fingers: index, middle, ring, pinky (use y axis)
    tips_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for tip, pip in zip(tips_ids, pip_ids):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            finger_states.append(1)
        else:
            finger_states.append(0)

    return finger_states

# Gesture action map
gesture_actions = {
    (0, 0, 0, 0, 1): ("Next Video", lambda: pyautogui.hotkey("shift", "n")),
    (1, 0, 0, 0, 0): ("Previous Video", lambda: pyautogui.hotkey("shift", "p")),
    (1, 1, 1, 1, 1): ("Play", lambda: pyautogui.press("space")),
    (0, 1, 1, 0, 0): ("Volume Up", lambda: pyautogui.press("up")),
    (0, 1, 1, 1, 0): ("Volume Down", lambda: pyautogui.press("down")),
    (0, 0, 0, 0, 0): ("Pause", lambda: pyautogui.press("space")),
    (1, 1, 0, 0, 0): ("Seek Forward (5s)", lambda: pyautogui.press('right')),
    (1, 0, 0, 0, 1): ("Seek Backward (5s)", lambda: pyautogui.press('left'))
}

# Initialize MediaPipe
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Track previous gesture to prevent spamming
prev_gesture = None
last_gesture_time = time.time()
display_gesture_name = ""

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    current_time = time.time()

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        finger_states = tuple(get_finger_states(hand_landmarks))

        # Check if gesture is defined
        if finger_states in gesture_actions:
            gesture_name, action = gesture_actions[finger_states]
            display_gesture_name = gesture_name
            # Only trigger if new gesture or enough time has passed
            if gesture_name != prev_gesture or (current_time - last_gesture_time) > 1:
                print(f"Gesture: {gesture_name}")
                action()
                prev_gesture = gesture_name
                last_gesture_time = current_time

         # Show the detected gesture on the screen
        cv2.putText(frame, f"Gesture: {display_gesture_name}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with gestures and feedback
    cv2.imshow("Hand Gesture Control", frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()