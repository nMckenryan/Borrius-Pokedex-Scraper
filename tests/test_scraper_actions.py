import string
from bs4 import BeautifulSoup
import asyncio
import pytest

from mainFunctions.scraper_actions import *


top_card = BeautifulSoup('<div><h3 class="card-title text-4xl">Name: Pikachu</h3></div>', 'html.parser')

one_type = BeautifulSoup("<p class='text-3xl font-bold'>['Fire']</p>", 'html.parser')
two_type = BeautifulSoup("<p class='text-3xl font-bold'>['Fire', 'Water']</p>", 'html.parser')


@pytest.mark.asyncio
def test_get_name():
    assert get_name(top_card) == 'Pikachu'

@pytest.mark.asyncio
def test_get_types_single():
    assert get_types(one_type) == ['Fire']

@pytest.mark.asyncio
def test_get_types_two():
    assert get_types(two_type) == ['Fire', 'Water']


@pytest.mark.asyncio
async def test_get_missing_moves_for_pokemon():
    moveList = await get_missing_moves_from_pokeapi(374)
    assert len(moveList) == 8
    ##TODO: fix tutor showing up?
    assert moveList[0] == {'name': 'headbutt', 'type': 'normal', 'category': 'physical', 'power': 70, 'accuracy': 100, 'level_learned_at': 0, 'method': 'tutor'}