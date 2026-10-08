# Cambios v3 — Optimización para celular (8 oct 2026)

## Sucursales
- Solo **Las Delicias** y **Estrellas de Buena Vista** son funcionales (llamar, WhatsApp, mapa, seleccionar, cotizar).
- **Gaviotas Norte, Miguel Hidalgo III Etapa y Joem** siguen visibles, pero sus botones son decorativos
  (`data-decorative="true"`, sin `href`, opciones `disabled` en el selector). En `app.js` tienen `active: false`
  y `isActiveBranch()` bloquea cualquier selección, incluso si quedó guardada en el celular de visitas anteriores.
- Se quitaron del marcado Schema.org (Google) para que no aparezcan como llamables.
- `<meta name="format-detection" content="telephone=no">` evita que el celular vuelva "tocables" sus números.
- Para reactivar una sucursal: `active: true` en `BRANCHES` y restaurar sus enlaces en `index.html`.

## Celular
- Encabezado compacto: al bajar solo queda el buscador fijo arriba.
- Productos en formato lista (foto chica, nombre, precio grande, botones de 50 px).
- Departamentos y marcas como fichas deslizables; búsquedas rápidas de obra en el inicio.
- Aviso al agregar ("Ver cotización"), contador con rebote, botón "Vaciar lista", +/- en la lista.
- Barra inferior: Buscar · Llamar (a la sucursal elegida) · Sucursales · WhatsApp · Mi lista.
- El botón "Atrás" de Android cierra la cotización en lugar de salir de la página.
- Campos a 16 px (iPhone ya no hace zoom), probado en 320 px (iPhone SE) hasta escritorio.

## Búsqueda
- Sin acentos y con plurales: "valvulas" → Válvula, "tornillos" → Tornillo, "luces" → Luz.
- Orden por relevancia; sugerencias en vivo con botón "+" para agregar directo.
- Si no hay coincidencia exacta muestra los más parecidos. Enlaces compartibles: `?q=cemento`, `?depto=...`.
- Precios con separador de miles ($1,234.50); precio 0 → "Precio en mostrador".

## Rendimiento
- Fotos genéricas de departamento en WebP (`assets/images/opt/`): de ~800 KB a ~10 KB por tarjeta.
- Supabase JS ya no bloquea la carga (solo se descarga si se configura).
- PWA: `manifest.webmanifest` + `sw.js` (se puede instalar y funciona con señal débil).
  Si cambias archivos y quieres forzar actualización, sube `CACHE_VERSION` en `sw.js`.
- Carga continua de productos (3 tandas automáticas, luego botón para poder llegar a Sucursales).

## Pruebas
- `python3 tests/test_runner.py` → 107 pruebas OK. Se corrigió la ruta fija de `test_audit_updates.py`
  y se actualizaron las pruebas de sucursales a la nueva regla.
