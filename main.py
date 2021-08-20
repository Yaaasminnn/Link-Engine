import time
from utils.json_utils import load_json
from graphics.maps.scripts.load_maps import load_map_data, load_tiles, is_at_gate
from graphics.sprites.Sprites.Sprites import Window, Static_Sprite
from audio import dialogue_sys
from utils.pygame_utils import *
from mechanics.load_userdata import User_Config     #gets the user info specific to the specific account/player
from utils.system.sys_info import *

#GLOBAL VARIABLES======================================================================================================#
user = User_Config("loona")
#FPS AND ANIMATIONS
prev_time = time.time() #for limiting fps. remove
counter_limit = int((FPS/1.875)/user.base_speed) #how many frames an animation period is. based on the current fps and base_speed. debatable where this will be stored
conversation = load_json("./audio/conversation.json"); conversation = conversation["conversation"] #loads in the convo


#loads up a window=====================================================================================================#
window = create_window(sc_w, sc_h, resizable=True, icon="Dump stuff/server-icon.jpg", caption="Pokemon Link Engine")

text_x, text_y = 10,10 #make these diff depending on which text. each text will have locations to load em from a json config

#Sprites and map-specific data=========================================================================================#
#Sprite Groups
player_group = pygame.sprite.Group() #player sprite and player stuff
background_group = pygame.sprite.Group() #background group
obstacle_group = pygame.sprite.Group() #obstacle groups
npc_group = pygame.sprite.Group() #npc and moving obstacle group
passthrough_group = pygame.sprite.Group() #all tiles that can be passed through
gate_group = pygame.sprite.Group() #gates group

#Loads the map metadata
map = load_map_data("twinleaf") #loads the map data
name = map["name"] #map name
gate = map["gates"]["gate 1"] #gate we initially draw the player at.(ofc the player may load elsewhere)
gates = map["gates"] #loads in all the gates
backdrop_x = gate["bg coords"]["x"] # for now, loads the backdrop around the gate
backdrop_y = gate["bg coords"]["y"]


#GATES
"""
loads all gates in
"""
gate_group = load_tiles((backdrop_x, backdrop_y), gate_group, gates, id=True)
#print(gate_group)

#PLAYER
"""
todo: allow for gendered avatars ina  config file
"""
player_group = load_tiles((960,540), player_group, group_animated=True, is_player=True)

#BACKDROP
"""
backdrop is loaded in based on gate coordinates. player is always loaded in the middle of the screen
"""
backdrop = Static_Sprite(backdrop_x, backdrop_y, map["image"])
background_group.add(backdrop)


"""
OTHER TILE GROUPS.

Reads the data from the metadata file and loads in each group.
"""
#NPC'S
NPCs = map["NPC's"]
npc_group = load_tiles((backdrop_x, backdrop_y), npc_group, NPCs, group_animated=True)

#TILES
obstacles = map["Obstacles"]
obstacle_group = load_tiles((backdrop_x, backdrop_y), obstacle_group, obstacles)

#Main Game loop========================================================================================================#

Game_Running = True #so long as the application is running
Intro = False #the intro screen
Main_Menu = False #menu outside of the game. aka, choosing which save file, settings etc
In_Game = True #in the main game
Game_Menu = False #game menu if it will be fullscreen. not finalized
Dialogue = True

frame_counter = 0 #keeps track of the frames. used for sprite animations
map_change_init = 0 #time when the map is changed. used for time delays between map changes.
prev = 0 #previous time. called when
pid = os.getpid() #gets the process id of main so we can monitor its resource usage (RAM, CPU usage etc)
while True:
    exit_conditions(user.exit)

    Window.draw_to_screen() #draws all sprite groups to the screen

    inputs = Window.get_inputs() #gets inputs
    x, y = inputs[0], inputs[1]

    user.draw_hud = Window.toggle_hud() #hud

    now = time.time() #sets the current time

    new_map = is_at_gate(now, map_change_init) #checks if at gate

    #if at a gate, it changes the map. also sets an init time
    if new_map is not None: name = new_map; map_change_init = time.time()

    dialogue_sys.show_lines() #draws dialogue

    Window.update_screen(x, y) #updates the screen

    dialogue_sys.clear_lines() #clears the dialogue

    #fps incrementer. this helps with things that arent meant to be updated every frame
    frame_counter+=1
    if frame_counter == 75: frame_counter=0

