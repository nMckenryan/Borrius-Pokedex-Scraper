import pytest

from helpers import get_special_encounter_pokemon
from index_getter import get_pokemon_indexes


@pytest.mark.asyncio
async def test_get_pokemon_indexes():
    missing_pokemon = get_special_encounter_pokemon()
    indexes = await get_pokemon_indexes()
    assert len(missing_pokemon) == len(indexes)


@pytest.mark.asyncio
async def get_pokemon_index_from_name():
    pokemon_name = "pikachu"
    index = await get_pokemon_index_from_name(pokemon_name)
    assert index == 25