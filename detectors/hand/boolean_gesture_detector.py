# boolean_gesture_detector.py

import math

class BooleanGestureDetector:
    def __init__(self):
        # Format: (Tip_Index, PIP_Index, MCP_Index)
        # Using PIP as the reference for 'up' vs 'down' via distance from wrist
        self.finger_joints = {
            'index': (8, 6, 5),
            'middle': (12, 10, 9),
            'ring': (16, 14, 13),
            'pinky': (20, 18, 17)
        }
        
        # Tuple format: (Thumb, Index, Middle, Ring, Pinky) representing up (True) or down (False)
        self.gesture_map = {
            (False, False, False, False, False): "Fist",
            (True, True, True, True, True): "Open Hand",
            (True, False, False, False, False): "Thumbs Up",
            (False, True, False, False, False): "Pointing Up (1)",
            (False, True, True, False, False): "Peace Sign (2)",
            (False, True, True, True, False): "Three Fingers",
            (False, True, True, True, True): "Four Fingers",
            (True, True, True, False, False): "Number 3 (ASL)",
            (True, True, True, True, False): "Four Fingers with Thumb",
            (False, False, False, False, True): "Pinky Promise",
            (True, False, False, False, True): "Shaka / Call Me",
            (False, True, False, False, True): "Rock On",
            (True, True, False, False, True): "I Love You",
            (True, True, False, False, False): "Finger Gun / L-Shape",
            (False, False, True, False, False): "Middle Finger",
            (False, False, False, True, False): "Ring Finger",
            (False, False, True, True, True): "OK Sign (Approx)",
            (True, False, True, True, True): "Perfect / Coin",
            (False, True, False, True, True): "Index, Ring, Pinky",
            (False, False, True, True, False): "Middle & Ring",
            (True, False, True, False, False): "Thumb & Middle",
            (True, False, False, True, False): "Thumb & Ring",
            (False, True, True, False, True): "Index, Middle, Pinky",
            (False, True, False, True, False): "Index & Ring",
            (True, False, True, False, True): "Thumb, Middle, Pinky",
            (True, True, False, True, False): "Thumb, Index, Ring",
            (False, False, True, False, True): "Middle & Pinky",
            (True, True, False, True, True): "Thumb, Index, Ring, Pinky",
            (True, False, True, True, False): "Thumb, Middle, Ring",
            (False, False, False, True, True): "Ring & Pinky"
        }

    def _get_distance(self, p1, p2):
        """Calculates Euclidean distance between two landmarks."""
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def get_finger_states(self, hand_landmarks):
        """Returns boolean values for the 4 main fingers (Distance-based logic)."""
        states = {}
        wrist = hand_landmarks[0]
        
        for finger_name, joints in self.finger_joints.items():
            tip = hand_landmarks[joints[0]]
            pip = hand_landmarks[joints[1]]
            
            # Rotationally invariant: if Tip is further from Wrist than the PIP joint is
            states[finger_name] = self._get_distance(wrist, tip) > self._get_distance(wrist, pip)
        return states

    def is_palm_facing(self, hand_landmarks, handedness):
        """
        Determines if the palm or back of the hand is facing the camera.
        Logic: Compares Index MCP (5) and Pinky MCP (17) relative positions.
        """
        index_mcp = hand_landmarks[5]
        pinky_mcp = hand_landmarks[17]
        
        # Adjusting for the mirrored coordinate space in main.py
        if handedness == "Right":
            return index_mcp.x > pinky_mcp.x
        else:
            return index_mcp.x < pinky_mcp.x

    def get_thumb_state(self, hand_landmarks, handedness):
        """Returns boolean value for the thumb (Distance-based logic)."""
        # Distance from thumb tip to pinky MCP is a robust indicator of extension
        # across all rotations.
        thumb_tip = hand_landmarks[4]
        thumb_ip = hand_landmarks[3]
        pinky_mcp = hand_landmarks[17]
        
        return self._get_distance(thumb_tip, pinky_mcp) > self._get_distance(thumb_ip, pinky_mcp)

    def detect_gesture(self, hand_landmarks, handedness):
        """Evaluates all 5 fingers and returns the mapped gesture name, state tuple, and facing."""
        is_palm = self.is_palm_facing(hand_landmarks, handedness)
        states = self.get_finger_states(hand_landmarks)
        
        # Thumb state now respects if the hand is flipped
        thumb_state = self.get_thumb_state(hand_landmarks, handedness)
        
        state_tuple = (
            thumb_state,
            states['index'],
            states['middle'],
            states['ring'],
            states['pinky']
        )
        
        gesture_name = self.gesture_map.get(state_tuple, "Unknown Gesture")
        facing = "Palm" if is_palm else "Back"
        return gesture_name, state_tuple, facing



    def detect_gesture(self, hand_landmarks, handedness):
        """Evaluates all 5 fingers and returns the mapped gesture name, state tuple, and facing."""
        is_palm = self.is_palm_facing(hand_landmarks, handedness)
        states = self.get_finger_states(hand_landmarks)
        
        # Thumb state now respects if the hand is flipped
        thumb_state = self.get_thumb_state(hand_landmarks, handedness)
        
        state_tuple = (
            thumb_state,
            states['index'],
            states['middle'],
            states['ring'],
            states['pinky']
        )
        
        gesture_name = self.gesture_map.get(state_tuple, "Unknown Gesture")
        facing = "Palm" if is_palm else "Back"
        return gesture_name, state_tuple, facing
