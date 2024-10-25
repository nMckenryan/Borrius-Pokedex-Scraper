import pytest
from mainFunctions.borrius_pokemon_scraper import scrape_pokemon_data
from mainFunctions.helpers import BorriusPokedexHelpers
import datetime

borrius_data = BorriusPokedexHelpers()
borrius_page = borrius_data.borrius_page
national_page = "https://www.pokemonunboundpokedex.com/national/"
borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
national_numbers = [246, 247, 248, 374, 375, 376, 443, 444, 445]  # + get_missing_pokemon_indexes(),
borrius_numbers = range(1, 495)
pokemonJson = [
    {
        "info": {
            "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
            "dataPulledOn": str(datetime.datetime.now()),
        },
        "pokemon": [],
    }
]


async def test_get_all_starters():
    await scrape_pokemon_data(national_page, national_numbers, pokemonJson)
    for pokemon in pokemonJson[0].get("pokemon"):
        assert pokemon.get("name") != ""
        assert pokemon.get("description") != ""
        assert pokemon.get("abilities") != []
        assert pokemon.get("moves") != []
        assert pokemon.get("location") != ""
        assert pokemon.get("types") != []
        assert pokemon.get("evolutionChain") != []
        assert pokemon.get("sprites") != []
        assert pokemon.get("stats") != []


@pytest.mark.asyncio
async def test_scrape_pokemon_data_borrius():

    await scrape_pokemon_data(borrius_page, borrius_numbers, 1, pokemonJson)

    assert pokemonJson[0].get("pokemon")[0].get("name") == "snorunt"
    
    for pokemon in pokemonJson[0].get("pokemon"):
        assert pokemon.get("name") != ""
        assert pokemon.get("description") != ""
        assert pokemon.get("abilities") != []
        assert pokemon.get("moves") != []
        assert pokemon.get("location") != ""
        assert pokemon.get("types") != []
        assert pokemon.get("evolutionChain") != []
        assert pokemon.get("sprites") != []
        assert pokemon.get("stats") != []

