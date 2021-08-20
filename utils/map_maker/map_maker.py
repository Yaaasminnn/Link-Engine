"""
MAP MAKER.

todo:
    add in elements
    add em into a json
    show x,y coords from the mouse
    optimize
"""

from utils.pygame_utils import *
from utils.directories import get_project_dir
from utils.map_maker.globvars import *

get_project_dir() #might be redundant if we use file explorer
pid = os.getpid()

# PYGAME VARIABLES
window = pygame.display.set_mode((sc_w,sc_h), pygame.RESIZABLE) #creates a window

#gets the backdrop image and sets it as the backdrop
img = get_img()
backdrop = pygame.image.load(img)

def move_map(backdrop_coords):
    #from main import base_speed
    key = keyboard
    if key.is_pressed("Up"): backdrop_coords[1] +=4
    if key.is_pressed("Down"): backdrop_coords[1] -=4
    if key.is_pressed("Right"): backdrop_coords[0] -=4
    if key.is_pressed("Left"): backdrop_coords[0] +=4
    return backdrop_coords

while True:
    exit_conditions(exit) #checks for exit conditions every frame

    window.blit(backdrop, backdrop_coords) #draw the backdrop to the screen
    show_fps(window)
    show_memory(pid, window)

    backdrop_coords = move_map(backdrop_coords); print(backdrop_coords)

    pygame.display.flip() #updates display
    clock.tick(75) #sets the fps
    window.fill((0,0,0)) #fills the screen with black every frame to move to the next frame
