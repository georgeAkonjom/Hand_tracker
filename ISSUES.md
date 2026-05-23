# Identified Issues and Potential Improvements

This document tracks technical debt, bugs, and suggested enhancements for the Hand Tracker project.

## 1. Rotation-Sensitive Gesture Detection
- **Issue:** `boolean_gesture_detector.py` uses absolute coordinate comparisons (e.g., `tip.y < knuckle.y`).
- **Impact:** Gestures only work when the hand is oriented vertically. Rotating the hand 90 degrees breaks detection.
- **Status:** Open.

## 2. Inefficient Running Mode
- **Issue:** The hand detector uses `vision.RunningMode.IMAGE`.
- **Impact:** For real-time video, `LIVE_STREAM` mode is more efficient and provides better temporal consistency (tracking).
- **Status:** Open.

## 3. Lack of Automated Testing
- **Issue:** No unit or integration tests exist for the 30 gesture mappings or coordinate translation logic.
- **Status:** Open.

## 4. Hardcoded Model Paths
- **Issue:** Pathing for `.task` files is relative to the root and hardcoded.
- **Status:** Open.
