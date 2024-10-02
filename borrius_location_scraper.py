import json
import openpyxl

wb = openpyxl.load_workbook("./scraperData/borrius_location_data.xlsx", data_only=True)

locationDataList = []


def correctPokemonName(pokemon):
    pokemon = pokemon.lower().replace(". ", "-").replace("'", "")
    if "dome fossil" in pokemon:
        return "kabuto"
    if "helix fossil" in pokemon:
        return "omanyte"
    if "claw fossil" in pokemon:
        return "anorith"
    if "root fossil" in pokemon:
        return "lileep"
    if "skull fossil" in pokemon:
        return "cranidos"
    if "armor fossil" in pokemon:
        return "shieldon"
    if "cover fossil" in pokemon:
        return "tirtouga"
    if "plume fossil" in pokemon:
        return "archen"
    if "jaw fossil" in pokemon:
        return "tyrunt"
    if "sail fossil" in pokemon:
        return "amaura"
    if "old amber" in pokemon:
        return "aerodactyl"
    if "galarian slowpoke" in pokemon:
        return "slowpoke-galar"
    if "galarian darmanitan" in pokemon:
        return "darmanitan-galar-standard"
    if "galarian " in pokemon:
        return pokemon.replace("galarian ", "") + "-galar"
    if "hisuian " in pokemon:
        return pokemon.replace("hisuian ", "") + "-hisui"
    if "alolan " in pokemon:
        return pokemon.replace("alolan ", "") + "-alola"

    if "indeedee\u2642" in pokemon:
        return "indeedee-male"

    if "indeedee\u2640" in pokemon:
        return "indeedee-female"

    if "flabébé" in pokemon:
        return "flabebe"

    if "nidoran\u2642" in pokemon:
        return "nidoran-m"

    if "nidoran\u2640" in pokemon:
        return "nidoran-f"

    return pokemon


async def getGrassCaveLocations():
    try:
        grassSheet = wb["Grass & Cave Encounters"]
        # map through each column of the spreadsheet, apply the headers as locationData.location
        for col in range(1, grassSheet.max_column + 1):
            location_header = grassSheet.cell(row=1, column=col).value
            isSpecialEncounter = 0
            # map down through each row, applying each value from there as "pokemon"
            for row in range(2, grassSheet.max_row + 1):
                pokemon = grassSheet.cell(row=row, column=col).value
                if pokemon is None:
                    continue
                pokemonName = correctPokemonName(pokemon)

                # Special encounters are always shown at the bottom of the row.
                if pokemonName == "Special Encounter":
                    isSpecialEncounter = 1
                    continue
                fontColor = grassSheet.cell(row=row, column=col).font.color
                if fontColor:
                    rgb = [0, 0, 0]
                    rgb = f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
                    match rgb:
                        # orange
                        case "#FFB500":
                            timeOfDay = "Morning"
                        # purple
                        case "#B300FF":
                            timeOfDay = "Night"
                        # red
                        case "#FF0000":
                            timeOfDay = "Swarm"
                        case "#000000":
                            timeOfDay = "All Day"
                        case _:
                            timeOfDay = "Other"
                else:
                    timeOfDay = "Other"

                # check if "pokemon" already exists in locationDataList, then appends locationData object to array
                existingPokemon = next(
                    (p for p in locationDataList if p["pokemon"] == pokemonName), None
                )
                if existingPokemon is not None:
                    existingPokemon["locationData"].append(
                        {
                            "location": location_header,
                            "encounterMethod": "Grass/Cave",
                            "timeOfDay": timeOfDay,
                            "isSpecialEncounter": isSpecialEncounter,
                        }
                    )
            

    except Exception as e:
        print(f"Failed to get Grass/Cave Locations: {e}")


# Fish Locations also includes rocksmash
async def getFishingLocations():
    try:
        grassSheet = wb["fishingRockSmash"]
        # map through each column of the spreadsheet, apply the headers as locationData.location
        for col in range(1, grassSheet.max_column + 1):
            location_header = grassSheet.cell(row=1, column=col).value
            isSpecialEncounter = 0

            isGoodRod = 0
            isSuperRod = 0
            isUnderwater = 0
            isRockSmash = 0

            # map down through each row, applying each value from there as "pokemon"
            for row in range(2, grassSheet.max_row + 1):
                pokemon = grassSheet.cell(row=row, column=col).value
                if pokemon is None:
                    continue

                # Special encounters are always shown at the bottom of the row (only one in this case).
                if pokemon == "Special Encounter":
                    isSpecialEncounter = 1
                    isGoodRod = 0
                    isSuperRod = 0
                    isUnderwater = 1
                    isRockSmash = 0
                    continue

                if pokemon == "Good Rod":
                    isGoodRod = 1
                    isSuperRod = 0
                    isUnderwater = 0
                    isRockSmash = 0
                    continue
                elif pokemon == "Super Rod":
                    isGoodRod = 0
                    isSuperRod = 1
                    isUnderwater = 0
                    isRockSmash = 0
                elif pokemon == "Underwater":
                    isGoodRod = 0
                    isSuperRod = 0
                    isUnderwater = 1
                    isRockSmash = 0
                    continue
                elif pokemon == "Rock Smash":
                    isGoodRod = 0
                    isSuperRod = 0
                    isUnderwater = 0
                    isRockSmash = 1
                    continue

                method = "Unknown"

                match (isGoodRod, isSuperRod, isUnderwater, isRockSmash):
                    case (1, 0, 0, 0):
                        method = "Good Rod"
                    case (0, 1, 0, 0):
                        method = "Super Rod"
                    case (0, 0, 1, 0):
                        method = "Underwater"
                    case (0, 0, 0, 1):
                        method = "Rock Smash"
                    case _:
                        method = "Unknown"

                pokemonName = correctPokemonName(pokemon)
                # check if "pokemon" already exists in locationDataList, then appends locationData object to array
                existingPokemon = next(
                    (p for p in locationDataList if p["pokemon"] == pokemonName), None
                )
                if existingPokemon is not None:
                    existingPokemon["locationData"].append(
                        {
                            "location": location_header,
                            "encounterMethod": method,
                            "timeOfDay": "All Day",
                            "isSpecialEncounter": isSpecialEncounter,
                        }
                    )
               
    except Exception as e:
        print(f"Failed to retrieve fishing data {e}")


# SURF LOCATIONS
async def getSurfLocations():
    try:
        surfSheet = wb["surfing"]
        # map through each column of the spreadsheet, apply the headers as locationData.location
        for col in range(1, surfSheet.max_column + 1):
            location_header = surfSheet.cell(row=1, column=col).value
            isSpecialEncounter = 0
            # map down through each row, applying each value from there as "pokemon"
            for row in range(2, surfSheet.max_row + 1):
                pokemon = surfSheet.cell(row=row, column=col).value
                if pokemon is None:
                    continue
                # Special encounters are always shown at the bottom of the row.
                if pokemon == "Special Encounter":
                    isSpecialEncounter = 1
                    continue

                # check if "pokemon" already exists in locationDataList, then appends locationData object to array
                existingPokemon = next(
                    (p for p in locationDataList if p["pokemon"] == pokemon), None
                )
                if existingPokemon is not None:
                    existingPokemon["locationData"].append(
                        {
                            "location": location_header,
                            "encounterMethod": "Surfing",
                            "timeOfDay": "All Day",
                            "isSpecialEncounter": isSpecialEncounter,
                        }
                    )
                
    except Exception as e:
        print(f"Failed to get Surf Locations: {e}")


def fillInEvolutionGaps():
    try:
        with open("scraperData/pokelocation.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for pokemon in data:
                pokemonName = correctPokemonName(pokemon["name"])

                existingPokemon = next(
                    (p for p in locationDataList if p["pokemon"] == pokemonName), None
                )

                if existingPokemon is not None and len(existingPokemon["locationData"]) == 0:
                    existingPokemon["locationData"].append(
                        {
                            "location": pokemon["location"],
                            "encounterMethod": "Evolution",
                            "timeOfDay": "All Day",
                            "isSpecialEncounter": 0,
                        }
                    )

    except Exception as e:
        print(f"fillInEvolutionGaps failed: {e}")


def getBorriusPokemonNames():
    with open("scraperData/borrius_pokedex_data.json", "r") as file:
        data = json.load(file)

        for pokemon in data[0]["pokemon"]:
            locationDataList.append(
                {
                    "pokemon": pokemon["name"].lower(),
                    "locationData": [],
                }
            )


async def printLocationJson():
    try:
        getBorriusPokemonNames()
        await getGrassCaveLocations()
        await getSurfLocations()
        await getFishingLocations()
        fillInEvolutionGaps()

        fileName = "scraperData/locationData.json"
        with open(fileName, "w") as fp:
            json.dump(locationDataList, fp, indent=4)
        print(f"{fileName} successfully created")
    except Exception as e:
        print(f"locationData Json Generation Failed : {e}")
