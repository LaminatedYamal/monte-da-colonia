import json
import re
import os
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

urllib3.disable_warnings()

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()

def download(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return
    try:
        r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(r.content)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    print("=== Enriching Products from Live Pages ===")
    with open('extracted_data/copy/catalog/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    for i, p in enumerate(products, 1):
        url = p.get('link')
        if not url:
            continue
        print(f"[{i}/{len(products)}] Scraping {p['name']} ({url})")
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')

            # Rendered Short Description
            short_el = soup.select_one('.woocommerce-product-details__short-description, .summary .entry-summary')
            # Rendered Long Description / Tabs
            tab_desc = soup.select_one('#tab-description, .woocommerce-Tabs-panel--description')
            # Rendered Additional Information (attributes like volume, weight)
            tab_attrs = soup.select_one('#tab-additional_information, .woocommerce-Tabs-panel--additional_information')

            # Extract any rendered tables
            tables_text = []
            for t in soup.find_all('table'):
                rows = []
                for tr in t.find_all('tr'):
                    cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                    if cells:
                        rows.append(" | ".join(cells))
                if rows:
                    tables_text.append("\n".join(rows))

            # Look for gallery images
            gallery_imgs = []
            for img in soup.select('.woocommerce-product-gallery__image img, .woocommerce-product-gallery img'):
                src = img.get('src') or img.get('data-src') or img.get('data-large_image')
                if src:
                    gallery_imgs.append(src)
                    fname = sanitize(os.path.basename(unquote(urlparse(src).path)))
                    download(src, os.path.join('extracted_assets/products', fname))

            p['live_short_description'] = short_el.get_text(strip=True, separator='\n') if short_el else ''
            p['live_description'] = tab_desc.get_text(strip=True, separator='\n') if tab_desc else ''
            p['live_additional_info'] = tab_attrs.get_text(strip=True, separator='\n') if tab_attrs else ''
            p['rendered_tables'] = tables_text
            p['gallery_images'] = list(set(gallery_imgs))

        except Exception as e:
            print(f"Error processing {url}: {e}")

    with open('extracted_data/copy/catalog/products_enriched.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"Enrichment complete. Total products enriched: {len(products)}")

if __name__ == '__main__':
    main()
