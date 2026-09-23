#!/usr/bin/env python3
"""
Comprehensive Unified Test Runner for Ferretería y Tlapalería El Águila
Executes all milestone test suites:
- Milestone 1: Catalog Replacement & Pricing (tests/test_milestone_1.py)
- Milestone 2: Hero Banner Visual Clearing (tests/test_milestone_2.py)
- Milestone 3: Eagle Logo & Brand Harmonization (tests/test_milestone_3.py)
- Milestone 4: WhatsApp Checkout, Multi-Branch Routing & Tiers 1-4 (tests/test_milestone_4.py)
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.test_milestone_1 import TestMilestone1CatalogAndCounters
from tests.test_milestone_2 import TestMilestone2HeroBanner
from tests.test_milestone_3 import TestMilestone3
from tests.test_milestone_4 import TestMilestone4WhatsAppAndTiers
from tests.test_senior_search_and_maps import TestSeniorSearchAndMaps
from tests.test_frequent_product_covers_and_branch_grid import TestFrequentProductsAndBranchGrid
from tests.test_audit_updates import TestAuditUpdates


def build_suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestMilestone1CatalogAndCounters))
    suite.addTests(loader.loadTestsFromTestCase(TestMilestone2HeroBanner))
    suite.addTests(loader.loadTestsFromTestCase(TestMilestone3))
    suite.addTests(loader.loadTestsFromTestCase(TestMilestone4WhatsAppAndTiers))
    suite.addTests(loader.loadTestsFromTestCase(TestSeniorSearchAndMaps))
    suite.addTests(loader.loadTestsFromTestCase(TestFrequentProductsAndBranchGrid))
    suite.addTests(loader.loadTestsFromTestCase(TestAuditUpdates))
    return suite


def run_all():
    suite = build_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("\n" + "=" * 60)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 60)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
