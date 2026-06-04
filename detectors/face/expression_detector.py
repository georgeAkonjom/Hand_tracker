import math

class ExpressionDetector:
    def __init__(self, calibration_duration_sec=3.0):
        self.calibration_duration_sec = calibration_duration_sec
        self.is_calibrated = False
        self.calibration_start_time = None
        self.calibration_data = []
        
        # Neutral baselines
        self.neutral_mouth_width = 0.0
        self.neutral_mouth_corner_y_avg = 0.0
        self.neutral_nose_to_corner_dist = 0.0
        
        # Landmark indices (MediaPipe Face Mesh)
        self.LEFT_CORNER = 61
        self.RIGHT_CORNER = 291
        self.NOSE_TIP = 1
        self.UPPER_LIP = 13
        self.LOWER_LIP = 14

    def _get_distance(self, p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def calibrate(self, face_landmarks, current_time):
        if self.calibration_start_time is None:
            self.calibration_start_time = current_time
            print("Calibration started... Keep a neutral expression.")
            return False

        elapsed = current_time - self.calibration_start_time
        
        # Collect data during the window
        left = face_landmarks[self.LEFT_CORNER]
        right = face_landmarks[self.RIGHT_CORNER]
        nose = face_landmarks[self.NOSE_TIP]
        
        self.calibration_data.append({
            'width': self._get_distance(left, right),
            'corner_y': (left.y + right.y) / 2.0,
            'nose_dist': (self._get_distance(nose, left) + self._get_distance(nose, right)) / 2.0
        })

        if elapsed >= self.calibration_duration_sec:
            # Calculate averages
            self.neutral_mouth_width = sum(d['width'] for d in self.calibration_data) / len(self.calibration_data)
            self.neutral_mouth_corner_y_avg = sum(d['corner_y'] for d in self.calibration_data) / len(self.calibration_data)
            self.neutral_nose_to_corner_dist = sum(d['nose_dist'] for d in self.calibration_data) / len(self.calibration_data)
            
            self.is_calibrated = True
            print("Calibration complete.")
            return True
            
        return False

    def detect_expression(self, face_landmarks):
        if not self.is_calibrated:
            return "Calibrating..."

        left = face_landmarks[self.LEFT_CORNER]
        right = face_landmarks[self.RIGHT_CORNER]
        nose = face_landmarks[self.NOSE_TIP]
        
        current_width = self._get_distance(left, right)
        current_corner_y = (left.y + right.y) / 2.0
        current_nose_dist = (self._get_distance(nose, left) + self._get_distance(nose, right)) / 2.0
        
        # Heuristics:
        # Smile: Mouth width increases, corners move up (y decreases)
        # Frown: Corners move down (y increases) relative to nose/eyes
        
        width_ratio = current_width / self.neutral_mouth_width
        y_diff = current_corner_y - self.neutral_mouth_corner_y_avg
        
        if width_ratio > 1.15 and y_diff < -0.005:
            return "Smile"
        elif y_diff > 0.008:
            return "Frown"
        else:
            return "Neutral"
