# Compare Pokemon in dex to pokemon in locations doc. then get names/numbers that aren't present.

import asyncio
import json
import aiohttp

from borrius_location_scraper import printLocationJson


def getMissingPokemonList():
    with open("scraperData/locationData.json") as f:
        location_data = json.load(f)

    location_names = [pokemon["pokemon"] for pokemon in location_data]

    with open("scraperData/borrius_pokedex_data.json") as f:
        borrius_pokedex_data = json.load(f)

    pokemon_names = [
        pokemon["name"].lower() for pokemon in borrius_pokedex_data[0]["pokemon"]
    ]
    not_in_pokedex = [name for name in location_names if name not in pokemon_names]

    results = sorted(not_in_pokedex, key=lambda x: len(x.split()) != 1)

    return [name.lower() for name in results]


async def getPokeApiData(pokemon):
    async with aiohttp.ClientSession() as session:
        try:
            pokeapi_species = await session.get(
                f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
            )
            data = await pokeapi_species.json()
            return data
        except Exception as e:
            print(f"Failed to retrieve data from PokeAPI: {e}")


async def getMissingPokemonData():
    missingPokemon = getMissingPokemonList()
    missingPokemon = [
        name
        for name in missingPokemon
        if name not in ["super rod", "good rod", "old rod", "special encounter"]
    ]

    pokemonReturned = []

    for pokemon_name in missingPokemon:
        if pokemon_name == "galarian slowpoke":
            pokemon_name = "slowpoke-galar"
        if pokemon_name == "morpeko":
            pokemon_name = "morpeko-full-belly"
        if pokemon_name == "eiscue":
            pokemon_name = "eiscue-ice"
        if pokemon_name == "basculin":
            pokemon_name = "basculin-red-striped"
        if pokemon_name == "minior":
            pokemon_name = "minior-red-meteor"
        if pokemon_name == "oricorio":
            pokemon_name = "oricorio-baile"
        if pokemon_name == "pumpkaboo":
            pokemon_name = "pumpkaboo-average"
        if pokemon_name == "gourgeist":
            pokemon_name = "gourgeist-average"
        if pokemon_name == "wormadam":
            pokemon_name = "wormadam-plant"
        if pokemon_name == "meowstic":
            pokemon_name = "meowstic-male"
        if pokemon_name == "wishiwashi":
            pokemon_name = "wishiwashi-solo"
        if pokemon_name == "lycanroc":
            pokemon_name = "lycanroc-midday"
        if pokemon_name == "darmanitan":
            pokemon_name = "darmanitan-standard"
        if pokemon_name == "deoxys":
            pokemon_name = "deoxys-normal"
        if pokemon_name == "shaymin":
            pokemon_name = "shaymin-land"
        if pokemon_name == "keldeo":
            pokemon_name = "keldeo-ordinary"
        if pokemon_name == "enamorus":
            pokemon_name = "enamorus-incarnate"

        pokemon_name = pokemon_name.rstrip()
        pokemonData = await getPokeApiData(pokemon_name)
        pokemon_id = pokemonData["id"]
        pokemonReturned.append({"pokemon": pokemon_name, "id": pokemon_id})
    return pokemonReturned


asyncio.run(printLocationJson())
asyncio.run(getMissingPokemonData())
