#!/usr/bin/env node
/**
 * scripts/convert_catalog.js
 * Ferretería y Tlapalería El Águila - Conversor de Catálogo Oficial
 * Procesa 17,641 artículos desde 'raticulos ferre precios.csv'
 * Aplica fórmula base_price = round(PRECIO_1 * 1.16, 2)
 * Clasifica en 5 departamentos oficiales y extrae marcas homologadas.
 * Exporta data/products.json pre-ordenado por nombre ascendente.
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = (typeof __dirname !== 'undefined' && __dirname && fs.existsSync(path.join(__dirname, '..', 'raticulos ferre precios.csv'))) ? path.resolve(__dirname, '..') : process.cwd();
const CSV_FILE = path.join(ROOT_DIR, 'raticulos ferre precios.csv');
const OUTPUT_FILE = path.join(ROOT_DIR, 'data', 'products.json');

const BRANDS = [
  "Truper", "Pretul", "Voltech", "Basic", "Hermex", "Foset", "Fiero", "Fandeli",
  "Urrea", "Surtek", "Nacobre", "Cresco", "Rotoplas", "Coflex", "Helvex", "Dica",
  "Resistol", "Sika", "Comex", "DeWalt", "Makita", "Bosch", "Milwaukee", "Stanley",
  "IUSA", "Condumex", "Viakon", "Bticino"
];

const CATEGORY_IMAGES = {
  "Tornillería y Fijación": "assets/images/cat-tornilleria.jpg",
  "Material Eléctrico": "assets/images/cat-electrico.jpg",
  "Plomería y Conexiones": "assets/images/cat-plomeria.jpg",
  "Herramientas en General": "assets/images/cat-herramientas.jpg",
  "Tlapalería y Construcción": "assets/images/cat-tlapaleria.jpg"
};

function extractBrand(desc) {
  if (!desc) return "Homologado";
  
  // 1. Trailing brand match: ", Brand" at end of string
  for (const b of BRANDS) {
    const trailingRegex = new RegExp(`,\\s*${b}[\\s."']*$`, 'i');
    if (trailingRegex.test(desc)) {
      return b;
    }
  }

  // 2. Word boundary match
  for (const b of BRANDS) {
    if (b.toLowerCase() === "basic") {
      if (/(?:,\s*Basic\b|\bBasic\b)/.test(desc)) {
        return "Basic";
      }
    } else {
      const wordRegex = new RegExp(`\\b${b}\\b`, 'i');
      if (wordRegex.test(desc)) {
        return b;
      }
    }
  }

  return "Homologado";
}

function classifyCategory(sku, name, brand) {
  const text = (sku + " " + name).toLowerCase();

  // Strong brand affiliations
  if (["Voltech", "IUSA", "Condumex", "Viakon", "Bticino"].includes(brand)) {
    return "Material Eléctrico";
  }
  if (["Foset", "Nacobre", "Cresco", "Rotoplas", "Coflex", "Helvex", "Dica"].includes(brand)) {
    return "Plomería y Conexiones";
  }
  if (["Fandeli", "Resistol", "Sika", "Comex", "Hermex"].includes(brand)) {
    return "Tlapalería y Construcción";
  }

  // 1. Material Eléctrico
  const electricalRegex = /\b(?:mufa|zumbador|timbre|campanill\w*|soquet\w*|socket\w*|portalampara\w*|clavija\w*|multicontacto\w*|apagador\w*|interrup\w*|contacto\w*|polarizado\w*|duplex|termomagnet\w*|pastilla\w*|centro de carga|tablero|balastr\w*|conduit|chalupa\w*|caja registro|cable\w*|alambre\w*|thw|cordon\w*|conductor\w*|uso rudo|pot|foco\w*|led\w*|lampara\w*|luminaria\w*|reflector\w*|arbotante\w*|tubo led|canaleta\w*|cinta aislar|cinta de aislar|clema\w*|fusible\w*|cuchilla\w*|fotoceld\w*|fotocontrol\w*|sensor\w*|127\s*v|220\s*v|volts|extension|extensiones)\b/i;
  if (electricalRegex.test(text)) {
    return "Material Eléctrico";
  }

  // 2. Tornillería y Fijación
  const fastenerRegex = /\b(?:tornillo\w*|pija\w*|tuerca\w*|rondana\w*|arandela\w*|varilla roscada|taquete\w*|birlo\w*|abrazadera\w*|perno\w*|remache\w*|clavo\w*|grapa\w*|esparrago\w*|cancamo\w*|alcayata\w*|chilillo\w*|mariposa\w*|hembrilla\w*|argolla\w*|grillete\w*|tensor\w*|opresor\w*|chaveta\w*)\b/i;
  if (fastenerRegex.test(text)) {
    return "Tornillería y Fijación";
  }

  // 3. Plomería y Conexiones
  const plumbingRegex = /\b(?:tubo\b|tuberia\w*|pvc\b|cpvc\b|cobre\b|galvaniz\w*|poliducto\w*|manguera\w*|valvula\w*|llave\b|mezcladora\w*|monomando\w*|regadera\w*|maneral\w*|cespol\w*|coladera\w*|flotador\w*|wc\b|taza\b|tanque\b|asiento wc|herraje wc|sapito\w*|cuello de cera|cople\w*|codo\w*|tee\b|reduccion\w*|tuerca union|tapon\w*|conector\w*|niple\w*|bushing\w*|tinaco\w*|cisterna\w*|bomba agua|motobomba\w*|presurizador\w*|hidroneumatico\w*|pichancha\w*|filtro agua|cartucho\w*|teflon\b|fluxometr\w*|trampa\b|mingitorio\w*|lavabo\w*|fregadero\w*|tarja\w*)\b/i;
  if (plumbingRegex.test(text)) {
    return "Plomería y Conexiones";
  }

  // 4. Herramientas en General
  const toolRegex = /\b(?:pinza\w*|alicate\w*|martillo\w*|marro\w*|desarmador\w*|destornillador\w*|llave espanol\w*|llave combinad\w*|llave stilson|llave perico|llave ajustable|llave allen|llave torx|matraca\w*|dado\b|dados\b|juego de dado\w*|segueta\w*|arco\b|serrucho\w*|sierra\w*|disco de corte|disco diamant\w*|broca\w*|cincel\w*|punzon\w*|cinta metric\w*|flexometr\w*|nivel\b|escuadra\w*|escalera\w*|carretilla\w*|pala\b|talacho\w*|zapapico\w*|azadon\w*|rastrillo\w*|machete\w*|tijera\w*|cizalla\w*|cortadora\w*|remachadora\w*|pistola\w*|engrapadora\w*|esmeril\w*|taladro\w*|rotomartillo\w*|caladora\w*|pulidora\w*|cepillo\w*|compresor\w*|soldadora\w*|careta\w*|generador\w*|bateria\b|cargador\b|torquimetr\w*|caja herramienta\w*|maleta herramienta\w*|cautin\b)\b/i;
  if (toolRegex.test(text)) {
    return "Herramientas en General";
  }

  // 5. Default: Tlapalería y Construcción
  return "Tlapalería y Construcción";
}

function parseCSVLine(line) {
  const result = [];
  let cur = '';
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (c === '"') {
      if (inQuotes && line[i + 1] === '"') {
        cur += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      result.push(cur);
      cur = '';
    } else {
      cur += c;
    }
  }
  result.push(cur);
  return result;
}

function inferUnitMeasure(name) {
  const lower = name.toLowerCase();
  if (/\b(?:rollo|rollos)\b/.test(lower)) return "ROLLO";
  if (/\b(?:metro|metros|mts)\b/.test(lower)) return "MTR";
  if (/\b(?:litro|litros|lto|ltos)\b/.test(lower)) return "LTO";
  if (/\b(?:kilo|kilos|kg|kgs)\b/.test(lower)) return "KG";
  if (/\b(?:juego|juegos|jgo|jgos)\b/.test(lower)) return "JGO";
  if (/\b(?:ciento|cientos)\b/.test(lower)) return "CTO";
  if (/\b(?:millar|millares)\b/.test(lower)) return "MIL";
  if (/\b(?:par|pares)\b/.test(lower)) return "PAR";
  return "PZA";
}

function runConversion() {
  console.log(`[convert_catalog] Leyendo ${CSV_FILE}...`);
  const content = fs.readFileSync(CSV_FILE, 'utf-8');
  const rawLines = content.split(/\r?\n/);
  
  // Skip 2 header lines: Line 1 metadata ("Lista de precios,,"), Line 2 header ("ARTICULO,DESCRIPCION,PRECIO 1")
  const dataLines = [];
  for (let i = 2; i < rawLines.length; i++) {
    const line = rawLines[i].trim();
    if (line) {
      dataLines.push(rawLines[i]);
    }
  }

  console.log(`[convert_catalog] Total de líneas de productos detectadas: ${dataLines.length}`);
  if (dataLines.length !== 17641) {
    console.warn(`[convert_catalog] ADVERTENCIA: Se esperaban 17,641 registros, pero se encontraron ${dataLines.length}`);
  }

  const products = [];
  const categoryStats = {};
  const brandStats = {};

  for (let i = 0; i < dataLines.length; i++) {
    const row = parseCSVLine(dataLines[i]);
    if (row.length < 3) continue;

    const sku = row[0].trim();
    let desc = row[1].replace(/^[\s\u00A0]+|[\s\u00A0]+$/g, '').trim();
    const precio1 = parseFloat(row[2].trim()) || 0;

    // Handle placeholder SKUs with description '.'
    let name = desc;
    if (name === '.' || name === '') {
      name = `Artículo Técnico ${sku}`;
    }

    const basePrice = Math.round(precio1 * 1.16 * 100) / 100;
    const brand = extractBrand(desc);
    const category = classifyCategory(sku, name, brand);
    const unitMeasure = inferUnitMeasure(name);
    const imageUrl = CATEGORY_IMAGES[category] || "assets/images/cat-tlapaleria.jpg";

    categoryStats[category] = (categoryStats[category] || 0) + 1;
    brandStats[brand] = (brandStats[brand] || 0) + 1;

    products.push({
      sku: sku,
      manufacturer_code: sku,
      name: name,
      category: category,
      categories: { name: category },
      brand: brand,
      brands: { name: brand },
      base_price: basePrice,
      unit_measure: unitMeasure,
      image_url: imageUrl,
      image: imageUrl
    });
  }

  // Pre-sort array by name ascending (case-insensitive)
  console.log(`[convert_catalog] Pre-ordenando ${products.length} productos por nombre ascendente...`);
  products.sort((a, b) => a.name.localeCompare(b.name, 'es', { sensitivity: 'base' }));

  // Assign sequential 1-based IDs after sorting
  for (let i = 0; i < products.length; i++) {
    products[i].id = i + 1;
  }

  // Ensure output directory exists and write JSON
  fs.mkdirSync(path.dirname(OUTPUT_FILE), { recursive: true });
  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(products, null, 2), 'utf-8');
  console.log(`[convert_catalog] Guardado exitosamente en: ${OUTPUT_FILE} (${products.length} artículos)`);

  // Spot-check validation
  console.log("\n=== VALIDACIÓN DE SPOT-CHECKS ===");
  const checkSkus = ["661", "5661R", "MUFA-3/4", "M-048P", "1524"];
  const skuMap = new Map(products.map(p => [p.sku, p]));
  for (const sku of checkSkus) {
    const item = skuMap.get(sku);
    if (item) {
      console.log(`  SKU ${sku}: base_price=${item.base_price} | cat='${item.category}' | brand='${item.brand}' | name='${item.name}'`);
    } else {
      console.error(`  ERROR: SKU ${sku} no encontrado en catálogo generado!`);
    }
  }

  console.log("\n=== DISTRIBUCIÓN POR DEPARTAMENTO ===");
  for (const [cat, count] of Object.entries(categoryStats).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${cat}: ${count}`);
  }

  console.log("\n=== TOP 10 MARCAS HOMOLOGADAS ===");
  for (const [b, count] of Object.entries(brandStats).sort((a, b) => b[1] - a[1]).slice(0, 10)) {
    console.log(`  ${b}: ${count}`);
  }

  return { total: products.length, categoryStats, brandStats };
}

runConversion();

module.exports = { runConversion, extractBrand, classifyCategory, inferUnitMeasure };
