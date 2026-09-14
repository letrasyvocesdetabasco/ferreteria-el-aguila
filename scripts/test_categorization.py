#!/usr/bin/env python3
import csv
import re

BRANDS = [
    "Truper", "Pretul", "Voltech", "Basic", "Hermex", "Foset", "Fiero", "Fandeli",
    "Urrea", "Surtek", "Nacobre", "Cresco", "Rotoplas", "Coflex", "Helvex", "Dica",
    "Resistol", "Sika", "Comex", "DeWalt", "Makita", "Bosch", "Milwaukee", "Stanley",
    "IUSA", "Condumex", "Viakon", "Bticino"
]

def extract_brand(desc):
    # 1. Trailing brand match: ", Brand" at end of string
    for b in BRANDS:
        pattern = rf',\s*{re.escape(b)}[\s."\']*$'
        if re.search(pattern, desc, re.IGNORECASE):
            return b
            
    # 2. Whole word match
    for b in BRANDS:
        if b.lower() == "basic":
            # For Basic, match exact case or with comma
            if re.search(r'(?:,\s*Basic\b|\bBasic\b)', desc):
                return "Basic"
        else:
            pattern = rf'\b{re.escape(b)}\b'
            if re.search(pattern, desc, re.IGNORECASE):
                return b
                
    return "Homologado"

def classify_category(sku, name, brand):
    text = (sku + " " + name).lower()
    
    # Check strong electrical brand
    if brand in ["Voltech", "IUSA", "Condumex", "Viakon", "Bticino"]:
        # Strong electrical brand
        return "Material Eléctrico"
        
    # Check strong plumbing brand
    if brand in ["Foset", "Nacobre", "Cresco", "Rotoplas", "Coflex", "Helvex", "Dica"]:
        return "Plomería y Conexiones"
        
    # Check strong abrasives/adhesives/paints brand
    if brand in ["Fandeli", "Resistol", "Sika", "Comex"]:
        return "Tlapalería y Construcción"
        
    # Check strong lock/hardware brand
    if brand in ["Hermex"]:
        return "Tlapalería y Construcción"

    # Specific electrical terms
    electrical_keywords = [
        r'\bmufa\b', r'\bzumbador\b', r'\btimbre\b', r'\bcampanill', r'\bsoquet\b', r'\bsocket\b',
        r'\bportalampara\b', r'\bclavija\b', r'\bmulticontacto\b', r'\bapagador\b', r'\binterrup\w*',
        r'\bcontacto\b', r'\bcontactos\b', r'\bpolarizado\b', r'\bduplex\b', r'\btermomagnet\w*',
        r'\bpastilla\b', r'\bcentro de carga\b', r'\btablero\b', r'\bbalastr\w*', r'\bconduit\b',
        r'\bchalupa\b', r'\bcaja registro\b', r'\bcable\b', r'\balambre\b', r'\bthw\b', r'\bcordon\b',
        r'\bconductor\b', r'\buso rudo\b', r'\bpot\b', r'\bfoco\b', r'\bled\b', r'\blampara\b',
        r'\bluminaria\b', r'\breflector\b', r'\barbotante\b', r'\btubo led\b', r'\bcanaleta\b',
        r'\bcinta aislar\b', r'\bcinta de aislar\b', r'\bclema\b', r'\bfusible\b', r'\bcuchilla\b',
        r'\bfotoceld\w*', r'\bfotocontrol\b', r'\bsensor\b', r'\b127\s*v', r'\b220\s*v', r'\bvolts\b',
        r'\bextension\b', r'\bextensiones\b', r'\bportal\w*mp'
    ]
    for kw in electrical_keywords:
        if re.search(kw, text):
            return "Material Eléctrico"

    # Fasteners (Tornillería y Fijación)
    fastener_keywords = [
        r'\btornillo\w*', r'\bpija\w*', r'\btuerca\w*', r'\brondana\w*', r'\barandela\w*',
        r'\bvarilla roscada\b', r'\btaquete\w*', r'\bbirlo\w*', r'\babrazadera\w*', r'\bperno\w*',
        r'\bremache\w*', r'\bclavo\w*', r'\bgrapa\w*', r'\besparrago\w*', r'\bcancamo\w*',
        r'\balcayata\w*', r'\bchilillo\w*', r'\bmariposa\w*', r'\bhembrilla\w*', r'\bargolla\w*',
        r'\bgrillete\w*', r'\btensor\w*', r'\bopresor\w*', r'\bchaveta\w*'
    ]
    for kw in fastener_keywords:
        if re.search(kw, text):
            return "Tornillería y Fijación"

    # Plumbing (Plomería y Conexiones)
    plumbing_keywords = [
        r'\btubo\b', r'\btuberia\b', r'\bpvc\b', r'\bcpvc\b', r'\bcobre\b', r'\bgalvaniz\w*',
        r'\bpoliducto\b', r'\bmanguera\w*', r'\bvalvula\w*', r'\bllave\b', r'\bmezcladora\w*',
        r'\bmonomando\w*', r'\bregadera\w*', r'\bmaneral\w*', r'\bcespol\b', r'\bcoladera\w*',
        r'\bflotador\w*', r'\bwc\b', r'\btaza\b', r'\btanque\b', r'\basiento wc\b',
        r'\bherraje wc\b', r'\bsapito\b', r'\bcuello de cera\b', r'\bcople\w*', r'\bcodo\w*',
        r'\btee\b', r'\breduccion\w*', r'\btuerca union\b', r'\btapon\w*', r'\bconector\w*',
        r'\bniple\w*', r'\bbushing\w*', r'\btinaco\w*', r'\bcisterna\w*', r'\bbomba agua\b',
        r'\bmotobomba\w*', r'\bpresurizador\w*', r'\bhidroneumatico\w*', r'\bpichancha\w*',
        r'\bfiltro agua\b', r'\bcartucho\w*', r'\bteflon\b', r'\bfluxometr\w*', r'\btrampa\b',
        r'\bmingitorio\w*', r'\blavabo\w*', r'\bfregadero\w*', r'\btarja\w*'
    ]
    for kw in plumbing_keywords:
        if re.search(kw, text):
            return "Plomería y Conexiones"

    # Tools (Herramientas en General)
    tool_keywords = [
        r'\bpinza\w*', r'\balicate\w*', r'\bmartillo\w*', r'\bmarro\w*', r'\bdesarmador\w*',
        r'\bdestornillador\w*', r'\bllave espanol\w*', r'\bllave combinad\w*', r'\bllave stilson\b',
        r'\bllave perico\b', r'\bllave ajustable\b', r'\bllave allen\b', r'\bllave torx\b',
        r'\bmatraca\w*', r'\bdado\b', r'\bdados\b', r'\bjuego de dado\w*', r'\bsegueta\w*',
        r'\barco\b', r'\bserrucho\w*', r'\bsierra\w*', r'\bdisco de corte\b', r'\bdisco diamant\w*',
        r'\bbroca\w*', r'\bcincel\w*', r'\bpunzon\w*', r'\bcinta metric\w*', r'\bflexometr\w*',
        r'\bnivel\b', r'\bescuadra\w*', r'\bescalera\w*', r'\bcarretilla\w*', r'\bpala\b',
        r'\btalacho\w*', r'\bzapapico\w*', r'\bazadon\w*', r'\brastrillo\w*', r'\bmachete\w*',
        r'\btijera\w*', r'\bcizalla\w*', r'\bcortadora\w*', r'\bremachadora\w*', r'\bpistola\w*',
        r'\bengrapadora\w*', r'\besmeril\w*', r'\btaladro\w*', r'\brotomartillo\w*', r'\bcaladora\w*',
        r'\bpulidora\w*', r'\bcepillo\w*', r'\bcompresor\w*', r'\bsoldadora\w*', r'\bcareta\w*',
        r'\bgenerador\w*', r'\bbateria\b', r'\bcargador\b', r'\btorquimetr\w*', r'\bcaja herramienta\w*',
        r'\bmaleta herramienta\w*', r'\bcautin\b'
    ]
    for kw in tool_keywords:
        if re.search(kw, text):
            return "Herramientas en General"

    # Default: Tlapalería y Construcción
    return "Tlapalería y Construcción"

with open("raticulos ferre precios.csv", "r", encoding="utf-8", errors="replace") as f:
    reader = csv.reader(f)
    next(reader)
    next(reader)
    
    cat_counts = {}
    brand_counts = {}
    spot_checks = {}
    
    for row in reader:
        if not row: continue
        sku = row[0].strip()
        desc = row[1].strip()
        p1 = float(row[2].strip())
        
        brand = extract_brand(desc)
        cat = classify_category(sku, desc, brand)
        price = round(p1 * 1.16, 2)
        
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        if sku in ["661", "5661R", "MUFA-3/4", "M-048P", "1524"]:
            spot_checks[sku] = (desc, price, cat, brand)

print("=== SPOT CHECKS ===")
for sku, info in spot_checks.items():
    print(f"{sku}: price={info[1]}, cat={info[2]}, brand={info[3]}")
    
print("\n=== CATEGORY COUNTS ===")
for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {cnt}")
    
print("\n=== TOP BRANDS ===")
for b, cnt in sorted(brand_counts.items(), key=lambda x: -x[1])[:15]:
    print(f"  {b}: {cnt}")
