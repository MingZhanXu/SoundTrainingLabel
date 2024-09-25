from lib.recording import Recorder
from lib.sql_commands import SqlCommands
from lib.cmd_ui import UIFunction, UI, get_key
import os

def get_file_sequence(file_path):
    file_sequence = []
    for file in os.listdir(file_path):
        if file.endswith(".wav"):
            file_sequence.append(file)
    return file_sequence


if __name__ == "__main__":
    sql = SqlCommands()
    sql.connect_to_database()
    recorder = Recorder()
    page_name = [
        ["up", "down", "left", "right", "start", "rotation", "stop"],
        ["上", "下", "左", "右", "開始", "旋轉", "停止"],
    ]
    ui_functions = [
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=recorder.record_audio),
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=recorder.record_audio),
    ]
    ui = UI(page_name, ui_functions)
    try:
        last_file = sql.select_latest_data()[1]
    except Exception as e:
        print(e)
        last_file = None
    ui.show(last_file)
    while True:
        try:
            last_file = sql.select_latest_data()[1]
        except Exception as e:
            last_file = None
        key = get_key()
        if key is None:
            continue
        if key == "p":
            ui.previous_page()
            ui.show(last_file)
        elif key == "n":
            ui.next_page()
            ui.show(last_file)
        elif key == "\x1b":
            ui.exit()
            break
        elif key == "d":
            sql.delete_last_data()
            try:
                last_file = sql.select_latest_data()[1]
            except Exception as e:
                last_file = None
            ui.show(last_file)
        elif key > "0" and key <= "9":
            ui.show(last_file)
            file_name = ui.names()[int(key) - 1]
            if file_name is not None:
                save_path = os.path.join(os.getcwd(), f"page_{ui.page() + 1}", file_name)
            else:
                save_path = os.getcwd()
            path = ui.run_function(int(key) - 1, save_path, file_name)
            if file_name is not None:
                sql.insert_file_path(path)
                try:
                    last_file = sql.select_latest_data()[1]
                except Exception as e:
                    last_file = None
                ui.show(last_file)
                ui.finish_function()