import requests
import re
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8'
}

try:
    r = requests.get('https://www.facebook.com/montedacolonia/', headers=headers, timeout=15)
    print('FB status:', r.status_code)
    img_urls = set(re.findall(r'https://scontent[^\s"\'\\]+', r.text))
    print('Found fbcdn images:', len(img_urls))
    os.makedirs('public/assets/fb_photos', exist_ok=True)
    count = 0
    for u in img_urls:
        clean = u.replace('\\/', '/')
        if any(ext in clean.lower() for ext in ['.jpg', '.png', '.webp']) or 'stp=' in clean:
            try:
                res = requests.get(clean, headers=headers, timeout=10)
                if res.status_code == 200 and len(res.content) > 30000: # only decent size images
                    count += 1
                    with open(f'public/assets/fb_photos/fb_{count}.jpg', 'wb') as f:
                        f.write(res.content)
                    print(f'Saved fb_{count}.jpg ({len(res.content)} bytes)')
                    if count >= 10:
                        break
            except Exception as e:
                pass
except Exception as e:
    print('Error:', e)
