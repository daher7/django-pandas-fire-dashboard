
SELECT 
    anio, 
    COUNT(id) AS total_incendios, 
    SUM(superficie) AS superficie_total
FROM incendios
WHERE anio BETWEEN 1968 AND 2020
GROUP BY anio
ORDER BY anio ASC;


/* 1. Tiempo: Evolución anual TOTAL INCENDIOS Y SUPERFICIE QUEMADA POR AÑO */
SELECT 
    anio, 
    COUNT(id) AS total_incendios, 
    SUM(superficie) AS superficie_total
FROM incendios
WHERE anio BETWEEN 1968 AND 2020
GROUP BY anio
ORDER BY anio ASC;


/* Espacio: Top 20 provincias. */
SELECT 	
	sum(superficie) AS superficie_total,
	p.provincia
FROM incendios AS i 
INNER JOIN provincias AS p 
ON i.idprovincia = p.idprovincia 
WHERE i.anio BETWEEN 1968 AND 2020
GROUP BY p.provincia
ORDER BY superficie_total DESC
LIMIT 20;

/* 3. Calendario: Estacionalidad mensual */
SELECT 
	mes,
	count(id) AS incendios_totales,
	sum(superficie) AS superficie_quemada
FROM  incendios 
WHERE anio BETWEEN 1968 AND 2020
GROUP BY mes;

/* 4. Gravedad: Relación Cantidad vs. Tamaño (GIF) */
SELECT 
	count(id) AS incendios_totales,
	sum(superficie) AS superficie_quemada,
	sum(superficie)/count(id) AS superficie_media,
	anio
FROM  incendios 
WHERE anio BETWEEN 1968 AND 2020
GROUP BY anio;

/* 5. Tragedia: Ranking de víctimas mortales */
SELECT i.anio, i.municipio, p.provincia, i.muertos, i.superficie
FROM incendios AS i
INNER JOIN provincias AS p
ON i.idprovincia = p.idprovincia
ORDER BY i.muertos DESC 
LIMIT 10;

/* 6. Origen: Causas y detalles técnicos */
SELECT 
	c.causa,
	count(id) AS incendios_totales,
	sum(superficie)
FROM incendios AS i 
INNER JOIN causas AS c 
ON i.idcausa = c.idcausa
WHERE anio BETWEEN 1968 AND 2020
GROUP BY c.causa;








