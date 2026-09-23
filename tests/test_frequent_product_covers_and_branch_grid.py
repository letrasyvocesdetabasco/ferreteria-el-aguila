#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for the 15 most frequent products cover images and 4-column branch layout.
Includes strict tests against false positives (e.g. plumbing valves/keys getting wrench images).
"""

import json
import os
import re
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_JSON = os.path.join(PROJECT_ROOT, "data", "products.json")
PRODUCTS_IMG_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products")
APP_JS = os.path.join(PROJECT_ROOT, "assets", "js", "app.js")
STYLES_CSS = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")
INDEX_HTML = os.path.join(PROJECT_ROOT, "index.html")

FREQUENT_15 = [
    "tornillo", "llave", "dado", "tuerca", "desarmador",
    "broca", "foco", "manguera", "pija", "pinza",
    "valvula", "extension", "candado", "cinta", "niple"
]


class TestFrequentProductsAndBranchGrid(unittest.TestCase):

    def test_all_15_product_images_exist_and_optimized(self):
        """Verify all 15 generated product cover images exist and are under 100 KB."""
        self.assertTrue(os.path.isdir(PRODUCTS_IMG_DIR), f"Missing dir {PRODUCTS_IMG_DIR}")
        for item in FREQUENT_15:
            filename = f"prod-{item}.webp"
            filepath = os.path.join(PRODUCTS_IMG_DIR, filename)
            self.assertTrue(os.path.isfile(filepath), f"Missing product image: {filename}")
            size_kb = os.path.getsize(filepath) / 1024
            self.assertLess(size_kb, 100, f"Image {filename} is too large ({size_kb:.1f} KB > 100 KB)")

    def test_strict_and_truthful_product_covers_in_products_json(self):
        """Verify products_json assigns product covers ONLY to true, verified products (2000+ items)."""
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            products = json.load(f)

        self.assertEqual(len(products), 17641)

        counts = {item: 0 for item in FREQUENT_15}
        for p in products:
            img = p.get("image", "")
            for item in FREQUENT_15:
                if f"prod-{item}.webp" in img or (item == "candado" and "candados" in img) or (item == "tornillo" and "tornilleria" in img):
                    counts[item] += 1

        total_with_covers = sum(counts.values())
        self.assertGreater(total_with_covers, 2500, f"Expected > 2500 strictly matched products, got {total_with_covers}")

        # Ensure every one of the 15 categories has authentic matching products
        for item, count in counts.items():
            self.assertGreater(count, 10, f"Expected at least 10 products for {item}, got {count}")

    def test_zero_false_positives_on_plumbing_valves_and_accessories(self):
        """Critical test: Ensure plumbing valves (llave hembra, llave de paso) do NOT have wrench images, clamps do not have bolt images, etc."""
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            products = json.load(f)

        for p in products:
            name = p.get("name", "").lower()
            img = p.get("image", "")
            cat = p.get("category", "")

            # 1. No plumbing valve or stopcock should have the mechanic wrench image
            if "valvula" in name or "llave hembra" in name or "llave de paso" in name or "llave mezcladora" in name or "llave angular" in name or "llave jardinera" in name:
                self.assertNotIn("prod-llave.webp", img, f"Plumbing valve '{p['name']}' incorrectly received wrench image: {img}")

            # 2. Clamps (abrazaderas) should not have the hex bolt image
            if "abrazadera" in name:
                self.assertNotIn("prod-tornillo.webp", img, f"Clamp '{p['name']}' incorrectly received bolt image: {img}")
                self.assertNotIn("prod-tuerca.webp", img, f"Clamp '{p['name']}' incorrectly received nut image: {img}")

            # 3. Welding machines (soldadoras) should not have the ratchet socket image
            if "soldadora" in name or "antorcha" in name:
                self.assertNotIn("prod-dado.webp", img, f"Welding item '{p['name']}' incorrectly received socket image: {img}")

            # 4. Plumbing extensions (p/lav, cespol) should not have the electrical extension cord image
            if "p/lav" in name or "cespol" in name or "fregadero" in name:
                self.assertNotIn("prod-extension.webp", img, f"Plumbing extension '{p['name']}' incorrectly received cord image: {img}")

            # 5. Saw blades should not have electrical tape image
            if "sierra" in name:
                self.assertNotIn("prod-cinta.webp", img, f"Saw item '{p['name']}' incorrectly received tape image: {img}")

    def test_app_js_has_image_resolver(self):
        """Verify app.js includes resolveProductImage with strict anti-false-positive filtering."""
        with open(APP_JS, "r", encoding="utf-8") as f:
            js = f.read()

        self.assertIn("resolveProductImage", js)
        for item in FREQUENT_15:
            self.assertIn(f"prod-{item}.webp", js)
        # Ensure exclusions exist in app.js
        self.assertIn("valvula|paso|hembra", js)
        self.assertIn("abrazadera|extractor", js)
        self.assertIn("soldadora|antorcha", js)

    def test_styles_css_restores_four_column_grid(self):
        """Verify styles.css uses repeat(4, 1fr) for desktop branches grid."""
        with open(STYLES_CSS, "r", encoding="utf-8") as f:
            css = f.read()

        self.assertIn("grid-template-columns: repeat(4, 1fr)", css)
        self.assertIn(".branches-grid-four", css)

    def test_no_confidential_owner_names_in_public_branch_cards(self):
        """Verify confidential owner names (Tito, Salomón, Miguel Méndez, Timoteo) are NOT present in index.html branch section."""
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            html = f.read()

        branch_section_match = re.search(r'<section id="branches-section".*?</section>', html, re.DOTALL)
        self.assertIsNotNone(branch_section_match, "branches-section not found in index.html")
        branch_section = branch_section_match.group(0)

        for confidential in ["Timoteo", "Tito", "Salomón", "Miguel Méndez"]:
            self.assertNotIn(confidential, branch_section, f"Confidential name '{confidential}' found in branches section!")


if __name__ == "__main__":
    unittest.main()
