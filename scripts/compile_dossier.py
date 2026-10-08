import json
import os

def compile_master_dossier():
    with open('extracted_data/copy/catalog/products_enriched.json', 'r', encoding='utf-8') as f:
        products = json.load(f)

    with open('extracted_data/copy/catalog/fichas_nutricionais.json', 'r', encoding='utf-8') as f:
        nutri_sheets = json.load(f)

    # Read pages
    pages_data = {}
    pages_dir = 'extracted_data/copy/pages'
    for fname in os.listdir(pages_dir):
        if fname.endswith('.md'):
            with open(os.path.join(pages_dir, fname), 'r', encoding='utf-8') as f:
                pages_data[fname] = f.read()

    doc = """# DOSSIÊ COMPLETO DE CONTEÚDO, IDENTIDADE & AUDITORIA PARA PITCH
## Cliente: Monte da Colónia (Vale de Seda, Fronteira, Alentejo)
**Website Atual:** https://montedacolonia.pt/
**Data de Extração:** Outubro 2026

---

## ÍNDICE
1. [Resumo Executivo & Oportunidades para o Pitch](#1-resumo-executivo--oportunidades-para-o-pitch)
2. [Identidade da Marca, História e Pessoas](#2-identidade-da-marca-história-e-pessoas)
3. [Contactos, Localização e Informações Legais](#3-contactos-localização-e-informações-legais)
4. [Estrutura de Páginas & Cópia Integral dos Textos](#4-estrutura-de-páginas--cópia-integral-dos-textos)
5. [Catálogo Completo de Produtos (40 Artigos)](#5-catálogo-completo-de-produtos-40-artigos)
6. [Regulamentação UE & Fichas Nutricionais de Vinhos (36 Fichas)](#6-regulamentação-ue--fichas-nutricionais-de-vinhos-36-fichas)
7. [Inventário de Recursos Visuais & Audiovisuais](#7-inventário-de-recursos-visuais--audiovisuais)
8. [Recomendações Arquiteturais: Astro vs. Shopify](#8-recomendações-arquiteturais-astro-vs-shopify)

---

## 1. Resumo Executivo & Oportunidades para o Pitch

Durante a auditoria e extração minuciosa da plataforma atual do Monte da Colónia, identificámos fragilidades críticas no website existente que constituem **argumentos irrefutáveis de venda** para a nossa proposta:

1. **Conteúdo Inacabado / "Lorem Ipsum" em Produção:**
   - A página `/services/` contém texto padrão de modelo Elementor em inglês (*"Our Services", "Service 1", "So, have you edited global styles already ;-)"*), prejudicando a perceção de qualidade de uma marca com 1000 hectares no Alentejo.
2. **Secções Fantasma:**
   - A secção *"Testemunho de Clientes"* na Homepage está vazia (apenas o título).
3. **Ligações de Vídeo / Redes Inexistentes:**
   - O link para YouTube no rodapé aponta de volta para a própria homepage. A marca tem presença em vídeo (ex.: reportagens *BRANDruralis* de olivicultura e vindimas) que não está aproveitada no site.
4. **Loja Online Limitada:**
   - O WooCommerce atual tem uma experiência de compra rudimentar, sem filtragem moderna de castas, anos de colheita ou combinações gastronómicas.
5. **Potencial Inexplorado de Enoturismo:**
   - As provas de vinho e visitas à adega/lagar são referidas nos textos mas não possuem um sistema direto de agendamento ou formulário interativo de reserva.
6. **Desempenho e Velocidade:**
   - O site atual carrega dezenas de ficheiros pesados de plugins WordPress/Elementor. Uma versão construída em **Astro** entrega pontuação 100 no Google PageSpeed (Core Web Vitals), carregamento instantâneo e SEO imbatível.

---

## 2. Identidade da Marca, História e Pessoas

- **Herdade:** Monte da Colónia (aprox. 1000 hectares no Vale de Seda, Fronteira, Portalegre, Alentejo).
- **Fundação:** 1980, pelo casal Manuel Pereira e Idalina Pereira.
- **2ª Geração / Gestão Atual:**
  - **António Justo:** Diretor Geral / Gestão Agropecuária (Licenciado em Engenharia Agropecuária pela Univ. de Coimbra).
  - **Manuela Pereira:** Direção de Vendas, Marketing e Promoção (Licenciada em Ensino).
- **Enologia:** Enólogo Rui Vieira.
- **Produção Agrícola:**
  - **Vinha:** 20 hectares. Castas: Aragonez, Cabernet Sauvignon, Arinto, Alicante Bouschet, Castelão, Syrah, Trincadeira, Verdelho, Touriga Nacional e Roupeiro. Produção média: 100 mil L tinto, 10 mil L branco, 6 mil L rosé, além de espumante bruto.
  - **Olival:** 100 hectares (50% Cobrançosa, 40% Galega, 10% outras). Lagar próprio de extração a frio modernizado. Produção média: 200 a 300 mil litros/campanha (Bio, Virgem Extra, Virgem). Azeitonas de conserva tradicionais.
  - **Destilaria (Novo projeto):** Linha de Aguardente, Vinho Licoroso e Gin.

---

## 3. Contactos, Localização e Informações Legais

- **Morada:** Apartado 236, Vale de Seda, 7460-160 Fronteira, Portugal
- **Telefone Fixo:** (+351) 245 604 190 (Rede fixa nacional)
- **Telemóveis:**
  - (+351) 919 095 923 (Rede móvel nacional)
  - (+351) 919 377 050 (Rede móvel nacional)
- **Emails Oficiais:**
  - Geral / Loja: `loja@montedacolonia.pt` / `info@montedacolonia.pt`
  - Direção (António Justo): `antonio.justo@montedacolonia.pt`
  - Comercial (Manuela Pereira): `manuela.pereira@montedacolonia.pt`
- **Coordenadas GPS / Mapa:** Monte da Colónia, Vale de Seda, Fronteira (Google Maps Embed existente).
- **Redes Sociais:**
  - Facebook: `https://www.facebook.com/montedacolonia`

---

## 4. Estrutura de Páginas & Cópia Integral dos Textos

"""
    for fname, content in pages_data.items():
        doc += f"\n### Ficheiro: `{fname}`\n\n```markdown\n{content}\n```\n\n---\n"

    doc += """
## 5. Catálogo Completo de Produtos (40 Artigos)

Abaixo lista-se o catálogo integral com especificações, categorias e galeria:

"""
    for p in products:
        doc += f"### {p['name']}\n"
        doc += f"- **ID:** `{p['id']}` | **Slug:** `{p['slug']}`\n"
        doc += f"- **Categoria(s):** {', '.join(p['categories'])}\n"
        doc += f"- **Preço Indicado:** {p['price']}\n"
        doc += f"- **Imagem Principal:** {p.get('image', 'N/D')}\n"
        if p.get('live_short_description'):
            doc += f"- **Resumo:** {p['live_short_description']}\n"
        if p.get('live_description'):
            doc += f"- **Descrição:** {p['live_description']}\n"
        if p.get('live_additional_info'):
            doc += f"- **Informação Adicional / Formato:** {p['live_additional_info']}\n"
        if p.get('rendered_tables'):
            doc += f"- **Tabelas / Valores:**\n"
            for t in p['rendered_tables']:
                doc += f"  ```\n  {t}\n  ```\n"
        doc += "\n---\n\n"

    doc += """
## 6. Regulamentação UE & Fichas Nutricionais de Vinhos (36 Fichas)

Em cumprimento com o Regulamento (UE) 2021/2117 relativo à rotulagem nutricional e lista de ingredientes dos vinhos, todas as referências possuem ficha nutricional detalhada:

"""
    for n in nutri_sheets:
        doc += f"#### {n['title']}\n"
        doc += f"- **URL:** {n['link']}\n"
        doc += f"```text\n{n['content']}\n```\n\n"

    doc += """
## 7. Inventário de Recursos Visuais & Audiovisuais

Todos os ficheiros foram descarregados em resolução máxima e categorizados na pasta `extracted_assets/`:

- **Logótipos e Identidade (`extracted_assets/logos/` - 12 ficheiros):**
  - `monte_da_colonia_logo.png`: Logótipo oficial institucional.
  - `antonio_justo_signature.png`: Assinatura do enólogo/diretor António Justo.
  - `aj_monogram.png`: Monograma "AJ".
  - `favicon-32x32-1.png`: Ícone de navegador.
  - `Partners-Logo_1` a `6.svg`: Vetores de selos e parceiros.
- **Produtos (`extracted_assets/products/` - 79 ficheiros):**
  - Fotografias individuais de garrafas, bag-in-box, tubos metálicos de 2L, latas e garrafões de azeite virgem extra, e frascos de azeitonas.
- **Herdade e Enoturismo (`extracted_assets/estate_and_experience/` - 8 ficheiros):**
  - Vinhas (`Vinha.jpg`), Provas de vinhos (`provadevinhos.jpg`), Degustação (`Degostacao.jpg`), Visitas (`Visita.jpg`), Casas tradicionais (`Casinha.jpg`).
- **Badges e Selos (`extracted_assets/badges_and_ui/` - 2 ficheiros):**
  - Livro de Reclamações e ícones de garantia.

---

## 8. Recomendações Arquiteturais: Astro vs. Shopify

### Abordagem Recomendada: Astro como Frontend Headless + Shopify Storefront
1. **Design sem Limitações:** Com Astro podemos criar uma experiência visual elegante ao nível das grandes casas vitivinícolas mundiais (como Herdade do Esporão ou Cartuxa).
2. **Velocidade Imbatível:** Tempo de carregamento inferior a 1 segundo, essencial para mobile.
3. **Checkout e Gestão no Shopify:** O cliente utiliza o Shopify Admin para gerir encomendas, inventário, portes de envio (CTT/SEUR) e métodos de pagamento portugueses (MB Way, Multibanco, Cartão).
4. **Fichas Nutricionais Digitais (QR Codes):** As páginas das fichas nutricionais em Astro são estáticas e ultra-rápidas para serem lidas através do QR Code impresso no contra-rótulo físico das garrafas, cumprindo a lei europeia a 100%.
"""

    with open('extracted_data/DOSSIER_PITCH_MONTE_DA_COLONIA.md', 'w', encoding='utf-8') as f:
        f.write(doc)
    print("Dossier created successfully!")

if __name__ == '__main__':
    compile_master_dossier()
