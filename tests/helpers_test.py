import aiohttp 
import pytest
from helpers import get_pokemon_indexes_from_list, get_pokemon_names_from_unbound_pokedex, read_location_data_json, correct_pokemon_name, fetch_page,\
    get_pokemon_locations, get_evolution_data_from_pokeapi,\
    initialise_pokemon_location_template, get_special_encounter_pokemon,\
    get_pokemon_api_data_gaps, get_missing_pokemon_data
from unittest.mock import patch, mock_open
import json

from one_off_functions.index_getter import get_pokemon_index_from_name



@pytest.mark.asyncio
async def test_fetch_page():
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(
            session, "https://www.pokemonunboundpokedex.com/national/1"
        )
        assert html is not None
        assert "Bulbasaur" in html


@pytest.mark.asyncio
async def test_read_location_data_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = await read_location_data_json()
        assert result == [] or result is None

@pytest.mark.asyncio
async def test_read_location_data_json_json_decode_error():
    with patch("builtins.open", mock_open(read_data="not a json")):
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            result = await read_location_data_json()
            assert result == [] or result is None

@pytest.mark.asyncio
async def test_read_location_data_json_success():
    mock_data = [{"pokemon": "bulbasaur", "locationData": []}]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        with patch("json.load", return_value=mock_data):
            result = await read_location_data_json()
            assert result == mock_data

@pytest.mark.asyncio
async def test_check_for_forbidden_names():
    location_list = []

    with patch("helpers.read_location_data_json") as mock_read_location_data_json:
        await mock_read_location_data_json()
    
    for pokemon in location_list:
        assert pokemon["pokemon"] != "super rod"
        assert pokemon["pokemon"] != "old rod"
        assert pokemon["pokemon"] != "good rod"

@pytest.mark.asyncio
def test_get_pokemon_locations():
    location_list = [{"pokemon": "snorunt", "locationData": [{"location": "Route 1"}, {"location": "Route 8"}]},
                     {"pokemon": "glacie", "locationData": []}]
    pokemon_location =  get_pokemon_locations("snorunt", location_list)
    
    assert len(pokemon_location) == 2
    assert pokemon_location[0]['location'] == 'Route 1'
    assert pokemon_location[1]['location'] == 'Route 8'


@pytest.mark.asyncio
async def test_get_evolution_data_from_pokeapi():
    pokemon_number = 1
    result = await get_evolution_data_from_pokeapi(pokemon_number)
    assert 'evolution_details' in result

@pytest.mark.asyncio
async def test_correctPokemonName():
    result = correct_pokemon_name("minior")
    assert result == "minior-red-meteor"


@pytest.mark.asyncio
async def test_correctPokemonName_fossil():
    result = correct_pokemon_name("Dome Fossil")
    assert result == "kabuto"
    
@pytest.mark.asyncio
async def test_correctPokemonName_regional():
    result = correct_pokemon_name("galarian numel")
    assert result == "numel-galar"

@pytest.mark.asyncio
async def test_initialise_pokemon_location_template():
    location_data_list = []

    await initialise_pokemon_location_template(location_data_list)
    assert len(location_data_list) == 503
    assert location_data_list[0]["pokemon"] == "larvitar"
    assert location_data_list[502]["pokemon"] == "hoopa"


@pytest.mark.asyncio
def test_get_special_encounter_pokemon():
    result =  get_special_encounter_pokemon()
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_pokemon_api_data_gaps():
    pokemon = "pikachu"
    result = await get_pokemon_api_data_gaps(pokemon)
    assert result["name"] == pokemon


@pytest.mark.asyncio
async def test_get_missing_pokemon_data():
    result = await get_missing_pokemon_data()
    assert len(result) > 0


@pytest.mark.asyncio
async def test_get_pokemon_names_from_unbound_pokedex():
    pokemon_names = await get_pokemon_names_from_unbound_pokedex()
    assert len(pokemon_names) == 494
    assert pokemon_names[0] == "Snorunt"


@pytest.mark.asyncio
async def test_get_pokemon_index_from_name():
    pokemon_index = await get_pokemon_index_from_name("minior")
    assert pokemon_index == 774
    
@pytest.mark.asyncio
async def test_get_pokemon_indexes_from_list():
    pokemon_indexes = await get_pokemon_indexes_from_list(["minior", "pikachu", "caterpie"])
    assert pokemon_indexes == [774, 25, 10]