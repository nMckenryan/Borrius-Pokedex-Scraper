
import asyncio
from types import SimpleNamespace
import aiohttp
from bs4 import BeautifulSoup
from termcolor import colored
import json
import datetime


class BorriusPokedexHelpers:
    def __init__(self):
        self.national_numbers = [246, 247, 248, 374, 375, 376, 443, 444, 445]
        self.borrius_numbers = range(1, 495)
        self.national_page = "https://www.pokemonunboundpokedex.com/national/"
        self.borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
        self.json_header = [
            {
                "info": {
                    "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                    "dataPulledOn": str(datetime.datetime.now()),
                },
                "pokemon": [],
            }
        ]

# Get data from BorriusPokedex web page for scraping
async def fetch_page(session, link):
    async with session.get(link) as page:
        if page.status == 200:
            return await page.text()


# read existing locationData.json file
async def read_location_data_json():
    location_list = []
    try:
        with open("scraperData/locationData.json") as f:
            data = json.load(f)
            location_list.extend(data)
            return location_list
    except FileNotFoundError:
        print(
            colored(
                "locationData.json file not found",
                "yellow",
            ),
        )
    except json.JSONDecodeError as e:
        print(
            colored(
                f"Failed to read locationData.json, error: {e}", "red",
            ),
        )

def get_regional_forms_by_name(pokemon_list):
    
    regional_forms = []
    
    for p in pokemon_list:
        if "galar" in p['pokemon'] or "alola" in p['pokemon'] or "hisui" in p['pokemon']:
            regional_forms.append(correct_pokemon_name(p['pokemon']))
    return regional_forms


# search thru location_list for a given pokemon
def get_pokemon_locations(pokemon_name, location_list):
    for pokemon in location_list:
        if pokemon_name.lower() in pokemon["pokemon"].lower():
            return pokemon["locationData"]
    return []


# get a pokemon's evolution chain data from pokeapi. (gets pokemon's evo chain URL, then gets THAT data)
async def get_evolution_data_from_pokeapi(officialDexNumber):
    async with aiohttp.ClientSession() as session:
        try:
            pokeapi_species = await session.get(
                f"https://pokeapi.co/api/v2/pokemon-species/{officialDexNumber}"
            )

            species_data = await pokeapi_species.json()

            evo_chain_url = species_data["evolution_chain"]["url"]

            pokeapi_evochain = await session.get(evo_chain_url)
            evo_data = await pokeapi_evochain.json()
            
            sanitised_evo_data = evo_data.get("chain", {}).get("evolves_to", {})
            
            sorted = []
            
            for ed in sanitised_evo_data:
                last_evo_method = ed.get("evolution_details")
                if(len(last_evo_method) > 1):
                    for e in last_evo_method:
                        if(e.get("location") == None):
                            sorted.append(e)
                    
                

            pokeapi_data = {"evolution_details": evo_data}

            return pokeapi_data
        except Exception as e:
            print(
                colored(
                    f"Failed to retrieve evolution data {officialDexNumber} from PokeAPI: {e}",
                    "red",
                ),
            )
class EvoObject:
    def __init__(self, evo_stage, evo_name, evo_trigger, evo_conditions):
        self.evo_stage = evo_stage
        self.evo_stage_name = evo_name
        self.evo_trigger = evo_trigger
        self.evo_conditions = evo_conditions


def get_evo_trigger(ed):
    evo_refactored = json.loads(json.dumps(ed), object_hook=lambda d: SimpleNamespace(**d))
    evo_object = EvoObject(0, "", "", [])

    gender = evo_refactored[0].gender
    held_item = evo_refactored[0].held_item
    item = evo_refactored[0].item
    known_move = evo_refactored[0].known_move
    known_move_type = evo_refactored[0].known_move_type
    min_affection = evo_refactored[0].min_affection
    min_happiness = evo_refactored[0].min_happiness
    needs_overworld_rain = evo_refactored[0].needs_overworld_rain
    time_of_day = evo_refactored[0].time_of_day
    trade_species = evo_refactored[0].trade_species
    min_level = evo_refactored[0].min_level
    trigger = evo_refactored[0].trigger
    
    if gender is not None:
        evo_object.evo_conditions.append("Female" if gender == 1 else "Male")
    if held_item is not None:
        evo_object.evo_conditions.append("Hold: " + held_item.name)
    if item is not None:
        evo_object.evo_conditions.append("Use: " + item.name)
    if known_move is not None:
        evo_object.evo_conditions.append("Know: " + known_move.name)
    if known_move_type is not None:
        evo_object.evo_conditions.append("Known Move Type: " + known_move_type.name)
    if min_affection is not None:
        evo_object.evo_conditions.append("Affection: " + str(min_affection))
    if min_happiness is not None:
        evo_object.evo_conditions.append("Happiness: " + str(min_happiness))
    if needs_overworld_rain:
        evo_object.evo_conditions.append("Rain")
    if time_of_day:
        evo_object.evo_conditions.append("Time of Day: " + time_of_day)
    if trade_species is not None:
        evo_object.evo_conditions.append("Trade species " + trade_species.name)
    if min_level is not None:
        evo_object.evo_conditions.append(min_level)

    evo_object.evo_trigger = trigger.name


    return evo_object


def parse_evolution_chain(chain_data):
    evolution_list = []
    evo_name = chain_data['species']['name']
    first = EvoObject(1, evo_name, "base", [])
    evolution_list.append(first)
    
    def process_evolution(evolution_data, index):
        if not evolution_data:
            return

        current_species = evolution_data['species']
        
        
        # Process evolution details if they exist
        if evolution_data["evolution_details"]:
            evo_details = get_evo_trigger(evolution_data["evolution_details"])
            evo_details.evo_stage = index
            evo_details.evo_stage_name = current_species["name"]
            evolution_list.append(evo_details)
        
        
        # Recursively process next evolutions
        if evolution_data["evolves_to"]:
            for i, evolution in enumerate(evolution_data["evolves_to"], start=index+1):
                process_evolution(evolution, i)
            

    # Start processing from the first evolution
    if chain_data["evolves_to"]:
        if len(chain_data["evolves_to"]) > 1:
            for evolution in chain_data["evolves_to"]:
                process_evolution(evolution, 2)
        else:
            for i, evolution in enumerate(chain_data["evolves_to"], start=2):
                process_evolution(evolution, i)
    
    return evolution_list


async def get_evo_details(officialDexNumber):
    try:
        getEvoDetails = await get_evolution_data_from_pokeapi(officialDexNumber)
        evoDetails = getEvoDetails.get("evolution_details", {}).get(
                        "chain", None
                    )
    except Exception as e:
        print(f"Failed to retrieve pokeapi data for {officialDexNumber}: {e}")
        evoDetails = None
    return evoDetails

async def get_and_parse_evo(dex):
    poke_api_evo_chain = await get_evo_details(dex)
    evo_list = parse_evolution_chain(poke_api_evo_chain)
    return evo_list


# Corrects name of pokemon so it can be successfully found in pokeapi
def correct_pokemon_name(p):
    """
    Corrects the name of the given Pokemon to match the name as used in the scraperData/pokelocation.json file.
    This is necessary because some Pokemon have special characters, or have names that are different in the English version of Borrius.
    :param pokemon: The name of the Pokemon that needs to be corrected.
    :return: The corrected name of the Pokemon.
    """
    pokemon = p.lower().replace(". ", "-").replace("'", "")
    corrections = {
        "dome fossil": "kabuto",
        "helix fossil": "omanyte",
        "claw fossil": "anorith",
        "root fossil": "lileep",
        "skull fossil": "cranidos",
        "armor fossil": "shieldon",
        "cover fossil": "tirtouga",
        "plume fossil": "archen",
        "jaw fossil": "tyrunt",
        "sail fossil": "amaura",
        "old amber": "aerodactyl",
        "galarian slowpoke": "slowpoke-galar",
        "galarian darmanitan": "darmanitan-galar-standard",
        "galarian ": lambda x: x.replace("galarian ", "") + "-galar",
        "hisuian ": lambda x: x.replace("hisuian ", "") + "-hisui",
        "alolan ": lambda x: x.replace("alolan ", "") + "-alola",
        "indeedee\u2642": "indeedee-male",
        "indeedee\u2640": "indeedee-female",
        "flabe\u0301be\u0301": "flabebe",
        "flab\u00e9b\u00e9": "flabebe",
        "nidoran\u2642": "nidoran-m",
        "nidoran\u2640": "nidoran-f",
        "basculin": "basculin-red-striped",
        "enamorus": "enamorus-incarnate",
        "morpeko": "morpeko-full-belly",
        "eiscue": "eiscue-ice",
        "minior": "minior-red-meteor",
        "oricorio": "oricorio-baile",
        "pumpkaboo": "pumpkaboo-average",
        "gourgeist": "gourgeist-average",
        "wormadam": "wormadam-plant",
        "meowstic": "meowstic-male",
        "wishiwashi": "wishiwashi-solo",
        "lycanroc": "lycanroc-midday",
        "darmanitan": "darmanitan-standard",
        "deoxys": "deoxys-normal",
        "shaymin": "shaymin-land",
        "keldeo": "keldeo-ordinary",
    }
    for key, value in corrections.items():
        if key in pokemon:
            if callable(value):
                return value(pokemon)
            else:
                return value
    return pokemon


# Creates a pokemon Location object (with empty location array) for each pokemon (both normal and special encounters)
async def initialise_pokemon_location_template(location_data_list):
    with open("scraperData/borrius_pokedex_data.json", "r") as file:
        data = json.load(file)
        # missing_pokemon = get_special_encounter_pokemon()

        for pokemon in data[0]["pokemon"]:
            location_data_list.append(
                {
                    "pokemon": pokemon["name"].lower(),
                    "locationData": [],
                }
            )

        # for mp in missing_pokemon:
        #     location_data_list.append(
        #         {
        #             "pokemon": mp.lower(),
        #             "locationData": [],
        #         }
        #     )


# checks current borrius pokedex data and compares it to the pokemon in the location data, any pokemon that are in the location data but not the borrius pokedex data are special encounters. 
# returns an array of pokemon that are special encoutners.
def get_special_encounter_pokemon():
    try:
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

        sortedResults = []

        for pn in results:
            pokemon_name = pn
            if pokemon_name in [
                "super rod",
                "good rod",
                "old rod",
                "special encounter",
            ]:
                continue
            sortedResults.append(correct_pokemon_name(pokemon_name.rstrip()))

        return [name.lower() for name in sortedResults]

    except Exception as e:
        print(f"Failed to retrieve missing pokemon data: {e}")


# Retrieves pokemondata from pokeapi to fill gaps
async def get_pokemon_api_data_gaps(pokemon):
    async with aiohttp.ClientSession() as session:
        try:
            pokeapi_species = await session.get(
                f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
            )
            data = await pokeapi_species.json()
            return data
        except Exception as e:
            print(f"Failed to retrieve data from PokeAPI: {e}")


async def get_missing_pokemon_data():
    missingPokemon = get_special_encounter_pokemon()
    missingPokemon = [name for name in missingPokemon]

    pokemonReturned = {}

    tasks = [get_pokemon_api_data_gaps(name) for name in missingPokemon]
    results = await asyncio.gather(*tasks)

    for pokemonData in results:
        try:
            if pokemonData is not None:
                pokemon_name = pokemonData["name"]
                pokemon_id = pokemonData["id"]
                pokemonReturned[pokemon_name] = pokemon_id
        except Exception as e:
            print(f"Failed to retrieve data from PokeAPI: {e}")

    return sorted(list(pokemonReturned.values()), key=lambda x: x)


async def get_pokemon_names_from_unbound_pokedex():
    page = "https://www.pokemonunboundpokedex.com/borrius/"
    
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch_page(session, page)
            soup = BeautifulSoup(html, "html.parser")

            pokemon_name = soup.find_all("button", class_="btn")
            
            pokemon_name_list = [x.text for x in pokemon_name]
            
            return pokemon_name_list
        except Exception as e:
            print(f"Failed to retrieve name data from Unbound Pokedex: {e}")


async def get_pokemon_index_from_name(pokemon_name):
    corrected_pokemon_name = correct_pokemon_name(pokemon_name)
    async with aiohttp.ClientSession() as session:
        try:
            pokeapi_response = await session.get(
                f"https://pokeapi.co/api/v2/pokemon/{corrected_pokemon_name}"
            )
            data = await pokeapi_response.json()
            pokemon_id = data["id"]
            return pokemon_id
        except Exception as e:
            print(f"Failed to retrieve data from PokeAPI: {e}")


async def get_pokemon_indexes_from_list(pokemon_list):
    index_list = []
    
    try:
        for pokemon in pokemon_list:
            index_list.append(await get_pokemon_index_from_name(pokemon))
        return index_list
    except Exception as e:
        print(f"Failed to retrieve data from PokeAPI: {e}")
