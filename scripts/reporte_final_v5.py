"""
PASO 5: Reporte final de la BD V5 tras los 4 pasos.
Imprime panorama y genera md en Downloads.
"""
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

DB = os.environ.get('ORION_DB_PATH', r'C:\opt\orion_v5\data\orion.db')
OUT = Path(r"C:\Users\garci\Downloads\ORION_auditoria_17_11_2026\23_estado_final_v5.md")


def main():
    if not os.path.exists(DB):
        print(f"[ERROR] no existe BD", file=sys.stderr); return 1
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    def q1(sql, *args):
        return conn.execute(sql, args).fetchone()[0]

    md = []
    md.append("# Estado final BD V5 tras los 5 pasos — 18/11/2026\n\n")

    # Sucursales + comerciales
    md.append("## Sucursales y comerciales\n\n")
    for r in conn.execute("""
        SELECT s.nombre AS suc,
               (SELECT COUNT(*) FROM corredores co WHERE co.sucursal=s.nombre) AS n_corredores,
               (SELECT COUNT(*) FROM comerciales c WHERE c.sucursal_id=s.id) AS n_comerciales,
               (SELECT GROUP_CONCAT(c.nombre, ', ') FROM comerciales c WHERE c.sucursal_id=s.id) AS comerciales
        FROM sucursales s ORDER BY s.nombre
    """).fetchall():
        md.append(f"- **{r['suc']}**: {r['n_corredores']} corredores · {r['n_comerciales']} comerciales ({r['comerciales']})\n")

    # Corredores
    total_corr = q1("SELECT COUNT(*) FROM corredores")
    con_cif = q1("SELECT COUNT(*) FROM corredores WHERE cif IS NOT NULL AND cif != ''")
    con_suc = q1("SELECT COUNT(*) FROM corredores WHERE sucursal IS NOT NULL AND sucursal != ''")
    md.append(f"\n## Corredores\n\n")
    md.append(f"- Total: **{total_corr}**\n- Con CIF: {con_cif}\n- Con sucursal: {con_suc}\n")

    # Flotas
    total_f = q1("SELECT COUNT(*) FROM flotas")
    con_cif_f = q1("SELECT COUNT(*) FROM flotas WHERE cif IS NOT NULL AND cif != ''")
    sin_cif_f = total_f - con_cif_f
    con_com = q1("SELECT COUNT(*) FROM flotas WHERE comercial_traido_id IS NOT NULL")
    md.append(f"\n## Flotas\n\n")
    md.append(f"- Total: **{total_f}**\n- Con CIF: **{con_cif_f}** ({100*con_cif_f/max(total_f,1):.0f}%)\n- Sin CIF: {sin_cif_f}\n- Con comercial que la trajo: {con_com}\n")

    # Flotas por estado del estudio más reciente
    md.append("\n## Flotas por estado del estudio más reciente\n\n")
    for r in conn.execute("""
        SELECT COALESCE((SELECT e.estado FROM estudios e WHERE e.flota_id=f.id ORDER BY e.actualizado_en DESC LIMIT 1), '(sin estudio)') AS estado,
               COUNT(*) AS n
        FROM flotas f GROUP BY estado ORDER BY n DESC
    """).fetchall():
        md.append(f"- {r['estado']}: {r['n']}\n")

    # Estudios
    total_e = q1("SELECT COUNT(*) FROM estudios")
    con_com_e = q1("SELECT COUNT(*) FROM estudios WHERE comercial_id IS NOT NULL")
    md.append(f"\n## Estudios\n\n")
    md.append(f"- Total: **{total_e}**\n- Con comercial asignado: **{con_com_e}** ({100*con_com_e/max(total_e,1):.0f}%)\n")

    # Emisiones
    total_em = q1("SELECT COUNT(*) FROM emisiones")
    md.append(f"\n## Emisiones\n\n- Total: **{total_em}**\n")

    # Verificación REMAR
    md.append("\n## Verificación REMAR\n\n")
    remar_rows = conn.execute("""
        SELECT nombre, cif FROM flotas WHERE nombre LIKE 'REMAR %' ORDER BY nombre
    """).fetchall()
    if remar_rows:
        md.append("| Nombre | CIF |\n|---|---|\n")
        for r in remar_rows:
            md.append(f"| {r['nombre']} | `{r['cif']}` |\n")
    else:
        md.append("_No se encontraron flotas REMAR._\n")

    # Top 10 corredores con más flotas
    md.append("\n## Top 10 corredores con más flotas\n\n")
    for r in conn.execute("""
        SELECT co.nombre, co.sucursal, COUNT(f.id) AS n
        FROM corredores co LEFT JOIN flotas f ON f.corredor_id = co.id
        GROUP BY co.id ORDER BY n DESC LIMIT 10
    """).fetchall():
        md.append(f"- **{r['nombre']}** ({r['sucursal']}): {r['n']} flotas\n")

    OUT.write_text(''.join(md), encoding='utf-8')

    # También imprimir en consola el resumen
    print()
    print("=" * 60)
    print("RESUMEN ESTADO FINAL V5")
    print("=" * 60)
    print(f"Sucursales:    {q1('SELECT COUNT(*) FROM sucursales')}")
    print(f"Comerciales:   {q1('SELECT COUNT(*) FROM comerciales')}")
    print(f"Corredores:    {q1('SELECT COUNT(*) FROM corredores')}")
    print(f"Flotas:        {q1('SELECT COUNT(*) FROM flotas')}  (con CIF: {q1('SELECT COUNT(*) FROM flotas WHERE cif IS NOT NULL AND cif != \"\"')})")
    print(f"Estudios:      {q1('SELECT COUNT(*) FROM estudios')}")
    print(f"Emisiones:     {q1('SELECT COUNT(*) FROM emisiones')}")
    print(f"\n[OK] Reporte -> {OUT}")
    conn.close()


if __name__ == '__main__':
    raise SystemExit(main() or 0)
