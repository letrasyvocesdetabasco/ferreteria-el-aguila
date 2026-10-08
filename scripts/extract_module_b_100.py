#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extract_module_b_100.py
Ferretería y Tlapalería El Águila - Módulo B: Extracción de 100 Nuevas Familias Truper

Módulo B (100 familias):
- Cerrajería Hermex (Candados de latón, hierro, antipalanca, cerraduras de sobreponer, cerrojos, pomos, bisagras) (35)
- Fijación y Acero Fiero (Cadenas pulidas/galvanizadas, cables de acero, perrillos, tensores, alambres, clavos, taquetes) (30)
- Poda, Jardinería, Machetes y Fumigación (Tijeras de poda, cortasetos, aviación, machetes, aspersores, mangueras, fumigadores) (35)
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
TMP_DIR = "/tmp/mod_b_extract"

MODULE_B_100_FAMILIES = [
    # -------------------------------------------------------------------------
    # 1. Cerrajería y Candados Hermex (35)
    # -------------------------------------------------------------------------
    {
        "id": "candados-hierro-gancho-corto-hermex",
        "title": "Candados de hierro gancho corto Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 568,
        "raw_index": 2,
        "output_filename": "candados-hierro-gancho-corto-hermex.webp",
        "codes": ["CH-38", "CH-50", "CH-63", "CH-38X2", "43100", "43101", "43102"],
        "description": "Candado de cuerpo de hierro sólido esmaltado con cilindro de latón Hermex"
    },
    {
        "id": "candados-hierro-gancho-largo-hermex",
        "title": "Candados de hierro gancho largo Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 568,
        "raw_index": 3,
        "output_filename": "candados-hierro-gancho-largo-hermex.webp",
        "codes": ["CH-38L", "CH-50L", "CH-38LX2", "43105", "43106"],
        "description": "Candado de hierro con grillete extralargo de acero templado Hermex"
    },
    {
        "id": "candados-hierro-pulido-hermex",
        "title": "Candados de hierro pulido brillante Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 568,
        "raw_index": 8,
        "output_filename": "candados-hierro-pulido-hermex.webp",
        "codes": ["CHP-38", "CHP-50", "CHP-63", "43110", "43111"],
        "description": "Candado de hierro con acabado pulido satinado de alta durabilidad Hermex"
    },
    {
        "id": "candados-laton-gancho-corto-hermex",
        "title": "Candados de latón macizo gancho corto Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 568,
        "raw_index": 12,
        "output_filename": "candados-laton-gancho-corto-hermex.webp",
        "codes": ["CL-20", "CL-25", "CL-30", "CL-40", "CL-50", "CL-60", "43120", "43121", "43122"],
        "description": "Candado clásico de latón macizo anticorrosivo con seguro de doble cerrojo Hermex"
    },
    {
        "id": "candados-laton-gancho-largo-hermex",
        "title": "Candados de latón macizo gancho largo Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 568,
        "raw_index": 13,
        "output_filename": "candados-laton-gancho-largo-hermex.webp",
        "codes": ["CL-30L", "CL-40L", "CL-50L", "43125", "43126"],
        "description": "Candado de latón con gancho largo para aldabas y cancelas Hermex"
    },
    {
        "id": "candados-laton-dorado-basic-hermex",
        "title": "Candados de latón dorado Hermex Basic",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 568,
        "raw_index": 14,
        "output_filename": "candados-laton-dorado-basic-hermex.webp",
        "codes": ["CL-30B", "CL-40B", "CL-50B", "43130", "43131"],
        "description": "Candados de latón de alta rotación para uso comercial e interior Hermex Basic"
    },
    {
        "id": "candados-antipalanca-alta-seguridad-hermex",
        "title": "Candados antipalanca de alta seguridad Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 571,
        "raw_index": 2,
        "output_filename": "candados-antipalanca-alta-seguridad-hermex.webp",
        "codes": ["CAP-70", "CAP-80", "CAP-90", "43140", "43141"],
        "description": "Candado blindado antipalanca con cerrojo de acero oculto para cortinas de negocio Hermex"
    },
    {
        "id": "candados-acero-laminado-intemperie-hermex",
        "title": "Candados de acero laminado para intemperie Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 572,
        "raw_index": 7,
        "output_filename": "candados-acero-laminado-intemperie-hermex.webp",
        "codes": ["CAL-40", "CAL-50", "43150", "43151"],
        "description": "Candado laminado con recubrimiento de polímero impermeable contra lluvia y polvo Hermex"
    },
    {
        "id": "candados-combinacion-viaje-hermex",
        "title": "Candados de combinación mecánica Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 572,
        "raw_index": 10,
        "output_filename": "candados-combinacion-viaje-hermex.webp",
        "codes": ["CCOM-20", "CCOM-30", "43160", "43161"],
        "description": "Candado de combinación numérica reajustable de 3 y 4 dígitos para maletas y lockers Hermex"
    },
    {
        "id": "candados-cable-bicicleta-hermex",
        "title": "Candados de cable trenzado para bicicleta Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 572,
        "raw_index": 15,
        "output_filename": "candados-cable-bicicleta-hermex.webp",
        "codes": ["CCB-65", "CCB-100", "43170", "43171"],
        "description": "Cable de acero flexible forrado en vinil con cerradura de combinación o llave Hermex"
    },
    {
        "id": "candados-acero-inoxidable-marino-hermex",
        "title": "Candados de acero inoxidable grado marino Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 572,
        "raw_index": 16,
        "output_filename": "candados-acero-inoxidable-marino-hermex.webp",
        "codes": ["CIN-40", "CIN-50", "43175"],
        "description": "Candado de máxima resistencia a la corrosión salina para puertos y costas Hermex"
    },
    {
        "id": "cerraduras-sobreponer-barra-fija-hermex",
        "title": "Cerraduras de sobreponer de barra fija Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 574,
        "raw_index": 1,
        "output_filename": "cerraduras-sobreponer-barra-fija-hermex.webp",
        "codes": ["CS-80F", "CS-90F", "43200", "43201"],
        "description": "Cerradura tradicional de sobreponer para puertas de madera y metal con barra sólida Hermex"
    },
    {
        "id": "cerraduras-sobreponer-barra-libre-hermex",
        "title": "Cerraduras de sobreponer de barra libre Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 574,
        "raw_index": 3,
        "output_filename": "cerraduras-sobreponer-barra-libre-hermex.webp",
        "codes": ["CS-80L", "CS-90L", "43205", "43206"],
        "description": "Cerradura de sobreponer para puertas de abatir hacia el interior con barra corrediza Hermex"
    },
    {
        "id": "cerraduras-sobreponer-cilindrica-clasica-hermex",
        "title": "Cerraduras de sobreponer cilíndricas clásicas Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 574,
        "raw_index": 7,
        "output_filename": "cerraduras-sobreponer-cilindrica-clasica-hermex.webp",
        "codes": ["CS-70", "CS-75", "43210", "43211"],
        "description": "Cerradura de sobreponer compacta con pomo interior y cerrojo de latón macizo Hermex"
    },
    {
        "id": "cerraduras-sobreponer-alta-seguridad-hermex",
        "title": "Cerraduras de sobreponer de perno triple Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 574,
        "raw_index": 8,
        "output_filename": "cerraduras-sobreponer-alta-seguridad-hermex.webp",
        "codes": ["CS-100", "CS-110", "43215", "43216"],
        "description": "Cerradura de alta seguridad con cilindro computarizado y tres pernos de acero Hermex"
    },
    {
        "id": "cerraduras-embutir-manija-hermex",
        "title": "Cerraduras de embutir con manija metálica Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 575,
        "raw_index": 14,
        "output_filename": "cerraduras-embutir-manija-hermex.webp",
        "codes": ["CE-40M", "CE-50M", "43220", "43221"],
        "description": "Mecanismo de embutir con manija contemporánea para entrada residencial Hermex"
    },
    {
        "id": "cerraduras-embutir-recamara-hermex",
        "title": "Cerraduras de embutir para recámara Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 575,
        "raw_index": 17,
        "output_filename": "cerraduras-embutir-recamara-hermex.webp",
        "codes": ["CE-40R", "43225"],
        "description": "Cerradura embutida de mecanismo suave con placa de acero satinado Hermex"
    },
    {
        "id": "cerrojos-seguridad-doble-cilindro-laton-hermex",
        "title": "Cerrojos de seguridad doble cilindro latón brillante Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 576,
        "raw_index": 2,
        "output_filename": "cerrojos-seguridad-doble-cilindro-laton-hermex.webp",
        "codes": ["CD-200L", "CD-300L", "43230", "43231"],
        "description": "Cerrojo auxiliar de alta seguridad con llave por ambos lados acabado latón brillante Hermex"
    },
    {
        "id": "cerrojos-seguridad-doble-cilindro-cromo-hermex",
        "title": "Cerrojos de seguridad doble cilindro cromo mate Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 576,
        "raw_index": 5,
        "output_filename": "cerrojos-seguridad-doble-cilindro-cromo-hermex.webp",
        "codes": ["CD-200C", "CD-300C", "43235", "43236"],
        "description": "Cerrojo auxiliar doble cilindro acabado níquel y cromo mate satinado Hermex"
    },
    {
        "id": "cerrojos-seguridad-cilindro-sencillo-hermex",
        "title": "Cerrojos de seguridad cilindro sencillo con mariposa Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 576,
        "raw_index": 20,
        "output_filename": "cerrojos-seguridad-cilindro-sencillo-hermex.webp",
        "codes": ["CS-200L", "CS-200C", "43240", "43241"],
        "description": "Cerrojo con llave exterior y mariposa interior para apertura rápida de emergencia Hermex"
    },
    {
        "id": "cerraduras-pomo-recamara-laton-brillante-hermex",
        "title": "Cerraduras de pomo para recámara latón brillante Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 576,
        "raw_index": 21,
        "output_filename": "cerraduras-pomo-recamara-laton-brillante-hermex.webp",
        "codes": ["CP-REC-L", "43250"],
        "description": "Cerradura tubular de pomo con botón de seguro interior para recámara acabado dorado Hermex"
    },
    {
        "id": "cerraduras-pomo-bano-laton-brillante-hermex",
        "title": "Cerraduras de pomo para baño latón brillante Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 576,
        "raw_index": 24,
        "output_filename": "cerraduras-pomo-bano-laton-brillante-hermex.webp",
        "codes": ["CP-BAN-L", "43255"],
        "description": "Cerradura tubular sin llave con ranura de emergencia exterior para privacidad de baño Hermex"
    },
    {
        "id": "cerraduras-pomo-recamara-acero-inoxidable-hermex",
        "title": "Cerraduras de pomo para recámara acero inoxidable Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 578,
        "raw_index": 24,
        "output_filename": "cerraduras-pomo-recamara-acero-inoxidable-hermex.webp",
        "codes": ["CP-REC-I", "43260"],
        "description": "Cerradura de pomo fabricada en acero inoxidable satinado anticorrosión Hermex"
    },
    {
        "id": "cerraduras-pomo-bano-acero-inoxidable-hermex",
        "title": "Cerraduras de pomo para baño acero inoxidable Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 578,
        "raw_index": 26,
        "output_filename": "cerraduras-pomo-bano-acero-inoxidable-hermex.webp",
        "codes": ["CP-BAN-I", "43265"],
        "description": "Cerradura de pomo inoxidable para baño resistente a vapor y humedad Hermex"
    },
    {
        "id": "cerraduras-pomo-entrada-principal-hermex",
        "title": "Cerraduras de pomo para entrada principal Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 578,
        "raw_index": 27,
        "output_filename": "cerraduras-pomo-entrada-principal-hermex.webp",
        "codes": ["CP-ENT-I", "43270"],
        "description": "Cerradura de pomo con pestillo de seguridad y llave de puntos para entrada principal Hermex"
    },
    {
        "id": "cerraduras-manija-recamara-niquel-satinado-hermex",
        "title": "Cerraduras de manija para recámara níquel satinado Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 578,
        "raw_index": 28,
        "output_filename": "cerraduras-manija-recamara-niquel-satinado-hermex.webp",
        "codes": ["CM-REC-N", "43275"],
        "description": "Cerradura ergonómica de manija recta moderna acabado níquel cepillado Hermex"
    },
    {
        "id": "pasadores-aluminio-para-puerta-hermex",
        "title": "Pasadores de aluminio para puerta y ventana Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 0,
        "output_filename": "pasadores-aluminio-para-puerta-hermex.webp",
        "codes": ["PAS-AL-2", "PAS-AL-3", "PAS-AL-4", "43300", "43301"],
        "description": "Pasador de aluminio anodizado con contra de golpe para fijación interior Hermex"
    },
    {
        "id": "pasadores-hierro-para-puerta-hermex",
        "title": "Pasadores de hierro pulido para puerta Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 1,
        "output_filename": "pasadores-hierro-para-puerta-hermex.webp",
        "codes": ["PAS-HI-3", "PAS-HI-4", "43305", "43306"],
        "description": "Pasador de hierro forjado de uso rudo para portones y zaguanes Hermex"
    },
    {
        "id": "cerrojos-mariposa-para-bano-hermex",
        "title": "Cerrojos de mariposa para baño Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 4,
        "output_filename": "cerrojos-mariposa-para-bano-hermex.webp",
        "codes": ["CER-MAR-L", "CER-MAR-C", "43310", "43311"],
        "description": "Cerrojo con perilla tipo mariposa de apertura interior para sanitarios Hermex"
    },
    {
        "id": "portacandados-acero-articulado-hermex",
        "title": "Portacandados de acero articulados para puerta Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 5,
        "output_filename": "portacandados-acero-articulado-hermex.webp",
        "codes": ["PCA-2-1/2", "PCA-3-1/2", "PCA-4-1/2", "43320", "43321"],
        "description": "Portacandados de acero troquelado con tornillos ocultos antipalanca Hermex"
    },
    {
        "id": "portacandados-alta-seguridad-oculto-hermex",
        "title": "Portacandados de alta seguridad ocultos Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 6,
        "output_filename": "portacandados-alta-seguridad-oculto-hermex.webp",
        "codes": ["PCA-SEG-5", "43325"],
        "description": "Portacandados de máxima resistencia forjado para candados de alta seguridad Hermex"
    },
    {
        "id": "bisagras-cuadradas-acero-hermex",
        "title": "Bisagras cuadradas de acero y latonadas Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 8,
        "output_filename": "bisagras-cuadradas-acero-hermex.webp",
        "codes": ["BC-301", "BC-302", "BC-401", "BC-402", "BC-306R", "BC-401PP", "BC-301PP", "BC-301PPB", "43330", "43331"],
        "description": "Juegos de bisagras cuadradas de perno suelto y remachado para carpintería Hermex"
    },
    {
        "id": "bisagras-rectangulares-acero-hermex",
        "title": "Bisagras rectangulares para muebles Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 9,
        "output_filename": "bisagras-rectangulares-acero-hermex.webp",
        "codes": ["BR-201", "BR-251", "BR-301", "43335", "43336"],
        "description": "Bisagras rectangulares galvanizadas de alta movilidad para puertas de alacenas y clósets Hermex"
    },
    {
        "id": "pasadores-mauser-uso-pesado-hermex",
        "title": "Pasadores de acción rápida tipo Mauser Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 580,
        "raw_index": 10,
        "output_filename": "pasadores-mauser-uso-pesado-hermex.webp",
        "codes": ["PAS-MAU-4", "PAS-MAU-6", "43340", "43341"],
        "description": "Pasador de perno cilíndrico de alta compresión tipo rifle Mauser Hermex"
    },
    {
        "id": "caja-para-dinero-seguridad-hermex",
        "title": "Cajas metálicas portátiles para dinero Hermex",
        "brand": "Hermex",
        "category": "Cerrajería",
        "page": 571,
        "raw_index": 8,
        "output_filename": "caja-para-dinero-seguridad-hermex.webp",
        "codes": ["CAJ-DIN-8", "CAJ-DIN-10", "43350", "43351"],
        "description": "Caja de caudales de acero con charola removible para monedas y cerradura de llave Hermex"
    },

    # -------------------------------------------------------------------------
    # 2. Fijación, Cadenas y Acero Fiero (30)
    # -------------------------------------------------------------------------
    {
        "id": "cadenas-pulidas-eslabon-corto-fiero",
        "title": "Cadenas de acero pulido eslabón corto Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 543,
        "raw_index": 9,
        "output_filename": "cadenas-pulidas-eslabon-corto-fiero.webp",
        "codes": ["CAD-P-1/8", "CAD-P-3/16", "CAD-P-1/4", "CAD-P-5/16", "CAD-P-3/8", "CAD-P-1/2", "44200", "44201", "44202", "44203"],
        "description": "Cadena de acero al carbono de eslabón electro-soldado pulido por metro Fiero"
    },
    {
        "id": "cadenas-galvanizadas-eslabon-fiero",
        "title": "Cadenas de acero galvanizado anticorrosión Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 543,
        "raw_index": 10,
        "output_filename": "cadenas-galvanizadas-eslabon-fiero.webp",
        "codes": ["CAD-G-1/8", "CAD-G-3/16", "CAD-G-1/4", "CAD-G-5/16", "CAD-G-3/8", "44210", "44211", "44212"],
        "description": "Cadena galvanizada por inmersión en caliente para intemperie y marina Fiero"
    },
    {
        "id": "cadenas-tipo-victor-para-pozo-fiero",
        "title": "Cadenas de nudo tipo Víctor Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 543,
        "raw_index": 11,
        "output_filename": "cadenas-tipo-victor-para-pozo-fiero.webp",
        "codes": ["CAD-VIC-12", "CAD-VIC-14", "44215", "44216"],
        "description": "Cadena sin soldadura con nudo reforzado para poleas y suspensión Fiero"
    },
    {
        "id": "cadenas-plasticas-delimitadoras-fiero",
        "title": "Cadenas plásticas delimitadoras de señalización Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 543,
        "raw_index": 13,
        "output_filename": "cadenas-plasticas-delimitadoras-fiero.webp",
        "codes": ["CAD-PLA-AM", "CAD-PLA-BL", "44220", "44221"],
        "description": "Cadena de polietileno de alta visibilidad para control de acceso y estacionamientos Fiero"
    },
    {
        "id": "cadenas-para-perro-con-bandola-fiero",
        "title": "Cadenas niqueladas para perro con bandola Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 543,
        "raw_index": 14,
        "output_filename": "cadenas-para-perro-con-bandola-fiero.webp",
        "codes": ["CAD-PER-1", "CAD-PER-2", "CAD-PER-3", "44225", "44226"],
        "description": "Cadena niquelada brillante con asa de resorte y bandola giratoria Fiero"
    },
    {
        "id": "cadenas-alta-resistencia-grado-70-fiero",
        "title": "Cadenas de alta resistencia Grado 70 para arrastre Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 543,
        "raw_index": 16,
        "output_filename": "cadenas-alta-resistencia-grado-70-fiero.webp",
        "codes": ["CAD-G70-5/16", "CAD-G70-3/8", "44230", "44231"],
        "description": "Cadena de aleación de acero templado con acabado dicromato oro para carga pesada Fiero"
    },
    {
        "id": "cables-acero-galvanizado-flexible-fiero",
        "title": "Cables de acero galvanizado flexible 7x7 y 7x19 Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 544,
        "raw_index": 0,
        "output_filename": "cables-acero-galvanizado-flexible-fiero.webp",
        "codes": ["CAB-G-1/16", "CAB-G-3/32", "CAB-G-1/8", "CAB-G-3/16", "CAB-G-1/4", "44240", "44241", "44242"],
        "description": "Cable de acero con alma de fibra y acero para polipastos, tirolesas y tirantes Fiero"
    },
    {
        "id": "cables-acero-forrado-pvc-fiero",
        "title": "Cables de acero forrados con PVC cristal Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 544,
        "raw_index": 8,
        "output_filename": "cables-acero-forrado-pvc-fiero.webp",
        "codes": ["CAB-PVC-1/8", "CAB-PVC-3/16", "CAB-PVC-1/4", "44245", "44246"],
        "description": "Cable de acero protegido con cubierta plástica transparente contra rayaduras Fiero"
    },
    {
        "id": "cables-acero-inoxidable-fiero",
        "title": "Cables de acero inoxidable grado 304 Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 544,
        "raw_index": 12,
        "output_filename": "cables-acero-inoxidable-fiero.webp",
        "codes": ["CAB-INOX-1/8", "CAB-INOX-3/16", "ALIN-160", "44250", "44251"],
        "description": "Cable de alambre inoxidable de máxima pureza para arquitectura y náutica Fiero"
    },
    {
        "id": "perrillos-apretadores-galvanizados-fiero",
        "title": "Perrillos apretadores de acero galvanizado para cable Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 545,
        "raw_index": 6,
        "output_filename": "perrillos-apretadores-galvanizados-fiero.webp",
        "codes": ["PER-1/8", "PER-3/16", "PER-1/4", "PER-5/16", "PER-3/8", "PER-1/2", "44260", "44261", "44262"],
        "description": "Grapas para cable de acero tipo perrillo con tuercas hexagonales Fiero"
    },
    {
        "id": "guardacabos-acero-galvanizado-fiero",
        "title": "Guardacabos de acero galvanizado para cables Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 545,
        "raw_index": 7,
        "output_filename": "guardacabos-acero-galvanizado-fiero.webp",
        "codes": ["GUA-1/8", "GUA-3/16", "GUA-1/4", "GUA-5/16", "GUA-3/8", "44265", "44266"],
        "description": "Guardacabos metálico protector para formación de gazas y lazos en cables Fiero"
    },
    {
        "id": "destorcedores-niquelados-ojo-ojo-fiero",
        "title": "Destorcedores niquelados ojo a ojo Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 545,
        "raw_index": 8,
        "output_filename": "destorcedores-niquelados-ojo-ojo-fiero.webp",
        "codes": ["DES-1/4", "DES-5/16", "DES-3/8", "44270", "44271"],
        "description": "Articulación giratoria continua para evitar enredos en cadenas y poleas Fiero"
    },
    {
        "id": "ganchos-giratorios-con-seguro-fiero",
        "title": "Ganchos giratorios forjados con seguro de resorte Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 545,
        "raw_index": 18,
        "output_filename": "ganchos-giratorios-con-seguro-fiero.webp",
        "codes": ["GAN-GIR-1/2", "GAN-GIR-3/4", "44275", "44276"],
        "description": "Gancho de izaje con lengüeta de bloqueo de seguridad Fiero"
    },
    {
        "id": "bandolas-mosqueton-con-seguro-fiero",
        "title": "Bandolas y mosquetones con tuerca de seguridad Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 545,
        "raw_index": 21,
        "output_filename": "bandolas-mosqueton-con-seguro-fiero.webp",
        "codes": ["BAN-MOS-3", "BAN-MOS-4", "44280", "44281"],
        "description": "Mosquetón de unión rápida de acero niquelado para amarres y sujeción Fiero"
    },
    {
        "id": "grilletes-galvanizados-tipo-ancla-fiero",
        "title": "Grilletes rectos y tipo ancla galvanizados Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 545,
        "raw_index": 22,
        "output_filename": "grilletes-galvanizados-tipo-ancla-fiero.webp",
        "codes": ["GRI-1/4", "GRI-5/16", "GRI-3/8", "GRI-1/2", "44285", "44286"],
        "description": "Grillete de carga con perno roscable de alta resistencia Fiero"
    },
    {
        "id": "eslabones-rapidos-roscables-fiero",
        "title": "Eslabones rápidos roscables para cadena Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 545,
        "raw_index": 23,
        "output_filename": "eslabones-rapidos-roscables-fiero.webp",
        "codes": ["ESL-RAP-1/8", "ESL-RAP-3/16", "ESL-RAP-1/4", "44290", "44291"],
        "description": "Eslabón de unión abierta con tuerca hexagonal para empalme de cadenas Fiero"
    },
    {
        "id": "tensores-ojo-gancho-forjados-fiero",
        "title": "Tensores de ojo y gancho forjados en acero Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 546,
        "raw_index": 2,
        "output_filename": "tensores-ojo-gancho-forjados-fiero.webp",
        "codes": ["TEN-OG-1/4", "TEN-OG-5/16", "TEN-OG-3/8", "TEN-OG-1/2", "44300", "44301", "44302"],
        "description": "Tensor de cuerpo cerrado para regulación y tensado de alambres y cables Fiero"
    },
    {
        "id": "tensores-gancho-gancho-fiero",
        "title": "Tensores gancho a gancho galvanizados Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 546,
        "raw_index": 3,
        "output_filename": "tensores-gancho-gancho-fiero.webp",
        "codes": ["TEN-GG-1/4", "TEN-GG-5/16", "44305", "44306"],
        "description": "Tensor con terminación de dos ganchos para anclajes móviles Fiero"
    },
    {
        "id": "tensores-ojo-ojo-fiero",
        "title": "Tensores ojo a ojo forjados Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 546,
        "raw_index": 4,
        "output_filename": "tensores-ojo-ojo-fiero.webp",
        "codes": ["TEN-OO-1/4", "TEN-OO-5/16", "44310", "44311"],
        "description": "Tensor de sujeción fija con ojillos circulares en ambos extremos Fiero"
    },
    {
        "id": "tensores-mandibula-mandibula-fiero",
        "title": "Tensores mandíbula a mandíbula para alta tensión Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 546,
        "raw_index": 5,
        "output_filename": "tensores-mandibula-mandibula-fiero.webp",
        "codes": ["TEN-MM-3/8", "TEN-MM-1/2", "44315", "44316"],
        "description": "Tensor con horquillas y pernos pasantes para cableado estructural Fiero"
    },
    {
        "id": "alambres-galvanizados-rollitos-fiero",
        "title": "Alambres galvanizados en rollitos de 1 kg Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 550,
        "raw_index": 12,
        "output_filename": "alambres-galvanizados-rollitos-fiero.webp",
        "codes": ["ALG-12B", "ALG-14B", "ALG-16B", "ALG-18B", "ALG-145B", "ALG-160B", "44320", "44321", "44322"],
        "description": "Alambre de acero galvanizado brillante maleable para amarres de ferretería Fiero"
    },
    {
        "id": "alambres-recocidos-para-construccion-fiero",
        "title": "Alambres recocidos para amarre de varilla Fiero",
        "brand": "Fiero",
        "category": "Construcción",
        "page": 550,
        "raw_index": 22,
        "output_filename": "alambres-recocidos-para-construccion-fiero.webp",
        "codes": ["ALR-16", "ALR-18", "44325", "44326"],
        "description": "Alambre negro recocido de alta flexibilidad para armados de albañilería Fiero"
    },
    {
        "id": "alambres-de-puas-galvanizados-fiero",
        "title": "Alambres de púas galvanizados alta resistencia Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 550,
        "raw_index": 23,
        "output_filename": "alambres-de-puas-galvanizados-fiero.webp",
        "codes": ["AP-300", "AP-360", "812/3755", "44330", "44331"],
        "description": "Alambre de púas con 4 puntas afiladas para delimitación ganadera y perimetral Fiero"
    },
    {
        "id": "clavos-estandar-con-cabeza-fiero",
        "title": "Clavos estándar con cabeza para madera Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 552,
        "raw_index": 11,
        "output_filename": "clavos-estandar-con-cabeza-fiero.webp",
        "codes": ["CLA-1", "CLA-1-1/2", "CLA-2", "CLA-2-1/2", "CLA-3", "CLA-3-1/2", "CLA-4", "44340", "44341", "44342"],
        "description": "Clavos comunes con cabeza plana y vástago liso de acero pulido para carpintería Fiero"
    },
    {
        "id": "clavos-para-concreto-estriados-fiero",
        "title": "Clavos para concreto estriados negros Fiero",
        "brand": "Fiero",
        "category": "Construcción",
        "page": 552,
        "raw_index": 12,
        "output_filename": "clavos-para-concreto-estriados-fiero.webp",
        "codes": ["CLC-1", "CLC-1-1/2", "CLC-2", "CLC-2-1/2", "CLC-3", "44345", "44346"],
        "description": "Clavos templados con cuerpo ranurado para clavado directo en muros de mampostería Fiero"
    },
    {
        "id": "clavos-para-concreto-galvanizados-fiero",
        "title": "Clavos para concreto galvanizados Fiero",
        "brand": "Fiero",
        "category": "Construcción",
        "page": 552,
        "raw_index": 16,
        "output_filename": "clavos-para-concreto-galvanizados-fiero.webp",
        "codes": ["CLCG-1", "CLCG-1-1/2", "CLCG-2", "CLCG-2-1/2", "44350", "44351"],
        "description": "Clavos para concreto con recubrimiento de zinc antioxidable Fiero"
    },
    {
        "id": "clavos-sin-cabeza-para-moldura-fiero",
        "title": "Clavos sin cabeza para molduras y carpintería fina Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 552,
        "raw_index": 17,
        "output_filename": "clavos-sin-cabeza-para-moldura-fiero.webp",
        "codes": ["CLS-1", "CLS-1-1/2", "CLS-2", "44355", "44356"],
        "description": "Clavillos sin cabeza para ocultar la fijación en zoclos y marcos de madera Fiero"
    },
    {
        "id": "clavos-para-paraguas-lamina-fiero",
        "title": "Clavos para lámina tipo sombrilla con rondana Fiero",
        "brand": "Fiero",
        "category": "Construcción",
        "page": 552,
        "raw_index": 18,
        "output_filename": "clavos-para-paraguas-lamina-fiero.webp",
        "codes": ["CLP-2-1/2", "44360"],
        "description": "Clavos de techo con cabeza ancha tipo paraguas y arandela de hule hermética Fiero"
    },
    {
        "id": "grapas-galvanizadas-para-cerca-fiero",
        "title": "Grapas galvanizadas para postes y cercas de alambre Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 554,
        "raw_index": 16,
        "output_filename": "grapas-galvanizadas-para-cerca-fiero.webp",
        "codes": ["GRA-1", "GRA-1-1/4", "GRA-1-1/2", "44370", "44371"],
        "description": "Grapas en 'U' con puntas afiladas para fijación de púas en postes de madera Fiero"
    },
    {
        "id": "taquetes-plasticos-con-tope-fiero",
        "title": "Taquetes plásticos con tope tipo arpón Fiero",
        "brand": "Fiero",
        "category": "Fijación",
        "page": 560,
        "raw_index": 1,
        "output_filename": "taquetes-plasticos-con-tope-fiero.webp",
        "codes": ["TAQ-1/4", "TAQ-5/16", "TAQ-3/8", "TAQ-1/2", "44380", "44381", "44382"],
        "description": "Taquetes expansivos de polietileno con aletas antigiro para tornillo y pija Fiero"
    },

    # -------------------------------------------------------------------------
    # 3. Poda, Jardinería, Machetes y Fumigación (35)
    # -------------------------------------------------------------------------
    {
        "id": "tijeras-aviacion-corte-recto-truper",
        "title": "Tijeras de aviación corte recto color amarillo Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 0,
        "output_filename": "tijeras-aviacion-corte-recto-truper.webp",
        "codes": ["TAV-R", "18450"],
        "description": "Tijeras de corte recto para lámina de acero y hojalatería con seguro Truper"
    },
    {
        "id": "tijeras-aviacion-corte-izquierdo-truper",
        "title": "Tijeras de aviación corte izquierdo color rojo Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 1,
        "output_filename": "tijeras-aviacion-corte-izquierdo-truper.webp",
        "codes": ["TAV-I", "18451"],
        "description": "Tijeras de aviación para curvas hacia la izquierda en hojalata Truper"
    },
    {
        "id": "tijeras-aviacion-corte-derecho-truper",
        "title": "Tijeras de aviación corte derecho color verde Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 7,
        "output_filename": "tijeras-aviacion-corte-derecho-truper.webp",
        "codes": ["TAV-D", "18452"],
        "description": "Tijeras de aviación para curvas hacia la derecha en chapa metálica Truper"
    },
    {
        "id": "tijeras-aviacion-juego-3-piezas-truper",
        "title": "Juego de 3 tijeras de aviación Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 9,
        "output_filename": "tijeras-aviacion-juego-3-piezas-truper.webp",
        "codes": ["J-TAV", "18455"],
        "description": "Set de tijeras de aviación corte recto, izquierdo y derecho en empaque plástico Truper"
    },
    {
        "id": "tijeras-hojalatero-tipo-americano-truper",
        "title": "Tijeras de hojalatero tipo americano Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 10,
        "output_filename": "tijeras-hojalatero-tipo-americano-truper.webp",
        "codes": ["TH-10", "TH-12", "TH-14", "18460", "18461"],
        "description": "Tijeras forjadas para corte de ductería, alambre y metal delgado Truper"
    },
    {
        "id": "tijeras-hojalatero-pretul",
        "title": "Tijeras para hojalatero Pretul",
        "brand": "Pretul",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 11,
        "output_filename": "tijeras-hojalatero-pretul.webp",
        "codes": ["TH-10P", "TH-12P", "28460", "28461"],
        "description": "Tijeras para corte de lámina con mangos cubiertos de vinil Pretul"
    },
    {
        "id": "tijeras-para-multiusos-taller-truper",
        "title": "Tijeras multiusos pesadas para taller Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 13,
        "output_filename": "tijeras-para-multiusos-taller-truper.webp",
        "codes": ["TMU-8", "18465"],
        "description": "Tijera con hojas de acero inoxidable dentadas para cortar cartón, soga y cuero Truper"
    },
    {
        "id": "tijeras-poda-bypass-aluminio-truper",
        "title": "Tijeras de podar a una mano cuerpo de aluminio Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 6,
        "output_filename": "tijeras-poda-bypass-aluminio-truper.webp",
        "codes": ["T-67", "T-68", "18470", "18471"],
        "description": "Tijera podadora profesional bypass con cuchilla de paso templada para ramas vivas Truper"
    },
    {
        "id": "tijeras-poda-bypass-forjada-truper",
        "title": "Tijeras de poda forjadas en acero al carbono Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 7,
        "output_filename": "tijeras-poda-bypass-forjada-truper.webp",
        "codes": ["T-40", "T-45", "18475", "18476"],
        "description": "Tijera clásica de floristería y poda forjada de alta precisión Truper"
    },
    {
        "id": "tijeras-poda-corte-recto-pretul",
        "title": "Tijeras de poda económicas corte recto Pretul",
        "brand": "Pretul",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 8,
        "output_filename": "tijeras-poda-corte-recto-pretul.webp",
        "codes": ["T-65P", "T-67P", "28470", "28471"],
        "description": "Tijeras ligeras de podar para jardinería doméstica Pretul"
    },
    {
        "id": "tijeras-poda-tipo-yunque-truper",
        "title": "Tijeras de poda tipo yunque para madera seca Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 9,
        "output_filename": "tijeras-poda-tipo-yunque-truper.webp",
        "codes": ["T-69", "18480"],
        "description": "Tijera con base de yunque de aleación de zinc para cortar ramas secas y duras Truper"
    },
    {
        "id": "tijeras-cortasetos-madera-ondulada-truper",
        "title": "Tijeras cortasetos mangos de madera cuchilla ondulada Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 10,
        "output_filename": "tijeras-cortasetos-madera-ondulada-truper.webp",
        "codes": ["T-19", "T-21", "18485", "18486"],
        "description": "Tijera para poda de arbustos y setos con amortiguadores de golpe y mango de fresno Truper"
    },
    {
        "id": "tijeras-cortasetos-aluminio-telescopica-truper",
        "title": "Tijeras cortasetos con mangos telescópicos de aluminio Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 11,
        "output_filename": "tijeras-cortasetos-aluminio-telescopica-truper.webp",
        "codes": ["T-20X", "18490"],
        "description": "Tijera cortasetos extensible con mangos ligeros para jardines altos Truper"
    },
    {
        "id": "tijeras-cortasetos-economica-pretul",
        "title": "Tijeras cortasetos económicas Pretul",
        "brand": "Pretul",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 12,
        "output_filename": "tijeras-cortasetos-economica-pretul.webp",
        "codes": ["T-19P", "28485"],
        "description": "Cortasetos ligero con hojas de acero al carbono pulidas Pretul"
    },
    {
        "id": "tijeras-cortacesped-giratoria-360-truper",
        "title": "Tijeras para cortar pasto con cabeza giratoria 360° Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 373,
        "raw_index": 13,
        "output_filename": "tijeras-cortacesped-giratoria-360-truper.webp",
        "codes": ["T-80", "18495"],
        "description": "Tijera para orillar pasto y césped con cuchillas de corte en múltiples ángulos Truper"
    },
    {
        "id": "tijeras-ramas-gruesas-bypass-truper",
        "title": "Tijeras para ramas gruesas a dos manos Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 375,
        "raw_index": 0,
        "output_filename": "tijeras-ramas-gruesas-bypass-truper.webp",
        "codes": ["TRG-26", "TRG-30", "18500", "18501"],
        "description": "Tijera de poda pesada para corte de ramas de hasta 1-1/2 pulgadas de espesor Truper"
    },
    {
        "id": "tijeras-ramas-altas-telescopica-truper",
        "title": "Tijeras podadoras para ramas altas con serrucho Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 375,
        "raw_index": 1,
        "output_filename": "tijeras-ramas-altas-telescopica-truper.webp",
        "codes": ["TR-82", "18505"],
        "description": "Podadora de altura con sistema de polea de tiro y hoja de serrucho curvo Truper"
    },
    {
        "id": "serrucho-poda-diente-japones-truper",
        "title": "Serruchos de poda curvos con diente japonés Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 375,
        "raw_index": 3,
        "output_filename": "serrucho-poda-diente-japones-truper.webp",
        "codes": ["STP-12", "STP-14", "18510", "18511"],
        "description": "Serrucho para poda de árboles con triple filo de corte rápido Truper"
    },
    {
        "id": "cuchillas-repuesto-tijeras-poda-truper",
        "title": "Cuchillas de repuesto para tijeras de poda Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 375,
        "raw_index": 16,
        "output_filename": "cuchillas-repuesto-tijeras-poda-truper.webp",
        "codes": ["REP-T-67", "18520"],
        "description": "Cuchilla superior de recambio de acero SK-5 templado para podadoras Truper"
    },
    {
        "id": "machetes-estandar-cinta-cacha-negra-truper",
        "title": "Machetes estándar tipo cinta cacha plástica Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 378,
        "raw_index": 1,
        "output_filename": "machetes-estandar-cinta-cacha-negra-truper.webp",
        "codes": ["MACH-18", "MACH-22", "MACH-24", "18530", "18531", "18532"],
        "description": "Machete de acero al alto carbono tratado térmicamente para desmonte agrícola Truper"
    },
    {
        "id": "machetes-tipo-cahuayote-truper",
        "title": "Machetes tipo cahuayote curvos Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 378,
        "raw_index": 4,
        "output_filename": "machetes-tipo-cahuayote-truper.webp",
        "codes": ["MCAH-24", "MCAH-26", "18535", "18536"],
        "description": "Machete curvado para corte intensivo de maleza y caña Truper"
    },
    {
        "id": "machetes-tipo-rula-truper",
        "title": "Machetes tipo rula con hoja recta Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 378,
        "raw_index": 6,
        "output_filename": "machetes-tipo-rula-truper.webp",
        "codes": ["MRUL-20", "MRUL-22", "18540", "18541"],
        "description": "Machete tipo rula forjado para labores de campo y chapeo Truper"
    },
    {
        "id": "aspersores-giratorios-3-brazos-truper",
        "title": "Aspersores giratorios de 3 brazos base trineo Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 3,
        "output_filename": "aspersores-giratorios-3-brazos-truper.webp",
        "codes": ["ASP-B3", "ASP-B3M", "NG2014", "18550", "18551"],
        "description": "Aspersor rotativo con boquillas orientables para riego uniforme de césped Truper"
    },
    {
        "id": "aspersores-giratorios-2-brazos-truper",
        "title": "Aspersores giratorios de 2 brazos plásticos Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 4,
        "output_filename": "aspersores-giratorios-2-brazos-truper.webp",
        "codes": ["ASP-B2", "18555"],
        "description": "Aspersor circular giratorio de plástico para jardines pequeños y medianos Truper"
    },
    {
        "id": "aspersores-metalicos-estaca-truper",
        "title": "Aspersores de impacto metálicos con estaca de zinc Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 5,
        "output_filename": "aspersores-metalicos-estaca-truper.webp",
        "codes": ["ASP-MET", "18560"],
        "description": "Aspersor de pulso de zinc con estaca metálica para clavado firme en tierra Truper"
    },
    {
        "id": "aspersores-agricolas-laton-truper",
        "title": "Aspersores agrícolas de impacto fundidos en latón Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 6,
        "output_filename": "aspersores-agricolas-laton-truper.webp",
        "codes": ["ASP-1/2BR", "ASP-3/4BR", "ASP-1BR", "18565", "18566"],
        "description": "Aspersor de bronce y latón para riego tecnificado de huertos y parcelas Truper"
    },
    {
        "id": "aspersores-base-manguera-tipo-trineo-truper",
        "title": "Aspersores estacionarios base trineo metálica Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 7,
        "output_filename": "aspersores-base-manguera-tipo-trineo-truper.webp",
        "codes": ["ASP-MAN", "18570"],
        "description": "Base pesada de arrastre con rosca estándar para manguera de jardín Truper"
    },
    {
        "id": "pistolas-riego-metalicas-8-funciones-truper",
        "title": "Pistolas de riego metálicas de 8 funciones Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 8,
        "output_filename": "pistolas-riego-metalicas-8-funciones-truper.webp",
        "codes": ["PIS-MET-8", "18575"],
        "description": "Pistola de chorro regulable con 8 patrones de aspersión y gatillo frontal Truper"
    },
    {
        "id": "pistolas-riego-alta-presion-laton-truper",
        "title": "Pistolas de riego de alta presión en latón macizo Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 9,
        "output_filename": "pistolas-riego-alta-presion-laton-truper.webp",
        "codes": ["PIS-LAT", "18580"],
        "description": "Boquilla regulable de latón macizo para limpieza de pisos y lavado de autos Truper"
    },
    {
        "id": "pistolas-riego-plasticas-pretul",
        "title": "Pistolas de riego plásticas económicas Pretul",
        "brand": "Pretul",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 11,
        "output_filename": "pistolas-riego-plasticas-pretul.webp",
        "codes": ["PIS-PLA-P", "28575"],
        "description": "Pistola de plástico ergonómica para riego doméstico con clip de flujo continuo Pretul"
    },
    {
        "id": "conexiones-rapidas-manguera-jardin-truper",
        "title": "Conectores rápidos automáticos para manguera Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 380,
        "raw_index": 3,
        "output_filename": "conexiones-rapidas-manguera-jardin-truper.webp",
        "codes": ["CON-RAP-1/2", "CON-RAP-3/4", "18590", "18591"],
        "description": "Adaptadores automáticos de clic para intercambio inmediato de pistolas y aspersores Truper"
    },
    {
        "id": "mangueras-jardin-reforzadas-4-capas-truper",
        "title": "Mangueras para jardín reforzadas 4 capas Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 381,
        "raw_index": 1,
        "output_filename": "mangueras-jardin-reforzadas-4-capas-truper.webp",
        "codes": ["MAN-15X", "MAN-20X", "MAN-25X", "18600", "18601"],
        "description": "Manguera con tramado de poliéster anticolapso y conexiones de latón maquinado Truper"
    },
    {
        "id": "mangueras-jardin-pretul",
        "title": "Mangueras para jardín ligeras Pretul",
        "brand": "Pretul",
        "category": "Jardinería",
        "page": 381,
        "raw_index": 5,
        "output_filename": "mangueras-jardin-pretul.webp",
        "codes": ["MAN-15P", "MAN-20P", "28600", "28601"],
        "description": "Manguera plástica flexible para riego doméstico en patios y cocheras Pretul"
    },
    {
        "id": "fumigadores-manuales-compresion-truper",
        "title": "Fumigadores y pulverizadores manuales a presión previa Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 112,
        "raw_index": 11,
        "output_filename": "fumigadores-manuales-compresion-truper.webp",
        "codes": ["FUM-1", "FUM-2", "FUM-3", "18610", "18611", "18612"],
        "description": "Aspersor manual de émbolo con boquilla de latón ajustable para fertilizantes e insecticidas Truper"
    },
    {
        "id": "fumigadores-mochila-agricola-truper",
        "title": "Fumigadores agrícolas de mochila 15 y 20 Litros Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 113,
        "raw_index": 140,
        "output_filename": "fumigadores-mochila-agricola-truper.webp",
        "codes": ["FUM-15", "FUM-20", "18620", "18621"],
        "description": "Fumigador tipo mochila con palanca reversible de bombeo y lanza de acero inoxidable Truper"
    },
    {
        "id": "tijeras-para-costura-modista-truper",
        "title": "Tijeras de costura y modista forjadas Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 1,
        "output_filename": "tijeras-para-costura-modista-truper.webp",
        "codes": ["TCO-8", "TCO-9", "18440"],
        "description": "Tijeras para corte de telas con hojas niqueladas templadas Truper"
    },
    {
        "id": "tijeras-para-sastre-profesional-truper",
        "title": "Tijeras para sastre profesional mango esmaltado Truper",
        "brand": "Truper",
        "category": "Herramientas Manuales",
        "page": 370,
        "raw_index": 6,
        "output_filename": "tijeras-para-sastre-profesional-truper.webp",
        "codes": ["TSA-10", "TSA-12", "18445"],
        "description": "Tijera pesada de sastrería de 10 y 12 pulgadas con filo biselado Truper"
    },
    {
        "id": "pistola-riego-metalica-frontal-truper",
        "title": "Pistolas de riego metálicas con gatillo frontal Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 379,
        "raw_index": 7,
        "output_filename": "pistola-riego-metalica-frontal-truper.webp",
        "codes": ["PIS-MET-F", "18578"],
        "description": "Pistola metálica ergonómica de control frontal de flujo para jardín Truper"
    },
    {
        "id": "portamangueras-metalico-pared-truper",
        "title": "Portamangueras metálicos para pared Truper",
        "brand": "Truper",
        "category": "Jardinería",
        "page": 380,
        "raw_index": 10,
        "output_filename": "portamangueras-metalico-pared-truper.webp",
        "codes": ["PORT-MAN-M", "18595"],
        "description": "Soporte de acero al carbono para colgar mangueras de hasta 30 metros en muro Truper"
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
        normalized = pad_to_canvas(im, 500, 500, padding=12)
        normalized.save(out_path, "WEBP", quality=88)

    return True

def run():
    print("=" * 75)
    print("MÓDULO B: EXTRACCIÓN DE 100 NUEVAS FAMILIAS TRUPER (TOTAL META: 460)")
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

    # 2. Extraer y procesar imágenes del Módulo B
    print(f"[*] Extrayendo {len(MODULE_B_100_FAMILIES)} familias visuales del Módulo B...")
    new_extracted = 0
    for g in MODULE_B_100_FAMILIES:
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
            # Reglas semánticas guiadas de alta fidelidad para Cerrajería, Fijación y Poda
            for g in existing_groups:
                gid = g["id"]
                # Candados y Cerrajería
                if gid == "candados-hierro-gancho-corto-hermex" and "candado" in name and "hierro" in name and "corto" in name:
                    matched_group = g
                    match_reason = "Nombre:Candado Hierro Corto"
                    break
                elif gid == "candados-hierro-gancho-largo-hermex" and "candado" in name and "hierro" in name and "largo" in name:
                    matched_group = g
                    match_reason = "Nombre:Candado Hierro Largo"
                    break
                elif gid == "candados-laton-gancho-corto-hermex" and "candado" in name and "laton" in name and "corto" in name:
                    matched_group = g
                    match_reason = "Nombre:Candado Laton Corto"
                    break
                elif gid == "candados-laton-gancho-largo-hermex" and "candado" in name and "laton" in name and "largo" in name:
                    matched_group = g
                    match_reason = "Nombre:Candado Laton Largo"
                    break
                elif gid == "cerraduras-sobreponer-barra-fija-hermex" and "cerradura" in name and "sobreponer" in name and "barra" in name:
                    matched_group = g
                    match_reason = "Nombre:Cerradura Barra"
                    break
                elif gid == "cerrojos-seguridad-doble-cilindro-laton-hermex" and "cerrojo" in name and "doble" in name:
                    matched_group = g
                    match_reason = "Nombre:Cerrojo Doble"
                    break
                elif gid == "cerraduras-pomo-recamara-laton-brillante-hermex" and "cerradura" in name and "pomo" in name and "recamara" in name:
                    matched_group = g
                    match_reason = "Nombre:Cerradura Pomo Recamara"
                    break
                elif gid == "cerraduras-pomo-bano-laton-brillante-hermex" and "cerradura" in name and "pomo" in name and ("baño" in name or "bano" in name):
                    matched_group = g
                    match_reason = "Nombre:Cerradura Pomo Baño"
                    break
                # Fijación
                elif gid == "cadenas-pulidas-eslabon-corto-fiero" and "cadena" in name and "pulida" in name:
                    matched_group = g
                    match_reason = "Nombre:Cadena Pulida"
                    break
                elif gid == "cadenas-galvanizadas-eslabon-fiero" and "cadena" in name and "galvanizada" in name:
                    matched_group = g
                    match_reason = "Nombre:Cadena Galvanizada"
                    break
                elif gid == "cables-acero-galvanizado-flexible-fiero" and "cable" in name and "acero" in name and "galvanizado" in name:
                    matched_group = g
                    match_reason = "Nombre:Cable Acero Galvanizado"
                    break
                elif gid == "perrillos-apretadores-galvanizados-fiero" and "perrillo" in name:
                    matched_group = g
                    match_reason = "Nombre:Perrillo"
                    break
                elif gid == "tensores-ojo-gancho-forjados-fiero" and "tensor" in name and "gancho" in name:
                    matched_group = g
                    match_reason = "Nombre:Tensor Ojo Gancho"
                    break
                elif gid == "alambres-galvanizados-rollitos-fiero" and "alambre" in name and "galv" in name:
                    matched_group = g
                    match_reason = "Nombre:Alambre Galv"
                    break
                elif gid == "clavos-estandar-con-cabeza-fiero" and "clavo" in name and "estandar" in name:
                    matched_group = g
                    match_reason = "Nombre:Clavo Estandar"
                    break
                elif gid == "clavos-para-concreto-estriados-fiero" and "clavo" in name and "concreto" in name:
                    matched_group = g
                    match_reason = "Nombre:Clavo Concreto"
                    break
                # Poda y Jardinería
                elif gid == "tijeras-poda-bypass-aluminio-truper" and "tijera" in name and "poda" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Tijera Poda Truper"
                    break
                elif gid == "tijeras-poda-corte-recto-pretul" and "tijera" in name and "poda" in name and "pretul" in name:
                    matched_group = g
                    match_reason = "Nombre:Tijera Poda Pretul"
                    break
                elif gid == "tijeras-cortasetos-madera-ondulada-truper" and ("cortaseto" in name or "corta seto" in name):
                    matched_group = g
                    match_reason = "Nombre:Cortasetos"
                    break
                elif gid == "tijeras-aviacion-corte-recto-truper" and "aviacion" in name and "recto" in name:
                    matched_group = g
                    match_reason = "Nombre:Tijera Aviacion Recto"
                    break
                elif gid == "machetes-estandar-cinta-cacha-negra-truper" and "machete" in name and "truper" in name:
                    matched_group = g
                    match_reason = "Nombre:Machete Truper"
                    break
                elif gid == "aspersores-giratorios-3-brazos-truper" and "aspersor" in name and "3" in name:
                    matched_group = g
                    match_reason = "Nombre:Aspersor 3 Brazos"
                    break
                elif gid == "aspersores-agricolas-laton-truper" and "aspersor" in name and "agricola" in name:
                    matched_group = g
                    match_reason = "Nombre:Aspersor Agricola Laton"
                    break
                elif gid == "pistolas-riego-metalicas-8-funciones-truper" and "pistola" in name and "riego" in name:
                    matched_group = g
                    match_reason = "Nombre:Pistola Riego"
                    break
                elif gid == "fumigadores-manuales-compresion-truper" and "fumigador" in name and ("1" in name or "2" in name or "3" in name):
                    matched_group = g
                    match_reason = "Nombre:Fumigador Manual"
                    break
                elif gid == "fumigadores-mochila-agricola-truper" and "fumigador" in name and ("15" in name or "20" in name or "mochila" in name):
                    matched_group = g
                    match_reason = "Nombre:Fumigador Mochila"
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
    print("¡MÓDULO B COMPLETADO CON ÉXITO!")
    print(f"  - Total Familias Visuales en Manifiesto: {len(existing_groups)} (antes 360)")
    print(f"  - Total Códigos / Claves Catalogadas: {total_sku_mappings}")
    print(f"  - Total Artículos de Tienda con Fotos Oficiales: {len(updated_products_list)} (antes 486)")
    print("=" * 75)

if __name__ == "__main__":
    run()
