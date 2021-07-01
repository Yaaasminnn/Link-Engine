import json
import time
import os


def load_map_data(map: str):
    """
    Takes in the map name, adds in " meta.json" and then returns all values we want
    :param map: the name of the map used
    :return: map data from the json
    """
    path = "./graphics/maps/"
    if " meta" not in map:
        map+= " meta"
    if ".json" not in map:
        map +=".json"
    path+= map
    with open(f"{path}", "r") as map_data:
        map_data=json.load(map_data)
    return map_data

def get_meta_files():
    path = os.getcwd()
    path+="/graphics/maps"
    path = os.listdir(path)
    meta_files = []
    for file in path:
        dot = file.rfind(".")
        ext = file[dot:]
        if ext == ".json":
            meta_files.append(file)
    return meta_files

def load_tiles(backdrop_coords, sprite_group,tiles = None, animated = False, is_player =False):
    """
    Function to load in instances of tiles from the metadata json.

    takes in the index of tiles of said type(npc, obstacle etc) and a
    sprite group, then, for every element in the index, set their coordinates
    relative to the backdrop location, their image and then adds them to
    the sprite group and an array containing all instances of said
    sprite group. depending on the value of animated, it will set the sprite as animated or static. False by default.
    returns the array

    The reason why this entire function is necessary is so that each map
    can have a dynamic amount of tiles and npc's etc

    :param backdrop_coords: the coordinates of the backdrop. a tuple
    :param tiles: the index of tiles from the meta json
    :param sprite_group: the given spritegroup
    :param animated: determines if the created sprites will be animated or not
    :return: tile_list, the list containing all instances

    Examples:
        >>> load_tiles((0,0), NPCs, npc_group, True)
        sets all npc's from the npc index in metadata, draws them relative to (0,0) adds them to the npc sprite group,
        and gives them animated sprites.

        >>> load_tiles((0,0), obstacles, obstacle_group, False)
        sets all obstacles from the obstacle index in metadata, main difference here is these are not animated

        >>> load_tiles((500,500),NPCs, npc_group, True)
        here, the backdrop is at (500,500), so draw all npc's with their coordinates relative to (500,500)

    """
    from graphics.sprites.Sprites.Sprites import Animated_Sprite, Static_Sprite
    if is_player:
        from main import mid_x, mid_y
        new_tile = Animated_Sprite(mid_x, mid_y, "graphics/sprites/overworld/player movement.png")
        sprite_group.add(new_tile)
        return sprite_group
    for tile in tiles:
        tile_data = tiles[tile]
        # x and y coordinates of the sprite which is relative to the pos of backdrop
        x = tile_data["coords"]["x"]; x+= backdrop_coords[0]
        y = tile_data["coords"]["y"]; y+= backdrop_coords[1]

        image = tile_data["image"] #image path

        if animated:
            new_tile = Animated_Sprite(x,y,image)
        if not animated:
            new_tile = Static_Sprite(x,y,image)

        sprite_group.add(new_tile)

    return sprite_group

def set_map(name):
    """
    Loads map metadata.

    Loads in the image, and gates and backdrop, npc's and tiles as well.
    put it all into an array, that is returned and each variable will be called upon.
    the same goes for values which are arrays like npc_list and obstacles_list.
    need to be reinitialized in the game loop.

    :param name: name of the map
    :return:
    """
    from main import npc_group, obstacle_group, background_group, mid_x, mid_y, player_group
    from graphics.sprites.Sprites.Sprites import Static_Sprite, Animated_Sprite

    map_data = [] #array that we will return
    map = load_map_data(name)
    gate = map["gates"]["gate 1"]; map_data.append(gate)
    backdrop_x = gate["coords"]["x"] #coordinates of the backdrop
    backdrop_y = gate["coords"]["y"]

    backdrop = Static_Sprite(backdrop_x, backdrop_y, map["image"]); map_data.append(backdrop)
    background_group.add(backdrop)

    NPCs = map["NPC's"]
    npc_group = load_tiles((backdrop_x, backdrop_y), npc_group, NPCs, True); map_data.append(npc_group)
    obstacles = map["Obstacles"]
    obstacle_group = load_tiles((backdrop_x, backdrop_y), obstacle_group, obstacles); map_data.append(obstacle_group)

    player_group = load_tiles((0,0), player_group, animated=True, is_player=True)

    return map_data

def link_gates(id):
    from main import name #gets the name of the current map
    meta_files = get_meta_files() #loads in all the meta data files
    for file in meta_files:
        map = load_map_data(file)
        map_name = map["name"] #gets the name of the meta file we want. if its name = global map name, we skip it
        if name != map_name:
            gates = map["gates"]
            for gate in gates:
                gate = gates[gate]
                gate_id = gate["id"] #for all the gates in meta data, look for the one who's id = the id we want
                if gate_id == id: name = map_name; return map_name

def kill_group(group):
    for sprite in group:
        group.remove(sprite)

    return group

def return_gate_coords(pr, gr):
    """

    :param pr: player rect
    :param gr: gate rect
    :return: an array of the differences
    """
    return [(abs(pr.left-gr.right)),(abs(pr.right-gr.left)),(abs(pr.top-gr.bottom)),(abs(pr.bottom-gr.top))]

def is_at_gate():
    from main import \
        (gayte, col_tol,background_group, obstacle_group, npc_group, gate_group, player_group, map,gate, name)

    for player in player_group:
        player = player

    coords_diff = return_gate_coords(player.rect, gayte.rect)
    if (coords_diff[0] <=col_tol or coords_diff[1] <=col_tol) and (coords_diff[2]<=col_tol or coords_diff[3]<=col_tol):

        npc_group = kill_group(npc_group)
        obstacle_group = kill_group(obstacle_group)
        gate_group = kill_group(gate_group)
        player_group = kill_group(player_group)
        background_group = kill_group(background_group)

        new_map = link_gates(gate["id"])

        name = new_map
        print(map)
        map = set_map(new_map)
        print(name)
