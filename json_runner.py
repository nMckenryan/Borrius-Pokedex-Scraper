import asyncio

from borrius_location_scraper import printLocationJson
from borrius_pokemon_scraper import output_pokedex_json


asyncio.run(printLocationJson())
asyncio.run(output_pokedex_json())
