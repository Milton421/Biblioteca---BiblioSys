import os
import pymysql
import pymysql.cursors

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', os.environ.get('DB_DATABASE', 'biblioteca_db')),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_server_connection():
    """Conecta al servidor MySQL (sin especificar base de datos) para crearla si no existe."""
    return pymysql.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        charset='utf8mb4',
        autocommit=True
    )

def get_db_connection():
    """Obtiene una conexión a la base de datos configurada."""
    return pymysql.connect(**DB_CONFIG, autocommit=True)

def init_db():
    """Lee schema.sql e inicializa la base de datos y sus tablas."""
    try:
        try:
            conn_server = get_server_connection()
            with conn_server.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn_server.close()
        except Exception:
            pass

        conn = get_db_connection()
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                lines = [line for line in f if not line.strip().startswith('--')]
                sql_script = "\n".join(lines)

            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            with conn.cursor() as cursor:
                for command in commands:
                    cursor.execute(command)
        conn.close()
        print("[SUCCESS] Base de datos 'biblioteca_db' inicializada correctamente.")
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
        return False

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    """Ejecuta una consulta SQL de forma segura utilizando sintaxis parametrizada."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if commit:
                conn.commit()
                return cursor.lastrowid
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            return cursor.rowcount
    finally:
        conn.close()
