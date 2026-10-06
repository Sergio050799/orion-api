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
SELECT lower(hex(randomblob(16))), 'FORESTAL SOLIVA', 'RECHAZADA', 'FORESTAL SOLIVA', 'B17656133', 'PIQUÉ', '', datetime('now'), datetime('now')
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
SELECT lower(hex(randomblob(16))), 'GLASS LOGISTIC VLC SL', 'RECHAZADA', 'GLASS LOGISTIC VLC SL', 'B19939222', '', '', datetime('now'), datetime('now')
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
SELECT lower(hex(randomblob(16))), 'PRIMAVIA EUROPE SL', 'RECHAZADA', 'PRIMAVIA EUROPE SL', 'B05503594', 'GESA', '', datetime('now'), datetime('now')
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

-- AGUSTIN TALÓN (SRAGONES)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AGUSTIN TALÓN', 'COTIZADA', 'AGUSTIN TALÓN', '20442166L', 'SRAGONES', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AGUSTIN TALÓN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AGUSTIN TALÓN'));

-- ALQUILER O TRANSPORTES ALCOTRANS (PEDRO MARTÍNEZ DE QUEL)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALQUILER O TRANSPORTES ALCOTRANS', 'COTIZADA', 'ALQUILER O TRANSPORTES ALCOTRANS', '', 'PEDRO MARTÍNEZ DE QUEL', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ALQUILER O TRANSPORTES ALCOTRANS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALQUILER O TRANSPORTES ALCOTRANS'));

-- ANDREU TRUCKS SL (BROKERS 20 MEDITERRANEA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ANDREU TRUCKS SL', 'COTIZADA', 'ANDREU TRUCKS SL', '', 'BROKERS 20 MEDITERRANEA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ANDREU TRUCKS SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ANDREU TRUCKS SL'));

-- ANTA Y JESUS Sl (JAVIER)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ANTA Y JESUS Sl', 'COTIZADA', 'ANTA Y JESUS Sl', 'B49145162', 'JAVIER', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ANTA Y JESUS Sl')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ANTA Y JESUS Sl'));

-- ARIDOS BOFILL (ROIG)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ARIDOS BOFILL', 'COTIZADA', 'ARIDOS BOFILL', '', 'ROIG', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ARIDOS BOFILL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ARIDOS BOFILL'));

-- ARIDOS HNOS CURANTA (PALOL QUER)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ARIDOS HNOS CURANTA', 'COTIZADA', 'ARIDOS HNOS CURANTA', '', 'PALOL QUER', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ARIDOS HNOS CURANTA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ARIDOS HNOS CURANTA'));

-- ATALAYAS PORT, S (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ATALAYAS PORT, S', 'COTIZADA', 'ATALAYAS PORT, S', 'B54768502', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ATALAYAS PORT, S')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ATALAYAS PORT, S'));

-- CHICARRO TRANSPORTES SL (ERSM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CHICARRO TRANSPORTES SL', 'COTIZADA', 'CHICARRO TRANSPORTES SL', '', 'ERSM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CHICARRO TRANSPORTES SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CHICARRO TRANSPORTES SL'));

-- CITROGEST (MOCHOLI)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CITROGEST', 'COTIZADA', 'CITROGEST', '', 'MOCHOLI', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CITROGEST')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CITROGEST'));

-- COMERCIAL BI (BAT)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'COMERCIAL BI', 'COTIZADA', 'COMERCIAL BI', '', 'BAT', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('COMERCIAL BI')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('COMERCIAL BI'));

-- CONGELATS SALMA (PIQUÉ)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CONGELATS SALMA', 'COTIZADA', 'CONGELATS SALMA', '', 'PIQUÉ', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CONGELATS SALMA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CONGELATS SALMA'));

-- CONSTRUCCIONES MATESANZ SANZ (PMQ (SORIA))
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CONSTRUCCIONES MATESANZ SANZ', 'COTIZADA', 'CONSTRUCCIONES MATESANZ SANZ', '', 'PMQ (SORIA)', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CONSTRUCCIONES MATESANZ SANZ')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CONSTRUCCIONES MATESANZ SANZ'));

-- El cafetero 0 (MOLIMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'El cafetero 0', 'COTIZADA', 'El cafetero 0', '', 'MOLIMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('El cafetero 0')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('El cafetero 0'));

-- FELIX BUQUERIN SL (ROBERTO)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FELIX BUQUERIN SL', 'COTIZADA', 'FELIX BUQUERIN SL', '', 'ROBERTO', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FELIX BUQUERIN SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FELIX BUQUERIN SL'));

-- G.S.L (GESTION SERVICIOS LOGISTICOS SILLA SL)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'G.S.L', 'COTIZADA', 'G.S.L', '', 'GESTION SERVICIOS LOGISTICOS SILLA SL', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('G.S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('G.S.L'));

-- GOHERTRANS LOGISTICA SL (ARAGONES & CEMBORAIN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GOHERTRANS LOGISTICA SL', 'COTIZADA', 'GOHERTRANS LOGISTICA SL', '', 'ARAGONES & CEMBORAIN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GOHERTRANS LOGISTICA SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GOHERTRANS LOGISTICA SL'));

-- GRUPO LOGISTICA FOREVER (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO LOGISTICA FOREVER', 'COTIZADA', 'GRUPO LOGISTICA FOREVER', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO LOGISTICA FOREVER')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO LOGISTICA FOREVER'));

-- Hermanos Hernandez Matas SL (ARAGONES)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Hermanos Hernandez Matas SL', 'COTIZADA', 'Hermanos Hernandez Matas SL', 'B16152175', 'ARAGONES', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Hermanos Hernandez Matas SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Hermanos Hernandez Matas SL'));

-- LOALTRANS (ARAGONES)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LOALTRANS', 'COTIZADA', 'LOALTRANS', 'B73503757', 'ARAGONES', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LOALTRANS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LOALTRANS'));

-- MAGNA STELLA (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'MAGNA STELLA', 'COTIZADA', 'MAGNA STELLA', 'B66919531', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('MAGNA STELLA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('MAGNA STELLA'));

-- O.T TRANSIT QUALITY, S.L (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'O.T TRANSIT QUALITY, S.L', 'COTIZADA', 'O.T TRANSIT QUALITY, S.L', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('O.T TRANSIT QUALITY, S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('O.T TRANSIT QUALITY, S.L'));

-- SARATEKUA (DELTA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SARATEKUA', 'COTIZADA', 'SARATEKUA', '', 'DELTA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SARATEKUA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SARATEKUA'));

-- SERJA (DELTA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SERJA', 'COTIZADA', 'SERJA', 'B31674096', 'DELTA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SERJA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SERJA'));

-- SETOAN LOGISTICA Y TTE. INTERNACIONAL (ROBERTO)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SETOAN LOGISTICA Y TTE. INTERNACIONAL', 'COTIZADA', 'SETOAN LOGISTICA Y TTE. INTERNACIONAL', '', 'ROBERTO', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SETOAN LOGISTICA Y TTE. INTERNACIONAL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SETOAN LOGISTICA Y TTE. INTERNACIONAL'));

-- TOY CENTRE-VEHICULOS INDUSTRIALES- ENRIC (TOY CENTRE - ENRIC - FECHAS VARIAS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TOY CENTRE-VEHICULOS INDUSTRIALES- ENRIC', 'COTIZADA', 'TOY CENTRE-VEHICULOS INDUSTRIALES- ENRIC', '', 'TOY CENTRE - ENRIC - FECHAS VARIAS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TOY CENTRE-VEHICULOS INDUSTRIALES- ENRIC')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TOY CENTRE-VEHICULOS INDUSTRIALES- ENRIC'));

-- TOYS CENTRE - PIQUE - ENRIC (TOY CENTRE - ENRIC - FECHAS VARIAS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TOYS CENTRE - PIQUE - ENRIC', 'COTIZADA', 'TOYS CENTRE - PIQUE - ENRIC', '', 'TOY CENTRE - ENRIC - FECHAS VARIAS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TOYS CENTRE - PIQUE - ENRIC')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TOYS CENTRE - PIQUE - ENRIC'));

-- TRANSELEZ (JAVIER)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSELEZ', 'COTIZADA', 'TRANSELEZ', 'B45867751', 'JAVIER', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSELEZ')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSELEZ'));

-- TRANSMONTENEGRO (LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSMONTENEGRO', 'COTIZADA', 'TRANSMONTENEGRO', 'B13243472', 'LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSMONTENEGRO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSMONTENEGRO'));

-- TRANSMONTENEGRO SL (LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSMONTENEGRO SL', 'COTIZADA', 'TRANSMONTENEGRO SL', '', 'LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSMONTENEGRO SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSMONTENEGRO SL'));

-- TRANSPORTES DE CEREALES Y LEÑA (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES DE CEREALES Y LEÑA', 'COTIZADA', 'TRANSPORTES DE CEREALES Y LEÑA', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES DE CEREALES Y LEÑA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES DE CEREALES Y LEÑA'));

-- TRANSPORTES P. SARASA (ROBERTO)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES P. SARASA', 'COTIZADA', 'TRANSPORTES P. SARASA', 'B22279251', 'ROBERTO', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES P. SARASA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES P. SARASA'));

-- TRANSPORTES J.GAMIZ-OMEGAURBATRA-MARES-GOYO (TTE.S.J.GAMIZ-GOYO-MARES)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES J.GAMIZ-OMEGAURBATRA-MARES-GOYO', 'COTIZADA', 'TRANSPORTES J.GAMIZ-OMEGAURBATRA-MARES-GOYO', '', 'TTE.S.J.GAMIZ-GOYO-MARES', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES J.GAMIZ-OMEGAURBATRA-MARES-GOYO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES J.GAMIZ-OMEGAURBATRA-MARES-GOYO'));

-- TTES. PATRICIO (GADA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TTES. PATRICIO', 'COTIZADA', 'TTES. PATRICIO', 'B78915287', 'GADA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TTES. PATRICIO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TTES. PATRICIO'));

-- WITTMANN TECHNOLOGY SPAIN (PIQUE)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'WITTMANN TECHNOLOGY SPAIN', 'COTIZADA', 'WITTMANN TECHNOLOGY SPAIN', '', 'PIQUE', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('WITTMANN TECHNOLOGY SPAIN')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('WITTMANN TECHNOLOGY SPAIN'));

-- ABONOS Y SEMILLAS SA (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ABONOS Y SEMILLAS SA', 'EN ESTUDIO', 'ABONOS Y SEMILLAS SA', 'A09307935', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ABONOS Y SEMILLAS SA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ABONOS Y SEMILLAS SA'));

-- AFANDECOR, AFANMONTAJES Y APLOMO (ALCOSEGUR)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AFANDECOR, AFANMONTAJES Y APLOMO', 'EN ESTUDIO', 'AFANDECOR, AFANMONTAJES Y APLOMO', '', 'ALCOSEGUR', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AFANDECOR, AFANMONTAJES Y APLOMO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AFANDECOR, AFANMONTAJES Y APLOMO'));

-- ALTIPLANO TRANS (ASMEVAL)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ALTIPLANO TRANS', 'EN ESTUDIO', 'ALTIPLANO TRANS', '', 'ASMEVAL', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ALTIPLANO TRANS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ALTIPLANO TRANS'));

-- AMURIUZA CUBIERTAS (RICARDO OUTERIÑO)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'AMURIUZA CUBIERTAS', 'EN ESTUDIO', 'AMURIUZA CUBIERTAS', 'B48519425', 'RICARDO OUTERIÑO', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('AMURIUZA CUBIERTAS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('AMURIUZA CUBIERTAS'));

-- ANSAREO AEB (WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'ANSAREO AEB', 'EN ESTUDIO', 'ANSAREO AEB', 'B48619258', 'WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('ANSAREO AEB')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('ANSAREO AEB'));

-- botanicas de levante (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'botanicas de levante', 'EN ESTUDIO', 'botanicas de levante', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('botanicas de levante')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('botanicas de levante'));

-- CABEZOLARI (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CABEZOLARI', 'EN ESTUDIO', 'CABEZOLARI', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CABEZOLARI')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CABEZOLARI'));

-- CAMILO Y DEL ARCO SL (ARAGONES)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CAMILO Y DEL ARCO SL', 'EN ESTUDIO', 'CAMILO Y DEL ARCO SL', 'B87373643', 'ARAGONES', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CAMILO Y DEL ARCO SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CAMILO Y DEL ARCO SL'));

-- CARA Y TTES.DE BURGOS (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CARA Y TTES.DE BURGOS', 'EN ESTUDIO', 'CARA Y TTES.DE BURGOS', 'B09289406', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CARA Y TTES.DE BURGOS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CARA Y TTES.DE BURGOS'));

-- CIRAC LOGÍSTICA (ROBERTO LARREA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CIRAC LOGÍSTICA', 'EN ESTUDIO', 'CIRAC LOGÍSTICA', '', 'ROBERTO LARREA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CIRAC LOGÍSTICA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CIRAC LOGÍSTICA'));

-- cis flota agustin gonzalez (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'cis flota agustin gonzalez', 'EN ESTUDIO', 'cis flota agustin gonzalez', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('cis flota agustin gonzalez')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('cis flota agustin gonzalez'));

-- CONGELATS SALMA, S.L (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CONGELATS SALMA, S.L', 'EN ESTUDIO', 'CONGELATS SALMA, S.L', 'B84167410', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CONGELATS SALMA, S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CONGELATS SALMA, S.L'));

-- CONTENEDORES CALVO VARGAS (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'CONTENEDORES CALVO VARGAS', 'EN ESTUDIO', 'CONTENEDORES CALVO VARGAS', 'B26176354', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('CONTENEDORES CALVO VARGAS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('CONTENEDORES CALVO VARGAS'));

-- FLOTA AFANDECOR, AFANMONTAJES Y APLOMO (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FLOTA AFANDECOR, AFANMONTAJES Y APLOMO', 'EN ESTUDIO', 'FLOTA AFANDECOR, AFANMONTAJES Y APLOMO', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FLOTA AFANDECOR, AFANMONTAJES Y APLOMO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FLOTA AFANDECOR, AFANMONTAJES Y APLOMO'));

-- FRILESA & LEBROK (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'FRILESA & LEBROK', 'EN ESTUDIO', 'FRILESA & LEBROK', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('FRILESA & LEBROK')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('FRILESA & LEBROK'));

-- GARRIGA OBRES I SERVEIS, S.L (MGA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GARRIGA OBRES I SERVEIS, S.L', 'EN ESTUDIO', 'GARRIGA OBRES I SERVEIS, S.L', '', 'MGA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GARRIGA OBRES I SERVEIS, S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GARRIGA OBRES I SERVEIS, S.L'));

-- GESTIÓN DE INFRAESTRUCTURAS CIVILES (MATA GESTIÓN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GESTIÓN DE INFRAESTRUCTURAS CIVILES', 'EN ESTUDIO', 'GESTIÓN DE INFRAESTRUCTURAS CIVILES', 'A99066342', 'MATA GESTIÓN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GESTIÓN DE INFRAESTRUCTURAS CIVILES')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GESTIÓN DE INFRAESTRUCTURAS CIVILES'));

-- GRUPO VIGILANT A30085401 (GESA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'GRUPO VIGILANT A30085401', 'EN ESTUDIO', 'GRUPO VIGILANT A30085401', 'A30085401', 'GESA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('GRUPO VIGILANT A30085401')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('GRUPO VIGILANT A30085401'));

-- hidalgo (ROBERTO)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'hidalgo', 'EN ESTUDIO', 'hidalgo', 'B22248132', 'ROBERTO', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('hidalgo')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('hidalgo'));

-- IDM (PIQUÉ)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'IDM', 'EN ESTUDIO', 'IDM', '', 'PIQUÉ', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('IDM')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('IDM'));

-- JACINTO PEREZ (TRANSPORT & CUSTOMS BULL)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'JACINTO PEREZ', 'EN ESTUDIO', 'JACINTO PEREZ', '', 'TRANSPORT & CUSTOMS BULL', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('JACINTO PEREZ')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('JACINTO PEREZ'));

-- LA ABUELA MARGA (ARAGONES)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'LA ABUELA MARGA', 'EN ESTUDIO', 'LA ABUELA MARGA', 'B45289451', 'ARAGONES', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('LA ABUELA MARGA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('LA ABUELA MARGA'));

-- Nuñez Movilla S.L (KIDEKA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Nuñez Movilla S.L', 'EN ESTUDIO', 'Nuñez Movilla S.L', 'B09259839', 'KIDEKA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Nuñez Movilla S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Nuñez Movilla S.L'));

-- RECUPERACIONES MORALES (PREMIUM)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'RECUPERACIONES MORALES', 'EN ESTUDIO', 'RECUPERACIONES MORALES', 'B84174341', 'PREMIUM', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('RECUPERACIONES MORALES')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('RECUPERACIONES MORALES'));

-- REHABILITACIONS PONS (PIQUÉ)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'REHABILITACIONS PONS', 'EN ESTUDIO', 'REHABILITACIONS PONS', '', 'PIQUÉ', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('REHABILITACIONS PONS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('REHABILITACIONS PONS'));

-- Remar (GOYO)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Remar', 'EN ESTUDIO', 'Remar', '', 'GOYO', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Remar')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Remar'));

-- RG ROUTIER EUROPEAN TRANSPORT & LOGISTICS (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'RG ROUTIER EUROPEAN TRANSPORT & LOGISTICS', 'EN ESTUDIO', 'RG ROUTIER EUROPEAN TRANSPORT & LOGISTICS', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('RG ROUTIER EUROPEAN TRANSPORT & LOGISTICS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('RG ROUTIER EUROPEAN TRANSPORT & LOGISTICS'));

-- SANCHEZ VAZQUEZ (COTASEGUR)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SANCHEZ VAZQUEZ', 'EN ESTUDIO', 'SANCHEZ VAZQUEZ', '', 'COTASEGUR', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SANCHEZ VAZQUEZ')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SANCHEZ VAZQUEZ'));

-- SERVICIO DE ALQUILER CAIDERO S.L (ANAGAN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SERVICIO DE ALQUILER CAIDERO S.L', 'EN ESTUDIO', 'SERVICIO DE ALQUILER CAIDERO S.L', '', 'ANAGAN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SERVICIO DE ALQUILER CAIDERO S.L')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SERVICIO DE ALQUILER CAIDERO S.L'));

-- SERVICIOS LOGISTICOS DEL SUR (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'SERVICIOS LOGISTICOS DEL SUR', 'EN ESTUDIO', 'SERVICIOS LOGISTICOS DEL SUR', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('SERVICIOS LOGISTICOS DEL SUR')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('SERVICIOS LOGISTICOS DEL SUR'));

-- Tea Tek en Personal Family Office (PERSONALFAMILY)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'Tea Tek en Personal Family Office', 'EN ESTUDIO', 'Tea Tek en Personal Family Office', '', 'PERSONALFAMILY', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('Tea Tek en Personal Family Office')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('Tea Tek en Personal Family Office'));

-- TRACTOLE,S.A (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRACTOLE,S.A', 'EN ESTUDIO', 'TRACTOLE,S.A', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRACTOLE,S.A')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRACTOLE,S.A'));

-- TRANS JJ JUNDE SL (AENUS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANS JJ JUNDE SL', 'EN ESTUDIO', 'TRANS JJ JUNDE SL', '', 'AENUS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANS JJ JUNDE SL')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANS JJ JUNDE SL'));

-- TRANSPORTE SEGOVIA (TERRANEA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTE SEGOVIA', 'EN ESTUDIO', 'TRANSPORTE SEGOVIA', 'A78394699', 'TERRANEA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTE SEGOVIA')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTE SEGOVIA'));

-- callejero bueno 2025 (TRANSPORTES CALLEJERO BUENO - FLOTA WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'callejero bueno 2025', 'EN ESTUDIO', 'callejero bueno 2025', '', 'TRANSPORTES CALLEJERO BUENO - FLOTA WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('callejero bueno 2025')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('callejero bueno 2025'));

-- callejero bueno 2026 (TRANSPORTES CALLEJERO BUENO - FLOTA WILLIS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'callejero bueno 2026', 'EN ESTUDIO', 'callejero bueno 2026', 'B99479743', 'TRANSPORTES CALLEJERO BUENO - FLOTA WILLIS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('callejero bueno 2026')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('callejero bueno 2026'));

-- TRANSPORTES JABOSIO (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES JABOSIO', 'EN ESTUDIO', 'TRANSPORTES JABOSIO', 'B02239952', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES JABOSIO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES JABOSIO'));

-- TRANSPORTES JACINTO DEL POZO (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES JACINTO DEL POZO', 'EN ESTUDIO', 'TRANSPORTES JACINTO DEL POZO', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES JACINTO DEL POZO')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES JACINTO DEL POZO'));

-- TRANSPORTES MATAS 2016 (MOLYMA)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TRANSPORTES MATAS 2016', 'EN ESTUDIO', 'TRANSPORTES MATAS 2016', '', 'MOLYMA', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TRANSPORTES MATAS 2016')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TRANSPORTES MATAS 2016'));

-- TTES.DELFIN ESPINOSA, S.L + LOGIESBER (sin corredor)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'TTES.DELFIN ESPINOSA, S.L + LOGIESBER', 'EN ESTUDIO', 'TTES.DELFIN ESPINOSA, S.L + LOGIESBER', '', '', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('TTES.DELFIN ESPINOSA, S.L + LOGIESBER')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('TTES.DELFIN ESPINOSA, S.L + LOGIESBER'));

-- UNECOL ADHESIVE IDEAS (MDS)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'UNECOL ADHESIVE IDEAS', 'EN ESTUDIO', 'UNECOL ADHESIVE IDEAS', '', 'MDS', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('UNECOL ADHESIVE IDEAS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('UNECOL ADHESIVE IDEAS'));

-- VIDAL OBRAS Y SERVICIOS (MATA GESTIÓN)
INSERT INTO flotas_historicas (id, nombre, estado, tomador, cif, corredor_nombre, notas, created_at, updated_at)
SELECT lower(hex(randomblob(16))), 'VIDAL OBRAS Y SERVICIOS', 'EN ESTUDIO', 'VIDAL OBRAS Y SERVICIOS', 'A22027890', 'MATA GESTIÓN', '', datetime('now'), datetime('now')
WHERE NOT EXISTS (SELECT 1 FROM carpetas WHERE upper(trim(tomador)) = upper('VIDAL OBRAS Y SERVICIOS')) AND NOT EXISTS (SELECT 1 FROM flotas_historicas WHERE upper(trim(tomador)) = upper('VIDAL OBRAS Y SERVICIOS'));

COMMIT;

-- Verificar resultado:
-- SELECT count(*) FROM flotas_historicas;
-- SELECT nombre, estado, corredor_nombre FROM flotas_historicas ORDER BY nombre LIMIT 20;