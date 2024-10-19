# # Get data from BorriusPokedex page for scraping
# import asyncio
# import aiohttp
# from termcolor import colored
# from mainFunctions.helpers import correct_pokemon_name, get_special_encounter_pokemon

# # One time run for pokedex index collection
# async def get_pokemon_index_from_name(pokemon_name):
#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(
#                 f"https://pokeapi.co/api/v2/pokemon/{correct_pokemon_name(pokemon_name)}"
#             ) as resp:
#                 pokemon_data = await resp.json()
#                 return pokemon_data["id"]
#     except Exception as e:
#         print(
#             colored(
#                 f"Failed to retrieve index data from PokeAPI: {e}",
#                 "red",
#             ),
#         )

# # list through the above
# async def get_pokemon_indexes():
#     missing_pokemon = get_special_encounter_pokemon()
#     async with aiohttp.ClientSession() as session:
#         tasks = [get_pokemon_index_from_name(pokemon) for pokemon in missing_pokemon]
#         results = await asyncio.gather(*tasks, return_exceptions=True)
#         return [x for x in results if isinstance(x, int)]
