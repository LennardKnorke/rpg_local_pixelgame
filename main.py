import pygame, os, json, ctypes
from config_func import read_options, write_options

file_list = list(os.listdir())
if "options.json" in file_list:
    local_config = read_options()
else:
    local_config = write_options()
WINDOW = pygame.display.set_mode((local_config["Screen_Width"],local_config["Screen_Height"]))
#Find or create setting File
#Load GameWindow
#Find Profiles or create new Profile
#Main Menu
#   Play
#       Create
#           Find all Available levels
#               Start Server
#       Join
#           Input host adress
#       (Connect clients)
#   Options
#       Grafik
#       Control
#   Manage Profiles
#Run Game info on server, receive input and coordinate player and npc actions on the server
#
#Return updated information to players and 
#
#Adapt game stats based on player numbers 1-4
#
#During Game Menu