import os
import cv2
import re
from lib import UI, UIFunction, ArgsKwargs, Status, FileSequence
from lib import SqlCommands
from lib import Recorder
from lib import CameraCapture
from lib import get_key, print_flush
# 初始化設定資料夾
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
# 獲取資料夾內檔案數量
def get_file_sequence(file_path, file_type):
    file_sequence = []
    for page, folders in enumerate(file_path):
        file_sequence.append([])
        for path in folders:
            count = 0
            for file in os.listdir(path):
                if file.endswith(file_type[page]):
                    count += 1
            file_sequence[page].append(count)
    return file_sequence
# 無功能
def print_i():
    pass
# 獲取最後一筆資料
def get_last_file(sql):
    if isinstance(sql.select_latest_data(), tuple):
        return sql.select_latest_data()[1]
    return None
if __name__ == "__main__":
    index_name = [
        ["up", "down", "left", "right", "start", "rotation", "stop"],
        ["上", "下", "左", "右", "開始", "旋轉", "停止"],
        ["讚上", "讚下", "讚左", "讚右"]
        ]
    file_type = [".wav", ".wav", ".jpg"]
    file_path = set_folder(index_name)
    file_sequence = get_file_sequence(file_path, file_type)
    # print(file_sequence)
    # exit()
    sql = SqlCommands()
    recorder = Recorder()
    cap = cv2.VideoCapture(0)
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
    
    status = [
        [None, None],
        [None, None],
        [None, None]
    ]
    last_file = get_last_file(sql)
    file_info = FileSequence(last_file, file_sequence)
    
    ui.show(file_info)
    while True:
        key = get_key()
        if key is None:
            continue
        if key == "p":
            ui.previous_page(file_info, args_kwargs=status)
        elif key == "n":
            ui.next_page(file_info, args_kwargs=status)
        elif key == "\x1b":
            ui.end([s[1] for s in status])
            break
        elif key == "d":
            ui.show(file_info)
            del_file = get_last_file(sql)
            if del_file is None:
                print_flush(" 無檔案可刪除")
                continue
            parts = re.split(r'[\\/]', del_file)
            page = int(parts[0][5:]) - 1
            index = index_name[page].index(parts[1])
            try:
                os.remove(del_file)
                msg_str = f" 檔案已刪除 {del_file}"
            except Exception as e:
                msg_str = f" 檔案不存在 {del_file}"
            sql.delete_last_data()
            last_file = get_last_file(sql)
            file_info.del_file((page, index), last_file)
            ui.show(file_info)
            print_flush(msg_str)
        elif key > "0" and key <= "9":
            ui.show(file_info)
            index = int(key) - 1
            save_path = f"page_{ui.page()+1}"
            file_name = index_name[ui.page()][index]
            if file_name is not None:
                save_path = os.path.join(save_path, file_name)
            seq = file_info.index_sequence(ui.page(), index)
            file_name = f"{file_name}_{seq}"
            args_kwargs = ArgsKwargs(save_path, file_name)
            result = ui.run_function(index, args_kwargs)
            if result is not None:
                file_info.add_file((ui.page(), index), result)
                ui.show(file_info)
                print_flush(f" 檔案已儲存至 {result}")
                ui.finish_function(index)
                sql.insert_file_path(result)
        else:
            ui.show(file_info)
            ui.no_index()