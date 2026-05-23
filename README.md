# Hand Tracker & Gesture Recognizer

This project provides a real-time hand tracking and gesture recognition system using MediaPipe and OpenCV. It features dual tracking: high-fidelity raw coordinate extraction for reconstruction and a lightweight boolean-based gesture classifier.

## Features

- **Raw Geometry Extraction:** Provides (x, y, z) coordinates for all 21 hand landmarks via `CoordinateTranslator`.
- **30 Popular Gestures:** Recognizes 30 distinct hand signs using a deterministic boolean finger-state map.
- **Orientation Awareness:** Automatically detects if the Palm or the Back of the hand is facing the camera and adjusts detection logic (especially for the thumb) accordingly.
- **Natural Mirroring:** The video feed is flipped horizontally to provide an intuitive "selfie" view.

## Setup

1. **Environment:** It is recommended to use a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/bin/activate  # Linux/macOS
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **MediaPipe Model:** Ensure the `hand_landmarker.task` file is in the project root.

## Usage

Run the main script to start the tracker:
```bash
python main.py
```
- Press **'q'** to quit the application.
- The screen will display the Handedness, Orientation (Palm/Back), Wrist Coordinates, and the detected Gesture Name.

## Supported Gestures (30)

The system maps the boolean states (Up/Down) of the 5 fingers to the following gestures:

1.  **Fist**
2.  **Open Hand**
3.  **Thumbs Up**
4.  **Pointing Up (1)**
5.  **Peace Sign (2)**
6.  **Three Fingers**
7.  **Four Fingers**
8.  **Number 3 (ASL)**
9.  **Four Fingers with Thumb**
10. **Pinky Promise**
11. **Shaka / Call Me**
12. **Rock On**
13. **I Love You**
14. **Finger Gun / L-Shape**
15. **Middle Finger**
16. **Ring Finger**
17. **OK Sign (Approx)**
18. **Perfect / Coin**
19. **Index, Ring, Pinky**
20. **Middle & Ring**
21. **Thumb & Middle**
22. **Thumb & Ring**
23. **Index, Middle, Pinky**
24. **Index & Ring**
25. **Thumb, Middle, Pinky**
26. **Thumb, Index, Ring**
27. **Middle & Pinky**
28. **Thumb, Index, Ring, Pinky**
29. **Thumb, Middle, Ring**
30. **Ring & Pinky**

## Technical Details

- **Handedness:** Automatically corrected for the mirrored view.
- **Facing Detection:** Uses the relative position of the Index Knuckle (Landmark 5) and Pinky Knuckle (Landmark 17) to determine if the palm or back is visible.
- **Coordinate System:** Landmarks are normalized [0.0, 1.0] relative to the image width and height.
