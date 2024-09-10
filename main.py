import json
from fastapi import FastAPI

app = FastAPI()


@app.get("/borrius_pokemon/info")
async def read_info():
    with open("borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("info")
    return {"borrius_pokemon": pokemon_data}


@app.get("/borrius_pokemon/")
async def read_pokemon():
    with open("borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("pokemon")
    return {"borrius_pokemon": pokemon_data}


@app.get("/borrius_pokemon/{pokemon_id}")
async def read_pokemon(pokemon_id: int):
    with open("borrius_pokedex_data.json") as json_file:
        pokemon_data = json.load(json_file)[0].get("pokemon")
    try:
        return {"borrius_pokemon": pokemon_data[pokemon_id - 1]}
    except IndexError:
        return {"error": "Invalid pokemon ID"}
