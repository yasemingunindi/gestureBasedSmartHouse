import cv2
import mediapipe as mp
import math
# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Start video capture
cap = cv2.VideoCapture(0)

prev_x, prev_y = None, None

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
    """
    Check if only the index finger is pointing up and all other fingers are down.
    :param landmarks: List of hand landmarks.
    :return: Boolean indicating if only the index finger is up.
    """
    # Index finger is up
    index_up = is_finger_up(landmarks, 8, 7, 6)
    
    # Other fingers are down
    middle_down = not is_finger_up(landmarks, 12, 11, 10)  # Middle finger down
    ring_down = not is_finger_up(landmarks, 16, 15, 14)  # Ring finger down
    pinky_down = not is_finger_up(landmarks, 20, 19, 18)  # Pinky finger down
    
    return index_up and middle_down and ring_down and pinky_down


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
    return (landmarks[4].y < landmarks[3].y)
def is_thumbs_down(landmarks):
    """Check if the thumb is pointing down."""
    return (landmarks[4].y > landmarks[3].y)

def is_good_gesture(landmarks):
    """Check if the 'OK' or 'Good' gesture is made."""
    distance = calculate_distance(
        (landmarks[8].x, landmarks[8].y), (landmarks[4].x, landmarks[4].y)
    )
    return distance < 0.05

def is_rockn_roll(landmarks):
    """Check if rock n roll gesture is made."""
    # Index and Pinky fingers are up
    index_up = is_finger_up(landmarks, 8, 7, 6)
    pinky_up = is_finger_up(landmarks, 20, 19, 18)
    
    # Other fingers (middle, ring, and thumb) are down
    middle_down = not is_finger_up(landmarks, 12, 11, 10)
    ring_down = not is_finger_up(landmarks, 16, 15, 14)
    
    return index_up and pinky_up and middle_down and ring_down

def is_open(landmarks):
    """
    Check if the 'Four' gesture is made.
    :param landmarks: List of hand landmarks.
    :return: Boolean indicating if the Four gesture is detected.
    """
    # Index, Middle, Ring, and Pinky fingers are up
    index_up = is_finger_up(landmarks, 8, 7, 6)
    middle_up = is_finger_up(landmarks, 12, 11, 10)
    ring_up = is_finger_up(landmarks, 16, 15, 14)
    pinky_up = is_finger_up(landmarks, 20, 19, 18)
    
    return index_up and middle_up and ring_up and pinky_up

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
    elif is_rockn_roll(landmarks):
        return "ROCK'N ROLL!!!"
    elif is_open(landmarks):
        return(0)
    elif is_thumbs_up(landmarks):
        return "THUMBS UP"
    elif is_thumbs_down(landmarks):
        return "THUMBS DOWN"
    elif is_good_gesture(landmarks):
        return "GOOD GESTURE"
    return "UNKNOWN GESTURE"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    # Process hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            gesture = detect_gesture(landmarks)
            if(gesture != 0):
                print(gesture)
            # Get the tip of the index finger
            x = int(landmarks[8].x * frame.shape[1])  # Convert normalized x to pixel
            y = int(landmarks[8].y * frame.shape[0])  # Convert normalized y to pixel
            
            # Draw a circle to indicate the cursor
            cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
            
            if gesture == "PEACE SIGN":
                # Scroll behavior
                wrist_y = landmarks[0].y
                
                if prev_y is not None:
                    diff = wrist_y - prev_y
                    if diff > 0.05:  # Moving down
                        print("Scrolling Down")
                        cv2.putText(frame, "SCROLL DOWN", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    elif diff < -0.05:  # Moving up
                        print("Scrolling Up")
                        cv2.putText(frame, "SCROLL UP", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                prev_y = wrist_y
            else:
                prev_y = None  # Reset scroll variables if peace sign is not active

            
            if prev_x is not None and prev_y is not None:
                # Calculate movement
                dx = x - prev_x
                dy = y - prev_y
                
                # Determine gestures or actions
                if abs(dx) > 20 or abs(dy) > 20:
                    if abs(dx) > abs(dy):  # Horizontal movement
                        if dx > 0:
                            print("Moving Right")
                        else:
                            print("Moving Left")
                    else:  # Vertical movement
                        if dy > 0:
                            print("Moving Down")
                        else:
                            print("Moving Up")
            
            # Update previous coordinates
            prev_x, prev_y = x, y

    # Display the frame
    cv2.imshow('Gesture Recognition', frame)

    #  Exit the loop on spacebar press
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
