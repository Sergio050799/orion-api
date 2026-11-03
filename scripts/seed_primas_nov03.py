# Seed de primas/ajustes del 03/11/2026.
# Decisión del jefe: 2.ª categoría INTACTA (documento oficial); solo cambian 1.ª y 3.ª cat.
import os, sqlite3, sys
from pathlib import Path

DB = Path(os.environ.get("ORION_DB_PATH",
    r"C:\Users\garci\Documents\GitHub\orion-api\data\orion.db"))

# Nacional y, para 1.ª cat. + moto, se duplica en Internacional (decisión 03/11: ámbito no cambia la
# tarifa en esas tipologías; el fallback silencioso dejaba huecos en Admin).
_CAT1_MOTO = [
    ("turismo",              "terceros",           500.0),
    ("turismo",              "terceros_ampliado",  650.0),
    ("turismo",              "todo_riesgo",        850.0),
    ("derivado_turismo",     "terceros",           395.0),
    ("derivado_turismo",     "terceros_ampliado",  650.0),
    ("derivado_turismo",     "todo_riesgo",        950.0),
    ("derivado_todoterreno", "terceros",           550.0),
    ("derivado_todoterreno", "terceros_ampliado",  750.0),
    ("derivado_todoterreno", "todo_riesgo",       1150.0),
    ("furgoneta",            "terceros",           500.0),
    ("furgoneta",            "terceros_ampliado",  650.0),
    ("furgoneta",            "todo_riesgo",       1050.0),
    ("furgon",               "terceros",           640.0),
    ("furgon",               "terceros_ampliado",  950.0),
    ("furgon",               "todo_riesgo",       1350.0),
    ("moto",                 "terceros",           336.08),
    ("moto",                 "todo_riesgo",        426.89),
]
PRIMAS_NUEVAS = (
    [(t, c, "nacional",      p) for t, c, p in _CAT1_MOTO] +
    [(t, c, "internacional", p) for t, c, p in _CAT1_MOTO]
)

AJUSTES_NUEVOS = [
    # clave, valor, descripcion
    ("asistencia_oro",             35.0,  "Asistencia Oro (1.ª cat.)"),
    ("asistencia_oro_plus",        75.0,  "Asistencia Oro Plus (1.ª cat.)"),
    ("asistencia_platino",        110.0,  "Asistencia Platino (1.ª cat.)"),
    ("asistencia_servicio_pub",   160.0,  "Asistencia furgoneta servicio público (Platino)"),
    ("asistencia_servicio_pub_oro", 50.0, "Asistencia furgoneta SP (Oro)"),
    ("asistencia_servicio_pub_op", 105.0, "Asistencia furgoneta SP (Oro Plus)"),
    ("asistencia_moto_oro",        30.0,  "Asistencia Oro moto (3.ª cat.)"),
    ("asistencia_nacional",       221.0,  "Asistencia Nacional (2.ª cat.)"),
    ("asistencia_internacional",  327.0,  "Asistencia Internacional (2.ª cat.)"),
    ("reposo_cat1",                40.0,  "RC voluntaria en reposo — 1.ª cat."),
    ("reposo_cat2",                80.0,  "RC voluntaria en reposo — 2.ª cat."),
    ("reposo_moto",                25.0,  "RC voluntaria en reposo — moto"),
    ("lunas_cat1_terceros",        70.0,  "Suplemento lunas en Terceros — 1.ª cat. (turismo/derivados/furgoneta)"),
    ("lunas_furgon_terceros",     100.0,  "Suplemento lunas en Terceros — furgón grande"),
    ("animales",                   25.0,  "Colisión con animales (fijo)"),
    ("perdida_total_pct",           0.12, "Pérdida total (% sobre prima base)"),
    ("isotermo_pct",                0.30, "Isotermo (% sobre prima base)"),
    ("tr_alpha",                    0.35, "Exponente curva TR por franquicia"),
    ("tr_fref_cat1",              300.0,  "Franquicia de referencia TR — 1.ª cat."),
    ("tr_fref_cat2",             1800.0,  "Franquicia de referencia TR — 2.ª cat."),
    ("tr_fref_moto",              500.0,  "Franquicia de referencia TR — moto"),
]

def main():
    if not DB.exists():
        print(f"ERROR: no existe {DB}")
        sys.exit(1)
    con = sqlite3.connect(DB)
    cur = con.cursor()

    print(f"DB: {DB}")
    print(f"\n[1/2] primas_config — upsert de {len(PRIMAS_NUEVAS)} filas (1.ª y 3.ª cat.; 2.ª INTACTA)")
    for tipo, cob, amb, prima in PRIMAS_NUEVAS:
        cur.execute("""
            INSERT INTO primas_config (tipo_vehiculo, cobertura, ambito, prima, updated_by)
            VALUES (?,?,?,?, 'spike-nov03')
            ON CONFLICT(tipo_vehiculo, cobertura, ambito) DO UPDATE SET
                prima = excluded.prima,
                updated_at = datetime('now'),
                updated_by = excluded.updated_by
        """, (tipo, cob, amb, prima))
        print(f"  {tipo}:{cob}:{amb} = {prima}")

    print(f"\n[2/2] ajustes_config — upsert de {len(AJUSTES_NUEVOS)} claves")
    for clave, valor, desc in AJUSTES_NUEVOS:
        cur.execute("""
            INSERT INTO ajustes_config (clave, valor, descripcion)
            VALUES (?,?,?)
            ON CONFLICT(clave) DO UPDATE SET
                valor = excluded.valor,
                descripcion = excluded.descripcion,
                updated_at = datetime('now')
        """, (clave, valor, desc))
        print(f"  {clave} = {valor}")

    con.commit()

    # Verificación
    print("\n[verificación] primas_config · 1.ª cat.:")
    for r in cur.execute("""
        SELECT tipo_vehiculo, cobertura, prima FROM primas_config
         WHERE tipo_vehiculo IN ('turismo','derivado_turismo','derivado_todoterreno','furgoneta','furgon','moto')
         ORDER BY tipo_vehiculo, cobertura
    """):
        print(" ", r)

    print("\n[verificación] primas_config · 2.ª cat. (debe estar intacta):")
    for r in cur.execute("""
        SELECT tipo_vehiculo, cobertura, ambito, prima FROM primas_config
         WHERE tipo_vehiculo IN ('cabeza_tractora','camion_rigido','semirremolque','industrial_matriculado','industrial_no_matriculado')
         ORDER BY tipo_vehiculo, cobertura, ambito
    """):
        print(" ", r)

    con.close()
    print("\n✅ Seed completado.")

if __name__ == "__main__":
    main()
