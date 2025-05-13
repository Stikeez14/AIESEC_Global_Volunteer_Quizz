from PIL import Image

with Image.open('green.png') as img:
    img = img.resize((img.width // 2, img.height // 2))
    img.save('green.png')