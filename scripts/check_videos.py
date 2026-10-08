import json
import re

with open('extracted_data/raw/pages.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)
with open('extracted_data/raw/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)
with open('extracted_data/raw/media.json', 'r', encoding='utf-8') as f:
    media = json.load(f)
with open('extracted_data/raw/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

text_dump = json.dumps(pages) + json.dumps(posts) + json.dumps(media) + json.dumps(products)

video_urls = set()
for m in re.finditer(r'https?://[^\s"\'<>]*(?:youtube\.com|youtu\.be|vimeo\.com|wistia|\.mp4|\.mov|\.webm|\.m4v)[^\s"\'<>]*', text_dump, re.IGNORECASE):
    video_urls.add(m.group(0))

print(f"Total video URLs found: {len(video_urls)}")
for v in video_urls:
    print(" -", v)
