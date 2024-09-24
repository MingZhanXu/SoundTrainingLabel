import os
import traceback
from wcwidth import wcswidth
import msvcrt
import inspect

# Error type
class PageInfoError(Exception):
    def __init__(self, message):
        super().__init__(message)
        stack = traceback.extract_stack()[:-1]  # 捕捉整個堆疊
        self.stack = stack
    def __str__(self):
        stack = self.stack[0]
        stack_info = f"\n File: \"{stack.filename}\", line {stack.lineno}"
        return f"PageInfoError: {super().__str__()} {stack_info}"
class UIError(Exception):
    def __init__(self, message):
        super().__init__(message)
        stack = traceback.extract_stack()[:-1]  # 捕捉整個堆疊
        self.stack = stack
    def __str__(self):
        stack = self.stack[0]
        stack_info = f"\n File: \"{stack.filename}\", line {stack.lineno}"
        return f"UIError: {super().__str__()} {stack_info}"
    
class PageInfo:
    def __init__(self, page_type: list[str], page_name: list[list[str]], start_index=1):
        self.__type = page_type
        self.__name = page_name
        self.__page = 0
        self.check_input_data_formation(file_type, file_name)
        self.__max_page = len(file_name)
        self.__max_index = 10 - start_index
        self.init_name()
    # getter
    def type(self):
        return self.__type[self.page()]
    def names(self):
        return self.__name[self.page()]
    def page(self):
        return self.__page
    def max_page(self):
        return self.__max_page
    def max_index(self):
        return self.__max_index
    
    # initialization
    def check_input_data_formation(self, file_type, file_name):
        type_len = len(file_type)
        name_len = len(file_name)
        if name_len > type_len:
            raise PageInfoError("name_len is greater than type_len, both lengths must be equal")
        elif type_len > name_len:
            raise PageInfoError("type_len is greater than name_len, both lengths must be equal")
        for i, page_name in enumerate(file_name):
            if not isinstance(page_name, (tuple, list)):
                raise PageInfoError(f"file_name[{i}] type is {type(file_name[i])}, type must tuple or list")

    def init_name(self):
        for i, page_name in enumerate(self.__name):
            page_name_len = len(page_name)
            if page_name_len < self.max_index():
                for _ in range(self.max_index() - page_name_len):
                    page_name.append(None)
                self.__name[i] = page_name
    
    def next_page(self):
        self.__page = (self.__page + 1) % self.max_page()
    def previous_page(self):
        self.__page = (self.__page + self.__max_page - 1) % self.max_page()

class Status:
    def __init__(self, running: str, finish: str):
        self.__running = running
        self.__finish = finish
    def running(self):
        return self.__running
    def finish(self):
        return self.__finish

def null_function():
    # This function is intentionally left empty as a placeholder for default behavior.
    pass
class UIFunction(Status):
    def __init__(self,title= "null", running= "running",  finish= "finish", function=null_function):
        super().__init__(running, finish)
        self.__title = title
        self.__function = function
    def title(self):
        return self.__title
    def run(self, *args, **kwargs):
        # 檢查 __function 是否接受傳遞的 *args 和 **kwargs
        sig = inspect.signature(self.__function)
        try:
            sig.bind(*args, **kwargs)
        except TypeError as e:
            func_name = self.__function.__name__
            func_signature = str(sig)
            raise TypeError(f"__function '{func_name}' don't agree with the provided arguments: {e}. It accepts: {func_signature}") from None
        self.__function(*args, **kwargs)

class UI(PageInfo):
    def __init__(self, file_type, file_name, function: list[UIFunction], start_index=1):
        super().__init__(file_type, file_name, start_index)
        if len(file_name) != len(function):
            raise UIError("The length of file_name and function must be equal")
        self.__no_none_name = [list(filter(None, names)) for names in file_name]
        self.__function = function
        # set ui message
        self.__title = "|\t\t\t      | [ESC] 結束程式\t\t  |\n|   第%s頁\t\t      | [D] 刪除最後一筆\t  |"
        self.__info = "| * [%s]  %s %s|  目前有 %10s 筆資料 |"
        self.__divider = "|-----------------------------|---------------------------|"
        self.__up_divider = "|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|" 
        self.__down_divider = "|_________________________________________________________|"
        self.__page_key = "|    上一頁 [P]\t\t   %3s/%-3s\t\t[N] 下一頁|"
        self.__null_index = "{no}"
        self.__last_file = "     最後一筆: %s"
        self.__no_sql_data = "無資料"
        # set warring message
        self.__warring = "警告: %s"
        self.__no_index = "無此選項"
        self.__no_function_key = "無此功能鍵"
        # set status message
        self.__running = "運行中: %s..."
        self.__finish = "運行完成: %s"
        self.__end = "\n|\t\t\t  結束運行\t\t\t  |\n"
        self.__end = "\n" + self.__up_divider + self.__end + self.__down_divider
        # set print error message
        self.__no_index = self.__warring % self.__no_index
        self.__no_function_key = self.__warring % self.__no_function_key

    def reset_ui_message(self, title, info, divider, page_key, null_index, last_file):
        self.__title = title
        self.__info = info
        self.__divider = divider
        self.__page_key = page_key
        self.__null_index = null_index
        self.__last_file = last_file

    def reset_error_message(self, warring, no_index, no_function_key):
        self.__warring = warring
        self.__no_index = no_index
        self.__no_function_key = no_function_key

        self.__no_index = self.__error % self.__no_index
        self.__no_function_key = self.__error % self.__no_function_key

    def reset_status_message(self, end):
        self.__end = end
    def reset_print_error_message(self, no_index, no_function_key):
        self.__no_index = no_index
        self.__no_function_key = no_function_key
        self.__no_index = self.__error % self.__no_index
        self.__no_function_key = self.__error % self.__no_function_key

    def print_flush(self, *args, **kwargs):
        print(*args, **kwargs, flush=True)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def show_info(self, last_file=None):
        page = self.page()
        self.print_flush(self.__up_divider)
        self.print_flush(self.__title % (page + 1))
        self.print_flush(self.__divider)
        func_type = self.__function[page].title()
        for index, name in enumerate(self.names()):
            if name is None:
                name = self.__null_index
            padding = 12 - wcswidth(name)
            name = name +  ' ' * padding
            padding = 8 - wcswidth(func_type)
            func_type = func_type + ' ' * padding
            self.print_flush(self.__info % (index + 1, func_type, name, 0))
        self.print_flush(self.__divider)
        self.print_flush(self.__page_key % (page + 1, self.max_page()))
        self.print_flush(self.__down_divider)
        if last_file is None:
            self.print_flush(self.__last_file % self.__no_sql_data)
        else:
            self.print_flush(self.__last_file % last_file)

    def show(self):
        self.clear_screen()
        self.show_info()
    def exit(self):
        self.print_flush(self.__end)
    def run_function(self, index, *args, **kwargs):
        running = self.__function[self.page()].running()
        finish = self.__function[self.page()].finish()
        if index > len(self.__no_none_name[self.page()]) - 1:
            self.print_flush(self.__no_index, end="")
            return None
        self.print_flush(self.__running % running, end="")
        self.__function[self.page()].run(*args, **kwargs)
        self.print_flush("\r", end="")
        self.print_flush(self.__finish % finish, end="")
        
def get_key():
        try:
            key = msvcrt.getch().decode('utf-8')
            return key
        except UnicodeDecodeError:
            return None
        
if __name__ == "__main__":
    # error test
    try:
        file_type = ["mp4"]
        file_name = [
            ["up", "down", "left", "right", "start", "rotation", "stop"],
            ["上", "下", "左", "右", "開始", "旋轉", "停止"],
            ]
        error_file_info = PageInfo(file_type, file_name)
    except Exception as e:
        print(e)

    file_type = ["mp4", "mp4"]
    file_name = [
        ["up", "down", "left", "right", "start", "rotation", "stop"],
        ["上", "下", "左", "右", "開始", "旋轉", "停止"],
        ]
    ui_function = [
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢"),
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢"),
        # UIFunction(title="錄製", running="錄音中", finish="錄音完畢"),
    ]
    ui = UI(file_type, file_name, ui_function)
    ui.show()
    while True:
        key = get_key()
        if key is None:
            continue
        if key == "p":
            ui.previous_page()
            ui.show()
        elif key == "n":
            ui.next_page()
            ui.show()
        elif key == "\x1b":
            ui.exit()
            break
        elif key > "0" and key <= "9":
            ui.show()
            ui.run_function(int(key) - 1)
