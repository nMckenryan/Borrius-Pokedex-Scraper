import asyncio
import json
import openpyxl

wb = openpyxl.load_workbook("./scraperData/borrius_location_data.xlsx", data_only=True)

locationDataList = []


async def getUniquePokemon():
    starters = [
        "Larvitar",
        "Metang",
        "Gible",
    ]

    for starter in starters:
        locationDataList.append(
            {
                "pokemon": starter,
                "locationData": [
                    {
                        "location": "Frozen Heights",
                        "encounterMethod": "Starter",
                        "timeOfDay": "All Day",
                        "isSpecialEncounter": 0,
                    }
                ],
            }
        )

    # Handle Magikarp as it is very prevalent
    locationDataList.append(
        {
            "pokemon": "Magikarp",
            "locationData": [
                {
                    "location": "Pretty much every Water Spot",
                    "encounterMethod": "Old Rod",
                    "timeOfDay": "All Day",
                    "isSpecialEncounter": 0,
                }
            ],
        }
    )


def correctPokemonName(pokemon):
    if "Dome Fossil" in pokemon:
        return "Kabuto"
    if "Helix Fossil" in pokemon:
        return "Omanyte"
    if "Claw Fossil" in pokemon:
        return "Anorith"
    if "Root Fossil" in pokemon:
        return "Lileep"
    if "Skull Fossil" in pokemon:
        return "Cranidos"
    if "Armour Fossil" in pokemon:
        return "Shieldon"
    if "Cover Fossil" in pokemon:
        return "Tirtouga"
    if "Plume Fossil" in pokemon:
        return "Archen"
    if "Jaw Fossil" in pokemon:
        return "Tyrunt"
    if "Sail Fossil" in pokemon:
        return "Amaura"
    if "Old Amber" in pokemon:
        return "Aerodactyl"

    if "sirfetch'd" in pokemon or "farfetch'd" in pokemon:
        return pokemon.replace("sirfetch'd", "sirfetchd").replace(
            "farfetch'd", "farfetchd-galar"
        )
    if "Galarian " in pokemon:
        return pokemon.replace("Galarian ", "") + "-Galar"
    if "Alolan " in pokemon:
        return pokemon.replace("Alolan ", "") + "-Alola"

    if "Indeedee\u2642\ufe0f" in pokemon or "indeedee♀️" in pokemon:
        return pokemon.replace("indeedee♂️", "Indeedee\u2640\ufe0f").replace(
            "indeedee♀️", "indeedee-female"
        )

    if "flabébé" in pokemon:
        return "flabebe"

    if "nidoran♀️" in pokemon or "nidoran♂️" in pokemon:
        return pokemon.replace("nidoran♀️", "nidoran-f").replace("nidoran♂️", "nidoran-m")

    return pokemon


async def getGrassCaveLocations():
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
            else:
                locationDataList.append(
                    {
                        "pokemon": pokemonName,
                        "locationData": [
                            {
                                "location": location_header,
                                "encounterMethod": "Grass/Cave",
                                "timeOfDay": timeOfDay,
                                "isSpecialEncounter": isSpecialEncounter,
                            }
                        ],
                    }
                )


# Fish Locations also includes rocksmash
async def getFishingLocations():
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
            else:
                locationDataList.append(
                    {
                        "pokemon": pokemonName,
                        "locationData": [
                            {
                                "location": location_header,
                                "encounterMethod": method,
                                "timeOfDay": "All Day",
                                "isSpecialEncounter": isSpecialEncounter,
                            }
                        ],
                    }
                )


# SURF LOCATIONS
async def getSurfLocations():
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
            else:
                locationDataList.append(
                    {
                        "pokemon": pokemon,
                        "locationData": [
                            {
                                "location": location_header,
                                "encounterMethod": "Surfing",
                                "timeOfDay": "All Day",
                                "isSpecialEncounter": isSpecialEncounter,
                            }
                        ],
                    }
                )


async def printLocationJson():
    try:
        await getGrassCaveLocations()
        await getSurfLocations()
        await getFishingLocations()
        await getUniquePokemon()
        fileName = "scraperData/locationData.json"
        with open(fileName, "w") as fp:
            json.dump(locationDataList, fp, indent=4)
        print(f"{fileName} successfully created")
    except Exception as e:
        print(f"Json Generation Failed : {e}")
