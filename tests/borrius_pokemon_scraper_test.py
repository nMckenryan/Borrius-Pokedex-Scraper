import pytest
from borrius_pokemon_scraper import scrape_pokemon_data


@pytest.mark.asyncio
async def test_scrape_pokemon_data_national():
    national_page = "https://www.pokemonunboundpokedex.com/national/"
    national_numbers = [246]

    pokemonJson = [
        {
            "pokemon": [],
        }
    ]

    await scrape_pokemon_data( national_page, national_numbers, 1, pokemonJson)

    assert pokemonJson[0].get("pokemon")[0].get("name") == "larvitar"


@pytest.mark.asyncio
async def test_scrape_pokemon_data_borrius_get_name():
    borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
    borrius_numbers = [1]

    pokemonJson = [
        {
            "pokemon": [],
        }
    ]

    await scrape_pokemon_data( borrius_page, borrius_numbers, 1, pokemonJson)

    assert pokemonJson[0].get("pokemon")[0].get("name") == 'snorunt'

# @pytest.mark.asyncio
# async def test_scrape_pokemon_data_borrius_get_locations():
#     borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
#     borrius_numbers = [1]

#     pokemonJson = [
#         {
#             "pokemon": [],
#         }
#     ]

#     await scrape_pokemon_data( borrius_page, borrius_numbers, 1, pokemonJson)

#     assert len(pokemonJson[0].get("pokemon")[0].get("locations")) == 2


@pytest.mark.asyncio
async def test_scrape_pokemon_data_borrius_get_types():
    borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
    borrius_numbers = [1]

    pokemonJson = [
        {
            "pokemon": [],
        }
    ]

    await scrape_pokemon_data( borrius_page, borrius_numbers, 1, pokemonJson)

    assert pokemonJson[0].get("pokemon")[0].get("types")[0] == 'Ice'


