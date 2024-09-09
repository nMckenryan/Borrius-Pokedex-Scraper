import json
from fastapi import FastAPI
from borrius_pokemon_scraper import compile_pokedex, createPokemonJson

app = FastAPI()

@app.get("/pokemon/")
async def read_pokemon():
    with open('borrius_pokedex_data.json') as json_file:
        pokemon_data = json.load(json_file)
    return {"pokemon": pokemon_data}

@app.get("/pokemon/{pokemon_id}")
async def read_pokemon(pokemon_id: int):
    with open('borrius_pokedex_data.json') as json_file:
        pokemon_data = json.load(json_file)[1:]
    pokemon = next((p for p in pokemon_data if p["id"] == pokemon_id), None)
    return {"pokemon": pokemon}
