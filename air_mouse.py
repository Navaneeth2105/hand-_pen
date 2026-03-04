"""
Hand Pen - Python Desktop Version
A gesture-controlled virtual mouse and drawing application using hand tracking.

Usage:
    python air_mouse.py

Controls:
    - Index Finger Position: Controls cursor movement
    - Index + Middle Pinch: Click
    - Both Fingers Up: Scroll
    - Press 'q' or 'Q': Exit application

Requirements:
    pip install opencv-python mediapipe pyautogui numpy
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import sys

# Configuration
CONFIG = {
    'smoothing': 5,
    'min_detection_confidence': 0.7,
    'max_num_hands': 1,
    'click_distance_threshold': 40,
    'double_click_delay': 0.2,
    'scroll_cooldown': 0.1,
    'fps_display': True,
    'debug_mode': False,
}

class HandMouseController:
    """Controller for hand gesture recognition and mouse control."""
    
    def __init__(self):
        """Initialize MediaPipe and webcam."""
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=CONFIG['max_num_hands'],
            min_detection_confidence=CONFIG['min_detection_confidence']
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam. Please check camera connection.")
        
        # Screen settings
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.FAILSAFE = False
        
        # State variables
        self.prev_x, self.prev_y = 0, 0
        self.last_click_time = 0
        self.last_scroll_time = 0
        self.is_clicking = False
        
        # FPS tracking
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
        
        print("✅ Hand Mouse Controller initialized")
        print(f"📺 Screen resolution: {self.screen_width}x{self.screen_height}")
        print("🖱️  Ready to control! Press 'q' to exit")
        
    def calculate_distance(self, point1, point2, width, height):
        """Calculate Euclidean distance between two hand landmarks."""
        dx = (point1.x - point2.x) * width
        dy = (point1.y - point2.y) * height
        return np.hypot(dx, dy)
    
    def apply_smoothing(self, current_x, current_y, prev_x, prev_y):
        """Apply exponential smoothing to cursor movement."""
        smoothed_x = prev_x + (current_x - prev_x) / CONFIG['smoothing']
        smoothed_y = prev_y + (current_y - prev_y) / CONFIG['smoothing']
        return smoothed_x, smoothed_y
    
    def handle_mouse_movement(self, landmarks, frame_width, frame_height):
        """Handle cursor movement based on index finger position."""
        index_finger = landmarks[8]  # Index finger tip
        
        # Map hand coordinates to screen coordinates
        x = np.interp(index_finger.x * frame_width, (100, frame_width - 100), 
                      (0, self.screen_width))
        y = np.interp(index_finger.y * frame_height, (100, frame_height - 100), 
                      (0, self.screen_height))
        
        # Apply smoothing
        smoothed_x, smoothed_y = self.apply_smoothing(x, y, self.prev_x, self.prev_y)
        
        # Move cursor
        pyautogui.moveTo(smoothed_x, smoothed_y)
        
        self.prev_x, self.prev_y = smoothed_x, smoothed_y
        return smoothed_x, smoothed_y
    
    def handle_click(self, landmarks, frame_width, frame_height):
        """Detect pinch gesture (index + middle finger) for clicking."""
        index_finger = landmarks[8]
        middle_finger = landmarks[12]
        
        distance = self.calculate_distance(index_finger, middle_finger, 
                                          frame_width, frame_height)
        
        # Pinch detected
        if distance < CONFIG['click_distance_threshold']:
            current_time = time.time()
            if current_time - self.last_click_time > CONFIG['double_click_delay']:
                pyautogui.click()
                self.last_click_time = current_time
                self.is_clicking = True
                if CONFIG['debug_mode']:
                    print(f"🖱️  Click detected (distance: {distance:.1f})")
        else:
            self.is_clicking = False
    
    def handle_scroll(self, landmarks):
        """Detect scroll gesture (both fingers up/down)."""
        index_finger = landmarks[8]
        middle_finger = landmarks[12]
        
        # Check if both index and middle fingers are pointing up
        if index_finger.y < landmarks[6].y and middle_finger.y < landmarks[10].y:
            current_time = time.time()
            
            if current_time - self.last_scroll_time > CONFIG['scroll_cooldown']:
                # Scroll up if fingers are in upper part of frame
                if index_finger.y < 0.3:
                    pyautogui.scroll(5)
                    self.last_scroll_time = current_time
                    if CONFIG['debug_mode']:
                        print("⬆️  Scroll up")
                # Scroll down if fingers are in lower part of frame
                elif index_finger.y > 0.7:
                    pyautogui.scroll(-5)
                    self.last_scroll_time = current_time
                    if CONFIG['debug_mode']:
                        print("⬇️  Scroll down")
    
    def update_fps(self):
        """Update and display FPS counter."""
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = time.time()
    
    def draw_debug_info(self, frame, hand_detected, cursor_pos=None):
        """Draw debug information on frame."""
        h, w = frame.shape[:2]
        
        # FPS counter
        if CONFIG['fps_display']:
            cv2.putText(frame, f"FPS: {self.fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Status
        status = "Hand Detected ✓" if hand_detected else "No Hand Detected"
        color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.putText(frame, status, (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Cursor position
        if cursor_pos:
            cv2.putText(frame, f"Cursor: ({cursor_pos[0]:.0f}, {cursor_pos[1]:.0f})",
                       (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Instructions
        cv2.putText(frame, "Press 'q' to exit", (w - 200, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Main application loop."""
        try:
            while True:
                success, frame = self.cap.read()
                if not success:
                    print("❌ Failed to read frame from webcam")
                    break
                
                # Flip frame for selfie view
                frame = cv2.flip(frame, 1)
                h, w, c = frame.shape
                
                # Process frame with MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                hand_detected = False
                cursor_pos = None
                
                # Process hand landmarks
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand_detected = True
                        landmarks = hand_landmarks.landmark
                        
                        # Handle gestures
                        cursor_pos = self.handle_mouse_movement(landmarks, w, h)
                        self.handle_click(landmarks, w, h)
                        self.handle_scroll(landmarks)
                        
                        # Draw hand skeleton
                        self.mp_draw.draw_landmarks(frame, hand_landmarks,
                                                   self.mp_hands.HAND_CONNECTIONS)
                
                # Update and display FPS
                self.update_fps()
                self.draw_debug_info(frame, hand_detected, cursor_pos)
                
                # Display frame
                cv2.imshow("Hand Mouse Controller", frame)
                
                # Check for exit
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    print("👋 Exiting application...")
                    break
        
        except KeyboardInterrupt:
            print("\n⏸️  Interrupted by user")
        except Exception as e:
            print(f"❌ Error occurred: {e}", file=sys.stderr)
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Resources cleaned up")


def main():
    """Main entry point."""
    try:
        controller = HandMouseController()
        controller.run()
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
