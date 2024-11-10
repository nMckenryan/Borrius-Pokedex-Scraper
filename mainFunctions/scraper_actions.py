

import re

import aiohttp
from termcolor import colored
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
            "ability_name": ability,
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
            "effort": 0
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


def get_moves_for_pokemon(move_table, officialDexNumber):
    moves = []
    try:
        for row in move_table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) > 0:
                moves.append(
                    {
                        "name": columns[1].text.strip(),
                        "type": columns[2].text.strip(),
                        "category": columns[3].text.strip(),
                        "power": columns[4].text.strip().replace("\u2014", "-"),
                        "accuracy": columns[5].text.strip().replace("\u2014", "-"),
                        "level_learned_at": columns[0].text.strip(),
                        "method": "level-up"
                    }
                )
    except Exception as e:
        print(f"Error processing move table for pokemon {officialDexNumber}: {e}")
    
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
                            "level_learned_at":  move["version_group_details"][-1]["level_learned_at"],
                            "method":  move["version_group_details"][-1]["move_learn_method"]["name"]
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
                    "name": columns[1].text.strip(),
                    "type": columns[2].text.strip(),
                    "category": columns[3].text.strip(),
                    "power": columns[4].text.strip(),
                    "accuracy": columns[5].text.strip().replace("\u2014", "-"),
                    "level_learned_at": 0,
                    "method": 'machine'
                }
            )
            
    return tmhm_moves


def merge_moves(moves, tmhm_moves):
    
    
    combined_moves = []
    for move in moves:
        for tmhm_move in tmhm_moves:
            if move["name"] == tmhm_move["name"]:
                combined_moves.append(
                    {
                        "name": move["name"],
                        "type": move["type"],
                        "category": move["category"],
                        "power": move["power"],
                        "accuracy": move["accuracy"],
                        "level_learned_at": move["level_learned_at"],
                        "method": "level-up/TM"
                    }
                )
                break
        else:
            combined_moves.append(move)
    for tmhm_move in tmhm_moves:
        if tmhm_move not in combined_moves:
            combined_moves.append(tmhm_move)

    return combined_moves
   
