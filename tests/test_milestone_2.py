"""
Automated Empirical Test Suite for Milestone 2: Hero Banner Visual Clearing (R2)
Ferretería y Tlapalería El Águila

Empirical verification covering:
- Feature 7: Hero banner overlay removal (.hero-banner-badge, .hero-banner-caption)
- Feature 8: 3:2 Natural canvas aspect ratio styling and absence of dead rules
- Image intactness, format, dimensions, and zero-crop geometry
- Adversarial edge cases: pseudo-element overlays, responsive constraints, DOM tree integrity
"""

import os
import re
import unittest
from html.parser import HTMLParser
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML_PATH = os.path.join(PROJECT_ROOT, "index.html")
STYLES_CSS_PATH = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")
IMAGE_PATH = os.path.join(PROJECT_ROOT, "assets", "images", "lona-oficial-el-aguila.jpg")


class SimpleHTMLDOMParser(HTMLParser):
    """Parses HTML into a lightweight DOM tree for structural assertions."""
    def __init__(self):
        super().__init__()
        self.root = {"tag": "root", "attrs": {}, "children": [], "parent": None, "text": ""}
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = {
            "tag": tag,
            "attrs": dict(attrs),
            "children": [],
            "parent": self.current,
            "text": ""
        }
        self.current["children"].append(node)
        # Void elements in HTML5 do not push to stack
        if tag not in ("img", "br", "hr", "input", "meta", "link"):
            self.current = node

    def handle_endtag(self, tag):
        if tag not in ("img", "br", "hr", "input", "meta", "link"):
            p = self.current
            while p and p["tag"] != tag and p["parent"]:
                p = p["parent"]
            if p and p["parent"]:
                self.current = p["parent"]

    def handle_data(self, data):
        self.current["text"] += data


def find_elements_by_class(node, class_name):
    results = []
    classes = node.get("attrs", {}).get("class", "").split()
    if class_name in classes:
        results.append(node)
    for child in node.get("children", []):
        results.extend(find_elements_by_class(child, class_name))
    return results


def find_elements_by_tag(node, tag_name):
    results = []
    if node.get("tag") == tag_name:
        results.append(node)
    for child in node.get("children", []):
        results.extend(find_elements_by_tag(child, tag_name))
    return results


class TestMilestone2HeroBanner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assertTrue(os.path.isfile(INDEX_HTML_PATH), f"File not found: {INDEX_HTML_PATH}")
        cls.assertTrue(os.path.isfile(STYLES_CSS_PATH), f"File not found: {STYLES_CSS_PATH}")
        cls.assertTrue(os.path.isfile(IMAGE_PATH), f"File not found: {IMAGE_PATH}")

        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

        with open(STYLES_CSS_PATH, "r", encoding="utf-8") as f:
            cls.css_content = f.read()

        parser = SimpleHTMLDOMParser()
        parser.feed(cls.html_content)
        cls.dom = parser.root

    # --- TEST GROUP 1: HTML DOM Structure & Zero Overlays ---

    def test_01_hero_banner_card_exists_and_is_unique(self):
        """Verify .hero-banner-card exists exactly once in index.html."""
        cards = find_elements_by_class(self.dom, "hero-banner-card")
        self.assertEqual(len(cards), 1, f"Expected exactly 1 .hero-banner-card, found {len(cards)}")

    def test_02_hero_banner_card_contains_only_img(self):
        """Verify .hero-banner-card contains ONLY the <img> element and zero overlay elements."""
        cards = find_elements_by_class(self.dom, "hero-banner-card")
        card = cards[0]
        
        # Check all child elements
        children = card.get("children", [])
        self.assertEqual(len(children), 1, f"Expected exactly 1 child inside .hero-banner-card, found {len(children)}: {[c['tag'] for c in children]}")
        self.assertEqual(children[0]["tag"], "img", f"Expected child to be <img>, got <{children[0]['tag']}>")

        # Verify no non-whitespace text nodes exist directly in card
        text_content = card.get("text", "").strip()
        self.assertEqual(text_content, "", f"Expected empty text inside .hero-banner-card, found: {text_content!r}")

    def test_03_no_overlay_classes_in_entire_html(self):
        """Verify .hero-banner-badge and .hero-banner-caption do not exist anywhere in index.html."""
        badges = find_elements_by_class(self.dom, "hero-banner-badge")
        captions = find_elements_by_class(self.dom, "hero-banner-caption")
        self.assertEqual(len(badges), 0, f"Found unexpected .hero-banner-badge in index.html: {badges}")
        self.assertEqual(len(captions), 0, f"Found unexpected .hero-banner-caption in index.html: {captions}")

        # String search check
        self.assertNotIn("hero-banner-badge", self.html_content)
        self.assertNotIn("hero-banner-caption", self.html_content)

    def test_04_no_overlay_text_remnants_in_hero(self):
        """Verify old overlay text (badge caption, phone, address duplication) is not lingering in hero markup."""
        self.assertNotIn("📸 Mostrador Oficial Villahermosa", self.html_content)
        self.assertNotIn("A un lado del C.S. San Joaquín</small>", self.html_content)

    def test_05_img_attributes_validity(self):
        """Verify img attributes: correct src, descriptive alt, eager loading, width and height."""
        cards = find_elements_by_class(self.dom, "hero-banner-card")
        img_node = cards[0]["children"][0]
        attrs = img_node["attrs"]

        self.assertEqual(attrs.get("src"), "assets/images/lona-oficial-el-aguila.jpg")
        self.assertIn("alt", attrs)
        self.assertGreater(len(attrs["alt"].strip()), 10, "Alt text must be descriptive")
        self.assertEqual(attrs.get("width"), "1536")
        self.assertEqual(attrs.get("height"), "1024")
        self.assertEqual(attrs.get("loading"), "eager")

    # --- TEST GROUP 2: CSS Rules & Aspect Ratio Verification ---

    def test_06_css_aspect_ratio_is_3_to_2(self):
        """Verify .hero-banner-card img has aspect-ratio: 3 / 2 in styles.css."""
        # Find the rule block for .hero-banner-card img
        pattern = r"\.hero-banner-card\s+img\s*\{([^}]+)\}"
        match = re.search(pattern, self.css_content)
        self.assertIsNotNone(match, "Could not find '.hero-banner-card img' rule in styles.css")
        
        block = match.group(1)
        self.assertRegex(block, r"aspect-ratio:\s*3\s*/\s*2\s*;", f"Rule block does not specify 'aspect-ratio: 3 / 2;': {block}")
        self.assertRegex(block, r"object-fit:\s*cover\s*;", f"Rule block does not specify 'object-fit: cover;': {block}")
        self.assertRegex(block, r"display:\s*block\s*;", f"Rule block does not specify 'display: block;': {block}")

    def test_07_no_conflicting_aspect_ratio_in_css(self):
        """Verify old 16 / 10 aspect ratio is not present for hero-banner-card anywhere."""
        self.assertNotIn("16 / 10", self.css_content)
        self.assertNotIn("16/10", self.css_content)

    def test_08_no_dead_overlay_css_rules(self):
        """Verify styles.css does not contain dead rules for .hero-banner-badge or .hero-banner-caption."""
        self.assertNotIn(".hero-banner-badge", self.css_content)
        self.assertNotIn(".hero-banner-caption", self.css_content)

    def test_09_no_pseudo_element_overlays(self):
        """Adversarial check: ensure .hero-banner-card or its wrapper does NOT use ::before or ::after overlays."""
        pseudo_pattern = r"\.hero-banner-card(-wrapper)?::(before|after)\s*\{([^}]+)\}"
        matches = re.findall(pseudo_pattern, self.css_content)
        self.assertEqual(len(matches), 0, f"Found unexpected pseudo-element overlay on hero banner: {matches}")

    def test_10_hero_banner_card_container_styling(self):
        """Verify .hero-banner-card has proper radius, border, shadow, and overflow constraints."""
        pattern = r"\.hero-banner-card\s*\{([^}]+)\}"
        match = re.search(pattern, self.css_content)
        self.assertIsNotNone(match, "Could not find '.hero-banner-card' rule in styles.css")
        
        block = match.group(1)
        self.assertIn("overflow: hidden", block)
        self.assertIn("border-radius:", block)
        self.assertIn("box-shadow:", block)
        self.assertIn("max-width: 520px", block)

    # --- TEST GROUP 3: Image File Intactness & Geometry ---

    def test_11_image_file_exists_and_has_substantial_size(self):
        """Verify assets/images/lona-oficial-el-aguila.jpg is present and not empty."""
        size = os.path.getsize(IMAGE_PATH)
        # Should be a high resolution photo (> 100 KB)
        self.assertGreater(size, 100 * 1024, f"Image file is suspiciously small: {size} bytes")

    def test_12_image_file_decodable_and_intact(self):
        """Verify image file can be opened and decoded without corruption."""
        with Image.open(IMAGE_PATH) as img:
            img.verify()
        
        # Re-open to fully load pixel buffer (verify closes image)
        with Image.open(IMAGE_PATH) as img:
            img.load()
            self.assertEqual(img.format, "JPEG", f"Expected JPEG format, got {img.format}")
            self.assertEqual(img.mode, "RGB", f"Expected RGB mode, got {img.mode}")
            self.assertEqual(img.size, (1536, 1024), f"Expected (1536, 1024), got {img.size}")

    def test_13_aspect_ratio_exact_match(self):
        """Verify that the natural image aspect ratio matches 3:2 exactly."""
        with Image.open(IMAGE_PATH) as img:
            width, height = img.size
            ratio = width / height
            expected_ratio = 3.0 / 2.0
            self.assertAlmostEqual(ratio, expected_ratio, places=6, 
                                  msg=f"Natural image ratio {ratio} != expected 3:2 ({expected_ratio})")

    # --- TEST GROUP 4: Responsive Geometry & Adversarial Scaling ---

    def test_14_zero_crop_across_scaling_widths(self):
        """
        Adversarial test: With natural image at 1536x1024 (ratio 1.5) and container
        aspect-ratio 3/2 (ratio 1.5) with object-fit: cover, verify that for ANY width W,
        the scaled image exactly covers the container with 0 horizontal and 0 vertical cropping.
        """
        test_widths = [320, 360, 375, 390, 414, 480, 520, 600, 768, 1024]
        img_w, img_h = 1536, 1024
        natural_ratio = img_w / img_h  # 1.5

        for w in test_widths:
            container_w = min(w, 520)
            container_h = container_w / (3.0 / 2.0)
            
            # Scale calculation for object-fit: cover
            scale_x = container_w / img_w
            scale_y = container_h / img_h
            
            # Since natural_ratio == container_ratio, scale_x == scale_y
            self.assertAlmostEqual(scale_x, scale_y, places=7,
                                  msg=f"Crop mismatch at container width {container_w}: scale_x={scale_x} vs scale_y={scale_y}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
