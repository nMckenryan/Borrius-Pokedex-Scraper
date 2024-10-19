import pytest

from borrius_location_scraper import fill_in_evolution_gaps, get_grasscave_locations,\
    get_fishing_locations, get_surf_locations


@pytest.mark.asyncio
async def test_get_grasscave_locations():
    locationDataList = []
    
    await get_grasscave_locations(locationDataList)

    assert len(locationDataList) == 363
    assert locationDataList[0]["pokemon"] == "snorunt"
    assert len(locationDataList[0]["locationData"]) == 2
    assert locationDataList[0]["locationData"][0] == {"location": "Route 1", "encounterMethod": "Grass/Cave", "timeOfDay": "All Day", "isSpecialEncounter": 0}


@pytest.mark.asyncio
async def test_get_fishing_locations():
    locationDataList = []
    
    await get_fishing_locations(locationDataList)

    assert len(locationDataList) == 75
    assert locationDataList[0]["pokemon"] == "shellder"
    assert len(locationDataList[0]["locationData"]) == 27
    assert locationDataList[0]["locationData"][0] == {'location': 'Route 2', 'encounterMethod': 'Good Rod',  'timeOfDay': 'All Day', 'isSpecialEncounter': 0}
    
    
@pytest.mark.asyncio
async def test_get_surf_locations():
    locationDataList = []
    
    await get_surf_locations(locationDataList)

    assert len(locationDataList) == 53
    assert locationDataList[0]["pokemon"] == "Tentacool"
    assert len(locationDataList[0]["locationData"]) == 23
    assert locationDataList[0]["locationData"][0] == {'location': 'Route 2', 'encounterMethod': 'Surfing', 'timeOfDay': 'All Day', 'isSpecialEncounter': 0}
    
@pytest.mark.asyncio
async def test_fill_in_evolution_gaps():
    locationDataList = [{"pokemon": "pupitar", "locationData": []}]
    get_surf_locations(locationDataList)
    
    fill_in_evolution_gaps(locationDataList)

    assert len(locationDataList[0]["locationData"]) == 1
    assert locationDataList[0]["locationData"][0] == {'location': 'Evolve Larvitar (Lv. 30)', 'encounterMethod': 'Evolution', 'timeOfDay': 'All Day', 'isSpecialEncounter': 0}





# @pytest.mark.asyncio
# async def test_print_location_json(tmp_path, mocker):
#     mockList = [{
#         "pokemon": "pupitar",
#         "locationData": [
#             {"location": "Route 1", "encounterMethod": "Grass/Cave", "timeOfDay": "All Day", "isSpecialEncounter": 0},
#         ],
#     }]
    
#     mocker.patch('borrius_location_scraper.get_grasscave_locations', return_value=mockList)
#     mocker.patch('borrius_location_scraper.get_surf_locations', return_value=mockList)
#     mocker.patch('borrius_location_scraper.get_fishing_locations', return_value=mockList)
#     mocker.patch('borrius_location_scraper.fill_in_evolution_gaps', return_value=mockList)
    
#     # Call the functions that populate the location data list
#     await get_grasscave_locations(mockList)
#     await get_surf_locations(mockList)
#     await get_fishing_locations(mockList)
#     fill_in_evolution_gaps(mockList)
    
#     assert len(mockList) == 475
    
# @pytest.mark.asyncio
# def test_print_json_file(tmp_path, mocker):
#     mockList = [{"pokemon": "pupitar", "locationData": [{"location": "Route 1", "encounterMethod": "Grass/Cave", "timeOfDay": "All Day", "isSpecialEncounter": 0}]}]
# INFINITE LOOP NEED 2 FIX    
#     mocker.patch('builtins.open')
#     mocker.patch('json.dump')
    
#     # Call the function to print json file
#     print_json_file(mockList)

#     # Assert that open was called with the correct filename and mode
#     open.assert_called_once_with("scraperData/locationData.json", 'w')
    
#     # Assert that json.dump was called with the correct arguments
#     json.dump.assert_called_once_with(mockList, open(), indent=4)
