
CREATE DATABASE Trivia; 
use Trivia;

CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    redes VARCHAR(255),
    puntaje INT,
    tiempo_respondido TIME
);

CREATE TABLE Preguntas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL
);

CREATE TABLE RespuestasUsuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    pregunta_id INT,
    respuesta_usuario TEXT,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
    FOREIGN KEY (pregunta_id) REFERENCES Preguntas(id)
);

INSERT INTO preguntas (pregunta, respuesta) VALUES 
('¿En qué año se fundó?', '1983'),
('VERDADERO O FALSO, Éste es el nombre del establecimiento cuando se fundó:', 'Complejo Facultativo de Enseñanza Superior San Francisco de Asis (COFES Sn. FCO De ASIS)'),
('Apellido y Nombre de los fundadores', 'Eduardo, Martin, Roberto'),
('¿En qué año se convierte en a Colegio Nacional?', '22/07/85'),
('¿Cuántos directores tuvo el instituto hasta la fecha', '4'), 
('¿Cuántas Carreras se dictan actualmente en el ISAUI?', '6'),
('¿Cuál fue el primer numero de telefono del Instituto?', '41464'),
('VERDADERO O FALSO, El Workshop es:', 'Una técnica de venta, en el ISAUI los alumnos venden los proyectos trabajados durante el ciclo lectivo en una muestra a fin de año.'),
('¿Qué carrera fue la pionera con los viajes en las materias de prácticas?', 'Tecnico y Guia Superior en Turismo'),
('VERDADERO O FALSO, El edificio a sus comienzos era:', 'Una casa con 3 ambientes que se convirtieron en aulas'),
('¿ISAUI es un Instituto público?', 'Sí'),
('¿A partir de que año la Cooperadora empezó a construir las aulas?', 'A partir de 1986, a razon de una por año'),
('VERDADERO O FALSO, El dinero provenia de:', 'El bono contribucion que abonaban los padres'),
('¿Quién fué el Presidente de la Cooperadora en esos años?', 'Sr. Gatica y posteriormente Sr. Constante Bogado'),
('Quién es la Presideta de la Cooperadora actualmente?', 'Daniela Maschio'),
('¿Cómo se logró la nacionalizaciòn?', 'Mediante la Gestion del diputado de VCP Anselmo Pelaez en la gestion de Leopoldo Bravo En la presidencia de R. Alfonsìn');


ALTER TABLE Usuarios
MODIFY tiempo_respondido FLOAT;

ALTER TABLE Usuarios AUTO_INCREMENT = 1;

UPDATE Preguntas
SET pregunta = '¿Cuál es el nombre del establecimiento cuando se fundó?', respuesta = 'Complejo Facultativo de Enseñanza Superior San Francisco de Asis (COFES Sn. FCO De ASIS)'
WHERE id = 2; -- Reemplaza 1 con el ID de la pregunta que deseas editar

UPDATE Preguntas
SET pregunta = '¿Qué es el Workshop?', respuesta = 'Una técnica de venta, en el ISAUI los alumnos venden los proyectos trabajados durante el ciclo lectivo en una muestra a fin de año.'
WHERE id = 8; -- Reemplaza 1 con el ID de la pregunta que deseas editar

UPDATE Preguntas
SET pregunta = '¿Cómo era el edificio a sus comienzos?', respuesta = 'Una casa con 3 ambientes que se convirtieron en aulas'
WHERE id = 10; -- Reemplaza 1 con el ID de la pregunta que deseas editar

UPDATE Preguntas
SET pregunta = '¿De dónde provenia el dinero?', respuesta = 'El bono contribucion que abonaban los padres'
WHERE id = 13; -- Reemplaza 1 con el ID de la pregunta que deseas editar

UPDATE Preguntas
SET pregunta = '¿Cuántos directores tuvo el instituto hasta la fecha?', respuesta = '4'
WHERE id = 5; -- Reemplaza 1 con el ID de la pregunta que deseas editar

UPDATE Preguntas
SET pregunta = '¿Quién es la Presideta de la Cooperadora actualmente?', respuesta = 'Daniela Maschio'
WHERE id = 15; -- Reemplaza 1 con el ID de la pregunta que deseas editar