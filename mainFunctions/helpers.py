
import asyncio
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

            pokeapi_data = {"evolution_details": evo_data}

            return pokeapi_data
        except Exception as e:
            print(
                colored(
                    f"Failed to retrieve evolution data {officialDexNumber} from PokeAPI: {e}",
                    "red",
                ),
            )

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


async def get_pokemon_indexes_from_list(pokemon_name):
    index_list = []
    
    try:
        for pokemon in pokemon_name:
            index_list.append(await get_pokemon_index_from_name(pokemon))
        return index_list
    except Exception as e:
        print(f"Failed to retrieve data from PokeAPI: {e}")
