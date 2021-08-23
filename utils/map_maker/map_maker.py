"""
MAP MAKER.

todo:
    add in elements
    add em into a json
    show x,y coords from the mouse
    optimize
"""
import pygame.sprite

from utils.pygame_utils import *
from utils.directories import get_project_dir
from utils.map_maker.globvars import *
from utils.system.sys_info import sc_w, sc_h, FPS, TARGET_FPS

c= Colours
get_project_dir() #might be redundant if we use file explorer
pid = os.getpid()
default = Obstacle

tile_group = pygame.sprite.Group()

# PYGAME VARIABLES
window = create_window(sc_w,sc_h,caption="Map Maker Program")

#gets the backdrop image and sets it as the backdrop
#img = get_img() #change to a file explorer prompt
backdrop = pygame.image.load("graphics/maps/twinleaf.jpg")

def move_map():
    key = keyboard; x,y = 0,0
    if key.is_pressed("Up"): y +=((4/FPS)*TARGET_FPS)
    if key.is_pressed("Down"): y -=((4/FPS)*TARGET_FPS)
    if key.is_pressed("Right"): x -=((4/FPS)*TARGET_FPS)
    if key.is_pressed("Left"): x +=((4/FPS)*TARGET_FPS)
    return [x,y]

def change_type():
    global default
    key = keyboard
    if key.is_pressed("1"): default = Obstacle
    if key.is_pressed("2"): default = npc
    if key.is_pressed("3"): default = gate
    return default

while True:
    exit_conditions(exit) #checks for exit conditions every frame
    mouse_focused = mouse.get_focused(); key_focused = pygame.key.get_focused()
    events = pygame.event.get()

    window.blit(backdrop, backdrop_coords) #draw the backdrop to the screen
    tile_group.draw(window) #draws all tiles to the window
    show_fps(window)
    show_memory(pid, window)

    if key_focused:
        inputs = move_map(); backdrop_coords[0]+= inputs[0]; backdrop_coords[1] +=  inputs[1]

        if default == gate: render_text(f"Tile Type: gate", window, (10, 110))
        if default == Obstacle: render_text(f"Tile Type: Obstacle", window, (10, 110))
        if default == npc: render_text(f"Tile Type: npc", window, (10, 110))

        pressed = []
        for key in keybinds:
            key = keybinds[key]
            if keyboard.is_pressed(key): pressed.append(key)
        render_text(f"Keystroke: {pressed}", window, (10, 140))

    if mouse_focused: mouse_coords = mouse.get_pos(); render_text(f"Mouse: [{mouse_coords[0] - backdrop_coords[0]},{mouse_coords[1] - backdrop_coords[1]}]", window, (10, 80)) #relative to backdrop coords

    default = change_type();
    #print(default)  # changes the default type of tile we want to place
    if mouse.get_pressed(num_buttons=3)[0] is True and mouse_focused:
        if default == gate: new_tile = gate(mouse_coords)
        if default == Obstacle: new_tile = Obstacle(mouse_coords)
        if default == npc: new_tile = npc(mouse_coords)
        tile_group.add(new_tile)


    tile_group.update(inputs[0], inputs[1], True)
    pygame.display.flip() #updates display
    clock.tick(FPS) #sets the fps
    window.fill(c.black) #fills the screen with black every frame to move to the next frame
