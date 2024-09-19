import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
import msvcrt

# Define constants
SAMPLE_RATE = 22050
DURATION = 1

# list[page][0~9]
FILE_NAME = [
    ["up", "down", "left", "right", "start", "rotation", "stop"],
    ["上", "下", "左", "右", "開始", "旋轉", "停止"],
    ]
# 輸出格式
PAGE_STR = "   第%s頁\t\t\t[ESC] 結束錄音"
INFO_STR = " * [%s]  錄製 %s\t目前有 %5s \t筆資料"
DIVIDER = "--------------------------------------------------------"
FUNCTION_KEY_STR = "上一頁 [P]\t\t%s/%s\t\t[N] 下一頁"
ERROR_STR = "錯誤: %s"
RUNNING_STR = "錄音中: %s%s.wav..."
INDEX_ERROR_STR = "錯誤: 無此選項"
FINISH_STR = "錄音完成"
END_STR = "結束錄音"
NO_FUNCTION_STR = "錯誤: 無此功能鍵"
NO_INDEX_SHOW_STR = "{無}"
ERROR_FILE_NAME_STR = "錯誤: 檔案名稱不符合格式"

def print_flush(*args, **kwargs):
    print(*args, **kwargs, flush=True)

# 確認 FILE_NAME 是否符合格式
def check_file_name():
    for page in FILE_NAME:
        if len(page) > 10:
            print_flush(ERROR_FILE_NAME_STR)
            return False
    return True

# 確認 FILE_NAME 是否有錯誤
if check_file_name() == False:
    exit()

# 獲取檔案數量
def file_count(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

# 初始化檔案數量資訊
def rest_file_count():
    global file_data
    file_data = dict()
    for i, page in enumerate(FILE_NAME):
        for file in page:
            directory = f"page{i + 1}/{file}"
            if not os.path.exists(directory):
                os.makedirs(name=directory)
            file_data[file] = file_count(directory)

# 初始化輸出名稱
def rest_print_name():
    global PRINT_FILE_NAME
    PRINT_FILE_NAME = list()
    max_len = max([len(name.encode('utf-8')) for page in FILE_NAME for name in page])
    for i, page in enumerate(FILE_NAME):
        PRINT_FILE_NAME.append([])
        for name in page:
            name_len = len(name.encode('utf-8'))
            add_tab_count = (max_len - name_len - 1) // 4
            add_tab = "\t" * add_tab_count
            PRINT_FILE_NAME[i].append(f"{name}{add_tab}")

# 初始化輸出名稱
def reset():
    try:
        rest_file_count()
        rest_print_name()
    except Exception as e:
        print_flush(ERROR_STR % e)
        exit()

# 錄音
def record_audio(save_path, file_name, seq):
    print_flush("\r\033[K", end="")
    print_flush(RUNNING_STR % (file_name, seq), end="\t")
    audio_data = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    file_path = os.path.join(save_path, f"{file_name}{seq}.wav")
    write(file_path, SAMPLE_RATE, audio_data)

# 輸出資訊
def print_info(page):
    print_flush(PAGE_STR % (page + 1))
    print_flush(DIVIDER)

    page_file_name = FILE_NAME[page]
    total_page = len(FILE_NAME)
    for i, v in enumerate(page_file_name):
        pv = PRINT_FILE_NAME[page][i]
        print_flush(INFO_STR % (i, pv, file_data[v]))
    file_len = len(page_file_name)
    for i in range(10 - file_len):
        print_flush(INFO_STR % (i + file_len, NO_INDEX_SHOW_STR, "0"))
    
    print_flush(DIVIDER)
    print_flush(FUNCTION_KEY_STR % (page + 1, total_page))

# 清除畫面
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 輸出訊息
def print_msg(page):
    clear_screen()
    print_info(page)

if __name__ == "__main__":
    page = 0
    reset()
    print_msg(page)
    while True:
        try:
            key = msvcrt.getch().decode('utf-8')
        except UnicodeDecodeError:
            continue

        if key >= "0" and key <= "9":
            index = int(key) - int("0")
            if index > len(FILE_NAME[page]) - 1:
                print_msg(page)
                print_flush(INDEX_ERROR_STR, end="")
            else:
                seq = file_data[FILE_NAME[page][index]]
                file_name = FILE_NAME[page][index]
                save_path = f"page{page + 1}/{file_name}"
                record_audio(save_path, file_name, seq)
                file_data[FILE_NAME[page][index]] += 1
                print_msg(page)
                print_flush(FINISH_STR, end="")
        elif key == 'n':
            page = (page + 1) % len(FILE_NAME)
            print_msg(page)
        elif key == 'p':
            page = (page + len(FILE_NAME) - 1) % len(FILE_NAME)
            print_msg(page)
        elif key == '\x1b':  # ESC key
            print_flush(END_STR)
            break
        else:
            print_msg(page)
            print_flush(NO_FUNCTION_STR, end="")
            