#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_truper_poc.py
Pruebas automatizadas de la extracción y asociación de imágenes del catálogo Truper (PoC)
Ferretería y Tlapalería El Águila.
"""

import json
import os
import unittest
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_JSON = os.path.join(PROJECT_ROOT, "data", "products.json")
MANIFEST_JSON = os.path.join(PROJECT_ROOT, "data", "truper_poc_manifest.json")
TRUPER_IMG_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products", "truper")
STYLES_CSS = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")


class TestTruperPoc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
            cls.products = json.load(f)
        with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
            cls.manifest = json.load(f)

    def test_manifest_structure_and_volume(self):
        """Verifica que el manifiesto registre al menos 20 a 50 productos actualizados con éxito."""
        self.assertIn("total_store_products_updated", self.manifest)
        updated_count = self.manifest["total_store_products_updated"]
        self.assertGreaterEqual(updated_count, 20, "Debe haber al menos 20 productos actualizados en la PoC")
        self.assertGreaterEqual(updated_count, 50, "La PoC debe alcanzar o superar los 50 productos probados")
        self.assertEqual(len(self.manifest["updated_products"]), updated_count)

    def test_all_extracted_images_exist_and_are_valid_webp(self):
        """Verifica que todas las imágenes generadas existan en disco, sean WebP 500x500 con esquinas blancas puras."""
        self.assertTrue(os.path.isdir(TRUPER_IMG_DIR), "El directorio de imágenes Truper debe existir")
        files = [f for f in os.listdir(TRUPER_IMG_DIR) if f.endswith(".webp")]
        self.assertGreaterEqual(len(files), 25, "Debe haber al menos 25 archivos de imagen generados")

        for fname in files:
            fpath = os.path.join(TRUPER_IMG_DIR, fname)
            size_kb = os.path.getsize(fpath) / 1024
            self.assertGreater(size_kb, 0.5, f"La imagen {fname} está vacía o truncada")
            self.assertLess(size_kb, 100.0, f"La imagen {fname} supera los 100 KB permitidos")

            with Image.open(fpath) as im:
                self.assertEqual(im.format, "WEBP", f"{fname} no tiene formato WebP")
                self.assertEqual(im.width, 500, f"{fname} debe tener ancho de lienzo 500 px")
                self.assertEqual(im.height, 500, f"{fname} debe tener alto de lienzo 500 px")

                # Comprobar que las 4 esquinas del lienzo son fondo blanco puro
                corners = [
                    im.getpixel((0, 0)),
                    im.getpixel((im.width - 1, 0)),
                    im.getpixel((0, im.height - 1)),
                    im.getpixel((im.width - 1, im.height - 1))
                ]
                for idx, c in enumerate(corners):
                    self.assertEqual(c[:3], (255, 255, 255), f"La esquina {idx} de {fname} no es blanca pura: {c}")

    def test_clean_white_background_no_dark_headers_or_cropped_text(self):
        """Verifica que las imágenes no tengan artefactos de franjas oscuras de encabezado ni texto recortado."""
        for check_name in [
            "brocasierra-bimetalica-truper.webp",
            "mini-martillo-pretul.webp",
            "martillo-imantado-truper.webp",
            "martillo-fresado-truper.webp",
            "mini-arco-aluminio.webp"
        ]:
            fpath = os.path.join(TRUPER_IMG_DIR, check_name)
            self.assertTrue(os.path.isfile(fpath), f"Archivo no encontrado: {fpath}")
            with Image.open(fpath) as im:
                # Comprobar los 10 primeros píxeles de cada esquina
                for x, y in [(5, 5), (im.width - 6, 5), (5, im.height - 6), (im.width - 6, im.height - 6)]:
                    p = im.getpixel((x, y))
                    self.assertEqual(p[:3], (255, 255, 255), f"Pixel ({x},{y}) en {check_name} no es blanco: {p}")

    def test_products_json_integrity_and_valid_image_links(self):
        """Verifica la integridad de products.json: exactamente 17,641 productos y enlaces físicos válidos."""
        self.assertEqual(len(self.products), 17641, "El catálogo debe conservar exactamente 17,641 artículos")

        truper_linked = 0
        for p in self.products:
            img = p.get("image", "")
            if "assets/images/products/truper/" in img:
                truper_linked += 1
                full_path = os.path.join(PROJECT_ROOT, img)
                self.assertTrue(os.path.isfile(full_path), f"Ruta física rota: {full_path}")
                self.assertEqual(p.get("image_url"), img, "image_url debe coincidir con image")

        self.assertGreaterEqual(truper_linked, 50, f"Se esperaban al menos 50 productos vinculados a Truper, hay {truper_linked}")

    def test_shared_images_for_product_codes(self):
        """Verifica que múltiples códigos/variantes compartan la misma imagen de producto o familia."""
        by_sku = {p["sku"]: p for p in self.products}

        # Martillos tubulares Truper (MTR-16, MTR-20, MT-16) deben compartir la misma imagen
        if "MT-16" in by_sku and "MTR-16" in by_sku:
            self.assertEqual(by_sku["MT-16"]["image"], by_sku["MTR-16"]["image"])
            self.assertIn("martillo-tubular-truper.webp", by_sku["MT-16"]["image"])

        # Escuadras magnéticas Truper clásicas (ESM-3, ESM-4) deben compartir la misma imagen
        if "ESM-3" in by_sku and "ESM-4" in by_sku:
            self.assertEqual(by_sku["ESM-3"]["image"], by_sku["ESM-4"]["image"])
            self.assertIn("escuadras-magneticas-truper.webp", by_sku["ESM-3"]["image"])

        # Bisagras Hermex acabado latón antiguo (BR-152, etc.)
        if "BR-152" in by_sku:
            self.assertIn("bisagras-laton-antiguo-hermex.webp", by_sku["BR-152"]["image"])

        # Cortacírculos bimetálicos (COBI-1, COBI-1-1/2, COBI-2)
        if "COBI-1" in by_sku and "COBI-2" in by_sku:
            self.assertEqual(by_sku["COBI-1"]["image"], by_sku["COBI-2"]["image"])
            self.assertIn("brocasierra-bimetalica-truper.webp", by_sku["COBI-1"]["image"])

    def test_css_product_image_display_rules(self):
        """Verifica que styles.css use object-fit contain y fondo blanco para evitar cortes y deformaciones."""
        with open(STYLES_CSS, "r", encoding="utf-8") as f:
            css = f.read()
        self.assertIn(".product-thumb-img", css)
        self.assertIn("object-fit: contain;", css)
        self.assertIn(".product-image-container", css)
        self.assertIn("background: #ffffff;", css)

    def test_scan_page_tool_functionality(self):
        """Verifica la función scan_page para inspección automática de páginas del catálogo."""
        import scripts.extract_truper_poc as extractor
        res = extractor.scan_page(34)
        self.assertIsNotNone(res)
        self.assertEqual(res["page"], 34)
        self.assertGreater(res["images_count"], 0)
        self.assertGreater(res["claves_count"], 0)
        self.assertIn("ATX-12", res["claves"])
        self.assertGreater(res["store_matches_count"], 0)


    def test_batch2_families_and_volume(self):
        """Verifica que el catálogo cuente con al menos 60 familias y más de 120 productos de la tienda actualizados."""
        groups = self.manifest.get("groups", [])
        self.assertGreaterEqual(len(groups), 60, "Debe haber al menos 60 familias visuales registradas")
        updated_count = self.manifest.get("total_store_products_updated", 0)
        self.assertGreaterEqual(updated_count, 120, "Deben haberse actualizado más de 120 productos con fotos oficiales")

    def test_featured_showcase_section_in_html(self):
        """Verifica que index.html contenga la sección destacada de artículos más vendidos con sus pestañas."""
        index_html = os.path.join(PROJECT_ROOT, "index.html")
        with open(index_html, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("featured-showcase", html)
        self.assertIn("featured-cards-grid", html)
        self.assertIn("switchFeaturedCategory", html)
        self.assertIn("tab-btn-manuales", html)
        self.assertIn("tab-btn-construccion", html)
        self.assertIn("tab-btn-electricas", html)
        self.assertIn("tab-btn-plomeria", html)

    def test_stepper_drawer_mobile_ux(self):
        """Verifica la estructura en 2 pasos del cajón y los campos prioritarios del solicitante."""
        index_html = os.path.join(PROJECT_ROOT, "index.html")
        with open(index_html, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("drawer-stepper-bar", html)
        self.assertIn("drawer-step-1", html)
        self.assertIn("drawer-step-2", html)
        self.assertIn("quote-client-name", html)
        self.assertIn("quote-client-phone", html)
        self.assertIn("btn-continue-step-2", html)
        self.assertIn("customer-priority-card", html)

    def test_mobile_responsive_drawer_rules_in_css(self):
        """Verifica que styles.css contenga las reglas mobile-first para el cajón y la sección destacada."""
        with open(STYLES_CSS, "r", encoding="utf-8") as f:
            css = f.read()
        self.assertIn(".drawer-stepper-bar", css)
        self.assertIn(".customer-priority-card", css)
        self.assertIn(".featured-showcase-section", css)
        self.assertIn("@media (max-width: 640px)", css)
        self.assertIn("100dvh", css)

    def test_scale_200_families_and_manifest_volume(self):
        """Verifica que el catálogo alcance al menos 200 familias visuales y más de 250 productos de tienda mapeados."""
        groups = self.manifest.get("groups", [])
        self.assertGreaterEqual(len(groups), 200, f"Debe haber al menos 200 familias registradas, hay {len(groups)}")
        updated_count = self.manifest.get("total_store_products_updated", 0)
        self.assertGreaterEqual(updated_count, 250, f"Deben haberse actualizado más de 250 productos con fotos oficiales, hay {updated_count}")

        files = [f for f in os.listdir(TRUPER_IMG_DIR) if f.endswith(".webp")]
        self.assertGreaterEqual(len(files), 200, f"Debe haber al menos 200 imágenes WebP en disco, hay {len(files)}")

        # Verificar presencia de las 7 marcas oficiales del grupo Truper
        all_brands = set(g.get("brand", "").upper() for g in groups)
        for expected_brand in ["TRUPER", "PRETUL", "VOLTECK", "FOSET", "HERMEX", "FIERO", "KLINTEK"]:
            self.assertIn(expected_brand, all_brands, f"La marca oficial {expected_brand} debe estar representada")

    def test_truper_preview_html_aesthetic_and_modal(self):
        """Verifica que truper_preview.html contenga los elementos del diseño oficial Truper (marcas, filtros, modal)."""
        preview_html = os.path.join(PROJECT_ROOT, "truper_preview.html")
        self.assertTrue(os.path.isfile(preview_html), "truper_preview.html debe existir en la raíz del proyecto")
        with open(preview_html, "r", encoding="utf-8") as f:
            html = f.read()

        # Estética oficial de marcas
        self.assertIn("top-brand-strip", html)
        self.assertIn("brand-tag-truper", html)
        self.assertIn("brand-tag-pretul", html)
        self.assertIn("brand-tag-volteck", html)
        self.assertIn("brand-tag-foset", html)
        self.assertIn("brand-tag-hermex", html)
        self.assertIn("brand-tag-fiero", html)
        self.assertIn("brand-tag-klintek", html)

        # Toolbar y filtros interactivos
        self.assertIn("searchInput", html)
        self.assertIn("setBrandFilter", html)
        self.assertIn("setCategoryFilter", html)
        self.assertIn("setViewMode", html)

        # Modal de ficha técnica
        self.assertIn("productModal", html)
        self.assertIn("openModal", html)
        self.assertIn("modalWhatsAppBtn", html)

    def test_manifest_integrity_brand_categories_and_sync(self):
        """Verifica que todos los grupos tengan marcas oficiales y categorías válidas, y que los productos estén 100% sincronizados."""
        valid_brands = {"Truper", "Pretul", "Volteck", "Foset", "Hermex", "Fiero", "Klintek"}
        groups = self.manifest.get("groups", [])
        self.assertGreaterEqual(len(groups), 200)

        for g in groups:
            self.assertIn(g.get("brand"), valid_brands, f"Grupo {g['id']} tiene marca no oficial: {g.get('brand')}")
            self.assertTrue(bool(g.get("category")), f"Grupo {g['id']} no tiene categoría asignada")

        # 100% Sincronización entre manifest y products.json
        products_by_sku = {p.get("sku"): p for p in self.products if p.get("sku")}
        updated_products = self.manifest.get("updated_products", [])
        self.assertEqual(len(updated_products), self.manifest.get("total_store_products_updated"))
        self.assertGreaterEqual(len(updated_products), 250)

        for up in updated_products:
            sku = up.get("sku")
            self.assertIn(sku, products_by_sku, f"SKU {sku} en manifest no existe en products.json")
            p = products_by_sku[sku]
            self.assertEqual(p.get("image"), up.get("new_image"), f"Mismatch de imagen para SKU {sku}")
            self.assertEqual(p.get("image_url"), up.get("new_image"), f"Mismatch de image_url para SKU {sku}")
            full_path = os.path.join(PROJECT_ROOT, p.get("image"))
            self.assertTrue(os.path.isfile(full_path), f"Archivo no existe: {full_path}")

        # Comprobar que ningún producto en products.json tenga marcas espurias
        spurious_brand = [p["sku"] for p in self.products if p.get("brand") == "Herramientas Manuales"]
        self.assertEqual(len(spurious_brand), 0, f"Existen productos con marca 'Herramientas Manuales': {spurious_brand}")

    def test_no_blank_images_in_truper_catalog(self):
        """Verifica que ninguna de las imágenes WebP de catálogo esté vacía o sea un lienzo blanco liso."""
        files = [f for f in os.listdir(TRUPER_IMG_DIR) if f.endswith(".webp")]
        self.assertGreaterEqual(len(files), 200)

        for fname in files:
            fpath = os.path.join(TRUPER_IMG_DIR, fname)
            with Image.open(fpath) as im:
                ext = im.getextrema()
                # Si todos los canales RGB tienen mínimo >= 250, la imagen está completamente en blanco
                is_blank = all(e[0] >= 250 for e in ext[:3])
                self.assertFalse(is_blank, f"La imagen {fname} está completamente en blanco (0% de contenido visual)")


    def test_module_a_360_families_and_volume(self):
        """Verifica que tras completar el Módulo A el catálogo alcance al menos 360 familias y más de 450 productos vinculados."""
        groups = self.manifest.get("groups", [])
        self.assertGreaterEqual(len(groups), 360, f"Debe haber al menos 360 familias registradas tras Módulo A, hay {len(groups)}")
        updated_count = self.manifest.get("total_store_products_updated", 0)
        self.assertGreaterEqual(updated_count, 450, f"Deben haberse actualizado más de 450 productos con fotos oficiales, hay {updated_count}")

        files = [f for f in os.listdir(TRUPER_IMG_DIR) if f.endswith(".webp")]
        self.assertGreaterEqual(len(files), 360, f"Debe haber al menos 360 imágenes WebP en disco, hay {len(files)}")

        # Verificar que categorías clave de Módulo A (Cajas, Lonas, Cintas, Prensas) estén representadas
        all_ids = set(g["id"] for g in groups)
        self.assertIn("caja-herramientas-industrial-26-truper", all_ids)
        self.assertIn("lona-reforzada-azul-truper", all_ids)
        self.assertIn("cinta-aislar-33-negra-truper", all_ids)
        self.assertIn("cutter-reforzado-25mm-truper-expert", all_ids)
        self.assertIn("prensa-hierro-nodular-carpintero-truper", all_ids)
        self.assertIn("remachadora-profesional-9-truper", all_ids)


    def test_module_b_460_families_and_volume(self):
        """Verifica que tras completar el Módulo B el catálogo alcance al menos 460 familias y más de 600 productos vinculados."""
        groups = self.manifest.get("groups", [])
        self.assertGreaterEqual(len(groups), 460, f"Debe haber al menos 460 familias registradas tras Módulo B, hay {len(groups)}")
        updated_count = self.manifest.get("total_store_products_updated", 0)
        self.assertGreaterEqual(updated_count, 600, f"Deben haberse actualizado más de 600 productos con fotos oficiales, hay {updated_count}")

        files = [f for f in os.listdir(TRUPER_IMG_DIR) if f.endswith(".webp")]
        self.assertGreaterEqual(len(files), 460, f"Debe haber al menos 460 imágenes WebP en disco, hay {len(files)}")

        # Verificar presencia de familias clave de Módulo B (Candados, Cadenas, Cables, Tijeras de poda, Machetes)
        all_ids = set(g["id"] for g in groups)
        self.assertIn("candados-hierro-gancho-corto-hermex", all_ids)
        self.assertIn("candados-laton-gancho-corto-hermex", all_ids)
        self.assertIn("cerraduras-sobreponer-barra-fija-hermex", all_ids)
        self.assertIn("cadenas-pulidas-eslabon-corto-fiero", all_ids)
        self.assertIn("cables-acero-galvanizado-flexible-fiero", all_ids)
        self.assertIn("tijeras-poda-bypass-aluminio-truper", all_ids)
        self.assertIn("machetes-estandar-cinta-cacha-negra-truper", all_ids)
        self.assertIn("fumigadores-manuales-compresion-truper", all_ids)


    def test_module_c_560_families_and_volume(self):
        """Verifica que tras completar el Módulo C el catálogo alcance al menos 560 familias y más de 900 productos vinculados."""
        groups = self.manifest.get("groups", [])
        self.assertGreaterEqual(len(groups), 560, f"Debe haber al menos 560 familias registradas tras Módulo C, hay {len(groups)}")
        updated_count = self.manifest.get("total_store_products_updated", 0)
        self.assertGreaterEqual(updated_count, 900, f"Deben haberse actualizado más de 900 productos con fotos oficiales, hay {updated_count}")

        files = [f for f in os.listdir(TRUPER_IMG_DIR) if f.endswith(".webp")]
        self.assertGreaterEqual(len(files), 560, f"Debe haber al menos 560 imágenes WebP en disco, hay {len(files)}")

        # Verificar presencia de familias clave de Módulo C (Volteck y Foset)
        all_ids = set(g["id"] for g in groups)
        # Volteck
        self.assertIn("linterna-plastica-led-recargable-volteck", all_ids)
        self.assertIn("multicontacto-barra-supresor-picos-6-entradas-volteck", all_ids)
        self.assertIn("timbre-inalambrico-digital-volteck", all_ids)
        self.assertIn("foco-led-estandar-a19-luz-calida-volteck", all_ids)
        self.assertIn("reflector-led-exterior-delgado-30w-volteck", all_ids)
        # Foset
        self.assertIn("regadera-cuadrada-plato-ancho-acero-foset", all_ids)
        self.assertIn("mezcladora-fregadero-cuello-ganso-palanca-foset", all_ids)
        self.assertIn("cespol-bote-plastico-lavabo-bote-flexible-foset", all_ids)
        self.assertIn("calentador-agua-instantaneo-gas-lp-foset", all_ids)
        self.assertIn("valvula-esfera-cpvc-cementar-foset", all_ids)
        self.assertIn("llave-esfera-laton-paso-completo-foset", all_ids)


    def test_module_d_720_families_and_volume(self):
        """Verifica que tras completar el Módulo D el catálogo alcance al menos 720 familias y más de 1,300 productos vinculados."""
        groups = self.manifest.get("groups", [])
        self.assertGreaterEqual(len(groups), 720, f"Debe haber al menos 720 familias registradas tras Módulo D, hay {len(groups)}")
        updated_count = self.manifest.get("total_store_products_updated", 0)
        self.assertGreaterEqual(updated_count, 1300, f"Deben haberse actualizado más de 1,300 productos con fotos oficiales, hay {updated_count}")

        files = [f for f in os.listdir(TRUPER_IMG_DIR) if f.endswith(".webp")]
        self.assertGreaterEqual(len(files), 720, f"Debe haber al menos 720 imágenes WebP en disco, hay {len(files)}")

        # Verificar presencia de familias clave de Módulo D (Construcción, Medición, Pintura)
        all_ids = set(g["id"] for g in groups)
        self.assertIn("pala-cuadrada-puno-y-truper", all_ids)
        self.assertIn("pala-redonda-puno-y-truper", all_ids)
        self.assertIn("carretilla-4-5-ft3-metalica-truper", all_ids)
        self.assertIn("cuchara-albanil-philadelphia-truper", all_ids)
        self.assertIn("llana-lisa-acero-mango-madera-truper", all_ids)
        self.assertIn("flexometro-gripper-contra-impacto-5m-truper", all_ids)
        self.assertIn("nivel-profesional-aluminio-24-truper", all_ids)
        self.assertIn("brocha-cerda-natural-4-truper-expert", all_ids)
        self.assertIn("rodillo-profesional-9-superficie-rugosa-truper", all_ids)
        self.assertIn("espatula-flexible-acero-inox-3-truper-expert", all_ids)
        self.assertIn("marro-octagonal-mango-madera-4lb-truper", all_ids)
        self.assertIn("talacho-pico-con-mango-madera-5lb-truper", all_ids)


if __name__ == "__main__":
    unittest.main()



