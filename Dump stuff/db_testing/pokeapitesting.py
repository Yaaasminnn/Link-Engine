import time
import requests
import json
from utils.json_utils import load_json, create_json, update_json

id = 1
pokemon = f"https://pokeapi.co/api/v2/pokemon/{id}/"

url = f"https://pokeapi.co/api/v2/growth-rate/{2}/"
response = requests.request("GET", url=url)
data = json.loads(response.text)
update_json("dump.json", data,operation="w")
print(json.dumps(data, indent=4, sort_keys=False))
#time.sleep(1)