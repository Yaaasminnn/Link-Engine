"""
MAP MAKER.

todo:
    add in elements
    add em into a json
    show x,y coords from the mouse
    optimize
"""
import time
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
data = load_json("utils/map_maker/data.json")
update_json(f"utils/map_maker/exports/twinleaf meta.json", data)

def move_map(invert=False):
    key = keyboard; x,y = 0,0
    if key.is_pressed("Up"): y +=((4/FPS)*TARGET_FPS)
    if key.is_pressed("Down"): y -=((4/FPS)*TARGET_FPS)
    if key.is_pressed("Right"): x -=((4/FPS)*TARGET_FPS)
    if key.is_pressed("Left"): x +=((4/FPS)*TARGET_FPS)
    if invert: x*=-1; y*=-1
    return [x,y]

def change_type():
    global default
    key = keyboard
    if key.is_pressed("1"): default = Obstacle
    if key.is_pressed("2"): default = npc
    if key.is_pressed("3"): default = gate
    return default

def add_new_tile(type, type_str, mouse_coords):
    new_tile = type(mouse_coords)
    length = len(data[f"{type_str}s"])
    data[f"{type_str}s"][f"{type_str}{length}"] = {}; tile = data[f"{type_str}s"][f"{type_str}{length}"]
    tile["image"] = str(type.image)
    tile["coords"] = {"X":new_tile.coords[0],"y":new_tile.coords[1]}

    if type == gate:
        tile["bg coords"] = {"X":new_tile.bg_coords[0], "y":new_tile.bg_coords[1]}
        tile["id"] = new_tile.id

    if type == npc:
        tile["ai"] = new_tile.ai

    return new_tile

prev_time = 0
focused = None

while True:
    mouse_focused = mouse.get_focused(); key_focused = pygame.key.get_focused()
    # events = pygame.event.get()
    window.blit(backdrop, backdrop_coords)  # draw the backdrop to the screen
    Sprite.group.draw(window, tile_group)  # draws all tiles to the window
    show_fps(window); show_memory(pid, window)

    #print(tile_group)

    if focused is not None: #If we are focusing on a sprite
        exit_conditions()  # checks for exit conditions every frame
        if key_focused:
            inputs = move_map(invert=True)
            if keyboard.is_pressed(exit): focused = None
            if keyboard.is_pressed(delete): tile_group.remove(focused); focused = None #needa remove it from the default num
            try:
                draw_hitbox(focused, window)
                colliding = Sprite.collide.with_group(focused, tile_group, return_rect=True, excluded=focused)
                if colliding is not False and colliding is not True: inputs = Sprite.func(inputs, colliding)
                focused.update(inputs[0]/4, inputs[1]/4, True)
                tile_group.update(0,0, True)
            except: pass

    if focused is None: #If we are not focusing on a sprite
        exit_conditions(exit)
        if key_focused:
             inputs = move_map()
             backdrop_coords[0]+= inputs[0]; backdrop_coords[1] +=  inputs[1]
             tile_group.update(inputs[0], inputs[1], True)



    if key_focused:
        #print(default)
        if default == gate: render_text(f"Tile Type: gate", window, (10, 110))
        if default == Obstacle: render_text(f"Tile Type: Obstacle", window, (10, 110))
        if default == npc: render_text(f"Tile Type: npc", window, (10, 110))
        render_text(f"Number of tiles: [{len(tile_group)}], [{Obstacle.num}, {npc.num}, {gate.num}]", window, (10, 170))

        #records keypresses
        pressed = []
        for key in keybinds:
            key = keybinds[key]
            if keyboard.is_pressed(key): pressed.append(key)
        render_text(f"Keystroke: {pressed}", window, (10, 140))

        #saving
        if keyboard.is_pressed(save):
            update_json(f"utils/map_maker/exports/twinleaf meta.json", data)
            print("saved!")
            render_text("Saved!", window, coords=(1830, 30))
            #init = show_text("Saved!", window, coords=(1900, 30)); now = time.time()

    #ALL HAPPENS REGARDLESS OF FOCUSED
    if mouse_focused:
        mouse_coords = mouse.get_pos()
        render_text(f"Mouse: [{mouse_coords[0] - backdrop_coords[0]},{mouse_coords[1] - backdrop_coords[1]}]", window, (10, 80)) #relative to backdrop coords

        if mouse.get_pressed(num_buttons=3)[0]:
            if default == gate: new_tile = add_new_tile(default, "gate", mouse_coords)
            if default == Obstacle: new_tile = add_new_tile(default, "Obstacle", mouse_coords)
            if default == npc: new_tile = add_new_tile(default, "NPC'", mouse_coords)

            colliding = Sprite.collide.with_group(new_tile, tile_group)
            print(colliding)
            if colliding: del new_tile; default.num -=1
            if not colliding:
                tile_group.add(new_tile)
                if focused is not None: focused = new_tile

        if mouse.get_pressed(num_buttons=3)[2]:
            selecting = Sprite.collide.group_with_point(mouse_coords, tile_group, return_sprite=True)
            if selecting is not False and selecting is not True: focused = selecting

    default = change_type()

    #tile_group.update(inputs[0], inputs[1], True)

    update_screen(window, FPS, c.black)
