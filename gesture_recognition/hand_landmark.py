import mediapipe as mp
import cv2

class HandLandmarkDetector:
    def __init__(self):
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(static_image_mode=False,
                                    max_num_hands=1,
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5)

    def get_hand_landmarks(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            return [hand_landmark for hand_landmark in results.multi_hand_landmarks]
        return []

