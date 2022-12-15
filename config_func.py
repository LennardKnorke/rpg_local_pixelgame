import os
import json
import ctypes
import pygame
import socket


def read_options():
    return json.load(open('options.json', 'r'))

#Give an ip adress to connect to
def valid_ip(adress_port, connect_to = True):
    for idx in range(0,2):
        counter = 0
        for ch in adress_port[idx]:
            if ("0" <= ch <= "9"):
                counter += 1
                if counter > 3 and idx == 0:
                    return False
                elif counter > 4:
                    return False
            elif ch == "." and idx == 0:
              counter = 0
            else:
                return False
    #try to connect or just check ip, run and in case of failure return to main menu?
    try:
        pass
    except:
        pass
    return True


def create_options():
    new_profile_options = {"Screen_Size": 1, "Screen_Height": 360, "Screen_Width": 640, "FPS": 30, "Jump": "w", "Left": "a", "Right": "d", "Defend": " "}
    with open("options.json", "w") as file:
        json.dumb(new_profile_options, file)
    return read_options()


def get_monitor_specs():
    tmp = ctypes.windll.user32
    screen_size = (tmp.GetSystemMetrics(0), tmp.GetSystemMetrics(1))
    return screen_size


adres = ["192.168.2.199", "8888"]
adres2 = ["192.168.2.199", "8.88"]
adres3 = ["192.1682199", "8888"]

valid_ip(adres)
valid_ip(adres2)
valid_ip(adres3)

"1" < adres[0][0] 