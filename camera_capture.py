import cv2
import os
from time import sleep
import threading
import msvcrt
class CameraCapture():
    def __init__(self, cap, window_name="camera"):
        self.__cap = cap
        self.__window_name = window_name
        self.__status = False
        self.__frame = None
        self.__threading_event = threading.Event()

    def capture(self):
        try:
            ret, frame = self.__cap.read()
        except Exception:
            return None
        if not ret:
            return None
        return frame
    def start_status(self):
        self.__status = True
        self.__threading_event.clear()
        self.__show_thread = threading.Thread(target=self.__show_img_thread)
        self.__show_thread.start()

    def stop_status(self):
        self.__status = False
        self.__threading_event.set()
        if self.__show_thread is not None:
            self.__show_thread.join()

    def __show_img_thread(self):
        while True:
            self.__frame = self.capture()
            if self.__status:
                cv2.imshow(self.__window_name, self.__frame)
                cv2.waitKey(1)
            else:
                if cv2.getWindowProperty(self.__window_name, cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow(self.__window_name)
                break

    def frame_to_file(self, save_path, file_name):
        frame = None
        if self.__frame is not None:
            frame = self.__frame
        if frame is None:
            return None
        file_path = os.path.join(save_path, f"{file_name}.jpg")
        cv2.imwrite(file_path, frame)
        return file_path
    def camera_capture(self, save_path, file_name):
        result = self.frame_to_file(save_path, file_name)
        return result
        
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    camera = CameraCapture(cap)
    camera.start_status()
    save_path = "tmp"
    file_name = "img_test"
    file_path = camera.camera_capture(save_path, file_name)
    print(file_path)
    while True:
        # continue
        key = msvcrt.getch().decode("utf-8")
        print(key, key=="q")
        if key == "q":
            camera.stop_status()
            break
        else:
            file_path = camera.camera_capture(save_path, file_name)
            print(file_path)