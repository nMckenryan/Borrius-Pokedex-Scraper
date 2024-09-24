# Compare Pokemon in dex to pokemon in locations doc. then get names/numbers that aren't present.

import asyncio
import aiohttp
from bs4 import BeautifulSoup

from borrius_pokemon_scraper import fetch_page


import json

with open("scraperData/locationData.json") as f:
    location_data = json.load(f)

location_names = [pokemon["pokemon"] for pokemon in location_data]


with open("scraperData/borrius_pokedex_data.json") as f:
    borrius_pokedex_data = json.load(f)

pokemon_names = [pokemon["name"] for pokemon in borrius_pokedex_data[0]["pokemon"]]

# sorts so aloan forms etc coem last (they contain two words)
not_in_pokedex = [name for name in location_names if name not in pokemon_names]
not_in_locations = [name for name in pokemon_names if name not in location_names]

results = not_in_pokedex.sort(key=lambda x: len(x.split()) != 1)

print("Pokemon not in pokedex but in locations:")
for name in results:
    print(name)
