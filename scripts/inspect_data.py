import json
from bs4 import BeautifulSoup
import re

with open('extracted_data/raw/media.json', 'r', encoding='utf-8') as f:
    media = json.load(f)

with open('extracted_data/raw/pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

with open('extracted_data/raw/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total media: {len(media)}")
mime_types = {}
logos = []
videos = []
for m in media:
    mime = m.get('mime_type', '')
    mime_types[mime] = mime_types.get(mime, 0) + 1
    url = m.get('source_url', '')
    slug = m.get('slug', '')
    title = m.get('title', {}).get('rendered', '')
    
    if any(k in url.lower() or k in slug.lower() or k in title.lower() for k in ['logo', 'brand', 'marca', 'icone', 'icon']):
        logos.append((m['id'], title, url))
        
    if 'video' in mime or any(k in url.lower() for k in ['.mp4', '.mov', '.webm', '.m4v']):
        videos.append((m['id'], title, url))

print("Mime types in media library:", mime_types)
print("\nLogos identified:")
for lid, ltitle, lurl in logos:
    print(f"  [{lid}] {ltitle} -> {lurl}")

print(f"\nVideos in media library: {len(videos)}")
for vid, vtitle, vurl in videos:
    print(f"  [{vid}] {vtitle} -> {vurl}")

print("\nChecking pages for video embeds (youtube/vimeo/video tags)...")
page_videos = []
for p in pages:
    content = p.get('content', {}).get('rendered', '')
    soup = BeautifulSoup(content, 'html.parser')
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')
        page_videos.append((p.get('title', {}).get('rendered', ''), src))
    for vid_tag in soup.find_all('video'):
        src = vid_tag.get('src', '')
        for s in vid_tag.find_all('source'):
            src = s.get('src', src)
        page_videos.append((p.get('title', {}).get('rendered', ''), src))
    # Check for youtube links or data attributes
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if 'youtube' in href or 'youtu.be' in href or 'vimeo' in href:
            page_videos.append((p.get('title', {}).get('rendered', ''), href))

print("Videos in pages:", page_videos)

print("\nPages list:")
for p in pages:
    print(f"  ID: {p['id']}, Slug: {p['slug']}, Title: {p.get('title', {}).get('rendered')}, Link: {p.get('link')}")

print("\nSample Product structure keys:")
if products:
    p0 = products[0]
    print(list(p0.keys()))
    print("Product 0:", p0.get('name') or p0.get('title'), p0.get('slug'))
