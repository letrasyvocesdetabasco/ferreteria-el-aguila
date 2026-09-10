-- =====================================================================
-- Ferretería y Tlapalería El Águila (Villahermosa, Tabasco)
-- Esquema de Base de Datos para Catálogo Técnico Paramétrico (PostgreSQL / Supabase)
-- =====================================================================

-- Extensiones requeridas para generación de identificadores y soporte de búsqueda difusa (trigramas)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 1. Tabla de Categorías con jerarquía recursiva padre-hijo
CREATE TABLE IF NOT EXISTS public.categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES public.categories(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    icon TEXT,
    display_order INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Tabla de Marcas Comerciales Homologadas
CREATE TABLE IF NOT EXISTS public.brands (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    logo_url TEXT,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Tabla Principal de Inventario Ferretero y Tlapalero
CREATE TABLE IF NOT EXISTS public.products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku TEXT UNIQUE NOT NULL,                       -- Código interno de mostrador (ej. EAG-TORN-001)
    manufacturer_code TEXT,                         -- Clave de catálogo técnico (ej. 49012, 10845)
    barcode TEXT,                                   -- Código de barras universal (EAN-13/UPC)
    category_id UUID NOT NULL REFERENCES public.categories(id) ON DELETE RESTRICT,
    brand_id UUID NOT NULL REFERENCES public.brands(id) ON DELETE RESTRICT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    short_description TEXT,
    description TEXT,
    base_price NUMERIC(12, 2) NOT NULL CHECK (base_price >= 0),
    unit_measure TEXT NOT NULL DEFAULT 'PIEZA',     -- PIEZA, METRO, KG, ROLLO, JUEGO, MILLAR, CIENTO
    stock_status TEXT NOT NULL DEFAULT 'in_stock' 
        CHECK (stock_status IN ('in_stock', 'low_stock', 'out_of_stock', 'on_demand')),
    images TEXT[] NOT NULL DEFAULT '{}',
    technical_sheet_url TEXT,
    
    -- Atributos técnicos variables (material, rosca, calibre, presión, medida, etc.)
    attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
    
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_featured BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Índices Convencionales (B-Tree) para relaciones y filtros básicos
CREATE INDEX IF NOT EXISTS idx_products_category ON public.products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_brand ON public.products(brand_id);
CREATE INDEX IF NOT EXISTS idx_products_sku ON public.products(sku);
CREATE INDEX IF NOT EXISTS idx_products_active ON public.products(is_active);

-- 5. Índice GIN sobre JSONB para consultas paramétricas de alta velocidad
CREATE INDEX IF NOT EXISTS idx_products_attributes_gin ON public.products USING gin (attributes jsonb_path_ops);

-- 6. Índice GIN con trigramas para búsqueda difusa tolerante a errores ortográficos
CREATE INDEX IF NOT EXISTS idx_products_name_trgm ON public.products USING gin (name gin_trgm_ops);

-- 7. Índice de Texto Completo (Full-Text Search) en español
CREATE INDEX IF NOT EXISTS idx_products_fulltext ON public.products USING gin (
    to_tsvector('spanish', coalesce(name, '') || ' ' || coalesce(description, '') || ' ' || coalesce(manufacturer_code, ''))
);

-- =====================================================================
-- Configuración de Seguridad a Nivel de Fila (Row Level Security - RLS)
-- =====================================================================

ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

-- Revocar mutaciones públicas
REVOKE ALL ON public.categories FROM anon;
REVOKE ALL ON public.brands FROM anon;
REVOKE ALL ON public.products FROM anon;

-- Conceder exclusivamente lectura al rol anónimo
GRANT SELECT ON public.categories TO anon;
GRANT SELECT ON public.brands TO anon;
GRANT SELECT ON public.products TO anon;

-- Políticas de lectura controlada (solo activos)
DROP POLICY IF EXISTS "Public Read Categories" ON public.categories;
CREATE POLICY "Public Read Categories" 
ON public.categories FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read Brands" ON public.brands;
CREATE POLICY "Public Read Brands" 
ON public.brands FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "Public Read Active Products" ON public.products;
CREATE POLICY "Public Read Active Products" 
ON public.products FOR SELECT TO anon, authenticated 
USING (is_active = true);
