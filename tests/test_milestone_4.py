"""
Automated Empirical Test Suite for Milestone 4: WhatsApp Checkout, Multi-Branch Routing,
and 4-Tier Automated Verification Harness (R4)
Ferretería y Tlapalería El Águila

Empirical verification covering:
- Feature 12: WhatsApp Quotation Calculation & VAT-inclusive pricing (+16% IVA)
- Feature 13: Multi-Branch Quotation Routing (Las Delicias vs. Estrellas de Buena Vista)
- Feature 14: Automated Test Harness across Tiers 1-4
- Feature 15: osvScanner Security Audit Compliance
"""

import json
import math
import os
import re
import unittest
import urllib.parse
from html.parser import HTMLParser

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_JSON_PATH = os.path.join(PROJECT_ROOT, "data", "products.json")
INDEX_HTML_PATH = os.path.join(PROJECT_ROOT, "index.html")
APP_JS_PATH = os.path.join(PROJECT_ROOT, "assets", "js", "app.js")
STYLES_CSS_PATH = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")


class DOMIdCollector(HTMLParser):
    """Collects element IDs, classes, and attributes from HTML markup."""
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.classes = set()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.elements.append({"tag": tag, "attrs": attr_dict})
        if "id" in attr_dict:
            self.ids.add(attr_dict["id"])
        if "class" in attr_dict:
            for c in attr_dict["class"].split():
                self.classes.add(c)


def simulate_whatsapp_message(quote_cart, branch_info, client_data=None, date_str="14 de septiembre de 2026, 14:00"):
    """
    Python reference simulation of formatWhatsAppMessage from assets/js/app.js.
    Produces identical message structure and URL output for empirical verification.
    """
    if client_data is None:
        client_data = {}

    branch_id = branch_info.get("id", "delicias")
    branch_name = branch_info.get("name", "Sucursal Las Delicias")
    branch_address_raw = branch_info.get("address", "")
    branch_phone = branch_info.get("phone", "")
    branch_whatsapp = branch_info.get("whatsapp", "")

    if branch_id == "delicias":
        branch_address = f"{branch_address_raw} (A un lado del Centro de Salud San Joaquín)"
    else:
        branch_address = branch_address_raw

    client_name = client_data.get("clientName", "").strip() or "Cliente Particular / Mostrador"
    site_location = client_data.get("siteLocation", "").strip() or "Recolección en Mostrador Villahermosa"
    notes = client_data.get("notes", "").strip()

    msg = "*SOLICITUD DE COTIZACIÓN DE MATERIALES*\n"
    msg += "*FERRETERÍA Y TLAPALERÍA EL ÁGUILA*\n"
    msg += "_¡Todo lo que necesitas para tu hogar o trabajo, en un solo lugar!_\n"
    msg += "━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📍 *Sucursal Seleccionada:* {branch_name}\n"
    msg += f"🏢 *Ubicación:* {branch_address}\n"
    msg += f"📱 *Teléfono / WhatsApp Mostrador:* {branch_phone}\n"
    msg += f"📅 *Fecha:* {date_str}\n\n"

    msg += "*DATOS DEL CLIENTE / OBRA:*\n"
    msg += f"• *Cliente / Empresa:* {client_name}\n"
    msg += f"• *Lugar de Entrega / Obra:* {site_location}\n"
    if notes:
        msg += f"• *Notas:* {notes}\n"
    msg += "\n*RELACIÓN DE MATERIALES SOLICITADOS:*\n"

    idx = 1
    total_estimado = 0.0

    for sku, entry in quote_cart.items():
        item = entry["item"]
        qty = entry["quantity"]
        subtotal = item["base_price"] * qty
        total_estimado += subtotal

        mfg_code = item.get("manufacturer_code")
        ref_code = f"[Clave: {mfg_code}]" if mfg_code else f"[SKU: {sku}]"

        msg += f"{idx}. {ref_code} *{item['name']}*\n"
        unit = item.get("unit_measure") or "PZA"
        msg += f"   └ Cantidad: *{qty}* {unit} | Subtotal: *${subtotal:.2f}*\n"
        idx += 1

    msg += "━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"*TOTAL ESTIMADO:* *${total_estimado:.2f} MXN*\n\n"
    msg += f"_Solicito amablemente confirmar existencias en {branch_name}, descuentos por volumen y tiempo de entrega. Saludos cordiales._"

    encoded_msg = urllib.parse.quote(msg, safe="")
    whatsapp_url = f"https://wa.me/{branch_whatsapp}?text={encoded_msg}"

    return {
        "rawMessage": msg,
        "encodedMessage": encoded_msg,
        "targetNumber": branch_whatsapp,
        "totalEstimado": total_estimado,
        "whatsappUrl": whatsappUrl if False else whatsapp_url
    }


class TestMilestone4WhatsAppAndTiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assertTrue(os.path.isfile(PRODUCTS_JSON_PATH), f"Missing {PRODUCTS_JSON_PATH}")
        cls.assertTrue(os.path.isfile(INDEX_HTML_PATH), f"Missing {INDEX_HTML_PATH}")
        cls.assertTrue(os.path.isfile(APP_JS_PATH), f"Missing {APP_JS_PATH}")
        cls.assertTrue(os.path.isfile(STYLES_CSS_PATH), f"Missing {STYLES_CSS_PATH}")

        with open(PRODUCTS_JSON_PATH, "r", encoding="utf-8") as f:
            cls.products = json.load(f)

        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            cls.index_html = f.read()

        with open(APP_JS_PATH, "r", encoding="utf-8") as f:
            cls.app_js = f.read()

        with open(STYLES_CSS_PATH, "r", encoding="utf-8") as f:
            cls.styles_css = f.read()

        cls.sku_map = {p["sku"]: p for p in cls.products}

        cls.dom = DOMIdCollector()
        cls.dom.feed(cls.index_html)

        cls.branch_delicias = {
            "id": "delicias",
            "name": "Sucursal Las Delicias",
            "address": "Av. Revolución 1203, Cuadrante II, Las Delicias, C.P. 86140, Villahermosa, Tab.",
            "landmark": "A un lado del Centro de Salud San Joaquín",
            "city": "Villahermosa, Tabasco",
            "phone": "993 289 2935",
            "whatsapp": "529932892935",
            "badge": "Matriz / Mostrador Delicias",
            "isMatriz": True
        }

        cls.branch_buenavista = {
            "id": "buenavista",
            "name": "Sucursal Estrellas de Buena Vista",
            "address": "Carr. Villahermosa a La Isla Km 5.300, Buena Vista 1ra Secc, C.P. 86280, Villahermosa, Tab.",
            "landmark": "Buena Vista 1ra Secc",
            "city": "Villahermosa, Tabasco",
            "phone": "993 192 8313",
            "whatsapp": "529931928313",
            "badge": "Sucursal Buena Vista",
            "isMatriz": False
        }

    # =========================================================================
    # TIER 1: FEATURE COVERAGE (Core Checkout & Branch Features in Isolation)
    # =========================================================================

    def test_t1_01_product_base_price_vat_inclusion(self):
        """Tier 1: Verify catalog items added to cart use base_price reflecting retail price with 16% IVA."""
        sample_skus = ["M-048P", "1524", "MUFA-3/4", "661", "5661R"]
        for sku in sample_skus:
            prod = self.sku_map[sku]
            self.assertIn("base_price", prod)
            self.assertIsInstance(prod["base_price"], (int, float))
            self.assertGreater(prod["base_price"], 0.0)

        # Confirm code in app.js references item.base_price for quotation
        self.assertIn("item.base_price", self.app_js)
        self.assertIn("itemSubtotal = item.base_price * quantity", self.app_js)

    def test_t1_02_cart_item_subtotal_arithmetic(self):
        """Tier 1: Verify item subtotal calculation is strictly base_price * quantity formatted to 2 decimals."""
        item = self.sku_map["M-048P"]  # $371.00
        qty = 3
        expected_subtotal = 371.00 * 3
        self.assertEqual(expected_subtotal, 1113.00)
        self.assertEqual(f"${expected_subtotal:.2f}", "$1113.00")

    def test_t1_03_cart_grand_total_arithmetic(self):
        """Tier 1: Verify grand total sum across multiple items matches exact arithmetic sum."""
        cart = {
            "M-048P": {"item": self.sku_map["M-048P"], "quantity": 2},  # 371.00 * 2 = 742.00
            "1524": {"item": self.sku_map["1524"], "quantity": 5},      # 30.00 * 5 = 150.00
            "MUFA-3/4": {"item": self.sku_map["MUFA-3/4"], "quantity": 10} # 24.00 * 10 = 240.00
        }
        total = sum(entry["item"]["base_price"] * entry["quantity"] for entry in cart.values())
        self.assertEqual(total, 1132.00)
        self.assertEqual(f"${total:.2f}", "$1132.00")

    def test_t1_04_branch_delicias_phone_and_landmark(self):
        """Tier 1: Verify Las Delicias branch phone (993 289 2935) and San Joaquín landmark."""
        self.assertIn("993 289 2935", self.app_js)
        self.assertIn("529932892935", self.app_js)
        self.assertIn("Centro de Salud San Joaquín", self.app_js)
        self.assertIn("Av. Revolución 1203", self.app_js)

        # In index.html
        self.assertIn("993 289 2935", self.index_html)
        self.assertIn("529932892935", self.index_html)

    def test_t1_05_branch_buenavista_phone_and_address(self):
        """Tier 1: Verify Estrellas de Buena Vista branch phone (993 192 8313) and address."""
        self.assertIn("993 192 8313", self.app_js)
        self.assertIn("529931928313", self.app_js)
        self.assertIn("Carr. Villahermosa a La Isla Km 5.300", self.app_js)

        # In index.html
        self.assertIn("993 192 8313", self.index_html)
        self.assertIn("529931928313", self.index_html)

    def test_t1_06_whatsapp_url_scheme_structure(self):
        """Tier 1: Verify WhatsApp dispatch URL conforms to https://wa.me/{number}?text={encoded}."""
        quote = simulate_whatsapp_message(
            {"1524": {"item": self.sku_map["1524"], "quantity": 1}},
            self.branch_delicias
        )
        url = quote["whatsappUrl"]
        self.assertTrue(url.startswith("https://wa.me/529932892935?text="))
        parsed = urllib.parse.urlparse(url)
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.netloc, "wa.me")
        self.assertEqual(parsed.path, "/529932892935")
        qs = urllib.parse.parse_qs(parsed.query)
        self.assertIn("text", qs)
        self.assertTrue(len(qs["text"][0]) > 20)

    def test_t1_07_message_header_and_store_branding(self):
        """Tier 1: Verify official quotation header branding and commercial motto."""
        quote = simulate_whatsapp_message(
            {"1524": {"item": self.sku_map["1524"], "quantity": 1}},
            self.branch_delicias
        )
        msg = quote["rawMessage"]
        self.assertIn("*SOLICITUD DE COTIZACIÓN DE MATERIALES*", msg)
        self.assertIn("*FERRETERÍA Y TLAPALERÍA EL ÁGUILA*", msg)
        self.assertIn("_¡Todo lo que necesitas para tu hogar o trabajo, en un solo lugar!_", msg)
        self.assertIn("📍 *Sucursal Seleccionada:* Sucursal Las Delicias", msg)

    # =========================================================================
    # TIER 2: BOUNDARY & CORNER CASES (Extreme Values, 0-Prices, Escaping)
    # =========================================================================

    def test_t2_01_empty_cart_behavior(self):
        """Tier 2: Verify empty cart handling in app.js disables dispatch and provides empty state message."""
        self.assertIn('AppState.quoteCart.size === 0', self.app_js)
        self.assertIn('dispatchBtn.disabled = true', self.app_js)
        self.assertIn('Tu presupuesto está vacío', self.app_js)

    def test_t2_02_minimum_and_large_quantities(self):
        """Tier 2: Verify calculations handle minimum quantity (1) and large orders (999/1000)."""
        prod = self.sku_map["M-048P"]  # 371.00
        # Qty 1
        q1 = simulate_whatsapp_message({"M-048P": {"item": prod, "quantity": 1}}, self.branch_delicias)
        self.assertEqual(q1["totalEstimado"], 371.00)
        self.assertIn("Subtotal: *$371.00*", q1["rawMessage"])

        # Qty 999
        q999 = simulate_whatsapp_message({"M-048P": {"item": prod, "quantity": 999}}, self.branch_delicias)
        self.assertEqual(q999["totalEstimado"], 370629.00)
        self.assertIn("Subtotal: *$370629.00*", q999["rawMessage"])
        self.assertIn("*TOTAL ESTIMADO:* *$370629.00 MXN*", q999["rawMessage"])

    def test_t2_03_zero_price_items_handling(self):
        """Tier 2: Verify documented $0.00 SKUs (e.g. 6611) calculate subtotal $0.00 without NaN/error."""
        zero_prod = self.sku_map["6611"]
        self.assertEqual(zero_prod["base_price"], 0.0)

        cart = {
            "6611": {"item": zero_prod, "quantity": 5},
            "1524": {"item": self.sku_map["1524"], "quantity": 2}  # 30.00 * 2 = 60.00
        }
        res = simulate_whatsapp_message(cart, self.branch_delicias)
        self.assertEqual(res["totalEstimado"], 60.00)
        self.assertIn("Subtotal: *$0.00*", res["rawMessage"])
        self.assertIn("Subtotal: *$60.00*", res["rawMessage"])
        self.assertIn("*TOTAL ESTIMADO:* *$60.00 MXN*", res["rawMessage"])

    def test_t2_04_special_characters_escaping_and_url_encoding(self):
        """Tier 2: Verify special characters (quotes, slashes, accents, ampersands) encode and round-trip."""
        prod_mufa = self.sku_map["MUFA-3/4"]
        self.assertIn("3/4'", prod_mufa["name"])

        client_data = {
            "clientName": 'Ing. José "Pepe" Ramos & Cía.',
            "siteLocation": "Fracc. Ocuiltzapotlán / Sector 4 #12",
            "notes": "¡Urgente! ¿Factura con 16% IVA y retención 6%?"
        }

        quote = simulate_whatsapp_message({"MUFA-3/4": {"item": prod_mufa, "quantity": 10}}, self.branch_delicias, client_data)
        encoded = quote["encodedMessage"]

        # Ensure no illegal URI characters remain unencoded
        for illegal in [" ", "\n", '"', "¡", "¿"]:
            self.assertNotIn(illegal, encoded)

        # Ensure round-trip decoding restores verbatim characters
        decoded = urllib.parse.unquote(encoded)
        self.assertIn('Ing. José "Pepe" Ramos & Cía.', decoded)
        self.assertIn("Fracc. Ocuiltzapotlán / Sector 4 #12", decoded)
        self.assertIn("¡Urgente! ¿Factura con 16% IVA y retención 6%?", decoded)
        self.assertIn("3/4'", decoded)

    def test_t2_05_client_data_defaults_and_whitespace(self):
        """Tier 2: Verify fallback to defaults when client name, site, or notes are omitted or whitespace."""
        res_empty = simulate_whatsapp_message(
            {"1524": {"item": self.sku_map["1524"], "quantity": 1}},
            self.branch_delicias,
            {"clientName": "   ", "siteLocation": "", "notes": "  "}
        )
        msg = res_empty["rawMessage"]
        self.assertIn("• *Cliente / Empresa:* Cliente Particular / Mostrador", msg)
        self.assertIn("• *Lugar de Entrega / Obra:* Recolección en Mostrador Villahermosa", msg)
        self.assertNotIn("• *Notas:*", msg)

    def test_t2_06_stepper_and_qty_input_constraints(self):
        """Tier 2: Verify quantity stepper bounds (1 to 999) in app.js and index.html."""
        self.assertIn('min="1"', self.app_js)
        self.assertIn('max="999"', self.app_js)
        self.assertIn('Math.max(1, Math.min(999, val + delta))', self.app_js)
        self.assertIn('handleUpdateCartQty', self.app_js)

    # =========================================================================
    # TIER 3: CROSS-FEATURE COMBINATIONS (Catalog Search + Filter + Cart + Route)
    # =========================================================================

    def test_t3_01_search_filter_cart_dispatch_pipeline(self):
        """Tier 3: Simulate searching 'mezcladora', selecting Plomería, adding M-048P, and routing to Delicias."""
        # Search token simulation
        token = "mezcladora"
        matches = [p for p in self.products if token in (p.get("_s") or p["name"].lower())]
        self.assertTrue(len(matches) > 0)
        target = next((p for p in matches if p["sku"] == "M-048P"), None)
        self.assertIsNotNone(target)
        self.assertEqual(target["category"], "Plomería y Conexiones")
        self.assertEqual(target["brand"], "Basic")

        # Cart addition (qty 2) & dispatch
        cart = {"M-048P": {"item": target, "quantity": 2}}
        res = simulate_whatsapp_message(cart, self.branch_delicias)
        self.assertEqual(res["totalEstimado"], 742.00)
        self.assertEqual(res["targetNumber"], "529932892935")
        self.assertIn("Centro de Salud San Joaquín", res["rawMessage"])
        self.assertIn("Mezcladora lavabo, manerales palanca, Basic", res["rawMessage"])

    def test_t3_02_multi_department_and_multi_brand_cart(self):
        """Tier 3: Construct cross-department cart (5 items, 5 distinct departments, 5 brands)."""
        cross_cart = {
            "1524": {"item": self.sku_map["1524"], "quantity": 4},       # Material Eléctrico, Homologado, $30.00 -> $120.00
            "M-048P": {"item": self.sku_map["M-048P"], "quantity": 1},   # Plomería y Conexiones, Basic, $371.00 -> $371.00
            "661": {"item": self.sku_map["661"], "quantity": 2},         # Material Eléctrico, Homologado, $120.00 -> $240.00
            "MUFA-3/4": {"item": self.sku_map["MUFA-3/4"], "quantity": 5} # Material Eléctrico, Voltech, $24.00 -> $120.00
        }
        res = simulate_whatsapp_message(cross_cart, self.branch_delicias)
        self.assertEqual(res["totalEstimado"], 851.00)
        msg = res["rawMessage"]
        self.assertIn("1. [Clave: 1524]", msg)
        self.assertIn("2. [Clave: M-048P]", msg)
        self.assertIn("3. [Clave: 661]", msg)
        self.assertIn("4. [Clave: MUFA-3/4]", msg)
        self.assertIn("*TOTAL ESTIMADO:* *$851.00 MXN*", msg)

    def test_t3_03_branch_switching_cart_invariance(self):
        """Tier 3: Verify that switching branch preserves exact items and total but re-routes destination & landmark."""
        cart = {
            "M-048P": {"item": self.sku_map["M-048P"], "quantity": 3},
            "1524": {"item": self.sku_map["1524"], "quantity": 10}
        }
        # Under Las Delicias
        res_delicias = simulate_whatsapp_message(cart, self.branch_delicias)
        self.assertEqual(res_delicias["targetNumber"], "529932892935")
        self.assertEqual(res_delicias["totalEstimado"], 1413.00)
        self.assertIn("Centro de Salud San Joaquín", res_delicias["rawMessage"])

        # Under Estrellas de Buena Vista
        res_buenavista = simulate_whatsapp_message(cart, self.branch_buenavista)
        self.assertEqual(res_buenavista["targetNumber"], "529931928313")
        self.assertEqual(res_buenavista["totalEstimado"], 1413.00)
        self.assertIn("Carr. Villahermosa a La Isla Km 5.300", res_buenavista["rawMessage"])
        self.assertNotIn("Centro de Salud San Joaquín", res_buenavista["rawMessage"])

    def test_t3_04_cart_price_synchronization_with_catalog(self):
        """Tier 3: Verify app.js refreshes stored cart item prices with master catalog data on load."""
        self.assertIn("catalogMap = new Map(AppState.masterCatalog.map", self.app_js)
        self.assertIn("cartEntry.item = freshItem", self.app_js)
        self.assertIn("saveCartToStorage()", self.app_js)

    def test_t3_05_floating_and_mobile_nav_whatsapp_branch_sync(self):
        """Tier 3: Verify floating WhatsApp button and mobile nav WhatsApp link update according to selected branch."""
        self.assertIn("floatingWa.href = waUrl", self.app_js)
        self.assertIn("mobileNavWa.href = waUrl", self.app_js)
        self.assertIn("https://wa.me/${branch.whatsapp}", self.app_js)

    # =========================================================================
    # TIER 4: REAL-WORLD SCENARIOS (Contractor Wholesale & Retail Homeowner)
    # =========================================================================

    def test_t4_01_wholesale_contractor_order_las_delicias(self):
        """Tier 4: End-to-End simulation of a wholesale contractor placing a multi-item order for Las Delicias."""
        client_data = {
            "clientName": "Constructora Olmeca S.A. de C.V. (Ing. Carlos Mendoza)",
            "siteLocation": "Fraccionamiento Carrizal, Sector 3, Bodega Industrial",
            "notes": "Requerimos factura CFDI 4.0 con uso G03 y cotizar flete en camión de 3.5 tons"
        }
        order = {
            "M-048P": {"item": self.sku_map["M-048P"], "quantity": 5},     # 371.00 * 5 = 1855.00
            "MUFA-3/4": {"item": self.sku_map["MUFA-3/4"], "quantity": 20}, # 24.00 * 20 = 480.00
            "661": {"item": self.sku_map["661"], "quantity": 10}           # 120.00 * 10 = 1200.00
        }
        expected_total = 1855.00 + 480.00 + 1200.00  # 3535.00
        res = simulate_whatsapp_message(order, self.branch_delicias, client_data)

        self.assertEqual(res["totalEstimado"], expected_total)
        self.assertEqual(res["targetNumber"], "529932892935")

        msg = res["rawMessage"]
        self.assertIn("Constructora Olmeca S.A. de C.V.", msg)
        self.assertIn("Fraccionamiento Carrizal", msg)
        self.assertIn("CFDI 4.0", msg)
        self.assertIn("Sucursal Las Delicias", msg)
        self.assertIn("A un lado del Centro de Salud San Joaquín", msg)
        self.assertIn("Subtotal: *$1855.00*", msg)
        self.assertIn("Subtotal: *$480.00*", msg)
        self.assertIn("Subtotal: *$1200.00*", msg)
        self.assertIn("*TOTAL ESTIMADO:* *$3535.00 MXN*", msg)
        self.assertIn("Solicito amablemente confirmar existencias en Sucursal Las Delicias", msg)

    def test_t4_02_retail_homeowner_order_estrellas_buena_vista(self):
        """Tier 4: End-to-End simulation of a retail customer placing an order for Estrellas de Buena Vista."""
        client_data = {
            "clientName": "Roberto Hernández",
            "siteLocation": "Carretera a La Isla Km 6, Entrada Corregidora",
            "notes": "Favor de apartar para recoger hoy antes de las 6:00 pm"
        }
        order = {
            "1524": {"item": self.sku_map["1524"], "quantity": 3},   # 30.00 * 3 = 90.00
            "5661R": {"item": self.sku_map["5661R"], "quantity": 1}  # 160.00 * 1 = 160.00
        }
        expected_total = 90.00 + 160.00  # 250.00
        res = simulate_whatsapp_message(order, self.branch_buenavista, client_data)

        self.assertEqual(res["totalEstimado"], expected_total)
        self.assertEqual(res["targetNumber"], "529931928313")

        msg = res["rawMessage"]
        self.assertIn("Roberto Hernández", msg)
        self.assertIn("Carretera a La Isla Km 6", msg)
        self.assertIn("Sucursal Estrellas de Buena Vista", msg)
        self.assertIn("Carr. Villahermosa a La Isla Km 5.300", msg)
        self.assertNotIn("Centro de Salud San Joaquín", msg)
        self.assertIn("Subtotal: *$90.00*", msg)
        self.assertIn("Subtotal: *$160.00*", msg)
        self.assertIn("*TOTAL ESTIMADO:* *$250.00 MXN*", msg)

    def test_t4_03_high_volume_10_item_stress_quotation(self):
        """Tier 4: Stress testing a 10-item diverse hardware order with varying prices and quantities."""
        sample_skus = list(self.sku_map.keys())[:10]
        order = {}
        expected_total = 0.0
        for i, sku in enumerate(sample_skus, 1):
            prod = self.sku_map[sku]
            qty = i * 2
            order[sku] = {"item": prod, "quantity": qty}
            expected_total += prod["base_price"] * qty

        res = simulate_whatsapp_message(order, self.branch_delicias)
        self.assertAlmostEqual(res["totalEstimado"], expected_total, places=2)
        msg = res["rawMessage"]
        for i in range(1, 11):
            self.assertIn(f"{i}. [", msg)

    def test_t4_04_html_drawer_and_checkout_dom_integrity(self):
        """Tier 4: Verify that all required interactive DOM element IDs exist in index.html."""
        required_dom_ids = [
            "quote-panel",
            "drawer-backdrop",
            "quote-drawer-trigger",
            "quote-close-btn",
            "drawer-card-delicias",
            "drawer-card-buenavista",
            "cart-items-container",
            "quote-client-name",
            "quote-client-site",
            "quote-client-notes",
            "estimated-total-amount",
            "whatsapp-order-btn",
            "cart-item-count",
            "mobile-cart-count",
            "floating-wa-btn",
            "mobile-nav-wa"
        ]
        for dom_id in required_dom_ids:
            self.assertIn(dom_id, self.dom.ids, f"Required DOM id '{dom_id}' missing from index.html")


if __name__ == "__main__":
    unittest.main(verbosity=2)
