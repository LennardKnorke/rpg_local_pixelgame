import os
import json
import ctypes
import socket


def read_options():
    return json.load(open('options.json', 'r'))



def get_monitor_specs():
    tmp = ctypes.windll.user32
    screen_size = (tmp.GetSystemMetrics(0), tmp.GetSystemMetrics(1))
    return screen_size
