import json
import openpyxl

wb = openpyxl.load_workbook("./borrius_location_data.xlsx", data_only=True)
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
        # Special encounters are shown at the bottom of the row.
        if pokemon == "Special Encounter":
            isSpecialEncounter = 1
            continue

        match sheet.cell(row=row, column=col).fill.start_color.rgb:
            case "ffb500":
                timeOfDay = "Morning"
            case "b300ff":
                timeOfDay = "Night"
            case "ff0000":
                timeOfDay = "Swarm"
            case _:
                timeOfDay = "All Day"

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
