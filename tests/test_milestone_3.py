"""
Automated Empirical Test Suite for Milestone 3: Eagle Logo & Brand Harmonization (R3)
Ferretería y Tlapalería El Águila

Empirical verification covering:
- Feature 9: Official eagle logo extraction, dimensions (512x512), RGBA mode, non-empty alpha
- Feature 10: Replacement of emoji 🦅 across markup, header/hero logo tags, and favicon links in <head>
- Feature 11: Brand palette harmonization in CSS variables and classes (#004b97, #0052a5, #ffcb05, #f59e0b)
- Structural integrity of index.html and assets/css/styles.css
"""

import os
import re
import unittest
from html.parser import HTMLParser
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML_PATH = os.path.join(PROJECT_ROOT, "index.html")
STYLES_CSS_PATH = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")
LOGO_PATH = os.path.join(PROJECT_ROOT, "assets", "images", "logo-aguila.png")
LOGO_GOLD_PATH = os.path.join(PROJECT_ROOT, "assets", "images", "logo-aguila-gold.png")
LOGO_NAVY_PATH = os.path.join(PROJECT_ROOT, "assets", "images", "logo-aguila-navy.png")
LOGO_WHITE_PATH = os.path.join(PROJECT_ROOT, "assets", "images", "logo-aguila-white.png")
FAVICON_PATH = os.path.join(PROJECT_ROOT, "assets", "images", "favicon.png")


class SimpleDOMParser(HTMLParser):
    """Minimal robust parser to traverse DOM elements in index.html."""
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.imgs = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tags.append((tag, attr_dict))
        if tag == "link":
            self.links.append(attr_dict)
        elif tag == "img":
            self.imgs.append(attr_dict)


class TestMilestone3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        self_project_root = PROJECT_ROOT
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            cls.html_content = f.read()
        with open(STYLES_CSS_PATH, "r", encoding="utf-8") as f:
            cls.css_content = f.read()

        cls.parser = SimpleDOMParser()
        cls.parser.feed(cls.html_content)

    def test_01_primary_logo_properties(self):
        """Verify assets/images/logo-aguila.png exists, is 512x512, RGBA, with genuine alpha channel."""
        self.assertTrue(os.path.isfile(LOGO_PATH), f"Missing primary logo: {LOGO_PATH}")
        with Image.open(LOGO_PATH) as img:
            self.assertEqual(img.size, (512, 512), f"Logo size should be 512x512, got {img.size}")
            self.assertEqual(img.mode, "RGBA", f"Logo mode must be RGBA, got {img.mode}")
            
            # Check transparency and non-empty alpha channel
            bands = img.split()
            self.assertEqual(len(bands), 4, "Image must have 4 bands (RGBA)")
            alpha = bands[3]
            bbox = alpha.getbbox()
            self.assertIsNotNone(bbox, "Alpha channel cannot be completely transparent/empty")
            
            # Verify optical centering: bounding box width and height must span significant portion
            min_x, min_y, max_x, max_y = bbox
            width = max_x - min_x
            height = max_y - min_y
            self.assertGreater(width, 300, f"Eagle width too small: {width}px")
            self.assertGreater(height, 300, f"Eagle height too small: {height}px")
            self.assertLess(max_x, 512, "Bounding box exceeds canvas width")
            self.assertLess(max_y, 512, "Bounding box exceeds canvas height")

    def test_02_logo_variants_integrity(self):
        """Verify complementary logo assets (gold, navy, white, favicon)."""
        variants = [LOGO_GOLD_PATH, LOGO_NAVY_PATH, LOGO_WHITE_PATH]
        for v_path in variants:
            self.assertTrue(os.path.isfile(v_path), f"Variant not found: {v_path}")
            with Image.open(v_path) as img:
                self.assertEqual(img.size, (512, 512))
                self.assertEqual(img.mode, "RGBA")
                self.assertIsNotNone(img.split()[3].getbbox())

        self.assertTrue(os.path.isfile(FAVICON_PATH), "favicon.png not found")
        with Image.open(FAVICON_PATH) as fav:
            self.assertEqual(fav.mode, "RGBA")
            self.assertGreaterEqual(fav.width, 32)
            self.assertGreaterEqual(fav.height, 32)

    def test_03_zero_eagle_emoji_in_index_html(self):
        """Verify zero occurrences of the 🦅 emoji remain in index.html."""
        count = self.html_content.count("🦅")
        self.assertEqual(count, 0, f"Found {count} instances of 🦅 in index.html, expected 0")

    def test_04_favicon_links_in_head(self):
        """Verify <head> contains official favicon and apple-touch-icon links."""
        favicon_links = [
            l for l in self.parser.links
            if "icon" in l.get("rel", "")
        ]
        self.assertGreater(len(favicon_links), 0, "No favicon link tags found in <head>")
        
        # Must reference logo-aguila.png as icon or apple-touch-icon
        hrefs = [l.get("href", "") for l in favicon_links]
        self.assertTrue(
            any("logo-aguila.png" in h for h in hrefs),
            f"Expected logo-aguila.png in favicon links, found {hrefs}"
        )
        
        # Verify apple-touch-icon exists
        apple_icons = [
            l for l in self.parser.links
            if l.get("rel") == "apple-touch-icon"
        ]
        self.assertGreater(len(apple_icons), 0, "apple-touch-icon link not found in head")
        self.assertIn("logo-aguila.png", apple_icons[0].get("href", ""))

    def test_05_header_eagle_logo(self):
        """Verify header contains official brand logo image."""
        header_imgs = [
            img for img in self.parser.imgs
            if "brand-logo-img" in img.get("class", "").split()
        ]
        self.assertEqual(len(header_imgs), 1, "Exactly one .brand-logo-img expected in header")
        img = header_imgs[0]
        self.assertEqual(img.get("src"), "assets/images/logo-aguila.png")
        self.assertIn("Logo Oficial", img.get("alt", ""))

    def test_06_hero_badge_eagle_logo(self):
        """Verify hero section badge contains official gold eagle logo."""
        hero_imgs = [
            img for img in self.parser.imgs
            if "hero-eagle-icon" in img.get("class", "").split() or "hero-tag-logo" in img.get("class", "").split()
        ]
        self.assertGreaterEqual(len(hero_imgs), 1, "Hero badge eagle logo image not found")
        img = hero_imgs[0]
        self.assertIn("logo-aguila-gold.png", img.get("src", ""))
        classes = img.get("class", "").split()
        self.assertIn("hero-eagle-icon", classes)
        self.assertIn("hero-tag-logo", classes)

    def test_07_css_brand_palette_variables(self):
        """Verify CSS contains Azul Eléctrico Mostrador and Oro Intenso variables."""
        # Azul Mostrador (#004b97 / #0052a5)
        self.assertIn("--azul-mostrador: #004b97", self.css_content)
        self.assertIn("--azul-mostrador-hover: #0052a5", self.css_content)
        
        # Oro Intenso (#ffcb05 / #f59e0b)
        self.assertIn("--oro-intenso: #ffcb05", self.css_content)
        self.assertIn("--oro-profundo: #f59e0b", self.css_content)
        self.assertIn("--accent-gold: #ffcb05", self.css_content)
        self.assertIn("--accent-gold-hover: #f59e0b", self.css_content)

    def test_08_css_logo_classes(self):
        """Verify styles.css defines .brand-logo-img and .hero-eagle-icon / .hero-tag-logo."""
        # .brand-logo-img rule
        self.assertIn(".brand-logo-img", self.css_content)
        self.assertRegex(self.css_content, r"\.brand-logo-img\s*\{[^}]*object-fit:\s*contain")

        # .hero-eagle-icon and .hero-tag-logo rule
        self.assertIn(".hero-eagle-icon", self.css_content)
        self.assertIn(".hero-tag-logo", self.css_content)
        self.assertRegex(self.css_content, r"(\.hero-eagle-icon|\.hero-tag-logo)[^{]*\{[^}]*object-fit:\s*contain")

    def test_09_css_button_color_harmonization(self):
        """Verify primary and interactive buttons use the harmonized corporate colors."""
        self.assertRegex(self.css_content, r"\.btn-quote-cart\s*\{[^}]*var\(--oro-intenso\)")
        self.assertRegex(self.css_content, r"\.btn-hero-primary\s*\{[^}]*var\(--oro-intenso\)")
        self.assertRegex(self.css_content, r"\.btn-add-to-quote\s*\{[^}]*var\(--oro-intenso\)")
        self.assertRegex(self.css_content, r"\.btn-load-more\s*\{[^}]*var\(--azul-mostrador\)")


if __name__ == "__main__":
    unittest.main()
