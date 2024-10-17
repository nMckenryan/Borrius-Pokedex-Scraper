import json
from typing import List
from fastapi import FastAPI
from pip._vendor.typing_extensions import Annotated
from fastapi.param_functions import Query

app = FastAPI()


@app.get("/borrius_pokemon/info")
async def read_info():
    with open("scraperData/borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("info")
    return {"borrius_pokemon": pokemon_data}


@app.get("/borrius_pokemon/")
async def read_pokemon():
    with open("scraperData/borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("pokemon")
    return {"borrius_pokemon": pokemon_data}


@app.get("/borrius_pokemon/{pokemon_id}")
async def read_pokemon_by_id(pokemon_id: int):
    with open("scraperData/borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("pokemon")
    try:
        return {"borrius_pokemon": pokemon_data[pokemon_id - 1]}
    except IndexError:
        return {"error": "Invalid pokemon ID"}
    
@app.get("/borrius_pokemon/name/{pokemon_name}")
async def read_pokemon_by_name(pokemon_name: str):
    with open("scraperData/borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("pokemon")
    try:
        return {"borrius_pokemon": next((pokemon for pokemon in pokemon_data if pokemon["name"].lower() == pokemon_name.lower()), None)}
    except IndexError:
        return {"error": "Invalid pokemon name"}

    
@app.get("/borrius_pokemon/type/{pokemon_type}")
async def read_pokemon_by_type(pokemon_type: str):
    with open("scraperData/borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("pokemon")
    matching_pokemon = [
        pokemon for pokemon in pokemon_data if pokemon_type.capitalize() in pokemon.get("types", [])
    ]
    if matching_pokemon:
        return {"borrius_pokemon": matching_pokemon}
    else:
        return {"error": "No Pokemon found with the given type"}


@app.get("/borrius_pokemon/types/")
async def get_pokemon_by_types(
    type1: str = Query(..., description="First Pokemon type"),
    type2: str = Query(None, description="Second Pokemon type", required=False)
) -> List[dict]:
    with open("scraperData/borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("pokemon")
    
    if(type2 is not None):
        matching_pokemon = [
            pokemon for pokemon in pokemon_data if type1.capitalize() in pokemon.get("types", []) or type1.capitalize() in pokemon.get("types", [])
        ]
    else:
        matching_pokemon = [
            pokemon for pokemon in pokemon_data if type1.capitalize() in pokemon.get("types", [])
        ]
        
    if matching_pokemon:
        return [pokemon for pokemon in matching_pokemon]
    else:
        return {"error": "No Pokemon found with the given type"}