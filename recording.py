import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
import msvcrt

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

class Recorder:
    def __init__(self, sample_rate=22050, duration=1, file_name=FILE_NAME):
        # Define constants
        self.sample_rate = sample_rate
        self.duration = duration
        # set out msg str
        self.set_out_msg_str()
        # list[page][0~9]
        self.file_name = file_name
        # check file name is correct format
        if self.check_file_name() == False:
            self.print_flush(ERROR_FILE_NAME_STR)
            exit()
        self.reset()

    def set_out_msg_str(self):
        self.page_str = PAGE_STR
        self.info_str = INFO_STR
        self.divider = DIVIDER
        self.function_key_str = FUNCTION_KEY_STR
        self.error_str = ERROR_STR
        self.running_str = RUNNING_STR
        self.index_error_str = INDEX_ERROR_STR
        self.finish_str = FINISH_STR
        self.end_str = END_STR
        self.no_function_str = NO_FUNCTION_STR
        self.no_index_show_str = NO_INDEX_SHOW_STR
        self.error_file_name_str = ERROR_FILE_NAME_STR

    # fast print
    def print_flush(self, *args, **kwargs):
        print(*args, **kwargs, flush=True)

    # check file_name is correct format
    def check_file_name(self):
        for page in self.file_name:
            if len(page) > 10:
                self.print_flush(self.error_file_name_str)
                return False
        return True
    
    # get file count
    def file_count(self, directory):
        return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    
    # reset file count
    def rest_file_count(self):
        self.file_data = dict()
        for i, page in enumerate(self.file_name):
            for file in page:
                directory = f"page{i + 1}/{file}"
                if not os.path.exists(directory):
                    os.makedirs(name=directory)
                self.file_data[file] = self.file_count(directory)

    # reset print name
    def rest_print_name(self):
        self.print_file_name = list()
        max_len = max([len(name.encode('utf-8')) for page in self.file_name for name in page])
        for i, page in enumerate(self.file_name):
            self.print_file_name.append([])
            for name in page:
                name_len = len(name.encode('utf-8'))
                add_tab_count = (max_len - name_len - 1) // 4
                add_tab = "\t" * add_tab_count
                self.print_file_name[i].append(f"{name}{add_tab}")

    # reset file count and print name
    def reset(self):
        try:
            self.page = 0
            self.rest_file_count()
            self.rest_print_name()
        except Exception as e:
            self.print_flush(self.error_str % e)
            exit()
    
    # print data information
    def print_info(self):
        page = self.page
        self.print_flush(self.page_str % (page + 1))
        self.print_flush(self.divider)
        page_file_name = self.file_name[page]
        total_page = len(self.file_name)
        for i, v in enumerate(page_file_name):
            pv = self.print_file_name[page][i]
            self.print_flush(self.info_str % (i, pv, self.file_data[v]))
        file_len = len(page_file_name)
        for i in range(10 - file_len):
            self.print_flush(self.info_str % (i + file_len, self.no_index_show_str, "0"))
        self.print_flush(self.divider)
        self.print_flush(self.function_key_str % (page + 1, total_page))

    # clear screen
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # print screen message
    def print_msg(self):
        self.clear_screen()
        self.print_info()

    # get key
    def get_key(self):
        try:
            key = msvcrt.getch().decode('utf-8')
            return key
        except UnicodeDecodeError:
            return None
        
    # record audio
    def record_audio(self, save_path, file_name, seq):
        self.print_flush("\r\033[K", end="")
        self.print_flush(self.running_str % (file_name, seq), end="\t")
        audio_data = sd.rec(int(self.sample_rate * self.duration), samplerate=self.sample_rate, channels=1, dtype=np.int16)
        sd.wait()
        file_path = os.path.join(save_path, f"{file_name}{seq}.wav")
        write(file_path, self.sample_rate, audio_data)
        
if __name__ == "__main__":
    record = Recorder()
    record.print_msg()
    while True:
        key = record.get_key()
        if key == 'n':
            record.page = (record.page + 1) % len(record.file_name)
            record.print_msg()
        elif key == 'p':
            record.page = (record.page + len(record.file_name) - 1) % len(record.file_name)
            record.print_msg()
        elif key == '\x1b':  # ESC key
            record.print_flush(record.end_str)
            break
        elif key >= "0" and key <= "9":
            index = int(key) - int("0")
            if index > len(record.file_name[record.page]) - 1:
                record.print_msg()
                record.print_flush(record.index_error_str, end="")
            else:
                seq = record.file_data[record.file_name[record.page][index]]
                file_name = record.file_name[record.page][index]
                save_path = f"page{record.page + 1}/{file_name}"
                record.record_audio(save_path, file_name, seq)
                record.file_data[record.file_name[record.page][index]] += 1
                record.print_msg()
                record.print_flush(record.finish_str, end="")
        else:
            record.print_msg()
            record.print_flush(record.no_function_str, end="")