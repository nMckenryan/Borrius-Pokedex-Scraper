import pytest
from termcolor import colored
from mainFunctions.borrius_pokemon_scraper import scrape_pokemon_data
from mainFunctions.helpers import BorriusPokedexHelpers
import datetime

borrius_data = BorriusPokedexHelpers()
borrius_page = borrius_data.borrius_page

pokemonJson =borrius_data.json_header

@pytest.mark.asyncio
async def test_get_all_starters():
    await scrape_pokemon_data(borrius_data.national_page, borrius_data.national_numbers, 0, pokemonJson)
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
async def test_scrape_pokemon_data_borrius_first():
    await scrape_pokemon_data(borrius_page, [1], 1, pokemonJson)
    firstPokemon = pokemonJson[0].get("pokemon")[0]
    
    assert firstPokemon.get("name") == 'snorunt'
    assert firstPokemon.get("id") == 361
    assert firstPokemon.get("abilities") != []
    assert firstPokemon.get("moves") != []
    assert firstPokemon.get("location") != ""
    assert firstPokemon.get("types") != []
    assert firstPokemon.get("evolutionChain") != []
    assert firstPokemon.get("sprites") != []
    assert firstPokemon.get("stats") != []

@pytest.mark.asyncio
async def test_scrape_pokemon_data_check_all_generated():
    await scrape_pokemon_data(borrius_page, borrius_data.borrius_numbers, 1, pokemonJson)
    assert(len(pokemonJson[0].get("pokemon")) == 494)

@pytest.mark.asyncio
async def test_scrape_pokemon_data_check_null_checks():
    await scrape_pokemon_data(borrius_page, borrius_data.borrius_numbers, 1, pokemonJson)
    
    for pokemon in pokemonJson[0].get("pokemon"):
        try:
            assert pokemon.get("id") is not None
            assert pokemon.get("name") != ''
            assert pokemon.get("abilities") != []
            assert pokemon.get("moves") != []
            assert pokemon.get("location") != []
            assert pokemon.get("types") != []
            assert pokemon.get("evolutionChain") != []
            assert pokemon.get("sprites") != []
            assert pokemon.get("stats") is not None
        except Exception as e:
            print(
                colored(
                    f"ERROR: Data incomplete for: {pokemon.get('name')} - {e}",
                    "red",
                ),
            )
            
