-- Tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabla de Libros
CREATE TABLE IF NOT EXISTS libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    categoria_id INT,
    anio_publicacion INT,
    stock_total INT NOT NULL DEFAULT 1,
    stock_disponible INT NOT NULL DEFAULT 1,
    portada_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Tabla de Usuarios 
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(30),
    direccion VARCHAR(255),
    fecha_registro DATE NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Tabla de Préstamos
CREATE TABLE IF NOT EXISTS prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE NULL,
    estado ENUM('ACTIVO', 'DEVUELTO', 'VENCIDO') DEFAULT 'ACTIVO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

--  Tabla de Multas
CREATE TABLE IF NOT EXISTS multas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prestamo_id INT NOT NULL UNIQUE,
    monto DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    dias_retraso INT DEFAULT 0,
    pagada TINYINT(1) DEFAULT 0,
    fecha_generada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- DATOS SEMILLA

INSERT IGNORE INTO categorias (id, nombre, descripcion) VALUES
(1, 'Ficción y Literatura', 'Novelas, clásicos literarios y narrativa general'),
(2, 'Ciencia y Tecnología', 'Libros de informática, programación, ingeniería y ciencia'),
(3, 'Historia y Biografías', 'Eventos históricos, biografías de personajes memorables'),
(4, 'Filosofía y Psicología', 'Pensamiento crítico, mente humana y filosofía clásica'),
(5, 'Desarrollo Personal', 'Liderazgo, productividad y crecimiento profesional');

INSERT IGNORE INTO libros (id, titulo, autor, isbn, categoria_id, anio_publicacion, stock_total, stock_disponible, portada_url) VALUES
(1, 'Cien Años de Soledad', 'Gabriel García Márquez', '978-0307474728', 1, 1967, 5, 4, '/static/img/cien_anos_soledad.jpg'),
(2, 'Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '978-0132350884', 2, 2008, 3, 2, '/static/img/clean_code.jpg'),
(3, 'Don Quijote de la Mancha', 'Miguel de Cervantes', '978-8424115456', 1, 1605, 4, 4, '/static/img/don_quijote.jpg'),
(4, 'Sapiens: De animales a dioses', 'Yuval Noah Harari', '978-8499926223', 3, 2014, 4, 3, '/static/img/sapiens.jpg'),
(5, 'El Pragmatic Programmer', 'Andrew Hunt & David Thomas', '978-0135957059', 2, 2019, 2, 2, '/static/img/pragmatic_programmer.jpg');


INSERT IGNORE INTO usuarios (id, nombre, email, telefono, direccion, fecha_registro, activo) VALUES
(1, 'Carlos Rodas', 'carlos.rodas@email.com.gt', '+502 2456 7890', 'Av. La Reforma 12-01, Zona 10, Guatemala', '2025-01-15', 1),
(2, 'Ana Lucía Morales', 'ana.morales@email.com.gt', '+502 5987 6543', '6ta Avenida 8-45, Zona 1, Guatemala', '2025-02-01', 1),
(3, 'Roberto Fuentes', 'roberto.fuentes@email.com.gt', '+502 4123 9876', 'Calle del Arco #14, Antigua Guatemala, Sacatepéquez', '2025-02-10', 1),
(4, 'Laura Asturias', 'laura.asturias@email.com.gt', '+502 3344 5566', '7ma Calle 4-12, Zona 3, Quetzaltenango', '2025-02-20', 1);


UPDATE usuarios SET nombre = 'Carlos Rodas', email = 'carlos.rodas@email.com.gt', telefono = '+502 2456 7890', direccion = 'Av. La Reforma 12-01, Zona 10, Guatemala' WHERE id = 1;
UPDATE usuarios SET nombre = 'Ana Lucía Morales', email = 'ana.morales@email.com.gt', telefono = '+502 5987 6543', direccion = '6ta Avenida 8-45, Zona 1, Guatemala' WHERE id = 2;
UPDATE usuarios SET nombre = 'Roberto Fuentes', email = 'roberto.fuentes@email.com.gt', telefono = '+502 4123 9876', direccion = 'Calle del Arco #14, Antigua Guatemala, Sacatepéquez' WHERE id = 3;
UPDATE usuarios SET nombre = 'Laura Asturias', email = 'laura.asturias@email.com.gt', telefono = '+502 3344 5566', direccion = '7ma Calle 4-12, Zona 3, Quetzaltenango' WHERE id = 4;

-- Préstamos Iniciales
INSERT IGNORE INTO prestamos (id, libro_id, usuario_id, fecha_prestamo, fecha_devolucion_esperada, fecha_devolucion_real, estado) VALUES
(1, 1, 1, '2026-07-20', '2026-08-03', NULL, 'ACTIVO'),
(2, 2, 2, '2026-07-10', '2026-07-24', NULL, 'VENCIDO'),
(3, 4, 3, '2026-07-01', '2026-07-15', '2026-07-14', 'DEVUELTO');

-- Multa
INSERT IGNORE INTO multas (id, prestamo_id, monto, dias_retraso, pagada) VALUES
(1, 2, 35.00, 7, 0);

UPDATE multas SET monto = 35.00 WHERE id = 1;
