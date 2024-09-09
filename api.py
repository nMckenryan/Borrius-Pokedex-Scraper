from fastapi import FastAPI
from borrius_pokemon_scraper import createPokemonJson

app = FastAPI()

@app.get("/pokemon/")
async def read_pokemon():
    pokemon_data = createPokemonJson()
    return {"pokemon": pokemon_data}

@app.get("/pokemon/{pokemon_id}")
async def read_pokemon(pokemon_id: int):
    pokemon_data = createPokemonJson()
    pokemon = next((p for p in pokemon_data if p["id"] == pokemon_id), None)
    return {"pokemon": pokemon}