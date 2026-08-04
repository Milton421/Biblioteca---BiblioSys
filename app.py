import os
from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__, template_folder='.')

with app.app_context():
    database.init_db()

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
@app.route('/dashboard')
def index():
    return render_template('index.html', active_section='dashboard')

@app.route('/libros')
def libros_page():
    return render_template('index.html', active_section='libros')

@app.route('/usuarios')
def usuarios_page():
    return render_template('index.html', active_section='usuarios')

@app.route('/prestamos')
def prestamos_page():
    return render_template('index.html', active_section='prestamos')

@app.route('/multas')
def multas_page():
    return render_template('index.html', active_section='multas')


# --- RUTAS DE API RESTFUL ---

# DASHBOARD
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'No se pudo conectar a la base de datos MySQL en XAMPP.'}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM libros")
            total_libros = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM prestamos WHERE estado = 'ACTIVO' OR estado = 'VENCIDO'")
            libros_prestados = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE activo = 1")
            usuarios_activos = cursor.fetchone()['total']

            cursor.execute("SELECT IFNULL(SUM(monto), 0) AS total FROM multas WHERE pagada = 0")
            multas_pendientes = cursor.fetchone()['total']

            cursor.execute("""
                SELECT p.id, l.titulo, u.nombre AS usuario, 
                       CAST(p.fecha_prestamo AS CHAR) AS fecha_prestamo, 
                       p.estado
                FROM prestamos p
                JOIN libros l ON p.libro_id = l.id
                JOIN usuarios u ON p.usuario_id = u.id
                ORDER BY p.id DESC LIMIT 5
            """)
            recientes = cursor.fetchall()

            return jsonify({
                'total_libros': total_libros,
                'libros_prestados': libros_prestados,
                'usuarios_activos': usuarios_activos,
                'multas_pendientes': float(multas_pendientes),
                'recientes': recientes
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

#  CATEGORÍAS
@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión MySQL'}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM categorias ORDER BY nombre ASC")
            categorias = cursor.fetchall()
            return jsonify(categorias)
    finally:
        conn.close()

# LIBROS
@app.route('/api/libros', methods=['GET'])
def get_libros():
    query = request.args.get('q', '').strip()
    categoria_id = request.args.get('categoria', '').strip()

    sql = """
        SELECT l.id, l.titulo, l.autor, l.isbn, l.categoria_id, l.anio_publicacion, 
               l.stock_total, l.stock_disponible, l.portada_url, l.created_at,
               c.nombre AS categoria_nombre
        FROM libros l
        LEFT JOIN categorias c ON l.categoria_id = c.id
        WHERE 1=1
    """
    params = []

    if query:
        sql += " AND (l.titulo LIKE %s OR l.autor LIKE %s OR l.isbn LIKE %s)"
        like_q = f"%{query}%"
        params.extend([like_q, like_q, like_q])

    if categoria_id:
        sql += " AND l.categoria_id = %s"
        params.append(categoria_id)

    sql += " ORDER BY l.id DESC"

    conn = database.get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión MySQL'}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            libros = cursor.fetchall()
            return jsonify(libros)
    finally:
        conn.close()

@app.route('/api/libros/<int:libro_id>', methods=['GET'])
def get_libro_by_id(libro_id):
    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
            libro = cursor.fetchone()
            if not libro:
                return jsonify({'error': 'Libro no encontrado'}), 404
            return jsonify(libro)
    finally:
        conn.close()

@app.route('/api/libros', methods=['POST'])
def add_libro():
    data = request.json
    titulo = data.get('titulo')
    autor = data.get('autor')
    isbn = data.get('isbn')
    categoria_id = data.get('categoria_id') or None
    anio_publicacion = data.get('anio_publicacion') or None
    stock_total = int(data.get('stock_total', 1))
    portada_url = data.get('portada_url') or 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=400&q=80'

    if not titulo or not autor:
        return jsonify({'error': 'Título y autor son obligatorios'}), 400

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO libros (titulo, autor, isbn, categoria_id, anio_publicacion, stock_total, stock_disponible, portada_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (titulo, autor, isbn, categoria_id, anio_publicacion, stock_total, stock_total, portada_url))
            conn.commit()
            return jsonify({'message': 'Libro registrado exitosamente', 'id': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/libros/<int:libro_id>', methods=['PUT'])
def update_libro(libro_id):
    data = request.json
    titulo = data.get('titulo')
    autor = data.get('autor')
    isbn = data.get('isbn')
    categoria_id = data.get('categoria_id') or None
    anio_publicacion = data.get('anio_publicacion') or None
    stock_total = int(data.get('stock_total', 1))
    portada_url = data.get('portada_url')

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT stock_total, stock_disponible FROM libros WHERE id = %s", (libro_id,))
            actual = cursor.fetchone()
            if not actual:
                return jsonify({'error': 'Libro no encontrado'}), 404

            prestados = actual['stock_total'] - actual['stock_disponible']
            nuevo_disponible = stock_total - prestados
            if nuevo_disponible < 0:
                return jsonify({'error': f'No puedes reducir el stock a {stock_total} porque hay {prestados} copias en préstamo activo.'}), 400

            sql = """
                UPDATE libros 
                SET titulo=%s, autor=%s, isbn=%s, categoria_id=%s, anio_publicacion=%s, stock_total=%s, stock_disponible=%s, portada_url=%s
                WHERE id=%s
            """
            cursor.execute(sql, (titulo, autor, isbn, categoria_id, anio_publicacion, stock_total, nuevo_disponible, portada_url, libro_id))
            conn.commit()
            return jsonify({'message': 'Libro actualizado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/libros/<int:libro_id>', methods=['DELETE'])
def delete_libro(libro_id):
    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM libros WHERE id = %s", (libro_id,))
            conn.commit()
            return jsonify({'message': 'Libro eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar el libro porque tiene préstamos asociados.'}), 400
    finally:
        conn.close()

# USUARIOS / SOCIOS
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    query = request.args.get('q', '').strip()
    sql = "SELECT id, nombre, email, telefono, direccion, CAST(fecha_registro AS CHAR) AS fecha_registro, activo FROM usuarios WHERE 1=1"
    params = []

    if query:
        sql += " AND (nombre LIKE %s OR email LIKE %s OR telefono LIKE %s)"
        like_q = f"%{query}%"
        params.extend([like_q, like_q, like_q])

    sql += " ORDER BY id DESC"

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            usuarios = cursor.fetchall()
            return jsonify(usuarios)
    finally:
        conn.close()

@app.route('/api/usuarios', methods=['POST'])
def add_usuario():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    if not nombre or not email:
        return jsonify({'error': 'Nombre y correo son obligatorios'}), 400

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, email, telefono, direccion, fecha_registro) VALUES (%s, %s, %s, %s, CURDATE())"
            cursor.execute(sql, (nombre, email, telefono, direccion))
            conn.commit()
            return jsonify({'message': 'Socio registrado exitosamente', 'id': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': 'El correo ya está registrado'}), 400
    finally:
        conn.close()

@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE usuarios SET nombre=%s, email=%s, telefono=%s, direccion=%s WHERE id=%s"
            cursor.execute(sql, (nombre, email, telefono, direccion, usuario_id))
            conn.commit()
            return jsonify({'message': 'Socio actualizado exitosamente'})
    finally:
        conn.close()

@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            conn.commit()
            return jsonify({'message': 'Socio eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': 'No se puede eliminar el socio porque tiene préstamos asociados.'}), 400
    finally:
        conn.close()

# GESTIÓN DE PRÉSTAMOS 
@app.route('/api/prestamos', methods=['GET'])
def get_prestamos():
    query = request.args.get('q', '').strip()
    estado_filtro = request.args.get('estado', 'ALL')

    sql = """
        SELECT p.id, p.libro_id, p.usuario_id, 
               CAST(p.fecha_prestamo AS CHAR) AS fecha_prestamo, 
               CAST(p.fecha_devolucion_esperada AS CHAR) AS fecha_devolucion_esperada, 
               CAST(p.fecha_devolucion_real AS CHAR) AS fecha_devolucion_real, 
               p.estado,
               l.titulo AS libro_titulo,
               u.nombre AS usuario_nombre
        FROM prestamos p
        JOIN libros l ON p.libro_id = l.id
        JOIN usuarios u ON p.usuario_id = u.id
        WHERE 1=1
    """
    params = []

    if query:
        sql += " AND (u.nombre LIKE %s OR l.titulo LIKE %s)"
        like_q = f"%{query}%"
        params.extend([like_q, like_q])

    if estado_filtro != 'ALL':
        sql += " AND p.estado = %s"
        params.append(estado_filtro)

    sql += " ORDER BY p.id DESC"

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE prestamos 
                SET estado = 'VENCIDO' 
                WHERE estado = 'ACTIVO' AND fecha_devolucion_esperada < CURDATE()
            """)
            conn.commit()

            cursor.execute(sql, params)
            prestamos = cursor.fetchall()
            return jsonify(prestamos)
    finally:
        conn.close()

@app.route('/api/prestamos', methods=['POST'])
def add_prestamo():
    data = request.json
    libro_id = data.get('libro_id')
    usuario_id = data.get('usuario_id')
    dias_prestamo = int(data.get('dias_prestamo', 14))

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT stock_disponible FROM libros WHERE id = %s", (libro_id,))
            libro = cursor.fetchone()
            if not libro or libro['stock_disponible'] <= 0:
                return jsonify({'error': 'El libro no tiene copias disponibles'}), 400

            sql_prestamo = """
                INSERT INTO prestamos (libro_id, usuario_id, fecha_prestamo, fecha_devolucion_esperada, estado)
                VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL %s DAY), 'ACTIVO')
            """
            cursor.execute(sql_prestamo, (libro_id, usuario_id, dias_prestamo))

            cursor.execute("UPDATE libros SET stock_disponible = stock_disponible - 1 WHERE id = %s", (libro_id,))
            conn.commit()
            return jsonify({'message': 'Préstamo registrado exitosamente'}), 201
    finally:
        conn.close()

@app.route('/api/prestamos/<int:prestamo_id>/devolver', methods=['POST'])
def devolver_prestamo(prestamo_id):
    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM prestamos WHERE id = %s", (prestamo_id,))
            prestamo = cursor.fetchone()
            if not prestamo or prestamo['estado'] == 'DEVUELTO':
                return jsonify({'error': 'El préstamo ya fue devuelto o no existe'}), 400

            cursor.execute("""
                UPDATE prestamos 
                SET estado = 'DEVUELTO', fecha_devolucion_real = CURDATE() 
                WHERE id = %s
            """, (prestamo_id,))

            cursor.execute("UPDATE libros SET stock_disponible = stock_disponible + 1 WHERE id = %s", (prestamo['libro_id'],))

            # Calcular multa si se entregó tarde (Q5.00 GTQ por día)
            cursor.execute("SELECT DATEDIFF(CURDATE(), %s) AS dias_retraso", (prestamo['fecha_devolucion_esperada'],))
            res_dias = cursor.fetchone()
            dias_retraso = res_dias['dias_retraso'] if res_dias else 0

            monto_multa = 0.00
            if dias_retraso > 0:
                monto_multa = dias_retraso * 5.00
                cursor.execute("""
                    INSERT INTO multas (prestamo_id, monto, dias_retraso, pagada)
                    VALUES (%s, %s, %s, 0)
                    ON DUPLICATE KEY UPDATE monto = %s, dias_retraso = %s
                """, (prestamo_id, monto_multa, dias_retraso, monto_multa, dias_retraso))

            conn.commit()

            msg = 'Devolución registrada correctamente.'
            if monto_multa > 0:
                msg += f' Se generó una multa por retraso de Q{monto_multa:.2f} GTQ ({dias_retraso} días).'

            return jsonify({'message': msg, 'multa': monto_multa})
    finally:
        conn.close()

# GESTIÓN DE MULTAS 
@app.route('/api/multas', methods=['GET'])
def get_multas():
    query = request.args.get('q', '').strip()
    sql = """
        SELECT m.id, m.prestamo_id, m.monto, m.dias_retraso, m.pagada, m.fecha_generada,
               u.nombre AS usuario_nombre, l.titulo AS libro_titulo
        FROM multas m
        JOIN prestamos p ON m.prestamo_id = p.id
        JOIN usuarios u ON p.usuario_id = u.id
        JOIN libros l ON p.libro_id = l.id
        WHERE 1=1
    """
    params = []

    if query:
        sql += " AND (u.nombre LIKE %s OR l.titulo LIKE %s)"
        like_q = f"%{query}%"
        params.extend([like_q, like_q])

    sql += " ORDER BY m.pagada ASC, m.id DESC"

    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            multas = cursor.fetchall()
            return jsonify(multas)
    finally:
        conn.close()

@app.route('/api/multas/<int:multa_id>/pagar', methods=['POST'])
def pagar_multa(multa_id):
    conn = database.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE multas SET pagada = 1 WHERE id = %s", (multa_id,))
            conn.commit()
            return jsonify({'message': 'Multa marcada como pagada correctamente'})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
