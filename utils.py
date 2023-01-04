import ctypes


def get_screen_size():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0) / 3*2, user32.GetSystemMetrics(1) / 3*2
    return screensize
