import os
import ssl
from urllib.parse import urlparse

# Driver de PostgreSQL en Python Puro (compatible 100% con Vercel sin C-libraries)
IS_PG8000 = False
try:
    import pg8000.dbapi
    IS_PG8000 = True
except ImportError:
    pass

import pymysql
import pymysql.cursors

def is_supabase_enabled():
    """Detecta si la conexión es hacia PostgreSQL / Supabase en Vercel."""
    postgres_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DATABASE_URL')
    postgres_host = os.environ.get('POSTGRES_HOST') or os.environ.get('DB_HOST', '')
    db_type = os.environ.get('DB_TYPE', '').lower()

    if db_type in ('postgres', 'postgresql', 'supabase'):
        return True
    if postgres_url and ('postgres' in postgres_url or 'postgresql' in postgres_url):
        return True
    if 'supabase' in postgres_host or 'postgres' in postgres_host:
        return True

    return False

class Pg8000CursorWrapper:
    """Wrapper para hacer que pg8000 devuelva diccionarios al igual que PyMySQL DictCursor."""
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        query = query.replace('IFNULL(', 'COALESCE(')
        query = query.replace('CAST(p.fecha_prestamo AS CHAR)', 'CAST(p.fecha_prestamo AS VARCHAR)')
        query = query.replace('CAST(fecha_registro AS CHAR)', 'CAST(fecha_registro AS VARCHAR)')
        if params is not None:
            return self.cursor.execute(query, params)
        return self.cursor.execute(query)

    def _to_dict(self, row):
        if row is None or not self.cursor.description:
            return row
        cols = [col[0] for col in self.cursor.description]
        return dict(zip(cols, row))

    def fetchone(self):
        row = self.cursor.fetchone()
        return self._to_dict(row)

    def fetchall(self):
        rows = self.cursor.fetchall()
        if not rows or not self.cursor.description:
            return rows
        cols = [col[0] for col in self.cursor.description]
        return [dict(zip(cols, row)) for row in rows]

    @property
    def lastrowid(self):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()

class Pg8000ConnWrapper:
    """Wrapper de conexión PostgreSQL con pg8000."""
    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return Pg8000CursorWrapper(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

def get_db_connection():
    """Obtiene una conexión a la base de datos (Supabase en Vercel o MySQL)."""
    postgres_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DATABASE_URL')

    if is_supabase_enabled() and IS_PG8000:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        if postgres_url:
            if postgres_url.startswith("postgres://"):
                postgres_url = postgres_url.replace("postgres://", "postgresql://", 1)
            parsed = urlparse(postgres_url)
            conn = pg8000.dbapi.connect(
                user=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port or 5432,
                database=parsed.path.lstrip('/'),
                ssl_context=ssl_ctx
            )
        else:
            conn = pg8000.dbapi.connect(
                host=os.environ.get('POSTGRES_HOST', os.environ.get('DB_HOST', 'localhost')),
                port=int(os.environ.get('POSTGRES_PORT', os.environ.get('DB_PORT', 5432))),
                user=os.environ.get('POSTGRES_USER', os.environ.get('DB_USER', 'postgres')),
                password=os.environ.get('POSTGRES_PASSWORD', os.environ.get('DB_PASSWORD', '')),
                database=os.environ.get('POSTGRES_DATABASE', os.environ.get('DB_NAME', 'postgres')),
                ssl_context=ssl_ctx
            )
        return Pg8000ConnWrapper(conn)

    # De lo contrario, usar PyMySQL (MySQL Local o Aiven)
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
        'database': database_name,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        'autocommit': True
    }

    if ssl_env in ('true', '1', 'required', 'require') or 'aivencloud.com' in host:
        kwargs['ssl'] = {'ssl': True}

    return pymysql.connect(**kwargs)

def init_db():
    """Inicializa la base de datos según el motor configurado."""
    try:
        if is_supabase_enabled() and IS_PG8000:
            conn = get_db_connection()
            schema_path = os.path.join(os.path.dirname(__file__), 'schema_supabase.sql')
            if not os.path.exists(schema_path):
                schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

            with open(schema_path, 'r', encoding='utf-8') as f:
                lines = [line for line in f if not line.strip().startswith('--')]
                sql_script = "\n".join(lines)

            commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
            with conn.cursor() as cursor:
                for command in commands:
                    cursor.execute(command)
            conn.commit()
            conn.close()
            print("[SUCCESS] Base de datos Supabase (PostgreSQL) inicializada correctamente con pg8000.")
            return True
        else:
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
            print("[SUCCESS] Base de datos MySQL inicializada correctamente.")
            return True
    except Exception as e:
        print(f"[NOTE] Inicialización DB omitida o manejada remotamente: {e}")
        return False

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    """Ejecuta una consulta SQL parametrizada."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if commit:
                conn.commit()
                return getattr(cursor, 'lastrowid', None)
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            return True
    finally:
        conn.close()
