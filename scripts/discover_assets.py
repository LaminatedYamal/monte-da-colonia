import json
from bs4 import BeautifulSoup
import re
import requests
import urllib3

urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0'}

with open('extracted_data/raw/pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

# Also let's fetch products details with WooCommerce store API to get complete product images and details!
r_prods = requests.get('https://montedacolonia.pt/wp-json/wc/store/v1/products?per_page=100', headers=headers, verify=False)
wc_products = r_prods.json() if r_prods.status_code == 200 else []
with open('extracted_data/raw/wc_products.json', 'w', encoding='utf-8') as f:
    json.dump(wc_products, f, ensure_ascii=False, indent=2)

print(f"Fetched {len(wc_products)} full WC Store products!")

all_image_urls = set()
all_video_urls = set()

# Check media library
with open('extracted_data/raw/media.json', 'r', encoding='utf-8') as f:
    media = json.load(f)
for m in media:
    u = m.get('source_url')
    if u:
        all_image_urls.add(u)

# Check all pages HTML directly by requesting the live pages (to capture Elementor rendered output, background images, videos)
for p in pages:
    link = p.get('link')
    title = p.get('title', {}).get('rendered', '')
    print(f"Crawling live page: {title} ({link})")
    try:
        r = requests.get(link, headers=headers, verify=False, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Find img tags
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src:
                all_image_urls.add(src)
            srcset = img.get('srcset')
            if srcset:
                for part in srcset.split(','):
                    s_url = part.strip().split(' ')[0]
                    if s_url:
                        all_image_urls.add(s_url)

        # Find CSS background images
        for tag in soup.find_all(style=True):
            style = tag['style']
            urls = re.findall(r'url\(["\']?(.*?)["\']?\)', style)
            for u in urls:
                if u and not u.startswith('data:'):
                    all_image_urls.add(u)

        # Check for videos (video tags, data-settings, youtube/vimeo, mp4)
        for v in soup.find_all('video'):
            src = v.get('src')
            if src:
                all_video_urls.add(src)
            for s in v.find_all('source'):
                if s.get('src'):
                    all_video_urls.add(s.get('src'))

        for iframe in soup.find_all('iframe'):
            src = iframe.get('src')
            if src and any(k in src.lower() for k in ['youtube', 'vimeo', 'dailymotion', 'wistia', '.mp4']):
                all_video_urls.add(src)

        # Elementor video data-settings
        for el in soup.find_all(attrs={"data-settings": True}):
            ds = el.get("data-settings", "")
            matches = re.findall(r'https?://[^\s"\'\\]+', ds)
            for m in matches:
                clean_m = m.replace(r'\/', '/')
                if any(ext in clean_m.lower() for ext in ['.mp4', '.webm', 'youtube.com', 'youtu.be', 'vimeo.com']):
                    all_video_urls.add(clean_m)

    except Exception as e:
        print(f"Error crawling {link}: {e}")

# Check WC products
for p in wc_products:
    for img in p.get('images', []):
        if img.get('src'):
            all_image_urls.add(img['src'])

print(f"\nTotal unique asset URLs discovered:")
print(f"- Images / SVG / Graphic assets: {len(all_image_urls)}")
print(f"- Videos: {len(all_video_urls)} -> {list(all_video_urls)}")
