class ArgsKwargs:
    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
    def args(self):
        return self.__args
    def kwargs(self):
        return self.__kwargs

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