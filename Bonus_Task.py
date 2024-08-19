from PIL import Image
import requests
from io import BytesIO


def check_color():
    # Fetching Pokemon Data
    url = 'https://pokeapi.co/api/v2/pokemon/charizard'
    response = requests.get(url)
    data = response.json()

    # Fetching image
    sprite_url = data['sprites']['back_default']
    response = requests.get(sprite_url)
    img = Image.open(BytesIO(response.content))

    # Display the image(just for fun)
    img.show()

    # Check for color #1c4050
    for x in range(img.width):
        for y in range(img.height):
            if img.getpixel((x, y)) == (28, 64, 80):  # RGB for #1c4050
                print(f"Pixel with color #1c4050 found at ({x}, {y})")
                return True

    print("Charizard has no pixel with the color #1c4050 :).image will now open")
    return False


check_color()
