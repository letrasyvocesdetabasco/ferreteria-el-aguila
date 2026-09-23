#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditing Test Suite: Logo, Branch 2 Exterior, Gaviotas WhatsApp-only, Search UX & ZIP Product Images.
Ferretería y Tlapalería El Águila.
"""

import json
import os
import re
import unittest
from PIL import Image

PROJECT_ROOT = "/home/divadios/Escritorio/pagina web/ferreteria_el_aguila"
INDEX_HTML = os.path.join(PROJECT_ROOT, "index.html")
APP_JS = os.path.join(PROJECT_ROOT, "assets", "js", "app.js")
STYLES_CSS = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")
PRODUCTS_JSON = os.path.join(PROJECT_ROOT, "data", "products.json")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "assets", "images")


class TestAuditUpdates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html = f.read()
        with open(APP_JS, "r", encoding="utf-8") as f:
            cls.js = f.read()
        with open(STYLES_CSS, "r", encoding="utf-8") as f:
            cls.css = f.read()
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            cls.products = json.load(f)

    # 1. LOGO, FAVICON & SEO SCHEMA
    def test_official_logo_and_favicons_exist(self):
        """Verify official logo, og-image, and favicon files exist with correct modes."""
        logo_path = os.path.join(IMAGES_DIR, "logo-aguila-oficial.png")
        self.assertTrue(os.path.isfile(logo_path), "Missing logo-aguila-oficial.png")

        fav_path = os.path.join(IMAGES_DIR, "favicon.png")
        self.assertTrue(os.path.isfile(fav_path), "Missing favicon.png")

        ico_path = os.path.join(PROJECT_ROOT, "favicon.ico")
        self.assertTrue(os.path.isfile(ico_path), "Missing favicon.ico")

        og_path = os.path.join(IMAGES_DIR, "og-image.jpg")
        self.assertTrue(os.path.isfile(og_path), "Missing og-image.jpg")
        with Image.open(og_path) as im:
            self.assertEqual(im.size, (1200, 630), "OG image must be 1200x630")

    def test_seo_metadata_and_schema_ldjson_in_html(self):
        """Verify OpenGraph, Twitter Cards, canonical link, and Schema.org JSON-LD in index.html."""
        self.assertIn('<link rel="canonical" href="https://ferreteriaytlapaleria-elaguila.com/">', self.html)
        self.assertIn('property="og:image"', self.html)
        self.assertIn('assets/images/og-image.jpg', self.html)
        self.assertIn('name="twitter:card"', self.html)
        self.assertIn('"@type": "HardwareStore"', self.html)
        self.assertIn('"potentialAction"', self.html)
        self.assertIn('"SearchAction"', self.html)

    # 2. SUCURSAL 2 (ESTRELLAS DE BUENA VISTA)
    def test_branch2_exterior_image_properties(self):
        """Verify Buena Vista exterior photo is WebP, >= 800px wide, < 250 KB."""
        img_path = os.path.join(IMAGES_DIR, "branches", "fachada-buenavista.webp")
        self.assertTrue(os.path.isfile(img_path), "Missing fachada-buenavista.webp")
        size_kb = os.path.getsize(img_path) / 1024
        self.assertLess(size_kb, 250, f"fachada-buenavista.webp is too large: {size_kb:.1f} KB")
        with Image.open(img_path) as im:
            self.assertGreaterEqual(im.width, 800)
            self.assertEqual(im.format, "WEBP")

    def test_branch2_exterior_alt_text_updated(self):
        """Verify Buena Vista card alt text mentions exterior photo."""
        self.assertIn('alt="Fachada Exterior Sucursal Estrellas de Buena Vista', self.html)

    # 3. SUCURSAL GAVIOTAS (PHONE 993 200 1178 & NO CALL BUTTON)
    def test_gaviotas_card_has_no_call_button(self):
        """Verify Gaviotas card does NOT have a tel: call button in index.html and WhatsApp button is concise."""
        gaviotas_card_match = re.search(r'<article[^>]+data-branch-id="gaviotas".*?</article>', self.html, re.DOTALL)
        self.assertIsNotNone(gaviotas_card_match, "Gaviotas card not found in index.html")
        gaviotas_card = gaviotas_card_match.group(0)

        self.assertNotIn("href=\"tel:", gaviotas_card, "Gaviotas branch must NOT have a call button (tel: link)!")
        self.assertIn("https://wa.me/529932001178", gaviotas_card, "Gaviotas must link to WhatsApp 993 200 1178")
        self.assertNotIn("Solo Mensajes", gaviotas_card, "Solo Mensajes must be removed from button for layout balance")
        self.assertIn("💬 WhatsApp", gaviotas_card)

    def test_gaviotas_contact_in_footer_and_drawer(self):
        """Verify Gaviotas contact in footer and drawer uses 993 200 1178."""
        self.assertIn("https://wa.me/529932001178", self.html)
        self.assertIn("993 200 1178", self.html)

    def test_gaviotas_in_app_js(self):
        """Verify BRANCHES.gaviotas phone and whatsapp in app.js."""
        self.assertIn('phone: "993 200 1178"', self.js)
        self.assertIn('whatsapp: "529932001178"', self.js)

    def test_header_selector_has_all_five_branches_and_click_handler(self):
        """Verify header select dropdown has all 5 options and openBranchSelectorDropdown handler."""
        for branch_key in ["delicias", "buenavista", "gaviotas", "hidalgo", "joem"]:
            self.assertIn(f'value="{branch_key}"', self.html)

        self.assertIn("openBranchSelectorDropdown", self.html)
        self.assertIn("openBranchSelectorDropdown", self.js)

    def test_no_familiar_confidential_terms_in_html(self):
        """Verify 'familiar' term is completely removed from public index.html."""
        self.assertNotIn("familiar", self.html.lower())

    # 4. SEARCH UX & REDIRECTION
    def test_search_form_and_submit_button_in_html(self):
        """Verify search is an accessible form with a dedicated submit button."""
        self.assertIn('<form role="search" id="catalog-search-form"', self.html)
        self.assertIn('id="search-submit-btn"', self.html)
        self.assertIn('triggerCatalogSearch()', self.html)

    def test_search_event_wiring_in_app_js(self):
        """Verify triggerCatalogSearch and event listeners in app.js."""
        self.assertIn("window.triggerCatalogSearch", self.js)
        self.assertIn("catalog-search-form", self.js)
        self.assertIn("search-submit-btn", self.js)
        self.assertIn('e.key === "Enter"', self.js)

    def test_search_submit_button_styles_in_css(self):
        """Verify styling for search-submit-btn and main-layout scroll-margin-top in styles.css."""
        self.assertIn(".search-submit-btn", self.css)
        self.assertIn("scroll-margin-top: 80px", self.css)

    # 5. PRODUCT IMAGES FROM ZIP & CATALOG
    def test_zip_product_images_exist_on_disk(self):
        """Verify that all 34 product images extracted from the zip exist on disk."""
        categories = ["royer", "baleros", "candados", "tornilleria"]
        total_files = 0
        for cat in categories:
            cat_dir = os.path.join(IMAGES_DIR, "products", cat)
            self.assertTrue(os.path.isdir(cat_dir), f"Missing directory: {cat_dir}")
            files = [f for f in os.listdir(cat_dir) if os.path.isfile(os.path.join(cat_dir, f))]
            total_files += len(files)
            self.assertGreater(len(files), 0, f"No files in {cat_dir}")

        self.assertEqual(total_files, 34, f"Expected 34 images from ZIP, found {total_files}")

    def test_all_catalog_image_paths_exist(self):
        """Verify that EVERY image path referenced in products.json physically exists on disk."""
        checked = set()
        missing = []
        for p in self.products:
            for field in ["image", "image_url"]:
                rel_path = p.get(field)
                if rel_path and rel_path not in checked:
                    checked.add(rel_path)
                    full_path = os.path.join(PROJECT_ROOT, rel_path)
                    if not os.path.isfile(full_path):
                        missing.append(rel_path)

        self.assertEqual(len(missing), 0, f"Found broken image paths in products.json: {missing[:10]}")

    def test_over_1500_products_have_new_zip_images(self):
        """Verify that > 1,500 products in products.json have received the authentic images from ZIP."""
        matched = 0
        for p in self.products:
            img = p.get("image", "")
            if any(k in img for k in ["/royer/", "/baleros/", "/candados/", "/tornilleria/"]):
                matched += 1

        self.assertGreater(matched, 1500, f"Expected > 1500 products with authentic images, got {matched}")

    # 6. SUCURSAL 5 (JOEM)
    def test_fifth_branch_joem_image_and_properties(self):
        """Verify Joem storefront image exists, is WebP, >= 800px wide, < 250 KB."""
        img_path = os.path.join(IMAGES_DIR, "branches", "fachada-joem.webp")
        self.assertTrue(os.path.isfile(img_path), "Missing fachada-joem.webp")
        size_kb = os.path.getsize(img_path) / 1024
        self.assertLess(size_kb, 250, f"fachada-joem.webp is too large: {size_kb:.1f} KB")
        with Image.open(img_path) as im:
            self.assertGreaterEqual(im.width, 800)
            self.assertEqual(im.format, "WEBP")

    def test_fifth_branch_joem_in_js_and_html(self):
        """Verify Joem branch in app.js and index.html with confidentiality and maps URL."""
        self.assertIn("joem:", self.js)
        self.assertIn("https://maps.app.goo.gl/y2qguKEAUhhGPpfw5", self.js)
        self.assertIn("https://maps.app.goo.gl/y2qguKEAUhhGPpfw5", self.html)
        self.assertIn('data-branch-id="joem"', self.html)
        self.assertIn('id="drawer-card-joem"', self.html)

        # Confirm manager name is in JS but strictly confidential in HTML branch section
        self.assertIn('"Salomón Méndez"', self.js)
        joem_card_match = re.search(r'<article[^>]+data-branch-id="joem".*?</article>', self.html, re.DOTALL)
        self.assertIsNotNone(joem_card_match, "Joem card not found in index.html")
        joem_card = joem_card_match.group(0)
        self.assertNotIn("Salomón", joem_card)
        self.assertNotIn("Méndez", joem_card)

    # 7. RECENT USER REFINEMENTS (AUDIT COMPLIANCE)
    def test_no_solo_mensajes_anywhere(self):
        """Verify that 'Solo Mensajes' has been 100% eliminated from index.html and app.js."""
        self.assertNotIn("solo mensajes", self.html.lower(), "Found 'solo mensajes' in index.html")
        self.assertNotIn("solo mensajes", self.js.lower(), "Found 'solo mensajes' in app.js")

    def test_no_whatsapp_central_anywhere(self):
        """Verify that 'WhatsApp Central' has been 100% eliminated from index.html and app.js."""
        self.assertNotIn("whatsapp central", self.html.lower(), "Found 'whatsapp central' in index.html")
        self.assertNotIn("whatsapp central", self.js.lower(), "Found 'whatsapp central' in app.js")

    def test_hidalgo_branch_official_phone_number(self):
        """Verify Miguel Hidalgo III Etapa branch phone number is strictly 993 141 2679 and old number 2755 is gone."""
        self.assertNotIn("993 141 2755", self.html, "Found obsolete phone 993 141 2755 in index.html")
        self.assertNotIn("993 141 2755", self.js, "Found obsolete phone 993 141 2755 in app.js")
        self.assertNotIn("529931412755", self.html)
        self.assertNotIn("529931412755", self.js)
        self.assertIn("993 141 2679", self.html)
        self.assertIn("+529931412679", self.html)
        self.assertIn('phone: "993 141 2679"', self.js)
        self.assertIn('whatsapp: "529931412679"', self.js)

    def test_joem_branch_no_fake_phone_and_informative_handling(self):
        """Verify Joem has no fabricated phone number or WhatsApp in app.js, and graceful handling in UI."""
        self.assertIn('noWhatsApp: true', self.js)
        self.assertIn('whatsapp: ""', self.js)
        self.assertIn('Mostrador Presencial', self.html)

    def test_drawer_grid_layout_and_dimensions(self):
        """Verify quote drawer has 520px width and drawer-branch-options-grid uses minmax(0, 1fr) with joem spanning."""
        self.assertIn("width: 520px;", self.css)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr));", self.css)
        self.assertIn("#drawer-card-joem {\n  grid-column: 1 / -1;\n}", self.css)


if __name__ == "__main__":
    unittest.main()
