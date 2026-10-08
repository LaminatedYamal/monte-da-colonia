import os
import sys
import json
import re
import urllib3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|]', '_', name)
    clean = clean.strip()
    return clean if clean else "file"

def download_file(url, target_path):
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return True
    try:
        r = requests.get(url, headers=HEADERS, verify=False, timeout=25, stream=True)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
        else:
            print(f"Failed to download {url}: HTTP {r.status_code}")
    except Exception as e:
        print(f"Exception downloading {url}: {e}")
    return False

def categorize_media(item):
    url = item.get('source_url', '')
    title = item.get('title', {}).get('rendered', '')
    slug = item.get('slug', '')
    alt = item.get('alt_text', '')
    combined = f"{url} {title} {slug} {alt}".lower()

    if any(k in combined for k in ['unnamed.png', 'logo', 'favicon', 'brand', 'marca', 'benefit_icon']):
        return 'logos'
    if any(k in combined for k in ['vinho', 'azeite', 'vinagre', 'azeitona', 'garrafa', 'bag-in-box', 'tubo', 'lata', 'frasco', '3l', '5l', '0-5l', '250ml', '750ml']):
        return 'products'
    if any(k in combined for k in ['vinha', 'adega', 'visita', 'degostacao', 'degustacao', 'casinha', 'imagem', 'montedacolonia.jpg']):
        return 'estate_and_gallery'
    return 'general'

def main():
    print("=== Step 2: Downloading Media Assets ===")
    with open('extracted_data/raw/media.json', 'r', encoding='utf-8') as f:
        media_items = json.load(f)

    base_dir = os.path.abspath('extracted_assets')
    os.makedirs(base_dir, exist_ok=True)

    downloaded = 0
    categories_count = {}

    for i, item in enumerate(media_items, 1):
        url = item.get('source_url')
        if not url:
            continue
        
        category = categorize_media(item)
        parsed = urlparse(url)
        filename = sanitize_filename(os.path.basename(unquote(parsed.path)))
        if not filename:
            filename = f"media_{item['id']}.jpg"

        cat_folder = os.path.join(base_dir, category)
        target_path = os.path.join(cat_folder, filename)

        success = download_file(url, target_path)
        if success:
            downloaded += 1
            categories_count[category] = categories_count.get(category, 0) + 1
            if downloaded % 20 == 0 or downloaded == len(media_items):
                print(f"Downloaded {downloaded}/{len(media_items)} files...")

    print(f"\nDownload summary:")
    print(f"Total downloaded files: {downloaded}")
    for cat, count in categories_count.items():
        print(f"  - {cat}: {count} assets")

if __name__ == '__main__':
    main()
