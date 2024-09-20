import sounddevice as sd
import numpy as np
import os
from scipy.io.wavfile import write
import msvcrt

FILE_NAME = [
    ["up", "down", "left", "right", "start", "rotation", "stop"],
    ["上", "下", "左", "右", "開始", "旋轉", "停止"],
    ]

class PrintStyle:
    def __init__(self):
        # set ui msg
        self.title = "   第%s頁\t\t\t[ESC] 結束錄音"
        self.info = " * [%s]  錄製 %s\t目前有 %5s \t筆資料"
        self.divider = "--------------------------------------------------------"
        self.page_key = "上一頁 [P]\t\t%s/%s\t\t[N] 下一頁"
        self.no_index = "{無}"
        # set error msg
        self.error = "錯誤: %s"
        self.index_error = "無此選項"
        self.no_function_key = "無此功能鍵"
        self.error_file_name = "檔案名稱不符合格式"
        # set status msg
        self.running = "錄音中: %s%s.wav..."
        self.finish = "錄音完成"
        self.end = "結束錄音"
        # set print error msg
        self.index_error = self.error % self.index_error
        self.no_function_key = self.error % self.no_function_key
        self.error_file_name = self.error % self.error_file_name
    # reset ui msg
    def set_ui_msg(self, title, info, divider, page_key, no_index):
        self.title = title
        self.info = info
        self.divider = divider
        self.page_key = page_key
        self.no_index = no_index
    # reset error msg
    def set_error_msg(self, error, index_error, no_function_key, error_file_name):
        self.error = error
        self.index_error = index_error
        self.no_function_key = no_function_key
        self.error_file_name = error_file_name
    # reset status msg
    def set_status_msg(self, running, finish, end):
        self.running = running
        self.finish = finish
        self.end = end

class Recorder(PrintStyle):
    def __init__(self, sample_rate=22050, duration=1, file_name=FILE_NAME):
        super().__init__()
        # Define constants
        self.sample_rate = sample_rate
        self.duration = duration
        # list[page][0~9]
        self.file_name = file_name
        self.total_page = len(file_name)
        # check file name is correct format
        if self.check_file_name_format() == False:
            self.print_flush(self.style.error_file_name)
            exit()
        self.reset()

    ############################################################################################################
    # user interface
    ############################################################################################################
    # fast print
    def print_flush(self, *args, **kwargs):
        print(*args, **kwargs, flush=True)
    
    # get key
    def get_key(self):
        try:
            key = msvcrt.getch().decode('utf-8')
            return key
        except UnicodeDecodeError:
            return None
        
    # check file_name is correct format
    def check_file_name_format(self):
        for page in self.file_name:
            if len(page) > 10:
                return False
        return True
    
    # get file count
    def file_count(self, directory):
        return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    
    # record audio
    def record_audio(self, save_path, file_name, seq):
        self.print_flush("\r\033[K", end="")
        self.print_flush(self.running % (file_name, seq), end="\t")
        audio_data = sd.rec(int(self.sample_rate * self.duration), samplerate=self.sample_rate, channels=1, dtype=np.int16)
        sd.wait()
        file_path = os.path.join(save_path, f"{file_name}{seq}.wav")
        write(file_path, self.sample_rate, audio_data)
    
    # add file count
    def add_file_count(self, index):
        self.file_data[self.file_name[self.page][index]] += 1
    ############################################################################################################
    # reset
    ############################################################################################################
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
        self.page_file_name = list()
        max_len = max([len(name.encode('utf-8')) for page in self.file_name for name in page])
        for i, page in enumerate(self.file_name):
            self.page_file_name.append([])
            for name in page:
                name_len = len(name.encode('utf-8'))
                add_tab_count = (max_len - name_len - 1) // 4
                add_tab = "\t" * add_tab_count
                self.page_file_name[i].append(f"{name}{add_tab}")

    # reset file count and print name
    def reset(self):
        try:
            self.page = 0
            self.rest_file_count()
            self.rest_print_name()
        except Exception as e:
            self.print_flush(self.error % e)
            exit()
    ############################################################################################################
    ############################################################################################################
    
    ############################################################################################################
    # user interface
    ############################################################################################################
    # print data information
    def print_info(self):
        page = self.page
        # page is 0 to pages - 1 so add 1
        self.print_flush(self.title % (page + 1))
        self.print_flush(self.divider)
        for i in range(10):
            if i < len(self.file_name[page]):
                self.print_flush(self.info % (i, self.page_file_name[page][i], self.file_data[self.file_name[page][i]]))
            else:
                self.print_flush(self.info % (i, self.no_index, "0"))
        self.print_flush(self.divider)
        self.print_flush(self.page_key % (page + 1, self.total_page))

    # clear screen
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # print screen message
    def print_msg(self):
        self.clear_screen()
        self.print_info()
    ############################################################################################################
    ############################################################################################################

    ############################################################################################################
    # function key
    ############################################################################################################
    def next_page(self):
        self.page = (self.page + 1) % len(self.file_name)
        self.print_msg()

    def previous_page(self):
        self.page = (self.page + len(self.file_name) - 1) % len(self.file_name)
        self.print_msg()
    
    def exit(self):
        self.print_flush(self.end)
    ############################################################################################################
    ############################################################################################################

        
if __name__ == "__main__":
    record = Recorder()
    record.print_msg()
    while True:
        key = record.get_key()
        if key == 'n':
            record.next_page()
        elif key == 'p':
            record.previous_page()
        elif key == '\x1b':  # ESC key
            record.exit()
            break
        elif key >= "0" and key <= "9":
            index = int(key) - int("0")
            if index > len(record.file_name[record.page]) - 1:
                record.print_msg()
                record.print_flush(record.index_error, end="")
            else:
                # set file information
                seq = record.file_data[record.file_name[record.page][index]]
                file_name = record.file_name[record.page][index]
                save_path = f"page{record.page + 1}/{file_name}"
                # record audio
                record.record_audio(save_path, file_name, seq)
                record.add_file_count(index)
                record.print_msg()
                record.print_flush(record.finish, end="")
        else:
            record.print_msg()
            record.print_flush(record.no_function_key, end="")