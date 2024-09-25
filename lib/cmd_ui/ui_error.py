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