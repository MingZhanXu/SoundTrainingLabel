import os
import cv2
from lib import UI, UIFunction, ArgsKwargs, Status
from lib import SqlCommands
from lib import Recorder
from lib import CameraCapture
from lib import get_key, print_flush
def set_folder(index_name):
    file_path = []
    for page, names in enumerate(index_name):
        file_path.append([])
        page_str = f"page_{page+1}"
        if not os.path.exists(page_str):
            os.makedirs(page_str)
        for path in names:
            full_path = os.path.join(page_str, path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            file_path[page].append(full_path)
    return file_path
def get_file_sequence(file_path, file_type):
    file_sequence = []
    for page, folders in enumerate(file_path):
        file_sequence.append([])
        for path in folders:
            count = 0
            for file in os.listdir(path):
                if file.endswith(file_type):
                    count += 1
            file_sequence[page].append(count)
    return file_sequence
def print_i():
    # print()
    pass
def get_last_file(sql):
    return sql.select_last_data()[1]
if __name__ == "__main__":
    index_name = [
        ["up", "down", "left", "right", "start", "rotation", "stop"],
        ["上", "下", "左", "右", "開始", "旋轉", "停止"],
        ["讚上", "讚下", "讚左", "讚右"]
        ]
    file_type = [".wav", ".wav", ".jpg"]
    file_path = set_folder(index_name)
    file_sequence = get_file_sequence(file_path, file_type)
    print(file_sequence)
    exit()
    sql = SqlCommands()
    cap = cv2.VideoCapture(1)
    recorder = Recorder()
    camera_capture = CameraCapture(cap)
    function = [
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=recorder.record_audio),
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=recorder.record_audio),
        UIFunction(title="拍攝", running="拍攝中", finish="拍攝完畢", function=camera_capture.camera_capture),
    ]
    status_function = [
        Status(print_i, print_i),
        Status(print_i, print_i),
        Status(camera_capture.start_status, camera_capture.stop_status),
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
            ui.end([s[1] for s in status])
            break
        elif key > "0" and key <= "9":
            ui.show()
            index = int(key) - 1
            args_kwargs = ArgsKwargs(save_path="test", file_name="test")
            result = ui.run_function(index, args_kwargs)
            print_flush(f" 檔案已儲存至 {result}")
            ui.finish_function(index)
        else:
            ui.show()
            ui.no_index()