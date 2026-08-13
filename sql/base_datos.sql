-- =============================================================
-- PROYECTO: Reserva de computadores del laboratorio
-- Motor: MySQL 8 o superior
-- Este archivo se puede abrir y ejecutar completo desde DBeaver.
-- =============================================================

CREATE DATABASE IF NOT EXISTS reservas_laboratorio
CHARACTER SET utf8mb4 COLLATE utf8mb4_spanish_ci;

USE reservas_laboratorio;

-- Se eliminan primero las tablas dependientes para poder repetir la instalación.
DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS bloques;
DROP TABLE IF EXISTS computadores;
DROP TABLE IF EXISTS alumnos;

CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    curso VARCHAR(20) NOT NULL
);

CREATE TABLE computadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    ubicacion VARCHAR(50) NOT NULL,
    estado ENUM('DISPONIBLE', 'MANTENCION') NOT NULL DEFAULT 'DISPONIBLE'
);

CREATE TABLE bloques (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    computador_id INT NOT NULL,
    bloque_id INT NOT NULL,
    fecha DATE NOT NULL,
    estado ENUM('ACTIVA', 'CANCELADA') NOT NULL DEFAULT 'ACTIVA',
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reserva_alumno
        FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
    CONSTRAINT fk_reserva_computador
        FOREIGN KEY (computador_id) REFERENCES computadores(id),
    CONSTRAINT fk_reserva_bloque
        FOREIGN KEY (bloque_id) REFERENCES bloques(id)
);

-- Datos pequeños para que la demostración esté lista inmediatamente.
INSERT INTO alumnos (nombre, curso) VALUES
('Camila Soto', '2°A'),
('Diego Muñoz', '2°A'),
('Valentina Rojas', '2°B');

INSERT INTO computadores (codigo, ubicacion, estado) VALUES
('PC-01', 'Laboratorio 1', 'DISPONIBLE'),
('PC-02', 'Laboratorio 1', 'DISPONIBLE'),
('PC-03', 'Laboratorio 1', 'DISPONIBLE'),
('PC-04', 'Laboratorio 1', 'MANTENCION');

INSERT INTO bloques (nombre, hora_inicio, hora_fin) VALUES
('Bloque 1', '08:00:00', '09:30:00'),
('Bloque 2', '09:45:00', '11:15:00'),
('Bloque 3', '11:30:00', '13:00:00');

DROP PROCEDURE IF EXISTS realizar_reserva;

CREATE PROCEDURE realizar_reserva(
    IN p_alumno_id INT,
    IN p_computador_id INT,
    IN p_bloque_id INT,
    IN p_fecha DATE
)
BEGIN
    DECLARE cantidad_reservas INT;

    -- Cuenta las reservas activas del computador
    -- para la misma fecha y bloque.
    SELECT COUNT(*)
    INTO cantidad_reservas
    FROM reservas
    WHERE computador_id = p_computador_id
      AND bloque_id = p_bloque_id
      AND fecha = p_fecha
      AND estado = 'ACTIVA';

    -- Si no existen reservas, se registra una nueva.
    IF cantidad_reservas = 0 THEN

        INSERT INTO reservas (
            alumno_id,
            computador_id,
            bloque_id,
            fecha
        )
        VALUES (
            p_alumno_id,
            p_computador_id,
            p_bloque_id,
            p_fecha
        );

    ELSE

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'El computador ya está reservado en ese bloque';

    END IF;
END;


-- Consulta opcional para revisar las reservas directamente en DBeaver.
SELECT * FROM reservas;
