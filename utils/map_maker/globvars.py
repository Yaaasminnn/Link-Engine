from utils.json_utils import load_json, update_json
import os
from utils.key_press import Key
from graphics.sprites.Sprites.Sprites import Static_Sprite

#starting backdrop coords
backdrop_coords = [0,0]

#KEYBINDS
#print(os.curdir, os.getcwd())
keybinds = load_json("./map_maker/keybinds.json"); keybinds = keybinds["keybinds"]

exit = keybinds["exit"]

class gate(Static_Sprite):
    id = 0
    bg_coords = [0,0]
    coords = [0,0]
    image = "./Dump stuff/server-icon.jpg"

    def __init__(self, coords=None):
        if coords is None: coords = gate.coords
        gate.coords = coords
        super().__init__(pos_x=gate.coords[0], pos_y=gate.coords[1], picture_path=gate.image)

class npc(Static_Sprite):
    ai = "static"
    coords = [0,0]
    image = "./Dump stuff/server-icon.jpg"

    def __init__(self, coords = None):
        if coords is None: coords = npc.coords
        npc.coords = coords
        super().__init__(pos_x=npc.coords[0], pos_y=npc.coords[1], picture_path=npc.image)

class Obstacle(Static_Sprite):
    coords = [0,0]
    image = "./Dump stuff/server-icon.jpg"

    def __init__(self, coords=None):
        if coords is None: coords = Obstacle.coords
        Obstacle.coords = coords
        super().__init__(pos_x=Obstacle.coords[0], pos_y=Obstacle.coords[1], picture_path=Obstacle.image)
