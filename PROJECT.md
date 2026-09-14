# Project: Ferretería y Tlapalería El Águila

## Architecture & Overview
Ferretería y Tlapalería El Águila is a high-performance, single-page web application and technical digital catalog for two retail branches in Villahermosa, Tabasco (Sucursal Las Delicias / Matriz and Sucursal Estrellas de Buena Vista).
The application is hosted as a Jamstack static site on GitHub Pages with custom domain `ferreteriaytlapaleria-elaguila.com`.

### Technical Components:
- **Presentation Layer**: Vanilla HTML5 (`index.html`) and responsive CSS3 design system (`assets/css/styles.css`) using CSS Custom Properties.
- **Client Application Engine**: Vanilla ES6+ (`assets/js/app.js`) handling in-memory catalog storage, tokenized instant search, facet filtering, batch DOM rendering via `DocumentFragment` (`PAGE_SIZE = 36`), and WhatsApp quotation generation.
- **Data Layer**: Static JSON catalog (`data/products.json`) containing exactly 17,641 items with retail pricing (+16% IVA), categorized into 5 official departments.
- **Visual & Brand Assets**: High-resolution counter canvas photograph (`assets/images/lona-oficial-el-aguila.jpg`), extracted transparent official eagle logo (`assets/images/logo-aguila.png`), and 5 department banners.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Full Catalog Ingestion (17,641 items) | Process all 17,641 records from `raticulos ferre precios.csv` / `.xls` into `data/products.json` | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Retail Price IVA Calculation (+16%) | Apply `base_price = round(PRECIO_1 * 1.16, 2)` to eliminate stale cost prices | M1 | ORIGINAL_REQUEST §R1 |
| 3 | 5 Official Department Classifications | Map all items to Tlapalería y Construcción, Tornillería y Fijación, Plomería y Conexiones, Herramientas en General, Material Eléctrico | M1 | ORIGINAL_REQUEST §R1 |
| 4 | Brand Recognition Heuristics | Detect Truper, Pretul, Voltech, Basic, Hermex, Foset, Fiero, Fandeli, etc. (defaulting to "Homologado") | M1 | ORIGINAL_REQUEST §R1 |
| 5 | High-Speed Search Indexing (<25ms) | Pre-compute `item._s` lowercase tokens and pre-sort by name ascending for sub-10ms search | M1 | ORIGINAL_REQUEST §R1 & Explorer 1 |
| 6 | Batch Rendering & 60 FPS Maintenance | Maintain `PAGE_SIZE = 36` with `DocumentFragment` batching and lazy loading | M1 | ORIGINAL_REQUEST §R1 & Explorer 1 |
| 7 | Hero Banner Overlay Removal | Remove `.hero-banner-badge` and `.hero-banner-caption` to unobstruct the physical canvas | M2 | ORIGINAL_REQUEST §R2 |
| 8 | 3:2 Aspect Ratio Hero Styling | Set `.hero-banner-card img` to `aspect-ratio: 3 / 2` with clean border radius and branded box shadow | M2 | ORIGINAL_REQUEST §R2 |
| 9 | Official Eagle Logo Extraction | Extract flying eagle silhouette from `lona-oficial-el-aguila.jpg` as transparent `assets/images/logo-aguila.png` (512x512) | M3 | ORIGINAL_REQUEST §R3 |
| 10 | Emoji 🦅 Replacement & Favicon | Replace `🦅` in header (line 40) and hero badge (line 89) with logo image; add favicon in `<head>` | M3 | ORIGINAL_REQUEST §R3 |
| 11 | Brand Palette Harmonization | Harmonize CSS variables to Azul Eléctrico Mostrador (#004b97 / #0052a5) and Oro Intenso (#ffcb05 / #f59e0b) | M3 | ORIGINAL_REQUEST §R3 |
| 12 | WhatsApp Quotation Calculation Verification | Ensure cart item subtotals and total reflect VAT-inclusive prices accurately | M4 | ORIGINAL_REQUEST §R4 |
| 13 | Multi-Branch Quotation Routing | Verify Las Delicias (993 289 2935 with San Joaquín landmark) and Buena Vista (993 192 8313) routing | M4 | ORIGINAL_REQUEST §R4 |
| 14 | Automated Test Harness (Tiers 1-4) | Automated tests verifying data integrity, pricing formulas, UI elements, search latency, and cart calculations | M4 | ORIGINAL_REQUEST §R4 & Dual Track |
| 15 | osvScanner Security Audit | Run `osvScanner` security scan and verify 0 vulnerabilities | M4 | ORIGINAL_REQUEST §R4 & User Rules |
| 16 | Final E2E Pass & GitHub Pages Deployment | Pass 100% E2E test suite, adversarial coverage hardening, git commit and push to `origin/main` | M5 | ORIGINAL_REQUEST §R4 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Catalog Replacement & Search Optimization | Convert 17,641 items, apply +16% IVA formula, classify 5 departments & brands, pre-compute search index, pre-sort JSON | none | COMPLETED |
| 2 | M2: Hero Banner Visual Clearing | Remove overlay badge and caption in HTML, set 3:2 aspect ratio in CSS, smooth shadow and borders | none | COMPLETED |
| 3 | M3: Eagle Logo & Brand Harmonization | Extract transparent `assets/images/logo-aguila.png`, replace 🦅 emoji, add favicon, update CSS palette to #004b97 and #ffcb05 | none | COMPLETED |
| 4 | M4: WhatsApp Checkout, Test Harness & Security Audit | Verify WhatsApp pricing & branches, build automated test suite (Tiers 1-4), execute osvScanner audit, publish TEST_READY.md | M1, M2, M3 | COMPLETED |
| 5 | M5: Final E2E Pass & Git Deployment | Verify 100% E2E tests pass, adversarial test hardening, git commit and push to GitHub Pages | M4 | COMPLETED |

## Interface Contracts
### Catalog Generator (`scripts/convert_catalog.py`) ↔ Client App (`assets/js/app.js`)
- `data/products.json` schema per item:
  ```json
  {
    "id": 1,
    "sku": "M-048P",
    "manufacturer_code": "M-048P",
    "name": "Mezcladora lavabo, manerales palanca, Basic",
    "category": "Plomería y Conexiones",
    "categories": { "name": "Plomería y Conexiones" },
    "brand": "Basic",
    "brands": { "name": "Basic" },
    "base_price": 371.0,
    "unit_measure": "PZA",
    "image_url": "assets/images/cat-plomeria.jpg",
    "image": "assets/images/cat-plomeria.jpg"
  }
  ```
- Total items: exactly 17,641.
- Pre-sorted: by `name` ascending (case-insensitive).
- Search index: client `app.js` builds `item._s = (item.sku + " " + (item.manufacturer_code||"") + " " + item.name + " " + item.brand + " " + item.category).toLowerCase()`.

### Image Extractor ↔ Web Frontend (`index.html`)
- Extracted Logo: `assets/images/logo-aguila.png` (PNG format, transparent background, 512x512 px).
- Header image tag: `<img src="assets/images/logo-aguila.png" alt="Logo Ferretería El Águila" class="brand-logo-img">`.
- Hero tag image: `<img src="assets/images/logo-aguila.png" alt="Águila en Vuelo" class="hero-tag-logo">`.
- Favicon link: `<link rel="icon" type="image/png" href="assets/images/logo-aguila.png">`.

## Code Layout
- `index.html` — Main SPA markup.
- `assets/css/styles.css` — Global styles, CSS variables, hero card styling, responsive layouts.
- `assets/js/app.js` — Client state, search pipeline, batch rendering, quotation drawer, WhatsApp generator.
- `data/products.json` — Static product catalog dataset (17,641 items).
- `assets/images/` — Image assets (`lona-oficial-el-aguila.jpg`, `logo-aguila.png`, `cat-*.jpg`).
- `scripts/convert_catalog.py` — Deterministic catalog conversion & validation script.
- `tests/` — Automated test suites verifying data integrity, pricing arithmetic, search performance, and checkout dispatch.
