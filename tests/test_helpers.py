
import json
from unittest.mock import mock_open, patch

import aiohttp
import pytest

from mainFunctions.helpers import EvoObject, correct_pokemon_name, fetch_page, get_and_parse_evo, get_evo_trigger, get_evolution_data_from_pokeapi, get_missing_pokemon_data, get_pokemon_api_data_gaps, get_pokemon_index_from_name, get_pokemon_indexes_from_list, get_pokemon_locations, get_pokemon_names_from_unbound_pokedex, get_regional_forms_by_name, get_special_encounter_pokemon, initialise_pokemon_location_template, parse_evolution_chain, read_location_data_json


@pytest.mark.asyncio
async def test_fetch_page():
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(
            session, "https://www.pokemonunboundpokedex.com/national/1"
        )
        assert html is not None
        assert "Bulbasaur" in html


@pytest.mark.asyncio
async def test_read_location_data_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = await read_location_data_json()
        assert result == [] or result == None


@pytest.mark.asyncio
async def test_read_location_data_json_json_decode_error():
    with patch("builtins.open", mock_open(read_data="not a json")):
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            result = await read_location_data_json()
            assert result == [] or result == None


@pytest.mark.asyncio
async def test_read_location_data_json_success():
    mock_data = [{"pokemon": "bulbasaur", "locationData": []}]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        with patch("json.load", return_value=mock_data):
            result = await read_location_data_json()
            assert result == mock_data


@pytest.mark.asyncio
async def test_check_for_forbidden_names():
    location_list = []

    with patch("mainFunctions.helpers.read_location_data_json") as mock_read_location_data_json:
        await mock_read_location_data_json()
    
    for pokemon in location_list:
        assert pokemon["pokemon"] != "super rod"
        assert pokemon["pokemon"] != "old rod"
        assert pokemon["pokemon"] != "good rod"


def test_get_pokemon_locations():
    location_list = [{"pokemon": "snorunt", "locationData": [{"location": "Route 1"}, {"location": "Route 8"}]},
                     {"pokemon": "glacie", "locationData": []}]
    pokemon_location = get_pokemon_locations("snorunt", location_list)
    
    assert len(pokemon_location) == 2
    assert pokemon_location[0]['location'] == 'Route 1'
    assert pokemon_location[1]['location'] == 'Route 8'


@pytest.mark.asyncio
async def test_get_evolution_data_from_pokeapi():
    pokemon_number = 1
    result = await get_evolution_data_from_pokeapi(pokemon_number)
    assert 'evolution_details' in result

@pytest.mark.asyncio
async def test_correctPokemonName():
    result = correct_pokemon_name("minior")
    assert result == "minior-red-meteor"


@pytest.mark.asyncio
async def test_correctPokemonName_fossil():
    result = correct_pokemon_name("Dome Fossil")
    assert result == "kabuto"

    
@pytest.mark.asyncio
async def test_correctPokemonName_regional():
    result = correct_pokemon_name("galarian numel")
    assert result == "numel-galar"


@pytest.mark.asyncio
async def test_initialise_pokemon_location_template():
    location_data_list = []

    await initialise_pokemon_location_template(location_data_list)
    assert len(location_data_list) == 503
    assert location_data_list[0]["pokemon"] == "larvitar"
    assert location_data_list[502]["pokemon"] == "hoopa"


def test_get_special_encounter_pokemon():
    result = get_special_encounter_pokemon()
    assert len(result) > 0


@pytest.mark.asyncio
async def test_get_pokemon_api_data_gaps():
    pokemon = "pikachu"
    result = await get_pokemon_api_data_gaps(pokemon)
    assert result["name"] == pokemon


@pytest.mark.asyncio
async def test_get_missing_pokemon_data():
    result = await get_missing_pokemon_data()
    assert len(result) > 0


@pytest.mark.asyncio
async def test_get_pokemon_names_from_unbound_pokedex():
    pokemon_names = await get_pokemon_names_from_unbound_pokedex()
    assert len(pokemon_names) == 494
    assert pokemon_names[0] == "Snorunt"


@pytest.mark.asyncio
async def test_get_pokemon_index_from_name():
    pokemon_index = await get_pokemon_index_from_name("minior")
    assert pokemon_index == 774

    
@pytest.mark.asyncio
async def test_get_pokemon_indexes_from_list():
    pokemon_indexes = await get_pokemon_indexes_from_list(["minior", "pikachu", "caterpie"])
    assert pokemon_indexes == [774, 25, 10]

@pytest.mark.asyncio
async def test_get_regional_forms_by_name():
    pokemon_location = [{'pokemon': 'linoone-galar', 'locationData': []}, 
                        {'pokemon': 'test-alola', 'locationData': []},
                        {'pokemon': 'test-hisui', 'locationData': []},
                        {'pokemon': 'nothing', 'locationData': []}]
    regional_form_list = get_regional_forms_by_name(pokemon_location)
    assert len(regional_form_list) == 3
    
@pytest.mark.asyncio
async def test_get_regional_forms_by_name_real():
    pokemon_location = await read_location_data_json()
    regional_form_list = get_regional_forms_by_name(pokemon_location)
    assert len(regional_form_list) == 18
    
    
def test_get_evo_trigger():
    sample_evo = [
        {
            "gender": None,
            "held_item": {
                "name": "kings-rock",
                "url": "https://pokeapi.co/api/v2/item/198/"
            },
            "item": None,
            "known_move": None,
            "known_move_type": None,
            "location": None,
            "min_affection": None,
            "min_beauty": None,
            "min_happiness": None,
            "min_level": None,
            "needs_overworld_rain": False,
            "party_species": None,
            "party_type": None,
            "relative_physical_stats": None,
            "time_of_day": "",
            "trade_species": None,
            "trigger": {
                "name": "trade",
                "url": "https://pokeapi.co/api/v2/evolution-trigger/2/"
            },
            "turn_upside_down": False
        }
    ]
    
    desired_result = EvoObject( 0, "trade", ['kings-rock']
    )
    result = get_evo_trigger(sample_evo)
    assert result.evo_trigger == desired_result.evo_trigger
    assert result.evo_conditions == desired_result.evo_conditions
    assert result.evo_stage == desired_result.evo_stage
    
    
def test_get_evo_trigger():
    sample_evo = [
        {
            "gender": None,
            "held_item": {
                "name": "kings-rock",
                "url": "https://pokeapi.co/api/v2/item/198/"
            },
            "item": None,
            "known_move": None,
            "known_move_type": None,
            "location": None,
            "min_affection": None,
            "min_beauty": None,
            "min_happiness": None,
            "min_level": None,
            "needs_overworld_rain": False,
            "party_species": None,
            "party_type": None,
            "relative_physical_stats": None,
            "time_of_day": "",
            "trade_species": None,
            "trigger": {
                "name": "trade",
                "url": "https://pokeapi.co/api/v2/evolution-trigger/2/"
            },
            "turn_upside_down": False
        }
    ]
    
    desired_result = EvoObject(0, "poliwhirl", "trade", ['Hold: kings-rock']
    )
    result = get_evo_trigger(sample_evo)
    assert result.evo_trigger == desired_result.evo_trigger
    assert result.evo_conditions == desired_result.evo_conditions
    assert result.evo_stage == desired_result.evo_stage
    
    
def test_parse_evo_chain():
    evo_sample =  {
                "evolution_details": [],
                "evolves_to": [
                    {
                        "evolution_details": [
                            {
                                "gender": None,
                                "held_item": None,
                                "item": None,
                                "known_move": None,
                                "known_move_type": None,
                                "location": None,
                                "min_affection": None,
                                "min_beauty": None,
                                "min_happiness": None,
                                "min_level": 30,
                                "needs_overworld_rain": False,
                                "party_species": None,
                                "party_type": None,
                                "relative_physical_stats": None,
                                "time_of_day": "",
                                "trade_species": None,
                                "trigger": {
                                    "name": "level-up",
                                    "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                },
                                "turn_upside_down": False
                            }
                        ],
                        "evolves_to": [
                            {
                                "evolution_details": [
                                    {
                                        "gender": None,
                                        "held_item": None,
                                        "item": None,
                                        "known_move": None,
                                        "known_move_type": None,
                                        "location": None,
                                        "min_affection": None,
                                        "min_beauty": None,
                                        "min_happiness": None,
                                        "min_level": 55,
                                        "needs_overworld_rain": False,
                                        "party_species": None,
                                        "party_type": None,
                                        "relative_physical_stats": None,
                                        "time_of_day": "",
                                        "trade_species": None,
                                        "trigger": {
                                            "name": "level-up",
                                            "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                        },
                                        "turn_upside_down": False
                                    }
                                ],
                                "evolves_to": [],
                                "is_baby": False,
                                "species": {
                                    "name": "tyranitar",
                                    "url": "https://pokeapi.co/api/v2/pokemon-species/248/"
                                }
                            }
                        ],
                        "is_baby": False,
                        "species": {
                            "name": "pupitar",
                            "url": "https://pokeapi.co/api/v2/pokemon-species/247/"
                        }
                    }
                ],
                "is_baby": False,
                "species": {
                    "name": "larvitar",
                    "url": "https://pokeapi.co/api/v2/pokemon-species/246/"
                }
            }
    
    desired_evo_sample = [
        EvoObject(1, "larvitar", "base", []),
        EvoObject(2, "pupitar", "level-up", [30]),
        EvoObject(3, "tyranitar", "level-up", [55])
    ]
    
    parsed = parse_evolution_chain(evo_sample) 
    assert parsed[0].evo_stage == desired_evo_sample[0].evo_stage
    assert parsed[0].evo_stage_name == desired_evo_sample[0].evo_stage_name
    assert parsed[0].evo_trigger == desired_evo_sample[0].evo_trigger
    assert parsed[0].evo_conditions == desired_evo_sample[0].evo_conditions
    
    assert parsed[1].evo_stage == desired_evo_sample[1].evo_stage
    assert parsed[1].evo_stage_name == desired_evo_sample[1].evo_stage_name
    assert parsed[1].evo_trigger == desired_evo_sample[1].evo_trigger
    assert parsed[1].evo_conditions == desired_evo_sample[1].evo_conditions
    
    assert parsed[2].evo_stage == desired_evo_sample[2].evo_stage
    assert parsed[2].evo_stage_name == desired_evo_sample[2].evo_stage_name
    assert parsed[2].evo_trigger == desired_evo_sample[2].evo_trigger
    assert parsed[2].evo_conditions == desired_evo_sample[2].evo_conditions
    

# @pytest.mark.asyncio
# async def test_get_evolution_data_from_pokeapi_check_locations_omitted():
#     pokemon_number = 133
#     result = await get_evolution_data_from_pokeapi(pokemon_number)
#     glaceon_details = result["evolution_details"]["chain"]["evolves_to"][6]["evolution_details"]
#     assert len(glaceon_details["evolves_to"]) == 1

@pytest.mark.asyncio
async def test_get_and_parse_evo():
    pokemon_number = 12
    result = await get_and_parse_evo(pokemon_number)
    assert result[0].evo_stage_name == "caterpie"
    assert result[1].evo_stage_name == "metapod"
    assert result[2].evo_stage_name == "butterfree"
    

    
def test_parse_evo_chain_split_evo():
    
    split_evo_sample = {
                    "evolution_details": [],
                    "evolves_to": [
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": {
                                        "name": "water-stone",
                                        "url": "https://pokeapi.co/api/v2/item/84/"
                                    },
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": None,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "use-item",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "vaporeon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/134/"
                            }
                        },
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": {
                                        "name": "thunder-stone",
                                        "url": "https://pokeapi.co/api/v2/item/83/"
                                    },
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": None,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "use-item",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "jolteon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/135/"
                            }
                        },
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": {
                                        "name": "fire-stone",
                                        "url": "https://pokeapi.co/api/v2/item/82/"
                                    },
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": None,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "use-item",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "flareon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/136/"
                            }
                        },
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": None,
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": 160,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "day",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "level-up",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "espeon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/196/"
                            }
                        },
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": None,
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": 160,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "night",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "level-up",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "umbreon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/197/"
                            }
                        },
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": {
                                        "name": "leaf-stone",
                                        "url": "https://pokeapi.co/api/v2/item/85/"
                                    },
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": None,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "use-item",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "leafeon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/470/"
                            }
                        },
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": {
                                        "name": "ice-stone",
                                        "url": "https://pokeapi.co/api/v2/item/885/"
                                    },
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": None,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "use-item",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "glaceon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/471/"
                            }
                        },
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": None,
                                    "known_move": None,
                                    "known_move_type": {
                                        "name": "fairy",
                                        "url": "https://pokeapi.co/api/v2/type/18/"
                                    },
                                    "location": None,
                                    "min_affection": 2,
                                    "min_beauty": None,
                                    "min_happiness": None,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "level-up",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                    },
                                    "turn_upside_down": False
                                },
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": None,
                                    "known_move": None,
                                    "known_move_type": {
                                        "name": "fairy",
                                        "url": "https://pokeapi.co/api/v2/type/18/"
                                    },
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": 160,
                                    "min_level": None,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "level-up",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [],
                            "is_baby": False,
                            "species": {
                                "name": "sylveon",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/700/"
                            }
                        }
                    ],
                    "is_baby": False,
                    "species": {
                        "name": "eevee",
                        "url": "https://pokeapi.co/api/v2/pokemon-species/133/"
                    }
    }
    
    desired_evo_sample = [
        EvoObject(1, "eevee", "base", []),
        EvoObject(2, "vaporeon", "use-item", ["Use: water-stone"]),
        EvoObject(2, "jolteon", "use-item", ["Use: thunder-stone"]),
        EvoObject(2, "flareon", "use-item", ["Use: fire-stone"]),
        EvoObject(2, "espeon", "level-up", ['Happiness: 160', 'Time of Day: day']),
        EvoObject(2, "umbreon", "level-up", ['Happiness: 160', 'Time of Day: night']),
        EvoObject(2, "leafeon", "use-item", ["Use: leaf-stone"]),
        EvoObject(2, "glaceon", "use-item", ["Use: ice-stone"]),
        EvoObject(2, "sylveon", "level-up", ['Known Move Type: fairy', 'Affection: 2']),
        
    ]
    
    parsed = parse_evolution_chain(split_evo_sample) 
    assert parsed[0].evo_stage == desired_evo_sample[0].evo_stage
    assert parsed[0].evo_stage_name == desired_evo_sample[0].evo_stage_name
    assert parsed[0].evo_trigger == desired_evo_sample[0].evo_trigger
    assert parsed[0].evo_conditions == desired_evo_sample[0].evo_conditions
    
    assert parsed[1].evo_stage == desired_evo_sample[1].evo_stage
    assert parsed[1].evo_stage_name == desired_evo_sample[1].evo_stage_name
    assert parsed[1].evo_trigger == desired_evo_sample[1].evo_trigger
    assert parsed[1].evo_conditions == desired_evo_sample[1].evo_conditions
    
    assert parsed[2].evo_stage == desired_evo_sample[2].evo_stage
    assert parsed[2].evo_stage_name == desired_evo_sample[2].evo_stage_name
    assert parsed[2].evo_trigger == desired_evo_sample[2].evo_trigger
    assert parsed[2].evo_conditions == desired_evo_sample[2].evo_conditions
    
    assert parsed[3].evo_stage == desired_evo_sample[3].evo_stage
    assert parsed[3].evo_stage_name == desired_evo_sample[3].evo_stage_name
    assert parsed[3].evo_trigger == desired_evo_sample[3].evo_trigger
    assert parsed[3].evo_conditions == desired_evo_sample[3].evo_conditions
    
    assert parsed[4].evo_stage == desired_evo_sample[4].evo_stage   
    assert parsed[4].evo_stage_name == desired_evo_sample[4].evo_stage_name
    assert parsed[4].evo_trigger == desired_evo_sample[4].evo_trigger
    assert parsed[4].evo_conditions == desired_evo_sample[4].evo_conditions
    
    assert parsed[5].evo_stage == desired_evo_sample[5].evo_stage
    assert parsed[5].evo_stage_name == desired_evo_sample[5].evo_stage_name 
    assert parsed[5].evo_trigger == desired_evo_sample[5].evo_trigger
    assert parsed[5].evo_conditions == desired_evo_sample[5].evo_conditions
    
    assert parsed[6].evo_stage == desired_evo_sample[6].evo_stage
    assert parsed[6].evo_stage_name == desired_evo_sample[6].evo_stage_name
    assert parsed[6].evo_trigger == desired_evo_sample[6].evo_trigger
    assert parsed[6].evo_conditions == desired_evo_sample[6].evo_conditions
    
    assert parsed[7].evo_stage == desired_evo_sample[7].evo_stage
    assert parsed[7].evo_stage_name == desired_evo_sample[7].evo_stage_name
    assert parsed[7].evo_trigger == desired_evo_sample[7].evo_trigger
    assert parsed[7].evo_conditions == desired_evo_sample[7].evo_conditions
    
    assert parsed[8].evo_stage == desired_evo_sample[8].evo_stage
    assert parsed[8].evo_stage_name == desired_evo_sample[8].evo_stage_name
    assert parsed[8].evo_trigger == desired_evo_sample[8].evo_trigger
    assert parsed[8].evo_conditions == desired_evo_sample[8].evo_conditions
    
def test_parse_evo_chain_y_shape_evo():
    
    y_evo = {
                    "evolution_details": [],
                    "evolves_to": [
                        {
                            "evolution_details": [
                                {
                                    "gender": None,
                                    "held_item": None,
                                    "item": None,
                                    "known_move": None,
                                    "known_move_type": None,
                                    "location": None,
                                    "min_affection": None,
                                    "min_beauty": None,
                                    "min_happiness": None,
                                    "min_level": 25,
                                    "needs_overworld_rain": False,
                                    "party_species": None,
                                    "party_type": None,
                                    "relative_physical_stats": None,
                                    "time_of_day": "",
                                    "trade_species": None,
                                    "trigger": {
                                        "name": "level-up",
                                        "url": "https://pokeapi.co/api/v2/evolution-trigger/1/"
                                    },
                                    "turn_upside_down": False
                                }
                            ],
                            "evolves_to": [
                                {
                                    "evolution_details": [
                                        {
                                            "gender": None,
                                            "held_item": None,
                                            "item": {
                                                "name": "water-stone",
                                                "url": "https://pokeapi.co/api/v2/item/84/"
                                            },
                                            "known_move": None,
                                            "known_move_type": None,
                                            "location": None,
                                            "min_affection": None,
                                            "min_beauty": None,
                                            "min_happiness": None,
                                            "min_level": None,
                                            "needs_overworld_rain": False,
                                            "party_species": None,
                                            "party_type": None,
                                            "relative_physical_stats": None,
                                            "time_of_day": "",
                                            "trade_species": None,
                                            "trigger": {
                                                "name": "use-item",
                                                "url": "https://pokeapi.co/api/v2/evolution-trigger/3/"
                                            },
                                            "turn_upside_down": False
                                        }
                                    ],
                                    "evolves_to": [],
                                    "is_baby": False,
                                    "species": {
                                        "name": "poliwrath",
                                        "url": "https://pokeapi.co/api/v2/pokemon-species/62/"
                                    }
                                },
                                {
                                    "evolution_details": [
                                        {
                                            "gender": None,
                                            "held_item": {
                                                "name": "kings-rock",
                                                "url": "https://pokeapi.co/api/v2/item/198/"
                                            },
                                            "item": None,
                                            "known_move": None,
                                            "known_move_type": None,
                                            "location": None,
                                            "min_affection": None,
                                            "min_beauty": None,
                                            "min_happiness": None,
                                            "min_level": None,
                                            "needs_overworld_rain": False,
                                            "party_species": None,
                                            "party_type": None,
                                            "relative_physical_stats": None,
                                            "time_of_day": "",
                                            "trade_species": None,
                                            "trigger": {
                                                "name": "trade",
                                                "url": "https://pokeapi.co/api/v2/evolution-trigger/2/"
                                            },
                                            "turn_upside_down": False
                                        }
                                    ],
                                    "evolves_to": [],
                                    "is_baby": False,
                                    "species": {
                                        "name": "politoed",
                                        "url": "https://pokeapi.co/api/v2/pokemon-species/186/"
                                    }
                                }
                            ],
                            "is_baby": False,
                            "species": {
                                "name": "poliwhirl",
                                "url": "https://pokeapi.co/api/v2/pokemon-species/61/"
                            }
                        }
                    ],
                    "is_baby": False,
                    "species": {
                        "name": "poliwag",
                        "url": "https://pokeapi.co/api/v2/pokemon-species/60/"
                    }
                }
    
    desired_evo_sample = [
        EvoObject(1, "poliwag", "base", []),
        EvoObject(2, "poliwhirl", "level-up", [25]),
        EvoObject(3, "poliwrath", "use-item", ["Use: water-stone"]),
        EvoObject(3, "politoed", "trade", ["Hold: kings-rock"]),
    ]
    
    parsed = parse_evolution_chain(y_evo) 
    assert parsed[0].evo_stage == desired_evo_sample[0].evo_stage
    assert parsed[0].evo_stage_name == desired_evo_sample[0].evo_stage_name
    assert parsed[0].evo_trigger == desired_evo_sample[0].evo_trigger
    assert parsed[0].evo_conditions == desired_evo_sample[0].evo_conditions
    
    assert parsed[1].evo_stage == desired_evo_sample[1].evo_stage
    assert parsed[1].evo_stage_name == desired_evo_sample[1].evo_stage_name
    assert parsed[1].evo_trigger == desired_evo_sample[1].evo_trigger
    assert parsed[1].evo_conditions == desired_evo_sample[1].evo_conditions
    
    assert parsed[2].evo_stage == desired_evo_sample[2].evo_stage
    assert parsed[2].evo_stage_name == desired_evo_sample[2].evo_stage_name
    assert parsed[2].evo_trigger == desired_evo_sample[2].evo_trigger
    assert parsed[2].evo_conditions == desired_evo_sample[2].evo_conditions