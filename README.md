# Sistema de Gestión de Biblioteca (BiblioSys)

Un sistema de gestión web integral orientado a la digitalización, control de inventario y automatización de procesos operativos en bibliotecas. Esta aplicación permite administrar catálogos de libros, categorías, registro de usuarios, control de préstamos, devoluciones y seguimiento de penalizaciones por retraso.

---

## Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Características Principales](#características-principales)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Tecnologías Utilizadas](#tecnologías-utilizadas)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Requisitos del Sistema](#requisitos-del-sistema)
7. [Instalación y Configuración Local](#instalación-y-configuración-local)
8. [Gestión de Variables de Entorno y Credenciales](#gestión-de-variables-de-entorno-y-credenciales)
9. [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
10. [Despliegue en Servidor de Producción](#despliegue-en-servidor-de-producción)
11. [Especificación de la API RESTful](#especificación-de-la-api-restful)
12. [Buenas Prácticas e Implementación de Seguridad](#buenas-prácticas-e-implementación-de-seguridad)

---

## Descripción del Proyecto

BiblioSys es una solución de software cliente-servidor construida con una arquitectura orientada a servicios web (REST API) y una interfaz de usuario dinámica de tipo Single Page Application (SPA). Está diseñada para optimizar los flujos de trabajo administrativos de una biblioteca tradicional mediante la automatización del control de existencias, cálculo automático de fechas de vencimiento y seguimiento de cuentas por cobrar asociadas a multas por devolución tardía.

El sistema garantiza la integridad referencial de la información mediante transacciones en la base de datos relacional y proporciona una interfaz limpia, responsiva y accesible para los administradores. Está preparado tanto para entornos de desarrollo local como para su despliegue en servidores web de producción.

---

## Características Principales

* **Panel de Control (Dashboard) Centralizado:**
  * Métricas en tiempo real de libros registrados, préstamos activos/vencidos, usuarios activos y monto acumulado de multas pendientes.
  * Listado de las últimas operaciones registradas.

* **Gestión de Catálogo (CRUD de Libros y Categorías):**
  * Alta, consulta, edición y eliminación de libros.
  * Clasificación por categorías temáticas.
  * Control automático de stock total y stock disponible según transacciones de préstamos.
  * Búsqueda en tiempo real por título, autor o código ISBN.

* **Administración de Usuarios y Socios:**
  * Registro de usuarios con datos de contacto y estado operativo (activo/inactivo).
  * Historial individual de préstamos y sanciones asociadas.

* **Módulo de Préstamos y Devoluciones:**
  * Asignación de libros a usuarios con cálculo automático de la fecha límite de devolución.
  * Actualización en tiempo real de la disponibilidad física de los libros.
  * Registro de devoluciones y cambio de estado del préstamo (Activo, Devuelto, Vencido).

* **Control Financiero de Multas:**
  * Generación y registro automático de penalizaciones económicas según los días de retraso.
  * Gestión del estado de pago de las multas generadas.

---

## Arquitectura del Sistema

El proyecto sigue una arquitectura de capas bien delimitadas:

1. **Capa de Presentación (Frontend):** Desarrollada con HTML5 semántico, CSS3 modular (con variables y diseño adaptativo) y JavaScript Vanilla (ES6+). Implementa el patrón SPA para actualizar vistas y consumir datos asíncronamente mediante `Fetch API`.
2. **Capa de Aplicación / Servicios (Backend):** Implementada en Python utilizando el microframework Flask. Expone endpoints RESTful que procesan solicitudes HTTP, gestionan la lógica de negocio y retornan respuestas en formato JSON. Compatible con servidores WSGI (como Gunicorn o uWSGI) para entornos de servidor.
3. **Capa de Persistencia (Base de Datos):** Servidor relacional MySQL / MariaDB interactuando a través del conector `PyMySQL`, con ejecuciones mediante SQL preparado para la prevención de vulnerabilidades.

---

## Tecnologías Utilizadas

### Backend
* **Lenguaje:** Python 3.x
* **Framework Web:** Flask (v3.0.0 o superior)
* **Conector de Base de Datos:** PyMySQL (v1.1.0 o superior)
* **Servidor WSGI (Producción):** Gunicorn / uWSGI

### Base de Datos
* **Motor Relacional:** MySQL 8.0+ / MariaDB 10.4+
* **Gestión de Esquema:** Script SQL parametrizado (`schema.sql`) con restricciones de clave foránea (`FOREIGN KEY`), índices únicos y tipos de datos numéricos/fecha estrictos.

### Frontend
* **Estructura y Estilos:** HTML5, CSS3 puro (Flexbox, CSS Grid, CSS Variables)
* **Lógica Cliente:** JavaScript ES6+ (Fetch API, manipulación asíncrona del DOM)
* **Componentes Visuales:** Bootstrap Icons, Google Fonts (Inter / System Fonts)

---

## Estructura del Proyecto

```text
biblioteca/
├── app.py              # Aplicación principal Flask y definición de endpoints REST API
├── database.py         # Módulo de conexión y utilidades para ejecutar consultas MySQL
├── schema.sql          # Estructura DDL de la base de datos y datos semilla (Seed Data)
├── requirements.txt    # Dependencias del proyecto Python
├── static/             # Recursos estáticos servidos por el backend
│   ├── css/
│   │   └── style.css   # Hoja de estilos principal del sistema
│   ├── js/
│   │   └── main.js     # Lógica JavaScript del lado del cliente (SPA / Fetch)
│   ├── img/            # Portadas e imágenes de apoyo
│   └── favicon.svg     # Icono de la aplicación
└── templates/
    └── index.html      # Plantilla principal renderizada por Flask
```

---

## Requisitos del Sistema

* Python 3.9 o superior.
* Servidor MySQL 8.0+ o MariaDB 10.4+ en la infraestructura del servidor.
* Administrador de paquetes `pip`.

---

## Instalación y Configuración Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/usuario/biblioteca.git
cd biblioteca
```

### 2. Crear y activar un entorno virtual
En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

---

## Gestión de Variables de Entorno y Credenciales

Por razones estrictas de seguridad, el sistema no almacena ni expone credenciales de acceso a la base de datos o claves secretas en el código fuente ni en el repositorio de control de versiones.

Las credenciales de acceso deben configurarse exclusivamente a través de variables de entorno en el sistema operativo del servidor o mediante un gestor de secretos.

### Variables de Entorno Requeridas:

* `DB_HOST`: Dirección IP o nombre de dominio del servidor de base de datos MySQL (ej. `sql101.infinityfree.com`).
* `DB_PORT`: Puerto de conexión al servicio MySQL (por defecto `3306`).
* `DB_NAME`: Nombre asignado a la base de datos (ej. `if0_42525650_biblioteca_db`).
* `DB_USER`: Usuario autenticado con permisos en dicha base de datos.
* `DB_PASSWORD`: Contraseña de acceso a la base de datos.

### Ejemplo de Configuración en el Servidor (Bash/Linux):

```bash
export DB_HOST="sql101.infinityfree.com"
export DB_PORT="3306"
export DB_NAME="if0_42525650_biblioteca_db"
export DB_USER="usuario_bd"
export DB_PASSWORD="tu_password_segura"
```

---

## Configuración de la Base de Datos

1. Verificar que el servicio MySQL o MariaDB se encuentre activo en la infraestructura del servidor.
2. Asegurar que el usuario configurado en las variables de entorno cuente con los privilegios requeridos para la creación de esquemas y tablas (`CREATE`, `SELECT`, `INSERT`, `UPDATE`, `DELETE`).
3. El módulo `database.py` verificará la existencia del esquema `biblioteca_db` al iniciar la aplicación. Si el esquema no existe, ejecutará automáticamente el archivo DDL `schema.sql` para estructurar la base de datos y cargar la configuración inicial.

---

## Despliegue en Servidor de Producción

Para desplegar la aplicación en un entorno de producción (Linux / VPS / Servidor Cloud), se recomienda la siguiente arquitectura:

### 1. Servidor de Aplicación (WSGI)
En lugar de utilizar el servidor de desarrollo integrado de Flask, utilice un servidor WSGI de grado de producción como **Gunicorn**:

```bash
pip install gunicorn
gunicorn --workers 4 --bind 127.0.0.1:8000 app:app
```

### 2. Proxy Inverso (Nginx / Apache)
Se recomienda configurar **Nginx** como proxy inverso para gestionar las peticiones entrantes, servir recursos estáticos y proveer certificados de seguridad SSL/TLS (HTTPS).

Ejemplo de bloque de configuración de Nginx:

```nginx
server {
    listen 80;
    server_name biblioteca.midominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /ruta/al/proyecto/biblioteca/static/;
    }
}
```

### 3. Servicio de Sistema (systemd)
Para garantizar que la aplicación se mantenga activa y se reinicie automáticamente ante fallos o reinicios del servidor, configure un servicio en `systemd`.

---

## Especificación de la API RESTful

El servidor backend expone los siguientes endpoints para el intercambio de información:

### Dashboard y Estadísticas
* `GET /api/stats` - Retorna los indicadores numéricos del sistema y los préstamos recientes.

### Categorías
* `GET /api/categorias` - Obtiene la lista completa de categorías registradas.

### Libros
* `GET /api/libros` - Obtiene el catálogo de libros. Soporta parámetros de consulta `?q=busqueda` y `?categoria=id`.

### Usuarios
* `GET /api/usuarios` - Lista los usuarios registrados en el sistema.

### Préstamos
* `GET /api/prestamos` - Devuelve el historial y estado de los préstamos.
* `POST /api/prestamos` - Registra un nuevo préstamo de libro.
* `PUT /api/prestamos/<id>/devolver` - Procesa la devolución de un libro y actualiza el stock.

### Multas
* `GET /api/multas` - Retorna el listado de sanciones económicas registradas.

---

## Buenas Prácticas e Implementación de Seguridad

* **Aislamiento de Credenciales:** Absoluta separación entre el código fuente y las credenciales de acceso a la base de datos mediante variables de entorno, evitando fugas de información en repositorios públicos o privados.
* **Consultas Parametrizadas:** Toda interacción con la base de datos utiliza marcadores de posición (`%s`) para evitar vulnerabilidades de inyección de código SQL.
* **Manejo de Transacciones e Integridad Referencial:** Configuración explícita de `CASCADE` y `SET NULL` en relaciones DDL para prevenir registros huérfanos.
* **Separación de Responsabilidades:** Arquitectura modular con desacoplamiento entre el controlador HTTP, la capa de datos y la interfaz de usuario.
* **Control de Errores HTTP:** Retorno de códigos de estado HTTP estandarizados (200, 400, 404, 500) acompañados de respuestas estructuradas en JSON.
# Biblioteca---BiblioSys
# Biblioteca---BiblioSys
# Biblioteca---BiblioSys
# Biblioteca---BiblioSys
