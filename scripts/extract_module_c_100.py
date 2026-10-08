#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/extract_module_c_100.py
Ferretería y Tlapalería El Águila - Módulo C: Extracción de 100 Nuevas Familias Truper

Módulo C (100 familias):
- Material Eléctrico e Iluminación Volteck (Linternas recargables, reflectores LED, focos LED, multicontactos, clavijas, portalámparas, sensores, timbres) (50)
- Plomería y Grifería Foset (Regaderas de plato ancho, brazos, mezcladoras fregadero/lavabo, céspoles bote PVC/latón, contrarrejillas, calentadores, cilindros gas, válvulas esfera/globo/compuerta/check, llaves jardín) (50)

Completa la solicitud de +300 familias adicionales:
Módulo A (+100) -> Módulo B (+101) -> Módulo C (+100) = 561 familias totales.
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
TMP_DIR = "/tmp/mod_c_extract"

MODULE_C_100_FAMILIES = [
    # -------------------------------------------------------------------------
    # 1. Material Eléctrico e Iluminación Volteck (50 familias)
    # -------------------------------------------------------------------------
    {
        "id": "linterna-plastica-led-recargable-volteck",
        "title": "Linternas LED plásticas recargables Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 202,
        "raw_index": 24,
        "output_filename": "linterna-plastica-led-recargable-volteck.webp",
        "codes": ["LIRE-145P", "24091", "16005", "13019"],
        "description": "Linterna recargable de alta luminosidad con cuerpo plástico ligero y haz de largo alcance Volteck"
    },
    {
        "id": "linterna-led-plastica-alta-potencia-volteck",
        "title": "Linternas LED plásticas de alta potencia Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 202,
        "raw_index": 27,
        "output_filename": "linterna-led-plastica-alta-potencia-volteck.webp",
        "codes": ["LILE-11T", "LILE-9T", "13018", "13019"],
        "description": "Linterna LED portátil con reflectores de alta eficiencia y diseño ergonómico antideslizante Volteck"
    },
    {
        "id": "lampara-led-plastica-reflector-volteck",
        "title": "Lámparas reflectoras LED plásticas Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 202,
        "raw_index": 41,
        "output_filename": "lampara-led-plastica-reflector-volteck.webp",
        "codes": ["LIPLA-180", "16005", "24091"],
        "description": "Lámpara reflectora de haz amplio para trabajo e inspección nocturna Volteck"
    },
    {
        "id": "linterna-led-recargable-aluminio-volteck",
        "title": "Linternas LED recargables de aluminio de alta resistencia Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 204,
        "raw_index": 12,
        "output_filename": "linterna-led-recargable-aluminio-volteck.webp",
        "codes": ["LIRE-200P", "LINAR-260", "14631", "15143"],
        "description": "Linterna LED táctica recargable con cuerpo maquinado en aluminio anodizado resistente a impactos Volteck"
    },
    {
        "id": "linterna-led-tipo-tactica-recargable-volteck",
        "title": "Linternas tácticas LED recargables uso rudo Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 204,
        "raw_index": 74,
        "output_filename": "linterna-led-tipo-tactica-recargable-volteck.webp",
        "codes": ["LIREX-480", "LAT-2600", "LAT-280", "26070"],
        "description": "Linterna táctica de alta potencia luminosa con lente zoom enfocable y carga USB-C Volteck"
    },
    {
        "id": "linterna-led-tipo-minero-recargable-volteck",
        "title": "Linternas LED recargables tipo minero / cabeza Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 206,
        "raw_index": 21,
        "output_filename": "linterna-led-tipo-minero-recargable-volteck.webp",
        "codes": ["CA-150", "CA-125", "CA-110", "11751", "29089", "28256"],
        "description": "Linterna de cabeza tipo minero manos libres con banda elástica ajustable y múltiples modos de luz Volteck"
    },
    {
        "id": "linterna-led-tipo-minero-pilas-volteck",
        "title": "Linternas de cabeza LED de pilas Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 207,
        "raw_index": 23,
        "output_filename": "linterna-led-tipo-minero-pilas-volteck.webp",
        "codes": ["CA-70", "LIBI-K2", "LACA-3D", "29088", "27083", "29075"],
        "description": "Lámpara de cabeza compacta y ligera para campismo, ciclismo y trabajos en espacios reducidos Volteck"
    },
    {
        "id": "linterna-cabeza-led-multifuncion-volteck",
        "title": "Linternas LED frontales multifunción Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 207,
        "raw_index": 4,
        "output_filename": "linterna-cabeza-led-multifuncion-volteck.webp",
        "codes": ["LIBI-9T", "LIBI-2P", "16796", "16798", "16797", "10760", "27050"],
        "description": "Linterna frontal angular con luz LED puntual y difusa para inspección técnica Volteck"
    },
    {
        "id": "extension-electrica-domestica-polarizada-volteck",
        "title": "Extensiones eléctricas domésticas polarizadas Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 408,
        "raw_index": 2,
        "output_filename": "extension-electrica-domestica-polarizada-volteck.webp",
        "codes": ["ED-2", "ED-3", "ED-4", "ED-5", "ED-6", "ED-8", "ED-10", "48041", "48042", "48043"],
        "description": "Extensión doméstica flexible calibre 16 AWG con tres contactos polarizados y clavija plana Volteck"
    },
    {
        "id": "extension-electrica-reforzada-clavija-plana-volteck",
        "title": "Extensiones eléctricas de uso rudo con clavija plana Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 408,
        "raw_index": 3,
        "output_filename": "extension-electrica-reforzada-clavija-plana-volteck.webp",
        "codes": ["ER-5", "ER-10", "ER-15", "ER-20", "ER-25", "48050", "48051", "48052"],
        "description": "Extensión de uso rudo con recubrimiento de PVC termoplástico retardante a la flama Volteck"
    },
    {
        "id": "lampara-inspeccion-taller-volteck",
        "title": "Lámparas de inspección de taller con rejilla metálica Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 408,
        "raw_index": 25,
        "output_filename": "lampara-inspeccion-taller-volteck.webp",
        "codes": ["AT-15", "AT-15P", "48060", "48061"],
        "description": "Lámpara portátil para mecánica y taller con jaula de protección de acero y gancho giratorio Volteck"
    },
    {
        "id": "multicontacto-barra-supresor-picos-6-entradas-volteck",
        "title": "Multicontactos de barra con supresor de picos 6 entradas Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 412,
        "raw_index": 6,
        "output_filename": "multicontacto-barra-supresor-picos-6-entradas-volteck.webp",
        "codes": ["MUL-6", "MUL-6P", "MUL-6E", "46101", "46102", "46103"],
        "description": "Barra multicontacto de 6 tomas aterrizadas con interruptor breaker de protección contra sobrecarga Volteck"
    },
    {
        "id": "multicontacto-barra-reforzado-8-entradas-volteck",
        "title": "Multicontactos de barra uso rudo 8 entradas Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 412,
        "raw_index": 17,
        "output_filename": "multicontacto-barra-reforzado-8-entradas-volteck.webp",
        "codes": ["MUL-8", "MUL-8P", "MUL-8E", "46108", "46109"],
        "description": "Multicontacto de 8 salidas aterrizadas con gabinete metálico robusto para talleres y centros de cómputo Volteck"
    },
    {
        "id": "multicontacto-cubo-giratorio-volteck",
        "title": "Adaptadores multicontacto tipo cubo giratorio Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 414,
        "raw_index": 11,
        "output_filename": "multicontacto-cubo-giratorio-volteck.webp",
        "codes": ["AD-CU", "AD-3T", "AD-RP", "1500", "1503", "1505", "1506", "1507"],
        "description": "Adaptador multicontacto compacto de 3 tomas con clavija articulada para lugares de difícil acceso Volteck"
    },
    {
        "id": "multicontacto-pared-puertos-usb-volteck",
        "title": "Multicontactos de pared con cargadores USB y USB-C Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 414,
        "raw_index": 12,
        "output_filename": "multicontacto-pared-puertos-usb-volteck.webp",
        "codes": ["MUL-USB", "MUL-3U", "46115", "46116"],
        "description": "Estación de carga multicontacto de pared con tomas aterrizadas y puertos de carga rápida inteligente Volteck"
    },
    {
        "id": "portalamparas-porcelana-redondo-volteck",
        "title": "Portalámparas de porcelana para sobreponer Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 418,
        "raw_index": 4,
        "output_filename": "portalamparas-porcelana-redondo-volteck.webp",
        "codes": ["POPO-15", "POPO-18", "POPO-10", "POPO-9", "POPO-12", "48150", "48151"],
        "description": "Socket de porcelana con casquillo de latón resistente a altas temperaturas para interiores y plafones Volteck"
    },
    {
        "id": "portalamparas-baquelita-cadena-volteck",
        "title": "Portalámparas de baquelita con interruptor de cadena Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 418,
        "raw_index": 8,
        "output_filename": "portalamparas-baquelita-cadena-volteck.webp",
        "codes": ["POBA-C", "POBA-L", "48155", "48156"],
        "description": "Portalámparas E26 en baquelita negra de alta resistencia térmica con tirón de cadena Volteck"
    },
    {
        "id": "temporizador-digital-programable-volteck",
        "title": "Temporizadores digitales programables semanales Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 421,
        "raw_index": 9,
        "output_filename": "temporizador-digital-programable-volteck.webp",
        "codes": ["TEM-8", "TEM-1", "TEM-1B", "48386", "48385", "46997"],
        "description": "Timer digital enchufable con pantalla LCD para programación automática de encendido y apagado de luces Volteck"
    },
    {
        "id": "temporizador-mecanico-24h-volteck",
        "title": "Temporizadores mecánicos de 24 horas Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 421,
        "raw_index": 12,
        "output_filename": "temporizador-mecanico-24h-volteck.webp",
        "codes": ["TEM-1E", "45519", "43669"],
        "description": "Temporizador análogo de perilla con intervalos de 15 minutos para ahorro energético doméstico Volteck"
    },
    {
        "id": "sensor-movimiento-infrarrojo-360-volteck",
        "title": "Sensores de movimiento infrarrojos 360 grados Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 421,
        "raw_index": 18,
        "output_filename": "sensor-movimiento-infrarrojo-360-volteck.webp",
        "codes": ["SEMO-6", "SEMO-20", "SEMO-IN", "48171", "46599", "48172"],
        "description": "Detector de movimiento para techo con cobertura panorámica de 360° y ajuste de tiempo y fotocelda Volteck"
    },
    {
        "id": "timbre-inalambrico-digital-volteck",
        "title": "Timbres inalámbricos digitales para casa u oficina Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 421,
        "raw_index": 23,
        "output_filename": "timbre-inalambrico-digital-volteck.webp",
        "codes": ["TIM-I", "TIM-ID", "46595", "43571", "47231", "46594"],
        "description": "Timbre sin cables con 36 melodías seleccionables, control de volumen y alcance de hasta 100 metros Volteck"
    },
    {
        "id": "fotocelda-electronica-control-luz-volteck",
        "title": "Fotoceldas electrónicas para control de iluminación exterior Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 423,
        "raw_index": 4,
        "output_filename": "fotocelda-electronica-control-luz-volteck.webp",
        "codes": ["FOTO-1", "FOTO-2", "40134", "45018", "40135", "45019"],
        "description": "Interruptor fotoeléctrico de encendido al anochecer y apagado al amanecer para luminarias Volteck"
    },
    {
        "id": "sensor-presencia-luz-exterior-volteck",
        "title": "Sensores de presencia y movimiento para exteriores Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 423,
        "raw_index": 5,
        "output_filename": "sensor-presencia-luz-exterior-volteck.webp",
        "codes": ["SEMO-EX", "40132", "45016", "40133", "45017"],
        "description": "Sensor de movimiento hermético IP65 resistente a la intemperie para cocheras y fachadas Volteck"
    },
    {
        "id": "detector-humo-autonomo-volteck",
        "title": "Detectores de humo autónomos fotoeléctricos Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 423,
        "raw_index": 11,
        "output_filename": "detector-humo-autonomo-volteck.webp",
        "codes": ["DEHU-1", "40138", "40139"],
        "description": "Alarma de humo con sirena integrada de 85 dB y botón de prueba para seguridad en el hogar Volteck"
    },
    {
        "id": "clavija-blindada-reforzada-aterrizada-volteck",
        "title": "Clavijas blindadas reforzadas aterrizadas 15A Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 426,
        "raw_index": 3,
        "output_filename": "clavija-blindada-reforzada-aterrizada-volteck.webp",
        "codes": ["CL-B", "CL-BA", "43946", "43945", "43944"],
        "description": "Clavija industrial de uso pesado con cuerpo blindado de acero galvanizado y terminales de latón Volteck"
    },
    {
        "id": "conector-blindado-hembra-aterrizado-volteck",
        "title": "Conectores blindados hembra aterrizados 15A Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 426,
        "raw_index": 4,
        "output_filename": "conector-blindado-hembra-aterrizado-volteck.webp",
        "codes": ["CO-B", "CO-BA", "43943", "43942"],
        "description": "Conector hembra blindado con abrazadera para sujeción firme de cable de extensión Volteck"
    },
    {
        "id": "clavija-amarilla-uso-pesado-volteck",
        "title": "Clavijas uso pesado hule color amarillo Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 426,
        "raw_index": 14,
        "output_filename": "clavija-amarilla-uso-pesado-volteck.webp",
        "codes": ["CL-AM", "44196", "44195"],
        "description": "Clavija de hule alta visibilidad resistente a aceites, golpes y químicos para obra y taller Volteck"
    },
    {
        "id": "conector-amarillo-uso-pesado-volteck",
        "title": "Conectores uso pesado hule color amarillo Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 426,
        "raw_index": 16,
        "output_filename": "conector-amarillo-uso-pesado-volteck.webp",
        "codes": ["CO-AM", "44194", "44193"],
        "description": "Conector hembra de hule industrial amarillo con agarre ergonómico y bornes de tornillo Volteck"
    },
    {
        "id": "cinta-aislar-negra-profesional-volteck",
        "title": "Cintas de aislar de PVC profesionales negras Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 428,
        "raw_index": 1,
        "output_filename": "cinta-aislar-negra-profesional-volteck.webp",
        "codes": ["M-18", "M-19", "M-20", "49586", "49588", "49579"],
        "description": "Cinta aislante de policloruro de vinilo retardante a la flama con capacidad dieléctrica de hasta 600V Volteck"
    },
    {
        "id": "cinta-aislar-colores-paquete-volteck",
        "title": "Cintas de aislar de colores para identificación de fases Volteck",
        "brand": "Volteck",
        "category": "Material Eléctrico",
        "page": 428,
        "raw_index": 6,
        "output_filename": "cinta-aislar-colores-paquete-volteck.webp",
        "codes": ["MC-5", "MC-6", "49580", "49584", "49574", "49578"],
        "description": "Juego de cintas aislantes de colores vivos (rojo, azul, verde, blanco, amarillo) para electricistas Volteck"
    },
    {
        "id": "foco-led-estandar-a19-luz-calida-volteck",
        "title": "Focos LED tipo bulbo A19 luz cálida Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 430,
        "raw_index": 3,
        "output_filename": "foco-led-estandar-a19-luz-calida-volteck.webp",
        "codes": ["LED-60C", "LED-75C", "LED-100C", "43545", "49036", "48052"],
        "description": "Foco LED de bajo consumo base E26 con temperatura de color cálida ideal para salas y recámaras Volteck"
    },
    {
        "id": "foco-led-estandar-a19-luz-fria-volteck",
        "title": "Focos LED tipo bulbo A19 luz fría de día Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 430,
        "raw_index": 6,
        "output_filename": "foco-led-estandar-a19-luz-fria-volteck.webp",
        "codes": ["LED-60F", "LED-75F", "LED-100F", "48297", "46038", "46039", "46993"],
        "description": "Foco LED omnidireccional de alto rendimiento lumínico para cocinas, oficinas y áreas de trabajo Volteck"
    },
    {
        "id": "foco-led-bulbo-omnidireccional-volteck",
        "title": "Focos LED tipo bulbo omnidireccionales alto flujo Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 431,
        "raw_index": 6,
        "output_filename": "foco-led-bulbo-omnidireccional-volteck.webp",
        "codes": ["LED-85", "LED-120", "48459", "46593", "47548", "47546"],
        "description": "Foco LED con difusor opalino que distribuye uniformemente la luz sin deslumbrar Volteck"
    },
    {
        "id": "foco-led-globo-decorativo-volteck",
        "title": "Focos LED tipo globo G95 decorativos Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 431,
        "raw_index": 18,
        "output_filename": "foco-led-globo-decorativo-volteck.webp",
        "codes": ["LED-G95", "LED-G120", "47542", "46861", "46859", "46856"],
        "description": "Lámpara LED con formato globo grande para luminarias colgantes y candiles de diseño Volteck"
    },
    {
        "id": "foco-led-basic-luz-dia-volteck",
        "title": "Focos LED Volteck Basic luz de día",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 432,
        "raw_index": 0,
        "output_filename": "foco-led-basic-luz-dia-volteck.webp",
        "codes": ["LEDB-60F", "LEDB-75F", "LEDB-100F", "27165", "28066", "27215"],
        "description": "Foco LED económico de larga vida útil para reposición masiva en hogar y comercio Volteck Basic"
    },
    {
        "id": "foco-led-basic-luz-calida-volteck",
        "title": "Focos LED Volteck Basic luz cálida",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 432,
        "raw_index": 1,
        "output_filename": "foco-led-basic-luz-calida-volteck.webp",
        "codes": ["LEDB-60C", "LEDB-75C", "LEDB-100C", "28065", "27214", "28061", "28059", "27162"],
        "description": "Foco LED de línea económica con excelente índice de reproducción cromática Volteck Basic"
    },
    {
        "id": "foco-led-alta-potencia-industrial-volteck",
        "title": "Focos LED de alta potencia cilíndricos T100 Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 433,
        "raw_index": 2,
        "output_filename": "foco-led-alta-potencia-industrial-volteck.webp",
        "codes": ["LED-30A", "LED-40A", "LED-50A", "48079", "48078", "45386", "45387"],
        "description": "Lámpara LED industrial de alto flujo luminoso con disipador térmico integrado de aluminio Volteck"
    },
    {
        "id": "foco-led-alta-potencia-t120-volteck",
        "title": "Focos LED de súper alta potencia T120 Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 433,
        "raw_index": 12,
        "output_filename": "foco-led-alta-potencia-t120-volteck.webp",
        "codes": ["LED-65A", "LED-80A", "LED-100A", "28209", "28208", "28207", "28206"],
        "description": "Foco LED de gran potencia para bodegas, hangares, talleres y alumbrado comercial Volteck"
    },
    {
        "id": "tubo-led-t8-cristal-luz-fria-volteck",
        "title": "Tubos LED T8 de cristal para balastra eliminada Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 433,
        "raw_index": 13,
        "output_filename": "tubo-led-t8-cristal-luz-fria-volteck.webp",
        "codes": ["T8-18L", "T8-9L", "48080", "48081", "48082"],
        "description": "Tubo lineal LED de 1.20 metros con conexión directa a 127V sin necesidad de balastro Volteck"
    },
    {
        "id": "lampara-led-espiral-ahorradora-volteck",
        "title": "Lámparas fluorescentes y LED espirales compactas Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 435,
        "raw_index": 4,
        "output_filename": "lampara-led-espiral-ahorradora-volteck.webp",
        "codes": ["FES-23", "FES-15", "48402", "48403", "48404", "48405"],
        "description": "Lámpara compacta de espiral de alta eficiencia energética para luminarias residenciales Volteck"
    },
    {
        "id": "foco-led-vela-tipo-flama-volteck",
        "title": "Focos LED tipo vela con punta de flama decorativos Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 435,
        "raw_index": 5,
        "output_filename": "foco-led-vela-tipo-flama-volteck.webp",
        "codes": ["LED-VEL", "LED-FLA", "46180", "46179", "46178", "46177"],
        "description": "Foco LED decorativo tipo flama base E12/E26 para candiles y lámparas de pared clásicas Volteck"
    },
    {
        "id": "foco-vintage-filamento-ambar-edison-volteck",
        "title": "Focos vintage tipo Edison filamento de carbón ámbar Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 436,
        "raw_index": 12,
        "output_filename": "foco-vintage-filamento-ambar-edison-volteck.webp",
        "codes": ["ED-40", "ED-60", "47108", "47105", "47106", "47104"],
        "description": "Foco decorativo estilo vintage retro con cristal entintado ámbar y filamento visible tipo jaula Volteck"
    },
    {
        "id": "foco-vintage-filamento-globo-volteck",
        "title": "Focos vintage decorativos formato globo filamento ámbar Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 436,
        "raw_index": 21,
        "output_filename": "foco-vintage-filamento-globo-volteck.webp",
        "codes": ["ED-G80", "ED-G125", "47103", "48324", "46834"],
        "description": "Lámpara vintage esférica retro para ambientación cálida en restaurantes, cafeterías y hogares Volteck"
    },
    {
        "id": "luminario-decorativo-sobreponer-techo-volteck",
        "title": "Luminarios decorativos de sobreponer en techo Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 439,
        "raw_index": 3,
        "output_filename": "luminario-decorativo-sobreponer-techo-volteck.webp",
        "codes": ["LUSO-12", "LUSO-18", "46626", "46262", "45218"],
        "description": "Plafón redondo LED de perfil ultradelgado para instalación limpia en losas y techos Volteck"
    },
    {
        "id": "luminario-decorativo-plafon-cilindrico-volteck",
        "title": "Luminarios cilíndricos decorativos de sobreponer Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 439,
        "raw_index": 5,
        "output_filename": "luminario-decorativo-plafon-cilindrico-volteck.webp",
        "codes": ["LUSO-CIL", "46346", "46347"],
        "description": "Downlight cilíndrico de aluminio blanco/negro para iluminación puntual contemporánea Volteck"
    },
    {
        "id": "spot-led-empotrable-dirigible-volteck",
        "title": "Luminarios spot LED empotrables dirigibles para tablaroca Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 440,
        "raw_index": 9,
        "output_filename": "spot-led-empotrable-dirigible-volteck.webp",
        "codes": ["SPOT-7", "SPOT-9", "45672", "45673", "45674"],
        "description": "Foco spot dirigible para falso plafón con clips de sujeción de acero y marco articulado Volteck"
    },
    {
        "id": "arbotante-exterior-decorativo-aluminio-volteck",
        "title": "Arbotantes decorativos exteriores de aluminio Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 446,
        "raw_index": 4,
        "output_filename": "arbotante-exterior-decorativo-aluminio-volteck.webp",
        "codes": ["ARB-10", "ARB-12", "45408", "45409", "48143", "47392"],
        "description": "Luminaria de pared con doble haz de luz superior e inferior para iluminación de fachadas y muros Volteck"
    },
    {
        "id": "luminario-solar-suburbano-sensor-volteck",
        "title": "Luminarios solares suburbanos con panel y sensor Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 448,
        "raw_index": 1,
        "output_filename": "luminario-solar-suburbano-sensor-volteck.webp",
        "codes": ["LUSO-SOL", "49782", "49827", "45870", "47275", "46480"],
        "description": "Lámpara suburbana todo-en-uno con panel solar fotovoltaico, batería de litio y control remoto Volteck"
    },
    {
        "id": "reflector-led-exterior-delgado-30w-volteck",
        "title": "Reflectores LED para exteriores ultradelgados 30W-50W Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 451,
        "raw_index": 0,
        "output_filename": "reflector-led-exterior-delgado-30w-volteck.webp",
        "codes": ["REF-30", "REF-50", "48228", "48229", "48230", "49896"],
        "description": "Reflector de alta potencia con carcasa de aluminio inyectado y cristal templado hermético IP65 Volteck"
    },
    {
        "id": "reflector-led-exterior-alta-potencia-100w-volteck",
        "title": "Reflectores LED industriales de alta potencia 100W-200W Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 451,
        "raw_index": 2,
        "output_filename": "reflector-led-exterior-alta-potencia-100w-volteck.webp",
        "codes": ["REF-100", "REF-150", "REF-200", "48218", "48219", "48220", "48221"],
        "description": "Reflector para canchas, estacionamientos y naves industriales con soporte orientable reforzado Volteck"
    },

    # -------------------------------------------------------------------------
    # 2. Plomería y Grifería Foset (50 familias)
    # -------------------------------------------------------------------------
    {
        "id": "dosificador-jabon-liquido-acero-foset",
        "title": "Dosificadores de jabón líquido de acero inoxidable Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 485,
        "raw_index": 4,
        "output_filename": "dosificador-jabon-liquido-acero-foset.webp",
        "codes": ["DJ-100", "DJ-80", "47934", "45742", "45743"],
        "description": "Dispensador institucional de jabón o gel antibacterial montable en pared de acero inoxidable satinado Foset"
    },
    {
        "id": "dispensador-toallas-papel-institucional-foset",
        "title": "Dispensadores institucionales de toallas de papel Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 485,
        "raw_index": 6,
        "output_filename": "dispensador-toallas-papel-institucional-foset.webp",
        "codes": ["DTO-100", "47931", "45856", "47933", "47936"],
        "description": "Gabinete dispensador de toallas interdobladas con cerradura de seguridad para baños públicos Foset"
    },
    {
        "id": "regadera-cuadrada-plato-ancho-acero-foset",
        "title": "Regaderas cuadradas de plato ancho tipo lluvia Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 486,
        "raw_index": 0,
        "output_filename": "regadera-cuadrada-plato-ancho-acero-foset.webp",
        "codes": ["REG-8C", "REG-10C", "REG-12C", "50483", "45248", "45249"],
        "description": "Regadera de acero inoxidable ultraplana con pivotes de silicón autolimpiables antisarro Foset"
    },
    {
        "id": "regadera-redonda-antisarro-cromada-foset",
        "title": "Regaderas redondas cromadas de media y baja presión Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 486,
        "raw_index": 12,
        "output_filename": "regadera-redonda-antisarro-cromada-foset.webp",
        "codes": ["REG-4", "REG-6", "43267", "45855", "45854", "49216"],
        "description": "Regadera clásica cromada con articulación esférica de latón orientable Foset"
    },
    {
        "id": "brazo-regadera-curvo-chapeton-foset",
        "title": "Brazos para regadera curvos con chapetón de latón Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 486,
        "raw_index": 13,
        "output_filename": "brazo-regadera-curvo-chapeton-foset.webp",
        "codes": ["BCH-20", "BCH-30", "BCH-600", "BCH-720", "F4203"],
        "description": "Brazo metálico de pared cromado con rosca macho de 1/2 pulgada y chapetón decorativo Foset"
    },
    {
        "id": "brazo-regadera-recto-techo-foset",
        "title": "Brazos para regadera rectos de bajada de techo Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 486,
        "raw_index": 18,
        "output_filename": "brazo-regadera-recto-techo-foset.webp",
        "codes": ["BCH-T20", "BCH-T30", "45250", "45251"],
        "description": "Brazo vertical de techo para regaderas tipo lluvia de plato ancho acabado cromo brillante Foset"
    },
    {
        "id": "regadera-manual-multichorro-telefono-foset",
        "title": "Regaderas manuales tipo teléfono con manguera flexible Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 486,
        "raw_index": 24,
        "output_filename": "regadera-manual-multichorro-telefono-foset.webp",
        "codes": ["REG-TEL", "REG-TEL5", "45255", "45256"],
        "description": "Regadera manual de mano con 5 tipos de chorro hidromasaje y manguera de acero inoxidable de 1.5 m Foset"
    },
    {
        "id": "mezcladora-fregadero-cuello-ganso-palanca-foset",
        "title": "Mezcladoras para fregadero 8 pulgadas cuello de ganso Foset",
        "brand": "Foset",
        "category": "Grifería",
        "page": 492,
        "raw_index": 4,
        "output_filename": "mezcladora-fregadero-cuello-ganso-palanca-foset.webp",
        "codes": ["M-590", "M-591", "49297", "49296", "49295"],
        "description": "Mezcladora de 8 pulgadas para cocina con caño giratorio alto de latón y manerales de palanca suaves Foset"
    },
    {
        "id": "mezcladora-fregadero-cubierta-acero-foset",
        "title": "Mezcladoras para fregadero con cubierta metálica Foset",
        "brand": "Foset",
        "category": "Grifería",
        "page": 492,
        "raw_index": 5,
        "output_filename": "mezcladora-fregadero-cubierta-acero-foset.webp",
        "codes": ["M-580", "M-585", "43514", "43513"],
        "description": "Llave mezcladora para tarja de cocina con cartucho cerámico antifuga y aireador economizador de agua Foset"
    },
    {
        "id": "mezcladora-lavabo-4-manerales-palanca-foset",
        "title": "Mezcladoras para lavabo 4 pulgadas manerales de palanca Foset",
        "brand": "Foset",
        "category": "Grifería",
        "page": 492,
        "raw_index": 8,
        "output_filename": "mezcladora-lavabo-4-manerales-palanca-foset.webp",
        "codes": ["M-490", "M-495", "43504", "43424", "43431"],
        "description": "Mezcladora para baño de 4 pulgadas con cuerpo de latón resistente y acabado cromado espejo Foset"
    },
    {
        "id": "mezcladora-lavabo-monomando-alto-foset",
        "title": "Monomandos para lavabo cuerpo alto contemporáneos Foset",
        "brand": "Foset",
        "category": "Grifería",
        "page": 492,
        "raw_index": 12,
        "output_filename": "mezcladora-lavabo-monomando-alto-foset.webp",
        "codes": ["MON-AL", "MON-LAV", "43520", "43521"],
        "description": "Grifo monomando de monocomando único para lavabos de sobreponer tipo bowl de diseño europeo Foset"
    },
    {
        "id": "monomando-fregadero-retractil-foset",
        "title": "Monomandos para fregadero con manguera retráctil pull-down Foset",
        "brand": "Foset",
        "category": "Grifería",
        "page": 492,
        "raw_index": 28,
        "output_filename": "monomando-fregadero-retractil-foset.webp",
        "codes": ["MON-FRE", "MON-PULL", "43530", "43531"],
        "description": "Grifería gourmet monomando para cocina con rociador extraíble de dos funciones Foset"
    },
    {
        "id": "cespol-bote-plastico-lavabo-bote-flexible-foset",
        "title": "Céspoles bote de polipropileno para lavabo Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 493,
        "raw_index": 11,
        "output_filename": "cespol-bote-plastico-lavabo-bote-flexible-foset.webp",
        "codes": ["CES-PL", "CES-P1", "43129", "43128", "43124"],
        "description": "Céspol de trampa registrable para lavabo de baño con empaques cónicos de hule hermético Foset"
    },
    {
        "id": "cespol-bote-flexible-con-extension-foset",
        "title": "Céspoles flexibles tipo acordeón para lavabo y fregadero Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 493,
        "raw_index": 12,
        "output_filename": "cespol-bote-flexible-con-extension-foset.webp",
        "codes": ["CES-FLEX", "43123", "43133", "43125"],
        "description": "Desagüe flexible extensible adaptable a desalineaciones entre la tubería del muro y la bacha Foset"
    },
    {
        "id": "tubo-extension-cespol-lavabo-pvc-foset",
        "title": "Tubos tuerca extensión para céspol Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 493,
        "raw_index": 13,
        "output_filename": "tubo-extension-cespol-lavabo-pvc-foset.webp",
        "codes": ["EXT-CES", "43135", "49508"],
        "description": "Extensión tubular para céspol de lavabo de 1 1/4 pulgada con tuerca deslizable Foset"
    },
    {
        "id": "cespol-laton-cromado-lavabo-foset",
        "title": "Céspoles bote de latón cromado de alta durabilidad Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 493,
        "raw_index": 23,
        "output_filename": "cespol-laton-cromado-lavabo-foset.webp",
        "codes": ["CES-LAT", "43140", "43141"],
        "description": "Céspol metálico de latón macizo cromado con registro inferior para limpieza y destape de drenaje Foset"
    },
    {
        "id": "cespol-bote-fregadero-doble-tina-foset",
        "title": "Céspoles para fregadero de doble tina con trampa Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 494,
        "raw_index": 4,
        "output_filename": "cespol-bote-fregadero-doble-tina-foset.webp",
        "codes": ["CES-DOB", "43115", "43118", "43114"],
        "description": "Kit de desagüe para tarja de doble tina con trampa en P y conexión al desagüe general Foset"
    },
    {
        "id": "contrarrejilla-fregadero-acero-inox-canasta-foset",
        "title": "Contrarrejillas para fregadero de acero inoxidable con canastilla Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 494,
        "raw_index": 8,
        "output_filename": "contrarrejilla-fregadero-acero-inox-canasta-foset.webp",
        "codes": ["CONT-F", "CONT-FA", "43116", "43119", "45319"],
        "description": "Contrarrejilla para tarja de 3 1/2 pulgadas con colador canastilla de acero inoxidable y tapón de sello Foset"
    },
    {
        "id": "contrarrejilla-lavabo-laton-rebosadero-foset",
        "title": "Contrarrejillas para lavabo de latón con rebosadero Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 494,
        "raw_index": 13,
        "output_filename": "contrarrejilla-lavabo-laton-rebosadero-foset.webp",
        "codes": ["CONT-L", "CONT-LR", "43117", "49334"],
        "description": "Contrarrejilla de latón para lavabo de baño con barrenos de rebosadero y tuerca de apriete Foset"
    },
    {
        "id": "desague-automatico-boton-push-lavabo-foset",
        "title": "Desagües automáticos de botón push pop-up Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 494,
        "raw_index": 29,
        "output_filename": "desague-automatico-boton-push-lavabo-foset.webp",
        "codes": ["DES-PUSH", "43120", "43121"],
        "description": "Válvula de desagüe pop-up push button que abre y cierra con un solo toque sobre la tapa superior Foset"
    },
    {
        "id": "coladera-piso-redonda-acero-rejilla-foset",
        "title": "Coladeras de piso redondas con rejilla de acero inoxidable Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 495,
        "raw_index": 0,
        "output_filename": "coladera-piso-redonda-acero-rejilla-foset.webp",
        "codes": ["COL-R", "COL-R4", "46469", "45301", "45302"],
        "description": "Coladera para piso de regadera con cúpula antirroedores e insectos y acabado acero inoxidable cepillado Foset"
    },
    {
        "id": "coladera-piso-cuadrada-trampa-olores-foset",
        "title": "Coladeras de piso cuadradas con trampa de olores Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 495,
        "raw_index": 1,
        "output_filename": "coladera-piso-cuadrada-trampa-olores-foset.webp",
        "codes": ["COL-C", "COL-C4", "45303", "43165", "43169", "49618", "46024"],
        "description": "Coladera cuadrada moderna para baño con válvula de retención antiolores y rejilla desmontable Foset"
    },
    {
        "id": "calentador-agua-instantaneo-gas-lp-foset",
        "title": "Calentadores de agua instantáneos de gas LP Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 497,
        "raw_index": 2,
        "output_filename": "calentador-agua-instantaneo-gas-lp-foset.webp",
        "codes": ["CALE-6L", "CALE-8L", "45271", "43050", "43051"],
        "description": "Boiler instantáneo de paso que suministra agua caliente continua ahorrando hasta 70% de gas Foset"
    },
    {
        "id": "calentador-agua-instantaneo-alta-capacidad-foset",
        "title": "Calentadores instantáneos de alta capacidad 13L-16L Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 497,
        "raw_index": 6,
        "output_filename": "calentador-agua-instantaneo-alta-capacidad-foset.webp",
        "codes": ["CALE-13L", "CALE-16L", "43929", "47352", "47353", "47354", "48015"],
        "description": "Calentador de agua modulación inteligente para servicio múltiple simultáneo con display digital de temperatura Foset"
    },
    {
        "id": "calentador-agua-deposito-gas-lp-foset",
        "title": "Calentadores de agua de depósito tradicionales Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 498,
        "raw_index": 2,
        "output_filename": "calentador-agua-deposito-gas-lp-foset.webp",
        "codes": ["CADE-40", "CADE-60", "47921", "47922", "45267"],
        "description": "Boiler de depósito porcelanizado con ánodo de sacrificio de magnesio para protección anticorrosiva Foset"
    },
    {
        "id": "calentador-agua-de-paso-foset",
        "title": "Calentadores de paso rápida recuperación Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 498,
        "raw_index": 7,
        "output_filename": "calentador-agua-de-paso-foset.webp",
        "codes": ["CAPA-6", "CAPA-9", "46148", "49210", "46149", "46147", "49212"],
        "description": "Calentador de paso de rápida recuperación que no requiere presión mínima de agua para encender Foset"
    },
    {
        "id": "calentador-agua-solar-tubos-vacio-foset",
        "title": "Calentadores solares de agua con tubos de vacío Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 499,
        "raw_index": 0,
        "output_filename": "calentador-agua-solar-tubos-vacio-foset.webp",
        "codes": ["SOL-150", "SOL-200", "49965", "49966", "45274", "45270"],
        "description": "Sistema de calentamiento de agua solar ecológico por termosifón con tubos de borosilicato de alta absorción Foset"
    },
    {
        "id": "tanque-termo-calentador-solar-foset",
        "title": "Termotanques de reemplazo para calentadores solares Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 499,
        "raw_index": 7,
        "output_filename": "tanque-termo-calentador-solar-foset.webp",
        "codes": ["TER-SOL", "48287", "45272", "45273", "48312"],
        "description": "Tanque térmico insulado con espuma de poliuretano de alta densidad para retener el calor por más de 72 horas Foset"
    },
    {
        "id": "cilindro-gas-lp-portatil-foset",
        "title": "Cilindros portátiles para gas LP de acero Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 500,
        "raw_index": 0,
        "output_filename": "cilindro-gas-lp-portatil-foset.webp",
        "codes": ["CIL-GAS", "CIL-10", "CIL-20", "45887", "40710", "49117"],
        "description": "Tanque de gas LP portátil de acero reforzado con válvula de seguridad normalizada para estufas y calentadores Foset"
    },
    {
        "id": "regulador-gas-lp-baja-presion-manguera-foset",
        "title": "Reguladores de gas LP de baja presión con manguera Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 500,
        "raw_index": 3,
        "output_filename": "regulador-gas-lp-baja-presion-manguera-foset.webp",
        "codes": ["REG-GAS", "REG-G1", "49120", "49121"],
        "description": "Regulador de una vía con manómetro y manguera tramada flexible para conexión de gas segura Foset"
    },
    {
        "id": "valvula-cilindro-gas-lp-seguridad-foset",
        "title": "Válvulas de seguridad para cilindros de gas LP Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 500,
        "raw_index": 8,
        "output_filename": "valvula-cilindro-gas-lp-seguridad-foset.webp",
        "codes": ["VAL-GAS", "49125", "49126"],
        "description": "Válvula de latón forjado para recarga y control de salida en tanques portátiles de gas Foset"
    },
    {
        "id": "valvula-esfera-cpvc-cementar-foset",
        "title": "Válvulas de esfera de CPVC para cementar Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 509,
        "raw_index": 8,
        "output_filename": "valvula-esfera-cpvc-cementar-foset.webp",
        "codes": ["V-CPVC-12", "V-CPVC-34", "V-CPVC-1", "44462", "42016", "42017", "42015"],
        "description": "Válvula de corte hermético para tubería de agua caliente de CPVC de alta resistencia a presión Foset"
    },
    {
        "id": "tuerca-union-cpvc-foset",
        "title": "Tuercas unión de CPVC para agua caliente Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 509,
        "raw_index": 9,
        "output_filename": "tuerca-union-cpvc-foset.webp",
        "codes": ["TU-CPVC", "42018", "49294", "45486"],
        "description": "Conexión desmontable tuerca unión que facilita el mantenimiento en bombas y calentadores de agua Foset"
    },
    {
        "id": "codo-cpvc-90-grados-foset",
        "title": "Codos de CPVC a 90 grados para cementar Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 509,
        "raw_index": 10,
        "output_filename": "codo-cpvc-90-grados-foset.webp",
        "codes": ["C-CPVC-12", "C-CPVC-34", "45487", "45488"],
        "description": "Codo termoplástico para cambios de dirección en redes hidráulicas sanitarias y de agua potable Foset"
    },
    {
        "id": "juego-llaves-empotrar-soldables-foset",
        "title": "Juegos de llaves de empotrar roscables y soldables para regadera Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 512,
        "raw_index": 5,
        "output_filename": "juego-llaves-empotrar-soldables-foset.webp",
        "codes": ["JLL-EMP", "45860", "44449", "45859"],
        "description": "Par de válvulas de empotrar en muro de latón para control individual de agua fría y caliente en ducha Foset"
    },
    {
        "id": "manerales-para-llave-empotrar-acrilico-foset",
        "title": "Manerales de acrílico y metal para llaves de empotrar Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 512,
        "raw_index": 14,
        "output_filename": "manerales-para-llave-empotrar-acrilico-foset.webp",
        "codes": ["MAN-ACR", "MAN-CR", "45174", "45172"],
        "description": "Juego de manerales ergonómicos con chapetones cromados para reemplazo en regaderas Foset"
    },
    {
        "id": "llave-jardin-manguera-laton-foset",
        "title": "Llaves de jardín para manguera de latón de 1/2 pulgada Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 523,
        "raw_index": 0,
        "output_filename": "llave-jardin-manguera-laton-foset.webp",
        "codes": ["LL-J12", "LL-J34", "48537", "48538"],
        "description": "Llave para toma de agua exterior con salida roscada estándar para manguera de riego Foset"
    },
    {
        "id": "llave-jardin-esfera-palanca-foset",
        "title": "Llaves de jardín tipo esfera con palanca de cuarto de vuelta Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 523,
        "raw_index": 2,
        "output_filename": "llave-jardin-esfera-palanca-foset.webp",
        "codes": ["LL-JE", "48539", "48540"],
        "description": "Llave de esfera para manguera con apertura rápida de 1/4 de vuelta y cuerpo de latón niquelado Foset"
    },
    {
        "id": "llave-esfera-dual-laton-niquelado-foset",
        "title": "Llaves de esfera duales de latón niquelado Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 524,
        "raw_index": 1,
        "output_filename": "llave-esfera-dual-laton-niquelado-foset.webp",
        "codes": ["LL-DUAL", "48545", "48546"],
        "description": "Válvula de doble salida independiente para alimentar lavadora y manguera desde una misma toma Foset"
    },
    {
        "id": "llave-esfera-laton-paso-completo-foset",
        "title": "Válvulas de esfera de latón paso completo roscables Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 524,
        "raw_index": 2,
        "output_filename": "llave-esfera-laton-paso-completo-foset.webp",
        "codes": ["VES-12", "VES-34", "VES-1", "VES-114", "VES-112", "VES-2", "49012", "49013"],
        "description": "Válvula de corte de esfera de paso total de latón para agua, gas o vapor de hasta 600 PSI Foset"
    },
    {
        "id": "valvula-check-columpio-laton-roscable-foset",
        "title": "Válvulas check de columpio de latón Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 525,
        "raw_index": 0,
        "output_filename": "valvula-check-columpio-laton-roscable-foset.webp",
        "codes": ["VCH-C12", "VCH-C34", "VCH-C1", "49481", "49482", "49483"],
        "description": "Válvula de retención antirretorno tipo columpio para evitar el retroceso del flujo de agua Foset"
    },
    {
        "id": "valvula-check-vertical-resorte-laton-foset",
        "title": "Válvulas check verticales de resorte de latón Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 525,
        "raw_index": 1,
        "output_filename": "valvula-check-vertical-resorte-laton-foset.webp",
        "codes": ["VCH-V12", "VCH-V34", "VCH-V1", "43739", "43742"],
        "description": "Válvula de retención vertical con obturador de resorte para líneas de bombeo hidroneumático Foset"
    },
    {
        "id": "pichancha-valvula-pie-cisterna-laton-foset",
        "title": "Válvulas de pie con canastilla pichanchas de latón Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 525,
        "raw_index": 5,
        "output_filename": "pichancha-valvula-pie-cisterna-laton-foset.webp",
        "codes": ["PICH-12", "PICH-34", "PICH-1", "49014", "49015"],
        "description": "Pichancha para succión de cisterna con filtro de rejilla que impide la entrada de sedimentos a la bomba Foset"
    },
    {
        "id": "valvula-globo-laton-roscable-foset",
        "title": "Válvulas de globo de latón roscables Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 526,
        "raw_index": 0,
        "output_filename": "valvula-globo-laton-roscable-foset.webp",
        "codes": ["VGL-12", "VGL-34", "VGL-1", "49020", "49021"],
        "description": "Válvula de estrangulamiento fino de flujo para regulación precisa de caudal en instalaciones hidráulicas Foset"
    },
    {
        "id": "valvula-compuerta-laton-roscable-foset",
        "title": "Válvulas de compuerta de latón roscables Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 526,
        "raw_index": 10,
        "output_filename": "valvula-compuerta-laton-roscable-foset.webp",
        "codes": ["VCO-12", "VCO-34", "VCO-1", "49025", "49026"],
        "description": "Válvula de seccionamiento con cuña sólida de latón y vástago no ascendente Foset"
    },
    {
        "id": "flotador-esferico-polietileno-tinaco-foset",
        "title": "Flotadores de plástico con varilla para tinaco Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 527,
        "raw_index": 1,
        "output_filename": "flotador-esferico-polietileno-tinaco-foset.webp",
        "codes": ["FLOT-T", "FLOT-5", "49030", "49031"],
        "description": "Flotador esférico de polietileno con varilla de latón para corte mecánico de nivel de agua en depósitos Foset"
    },
    {
        "id": "valvula-llenado-alta-presion-tinaco-foset",
        "title": "Válvulas de llenado para tinaco y cisterna Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 527,
        "raw_index": 11,
        "output_filename": "valvula-llenado-alta-presion-tinaco-foset.webp",
        "codes": ["VLL-TIN", "49035", "49036"],
        "description": "Válvula de admisión para tinaco de llenado silencioso con flotador integrado Foset"
    },
    {
        "id": "multiconector-tinaco-valvula-esfera-foset",
        "title": "Multiconectores para tinaco con válvula de esfera integrada Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 527,
        "raw_index": 21,
        "output_filename": "multiconector-tinaco-valvula-esfera-foset.webp",
        "codes": ["MUL-TIN", "49040", "49041"],
        "description": "Conector multifuncional para salida inferior de tinaco con llave de paso y derivación para jarro de aire Foset"
    },
    {
        "id": "valvula-angular-paso-lavabo-fregadero-foset",
        "title": "Válvulas de paso angulares cromadas de 1/2 x 1/2 y 1/2 x 3/8 Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 532,
        "raw_index": 16,
        "output_filename": "valvula-angular-paso-lavabo-fregadero-foset.webp",
        "codes": ["VAN-12", "VAN-38", "43404", "45477", "45479", "49357", "44178", "44179"],
        "description": "Llave angular de corte para alimentación de mangueras coflex en sanitarios y lavabos Foset"
    },
    {
        "id": "herraje-completo-tanque-wc-descarga-foset",
        "title": "Herrajes completos para tanque bajo de WC con válvula de descarga Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 529,
        "raw_index": 4,
        "output_filename": "herraje-completo-tanque-wc-descarga-foset.webp",
        "codes": ["HER-WC", "45308", "48447", "48446", "P-B6007", "PW-024"],
        "description": "Kit universal de reemplazo para inodoro con válvula de llenado antisifón, sapo de silicón y palanca cromada Foset"
    },
    {
        "id": "gabinete-estanco-tubos-led-volteck",
        "title": "Gabinetes industriales estancos para tubos LED IP65 Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 445,
        "raw_index": 6,
        "output_filename": "gabinete-estanco-tubos-led-volteck.webp",
        "codes": ["GAB-2T8", "47395", "47396", "48257"],
        "description": "Luminario hermético a prueba de vapor y polvo para estacionamientos, almacenes e industrias Volteck"
    },
    {
        "id": "plafon-led-redondo-sobreponer-volteck",
        "title": "Plafones decorativos LED redondos de sobreponer Volteck",
        "brand": "Volteck",
        "category": "Iluminación",
        "page": 438,
        "raw_index": 13,
        "output_filename": "plafon-led-redondo-sobreponer-volteck.webp",
        "codes": ["PLAF-18", "PLAF-24", "46711", "47347", "46713"],
        "description": "Plafón de luz blanca difusa uniforme con driver integrado de alta eficiencia Volteck"
    },
    {
        "id": "maneral-cruz-laton-cromado-foset",
        "title": "Manerales metálicos tipo cruz para llave de empotrar Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 512,
        "raw_index": 8,
        "output_filename": "maneral-cruz-laton-cromado-foset.webp",
        "codes": ["MAN-CRUZ", "45176", "45178"],
        "description": "Maneral metálico cromado clásico de 4 brazos para vástago de empotrar Foset"
    },
    {
        "id": "valvula-esfera-roscable-mariposa-foset",
        "title": "Válvulas de esfera con maneral tipo mariposa Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 524,
        "raw_index": 3,
        "output_filename": "valvula-esfera-roscable-mariposa-foset.webp",
        "codes": ["VES-MAR", "49016", "49017"],
        "description": "Válvula de corte rápido en espacios reducidos con manija mariposa de aluminio Foset"
    },
    {
        "id": "abrazadera-toma-domiciliaria-foset",
        "title": "Abrazaderas de reparación y toma domiciliaria para tubería Foset",
        "brand": "Foset",
        "category": "Plomería",
        "page": 527,
        "raw_index": 16,
        "output_filename": "abrazadera-toma-domiciliaria-foset.webp",
        "codes": ["ABRA-DOM", "49050", "49051"],
        "description": "Abrazadera de dos secciones de hierro nodular con empaque de neopreno para derivación o reparación hidráulica Foset"
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

    # Si ya se inspeccionó previamente en /tmp/inspect_mod_c, podemos reutilizarla
    inspect_png = f"/tmp/inspect_mod_c/p{page}-{raw_idx:03d}.png"
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
    print("MÓDULO C: EXTRACCIÓN DE 100 NUEVAS FAMILIAS TRUPER (TOTAL META: 561)")
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

    # 2. Extraer y procesar imágenes del Módulo C
    print(f"[*] Extrayendo {len(MODULE_C_100_FAMILIES)} familias visuales del Módulo C...")
    new_extracted = 0
    for g in MODULE_C_100_FAMILIES:
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
            # Reglas semánticas guiadas de alta fidelidad para Volteck e Foset
            for g in existing_groups:
                gid = g["id"]
                # Volteck Eléctrico e Iluminación
                if gid == "linterna-plastica-led-recargable-volteck" and "linterna" in name and ("recargable" in name or "plastica" in name):
                    matched_group = g
                    match_reason = "Nombre:Linterna Recargable"
                    break
                elif gid == "linterna-led-tipo-minero-recargable-volteck" and "linterna" in name and ("minero" in name or "cabeza" in name):
                    matched_group = g
                    match_reason = "Nombre:Linterna Minero"
                    break
                elif gid == "extension-electrica-domestica-polarizada-volteck" and "extension" in name and ("polarizada" in name or "domestica" in name):
                    matched_group = g
                    match_reason = "Nombre:Extension Polarizada"
                    break
                elif gid == "lampara-inspeccion-taller-volteck" and ("lampara" in name and "taller" in name or "portalampara" in name and "taller" in name):
                    matched_group = g
                    match_reason = "Nombre:Lampara Taller"
                    break
                elif gid == "multicontacto-barra-supresor-picos-6-entradas-volteck" and "multicontacto" in name and ("6" in name or "barra" in name or "supresor" in name):
                    matched_group = g
                    match_reason = "Nombre:Multicontacto Barra"
                    break
                elif gid == "multicontacto-cubo-giratorio-volteck" and "multicontacto" in name and ("adaptador" in name or "3 contactos" in name or "cubo" in name):
                    matched_group = g
                    match_reason = "Nombre:Multicontacto Adaptador"
                    break
                elif gid == "portalamparas-porcelana-redondo-volteck" and ("portalampara" in name or "socket" in name) and "porcelana" in name:
                    matched_group = g
                    match_reason = "Nombre:Socket Porcelana"
                    break
                elif gid == "portalamparas-baquelita-cadena-volteck" and ("portalampara" in name or "socket" in name) and ("baquelita" in name or "cadena" in name):
                    matched_group = g
                    match_reason = "Nombre:Socket Baquelita"
                    break
                elif gid == "timbre-inalambrico-digital-volteck" and "timbre" in name and ("inalambrico" in name or "digital" in name or "sobreponer" in name):
                    matched_group = g
                    match_reason = "Nombre:Timbre"
                    break
                elif gid == "sensor-movimiento-infrarrojo-360-volteck" and "sensor" in name and "movimiento" in name:
                    matched_group = g
                    match_reason = "Nombre:Sensor Movimiento"
                    break
                elif gid == "clavija-blindada-reforzada-aterrizada-volteck" and "clavija" in name and ("blindada" in name or "aterrizada" in name):
                    matched_group = g
                    match_reason = "Nombre:Clavija Blindada"
                    break
                elif gid == "conector-blindado-hembra-aterrizado-volteck" and "conector" in name and ("blindado" in name or "aterrizado" in name):
                    matched_group = g
                    match_reason = "Nombre:Conector Blindado"
                    break
                elif gid == "cinta-aislar-negra-profesional-volteck" and "cinta" in name and "aislar" in name and "negra" in name:
                    matched_group = g
                    match_reason = "Nombre:Cinta Aislar Negra"
                    break
                elif gid == "cinta-aislar-colores-paquete-volteck" and "cinta" in name and "aislar" in name and any(col in name for col in ["color", "roja", "azul", "verde", "amarill"]):
                    matched_group = g
                    match_reason = "Nombre:Cinta Aislar Color"
                    break
                elif gid == "foco-led-estandar-a19-luz-calida-volteck" and "foco" in name and "led" in name and ("calid" in name or "ambar" in name or "3000k" in name):
                    matched_group = g
                    match_reason = "Nombre:Foco LED Calido"
                    break
                elif gid == "foco-led-estandar-a19-luz-fria-volteck" and "foco" in name and "led" in name and ("fria" in name or "blanca" in name or "dia" in name or "6500k" in name):
                    matched_group = g
                    match_reason = "Nombre:Foco LED Frio"
                    break
                elif gid == "foco-led-alta-potencia-industrial-volteck" and "foco" in name and ("alta potencia" in name or "t100" in name or "30w" in name or "40w" in name or "50w" in name):
                    matched_group = g
                    match_reason = "Nombre:Foco Alta Potencia"
                    break
                elif gid == "tubo-led-t8-cristal-luz-fria-volteck" and "tubo" in name and ("t8" in name or "led" in name) and "cristal" in name:
                    matched_group = g
                    match_reason = "Nombre:Tubo LED T8"
                    break
                elif gid == "foco-vintage-filamento-ambar-edison-volteck" and "foco" in name and ("vintage" in name or "edison" in name or "filamento" in name):
                    matched_group = g
                    match_reason = "Nombre:Foco Vintage Edison"
                    break
                elif gid == "reflector-led-exterior-delgado-30w-volteck" and "reflector" in name and ("led" in name or "exterior" in name):
                    matched_group = g
                    match_reason = "Nombre:Reflector LED"
                    break

                # Foset Plomería y Grifería
                elif gid == "regadera-cuadrada-plato-ancho-acero-foset" and "regadera" in name and ("cuadrad" in name or "plato" in name or "lluvia" in name):
                    matched_group = g
                    match_reason = "Nombre:Regadera Cuadrada"
                    break
                elif gid == "regadera-redonda-antisarro-cromada-foset" and "regadera" in name and ("redonda" in name or "antisarro" in name or "cromo" in name or "cromada" in name):
                    matched_group = g
                    match_reason = "Nombre:Regadera Redonda"
                    break
                elif gid == "brazo-regadera-curvo-chapeton-foset" and "brazo" in name and "regadera" in name:
                    matched_group = g
                    match_reason = "Nombre:Brazo Regadera"
                    break
                elif gid == "regadera-manual-multichorro-telefono-foset" and "regadera" in name and ("telefono" in name or "manual" in name or "manguera" in name):
                    matched_group = g
                    match_reason = "Nombre:Regadera Telefono"
                    break
                elif gid == "mezcladora-fregadero-cuello-ganso-palanca-foset" and "mezcladora" in name and "fregadero" in name and ("cuello" in name or "ganso" in name):
                    matched_group = g
                    match_reason = "Nombre:Mezcladora Fregadero Ganso"
                    break
                elif gid == "mezcladora-fregadero-cubierta-acero-foset" and "mezcladora" in name and "fregadero" in name:
                    matched_group = g
                    match_reason = "Nombre:Mezcladora Fregadero"
                    break
                elif gid == "mezcladora-lavabo-4-manerales-palanca-foset" and "mezcladora" in name and "lavabo" in name:
                    matched_group = g
                    match_reason = "Nombre:Mezcladora Lavabo"
                    break
                elif gid == "mezcladora-lavabo-monomando-alto-foset" and "monomando" in name and "lavabo" in name:
                    matched_group = g
                    match_reason = "Nombre:Monomando Lavabo"
                    break
                elif gid == "monomando-fregadero-retractil-foset" and "monomando" in name and "fregadero" in name:
                    matched_group = g
                    match_reason = "Nombre:Monomando Fregadero"
                    break
                elif gid == "cespol-bote-plastico-lavabo-bote-flexible-foset" and "cespol" in name and ("lavabo" in name or "plastico" in name or "bote" in name):
                    matched_group = g
                    match_reason = "Nombre:Cespol Lavabo"
                    break
                elif gid == "cespol-bote-fregadero-doble-tina-foset" and "cespol" in name and "fregadero" in name:
                    matched_group = g
                    match_reason = "Nombre:Cespol Fregadero"
                    break
                elif gid == "contrarrejilla-fregadero-acero-inox-canasta-foset" and "contrarrejilla" in name and ("fregadero" in name or "tarja" in name or "canasta" in name):
                    matched_group = g
                    match_reason = "Nombre:Contrarrejilla Fregadero"
                    break
                elif gid == "contrarrejilla-lavabo-laton-rebosadero-foset" and "contrarrejilla" in name and "lavabo" in name:
                    matched_group = g
                    match_reason = "Nombre:Contrarrejilla Lavabo"
                    break
                elif gid == "coladera-piso-redonda-acero-rejilla-foset" and "coladera" in name and ("piso" in name or "redonda" in name):
                    matched_group = g
                    match_reason = "Nombre:Coladera Redonda"
                    break
                elif gid == "coladera-piso-cuadrada-trampa-olores-foset" and "coladera" in name and ("cuadrad" in name or "trampa" in name):
                    matched_group = g
                    match_reason = "Nombre:Coladera Cuadrada"
                    break
                elif gid == "calentador-agua-instantaneo-gas-lp-foset" and ("calentador" in name or "boiler" in name) and "instantaneo" in name:
                    matched_group = g
                    match_reason = "Nombre:Boiler Instantaneo"
                    break
                elif gid == "calentador-agua-deposito-gas-lp-foset" and ("calentador" in name or "boiler" in name) and "deposito" in name:
                    matched_group = g
                    match_reason = "Nombre:Boiler Deposito"
                    break
                elif gid == "calentador-agua-solar-tubos-vacio-foset" and ("calentador" in name or "boiler" in name) and "solar" in name:
                    matched_group = g
                    match_reason = "Nombre:Boiler Solar"
                    break
                elif gid == "cilindro-gas-lp-portatil-foset" and ("cilindro" in name or "tanque" in name) and "gas" in name:
                    matched_group = g
                    match_reason = "Nombre:Tanque Gas"
                    break
                elif gid == "regulador-gas-lp-baja-presion-manguera-foset" and "regulador" in name and "gas" in name:
                    matched_group = g
                    match_reason = "Nombre:Regulador Gas"
                    break
                elif gid == "valvula-esfera-cpvc-cementar-foset" and "valvula" in name and "esfera" in name and "cpvc" in name:
                    matched_group = g
                    match_reason = "Nombre:Valvula Esfera CPVC"
                    break
                elif gid == "llave-jardin-manguera-laton-foset" and "llave" in name and ("jardin" in name or "manguera" in name) and "laton" in name:
                    matched_group = g
                    match_reason = "Nombre:Llave Jardin Laton"
                    break
                elif gid == "llave-jardin-esfera-palanca-foset" and "llave" in name and ("jardin" in name or "manguera" in name) and "esfera" in name:
                    matched_group = g
                    match_reason = "Nombre:Llave Jardin Esfera"
                    break
                elif gid == "llave-esfera-laton-paso-completo-foset" and "valvula" in name and "esfera" in name and ("paso completo" in name or "laton" in name):
                    matched_group = g
                    match_reason = "Nombre:Valvula Esfera Laton"
                    break
                elif gid == "valvula-check-columpio-laton-roscable-foset" and "valvula" in name and "check" in name and "columpio" in name:
                    matched_group = g
                    match_reason = "Nombre:Valvula Check Columpio"
                    break
                elif gid == "valvula-check-vertical-resorte-laton-foset" and "valvula" in name and "check" in name and ("vertical" in name or "resorte" in name):
                    matched_group = g
                    match_reason = "Nombre:Valvula Check Vertical"
                    break
                elif gid == "pichancha-valvula-pie-cisterna-laton-foset" and ("pichancha" in name or ("valvula" in name and "pie" in name)):
                    matched_group = g
                    match_reason = "Nombre:Pichancha Cisterna"
                    break
                elif gid == "valvula-globo-laton-roscable-foset" and "valvula" in name and "globo" in name:
                    matched_group = g
                    match_reason = "Nombre:Valvula Globo"
                    break
                elif gid == "valvula-compuerta-laton-roscable-foset" and "valvula" in name and "compuerta" in name:
                    matched_group = g
                    match_reason = "Nombre:Valvula Compuerta"
                    break
                elif gid == "flotador-esferico-polietileno-tinaco-foset" and "flotador" in name and ("tinaco" in name or "varilla" in name or "polietileno" in name):
                    matched_group = g
                    match_reason = "Nombre:Flotador Tinaco"
                    break
                elif gid == "valvula-angular-paso-lavabo-fregadero-foset" and "valvula" in name and ("angular" in name or "paso" in name) and ("lavabo" in name or "fregadero" in name):
                    matched_group = g
                    match_reason = "Nombre:Valvula Angular"
                    break
                elif gid == "herraje-completo-tanque-wc-descarga-foset" and ("herraje" in name or "valvula" in name) and ("wc" in name or "tanque" in name or "inodoro" in name):
                    matched_group = g
                    match_reason = "Nombre:Herraje WC"
                    break
                elif gid == "gabinete-estanco-tubos-led-volteck" and ("gabinete" in name or "estanco" in name) and ("tubo" in name or "led" in name):
                    matched_group = g
                    match_reason = "Nombre:Gabinete Estanco"
                    break
                elif gid == "plafon-led-redondo-sobreponer-volteck" and ("plafon" in name or "panel" in name) and "led" in name:
                    matched_group = g
                    match_reason = "Nombre:Plafon LED"
                    break
                elif gid == "maneral-cruz-laton-cromado-foset" and "maneral" in name and ("cruz" in name or "llave" in name or "cromo" in name):
                    matched_group = g
                    match_reason = "Nombre:Maneral Cruz"
                    break
                elif gid == "valvula-esfera-roscable-mariposa-foset" and "valvula" in name and "esfera" in name and "mariposa" in name:
                    matched_group = g
                    match_reason = "Nombre:Valvula Esfera Mariposa"
                    break
                elif gid == "abrazadera-toma-domiciliaria-foset" and "abrazadera" in name and ("toma" in name or "reparacion" in name or "tuberia" in name):
                    matched_group = g
                    match_reason = "Nombre:Abrazadera Toma"
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
    print("¡MÓDULO C COMPLETADO CON ÉXITO!")
    print(f"  - Total Familias Visuales en Manifiesto: {len(existing_groups)} (meta: 561)")
    print(f"  - Total Códigos / Claves Catalogadas: {total_sku_mappings}")
    print(f"  - Total Artículos de Tienda con Fotos Oficiales: {len(updated_products_list)} (antes 638)")
    print("=" * 75)

if __name__ == "__main__":
    run()
