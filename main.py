import cv2
import mediapipe as mp
import time
import argparse
import sys

from detectors.hand.hand_detector import HandDetectorWrapper
from detectors.face.face_detector import FaceDetectorWrapper
from detectors.pose.pose_detector import PoseDetectorWrapper

def main():
    parser = argparse.ArgumentParser(description="Multi-Module Hand, Face, and Pose Tracker")
    parser.add_argument('--hand', action='store_true', help='Enable Hand Tracking')
    parser.add_argument('--face', action='store_true', help='Enable Face Tracking')
    parser.add_argument('--pose', action='store_true', help='Enable Pose Tracking')
    parser.add_argument('--all', action='store_true', help='Enable all modules')
    parser.add_argument('--url', type=str, help='IP Webcam URL (e.g., http://192.168.0.209:8080/video)')
    
    args = parser.parse_args()

    # If no flags are provided, default to --hand
    if not (args.hand or args.face or args.pose or args.all):
        print("No module specified. Defaulting to Hand Tracking.")
        args.hand = True

    active_detectors = []
    
    if args.hand or args.all:
        active_detectors.append(HandDetectorWrapper())
    if args.face or args.all:
        active_detectors.append(FaceDetectorWrapper())
    if args.pose or args.all:
        active_detectors.append(PoseDetectorWrapper())

    # Initialize Video Source
    video_source = args.url if args.url else 0
    
    # If the video source is a digit string, cast it to an integer device index
    if isinstance(video_source, str) and video_source.isdigit():
        video_source = int(video_source)
        
    # Common fix: IP Webcam usually requires /video suffix for the raw stream
    elif isinstance(video_source, str) and video_source.startswith("http") and not video_source.endswith("/video"):
        if not video_source.endswith("/"):
            video_source += "/"
        video_source += "video"
        
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}")
        sys.exit(1)
        
    # Minimize buffering latency for real-time camera feeds
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
    print(f"Streaming from: {'Local Camera' if video_source == 0 else video_source}")
    print("Press 'q' to quit.")

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue
                
            # Flip for natural mirrored view
            frame = cv2.flip(frame, 1)
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            
            # 1. Trigger Asynchronous Inference for all active detectors
            timestamp_ms = int(time.time() * 1000)
            for detector in active_detectors:
                detector.detect_async(mp_image, timestamp_ms)
            
            # 2. Draw results from all active detectors
            for detector in active_detectors:
                detector.draw(frame)

            cv2.imshow("Multi-Module Tracker", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        print("\nCleaning up...")
        for detector in active_detectors:
            detector.close()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
