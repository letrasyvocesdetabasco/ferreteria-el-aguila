#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extract_module_d_145.py
Ferretería y Tlapalería El Águila - Módulo D: Extracción de 145 Nuevas Familias Truper

Módulo D (145 familias):
- Palas y Cavadores (Palas cuadradas, redondas, escarramán, zanjeras, carboneras, sanitarias) (20)
- Carretillas y Ruedas (Carretillas 4.5/5.5/6 ft3 metálicas y plásticas, ruedas impinchables y neumáticas) (15)
- Albañilería, Cucharas, Llanas y Azulejo (Llanas dentadas/lisas, cucharas Philadelphia/Guadalajara, cortadores) (35)
- Nivelación, Medición y Trazo (Flexómetros Gripper, cintas de cruceta, niveles de gota/torpedo, plomadas) (25)
- Brochas, Rodillos y Pintura (Brochas cerda natural/sintética, rodillos 9", felpas, manerales, charolas) (30)
- Espátulas, Raspadores, Marros y Demolición (Espátulas flexibles/rígidas, marros octagonales, cinceles, picos) (20)

Progreso acumulado: 566 -> 711 familias oficiales Truper.
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
TMP_DIR = "/tmp/mod_d_extract"

MODULE_D_145_FAMILIES = [
    # -------------------------------------------------------------------------
    # 1. Palas y Cavadores (20 familias, Páginas 291-294)
    # -------------------------------------------------------------------------
    {
        "id": "pala-cuadrada-puno-y-truper",
        "title": "Palas cuadradas con puño Y Truper Classic",
        "brand": "Truper",
        "category": "Construcción",
        "page": 291,
        "raw_index": 0,
        "output_filename": "pala-cuadrada-puno-y-truper.webp",
        "codes": ["PCY", "PCY-T", "17160", "17161"],
        "description": "Pala cuadrada con mango de madera y puño 'Y' de acero con agarradera plástica Truper"
    },
    {
        "id": "pala-cuadrada-mango-largo-truper",
        "title": "Palas cuadradas con mango largo recto Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 291,
        "raw_index": 16,
        "output_filename": "pala-cuadrada-mango-largo-truper.webp",
        "codes": ["PCL", "PCL-T", "17165", "17166"],
        "description": "Pala cuadrada con mango largo de madera de fresno americano para mayor palanca Truper"
    },
    {
        "id": "pala-cuadrada-puno-y-pretul",
        "title": "Palas cuadradas puño Y Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 291,
        "raw_index": 8,
        "output_filename": "pala-cuadrada-puno-y-pretul.webp",
        "codes": ["PCY-P", "20160", "20161"],
        "description": "Pala cuadrada de construcción económica con cabeza de acero al carbono Pretul"
    },
    {
        "id": "pala-cuadrada-mango-largo-pretul",
        "title": "Palas cuadradas mango largo Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 291,
        "raw_index": 20,
        "output_filename": "pala-cuadrada-mango-largo-pretul.webp",
        "codes": ["PCL-P", "20165", "20166"],
        "description": "Pala cuadrada de uso ligero con mango recto de madera pulida Pretul"
    },
    {
        "id": "pala-redonda-puno-y-truper",
        "title": "Palas redondas con puño Y Truper Classic",
        "brand": "Truper",
        "category": "Construcción",
        "page": 292,
        "raw_index": 0,
        "output_filename": "pala-redonda-puno-y-truper.webp",
        "codes": ["PRY", "PRY-T", "17170", "17171"],
        "description": "Pala redonda forjada en acero al carbono con hombros doblados hacia adelante Truper"
    },
    {
        "id": "pala-redonda-mango-largo-truper",
        "title": "Palas redondas con mango largo recto Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 292,
        "raw_index": 9,
        "output_filename": "pala-redonda-mango-largo-truper.webp",
        "codes": ["PRL", "PRL-T", "17175", "17176"],
        "description": "Pala redonda de excavación con mango largo ergonómico de madera de fresno Truper"
    },
    {
        "id": "pala-redonda-puno-y-pretul",
        "title": "Palas redondas puño Y Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 292,
        "raw_index": 2,
        "output_filename": "pala-redonda-puno-y-pretul.webp",
        "codes": ["PRY-P", "20170", "20171"],
        "description": "Pala redonda básica para albañilería y jardinería con puño de polipropileno Pretul"
    },
    {
        "id": "pala-redonda-mango-largo-pretul",
        "title": "Palas redondas mango largo Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 292,
        "raw_index": 11,
        "output_filename": "pala-redonda-mango-largo-pretul.webp",
        "codes": ["PRL-P", "20175", "20176"],
        "description": "Pala redonda ligera para excavación de zanjas y trasvase de tierra Pretul"
    },
    {
        "id": "pala-carbonera-puno-y-truper",
        "title": "Palas carboneras con puño Y Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 293,
        "raw_index": 14,
        "output_filename": "pala-carbonera-puno-y-truper.webp",
        "codes": ["PACAR", "PACAR-Y", "17180", "17181"],
        "description": "Pala carbonera de tolva ancha de gran capacidad para granos, carbón y áridos Truper"
    },
    {
        "id": "pala-escarraman-zanja-truper",
        "title": "Palas tipo escarramán para drenaje y zanja Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 293,
        "raw_index": 0,
        "output_filename": "pala-escarraman-zanja-truper.webp",
        "codes": ["PESC", "PESC-Y", "17185", "17186"],
        "description": "Pala escarramán de hoja angosta y curva para excavar zanjas profundas de tubería Truper"
    },
    {
        "id": "pala-sanitaria-polipropileno-truper",
        "title": "Palas sanitarias de polipropileno blanco Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 294,
        "raw_index": 3,
        "output_filename": "pala-sanitaria-polipropileno-truper.webp",
        "codes": ["P-SANI", "17190", "17191"],
        "description": "Pala sanitaria higiénica de plástico grado alimenticio de una sola pieza Truper"
    },
    {
        "id": "pala-irrigacion-mango-largo-truper",
        "title": "Palas para irrigación mango largo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 294,
        "raw_index": 4,
        "output_filename": "pala-irrigacion-mango-largo-truper.webp",
        "codes": ["P-IRRI", "17195", "17196"],
        "description": "Pala de irrigación con hombros rectos para limpieza de canales y acequias Truper"
    },
    {
        "id": "pala-pocera-mango-largo-truper",
        "title": "Palas poceras para excavación profunda Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 292,
        "raw_index": 5,
        "output_filename": "pala-pocera-mango-largo-truper.webp",
        "codes": ["PPOC", "17198", "17199"],
        "description": "Pala pocera de hoja extendida especial para excavar pozos estrechos y cimientos Truper"
    },
    {
        "id": "cavador-agricola-doble-mango-truper",
        "title": "Cavadores agrícolas dobles para postes Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 294,
        "raw_index": 12,
        "output_filename": "cavador-agricola-doble-mango-truper.webp",
        "codes": ["CAV-P", "17200", "17201"],
        "description": "Cavador de dos hojas encontradas con mangos de madera para colocación de postes Truper"
    },
    {
        "id": "pala-plegable-campismo-truper",
        "title": "Palas plegables tácticas de acero al carbono Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 291,
        "raw_index": 27,
        "output_filename": "pala-plegable-campismo-truper.webp",
        "codes": ["PAL-PLEG", "17210"],
        "description": "Pala plegable compacta con sierra lateral y funda de transporte para emergencia y campo Truper"
    },
    {
        "id": "pala-cuadrada-fibra-vidrio-truper-expert",
        "title": "Palas cuadradas con mango de fibra de vidrio Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 291,
        "raw_index": 12,
        "output_filename": "pala-cuadrada-fibra-vidrio-truper-expert.webp",
        "codes": ["PCY-F", "17215", "17216"],
        "description": "Pala cuadrada de uso rudo con mango dieléctrico de fibra de vidrio irrompible Truper Expert"
    },
    {
        "id": "pala-redonda-fibra-vidrio-truper-expert",
        "title": "Palas redondas con mango de fibra de vidrio Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 292,
        "raw_index": 7,
        "output_filename": "pala-redonda-fibra-vidrio-truper-expert.webp",
        "codes": ["PRY-F", "17220", "17221"],
        "description": "Pala redonda con núcleo de fibra de vidrio y mango ergonómico antideslizante Truper Expert"
    },
    {
        "id": "pala-cuchara-granelera-aluminio-truper",
        "title": "Palas graneleras de aluminio de alta resistencia Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 293,
        "raw_index": 13,
        "output_filename": "pala-cuchara-granelera-aluminio-truper.webp",
        "codes": ["PALU", "17225"],
        "description": "Pala de aluminio ultraligera anticorrosiva para manejo de semillas y granos Truper"
    },
    {
        "id": "pala-cajon-nieve-granos-plastica-truper",
        "title": "Palas de plástico tipo cajón para granos y nieve Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 293,
        "raw_index": 15,
        "output_filename": "pala-cajon-nieve-granos-plastica-truper.webp",
        "codes": ["P-PLAS", "17230"],
        "description": "Pala con concha profunda de plástico virgen y borde reforzado con tira de acero Truper"
    },
    {
        "id": "pala-infantil-jardin-truper-kids",
        "title": "Palas pequeñas infantiles para jardín Truper Kids",
        "brand": "Truper",
        "category": "Construcción",
        "page": 195,
        "raw_index": 34,
        "output_filename": "pala-infantil-jardin-truper-kids.webp",
        "codes": ["PRL-KID", "PCL-KID", "17239", "19712"],
        "description": "Pala infantil de acero ligero y mango de madera pulida para niños Truper Kids"
    },

    # -------------------------------------------------------------------------
    # 2. Carretillas y Ruedas (15 familias, Páginas 84-88)
    # -------------------------------------------------------------------------
    {
        "id": "carretilla-4-5-ft3-metalica-truper",
        "title": "Carretillas con concha metálica 4.5 ft3 Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 84,
        "raw_index": 3,
        "output_filename": "carretilla-4-5-ft3-metalica-truper.webp",
        "codes": ["CAT-45", "CAT-45ND", "11740", "11741"],
        "description": "Carretilla clásica para construcción con concha de lámina calibre 20 y bastidor de madera o acero Truper"
    },
    {
        "id": "carretilla-5-5-ft3-reforzada-truper",
        "title": "Carretillas reforzadas 5.5 ft3 concha metálica Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 84,
        "raw_index": 10,
        "output_filename": "carretilla-5-5-ft3-reforzada-truper.webp",
        "codes": ["CAT-55", "11745", "11746"],
        "description": "Carretilla de gran capacidad con refuerzo frontal y concha troquelada de alta rigidez Truper"
    },
    {
        "id": "carretilla-6-ft3-plastica-irrompible-truper",
        "title": "Carretillas con concha plástica 6 ft3 de polietileno Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 85,
        "raw_index": 4,
        "output_filename": "carretilla-6-ft3-plastica-irrompible-truper.webp",
        "codes": ["CAP-60", "CAP-60ND", "11750", "11751"],
        "description": "Carretilla para obra y jardinería con tolva plástica irrompible resistente a ácidos y químicos Truper"
    },
    {
        "id": "carretilla-obra-pretul-4-ft3",
        "title": "Carretillas para obra 4 ft3 Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 86,
        "raw_index": 5,
        "output_filename": "carretilla-obra-pretul-4-ft3.webp",
        "codes": ["CAP-4P", "20740", "20741"],
        "description": "Carretilla económica para uso doméstico y ligera en obra con llanta neumática Pretul"
    },
    {
        "id": "carretilla-bastidor-tubular-truper",
        "title": "Carretillas con bastidor tubular metálico continuo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 87,
        "raw_index": 7,
        "output_filename": "carretilla-bastidor-tubular-truper.webp",
        "codes": ["CAT-60BT", "11755"],
        "description": "Carretilla de uso pesado con chasis tubular de acero soldado de una sola pieza Truper"
    },
    {
        "id": "rueda-neumatica-reforzada-carretilla-truper",
        "title": "Ruedas neumáticas reforzadas para carretilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 88,
        "raw_index": 2,
        "output_filename": "rueda-neumatica-reforzada-carretilla-truper.webp",
        "codes": ["RN-C", "11760", "11761"],
        "description": "Llanta neumática de 16 pulgadas con rin de acero y rodamientos de bolas de alta durabilidad Truper"
    },
    {
        "id": "rueda-impinchable-solida-carretilla-truper",
        "title": "Ruedas impinchables de poliuretano sólido para carretilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 88,
        "raw_index": 3,
        "output_filename": "rueda-impinchable-solida-carretilla-truper.webp",
        "codes": ["RI-C", "11765", "11766"],
        "description": "Rueda sólida de microcelda de poliuretano que nunca se desinfla ni se pincha con clavos o escombros Truper"
    },
    {
        "id": "camara-de-repuesto-llanta-carretilla-truper",
        "title": "Cámaras de repuesto para llanta de carretilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 88,
        "raw_index": 4,
        "output_filename": "camara-de-repuesto-llanta-carretilla-truper.webp",
        "codes": ["CAM-C", "11770"],
        "description": "Cámara neumática de hule de alta elasticidad con válvula recta para carretillas de 16 pulgadas Truper"
    },
    {
        "id": "concha-de-repuesto-metalica-carretilla-truper",
        "title": "Conchas metálicas troqueladas de repuesto para carretilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 85,
        "raw_index": 6,
        "output_filename": "concha-de-repuesto-metalica-carretilla-truper.webp",
        "codes": ["CON-MET", "11775"],
        "description": "Bandeja de lámina de acero con pintura epóxica electrostática para recambio de carretilla Truper"
    },
    {
        "id": "concha-de-repuesto-plastica-carretilla-truper",
        "title": "Conchas plásticas de repuesto para carretilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 85,
        "raw_index": 8,
        "output_filename": "concha-de-repuesto-plastica-carretilla-truper.webp",
        "codes": ["CON-PLA", "11780"],
        "description": "Concha plástica gruesa de polietileno de alta resistencia al impacto y corrosión Truper"
    },
    {
        "id": "chumaceras-y-eje-para-carretilla-truper",
        "title": "Juegos de chumaceras, eje y herrajes para carretilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 88,
        "raw_index": 7,
        "output_filename": "chumaceras-y-eje-para-carretilla-truper.webp",
        "codes": ["J-CHUM", "11785"],
        "description": "Kit de refacciones con soportes de eje, tornillería y chumaceras de acero para carretillas Truper"
    },
    {
        "id": "mangos-madera-repuesto-carretilla-truper",
        "title": "Mangos de madera de repuesto para carretilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 85,
        "raw_index": 16,
        "output_filename": "mangos-madera-repuesto-carretilla-truper.webp",
        "codes": ["M-CAR", "11790"],
        "description": "Par de largueros de madera de encino o fresno maquinados con barrenos preperforados Truper"
    },
    {
        "id": "diablo-de-carga-tubular-200kg-truper",
        "title": "Diablos de carga tubulares para almacén 200 kg Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 86,
        "raw_index": 11,
        "output_filename": "diablo-de-carga-tubular-200kg-truper.webp",
        "codes": ["DIA-200", "11795"],
        "description": "Carretilla vertical tipo diablo para transporte de cajas y bultos pesados de acero esmaltado Truper"
    },
    {
        "id": "plataforma-de-carga-plegable-truper",
        "title": "Carritos plataforma de carga plegables para almacén Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 87,
        "raw_index": 11,
        "output_filename": "plataforma-de-carga-plegable-truper.webp",
        "codes": ["PLAT-150", "PLAT-300", "11800", "11801"],
        "description": "Plataforma de cuatro ruedas con manubrio abatible y superficie antiderrapante Truper"
    },
    {
        "id": "carretilla-infantil-metalica-truper-kids",
        "title": "Carretillas infantiles con concha metálica Truper Kids",
        "brand": "Truper",
        "category": "Construcción",
        "page": 195,
        "raw_index": 1,
        "output_filename": "carretilla-infantil-metalica-truper-kids.webp",
        "codes": ["CAR-KID", "10440", "11805"],
        "description": "Carretilla para niños a escala real con rueda de hule y concha metálica pintada Truper Kids"
    },

    # -------------------------------------------------------------------------
    # 3. Albañilería, Cucharas, Llanas y Azulejo (35 familias, Páginas 114-119, 210-212)
    # -------------------------------------------------------------------------
    {
        "id": "cuchara-albanil-philadelphia-truper",
        "title": "Cucharas para albañil tipo Philadelphia forjadas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 114,
        "raw_index": 4,
        "output_filename": "cuchara-albanil-philadelphia-truper.webp",
        "codes": ["CT-6", "CT-7", "CT-8", "CT-9", "CT-10", "11810", "11811", "11812"],
        "description": "Cuchara de una sola pieza forjada en acero al carbono con mango de madera y casquillo metálico Truper"
    },
    {
        "id": "cuchara-albanil-guadalajara-truper",
        "title": "Cucharas para albañil tipo Guadalajara cantos rectos Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 114,
        "raw_index": 8,
        "output_filename": "cuchara-albanil-guadalajara-truper.webp",
        "codes": ["CG-7", "CG-8", "CG-9", "CG-10", "11815", "11816"],
        "description": "Cuchara con hoja ancha de terminación recta para cargar mayor volumen de mortero y mezcla Truper"
    },
    {
        "id": "cuchara-albanil-philadelphia-pretul",
        "title": "Cucharas para albañil tipo Philadelphia Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 114,
        "raw_index": 11,
        "output_filename": "cuchara-albanil-philadelphia-pretul.webp",
        "codes": ["CP-6", "CP-7", "CP-8", "CP-9", "20810", "20811"],
        "description": "Cuchara de albañil económica con mango de madera encerado Pretul"
    },
    {
        "id": "cuchara-albanil-comfort-grip-truper-expert",
        "title": "Cucharas para albañil con mango Comfort Grip Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 115,
        "raw_index": 0,
        "output_filename": "cuchara-albanil-comfort-grip-truper-expert.webp",
        "codes": ["CTX-8", "CTX-9", "CTX-10", "11820", "11821"],
        "description": "Cuchara forjada con mango bimaterial antiderrapante de alta absorción de vibraciones Truper Expert"
    },
    {
        "id": "cucharin-para-yesero-truper",
        "title": "Cucharines punta aguda para yesero y molduras Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 115,
        "raw_index": 16,
        "output_filename": "cucharin-para-yesero-truper.webp",
        "codes": ["CY-5", "CY-6", "11825"],
        "description": "Cucharín de dimensiones compactas para detalles finos de estuco, yeso y remates Truper"
    },
    {
        "id": "llana-lisa-acero-mango-madera-truper",
        "title": "Llanas lisas de acero al carbono con mango de madera Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 119,
        "raw_index": 0,
        "output_filename": "llana-lisa-acero-mango-madera-truper.webp",
        "codes": ["LL-L", "11830", "11831"],
        "description": "Llana plana de 11 x 5 pulgadas con hoja pulida espejo para acabado liso de muros y pisos Truper"
    },
    {
        "id": "llana-dentada-cuadrada-truper",
        "title": "Llanas dentadas de dientes cuadrados para loseta Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 119,
        "raw_index": 2,
        "output_filename": "llana-dentada-cuadrada-truper.webp",
        "codes": ["LL-D1/4", "LL-D1/2", "11835", "11836"],
        "description": "Llana dentada para esparcir y peinar adhesivo pegazulejo con muescas cuadradas de 1/4\" y 1/2\" Truper"
    },
    {
        "id": "llana-dentada-triangular-truper",
        "title": "Llanas dentadas de dientes triangulares para azulejo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 119,
        "raw_index": 3,
        "output_filename": "llana-dentada-triangular-truper.webp",
        "codes": ["LL-DT", "11840"],
        "description": "Llana con dientes triangulares en 'V' ideal para colocación de azulejo y cerámica en muro Truper"
    },
    {
        "id": "llana-lisa-acero-inoxidable-truper-expert",
        "title": "Llanas lisas de acero inoxidable Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 119,
        "raw_index": 4,
        "output_filename": "llana-lisa-acero-inoxidable-truper-expert.webp",
        "codes": ["LLX-L", "11845"],
        "description": "Llana inoxidable antiflexión con soporte de aluminio ultraligero remachado Truper Expert"
    },
    {
        "id": "llana-esquinera-interior-exterior-truper",
        "title": "Llanas esquineras para esquinas interiores y exteriores Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 119,
        "raw_index": 5,
        "output_filename": "llana-esquinera-interior-exterior-truper.webp",
        "codes": ["LL-ESQ-IN", "LL-ESQ-EX", "11850", "11851"],
        "description": "Llana angular a 90 grados para perfilado perfecto de aristas en yeso y pasta Truper"
    },
    {
        "id": "llana-dentada-pretul",
        "title": "Llanas dentadas económicas para albañilería Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 119,
        "raw_index": 6,
        "output_filename": "llana-dentada-pretul.webp",
        "codes": ["LLP-D", "20835"],
        "description": "Llana dentada básica con mango ergonómico de plástico resistente Pretul"
    },
    {
        "id": "llana-lisa-pretul",
        "title": "Llanas lisas para empaste Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 210,
        "raw_index": 0,
        "output_filename": "llana-lisa-pretul.webp",
        "codes": ["LLP-L", "20830"],
        "description": "Llana plana para aplicación uniforme de tirol, pasta y acabados Pretul"
    },
    {
        "id": "flota-de-esponja-para-acabados-truper",
        "title": "Flotas de esponja de hule para acabado fino Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 210,
        "raw_index": 1,
        "output_filename": "flota-de-esponja-para-acabados-truper.webp",
        "codes": ["FL-ESP", "11855"],
        "description": "Flota con base de esponja poro fino para pulir revoques y aplanados de cemento Truper"
    },
    {
        "id": "flota-de-hule-para-emboquillado-truper",
        "title": "Flotas de hule para emboquillador y junteador Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 210,
        "raw_index": 2,
        "output_filename": "flota-de-hule-para-emboquillado-truper.webp",
        "codes": ["FL-HUL", "11860"],
        "description": "Flota de goma compacta biselada para embutir boquilla en juntas de azulejo y piso Truper"
    },
    {
        "id": "flota-de-madera-para-aplanado-truper",
        "title": "Flotas de madera para aplanado rústico Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 210,
        "raw_index": 3,
        "output_filename": "flota-de-madera-para-aplanado-truper.webp",
        "codes": ["FL-MAD", "11865"],
        "description": "Flota de madera de pino curada con mango anatómico para repellado de mortero Truper"
    },
    {
        "id": "revolvedor-de-pintura-y-mezcla-truper",
        "title": "Revolvedores mezcladores helicoidales para taladro Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 212,
        "raw_index": 6,
        "output_filename": "revolvedor-de-pintura-y-mezcla-truper.webp",
        "codes": ["REV-P", "REV-M", "11870", "11871"],
        "description": "Varilla mezcladora con aspas de acero galvanizado con zanco hexagonal para taladro Truper"
    },
    {
        "id": "cortador-de-azulejo-manual-40cm-truper",
        "title": "Cortadores manuales de azulejo de 40 cm Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 114,
        "raw_index": 1,
        "output_filename": "cortador-de-azulejo-manual-40cm-truper.webp",
        "codes": ["CAZ-40", "11875"],
        "description": "Cortadora de azulejo con rieles de acero sólido y cuchilla de carburo de tungsteno Truper"
    },
    {
        "id": "cortador-de-azulejo-manual-60cm-truper-expert",
        "title": "Cortadores de azulejo profesionales 60 cm con balero Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 114,
        "raw_index": 2,
        "output_filename": "cortador-de-azulejo-manual-60cm-truper-expert.webp",
        "codes": ["CAZX-60", "11880"],
        "description": "Cortadora profesional para porcelanato de gran formato con baleros de deslizamiento suave Truper Expert"
    },
    {
        "id": "cuchilla-repuesto-cortador-azulejo-truper",
        "title": "Cuchillas de repuesto con balero para cortador de azulejo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 115,
        "raw_index": 0,
        "output_filename": "cuchilla-repuesto-cortador-azulejo-truper.webp",
        "codes": ["REP-CAZ", "11885"],
        "description": "Rodel de carburo de tungsteno recubierto de titanio para cortes precisos en cerámica Truper"
    },
    {
        "id": "anclas-niveladoras-para-porcelanato-truper",
        "title": "Anclas niveladoras desechables para piso y azulejo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 116,
        "raw_index": 3,
        "output_filename": "anclas-niveladoras-para-porcelanato-truper.webp",
        "codes": ["AN-NIV1", "AN-NIV2", "11890", "11891"],
        "description": "Bolsa de clips anclas de nivelación de polipropileno para evitar cejas en pisos cerámicos Truper"
    },
    {
        "id": "cunas-reutilizables-nivelacion-azulejo-truper",
        "title": "Cuñas niveladoras reutilizables para azulejo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 116,
        "raw_index": 5,
        "output_filename": "cunas-reutilizables-nivelacion-azulejo-truper.webp",
        "codes": ["CU-NIV", "11895"],
        "description": "Cuñas plásticas estriadas de alta densidad reutilizables para sistema de nivelación Truper"
    },
    {
        "id": "pinza-para-sistema-nivelacion-azulejo-truper",
        "title": "Pinzas ajustables para sistema de nivelación de azulejo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 116,
        "raw_index": 14,
        "output_filename": "pinza-para-sistema-nivelacion-azulejo-truper.webp",
        "codes": ["PIN-NIV", "11900"],
        "description": "Alicate metálico regulable para apriete uniforme de cuñas sin quebrar las piezas cerámicas Truper"
    },
    {
        "id": "crucetas-separadoras-azulejo-truper",
        "title": "Crucetas separadoras espaciadoras para loseta Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 116,
        "raw_index": 15,
        "output_filename": "crucetas-separadoras-azulejo-truper.webp",
        "codes": ["CRUC-2", "CRUC-3", "CRUC-5", "11905", "11906"],
        "description": "Separadores plásticos en cruz de 2 mm, 3 mm y 5 mm para alineación perfecta de boquillas Truper"
    },
    {
        "id": "cortador-electrico-azulejo-disco-diamante-truper",
        "title": "Cortadores eléctricos de azulejo húmedo 7 pulgadas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 114,
        "raw_index": 4,
        "output_filename": "cortador-electrico-azulejo-disco-diamante-truper.webp",
        "codes": ["COZ-7", "11910"],
        "description": "Mesa cortadora eléctrica para cerámica con charola de enfriamiento por agua y guía graduada Truper"
    },
    {
        "id": "tenaza-para-azulejo-carburo-truper",
        "title": "Tenazas para azulejo con insertos de carburo de tungsteno Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 117,
        "raw_index": 22,
        "output_filename": "tenaza-para-azulejo-carburo-truper.webp",
        "codes": ["TEN-AZ", "11915"],
        "description": "Tenaza curva especial para mordisquear y realizar recortes redondos en azulejos para tuberías Truper"
    },
    {
        "id": "ventosa-sencilla-para-cristal-y-azulejo-truper",
        "title": "Ventosas sencillas de succión para cargar losetas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 211,
        "raw_index": 15,
        "output_filename": "ventosa-sencilla-para-cristal-y-azulejo-truper.webp",
        "codes": ["VEN-1", "11920"],
        "description": "Ventosa de hule sintético con palanca de vacío para mover vidrio y azulejo de hasta 40 kg Truper"
    },
    {
        "id": "ventosa-doble-para-porcelanato-truper",
        "title": "Ventosas dobles de aluminio para porcelanato pesado Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 211,
        "raw_index": 16,
        "output_filename": "ventosa-doble-para-porcelanato-truper.webp",
        "codes": ["VEN-2", "11925"],
        "description": "Ventosa de doble cabezal de aluminio inyectado para manipulación segura de placas de mármol Truper"
    },
    {
        "id": "ventosa-triple-industrial-para-vidrio-truper",
        "title": "Ventosas triples industriales de alta succión 100 kg Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 211,
        "raw_index": 17,
        "output_filename": "ventosa-triple-industrial-para-vidrio-truper.webp",
        "codes": ["VEN-3", "11930"],
        "description": "Ventosa triple de aleación de aluminio para cancelería y carga de grandes ventanales Truper"
    },
    {
        "id": "bidel-para-junta-azulejo-truper",
        "title": "Limpia juntas y rascadores de boquilla para azulejo Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 212,
        "raw_index": 7,
        "output_filename": "bidel-para-junta-azulejo-truper.webp",
        "codes": ["RAS-JUN", "11935"],
        "description": "Herramienta con cuchilla de carburo diamantado para remover boquilla vieja o manchada en baños Truper"
    },
    {
        "id": "escalímetro-triangular-arquitecto-truper",
        "title": "Escalímetros triangulares de plástico de alta precisión Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 212,
        "raw_index": 9,
        "output_filename": "escalimetro-triangular-arquitecto-truper.webp",
        "codes": ["ESCA-30", "11940"],
        "description": "Regla escalímetro de 30 cm con 6 escalas arquitectónicas diferentes grabadas con láser Truper"
    },
    {
        "id": "marcador-de-contorno-duplicador-truper",
        "title": "Calibradores duplicadores copiadores de contorno Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 212,
        "raw_index": 10,
        "output_filename": "marcador-de-contorno-duplicador-truper.webp",
        "codes": ["COP-CON", "11945"],
        "description": "Copiador de formas con láminas de plástico para trazar perfiles irregulares en azulejo y madera Truper"
    },
    {
        "id": "guia-para-ingletes-caja-madera-truper",
        "title": "Cajas de inglete plásticas con serrucho de costilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 212,
        "raw_index": 11,
        "output_filename": "guia-para-ingletes-caja-madera-truper.webp",
        "codes": ["CAJ-ING", "11950"],
        "description": "Caja para cortes a 45 y 90 grados con ranuras guía para zoclos y molduras decorativas Truper"
    },
    {
        "id": "cuchara-punta-redonda-truper",
        "title": "Cucharas de punta redonda para acabados especiales Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 114,
        "raw_index": 0,
        "output_filename": "cuchara-punta-redonda-truper.webp",
        "codes": ["CT-R8", "11955"],
        "description": "Cuchara forjada con punta circular para remates curvos y molduras de yeso Truper"
    },
    {
        "id": "cuchara-yesera-trapezoidal-truper",
        "title": "Cucharas yeseras trapezoidales para aplicación de mortero Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 119,
        "raw_index": 6,
        "output_filename": "cuchara-yesera-trapezoidal-truper.webp",
        "codes": ["CY-TRAP", "11960"],
        "description": "Cuchara trapezoidal para empaste uniforme en muros y plafones Truper"
    },
    {
        "id": "llana-chanfleada-para-yeso-truper",
        "title": "Llanas chanfleadas con bordes redondeados para masilla Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 210,
        "raw_index": 4,
        "output_filename": "llana-chanfleada-para-yeso-truper.webp",
        "codes": ["LL-CHAN", "11965"],
        "description": "Llana especial con extremos boleados que evita rayaduras al alisar acabados de microcemento Truper"
    },

    # -------------------------------------------------------------------------
    # 4. Nivelación, Medición y Trazo (25 familias, Páginas 174-175, 289-290, 166)
    # -------------------------------------------------------------------------
    {
        "id": "flexometro-gripper-contra-impacto-5m-truper",
        "title": "Flexómetros Gripper contra impacto de 5 metros Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 174,
        "raw_index": 16,
        "output_filename": "flexometro-gripper-contra-impacto-5m-truper.webp",
        "codes": ["FH-5M", "10740", "10741"],
        "description": "Flexómetro con cinta recubierta de nylon resistente a la abrasión y carcasa de ABS con sobremolde de hule Truper"
    },
    {
        "id": "flexometro-gripper-contra-impacto-8m-truper",
        "title": "Flexómetros Gripper contra impacto de 8 metros Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 174,
        "raw_index": 24,
        "output_filename": "flexometro-gripper-contra-impacto-8m-truper.webp",
        "codes": ["FH-8M", "10745"],
        "description": "Cinta métrica de 8 metros cinta extra ancha con gancho magnético triple remache Truper"
    },
    {
        "id": "flexometro-gripper-contra-impacto-3m-truper",
        "title": "Flexómetros Gripper contra impacto de 3 metros Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 174,
        "raw_index": 29,
        "output_filename": "flexometro-gripper-contra-impacto-3m-truper.webp",
        "codes": ["FH-3M", "10750"],
        "description": "Flexómetro compacto de bolsillo de 3 m con seguro de bloqueo deslizante Truper"
    },
    {
        "id": "flexometro-industrial-10m-truper-expert",
        "title": "Flexómetros industriales cinta extra ancha 10 metros Truper Expert",
        "brand": "Truper",
        "category": "Medición",
        "page": 174,
        "raw_index": 30,
        "output_filename": "flexometro-industrial-10m-truper-expert.webp",
        "codes": ["FH-10M", "10755"],
        "description": "Flexómetro de alta durabilidad con cinta que sobresale hasta 3 metros sin doblarse Truper Expert"
    },
    {
        "id": "flexometro-economico-pretul-5m",
        "title": "Flexómetros económicos de 5 metros Pretul",
        "brand": "Pretul",
        "category": "Medición",
        "page": 175,
        "raw_index": 3,
        "output_filename": "flexometro-economico-pretul-5m.webp",
        "codes": ["PRO-5MEB", "21600", "21601"],
        "description": "Cinta métrica de 5 metros con escala graduada en milímetros y pulgadas Pretul"
    },
    {
        "id": "flexometro-economico-pretul-3m",
        "title": "Flexómetros económicos de 3 metros Pretul",
        "brand": "Pretul",
        "category": "Medición",
        "page": 175,
        "raw_index": 6,
        "output_filename": "flexometro-economico-pretul-3m.webp",
        "codes": ["PRO-3MEB", "21605"],
        "description": "Flexómetro de uso doméstico ligero y práctico con clip para cinturón Pretul"
    },
    {
        "id": "flexometro-economico-pretul-8m",
        "title": "Flexómetros económicos de 8 metros Pretul",
        "brand": "Pretul",
        "category": "Medición",
        "page": 175,
        "raw_index": 7,
        "output_filename": "flexometro-economico-pretul-8m.webp",
        "codes": ["PRO-8MEB", "21610"],
        "description": "Cinta métrica larga para obras y mediciones generales de construcción Pretul"
    },
    {
        "id": "cinta-metrica-cruceta-fibra-vidrio-30m-truper",
        "title": "Cintas métricas de cruceta de fibra de vidrio 30 metros Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 175,
        "raw_index": 8,
        "output_filename": "cinta-metrica-cruceta-fibra-vidrio-30m-truper.webp",
        "codes": ["TP-30M", "10765"],
        "description": "Cinta topográfica de fibra de vidrio resistente a la humedad con marco abierto de cruceta Truper"
    },
    {
        "id": "cinta-metrica-cruceta-fibra-vidrio-50m-truper",
        "title": "Cintas métricas de cruceta de fibra de vidrio 50 metros Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 175,
        "raw_index": 9,
        "output_filename": "cinta-metrica-cruceta-fibra-vidrio-50m-truper.webp",
        "codes": ["TP-50M", "10770"],
        "description": "Cinta agrimensora de 50 metros con manivela de rebobinado rápido Truper"
    },
    {
        "id": "cinta-metrica-carcasa-cerrada-20m-truper",
        "title": "Cintas métricas de fibra de vidrio con caja cerrada 20 metros Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 175,
        "raw_index": 10,
        "output_filename": "cinta-metrica-carcasa-cerrada-20m-truper.webp",
        "codes": ["TF-20M", "10775"],
        "description": "Cinta métrica protegida contra polvo en estuche cerrado de alto impacto Truper"
    },
    {
        "id": "nivel-profesional-aluminio-24-truper",
        "title": "Niveles profesionales de aluminio maquinado 24 pulgadas Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 289,
        "raw_index": 0,
        "output_filename": "nivel-profesional-aluminio-24-truper.webp",
        "codes": ["NL-24", "10780"],
        "description": "Nivel de viga de aluminio con 3 gotas acrílicas resistentes a impactos de 0°, 45° y 90° Truper"
    },
    {
        "id": "nivel-profesional-aluminio-48-truper",
        "title": "Niveles profesionales de aluminio maquinado 48 pulgadas Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 289,
        "raw_index": 1,
        "output_filename": "nivel-profesional-aluminio-48-truper.webp",
        "codes": ["NL-48", "10785"],
        "description": "Nivel largo de 1.20 metros para albañilería, instalación de tablaroca y cancelería Truper"
    },
    {
        "id": "nivel-magnetico-aluminio-24-truper-expert",
        "title": "Niveles magnéticos de aluminio 24 pulgadas con base imantada Truper Expert",
        "brand": "Truper",
        "category": "Medición",
        "page": 289,
        "raw_index": 12,
        "output_filename": "nivel-magnetico-aluminio-24-truper-expert.webp",
        "codes": ["NL-24M", "10790"],
        "description": "Nivel con potentes imanes de neodimio integrados para sujeción en estructuras metálicas y tuberías Truper Expert"
    },
    {
        "id": "nivel-magnetico-aluminio-12-truper",
        "title": "Niveles compactos de aluminio 12 pulgadas Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 289,
        "raw_index": 13,
        "output_filename": "nivel-magnetico-aluminio-12-truper.webp",
        "codes": ["NL-12", "10795"],
        "description": "Nivel de aluminio de bolsillo de 30 cm para fontanería y espacios confinados Truper"
    },
    {
        "id": "nivel-torpedo-magnetico-9-truper",
        "title": "Niveles magnéticos tipo torpedo 9 pulgadas Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 290,
        "raw_index": 0,
        "output_filename": "nivel-torpedo-magnetico-9-truper.webp",
        "codes": ["NT-9", "10800"],
        "description": "Nivel tipo torpedo con cuerpo de plástico ABS resistente y ranura en 'V' para tuberías Truper"
    },
    {
        "id": "nivel-torpedo-pretul-9",
        "title": "Niveles tipo torpedo 9 pulgadas Pretul",
        "brand": "Pretul",
        "category": "Medición",
        "page": 290,
        "raw_index": 2,
        "output_filename": "nivel-torpedo-pretul-9.webp",
        "codes": ["NTP-9", "21800"],
        "description": "Nivel torpedo ligero de 3 gotas para uso en taller doméstico Pretul"
    },
    {
        "id": "nivel-de-linea-hilo-truper",
        "title": "Niveles de línea para colgar en hilo de albañil Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 290,
        "raw_index": 5,
        "output_filename": "nivel-de-linea-hilo-truper.webp",
        "codes": ["NL-HIL", "10805"],
        "description": "Par de niveles miniatura con ganchos para tender líneas maestras en cimientos y zanjas Truper"
    },
    {
        "id": "plomada-laton-pulido-16oz-truper",
        "title": "Plomadas de latón pulido macizo 16 oz para albañilería Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 166,
        "raw_index": 0,
        "output_filename": "plomada-laton-pulido-16oz-truper.webp",
        "codes": ["PL-16", "10810"],
        "description": "Plomada cónica torneada en latón anticorrosivo con punta intercambiable de acero Truper"
    },
    {
        "id": "plomada-laton-pulido-8oz-truper",
        "title": "Plomadas de latón pulido 8 oz Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 166,
        "raw_index": 2,
        "output_filename": "plomada-laton-pulido-8oz-truper.webp",
        "codes": ["PL-8", "10815"],
        "description": "Plomada de precisión para verticalidad en muros y colocación de puertas y ventanas Truper"
    },
    {
        "id": "plomada-hierro-esmaltado-truper",
        "title": "Plomadas de hierro fundido esmaltado Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 166,
        "raw_index": 10,
        "output_filename": "plomada-hierro-esmaltado-truper.webp",
        "codes": ["PH-16", "10820"],
        "description": "Plomada económica de hierro con carrete de hilo para albañil Truper"
    },
    {
        "id": "hilo-para-albanil-polietileno-rollo-truper",
        "title": "Hilos para albañil de polietileno trenzado 100 m Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 166,
        "raw_index": 11,
        "output_filename": "hilo-para-albanil-polietileno-rollo-truper.webp",
        "codes": ["HIL-100", "10825"],
        "description": "Madeja de hilo de alta tensión color amarillo fluorescente para trazo de cimentación Truper"
    },
    {
        "id": "tiralineas-gis-marcador-truper",
        "title": "Tiralíneas marcadores de gis con cordón y tiza azul Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 166,
        "raw_index": 12,
        "output_filename": "tiralineas-gis-marcador-truper.webp",
        "codes": ["TL-30", "10830"],
        "description": "Chicote tiralíneas de 30 metros con cuerpo de aluminio y depósito de tiza azul recargable Truper"
    },
    {
        "id": "polvo-tiza-azul-repuesto-tiralineas-truper",
        "title": "Botes de polvo de tiza azul para tiralíneas Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 166,
        "raw_index": 13,
        "output_filename": "polvo-tiza-azul-repuesto-tiralineas-truper.webp",
        "codes": ["GIS-AZ", "10835"],
        "description": "Frasco aplicador de tiza en polvo resistente al viento para marcado visible de líneas Truper"
    },
    {
        "id": "regla-graduada-aluminio-1m-truper",
        "title": "Reglas de aluminio maquinado graduadas de 1 metro Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 290,
        "raw_index": 12,
        "output_filename": "regla-graduada-aluminio-1m-truper.webp",
        "codes": ["REG-1M", "10840"],
        "description": "Regla metálica recta para corte y trazo con borde biselado y graduación en bajo relieve Truper"
    },
    {
        "id": "escuadra-albanil-metalica-24-truper",
        "title": "Escuadras metálicas para albañil y herrero 24 pulgadas Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 290,
        "raw_index": 14,
        "output_filename": "escuadra-albanil-metalica-24-truper.webp",
        "codes": ["ET-24", "10845"],
        "description": "Escuadra fija de acero templado de 16 x 24 pulgadas para escuadrar muros y losas Truper"
    },

    # -------------------------------------------------------------------------
    # 5. Brochas, Rodillos y Pintura (30 familias, Páginas 295-299)
    # -------------------------------------------------------------------------
    {
        "id": "brocha-cerda-natural-4-truper-expert",
        "title": "Brochas de cerda natural 4 pulgadas Truper Expert",
        "brand": "Truper",
        "category": "Pintura",
        "page": 295,
        "raw_index": 1,
        "output_filename": "brocha-cerda-natural-4-truper-expert.webp",
        "codes": ["BR-4X", "10850"],
        "description": "Brocha profesional de 4\" con cerda 100% natural de cerdo para aplicación uniforme de vinílicas y esmaltes Truper Expert"
    },
    {
        "id": "brocha-cerda-natural-3-truper-expert",
        "title": "Brochas de cerda natural 3 pulgadas Truper Expert",
        "brand": "Truper",
        "category": "Pintura",
        "page": 295,
        "raw_index": 11,
        "output_filename": "brocha-cerda-natural-3-truper-expert.webp",
        "codes": ["BR-3X", "10855"],
        "description": "Brocha con mango de madera pulida y casquillo de acero inoxidable resistente a solventes Truper Expert"
    },
    {
        "id": "brocha-cerda-natural-2-truper-expert",
        "title": "Brochas de cerda natural 2 pulgadas Truper Expert",
        "brand": "Truper",
        "category": "Pintura",
        "page": 295,
        "raw_index": 12,
        "output_filename": "brocha-cerda-natural-2-truper-expert.webp",
        "codes": ["BR-2X", "10860"],
        "description": "Brocha de 2\" para molduras, puertas y acabados finos Truper Expert"
    },
    {
        "id": "brocha-cerda-natural-1-1-2-truper",
        "title": "Brochas de cerda natural 1-1/2 pulgadas Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 295,
        "raw_index": 34,
        "output_filename": "brocha-cerda-natural-1-1-2-truper.webp",
        "codes": ["BR-1-1/2", "10865"],
        "description": "Brocha estándar de uso general para retoques y áreas estrechas Truper"
    },
    {
        "id": "brocha-cerda-natural-5-truper",
        "title": "Brochas de cerda natural 5 pulgadas para fachadas Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 295,
        "raw_index": 35,
        "output_filename": "brocha-cerda-natural-5-truper.webp",
        "codes": ["BR-5", "10870"],
        "description": "Brocha ancha de 5\" para cubrimiento rápido de bardas y paredes exteriores Truper"
    },
    {
        "id": "brocha-cerda-natural-6-truper",
        "title": "Brochas de cerda natural 6 pulgadas tipo pintor Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 295,
        "raw_index": 36,
        "output_filename": "brocha-cerda-natural-6-truper.webp",
        "codes": ["BR-6", "10875"],
        "description": "Brocha extra ancha de 6\" con gran retención de pintura sin goteo Truper"
    },
    {
        "id": "brocha-economica-pretul-4",
        "title": "Brochas económicas cerda sintética 4 pulgadas Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 296,
        "raw_index": 0,
        "output_filename": "brocha-economica-pretul-4.webp",
        "codes": ["BRP-4", "21850"],
        "description": "Brocha económica de 4\" con mango plástico hueco ligero Pretul"
    },
    {
        "id": "brocha-economica-pretul-3",
        "title": "Brochas económicas cerda sintética 3 pulgadas Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 296,
        "raw_index": 13,
        "output_filename": "brocha-economica-pretul-3.webp",
        "codes": ["BRP-3", "21855"],
        "description": "Brocha popular de alta rotación para reparaciones caseras Pretul"
    },
    {
        "id": "brocha-economica-pretul-2",
        "title": "Brochas económicas cerda sintética 2 pulgadas Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 296,
        "raw_index": 18,
        "output_filename": "brocha-economica-pretul-2.webp",
        "codes": ["BRP-2", "21860"],
        "description": "Brocha de 2\" económica para pinturas base agua y solvente Pretul"
    },
    {
        "id": "brocha-economica-pretul-1",
        "title": "Brochas económicas cerda sintética 1 pulgada Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 296,
        "raw_index": 22,
        "output_filename": "brocha-economica-pretul-1.webp",
        "codes": ["BRP-1", "21865"],
        "description": "Brocha angosta de 1\" para pintura en herrería y rejas Pretul"
    },
    {
        "id": "brocha-para-barniz-cerda-blanca-truper",
        "title": "Brochas especiales para barniz cerda blanca extra suave Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 296,
        "raw_index": 23,
        "output_filename": "brocha-para-barniz-cerda-blanca-truper.webp",
        "codes": ["BR-BARN", "10880"],
        "description": "Brocha con cerdas blancas finamente abiertas para evitar marcas de brocha en maderas y lacas Truper"
    },
    {
        "id": "brocha-angular-para-recortes-truper",
        "title": "Brochas angulares de corte perfecto para esquinas Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 296,
        "raw_index": 30,
        "output_filename": "brocha-angular-para-recortes-truper.webp",
        "codes": ["BR-ANG", "10885"],
        "description": "Brocha con corte sesgado para trazar líneas rectas en unión de techo y pared sin cinta Truper"
    },
    {
        "id": "rodillo-profesional-9-superficie-rugosa-truper",
        "title": "Rodillos profesionales de 9 pulgadas para superficie rugosa Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 297,
        "raw_index": 0,
        "output_filename": "rodillo-profesional-9-superficie-rugosa-truper.webp",
        "codes": ["ROPI-9X", "10890"],
        "description": "Rodillo completo con felpa gruesa de 3/4\" de alta densidad para tirol, tabique y block Truper"
    },
    {
        "id": "rodillo-profesional-9-superficie-lisa-truper",
        "title": "Rodillos profesionales de 9 pulgadas para superficie lisa Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 297,
        "raw_index": 2,
        "output_filename": "rodillo-profesional-9-superficie-lisa-truper.webp",
        "codes": ["ROPI-9L", "10895"],
        "description": "Rodillo con felpa de 3/8\" para acabado terso en tablaroca y yeso liso Truper"
    },
    {
        "id": "rodillo-economico-pretul-9",
        "title": "Rodillos para pintar 9 pulgadas económicos Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 297,
        "raw_index": 3,
        "output_filename": "rodillo-economico-pretul-9.webp",
        "codes": ["ROPI-9P", "21890"],
        "description": "Rodillo de 9\" con maneral de alambre galvanizado y mango de polipropileno Pretul"
    },
    {
        "id": "mini-rodillo-esmalte-4-truper",
        "title": "Mini rodillos de 4 pulgadas para esmaltes y poliuretano Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 297,
        "raw_index": 4,
        "output_filename": "mini-rodillo-esmalte-4-truper.webp",
        "codes": ["ROPI-4", "10900"],
        "description": "Rodillo compacto de espuma de alta densidad para puertas, closets y herrería Truper"
    },
    {
        "id": "mini-rodillo-esponja-pretul-4",
        "title": "Mini rodillos de esponja 4 pulgadas Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 297,
        "raw_index": 5,
        "output_filename": "mini-rodillo-esponja-pretul-4.webp",
        "codes": ["ROPI-4P", "21900"],
        "description": "Mini rodillo ligero para manualidades y aplicación de barnices en espacios pequeños Pretul"
    },
    {
        "id": "maneral-reforzado-jaula-rodillo-9-truper",
        "title": "Manerales reforzados de jaula para rodillo de 9 pulgadas Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 297,
        "raw_index": 6,
        "output_filename": "maneral-reforzado-jaula-rodillo-9-truper.webp",
        "codes": ["MAN-ROD9", "10905"],
        "description": "Maneral profesional de jaula con baleros metálicos para giro suave sin atorarse Truper"
    },
    {
        "id": "felpa-repuesto-superficie-rugosa-9-truper",
        "title": "Felpas de repuesto para rodillo 9 pulgadas rugosa Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 298,
        "raw_index": 5,
        "output_filename": "felpa-repuesto-superficie-rugosa-9-truper.webp",
        "codes": ["FEL-9R", "10910"],
        "description": "Tubo de felpa de lana sintética de 3/4\" resistente a solventes para repuesto Truper"
    },
    {
        "id": "felpa-repuesto-superficie-lisa-9-truper",
        "title": "Felpas de repuesto para rodillo 9 pulgadas lisa Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 298,
        "raw_index": 6,
        "output_filename": "felpa-repuesto-superficie-lisa-9-truper.webp",
        "codes": ["FEL-9L", "10915"],
        "description": "Felpa de microfibra de 3/8\" que no desprende pelusa para acabados perfectos Truper"
    },
    {
        "id": "felpa-de-borrego-natural-9-truper-expert",
        "title": "Felpas de borrego natural 100% 9 pulgadas Truper Expert",
        "brand": "Truper",
        "category": "Pintura",
        "page": 298,
        "raw_index": 7,
        "output_filename": "felpa-de-borrego-natural-9-truper-expert.webp",
        "codes": ["FEL-BORR", "10920"],
        "description": "Felpa de lana de borrego genuina con máxima absorción y transferencia de pintura Truper Expert"
    },
    {
        "id": "felpa-economica-pretul-9",
        "title": "Felpas de repuesto para rodillo 9 pulgadas Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 298,
        "raw_index": 9,
        "output_filename": "felpa-economica-pretul-9.webp",
        "codes": ["FEL-9P", "21910"],
        "description": "Felpa económica de poliéster para aplicaciones rápidas en hogar Pretul"
    },
    {
        "id": "juego-repuesto-mini-felpas-4-truper",
        "title": "Juegos de 2 mini felpas de repuesto de 4 pulgadas Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 298,
        "raw_index": 17,
        "output_filename": "juego-repuesto-mini-felpas-4-truper.webp",
        "codes": ["FEL-4X2", "10925"],
        "description": "Paquete con 2 rodillos miniatura de 4\" para marcos de ventanas y puertas Truper"
    },
    {
        "id": "charola-plastica-para-pintar-reforzada-truper",
        "title": "Charolas plásticas reforzadas para pintura de 9 pulgadas Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 299,
        "raw_index": 3,
        "output_filename": "charola-plastica-para-pintar-reforzada-truper.webp",
        "codes": ["CHAR-P", "10930"],
        "description": "Charola de plástico de polipropileno de alta resistencia con estrías escurridoras Truper"
    },
    {
        "id": "charola-metalica-para-pintar-truper",
        "title": "Charolas metálicas galvanizadas para pintura Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 299,
        "raw_index": 10,
        "output_filename": "charola-metalica-para-pintar-truper.webp",
        "codes": ["CHAR-MET", "10935"],
        "description": "Bandeja de lámina galvanizada inoxidable compatible con solventes y thiner Truper"
    },
    {
        "id": "kit-para-pintar-charola-rodillo-brocha-truper",
        "title": "Kits profesionales para pintar con charola, rodillo y brocha Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 299,
        "raw_index": 13,
        "output_filename": "kit-para-pintar-charola-rodillo-brocha-truper.webp",
        "codes": ["KIT-PINT", "10940"],
        "description": "Juego completo de pintura con charola, rodillo de 9\", brocha de 2\" y mezclador Truper"
    },
    {
        "id": "kit-para-pintar-pretul-4-piezas",
        "title": "Kits para pintar económicos de 4 piezas Pretul",
        "brand": "Pretul",
        "category": "Pintura",
        "page": 299,
        "raw_index": 16,
        "output_filename": "kit-para-pintar-pretul-4-piezas.webp",
        "codes": ["KIT-PINTP", "21940"],
        "description": "Kit básico de pintura con charola ligera y rodillo completo Pretul"
    },
    {
        "id": "extension-telescopica-aluminio-pintor-2m-truper",
        "title": "Extensiones telescópicas de aluminio para pintar 2 metros Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 299,
        "raw_index": 17,
        "output_filename": "extension-telescopica-aluminio-pintor-2m-truper.webp",
        "codes": ["EXT-ALU2", "10945"],
        "description": "Tubo telescópico extensible de aluminio anodizado con rosca estándar para rodillos Truper"
    },
    {
        "id": "extension-telescopica-aluminio-pintor-3m-truper",
        "title": "Extensiones telescópicas de aluminio para pintar 3 metros Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 299,
        "raw_index": 20,
        "output_filename": "extension-telescopica-aluminio-pintor-3m-truper.webp",
        "codes": ["EXT-ALU3", "10950"],
        "description": "Extensión de 3 metros con seguro giratorio para pintar techos y fachadas altas sin escalera Truper"
    },
    {
        "id": "peine-limpiador-de-rodillos-truper",
        "title": "Limpiadores raspadores de rodillos 5 en 1 Truper",
        "brand": "Truper",
        "category": "Pintura",
        "page": 298,
        "raw_index": 18,
        "output_filename": "peine-limpiador-de-rodillos-truper.webp",
        "codes": ["LIMP-ROD", "10955"],
        "description": "Herramienta con cuchilla curva para escurrir el exceso de pintura y prolongar la vida de la felpa Truper"
    },

    # -------------------------------------------------------------------------
    # 6. Espátulas, Raspadores, Marros y Demolición (20 familias, Páginas 168-169, 282, 381, 78)
    # -------------------------------------------------------------------------
    {
        "id": "espatula-flexible-acero-inox-3-truper-expert",
        "title": "Espátulas flexibles de acero inoxidable 3 pulgadas Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 168,
        "raw_index": 4,
        "output_filename": "espatula-flexible-acero-inox-3-truper-expert.webp",
        "codes": ["ET-3X", "10960"],
        "description": "Espátula con hoja flexible de acero inoxidable pulido espejo y casquillo de golpe Truper Expert"
    },
    {
        "id": "espatula-flexible-acero-inox-4-truper-expert",
        "title": "Espátulas flexibles de acero inoxidable 4 pulgadas Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 168,
        "raw_index": 6,
        "output_filename": "espatula-flexible-acero-inox-4-truper-expert.webp",
        "codes": ["ET-4X", "10965"],
        "description": "Espátula para resanado y aplicación de masilla y pasta en muros con mango Comfort Grip Truper Expert"
    },
    {
        "id": "espatula-rigida-raspador-2-truper",
        "title": "Espátulas rígidas raspadoras de 2 pulgadas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 169,
        "raw_index": 3,
        "output_filename": "espatula-rigida-raspador-2-truper.webp",
        "codes": ["ET-2R", "10970"],
        "description": "Espátula de hoja gruesa indeformable para retirar pintura vieja, sarro y yeso Truper"
    },
    {
        "id": "espatula-flexible-acero-al-carbon-2-truper",
        "title": "Espátulas flexibles de acero al carbono 2 pulgadas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 169,
        "raw_index": 4,
        "output_filename": "espatula-flexible-acero-al-carbon-2-truper.webp",
        "codes": ["ET-2F", "10975"],
        "description": "Espátula de mango de madera remachado para albañilería y carpintería Truper"
    },
    {
        "id": "espatula-economica-pretul-3",
        "title": "Espátulas económicas mango de plástico 3 pulgadas Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 169,
        "raw_index": 5,
        "output_filename": "espatula-economica-pretul-3.webp",
        "codes": ["EP-3F", "21960"],
        "description": "Espátula económica para parchar grietas y agujeros con resanador Pretul"
    },
    {
        "id": "espatula-yesera-carrocero-6-truper",
        "title": "Espátulas carrocero yeseras de hoja ancha 6 pulgadas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 169,
        "raw_index": 15,
        "output_filename": "espatula-yesera-carrocero-6-truper.webp",
        "codes": ["ET-6F", "10980"],
        "description": "Espátula ancha para alisar uniones de tablaroca y empastado de paneles Truper"
    },
    {
        "id": "espatula-yesera-carrocero-8-truper",
        "title": "Espátulas carrocero yeseras de hoja ancha 8 pulgadas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 169,
        "raw_index": 16,
        "output_filename": "espatula-yesera-carrocero-8-truper.webp",
        "codes": ["ET-8F", "10985"],
        "description": "Espátula plana para acabados ultra lisos de pasta y microcemento Truper"
    },
    {
        "id": "espatula-multiusos-pintor-6-en-1-truper",
        "title": "Espátulas multiusos para pintor 6 en 1 Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 169,
        "raw_index": 22,
        "output_filename": "espatula-multiusos-pintor-6-en-1-truper.webp",
        "codes": ["ET-6EN1", "10990"],
        "description": "Herramienta con raspador, limpia rodillo, saca clavos, destapador y limpiador de grietas Truper"
    },
    {
        "id": "marro-octagonal-mango-madera-4lb-truper",
        "title": "Marros octagonales de 4 libras con mango de madera Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 282,
        "raw_index": 0,
        "output_filename": "marro-octagonal-mango-madera-4lb-truper.webp",
        "codes": ["MD-4M", "10995"],
        "description": "Marro forjado en acero alto carbono con caras maquinadas y biseladas para demolición Truper"
    },
    {
        "id": "marro-octagonal-mango-madera-6lb-truper",
        "title": "Marros octagonales de 6 libras con mango de madera Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 282,
        "raw_index": 2,
        "output_filename": "marro-octagonal-mango-madera-6lb-truper.webp",
        "codes": ["MD-6M", "11000"],
        "description": "Marro de demolición de 6 lb con mango largo de nogal hickory Truper"
    },
    {
        "id": "marro-octagonal-mango-madera-8lb-truper",
        "title": "Marros octagonales de 8 libras con mango de madera Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 282,
        "raw_index": 3,
        "output_filename": "marro-octagonal-mango-madera-8lb-truper.webp",
        "codes": ["MD-8M", "11005"],
        "description": "Marro pesado de 8 lb para romper concreto, muros y mampostería Truper"
    },
    {
        "id": "marro-octagonal-fibra-vidrio-4lb-truper-expert",
        "title": "Marros octagonales de 4 lb con mango de fibra de vidrio Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 282,
        "raw_index": 4,
        "output_filename": "marro-octagonal-fibra-vidrio-4lb-truper-expert.webp",
        "codes": ["MD-4F", "11010"],
        "description": "Marro con mango de fibra de vidrio antigolpe con collarín de protección de sobreimpacto Truper Expert"
    },
    {
        "id": "marro-octagonal-pretul-4lb",
        "title": "Marros octagonales de 4 libras Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 282,
        "raw_index": 10,
        "output_filename": "marro-octagonal-pretul-4lb.webp",
        "codes": ["MDP-4M", "22000"],
        "description": "Marro económico de acero forjado para herrería y construcción Pretul"
    },
    {
        "id": "marro-octagonal-pretul-6lb",
        "title": "Marros octagonales de 6 libras Pretul",
        "brand": "Pretul",
        "category": "Construcción",
        "page": 282,
        "raw_index": 11,
        "output_filename": "marro-octagonal-pretul-6lb.webp",
        "codes": ["MDP-6M", "22005"],
        "description": "Marro de 6 lb para demolición y golpe de cinceles Pretul"
    },
    {
        "id": "talacho-pico-con-mango-madera-5lb-truper",
        "title": "Talachos tipo pico con mango de madera 5 libras Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 381,
        "raw_index": 0,
        "output_filename": "talacho-pico-con-mango-madera-5lb-truper.webp",
        "codes": ["TP-5M", "11015"],
        "description": "Talacho pico forjado con extremo en punta y pala angosta para zanjado de terrenos duros Truper"
    },
    {
        "id": "zapapico-con-mango-madera-5lb-truper",
        "title": "Zapapicos con mango de madera 5 libras Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 381,
        "raw_index": 1,
        "output_filename": "zapapico-con-mango-madera-5lb-truper.webp",
        "codes": ["ZP-5M", "11020"],
        "description": "Zapapico minero con doble punta forjada para quebrar piedra y roca Truper"
    },
    {
        "id": "talacho-pico-fibra-vidrio-5lb-truper-expert",
        "title": "Talachos tipo pico con mango de fibra de vidrio 5 lb Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 381,
        "raw_index": 2,
        "output_filename": "talacho-pico-fibra-vidrio-5lb-truper-expert.webp",
        "codes": ["TP-5F", "11025"],
        "description": "Talacho con cabo irrompible de fibra de vidrio con agarre termoplástico antiderrapante Truper Expert"
    },
    {
        "id": "zapapico-fibra-vidrio-5lb-truper-expert",
        "title": "Zapapicos con mango de fibra de vidrio 5 lb Truper Expert",
        "brand": "Truper",
        "category": "Construcción",
        "page": 381,
        "raw_index": 3,
        "output_filename": "zapapico-fibra-vidrio-5lb-truper-expert.webp",
        "codes": ["ZP-5F", "11030"],
        "description": "Zapapico de alta resistencia con absorción de impacto para minería y excavación Truper Expert"
    },
    {
        "id": "puntero-cincel-con-protector-de-impacto-truper",
        "title": "Punteros de acero con protector de mano para golpe Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 78,
        "raw_index": 0,
        "output_filename": "puntero-cincel-con-protector-de-impacto-truper.webp",
        "codes": ["PUN-PROT", "11035"],
        "description": "Puntero para romper concreto con empuñadura de hule que protege la mano contra martillazos Truper"
    },
    {
        "id": "cincel-cortafrío-plano-con-protector-truper",
        "title": "Cinceles cortafrío planos con protector de golpe Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 78,
        "raw_index": 1,
        "output_filename": "cincel-cortafrio-plano-con-protector-truper.webp",
        "codes": ["CIN-PROT", "11040"],
        "description": "Cincel plano de 1 pulgada forjado en acero al cromo vanadio con guardia de seguridad Truper"
    },

    # -------------------------------------------------------------------------
    # 7. Equipos Neumáticos y Taller (10 familias, Páginas 104-105, 80-81)
    # -------------------------------------------------------------------------
    {
        "id": "clavadora-neumatica-calibre-18-truper",
        "title": "Clavadoras neumáticas calibre 18 para carpintería Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 104,
        "raw_index": 8,
        "output_filename": "clavadora-neumatica-calibre-18-truper.webp",
        "codes": ["CLNE-18", "11045"],
        "description": "Pistola clavadora neumática para clavos de 3/8\" a 2\" con deflector de aire direccional 360° Truper"
    },
    {
        "id": "engrapadora-neumatica-corona-ancha-truper",
        "title": "Engrapadoras neumáticas de corona ancha para tapicería Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 104,
        "raw_index": 13,
        "output_filename": "engrapadora-neumatica-corona-ancha-truper.webp",
        "codes": ["ENNE-16", "11050"],
        "description": "Engrapadora de aire para trabajo continuo con cargador de liberación rápida Truper"
    },
    {
        "id": "clavadora-engrapadora-combo-neumatica-truper",
        "title": "Clavadoras y engrapadoras neumáticas combo 2 en 1 Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 105,
        "raw_index": 3,
        "output_filename": "clavadora-engrapadora-combo-neumatica-truper.webp",
        "codes": ["CLEN-2EN1", "11055"],
        "description": "Herramienta neumática dual que dispara tanto grapas como clavos sin cambiar de equipo Truper"
    },
    {
        "id": "manguera-hibrida-para-aire-neumatica-truper",
        "title": "Mangueras híbridas para compresor de aire 15 metros Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 103,
        "raw_index": 106,
        "output_filename": "manguera-hibrida-para-aire-neumatica-truper.webp",
        "codes": ["MAN-AIR15", "11060"],
        "description": "Manguera flexible de polímero híbrido de 300 PSI que no se enreda ni se endurece en frío Truper"
    },
    {
        "id": "gavetas-apilables-organizadoras-plastica-truper",
        "title": "Gavetas apilables organizadoras de plástico (bins) Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 80,
        "raw_index": 0,
        "output_filename": "gavetas-apilables-organizadoras-plastica-truper.webp",
        "codes": ["GAV-AP", "11065"],
        "description": "Caja gaveta de polipropileno para mostrador de tornillería y ferretería Truper"
    },
    {
        "id": "cama-mecanico-taller-con-ruedas-truper",
        "title": "Camas para mecánico de taller acolchonadas con ruedas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 81,
        "raw_index": 0,
        "output_filename": "cama-mecanico-taller-con-ruedas-truper.webp",
        "codes": ["CAM-MEC", "11070"],
        "description": "Camilla para mecánica automotriz con cabecera acolchonada y 6 ruedas giratorias 360° Truper"
    },
    {
        "id": "banco-asiento-giratorio-para-mecanico-truper",
        "title": "Bancos asientos giratorios con charola portaherramientas Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 81,
        "raw_index": 5,
        "output_filename": "banco-asiento-giratorio-para-mecanico-truper.webp",
        "codes": ["BAN-MEC", "11075"],
        "description": "Asiento neumático de altura ajustable para mecánico con charola de herramientas inferior Truper"
    },
    {
        "id": "bascula-electronica-digital-40kg-truper",
        "title": "Básculas electrónicas digitales multifuncionales 40 kg Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 41,
        "raw_index": 1,
        "output_filename": "bascula-electronica-digital-40kg-truper.webp",
        "codes": ["BAS-40D", "11080"],
        "description": "Báscula comercial con display de doble pantalla para peso, precio y cálculo de cambio Truper"
    },
    {
        "id": "bascula-colgante-romana-reloj-truper",
        "title": "Básculas colgantes tipo reloj con gancho 25 kg Truper",
        "brand": "Truper",
        "category": "Medición",
        "page": 41,
        "raw_index": 8,
        "output_filename": "bascula-colgante-romana-reloj-truper.webp",
        "codes": ["BAS-25R", "11085"],
        "description": "Báscula mecánica romana con carátula circular y gancho de acero galvanizado Truper"
    },
    {
        "id": "cuchillo-tactico-monte-con-funda-truper",
        "title": "Cuchillos tácticos de monte con hoja de acero inoxidable Truper",
        "brand": "Truper",
        "category": "Construcción",
        "page": 122,
        "raw_index": 1,
        "output_filename": "cuchillo-tactico-monte-con-funda-truper.webp",
        "codes": ["CUCH-TAC", "11090"],
        "description": "Cuchillo de supervivencia con hoja pavonada, sierra superior y funda rígida con clip Truper"
    }
]

def pad_to_canvas(im, target_w=500, target_h=500, padding=12, bg_color=(255, 255, 255)):
    """Centra la imagen en un lienzo cuadrado con 12px de margen y fondo blanco puro."""
    im = im.convert("RGB")
    w, h = im.size
    max_w = target_w - (padding * 2)
    max_h = target_h - (padding * 2)
    scale = min(max_w / w, max_h / h)
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
    data = rgb.getdata()
    non_white = sum(1 for p in data if p != (255, 255, 255))
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

    # Si ya se inspeccionó previamente en /tmp/inspect_mod_d, reutilizar
    inspect_png = f"/tmp/inspect_mod_d/p{page}-{raw_idx:03d}.png"
    if not os.path.exists(raw_png) and os.path.exists(inspect_png):
        import shutil
        shutil.copy2(inspect_png, raw_png)

    if not os.path.exists(raw_png):
        subprocess.run(["pdfimages", "-png", "-f", str(page), "-l", str(page), PDF_PATH, prefix], check=True)

    if not os.path.exists(raw_png):
        print(f"[!] Archivo de imagen cruda no encontrado: {raw_png}", file=sys.stderr)
        return False

    with Image.open(raw_png) as im:
        if is_blank_or_invalid(im):
            print(f"[!] Advertencia: Imagen cruda vacía en página {page} índice {raw_idx} ({out_file})")
            return False
        normalized = pad_to_canvas(im, 500, 500, padding=12)
        normalized.save(out_path, "WEBP", quality=88)

    return True

def run():
    print("=" * 75)
    print("MÓDULO D: EXTRACCIÓN DE 145 NUEVAS FAMILIAS TRUPER (TOTAL META: 711)")
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

    # 2. Extraer y procesar imágenes del Módulo D
    print(f"[*] Extrayendo {len(MODULE_D_145_FAMILIES)} familias visuales del Módulo D...")
    new_extracted = 0
    for g in MODULE_D_145_FAMILIES:
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
            # Reglas semánticas guiadas de alta fidelidad para Construcción, Medición y Pintura
            for g in existing_groups:
                gid = g["id"]
                # Palas y Cavadores
                if gid == "pala-cuadrada-puno-y-truper" and "pala" in name and "cuadrad" in name and ("truper" in name or "classic" in name):
                    matched_group = g
                    match_reason = "Nombre:Pala Cuadrada Truper"
                    break
                elif gid == "pala-cuadrada-puno-y-pretul" and "pala" in name and "cuadrad" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Pala Cuadrada Pretul"
                    break
                elif gid == "pala-redonda-puno-y-truper" and "pala" in name and "redonda" in name and ("truper" in name or "classic" in name):
                    matched_group = g
                    match_reason = "Nombre:Pala Redonda Truper"
                    break
                elif gid == "pala-redonda-puno-y-pretul" and "pala" in name and "redonda" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Pala Redonda Pretul"
                    break
                elif gid == "pala-carbonera-puno-y-truper" and "pala" in name and "carbonera" in name:
                    matched_group = g
                    match_reason = "Nombre:Pala Carbonera"
                    break
                elif gid == "pala-escarraman-zanja-truper" and "pala" in name and ("escarraman" in name or "zanja" in name):
                    matched_group = g
                    match_reason = "Nombre:Pala Escarraman"
                    break
                elif gid == "cavador-agricola-doble-mango-truper" and ("cavador" in name or "pocera" in name):
                    matched_group = g
                    match_reason = "Nombre:Cavador Doble"
                    break

                # Carretillas y Ruedas
                elif gid == "carretilla-4-5-ft3-metalica-truper" and "carretilla" in name and ("truper" in name or "metalica" in name or "4.5" in name):
                    matched_group = g
                    match_reason = "Nombre:Carretilla Truper"
                    break
                elif gid == "carretilla-obra-pretul-4-ft3" and "carretilla" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Carretilla Pretul"
                    break
                elif gid == "carretilla-6-ft3-plastica-irrompible-truper" and "carretilla" in name and "plastic" in name:
                    matched_group = g
                    match_reason = "Nombre:Carretilla Plastica"
                    break
                elif gid == "rueda-neumatica-reforzada-carretilla-truper" and ("rueda" in name or "llanta" in name) and "carretilla" in name and "neumatic" in name:
                    matched_group = g
                    match_reason = "Nombre:Llanta Carretilla Neumatica"
                    break
                elif gid == "rueda-impinchable-solida-carretilla-truper" and ("rueda" in name or "llanta" in name) and "carretilla" in name and ("impinchable" in name or "solida" in name):
                    matched_group = g
                    match_reason = "Nombre:Llanta Carretilla Impinchable"
                    break
                elif gid == "camara-de-repuesto-llanta-carretilla-truper" and "camara" in name and "carretilla" in name:
                    matched_group = g
                    match_reason = "Nombre:Camara Carretilla"
                    break

                # Albañilería, Cucharas, Llanas
                elif gid == "cuchara-albanil-philadelphia-truper" and "cuchara" in name and "albanil" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Cuchara Albanil Truper"
                    break
                elif gid == "cuchara-albanil-philadelphia-pretul" and "cuchara" in name and "albanil" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Cuchara Albanil Pretul"
                    break
                elif gid == "cuchara-albanil-guadalajara-truper" and "cuchara" in name and "guadalajara" in name:
                    matched_group = g
                    match_reason = "Nombre:Cuchara Guadalajara"
                    break
                elif gid == "llana-lisa-acero-mango-madera-truper" and "llana" in name and "lisa" in name:
                    matched_group = g
                    match_reason = "Nombre:Llana Lisa"
                    break
                elif gid == "llana-dentada-cuadrada-truper" and "llana" in name and "dentad" in name:
                    matched_group = g
                    match_reason = "Nombre:Llana Dentada"
                    break
                elif gid == "flota-de-esponja-para-acabados-truper" and "flota" in name and "esponja" in name:
                    matched_group = g
                    match_reason = "Nombre:Flota Esponja"
                    break
                elif gid == "flota-de-hule-para-emboquillado-truper" and "flota" in name and "hule" in name:
                    matched_group = g
                    match_reason = "Nombre:Flota Hule"
                    break
                elif gid == "cortador-de-azulejo-manual-40cm-truper" and "cortador" in name and "azulejo" in name:
                    matched_group = g
                    match_reason = "Nombre:Cortador Azulejo"
                    break
                elif gid == "cuchilla-repuesto-cortador-azulejo-truper" and ("cuchilla" in name or "rodel" in name) and "azulejo" in name:
                    matched_group = g
                    match_reason = "Nombre:Rodel Azulejo"
                    break
                elif gid == "anclas-niveladoras-para-porcelanato-truper" and ("ancla" in name or "clip" in name) and "nivelaci" in name:
                    matched_group = g
                    match_reason = "Nombre:Anclas Nivelacion"
                    break
                elif gid == "cunas-reutilizables-nivelacion-azulejo-truper" and "cuna" in name and "nivelaci" in name:
                    matched_group = g
                    match_reason = "Nombre:Cunas Nivelacion"
                    break
                elif gid == "crucetas-separadoras-azulejo-truper" and ("cruceta" in name or "separador" in name) and ("azulejo" in name or "piso" in name):
                    matched_group = g
                    match_reason = "Nombre:Crucetas Azulejo"
                    break

                # Medición y Nivelación
                elif gid == "flexometro-gripper-contra-impacto-5m-truper" and ("flexometro" in name or "cinta metrica" in name) and "5" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Flexometro 5m Truper"
                    break
                elif gid == "flexometro-gripper-contra-impacto-8m-truper" and ("flexometro" in name or "cinta metrica" in name) and "8" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Flexometro 8m Truper"
                    break
                elif gid == "flexometro-economico-pretul-5m" and ("flexometro" in name or "cinta metrica" in name) and "pretul" in name and "5" in name:
                    matched_group = g
                    match_reason = "Nombre:Flexometro 5m Pretul"
                    break
                elif gid == "cinta-metrica-cruceta-fibra-vidrio-30m-truper" and "cinta" in name and ("cruceta" in name or "fibra" in name or "topografica" in name):
                    matched_group = g
                    match_reason = "Nombre:Cinta Topografica"
                    break
                elif gid == "nivel-profesional-aluminio-24-truper" and "nivel" in name and "aluminio" in name:
                    matched_group = g
                    match_reason = "Nombre:Nivel Aluminio"
                    break
                elif gid == "nivel-torpedo-magnetico-9-truper" and "nivel" in name and "torpedo" in name:
                    matched_group = g
                    match_reason = "Nombre:Nivel Torpedo"
                    break
                elif gid == "plomada-laton-pulido-16oz-truper" and "plomada" in name:
                    matched_group = g
                    match_reason = "Nombre:Plomada"
                    break
                elif gid == "tiralineas-gis-marcador-truper" and ("tiralineas" in name or "tiralinea" in name):
                    matched_group = g
                    match_reason = "Nombre:Tiralineas"
                    break

                # Pintura, Brochas y Rodillos
                elif gid == "brocha-cerda-natural-4-truper-expert" and "brocha" in name and "4" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Brocha 4 Truper"
                    break
                elif gid == "brocha-cerda-natural-3-truper-expert" and "brocha" in name and "3" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Brocha 3 Truper"
                    break
                elif gid == "brocha-cerda-natural-2-truper-expert" and "brocha" in name and "2" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Brocha 2 Truper"
                    break
                elif gid == "brocha-economica-pretul-4" and "brocha" in name and "4" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Brocha 4 Pretul"
                    break
                elif gid == "brocha-economica-pretul-3" and "brocha" in name and "3" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Brocha 3 Pretul"
                    break
                elif gid == "brocha-economica-pretul-2" and "brocha" in name and "2" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Brocha 2 Pretul"
                    break
                elif gid == "rodillo-profesional-9-superficie-rugosa-truper" and "rodillo" in name and ("9" in name or "rugos" in name) and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Rodillo Rugoso Truper"
                    break
                elif gid == "rodillo-economico-pretul-9" and "rodillo" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Rodillo Pretul"
                    break
                elif gid == "felpa-repuesto-superficie-rugosa-9-truper" and "felpa" in name and ("rugos" in name or "9" in name):
                    matched_group = g
                    match_reason = "Nombre:Felpa Rugosa"
                    break
                elif gid == "felpa-repuesto-superficie-lisa-9-truper" and "felpa" in name and ("lisa" in name or "microfibra" in name):
                    matched_group = g
                    match_reason = "Nombre:Felpa Lisa"
                    break
                elif gid == "charola-plastica-para-pintar-reforzada-truper" and "charola" in name and "pint" in name:
                    matched_group = g
                    match_reason = "Nombre:Charola Pintura"
                    break
                elif gid == "extension-telescopica-aluminio-pintor-2m-truper" and "extension" in name and ("rodillo" in name or "pintor" in name):
                    matched_group = g
                    match_reason = "Nombre:Extension Pintor"
                    break

                # Espátulas, Marros y Demolición
                elif gid == "espatula-flexible-acero-inox-3-truper-expert" and "espatula" in name and ("3" in name or "flexible" in name):
                    matched_group = g
                    match_reason = "Nombre:Espatula Flexible"
                    break
                elif gid == "espatula-rigida-raspador-2-truper" and "espatula" in name and ("rigida" in name or "raspador" in name):
                    matched_group = g
                    match_reason = "Nombre:Espatula Rigida"
                    break
                elif gid == "marro-octagonal-mango-madera-4lb-truper" and "marro" in name and ("4" in name or "madera" in name):
                    matched_group = g
                    match_reason = "Nombre:Marro 4lb"
                    break
                elif gid == "marro-octagonal-mango-madera-8lb-truper" and "marro" in name and ("8" in name or "pesado" in name):
                    matched_group = g
                    match_reason = "Nombre:Marro 8lb"
                    break
                elif gid == "talacho-pico-con-mango-madera-5lb-truper" and ("talacho" in name or ("pico" in name and "talacho" in name)):
                    matched_group = g
                    match_reason = "Nombre:Talacho Pico"
                    break
                elif gid == "zapapico-con-mango-madera-5lb-truper" and "zapapico" in name:
                    matched_group = g
                    match_reason = "Nombre:Zapapico"
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

    # Construir la lista acumulada de todos los productos de tienda con imagen oficial Truper
    all_truper_products = []
    seen_skus = set()
    for p in products:
        img = p.get("image", "")
        if img.startswith("assets/images/products/truper/") and p.get("sku") not in seen_skus:
            seen_skus.add(p.get("sku"))
            all_truper_products.append({
                "id": p.get("id"),
                "sku": p.get("sku"),
                "name": p.get("name"),
                "brand": p.get("brand"),
                "new_image": img
            })

    # Guardar data/products.json actualizado
    with open(PRODUCTS_JSON, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    # Actualizar manifiesto
    total_sku_mappings = sum(len(grp.get("codes", [])) for grp in existing_groups)
    manifest["total_catalog_groups"] = len(existing_groups)
    manifest["total_sku_mappings"] = total_sku_mappings
    manifest["total_store_products_updated"] = len(all_truper_products)
    manifest["groups"] = existing_groups
    manifest["updated_products"] = all_truper_products

    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 75)
    print("¡MÓDULO D COMPLETADO CON ÉXITO!")
    print(f"  - Total Familias Visuales en Manifiesto: {len(existing_groups)} (antes 566)")
    print(f"  - Total Códigos / Claves Catalogadas: {total_sku_mappings}")
    print(f"  - Total Artículos de Tienda con Fotos Oficiales: {len(all_truper_products)} (antes 985)")
    print("=" * 75)

if __name__ == "__main__":
    run()
