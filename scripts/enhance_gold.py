from PIL import Image
import numpy as np

def enhance_gold(path, out_path):
    im = Image.open(path).convert('RGBA')
    arr = np.array(im, dtype=np.float32)

    # Original gold is around RGB (185, 145, 75). Let's brighten it to a warm, luminous champage/regal gold:
    # Highlights: #FBE69C (251, 230, 156)
    # Midtones:   #E2BC68 (226, 188, 104)
    # Shadows:    #C59D4A (197, 157, 74)

    alpha = arr[:, :, 3]
    mask = alpha > 10

    # Boost luminosity while keeping the authentic engraving lines
    # Map brightness
    gray = (arr[:, :, 0] * 0.299 + arr[:, :, 1] * 0.587 + arr[:, :, 2] * 0.114) / 255.0
    
    # Warm radiant gold
    arr[:, :, 0] = np.clip(235 + gray * 20, 0, 255)  # R: 235-255
    arr[:, :, 1] = np.clip(195 + gray * 40, 0, 255)  # G: 195-235
    arr[:, :, 2] = np.clip(105 + gray * 50, 0, 255)  # B: 105-155
    arr[:, :, 3] = alpha  # Preserve exact alpha sharpness

    res = Image.fromarray(arr.astype(np.uint8))
    res.save(out_path)
    print(f"Saved luminous gold: {out_path} ({res.size})")

enhance_gold('public/assets/logos/logo_house_4x.png', 'public/assets/logos/logo_house_gold.png')
enhance_gold('public/assets/logos/logo_text_4x.png', 'public/assets/logos/logo_text_gold.png')
