# Ferretería y Tlapalería El Águila — Plataforma Web Estática

Plataforma web técnica de alta densidad para **Ferretería y Tlapalería El Águila**, orientada al suministro de herramientas, material eléctrico, plomería hidráulica, tornillería de alta resistencia (G5, NF, NC, métrica), varilla roscada, abrasivos Fandeli y artículos para la construcción y taller en **Villahermosa, Tabasco**.

Inspirada en los estándares de interfaces técnicas de alta densidad (McMaster-Carr y Truper), esta plataforma Jamstack opera con coste cero de servidor, búsqueda instantánea en cliente, arquitectura híbrida de datos con Supabase y cotización directa para mostrador vía WhatsApp.

---

## 📍 Sucursales en Villahermosa, Tabasco

| Sucursal | Responsable | Dirección | Teléfono / WhatsApp | Horario |
|---|---|---|---|---|
| **1. Las Delicias** | Timoteo Méndez | Av. Revolución 1203, Cuadrante II (junto al C.S. San Joaquín) | 993 289 2935 | Lun - Vie: 8:00 - 18:00 <br> Sáb: 8:00 - 15:00 <br> Dom: 9:00 - 14:00 |
| **2. Estrellas de Buena Vista** | Timoteo Méndez | Carr. Villahermosa a La Isla Km 5.300, Buena Vista 1ra Secc | 993 192 8313 | Lun - Vie: 8:00 - 18:00 <br> Sáb: 8:00 - 15:00 <br> Dom: 9:00 - 14:00 |
| **3. Gaviotas Norte** | Miguel Méndez | Aquiles Calderón Marchena 120, Col. Gaviotas Nte. | 993 289 2935 | Todos los días: 8:00 - 18:00 continuo |
| **4. Miguel Hidalgo III Etapa** | Salomón Méndez | Carr. Villahermosa a La Isla, Miguel Hidalgo III Etapa | 993 141 2755 | Lun - Vie: 8:00 - 18:30 <br> Sáb: 8:00 - 17:00 <br> Dom: 8:00 - 13:00 |

---

## 🛠️ Arquitectura Técnica

- **Frontend Estático (Jamstack)**: HTML5 semántico, CSS3 puro responsivo sin dependencias pesadas y JavaScript Vanilla (ES6+).
- **Modelo de Datos Híbrido (Dual-Sync)**:
  - **Tiempo Real**: Cliente oficial de `@supabase/supabase-js` consultando la API PostgREST.
  - **Contingencia Offline / GitHub Pages**: Respaldo serializado `data/products.json` actualizado en build-time con `scripts/sync_supabase.py`.
- **Búsqueda Paramétrica Multicriterio**: Filtrado en memoria por nombre, SKU, clave de fabricante, marca y atributos técnicos (`JSONB`).
- **Cierre de Presupuesto WhatsApp**: Serializador de partidas con cálculo de subtotales y generación de enlaces universales `https://wa.me/...`.
- **Despliegue Continuo (CI/CD)**: GitHub Actions configurado en `.github/workflows/deploy.yml` para publicación automática en GitHub Pages.

---

## 📂 Estructura del Repositorio

```
ferreteria_el_aguila/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Pipeline CI/CD para GitHub Pages
├── assets/
│   ├── css/
│   │   └── styles.css          # Estilos de alta densidad técnica
│   └── js/
│       └── app.js              # Lógica de filtrado, carrito y WhatsApp
├── data/
│   └── products.json           # Catálogo maestro local (17,641 artículos con IVA 16%)
├── database/
│   └── schema.sql              # Esquema PostgreSQL con JSONB, GIN y RLS
├── scripts/
│   └── sync_supabase.py        # Extracción y respaldo del catálogo remoto
├── index.html                  # Estructura principal y componentes
└── README.md                   # Documentación técnica
```

---

## 🚀 Pruebas y Ejecución Local

Para levantar la plataforma en local mediante un servidor HTTP nativo de un solo hilo:

```bash
# Desde la carpeta del proyecto
cd ferreteria_el_aguila

# Iniciar servidor local en el puerto 8080
python3 -m http.server 8080
```

Abre en tu navegador: **[http://localhost:8080](http://localhost:8080)**

---

## 🗄️ Configuración de Base de Datos en Supabase (Opcional)

Si deseas sincronizar el catálogo con una base de datos gestionada en la nube:

1. Crea un proyecto gratuito en [Supabase](https://supabase.com).
2. En el **SQL Editor**, ejecuta íntegramente el script [`database/schema.sql`](database/schema.sql).
3. Obtén tu **Project URL** y tu **anon public key** en `Project Settings > API`.
4. Configura los secretos en tu repositorio de GitHub (`Settings > Secrets and variables > Actions`):
   - `SUPABASE_URL`: Tu URL de proyecto.
   - `SUPABASE_ANON_KEY`: Tu clave anónima pública.
5. Edita `assets/js/app.js` con tus claves para habilitar la consulta en tiempo real desde el navegador.

---

## 📦 Despliegue en GitHub Pages

1. Inicializa el repositorio Git y haz tu primer commit:
   ```bash
   git init
   git add .
   git commit -m "feat: plataforma técnica inicial Ferretería El Águila"
   ```
2. Crea un repositorio nuevo en GitHub y vincúlalo:
   ```bash
   git remote add origin https://github.com/TU_USUARIO/ferreteria-el-aguila.git
   git branch -M main
   git push -u origin main
   ```
3. En GitHub, ve a **Settings > Pages** y en **Build and deployment > Source** selecciona **GitHub Actions**.
4. Cada push compilará el catálogo y publicará la web automáticamente.
