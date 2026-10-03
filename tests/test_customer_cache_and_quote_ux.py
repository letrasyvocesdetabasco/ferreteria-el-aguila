#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_customer_cache_and_quote_ux.py
Automated tests for customer priority, localStorage caching, phone formatting,
and strict validation in the quotation drawer.
Ferretería y Tlapalería El Águila.
"""

import os
import re
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(PROJECT_ROOT, "index.html")
APP_JS = os.path.join(PROJECT_ROOT, "assets", "js", "app.js")
STYLES_CSS = os.path.join(PROJECT_ROOT, "assets", "css", "styles.css")


class TestCustomerCacheAndQuoteUX(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html = f.read()
        with open(APP_JS, "r", encoding="utf-8") as f:
            cls.js = f.read()
        with open(STYLES_CSS, "r", encoding="utf-8") as f:
            cls.css = f.read()

    def test_customer_prominence_dom_elements(self):
        """Verifica que index.html contenga los elementos del stepper, badge de cache y mensajes de error."""
        self.assertIn('id="stepper-client-pill"', self.html)
        self.assertIn('id="customer-cache-status-badge"', self.html)
        self.assertIn('btn-clear-cache', self.html)
        self.assertIn('id="name-error-msg"', self.html)
        self.assertIn('id="phone-error-msg"', self.html)
        self.assertIn('id="quote-client-name"', self.html)
        self.assertIn('id="quote-client-phone"', self.html)
        self.assertIn('step-guide-banner', self.html)

    def test_customer_inputs_attributes(self):
        """Verifica que los inputs de nombre y teléfono tengan requerimientos y autocompletado nativo."""
        self.assertRegex(self.html, r'<input[^>]+id="quote-client-name"[^>]+required')
        self.assertRegex(self.html, r'<input[^>]+id="quote-client-phone"[^>]+required')
        self.assertIn('autocomplete="name"', self.html)
        self.assertIn('autocomplete="tel"', self.html)

    def test_css_styles_for_cache_and_validation(self):
        """Verifica que styles.css contenga las clases para badge de cache, errores animados y pills."""
        self.assertIn(".customer-cache-status-badge", self.css)
        self.assertIn(".btn-clear-cache", self.css)
        self.assertIn(".stepper-pill-pending", self.css)
        self.assertIn(".stepper-pill-complete", self.css)
        self.assertIn(".field-error-msg", self.css)
        self.assertIn(".form-input-error", self.css)
        self.assertIn("@keyframes shakeInput", self.css)

    def test_app_js_cache_and_validation_functions_exist(self):
        """Verifica que app.js defina e implemente las funciones de persistencia y formateo."""
        self.assertIn("saveCustomerDataToCache", self.js)
        self.assertIn("loadCustomerDataFromCache", self.js)
        self.assertIn("clearCustomerCache", self.js)
        self.assertIn("updateCustomerDataStatusBadge", self.js)
        self.assertIn("formatPhoneInput", self.js)
        self.assertIn("CUSTOMER_CACHE_KEY", self.js)

    def test_app_js_exports_contain_new_functions(self):
        """Verifica que window y module.exports expongan las nuevas funciones del perfil de cliente."""
        self.assertIn("window.saveCustomerDataToCache", self.js)
        self.assertIn("window.loadCustomerDataFromCache", self.js)
        self.assertIn("window.clearCustomerCache", self.js)
        self.assertIn("window.updateCustomerDataStatusBadge", self.js)
        self.assertIn("window.formatPhoneInput", self.js)

    def test_dispatch_to_whatsapp_validation_rules(self):
        """Verifica que dispatchToWhatsApp valide nombre (>= 2 caracteres) y teléfono limpio (>= 10 dígitos)."""
        self.assertIn("nameVal.length < 2", self.js)
        self.assertIn("phoneClean.length < 10", self.js)
        self.assertIn("setDrawerStep(2)", self.js)
        self.assertIn("saveCustomerDataToCache()", self.js)

    def test_phone_formatting_in_app_js(self):
        """Verifica la lógica de formateo de 10 dígitos (ej. 993 123 4567) en formatPhoneInput."""
        self.assertIn("digits.slice(0, 3)", self.js)
        self.assertIn("digits.slice(3, 6)", self.js)


if __name__ == "__main__":
    unittest.main()
