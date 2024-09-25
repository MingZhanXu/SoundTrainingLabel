import inspect

from ui_type import Status

def null_function(*args, **kwargs):
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
        result = self.__function(*args, **kwargs)
        return result
