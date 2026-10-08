#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extract_batch2.py
Ferretería y Tlapalería El Águila - Extractor Lote 2 Catálogo Truper 2026
Extrae 30 nuevas familias visuales de alta demanda (carretillas, palas, flexómetros,
pinzas, desarmadores, pericos, stilson, esmeriladoras, rotomartillos, niveles,
discos de corte, lentes, extensiones, etc.) y actualiza data/products.json y el manifiesto.
"""

import json
import os
import subprocess
import sys
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = "/home/divadios/Descargas/catalogo_nacional_2026.pdf"
OUTPUT_IMG_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products", "truper")
PRODUCTS_JSON = os.path.join(PROJECT_ROOT, "data", "products.json")
MANIFEST_JSON = os.path.join(PROJECT_ROOT, "data", "truper_poc_manifest.json")
TMP_DIR = "/tmp/truper_batch2_extract"

NEW_GROUPS = [
    # 1. Carretilla Truper bastidor tubular
    {
        "id": "carretilla-bastidor-truper",
        "title": "Carretillas 5.5 y 6 ft³ bastidor tubular Truper",
        "brand": "Truper",
        "page": 85,
        "raw_index": 6,
        "output_filename": "carretilla-bastidor-truper.webp",
        "codes": ["CAT-50", "CAT-60", "CAP-50", "11776", "11777", "11778", "20550"],
        "description": "Carretilla bastidor tubular con llanta neumática reforzada Truper"
    },
    # 2. Carretilla Pretul bastidor tubular
    {
        "id": "carretilla-pretul",
        "title": "Carretillas 5 ft³ Pretul",
        "brand": "Pretul",
        "page": 85,
        "raw_index": 4,
        "output_filename": "carretilla-pretul.webp",
        "codes": ["CAP-50P", "CAP-40P", "20551", "20552"],
        "description": "Carretilla uso ligero 5 ft³ con llanta neumática Pretul"
    },
    # 3. Cuchara para albañil tipo Filadelfia Truper
    {
        "id": "cuchara-filadelfia-truper",
        "title": "Cuchara para albañil tipo Filadelfia Truper",
        "brand": "Truper",
        "page": 119,
        "raw_index": 0,
        "output_filename": "cuchara-filadelfia-truper.webp",
        "codes": ["CT-8", "CT-9", "CT-10", "CT-11", "10892", "10893", "10894", "10895"],
        "description": "Cuchara de acero al carbono forjada en una sola pieza tipo Filadelfia Truper"
    },
    # 4. Cuchara para albañil tipo Guadalajara Truper
    {
        "id": "cuchara-guadalajara-truper",
        "title": "Cuchara para albañil tipo Guadalajara Truper",
        "brand": "Truper",
        "page": 119,
        "raw_index": 3,
        "output_filename": "cuchara-guadalajara-truper.webp",
        "codes": ["CG-8", "CG-9", "CG-10", "10888", "10889", "10890"],
        "description": "Cuchara de acero forjada tipo Guadalajara para mezcla de cemento Truper"
    },
    # 5. Flexómetro Gripper contra impacto Truper
    {
        "id": "flexometro-gripper-truper",
        "title": "Flexómetros Gripper contra impacto Truper",
        "brand": "Truper",
        "page": 174,
        "raw_index": 16,
        "output_filename": "flexometro-gripper-truper.webp",
        "codes": ["FH-3M", "FH-5M", "FH-55M", "FH-8M", "14577", "14578", "14579", "14580"],
        "description": "Flexómetro de cinta extra ancha con cubierta de goma contra impactos Truper Gripper"
    },
    # 6. Flexómetro amarillo tradicional Pretul
    {
        "id": "flexometro-pretul",
        "title": "Flexómetros tradicionales amarillos Pretul",
        "brand": "Pretul",
        "page": 174,
        "raw_index": 24,
        "output_filename": "flexometro-pretul.webp",
        "codes": ["PRO-3MEB", "PRO-5MEB", "PRO-8MEB", "21601", "21602", "21603"],
        "description": "Flexómetro de cinta métrica graduada caja de plástico de alto impacto Pretul"
    },
    # 7. Juego de desarmadores Comfort Grip Truper
    {
        "id": "desarmadores-comfortgrip-truper",
        "title": "Juegos de desarmadores Comfort Grip Truper",
        "brand": "Truper",
        "page": 196,
        "raw_index": 140,
        "output_filename": "desarmadores-comfortgrip-truper.webp",
        "codes": ["DT-6", "DT-8", "DT-10", "14161", "14162", "14163"],
        "description": "Juego de desarmadores punta plana y Phillips de acero al cromo vanadio Comfort Grip Truper"
    },
    # 8. Desarmador barra redonda plano Cabinet Truper
    {
        "id": "desarmador-plano-truper",
        "title": "Desarmadores barra redonda plano Cabinet Truper",
        "brand": "Truper",
        "page": 196,
        "raw_index": 2,
        "output_filename": "desarmador-plano-truper.webp",
        "codes": ["DP-3/16X4", "DP-1/4X4", "DP-1/4X6", "14010", "14011", "14012"],
        "description": "Desarmador barra redonda con punta plana gabinete imantada Truper"
    },
    # 9. Desarmador punta de cruz Phillips Truper
    {
        "id": "desarmador-cruz-truper",
        "title": "Desarmadores punta de cruz Phillips Truper",
        "brand": "Truper",
        "page": 196,
        "raw_index": 3,
        "output_filename": "desarmador-cruz-truper.webp",
        "codes": ["DR-1/4X4", "DR-3/16X4", "DR-5/16X6", "14030", "14031", "14032"],
        "description": "Desarmador barra redonda con punta Phillips de cruz imantada Truper"
    },
    # 10. Llave ajustable perico cromado Truper
    {
        "id": "llave-ajustable-perico-truper",
        "title": "Llaves ajustables cromadas (Pericos) Truper",
        "brand": "Truper",
        "page": 213,
        "raw_index": 8,
        "output_filename": "llave-ajustable-perico-truper.webp",
        "codes": ["PET-6", "PET-8", "PET-10", "PET-12", "PET-15", "15509", "15510", "15511", "15512"],
        "description": "Llave ajustable cromada forjada en acero al carbono con graduación láser Truper"
    },
    # 11. Llave para tubo Stilson Truper
    {
        "id": "llave-tubo-stilson-truper",
        "title": "Llaves para tubo Stilson uso pesado Truper",
        "brand": "Truper",
        "page": 213,
        "raw_index": 14,
        "output_filename": "llave-tubo-stilson-truper.webp",
        "codes": ["STI-10", "STI-12", "STI-14", "STI-18", "STI-24", "15836", "15837", "15838", "15839"],
        "description": "Llave para plomería tipo Stilson con cuerpo de hierro maleable y mordazas templadas Truper"
    },
    # 12. Pinza de chofer mango vinil Truper
    {
        "id": "pinza-chofer-truper",
        "title": "Pinzas de chofer mango de vinil Truper",
        "brand": "Truper",
        "page": 302,
        "raw_index": 6,
        "output_filename": "pinza-chofer-truper.webp",
        "codes": ["T201-8", "T201-10", "T201-6", "17320", "17321", "17322"],
        "description": "Pinza de chofer forjada en acero al carbono con dos posiciones de ajuste y mango de vinil Truper"
    },
    # 13. Pinza de electricista alta palanca Truper
    {
        "id": "pinza-electricista-truper",
        "title": "Pinzas de electricista alta palanca Truper",
        "brand": "Truper",
        "page": 302,
        "raw_index": 7,
        "output_filename": "pinza-electricista-truper.webp",
        "codes": ["T200-8X", "T200-9X", "17330", "17331"],
        "description": "Pinza de electricista profesional alta palanca con mordazas estriadas y corte templado Truper"
    },
    # 14. Pinza de punta y corte Truper
    {
        "id": "pinza-punta-corte-truper",
        "title": "Pinzas de punta y corte largo Truper",
        "brand": "Truper",
        "page": 302,
        "raw_index": 10,
        "output_filename": "pinza-punta-corte-truper.webp",
        "codes": ["T203-6", "T203-8", "17334", "17335"],
        "description": "Pinza de punta y corte con mordazas largas estriadas para precisión en espacios reducidos Truper"
    },
    # 15. Pinza de presión mordaza curva Truper
    {
        "id": "pinza-presion-curva-truper",
        "title": "Pinzas de presión mordaza curva 10\" Truper",
        "brand": "Truper",
        "page": 307,
        "raw_index": 4,
        "output_filename": "pinza-presion-curva-truper.webp",
        "codes": ["PPT-10C", "PPT-7C", "17424", "17425"],
        "description": "Pinza de presión con mordaza curva y cortador de alambre forjada en acero al cromo vanadio Truper"
    },
    # 16. Pinza de presión mordaza recta Truper
    {
        "id": "pinza-presion-recta-truper",
        "title": "Pinzas de presión mordaza recta 10\" Truper",
        "brand": "Truper",
        "page": 307,
        "raw_index": 8,
        "output_filename": "pinza-presion-recta-truper.webp",
        "codes": ["PPT-10R", "PPT-7R", "17426", "17427"],
        "description": "Pinza de presión con mordaza recta para superficies planas y láminas Truper"
    },
    # 17. Pinza de extensión mecánica Truper
    {
        "id": "pinza-extension-truper",
        "title": "Pinzas de extensión mecánica ranurada Truper",
        "brand": "Truper",
        "page": 302,
        "raw_index": 8,
        "output_filename": "pinza-extension-truper.webp",
        "codes": ["PEX-10", "PEX-12", "17342", "17343"],
        "description": "Pinza de extensión con ranuras de ajuste múltiple para plomería y mecánica Truper"
    },
    # 18. Lentes de seguridad transparentes Truper
    {
        "id": "lentes-seguridad-truper",
        "title": "Lentes de seguridad transparentes ultraligeros Truper",
        "brand": "Truper",
        "page": 331,
        "raw_index": 17,
        "output_filename": "lentes-seguridad-truper.webp",
        "codes": ["LEN-ST", "LEN-SN", "LEN-SK", "14210", "14211", "14212"],
        "description": "Lentes de seguridad con mica de policarbonato 100% antirrayadura y protección UV Truper"
    },
    # 19. Lentes de seguridad económicos Pretul
    {
        "id": "lentes-seguridad-pretul",
        "title": "Lentes de seguridad económicos Pretul",
        "brand": "Pretul",
        "page": 331,
        "raw_index": 12,
        "output_filename": "lentes-seguridad-pretul.webp",
        "codes": ["LEN-P", "21980"],
        "description": "Lentes de seguridad transparentes con protección lateral contra impactos ligeros Pretul"
    },
    # 20. Extensión eléctrica uso rudo naranja Volteck
    {
        "id": "extension-electrica-naranja-volteck",
        "title": "Extensiones eléctricas de uso rudo naranja Volteck",
        "brand": "Volteck",
        "page": 406,
        "raw_index": 11,
        "output_filename": "extension-electrica-naranja-volteck.webp",
        "codes": ["ED-5", "ED-10", "ED-15", "ED-20", "48020", "48021", "48022", "48023"],
        "description": "Extensión eléctrica de uso rudo calibre 16 AWG aterrizada 3 conductores naranja Volteck"
    },
    # 21. Extensión eléctrica doméstica blanca Volteck
    {
        "id": "extension-electrica-blanca-volteck",
        "title": "Extensiones domésticas aterrizadas blancas Volteck",
        "brand": "Volteck",
        "page": 406,
        "raw_index": 14,
        "output_filename": "extension-electrica-blanca-volteck.webp",
        "codes": ["EB-3", "EB-5", "EB-8", "48030", "48031", "48032"],
        "description": "Extensión eléctrica doméstica aterrizada color blanco de 3 contactos polarizados Volteck"
    },
    # 22. Nivel de aluminio magnético Truper
    {
        "id": "nivel-aluminio-magnetico-truper",
        "title": "Niveles de aluminio magnéticos de 3 gotas Truper",
        "brand": "Truper",
        "page": 485,
        "raw_index": 6,
        "output_filename": "nivel-aluminio-magnetico-truper.webp",
        "codes": ["NL-18", "NL-24", "NL-36", "12242", "12243", "12244"],
        "description": "Nivel de viga de aluminio reforzado con banda magnética y 3 gotas de acrílico Truper"
    },
    # 23. Nivel tipo torpedo compacto Truper
    {
        "id": "nivel-torpedo-truper",
        "title": "Nivel tipo torpedo compacto magnético 9\" Truper",
        "brand": "Truper",
        "page": 485,
        "raw_index": 4,
        "output_filename": "nivel-torpedo-truper.webp",
        "codes": ["NT-9", "12240"],
        "description": "Nivel tipo torpedo cuerpo de plástico ABS resistente con imán y 3 gotas Truper"
    },
    # 24. Disco abrasivo de corte fino Truper
    {
        "id": "disco-corte-fino-truper",
        "title": "Discos abrasivos de corte fino para metal 4-1/2\" Truper",
        "brand": "Truper",
        "page": 154,
        "raw_index": 8,
        "output_filename": "disco-corte-fino-truper.webp",
        "codes": ["ABR-810", "ABR-812", "11570", "11571", "11572"],
        "description": "Disco abrasivo de óxido de aluminio para corte rápido de metal y acero inoxidable 4-1/2\" Truper"
    },
    # 25. Disco abrasivo para corte de metal Pretul
    {
        "id": "disco-corte-metal-pretul",
        "title": "Discos abrasivos para corte de metal 4-1/2\" Pretul",
        "brand": "Pretul",
        "page": 154,
        "raw_index": 31,
        "output_filename": "disco-corte-metal-pretul.webp",
        "codes": ["ABR-810P", "ABR-812P", "22401", "22402"],
        "description": "Disco abrasivo para corte general de metales ferrosos y perfiles 4-1/2\" Pretul"
    },
    # 26. Disco de diamante rin continuo Truper
    {
        "id": "disco-diamante-continuo-truper",
        "title": "Discos de diamante rin continuo 4-1/2\" Truper",
        "brand": "Truper",
        "page": 154,
        "raw_index": 18,
        "output_filename": "disco-diamante-continuo-truper.webp",
        "codes": ["DIDA-45", "DIDA-70", "11580", "11581"],
        "description": "Disco de diamante rin continuo para corte limpio y fino de azulejo, loseta y cerámica Truper"
    },
    # 27. Disco de diamante segmentado Truper
    {
        "id": "disco-diamante-segmentado-truper",
        "title": "Discos de diamante segmentado 4-1/2\" Truper",
        "brand": "Truper",
        "page": 154,
        "raw_index": 20,
        "output_filename": "disco-diamante-segmentado-truper.webp",
        "codes": ["DID-45", "DID-70", "11582", "11583"],
        "description": "Disco de diamante segmentado para corte rápido en seco o húmedo de concreto y mampostería Truper"
    },
    # 28. Pala redonda mango madera Truper
    {
        "id": "pala-redonda-truper",
        "title": "Palas redondas mango de madera Truper",
        "brand": "Truper",
        "page": 291,
        "raw_index": 8,
        "output_filename": "pala-redonda-truper.webp",
        "codes": ["PRY-P", "PRY-F", "17160", "17161"],
        "description": "Pala redonda de acero con mango de encino y puño ergonómico Truper"
    },
    # 29. Pala cuadrada mango madera Truper
    {
        "id": "pala-cuadrada-truper",
        "title": "Palas cuadradas mango de madera Truper",
        "brand": "Truper",
        "page": 292,
        "raw_index": 2,
        "output_filename": "pala-cuadrada-truper.webp",
        "codes": ["PCY-P", "PCY-F", "17162", "17163"],
        "description": "Pala cuadrada para acarreo y mezcla de grava o arena mango de madera Truper"
    },
    # 30. Esmeriladora angular profesional 4-1/2" Truper
    {
        "id": "esmeriladora-angular-truper",
        "title": "Esmeriladoras angulares 4-1/2\" 800W Truper",
        "brand": "Truper",
        "page": 235,
        "raw_index": 29,
        "output_filename": "esmeriladora-angular-truper.webp",
        "codes": ["ESMA-4-1/2A9", "ESMA-4-1/2P", "16683", "20850"],
        "description": "Esmeriladora angular eléctrica 4-1/2\" con motor de baleros y mango auxiliar Truper"
    }
]

def pad_to_canvas(im, target_size=500, padding_pct=0.08):
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        base_im = bg
    else:
        base_im = im.convert("RGB")

    w, h = base_im.size
    max_dim = max(w, h)
    usable_size = int(target_size * (1 - 2 * padding_pct))
    scale = usable_size / max_dim

    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resample_filter = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS
    resized = base_im.resize((new_w, new_h), resample=resample_filter)

    canvas = Image.new("RGB", (target_size, target_size), (255, 255, 255))
    offset_x = (target_size - new_w) // 2
    offset_y = (target_size - new_h) // 2
    canvas.paste(resized, (offset_x, offset_y))
    return canvas

def run_extraction():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

    # 1. Extraer imágenes crudas de las páginas necesarias
    pages_needed = sorted(list(set(g["page"] for g in NEW_GROUPS)))
    print(f"[*] Extrayendo imágenes crudas de páginas: {pages_needed}...")

    for p in pages_needed:
        prefix = os.path.join(TMP_DIR, f"p{p}_raw")
        if not os.path.exists(f"{prefix}-000.png"):
            cmd = ["pdfimages", "-png", "-f", str(p), "-l", str(p), PDF_PATH, prefix]
            subprocess.run(cmd, check=True)

    # 2. Procesar y normalizar a WebP
    print("[*] Normalizando 30 nuevas imágenes a 500x500 WebP...")
    extracted_count = 0
    for g in NEW_GROUPS:
        p = g["page"]
        idx = g["raw_index"]
        raw_path = os.path.join(TMP_DIR, f"p{p}_raw-{idx:03d}.png")
        if not os.path.exists(raw_path):
            print(f"[!] Archivo {raw_path} no encontrado para {g['id']}", file=sys.stderr)
            continue

        im = Image.open(raw_path)
        canvas = pad_to_canvas(im, target_size=500, padding_pct=0.08)
        out_path = os.path.join(OUTPUT_IMG_DIR, g["output_filename"])
        canvas.save(out_path, "WEBP", quality=90, method=6)
        file_size_kb = os.path.getsize(out_path) / 1024.0
        print(f"  [+] Generado {g['output_filename']} ({canvas.size[0]}x{canvas.size[1]} px, {file_size_kb:.1f} KB)")
        extracted_count += 1

    # 3. Cruzar con data/products.json
    print("[*] Actualizando data/products.json con el segundo lote de imágenes...")
    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        products = json.load(f)

    # Cargar manifiesto existente
    with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    existing_groups = manifest.get("groups", [])
    existing_group_ids = set(g["id"] for g in existing_groups)

    # Agregar los nuevos grupos sin duplicar
    for ng in NEW_GROUPS:
        if ng["id"] not in existing_group_ids:
            existing_groups.append(ng)
            existing_group_ids.add(ng["id"])

    updated_count = 0
    updated_products_list = manifest.get("updated_products", [])
    already_updated_skus = set(up.get("sku") for up in updated_products_list)

    # Indexar productos existentes para coincidencia rápida
    for g in NEW_GROUPS:
        group_codes = set(c.upper() for c in g["codes"])
        group_rel_img = f"assets/images/products/truper/{g['output_filename']}"

        for p in products:
            sku = str(p.get("sku", "")).strip().upper()
            mfg = str(p.get("manufacturer_code", "")).strip().upper()
            name = p.get("name", "").lower()

            matched = False
            match_reason = ""

            if sku in group_codes:
                matched = True
                match_reason = f"SKU:{sku}"
            elif mfg in group_codes:
                matched = True
                match_reason = f"Clave:{mfg}"
            elif g["id"] == "carretilla-bastidor-truper" and "carretilla" in name and "truper" in name and "5.5" in name:
                matched = True
                match_reason = "Nombre:Carretilla Truper 5.5"
            elif g["id"] == "cuchara-filadelfia-truper" and "cuchara" in name and "filadelfia" in name:
                matched = True
                match_reason = "Nombre:Cuchara Filadelfia"
            elif g["id"] == "flexometro-gripper-truper" and "flexometro" in name and "gripper" in name:
                matched = True
                match_reason = "Nombre:Flexómetro Gripper"
            elif g["id"] == "desarmadores-comfortgrip-truper" and "desarmador" in name and "comfort grip" in name:
                matched = True
                match_reason = "Nombre:Desarmador Comfort Grip"
            elif g["id"] == "llave-ajustable-perico-truper" and ("perico" in name or "llave ajustable" in name) and "truper" in name:
                matched = True
                match_reason = "Nombre:Perico Truper"
            elif g["id"] == "llave-tubo-stilson-truper" and "stilson" in name and "truper" in name:
                matched = True
                match_reason = "Nombre:Stilson Truper"
            elif g["id"] == "pinza-electricista-truper" and "electricista" in name and "truper" in name:
                matched = True
                match_reason = "Nombre:Pinza Electricista"
            elif g["id"] == "pinza-chofer-truper" and "chofer" in name and "truper" in name:
                matched = True
                match_reason = "Nombre:Pinza Chofer"
            elif g["id"] == "pinza-presion-curva-truper" and "presion" in name and "curva" in name:
                matched = True
                match_reason = "Nombre:Pinza Presión Curva"
            elif g["id"] == "esmeriladora-angular-truper" and "esmeriladora" in name and "truper" in name:
                matched = True
                match_reason = "Nombre:Esmeriladora Truper"

            if matched:
                old_img = p.get("image", "")
                p["image"] = group_rel_img
                p["image_url"] = group_rel_img
                updated_count += 1
                if p.get("sku") not in already_updated_skus:
                    already_updated_skus.add(p.get("sku"))
                    updated_products_list.append({
                        "id": p.get("id"),
                        "sku": p.get("sku"),
                        "name": p.get("name"),
                        "brand": p.get("brand", g["brand"]),
                        "matched_by": match_reason,
                        "group": g["title"],
                        "old_image": old_img,
                        "new_image": group_rel_img
                    })

    # Guardar products.json actualizado
    with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    # Actualizar manifiesto
    total_sku_mappings = sum(len(grp.get("codes", [])) for grp in existing_groups)
    manifest["total_catalog_groups"] = len(existing_groups)
    manifest["total_sku_mappings"] = total_sku_mappings
    manifest["total_store_products_updated"] = len(updated_products_list)
    manifest["groups"] = existing_groups
    manifest["updated_products"] = updated_products_list

    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Extracción Lote 2 completada con éxito:")
    print(f"    - Nuevas familias generadas: {extracted_count}")
    print(f"    - Total familias visuales en catálogo: {len(existing_groups)}")
    print(f"    - Total códigos / SKUs mapeados: {total_sku_mappings}")
    print(f"    - Total productos en tienda con fotos oficiales: {len(updated_products_list)}")

if __name__ == "__main__":
    run_extraction()
