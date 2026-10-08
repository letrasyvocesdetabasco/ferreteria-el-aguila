#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_preview_html.py
Ferretería y Tlapalería El Águila - Visor y Catálogo Visual Truper 2026

Genera un visor web interactivo de alto impacto (truper_preview.html) que
replica la estética del catálogo oficial de Truper (truper.com):
- Tarjetas de estudio en blanco puro con elevación sutil
- Badges cromáticos oficiales para las 7 marcas (Truper, Pretul, Volteck, Foset, Hermex, Fiero, Klintek)
- Pestañas de filtrado intuitivo por marca y categoría técnica
- Buscador reactivo en tiempo real con resaltado
- Ficha técnica desplegable (modal interactivo)
- Vista dual: Familias de Catálogo (260) vs. Artículos en Tienda El Águila (333)
"""

import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "data", "truper_poc_manifest.json")
PRODUCTS_PATH = os.path.join(PROJECT_ROOT, "data", "products.json")
OUTPUT_HTML = os.path.join(PROJECT_ROOT, "truper_preview.html")

def generate_preview():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    with open(PRODUCTS_PATH, "r", encoding="utf-8") as f:
        products = json.load(f)

    products_by_sku = {p.get("sku"): p for p in products if p.get("sku")}

    groups_data = manifest.get("groups", [])
    updated_products = manifest.get("updated_products", [])

    # Enriquecer updated_products con precio, categoría y descripción
    for up in updated_products:
        prod = products_by_sku.get(up.get("sku"))
        if prod:
            up["base_price"] = prod.get("base_price", 0)
            up["category"] = prod.get("category", "")
            up["description"] = prod.get("description", "")
            up["image"] = prod.get("image", "")

    # Marcas y sus colores característicos
    brand_styles = {
        "truper": {"bg": "#ff5000", "color": "#ffffff", "border": "#e04800", "label": "TRUPER", "accent": "#ff5000"},
        "pretul": {"bg": "#facc15", "color": "#78350f", "border": "#eab308", "label": "PRETUL", "accent": "#ca8a04"},
        "volteck": {"bg": "#0284c7", "color": "#ffffff", "border": "#0369a1", "label": "VOLTECK", "accent": "#0284c7"},
        "foset": {"bg": "#0d9488", "color": "#ffffff", "border": "#0f766e", "label": "FOSET", "accent": "#0d9488"},
        "hermex": {"bg": "#334155", "color": "#ffffff", "border": "#1e293b", "label": "HERMEX", "accent": "#334155"},
        "fiero": {"bg": "#2563eb", "color": "#ffffff", "border": "#1d4ed8", "label": "FIERO", "accent": "#2563eb"},
        "klintek": {"bg": "#16a34a", "color": "#ffffff", "border": "#15803d", "label": "KLINTEK", "accent": "#16a34a"}
    }

    # Extraer categorías únicas
    categories = sorted(list(set(g.get("category", "Herramientas Manuales") for g in groups_data)))

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catálogo Oficial Truper 2026 | Ferretería El Águila</title>
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <style>
    :root {{
      --truper-orange: #ff5000;
      --truper-orange-dark: #d94300;
      --truper-black: #111827;
      --truper-gray: #374151;
      --bg-canvas: #f3f4f6;
      --card-bg: #ffffff;
      --border-color: #e5e7eb;
      --border-light: #f3f4f6;
      --text-main: #1f2937;
      --text-muted: #6b7280;
      --primary-red: #c9242b;
      --success-green: #10b981;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg-canvas);
      color: var(--text-main);
      line-height: 1.5;
      padding-bottom: 80px;
    }}

    /* BARRA SUPERIOR DE MARCAS TRUPER */
    .top-brand-strip {{
      background: #0b0f19;
      color: #9ca3af;
      font-size: 0.75rem;
      padding: 8px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1f2937;
    }}
    .brand-logos {{
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .brand-pill-tag {{
      font-weight: 800;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      font-size: 0.7rem;
      padding: 2px 8px;
      border-radius: 4px;
    }}
    .brand-tag-truper {{ background: #ff5000; color: #fff; }}
    .brand-tag-pretul {{ background: #facc15; color: #78350f; }}
    .brand-tag-volteck {{ background: #0284c7; color: #fff; }}
    .brand-tag-foset {{ background: #0d9488; color: #fff; }}
    .brand-tag-hermex {{ background: #475569; color: #fff; }}
    .brand-tag-fiero {{ background: #2563eb; color: #fff; }}
    .brand-tag-klintek {{ background: #16a34a; color: #fff; }}

    /* HEADER PRINCIPAL ESTILO TRUPER */
    header {{
      background: #ffffff;
      border-bottom: 3px solid var(--truper-orange);
      padding: 24px 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }}
    .header-container {{
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .header-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .brand-title-area {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .truper-logo-badge {{
      background: var(--truper-orange);
      color: white;
      font-size: 1.3rem;
      font-weight: 900;
      letter-spacing: 2px;
      padding: 8px 18px;
      border-radius: 6px;
      text-transform: uppercase;
      box-shadow: 0 4px 12px rgba(255, 80, 0, 0.3);
    }}
    .store-tagline {{
      font-size: 0.85rem;
      color: var(--text-muted);
      font-weight: 500;
    }}
    .header-link-btn {{
      background: var(--primary-red);
      color: white;
      text-decoration: none;
      font-weight: 700;
      font-size: 0.9rem;
      padding: 10px 20px;
      border-radius: 8px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: background 0.2s, transform 0.1s;
    }}
    .header-link-btn:hover {{
      background: #a81c22;
      transform: translateY(-1px);
    }}

    /* MÉTRICAS DESTACADAS */
    .metrics-bar {{
      max-width: 1400px;
      margin: 24px auto 0;
      padding: 0 20px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
    }}
    .metric-card {{
      background: white;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 18px 20px;
      text-align: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
      transition: transform 0.2s;
    }}
    .metric-card:hover {{
      transform: translateY(-2px);
    }}
    .metric-val {{
      font-size: 2rem;
      font-weight: 900;
      color: var(--truper-orange);
      line-height: 1.1;
    }}
    .metric-label {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-top: 4px;
    }}

    /* TOOLBAR Y FILTROS */
    .toolbar-wrapper {{
      max-width: 1400px;
      margin: 24px auto;
      padding: 0 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .search-filter-panel {{
      background: white;
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }}
    .search-row {{
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .search-input-wrap {{
      flex: 1;
      min-width: 280px;
      position: relative;
    }}
    .search-input-wrap input {{
      width: 100%;
      padding: 12px 18px 12px 42px;
      font-size: 1rem;
      border: 1.5px solid var(--border-color);
      border-radius: 10px;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .search-input-wrap input:focus {{
      border-color: var(--truper-orange);
      box-shadow: 0 0 0 4px rgba(255, 80, 0, 0.12);
    }}
    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.1rem;
      color: #9ca3af;
    }}
    .view-toggle-btns {{
      display: flex;
      gap: 8px;
    }}
    .view-btn {{
      padding: 11px 20px;
      font-size: 0.9rem;
      font-weight: 700;
      border: 1.5px solid var(--border-color);
      border-radius: 10px;
      background: white;
      cursor: pointer;
      color: var(--text-main);
      transition: all 0.2s;
    }}
    .view-btn.active {{
      background: var(--truper-orange);
      border-color: var(--truper-orange);
      color: white;
      box-shadow: 0 3px 10px rgba(255, 80, 0, 0.25);
    }}

    /* FILTROS POR MARCA Y CATEGORÍA */
    .filter-chips-row {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 14px;
      padding-top: 14px;
      border-top: 1px solid var(--border-light);
    }}
    .filter-chip {{
      padding: 6px 14px;
      font-size: 0.8rem;
      font-weight: 700;
      border-radius: 20px;
      cursor: pointer;
      border: 1px solid var(--border-color);
      background: #f9fafb;
      color: var(--text-gray);
      transition: all 0.15s;
    }}
    .filter-chip:hover {{
      background: #f3f4f6;
      border-color: #cbd5e1;
    }}
    .filter-chip.active {{
      background: var(--truper-black);
      color: white;
      border-color: var(--truper-black);
    }}

    /* GRID DE PRODUCTOS ESTILO TRUPER STUDIO */
    .container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 0 20px;
    }}
    .products-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 22px;
    }}
    .product-card {{
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 14px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
      transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
      cursor: pointer;
      position: relative;
    }}
    .product-card:hover {{
      transform: translateY(-5px);
      box-shadow: 0 12px 24px rgba(0,0,0,0.08);
      border-color: #d1d5db;
    }}
    .card-photo-box {{
      background: #ffffff;
      height: 250px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 16px;
      border-bottom: 1px solid #f3f4f6;
      position: relative;
    }}
    .card-photo-box img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform 0.3s ease;
    }}
    .product-card:hover .card-photo-box img {{
      transform: scale(1.04);
    }}
    .card-content {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}
    .card-header-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .badge-brand {{
      font-size: 0.7rem;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 6px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    .card-cat-pill {{
      font-size: 0.72rem;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .card-title {{
      font-size: 1.05rem;
      font-weight: 800;
      line-height: 1.35;
      color: var(--truper-black);
      margin-bottom: 10px;
    }}
    .card-desc {{
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 14px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .card-footer {{
      margin-top: auto;
      background: #f9fafb;
      border: 1px solid #f3f4f6;
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 0.78rem;
    }}
    .code-chip {{
      display: inline-block;
      background: #ffffff;
      border: 1px solid #e5e7eb;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.74rem;
      font-weight: 700;
      margin: 2px 3px 2px 0;
      color: #1f2937;
    }}
    .price-badge {{
      font-size: 1.35rem;
      font-weight: 900;
      color: var(--primary-red);
      margin: 8px 0;
    }}
    .btn-quote-wa {{
      background: #25d366;
      color: white;
      text-decoration: none;
      font-weight: 700;
      font-size: 0.82rem;
      padding: 8px 14px;
      border-radius: 8px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      margin-top: 10px;
      transition: background 0.15s;
    }}
    .btn-quote-wa:hover {{
      background: #1eb956;
    }}

    /* MODAL DE DETALLE DE PRODUCTO */
    .modal-backdrop {{
      display: none;
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(17, 24, 39, 0.7);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .modal-box {{
      background: white;
      width: 100%;
      max-width: 800px;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 20px 40px rgba(0,0,0,0.25);
      position: relative;
      display: flex;
      flex-direction: column;
      max-height: 90vh;
    }}
    .modal-header {{
      padding: 16px 24px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .modal-title {{
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--truper-black);
    }}
    .modal-close-btn {{
      background: #f3f4f6;
      border: none;
      font-size: 1.2rem;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
    }}
    .modal-body {{
      padding: 24px;
      overflow-y: auto;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }}
    @media (max-width: 700px) {{
      .modal-body {{
        grid-template-columns: 1fr;
      }}
    }}
    .modal-img-wrap {{
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 320px;
    }}
    .modal-img-wrap img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}
    .modal-info {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    /* NO RESULTS */
    .empty-state {{
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      background: white;
      border-radius: 14px;
      border: 1px dashed var(--border-color);
    }}
    .empty-state h3 {{
      font-size: 1.3rem;
      margin-bottom: 8px;
    }}
  </style>
</head>
<body>

  <!-- BARRA DE MARCAS TRUPER -->
  <div class="top-brand-strip">
    <div class="brand-logos">
      <span style="font-weight: 800; color: #fff;">MARCAS DEL GRUPO:</span>
      <span class="brand-pill-tag brand-tag-truper">TRUPER</span>
      <span class="brand-pill-tag brand-tag-pretul">PRETUL</span>
      <span class="brand-pill-tag brand-tag-volteck">VOLTECK</span>
      <span class="brand-pill-tag brand-tag-foset">FOSET</span>
      <span class="brand-pill-tag brand-tag-hermex">HERMEX</span>
      <span class="brand-pill-tag brand-tag-fiero">FIERO</span>
      <span class="brand-pill-tag brand-tag-klintek">KLINTEK</span>
    </div>
    <div>Catálogo Oficial 2026 | Edición Especial El Águila</div>
  </div>

  <!-- HEADER -->
  <header>
    <div class="header-container">
      <div class="header-top">
        <div class="brand-title-area">
          <div class="truper-logo-badge">TRUPER</div>
          <div>
            <h1 style="font-size: 1.5rem; font-weight: 900; color: var(--truper-black);">
              Catálogo Nacional 2026 — Visor de Estudio
            </h1>
            <div class="store-tagline">
              Ferretería y Tlapalería El Águila — {len(groups_data)} Familias Visuales &amp; {len(updated_products)} Productos Vinculados
            </div>
          </div>
        </div>
        <div>
          <a href="http://localhost:8080" target="_blank" class="header-link-btn">
            <span>Ir a Tienda en Vivo (17,641 Artículos)</span>
            <span>&rarr;</span>
          </a>
        </div>
      </div>
    </div>
  </header>

  <!-- MÉTRICAS EN VIVO -->
  <div class="metrics-bar">
    <div class="metric-card">
      <div class="metric-val">{manifest.get('total_catalog_groups', len(groups_data))}</div>
      <div class="metric-label">Familias Visuales Extraídas</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">{manifest.get('total_store_products_updated', len(updated_products))}</div>
      <div class="metric-label">Productos Vinculados en Tienda</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">{manifest.get('total_sku_mappings', 1386)}</div>
      <div class="metric-label">Códigos y SKUs Homologados</div>
    </div>
    <div class="metric-card">
      <div class="metric-val" style="color: #10b981;">500x500</div>
      <div class="metric-label">Lienzo Blanco WebP de Estudio</div>
    </div>
  </div>

  <!-- TOOLBAR Y FILTRADO INTUITIVO -->
  <div class="toolbar-wrapper">
    <div class="search-filter-panel">
      <div class="search-row">
        <div class="search-input-wrap">
          <span class="search-icon">&#128269;</span>
          <input type="text" id="searchInput" placeholder="Buscar por herramienta, clave (ej. MT-16, VER-1/2), código (16701, 45000), o marca..." />
        </div>
        <div class="view-toggle-btns">
          <button class="view-btn active" id="btnViewGroups" onclick="setViewMode('groups')">
            Familias de Catálogo ({len(groups_data)})
          </button>
          <button class="view-btn" id="btnViewProducts" onclick="setViewMode('products')">
            Productos en Tienda ({len(updated_products)})
          </button>
        </div>
      </div>

      <!-- Filtros de Marca -->
      <div class="filter-chips-row" id="brandFilterRow">
        <span class="filter-chip active" onclick="setBrandFilter('all', this)">Todas las Marcas</span>
        <span class="filter-chip" onclick="setBrandFilter('truper', this)">TRUPER</span>
        <span class="filter-chip" onclick="setBrandFilter('pretul', this)">PRETUL</span>
        <span class="filter-chip" onclick="setBrandFilter('volteck', this)">VOLTECK</span>
        <span class="filter-chip" onclick="setBrandFilter('foset', this)">FOSET</span>
        <span class="filter-chip" onclick="setBrandFilter('hermex', this)">HERMEX</span>
        <span class="filter-chip" onclick="setBrandFilter('fiero', this)">FIERO</span>
        <span class="filter-chip" onclick="setBrandFilter('klintek', this)">KLINTEK</span>
      </div>

      <!-- Filtros de Categoría -->
      <div class="filter-chips-row" id="categoryFilterRow">
        <span class="filter-chip active" onclick="setCategoryFilter('all', this)">Todas las Categorías</span>
"""

    for cat in categories:
        html_content += f"""        <span class="filter-chip" onclick="setCategoryFilter('{cat}', this)">{cat}</span>\n"""

    html_content += f"""      </div>
    </div>
  </div>

  <!-- CONTENEDOR PRINCIPAL DE TARJETAS -->
  <div class="container">

    <!-- VISTA 1: FAMILIAS VISUALES DE ESTUDIO (260) -->
    <div id="gridGroups" class="products-grid">
"""

    for g in groups_data:
        brand = g.get("brand", "Truper")
        brand_key = brand.lower()
        bs = brand_styles.get(brand_key, brand_styles["truper"])
        cat = g.get("category", "Herramientas Manuales")
        codes = g.get("codes", [])
        codes_chips = "".join([f'<span class="code-chip">{c}</span>' for c in codes[:6]])
        if len(codes) > 6:
            codes_chips += f'<span class="code-chip">+{len(codes)-6} más</span>'
        img_src = f"assets/images/products/truper/{g.get('output_filename', '')}"

        html_content += f"""
      <div class="product-card item-card" 
           data-view="groups"
           data-brand="{brand_key}"
           data-category="{cat}"
           data-title="{g.get('title', '')}"
           data-desc="{g.get('description', '')}"
           data-codes="{' '.join(codes)}"
           data-img="{img_src}"
           onclick="openModal(this)">
        <div class="card-photo-box">
          <img src="{img_src}" alt="{g.get('title', '')}" loading="lazy" />
        </div>
        <div class="card-content">
          <div class="card-header-meta">
            <span class="badge-brand" style="background:{bs['bg']}; color:{bs['color']}; border: 1px solid {bs['border']};">
              {brand}
            </span>
            <span class="card-cat-pill">{cat}</span>
          </div>
          <h2 class="card-title">{g.get('title', '')}</h2>
          <p class="card-desc">{g.get('description', '')}</p>
          <div class="card-footer">
            <div style="font-weight: 700; color: #4b5563; margin-bottom: 4px;">Códigos y Claves Cubiertos:</div>
            <div>{codes_chips}</div>
          </div>
        </div>
      </div>
"""

    html_content += f"""
    </div>

    <!-- VISTA 2: ARTÍCULOS EN TIENDA VINCULADOS (333) -->
    <div id="gridProducts" class="products-grid" style="display: none;">
"""

    for p in updated_products:
        brand = p.get("brand", "Truper")
        brand_key = brand.lower()
        bs = brand_styles.get(brand_key, brand_styles["truper"])
        cat = p.get("category", "Herramientas")
        sku = p.get("sku", "")
        price = p.get("base_price", 0)
        img_src = p.get("new_image", p.get("image", ""))
        name = p.get("name", "")
        family = p.get("group", "")

        wa_msg = f"Hola, deseo cotizar el producto: {name} (SKU: {sku}) visto en el catálogo oficial Truper de Ferretería El Águila."
        import urllib.parse
        wa_url = f"https://wa.me/529931412679?text={urllib.parse.quote(wa_msg)}"

        html_content += f"""
      <div class="product-card item-card"
           data-view="products"
           data-brand="{brand_key}"
           data-category="{cat}"
           data-title="{name}"
           data-desc="{family} — {p.get('matched_by', '')}"
           data-codes="{sku}"
           data-img="{img_src}"
           onclick="openModal(this)">
        <div class="card-photo-box">
          <img src="{img_src}" alt="{name}" loading="lazy" />
        </div>
        <div class="card-content">
          <div class="card-header-meta">
            <span class="badge-brand" style="background:{bs['bg']}; color:{bs['color']}; border: 1px solid {bs['border']};">
              {brand}
            </span>
            <span class="card-cat-pill">SKU: {sku}</span>
          </div>
          <h2 class="card-title">{name}</h2>
          <div class="price-badge">${price:,.2f} MXN</div>
          <p class="card-desc">Familia: {family} ({p.get('matched_by', '')})</p>
          <a href="{wa_url}" target="_blank" class="btn-quote-wa" onclick="event.stopPropagation();">
            <span>&#128172; Cotizar por WhatsApp</span>
          </a>
        </div>
      </div>
"""

    html_content += f"""
    </div>

    <!-- ESTADO VACÍO -->
    <div id="emptyState" class="empty-state" style="display: none;">
      <h3>No se encontraron productos</h3>
      <p style="color: var(--text-muted);">Intenta ajustar los términos de búsqueda o cambiar los filtros de marca y categoría.</p>
    </div>

  </div>

  <!-- MODAL DE ESPECIFICACIONES DE PRODUCTO -->
  <div class="modal-backdrop" id="productModal" onclick="closeModal(event)">
    <div class="modal-box" onclick="event.stopPropagation();">
      <div class="modal-header">
        <h3 class="modal-title" id="modalTitle">Detalle de Producto</h3>
        <button class="modal-close-btn" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <div class="modal-img-wrap">
          <img id="modalImg" src="" alt="" />
        </div>
        <div class="modal-info">
          <div>
            <span id="modalBrandBadge" class="badge-brand">TRUPER</span>
            <span id="modalCategory" style="margin-left: 8px; font-size: 0.85rem; color: var(--text-muted); font-weight: 600;"></span>
          </div>
          <p id="modalDesc" style="color: #374151; font-size: 0.95rem; line-height: 1.5;"></p>
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
            <strong style="display: block; font-size: 0.85rem; color: #1e293b; margin-bottom: 6px;">Códigos y Claves Asociados:</strong>
            <div id="modalCodesWrap"></div>
          </div>
          <a id="modalWhatsAppBtn" href="#" target="_blank" class="btn-quote-wa" style="padding: 12px; font-size: 0.95rem;">
            &#128172; Cotizar este artículo vía WhatsApp
          </a>
        </div>
      </div>
    </div>
  </div>

  <script>
    let currentView = 'groups';
    let selectedBrand = 'all';
    let selectedCategory = 'all';

    function setViewMode(mode) {{
      currentView = mode;
      document.getElementById('btnViewGroups').classList.toggle('active', mode === 'groups');
      document.getElementById('btnViewProducts').classList.toggle('active', mode === 'products');
      document.getElementById('gridGroups').style.display = mode === 'groups' ? 'grid' : 'none';
      document.getElementById('gridProducts').style.display = mode === 'products' ? 'grid' : 'none';
      filterCards();
    }}

    function setBrandFilter(brand, element) {{
      selectedBrand = brand.toLowerCase();
      document.querySelectorAll('#brandFilterRow .filter-chip').forEach(el => el.classList.remove('active'));
      element.classList.add('active');
      filterCards();
    }}

    function setCategoryFilter(category, element) {{
      selectedCategory = category;
      document.querySelectorAll('#categoryFilterRow .filter-chip').forEach(el => el.classList.remove('active'));
      element.classList.add('active');
      filterCards();
    }}

    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', filterCards);

    function filterCards() {{
      const query = searchInput.value.toLowerCase().trim();
      const activeGrid = currentView === 'groups' ? document.getElementById('gridGroups') : document.getElementById('gridProducts');
      const cards = activeGrid.querySelectorAll('.item-card');
      let visibleCount = 0;

      cards.forEach(card => {{
        const brand = card.getAttribute('data-brand') || '';
        const category = card.getAttribute('data-category') || '';
        const title = (card.getAttribute('data-title') || '').toLowerCase();
        const desc = (card.getAttribute('data-desc') || '').toLowerCase();
        const codes = (card.getAttribute('data-codes') || '').toLowerCase();

        const matchBrand = (selectedBrand === 'all' || brand === selectedBrand);
        const matchCategory = (selectedCategory === 'all' || category === selectedCategory);
        const matchSearch = (!query || title.includes(query) || desc.includes(query) || codes.includes(query) || brand.includes(query));

        if (matchBrand && matchCategory && matchSearch) {{
          card.style.display = 'flex';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      document.getElementById('emptyState').style.display = visibleCount === 0 ? 'block' : 'none';
    }}

    function openModal(card) {{
      const title = card.getAttribute('data-title');
      const desc = card.getAttribute('data-desc');
      const brand = card.getAttribute('data-brand').toUpperCase();
      const category = card.getAttribute('data-category');
      const img = card.getAttribute('data-img');
      const codesStr = card.getAttribute('data-codes') || '';
      const codes = codesStr.split(' ').filter(c => c.trim().length > 0);

      document.getElementById('modalTitle').textContent = title;
      document.getElementById('modalDesc').textContent = desc;

      const brandKey = (card.getAttribute('data-brand') || 'truper').toLowerCase();
      const brandPalette = {{
        'truper': {{ bg: '#ff5000', color: '#ffffff', border: '#e04800' }},
        'pretul': {{ bg: '#facc15', color: '#78350f', border: '#eab308' }},
        'volteck': {{ bg: '#0284c7', color: '#ffffff', border: '#0369a1' }},
        'foset': {{ bg: '#0d9488', color: '#ffffff', border: '#0f766e' }},
        'hermex': {{ bg: '#334155', color: '#ffffff', border: '#1e293b' }},
        'fiero': {{ bg: '#2563eb', color: '#ffffff', border: '#1d4ed8' }},
        'klintek': {{ bg: '#16a34a', color: '#ffffff', border: '#15803d' }}
      }};
      const bs = brandPalette[brandKey] || brandPalette['truper'];
      const badge = document.getElementById('modalBrandBadge');
      badge.textContent = brand;
      badge.style.backgroundColor = bs.bg;
      badge.style.color = bs.color;
      badge.style.border = `1px solid ${{bs.border}}`;

      document.getElementById('modalCategory').textContent = category;
      document.getElementById('modalImg').src = img;

      const codesWrap = document.getElementById('modalCodesWrap');
      codesWrap.innerHTML = codes.map(c => `<span class="code-chip">${{c}}</span>`).join(' ');

      const waMsg = encodeURIComponent(`Hola, deseo cotizar el producto: ${{title}} (${{codes[0] || ''}}) visto en el visor Truper.`);
      document.getElementById('modalWhatsAppBtn').href = `https://wa.me/529931412679?text=${{waMsg}}`;

      document.getElementById('productModal').style.display = 'flex';
    }}

    function closeModal(event) {{
      document.getElementById('productModal').style.display = 'none';
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeModal();
    }});
  </script>

</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] {OUTPUT_HTML} generado con éxito ({len(groups_data)} familias, {len(updated_products)} productos en tienda).")

if __name__ == "__main__":
    generate_preview()
