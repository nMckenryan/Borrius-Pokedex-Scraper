import pytest
from one_off_functions.index_getter import get_pokemon_indexes, get_pokemon_index_from_name

@pytest.mark.asyncio
async def test_get_pokemon_index_from_name():
    result = await get_pokemon_index_from_name("pikachu")
    assert result == 25
    
@pytest.mark.asyncio
async def test_get_pokemon_indexes_clobbopus():
    result = await get_pokemon_indexes()
    assert result[0] == 852
