-- Vista para el índice
CREATE OR REPLACE VIEW vista_vehiculos AS
SELECT
    v.id,
    v.modelo,
    v.anio,
    v.precio,
    v.tipo,
    v.descripcion,
    m.nombre AS marca,
    u.nombre AS vendedor,
    v.disponible,
    v.fecha_publicacion
FROM vehiculos v
JOIN marcas m ON v.marca_id = m.id
JOIN usuarios u ON v.vendedor_id = u.id;