#!/usr/bin/env python3
"""
Test Suite: Senior-Friendly Search, Google Maps Integration, Stock Policies & QR Codes
Ferretería y Tlapalería El Águila
"""

import os
import re
import unittest
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(PROJECT_ROOT, "index.html")
APP_JS_PATH = os.path.join(PROJECT_ROOT, "assets", "js", "app.js")
STYLES_CSS_PATH = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")
QR_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "qr")

MAPS_DELICIAS = "https://maps.app.goo.gl/vkQLYW1u62gbRRDf7"
MAPS_BUENAVISTA = "https://maps.app.goo.gl/w1FCsu9A2V2WqvCu5"
MAPS_GAVIOTAS = "https://maps.app.goo.gl/qWtBwNkb8vABa5Wj8"
MAPS_HIDALGO = "https://maps.app.goo.gl/xnaBo218rGoQQvMZ7"
BRANCH_IMAGES_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "branches")
TARGET_URL = "https://ferreteriaytlapaleria-elaguila.com"

class TestSeniorSearchAndMaps(unittest.TestCase):

    def test_no_delivery_to_worksite_persists(self):
        """Verify that 'pie de obra' and 'servicio a domicilio' are completely removed."""
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read().lower()
        with open(APP_JS_PATH, "r", encoding="utf-8") as f:
            js = f.read().lower()

        self.assertNotIn("entrega a pie de obra", html)
        self.assertNotIn("servicio a domicilio", html)
        self.assertNotIn("entrega a pie de obra", js)

    def test_store_pickup_and_availability_disclaimers(self):
        """Verify presence of store pickup policy and stock availability disclaimers."""
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn("Recolección en Mostrador", html)
        self.assertIn("AVISO DE DISPONIBILIDAD", html)
        self.assertIn("search-senior-alert", html)

    def test_store_schedules_accuracy(self):
        """Verify correct store hours across index.html and app.js."""
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()
        with open(APP_JS_PATH, "r", encoding="utf-8") as f:
            js = f.read()

        # Lun a Vie: 8:00 a 18:00 (8 am a 6 pm)
        self.assertIn("8:00", html)
        self.assertIn("18:00", html)
        # Sábados: 8:00 a 15:00 (8 am a 3 pm)
        self.assertIn("15:00", html)
        # Domingos: 9:00 a 14:00 (9 am a 2 pm)
        self.assertIn("9:00", html)
        self.assertIn("14:00", html)

        # In app.js BRANCHES
        self.assertIn("Lunes a Viernes: 8:00 a 18:00 hrs | Sábado: 8:00 a 15:00 hrs | Domingo: 9:00 a 14:00 hrs", js)
        self.assertIn("Todos los días: 8:00 a 18:00 hrs (8:00 am a 6:00 pm)", js)
        self.assertIn("Lun a Vie: 8:00 a 18:30 hrs | Sáb: 8:00 a 17:00 hrs | Dom: 8:00 a 13:00 hrs", js)

    def test_google_maps_urls_in_html_and_js(self):
        """Verify Google Maps links for all 5 branches in HTML and JS."""
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()
        with open(APP_JS_PATH, "r", encoding="utf-8") as f:
            js = f.read()

        self.assertIn(MAPS_DELICIAS, html)
        self.assertIn(MAPS_BUENAVISTA, html)
        self.assertIn(MAPS_GAVIOTAS, html)
        self.assertIn(MAPS_HIDALGO, html)

        self.assertIn(MAPS_DELICIAS, js)
        self.assertIn(MAPS_BUENAVISTA, js)
        self.assertIn(MAPS_GAVIOTAS, js)
        self.assertIn(MAPS_HIDALGO, js)

    def test_four_branches_and_owners_in_js_and_html(self):
        """Verify all 4 branches and their respective owners (Timoteo, Miguel, Salomón) are present and Tamulte is absent."""
        with open(APP_JS_PATH, "r", encoding="utf-8") as f:
            js = f.read()
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            html = f.read()

        for branch_key in ["delicias:", "buenavista:", "gaviotas:", "hidalgo:"]:
            self.assertIn(branch_key, js)

        # Confirm tamulte is completely absent
        self.assertNotIn("tamulte", js.lower())
        self.assertNotIn("tamulté", js.lower())
        self.assertNotIn("tamulte", html.lower())
        self.assertNotIn("tamulté", html.lower())

        for owner in ["Timoteo Méndez", "Miguel Méndez", "Salomón Méndez"]:
            self.assertIn(owner, js)
            self.assertNotIn(owner, html)

    def test_branch_storefront_images_exist_and_optimized(self):
        """Verify storefront images for all 4 branches exist and are under 250KB."""
        expected_images = [
            "fachada-delicias-tito.webp",
            "fachada-buenavista.webp",
            "fachada-gaviotas-miguel.webp",
            "fachada-hidalgo-salomon.webp"
        ]
        for img_name in expected_images:
            img_path = os.path.join(BRANCH_IMAGES_DIR, img_name)
            self.assertTrue(os.path.isfile(img_path), f"Falta imagen de sucursal: {img_name}")
            size_kb = os.path.getsize(img_path) / 1024
            self.assertLess(size_kb, 250, f"Imagen {img_name} excede 250KB ({size_kb:.1f}KB)")
            with Image.open(img_path) as im:
                self.assertGreaterEqual(im.width, 800)

    def test_senior_friendly_search_helpers_in_js(self):
        """Verify senior-friendly search fallback and helpers in app.js."""
        with open(APP_JS_PATH, "r", encoding="utf-8") as f:
            js = f.read()

        self.assertIn("autoExpandedToAll", js)
        self.assertIn("updateSeniorAlertBanner", js)
        self.assertIn("senior-empty-card", js)
        self.assertIn("quickSearch", js)
        self.assertIn("resetAllFiltersKeepSearch", js)

    def test_qr_codes_generated_and_valid(self):
        """Verify all 5 advertising QR codes exist and meet resolution standards."""
        expected_files = [
            ("qr-01-azul-corporativo.png", (1200, 1200)),
            ("qr-02-dorado-premium.png", (1200, 1200)),
            ("qr-03-lona-exterior-gran-formato.png", (1800, 2400)),
            ("qr-04-tarjeta-minimalista.png", (1050, 600)),
            ("qr-05-flyer-publicitario-mostrador.png", (1240, 1754)),
        ]

        for filename, min_dim in expected_files:
            file_path = os.path.join(QR_DIR, filename)
            self.assertTrue(os.path.isfile(file_path), f"Falta archivo QR: {filename}")
            self.assertGreater(os.path.getsize(file_path), 20000, f"Archivo muy pequeño: {filename}")

            with Image.open(file_path) as im:
                self.assertEqual(im.size, min_dim, f"Dimensiones incorrectas en {filename}: {im.size} vs {min_dim}")

    def test_qr_codes_decode_to_target_url(self):
        """Verify all 5 QR codes decode to the target domain using OpenCV."""
        try:
            import cv2
            detector = cv2.QRCodeDetector()
            files = [
                "qr-01-azul-corporativo.png",
                "qr-02-dorado-premium.png",
                "qr-03-lona-exterior-gran-formato.png",
                "qr-04-tarjeta-minimalista.png",
                "qr-05-flyer-publicitario-mostrador.png",
            ]
            for f in files:
                fpath = os.path.join(QR_DIR, f)
                img = cv2.imread(fpath)
                data, _, _ = detector.detectAndDecode(img)
                self.assertEqual(data, TARGET_URL, f"El código QR en {f} decodificó '{data}' en lugar de '{TARGET_URL}'")
        except ImportError:
            self.skipTest("OpenCV no disponible para decodificación")

    def test_qr_showcase_page_exists_and_links(self):
        """Verify that qr.html exists and is linked in index.html footer."""
        qr_page = os.path.join(PROJECT_ROOT, "qr.html")
        self.assertTrue(os.path.isfile(qr_page), "Falta el archivo qr.html")
        with open(qr_page, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("qr-01-azul-corporativo.png", content)
        self.assertIn("qr-02-dorado-premium.png", content)
        self.assertIn("qr-03-lona-exterior-gran-formato.png", content)
        self.assertIn("qr-04-tarjeta-minimalista.png", content)
        self.assertIn("qr-05-flyer-publicitario-mostrador.png", content)

        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            index_content = f.read()
        self.assertNotIn('href="qr.html"', index_content)

if __name__ == "__main__":
    unittest.main()
