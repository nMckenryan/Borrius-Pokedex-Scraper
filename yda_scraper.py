from bs4 import BeautifulSoup
import aiohttp
import asyncio


from helpers import fetch_page, get_pokemon_names_from_unbound_pokedex

# SCRAPE POKEMON DATA FROM BORRIUS POKEDEX
async def scrape_yda_pokemon_data():
    
    borrius_pokemon_names = get_pokemon_names_from_unbound_pokedex()  
    
    pokemon_list = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in borrius_pokemon_names:
            try:
                link = f"https://ydarissep.github.io/Unbound-Pokedex/?species=SPECIES_{i}&table=speciesTable&input=larvi&"
                tasks.append(fetch_page(session, link))
            except Exception as e:
                print(f"Failed to get page for {i} : {e}")

        pages = await asyncio.gather(*tasks, return_exceptions=True)

        for page in pages:
            if page is not None and not isinstance(page, Exception):
                # GET DATA FROM PAGE
                soup = BeautifulSoup(page, "html.parser")
                species_name = soup.find("span", id="speciesName").text()
                speciesPanelSubcontainer2 = soup.find("div", id="speciesPanelSubcontainer2")
                
                pokemon_list.append(species_name)
            else:
                print(f"Failed to get data for Pokemon : {page}")
                
    return pokemon_list
                
                
                
                
                
                
                
                
                
                
                
                
                
           
     