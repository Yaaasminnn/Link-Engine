#!/usr/bin/python3
import json

"""
Pokedex Generator.
Developer: lvlonEmperor/Loona
Date: 2021-12-14 1:02 am
"""

pokedex_data = {

      "Number": 0,

      "Name": "-",

      "Base Stats": {
        "Hit Points": 0,
        "Attack": 0,
        "Defence":  0,
        "Special Attack":  0,
        "Special Defence": 0,
        "Speed": 0
      },

      "Abilities": {"normal0": "Overgrow", "normal1": "", "hidden": "Chlorophyll"},

      "Moveset": {

        "Move 1": {"Name": "Tackle", "Level": 1}
      },

      "Types": {"Type 1": "Grass", "Type 2": "Poison"},

      "Evolutions": [{
        "id": 0,
        "level": 0
      },{
        "id": 0,
        "level": 0
      }],

      "gender ratio": 87.5,

      "Catch Rate": 45,

      "Height": {"metric": "0.7", "imperial": "2'04\""},

      "Weight": {"metric": "6.9", "imperial": "15.2"},

      "Egg Groups": ["Monster", "Grass"],

      "Levelling Rate": "Medium Slow",

      "Hatch Time": [5140, 5396],

      "Base Friendship": 70,

      "Base EXP Yield": 64

    }

def gen_json(num_pkmn):
    global pokedex_data
    with open("generated_pokedex.json", "w") as pokedex:
        json.dump({}, pokedex)
        for i in range(1,num_pkmn+1):
            json.dump(pokedex_data, pokedex)
            print(i)

num_pkmn = int(input("How many pokemon would you like to generate?"))
gen_json(num_pkmn)

