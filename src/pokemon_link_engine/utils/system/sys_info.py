from screeninfo import get_monitors
import ctypes #refresh rate

def get_primary_display():
    for monitor in get_monitors():
        if monitor.is_primary: return monitor

monitor = get_primary_display()

sc_w = monitor.width
sc_h = monitor.height
mid_x,mid_y = sc_w/2, sc_h/2

FPS = 75
TARGET_FPS = 75