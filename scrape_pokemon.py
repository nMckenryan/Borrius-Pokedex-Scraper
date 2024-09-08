import requests
from bs4 import BeautifulSoup

# Search thru all 494 pokemon in the Pokemon Unbound dex

URL = "https://www.pokemonunboundpokedex.com/borrius/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="snorunt")

# Look for Python jobs
print("Borrius Pokemon\n==============================\n")

pokemon = results.find_all(
    "button", class_="btn btn-primary my-button text-2xl"
)

pokemon_elements = [
    h2_element.parent.parent.parent.parent for h2_element in pokemon
]

for p_element in pokemon_elements:
    # dex_number = p_element.find("div", class_="content-start font-bold text-2xl col-span-2")
    # type_element = p_element.find("div", class_="col-span-2 text-3xl font-semibold")
    # hp_element = p_element.find("div", class_="text-3xl font-semibold")

    result = p_element.get_text(strip=True, separator=",")
    print(result)

