#!/usr/bin/env python3
import os
import unittest
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestMilestone3And4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index_path = os.path.join(PROJECT_ROOT, "index.html")
        cls.css_path = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")
        cls.js_path = os.path.join(PROJECT_ROOT, "assets", "js", "app.js")
        with open(cls.index_path, "r", encoding="utf-8") as f:
            cls.index_html = f.read()
        with open(cls.css_path, "r", encoding="utf-8") as f:
            cls.styles_css = f.read()
        with open(cls.js_path, "r", encoding="utf-8") as f:
            cls.app_js = f.read()

    def test_01_logo_files_exist_and_valid(self):
        files = [
            "assets/images/logo-aguila.png",
            "assets/images/logo-aguila-gold.png",
            "assets/images/logo-aguila.svg",
            "assets/images/favicon.png",
            "favicon.ico"
        ]
        for rel in files:
            p = os.path.join(PROJECT_ROOT, rel)
            self.assertTrue(os.path.exists(p), f"File {rel} must exist")
            self.assertGreater(os.path.getsize(p), 100, f"File {rel} must not be empty")

    def test_02_logo_png_dimensions_and_transparency(self):
        p = os.path.join(PROJECT_ROOT, "assets", "images", "logo-aguila.png")
        with Image.open(p) as img:
            self.assertEqual(img.size, (512, 512))
            self.assertEqual(img.mode, "RGBA")

    def test_03_brand_badge_uses_official_logo(self):
        self.assertIn("logo-aguila.png", self.index_html)
        self.assertNotIn('<div class="brand-badge-logo">🦅</div>', self.index_html)

    def test_04_favicon_links_present_in_head(self):
        self.assertRegex(self.index_html, r"<link\s+rel=\"icon\"[^>]+favicon")

    def test_05_css_has_brand_logo_img_class(self):
        self.assertIn(".brand-logo-img", self.styles_css)
        self.assertIn("object-fit: contain", self.styles_css)

    def test_06_two_branches_configured_in_js(self):
        self.assertIn("delicias", self.app_js)
        self.assertIn("buenavista", self.app_js)
        self.assertIn("9932892935", self.app_js)
        self.assertIn("9931928313", self.app_js)

    def test_07_branch_selector_in_html(self):
        self.assertIn('value="delicias"', self.index_html)
        self.assertIn('value="buenavista"', self.index_html)
        self.assertIn("Av. Revolución 1203", self.index_html)
        self.assertIn("Carr. Villahermosa a La Isla Km 5.300", self.index_html)

    def test_08_whatsapp_dispatch_flow(self):
        self.assertIn("whatsapp", self.app_js.lower())
        self.assertIn("encodeURIComponent", self.app_js)

if __name__ == "__main__":
    unittest.main()
