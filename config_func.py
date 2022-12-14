import os
import json
import ctypes
import pygame


def read_options():
    return json.load(open('options.json', 'r'))

def valid_ip(ip):
    pass
def create_options():
    new_profile_options = {"Screen_Size": 1, "Screen_Height": 360, "Screen_Width": 640, "FPS": 30, "Jump": "w", "Left": "a", "Right": "d", "Defend": " "}
    with open("options.json", "w") as file:
        json.dumb(new_profile_options, file)
    return read_options()


def get_monitor_specs():
    tmp = ctypes.windll.user32
    screen_size = (tmp.GetSystemMetrics(0), tmp.GetSystemMetrics(1))
    return screen_size
