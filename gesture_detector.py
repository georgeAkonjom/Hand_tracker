# gesture_detector.py

class GestureDetector:
    def __init__(self):
        # Format: (Tip_Index, Knuckle_Index)
        self.finger_joints = {
            'index': (8, 6),
            'middle': (12, 10),
            'ring': (16, 14),
            'pinky': (20, 18)
        }

    def get_finger_states(self, hand_landmarks):
        """Returns boolean values for the 4 main fingers (Y-axis logic)."""
        states = {}
        for finger_name, joints in self.finger_joints.items():
            tip_idx = joints[0]
            knuckle_idx = joints[1]
            states[finger_name] = hand_landmarks[tip_idx].y < hand_landmarks[knuckle_idx].y
        return states

    def get_thumb_state(self, hand_landmarks, handedness):
        """Returns boolean value for the thumb (X-axis logic adjusted for mirrored screen)."""
        thumb_tip = hand_landmarks[4]
        thumb_base = hand_landmarks[2]
        
        if handedness == "Right":
            return thumb_tip.x > thumb_base.x
        else:
            return thumb_tip.x < thumb_base.x

    def recognize(self, hand_landmarks, handedness):
        """Evaluates all 5 fingers and returns a gesture name AND finger count."""
        states = self.get_finger_states(hand_landmarks)
        states['thumb'] = self.get_thumb_state(hand_landmarks, handedness)
        
        finger_count = sum(states.values())
        gesture_name = "Unknown Gesture"

        # Gesture Navigation
        if states['thumb'] and not any([states['index'], states['middle'], states['ring'], states['pinky']]):
            gesture_name = "Thumbs Up!"
            
        elif all(states.values()):
            gesture_name = "High Five"
            
        elif not any(states.values()):
            gesture_name = "Fist"
            
        elif not states['thumb'] and states['index'] and states['middle'] and not states['ring'] and not states['pinky']:
            gesture_name = "Peace Sign"

        return gesture_name, finger_count