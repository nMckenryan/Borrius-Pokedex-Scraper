import datetime
import time
import json
from bs4 import BeautifulSoup
import aiohttp
import asyncio

from termcolor import colored
    
from mainFunctions.helpers import BorriusPokedexHelpers, correct_pokemon_name, fetch_page, get_evo_details, get_pokemon_locations, read_location_data_json
from mainFunctions.scraper_actions import  get_moves_for_pokemon, get_tmhm_moves, \
    merge_moves, get_gender_data, get_stats, get_abilities, get_weight_height, \
    get_types, get_name, get_missing_moves_from_pokeapi


# SCRAPE POKEMON DATA FROM BORRIUS POKEDEX

bph = BorriusPokedexHelpers()
json_file = bph.json_header

async def scrape_pokemon_data(dex_page, numbers, indexCount, pokemonJson):
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
                moves = get_moves_for_pokemon(move_table, officialDexNumber)
                
                if(moves) == []:
                    moves = await get_missing_moves_from_pokeapi(officialDexNumber)

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
        try:
            await scrape_pokemon_data(bph.national_page, bph.national_numbers, 1, json_file)
        except Exception as e:
            print(colored(f"Failed to retrieve starters: {e}", "red"))

        try: 
            await scrape_pokemon_data(bph.borrius_page, bph.borrius_numbers, 10, json_file)
        except Exception as e:
            print(colored(f"Failed to retrieve main dex: {e}", "red"))


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

    await compile_pokedex()

    printTime = datetime.datetime.now()
    print(f"Printing JSON to file process started at {printTime}")
    try:
        fileName = "scraperData/borrius_pokedex_data.json"
        with open(fileName, "w") as fp:
            json.dump(json_file, fp, indent=4)

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
