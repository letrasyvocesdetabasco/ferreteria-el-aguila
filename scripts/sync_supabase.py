#!/usr/bin/env python3
"""
Script de sincronización e ingesta de datos en build-time para Ferretería El Águila.
Consulta la API REST de PostgREST en Supabase y actualiza data/products.json.
En caso de fallo de red o ausencia de credenciales, preserva de forma segura el caché local.
"""

import json
import os
import sys
from typing import Any, Dict, List

try:
    import requests
except ImportError:
    print("Aviso: 'requests' no está instalado. Manteniendo dataset local existente.", file=sys.stderr)
    requests = None


def extract_remote_catalog() -> List[Dict[str, Any]]:
    """Consulta la API de Supabase y retorna el catálogo completo de productos activos.
    
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con la información de los productos.
    """
    if requests is None:
        return []

    supabase_url: str = os.getenv("SUPABASE_URL", "").rstrip("/")
    api_key: str = os.getenv("SUPABASE_ANON_KEY", "")

    if not supabase_url or not api_key:
        print("[sync_supabase] Credenciales no configuradas (SUPABASE_URL / SUPABASE_ANON_KEY).", file=sys.stderr)
        print("[sync_supabase] Operando en modo contingencia local (data/products.json preservado).", file=sys.stderr)
        return []

    endpoint: str = f"{supabase_url}/rest/v1/products"
    params: Dict[str, str] = {
        "select": "sku,manufacturer_code,name,slug,base_price,unit_measure,stock_status,attributes,description,categories(name,slug),brands(name)",
        "is_active": "eq.true",
        "order": "name.asc"
    }
    headers: Dict[str, str] = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        print(f"[sync_supabase] Solicitando catálogo remoto a {endpoint}...")
        response = requests.get(endpoint, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, list) and len(payload) > 0:
            print(f"[sync_supabase] {len(payload)} productos obtenidos exitosamente desde Supabase.")
            return payload
        print("[sync_supabase] La respuesta no contiene productos válidos.", file=sys.stderr)
        return []
    except Exception as err:
        print(f"[sync_supabase] Error al conectar con Supabase: {err}", file=sys.stderr)
        print("[sync_supabase] Se mantendrá el archivo data/products.json existente.", file=sys.stderr)
        return []


def main() -> None:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(base_dir, "data", "products.json")

    catalog_data = extract_remote_catalog()

    if catalog_data:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as file_handle:
            json.dump(catalog_data, file_handle, ensure_ascii=False, indent=2)
        print(f"[sync_supabase] Archivo actualizado exitosamente: {output_file} ({len(catalog_data)} partidas).")
    else:
        if os.path.exists(output_file):
            print(f"[sync_supabase] Archivo local existente conservado sin modificaciones: {output_file}")
        else:
            print(f"[sync_supabase] ALERTA: No existe archivo local previo en {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
