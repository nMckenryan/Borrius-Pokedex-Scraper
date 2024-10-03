import pytest
from borrius_location_scraper import (
    correctPokemonName,
    getFullBorriusPokemonNames,
    getGrassCaveLocations,
)


@pytest.mark.asyncio
async def test_correctPokemonName():
    result = correctPokemonName("Venusaur")
    assert result == "venusaur"


@pytest.mark.asyncio
async def test_correctPokemonName_fossil():
    result = correctPokemonName("Dome Fossil")
    assert result == "kabuto"


@pytest.mark.asyncio
async def test_getBorriusPokemonNames():
    result = []
    await getFullBorriusPokemonNames(result)
    assert isinstance(result, list)
    assert len(result) == 901


@pytest.mark.asyncio
async def test_getGrassCaveLocations():
    result = []
    await getGrassCaveLocations(result)
    assert isinstance(result, list)
    assert len(result) > 0


# @pytest.mark.asyncio
# async def test_getSurfLocations():
#     result = await getSurfLocations()
#     assert isinstance(result, list)
#     assert len(result) > 0


# @pytest.mark.asyncio
# async def test_getFishingLocations():
#     result = await getFishingLocations()
#     assert isinstance(result, list)
#     assert len(result) > 0


# @pytest.mark.asyncio
# async def test_fillInEvolutionGaps():
#     result = await fillInEvolutionGaps()
#     assert isinstance(result, list)
#     assert len(result) > 0


# @pytest.mark.asyncio
# async def test_printLocationJson():
#     result = await printLocationJson()
#     assert result is None
#     assert os.path.exists("scraperData/locationData.json")
