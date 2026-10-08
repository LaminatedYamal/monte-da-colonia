import os
import json
import re
import shutil
from bs4 import BeautifulSoup

def clean_html_to_markdown(html_content):
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove script, style, elementor empty tags
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()

    # Convert common elements
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        level = int(h.name[1])
        h.replace_with(f"\n\n{'#' * level} {h.get_text(strip=True)}\n\n")

    for p in soup.find_all('p'):
        p.replace_with(f"\n\n{p.get_text(strip=True)}\n\n")

    for li in soup.find_all('li'):
        li.replace_with(f"\n- {li.get_text(strip=True)}")

    for a in soup.find_all('a'):
        text = a.get_text(strip=True)
        href = a.get('href', '')
        if text and href:
            a.replace_with(f"[{text}]({href})")

    for b in soup.find_all(['b', 'strong']):
        b.replace_with(f"**{b.get_text(strip=True)}**")

    for i in soup.find_all(['i', 'em']):
        i.replace_with(f"*{i.get_text(strip=True)}*")

    text = soup.get_text()
    # Normalize multiple newlines and spaces
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def main():
    print("=== Processing & Organizing Assets ===")
    os.makedirs('extracted_assets/logos', exist_ok=True)
    os.makedirs('extracted_assets/products', exist_ok=True)
    os.makedirs('extracted_assets/estate_and_experience', exist_ok=True)
    os.makedirs('extracted_assets/badges_and_ui', exist_ok=True)

    # Copy / rename main logo
    src_logo = 'extracted_assets/logos/unnamed.png'
    if os.path.exists(src_logo):
        shutil.copy(src_logo, 'extracted_assets/logos/monte_da_colonia_logo.png')
        print("Created extracted_assets/logos/monte_da_colonia_logo.png")

    # Move known winemaker signatures/monograms from general
    gen_dir = 'extracted_assets/general'
    if os.path.exists(os.path.join(gen_dir, 'antoniojusto.png')):
        shutil.move(os.path.join(gen_dir, 'antoniojusto.png'), 'extracted_assets/logos/antonio_justo_signature.png')
    if os.path.exists(os.path.join(gen_dir, 'aj.png')):
        shutil.move(os.path.join(gen_dir, 'aj.png'), 'extracted_assets/logos/aj_monogram.png')

    # Move known estate pictures from general
    estate_files = ['Degostacao.jpg', 'imagem.jpg', 'imagem3.jpg', 'provadevinhos.jpg', 
                    'Visita.jpg', 'Casinha.jpg', 'Vinha.jpg', 'montedacolonia.jpg']
    for ef in estate_files:
        src = os.path.join(gen_dir, ef)
        if os.path.exists(src):
            shutil.move(src, os.path.join('extracted_assets/estate_and_experience', ef))

    # Move badges
    badges = ['Livro-de-Reclamacoes.png', 'Benefit_Icon.svg']
    for b in badges:
        for folder in [gen_dir, 'extracted_assets/logos']:
            src = os.path.join(folder, b)
            if os.path.exists(src):
                shutil.copy(src, os.path.join('extracted_assets/badges_and_ui', b))

    # Identify wine and product photos in general and move to products
    for fname in os.listdir(gen_dir):
        lower = fname.lower()
        if any(term in lower for term in [
            'colheita', 'escolha', 'reserva', 'merlot', 'syrah', 'touriga', 'sauvignon', 
            'fernao', 'espumante', 'rose', 'tinto', 'branco', 'bag-in-box', 'azeite', 'vinagre', 'azeitona'
        ]):
            shutil.move(os.path.join(gen_dir, fname), os.path.join('extracted_assets/products', fname))

    print(f"Products folder now has {len(os.listdir('extracted_assets/products'))} items")
    print(f"Estate folder now has {len(os.listdir('extracted_assets/estate_and_experience'))} items")
    print(f"Logos folder now has {len(os.listdir('extracted_assets/logos'))} items")

    print("\n=== Extracting All Copy ===")
    os.makedirs('extracted_data/copy/pages', exist_ok=True)
    os.makedirs('extracted_data/copy/catalog', exist_ok=True)

    with open('extracted_data/raw/pages.json', 'r', encoding='utf-8') as f:
        pages = json.load(f)

    with open('extracted_data/raw/products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    with open('extracted_data/raw/posts.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)

    with open('extracted_data/raw/wc_products.json', 'r', encoding='utf-8') as f:
        wc_products = json.load(f)

    # 1. Process Pages
    master_pages_md = "# Monte da Colónia — Todas as Páginas e Conteúdos (Website Copy)\n\n"
    
    for page in pages:
        title = page.get('title', {}).get('rendered', 'Página Sem Título')
        slug = page.get('slug', 'page')
        raw_html = page.get('content', {}).get('rendered', '')
        link = page.get('link', '')
        clean_text = clean_html_to_markdown(raw_html)

        page_doc = f"# {title}\n\n**URL Original:** {link}\n**Slug:** `{slug}`\n\n---\n\n## Conteúdo da Página:\n\n{clean_text}\n"
        
        with open(f'extracted_data/copy/pages/{slug}.md', 'w', encoding='utf-8') as f:
            f.write(page_doc)

        master_pages_md += f"## Página: {title} (`/{slug}`)\n\n"
        master_pages_md += f"> URL: {link}\n\n"
        master_pages_md += clean_text + "\n\n---\n\n"

    # 2. Process Products (combining WP REST and WC Store data)
    wc_lookup = {p.get('id'): p for p in wc_products}
    
    catalog_list = []
    catalog_md = "# Catálogo de Produtos Monte da Colónia\n\n"
    catalog_md += "| ID | Nome do Produto | Preço | Categoria | Imagem Principal |\n"
    catalog_md += "|---|---|---|---|---|\n"

    for p in products:
        pid = p.get('id')
        p_name = p.get('title', {}).get('rendered', '')
        slug = p.get('slug', '')
        link = p.get('link', '')
        content_html = p.get('content', {}).get('rendered', '')
        excerpt_html = p.get('excerpt', {}).get('rendered', '')

        # Enrich with WC store details if available
        wc_info = wc_lookup.get(pid, {})
        prices = wc_info.get('prices', {})
        currency_prefix = prices.get('currency_prefix', '€')
        raw_price = prices.get('price', '')
        price_str = f"{currency_prefix} {float(raw_price)/100:.2f}" if raw_price and raw_price.isdigit() else "Sob Consulta / Ver Loja"
        
        categories = [c.get('name') for c in wc_info.get('categories', [])]
        cat_str = ", ".join(categories) if categories else "Geral"

        img_url = ""
        if wc_info.get('images'):
            img_url = wc_info['images'][0].get('src', '')

        item = {
            "id": pid,
            "name": p_name,
            "slug": slug,
            "link": link,
            "price": price_str,
            "categories": categories,
            "image": img_url,
            "description": clean_html_to_markdown(content_html),
            "short_description": clean_html_to_markdown(excerpt_html)
        }
        catalog_list.append(item)

        catalog_md += f"| {pid} | [{p_name}]({link}) | {price_str} | {cat_str} | {img_url} |\n"

    catalog_md += "\n\n## Detalhes Individuais dos Produtos\n\n"
    for item in catalog_list:
        catalog_md += f"### {item['name']}\n"
        catalog_md += f"- **ID:** {item['id']}\n"
        catalog_md += f"- **Slug:** `{item['slug']}`\n"
        catalog_md += f"- **Preço:** {item['price']}\n"
        catalog_md += f"- **Categorias:** {', '.join(item['categories'])}\n"
        catalog_md += f"- **Link Original:** {item['link']}\n"
        catalog_md += f"- **Imagem:** {item['image']}\n\n"
        if item['short_description']:
            catalog_md += f"**Resumo:**\n{item['short_description']}\n\n"
        if item['description']:
            catalog_md += f"**Descrição Completa:**\n{item['description']}\n\n"
        catalog_md += "---\n\n"

    with open('extracted_data/copy/catalog/products.json', 'w', encoding='utf-8') as f:
        json.dump(catalog_list, f, ensure_ascii=False, indent=2)

    with open('extracted_data/copy/catalog/products.md', 'w', encoding='utf-8') as f:
        f.write(catalog_md)

    # 3. Process Nutritional Sheets / Posts
    nutri_list = []
    nutri_md = "# Fichas Nutricionais e Regulamentares (Vinhos)\n\n"
    for post in posts:
        pid = post.get('id')
        p_title = post.get('title', {}).get('rendered', '')
        link = post.get('link', '')
        content_html = post.get('content', {}).get('rendered', '')
        clean_text = clean_html_to_markdown(content_html)

        nutri_item = {
            "id": pid,
            "title": p_title,
            "link": link,
            "content": clean_text
        }
        nutri_list.append(nutri_item)

        nutri_md += f"### {p_title}\n"
        nutri_md += f"- **URL:** {link}\n\n"
        nutri_md += f"{clean_text}\n\n---\n\n"

    with open('extracted_data/copy/catalog/fichas_nutricionais.json', 'w', encoding='utf-8') as f:
        json.dump(nutri_list, f, ensure_ascii=False, indent=2)

    with open('extracted_data/copy/catalog/fichas_nutricionais.md', 'w', encoding='utf-8') as f:
        f.write(nutri_md)

    # 4. Master Presentation Copy Book
    master_copy = f"""# Monte da Colónia — Livro Completo de Conteúdos, Identidade & Assets

Este documento consolida toda a cópia, dados institucionais, catálogo de produtos, fichas técnicas e elementos de identidade do Monte da Colónia extraídos diretamente da plataforma oficial (https://montedacolonia.pt/).

---

## 1. Identidade da Marca e Contactos
- **Nome da Marca:** Monte da Colónia
- **Fundador / Enologia:** António Justo
- **Localização:** Vale de Seda, 7460-160 Fronteira, Portalegre, Alentejo, Portugal
- **Telefone:** (+351) 245 604 190 (Rede fixa nacional)
- **Email:** info@montedacolonia.pt
- **Redes Sociais:**
  - Facebook: https://www.facebook.com/montedacolonia
- **Vídeos Identificados na Web:**
  - "Monte da Colónia | Olivicultura" (BRANDruralis)
  - "Monte da Colónia | Festa da Vindima" (BRANDruralis)

---

{master_pages_md}

---

{catalog_md}

---

{nutri_md}
"""

    with open('extracted_data/MASTER_COPY_BOOK.md', 'w', encoding='utf-8') as f:
        f.write(master_copy)

    print("Master Copy Book written to extracted_data/MASTER_COPY_BOOK.md")

if __name__ == '__main__':
    main()
