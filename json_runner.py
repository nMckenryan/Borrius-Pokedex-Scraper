import asyncio

from borrius_location_scraper import printLocationJson
from borrius_pokemon_scraper import output_pokedex_json

# This script is used to run both the borrius_location_scraper and borrius_pokemon_scraper scripts manually to generate the JSON files.


async def run_json_generation():
    await printLocationJson()
    await output_pokedex_json()


asyncio.run(run_json_generation())
