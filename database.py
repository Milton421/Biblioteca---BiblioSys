import os
import pymysql
import pymysql.cursors

def get_db_kwargs(include_db=True):
    host = os.environ.get('DB_HOST', 'localhost')
    port = int(os.environ.get('DB_PORT', 3306))
    user = os.environ.get('DB_USER', 'root')
    password = os.environ.get('DB_PASSWORD', '')
    database_name = os.environ.get('DB_NAME', os.environ.get('DB_DATABASE', 'biblioteca_db'))
    ssl_env = os.environ.get('DB_SSL_MODE', os.environ.get('DB_SSL', '')).lower()

    kwargs = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        'autocommit': True
    }

    if include_db:
        kwargs['database'] = database_name

    if ssl_env in ('true', '1', 'required', 'require') or 'aivencloud.com' in host:
        kwargs['ssl'] = {'ssl': True}

    return kwargs, database_name

def get_server_connection():
    """Conecta al servidor MySQL (sin especificar base de datos) para crearla si no existe."""
    kwargs, _ = get_db_kwargs(include_db=False)
    return pymysql.connect(**kwargs)

def get_db_connection():
    """Obtiene una conexión a la base de datos configurada."""
    kwargs, _ = get_db_kwargs(include_db=True)
    return pymysql.connect(**kwargs)

def init_db():
    """Lee schema.sql e inicializa la base de datos y sus tablas."""
    try:
        kwargs, db_name = get_db_kwargs(include_db=True)

        # Intentar crear la DB si el usuario tiene permisos
        try:
            conn_server = get_server_connection()
            with conn_server.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
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
        print(f"[SUCCESS] Base de datos '{db_name}' inicializada correctamente.")
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
