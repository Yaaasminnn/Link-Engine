import json

def load_config():
    """
    Loads config data.

    Includes, base speed, and debug/HUD features such as hitbox colours and whether we should draw the HUD or not
    """
    with open("./config/config.json", "r") as config:
        config_data = json.load(config)
    return config_data

def update_config(config_data):
    """
    updates config file.

    :param config_data: the configurations we want to change

    only meant to be used for draw HUD in game. nothing else is meant to be tampered with ingame.

    Takes the given config data we want to change and dumps it into the json file.
    """
    with open("./config/config.json", "w") as config:
        json.dump(config_data, config)
