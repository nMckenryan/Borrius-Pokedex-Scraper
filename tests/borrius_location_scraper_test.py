import pytest
from borrius_location_scraper import getGrassCaveLocations, getFishingLocations,\
    getSurfLocations, fillInEvolutionGaps, printLocationJson
from unittest.mock import patch, mock_open
import json
from unittest import mock

@pytest.mark.asyncio
async def test_getGrassCaveLocations():
    locationDataList = []
    
    await getGrassCaveLocations(locationDataList)

    assert len(locationDataList) == 363
    assert locationDataList[0]["pokemon"] == "snorunt"
    assert len(locationDataList[0]["locationData"]) == 2
    assert locationDataList[0]["locationData"][0] == {"location": "Route 1", "encounterMethod": "Grass/Cave", "timeOfDay": "All Day", "isSpecialEncounter": 0}


@pytest.mark.asyncio
async def test_getFishingLocations():
    locationDataList = []
    
    await getFishingLocations(locationDataList)

    assert len(locationDataList) == 75
    assert locationDataList[0]["pokemon"] == "shellder"
    assert len(locationDataList[0]["locationData"]) == 27
    assert locationDataList[0]["locationData"][0] == {'location': 'Route 2', 'encounterMethod': 'Good Rod',  'timeOfDay': 'All Day', 'isSpecialEncounter': 0}
    
    
@pytest.mark.asyncio
async def test_getSurfLocations():
    locationDataList = []
    
    await getSurfLocations(locationDataList)

    assert len(locationDataList) == 53
    assert locationDataList[0]["pokemon"] == "Tentacool"
    assert len(locationDataList[0]["locationData"]) == 23
    assert locationDataList[0]["locationData"][0] == {'location': 'Route 2', 'encounterMethod': 'Surfing', 'timeOfDay': 'All Day', 'isSpecialEncounter': 0}
    
# @pytest.mark.asyncio
# async def test_fillInEvolutionGaps():
#     locationDataList = [{"pokemon": "ivysaur", "locationData": []}]
    
#     fillInEvolutionGaps(locationDataList)

#     assert len(locationDataList[0]["locationData"]) == 1
#     assert locationDataList[0]["locationData"][0] == {
#         "location": "Obtained as an egg randomly from the Magnolia Café Egg Lady",
#         "encounterMethod": "Evolution",
#         "timeOfDay": "All Day",
#         "isSpecialEncounter": 0,
#     }

# @pytest.mark.asyncio
# async def test_printLocationJson(tmp_path):
#     locationDataList = [{"pokemon": "pikachu", "locationData": [{"location": "route 1", "encounterMethod": "Grass/Cave", "timeOfDay": "All Day", "isSpecialEncounter": 0}]}]
#     with patch('borrius_location_scraper.json.dump', autospec=True) as mock_json_dump:
#         with patch('borrius_location_scraper.open', mock_open()) as mock_open:
#             await printLocationJson()
#             mock_open.assert_called_once_with(str(tmp_path / "scraperData/locationData.json"), "w")
#             mock_json_dump.assert_called_once_with(locationDataList, mock.ANY, indent=4)

