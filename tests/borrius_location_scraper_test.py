# import os
# import pytest

# from borrius_location_scraper import fillInEvolutionGaps, getFishingLocations, getGrassCaveLocations, getSurfLocations, printLocationJson

# @pytest.mark.asyncio
# async def test_getGrassCaveLocations():
#     result = []
#     await getGrassCaveLocations(result)
#     assert isinstance(result, list)
#     assert len(result) > 0


# @pytest.mark.asyncio
# async def test_getSurfLocations():
#     result = []
#     await getSurfLocations(result)
#     assert isinstance(result, list)
#     assert len(result) > 0


# @pytest.mark.asyncio
# async def test_getFishingLocations():
#     result = []
#     await getFishingLocations(result)
#     assert isinstance(result, list)
#     assert len(result) > 0


# @pytest.mark.asyncio
# async def test_fillInEvolutionGaps():
#     result = []
#     await fillInEvolutionGaps(result)
#     assert isinstance(result, list)
#     assert len(result) > 0


# @pytest.mark.asyncio
# async def test_printLocationJson():
#     result = []
#     await printLocationJson()
#     assert result == []
#     assert os.path.exists("scraperData/locationData.json")

