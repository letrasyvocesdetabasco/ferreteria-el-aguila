#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extract_module_a_100.py
Ferretería y Tlapalería El Águila - Módulo A: Extracción de 100 Nuevas Familias Truper

Módulo A (100 familias):
- Cajas de herramientas y organizadores plásticos (Págs 78, 80)
- Cintas de aislar #33, teflón, ducto, masking, empaque, aluminio, antiderrapante (Págs 94-98)
- Lonas reforzadas Truper y Pretul (azul, plata, naranja, verde, camuflaje) (Págs 208-209)
- Cúters profesionales, navajas y cuchillas de repuesto (Págs 123-124)
- Dados, extensiones, nudos articulados y puntas de destornillador (Págs 128, 317)
- Desarmadores de golpe, de acetato, basic, cabinet y joyero (Págs 142-143)
- Prensas de hierro nodular, de resorte, esquineras, barra F y de tubo (Págs 312-314)
- Remachadoras profesionales, Pretul y de acordeón (Pág 325)
- Engrapadoras tipo pistola y escuadras de combinación (Págs 164, 166)
"""

import json
import os
import re
import subprocess
import sys
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = "/home/divadios/Descargas/catalogo_nacional_2026.pdf"
OUTPUT_IMG_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products", "truper")
PRODUCTS_JSON = os.path.join(PROJECT_ROOT, "data", "products.json")
MANIFEST_JSON = os.path.join(PROJECT_ROOT, "data", "truper_poc_manifest.json")
TMP_DIR = "/tmp/mod_a_extract"

# 100 Nuevas Familias de Módulo A
MODULE_A_100_FAMILIES = [
    # -------------------------------------------------------------------------
    # 1. Cajas de Herramientas y Organizadores (12)
    # -------------------------------------------------------------------------
    {
        "id": "caja-herramientas-industrial-26-truper",
        "title": "Cajas para herramienta 26' calidad industrial Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 0,
        "output_filename": "caja-herramientas-industrial-26-truper.webp",
        "codes": ["CHP-26X", "19789", "CHP-26"],
        "description": "Caja plástica de 26 pulgadas con broches metálicos y charola interior Truper"
    },
    {
        "id": "caja-herramientas-industrial-23-truper",
        "title": "Cajas para herramienta 23' calidad industrial Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 1,
        "output_filename": "caja-herramientas-industrial-23-truper.webp",
        "codes": ["CHP-23X", "19788", "CHP-23", "6428", "6459"],
        "description": "Caja plástica de 23 pulgadas con broches metálicos y organizador en tapa Truper"
    },
    {
        "id": "caja-herramientas-industrial-20-truper",
        "title": "Cajas para herramienta 20' calidad industrial Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 2,
        "output_filename": "caja-herramientas-industrial-20-truper.webp",
        "codes": ["CHP-20X", "19787", "CHP-20", "6423", "6427"],
        "description": "Caja plástica de 20 pulgadas con broches metálicos reforzados Truper"
    },
    {
        "id": "caja-herramientas-industrial-17-truper",
        "title": "Cajas para herramienta 17' calidad industrial Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 9,
        "output_filename": "caja-herramientas-industrial-17-truper.webp",
        "codes": ["CHP-17X", "19786", "CHP-17", "CHP-14X"],
        "description": "Caja plástica compacta de 17 pulgadas con broches de alta resistencia Truper"
    },
    {
        "id": "caja-herramientas-plastica-pretul-19",
        "title": "Cajas plásticas para herramienta 19' Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 10,
        "output_filename": "caja-herramientas-plastica-pretul-19.webp",
        "codes": ["CHP-19P", "CHP-19Z", "20608", "5814"],
        "description": "Caja plástica de 19 pulgadas ligera con organizador en tapa Pretul"
    },
    {
        "id": "caja-herramientas-plastica-pretul-16",
        "title": "Cajas plásticas para herramienta 16' Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 11,
        "output_filename": "caja-herramientas-plastica-pretul-16.webp",
        "codes": ["CHP-16P", "CHP-16Z", "20607", "6426"],
        "description": "Caja plástica de 16 pulgadas con broche plástico y agarradera ergonómica Pretul"
    },
    {
        "id": "caja-herramientas-plastica-pretul-13",
        "title": "Cajas plásticas para herramienta 13' Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 12,
        "output_filename": "caja-herramientas-plastica-pretul-13.webp",
        "codes": ["CHP-13P", "CHP-13Z", "CHP-12P", "20606", "20605", "5813", "6403", "6425", "6415", "6429"],
        "description": "Caja plástica para herramientas 12 y 13 pulgadas de uso hogareño Pretul"
    },
    {
        "id": "caja-herramientas-ruedas-25-truper",
        "title": "Caja para herramienta 25' móvil con ruedas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 13,
        "output_filename": "caja-herramientas-ruedas-25-truper.webp",
        "codes": ["CHP-25R", "19790"],
        "description": "Caja móvil de uso rudo con asa telescópica y ruedas de uso rudo Truper"
    },
    {
        "id": "caja-herramientas-compartimentos-22-truper",
        "title": "Cajas para herramienta 22' con compartimentos Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 0,
        "output_filename": "caja-herramientas-compartimentos-22-truper.webp",
        "codes": ["CHA-22NC", "CHA-22S", "CHA-22N", "CHA-22G", "19795"],
        "description": "Caja amplia de 22 pulgadas con compartimentos organizadores superiores Truper"
    },
    {
        "id": "caja-herramientas-amplia-16-truper",
        "title": "Cajas para herramienta amplias 16' Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 78,
        "raw_index": 1,
        "output_filename": "caja-herramientas-amplia-16-truper.webp",
        "codes": ["CHA-16NC", "CHA-16N", "CHA-16G", "CHA-14N", "CHA-14G", "19792"],
        "description": "Caja de diseño espacioso de 16 y 14 pulgadas en colores naranja y gris Truper"
    },
    {
        "id": "organizador-plastico-gavetas-truper",
        "title": "Organizadores plásticos multi-gavetas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 80,
        "raw_index": 0,
        "output_filename": "organizador-plastico-gavetas-truper.webp",
        "codes": ["ORG-64", "ORG-32", "10893", "10894"],
        "description": "Organizador vertical con cajones transparentes para tornillería y piezas pequeñas Truper"
    },
    {
        "id": "gaveta-apilable-almacenamiento-truper",
        "title": "Gavetas plásticas apilables para mostrador Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 80,
        "raw_index": 6,
        "output_filename": "gaveta-apilable-almacenamiento-truper.webp",
        "codes": ["GAV-1", "GAV-2", "GAV-3", "GAV-4", "GAV-5", "GAV-6", "10895"],
        "description": "Gavetas apilables de polipropileno de alta resistencia para ferretería y taller Truper"
    },

    # -------------------------------------------------------------------------
    # 2. Cintas Especializadas, Teflón, Ducto y Antiderrapantes (18)
    # -------------------------------------------------------------------------
    {
        "id": "cinta-aislar-33-negra-truper",
        "title": "Cinta de aislar PVC #33 negra Truper",
        "brand": "Truper",
        "category": "Eléctrico",
        "page": 98,
        "raw_index": 1,
        "output_filename": "cinta-aislar-33-negra-truper.webp",
        "codes": ["M-33NB", "M-33N", "12500", "12501", "12502"],
        "description": "Cinta aislante de PVC grado profesional autoextinguible hasta 600V Truper"
    },
    {
        "id": "cinta-aislar-33-amarilla-truper",
        "title": "Cinta de aislar PVC #33 amarilla Truper",
        "brand": "Truper",
        "category": "Eléctrico",
        "page": 98,
        "raw_index": 3,
        "output_filename": "cinta-aislar-33-amarilla-truper.webp",
        "codes": ["M-33A", "12503"],
        "description": "Cinta aislante amarilla para identificación de fases eléctricas Truper"
    },
    {
        "id": "cinta-aislar-33-azul-truper",
        "title": "Cinta de aislar PVC #33 azul Truper",
        "brand": "Truper",
        "category": "Eléctrico",
        "page": 98,
        "raw_index": 3,
        "output_filename": "cinta-aislar-33-azul-truper.webp",
        "codes": ["M-33Z", "12504", "5761"],
        "description": "Cinta aislante azul para codificación de circuitos Truper"
    },
    {
        "id": "cinta-aislar-33-blanca-truper",
        "title": "Cinta de aislar PVC #33 blanca Truper",
        "brand": "Truper",
        "category": "Eléctrico",
        "page": 98,
        "raw_index": 3,
        "output_filename": "cinta-aislar-33-blanca-truper.webp",
        "codes": ["M-33B", "12505", "5763"],
        "description": "Cinta aislante blanca para señalización y marcado neutro Truper"
    },
    {
        "id": "cinta-aislar-33-roja-truper",
        "title": "Cinta de aislar PVC #33 roja Truper",
        "brand": "Truper",
        "category": "Eléctrico",
        "page": 98,
        "raw_index": 3,
        "output_filename": "cinta-aislar-33-roja-truper.webp",
        "codes": ["M-33R", "12506"],
        "description": "Cinta aislante roja para identificación de líneas vivas Truper"
    },
    {
        "id": "cinta-aislar-33-verde-truper",
        "title": "Cinta de aislar PVC #33 verde Truper",
        "brand": "Truper",
        "category": "Eléctrico",
        "page": 98,
        "raw_index": 3,
        "output_filename": "cinta-aislar-33-verde-truper.webp",
        "codes": ["M-33V", "12507", "5762"],
        "description": "Cinta aislante verde para identificación de tierra física Truper"
    },
    {
        "id": "cinta-aislar-33-gris-truper",
        "title": "Cinta de aislar PVC #33 gris Truper",
        "brand": "Truper",
        "category": "Eléctrico",
        "page": 98,
        "raw_index": 3,
        "output_filename": "cinta-aislar-33-gris-truper.webp",
        "codes": ["M-33G", "12508"],
        "description": "Cinta aislante de PVC color gris Truper"
    },
    {
        "id": "cinta-teflon-sella-roscas-truper",
        "title": "Cintas sella roscas de teflón PTFE Truper",
        "brand": "Truper",
        "category": "Plomería",
        "page": 98,
        "raw_index": 16,
        "output_filename": "cinta-teflon-sella-roscas-truper.webp",
        "codes": ["CT-1/2", "CT-3/4", "CT-1", "CT-10", "CT-13", "CT-19", "CT-25", "12520", "12521", "12522"],
        "description": "Cinta de teflón virgen de alta densidad para sellado hermético de tuberías de agua y gas Truper"
    },
    {
        "id": "cinta-teflon-pretul",
        "title": "Cintas de teflón económicas Pretul",
        "brand": "Pretul",
        "category": "Plomería",
        "page": 98,
        "raw_index": 18,
        "output_filename": "cinta-teflon-pretul.webp",
        "codes": ["CTP-1/2", "CTP-3/4", "22520", "22521"],
        "description": "Cinta sella roscas de teflón para conexiones roscadas sanitarias Pretul"
    },
    {
        "id": "cinta-masking-tape-azul-pintor-truper",
        "title": "Cintas masking tape azul para pintor Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 95,
        "raw_index": 0,
        "output_filename": "cinta-masking-tape-azul-pintor-truper.webp",
        "codes": ["MSK-AZ-3/4", "MSK-AZ-1", "MSK-AZ-1-1/2", "MSK-AZ-2", "12530", "12531"],
        "description": "Cinta azul de enmascarar resistente a rayos UV con remoción limpia hasta 14 días Truper"
    },
    {
        "id": "cinta-masking-tape-uso-general-truper",
        "title": "Cintas masking tape 50m uso general Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 95,
        "raw_index": 1,
        "output_filename": "cinta-masking-tape-uso-general-truper.webp",
        "codes": ["MSK-1/2", "MSK-3/4", "MSK-1", "MSK-1-1/2", "MSK-2", "20668", "20669", "20670", "20671", "20672"],
        "description": "Cintas adhesivas de papel crepado para protección de superficies y rotulado Truper"
    },
    {
        "id": "cinta-masking-tape-pretul",
        "title": "Cintas masking tape escolares y domésticas Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 95,
        "raw_index": 2,
        "output_filename": "cinta-masking-tape-pretul.webp",
        "codes": ["MSK-1/2P", "MSK-3/4P", "MSK-1P", "MSK-1-1/2P", "MSK-2P", "20680", "20681", "20682"],
        "description": "Cinta de papel adhesivo para uso general y fijación ligera Pretul"
    },
    {
        "id": "cinta-para-ducto-gris-truper",
        "title": "Cintas para ducto uso rudo plateada Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 94,
        "raw_index": 16,
        "output_filename": "cinta-para-ducto-gris-truper.webp",
        "codes": ["CD-10", "CD-30", "CD-50", "12550", "12551", "12552"],
        "description": "Cinta duct tape reforzada con malla textil e impermeable de alta adherencia Truper"
    },
    {
        "id": "cinta-para-ducto-negra-truper",
        "title": "Cintas para ducto negra impermeable Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 94,
        "raw_index": 17,
        "output_filename": "cinta-para-ducto-negra-truper.webp",
        "codes": ["CD-10N", "CD-30N", "12555", "12556"],
        "description": "Cinta adhesiva para ducto de color negro multiusos Truper"
    },
    {
        "id": "cinta-empaque-canela-truper",
        "title": "Cintas para empaque canela de polipropileno Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 94,
        "raw_index": 18,
        "output_filename": "cinta-empaque-canela-truper.webp",
        "codes": ["CCA-150", "CCA-50", "CCA-100", "12560", "12561", "5702"],
        "description": "Cinta canela para sellado seguro de cajas de cartón y envíos Truper"
    },
    {
        "id": "cinta-empaque-transparente-truper",
        "title": "Cintas para empaque transparentes y frágil Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 94,
        "raw_index": 19,
        "output_filename": "cinta-empaque-transparente-truper.webp",
        "codes": ["CTR-150", "CTR-50", "CTR-100", "CFR-150", "12565", "12566", "5703"],
        "description": "Cintas de embalaje transparentes y leyenda frágil con adhesivo acrílico Truper"
    },
    {
        "id": "cinta-aluminio-aislamiento-truper",
        "title": "Cintas de aluminio térmicas reforzadas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 96,
        "raw_index": 0,
        "output_filename": "cinta-aluminio-aislamiento-truper.webp",
        "codes": ["CALU-10", "CALU-30", "CALU-45", "12570", "12571", "TI6010"],
        "description": "Cinta de papel aluminio puro para sellado de aire acondicionado y ductos térmicos Truper"
    },
    {
        "id": "cinta-antiderrapante-rollo-truper",
        "title": "Cintas y tiras adhesivas antiderrapantes Truper",
        "brand": "Truper",
        "category": "Seguridad",
        "page": 97,
        "raw_index": 0,
        "output_filename": "cinta-antiderrapante-rollo-truper.webp",
        "codes": ["CAD-RN", "CAD-RT", "CAD-TN", "CAD-TT", "12580", "12581", "12582", "IM2001"],
        "description": "Cinta con grano mineral abrasivo antideslizante para rampas, escaleras y áreas húmedas Truper"
    },

    # -------------------------------------------------------------------------
    # 3. Lonas Reforzadas Truper y Pretul (15)
    # -------------------------------------------------------------------------
    {
        "id": "lona-reforzada-azul-truper",
        "title": "Lonas reforzadas multiusos azul Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 208,
        "raw_index": 4,
        "output_filename": "lona-reforzada-azul-truper.webp",
        "codes": ["LT-23", "LT-23Z", "LT-33", "LT-33Z", "LT-34", "LT-34Z", "LT-45", "LT-45Z", "LT-46", "LT-46Z", "LT-56", "LT-56Z", "LT-612", "LT-612Z", "LT-1217", "LT-1217Z", "12100", "12101", "12102", "12103", "12104", "12105", "12106", "5482"],
        "description": "Lona de polietileno con refuerzo perimetral y ojillos metálicos antioxidables azul Truper"
    },
    {
        "id": "lona-uso-pesado-gris-truper",
        "title": "Lonas para uso pesado reforzadas gris Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 208,
        "raw_index": 5,
        "output_filename": "lona-uso-pesado-gris-truper.webp",
        "codes": ["LT-152", "LT-35", "12110", "12111", "5471", "5472", "5476"],
        "description": "Lona impermeable gris de uso pesado para protección en intemperie y transporte Truper"
    },
    {
        "id": "lona-uso-rudo-verde-olivo-truper-expert",
        "title": "Lonas uso rudo 240 g/m2 verde olivo Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 208,
        "raw_index": 8,
        "output_filename": "lona-uso-rudo-verde-olivo-truper-expert.webp",
        "codes": ["LT-23X", "LT-34X", "LT-45X", "12120", "12121", "12122"],
        "description": "Lona de polietileno laminado de máxima durabilidad con esquinas plásticas reforzadas Truper Expert"
    },
    {
        "id": "lona-pretul-azul",
        "title": "Lonas impermeables color azul Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 209,
        "raw_index": 8,
        "output_filename": "lona-pretul-azul.webp",
        "codes": ["LP-23", "LP-33", "LP-34", "LP-35", "LP-36", "LP-44", "LP-45", "LP-46", "LP-56", "LP-612", "22100", "22101", "22102", "22103", "22104", "22105", "22106", "5442", "5410", "5412", "5418", "5420", "5406"],
        "description": "Lona ligera y resistente de polietileno para cubrir muebles, obras y carga Pretul"
    },
    {
        "id": "lona-pretul-naranja",
        "title": "Lonas impermeables de alta visibilidad naranja Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 209,
        "raw_index": 9,
        "output_filename": "lona-pretul-naranja.webp",
        "codes": ["LP-23N", "LP-33N", "LP-34N", "LP-45N", "LP-46N", "LP-56N", "LP-612N", "22110", "22111", "22112", "22113", "22114", "22115"],
        "description": "Lona de polietileno color naranja reflectante para protección en obras Pretul"
    },
    {
        "id": "lona-pretul-verde",
        "title": "Lonas impermeables de polietileno verde Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 209,
        "raw_index": 10,
        "output_filename": "lona-pretul-verde.webp",
        "codes": ["LP-23V", "LP-33V", "LP-34V", "LP-45V", "LP-46V", "LP-56V", "LP-612V", "22120", "22121", "22122", "22123", "22124", "5467", "5468", "5464"],
        "description": "Lona impermeable verde para jardinería, campamento y patios Pretul"
    },
    {
        "id": "lona-pretul-amarilla",
        "title": "Lonas impermeables color amarillo Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 209,
        "raw_index": 11,
        "output_filename": "lona-pretul-amarilla.webp",
        "codes": ["LP-23A", "LP-33A", "LP-34A", "LP-45A", "LP-46A", "LP-56A", "LP-612A", "22130", "22131", "22132", "22133", "22134"],
        "description": "Lona de alta resistencia y flexibilidad color amarillo con ojillos Pretul"
    },
    {
        "id": "lona-pretul-roja",
        "title": "Lonas impermeables color rojo Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 209,
        "raw_index": 12,
        "output_filename": "lona-pretul-roja.webp",
        "codes": ["LP-23R", "LP-33R", "LP-34R", "LP-45R", "LP-46R", "LP-56R", "LP-612R", "22140", "22141", "22142", "22143", "22144", "5429", "5430", "5432", "5438", "5439", "5425"],
        "description": "Lona impermeable roja para cubiertas y toldos Pretul"
    },
    {
        "id": "lona-pretul-blanca",
        "title": "Lonas impermeables color blanco Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 209,
        "raw_index": 13,
        "output_filename": "lona-pretul-blanca.webp",
        "codes": ["LP-23B", "LP-33B", "LP-34B", "LP-35B", "LP-45B", "LP-46B", "LP-56B", "LP-612B", "22150", "22151", "22152"],
        "description": "Lona blanca reflejante para eventos, puestos y cubiertas Pretul"
    },
    {
        "id": "lona-camuflaje-truper",
        "title": "Lonas tipo militar camuflaje Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 209,
        "raw_index": 25,
        "output_filename": "lona-camuflaje-truper.webp",
        "codes": ["LC-23", "LC-33", "LC-34", "LC-45", "12130", "12131"],
        "description": "Lona con diseño camuflaje para cacería, campamento y exteriores Truper"
    },
    {
        "id": "lona-plata-termica-truper",
        "title": "Lonas térmicas reflectivas aluminio / plata Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 209,
        "raw_index": 26,
        "output_filename": "lona-plata-termica-truper.webp",
        "codes": ["LP-PL-23", "LP-PL-33", "LP-PL-34", "12140", "12141", "5462", "5463", "5494", "5491"],
        "description": "Lona térmica de polietileno con acabado plata para rechazo solar Truper"
    },
    {
        "id": "cepillo-alambre-mango-truper",
        "title": "Cepillos de alambre con mango Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 85,
        "raw_index": 4,
        "output_filename": "cepillo-alambre-mango-truper.webp",
        "codes": ["CALA-4", "CALA-5", "CALA-6", "12400", "12401", "12402"],
        "description": "Cepillo con alambre de acero al carbono y mango de madera pulida ergonómica Truper"
    },
    {
        "id": "cepillo-alambre-curvo-truper",
        "title": "Cepillos de alambre mango curvo Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 85,
        "raw_index": 8,
        "output_filename": "cepillo-alambre-curvo-truper.webp",
        "codes": ["CALA-C", "12405"],
        "description": "Cepillo de alambre de alta resistencia con mango de plástico contorneado Truper"
    },
    {
        "id": "pistola-calafatear-esqueleto-truper",
        "title": "Pistolas para calafatear tipo esqueleto Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 316,
        "raw_index": 3,
        "output_filename": "pistola-calafatear-esqueleto-truper.webp",
        "codes": ["PESQ", "PESQ-X", "17400", "17401"],
        "description": "Pistola tipo esqueleto para cartuchos estándar de silicón y selladores de 300 ml Truper"
    },
    {
        "id": "pistola-calafatear-lisa-reforzada-truper",
        "title": "Pistolas para calafatear cuerpo liso reforzadas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 316,
        "raw_index": 14,
        "output_filename": "pistola-calafatear-lisa-reforzada-truper.webp",
        "codes": ["PLIS", "PLIS-X", "17410", "17411"],
        "description": "Pistola para silicón de cuerpo tubular cerrado y gatillo reforzado Truper"
    },

    # -------------------------------------------------------------------------
    # 4. Cúters, Cuchillas y Corte de Precisión (12)
    # -------------------------------------------------------------------------
    {
        "id": "cutter-reforzado-25mm-truper-expert",
        "title": "Cutter 25 mm trabajo pesado con grip Truper Expert",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 10,
        "output_filename": "cutter-reforzado-25mm-truper-expert.webp",
        "codes": ["CUT-7XX", "16978"],
        "description": "Cutter profesional de 25 mm con alma metálica, perilla de ajuste y mango antiderrapante Truper Expert"
    },
    {
        "id": "cutter-plastico-alma-metalica-25mm-truper",
        "title": "Cutter 25 mm reforzado con alma metálica Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 11,
        "output_filename": "cutter-plastico-alma-metalica-25mm-truper.webp",
        "codes": ["CUT-7", "16977"],
        "description": "Cutter reforzado de 25 mm de plástico rígido y guía de acero Truper"
    },
    {
        "id": "cutter-reforzado-grip-18mm-truper",
        "title": "Cutter 18 mm con grip antiderrapante Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 12,
        "output_filename": "cutter-reforzado-grip-18mm-truper.webp",
        "codes": ["CUT-6X", "CUT-6XX", "16975", "16976", "8739"],
        "description": "Cutter de 18 mm con seguro automático y recubrimiento ergonómico Truper"
    },
    {
        "id": "cutter-estandar-18mm-truper",
        "title": "Cutter 18 mm estándar Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 23,
        "output_filename": "cutter-estandar-18mm-truper.webp",
        "codes": ["CUT-6", "16974", "5904", "5902"],
        "description": "Cutter estándar de 18 mm para corte de cartón, vinil y plástico Truper"
    },
    {
        "id": "cutter-alma-metalica-18mm-pretul",
        "title": "Cutter 18 mm con alma metálica Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 26,
        "output_filename": "cutter-alma-metalica-18mm-pretul.webp",
        "codes": ["CUT-6P", "CUT-6PB", "21974", "21975"],
        "description": "Cutter económico de 18 mm con carril metálico y seguro corredizo Pretul"
    },
    {
        "id": "cutter-compacto-grip-9mm-truper",
        "title": "Cutter 9 mm con grip para precisión Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 32,
        "output_filename": "cutter-compacto-grip-9mm-truper.webp",
        "codes": ["CUT-5X", "16972", "8740"],
        "description": "Cutter delgado de 9 mm para trabajos de corte fino y manualidades Truper"
    },
    {
        "id": "cutter-compacto-9mm-truper",
        "title": "Cutter 9 mm compacto Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 11,
        "output_filename": "cutter-compacto-9mm-truper.webp",
        "codes": ["CUT-5", "16971", "5903", "5901"],
        "description": "Cutter compacto de 9 mm para corte ligero Truper"
    },
    {
        "id": "cutter-compacto-9mm-pretul",
        "title": "Cutter 9 mm con alma metálica Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 123,
        "raw_index": 26,
        "output_filename": "cutter-compacto-9mm-pretul.webp",
        "codes": ["CUT-5P", "CUT-5PB", "21971", "21972"],
        "description": "Cutter de 9 mm en blíster con carril de acero Pretul"
    },
    {
        "id": "cuchillas-repuesto-cutter-25mm-truper",
        "title": "Cuchillas de repuesto para cutter 25 mm Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 124,
        "raw_index": 14,
        "output_filename": "cuchillas-repuesto-cutter-25mm-truper.webp",
        "codes": ["REP-CUT-7", "16982"],
        "description": "Despachador con hojas de repuesto seccionadas de 25 mm de acero al carbono Truper"
    },
    {
        "id": "cuchillas-repuesto-cutter-18mm-truper",
        "title": "Cuchillas de repuesto para cutter 18 mm Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 124,
        "raw_index": 16,
        "output_filename": "cuchillas-repuesto-cutter-18mm-truper.webp",
        "codes": ["REP-CUT-6", "16980", "16981", "DC0311"],
        "description": "Estuche con cuchillas de repuesto seccionables de 18 mm Truper"
    },
    {
        "id": "cuchillas-repuesto-cutter-9mm-truper",
        "title": "Cuchillas de repuesto para cutter 9 mm Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 124,
        "raw_index": 18,
        "output_filename": "cuchillas-repuesto-cutter-9mm-truper.webp",
        "codes": ["REP-CUT-5", "16979", "5906"],
        "description": "Cuchillas de repuesto de 9 mm para corte de precisión Truper"
    },
    {
        "id": "cuchillas-repuesto-navaja-trapezoidal-truper",
        "title": "Cuchillas de repuesto trapezoidales para navaja Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 124,
        "raw_index": 20,
        "output_filename": "cuchillas-repuesto-navaja-trapezoidal-truper.webp",
        "codes": ["REP-NAV", "16985"],
        "description": "Hojas de repuesto trapezoidales de alta resistencia para navaja multiusos Truper"
    },

    # -------------------------------------------------------------------------
    # 5. Puntas de Destornillador, Dados y Accesorios (14)
    # -------------------------------------------------------------------------
    {
        "id": "juego-puntas-destornillador-estuche-truper",
        "title": "Juegos de puntas para destornillador con estuche Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 317,
        "raw_index": 5,
        "output_filename": "juego-puntas-destornillador-estuche-truper.webp",
        "codes": ["PUN-33", "PUN-29", "PUN-10", "12860", "12861"],
        "description": "Juego completo de puntas mixtas de 1 pulgada forjadas en acero S2 Truper"
    },
    {
        "id": "puntas-phillips-cromo-vanadio-truper",
        "title": "Puntas para destornillador tipo Phillips Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 317,
        "raw_index": 9,
        "output_filename": "puntas-phillips-cromo-vanadio-truper.webp",
        "codes": ["PPH-1", "PPH-2", "PPH-3", "12870", "12871", "12872"],
        "description": "Puntas para taladro y destornillador punta de cruz PH1, PH2 y PH3 Truper"
    },
    {
        "id": "puntas-planas-cromo-vanadio-truper",
        "title": "Puntas para destornillador punta plana Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 317,
        "raw_index": 11,
        "output_filename": "puntas-planas-cromo-vanadio-truper.webp",
        "codes": ["PPL-1", "PPL-2", "PPL-3", "12875", "12876"],
        "description": "Puntas planas de encastre hexagonal de 1/4\" Truper"
    },
    {
        "id": "puntas-torx-seguridad-truper",
        "title": "Puntas tipo Torx con guía de seguridad Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 317,
        "raw_index": 13,
        "output_filename": "puntas-torx-seguridad-truper.webp",
        "codes": ["PTX-10", "PTX-15", "PTX-20", "PTX-25", "12880", "12881"],
        "description": "Puntas Torx inviolables para automotriz y electrónica Truper"
    },
    {
        "id": "adaptador-magnetico-puntas-truper",
        "title": "Adaptadores magnéticos para puntas hexagonales Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 317,
        "raw_index": 18,
        "output_filename": "adaptador-magnetico-puntas-truper.webp",
        "codes": ["ADA-MAG", "12890"],
        "description": "Portapuntas magnético de 2-1/2 pulgadas de acople rápido Truper"
    },
    {
        "id": "extension-flexible-para-puntas-truper",
        "title": "Extensiones flexibles articuladas para puntas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 317,
        "raw_index": 21,
        "output_filename": "extension-flexible-para-puntas-truper.webp",
        "codes": ["EXT-FLEX", "12895"],
        "description": "Extensión flexible para acceder a tornillos en ángulos estrechos y difíciles Truper"
    },
    {
        "id": "dados-estandar-cuadro-1-2-truper",
        "title": "Dados estándar cuadro 1/2' de 6 puntas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 0,
        "output_filename": "dados-estandar-cuadro-1-2-truper.webp",
        "codes": ["D-1210", "D-1212", "D-1214", "D-1216", "D-1218", "D-1220", "13200", "13201"],
        "description": "Dados individuales en pulgadas forjados en acero al cromo vanadio cuadro 1/2\" Truper"
    },
    {
        "id": "dados-milimetricos-cuadro-1-2-truper",
        "title": "Dados milimétricos cuadro 1/2' de 6 puntas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 4,
        "output_filename": "dados-milimetricos-cuadro-1-2-truper.webp",
        "codes": ["D-1210M", "D-1212M", "D-1213M", "D-1214M", "D-1215M", "D-1217M", "D-1219M", "13210", "13211"],
        "description": "Dados métricos individuales de alta resistencia para mecánica cuadro 1/2\" Truper"
    },
    {
        "id": "dados-estandar-cuadro-3-8-truper",
        "title": "Dados estándar cuadro 3/8' Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 10,
        "output_filename": "dados-estandar-cuadro-3-8-truper.webp",
        "codes": ["D-3808", "D-3810", "D-3812", "D-3814", "D-3816", "13220", "13221"],
        "description": "Dados individuales estándar para matraca de 3/8\" Truper"
    },
    {
        "id": "dados-milimetricos-cuadro-3-8-truper",
        "title": "Dados milimétricos cuadro 3/8' Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 12,
        "output_filename": "dados-milimetricos-cuadro-3-8-truper.webp",
        "codes": ["D-3808M", "D-3810M", "D-3812M", "D-3813M", "D-3814M", "13230", "13231"],
        "description": "Dados individuales milimétricos para matraca de 3/8\" Truper"
    },
    {
        "id": "dados-estandar-cuadro-1-4-truper",
        "title": "Dados estándar cuadro 1/4' Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 13,
        "output_filename": "dados-estandar-cuadro-1-4-truper.webp",
        "codes": ["D-1404", "D-1405", "D-1406", "D-1407", "D-1408", "13240", "13241"],
        "description": "Dados individuales de 6 puntas cuadro de 1/4\" Truper"
    },
    {
        "id": "dados-milimetricos-cuadro-1-4-truper",
        "title": "Dados milimétricos cuadro 1/4' Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 15,
        "output_filename": "dados-milimetricos-cuadro-1-4-truper.webp",
        "codes": ["D-1404M", "D-1405M", "D-1406M", "D-1407M", "D-1408M", "13250", "13251"],
        "description": "Dados métricos pequeños cuadro 1/4\" para taller y electrónica Truper"
    },
    {
        "id": "extension-para-matraca-cuadro-1-2-truper",
        "title": "Extensiones de acero para matraca cuadro 1/2' Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 16,
        "output_filename": "extension-para-matraca-cuadro-1-2-truper.webp",
        "codes": ["EXT-1205", "EXT-1210", "13260", "13261"],
        "description": "Barras de extensión para dados con terminación cromo vanadio pulido Truper"
    },
    {
        "id": "nudo-universal-articulado-truper",
        "title": "Nudos universales articulados para dados Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 128,
        "raw_index": 17,
        "output_filename": "nudo-universal-articulado-truper.webp",
        "codes": ["NU-12", "NU-38", "NU-14", "13270", "13271"],
        "description": "Articulación flexible para matraca cuadros 1/2\", 3/8\" y 1/4\" Truper"
    },

    # -------------------------------------------------------------------------
    # 6. Desarmadores Especializados, de Golpe y Joyero (12)
    # -------------------------------------------------------------------------
    {
        "id": "desarmador-de-golpe-plano-truper",
        "title": "Desarmadores de golpe punta plana Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 5,
        "output_filename": "desarmador-de-golpe-plano-truper.webp",
        "codes": ["DPG-1/4X4", "DPG-5/16X6", "DPG-3/8X8", "14200", "14201", "7922", "7924"],
        "description": "Desarmador con barra hexagonal continua y casquillo metálico para impacto Truper"
    },
    {
        "id": "desarmador-de-golpe-phillips-truper",
        "title": "Desarmadores de golpe punta Phillips Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 6,
        "output_filename": "desarmador-de-golpe-phillips-truper.webp",
        "codes": ["DPG-1/4X4P", "DPG-5/16X6P", "14205", "14206", "7923", "7925"],
        "description": "Desarmador de impacto para tornillos agarrotados con punta cruz magnética Truper"
    },
    {
        "id": "desarmador-acetato-plano-truper",
        "title": "Desarmadores con mango de acetato punta plana Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 7,
        "output_filename": "desarmador-acetato-plano-truper.webp",
        "codes": ["DA-3/16X4", "DA-1/4X4", "DA-1/4X6", "DA-5/16X6", "14210", "14211", "7362", "6955"],
        "description": "Desarmador clásico con mango de acetato transparente resistente a solventes Truper"
    },
    {
        "id": "desarmador-acetato-phillips-truper",
        "title": "Desarmadores con mango de acetato punta Phillips Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 9,
        "output_filename": "desarmador-acetato-phillips-truper.webp",
        "codes": ["DA-1/4X4P", "DA-1/4X6P", "14215", "14216", "7102", "6990"],
        "description": "Desarmador de punta de cruz con mango de acetato ergonómico de alta torsión Truper"
    },
    {
        "id": "desarmador-polipropileno-basic-plano-pretul",
        "title": "Desarmadores Basic punta plana Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 11,
        "output_filename": "desarmador-polipropileno-basic-plano-pretul.webp",
        "codes": ["DP-3/16X4", "DP-1/4X4", "DP-1/4X6", "24210", "24211", "7094"],
        "description": "Desarmador económico con mango plástico de polipropileno ranurado Pretul"
    },
    {
        "id": "desarmador-polipropileno-basic-phillips-pretul",
        "title": "Desarmadores Basic punta Phillips Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 12,
        "output_filename": "desarmador-polipropileno-basic-phillips-pretul.webp",
        "codes": ["DP-1/4X4P", "DP-1/4X6P", "24215", "24216", "7103", "6991"],
        "description": "Desarmador de cruz económico mango de polipropileno Pretul"
    },
    {
        "id": "desarmador-cabinet-delgado-truper",
        "title": "Desarmadores delgados tipo cabinet Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 13,
        "output_filename": "desarmador-cabinet-delgado-truper.webp",
        "codes": ["DC-1/8X4", "DC-1/8X6", "DC-1/8X8", "14220", "14221", "7129", "7149", "7366", "7368"],
        "description": "Desarmador de varilla delgada recta para terminales eléctricas y tableros Truper"
    },
    {
        "id": "desarmador-puntas-intercambiables-multiusos-truper",
        "title": "Desarmadores multiusos con puntas intercambiables Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 142,
        "raw_index": 15,
        "output_filename": "desarmador-puntas-intercambiables-multiusos-truper.webp",
        "codes": ["DM-6", "DM-4", "14230", "7363"],
        "description": "Desarmador versátil 6 en 1 con puntas reversibles y mango bimaterial Truper"
    },
    {
        "id": "desarmadores-de-precision-joyero-truper",
        "title": "Juegos de desarmadores de precisión tipo joyero Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 143,
        "raw_index": 13,
        "output_filename": "desarmadores-de-precision-joyero-truper.webp",
        "codes": ["JOY-6", "JOY-8", "14240", "14241"],
        "description": "Juego de desarmadores con cabeza giratoria en estuche plástico para electrónica Truper"
    },
    {
        "id": "desarmadores-de-precision-joyero-pretul",
        "title": "Juegos de desarmadores de precisión tipo joyero Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 143,
        "raw_index": 14,
        "output_filename": "desarmadores-de-precision-joyero-pretul.webp",
        "codes": ["JOY-6P", "24240"],
        "description": "Juego de 6 piezas de desarmadores miniatura para relojería y gafas Pretul"
    },
    {
        "id": "juego-desarmadores-basic-pretul",
        "title": "Juegos de desarmadores con organizador Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 143,
        "raw_index": 15,
        "output_filename": "juego-desarmadores-basic-pretul.webp",
        "codes": ["J-DP-6P", "J-DP-4P", "24250", "24251"],
        "description": "Juego surtido de desarmadores planos y de cruz para el hogar Pretul"
    },
    {
        "id": "desarmador-stubby-trompo-truper",
        "title": "Desarmadores cortos tipo trompo (Stubby) Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 143,
        "raw_index": 18,
        "output_filename": "desarmador-stubby-trompo-truper.webp",
        "codes": ["DT-1/4", "DT-1/4P", "14260", "14261"],
        "description": "Desarmadores ultracortos de alta fuerza de palanca para espacios reducidos Truper"
    },

    # -------------------------------------------------------------------------
    # 7. Prensas, Sujeción, Remachadoras y Engrapadoras (17)
    # -------------------------------------------------------------------------
    {
        "id": "prensa-hierro-nodular-carpintero-truper",
        "title": "Prensas de hierro nodular tipo 'C' para carpintería Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 312,
        "raw_index": 1,
        "output_filename": "prensa-hierro-nodular-carpintero-truper.webp",
        "codes": ["PNT-1", "PNT-2", "PNT-3", "PNT-4", "PNT-5", "PNT-6", "PNT-8", "17200", "17201", "17202", "17203", "17204", "17205", "7302", "7308"],
        "description": "Prensa forjada en hierro nodular de alta tenacidad con tornillo de rosca Acme Truper"
    },
    {
        "id": "prensa-hierro-nodular-pretul",
        "title": "Prensas de hierro nodular tipo 'C' Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 312,
        "raw_index": 2,
        "output_filename": "prensa-hierro-nodular-pretul.webp",
        "codes": ["PNT-2P", "PNT-3P", "PNT-4P", "PNT-5P", "PNT-6P", "27200", "27201", "27202", "27203"],
        "description": "Prensas tipo 'C' resistentes para taller escolar y carpintería Pretul"
    },
    {
        "id": "prensa-garganta-profunda-truper",
        "title": "Prensas de garganta profunda para carpintería Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 312,
        "raw_index": 3,
        "output_filename": "prensa-garganta-profunda-truper.webp",
        "codes": ["PNT-2G", "PNT-3G", "17210", "17211", "7337", "7338"],
        "description": "Prensa con mayor profundidad de alcance para piezas anchas de madera Truper"
    },
    {
        "id": "prensa-de-resorte-mordaza-movil-truper",
        "title": "Prensas de resorte con mordaza móvil Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 312,
        "raw_index": 4,
        "output_filename": "prensa-de-resorte-mordaza-movil-truper.webp",
        "codes": ["PRE-4", "PRE-6", "PRE-8", "17220", "17221", "17222"],
        "description": "Prensa plástica de alta presión por resorte con puntas articuladas Truper"
    },
    {
        "id": "prensa-esquinera-aluminio-truper",
        "title": "Prensas esquineras de aluminio 3' para marcos Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 313,
        "raw_index": 7,
        "output_filename": "prensa-esquinera-aluminio-truper.webp",
        "codes": ["PESQ-3", "17230"],
        "description": "Prensa para uniones a 90 grados en cancelería, marcos de madera y cuadros Truper"
    },
    {
        "id": "prensa-de-ajuste-rapido-barra-f-truper",
        "title": "Prensas de ajuste rápido tipo barra F Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 313,
        "raw_index": 10,
        "output_filename": "prensa-de-ajuste-rapido-barra-f-truper.webp",
        "codes": ["PFA-6", "PFA-12", "PFA-18", "PFA-24", "17240", "17241"],
        "description": "Prensa de gatillo con gatillo de liberación rápida y barra de acero Truper"
    },
    {
        "id": "prensa-de-cadena-para-tubo-truper",
        "title": "Prensas de cadena para tubo 2-1/2' Truper",
        "brand": "Truper",
        "category": "Plomería",
        "page": 314,
        "raw_index": 1,
        "output_filename": "prensa-de-cadena-para-tubo-truper.webp",
        "codes": ["PTU-25C", "17250"],
        "description": "Prensa con mordazas de aleación y cadena templada para sujeción de tuberías pesadas Truper"
    },
    {
        "id": "prensa-de-yugo-para-tubo-truper",
        "title": "Prensas de yugo articuladas para tubo Truper",
        "brand": "Truper",
        "category": "Plomería",
        "page": 314,
        "raw_index": 4,
        "output_filename": "prensa-de-yugo-para-tubo-truper.webp",
        "codes": ["PTU-20", "17255"],
        "description": "Prensa con base de hierro maleable para banco de trabajo Truper"
    },
    {
        "id": "remachadora-profesional-9-truper",
        "title": "Remachadoras manuales profesionales 9' Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 325,
        "raw_index": 0,
        "output_filename": "remachadora-profesional-9-truper.webp",
        "codes": ["RE-9", "RE-9X", "17800", "17801", "7737", "7736"],
        "description": "Remachadora con cuerpo de aluminio forjado y 4 boquillas para remaches ciegos Truper"
    },
    {
        "id": "remachadora-pretul-10",
        "title": "Remachadoras manuales 10' Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 325,
        "raw_index": 1,
        "output_filename": "remachadora-pretul-10-pretul.webp",
        "codes": ["RE-10P", "RE-10PX", "27800", "27801", "7739", "7740"],
        "description": "Remachadora de palanca con llavín para boquillas Pretul"
    },
    {
        "id": "remachadora-tipo-acordeon-truper",
        "title": "Remachadoras tipo acordeón de servicio pesado Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 325,
        "raw_index": 2,
        "output_filename": "remachadora-tipo-acordeon-truper.webp",
        "codes": ["RE-AC", "17810"],
        "description": "Remachadora telescópica de alto apalancamiento para remaches de acero y aluminio Truper"
    },
    {
        "id": "remachadora-neumatica-industrial-truper",
        "title": "Remachadoras neumáticas industriales de aire Truper",
        "brand": "Truper",
        "category": "Herramientas Eléctricas",
        "page": 325,
        "raw_index": 3,
        "output_filename": "remachadora-neumatica-industrial-truper.webp",
        "codes": ["TPN-883", "TPN-884", "17820", "17821"],
        "description": "Remachadora neumática de alta velocidad para líneas de ensamble y carrozados Truper"
    },
    {
        "id": "engrapadora-tipo-pistola-uso-pesado-truper",
        "title": "Engrapadoras tipo pistola de uso pesado Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 164,
        "raw_index": 1,
        "output_filename": "engrapadora-tipo-pistola-uso-pesado-truper.webp",
        "codes": ["ET-50", "ET-50X", "17900", "17901"],
        "description": "Engrapadora metálica de alta potencia para grapas de 1/4\" a 9/16\" Truper"
    },
    {
        "id": "engrapadora-tipo-pistola-pretul",
        "title": "Engrapadoras tipo pistola con grapas Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 164,
        "raw_index": 2,
        "output_filename": "engrapadora-tipo-pistola-pretul.webp",
        "codes": ["ET-50P", "ET-21P", "27900", "27901"],
        "description": "Engrapadora para tapicería ligera y manualidades con 500 grapas incluidas Pretul"
    },
    {
        "id": "engrapadora-tipo-pistola-ligera-truper",
        "title": "Engrapadoras tipo pistola ligeras Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 164,
        "raw_index": 3,
        "output_filename": "engrapadora-tipo-pistola-ligera-truper.webp",
        "codes": ["ET-19", "ET-21", "17910", "17911"],
        "description": "Engrapadora compacta con mango ahulado antideslizante Truper"
    },
    {
        "id": "escuadra-de-combinacion-truper",
        "title": "Escuadras de combinación graduadas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 166,
        "raw_index": 0,
        "output_filename": "escuadra-de-combinacion-truper.webp",
        "codes": ["ECT-6", "ECT-12", "ECT-16", "17920", "17921", "17922", "7194"],
        "description": "Escuadra multifuncional de 12 pulgadas con nivel de gota y rayador metálico Truper"
    },
    {
        "id": "escuadra-falsa-mango-madera-truper",
        "title": "Escuadras falsas graduadas ajustables Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 166,
        "raw_index": 2,
        "output_filename": "escuadra-falsa-mango-madera-truper.webp",
        "codes": ["EFT-9X", "EFT-8", "17930", "17931", "8164"],
        "description": "Escuadra falsa con hoja de acero inoxidable y tuerca mariposa de bloqueo Truper"
    }
]

def pad_to_canvas(im, target_w=500, target_h=500, bg_color=(255, 255, 255)):
    """Centra la imagen en un lienzo cuadrado con fondo blanco puro sin distorsión."""
    im = im.convert("RGB")
    w, h = im.size
    scale = min(target_w / w, target_h / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), bg_color)
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    canvas.paste(im_resized, (paste_x, paste_y))
    return canvas

def is_blank_or_invalid(im):
    """Detecta si la imagen extraída está en blanco o carece de información visual."""
    rgb = im.convert("RGB")
    ext = rgb.getextrema()
    if ext == ((255, 255), (255, 255), (255, 255)):
        return True
    non_white = sum(1 for p in rgb.getdata() if p != (255, 255, 255))
    total_pixels = im.width * im.height
    if (non_white / total_pixels) < 0.005:
        return True
    return False

def extract_family_image(family):
    page = family["page"]
    raw_idx = family["raw_index"]
    out_file = family["output_filename"]
    out_path = os.path.join(OUTPUT_IMG_DIR, out_file)

    os.makedirs(TMP_DIR, exist_ok=True)
    prefix = os.path.join(TMP_DIR, f"p{page}")
    raw_png = f"{prefix}-{raw_idx:03d}.png"

    if not os.path.exists(raw_png):
        subprocess.run(["pdfimages", "-png", "-f", str(page), "-l", str(page), PDF_PATH, prefix], check=True)

    if not os.path.exists(raw_png):
        print(f"[!] Archivo de imagen cruda no encontrado: {raw_png}", file=sys.stderr)
        return False

    with Image.open(raw_png) as im:
        if is_blank_or_invalid(im):
            print(f"[!] Advertencia: Imagen cruda vacía en página {page} índice {raw_idx} ({out_file})")
            return False
        normalized = pad_to_canvas(im, 500, 500)
        normalized.save(out_path, "WEBP", quality=88)

    return True

def run():
    print("=" * 75)
    print("MÓDULO A: EXTRACCIÓN DE 100 NUEVAS FAMILIAS TRUPER (TOTAL META: 360)")
    print("=" * 75)

    if not os.path.exists(PDF_PATH):
        print(f"[!] Error: No se encontró el catálogo en {PDF_PATH}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)

    # 1. Cargar manifiesto existente
    with open(MANIFEST_JSON, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    existing_groups = manifest.get("groups", [])
    existing_ids = set(g["id"] for g in existing_groups)
    print(f"[*] Grupos preexistentes en manifiesto: {len(existing_groups)}")

    # 2. Extraer y procesar imágenes del Módulo A
    print(f"[*] Extrayendo {len(MODULE_A_100_FAMILIES)} familias visuales del Módulo A...")
    new_extracted = 0
    for g in MODULE_A_100_FAMILIES:
        ok = extract_family_image(g)
        if not ok:
            print(f"[!] Error extrayendo imagen para {g['id']}")
            continue
        if g["id"] not in existing_ids:
            existing_groups.append(g)
            existing_ids.add(g["id"])
            new_extracted += 1
        else:
            idx = next(i for i, eg in enumerate(existing_groups) if eg["id"] == g["id"])
            existing_groups[idx] = g

    print(f"[✓] Nuevas familias visuales agregadas al catálogo: {new_extracted}")
    print(f"[✓] Total acumulado de familias en catálogo: {len(existing_groups)}")

    # 3. Cruzar con data/products.json
    print("[*] Cruzando nuevas familias con catálogo de la ferretería...")
    with open(PRODUCTS_JSON, "r", encoding="utf-8") as f:
        products = json.load(f)

    code_to_family = {}
    for g in existing_groups:
        for c in g.get("codes", []):
            code_to_family[c.strip().upper()] = g

    updated_skus = set()
    updated_products_list = []
    updated_count = 0

    for p in products:
        sku = str(p.get("sku", "")).strip().upper()
        mfg = str(p.get("manufacturer_code", "")).strip().upper()
        name = p.get("name", "").lower()
        old_img = p.get("image", "")

        # Preservar imágenes frecuentes de portada
        if any(f"prod-{it}.webp" in old_img for it in ["cinta", "pinza", "pija", "valvula", "desarmador"]):
            continue

        # Evitar marcas externas incompatibles o carbones/refacciones
        if any(b in name for b in ["irwin", "wurth", "3m"]):
            continue
        if "carbon p/" in name or "carbones" in name:
            continue

        matched_group = None
        match_reason = ""

        if sku in code_to_family:
            matched_group = code_to_family[sku]
            match_reason = f"SKU:{sku}"
        elif mfg in code_to_family:
            matched_group = code_to_family[mfg]
            match_reason = f"Clave:{mfg}"
        else:
            # Reglas semánticas guiadas de alta fidelidad
            for g in existing_groups:
                gid = g["id"]
                # Lonas
                if gid == "lona-pretul-azul" and "lona" in name and "azul" in name and ("pretul" in name or "lp-" in sku.lower()):
                    matched_group = g
                    match_reason = "Nombre:Lona Azul Pretul"
                    break
                elif gid == "lona-reforzada-azul-truper" and "lona" in name and "reforzada" in name and ("truper" in name or "lt-" in sku.lower()):
                    matched_group = g
                    match_reason = "Nombre:Lona Reforzada Truper"
                    break
                elif gid == "lona-pretul-naranja" and "lona" in name and "naranja" in name:
                    matched_group = g
                    match_reason = "Nombre:Lona Naranja"
                    break
                elif gid == "lona-pretul-verde" and "lona" in name and "verde" in name:
                    matched_group = g
                    match_reason = "Nombre:Lona Verde"
                    break
                elif gid == "lona-pretul-amarilla" and "lona" in name and "amarilla" in name:
                    matched_group = g
                    match_reason = "Nombre:Lona Amarilla"
                    break
                elif gid == "lona-pretul-roja" and "lona" in name and "roja" in name:
                    matched_group = g
                    match_reason = "Nombre:Lona Roja"
                    break
                elif gid == "lona-pretul-blanca" and "lona" in name and "blanca" in name:
                    matched_group = g
                    match_reason = "Nombre:Lona Blanca"
                    break
                # Cajas
                elif gid == "caja-herramientas-industrial-26-truper" and "caja" in name and "26" in name:
                    matched_group = g
                    match_reason = "Nombre:Caja 26 Truper"
                    break
                elif gid == "caja-herramientas-industrial-23-truper" and "caja" in name and "23" in name:
                    matched_group = g
                    match_reason = "Nombre:Caja 23 Truper"
                    break
                elif gid == "caja-herramientas-industrial-20-truper" and "caja" in name and "20" in name:
                    matched_group = g
                    match_reason = "Nombre:Caja 20 Truper"
                    break
                elif gid == "caja-herramientas-industrial-17-truper" and "caja" in name and "17" in name:
                    matched_group = g
                    match_reason = "Nombre:Caja 17 Truper"
                    break
                elif gid == "caja-herramientas-plastica-pretul-19" and "caja" in name and "19" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Caja 19 Pretul"
                    break
                elif gid == "caja-herramientas-plastica-pretul-16" and "caja" in name and "16" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Caja 16 Pretul"
                    break
                elif gid == "caja-herramientas-plastica-pretul-13" and "caja" in name and ("13" in name or "12" in name) and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Caja 13 Pretul"
                    break
                # Cintas
                elif gid == "cinta-aislar-33-negra-truper" and "cinta" in name and "aislar" in name and "negra" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Cinta Aislar Truper"
                    break
                elif gid == "cinta-teflon-sella-roscas-truper" and "cinta" in name and "teflon" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Cinta Teflon Truper"
                    break
                elif gid == "cinta-masking-tape-uso-general-truper" and "masking" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Masking Tape Truper"
                    break
                elif gid == "cinta-para-ducto-gris-truper" and "cinta" in name and "ducto" in name:
                    matched_group = g
                    match_reason = "Nombre:Cinta Ducto"
                    break
                # Cutters
                elif gid == "cutter-estandar-18mm-truper" and "cutter" in name and "6" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Cutter 6 Truper"
                    break
                elif gid == "cutter-alma-metalica-18mm-pretul" and "cutter" in name and "6" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Cutter 6 Pretul"
                    break
                # Prensas
                elif gid == "prensa-hierro-nodular-carpintero-truper" and "prensa" in name and "nodular" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Prensa Truper"
                    break
                elif gid == "remachadora-profesional-9-truper" and "remachadora" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Remachadora Truper"
                    break
                elif gid == "engrapadora-tipo-pistola-uso-pesado-truper" and "engrapadora" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Engrapadora Truper"
                    break
                elif gid == "escuadra-de-combinacion-truper" and "escuadra" in name and "combinacion" in name:
                    matched_group = g
                    match_reason = "Nombre:Escuadra Combinacion"
                    break

        if matched_group:
            rel_img = f"assets/images/products/truper/{matched_group['output_filename']}"
            p["image"] = rel_img
            p["image_url"] = rel_img
            if p.get("brand") in ["Homologado", "Herramientas Manuales"] and matched_group.get("brand"):
                p["brand"] = matched_group["brand"]
                p["brands"] = {"name": matched_group["brand"]}

            updated_count += 1
            if p.get("sku") not in updated_skus:
                updated_skus.add(p.get("sku"))
                updated_products_list.append({
                    "id": p.get("id"),
                    "sku": p.get("sku"),
                    "name": p.get("name"),
                    "brand": p.get("brand", matched_group["brand"]),
                    "matched_by": match_reason,
                    "group": matched_group["title"],
                    "old_image": old_img,
                    "new_image": rel_img
                })

    # Guardar data/products.json actualizado
    with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    # Actualizar manifiesto
    total_sku_mappings = sum(len(grp.get("codes", [])) for grp in existing_groups)
    manifest["total_catalog_groups"] = len(existing_groups)
    manifest["total_sku_mappings"] = total_sku_mappings
    manifest["total_store_products_updated"] = len(updated_products_list)
    manifest["groups"] = existing_groups
    manifest["updated_products"] = updated_products_list

    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 75)
    print("¡MÓDULO A COMPLETADO CON ÉXITO!")
    print(f"  - Total Familias Visuales en Manifiesto: {len(existing_groups)} (antes 260)")
    print(f"  - Total Códigos / Claves Catalogadas: {total_sku_mappings}")
    print(f"  - Total Artículos de Tienda con Fotos Oficiales: {len(updated_products_list)} (antes 275)")
    print("=" * 75)

if __name__ == "__main__":
    run()
