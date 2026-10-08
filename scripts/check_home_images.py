import requests
from bs4 import BeautifulSoup
import json
import urllib3
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://montedacolonia.pt/', headers=headers, verify=False)
soup = BeautifulSoup(r.text, 'html.parser')

print("All images on homepage:")
for img in soup.find_all('img'):
    src = img.get('src', '')
    alt = img.get('alt', '')
    cls = img.get('class', [])
    print(f" - {src} | alt: '{alt}' | class: {cls}")

# Look for custom-logo or header elements
print("\nLogos in header:")
for el in soup.select('header img, .elementor-widget-theme-site-logo img, .site-header img, a.custom-logo-link img'):
    print(f"Header logo: {el.get('src')}")

# Also check site icon / favicon / og:image
print("\nMeta tags:")
for tag in soup.find_all(['link', 'meta']):
    rel = tag.get('rel', [])
    prop = tag.get('property', '')
    if any('icon' in r for r in rel) or 'image' in prop:
        print(f"Meta/Link: {tag.get('name') or prop or rel} -> {tag.get('href') or tag.get('content')}")
