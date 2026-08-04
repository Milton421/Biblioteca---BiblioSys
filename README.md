# BiblioSys

> Sistema web moderno e intuitivo para la gestión integral de bibliotecas, control de inventario de libros, registro de socios, préstamos y seguimiento de multas.

[🌐 Ver Aplicación en Producción](https://biblioteca-biblio-sys.vercel.app)

---

## ⚡ Características

- **Dashboard General:** Resumen ejecutivo de métricas clave y actividad reciente.
- **Catálogo de Libros:** Control de inventario, disponibilidad en tiempo real y filtrado por categorías.
- **Gestión de Socios:** Control de registro y estado de miembros de la biblioteca.
- **Préstamos y Devoluciones:** Automatización de plazos de entrega y actualización inmediata de existencias.
- **Control de Multas:** Cálculo y seguimiento de penalizaciones por devoluciones tardías.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
| --- | --- |
| **Frontend** | HTML5, CSS3, JavaScript Vanilla (SPA) |
| **Backend** | Python (Flask REST API) |
| **Base de Datos** | Supabase (PostgreSQL) / MySQL |
| **Despliegue** | Vercel |

---

## 📂 Estructura del Proyecto

```text
biblioteca/
├── app.py                  # API RESTful en Flask y definición de endpoints
├── database.py             # Capa de abstracción y conexión a PostgreSQL / MySQL
├── schema_supabase.sql     # Estructura DDL y datos semilla para Supabase (PostgreSQL)
├── schema.sql              # Estructura DDL para bases de datos MySQL
├── vercel.json             # Configuración de rutas y despliegue para Vercel
├── requirements.txt        # Librerías y dependencias de Python
├── index.html              # Interfaz de usuario principal (Single Page Application)
└── static/                 # Recursos estáticos del sistema
    ├── css/
    │   └── style.css       # Hoja de estilos global y diseño responsivo
    ├── js/
    │   └── main.js         # Lógica del cliente, controladores SPA y Fetch API
    └── favicon.svg         # Icono oficial de la aplicación
```

---

## 💻 Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/Milton421/Biblioteca---BiblioSys.git
cd Biblioteca---BiblioSys
```

### 2. Crear y activar entorno virtual (Opcional)
```bash
# En Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# En Linux / macOS:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación
```bash
python app.py
```

Accede desde tu navegador en: `http://127.0.0.1:5050`

---

