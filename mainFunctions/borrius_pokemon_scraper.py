"""
This script is used to scrape the Borrius Pokedex from the Pokemon Unbound website
and generate a JSON file containing the data for all the Pokemon in the Borrius
Dex.

The script works by first reading in the location data from a JSON file, then
scraping the data from the Pokemon Unbound website for the Borrius Pokedex, and
finally combining the two datasets and writing the combined data to a new JSON
file.

The script can be run from the command line with the following command:

    python borrius_pokemon_scraper.py

This will generate a JSON file called 'borrius_pokedex_data.json' in the
'scraperData' directory which contains the data for all the Pokemon in the
Borrius Dex.
"""

import datetime
import time
import json
from bs4 import BeautifulSoup
import aiohttp
import asyncio

from termcolor import colored

from mainFunctions.helpers import correct_pokemon_name, fetch_page, get_pokemon_locations, read_location_data_json, \
    borrius_pokedex_indexes
    
from mainFunctions.scraper_actions import get_evo_details, get_moves_for_pokemon, get_tmhm_moves, \
    merge_moves, get_gender_data, get_stats, get_abilities, get_weight_height, \
    get_types, get_name


# SCRAPE POKEMON DATA FROM BORRIUS POKEDEX
async def scrape_pokemon_data(dex_page, numbers, indexCount, pokemonJson):
    """
    This function scrapes data for Pokemon from the Borrius Pokedex website.
    It retrieves information such as stats, moves, abilities, location, sprites, and evolution chain for each Pokemon.

    Parameters:
    - dex_page (str): The base URL for the Pokedex page
    - numbers (list): A list of Pokemon numbers to scrape
    - indexCount (int): The index count for the Pokemon data
    - pokemonJson (list): A list containing the JSON data for the Pokemon

    Returns:
    None
    """

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in numbers:
            link = f"{dex_page}{i}"
            tasks.append(fetch_page(session, link))

        pages = await asyncio.gather(*tasks)
        
        location_data = await read_location_data_json()

        for page in pages:
            if page is not None:
                # GET DATA FROM PAGE
                soup = BeautifulSoup(page, "html.parser")
                top_card = soup.find("div", class_="card-body")
                stats_table = soup.find("table", class_="table table-zebra")
                learned_move_table_parent = soup.find(
                    lambda tag: tag.name == "div" and "Level Up Moves" in tag.decode(),
                    class_="overflow-x-auto col-span-6 col-start-2 justify-stretch",
                )
                tmhm_move_table_parent = soup.find(
                    lambda tag: tag.name == "div" and "Level Up Moves" in tag.decode(),
                    class_="overflow-x-auto col-span-6 col-start-2 justify-stretch",
                )
                move_table = learned_move_table_parent.find("tbody")
                tmhm_move_table = tmhm_move_table_parent.find("tbody")

                # Get SPRITES (also extracts actual pokemon number from official dex)
                sprite_src = soup.find("img")["src"]
                officialDexNumber = int(sprite_src.split("/")[4].split(".")[0])
                sprite_link = str(
                    f"https://www.pokemonunboundpokedex.com/{sprite_src.replace('../', '')}",
                )

                official_sprite_link = str(
                    f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{str(officialDexNumber)}.png"
                )

                evoDetails = await get_evo_details(officialDexNumber)
                
                # MOVES
                moves = get_moves_for_pokemon(move_table)

                tmhm_moves = get_tmhm_moves(tmhm_move_table)

                # COMBINE TMHM AND MOVES TABLES
                combined_moves = merge_moves(moves, tmhm_moves)

                # GENDER RATES
                gender_data = get_gender_data(top_card)

                # STATS
                stats_table_output = get_stats(stats_table)

                # ABILITIES
                abilities = get_abilities(top_card)

                # WEIGHT & HEIGHT
                weightInHectograms, heightInDecimetres = get_weight_height(top_card)

                # TYPES
                typeArray = get_types(top_card)
                
                rawName = get_name(top_card)
                pokemonName = correct_pokemon_name(rawName)
                
                pokemonLocations = get_pokemon_locations(pokemonName, location_data)
                
                capture_rates = {
                        "value": float(
                            top_card.find_all("p", class_="text-3xl font-bold")[1]
                            .text.strip()
                            .replace("%", "")
                            .split(" ")[1]
                        ),
                        "percentage": top_card.find_all(
                            "p", class_="text-3xl font-bold"
                        )[1]
                        .text.strip()
                        .split(" ")[0],
                    }
                
                gender_data = {
                        "isGenderless": top_card.find_all(
                            "p", class_="text-3xl font-bold"
                        )[2].text.strip()
                        == "Genderless",
                        "maleChance": gender_data[0],
                        "femaleChance": gender_data[1],
                    }
                
                sprites_data = {
                        "front_default": sprite_link,
                        "other": {"home": {"front_default": official_sprite_link}},
                    },
            
                # APPLY DATA TO JSON
                pokemon_data = {
                    "id": officialDexNumber,
                    "name": pokemonName,
                    "types": typeArray,
                    "abilities": abilities,
                    "game_indices": {
                        "unbound_index": indexCount,
                        "official_index": officialDexNumber,
                    },
                    "height": heightInDecimetres,
                    "weight": weightInHectograms,
                    "capture_rate": capture_rates,
                    "sprites": sprites_data,
                    "stats": stats_table_output,
                    "gender": gender_data,
                    "evolution_chain": evoDetails,
                    "locations": pokemonLocations,
                    "moves": combined_moves,
                }
                indexCount += 1
                pokemonJson[0]["pokemon"].append(pokemon_data)

                
# reads through the borrius pokedex website and gets basic data. 
async def compile_pokedex():

    national_page = "https://www.pokemonunboundpokedex.com/national/"
    borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"

    borrius_numbers = borrius_pokedex_indexes.get("borrius_numbers")
    national_numbers = borrius_pokedex_indexes.get("national_numbers")
    
    print("\n\n")
    print(
        colored("---- BORRIUS POKEDEX SCRAPER ----", "black", "on_yellow"),
    )
    start = time.time()
    print(
        f"Started creating Borrius Pokedex Json file at {datetime.datetime.now()}\n Creating Json file..."
    )
    try:
        # Retrieves 9 starters for the National Dex and 494 in the Borrius National Dex (both come from separate pages)
        await scrape_pokemon_data(national_page, national_numbers, 1)
        await scrape_pokemon_data(borrius_page, borrius_numbers, 10)

        end = time.time()
        length = end - start
        print(
            colored(
                f"successfully created JSON in {format(length, '.2f')} seconds ({format(length / 60, '.2f')} minutes)",
                "green",
            ),
        )
    except Exception as e:
        print(colored(f"Failed to retrieve data from Pokemon Unbound Site: {e}", "red"))


async def output_pokedex_json():
    
    currentTime = datetime.datetime.now()

    locationList = []

    pokemonJson = [
    {
        "info": {
            "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
            "dataPulledOn": str(currentTime),
        },
        "pokemon": [],
    }
    ]

    await compile_pokedex(pokemonJson)

    printTime = datetime.datetime.now()
    print(f"Printing JSON to file process started at {printTime}")
    try:
        fileName = "scraperData/borrius_pokedex_data.json"
        with open(fileName, "w") as fp:
            json.dump(pokemonJson, fp, indent=4)

        print(
            colored(
                f"{fileName} successfully created",
                "green",
            ),
        )
    except Exception as e:
        print(
            colored(
                f"Json Generation Failed : {e}",
                "red",
            ),
        )
