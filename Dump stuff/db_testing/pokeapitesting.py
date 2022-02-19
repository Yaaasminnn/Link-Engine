import requests
import json
from utils.json_utils import load_json, create_json, update_json

id = 1
pokemon = f"https://pokeapi.co/api/v2/pokemon/{id}/"

url = "https://pokeapi.co/api/v2/pokemon-species/1/"

response = requests.request("GET", url=url)

data = json.loads(response.text)
update_json("dump.json", data)
#print(json.dumps(data, indent=4, sort_keys=False))