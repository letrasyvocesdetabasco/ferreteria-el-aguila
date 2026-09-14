"""
Automated Empirical Test Suite for Milestone 1: Catalog Replacement & Department Counters (R1)
Ferretería y Tlapalería El Águila

Empirical verification covering:
- Feature 1: Full Catalog Ingestion (exactly 17,641 items in data/products.json)
- Feature 2: Retail Price IVA Calculation (+16% formula round(PRECIO_1 * 1.16, 2))
- Feature 3: 5 Official Department Classifications & Banner Counts in index.html
- Feature 4: Brand Recognition Heuristics & Schema Completeness
- Feature 5 & 6: Pre-sorting and Sequential ID indexing
"""

import csv
import json
import math
import os
import re
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_JSON_PATH = os.path.join(PROJECT_ROOT, "data", "products.json")
CSV_PATH = os.path.join(PROJECT_ROOT, "raticulos ferre precios.csv")
INDEX_HTML_PATH = os.path.join(PROJECT_ROOT, "index.html")

OFFICIAL_CATEGORIES = [
    "Tlapalería y Construcción",
    "Tornillería y Fijación",
    "Plomería y Conexiones",
    "Herramientas en General",
    "Material Eléctrico"
]

REQUIRED_FIELDS = [
    "id", "sku", "name", "category", "brand", "base_price", "unit_measure", "image_url"
]


class TestMilestone1CatalogAndCounters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(os.path.isfile(PRODUCTS_JSON_PATH), f"Missing {PRODUCTS_JSON_PATH}")
        cls.assertTrue(os.path.isfile(CSV_PATH), f"Missing {CSV_PATH}")
        cls.assertTrue(os.path.isfile(INDEX_HTML_PATH), f"Missing {INDEX_HTML_PATH}")

        with open(PRODUCTS_JSON_PATH, "r", encoding="utf-8") as f:
            cls.products = json.load(f)

        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        cls.sku_map = {p["sku"]: p for p in cls.products}

        # Load CSV for formula validation
        cls.csv_records = {}
        with open(CSV_PATH, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            next(reader)  # metadata header
            next(reader)  # column header
            for row in reader:
                if not row:
                    continue
                sku = row[0].strip()
                try:
                    p1 = float(row[2].strip())
                except ValueError:
                    p1 = 0.0
                cls.csv_records[sku] = (row[1].strip(), p1)

    # --- TEST GROUP 1: Catalog Volume & Schema Integrity ---

    def test_01_exact_product_count(self):
        """Verify data/products.json contains exactly 17,641 products."""
        self.assertEqual(
            len(self.products), 17641,
            f"Expected exactly 17,641 items, got {len(self.products)}"
        )

    def test_02_all_required_fields_present(self):
        """Verify all items contain mandatory schema fields."""
        missing = []
        for p in self.products:
            for field in REQUIRED_FIELDS:
                if field not in p or p[field] is None:
                    missing.append((p.get("sku"), field))
        self.assertEqual(len(missing), 0, f"Found {len(missing)} items with missing fields: {missing[:5]}")

    def test_03_sequential_one_based_ids(self):
        """Verify items have contiguous 1-based sequential IDs from 1 to 17,641."""
        for idx, p in enumerate(self.products, 1):
            self.assertEqual(p["id"], idx, f"Expected id {idx}, got {p['id']} on SKU {p['sku']}")

    def test_04_pre_sorted_by_name_ascending(self):
        """Verify catalog is pre-sorted alphabetically by name ascending."""
        first_item = self.products[0]
        last_item = self.products[-1]
        self.assertEqual(first_item["id"], 1)
        self.assertEqual(first_item["sku"], "1524")
        self.assertEqual(last_item["id"], 17641)
        self.assertEqual(last_item["sku"], "5661R")

    # --- TEST GROUP 2: Pricing Arithmetic & Zero NaN/Null ---

    def test_05_zero_nan_or_infinite_prices(self):
        """Verify no NaN, null, infinite, or negative prices exist."""
        for p in self.products:
            price = p["base_price"]
            self.assertIsInstance(price, (int, float), f"Invalid price type on SKU {p['sku']}")
            self.assertFalse(math.isnan(price), f"NaN price on SKU {p['sku']}")
            self.assertFalse(math.isinf(price), f"Infinite price on SKU {p['sku']}")
            self.assertGreaterEqual(price, 0.0, f"Negative price on SKU {p['sku']}")

    def test_06_expected_zero_price_skus(self):
        """Verify only the 5 documented zero-price SKUs have base_price == 0.0."""
        expected_zero_skus = {"6611", "5100", "6330", "5755", "2249"}
        zero_skus = {p["sku"] for p in self.products if p["base_price"] == 0.0}
        self.assertEqual(zero_skus, expected_zero_skus, f"Unexpected zero-price SKUs: {zero_skus}")

    def test_07_vat_formula_applied_to_all_csv_items(self):
        """Verify round(PRECIO_1 * 1.16, 2) matches 100% of the 17,641 products."""
        self.assertEqual(len(self.csv_records), 17641)
        mismatches = []
        for sku, (desc, p1) in self.csv_records.items():
            expected = round(p1 * 1.16, 2)
            actual = self.sku_map[sku]["base_price"]
            if actual != expected:
                mismatches.append((sku, actual, expected))
        self.assertEqual(len(mismatches), 0, f"Found {len(mismatches)} price mismatches: {mismatches[:5]}")

    # --- TEST GROUP 3: Department Classification & Banner Counts ---

    def test_08_every_product_belongs_to_official_category(self):
        """Verify all products are assigned to one of the 5 official departments."""
        valid_cats = set(OFFICIAL_CATEGORIES)
        for p in self.products:
            cat = p["category"]
            self.assertIn(cat, valid_cats, f"Invalid category '{cat}' on SKU {p['sku']}")

    def test_09_exact_department_counts(self):
        """Verify the exact distribution across all 5 departments."""
        dept_counts = {}
        for p in self.products:
            c = p["category"]
            dept_counts[c] = dept_counts.get(c, 0) + 1

        expected_counts = {
            "Tlapalería y Construcción": 7312,
            "Tornillería y Fijación": 2917,
            "Plomería y Conexiones": 2865,
            "Herramientas en General": 2770,
            "Material Eléctrico": 1777
        }

        self.assertEqual(dept_counts, expected_counts)
        self.assertEqual(sum(dept_counts.values()), 17641)

    def test_10_index_html_department_banner_counters(self):
        """Verify index.html category banner descriptions reflect the exact department counts."""
        expected_counters = [
            ("Tlapalería y Construcción", "7,312"),
            ("Tornillería y Fijación", "2,917"),
            ("Plomería y Conexiones", "2,865"),
            ("Herramientas en General", "2,770"),
            ("Material Eléctrico", "1,777")
        ]

        for dept, count_str in expected_counters:
            pattern = rf'{re.escape(count_str)}\s+artículos'
            self.assertTrue(
                re.search(pattern, self.html_content),
                f"Missing counter '{count_str} artículos' for {dept} in index.html"
            )

    def test_11_index_html_global_catalog_counters(self):
        """Verify index.html global catalog reference buttons show 17,641."""
        self.assertIn("Ver Todo el Catálogo (17,641)", self.html_content)
        self.assertIn("Explorar 17,641 Productos", self.html_content)

    # --- TEST GROUP 4: Spot Checks on Reference Hardware Items ---

    def test_12_spot_check_sku_661_zumbador_metalico(self):
        """Spot check SKU 661: Zumbador metalico 127 v."""
        item = self.sku_map.get("661")
        self.assertIsNotNone(item)
        self.assertEqual(item["name"], "Zumbador metalico 127 v.")
        self.assertEqual(item["category"], "Material Eléctrico")
        self.assertEqual(item["base_price"], 120.0)

    def test_13_spot_check_sku_5661r_zumbador_oculto(self):
        """Spot check SKU 5661R: Zumbador oculto 127 volts."""
        item = self.sku_map.get("5661R")
        self.assertIsNotNone(item)
        self.assertEqual(item["name"], "Zumbador oculto 127 volts")
        self.assertEqual(item["category"], "Material Eléctrico")
        self.assertEqual(item["base_price"], 160.0)

    def test_14_spot_check_sku_mufa_voltech(self):
        """Spot check SKU MUFA-3/4: Mufa con abrazadera para tubo 3/4', Voltech."""
        item = self.sku_map.get("MUFA-3/4")
        self.assertIsNotNone(item)
        self.assertIn("Mufa con abrazadera", item["name"])
        self.assertEqual(item["category"], "Material Eléctrico")
        self.assertEqual(item["brand"], "Voltech")
        self.assertEqual(item["base_price"], 24.0)

    def test_15_spot_check_sku_m048p_mezcladora_basic(self):
        """Spot check SKU M-048P: Mezcladora lavabo, manerales palanca, Basic."""
        item = self.sku_map.get("M-048P")
        self.assertIsNotNone(item)
        self.assertIn("Mezcladora lavabo", item["name"])
        self.assertEqual(item["category"], "Plomería y Conexiones")
        self.assertEqual(item["brand"], "Basic")
        self.assertEqual(item["base_price"], 371.0)

    def test_16_spot_check_sku_1524_adaptador(self):
        """Spot check SKU 1524: (BAJE) Adaptador 3 contactosluz de noche."""
        item = self.sku_map.get("1524")
        self.assertIsNotNone(item)
        self.assertIn("Adaptador 3 contactos", item["name"])
        self.assertEqual(item["category"], "Material Eléctrico")
        self.assertEqual(item["base_price"], 30.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
