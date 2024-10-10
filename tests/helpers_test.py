import pytest

from helpers import get_full_borrius_pokemon_names, get_missing_pokemon_indexes, correct_pokemon_name, get_missing_pokemon_list, get_pokeapi_data, get_pokemon_locations, read_location_data_json

    
@pytest.mark.asyncio
async def test_check_for_forbidden_names():
    location_list = []

    await read_location_data_json(location_list)
    
    for pokemon in location_list:
        assert pokemon["pokemon"] != "super rod"
        assert pokemon["pokemon"] != "old rod"
        assert pokemon["pokemon"] != "good rod"

@pytest.mark.asyncio
async def test_getMissingPokemonIndexes():
    missing_pokemon_indexes = await get_missing_pokemon_indexes()
    
    assert len(missing_pokemon_indexes) == 517
    
@pytest.mark.asyncio
async def test_getPokemonLocations():
    location_list = []

    pokemon_location = get_pokemon_locations("snorunt", location_list)
    assert pokemon_location[0]['location'] == 'Route 1'
    assert pokemon_location[1]['location'] == 'Route 8'


@pytest.mark.asyncio
async def test_correctPokemonName():
    result = correct_pokemon_name("Venusaur")
    assert result == "venusaur"


@pytest.mark.asyncio
async def test_correctPokemonName_fossil():
    result = correct_pokemon_name("Dome Fossil")
    assert result == "kabuto"


@pytest.mark.asyncio
async def test_getFullBorriusPokemonNames():
    result = []
    await get_full_borrius_pokemon_names(result)
    assert isinstance(result, list)
    assert len(result) == 901


@pytest.mark.asyncio
async def test_get_poke_api_data():
    """Test that we can get data from the Pokemon API"""
    data = await get_pokeapi_data("pikachu")
    assert isinstance(data, dict)
    assert data["name"] == "pikachu"
    assert data["id"] == 25


def test_get_missing_pokemon_list():
    """Test that we can get a list of missing Pokemon names"""
    missing_pokemon = get_missing_pokemon_list()
    assert isinstance(missing_pokemon, list)
    assert missing_pokemon is not None
    assert len(missing_pokemon) == 398
