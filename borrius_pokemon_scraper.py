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

import ast
import datetime
import time
import json
from bs4 import BeautifulSoup
import re
import aiohttp
import asyncio

from termcolor import colored

from helpers import correct_pokemon_name, fetch_page, get_evolution_data_from_pokeapi, get_pokemon_locations, read_location_data_json,\
    borrius_pokedex_indexes

async def createPokemonJson(dex_page, numbers, indexCount, pokemonJson):
    
    borrius_pokemon_names = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in numbers:
            link = f"{dex_page}{i}"
            tasks.append(fetch_page(session, link))

        pages = await asyncio.gather(*tasks)

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

                try:
                    getEvoDetails = await get_evolution_data_from_pokeapi(officialDexNumber)
                    evoDetails = getEvoDetails.get("evolution_details", {}).get(
                        "chain", None
                    )
                except Exception as e:
                    print(
                        f"Failed to retrieve pokeapi data for {officialDexNumber}: {e}"
                    )
                    evoDetails = None

                sprite_link = str(
                    f"https://www.pokemonunboundpokedex.com/{sprite_src.replace('../', '')}",
                )

                official_sprite_link = str(
                    f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{str(officialDexNumber)}.png"
                )
                # MOVES
                moves = []
                for row in move_table.find_all("tr"):
                    columns = row.find_all("td")
                    if len(columns) > 0:
                        moves.append(
                            {
                                "move": {
                                    "name": columns[1].text.strip(),
                                    "type": columns[2].text.strip(),
                                    "category": columns[3].text.strip(),
                                    "power": columns[4]
                                    .text.strip()
                                    .replace("\u2014", "-"),
                                    "accuracy": columns[5]
                                    .text.strip()
                                    .replace("\u2014", "-"),
                                },
                                "version_group_details": [
                                    {
                                        "level_learned_at": columns[0].text.strip(),
                                        "move_learn_method": {
                                            "name": "level-up",
                                            "url": "https://pokeapi.co/api/v2/move-learn-method/1/",
                                        },
                                        "version_group": {"name": "unbound"},
                                    }
                                ],
                            }
                        )

                tmhm_moves = []
                for row in tmhm_move_table.find_all("tr"):
                    columns = row.find_all("td")
                    if len(columns) > 0:
                        tmhm_moves.append(
                            {
                                "move": {
                                    "name": columns[1].text.strip(),
                                    "type": columns[2].text.strip(),
                                    "category": columns[3].text.strip(),
                                    "power": columns[4]
                                    .text.strip()
                                    .replace("\u2014", "-"),
                                    "accuracy": columns[5]
                                    .text.strip()
                                    .replace("\u2014", "-"),
                                },
                                "version_group_details": [
                                    {
                                        "level_learned_at": 0,
                                        "move_learn_method": {
                                            "name": "machine",
                                            "url": "https://pokeapi.co/api/v2/move-learn-method/4/",
                                        },
                                        "version_group": {"name": "unbound"},
                                    }
                                ],
                            }
                        )

                # COMBINE TMHM AND MOVES TABLES
                combined_moves = moves + tmhm_moves
                for combined_move in combined_moves:
                    for tmhm_move in tmhm_moves:
                        if (
                            combined_move["move"]["name"] == tmhm_move["move"]["name"]
                            and combined_move["version_group_details"][0][
                                "move_learn_method"
                            ]["name"]
                            != "machine"
                        ):
                            combined_move["version_group_details"][0][
                                "move_learn_method"
                            ]["name"] = "level-up/tm"
                            break

                # GENDER RATES
                gender_data = re.findall(
                    r"\d+",
                    top_card.find_all("p", class_="text-3xl font-bold")[2].text.strip(),
                )
                isGenderLess = len(gender_data) == 0
                if isGenderLess:
                    gender_data = [0, 0]

                # STATS
                stats_table_output = {}
                stats = [
                    "hp",
                    "attack",
                    "defense",
                    "specialAttack",
                    "specialDefense",
                    "speed",
                ]

                for i, stat in enumerate(stats):
                    stats_table_output[stat] = {
                        "base_stat": int(
                            stats_table.find_all("td")[i * 3].text.strip()
                        ),
                        "effort": 0,
                        "stat": {
                            "name": stat,
                            "url": f"https://pokeapi.co/api/v2/stat/{i+1}/",
                        },
                    }

                # ABILITIES
                abl = top_card.find_all("p", class_="text-3xl font-bold")[
                    3
                ].text.strip()

                abilitiesList = ast.literal_eval(abl)

                abilities = []
                for ability in abilitiesList:
                    ab = {
                        "ability": {
                            "name": ability,
                            # "url": f"https://pokeapi.co/api/v2/ability/{ability.lower()}/",
                        },
                        "is_hidden": 0,
                        "slot": 1,
                    }
                    abilities.append(ab)

                    # WEIGHT
                weightInHectograms = (
                    float(
                        top_card.find_all("p", class_="text-3xl font-bold")[4]
                        .text.strip()
                        .split(" ")[0]
                        .replace("\u00a0", "")
                        .replace("kg", "")
                        .replace(" ", "")
                        .replace(".", "")
                        .replace(",", "")
                    )
                    * 10
                )

                # HEIGHT
                heightInDecimetres = (
                    float(
                        top_card.find_all("p", class_="text-3xl font-bold")[5]
                        .text.strip()
                        .split(" ")[0]
                        .replace("\u00a0", "")
                        .replace("m", "")
                        .replace(" ", "")
                        .replace(".", "")
                        .replace(",", "")
                    )
                    * 10
                )

                # TYPES
                tA = top_card.find_all("p", class_="text-3xl font-bold")[0].text.strip()

                typeArray = ast.literal_eval(tA)

                retrievedName = str(
                    top_card.find("h3", class_="card-title text-4xl")
                    .text.strip()
                    .replace("Name: ", ""),
                )
                
                pokemonName = correct_pokemon_name(retrievedName)
                
                borrius_pokemon_names.append(pokemonName)
                
                pokemonLocations = get_pokemon_locations(pokemonName)
                
            
                # APPLY DATA TO JSON
                pokemon_data = {
                    "abilities": abilities,
                    "game_indices": [
                        {
                            "game_index": indexCount,
                            "version": {
                                "name": "red",
                                "url": "https://pokeapi.co/api/v2/version/1/",
                            },
                        },
                        {
                            "game_index": officialDexNumber,
                            "version": {"name": "unbound", "url": "-"},
                        },
                    ],
                    "height": heightInDecimetres,
                    "weight": weightInHectograms,
                    "id": officialDexNumber,
                    "name": pokemonName,
                    "locations": pokemonLocations,
                    "capture_rate": {
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
                    },
                    "moves": combined_moves,
                    "sprites": {
                        "front_default": sprite_link,
                        "other": {"home": {"front_default": official_sprite_link}},
                    },
                    "evolution_chain": evoDetails,
                    "stats": stats_table_output,
                    "types": typeArray,
                    "gender": {
                        "isGenderless": top_card.find_all(
                            "p", class_="text-3xl font-bold"
                        )[2].text.strip()
                        == "Genderless",
                        "maleChance": gender_data[0],
                        "femaleChance": gender_data[1],
                    },
                    "locations": pokemonLocations,
                }
                indexCount += 1
                pokemonJson[0]["pokemon"].append(pokemon_data)
# reads through the borrius pokedex website and gets basic data. 
async def compile_pokedex():
    # await read_location_data_json()
    
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
        await createPokemonJson(national_page, national_numbers, 1)
        await createPokemonJson(borrius_page, borrius_numbers, 10)

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
