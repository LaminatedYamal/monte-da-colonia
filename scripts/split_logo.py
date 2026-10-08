import os
from PIL import Image

im = Image.open('extracted_assets/logos/monte_da_colonia_logo.png').convert('RGBA')
w, h = im.size

# Split at Y=59
house = im.crop((0, 0, w, 59))
text = im.crop((0, 59, w, h))

# Trim empty borders
def autocrop(img):
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img

house_trimmed = autocrop(house)
text_trimmed = autocrop(text)

os.makedirs('public/assets/logos', exist_ok=True)

# Save trimmed originals
house_trimmed.save('public/assets/logos/logo_house.png')
text_trimmed.save('public/assets/logos/logo_text.png')

# Also create 4x upscaled high-res versions using Lanczos for crisp rendering on large screens
house_4x = house_trimmed.resize((house_trimmed.width * 4, house_trimmed.height * 4), Image.Resampling.LANCZOS)
text_4x = text_trimmed.resize((text_trimmed.width * 4, text_trimmed.height * 4), Image.Resampling.LANCZOS)

house_4x.save('public/assets/logos/logo_house_4x.png')
text_4x.save('public/assets/logos/logo_text_4x.png')

print(f"House cropped: {house_trimmed.size} -> 4x: {house_4x.size}")
print(f"Text cropped: {text_trimmed.size} -> 4x: {text_4x.size}")
