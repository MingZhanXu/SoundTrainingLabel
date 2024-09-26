import traceback
from .ui_tool import get_key, clear_screen, print_flush
from .ui_error import UIError
from .ui_type import ArgsKwargs, Status
from .ui_page import PageInfo, UIPage
from .ui_function import UIFunction

class UI(PageInfo, UIPage):
    def __init__(self, page_name, function: list[UIFunction], status_function: list[UIFunction|None], start_index=1):
        PageInfo.__init__(self, page_name, start_index)
        UIPage.__init__(self)
        if len(page_name) != len(function):
            message = f"The length of file_name and function must be equal, page_name: {len(page_name)}, function: {len(function)}"
            raise UIError(message)
        self.__no_none_name = [list(filter(None, names)) for names in page_name]
        self.__function = function
        self.__status_function = status_function
    
    def show(self, last_file=None):
        clear_screen()
        self.show_info(last_file)
    def show_info(self, last_file=None):
        func_type = self.__function[self.page()].title()
        super().show_page(self.names(), func_type, self.page_info(), last_file)
    def finish_function(self, index):
        finish = self.__function[self.page()].finish_title()
        if index > len(self.__no_none_name[self.page()]) - 1:
            super().no_index()
            return None
        super().finish_function(finish)

    def run_function(self, index, arg_kwargs: ArgsKwargs):
        running = self.__function[self.page()].title()
        if index > len(self.__no_none_name[self.page()]) - 1:
            super().no_index()
            return None
        super().run_function(running)
        args = arg_kwargs.args()
        kwargs = arg_kwargs.kwargs()
        func = self.__function[self.page()]
        result = func.run(*args, **kwargs)
        
        return result
    
    def next_page(self, last_fie=None, args_kwargs = list[list[ArgsKwargs|None]]):
        super().next_page()
        self.show(last_fie)
        self.change_status(args_kwargs)

    def previous_page(self, last_file=None, args_kwargs = list[list[ArgsKwargs|None]]):
        super().previous_page()
        self.show(last_file)
        self.change_status(args_kwargs)
    
    def start(self, args_kwargs: list[list[ArgsKwargs|None]], last_file=None):
        self.show(last_file)
        self.change_status(args_kwargs)

    def change_status(self, args_kwargs = list[list[ArgsKwargs|None]]):
        for page in range(self.max_page()):
            __args_kwargs = args_kwargs[page]
            if page == self.page():
                self.__status_function[page].running(__args_kwargs[0])
            else:
                self.__status_function[page].finish(__args_kwargs[1])

    def stop_status(self, args_kwargs = list[ArgsKwargs|None]):
        for page in range(self.max_page()):
            self.__status_function[page].finish(args_kwargs[page])

    def end(self, args_kwargs = list[ArgsKwargs|None]|None):
        super().exit()
        self.stop_status(args_kwargs)
        
def print_i():
    pass
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
    input("Press Enter to continue...")
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
