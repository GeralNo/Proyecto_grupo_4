create database Librerias;

use Librerias;

CREATE TABLE Estudiante (
    codigoEstudiante INT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion VARCHAR(255)
);

CREATE TABLE Recursos (
    codigoRecurso INT PRIMARY KEY,
    nombre VARCHAR(100),
    estado VARCHAR(50)
);

CREATE TABLE Prestamo (
    codigoPrestamo INT PRIMARY KEY,
    codigoEstudiante INT,
    codigoRecurso INT,
    fechaPrestamo DATE,
    fechaDevolucion DATE,
    estadoPrestamo VARCHAR(50),
    FOREIGN KEY (codigoEstudiante) REFERENCES Estudiante(codigoEstudiante),
    FOREIGN KEY (codigoRecurso) REFERENCES Recursos(codigoRecurso)
);

INSERT INTO Estudiante (codigoEstudiante, nombre, telefono, email, direccion) VALUES
(1012345678, 'María Gómez', '3105678901', 'maria.gomez@email.com', 'Carrera 45 #12-34, Bogotá'),
(1009876543, 'Carlos Rodríguez', '3209876543', 'carlos.rodriguez@email.com', 'Avenida caracas 742, Bogotá'),
(1034567890, 'Laura Fernández', '3006547890', 'laura.fernandez@email.com', 'Calle 56 #78-90, Bogotá'),
(1023456789, 'Pedro Sánchez', '3113456789', 'pedro.sanchez@email.com', 'Transversal 23 #45-67, Bogotá'),
(1045678901, 'Ana Martínez', '3222345678', 'ana.martinez@email.com', 'Diagonal 12 #34-56, Bogotá');

INSERT INTO Recursos (codigoRecurso, nombre, estado) VALUES
(201, 'Aprendiendo Python - Mark Lutz', 'Disponible'),
(202, 'Fundamentos de Bases de Datos - Elmasri & Navathe', 'Disponible'),
(203, 'Inteligencia Artificial: Un Enfoque Moderno - Stuart Russell y Peter Norvig', 'Disponible'),
(204, 'Redes de Computadoras - Andrew S. Tanenbaum', 'Disponible'),
(205, 'Seguridad Informática: Principios y Prácticas - William Stallings', 'Disponible');

CREATE TRIGGER trg_PrestamoRecurso
ON Prestamo
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (
        SELECT 1 FROM Recursos r
        JOIN inserted i ON r.codigoRecurso = i.codigoRecurso
        WHERE r.estado = 'Disponible'
    )
    BEGIN
	 INSERT INTO Prestamo (codigoPrestamo, codigoEstudiante, codigoRecurso, fechaPrestamo, fechaDevolucion, estadoPrestamo)
        SELECT codigoPrestamo, codigoEstudiante, codigoRecurso, fechaPrestamo, fechaDevolucion, estadoPrestamo
        FROM inserted;
		UPDATE Recursos
        SET estado = 'Prestado'
        WHERE codigoRecurso IN (SELECT codigoRecurso FROM inserted);
		END
    ELSE
    BEGIN
	 RAISERROR ('El recurso no está disponible para préstamo.', 16, 1);
    END
END;

INSERT INTO Prestamo (codigoPrestamo, codigoEstudiante, codigoRecurso, fechaPrestamo, fechaDevolucion, estadoPrestamo)
VALUES (1, 1009876543, 202, GETDATE(), DATEADD(DAY, 7, GETDATE()), 'Activo');
