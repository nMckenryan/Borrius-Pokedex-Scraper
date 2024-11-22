# Borrius Pokedex Scraper API

## Overview

A Web Scraper API that extracts pokemon number data from [Pokemon Unbound Pokedex](https://pokemonunbound.com/pokedex) website and outputs it to a JSON file.

- Built with Python and BeautifulSoup, Based on a tutorial from [RealPython](https://github.com/realpython/materials/blob/master/web-scraping-bs4/)
- API Endpoints Managed by FastAPI, Hosted on Google Cloud via a Docker Container
- Location Data scraped from the [Pokémon Unbound Location Guide v2.1.1.1](https://docs.google.com/spreadsheets/d/1bkNm3P9NI3AZTf53dxhCBjwiSPl830KDm28PE5zpYfs/edit?gid=897380238#gid=897380238) Excel File via OpenPyxl

## Features

- Contains data for the 503 Borrius Region Pokemon found in the Popular Romhack [Pokemon Unbound](https://www.pokecommunity.com/threads/pok%C3%A9mon-unbound-completed.382178/)
- Unlike the Borrius Dex, this scraper contains the 3 Starter Pokemon (Larvitar, Metang, Gible). They're at the beginning of the Pokedex Data.

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

### [View Sample JSON here!](https://borrius-pokemon-scraper-321133146790.australia-southeast1.run.app/docs)

## Instructions

### Note: As the project is completed, the Pokedex is unlikely to have changed, so you may want ot download the [ JSON provided](https://github.com/nMckenryan/BorriusPokedexScraper/blob/main/borrius_pokedex_data.json). Otherwise

### USING THE API ENDPOINT

Check out the Endpoints at https://borrius-pokemon-scraper-321133146790.australia-southeast1.run.app/docs

### Installing and generating JSON manually

0. Install Python dependancies from requirements.txt
1. Download and extract the project by cloning this project or running the ZIP
2. Run `python borrius_pokemon_scraper.py` in the terminal
3. Wait for the process to completes (takes around >2 minutes)
4. Open the `borrius_pokedex_data.json` file in your favorite text editor and enjoy

### Running the Docker Container/Api locally

0. Install all required dependancies (make sure docker desktop is running)
1. Run `docker build -t borrius-pokemon-scraper .`
2. Run `docker run -p 8000:8000 borrius-pokemon-scraper`


### TO DO

- [x] Collate Alolan, Hisui, Galar Forms invluded in the game
  - [] Add to dex after original versions (e.g. 30.a? )
- [] Fix issue with generating Starters intermittently. failing tests.

- [x] - Rewrite evolution compile
  - [x] - integrate
 - [x] Fix: Could not find learned move table for 10186
 - [] Ensure it's compiled in the right way

### FUTURE FEATURES:

- [ ] Reconfigure for use with Yda
- [x] Display Special Encounter Pokemon data
  - [ ] Get pokemon evolutions data from pokeapi for spec. encounter