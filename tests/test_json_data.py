import json
import pytest

@pytest.fixture(autouse=True)
def setup():
    with open("scraperData/borrius_pokedex_data.json") as f:
        global data
        data = json.load(f)


@pytest.mark.asyncio
async def test_borrius_pokedex_json_has_all_pokemon():
    assert len(data[0]["pokemon"]) == 503


@pytest.mark.asyncio
async def test_borrius_pokedex_json_has_full_data():
    for pokemon in data[0]["pokemon"]:
        assert "abilities" in pokemon
        assert "game_indices" in pokemon
        assert "id" in pokemon
        assert "name" in pokemon
        assert "types" in pokemon
        assert "weight" in pokemon
        assert "height" in pokemon
        assert "stats" in pokemon
        assert "moves" in pokemon
        assert "evolution_chain" in pokemon
        assert "gender" in pokemon
        assert "capture_rate" in pokemon
        assert "locations" in pokemon


@pytest.mark.asyncio
async def test_borrius_pokedex_json_check_abilities():

    for pokemon in data[0]["pokemon"]:
        assert "abilities" in pokemon

        for ability in pokemon["abilities"]:
            assert "ability_name" in ability
            assert "slot" in ability


@pytest.mark.asyncio
async def test_borrius_pokedex_json_check_index():
    for pokemon in data[0]["pokemon"]:
        assert "game_indices" in pokemon
        assert isinstance(pokemon["game_indices"]["unbound_index"], int)
        assert isinstance(pokemon["game_indices"]["official_index"], int)


@pytest.mark.asyncio
async def test_borrius_pokedex_json_check_id_name_height_weight():
    #         "height": 60.0,
#         "weight": 7200.0,
#         "id": 246,
#         "name": "larvitar",
    for pokemon in data[0]["pokemon"]:
        assert pokemon["id"] > 0
        assert pokemon["weight"] > 0
        assert pokemon["name"] is not None
            
            
@pytest.mark.asyncio
async def test_borrius_pokedex_json_check_stats():
    for pokemon in data[0]["pokemon"]:
        assert all(
            stat["base_stat"] > 0
            for stat in pokemon["stats"].values()
        )


@pytest.mark.asyncio
async def test_borrius_pokedex_json_check_locations():
    for pokemon in data[0]["pokemon"]:
        assert "locations" in pokemon
        for location in pokemon["locations"]:
            assert "location" in location and location["location"] != ""
            assert "encounterMethod" in location and location["encounterMethod"] != ""
            assert "timeOfDay" in location and  location["timeOfDay"] != ""
            assert "isSpecialEncounter" in location and location["isSpecialEncounter"] == 0 or location["isSpecialEncounter"] == 1

# @pytest.mark.asyncio
# async def test_borrius_pokedex_json_check_moves():
#     for pokemon in data[0]["pokemon"]:
#         assert "moves" in pokemon
#         assert len(pokemon["moves"]) > 0, f"ERROR: {pokemon['name']} has a no moves"
#         for move in pokemon["moves"]:
#             assert move is not None
#             assert "move" in move and move["move"] is not None
#             assert "name" in move["move"] and move["move"]["name"] != ""
#             assert "type" in move and move["type"] != "", f"ERROR: {pokemon['name']} has a no moves"
#             assert "category" in move and move["category"] in ["Status", "Physical", "Special"]
#             assert "power" in move and (move["power"] == "-" or int(move["power"]) > 0)
#             assert "version_group_details" in move and len(move["version_group_details"]) > 0
#             details = move["version_group_details"][0]
#             assert details is not None
#             assert details["level_learned_at"] >= 0
#             assert details["move_learn_method"] is not None
#             assert details["move_learn_method"]["name"] in ["level-up/tm", "machine", "level-up"]
#        
# "locations": [
#           {
#             "location": "Starter\nCan be acquired either in the Shadow Base Warehouse or your rival\u2019s house in Post-game",
#             "encounterMethod": "Evolution",
#             "timeOfDay": "All Day",
#             "isSpecialEncounter": 0
#           }
#         ],
