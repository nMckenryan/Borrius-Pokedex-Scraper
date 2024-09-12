import datetime
import time
import requests
import json
from bs4 import BeautifulSoup
import re
import aiohttp
import asyncio

currentTime = datetime.datetime.now()

pokemonJson = [
    {
        "info": {
            "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
            "dataPulledOn": str(currentTime),
        },
        "pokemon": [],
    }
]


# Loop through all 494 in the borrius dex


async def fetch_page(session, link):
    async with session.get(link) as page:
        if page.status == 200:
            return await page.text()


async def createPokemonJson(dex_page, numbers, indexCount):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in numbers:
            link = f"{dex_page}{i}"
            tasks.append(fetch_page(session, link))
        pages = await asyncio.gather(*tasks)

        for page in pages:
            if page is not None:
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

                # Get Sprites (also extracts actual pokemon number from official dex)
                sprite_src = soup.find("img")["src"]
                officialDexNumber = int(sprite_src.split("/")[4].split(".")[0])

                sprite_link = str(
                    f"https://www.pokemonunboundpokedex.com/{sprite_src.replace('../', '')}",
                )

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

                gender_data = re.findall(
                    r"\d+",
                    top_card.find_all("p", class_="text-3xl font-bold")[2].text.strip(),
                )
                isGenderLess = len(gender_data) == 0
                if isGenderLess:
                    gender_data = [0, 0]

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

                abilitiesList = (
                    top_card.find_all("p", class_="text-3xl font-bold")[3]
                    .text.strip("[]")
                    .replace("'", "")
                    .split(", "),
                )

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

                # APPLY DATA TO JSON
                pokemon_data = {
                    officialDexNumber: {
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
                        "id": officialDexNumber,
                        "name": top_card.find("h3", class_="card-title text-4xl")
                        .text.strip()
                        .replace("Name: ", ""),
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
                        "moves": [moves + tmhm_moves],
                        "sprites": {
                            "front_default": sprite_link,
                            "other": {
                                "home": {
                                    "front_default": sprite_link,
                                }
                            },
                        },
                        "stats": stats_table_output,
                        "types": top_card.find_all("p", class_="text-3xl font-bold")[
                            0
                        ].text.strip(),
                        "gender": {
                            "isGenderless": top_card.find_all(
                                "p", class_="text-3xl font-bold"
                            )[2].text.strip()
                            == "Genderless",
                            "maleChance": gender_data[0],
                            "femaleChance": gender_data[1],
                        },
                    }
                }

                indexCount += 1
                pokemonJson[0]["pokemon"].append(pokemon_data)


borrius_numbers = range(1, 495)
starter_numbers = [246, 247, 248, 374, 375, 376, 443, 444, 445]


national_page = "https://www.pokemonunboundpokedex.com/national/"
borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"


async def compile_pokedex():
    start = time.time()
    print("\n\n---- BORRIUS POKEDEX SCRAPER --------")
    print(
        f"Started creating Borrius Pokedex Json file at {currentTime}\n Creating Json file..."
    )
    try:
        # Retrieves 9 starters for the National Dex and 494 in the Borrius National Dex (both come from separate pages)
        await createPokemonJson(national_page, starter_numbers, 1)
        await createPokemonJson(borrius_page, borrius_numbers, 10)
        end = time.time()
        length = end - start
        print(
            f"successfully created JSON in {format(length, '.2f')} seconds ({format(length / 60, '.2f')} minutes"
        )
    except Exception as e:
        print(f"Failed to retrieve data from Pokemon Unbound Site: {e}")


async def output_pokedex_json():
    await compile_pokedex()

    printTime = datetime.datetime.now()
    print(f"Printing JSON to file process started at {printTime}")
    try:
        fileName = "borrius_pokedex_data.json"
        with open(fileName, "w") as fp:
            json.dump(pokemonJson, fp, indent=4)
        print(f"{fileName} successfully created")
    except Exception as e:
        print(f"Json Generation Failed : {e}")


## GET FROM POKEAPI
# starters = [246, 247, 248, 374, 375, 376, 443, 444, 445]
# starter = 1
# pokemonGet = [];
# for index in starters:
#     pokeapi_page = s.get(f"https://pokeapi.co/api/v2/pokemon/{index}")
#     # Get pokeapi data for missing pokemon
#     url = f"https://pokeapi.co/api/v2/pokemon/{index}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         pokemonData = response.json()
#         try:
#             # capRate = pokemonData["capture_rate"]
#             capRate = 1

#             pokemonGet.append(
#                 {
#                 "pokemon_index": starter + 1,
#                 "name": pokemonData["name"],
#                     "sprite": pokemonData["sprites"]["front_default"],
#                     "type": [pokemonData["types"]],
#                 "catchRate": {
#                     "value": capRate,
#                     "percentage": 999,
#                 },
#                 "gender": {
#                         "isGenderless": 0,
#                         "maleChance": 50,
#                         "femaleChance": 50
#                 },
#                 "abilities": pokemonData["abilities"],
#                 "weight": {
#                     "imperial": round(pokemonData["weight"] * 0.220462, 1),
#                     "metric": pokemonData["weight"],
#                 },
#                 "height": {
#                     "imperial": pokemonData["height"] * 0.393701,
#                     "metric": pokemonData["height"],
#                 },
#                 "stats": pokemonData["stats"],
#                 "learnedMoves": pokemonData["moves"],
#                 "tmhmMoves": pokemonData["moves"],
#                 }
#             )

#         except Exception as e:
#             print(f"Failed to retrieve data from PokeAPI: {e}")


# pokemonJson += pokemonGet
