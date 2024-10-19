from bs4 import BeautifulSoup
import aiohttp
import asyncio


from helpers import fetch_page, get_pokemon_names_from_unbound_pokedex

pokemon_list = []


# SCRAPE POKEMON DATA FROM BORRIUS POKEDEX
async def scrape_yda_pokemon_data():
    async with aiohttp.ClientSession() as session:
        borrius_pokemon_names = await get_pokemon_names_from_unbound_pokedex()  
        tasks = []
        for i in borrius_pokemon_names:
            link = f"https://ydarissep.github.io/Unbound-Pokedex/?species=SPECIES_{i.upper()}&table=speciesTable&input=larvi&"
            tasks.append(fetch_page(session, link))

        pages = await asyncio.gather(*tasks, return_exceptions=True)

        for page in pages:
            if page is not None and not isinstance(page, Exception):
                soup = BeautifulSoup(page, "html.parser")
                species_name_element = soup.select('div#speciesName')
                species_name = species_name_element.text()
                pokemon_list.append(species_name)

            else:
                print(f"Failed to get data for Pokemon : {page}")
                
    return pokemon_list
                
                
                
                
                
                
                
                
                
                
                
                
                
           
     