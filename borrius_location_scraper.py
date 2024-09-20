import openpyxl


wb = openpyxl.load_workbook("./borrius_location_data.xlsx", data_only=True)
sheet = wb["Grass & Cave Encounters"]


locationDataList = []
for pokemon, color in zip(sheet["A"][1:], sheet["B"][1:]):
    if pokemon.value is not None:
        timeOfDay = (
            "Morning"
            if color.font.color.rgb == "ffb500"
            else "Night"
            if color.fill.start_color.rgb == "b300ff"
            else "Swarm"
            if color.fill.start_color.rgb == "ff0000"
            else "Special Encounter"
            if color.fill.start_color.rgb == "00ff00"
            else "All Day"
        )
        locationDataList.append(
            {
                "pokemon": pokemon.value,
                "locationData": [
                    {
                        "location": sheet.cell(row=1, column=2).value,
                        "encounterMethod": "Grass",
                        "timeOfDay": timeOfDay,
                    }
                ],
            }
        )


print(locationDataList)
