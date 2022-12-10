import os
import json

def create_options():
    new_profile_options = {"Screen_Size": 1, "Screen_Height": 360, "Screen_Width": 640, "FPS": 30, "profile": "default", "Jump": "w", "Left": "a", "Right": "d", "Defend": " "}
    with open("options.json", "w") as file:
        json.dumb(new_profile_options, file)
    return json.load(open('options.json', 'r'))
def read_options():
    return json.load(open('options.json', 'r'))