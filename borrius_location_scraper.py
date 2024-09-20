import json
import openpyxl

wb = openpyxl.load_workbook("./scraperData/borrius_location_data.xlsx", data_only=True)
sheet = wb["Grass & Cave Encounters"]

locationDataList = []

# map through each column of the spreadsheet, apply the headers as locationData.location
for col in range(1, sheet.max_column + 1):
    location_header = sheet.cell(row=1, column=col).value
    isSpecialEncounter = 0
    # map down through each row, applying each value from there as "pokemon"
    for row in range(2, sheet.max_row + 1):
        pokemon = sheet.cell(row=row, column=col).value
        if pokemon is None:
            continue
        # Special encounters are always shown at the bottom of the row.
        if pokemon == "Special Encounter":
            isSpecialEncounter = 1
            continue
        fontColor = sheet.cell(row=row, column=col).font.color
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
            (p for p in locationDataList if p["pokemon"] == pokemon), None
        )
        if existingPokemon is not None:
            existingPokemon["locationData"].append(
                {
                    "location": location_header,
                    "encounterMethod": "Grass" if col < 5 else "Cave",
                    "timeOfDay": timeOfDay,
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
                            "encounterMethod": "Grass" if col < 5 else "Cave",
                            "timeOfDay": timeOfDay,
                            "isSpecialEncounter": isSpecialEncounter,
                        }
                    ],
                }
            )


try:
    fileName = "locationData.json"
    with open(fileName, "w") as fp:
        json.dump(locationDataList, fp, indent=4)
    print(f"{fileName} successfully created")
except Exception as e:
    print(f"Json Generation Failed : {e}")
