import traceback
from ui_tool import get_key, clear_screen, print_flush
from ui_error import UIError
from ui_type import ArgsKwargs, Status
from ui_page import PageInfo, UIPage
from ui_function import UIFunction

class UI(PageInfo, UIPage):
    def __init__(self, page_name, function: list[UIFunction], status_function: list[UIFunction|None], start_index=1):
        PageInfo.__init__(self, page_name, start_index)
        UIPage.__init__(self)
        if len(page_name) != len(function):
            raise UIError("The length of file_name and function must be equal")
        self.__no_none_name = [list(filter(None, names)) for names in page_name]
        self.__function = function
        self.__status_function = status_function
    
    def show(self, last_file=None):
        clear_screen()
        self.show_info(last_file)
    def show_info(self, last_file=None):
        func_type = self.__function[self.page()].title()
        super().show_page(self.names(), func_type, self.page_info(), last_file)
    def finish_function(self):
        finish = self.__function[self.page()].finish()
        super().finish_function(self, finish)

    def run_function(self, index, arg_kwargs: ArgsKwargs):
        running = self.__function[self.page()].title()
        if index > len(self.__no_none_name[self.page()]) - 1:
            super().no_index()
            return None
        super().run_function(running)
        args = arg_kwargs.args()
        kwargs = arg_kwargs.kwargs()
        result = self.__function[self.page()].run(*args, **kwargs)
        
        return result
    
    def next_page(self, last_fie=None, args_kwargs = list[ArgsKwargs]):
        super().next_page()
        self.show(last_fie)
        self.change_status(args_kwargs)

    def previous_page(self, last_file=None, args_kwargs = list[ArgsKwargs]):
        super().previous_page()
        self.show(last_file)
        self.change_status(args_kwargs)
    
    def start(self, args_kwargs: list[list[ArgsKwargs]], last_file=None):
        self.show(last_file)
        self.change_status(args_kwargs)

    def change_status(self, args_kwargs = list[list[ArgsKwargs]]):
        for page in range(self.max_page()):
            __args_kwargs = args_kwargs[page]
            if page == self.page():
                self.__status_function[page].running(__args_kwargs[0])
            else:
                self.__status_function[page].finish(__args_kwargs[1])

    def stop_status(self, args_kwargs = list[ArgsKwargs]):
        for page in range(self.max_page()):
            args = args_kwargs[page].args()
            kwargs = args_kwargs[page].kwargs()
            self.__status_function[page][1](*args, **kwargs)



def print_i(i):
    for i in range(i):
        print(i)
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

    file_name = [
        ["up", "down", "left", "right", "start", "rotation", "stop"],
        ["上", "下", "左", "右", "開始", "旋轉", "停止"],
        ]
    ui_function = [
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=print_i),
        UIFunction(title="錄製", running="錄音中", finish="錄音完畢", function=print_i),
        # UIFunction(title="錄製", running="錄音中", finish="錄音完畢"),
    ]
    status_function = [
        Status(print, print),
        Status(print, print)
    ]
    ui = UI(file_name, ui_function, status_function)
    ui.show()
    status = [
        [ArgsKwargs(1, 2), ArgsKwargs(3, 4)],
        [ArgsKwargs(5, 6), ArgsKwargs(7, 8)]
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
            args_kwargs = ArgsKwargs(int(key))
            ui.run_function(int(key) - 1, args_kwargs)
