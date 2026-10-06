-- Flotas CONTRATADAS (gestion manual jefe, oct-2026)
-- Anio de vencimiento: 2027 (renovacion proxima)
BEGIN TRANSACTION;

-- Transportes Laredo (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES LAREDO', 'CONTRATADA', 'TRANSPORTES LAREDO', '', 'AON', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES LAREDO'));

-- Tres Campanas (ARAGONES Y CEMBORAIN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRES CAMPANAS', 'CONTRATADA', 'TRES CAMPANAS', '', 'ARAGONES Y CEMBORAIN', '', '2027-07-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRES CAMPANAS'));

-- Transportes Isidro San Roman e Hijos SL (ARAGONES Y CEMBORAIN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES ISIDRO SAN ROMAN E HIJOS SL', 'CONTRATADA', 'TRANSPORTES ISIDRO SAN ROMAN E HIJOS SL', '', 'ARAGONES Y CEMBORAIN', '', '2027-08-07', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES ISIDRO SAN ROMAN E HIJOS SL'));

-- FUNDACION BANCO DE ALIMENTOS DE MADRID (ATSYR CORREDURIA DE SEGUROS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FUNDACION BANCO DE ALIMENTOS DE MADRID', 'CONTRATADA', 'FUNDACION BANCO DE ALIMENTOS DE MADRID', '', 'ATSYR CORREDURIA DE SEGUROS', '', '2027-06-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FUNDACION BANCO DE ALIMENTOS DE MADRID'));

-- TRANSPORTES HIRUMUGETA (BIDASOA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES HIRUMUGETA', 'CONTRATADA', 'TRANSPORTES HIRUMUGETA', '', 'BIDASOA', '', '2027-10-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES HIRUMUGETA'));

-- ALVEMACO (MDS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALVEMACO', 'CONTRATADA', 'ALVEMACO', '', 'MDS', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALVEMACO'));

-- MARMOLES TOLEDANOS (COTASEGUR SL)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'MARMOLES TOLEDANOS', 'CONTRATADA', 'MARMOLES TOLEDANOS', '', 'COTASEGUR SL', '', '2027-10-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('MARMOLES TOLEDANOS'));

-- IGNACIO LIMA ZABALEGUI (DELTA CORREDURIA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'IGNACIO LIMA ZABALEGUI', 'CONTRATADA', 'IGNACIO LIMA ZABALEGUI', '', 'DELTA CORREDURIA', '', '2027-09-14', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('IGNACIO LIMA ZABALEGUI'));

-- EMBOTITS PORTELLA SL (ERSM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'EMBOTITS PORTELLA SL', 'CONTRATADA', 'EMBOTITS PORTELLA SL', '', 'ERSM', '', '2027-09-11', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('EMBOTITS PORTELLA SL'));

-- GRUAS Y PORTA VEHICULOS PEDRO SL (JUNYENT PRAT CORREDURIA D'ASSEGURANCES, S.L.)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUAS Y PORTA VEHICULOS PEDRO SL', 'CONTRATADA', 'GRUAS Y PORTA VEHICULOS PEDRO SL', '', 'JUNYENT PRAT CORREDURIA D''ASSEGURANCES, S.L.', '', '2027-07-10', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUAS Y PORTA VEHICULOS PEDRO SL'));

-- TRANSPORTES VALLE DEL OJA SL (JOSEFINA FERREIROS SANCHEZ-GUISANDE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES VALLE DEL OJA SL', 'CONTRATADA', 'TRANSPORTES VALLE DEL OJA SL', '', 'JOSEFINA FERREIROS SANCHEZ-GUISANDE', '', '2027-05-29', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES VALLE DEL OJA SL'));

-- IMPULS WORLD LOGISTICS SL (LARREA & BAREA CORREDURIA DE SEGUROS, S.L.)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'IMPULS WORLD LOGISTICS SL', 'CONTRATADA', 'IMPULS WORLD LOGISTICS SL', '', 'LARREA & BAREA CORREDURIA DE SEGUROS, S.L.', '', '2027-10-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('IMPULS WORLD LOGISTICS SL'));

-- PSM VIVER DEL REC SL (M. PIQUE CORREDURIA TECNICA DE SEGUROS, S.A.)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'PSM VIVER DEL REC SL', 'CONTRATADA', 'PSM VIVER DEL REC SL', '', 'M. PIQUE CORREDURIA TECNICA DE SEGUROS, S.A.', '', '2027-07-17', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('PSM VIVER DEL REC SL'));

-- Transportes BRAMAR (MINGUEZ SAEZ BROKERS, S.L.)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES BRAMAR', 'CONTRATADA', 'TRANSPORTES BRAMAR', '', 'MINGUEZ SAEZ BROKERS, S.L.', '', '2027-01-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES BRAMAR'));

-- BENAYAS SERVICIOS LOGISTICOS SL (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'BENAYAS SERVICIOS LOGISTICOS SL', 'CONTRATADA', 'BENAYAS SERVICIOS LOGISTICOS SL', '', 'MOLYMA', '', '2027-09-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('BENAYAS SERVICIOS LOGISTICOS SL'));

-- Alberto y Antonio estrella grano de oro (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALBERTO Y ANTONIO ESTRELLA GRANO DE ORO', 'CONTRATADA', 'ALBERTO Y ANTONIO ESTRELLA GRANO DE ORO', '', 'MOLYMA', '', '2027-09-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALBERTO Y ANTONIO ESTRELLA GRANO DE ORO'));

-- ON-RED TRUCK LOGISTICS (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ON-RED TRUCK LOGISTICS', 'CONTRATADA', 'ON-RED TRUCK LOGISTICS', '', 'MOLYMA', '', '2027-05-17', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ON-RED TRUCK LOGISTICS'));

-- SERGETRANS SL (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SERGETRANS SL', 'CONTRATADA', 'SERGETRANS SL', '', 'MOLYMA', '', '2027-07-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SERGETRANS SL'));

-- SOTO ECOTRANS SL (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SOTO ECOTRANS SL', 'CONTRATADA', 'SOTO ECOTRANS SL', '', 'MOLYMA', '', '2027-03-25', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SOTO ECOTRANS SL'));

-- TRANSPORTES BAS 2023 SL (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES BAS 2023 SL', 'CONTRATADA', 'TRANSPORTES BAS 2023 SL', '', 'MOLYMA', '', '2027-04-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES BAS 2023 SL'));

-- TRANSPORTES FARMACOLOGICOS CASTILLA, S.L. (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES FARMACOLOGICOS CASTILLA, S.L.', 'CONTRATADA', 'TRANSPORTES FARMACOLOGICOS CASTILLA, S.L.', '', 'MOLYMA', '', '2027-02-24', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES FARMACOLOGICOS CASTILLA, S.L.'));

-- LOGISTICA Y TRANSPORTES DE PEDRO (PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOGISTICA Y TRANSPORTES DE PEDRO', 'CONTRATADA', 'LOGISTICA Y TRANSPORTES DE PEDRO', '', 'PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.', '', '2027-07-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOGISTICA Y TRANSPORTES DE PEDRO'));

-- DPM LOGISTICA 1966 SL (PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, fecha_vencimiento, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'DPM LOGISTICA 1966 SL', 'CONTRATADA', 'DPM LOGISTICA 1966 SL', '', 'PEDRO MARTINEZ DE QUEL CORREDURIA DE SEGUROS S.L.', '', '2027-07-01', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('DPM LOGISTICA 1966 SL'));

COMMIT;

-- Verificar:
-- SELECT count(*) FROM flotas_historicas WHERE estado='CONTRATADA';
-- SELECT nombre, corredor_nombre, fecha_vencimiento FROM flotas_historicas WHERE estado='CONTRATADA' ORDER BY nombre;