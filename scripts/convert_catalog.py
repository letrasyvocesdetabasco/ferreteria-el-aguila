#!/usr/bin/env python3
"""
scripts/convert_catalog.py
Ferretería y Tlapalería El Águila - Conversor de Catálogo Oficial
Procesa 17,641 artículos desde 'raticulos ferre precios.csv'
Aplica fórmula base_price = round(PRECIO_1 * 1.16, 2)
Clasifica en 5 departamentos oficiales y extrae marcas homologadas.
Exporta data/products.json pre-ordenado por nombre ascendente.
"""

import csv
import json
import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raticulos ferre precios.csv")) else os.getcwd()
CSV_FILE = os.path.join(ROOT_DIR, "raticulos ferre precios.csv")
OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "products.json")

BRANDS = [
    "Truper", "Pretul", "Voltech", "Basic", "Hermex", "Foset", "Fiero", "Fandeli",
    "Urrea", "Surtek", "Nacobre", "Cresco", "Rotoplas", "Coflex", "Helvex", "Dica",
    "Resistol", "Sika", "Comex", "DeWalt", "Makita", "Bosch", "Milwaukee", "Stanley",
    "IUSA", "Condumex", "Viakon", "Bticino"
]

CATEGORY_IMAGES = {
    "Tornillería y Fijación": "assets/images/cat-tornilleria.jpg",
    "Material Eléctrico": "assets/images/cat-electrico.jpg",
    "Plomería y Conexiones": "assets/images/cat-plomeria.jpg",
    "Herramientas en General": "assets/images/cat-herramientas.jpg",
    "Tlapalería y Construcción": "assets/images/cat-tlapaleria.jpg"
}

def extract_brand(desc: str) -> str:
    if not desc:
        return "Homologado"
        
    # 1. Trailing brand match: ", Brand" at end of string
    for b in BRANDS:
        pattern = rf',\s*{re.escape(b)}[\s."\']*$'
        if re.search(pattern, desc, re.IGNORECASE):
            return b

    # 2. Word boundary match
    for b in BRANDS:
        if b.lower() == "basic":
            if re.search(r'(?:,\s*Basic\b|\bBasic\b)', desc):
                return "Basic"
        else:
            pattern = rf'\b{re.escape(b)}\b'
            if re.search(pattern, desc, re.IGNORECASE):
                return b

    return "Homologado"

def classify_category(sku: str, name: str, brand: str) -> str:
    text = f"{sku} {name}".lower()

    # Strong brand affiliations
    if brand in ["Voltech", "IUSA", "Condumex", "Viakon", "Bticino"]:
        return "Material Eléctrico"
    if brand in ["Foset", "Nacobre", "Cresco", "Rotoplas", "Coflex", "Helvex", "Dica"]:
        return "Plomería y Conexiones"
    if brand in ["Fandeli", "Resistol", "Sika", "Comex", "Hermex"]:
        return "Tlapalería y Construcción"

    # 1. Material Eléctrico
    electrical_regex = r'\b(?:mufa|zumbador|timbre|campanill\w*|soquet\w*|socket\w*|portalampara\w*|clavija\w*|multicontacto\w*|apagador\w*|interrup\w*|contacto\w*|polarizado\w*|duplex|termomagnet\w*|pastilla\w*|centro de carga|tablero|balastr\w*|conduit|chalupa\w*|caja registro|cable\w*|alambre\w*|thw|cordon\w*|conductor\w*|uso rudo|pot|foco\w*|led\w*|lampara\w*|luminaria\w*|reflector\w*|arbotante\w*|tubo led|canaleta\w*|cinta aislar|cinta de aislar|clema\w*|fusible\w*|cuchilla\w*|fotoceld\w*|fotocontrol\w*|sensor\w*|127\s*v|220\s*v|volts|extension|extensiones)\b'
    if re.search(electrical_regex, text, re.IGNORECASE):
        return "Material Eléctrico"

    # 2. Tornillería y Fijación
    fastener_regex = r'\b(?:tornillo\w*|pija\w*|tuerca\w*|rondana\w*|arandela\w*|varilla roscada|taquete\w*|birlo\w*|abrazadera\w*|perno\w*|remache\w*|clavo\w*|grapa\w*|esparrago\w*|cancamo\w*|alcayata\w*|chilillo\w*|mariposa\w*|hembrilla\w*|argolla\w*|grillete\w*|tensor\w*|opresor\w*|chaveta\w*)\b'
    if re.search(fastener_regex, text, re.IGNORECASE):
        return "Tornillería y Fijación"

    # 3. Plomería y Conexiones
    plumbing_regex = r'\b(?:tubo\b|tuberia\w*|pvc\b|cpvc\b|cobre\b|galvaniz\w*|poliducto\w*|manguera\w*|valvula\w*|llave\b|mezcladora\w*|monomando\w*|regadera\w*|maneral\w*|cespol\w*|coladera\w*|flotador\w*|wc\b|taza\b|tanque\b|asiento wc|herraje wc|sapito\w*|cuello de cera|cople\w*|codo\w*|tee\b|reduccion\w*|tuerca union|tapon\w*|conector\w*|niple\w*|bushing\w*|tinaco\w*|cisterna\w*|bomba agua|motobomba\w*|presurizador\w*|hidroneumatico\w*|pichancha\w*|filtro agua|cartucho\w*|teflon\b|fluxometr\w*|trampa\b|mingitorio\w*|lavabo\w*|fregadero\w*|tarja\w*)\b'
    if re.search(plumbing_regex, text, re.IGNORECASE):
        return "Plomería y Conexiones"

    # 4. Herramientas en General
    tool_regex = r'\b(?:pinza\w*|alicate\w*|martillo\w*|marro\w*|desarmador\w*|destornillador\w*|llave espanol\w*|llave combinad\w*|llave stilson|llave perico|llave ajustable|llave allen|llave torx|matraca\w*|dado\b|dados\b|juego de dado\w*|segueta\w*|arco\b|serrucho\w*|sierra\w*|disco de corte|disco diamant\w*|broca\w*|cincel\w*|punzon\w*|cinta metric\w*|flexometr\w*|nivel\b|escuadra\w*|escalera\w*|carretilla\w*|pala\b|talacho\w*|zapapico\w*|azadon\w*|rastrillo\w*|machete\w*|tijera\w*|cizalla\w*|cortadora\w*|remachadora\w*|pistola\w*|engrapadora\w*|esmeril\w*|taladro\w*|rotomartillo\w*|caladora\w*|pulidora\w*|cepillo\w*|compresor\w*|soldadora\w*|careta\w*|generador\w*|bateria\b|cargador\b|torquimetr\w*|caja herramienta\w*|maleta herramienta\w*|cautin\b)\b'
    if re.search(tool_regex, text, re.IGNORECASE):
        return "Herramientas en General"

    # 5. Default: Tlapalería y Construcción
    return "Tlapalería y Construcción"

def infer_unit_measure(name: str) -> str:
    lower = name.lower()
    if re.search(r'\b(?:rollo|rollos)\b', lower):
        return "ROLLO"
    if re.search(r'\b(?:metro|metros|mts)\b', lower):
        return "MTR"
    if re.search(r'\b(?:litro|litros|lto|ltos)\b', lower):
        return "LTO"
    if re.search(r'\b(?:kilo|kilos|kg|kgs)\b', lower):
        return "KG"
    if re.search(r'\b(?:juego|juegos|jgo|jgos)\b', lower):
        return "JGO"
    if re.search(r'\b(?:ciento|cientos)\b', lower):
        return "CTO"
    if re.search(r'\b(?:millar|millares)\b', lower):
        return "MIL"
    if re.search(r'\b(?:par|pares)\b', lower):
        return "PAR"
    return "PZA"

def run_conversion():
    print(f"[convert_catalog] Leyendo {CSV_FILE}...")
    with open(CSV_FILE, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        # Skip 2 header lines: Line 1 metadata, Line 2 header
        next(reader)
        next(reader)

        products = []
        category_stats = {}
        brand_stats = {}

        for row in reader:
            if not row or len(row) < 3:
                continue

            sku = row[0].strip()
            desc = row[1].replace('\xa0', ' ').strip()
            try:
                precio_1 = float(row[2].strip())
            except ValueError:
                precio_1 = 0.0

            # Handle placeholder SKUs with description '.'
            name = desc
            if name in ['.', '']:
                name = f"Artículo Técnico {sku}"

            base_price = round(precio_1 * 1.16, 2)
            brand = extract_brand(desc)
            category = classify_category(sku, name, brand)
            unit_measure = infer_unit_measure(name)
            image_url = CATEGORY_IMAGES.get(category, "assets/images/cat-tlapaleria.jpg")

            category_stats[category] = category_stats.get(category, 0) + 1
            brand_stats[brand] = brand_stats.get(brand, 0) + 1

            products.append({
                "sku": sku,
                "manufacturer_code": sku,
                "name": name,
                "category": category,
                "categories": {"name": category},
                "brand": brand,
                "brands": {"name": brand},
                "base_price": base_price,
                "unit_measure": unit_measure,
                "image_url": image_url,
                "image": image_url
            })

    print(f"[convert_catalog] Total de productos procesados: {len(products)}")
    if len(products) != 17641:
        print(f"[convert_catalog] ADVERTENCIA: Se esperaban 17,641 productos, encontrados {len(products)}", file=sys.stderr)

    # Pre-sort array by name ascending (case-insensitive)
    print(f"[convert_catalog] Pre-ordenando {len(products)} productos por nombre ascendente...")
    products.sort(key=lambda p: p["name"].lower())

    # Assign sequential 1-based IDs after sorting
    for idx, p in enumerate(products, 1):
        p["id"] = idx

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"[convert_catalog] Guardado exitosamente en: {OUTPUT_FILE} ({len(products)} artículos)")

    # Spot-check validation
    print("\n=== VALIDACIÓN DE SPOT-CHECKS ===")
    check_skus = ["661", "5661R", "MUFA-3/4", "M-048P", "1524"]
    sku_map = {p["sku"]: p for p in products}
    for sku in check_skus:
        item = sku_map.get(sku)
        if item:
            print(f"  SKU {sku}: base_price={item['base_price']} | cat='{item['category']}' | brand='{item['brand']}' | name='{item['name']}'")
        else:
            print(f"  ERROR: SKU {sku} no encontrado en catálogo generado!", file=sys.stderr)

    print("\n=== DISTRIBUCIÓN POR DEPARTAMENTO ===")
    for cat, cnt in sorted(category_stats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {cnt}")

    print("\n=== TOP 10 MARCAS HOMOLOGADAS ===")
    for b, cnt in sorted(brand_stats.items(), key=lambda x: -x[1])[:10]:
        print(f"  {b}: {cnt}")

if __name__ == "__main__":
    run_conversion()
