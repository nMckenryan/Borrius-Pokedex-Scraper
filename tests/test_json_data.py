import json
import pytest

# EXAMPLE:
# {
#     "info": {
#       "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
#       "dataPulledOn": "2024-10-03 13:19:45.748356"
#     },
#     "pokemon": [
#       {
#         "abilities": [
#           {
#             "ability": {
#               "name": "Guts"
#             },
#             "is_hidden": 0,
#             "slot": 1
#           },

          
#         ],
#         "game_indices": [
#           {
#             "game_index": 1,
#             "version": {
#               "name": "red",
#               "url": "https://pokeapi.co/api/v2/version/1/"
#             }
#           },
#           {
#             "game_index": 246,
#             "version": {
#               "name": "unbound",
#               "url": "-"
#             }
#           }
#         ],
#         "height": 60.0,
#         "weight": 7200.0,
#         "id": 246,
#         "name": "larvitar",
#         "locations": [
#           {
#             "location": "Starter\nCan be acquired either in the Shadow Base Warehouse or your rival\u2019s house in Post-game",
#             "encounterMethod": "Evolution",
#             "timeOfDay": "All Day",
#             "isSpecialEncounter": 0
#           }
#         ],
#         "capture_rate": {
#           "value": 5.9,
#           "percentage": "45"
#         },
#         "moves": [
#           {
#             "move": {
#               "name": "Leer",
#               "type": "Normal",
#               "category": "Status",
#               "power": "-",
#               "accuracy": "100"
#             },
#             "version_group_details": [
#               {
#                 "level_learned_at": "1",
#                 "move_learn_method": {
#                   "name": "level-up/tm",
#                   "url": "https://pokeapi.co/api/v2/move-learn-method/1/"
#                 },
#                 "version_group": {
#                   "name": "unbound"
#                 }
#               }
#             ]
#           }
#         ],
#         "sprites": {
#           "front_default": "https://www.pokemonunboundpokedex.com/static/pixelart/246.png",
#           "other": {
#             "home": {
#               "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/246.png"
#             }
#           }
#         },
#         "evolution_chain": {
#           "evolution_details": [],
#           "evolves_to": [
#             {
#               "evolution_details": [
#                 {
#                   "gender": null,
#                   "held_item": null,
#                   "item": null,
#                   "known_move": null,
#                   "known_move_type": null,
#                   "location": null,
#                   "min_affection": null,
#                   "min_beauty": null,
#                   "min_happiness": null,
#                   "min_level": 30,
#                   "needs_overworld_rain": false,
#                   "party_species": null,
#                   "party_type": null,
#                   "relative_physical_stats": null,
#                   "time_of_day": "",
#                   "trade_species": null,
#                   "trigger": {
#                     "name": "level-up",
#                     "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
#                   },
#                   "turn_upside_down": false
#                 }
#               ],
#               "evolves_to": [
#                 {
#                   "evolution_details": [
#                     {
#                       "gender": null,
#                       "held_item": null,
#                       "item": null,
#                       "known_move": null,
#                       "known_move_type": null,
#                       "location": null,
#                       "min_affection": null,
#                       "min_beauty": null,
#                       "min_happiness": null,
#                       "min_level": 55,
#                       "needs_overworld_rain": false,
#                       "party_species": null,
#                       "party_type": null,
#                       "relative_physical_stats": null,
#                       "time_of_day": "",
#                       "trade_species": null,
#                       "trigger": {
#                         "name": "level-up",
#                         "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
#                       },
#                       "turn_upside_down": false
#                     }
#                   ],
#                   "evolves_to": [],
#                   "is_baby": false,
#                   "species": {
#                     "name": "tyranitar",
#                     "url": "https://pokeapi.co/api/v2/pokemon-species/248/"
#                   }
#                 }
#               ],
#               "is_baby": false,
#               "species": {
#                 "name": "pupitar",
#                 "url": "https://pokeapi.co/api/v2/pokemon-species/247/"
#               }
#             }
#           ],
#           "is_baby": false,
#           "species": {
#             "name": "larvitar",
#             "url": "https://pokeapi.co/api/v2/pokemon-species/246/"
#           }
#         },
#         "stats": {
#           "hp": {
#             "base_stat": 50,
#             "effort": 0,
#             "stat": {
#               "name": "hp",
#               "url": "https://pokeapi.co/api/v2/stat/1/"
#             }
#           },
#           "attack": {
#             "base_stat": 64,
#             "effort": 0,
#             "stat": {
#               "name": "attack",
#               "url": "https://pokeapi.co/api/v2/stat/2/"
#             }
#           },
#           "defense": {
#             "base_stat": 50,
#             "effort": 0,
#             "stat": {
#               "name": "defense",
#               "url": "https://pokeapi.co/api/v2/stat/3/"
#             }
#           },
#           "specialAttack": {
#             "base_stat": 45,
#             "effort": 0,
#             "stat": {
#               "name": "specialAttack",
#               "url": "https://pokeapi.co/api/v2/stat/4/"
#             }
#           },
#           "specialDefense": {
#             "base_stat": 50,
#             "effort": 0,
#             "stat": {
#               "name": "specialDefense",
#               "url": "https://pokeapi.co/api/v2/stat/5/"
#             }
#           },
#           "speed": {
#             "base_stat": 41,
#             "effort": 0,
#             "stat": {
#               "name": "speed",
#               "url": "https://pokeapi.co/api/v2/stat/6/"
#             }
#           }
#         },
#         "types": ["Rock", "Ground"],
#         "gender": {
#           "isGenderless": false,
#           "maleChance": "50",
#           "femaleChance": "50"
#         }
#       },
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
            assert "ability" in ability
            assert "is_hidden" in ability
            assert "slot" in ability


@pytest.mark.asyncio
async def test_borrius_pokedex_json_check_index():
    for pokemon in data[0]["pokemon"]:
        assert "game_indices" in pokemon

        for index in pokemon["game_indices"]:
            assert "game_index" in index
            assert "version" in index


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
