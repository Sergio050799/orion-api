-- Importacion flotas historicas (generado automaticamente)
-- Ejecutar en VPS: sqlite3 /opt/orion-api/data/orion.db < flotas_import.sql
-- Omite automaticamente tomadores ya existentes en carpetas o flotas_historicas

BEGIN TRANSACTION;

-- Muriel herrera (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Muriel herrera', 'RECHAZADA', 'Muriel herrera', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Muriel herrera')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Muriel herrera'));

-- AMBULANCIAS DOMINGO (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AMBULANCIAS DOMINGO', 'RECHAZADA', 'AMBULANCIAS DOMINGO', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AMBULANCIAS DOMINGO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AMBULANCIAS DOMINGO'));

-- DAV S.L (CONFIDE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'DAV S.L', 'RECHAZADA', 'DAV S.L', '', 'CONFIDE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('DAV S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('DAV S.L'));

-- PRIMAFRIO (GESA MEDIACIÓN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'PRIMAFRIO', 'RECHAZADA', 'PRIMAFRIO', 'D6838896C', 'GESA MEDIACIÓN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('PRIMAFRIO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('PRIMAFRIO'));

-- RENTAFRIO (GESA MEDIACIÓN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'RENTAFRIO', 'RECHAZADA', 'RENTAFRIO', '', 'GESA MEDIACIÓN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('RENTAFRIO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('RENTAFRIO'));

-- MEMORA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'MEMORA', 'RECHAZADA', 'MEMORA', 'B85012441', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('MEMORA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('MEMORA'));

-- ONDARA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ONDARA', 'RECHAZADA', 'ONDARA', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ONDARA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ONDARA'));

-- ALUMINIOS VALVERDEL DEL VALLES S.L (ERSM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALUMINIOS VALVERDEL DEL VALLES S.L', 'RECHAZADA', 'ALUMINIOS VALVERDEL DEL VALLES S.L', 'B56297443', 'ERSM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ALUMINIOS VALVERDEL DEL VALLES S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALUMINIOS VALVERDEL DEL VALLES S.L'));

-- Pan De Panes Aviva - antonio -Alcosegur (DE PANES -- ANTONIO-ALCOSEGUR)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Pan De Panes Aviva - antonio -Alcosegur', 'RECHAZADA', 'Pan De Panes Aviva - antonio -Alcosegur', 'B05254669', 'DE PANES -- ANTONIO-ALCOSEGUR', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Pan De Panes Aviva - antonio -Alcosegur')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Pan De Panes Aviva - antonio -Alcosegur'));

-- GRUAS PEDROSA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUAS PEDROSA', 'RECHAZADA', 'GRUAS PEDROSA', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUAS PEDROSA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUAS PEDROSA'));

-- Grupo Cron Logistica SLU (ARAGONES)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Grupo Cron Logistica SLU', 'RECHAZADA', 'Grupo Cron Logistica SLU', '79106752T', 'ARAGONES', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Grupo Cron Logistica SLU')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Grupo Cron Logistica SLU'));

-- GRUPO PENTA LOGIS, S.L (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO PENTA LOGIS, S.L', 'RECHAZADA', 'GRUPO PENTA LOGIS, S.L', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO PENTA LOGIS, S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO PENTA LOGIS, S.L'));

-- JESMAR ASTEC SL (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'JESMAR ASTEC SL', 'RECHAZADA', 'JESMAR ASTEC SL', 'B16266413', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('JESMAR ASTEC SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('JESMAR ASTEC SL'));

-- JOTPRO ELEVACION (PLATINUM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'JOTPRO ELEVACION', 'RECHAZADA', 'JOTPRO ELEVACION', '', 'PLATINUM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('JOTPRO ELEVACION')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('JOTPRO ELEVACION'));

-- MAÑERO TRANSPORTES LOGÍSTICA (WILIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'MAÑERO TRANSPORTES LOGÍSTICA', 'RECHAZADA', 'MAÑERO TRANSPORTES LOGÍSTICA', 'B06623128', 'WILIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('MAÑERO TRANSPORTES LOGÍSTICA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('MAÑERO TRANSPORTES LOGÍSTICA'));

-- OCTAVIANO PALOMO (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'OCTAVIANO PALOMO', 'RECHAZADA', 'OCTAVIANO PALOMO', 'B40215402', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('OCTAVIANO PALOMO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('OCTAVIANO PALOMO'));

-- pa igulada (MPIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'pa igulada', 'RECHAZADA', 'pa igulada', '', 'MPIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('pa igulada')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('pa igulada'));

-- placer gastronomico (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'placer gastronomico', 'RECHAZADA', 'placer gastronomico', '', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('placer gastronomico')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('placer gastronomico'));

-- RALOTRANS, S.L._ DISTRIBUCIONES ALONSO OTERO TRANSPORTES, S.L. (DALOT) (MDSCOBIAN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'RALOTRANS, S.L._ DISTRIBUCIONES ALONSO OTERO TRANSPORTES, S.L. (DALOT)', 'RECHAZADA', 'RALOTRANS, S.L._ DISTRIBUCIONES ALONSO OTERO TRANSPORTES, S.L. (DALOT)', '', 'MDSCOBIAN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('RALOTRANS, S.L._ DISTRIBUCIONES ALONSO OTERO TRANSPORTES, S.L. (DALOT)')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('RALOTRANS, S.L._ DISTRIBUCIONES ALONSO OTERO TRANSPORTES, S.L. (DALOT)'));

-- TOLEDANO FRESH SL (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TOLEDANO FRESH SL', 'RECHAZADA', 'TOLEDANO FRESH SL', 'B04869780', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TOLEDANO FRESH SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TOLEDANO FRESH SL'));

-- TRANSDIOR, S.L (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSDIOR, S.L', 'RECHAZADA', 'TRANSDIOR, S.L', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSDIOR, S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSDIOR, S.L'));

-- TRANSPORTES F. URIARTE (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES F. URIARTE', 'RECHAZADA', 'TRANSPORTES F. URIARTE', 'B01046424', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES F. URIARTE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES F. URIARTE'));

-- TRANSPORTES MATEI FLORIN (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES MATEI FLORIN', 'RECHAZADA', 'TRANSPORTES MATEI FLORIN', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES MATEI FLORIN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES MATEI FLORIN'));

-- AGENCIA TRANSPORTES ROBLES SA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AGENCIA TRANSPORTES ROBLES SA', 'RECHAZADA', 'AGENCIA TRANSPORTES ROBLES SA', 'A25042888', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AGENCIA TRANSPORTES ROBLES SA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AGENCIA TRANSPORTES ROBLES SA'));

-- AKZO NOBEL (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AKZO NOBEL', 'RECHAZADA', 'AKZO NOBEL', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AKZO NOBEL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AKZO NOBEL'));

-- Albia Servicios Funerarios (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Albia Servicios Funerarios', 'RECHAZADA', 'Albia Servicios Funerarios', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Albia Servicios Funerarios')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Albia Servicios Funerarios'));

-- ALIMERKA S.A (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALIMERKA S.A', 'RECHAZADA', 'ALIMERKA S.A', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ALIMERKA S.A')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALIMERKA S.A'));

-- ALMA ROAD SL (BFSEGUROS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALMA ROAD SL', 'RECHAZADA', 'ALMA ROAD SL', '', 'BFSEGUROS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ALMA ROAD SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALMA ROAD SL'));

-- ALVANA TRANSPORTES PERSONALIZADOS, S.L (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALVANA TRANSPORTES PERSONALIZADOS, S.L', 'RECHAZADA', 'ALVANA TRANSPORTES PERSONALIZADOS, S.L', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ALVANA TRANSPORTES PERSONALIZADOS, S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALVANA TRANSPORTES PERSONALIZADOS, S.L'));

-- AMBULANCIAS HABICHUELA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AMBULANCIAS HABICHUELA', 'RECHAZADA', 'AMBULANCIAS HABICHUELA', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AMBULANCIAS HABICHUELA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AMBULANCIAS HABICHUELA'));

-- ANI CONSTRUCCIONES Y CONTRATAS (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ANI CONSTRUCCIONES Y CONTRATAS', 'RECHAZADA', 'ANI CONSTRUCCIONES Y CONTRATAS', 'B45756046', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ANI CONSTRUCCIONES Y CONTRATAS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ANI CONSTRUCCIONES Y CONTRATAS'));

-- ARRIETA LEAL Y TOMAS ARRIETA (LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ARRIETA LEAL Y TOMAS ARRIETA', 'RECHAZADA', 'ARRIETA LEAL Y TOMAS ARRIETA', '', 'LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ARRIETA LEAL Y TOMAS ARRIETA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ARRIETA LEAL Y TOMAS ARRIETA'));

-- ASESORAMIENTO Y SERVICIOS LOGISTICOS DEL SUR (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ASESORAMIENTO Y SERVICIOS LOGISTICOS DEL SUR', 'RECHAZADA', 'ASESORAMIENTO Y SERVICIOS LOGISTICOS DEL SUR', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ASESORAMIENTO Y SERVICIOS LOGISTICOS DEL SUR')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ASESORAMIENTO Y SERVICIOS LOGISTICOS DEL SUR'));

-- AUTOS VELASCO (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AUTOS VELASCO', 'RECHAZADA', 'AUTOS VELASCO', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AUTOS VELASCO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AUTOS VELASCO'));

-- AVIMOLSA PROYECTO LIDER (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AVIMOLSA PROYECTO LIDER', 'RECHAZADA', 'AVIMOLSA PROYECTO LIDER', 'B67678078', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AVIMOLSA PROYECTO LIDER')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AVIMOLSA PROYECTO LIDER'));

-- AYUNTAMIENTO DE SAGUNTO (LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AYUNTAMIENTO DE SAGUNTO', 'RECHAZADA', 'AYUNTAMIENTO DE SAGUNTO', 'P4622200F', 'LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AYUNTAMIENTO DE SAGUNTO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AYUNTAMIENTO DE SAGUNTO'));

-- AYUNTAMIENTO DEL BOALO WILLIS (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AYUNTAMIENTO DEL BOALO WILLIS', 'RECHAZADA', 'AYUNTAMIENTO DEL BOALO WILLIS', '66393532B', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AYUNTAMIENTO DEL BOALO WILLIS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AYUNTAMIENTO DEL BOALO WILLIS'));

-- AZVI, SA (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AZVI, SA', 'RECHAZADA', 'AZVI, SA', 'S3933002B', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AZVI, SA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AZVI, SA'));

-- BOMBEOS MARBELLA (PLATINUM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'BOMBEOS MARBELLA', 'RECHAZADA', 'BOMBEOS MARBELLA', 'B93742302', 'PLATINUM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('BOMBEOS MARBELLA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('BOMBEOS MARBELLA'));

-- CALDERON Y RAMOS (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CALDERON Y RAMOS', 'RECHAZADA', 'CALDERON Y RAMOS', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CALDERON Y RAMOS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CALDERON Y RAMOS'));

-- CAMPEZO OBRAS Y SERVICIOS (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CAMPEZO OBRAS Y SERVICIOS', 'RECHAZADA', 'CAMPEZO OBRAS Y SERVICIOS', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CAMPEZO OBRAS Y SERVICIOS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CAMPEZO OBRAS Y SERVICIOS'));

-- CARAVANAS ALQUILER LIBERTY ROAD (LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CARAVANAS ALQUILER LIBERTY ROAD', 'RECHAZADA', 'CARAVANAS ALQUILER LIBERTY ROAD', 'B97857056', 'LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CARAVANAS ALQUILER LIBERTY ROAD')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CARAVANAS ALQUILER LIBERTY ROAD'));

-- CARMOMATRANS  LOGISTICA V JORGE (FLOTA PREMIUM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CARMOMATRANS  LOGISTICA V JORGE', 'RECHAZADA', 'CARMOMATRANS  LOGISTICA V JORGE', '', 'FLOTA PREMIUM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CARMOMATRANS  LOGISTICA V JORGE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CARMOMATRANS  LOGISTICA V JORGE'));

-- CIRAC LOGISTICA (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CIRAC LOGISTICA', 'RECHAZADA', 'CIRAC LOGISTICA', 'B99125429', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CIRAC LOGISTICA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CIRAC LOGISTICA'));

-- COEXA (PERIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'COEXA', 'RECHAZADA', 'COEXA', 'B57955171', 'PERIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('COEXA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('COEXA'));

-- Comercial Avícola Porcina SA (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Comercial Avícola Porcina SA', 'RECHAZADA', 'Comercial Avícola Porcina SA', 'B47035613', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Comercial Avícola Porcina SA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Comercial Avícola Porcina SA'));

-- COMPAÑÍA EUROPEA DE VIAJEROS (VIDA SR)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'COMPAÑÍA EUROPEA DE VIAJEROS', 'RECHAZADA', 'COMPAÑÍA EUROPEA DE VIAJEROS', '', 'VIDA SR', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('COMPAÑÍA EUROPEA DE VIAJEROS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('COMPAÑÍA EUROPEA DE VIAJEROS'));

-- CONSTRUCCIONES SABATER (MARIMON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CONSTRUCCIONES SABATER', 'RECHAZADA', 'CONSTRUCCIONES SABATER', 'A08578395', 'MARIMON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CONSTRUCCIONES SABATER')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CONSTRUCCIONES SABATER'));

-- COOPERATIVA AGRARIA SAN ISIDRO (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'COOPERATIVA AGRARIA SAN ISIDRO', 'RECHAZADA', 'COOPERATIVA AGRARIA SAN ISIDRO', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('COOPERATIVA AGRARIA SAN ISIDRO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('COOPERATIVA AGRARIA SAN ISIDRO'));

-- DELIKIA AON (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'DELIKIA AON', 'RECHAZADA', 'DELIKIA AON', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('DELIKIA AON')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('DELIKIA AON'));

-- DIPRIMSA (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'DIPRIMSA', 'RECHAZADA', 'DIPRIMSA', '', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('DIPRIMSA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('DIPRIMSA'));

-- DISBASE (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'DISBASE', 'RECHAZADA', 'DISBASE', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('DISBASE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('DISBASE'));

-- DURAN GARRABE (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'DURAN GARRABE', 'RECHAZADA', 'DURAN GARRABE', 'B6238797E', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('DURAN GARRABE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('DURAN GARRABE'));

-- EL MOSCA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'EL MOSCA', 'RECHAZADA', 'EL MOSCA', 'A58662081', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('EL MOSCA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('EL MOSCA'));

-- ETG CIMENTACIONES (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ETG CIMENTACIONES', 'RECHAZADA', 'ETG CIMENTACIONES', '14199453B', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ETG CIMENTACIONES')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ETG CIMENTACIONES'));

-- EUROLOGIN EXPRESS (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'EUROLOGIN EXPRESS', 'RECHAZADA', 'EUROLOGIN EXPRESS', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('EUROLOGIN EXPRESS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('EUROLOGIN EXPRESS'));

-- EXCAVACIONES Y TRANSPORTES MOVITEXGA (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'EXCAVACIONES Y TRANSPORTES MOVITEXGA', 'RECHAZADA', 'EXCAVACIONES Y TRANSPORTES MOVITEXGA', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('EXCAVACIONES Y TRANSPORTES MOVITEXGA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('EXCAVACIONES Y TRANSPORTES MOVITEXGA'));

-- FERMALUX S.L (PEMIUM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FERMALUX S.L', 'RECHAZADA', 'FERMALUX S.L', 'B83915470', 'PEMIUM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FERMALUX S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FERMALUX S.L'));

-- FERROVIAL (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FERROVIAL', 'RECHAZADA', 'FERROVIAL', 'W0265643G', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FERROVIAL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FERROVIAL'));

-- FESARU 2010 (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FESARU 2010', 'RECHAZADA', 'FESARU 2010', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FESARU 2010')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FESARU 2010'));

-- fibratel UNOCORRE (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'fibratel UNOCORRE', 'RECHAZADA', 'fibratel UNOCORRE', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('fibratel UNOCORRE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('fibratel UNOCORRE'));

-- FIRA CIRCUITS SL (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FIRA CIRCUITS SL', 'RECHAZADA', 'FIRA CIRCUITS SL', 'B16391484', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FIRA CIRCUITS SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FIRA CIRCUITS SL'));

-- FLOTA LIÑAGAR (COBIAN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FLOTA LIÑAGAR', 'RECHAZADA', 'FLOTA LIÑAGAR', '', 'COBIAN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FLOTA LIÑAGAR')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FLOTA LIÑAGAR'));

-- FLOTA NUTRAVE (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FLOTA NUTRAVE', 'RECHAZADA', 'FLOTA NUTRAVE', 'A45506854', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FLOTA NUTRAVE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FLOTA NUTRAVE'));

-- FLOTA PROSEÑAL (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FLOTA PROSEÑAL', 'RECHAZADA', 'FLOTA PROSEÑAL', '', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FLOTA PROSEÑAL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FLOTA PROSEÑAL'));

-- FLOTA RICARDO FUENTES E HIJOS (IURISBROKER)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FLOTA RICARDO FUENTES E HIJOS', 'RECHAZADA', 'FLOTA RICARDO FUENTES E HIJOS', '', 'IURISBROKER', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FLOTA RICARDO FUENTES E HIJOS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FLOTA RICARDO FUENTES E HIJOS'));

-- FLOTA TRANJOFE Y TEM (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FLOTA TRANJOFE Y TEM', 'RECHAZADA', 'FLOTA TRANJOFE Y TEM', 'B73045262', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FLOTA TRANJOFE Y TEM')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FLOTA TRANJOFE Y TEM'));

-- FLOTA TRANSRIBAL, SL (CALABUIG)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FLOTA TRANSRIBAL, SL', 'RECHAZADA', 'FLOTA TRANSRIBAL, SL', 'B12979878', 'CALABUIG', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FLOTA TRANSRIBAL, SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FLOTA TRANSRIBAL, SL'));

-- FORESTAL SOLIVA (PIQUÉ)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FORESTAL SOLIVA', 'RECHAZADA', 'FORESTAL SOLIVA', '', 'PIQUÉ', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FORESTAL SOLIVA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FORESTAL SOLIVA'));

-- FORZA HORMIGONES (MONTAGUT)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FORZA HORMIGONES', 'RECHAZADA', 'FORZA HORMIGONES', '', 'MONTAGUT', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FORZA HORMIGONES')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FORZA HORMIGONES'));

-- FRAIKIN (AQUASERVICE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FRAIKIN', 'RECHAZADA', 'FRAIKIN', 'W0017646A', 'AQUASERVICE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FRAIKIN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FRAIKIN'));

-- FRIO ALVAREZ SANCHEZ (LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FRIO ALVAREZ SANCHEZ', 'RECHAZADA', 'FRIO ALVAREZ SANCHEZ', '', 'LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FRIO ALVAREZ SANCHEZ')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FRIO ALVAREZ SANCHEZ'));

-- GAMBIN CANARIAS (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GAMBIN CANARIAS', 'RECHAZADA', 'GAMBIN CANARIAS', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GAMBIN CANARIAS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GAMBIN CANARIAS'));

-- GARCIA Y ATOCHA (PLATINUM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GARCIA Y ATOCHA', 'RECHAZADA', 'GARCIA Y ATOCHA', '', 'PLATINUM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GARCIA Y ATOCHA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GARCIA Y ATOCHA'));

-- GLASS LOGISTIC VLC SL (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GLASS LOGISTIC VLC SL', 'RECHAZADA', 'GLASS LOGISTIC VLC SL', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GLASS LOGISTIC VLC SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GLASS LOGISTIC VLC SL'));

-- GLOBAL SALCAI UTINSA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GLOBAL SALCAI UTINSA', 'RECHAZADA', 'GLOBAL SALCAI UTINSA', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GLOBAL SALCAI UTINSA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GLOBAL SALCAI UTINSA'));

-- GLOBALIA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GLOBALIA', 'RECHAZADA', 'GLOBALIA', 'A07129430', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GLOBALIA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GLOBALIA'));

-- GOCON - VIDA SR - MIGUEL 2026 (GOCON S.L. - VIDA SR)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GOCON - VIDA SR - MIGUEL 2026', 'RECHAZADA', 'GOCON - VIDA SR - MIGUEL 2026', '', 'GOCON S.L. - VIDA SR', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GOCON - VIDA SR - MIGUEL 2026')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GOCON - VIDA SR - MIGUEL 2026'));

-- GOCON SL - 2025 (GOCON S.L. - VIDA SR)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GOCON SL - 2025', 'RECHAZADA', 'GOCON SL - 2025', '', 'GOCON S.L. - VIDA SR', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GOCON SL - 2025')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GOCON SL - 2025'));

-- GOYBER GRUPO LOGISTICO (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GOYBER GRUPO LOGISTICO', 'RECHAZADA', 'GOYBER GRUPO LOGISTICO', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GOYBER GRUPO LOGISTICO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GOYBER GRUPO LOGISTICO'));

-- GRUPIVAZGLE AUTO RENTING (LUGO) AON (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPIVAZGLE AUTO RENTING (LUGO) AON', 'RECHAZADA', 'GRUPIVAZGLE AUTO RENTING (LUGO) AON', 'B27480581', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPIVAZGLE AUTO RENTING (LUGO) AON')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPIVAZGLE AUTO RENTING (LUGO) AON'));

-- GRUPO BABE (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO BABE', 'RECHAZADA', 'GRUPO BABE', 'B36600245', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO BABE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO BABE'));

-- GRUPO BELZUNCES GESA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO BELZUNCES GESA', 'RECHAZADA', 'GRUPO BELZUNCES GESA', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO BELZUNCES GESA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO BELZUNCES GESA'));

-- GRUPO CAMPAL (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO CAMPAL', 'RECHAZADA', 'GRUPO CAMPAL', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO CAMPAL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO CAMPAL'));

-- GRUPO COREN (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO COREN', 'RECHAZADA', 'GRUPO COREN', 'F32001976', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO COREN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO COREN'));

-- GRUPO DAVILA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO DAVILA', 'RECHAZADA', 'GRUPO DAVILA', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO DAVILA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO DAVILA'));

-- GRUPO KINETICO (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO KINETICO', 'RECHAZADA', 'GRUPO KINETICO', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO KINETICO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO KINETICO'));

-- GRUPO MAHOU (SAN MIGUEL)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO MAHOU', 'RECHAZADA', 'GRUPO MAHOU', '', 'SAN MIGUEL', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO MAHOU')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO MAHOU'));

-- GRUPO MIGUEL RAMON (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO MIGUEL RAMON', 'RECHAZADA', 'GRUPO MIGUEL RAMON', 'B43087998', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO MIGUEL RAMON')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO MIGUEL RAMON'));

-- Grupo Molinero (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Grupo Molinero', 'RECHAZADA', 'Grupo Molinero', 'B21901574', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Grupo Molinero')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Grupo Molinero'));

-- GRUPO SADISA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO SADISA', 'RECHAZADA', 'GRUPO SADISA', 'B39036744', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO SADISA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO SADISA'));

-- GRUPO SERVIMAN (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO SERVIMAN', 'RECHAZADA', 'GRUPO SERVIMAN', 'B73579583', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO SERVIMAN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO SERVIMAN'));

-- GRUPO TOTAL 2000, S.A (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO TOTAL 2000, S.A', 'RECHAZADA', 'GRUPO TOTAL 2000, S.A', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO TOTAL 2000, S.A')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO TOTAL 2000, S.A'));

-- GRUPO (TRANESA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO', 'RECHAZADA', 'GRUPO', '', 'TRANESA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO'));

-- GRUPO5 (CLARIANE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO5', 'RECHAZADA', 'GRUPO5', '', 'CLARIANE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO5')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO5'));

-- HERMANOS MORAN (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'HERMANOS MORAN', 'RECHAZADA', 'HERMANOS MORAN', 'B85668390', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('HERMANOS MORAN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('HERMANOS MORAN'));

-- HIJOS DE MARINO PALOMO (CORREDOR GARCIA OCHOA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'HIJOS DE MARINO PALOMO', 'RECHAZADA', 'HIJOS DE MARINO PALOMO', '', 'CORREDOR GARCIA OCHOA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('HIJOS DE MARINO PALOMO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('HIJOS DE MARINO PALOMO'));

-- ID Energy Group, S.A flota WILLIS (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ID Energy Group, S.A flota WILLIS', 'RECHAZADA', 'ID Energy Group, S.A flota WILLIS', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ID Energy Group, S.A flota WILLIS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ID Energy Group, S.A flota WILLIS'));

-- INDUSTRIAS CARNICAS TELLO (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'INDUSTRIAS CARNICAS TELLO', 'RECHAZADA', 'INDUSTRIAS CARNICAS TELLO', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('INDUSTRIAS CARNICAS TELLO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('INDUSTRIAS CARNICAS TELLO'));

-- ITP (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ITP', 'RECHAZADA', 'ITP', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ITP')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ITP'));

-- JEN CONSTRUCCIONES RENOVABLES (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'JEN CONSTRUCCIONES RENOVABLES', 'RECHAZADA', 'JEN CONSTRUCCIONES RENOVABLES', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('JEN CONSTRUCCIONES RENOVABLES')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('JEN CONSTRUCCIONES RENOVABLES'));

-- Leche Río carretillas (PERIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Leche Río carretillas', 'RECHAZADA', 'Leche Río carretillas', '', 'PERIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Leche Río carretillas')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Leche Río carretillas'));

-- LESMARC DISTRIBUCIONES SL (DELTA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LESMARC DISTRIBUCIONES SL', 'RECHAZADA', 'LESMARC DISTRIBUCIONES SL', '', 'DELTA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LESMARC DISTRIBUCIONES SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LESMARC DISTRIBUCIONES SL'));

-- LOGISTIC RACHEL (SEVERINO)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOGISTIC RACHEL', 'RECHAZADA', 'LOGISTIC RACHEL', '', 'SEVERINO', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LOGISTIC RACHEL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOGISTIC RACHEL'));

-- LOGISTICA TRANSALPYNA (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOGISTICA TRANSALPYNA', 'RECHAZADA', 'LOGISTICA TRANSALPYNA', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LOGISTICA TRANSALPYNA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOGISTICA TRANSALPYNA'));

-- LOGISTICA Y TRANSPORTES LDR (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOGISTICA Y TRANSPORTES LDR', 'RECHAZADA', 'LOGISTICA Y TRANSPORTES LDR', 'B86994159', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LOGISTICA Y TRANSPORTES LDR')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOGISTICA Y TRANSPORTES LDR'));

-- LOGISTICA Y TRANSPORTES LDR S.L (JAVIER)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOGISTICA Y TRANSPORTES LDR S.L', 'RECHAZADA', 'LOGISTICA Y TRANSPORTES LDR S.L', '', 'JAVIER', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LOGISTICA Y TRANSPORTES LDR S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOGISTICA Y TRANSPORTES LDR S.L'));

-- LOPEZ ASISTENCIA (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOPEZ ASISTENCIA', 'RECHAZADA', 'LOPEZ ASISTENCIA', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LOPEZ ASISTENCIA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOPEZ ASISTENCIA'));

-- LOTRANS SL (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOTRANS SL', 'RECHAZADA', 'LOTRANS SL', 'B60568730', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LOTRANS SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOTRANS SL'));

-- MARIN GIMENEZ HERMANOS, S.A (FLOTA  WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'MARIN GIMENEZ HERMANOS, S.A', 'RECHAZADA', 'MARIN GIMENEZ HERMANOS, S.A', '', 'FLOTA  WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('MARIN GIMENEZ HERMANOS, S.A')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('MARIN GIMENEZ HERMANOS, S.A'));

-- MIGUEL FERNANDEZ DEL ESTAL (P.LIDER)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'MIGUEL FERNANDEZ DEL ESTAL', 'RECHAZADA', 'MIGUEL FERNANDEZ DEL ESTAL', '', 'P.LIDER', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('MIGUEL FERNANDEZ DEL ESTAL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('MIGUEL FERNANDEZ DEL ESTAL'));

-- MONEGAS SA (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'MONEGAS SA', 'RECHAZADA', 'MONEGAS SA', 'A16015364', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('MONEGAS SA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('MONEGAS SA'));

-- NAVARRO HERMANOS, AON (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'NAVARRO HERMANOS, AON', 'RECHAZADA', 'NAVARRO HERMANOS, AON', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('NAVARRO HERMANOS, AON')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('NAVARRO HERMANOS, AON'));

-- NAVILAND CARGO ESPAGNE (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'NAVILAND CARGO ESPAGNE', 'RECHAZADA', 'NAVILAND CARGO ESPAGNE', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('NAVILAND CARGO ESPAGNE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('NAVILAND CARGO ESPAGNE'));

-- Newport logisctics and trading 2018 (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Newport logisctics and trading 2018', 'RECHAZADA', 'Newport logisctics and trading 2018', 'B67282483', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Newport logisctics and trading 2018')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Newport logisctics and trading 2018'));

-- OCON (WILIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'OCON', 'RECHAZADA', 'OCON', 'B26303586', 'WILIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('OCON')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('OCON'));

-- ONSELLA GLOBAL SERVICES (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ONSELLA GLOBAL SERVICES', 'RECHAZADA', 'ONSELLA GLOBAL SERVICES', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ONSELLA GLOBAL SERVICES')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ONSELLA GLOBAL SERVICES'));

-- OSGA, S.L (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'OSGA, S.L', 'RECHAZADA', 'OSGA, S.L', 'B26266395', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('OSGA, S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('OSGA, S.L'));

-- P&O (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'P&O', 'RECHAZADA', 'P&O', 'A48059083', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('P&O')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('P&O'));

-- PREZERO (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'PREZERO', 'RECHAZADA', 'PREZERO', 'A82741067', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('PREZERO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('PREZERO'));

-- PRIMAVIA EUROPE SL (GESA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'PRIMAVIA EUROPE SL', 'RECHAZADA', 'PRIMAVIA EUROPE SL', '', 'GESA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('PRIMAVIA EUROPE SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('PRIMAVIA EUROPE SL'));

-- RECAMBIOS COLON CATARROJA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'RECAMBIOS COLON CATARROJA', 'RECHAZADA', 'RECAMBIOS COLON CATARROJA', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('RECAMBIOS COLON CATARROJA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('RECAMBIOS COLON CATARROJA'));

-- RECOLLIDES SELECTIVES JOFER,SL (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'RECOLLIDES SELECTIVES JOFER,SL', 'RECHAZADA', 'RECOLLIDES SELECTIVES JOFER,SL', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('RECOLLIDES SELECTIVES JOFER,SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('RECOLLIDES SELECTIVES JOFER,SL'));

-- RED BULL (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'RED BULL', 'RECHAZADA', 'RED BULL', 'B62776216', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('RED BULL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('RED BULL'));

-- REMEDIOS TORRES SL (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'REMEDIOS TORRES SL', 'RECHAZADA', 'REMEDIOS TORRES SL', 'D66148212', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('REMEDIOS TORRES SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('REMEDIOS TORRES SL'));

-- SAMAT ESPAÑA SA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SAMAT ESPAÑA SA', 'RECHAZADA', 'SAMAT ESPAÑA SA', 'A58771973', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SAMAT ESPAÑA SA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SAMAT ESPAÑA SA'));

-- SCHAEFFLER IBERIA (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SCHAEFFLER IBERIA', 'RECHAZADA', 'SCHAEFFLER IBERIA', '', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SCHAEFFLER IBERIA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SCHAEFFLER IBERIA'));

-- SERTRANS (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SERTRANS', 'RECHAZADA', 'SERTRANS', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SERTRANS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SERTRANS'));

-- TAE TRANSPORTS I SERVEIS INTEGRALS (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TAE TRANSPORTS I SERVEIS INTEGRALS', 'RECHAZADA', 'TAE TRANSPORTS I SERVEIS INTEGRALS', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TAE TRANSPORTS I SERVEIS INTEGRALS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TAE TRANSPORTS I SERVEIS INTEGRALS'));

-- TECNICAS Y TRABAJOS FORESTALES  DOMINGUEZ (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TECNICAS Y TRABAJOS FORESTALES  DOMINGUEZ', 'RECHAZADA', 'TECNICAS Y TRABAJOS FORESTALES  DOMINGUEZ', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TECNICAS Y TRABAJOS FORESTALES  DOMINGUEZ')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TECNICAS Y TRABAJOS FORESTALES  DOMINGUEZ'));

-- TECNO SEGURETAT ANOIA (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TECNO SEGURETAT ANOIA', 'RECHAZADA', 'TECNO SEGURETAT ANOIA', '', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TECNO SEGURETAT ANOIA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TECNO SEGURETAT ANOIA'));

-- TECNOMATIC CATALUNYA (PIQUÉ)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TECNOMATIC CATALUNYA', 'RECHAZADA', 'TECNOMATIC CATALUNYA', '', 'PIQUÉ', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TECNOMATIC CATALUNYA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TECNOMATIC CATALUNYA'));

-- TECNOVE PIQUE (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TECNOVE PIQUE', 'RECHAZADA', 'TECNOVE PIQUE', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TECNOVE PIQUE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TECNOVE PIQUE'));

-- TECOZAN (TECOZAN - IURISBROKER)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TECOZAN', 'RECHAZADA', 'TECOZAN', '', 'TECOZAN - IURISBROKER', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TECOZAN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TECOZAN'));

-- TIP S.A INT. PIPA (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TIP S.A INT. PIPA', 'RECHAZADA', 'TIP S.A INT. PIPA', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TIP S.A INT. PIPA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TIP S.A INT. PIPA'));

-- TIRME (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TIRME', 'RECHAZADA', 'TIRME', 'A07326473', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TIRME')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TIRME'));

-- TORRES SERVICIOS TECNICOS (MARIMON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TORRES SERVICIOS TECNICOS', 'RECHAZADA', 'TORRES SERVICIOS TECNICOS', '', 'MARIMON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TORRES SERVICIOS TECNICOS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TORRES SERVICIOS TECNICOS'));

-- TRANJOFE Y TEM (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANJOFE Y TEM', 'RECHAZADA', 'TRANJOFE Y TEM', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANJOFE Y TEM')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANJOFE Y TEM'));

-- transportes bernadet 2026-pique (TRANPORTES BERNADET)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'transportes bernadet 2026-pique', 'RECHAZADA', 'transportes bernadet 2026-pique', '69352113F', 'TRANPORTES BERNADET', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('transportes bernadet 2026-pique')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('transportes bernadet 2026-pique'));

-- TRANSPORTS BERNADET - Piqué (TRANPORTES BERNADET)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTS BERNADET - Piqué', 'RECHAZADA', 'TRANSPORTS BERNADET - Piqué', '', 'TRANPORTES BERNADET', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTS BERNADET - Piqué')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTS BERNADET - Piqué'));

-- TRANSPORTS BERNADET - WILLIS (TRANPORTES BERNADET)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTS BERNADET - WILLIS', 'RECHAZADA', 'TRANSPORTS BERNADET - WILLIS', '', 'TRANPORTES BERNADET', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTS BERNADET - WILLIS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTS BERNADET - WILLIS'));

-- TRANS MORDU (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANS MORDU', 'RECHAZADA', 'TRANS MORDU', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANS MORDU')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANS MORDU'));

-- TRANS SARRIA SL (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANS SARRIA SL', 'RECHAZADA', 'TRANS SARRIA SL', 'B17374836', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANS SARRIA SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANS SARRIA SL'));

-- TRANSANDAMA Y SURIBITRANS (CALABUIG)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSANDAMA Y SURIBITRANS', 'RECHAZADA', 'TRANSANDAMA Y SURIBITRANS', '', 'CALABUIG', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSANDAMA Y SURIBITRANS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSANDAMA Y SURIBITRANS'));

-- TRANSCUÑA (PEDRO MARTINEZ DE QUEL)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSCUÑA', 'RECHAZADA', 'TRANSCUÑA', '', 'PEDRO MARTINEZ DE QUEL', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSCUÑA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSCUÑA'));

-- TRANSOLVER FINANCE (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSOLVER FINANCE', 'RECHAZADA', 'TRANSOLVER FINANCE', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSOLVER FINANCE')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSOLVER FINANCE'));

-- TRANSPORT SIMÓN (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORT SIMÓN', 'RECHAZADA', 'TRANSPORT SIMÓN', 'B17033465', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORT SIMÓN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORT SIMÓN'));

-- TRANSPORTES CALLIZO SA (MATA GESTION)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES CALLIZO SA', 'RECHAZADA', 'TRANSPORTES CALLIZO SA', 'A50102516', 'MATA GESTION', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES CALLIZO SA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES CALLIZO SA'));

-- TRANSPORTES ESPECIALES DOBLE A (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES ESPECIALES DOBLE A', 'RECHAZADA', 'TRANSPORTES ESPECIALES DOBLE A', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES ESPECIALES DOBLE A')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES ESPECIALES DOBLE A'));

-- TRANSPORTES HIRUMUGETA (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES HIRUMUGETA', 'RECHAZADA', 'TRANSPORTES HIRUMUGETA', 'B71110571', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES HIRUMUGETA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES HIRUMUGETA'));

-- TRANSPORTES M. A GUTIERREZ (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES M. A GUTIERREZ', 'RECHAZADA', 'TRANSPORTES M. A GUTIERREZ', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES M. A GUTIERREZ')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES M. A GUTIERREZ'));

-- TRANSPORTES MANDIOLA (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES MANDIOLA', 'RECHAZADA', 'TRANSPORTES MANDIOLA', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES MANDIOLA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES MANDIOLA'));

-- TRANSPORTES MARITIMOS ALCUDIA (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES MARITIMOS ALCUDIA', 'RECHAZADA', 'TRANSPORTES MARITIMOS ALCUDIA', '', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES MARITIMOS ALCUDIA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES MARITIMOS ALCUDIA'));

-- TRANSPORTES OLIVERA (LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES OLIVERA', 'RECHAZADA', 'TRANSPORTES OLIVERA', '', 'LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES OLIVERA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES OLIVERA'));

-- TRANSPORTES VARELA (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES VARELA', 'RECHAZADA', 'TRANSPORTES VARELA', '', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES VARELA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES VARELA'));

-- TRANSPORTES Y LOGISTICA AVANZADA S.L (ASSEGURA CORREDURÍA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES Y LOGISTICA AVANZADA S.L', 'RECHAZADA', 'TRANSPORTES Y LOGISTICA AVANZADA S.L', '', 'ASSEGURA CORREDURÍA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES Y LOGISTICA AVANZADA S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES Y LOGISTICA AVANZADA S.L'));

-- TRANSTECO (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSTECO', 'RECHAZADA', 'TRANSTECO', 'F39957089', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSTECO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSTECO'));

-- AON 11-2025 (TRANSVASA-GARVASA - WILLIS - AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AON 11-2025', 'RECHAZADA', 'AON 11-2025', '', 'TRANSVASA-GARVASA - WILLIS - AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AON 11-2025')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AON 11-2025'));

-- WILLIS 03-2025 (TRANSVASA-GARVASA - WILLIS - AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'WILLIS 03-2025', 'RECHAZADA', 'WILLIS 03-2025', 'A39020805', 'TRANSVASA-GARVASA - WILLIS - AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('WILLIS 03-2025')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('WILLIS 03-2025'));

-- TRUCK & WHEEL (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRUCK & WHEEL', 'RECHAZADA', 'TRUCK & WHEEL', 'B31619570', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRUCK & WHEEL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRUCK & WHEEL'));

-- VICO DE LA DUEÑA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'VICO DE LA DUEÑA', 'RECHAZADA', 'VICO DE LA DUEÑA', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('VICO DE LA DUEÑA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('VICO DE LA DUEÑA'));

-- VIRTO (AON)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'VIRTO', 'RECHAZADA', 'VIRTO', '', 'AON', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('VIRTO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('VIRTO'));

COMMIT;

-- Verificar resultado:
-- SELECT count(*) FROM flotas_historicas;
-- SELECT nombre, estado, corredor_nombre FROM flotas_historicas ORDER BY nombre LIMIT 20;