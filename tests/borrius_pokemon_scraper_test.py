import pytest

from borrius_pokemon_scraper import compile_pokedex


@pytest.mark.asyncio
async def test_compile_pokedex():
    pokemonJson = [
        {
            "info": {
                "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                "dataPulledOn": None,
            },
            "pokemon": [],
        }
    ]
    
    

    await compile_pokedex()

    assert len(pokemonJson[0]["pokemon"]) == 503
    assert pokemonJson[0]["info"]["dataPulledOn"] is not None
