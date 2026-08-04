
-- Tabla de Categorías
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  Tabla de Libros
CREATE TABLE IF NOT EXISTS libros (
    id SERIAL PRIMARY KEY,
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
);

-- Tabla de Usuarios 
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(30),
    direccion VARCHAR(255),
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  Tabla de Préstamos
CREATE TABLE IF NOT EXISTS prestamos (
    id SERIAL PRIMARY KEY,
    libro_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha_prestamo DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE NULL,
    estado VARCHAR(20) DEFAULT 'ACTIVO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

--  Tabla de Multas
CREATE TABLE IF NOT EXISTS multas (
    id SERIAL PRIMARY KEY,
    prestamo_id INT NOT NULL UNIQUE,
    monto NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    dias_retraso INT DEFAULT 0,
    pagada BOOLEAN DEFAULT FALSE,
    fecha_generada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(id) ON DELETE CASCADE
);


-- DATOS INICIALES 

INSERT INTO categorias (id, nombre, descripcion) VALUES
(1, 'Ficción y Literatura', 'Novelas, clásicos literarios y narrativa general'),
(2, 'Ciencia y Tecnología', 'Libros de informática, programación, ingeniería y ciencia'),
(3, 'Historia y Biografías', 'Eventos históricos, biografías de personajes memorables'),
(4, 'Filosofía y Psicología', 'Pensamiento crítico, mente humana y filosofía clásica'),
(5, 'Desarrollo Personal', 'Liderazgo, productividad y crecimiento profesional')
ON CONFLICT (id) DO NOTHING;

SELECT setval('categorias_id_seq', (SELECT MAX(id) FROM categorias));

INSERT INTO libros (id, titulo, autor, isbn, categoria_id, anio_publicacion, stock_total, stock_disponible, portada_url) VALUES
(1, 'Cien Años de Soledad', 'Gabriel García Márquez', '978-0307474728', 1, 1967, 5, 4, '/static/img/cien_anos_soledad.jpg'),
(2, 'Clean Code: A Handbook of Agile Software Craftsmanship', 'Robert C. Martin', '978-0132350884', 2, 2008, 3, 2, '/static/img/clean_code.jpg'),
(3, 'Don Quijote de la Mancha', 'Miguel de Cervantes', '978-8424115456', 1, 1605, 4, 4, '/static/img/don_quijote.jpg'),
(4, 'Sapiens: De animales a dioses', 'Yuval Noah Harari', '978-8499926223', 3, 2014, 4, 3, '/static/img/sapiens.jpg'),
(5, 'El Pragmatic Programmer', 'Andrew Hunt & David Thomas', '978-0135957059', 2, 2019, 2, 2, '/static/img/pragmatic_programmer.jpg')
ON CONFLICT (id) DO NOTHING;

SELECT setval('libros_id_seq', (SELECT MAX(id) FROM libros));

INSERT INTO usuarios (id, nombre, email, telefono, direccion, fecha_registro, activo) VALUES
(1, 'Carlos Rodas', 'carlos.rodas@email.com.gt', '+502 2456 7890', 'Av. La Reforma 12-01, Zona 10, Guatemala', '2025-01-15', TRUE),
(2, 'Ana Lucía Morales', 'ana.morales@email.com.gt', '+502 5987 6543', '6ta Avenida 8-45, Zona 1, Guatemala', '2025-02-01', TRUE),
(3, 'Roberto Fuentes', 'roberto.fuentes@email.com.gt', '+502 4123 9876', 'Calle del Arco #14, Antigua Guatemala, Sacatepéquez', '2025-02-10', TRUE),
(4, 'Laura Asturias', 'laura.asturias@email.com.gt', '+502 3344 5566', '7ma Calle 4-12, Zona 3, Quetzaltenango', '2025-02-20', TRUE)
ON CONFLICT (id) DO NOTHING;

SELECT setval('usuarios_id_seq', (SELECT MAX(id) FROM usuarios));

INSERT INTO prestamos (id, libro_id, usuario_id, fecha_prestamo, fecha_devolucion_esperada, fecha_devolucion_real, estado) VALUES
(1, 1, 1, '2026-07-20', '2026-08-03', NULL, 'ACTIVO'),
(2, 2, 2, '2026-07-10', '2026-07-24', NULL, 'VENCIDO'),
(3, 4, 3, '2026-07-01', '2026-07-15', '2026-07-14', 'DEVUELTO')
ON CONFLICT (id) DO NOTHING;

SELECT setval('prestamos_id_seq', (SELECT MAX(id) FROM prestamos));

INSERT INTO multas (id, prestamo_id, monto, dias_retraso, pagada) VALUES
(1, 2, 35.00, 7, FALSE)
ON CONFLICT (id) DO NOTHING;

SELECT setval('multas_id_seq', (SELECT MAX(id) FROM multas));
