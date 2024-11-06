

import re

import aiohttp
from mainFunctions.helpers import get_evolution_data_from_pokeapi
import ast


def get_name(top_card):
    retrievedName = str(
        top_card.find("h3", class_="card-title text-4xl")
        .text.strip()
        .replace("Name: ", ""),
    )
    return retrievedName


def get_types(top_card):
    tA = top_card.find_all("p", class_="text-3xl font-bold")[0].text.strip()
    typeArray = ast.literal_eval(tA)
    return typeArray 


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


def get_weight_height(top_card):
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
    
    return weightInHectograms, heightInDecimetres


def get_abilities(top_card):
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
    return abilities


def get_stats(stats_table):
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
        
    return stats_table_output


def get_gender_data(top_card):
    gender_data = re.findall(
                    r"\d+",
                    top_card.find_all("p", class_="text-3xl font-bold")[2].text.strip(),
                )
    isGenderLess = len(gender_data) == 0
    if isGenderLess:
        gender_data = [0, 0]
    return gender_data


def get_moves_for_pokemon(move_table):
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
                        "power": columns[4].text.strip().replace("\u2014", "-"),
                        "accuracy": columns[5].text.strip().replace("\u2014", "-"),
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
            
    return moves


async def get_missing_moves_from_pokeapi(pokemon_number) -> list:
    returned_moves = []
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}') as response:
                missing_moves = await response.json()
                
                ml  = missing_moves["moves"]
                
                for move in ml:
                    move_link = f"https://pokeapi.co/api/v2/move/{move['move']['name']}/"
                    mg = await session.get(move_link)
                    move_get = await mg.json()
                    
                    returned_moves.append({
                            "name": move_get["name"],
                            "type": move_get["type"]["name"],
                            "category": move_get["damage_class"]["name"],
                            "power": move_get["power"],
                            "accuracy": move_get["accuracy"],
                    })

            return returned_moves
            
        except Exception as e:
            print(
                colored(
                    f"Failed to retrieve missing move data {pokemon_number} from PokeAPI: {e}",
                    "red",
                ),
            )


def get_tmhm_moves(tmhm_move_table):
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
            
    return tmhm_moves


def merge_moves(moves, tmhm_moves):
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
                combined_move["version_group_details"][0]["move_learn_method"]["name"] = "level-up/tm"
                break
    return combined_moves