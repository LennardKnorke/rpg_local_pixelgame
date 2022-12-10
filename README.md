# rpg_local_pixelgame
In this pixelated adventure, players shall be able to play together levels with each other, level up and fight monsters. This is a learning project.

So a few notes on general structure
Main Folder
  main.py             main script combines all the others
  config_func.py      contains function for finding and regulating settings/ setting music
  game_classes.py     contains game classes
  server.py           server on which the state information of the game are running
  
  vsmaps.json         saves information about each vs level
  weapon_config.json  contains all informations about current weapons
  options.json        saves user settings and the currently chosen profile
  
  /Audio              not organized. supposed to contain all the necessary audio files
  /Profiles         
    Lennard.json      saves player level, weapons in inventory, current ingame level
  /Sprites            png for the game
    /adventure        shall contain for each level a folder with the necessary pngs in it
    /Player           player sprites
    /weapons
    /enemies
    /menu
    /vsmaps
