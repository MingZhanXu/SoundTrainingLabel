import cv2
import os
class CameraCapture():
    def __init__(self, cap):
        self.__cap = cap
    def capture(self):
        try:
            ret, frame = self.__cap.read()
        except Exception:
            return None
        if not ret:
            return None
        return frame
    def frame_to_file(self, frame, save_path, file_name):
        if frame is None:
            return frame
        file_path = os.path.join(save_path, f"{file_name}.jpg")
        if frame is not None:
            print(frame)
            cv2.imwrite(file_path, frame)
        return file_path
    def camera_capture(self, save_path, file_name, frame_count=5):
        for _ in range(frame_count):
            frame = self.capture()
        result = self.frame_to_file(frame, save_path, file_name)
        return result
        
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    camera = CameraCapture(cap)
    save_path = "tmp"
    file_name = "img_test"
    file_path = camera.camera_capture(save_path, file_name)
    print(file_path)