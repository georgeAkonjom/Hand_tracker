# boolean_gesture_detector.py

class BooleanGestureDetector:
    def __init__(self):
        # Format: (Tip_Index, Knuckle_Index)
        self.finger_joints = {
            'index': (8, 6),
            'middle': (12, 10),
            'ring': (16, 14),
            'pinky': (20, 18)
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

    def get_finger_states(self, hand_landmarks):
        """Returns boolean values for the 4 main fingers (Y-axis logic)."""
        states = {}
        for finger_name, joints in self.finger_joints.items():
            tip_idx = joints[0]
            knuckle_idx = joints[1]
            # Finger is considered 'up' if the tip is higher (lower y-coordinate) than the knuckle
            states[finger_name] = hand_landmarks[tip_idx].y < hand_landmarks[knuckle_idx].y
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
        """Returns boolean value for the thumb (X-axis logic), adjusted for palm facing."""
        thumb_tip = hand_landmarks[4]
        thumb_base = hand_landmarks[2]
        is_palm = self.is_palm_facing(hand_landmarks, handedness)
        
        # Base logic: Is the thumb extended 'outwards' from the palm?
        if handedness == "Right":
            state = thumb_tip.x > thumb_base.x
        else:
            state = thumb_tip.x < thumb_base.x
            
        # If the back of the hand is facing, the X-order of thumb-out vs thumb-in is reversed
        return state if is_palm else not state

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
