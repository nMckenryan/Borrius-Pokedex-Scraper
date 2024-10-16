import pytest

from borrius_pokemon_scraper import compile_pokedex, scrape_pokemon_data
import datetime

@pytest.mark.asyncio
async def test_scrape_pokemon_data_national():
    national_page = "https://www.pokemonunboundpokedex.com/national/"
    national_numbers = [246]

    pokemonJson = [
        {
            "info": {
                "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                "dataPulledOn": str(datetime.datetime.now()),
            },
            "pokemon": [],
        }
    ]

    await scrape_pokemon_data( national_page, national_numbers, 1, pokemonJson)

    assert pokemonJson[0].get("pokemon")[0].get("name") == "larvitar"


@pytest.mark.asyncio
async def test_scrape_pokemon_data_borrius():
    borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"
    borrius_numbers = [1]

    pokemonJson = [
        {
            "info": {
                "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                "dataPulledOn": str(datetime.datetime.now()),
            },
            "pokemon": [],
        }
    ]

    await scrape_pokemon_data( borrius_page, borrius_numbers, 1, pokemonJson)

    assert len(pokemonJson[0].get("pokemon")) == 494


