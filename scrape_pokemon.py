import requests
from bs4 import BeautifulSoup

import json

for i in range(1, 494):

    # Search thru all 494 pokemon in the Pokemon Unbound dex

    URL = "https://www.pokemonunboundpokedex.com/borrius/" + str(i)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    print("Borrius Pokemon\n==============================\n")

    top_card = soup.find_all(
        "div", class_="card-body"
    )

    for p_element in top_card:

        # DEX AND NAMES - first row
        dex_number = p_element.find("h3", class_="card-title text-5xl").text.strip().replace("Dex Num: ", "")
        name = p_element.find("h3", class_="card-title text-4xl").text.strip().replace("Name: ", "")
        
        first_card_table = p_element.find("div", class_="grid grid-cols-3")
        
        # Type, Catchrate, Gender, Abilities, Weight, Height
        statBoxes = first_card_table.find_all(
            "p", class_="text-3xl font-bold", limit=6
        )

        
        type = statBoxes[0].text.strip()
        catchRate = statBoxes[1].text.strip()
        gender = statBoxes[2].text.strip()
        abilities = statBoxes[3].text.strip()
        
        weight_split = statBoxes[4].text.strip().split(" ")
        
        weight_metric = weight_split[0].replace("\u00a0", "")
        weight_imperial = weight_split[1].replace("\u00a0", "").replace('(', '').replace(')', '')
        
        height_split = statBoxes[5].text.strip().split(" ")

        height_metric = height_split[0].replace("\u00a0", "")
        height_imperial = height_split[1].replace("\u2032", "'").replace("\u2033", "'").replace('(', '').replace(')', '')
        
        
       
        pokemon_data = {
            "pokemon_index": dex_number,
            "name": name,
            "type": type,
            "catchRate": catchRate,
            "gender": gender,
            "abilities": abilities,
            "weight": {
                "imperial": weight_imperial,
                "metric": weight_metric,
            },
            "height": {
                "imperial": height_imperial,
                "metric": height_metric,
            },
        }
        
        # Convert the dictionary to JSON
        pokemon_json = json.dumps(pokemon_data, indent=4)   

        # Print the JSON output
        print(pokemon_json)
        

    
        
       

