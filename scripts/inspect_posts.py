import json
from bs4 import BeautifulSoup

with open('extracted_data/raw/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

print(f"Total posts: {len(posts)}")
for p in posts[:10]:
    title = p.get('title', {}).get('rendered', '')
    link = p.get('link', '')
    print(f"- {title} ({link})")
