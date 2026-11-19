"""
Analiza la ESTRUCTURA REAL del inventario_drive.json.
Las categorías pueden tener niveles distintos:
  ACTIVAS: FLOTAS/ACTIVAS/[CORREDOR]/[FLOTA]/...
  REHUSADAS: FLOTAS/REHUSADAS/[FLOTA]/...
  etc.
Objetivo: detectar automáticamente dónde está la "flota" real.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

INV = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\inventario_drive.json")

CATEGORIAS = [
    "FLOTAS/ACTIVAS",
    "FLOTAS/FLOTAS SOLICITADAS O COTIZADAS Y NO CONTRATADAS",
    "FLOTAS/FLOTAS HECHAS POR TITAN 2025-2026",
    "FLOTAS/ESTUDIOS",
    "FLOTAS/FLOTAS REHUSADAS",
]


def main():
    items = json.load(INV.open(encoding='utf-8'))
    # Para cada categoría: contar carpetas de nivel 2 y nivel 3
    for cat in CATEGORIAS:
        n2_dirs = []
        n3_dirs = []
        for it in items:
            if not it.get('IsDir'):
                continue
            p = it.get('Path', '')
            if not p.startswith(cat + '/'):
                continue
            rel = p[len(cat) + 1:]
            depth = rel.count('/') + 1
            if depth == 1:
                n2_dirs.append(rel)
            elif depth == 2:
                n3_dirs.append(rel)
        # Heurística: si nivel 2 son pocos (<50) y nivel 3 son muchos (>50),
        # probablemente nivel 2 = corredor y nivel 3 = flota.
        print(f"\n=== {cat} ===")
        print(f"  Nivel 2 (hijos directos):   {len(n2_dirs)} carpetas")
        print(f"  Nivel 3 (nietos directos):  {len(n3_dirs)} carpetas")
        # Nombres típicos nivel 2
        print(f"  Muestra nivel 2 (primeros 6): {[n.split('/')[0] for n in n2_dirs[:6]]}")
        if n3_dirs:
            print(f"  Muestra nivel 3 (primeros 6): {[n for n in n3_dirs[:6]]}")

    print("\n" + "=" * 70)
    print("CONCLUSION PRELIMINAR POR CATEGORIA")
    print("=" * 70)


if __name__ == '__main__':
    main()
