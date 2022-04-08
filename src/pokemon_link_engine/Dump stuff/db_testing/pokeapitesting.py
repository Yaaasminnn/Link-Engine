import time
import requests
import json
from utils.json_utils import update_json

id = 521

def call(print_resp=False, id=id):
    url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
    response = requests.request("GET", url=url)
    data = json.loads(response.text)
    if print_resp:
        print(json.dumps(data, indent=4, sort_keys=False))
    else:
        update_json("dump.json", data, operation="w")

def list(print_resp=False):
    begin, end = 1,5
    for i in range(begin, end+1):
        call(print_resp, id=i)
        time.sleep(1)


def create_pokemon(id:int):
    """
    Pokemon database object:
    {
        abilities:[ // list of abilities
            {
                name: ""
                slot: int // 1st, 2nd or 3rd(hidden) ability
            }
        ]
        id: int // id of the pokemon
        name: "" // name of the pokemon
        base_experience: int // base experience gained when beating the pokemon in battle
        height: int // height in decimeters
        is_default: bool // if this is the default form
        weight: int // weight in hectograms
        sprites: {
                split off after the 8th slash and then replace remaining slashes in the substrings to underscores?
        }
    }
    """
    pass

call()