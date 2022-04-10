import time
import requests
import json
from utils.json_utils import update_json

id = 1

def call(print_resp=False, id=id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{id}/"
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
    research evolutions, moves
    Pokemon database object:
    {
        id: int // id of the pokemon. used for globals and references by the program
        name: "" // name of the pokemon. used for globals and references by the program
        varieties[ // different varieites of a pokemon(usually have diff stats, abilities, etc). megas, deoxys/kyurem forms
            { // only data universal across forms are kept outside of forms. (non universal: default, types etc)
                name: "" // name of the pokemon. used for ingame references
                abilities:[ // list of abilities. order determines slot. (1(1st),2(2nd),3(hidden))
                    ""
                ]
                base_experience: int // base experience gained when beating the pokemon in battle
                height: int // height in decimeters
                weight: int // weight in hectograms
                held_items: [ //list of items the pokemon could be holding when encountered?
                    ""
                ]
                moves:[
                    {
                        name: "" // name of the move
                        methods:[ // can have multiple methods of learning a move.
                            {
                                level_learned_at: int // level eligible to learn said move
                                move_learn_method: "" // how it gains it(level-up, tutor, machine, egg)
                            }
                        ]
                    }
                ]
                stats:[ //0-5 (hp, atk, def, spatk, spdef, speed)
                    int
                ]
                forms:[ // forms are with different appearances and types. otherwise the same. part of a variety. combine default pokemon into a form?
                    {
                        name: "" // full name
                        form_order: int // order of the form
                        is_default: bool // if this is the default form
                        is_battle_only: bool // only appears in battle (megas etc)
                        *is_mega: bool
                        form_name: "" // name of the form
                        types: [ // slots are the order in the array
                            "type1",
                            "type2"
                        ]
                    }
                ]
            }
        ]
        species:{ // globally shared for all pokemon
            gender rate: int // chance of being female in decimal. (rate/8)*100 = female precentage
            capture rate: int // how easy it is to capture 0-255
            base_happiness: int // 0-255. base happiness when caught with a normal pokemon
            is_baby: bool // is_baby. baby pokemon cannot breed
            is_legendary: bool
            is_mythical: bool
            hatch_counter: int // dont understand this
            has_gender_differences: bool // has gender differences. useful for determining what sprites
            forms_switchable: bool // can the pokemon switch between its forms?
            growth rate: "" // the growth rate
            egg groups:[ // list of all egg groups
                ""
            ]
            color: "" // what colour this pokemon is. make it colour hehe
            shape: "" // shape of the pokemon
            habitat: "" // habitat this pokemon can be found in
            flavour text entries: "" // the pokedex info stuff. get only one from b2w2
            genera: "" // just keep the english one
            evolves_from_species: "" // name of the pokemon it evolves from
            evolution_chain
        }
    }

    sprites: { // stored in their own folders
        split off after the 8th slash and then replace remaining slashes in the substrings to underscores?
        remove other and versions tab
        add all varieites and forms here
        [back/shiny/female]_[id]-[variety/form name].png ? megas?
            if is default, we dont add to the name
            if its form[name] == variety[name]: dont add
    }

    species[varieties] will help us find all varieties of a pokemon
    we can use species when on the base pokemon
    forms data are added to each variety
    """
    pass

call()