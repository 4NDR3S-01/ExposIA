-- Limpiar las tablas antes de insertar para evitar duplicados
DELETE FROM feedback_calificacion;
DELETE FROM detalle_calificacion;
DELETE FROM criterios_evaluacion;
DELETE FROM calificaciones;
DELETE FROM parametros_ideales;
DELETE FROM usuarios;
DELETE FROM grabacion;

-- Usuarios de prueba
INSERT INTO usuarios (id, nombre, correo, password) VALUES
  (1, 'Carlos Chile', 'carlos@demo.com', 'pass123'),
  (2, 'TestUser', 'test@demo.com', 'pass123');

-- Grabaciones de prueba
INSERT INTO grabacion (id) VALUES
  (1), (2);

-- Parametros ideales de prueba
INSERT INTO parametros_ideales (id, claridad_ideal, velocidad_ideal, pausas_ideales, otros_parametros)
VALUES (1, 8.5, 7.0, 6.0, 'nada');

INSERT INTO parametros_ideales (id, claridad_ideal, velocidad_ideal, pausas_ideales, otros_parametros)
VALUES (2, 6.0, 9.0, 3.5, 'ruido de fondo');

-- Calificaciones de prueba (los ids deben existir en usuarios, grabacion y parametros_ideales)
INSERT INTO calificaciones (id, grabacion_id, usuario_id, puntaje_global, observacion_global, tipo_calificacion, fecha, parametros_id) VALUES
  (1, 1, 1, 9.5, 'Buena exposición', 'oral', '2024-06-03 00:00:00', 1),
  (2, 2, 2, 7.2, 'Regular exposición', 'oral', '2024-06-04 00:00:00', 2);

-- Criterios de evaluación de prueba
INSERT INTO criterios_evaluacion (id, nombre, descripcion, peso) VALUES
  (1, 'Claridad', 'Claridad de la exposición', 0.4),
  (2, 'Dominio', 'Dominio del tema', 0.6);

-- Detalle calificación de prueba
INSERT INTO detalle_calificacion (id, calificacion_id, criterio_id, slide_ide, puntaje, comentario, fragmento_audio_id) VALUES
  (1, 1, 1, 1, 9.0, 'Muy claro', 101),
  (2, 1, 2, 2, 10.0, 'Dominio total', 102),
  (3, 2, 1, 1, 7.0, 'Falta claridad', 201),
  (4, 2, 2, 2, 7.5, 'Dominio aceptable', 202);

-- Feedback de prueba
INSERT INTO feedback_calificacion (id, calificacion_id, observacion, fecha, autor) VALUES
  (1, 1, 'Excelente trabajo', '2024-06-03 10:00:00', 'Profesor'),
  (2, 2, 'Mejorar claridad', '2024-06-04 12:00:00', 'Profesor');

-- Ajustar los autoincrementales para evitar conflicto de IDs en tests (H2 y PostgreSQL)
ALTER TABLE usuarios ALTER COLUMN id RESTART WITH 3;
ALTER TABLE grabacion ALTER COLUMN id RESTART WITH 3;
ALTER TABLE parametros_ideales ALTER COLUMN id RESTART WITH 3;
ALTER TABLE calificaciones ALTER COLUMN id RESTART WITH 3;
ALTER TABLE criterios_evaluacion ALTER COLUMN id RESTART WITH 3;
ALTER TABLE detalle_calificacion ALTER COLUMN id RESTART WITH 5;
ALTER TABLE feedback_calificacion ALTER COLUMN id RESTART WITH 3;
