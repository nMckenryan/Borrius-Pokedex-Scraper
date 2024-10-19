from bs4 import BeautifulSoup

from mainFunctions.scraper_actions import get_name, get_types

top_card = BeautifulSoup('<div><h3 class="card-title text-4xl">Name: Pikachu</h3></div>', 'html.parser')

one_type = BeautifulSoup("<p class='text-3xl font-bold'>['Fire']</p>", 'html.parser')
two_type = BeautifulSoup("<p class='text-3xl font-bold'>['Fire', 'Water']</p>", 'html.parser')


def test_get_name():
    assert get_name(top_card) == 'Pikachu'


def test_get_types_single():
    assert get_types(one_type) == ['Fire']


def test_get_types_two():
    assert get_types(two_type) == ['Fire', 'Water']

