from utils.json_utils import load_json, update_json
from utils.key_press import Key
import pygame

class User_Config:
    """
    Loads and edits user config files.

    todo:
        add in methods that update user configs
    """
    def __init__(self, name):
        config = load_json(f"users/{name}/config.json") #loads the json file containing all user data
        colour = config["hitbox colours"] #index of the hitboxes's RGB values
        keybinds = config["keybinds"] #index of the keybinds
        macros = keybinds["macros"] #index of the macro keys

        #Sets the speed-based values
        self.base_speed = int(config["base speed"]) #how fast the player moves by walking
        self.run_speed = self.base_speed*2 #player speed when running. 2xbase_speed
        self.col_tol = self.run_speed #how close(in pixels) sprites can be before being considered collided. equal to run speed

        self.hitbox_colour = (int(colour["red"]),int(colour["green"]),int(colour["blue"])) #colour of the hitboxes

        self.draw_hud = config["draw HUD"] #determines if the HUD should be drawn

        #All the keybinds
        self.up = keybinds["up"]
        self.down = keybinds["down"]
        self.left = keybinds["left"]
        self.right = keybinds["right"]
        self.dash = keybinds["dash"]
        self.select = keybinds["select"]
        self.cancel = keybinds["cancel"]
        self.menu = keybinds["menu"]
        self.registered_item = keybinds["registered item"]
        self.exit = keybinds["exit"]
        self.debug = Key(keybinds["debug menu"])
        # Macros: will be able to register items from the bag for use. AND ALSO, TO VIEW THE PC OR DAYCARE REMOTELY
        self.m1 = macros["1"] #macro #1
        self.m2 = macros["2"] #macro #2
        self.m3 = macros["3"] #macro #3
        self.m4 = macros["4"] #macro #4

        #dialogue based values
        self.text_speed = config["text speed"] #how fast text moves
        self.box_choice = config["textbox choice"] #what textbox image u want
        self.textbox = pygame.image.load(f"./audio/dialogue/textboxes/textbox{self.box_choice}.png") #box image

        self.animate = config["animate"] #determines if we should animate the sprites or not


class Save_Data:
    """
    Meant to read, and update save data.
    """
    pass