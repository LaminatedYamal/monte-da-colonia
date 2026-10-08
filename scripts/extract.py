import os
import sys
import json
import re
import urllib3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_URL = 'https://montedacolonia.pt'
API_URL = f'{BASE_URL}/wp-json'

def fetch_all_items(endpoint):
    items = []
    page = 1
    while True:
        url = f'{API_URL}/{endpoint}?per_page=100&page={page}'
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=20)
            if r.status_code != 200:
                break
            batch = r.json()
            if not batch or not isinstance(batch, list):
                break
            items.extend(batch)
            total_pages = int(r.headers.get('X-WP-TotalPages', 1))
            print(f"Fetched {endpoint} page {page}/{total_pages} ({len(items)} items so far)")
            if page >= total_pages:
                break
            page += 1
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            break
    return items

def main():
    print("=== Step 1: Discovering and downloading WP REST endpoints ===")
    media = fetch_all_items('wp/v2/media')
    pages = fetch_all_items('wp/v2/pages')
    posts = fetch_all_items('wp/v2/posts')
    products = fetch_all_items('wp/v2/product')
    product_cats = fetch_all_items('wp/v2/product_cat')

    print(f"\nDiscovered:")
    print(f"- Media items: {len(media)}")
    print(f"- Pages: {len(pages)}")
    print(f"- Posts: {len(posts)}")
    print(f"- Products: {len(products)}")
    print(f"- Product categories: {len(product_cats)}")

    # Save raw catalog
    os.makedirs('extracted_data/raw', exist_ok=True)
    with open('extracted_data/raw/media.json', 'w', encoding='utf-8') as f:
        json.dump(media, f, ensure_ascii=False, indent=2)
    with open('extracted_data/raw/pages.json', 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    with open('extracted_data/raw/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    with open('extracted_data/raw/products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    with open('extracted_data/raw/product_cats.json', 'w', encoding='utf-8') as f:
        json.dump(product_cats, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
