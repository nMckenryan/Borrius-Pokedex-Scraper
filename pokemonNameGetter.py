# Compare Pokemon in dex to pokemon in locations doc. then get names/numbers that aren't present.

import asyncio
import json
import aiohttp

from borrius_pokemon_scraper import fetch_page


def getMissingPokemon():
    with open("scraperData/locationData.json") as f:
        location_data = json.load(f)

    location_names = [pokemon["pokemon"] for pokemon in location_data]

    with open("scraperData/borrius_pokedex_data.json") as f:
        borrius_pokedex_data = json.load(f)

    pokemon_names = [pokemon["name"] for pokemon in borrius_pokedex_data[0]["pokemon"]]

    # sorts so alolan forms etc coem last (they contain two words)
    not_in_pokedex = [name for name in location_names if name not in pokemon_names]

    results = sorted(not_in_pokedex, key=lambda x: len(x.split()) != 1)

    for i, name in enumerate(results):
        if name.startswith("Galarian "):
            results[i] = name[9:].replace(" ", "-").replace(".", "") + "-Galar"
        if name.startswith("Alolan "):
            results[i] = name[7:].replace(" ", "-") + "-Alola"
    return results


# async def getMissingPokemonIndexes():
#     missingPokemon = getMissingPokemon()
#     borrius_pokedex_data = None
#     with open("scraperData/borrius_pokedex_data.json") as f:
#         borrius_pokedex_data = json.load(f)

#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for pokemon_name in missingPokemon:
#             tasks.append(
#                 fetch_page(session, "https://pokeapi.co/api/v2/pokemon/" + pokemon_name)
#             )
#         pokeapi_responses = await asyncio.gather(*tasks)

#         for response in pokeapi_responses:
#             if response is not None:
#                 pokemon_number = response["id"]
#                 missingPokemonIndexes = borrius_pokedex_data[0]["pokemon"].index(
#                     next(
#                         pokemon
#                         for pokemon in borrius_pokedex_data[0]["pokemon"]
#                         if pokemon["number"] == pokemon_number
#                     )
#                 )


print(getMissingPokemon())
