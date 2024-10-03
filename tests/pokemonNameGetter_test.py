# test_example.py

import pytest
from pokemonNameGetter import (
    getMissingPokemonData,
    getMissingPokemonList,
    getPokeApiData,
)


@pytest.mark.asyncio
async def test_get_poke_api_data():
    """Test that we can get data from the Pokemon API"""
    data = await getPokeApiData("pikachu")
    assert isinstance(data, dict)
    assert data["name"] == "pikachu"
    assert data["id"] == 25


def test_get_missing_pokemon_list():
    """Test that we can get a list of missing Pokemon names"""
    missing_pokemon = getMissingPokemonList()
    assert isinstance(missing_pokemon, list)
    assert missing_pokemon is not None
    assert len(missing_pokemon) == 398


@pytest.mark.asyncio
async def test_get_missing_pokemon_data():
    """Test that we can get data about missing Pokemon"""
    data = await getMissingPokemonData()
    assert isinstance(data, list)
