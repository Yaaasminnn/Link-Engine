from utils.json_utils import load_json, update_json
import os

#starting backdrop coords
backdrop_coords = [0,0]

#KEYBINDS
#print(os.curdir, os.getcwd())
keybinds = load_json("./map_maker/keybinds.json"); keybinds = keybinds["keybinds"]

exit = keybinds["exit"]