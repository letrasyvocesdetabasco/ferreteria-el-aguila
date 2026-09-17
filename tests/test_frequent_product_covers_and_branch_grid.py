#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for the 15 most frequent products cover images and 4-column branch layout.
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

    def test_products_json_has_updated_product_covers(self):
        """Verify thousands of products in data/products.json have been updated with real product covers."""
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            products = json.load(f)

        self.assertEqual(len(products), 17641)

        counts = {item: 0 for item in FREQUENT_15}
        for p in products:
            img = p.get("image", "")
            for item in FREQUENT_15:
                if f"prod-{item}.webp" in img:
                    counts[item] += 1

        total_with_new_covers = sum(counts.values())
        self.assertGreater(total_with_new_covers, 5000, f"Expected > 5000 updated products, got {total_with_new_covers}")

        # Ensure every single one of the 15 types has at least 100 products
        for item, count in counts.items():
            self.assertGreater(count, 100, f"Expected > 100 products for {item}, got {count}")

    def test_app_js_has_image_resolver(self):
        """Verify app.js includes resolveProductImage and all 15 product patterns."""
        with open(APP_JS, "r", encoding="utf-8") as f:
            js = f.read()

        self.assertIn("resolveProductImage", js)
        for item in FREQUENT_15:
            self.assertIn(f"prod-{item}.webp", js)

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

        # Extract branches section
        branch_section_match = re.search(r'<section id="branches-section".*?</section>', html, re.DOTALL)
        self.assertIsNotNone(branch_section_match, "branches-section not found in index.html")
        branch_section = branch_section_match.group(0)

        for confidential in ["Timoteo", "Tito", "Salomón", "Miguel Méndez"]:
            self.assertNotIn(confidential, branch_section, f"Confidential name '{confidential}' found in branches section!")


if __name__ == "__main__":
    unittest.main()
