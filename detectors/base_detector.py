import mediapipe as mp
from mediapipe.tasks.python import vision

class BaseDetector:
    """Base class for all MediaPipe Task detectors using LIVE_STREAM mode."""
    def __init__(self, model_path, running_mode=vision.RunningMode.LIVE_STREAM):
        self.model_path = model_path
        self.running_mode = running_mode
        self.latest_result = None
        self.detector = None

    def _result_callback(self, result, output_image, timestamp_ms):
        self.latest_result = result

    def detect_async(self, mp_image, timestamp_ms):
        if self.detector:
            self.detector.detect_async(mp_image, timestamp_ms)

    def draw(self, frame):
        """Draw landmarks and annotations on the frame. To be implemented by subclasses."""
        pass

    def get_latest_data(self):
        """Return structured dictionary data from the latest detection. To be implemented by subclasses."""
        return []

    def close(self):
        if self.detector:
            self.detector.close()
