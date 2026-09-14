# E2E Test Infra: Ferretería y Tlapalería El Águila

## Test Philosophy
- Requirement-driven, opaque-box & automated verification.
- Validates data integrity, arithmetic correctness, visual compliance, performance latency, security posture, and deployment readiness.
- 4-Tier methodology:
  - **Tier 1: Feature Coverage** (Core features in isolation).
  - **Tier 2: Boundary & Corner Cases** (Extreme values, zero prices, missing descriptions, edge tokens).
  - **Tier 3: Cross-Feature Combinations** (Search + Category + Brand filtering + Cart + Branch selection).
  - **Tier 4: Real-World Workload Testing** (Full end-to-end user journeys from search to WhatsApp dispatch).

## Feature Inventory Coverage Map
| # | Feature | Requirement Source | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|---------|-------------------|:------:|:------:|:------:|:------:|
| 1 | Full Catalog Ingestion (17,641 items) | ORIGINAL_REQUEST §R1 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 2 | Retail Price Formula (+16% IVA) | ORIGINAL_REQUEST §R1 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 3 | 5 Official Store Departments | ORIGINAL_REQUEST §R1 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 4 | Brand Recognition Heuristics | ORIGINAL_REQUEST §R1 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 5 | Instant Search Performance (<25ms) | ORIGINAL_REQUEST §R1 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 6 | Batch DOM Rendering (PAGE_SIZE = 36) | ORIGINAL_REQUEST §R1 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 7 | Hero Banner Overlay Removal | ORIGINAL_REQUEST §R2 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 8 | 3:2 Natural Canvas Aspect Ratio | ORIGINAL_REQUEST §R2 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 9 | Eagle Logo Extraction (logo-aguila.png) | ORIGINAL_REQUEST §R3 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 10 | Emoji Replacement & Favicon | ORIGINAL_REQUEST §R3 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 11 | Brand Palette Harmonization | ORIGINAL_REQUEST §R3 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 12 | WhatsApp Quotation Calculations | ORIGINAL_REQUEST §R4 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 13 | Multi-Branch Quotation Routing | ORIGINAL_REQUEST §R4 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 14 | osvScanner Security Audit (0 issues) | ORIGINAL_REQUEST §R4 | ✓ (5) | ✓ (5) | ✓ | ✓ |
| 15 | Deployment Readiness & CNAME | ORIGINAL_REQUEST §R4 | ✓ (5) | ✓ (5) | ✓ | ✓ |

## Test Architecture & Execution
- **Runner**: Node.js / Python test runner in `tests/test_suite.py` or `tests/test_runner.js`.
- **Pass Semantics**: Exit code 0, 100% assertions pass.
- **Coverage**: All 15 inventoried features exercised.
