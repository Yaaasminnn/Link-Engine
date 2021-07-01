import pygame
import sys
from random import randint
import time

#other scripts
from config.config import load_config
from graphics.maps.scripts.load_maps import load_map_data, load_tiles, is_at_gate
from graphics.sprites.Sprites.spritesheets import Spritesheet
from graphics.sprites.Sprites.Sprites import Animated_Sprite, Window, Static_Sprite
from mechanics.Log import log
from audio.speak import display_text
from key_press import Key

#GLOBAL VARIABLES======================================================================================================#
config = load_config() #loads the config file

#MOVEMENT
base_speed = int(config["base speed"]) #base speed is written in the config file for easy modifications from the json
run_speed = base_speed*2 #run speed is double the walk speed
col_tol = run_speed #how close(in pixels) sprites can be before being considered collided. equal to run speed

#FPS AND ANIMATIONS
prev_time = time.time()
FPS = 75  #make these vsync. watch the fps independence vid again
TARGET_FPS = 75 #fps we want
counter_limit = int((FPS/1.875)/base_speed) #how many frames an animation period is. based on the current fps and base_speed
#print(counter_limit)

#DEBUG HUD
draw_hud = config["draw HUD"] #determines if we should draw the HUD
colour = config["hitbox colours"] #colour of hitboxes
hitbox_clr = (int(colour["red"]), int(colour["green"]), int(colour["blue"]))

#KEYBINDS
keybinds = config["keybinds"] #loads the keybinds
up = keybinds["up"]
down = keybinds["down"]
left = keybinds["left"]
right = keybinds["right"]
dash = keybinds["dash"]
exit = keybinds["exit"]
debug = Key(keybinds["debug menu"])
#Macros: will be able to register items from the bag for use. AND ALSO, TO VIEW THE PC OR DAYCARE REMOTELY
macros = keybinds["macros"] #loads macro keys cuz FUCK YEAH
macro1 = macros["1"]
macro2 = macros["2"]
macro3 = macros["3"]
macro4 = macros["4"]

#GRAPHICS
animate = config["animate"]

#loads up a window=====================================================================================================#
pygame.init()
clock = pygame.time.Clock()

display = pygame.display.Info()
sc_w, sc_h = display.current_w, display.current_h
if config["fullscreen"] == 0: sc_w, sc_h =1025,760
mid_x,mid_y = sc_w/2, sc_h/2
window = pygame.display.set_mode((sc_w, sc_h),pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("Pokemon Link Engine") #caption
icon = pygame.image.load("Dump stuff/server-icon.jpg") #icon
pygame.display.set_icon(icon)

font = pygame.font.SysFont("Arial", 32)
text_x, text_y = 10,10

#Sprites and map-specific data=========================================================================================#
#Sprite Groups
player_group = pygame.sprite.Group() #player sprite and player stuff
background_group = pygame.sprite.Group() #background group
obstacle_group = pygame.sprite.Group() #obstacle groups
npc_group = pygame.sprite.Group() #npc and moving obstacle group
passthrough_group = pygame.sprite.Group() #all tiles that can be passed through
gate_group = pygame.sprite.Group()

#Loads the map metadata
map = load_map_data("twinleaf")
name = map["name"]
gate = map["gates"]["gate 1"]
backdrop_x = gate["coords"]["x"]
backdrop_y = gate["coords"]["y"]
gayte = Static_Sprite(gate["draw coords"][0]+backdrop_x, gate["draw coords"][1]+backdrop_y, "Dump stuff/server-icon.jpg")
gate_group.add(gayte)

#PLAYER
"""
todo: allow for gendered avatars and also load in players based off gates
"""
player_group = load_tiles((0,0),player_group, animated=True, is_player=True)
"""player = Animated_Sprite(mid_x, mid_y, "graphics/sprites/overworld/player movement.png")
player_group.add(player)"""

#BACKDROP
"""
todo: load in background based off gate pos

backdrop is loaded in based on gate coordinates. player is always loaded in the middle of the screen
"""
backdrop = Static_Sprite(backdrop_x, backdrop_y, map["image"])
background_group.add(backdrop)

#NPC'S
"""
Loads in all npc's.

Reads the data from the metadata file
"""
NPCs = map["NPC's"]
npc_group = load_tiles((backdrop_x, backdrop_y), npc_group, NPCs, animated=True)

#TILES
obstacles = map["Obstacles"]
obstacle_group = load_tiles((backdrop_x, backdrop_y), obstacle_group, obstacles)

#Main Game loop========================================================================================================#
frame_counter = 0
while True:
    Window.exit_conditions() #checks exit conditions

    Window.draw_to_screen() #draws all sprite groups to the screen

    inputs = Window.get_inputs() #gets inputs
    x, y = inputs[0], inputs[1]

    draw_hud = Window.toggle_hud()

    new_map = is_at_gate()

    #print(f"group:{npc_group}")
    #print(name, map)

    Window.update_screen(x,y) #updates the screen

    #fps incrementer. this helps with things that arent meant to be updated every frame
    frame_counter+=1
    if frame_counter == 75: frame_counter=0
