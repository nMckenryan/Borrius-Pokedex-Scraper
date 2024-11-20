import time
import pytest
from termcolor import colored
from mainFunctions.borrius_pokemon_scraper import scrape_pokemon_data
from mainFunctions.helpers import BorriusPokedexHelpers, get_missing_pokemon_data
import datetime


borrius_data = BorriusPokedexHelpers()

starter_json = borrius_data.json_header
borrius_dex_json = borrius_data.json_header
pokemon_json = []

@pytest.fixture(scope="module")
async def setup():

    spn = await get_missing_pokemon_data()
    
    await scrape_pokemon_data(borrius_data.national_page, borrius_data.national_numbers, 0, starter_json)
    await scrape_pokemon_data(borrius_data.borrius_page, borrius_data.borrius_numbers, 10, borrius_dex_json)

    pokemon_json = starter_json[0]["pokemon"].copy()
    pokemon_json.extend(borrius_dex_json[0]["pokemon"])

    
@pytest.mark.asyncio
async def test_scrape_pokemon_data_borrius_first(setup):
    await setup
    firstPokemon = borrius_dex_json[0].get("pokemon")[10]
    
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
async def test_get_all_starters(setup):
    for pokemon in starter_json[0].get("pokemon"):
        assert pokemon.get("name") != ""
        assert pokemon.get("description") != ""
        assert pokemon.get("abilities") != []
        assert pokemon.get("moves") != []
        assert pokemon.get("location") != ""
        assert pokemon.get("types") != []
        assert pokemon.get("evolutionChain") != []
        assert pokemon.get("sprites") != []
        assert pokemon.get("stats") != []

# ~180 in total
@pytest.mark.asyncio
async def test_get_all_special_encounters(setup):
    for pokemon in pokemon_json[0].get("pokemon"):
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
async def test_scrape_pokemon_data_check_all_generated_in_order(setup):
    expected_order = borrius_data.national_numbers + list(borrius_data.borrius_numbers)
    
    assert(len(pokemon_json[0].get("pokemon")) == 503)
    assert [pokemon["id"] for pokemon in pokemon_json[0]["pokemon"]] == expected_order


@pytest.mark.asyncio
async def test_scrape_pokemon_data_check_null_checks(setup):
    for pokemon in pokemon_json[0].get("pokemon"):
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
            