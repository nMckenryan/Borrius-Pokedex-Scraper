# Borrius Pokedex Scraper

## Overview

A Web Scraper that extracts data from the [Pokemon Unbound Pokedex](https://pokemonunbound.com/pokedex) website and outputs it to a JSON file.

- Built with Python and BeautifulSoup, Based on a tutorial from [RealPython](https://github.com/realpython/materials/blob/master/web-scraping-bs4/)
- Contains data for the 494 Borrius Region Pokemon found in the Popular Romhack [Pokemon Unbound](https://www.pokecommunity.com/threads/pok%C3%A9mon-unbound-completed.382178/)

- Data provided includes:
  - Number, Name and Types
  - Sprites
  - Catch Rate
  - Gender Ratio
  - Ability
  - Weight and Height (Metric and Imperial)
  - Stats (Min, Avg Max)
  - Learned Moves (Level, Move-name, Type, Category, Power, Accuracy)
  - TM/HM Moves ( Move-name, Type, Category, Power, Accuracy)

### [View Sample JSON here!](https://github.com/nMckenryan/BorriusPokedexScraper/blob/main/borrius_pokedex_data.json)

## Instructions

#### Note: As the project is completed, the Pokedex is unlikely to have changed, so you may want ot download the [ JSON provided](https://github.com/nMckenryan/BorriusPokedexScraper/blob/main/borrius_pokedex_data.json). Otherwise:

1. Download and extract the project by cloning this project or running the ZIP
2. Run `python borrius_pokemon_scraper.py` in the terminal
3. Wait for the process to completes (takes around ~2-5 Minutes)
4. Open the `borrius_pokedex_data.json` file in your favorite text editor and enjoy

### TO DO:

- [x] Scrape all pokemon
- [x] Extract Sprite Data from Site! (Not yet Implemented)
- [x] Print retrieved data into JSON
- [x] Save JSON to a file
- [x] Implement Error Messages for process
- [x] Make this available publically/for other projects

### FUTURE FEATURES:

- [] Download and store images for perpetuity
- [] Add back sprites from PokeApi
- [] Implement starter pokemon data from Borrius National Dex (+9 more attached to tip)
- [] Patch in missing data from PokeAPI
- [] Line up data for use with Curadex project
- [] Compile API
