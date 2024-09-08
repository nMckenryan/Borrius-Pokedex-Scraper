import datetime
import time
import requests
import json
from bs4 import BeautifulSoup
import re

currentTime = datetime.datetime.now()
pokemonJson = [
    {
        "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
        "dataPulledOn": currentTime,
    }
]

start = time.time()

print(f"Started creating Borrius Pokedex Json file at {currentTime}")
print("Creating Json file...")

# Loop through all 494 in the borrius dex
for i in range(1, 494):
    page = requests.get(f"https://www.pokemonunboundpokedex.com/borrius/{i}")
    soup = BeautifulSoup(page.content, "html.parser")
    top_card = soup.find("div", class_="card-body")
    stats_table = soup.find("table", class_="table table-zebra");
    
    learned_move_table_parent = soup.find(lambda tag: tag.name == "div" and "Level Up Moves" in tag.decode(), class_="overflow-x-auto col-span-6 col-start-2 justify-stretch");
    
    tmhm_move_table_parent = soup.find(lambda tag: tag.name == "div" and "Level Up Moves" in tag.decode(), class_="overflow-x-auto col-span-6 col-start-2 justify-stretch");
    
    move_table = learned_move_table_parent.find("tbody");
    tmhm_move_table = tmhm_move_table_parent.find("tbody");
    
    moves = []
    for row in move_table.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) > 0:
            retrieved_move = {
                "level": columns[0].text.strip(),
                "move": columns[1].text.strip(),
                "type": columns[2].text.strip(),
                "category": columns[3].text.strip(),
                "power": columns[4].text.strip().replace("\u2014", "-"),
                "accuracy": columns[5].text.strip().replace("\u2014", "-"),
            }
            moves.append(retrieved_move)
            
    tmhm_moves = []
    for row in tmhm_move_table.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) > 0:
            retrieved_tm_move = {
                "move": columns[1].text.strip(),
                "type": columns[2].text.strip(),
                "category": columns[3].text.strip(),
                "power": columns[4].text.strip().replace("\u2014", "-"),
                "accuracy": columns[5].text.strip().replace("\u2014", "-"),
            }
            tmhm_moves.append(retrieved_tm_move)

    gender_data = re.findall(r'\d+', top_card.find_all("p", class_="text-3xl font-bold")[2].text.strip()) 
    isGenderLess = len(gender_data) == 0
    if(isGenderLess):
        gender_data = [0, 0]
    
    stats_table_output = {}
    stats = ["hp", "attack", "defense", "specialAttack", "specialDefense", "speed"]
    
    for i, stat in enumerate(stats):
        stats_table_output[stat] = {
            "avg": int(stats_table.find_all("td")[i*3].text.strip()),
            "min": int(stats_table.find_all("td")[i*3+1].text.strip()),
            "max": int(stats_table.find_all("td")[i*3+2].text.strip()),
        }
    
    pokemon_data = {
        "pokemon_index": int(top_card.find("h3", class_="card-title text-5xl").text.strip().replace("Dex Num: ", "")),
        "name": top_card.find("h3", class_="card-title text-4xl").text.strip().replace("Name: ", ""),
        "type": top_card.find_all("p", class_="text-3xl font-bold")[0].text.strip(),
        "catchRate": {
            "value": float(top_card.find_all("p", class_="text-3xl font-bold")[1].text.strip().replace("%", "").split(" ")[1]),
            "percentage": top_card.find_all("p", class_="text-3xl font-bold")[1].text.strip().split(" ")[0]
        },
        "gender": {
            "isGenderless": top_card.find_all("p", class_="text-3xl font-bold")[2].text.strip() == "Genderless",
            "maleChance": gender_data[0],
            "femaleChance": gender_data[1]
        },
        "abilities": top_card.find_all("p", class_="text-3xl font-bold")[3].text.strip().split(", "),
        "weight": {
            "imperial": top_card.find_all("p", class_="text-3xl font-bold")[4].text.strip().split(" ")[1].replace("\u00a0", "").replace('(', '').replace(')', ''),
            "metric": top_card.find_all("p", class_="text-3xl font-bold")[4].text.strip().split(" ")[0].replace("\u00a0", ""),
        },
        "height": {
            "imperial": top_card.find_all("p", class_="text-3xl font-bold")[5].text.strip().split(" ")[1].replace("\u2032", "'").replace("\u2033", "'").replace('(', '').replace(')', ''),
            "metric": top_card.find_all("p", class_="text-3xl font-bold")[5].text.strip().split(" ")[0].replace("\u00a0", ""),
        },
        "stats": stats_table_output,
        "learnedMoves": moves,
        "tmhmMoves": tmhm_moves
    }
    
    pokemonJson.append(pokemon_data);
    
try:
    with open(f'pokemon_unbound_pokedex.json', 'w') as fp:
        json.dump(pokemonJson, fp, indent=4)
    end = time.time()
    print(f"pokemon_unbound_pokedex.json successfully create in {end - start} seconds")
except Exception as e:
    end = time.time()
    length = end - start;
    print(f"Json Generation Failed at: {length} seconds ({length / 60} minutes). An error occurred: {e}")


