import os
import msvcrt
def print_flush(*args, **kwargs):
    print(*args, **kwargs, flush=True)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def get_key():
    try:
        key = msvcrt.getch().decode('utf-8')
        return key
    except UnicodeDecodeError:
        return None