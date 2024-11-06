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

### Installing and running manually

0. Install Python dependancies from requirements.txt
1. Download and extract the project by cloning this project or running the ZIP
2. Run `python borrius_pokemon_scraper.py` in the terminal
3. Wait for the process to completes (takes around >2 minutes)
4. Open the `borrius_pokedex_data.json` file in your favorite text editor and enjoy

### TO DO

- [x] Scrape all pokemon
- [x] Extract Sprite Data from Site! (Not yet Implemented)
- [x] Print retrieved data into JSON
- [x] Save JSON to a file
- [x] Implement Error Messages for process
- [x] Make this available publically/for other projects

- [] Collate Alolan Forms
  - [] Get this data, and add to dex after original versions (e.g. 30.a? )

- [/] Display Special Encounter Pokemon data
  - [ ] Collate (include in search but not basic?)
  - [ ] Get pokemon evolutions data from pokeapi for spec. encounter
- [/] Handle movelists so they're not collosal lists for each pokemon
- [ ] Reconfigure for use with Yda

- [x] Write unit tests
- [x] Finish Unit Tests

- [x] Make API available
- [ ] Write endpoints for:
  - [x] Locations
  - [x] Pokemon
  - [x] Pokemon of certain type
- [ ] Remove Anachronicistic pokemon (e.g. Annihilape)
- [ ] Set Regional pokemon
- [ ] Clean up move data, long data
- [] Rewrite docs to note changes of above
- [x] Fix missing move data for pokemon
- [] Get json algo working again

### FUTURE FEATURES:

- [x] Download and store images for perpetuity in case i need to self host
- [x] Get real pokemon national number (extract from url, Recycling!)
- [x] speed up json generation
- [x] Implement starter pokemon data from Borrius National Dex (+9 more attached to start)
- [x] Compile API and publish to NPM
- [x] Compile Docker Image
- [x] Publish Docker Image to Dockerhub
- [x] Publish Docker Image to Google Cloud https://borrius-pokemon-scraper-321133146790.australia-southeast1.run.app/borrius_pokemon
- [x] Patch in missing data from PokeAPI
  - [x] Line up data for use with Curadex project
  - [x] Add official portraits from PokeApi
