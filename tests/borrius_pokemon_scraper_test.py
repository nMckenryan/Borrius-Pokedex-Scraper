import pytest

from borrius_pokemon_scraper import createPokemonJson
from helpers import borrius_pokedex_indexes


@pytest.mark.asyncio
async def test_compile_pokedex():
    """Test that we can compile the borrius pokedex"""
    pokemonJson = [
        {
            "info": {
                "description": "Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper",
                "dataPulledOn": "",
            },
            "pokemon": [],
        }
    ]

    await createPokemonJson("https://www.pokemonunboundpokedex.com/borrius/", borrius_pokedex_indexes["borrius_numbers"], 10, pokemonJson)

    assert len(pokemonJson[0]["pokemon"]) == 494
