# main.py
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gesture_detector import GestureDetector

mp_drawing = mp.tasks.vision.drawing_utils
mp_drawing_styles = mp.tasks.vision.drawing_styles
mp_hands = mp.tasks.vision.HandLandmarksConnections

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_hands=2, 
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
)

detector = vision.HandLandmarker.create_from_options(options)

# Initialize the gesture detector imported from gesture_detector.py
gesture_detector = GestureDetector()

cap = cv2.VideoCapture(0)
print("Watching for file changes... Press Ctrl+C in terminal to stop entirely.")

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
            
        # frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = detector.detect(mp_image)
        
        if detection_result.hand_landmarks:
            for idx in range(len(detection_result.hand_landmarks)):
                hand_landmarks = detection_result.hand_landmarks[idx]
                raw_handedness = detection_result.handedness[idx][0].category_name
                
                handedness = "Right" if raw_handedness == "Left" else "Left"
                
                # Use your external class
                gesture_name, finger_count = gesture_detector.recognize(hand_landmarks, handedness)
                
                display_text = f"{handedness}: {finger_count} Fingers | {gesture_name}"
                text_y_position = 50 + (idx * 40) 
                
                cv2.putText(
                    frame, display_text, (20, text_y_position), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
                )
                
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        cv2.imshow("Gesture Tracker", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    print("\nReleasing camera...")
    cap.release()
    cv2.destroyAllWindows()