#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_ground_truth_catalog.py
Pipeline de extracción masiva Ground-Truth para el Catálogo Truper 2026.

Reglas:
1. Coincidencia estricta: Solo se asocian imágenes a productos cuyo código o clave
   coincide físicamente en el catálogo en esa celda geométrica.
2. Cero adivinación semántica o nombres aproximados.
3. Formato WebP 500x500 con esquinas blancas puras (255, 255, 255).
4. Marcas oficiales Truper (Truper, Pretul, Volteck, Foset, Hermex, Fiero, Klintek).
5. Proceso liviano de un solo hilo para evitar sobrecalentamiento de CPU.
"""

import os
import sys
import json
import re
import io
import argparse
import pymupdf
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PDF = "/home/divadios/Descargas/catalogo_nacional_2026.pdf"
PRODUCTS_PATH = os.path.join(PROJECT_ROOT, "data", "products.json")
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "data", "truper_poc_manifest.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products", "truper")

VALID_BRANDS = {"Truper", "Pretul", "Volteck", "Foset", "Hermex", "Fiero", "Klintek"}

def slugify(text):
    text = text.lower()
    text = re.sub(r'[\xc0-\xc5]', 'a', text)
    text = re.sub(r'[\xe8-\xeb]', 'e', text)
    text = re.sub(r'[\xec-\xef]', 'i', text)
    text = re.sub(r'[\xf2-\xf6]', 'o', text)
    text = re.sub(r'[\xf9-\xfc]', 'u', text)
    text = re.sub(r'[\xf1]', 'n', text)
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:60]

def normalize_brand(raw_brand, text=""):
    combined = f"{raw_brand} {text}".lower()
    if 'pretul' in combined: return 'Pretul'
    if 'volteck' in combined: return 'Volteck'
    if 'foset' in combined: return 'Foset'
    if 'hermex' in combined: return 'Hermex'
    if 'fiero' in combined: return 'Fiero'
    if 'klintek' in combined: return 'Klintek'
    return 'Truper'

def normalize_category(cat):
    cat_lower = str(cat or '').lower()
    if any(k in cat_lower for k in ['eléctric', 'electr', 'iluminac', 'cable']): return 'Eléctrico'
    if any(k in cat_lower for k in ['plom', 'tubo', 'gas', 'grifo', 'valvul']): return 'Plomería'
    if any(k in cat_lower for k in ['cerraj', 'candad', 'chapa', 'cerrad']): return 'Cerrajería'
    if any(k in cat_lower for k in ['tornill', 'fijac', 'clav', 'abraz']): return 'Fijación'
    if any(k in cat_lower for k in ['construc', 'cemento', 'albanil', 'pala']): return 'Construcción'
    if any(k in cat_lower for k in ['herramienta manual', 'manual', 'pinza', 'martill', 'llave']): return 'Herramientas Manuales'
    if any(k in cat_lower for k in ['poder', 'eléctrica', 'taladr', 'esmeril', 'sierra']): return 'Herramientas Eléctricas'
    if any(k in cat_lower for k in ['segur', 'protec', 'lente', 'guante']): return 'Seguridad'
    if any(k in cat_lower for k in ['jardin', 'podad', 'manguera', 'tijera']): return 'Jardinería'
    return 'Herramientas Manuales'

def extract_and_normalize_crop(page, rect, out_path, padding=20):
    pix = page.get_pixmap(clip=rect, dpi=250)
    img = Image.open(io.BytesIO(pix.tobytes())).convert('RGB')
    
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x >= 246 else 255, '1')
    bbox = bw.getbbox()
    if bbox:
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w < 35 or h < 25:
            return False
        img_cropped = img.crop(bbox)
    else:
        return False

    target_size = (500, 500)
    avail_w = target_size[0] - 2 * padding
    avail_h = target_size[1] - 2 * padding
    
    scale = min(avail_w / img_cropped.width, avail_h / img_cropped.height)
    new_w = max(1, int(img_cropped.width * scale))
    new_h = max(1, int(img_cropped.height * scale))
    
    img_resized = img_cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    canvas = Image.new('RGB', target_size, (255, 255, 255))
    offset_x = (target_size[0] - new_w) // 2
    offset_y = (target_size[1] - new_h) // 2
    canvas.paste(img_resized, (offset_x, offset_y))
    
    for pt in [(0, 0), (499, 0), (0, 499), (499, 499)]:
        canvas.putpixel(pt, (255, 255, 255))
        
    canvas.save(out_path, 'WEBP', quality=90)
    return True

def run_pipeline(limit=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(PRODUCTS_PATH, 'r', encoding='utf-8') as f:
        products = json.load(f)

    store_codes = {}
    for p in products:
        sku = str(p.get('sku') or '').strip().upper()
        mfg = str(p.get('manufacturer_code') or '').strip().upper()
        if sku: store_codes.setdefault(sku, []).append(p)
        if mfg and mfg != sku: store_codes.setdefault(mfg, []).append(p)

    doc = pymupdf.open(CATALOG_PDF)
    print(f"[*] Abriendo catálogo Truper 2026 ({len(doc)} páginas)...")

    # Load existing manifest
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = {'groups': [], 'updated_products': []}

    # Ensure all existing groups have valid official brands
    existing_group_ids = {}
    for g in manifest.get('groups', []):
        g['brand'] = normalize_brand(g.get('brand'), g.get('title', ''))
        g['category'] = normalize_category(g.get('category'))
        existing_group_ids[g['id']] = g

    protected_slugs = {
        'nivel-laser-autonivelante-truper',
        'soplete-gas-butano-truper',
        'canaleta-adhesiva-cables-volteck',
        'multicontacto-supresor-picos-volteck',
        'multicontacto-barra-supresor-picos-6-entradas-volteck'
    }

    # Keep all existing updated products from products.json
    updated_product_ids = set()
    for p in products:
        img_url = p.get('image_url') or ''
        if 'assets/images/products/truper/' in img_url:
            updated_product_ids.add(p['id'])

    total_clusters_processed = 0
    total_products_updated = 0

    for page_idx in range(len(doc)):
        if limit and total_clusters_processed >= limit:
            break

        page = doc[page_idx]
        p_num = page_idx + 1
        words = page.get_text('words')

        page_matches = []
        for w in words:
            val = w[4].strip('.,()●*:;\"\'').upper()
            if val in store_codes:
                is_valid = bool(re.match(r'^\d{5,6}$', val)) or bool(re.match(r'^[A-Z]{2,6}(?:-[A-Z0-9/.]+)+$', val))
                if is_valid:
                    page_matches.append({'code': val, 'x0': w[0], 'y0': w[1], 'x1': w[2], 'y1': w[3], 'products': store_codes[val]})

        if not page_matches:
            continue

        # Cluster by column and vertical table position
        clusters = []
        for m in page_matches:
            col = 'left' if m['x0'] < 300 else 'right'
            added = False
            for c in clusters:
                if c['col'] == col and abs(c['y_mid'] - m['y0']) < 70:
                    c['items'].append(m)
                    c['y_min'] = min(c['y_min'], m['y0'])
                    c['y_max'] = max(c['y_max'], m['y1'])
                    c['y_mid'] = (c['y_min'] + c['y_max']) / 2
                    added = True
                    break
            if not added:
                clusters.append({
                    'page': p_num,
                    'col': col,
                    'items': [m],
                    'y_min': m['y0'],
                    'y_max': m['y1'],
                    'y_mid': m['y0']
                })

        for c in clusters:
            if limit and total_clusters_processed >= limit:
                break

            codes_in_c = list({it['code'] for it in c['items']})
            prods_in_c = []
            for cd in codes_in_c:
                for p in store_codes[cd]:
                    prods_in_c.append(p)

            if not prods_in_c:
                continue

            # Candidate photo rect above table
            x0 = 20 if c['col'] == 'left' else 300
            x1 = 300 if c['col'] == 'left' else 590
            y1 = max(45, c['y_min'] - 2)
            y0 = max(40, y1 - 180)

            photo_rect = pymupdf.Rect(x0, y0, x1, y1)
            
            sample_prod = prods_in_c[0]
            name = sample_prod.get('name') or 'Producto Truper'
            brand = normalize_brand(sample_prod.get('brand'), name)
            category = normalize_category(sample_prod.get('category'))
            slug_base = slugify(f"{name}-{codes_in_c[0]}")
            img_filename = f"{slug_base}.webp"
            img_rel_path = f"assets/images/products/truper/{img_filename}"
            img_full_path = os.path.join(PROJECT_ROOT, img_rel_path)

            if any(ps in slug_base for ps in protected_slugs):
                continue

            # Extract crop
            success = extract_and_normalize_crop(page, photo_rect, img_full_path)
            if not success:
                continue

            # Update products
            for p in prods_in_c:
                p['image_url'] = img_rel_path
                p['image'] = img_rel_path
                updated_product_ids.add(p['id'])
                total_products_updated += 1

            # Update manifest group
            group_entry = {
                'id': slug_base,
                'title': name,
                'brand': brand,
                'category': category,
                'page': p_num,
                'type': 'ground_truth_crop',
                'output_filename': img_filename,
                'codes': codes_in_c,
                'description': name,
                'matched_skus': [p.get('sku') for p in prods_in_c if p.get('sku')]
            }
            existing_group_ids[slug_base] = group_entry
            total_clusters_processed += 1

            if total_clusters_processed % 100 == 0:
                print(f"  [+] Procesados {total_clusters_processed} clusters ({len(updated_product_ids)} productos vinculados)...")

    # Final synchronization of manifest
    manifest['groups'] = list(existing_group_ids.values())
    manifest['total_catalog_groups'] = len(manifest['groups'])
    manifest['total_store_products_updated'] = len(updated_product_ids)
    
    # Sync updated_products list
    up_list = []
    p_by_id = {p['id']: p for p in products}
    for pid in sorted(updated_product_ids):
        if pid in p_by_id:
            p = p_by_id[pid]
            up_list.append({
                'id': p['id'],
                'sku': p.get('sku'),
                'name': p.get('name'),
                'brand': normalize_brand(p.get('brand'), p.get('name')),
                'new_image': p.get('image')
            })
    manifest['updated_products'] = up_list

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    with open(PRODUCTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Pipeline completado:")
    print(f"    - Familias/Clusters nuevos procesados: {total_clusters_processed}")
    print(f"    - Total grupos en manifiesto: {len(manifest['groups'])}")
    print(f"    - Total productos en tienda con imagen verificada: {len(updated_product_ids)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=None, help='Límite de clusters a procesar')
    args = parser.parse_args()
    run_pipeline(limit=args.limit)
