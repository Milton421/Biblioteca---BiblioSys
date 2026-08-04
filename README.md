# BiblioSys - Sistema de Gestión de Biblioteca

BiblioSys es un sistema web moderno diseñado para la administración integral de bibliotecas. Permite la digitalización del catálogo de libros, control de existencias en tiempo real, registro de socios, gestión de préstamos y automatización del cálculo de penalizaciones por entregas tardías.

**Aplicación en Producción:** [https://biblioteca-biblio-sys.vercel.app](https://biblioteca-biblio-sys.vercel.app)

---

## Módulos y Funcionalidades

### Panel de Control - Dashboard
- Visualización de métricas generales: total de libros, préstamos activos, socios registrados y saldo en multas pendientes.
- Listado de actividad reciente con estado de transacciones en tiempo real.

### Catálogo de Libros
- Administración completa de libros (Crear, Leer, Actualizar, Eliminar).
- Clasificación por categorías temáticas.
- Control automatizado de stock total y copias disponibles.
- Búsqueda dinámicas por título, autor o código ISBN.

### Administración de Socios
- Registro de usuarios con datos de contacto (correo, teléfono, dirección).
- Seguimiento de estado de socios activos en la plataforma.

### Préstamos y Devoluciones
- Registro de salidas de libros asociadas a socios.
- Cálculo automático de fecha límite de entrega según el plazo seleccionado.
- Actualización inmediata del inventario disponible al realizar devoluciones.

### Control de Multas
- Cálculo automatizado de tarifas por días de retraso en la devolución de ejemplares.
- Gestión de cobros y cambio de estado de multas pendientes a pagadas.

---

## Arquitectura y Tecnologías

### Frontend
- **HTML5 & CSS3:** Interfaz semántica con variables CSS y diseño adaptativo.
- **JavaScript (ES6+):** Arquitectura de Aplicación de Página Única (SPA) mediante consumo asíncrono de la API REST con `Fetch API`.

### Backend
- **Python / Flask:** API RESTful modular para el procesamiento de reglas de negocio y endpoints.
- **pg8000 & PyMySQL:** Conectores de base de datos ligeros compatibles con entornos serverless.

### Base de Datos e Infraestructura
- **Supabase (PostgreSQL):** Persistencia relacional en entorno de producción.
- **Vercel:** Plataforma de despliegue continuo y ejecución serverless.

---

## Estructura del Proyecto

```text
biblioteca/
├── app.py                  # Aplicación principal Flask y definición de rutas API
├── database.py             # Conexión y abstracción para PostgreSQL y MySQL
├── schema_supabase.sql     # Definición de tablas y datos semilla para PostgreSQL (Supabase)
├── schema.sql              # Definición de tablas para MySQL
├── vercel.json             # Configuración de rutas para la plataforma Vercel
├── requirements.txt        # Dependencias del proyecto en Python
├── index.html              # Plantilla y estructura de la interfaz cliente (SPA)
└── static/
    ├── css/
    │   └── style.css       # Hoja de estilos de la interfaz
    ├── js/
    │   └── main.js         # Lógica cliente, navegación SPA e interacción con la API
    └── favicon.svg         # Identificador visual del sistema
```

---

## Configuración e Instalación Local

### Requisitos Previos
- Python 3.9 o superior.
- Git.

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Milton421/Biblioteca---BiblioSys.git
   cd Biblioteca---BiblioSys
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor de desarrollo:**
   ```bash
   python app.py
   ```

4. **Acceder a la aplicación:**
   Abre tu navegador e ingresa a `http://127.0.0.1:5050`.

---

## Variables de Entorno

El sistema detecta automáticamente las variables inyectadas por Vercel para Supabase. En caso de requerir configuración manual, se utilizan las siguientes variables:

- `POSTGRES_URL`: Cadena de conexión completa a PostgreSQL.
- `DB_HOST`: Host del servidor de base de datos MySQL.
- `DB_USER`: Usuario autenticado.
- `DB_PASSWORD`: Contraseña de acceso.
- `DB_NAME`: Nombre de la base de datos.

---

