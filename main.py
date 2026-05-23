# main.py
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from coordinate_translator import CoordinateTranslator
from boolean_gesture_detector import BooleanGestureDetector

# Hand tracking utilities (using the more stable tasks API)
try:
    mp_drawing = mp.tasks.vision.drawing_utils
    mp_drawing_styles = mp.tasks.vision.drawing_styles
    mp_hands = mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS
except AttributeError:
    # Fallback to older drawing utils if necessary
    import mediapipe.python.solutions.drawing_utils as mp_drawing
    import mediapipe.python.solutions.drawing_styles as mp_drawing_styles
    from mediapipe.python.solutions.hands import HAND_CONNECTIONS as mp_hands

# --- Hand Detector Setup ---
hand_options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path='models_landmarkers/hand_landmarker.task'),
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2, 
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
)
hand_detector = vision.HandLandmarker.create_from_options(hand_options)

# Initialize utilities
translator = CoordinateTranslator()
bool_detector = BooleanGestureDetector()

cap = cv2.VideoCapture(0)
print("Watching for hand motion... Press 'q' to quit.")

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
            
        # Flip for natural mirrored view
        frame = cv2.flip(frame, 1)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # 1. Process Hands
        hand_result = hand_detector.detect(mp_image)
        if hand_result.hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_result.hand_landmarks):
                raw_handedness = hand_result.handedness[idx][0].category_name
                handedness = "Right" if raw_handedness == "Left" else "Left"

                # Get geometry & gestures
                hand_data = translator.get_structured_data(hand_landmarks, handedness)
                gesture_name, _, facing = bool_detector.detect_gesture(hand_landmarks, handedness)
                
                # Display Results
                text_y = 50 + (idx * 80)
                wrist = hand_data['landmarks'][0]
                
                cv2.putText(frame, f"{handedness} {facing}: x={wrist['x']:.2f}, y={wrist['y']:.2f}", 
                            (20, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Gesture: {gesture_name}", 
                            (20, text_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                
                if mp_drawing:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

        cv2.imshow("Hand Tracker", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    print("\nReleasing camera...")
    cap.release()
    cv2.destroyAllWindows()
