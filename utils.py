import ctypes


def get_screen_size():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0) , user32.GetSystemMetrics(1)
    return screensize
