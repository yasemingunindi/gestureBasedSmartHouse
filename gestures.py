import cv2
import mediapipe as mp

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

def is_hand_closed(landmarks):
    # Check if all finger tips are below the second knuckle (making a fist)
    finger_tips = [8, 12, 16, 20]  # Index finger, middle finger, ring finger, pinky tip landmarks
    closed = 0

    for tip in finger_tips:
        if landmarks.landmark[tip].y > landmarks.landmark[tip - 2].y:
            closed += 1

    # Hand is closed (fist) if all four fingers are curled in
    return closed == 4

def is_hand_open(landmarks):
    # Check if all finger tips are above the second knuckle (hand open)
    finger_tips = [8, 12, 16, 20]
    open_hand = 0

    for tip in finger_tips:
        if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
            open_hand += 1

    # Hand is open if all four fingers are extended
    return open_hand == 4

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame color to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    # Detect and process hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check if the hand is closed (fist)
            if is_hand_closed(hand_landmarks):
                print("FIST")
            elif is_hand_open(hand_landmarks):
                print("HAND OPEN")

    # Display the frame
    cv2.imshow('Gesture Recognition', frame)

    # Exit the loop on spacebar press
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
