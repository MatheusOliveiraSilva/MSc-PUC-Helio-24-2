from utils.video_stream import VideoStream
from gesture_recognition.hand_landmark import HandLandmarkDetector
from gesture_recognition.gesture_logic import detect_gesture

detector = HandLandmarkDetector()
video = VideoStream()

for frame in video.capture_frames():
    landmarks_list = detector.get_hand_landmarks(frame)  # Agora é uma lista
    for landmarks in landmarks_list:  # Percorra cada mão detectada
        gesture = detect_gesture(landmarks.landmark)  # Use `landmark` para acessar os pontos
        if gesture:
            print(f"Gesto detectado: {gesture}")
    video.show_frame(frame)
