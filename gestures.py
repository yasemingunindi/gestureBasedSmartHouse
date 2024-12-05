import cv2
import mediapipe as mp
import math

#comment 

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    :param point1: Tuple (x1, y1) of the first point.
    :param point2: Tuple (x2, y2) of the second point.
    :return: Distance as a float.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def is_finger_up(landmarks, tip_idx, pip_idx, mcp_idx):
    """
    Check if a specific finger is raised.
    :param landmarks: List of hand landmarks.
    :param tip_idx: Index of the fingertip landmark.
    :param pip_idx: Index of the PIP (middle joint) landmark.
    :param mcp_idx: Index of the MCP (base joint) landmark.
    :return: Boolean indicating if the finger is raised.
    """
    return landmarks[tip_idx].y < landmarks[pip_idx].y < landmarks[mcp_idx].y

def is_index_pointing_up(landmarks):
    """Check if the index finger is pointing up."""
    return is_finger_up(landmarks, 8, 7, 6)

def is_peace_sign(landmarks):
    """Check if the peace sign (index and middle fingers up) is shown."""
    return (is_finger_up(landmarks, 8, 7, 6) and
            is_finger_up(landmarks, 12, 11, 10) and
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

def is_three(landmarks):
    """Check if the gesture showing three fingers (index, middle, and ring) is made."""
    return (is_finger_up(landmarks, 8, 7, 6) and
            is_finger_up(landmarks, 12, 11, 10) and
            is_finger_up(landmarks, 16, 15, 14) and
            landmarks[20].y > landmarks[18].y)

def is_thumbs_up(landmarks):
    """Check if the thumb is pointing up."""
    return (landmarks[4].y < landmarks[3].y and
            landmarks[4].x < landmarks[3].x)

def is_thumbs_down(landmarks):
    """Check if the thumb is pointing down."""
    return (landmarks[4].y > landmarks[3].y and
            landmarks[4].x < landmarks[3].x)

def is_thumbs_left(landmarks):
    """Check if the thumb is rotated 90 degrees to the left."""
    return (landmarks[4].y > landmarks[3].y and
            landmarks[4].x > landmarks[3].x)

def is_thumbs_right(landmarks):
    """Check if the thumb is rotated 90 degrees to the right."""
    return (landmarks[4].y < landmarks[3].y and
            landmarks[4].x > landmarks[3].x)

def is_good_gesture(landmarks):
    """Check if the 'OK' or 'Good' gesture is made."""
    distance = calculate_distance(
        (landmarks[8].x, landmarks[8].y), (landmarks[4].x, landmarks[4].y)
    )
    return distance < 0.05

def detect_gesture(landmarks):
    """
    Detect gestures based on hand landmarks.
    :param landmarks: List of hand landmarks.
    :return: String indicating the gesture detected.
    """
    if is_index_pointing_up(landmarks):
        return "INDEX POINTING UP"
    elif is_peace_sign(landmarks):
        return "PEACE SIGN"
    elif is_three(landmarks):
        return "THREE"
    elif is_thumbs_up(landmarks):
        return "THUMBS UP"
    elif is_thumbs_down(landmarks):
        return "THUMBS DOWN"
    elif is_thumbs_left(landmarks):
        return "THUMBS LEFT"
    elif is_thumbs_right(landmarks):
        return "THUMBS RIGHT"
    elif is_good_gesture(landmarks):
        return "GOOD GESTURE"
    return "UNKNOWN GESTURE"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    # Process hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            gesture = detect_gesture(landmarks)
            print(gesture)

    # Display the frame
    cv2.imshow('Gesture Recognition', frame)

    # Exit loop on pressing the spacebar
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
