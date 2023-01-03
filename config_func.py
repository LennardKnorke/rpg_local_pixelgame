import os
import json
import ctypes
import socket

#search for the local ip adress. Recommend but leave it open to change in server!
def find_local_host():
    local_mashine_name = socket.gethostname()
    local_mashine_adress = socket.gethostbyname(local_mashine_name)
    return (local_mashine_adress)
    
def read_options():
    return json.load(open('options.json', 'r'))



def get_monitor_specs():
    #Problems getting screen size on different systems (linux vs windows)

    tmp = ctypes.windll.user32
    screen_size = (tmp.GetSystemMetrics(0), tmp.GetSystemMetrics(1))
    return screen_size

