import datetime
import time
import json
from bs4 import BeautifulSoup
import aiohttp
import asyncio

from termcolor import colored

from mainFunctions.helpers import BorriusPokedexHelpers, correct_pokemon_name, fetch_page, get_and_parse_evo, get_and_parse_evo_regional, get_pokemon_locations, get_regional_forms_by_name, read_location_data_json
from mainFunctions.scraper_actions import  get_moves_for_pokemon, get_tmhm_moves, \
    merge_moves, get_gender_data, get_stats, get_abilities, get_weight_height, \
    get_types, get_name, get_missing_moves_from_pokeapi


# SCRAPE POKEMON DATA FROM BORRIUS POKEDEX

bph = BorriusPokedexHelpers()
json_file = bph.json_header

async def scrape_pokemon_names():
    async with aiohttp.ClientSession() as session:
        tasks = []
        index_list = ["larvitar", "pupitar", "tyranitar", "beldum", "metang", "metagross", "gible", "gabite", "garchomp"]
        for i in bph.borrius_numbers:
            link = f"{bph.borrius_page}{i}"
            tasks.append(fetch_page(session, link))

        pages = await asyncio.gather(*tasks)
        
        for page in pages:
            if page is not None:
                # GET DATA FROM PAGE
                soup = BeautifulSoup(page, "html.parser")

                top_card = soup.find("div", class_="card-body")
                
                rawName = get_name(top_card)
                pokemonName = correct_pokemon_name(rawName)
                                
                index_list.append(pokemonName)
        return index_list
                
async def get_regional_from_pokeapi(list_of_pokemon, index_count, pokemon_json):
    async with aiohttp.ClientSession() as session:
                for p in list_of_pokemon:
                    try:
                        pokeapi = await session.get(
                            f"https://pokeapi.co/api/v2/pokemon/{p}"
                        )
                        
                        response = await pokeapi.json()
                        
                        pokeapi_species = await session.get(
                            response.get("species").get("url")
                        )
                        
                        species_response = await pokeapi_species.json()
                        
                        national_id = response.get("id")
                        
                        # The chance of this Pokémon being female, in eighths; or -1 for genderless.
                        gender_rate = species_response.get("gender_rate")
                        
                        evo_chain_url = species_response["evolution_chain"]["url"]

                        pokeapi_evochain = await session.get(evo_chain_url)
                        evo_data = await pokeapi_evochain.json()
                        
                        
                        evoDetails =  await get_and_parse_evo_regional(evo_data)
                        
                        evoDetailsJson = []
                        
                        for ed in evoDetails:
                            evoDetailsJson.append({
                                "stage": ed.evo_stage,
                                "evo_name": ed.evo_stage_name,
                                "evo_trigger": ed.evo_trigger,
                                "evo_conditions": ed.evo_conditions
                            })
                        
                        
                        gender_data = {
                            "isGenderless": gender_rate == -1,
                            "maleChance": 100 / gender_rate,
                            "femaleChance": 100 % gender_rate,
                        }

                        
                        abilities = []
                        types = []
                        stats = []
                        
                        
                        for ability in response.get("abilities"):
                            abilities.append(ability["ability"]["name"])
                            
                        for type in response.get("types"):
                            types.append(type["type"]["name"])
                        
                        for stat in response.get("stats"):
                            stats.append({stat["stat"]["name"]: stat["base_stat"]})                        

                        pokemon_data = {
                            "id": index_count,
                            "national_id": national_id,
                            "name": response.get("name"),
                            "types": types,
                            "abilities": abilities,
                            "height": response.get("height"),
                            "weight": response.get("weight"),
                            "capture_rate": species_response.get("capture_rate"),
                            "sprites": {
                                "front_default": response.get("sprites").get("front_default"),
                                "official_artwork": response.get("sprites").get("other").get("official-artwork").get("front_default"),
                            },
                            "stats": stats,
                            "gender": gender_data,
                            "evolution_chain": evoDetailsJson,
                            "locations": [],
                            "moves": [],
                        }
                        index_count += 1
                        pokemon_json[0]["pokemon"].append(pokemon_data)
                                
                        
                    except Exception as e:
                        print(
                            colored(
                                f"Failed to retrieve evolution data {p} from PokeAPI: {e}",
                                "red",
                            ),
                        )
            


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
                    lambda tag: tag.name == "div" and "TM/HM Moves" in tag.decode(),
                    class_="overflow-x-auto col-span-6 col-start-2 justify-stretch",
                )
                
                try:
                    move_table = learned_move_table_parent.find("tbody")
                except AttributeError:
                    print(f"Error: Could not find learned move table for {i}")
                    move_table = []
                    
                    
                try:
                    tmhm_move_table = tmhm_move_table_parent.find("tbody")
                except AttributeError:
                    print(f"Error: Could not find TMHM move table for {i}")
                    tmhm_move_table = []
                
                

                # Get SPRITES (also extracts actual pokemon number from official dex)
                sprite_src = soup.find("img")["src"]
                officialDexNumber = int(sprite_src.split("/")[4].split(".")[0])

                evoDetails = await get_and_parse_evo(officialDexNumber)
                
                evoDetailsJson = []
                
                for ed in evoDetails:
                    evoDetailsJson.append({
                        "stage": ed.evo_stage,
                        "evo_name": ed.evo_stage_name,
                        "evo_trigger": ed.evo_trigger,
                        "evo_conditions": ed.evo_conditions
                    })
                
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
            
                # APPLY DATA TO JSON
                pokemon_data = {
                    "id": indexCount,
                    "national_id":  officialDexNumber,
                    "name": pokemonName,
                    "types": typeArray,
                    "abilities": abilities,
                    "height": heightInDecimetres,
                    "weight": weightInHectograms,
                    "capture_rate": capture_rates,
                    "sprites": {
                        "front_default": str(f"https://www.pokemonunboundpokedex.com/{sprite_src.replace('../', '')}"),
                        "official_artwork": str(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{str(officialDexNumber)}.png")
                    },
                    "stats": stats_table_output,
                    "gender": gender_data,
                    "evolution_chain": evoDetailsJson,
                    "locations": pokemonLocations,
                    "moves": combined_moves,
                }
                indexCount += 1
                pokemonJson[0]["pokemon"].append(pokemon_data)
                
                
async def scrape_pokemon_category(page, numbers, start_index, category_name):
    try:
        return await scrape_pokemon_data(page, numbers, start_index, json_file)
    except Exception as e:
        print(colored(f"Failed to retrieve {category_name}: {e}", "red"))
        return []


# reads through the borrius pokedex website and gets basic data. 
async def compile_pokedex():
    pokemon_location = await read_location_data_json()
    regional_form_list = get_regional_forms_by_name(pokemon_location)
    # special_encounter_numbers = await get_missing_pokemon_data()
    
    start = time.perf_counter()
    
    print(
        colored(f"\n\n ---- BORRIUS POKEDEX SCRAPER ---- ", "black", "on_yellow"),
    )

    print(
        colored(f"Started creating Borrius Pokedex Json file at {datetime.datetime.now()} \n Creating Json file...", "yellow"),
    )

    try:
        # Retrieves 9 starters for the National Dex and 494 in the Borrius National Dex (both come from separate pages)
        
        await asyncio.gather(
            scrape_pokemon_category(bph.national_page, bph.national_numbers, 1, "starters"),
            scrape_pokemon_category(bph.borrius_page, bph.borrius_numbers, 10, "main dex"),
            scrape_pokemon_category(bph.borrius_page, bph, 503, "regional"),
            # scrape_pokemon_category(bph.borrius_page, special_encounter_numbers, 503, "special")
        )            
        
        json_file[0]["pokemon"].sort(key=lambda x: x["id"])
        
        end = time.perf_counter()
        length = end - start
        print(
            colored(
                f"successfully created pokemon data in {format(length, '.2f')} seconds ({format(length / 60, '.2f')} minutes)",
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
