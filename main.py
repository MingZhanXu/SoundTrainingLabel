import os
import cv2
from lib import UI, UIFunction, PageInfo, ArgsKwargs, Status
from lib import SqlCommands
from lib import Recorder
from lib import CameraCapture
from lib import get_key

def get_file_sequence(file_path, file_type):
    file_sequence = []
    for file in os.listdir(file_path):
        if file.endswith(file_type):
            file_sequence.append(file)
    return file_sequence
def print_i():
    print()

if __name__ == "__main__":
    index_name = [
        ["up", "down", "left", "right", "start", "rotation", "stop"],
        ["上", "下", "左", "右", "開始", "旋轉", "停止"],
        ["讚上", "讚下", "讚左", "讚右"]
        ]
    cap = cv2.VideoCapture(0)
    recorder = Recorder()
    camera_capture = CameraCapture(cap)
    function = [
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=recorder.record_audio),
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=recorder.record_audio),
        UIFunction(title="拍攝", running="拍攝中", finish="拍攝完畢", function=camera_capture.camera_capture),
    ]
    status_function = [
        Status(camera_capture.start_status, print_i),
        Status(print_i, camera_capture.start_status),
        Status(camera_capture.stop_status, camera_capture.stop_status),
    ]
    ui = UI(index_name, function, status_function)
    ui.show()
    status = [
        [None, None],
        [None, None],
        [None, None]
    ]
    while True:
        key = get_key()
        if key is None:
            continue
        if key == "p":
            ui.previous_page(args_kwargs=status)
        elif key == "n":
            ui.next_page(args_kwargs=status)
        elif key == "\x1b":
            ui.exit()
            break
        elif key > "0" and key <= "9":
            ui.show()
            args_kwargs = ArgsKwargs(save_path="test", file_name="test")
            result = ui.run_function(int(key) - 1, args_kwargs)
            print(result)