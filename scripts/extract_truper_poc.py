#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extract_truper_poc.py
Ferretería y Tlapalería El Águila - Extractor de Imágenes del Catálogo Truper 2026 (PoC)

Demuestra la viabilidad técnica y operativa de:
1. Extraer imágenes de productos y familias directamente del catálogo PDF oficial (catalogo_nacional_2026.pdf).
2. Asociar una misma imagen del producto a todos los códigos y claves agrupados bajo ella.
3. Convertir y optimizar los activos a formato WebP de alto rendimiento.
4. Actualizar automáticamente data/products.json vinculando las imágenes reales.
5. Generar un manifiesto de trazabilidad data/truper_poc_manifest.json.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = "/home/divadios/Descargas/catalogo_nacional_2026.pdf"
OUTPUT_IMG_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products", "truper")
PRODUCTS_JSON = os.path.join(PROJECT_ROOT, "data", "products.json")
MANIFEST_JSON = os.path.join(PROJECT_ROOT, "data", "truper_poc_manifest.json")
TMP_DIR = "/tmp/truper_poc_extract"

# Definición de Grupos de Productos, activos visuales en el PDF y códigos/claves asociados
# Cada entrada mapea un producto o familia visual a TODOS sus códigos en catálogo y tienda.
PRODUCT_GROUPS = [
    # -------------------------------------------------------------
    # 1. MARTILLOS (Página 283 del PDF / 280 del catálogo)
    # -------------------------------------------------------------
    {
        "id": "martillo-tubular-truper",
        "title": "Martillos tubulares pulidos Truper",
        "brand": "Truper",
        "page": 283,
        "type": "raw_image",
        "image_index": 5, # /tmp/test_hammer-005.png
        "output_filename": "martillo-tubular-truper.webp",
        "codes": ["MT-16", "MTR-16", "MTR-20", "16701", "16702", "16703"],
        "description": "Martillo tubular pulido cabeza uña curva y uña recta 16 y 20 oz Truper"
    },
    {
        "id": "martillo-tubular-pretul",
        "title": "Martillos tubulares Pretul",
        "brand": "Pretul",
        "page": 283,
        "type": "raw_image",
        "image_index": 0, # /tmp/test_hammer-000.png
        "output_filename": "martillo-tubular-pretul.webp",
        "codes": ["MT-16P", "MTR-16P", "MTR-20P", "20595", "20596", "20597"],
        "description": "Martillo tubular Pretul uña curva y recta 16 y 20 oz"
    },
    {
        "id": "martillo-cimbra-truper",
        "title": "Martillo tubular para cimbra Truper",
        "brand": "Truper",
        "page": 283,
        "type": "raw_image",
        "image_index": 21, # /tmp/test_hammer-021.png
        "output_filename": "martillo-cimbra-truper.webp",
        "codes": ["MCIM-16", "10754"],
        "description": "Martillo tubular para cimbra uña recta 16 oz con alojamiento imantado"
    },
    {
        "id": "martillo-tpr-truper",
        "title": "Martillo tubular mango TPR Truper",
        "brand": "Truper",
        "page": 283,
        "type": "raw_image",
        "image_index": 10, # /tmp/test_hammer-010.png
        "output_filename": "martillo-tpr-truper.webp",
        "codes": ["SJ-16", "16700"],
        "description": "Martillo tubular pulido uña curva 16 oz con mango TPR antivibración"
    },
    {
        "id": "martillo-tpr-pretul",
        "title": "Martillo tubular mango TPR Pretul",
        "brand": "Pretul",
        "page": 283,
        "type": "raw_image",
        "image_index": 2, # /tmp/test_hammer-002.png
        "output_filename": "martillo-tpr-pretul.webp",
        "codes": ["SJ-16P", "22270"],
        "description": "Martillo tubular pulido uña curva 16 oz Pretul"
    },
    {
        "id": "mini-martillo-pretul",
        "title": "Mini martillo Comfort Grip Pretul",
        "brand": "Pretul",
        "page": 283,
        "type": "raw_image",
        "image_index": 20,
        "output_filename": "mini-martillo-pretul.webp",
        "codes": ["MO-10E", "22291"],
        "description": "Mini martillo compacto Comfort Grip 10 oz Pretul"
    },
    {
        "id": "martillo-imantado-truper",
        "title": "Martillo tubular uña recta imantado Truper",
        "brand": "Truper",
        "page": 283,
        "type": "raw_image",
        "image_index": 16,
        "output_filename": "martillo-imantado-truper.webp",
        "codes": ["MTR-20X", "16661"],
        "description": "Martillo tubular pulido uña recta 20 oz con alojamiento imantado"
    },
    {
        "id": "martillo-fresado-truper",
        "title": "Martillo tubular uña recta cara fresada Truper",
        "brand": "Truper",
        "page": 283,
        "type": "raw_image",
        "image_index": 17,
        "output_filename": "martillo-fresado-truper.webp",
        "codes": ["MTR-20F", "16704"],
        "description": "Martillo tubular pulido uña recta 20 oz cara fresada antideslizamiento"
    },

    # -------------------------------------------------------------
    # 2. ESCUADRAS Y REGLAS (Página 167 del PDF / 165 del catálogo)
    # -------------------------------------------------------------
    {
        "id": "escuadras-esquineras-esm32",
        "title": "Juego de 2 escuadras magnéticas esquineras Truper",
        "brand": "Truper",
        "page": 167,
        "type": "raw_image",
        "image_index": 14, # p167_img-014.png
        "output_filename": "escuadras-esquineras-esm32.webp",
        "codes": ["ESM-32", "103031"],
        "description": "Juego de 2 escuadras magnéticas esquineras 3 pulgadas capacidad 11 kg"
    },
    {
        "id": "escuadras-magneticas-truper",
        "title": "Escuadras magnéticas para soldar Truper",
        "brand": "Truper",
        "page": 167,
        "type": "raw_image",
        "image_index": 4, # p167_img-004.png
        "output_filename": "escuadras-magneticas-truper.webp",
        "codes": ["ESM-3", "ESM-4", "ESM-5", "12119", "15407", "15408"],
        "description": "Escuadras magnéticas clásicas para soldador Truper (11 kg, 22 kg, 34 kg)"
    },
    {
        "id": "escuadras-magneticas-pretul",
        "title": "Escuadras magnéticas para soldar Pretul",
        "brand": "Pretul",
        "page": 167,
        "type": "raw_image",
        "image_index": 5, # p167_img-005.png
        "output_filename": "escuadras-magneticas-pretul.webp",
        "codes": ["ESM-3P", "ESM-4P", "ESM-5P", "28242", "28243", "28244"],
        "description": "Escuadras magnéticas para soldador Pretul (10 kg, 20 kg, 25 kg)"
    },
    {
        "id": "escuadras-magneticas-expert",
        "title": "Escuadras magnéticas para soldar Truper Expert",
        "brand": "Truper",
        "page": 167,
        "type": "raw_image",
        "image_index": 12, # p167_img-012.png
        "output_filename": "escuadras-magneticas-expert.webp",
        "codes": ["ESM-3X", "ESM-4X", "ESM-5X", "102860", "102861", "102862"],
        "description": "Escuadras magnéticas uso extra pesado Truper Expert (25 kg, 50 kg, 70 kg)"
    },
    {
        "id": "escuadra-falsa-plastico",
        "title": "Escuadra falsa mango plástico 8 pulgadas Truper",
        "brand": "Truper",
        "page": 167,
        "type": "raw_image",
        "image_index": 1, # p167_img-001.png
        "output_filename": "escuadra-falsa-plastico.webp",
        "codes": ["EFT-8", "MF-8", "14382"],
        "description": "Escuadra falsa de 8 pulgadas (20 cm) con mango de plástico ABS Truper"
    },
    {
        "id": "escuadra-falsa-aluminio",
        "title": "Escuadra falsa mango aluminio 9 pulgadas Truper",
        "brand": "Truper",
        "page": 167,
        "type": "raw_image",
        "image_index": 2, # p167_img-002.png
        "output_filename": "escuadra-falsa-aluminio.webp",
        "codes": ["EFT-9X", "MF-9", "14385"],
        "description": "Escuadra falsa de 9 pulgadas (23 cm) con mango de aluminio Truper Expert"
    },
    {
        "id": "regla-acero-30cm",
        "title": "Regla de acero inoxidable 30 cm Truper",
        "brand": "Truper",
        "page": 167,
        "type": "raw_image",
        "image_index": 19, # p167_img-019.png
        "output_filename": "regla-acero-30cm.webp",
        "codes": ["RGL-30", "RE-30", "14387"],
        "description": "Regla metálica de acero inoxidable graduada de 12 pulgadas / 30 cm Truper"
    },
    {
        "id": "regla-acero-bolsillo-15cm",
        "title": "Regla de acero inoxidable de bolsillo 15 cm Truper",
        "brand": "Truper",
        "page": 167,
        "type": "raw_image",
        "image_index": 10, # p167_img-010.png
        "output_filename": "regla-acero-bolsillo-15cm.webp",
        "codes": ["RGL-15B", "RE-15B", "101810"],
        "description": "Regla de bolsillo de acero inoxidable 6 pulgadas / 15 cm con clip Truper"
    },

    # -------------------------------------------------------------
    # 3. ARCOS PARA SEGUETA (Página 34 del PDF / 32 del catálogo)
    # -------------------------------------------------------------
    {
        "id": "arco-segueta-extra-pesado",
        "title": "Arco profesional extra pesado 1 kg Truper Expert",
        "brand": "Truper",
        "page": 34,
        "type": "raw_image",
        "image_index": 0, # p34_img-000.png
        "output_filename": "arco-segueta-extra-pesado.webp",
        "codes": ["ATX-12", "10232"],
        "description": "Arco profesional de alta tensión extra pesado 12 pulgadas Truper Expert"
    },
    {
        "id": "arco-segueta-tubular",
        "title": "Arco profesional tubular de acero Truper",
        "brand": "Truper",
        "page": 34,
        "type": "raw_image",
        "image_index": 1, # p34_img-001.png
        "output_filename": "arco-segueta-tubular.webp",
        "codes": ["ATT-12", "AT-12", "AT-12X", "10234"],
        "description": "Arco profesional tubular de acero 12 pulgadas para segueta Truper"
    },
    {
        "id": "arco-segueta-ajustable",
        "title": "Arco profesional ajustable niquelado Truper",
        "brand": "Truper",
        "page": 34,
        "type": "raw_image",
        "image_index": 4, # p34_img-004.png
        "output_filename": "arco-segueta-ajustable.webp",
        "codes": ["APT-12", "A-12", "A-12X", "10230"],
        "description": "Arco profesional ajustable de solera niquelada 12 pulgadas Truper"
    },
    {
        "id": "arco-segueta-solera-pretul",
        "title": "Arco de solera para segueta Pretul",
        "brand": "Pretul",
        "page": 34,
        "type": "raw_image",
        "image_index": 10, # p34_img-010.png
        "output_filename": "arco-segueta-solera-pretul.webp",
        "codes": ["APS-12", "20017"],
        "description": "Arco de solera para segueta 12 pulgadas Pretul"
    },
    {
        "id": "mini-arco-aluminio",
        "title": "Mini arco de aluminio para segueta Truper",
        "brand": "Truper",
        "page": 34,
        "type": "raw_image",
        "image_index": 3,
        "output_filename": "mini-arco-aluminio.webp",
        "codes": ["MAT-12", "10236"],
        "description": "Mini arco ergonómico de aluminio para segueta 12 pulgadas Truper"
    },
    {
        "id": "mini-arco-plastico-pretul",
        "title": "Mini arco de plástico para segueta Pretul",
        "brand": "Pretul",
        "page": 34,
        "type": "raw_image",
        "image_index": 6,
        "output_filename": "mini-arco-plastico-pretul.webp",
        "codes": ["MAT-12P", "20002"],
        "description": "Mini arco de plástico para segueta 12 pulgadas Pretul"
    },

    # -------------------------------------------------------------
    # 4. CINCELES Y BROCAS SDS (Página 71 del PDF / 69 del catálogo)
    # -------------------------------------------------------------
    {
        "id": "brocasierra-concreto-kit",
        "title": "Juego de brocasierras para concreto 9 piezas Truper",
        "brand": "Truper",
        "page": 71,
        "type": "raw_image",
        "image_index": 7, # p71_img-007.png
        "output_filename": "brocasierra-concreto-kit.webp",
        "codes": ["JBS-9C", "103577"],
        "description": "Juego de 9 piezas brocasierras para concreto SDS Plus y SDS Max con estuche"
    },
    {
        "id": "broca-sds-max-concreto",
        "title": "Brocas SDS Max para concreto Truper",
        "brand": "Truper",
        "page": 71,
        "type": "raw_image",
        "image_index": 15, # p71_img-015.png
        "output_filename": "broca-sds-max-concreto.webp",
        "codes": [
            "BSM-1/2X13", "BSM-5/8X13", "BSM-5/8X21", "BSM-5/8X36",
            "BSM-3/4X13", "BSM-3/4X21", "BSM-3/4X36", "BSM-7/8X13",
            "BSM-7/8X21", "BSM-1X13", "BSM-1X21", "BSM-1X36",
            "BSM-1-1/8X13", "BSM-1-1/8X21", "BSM-1-1/4X13", "BSM-1-1/4X21",
            "BSM-1-1/4X36", "BSM-1-3/8X21", "BSM-1-1/2X21"
        ],
        "description": "Broca SDS Max para concreto con doble flauta y punta de carburo Truper"
    },
    {
        "id": "cincel-sds-plus-punta",
        "title": "Cincel SDS Plus de punta Truper",
        "brand": "Truper",
        "page": 71,
        "type": "raw_image",
        "image_index": 29, # p71_img-029.png
        "output_filename": "cincel-sds-plus-punta.webp",
        "codes": ["SDS-P", "12095", "SDM-P", "101236", "HEX-P", "101230"],
        "description": "Cincel de punta para rotomartillos y demoledores SDS Plus y SDS Max"
    },
    {
        "id": "cincel-sds-plus-plano",
        "title": "Cincel SDS Plus plano Truper",
        "brand": "Truper",
        "page": 71,
        "type": "raw_image",
        "image_index": 30, # p71_img-030.png
        "output_filename": "cincel-sds-plus-plano.webp",
        "codes": ["SDS-C1", "SDS-C2", "SDS-C3", "SDS-C4", "12096", "12097", "13925", "13927", "SDM-C1", "101237"],
        "description": "Cincel plano delgado y grueso para demolición y desbaste SDS Plus y SDS Max"
    },

    # -------------------------------------------------------------
    # 5. BISAGRAS RECTANGULARES HERMEX (Página 566 del PDF / 563 del catálogo)
    # -------------------------------------------------------------
    {
        "id": "bisagras-latonadas-hermex",
        "title": "Bisagras de acero rectangulares acabado latonado Hermex",
        "brand": "Hermex",
        "page": 566,
        "type": "raw_image",
        "image_index": 1, # p566_img-001.png
        "output_filename": "bisagras-latonadas-hermex.webp",
        "codes": [
            "BR-101", "BR-151", "BR-201", "BR-251", "BR-301", "BR-351", "BR-401",
            "43192", "43193", "43194", "43195", "43196", "43197", "43198"
        ],
        "description": "Bisagras de acero rectangulares cabeza media bola acabado latonado Hermex"
    },
    {
        "id": "bisagras-laton-antiguo-hermex",
        "title": "Bisagras de acero rectangulares acabado latón antiguo Hermex",
        "brand": "Hermex",
        "page": 566,
        "type": "raw_image",
        "image_index": 2, # p566_img-002.png
        "output_filename": "bisagras-laton-antiguo-hermex.webp",
        "codes": [
            "BR-102", "BR-152", "BR-202", "BR-252", "BR-302", "BR-352", "BR-402",
            "46909", "46910", "46911", "46912", "46913", "46914", "46915"
        ],
        "description": "Bisagras de acero rectangulares cabeza media bola acabado latón antiguo Hermex"
    },
    {
        "id": "bisagras-acero-natural-hermex",
        "title": "Bisagras de acero rectangulares acabado natural Hermex",
        "brand": "Hermex",
        "page": 566,
        "type": "raw_image",
        "image_index": 3, # p566_img-003.png
        "output_filename": "bisagras-acero-natural-hermex.webp",
        "codes": [
            "BR-100", "BR-150", "BR-200", "BR-250", "BR-300", "BR-350", "BR-400",
            "43185", "43186", "43187", "43188", "43189", "43190", "43191"
        ],
        "description": "Bisagras de acero rectangulares cabeza media bola acabado natural pulido Hermex"
    },

    # -------------------------------------------------------------
    # 6. BROCASIERRAS BIMETÁLICAS (Página 72 del PDF / 70 del catálogo)
    # -------------------------------------------------------------
    {
        "id": "brocasierra-bimetalica-truper",
        "title": "Brocasierras bimetálicas Truper Expert",
        "brand": "Truper",
        "page": 72,
        "type": "crop",
        "crop_box": (240, 360, 480, 920),
        "output_filename": "brocasierra-bimetalica-truper.webp",
        "codes": [
            "COBI-9/16", "COBI-5/8", "COBI-3/4", "COBI-7/8", "COBI-1", "COBI-1-1/16",
            "COBI-1-1/8", "COBI-1-3/16", "COBI-1-1/4", "COBI-1-3/8", "COBI-1-1/2",
            "COBI-1-9/16", "COBI-1-3/4", "COBI-2", "COBI-2-1/8", "COBI-2-1/4",
            "COBI-2-3/8", "COBI-2-1/2", "COBI-2-3/4", "COBI-3", "COBI-3-1/4",
            "COBI-3-1/2", "COBI-4", "COBI-4-1/4", "COBI-4-1/2", "COBI-5", "COBI-5-1/2", "COBI-6",
            "BS-1/2", "BS-1", "BS-1-1/2", "BS-1-1/4", "BS-1-1/8", "BS-1-3/4", "BS-2", "BS-2-1/2"
        ],
        "description": "Brocasierra bimetálica Truper Expert para cortes en metal y madera"
    }
]


def ensure_temp_dir():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)


def extract_page_raw_images(page_num):
    """Extrae las imágenes directas de la página mediante pdfimages si no existen aún."""
    prefix = os.path.join(TMP_DIR, f"p{page_num}_raw")
    if not os.path.exists(f"{prefix}-000.png"):
        print(f"[*] Extrayendo imágenes crudas de página {page_num} con pdfimages...")
        cmd = ["pdfimages", "-png", "-f", str(page_num), "-l", str(page_num), PDF_PATH, prefix]
        subprocess.run(cmd, check=True)
    return prefix


def render_page_image(page_num):
    """Renderiza la página completa a 150 DPI para cortes morfológicos/boxes."""
    prefix = os.path.join(TMP_DIR, f"page_{page_num}")
    rendered_file = f"{prefix}-{page_num:03d}.png"
    alt_file = f"{prefix}-{page_num}.png"
    if not (os.path.exists(rendered_file) or os.path.exists(alt_file)):
        print(f"[*] Renderizando página {page_num} a 150 DPI con pdftoppm...")
        cmd = ["pdftoppm", "-png", "-r", "150", "-f", str(page_num), "-l", str(page_num), PDF_PATH, prefix]
        subprocess.run(cmd, check=True)
    return rendered_file if os.path.exists(rendered_file) else alt_file


def pad_to_canvas(im, target_size=500, padding_pct=0.08):
    """
    Normaliza y centra la imagen en un lienzo cuadrado blanco de 500x500 px.
    Evita que herramientas largas (cinceles, brocas, reglas) se deformen o se corten
    al ser desplegadas en tarjetas de comercio electrónico o vistas previas de WhatsApp.
    """
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        base_im = bg
    else:
        base_im = im.convert("RGB")

    avail = target_size * (1 - 2 * padding_pct)
    scale = min(avail / base_im.width, avail / base_im.height)
    new_w = max(1, int(base_im.width * scale))
    new_h = max(1, int(base_im.height * scale))
    resized = base_im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_size, target_size), (255, 255, 255))
    offset = ((target_size - new_w) // 2, (target_size - new_h) // 2)
    canvas.paste(resized, offset)
    return canvas


def process_and_save_image(group):
    """Procesa y guarda la imagen optimizada WebP para el grupo con lienzo cuadrado estándar."""
    out_path = os.path.join(OUTPUT_IMG_DIR, group["output_filename"])
    page_num = group["page"]

    if group["type"] == "raw_image":
        prefix = extract_page_raw_images(page_num)
        idx = group["image_index"]
        raw_path = f"{prefix}-{idx:03d}.png"
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Imagen cruda {raw_path} no encontrada.")
        with Image.open(raw_path) as im:
            canvas = pad_to_canvas(im, target_size=500, padding_pct=0.08)
            canvas.save(out_path, "WEBP", quality=90, method=6)

    elif group["type"] == "crop":
        page_img_path = render_page_image(page_num)
        y1, y2, x1, x2 = group["crop_box"]
        with Image.open(page_img_path) as im:
            crop_im = im.crop((x1, y1, x2, y2))
            canvas = pad_to_canvas(crop_im, target_size=500, padding_pct=0.08)
            canvas.save(out_path, "WEBP", quality=90, method=6)

    size_kb = os.path.getsize(out_path) / 1024
    with Image.open(out_path) as im:
        w, h = im.size
    print(f"  [+] Guardado: {group['output_filename']} ({w}x{h} px, {size_kb:.1f} KB)")
    return {
        "path": f"assets/images/products/truper/{group['output_filename']}",
        "width": w,
        "height": h,
        "size_kb": round(size_kb, 2)
    }


def main():
    print("=" * 70)
    print("EXTRACTOR DE PRODUCTOS TRUPER - PRUEBA DE CONCEPTO (PoC)")
    print("=" * 70)

    if not os.path.exists(PDF_PATH):
        print(f"[!] Error: Catálogo no encontrado en {PDF_PATH}", file=sys.stderr)
        sys.exit(1)

    ensure_temp_dir()

    # 1. Extraer y generar todas las imágenes WebP
    print("\n[Fase 1] Extrayendo y optimizando imágenes desde el PDF...")
    group_assets = {}
    code_to_asset = {}

    for g in PRODUCT_GROUPS:
        asset_info = process_and_save_image(g)
        group_assets[g["id"]] = asset_info
        for code in g["codes"]:
            clean_code = code.strip().upper()
            code_to_asset[clean_code] = {
                "group_id": g["id"],
                "group_title": g["title"],
                "brand": g["brand"],
                "image_rel": asset_info["path"]
            }

    print(f"\n[+] Total de grupos de producto procesados: {len(PRODUCT_GROUPS)}")
    print(f"[+] Total de códigos/claves asignados a imágenes: {len(code_to_asset)}")

    # 2. Cargar data/products.json y actualizar los artículos correspondientes
    print("\n[Fase 2] Actualizando data/products.json con imágenes de alta definición...")
    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        products = json.load(f)

    updated_count = 0
    manifest_records = []

    for p in products:
        sku = str(p.get("sku", "")).strip().upper()
        mfg = str(p.get("manufacturer_code", "")).strip().upper()

        match = None
        matched_by = None
        if sku in code_to_asset:
            match = code_to_asset[sku]
            matched_by = f"SKU:{sku}"
        elif mfg in code_to_asset:
            match = code_to_asset[mfg]
            matched_by = f"MFG:{mfg}"

        if match:
            old_image = p.get("image", "")
            new_image = match["image_rel"]
            
            p["image"] = new_image
            p["image_url"] = new_image
            if p.get("brand") == "Homologado" and match.get("brand"):
                p["brand"] = match["brand"]
                p["brands"] = {"name": match["brand"]}

            updated_count += 1
            manifest_records.append({
                "id": p.get("id"),
                "sku": p.get("sku"),
                "name": p.get("name"),
                "brand": p.get("brand"),
                "matched_by": matched_by,
                "group": match["group_title"],
                "old_image": old_image,
                "new_image": new_image
            })

    print(f"[+] Artículos en la tienda actualizados con su foto real: {updated_count}")

    # Guardar data/products.json
    with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"[+] {PRODUCTS_JSON} guardado exitosamente con {len(products)} artículos intactos.")

    # 3. Guardar data/truper_poc_manifest.json
    manifest_data = {
        "total_catalog_groups": len(PRODUCT_GROUPS),
        "total_sku_mappings": len(code_to_asset),
        "total_store_products_updated": updated_count,
        "groups": PRODUCT_GROUPS,
        "updated_products": manifest_records
    }
    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Manifiesto guardado en: {MANIFEST_JSON}")

    print("\n" + "=" * 70)
    print(f"¡ÉXITO! {updated_count} productos de la ferretería ahora cuentan con foto del catálogo.")
    print("=" * 70)


def scan_page(page_num, pdf_path=PDF_PATH):
    """
    Escaneo e inspección automática de cualquier página del catálogo (1 a 645):
    - Extrae metadatos de imágenes incrustadas (resolución, dimensiones, tipo).
    - Extrae códigos de 5 dígitos y claves del texto estructurado.
    - Cruza los códigos con data/products.json de la ferretería.
    """
    print(f"\n[*] Escaneando automáticamente página {page_num} del catálogo...")
    if not os.path.exists(pdf_path):
        print(f"[!] Error: Catálogo no encontrado en {pdf_path}", file=sys.stderr)
        return None

    # 1. Imágenes incrustadas
    img_cmd = ["pdfimages", "-list", "-f", str(page_num), "-l", str(page_num), pdf_path]
    img_res = subprocess.run(img_cmd, capture_output=True, text=True, check=True)
    img_lines = [l for l in img_res.stdout.splitlines() if l.strip() and not l.startswith("page") and not l.startswith("---")]

    # 2. Texto, códigos numéricos y claves de modelo
    txt_cmd = ["pdftotext", "-f", str(page_num), "-l", str(page_num), "-layout", pdf_path, "-"]
    txt_res = subprocess.run(txt_cmd, capture_output=True, text=True, check=True)

    codes_found = sorted(list(set(re.findall(r"\b\d{5}\b", txt_res.stdout))))
    claves_found = sorted(list(set(re.findall(r"\b[A-Z0-9]{1,6}-[\w/.]+\b", txt_res.stdout))))
    all_keys = set(c.upper() for c in (codes_found + claves_found))

    # 3. Cruce con tienda
    store_matches = []
    if os.path.exists(PRODUCTS_JSON):
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            prods = json.load(f)
        for p in prods:
            s = str(p.get("sku", "")).strip().upper()
            m = str(p.get("manufacturer_code", "")).strip().upper()
            if s in all_keys or m in all_keys:
                store_matches.append(p)

    print(f"  [+] Imágenes de producto identificadas en página {page_num}: {len(img_lines)}")
    print(f"  [+] Códigos numéricos de 5 dígitos detectados: {len(codes_found)}")
    print(f"  [+] Claves de modelo detectadas: {len(claves_found)} -> {claves_found[:8]}...")
    print(f"  [+] Artículos existentes en ferretería_el_aguila vinculables: {len(store_matches)}")
    for sm in store_matches[:6]:
        print(f"      - [{sm.get('sku')}] {sm.get('name')} (${sm.get('base_price')})")

    return {
        "page": page_num,
        "images_count": len(img_lines),
        "codes_count": len(codes_found),
        "codes": codes_found,
        "claves_count": len(claves_found),
        "claves": claves_found,
        "store_matches_count": len(store_matches),
        "store_matches": store_matches
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extractor de productos del catálogo Truper 2026")
    parser.add_argument("--scan-page", type=int, help="Escanea automáticamente una página específica (1-645) del catálogo")
    args = parser.parse_args()

    if args.scan_page:
        scan_page(args.scan_page)
    else:
        main()
