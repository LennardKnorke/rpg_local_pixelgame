# rpg_local_pixelgame
In this pixelated adventure, players shall be able to play together levels with each other in a local network, level up and fight monsters. This is a learning project.
Aims:
- Lern Github
- Game development in Python :))))))
  - Singleplayer/ Coop Campaign
- Networks
- (Random Level Generation?)

So a few notes on general structure
Main Folder
  main.py             main script combines all the others
  config_func.py      contains function for finding and regulating settings/ setting music
  game_classes.py     contains game classes
  server.py           server on which the state information of the game are running
  
  weapon_config.json  contains all informations about current weapons
  /Audio              not organized. supposed to contain all the necessary audio files
  /Sprites            png for the game
    /adventure        shall contain for each level a folder with the necessary pngs in it
    /Player           player sprites
    /weapons
    /enemies
    /menu

General Notes:
- Game engine runs in pygame. Avoid (python) for loop to examine sprite interaction
- to do: reading user input using pygame, translate (as string?) to send into network and convert back so the server can make adjustments
- Game play features (up to change):
    - 2d sidescroller
    - since there is no artistic talent in the group the enemies and player sprites will be cleverly merged to compensate for missing artists in our rows
    - per finished level distribute a skill point after each level.
    - variation comes through leveling and weapons
    - the question. restart on every death? like "enter the gungeon", "castlevania" or a saving everything? 
      I would almost dismiss every progress on death and only save the max level players have reached.
    - Every environment "type" (a forrest, city, space?) will contian 2-4 levels
      - Small boss after each environmental type (rewarding maybe more skillpoints)
      - a "PVP map is unlocked for that environment
      - Random generated level? :P
    - 3-5 different environment types and bosses before a final boss
    - Stop it Lennard. Enough ideas for this part.
- Crucial problem. Keep it adaptable so that new ideas can  be integrated or changed without disrupting the workflow again
