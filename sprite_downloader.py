# import requests

# def download_sprite(url, filename):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(filename, 'wb') as f:
#             f.write(response.content) 
#     else:
#         print({"Sprite {filename} could not be saved." + response.status_code})

# borrius_numbers = range(1, 495)
# starter_numbers = [246, 247, 248, 374, 375, 376, 443, 444, 445]

# national_page = "https://www.pokemonunboundpokedex.com/national/"
# borrius_page = "https://www.pokemonunboundpokedex.com/borrius/"


# for i in borrius_numbers:
#     sprite_link = f"https://www.pokemonunboundpokedex.com/static/pixelart/{i}.png"
#     for j in national_page:
        
    
#     sprite_link = f"https://www.pokemonunboundpokedex.com/static/pixelart/{i}.png"
#     download_sprite(sprite_link, f"sprites/test{i}.png")