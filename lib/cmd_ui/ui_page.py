from wcwidth import wcswidth

from .ui_error import PageInfoError
from .ui_tool import print_flush

class PageInfo:
    def __init__(self, page_name: list[list[str]], start_index=1):
        self.__name = page_name
        self.__page = 0
        self.check_input_data_formation(page_name)
        self.__max_page = len(page_name)
        self.__max_index = 10 - start_index
        self.init_name()
    def names(self):
        return self.__name[self.page()]
    def page(self):
        return self.__page
    def max_page(self):
        return self.__max_page
    def page_info(self):
        return self.page(), self.max_page()
    def max_index(self):
        return self.__max_index
    
    # initialization
    def check_input_data_formation(self, page_name):
        for i, page_name in enumerate(page_name):
            if not isinstance(page_name, (tuple, list)):
                raise PageInfoError(f"page_name[{i}] type is {type(page_name[i])}, type must tuple or list")

    def init_name(self):
        for i, page_name in enumerate(self.__name):
            page_name_len = len(page_name)
            if page_name_len < self.max_index():
                for _ in range(self.max_index() - page_name_len):
                    page_name.append(None)
                self.__name[i] = page_name
    
    def next_page(self):
        self.__page = (self.page() + 1) % self.max_page()
    def previous_page(self):
        self.__page = (self.page() + self.max_page() - 1) % self.max_page()

class UIPage():
    def __init__(self):
        # set ui message
        self.__title = "│\t\t\t      │ [ESC] 結束程式\t\t  │\n│   第%s頁\t\t      │ [D] 刪除最後一筆\t  │"
        self.__info = "│ * [%s]  %s %s│  目前有 %10s 筆資料 │"
        self.__divider = "┌─────────────────────────────┼───────────────────────────┐"
        self.__up_divider = "├─────────────────────────────────────────────────────────┤" 
        self.__down_divider = "└─────────────────────────────────────────────────────────┘"
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
    ###########################################################################################################################
    #reset var#################################################################################################################
    ###########################################################################################################################
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

    ###########################################################################################################################
    ###########################################################################################################################
    
    ###########################################################################################################################
    def show_page(self, names, func_type, page_info, last_file, file_sequence):
        page, max_page = page_info
        print_flush(self.__up_divider)
        print_flush(self.__title % (page + 1))
        print_flush(self.__divider)
        padding = 8 - wcswidth(func_type)
        func_type = func_type + ' ' * padding
        file_sequence_len = 0
        if file_sequence is not None:
            file_sequence_len = len(file_sequence)
        for index, name in enumerate(names):
            if name is None:
                name = self.__null_index
            padding = 12 - wcswidth(name)
            name = name +  ' ' * padding
            sequence = 0
            if file_sequence_len > index:
                sequence = file_sequence[index]
            print_flush(self.__info % (index + 1, func_type, name, sequence))
        print_flush(self.__divider)
        print_flush(self.__page_key % (page + 1, max_page))
        print_flush(self.__down_divider)
        if last_file is None:
            print_flush(self.__last_file % self.__no_sql_data)
        else:
            print_flush(self.__last_file % last_file)
    def finish_function(self, finish):
        print_flush("\r", end="")
        print_flush(self.__finish % finish, end="")
    def exit(self):
        print_flush(self.__end)
    def run_function(self, running):
        print_flush(self.__running % running, end="")
    def no_index(self):
        print_flush(self.__no_index, end="")

