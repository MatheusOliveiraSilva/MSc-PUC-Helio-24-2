import cv2

class VideoStream:
    def __init__(self, camera_index=1):
        self.cap = cv2.VideoCapture(camera_index)

    def capture_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame

    def show_frame(self, frame):
        cv2.imshow("Video Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Sai ao pressionar 'q'
            self.release()

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
