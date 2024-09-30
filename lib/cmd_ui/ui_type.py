# 傳遞多個參數的類別
class ArgsKwargs:
    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
    def args(self):
        return self.__args
    def kwargs(self):
        return self.__kwargs
# 上下頁狀態切換
class Status:
    def __init__(self, running=None, finish=None):
        self.__running = running
        self.__finish = finish
    def running(self, args_kwargs: ArgsKwargs|None):
        if self.__running is None:
            return None
        if args_kwargs is None:
            return self.__running()
        args = args_kwargs.args()
        kwargs = args_kwargs.kwargs()
        result = self.__running(*args, **kwargs)
        return result
    def finish(self, args_kwargs: ArgsKwargs|None):
        if self.__finish is None:
            return None
        if args_kwargs is None:
            return self.__finish()
        args = args_kwargs.args()
        kwargs = args_kwargs.kwargs()
        result = self.__finish(*args, **kwargs)
        return result
    
# 檔案計數
class FileSequence:
    def __init__(self, last_file:str|None=None, sequence:list[list[int]]|None=None):
        self.__last_file = last_file
        self.__sequence = sequence
    def last_file(self):
        return self.__last_file
    def sequence(self, page):
        if self.__sequence is None:
            return None
        return self.__sequence[page]
    def index_sequence(self, page, index):
        sequence = self.sequence(page)
        if sequence is None:
            return -1
        if index < len(sequence):
            return sequence[index]
        return -1
    def add_file(self, path:tuple[int, int], last_file:str):
        page, index = path
        self.__sequence[page][index] += 1
        self.__last_file = last_file
    def __str__(self) -> str:
        return f"last_file: {self.__last_file}, sequence: {self.__sequence}"