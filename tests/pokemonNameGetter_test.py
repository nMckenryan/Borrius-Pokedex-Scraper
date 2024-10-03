# test_example.py

import unittest
import asyncio
from pokemonNameGetter import (
    getMissingPokemonData,
    getMissingPokemonList,
    getPokeApiData,
)


class TestGetPokeApiData(unittest.IsolatedAsyncioTestCase):
    async def test_get_poke_api_data(self):
        """Test that we can get data from the Pokemon API"""
        data = await getPokeApiData("pikachu")
        self.assertIsInstance(data, dict)
        self.assertIn("name", data)
        self.assertEqual(data["name"], "pikachu")
        self.assertEqual(data["id"], 25)

    def test_get_missing_pokemon_list(self):
        """Test that we can get a list of missing Pokemon names"""
        missing_pokemon = getMissingPokemonList()
        self.assertIsInstance(missing_pokemon, list)
        self.assertIsNotNone(missing_pokemon)
        self.assertIs(len(missing_pokemon), 215)

    async def test_get_missing_pokemon_data(self):
        """Test that we can get data about missing Pokemon"""
        data = await getMissingPokemonData()
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
