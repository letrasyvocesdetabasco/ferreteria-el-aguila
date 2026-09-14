# Original User Request

## Initial Request — 2026-09-14T11:48:10-06:00

Actualización integral del catálogo de Ferretería y Tlapalería El Águila con 17,641 productos y precios reales con IVA (+16%) desde raticulos ferre precios.xls, despeje total de la lona física en el hero para visualización sin obstrucciones, e integración del logo oficial del águila extraído de la fachada.

Working directory: /home/divadios/Escritorio/pagina web/ferreteria_el_aguila
Integrity mode: development

## Requirements

### R1. Reemplazo Total del Catálogo con Precios Reales (+ IVA 16%)
- Procesar íntegramente los 17,641 artículos desde /home/divadios/Escritorio/pagina web/ferreteria_el_aguila/raticulos ferre precios.xls (convertido en raticulos ferre precios.csv).
- Eliminar completamente la base de datos de precios anterior de data/products.json.
- Aplicar a cada producto la fórmula de venta al público: base_price = round(PRECIO_1 * 1.16, 2).
- Mapear cada artículo a uno de los 5 departamentos oficiales de la tienda (Tlapalería y Construcción, Tornillería y Fijación, Plomería y Conexiones, Herramientas en General, Material Eléctrico) y detectar marcas homologadas (Truper, Pretul, Voltech, Basic, Hermex, Foset, etc.).
- Mantener la arquitectura de renderizado por lotes (PAGE_SIZE = 36) y búsqueda instantánea en cliente para garantizar 60 FPS sin congelamientos.

### R2. Despeje Visual Completo de la Lona de Mostrador
- En la sección Hero, eliminar los elementos superpuestos que cubren la fotografía oficial (.hero-banner-badge y .hero-banner-caption), permitiendo que el diseño original de la lona (título, silueta, departamentos, lema, teléfono y dirección) se aprecie al 100% de forma nítida.
- Ajustar el contenedor a la proporción natural de la imagen (3:2) con bordes suaves, sombra refinada y sin recortes artificiales.

### R3. Extracción e Integración del Logo Oficial del Águila y Paleta de Marca
- Extraer la silueta oficial del águila en vuelo presente en foto-portada-aguila.jpeg (assets/images/lona-oficial-el-aguila.jpg) como isotipo transparente de alta resolución (assets/images/logo-aguila.png).
- Reemplazar el emoji genérico (🦅) en la cabecera principal, favicon y hero por el logo extraído oficial.
- Armonizar los acentos de la página con los colores vivos de la lona: Azul Eléctrico Mostrador (#004b97 / #0052a5), Amarillo/Oro Intenso (#ffcb05 / #f59e0b) y blanco puro.

### R4. Verificación de Confiabilidad y Despacho WhatsApp
- Verificar que el cotizador de WhatsApp calcule correctamente subtotales y total con los nuevos precios con IVA.
- Asegurar que el selector de sucursales (Las Delicias con referencia al Centro de Salud San Joaquín y Estrellas de Buena Vista) opere sin fallos.
- Ejecutar pruebas automáticas de rendimiento y auditoría de seguridad osvScanner.
- Desplegar la versión final al repositorio GitHub y GitHub Pages.

## Acceptance Criteria

### Integridad de Precios y Catálogo
- [ ] data/products.json contiene los 17,641 artículos de raticulos ferre precios.xls sin duplicados vacíos.
- [ ] Todos los precios corresponden exactamente a PRECIO 1 * 1.16.
- [ ] No persiste ningún precio ni producto del inventario anterior.
- [ ] La búsqueda responde en tiempo real (< 25 ms) para términos clave (tornillo, cobre, pvc, fandeli, cable, broca).

### Estética y Branding
- [ ] La fotografía de la lona física (lona-oficial-el-aguila.jpg) se muestra completa y limpia, sin textos ni overlays encima que tapen la información.
- [ ] El isotipo del águila extraído de la foto se visualiza nítido en el branding de la cabecera.
- [ ] La interfaz mantiene armonía cromática con los colores corporativos azul rey y oro de la ferretería.

### Pruebas y Despliegue
- [ ] El carrito de cotización y mensaje de WhatsApp desglosa partidas con SKU y precios actualizados.
- [ ] La auditoría de seguridad osvScanner reporta 0 vulnerabilidades.
- [ ] El sitio está publicado y funcional en https://ferreteriaytlapaleria-elaguila.com y https://letrasyvocesdetabasco.github.io/ferreteria-el-aguila/.
