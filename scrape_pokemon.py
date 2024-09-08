import requests
import json
from bs4 import BeautifulSoup

for i in range(1, 494):
    page = requests.get(f"https://www.pokemonunboundpokedex.com/borrius/{i}")
    soup = BeautifulSoup(page.content, "html.parser")
    top_card = soup.find("div", class_="card-body")
    
    
    stats_table = soup.find("table", class_="table table-zebra");
    
    
    
    
    stats_table = {
        "hp": {
            "avg": int(stats_table.find_all("td")[0].text.strip()),
            "min": int(stats_table.find_all("td")[1].text.strip()),
            "max": int(stats_table.find_all("td")[2].text.strip()),
        }, 
        "attack": {
            "avg": int(stats_table.find_all("td")[3].text.strip()),
            "min": int(stats_table.find_all("td")[4].text.strip()),
            "max": int(stats_table.find_all("td")[5].text.strip()),
        }, 
        "defense": {
            "avg": int(stats_table.find_all("td")[6].text.strip()),
            "min": int(stats_table.find_all("td")[7].text.strip()),
            "max": int(stats_table.find_all("td")[8].text.strip()),
        }, 
        "specialAttack": {
            "avg": int(stats_table.find_all("td")[9].text.strip()),
            "min": int(stats_table.find_all("td")[10].text.strip()),
            "max": int(stats_table.find_all("td")[11].text.strip()),
        }, 
        "specialDefense": {
            "avg": int(stats_table.find_all("td")[12].text.strip()),
            "min": int(stats_table.find_all("td")[13].text.strip()),
            "max": int(stats_table.find_all("td")[14].text.strip()),
        },
        "speed": {
            "avg": int(stats_table.find_all("td")[15].text.strip()),
            "min": int(stats_table.find_all("td")[16].text.strip()),
            "max": int(stats_table.find_all("td")[17].text.strip()),
        }
    }
    
    
    pokemon_data = {
        "pokemon_index": top_card.find("h3", class_="card-title text-5xl").text.strip().replace("Dex Num: ", ""),
        "name": top_card.find("h3", class_="card-title text-4xl").text.strip().replace("Name: ", ""),
        "type": top_card.find_all("p", class_="text-3xl font-bold")[0].text.strip(),
        "catchRate": top_card.find_all("p", class_="text-3xl font-bold")[1].text.strip(),
        "gender": top_card.find_all("p", class_="text-3xl font-bold")[2].text.strip(),
        "abilities": top_card.find_all("p", class_="text-3xl font-bold")[3].text.strip(),
        "weight": {
            "imperial": top_card.find_all("p", class_="text-3xl font-bold")[4].text.strip().split(" ")[1].replace("\u00a0", "").replace('(', '').replace(')', ''),
            "metric": top_card.find_all("p", class_="text-3xl font-bold")[4].text.strip().split(" ")[0].replace("\u00a0", ""),
        },
        "height": {
            "imperial": top_card.find_all("p", class_="text-3xl font-bold")[5].text.strip().split(" ")[1].replace("\u2032", "'").replace("\u2033", "'").replace('(', '').replace(')', ''),
            "metric": top_card.find_all("p", class_="text-3xl font-bold")[5].text.strip().split(" ")[0].replace("\u00a0", ""),
        },
        "stats": stats_table
    }
    print(json.dumps(pokemon_data, indent=4))

