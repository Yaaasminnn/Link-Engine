from utils.json_utils import load_json, update_json
import os
from utils.key_press import Key
from graphics.sprites.Sprites.Sprites import Static_Sprite
from utils.directories import get_project_dir
from utils.system.sys_info import mid_x, mid_y

get_project_dir() #might be redundant if we use file explorer

#starting backdrop coords
backdrop_coords = [0,0]

#KEYBINDS
#print(os.curdir, os.getcwd())
keybinds = load_json("./utils/map_maker/keybinds.json"); keybinds = keybinds["keybinds"]

exit = keybinds["exit"]
save = keybinds["save"]
delete = keybinds["delete"]

col_tol = 1

class gate(Static_Sprite):
    id = 0
    bg_coords = [0,0]
    coords = [0,0]
    image = "./Dump stuff/server-icon.jpg"
    num = 0

    def __init__(self, coords=None):
        """
        self.coords will be recorded in the static sprite class
        """
        if coords is None: coords = gate.coords
        gate.coords = coords
        super().__init__(pos_x=gate.coords[0], pos_y=gate.coords[1], picture_path=gate.image)
        self.id = gate.id
        self.bg_coords = [mid_x-gate.coords[0],mid_y-gate.coords[1]]
        gate.num+=1

class npc(Static_Sprite):
    ai = "static"
    coords = [0,0]
    image = "./Dump stuff/server-icon.jpg"
    num = 0

    def __init__(self, coords = None):
        if coords is None: coords = npc.coords
        npc.coords = coords
        super().__init__(pos_x=npc.coords[0], pos_y=npc.coords[1], picture_path=npc.image)
        npc.num+=1

class Obstacle(Static_Sprite):
    coords = [0,0]
    image = "./Dump stuff/server-icon.jpg"
    num = 0

    def __init__(self, coords=None):
        if coords is None: coords = Obstacle.coords
        Obstacle.coords = coords
        super().__init__(pos_x=Obstacle.coords[0], pos_y=Obstacle.coords[1], picture_path=Obstacle.image)
        Obstacle.num +=1
