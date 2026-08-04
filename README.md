# 📚 BiblioSys — Sistema de Gestión de Biblioteca

Un sistema web moderno, ágil y elegante para la administración de bibliotecas. Permite gestionar inventarios de libros, socios, préstamos, devoluciones y cálculo automático de multas.

🌐 **Demo en línea (Producción):** [https://biblioteca-biblio-sys.vercel.app](https://biblioteca-biblio-sys.vercel.app)

---

## ✨ Características Principales

* **📊 Dashboard Integrado:** Métricas en tiempo real de inventario, socios activos, préstamos en curso y multas pendientes.
* **📖 Catálogo de Libros:** Control de stock total y disponible, categorías y búsqueda instantánea por título, autor o ISBN.
* **👥 Gestión de Socios:** Registro y control de información de usuarios con datos de contacto.
* **🔄 Préstamos y Devoluciones:** Asignación de plazos, devolución de ejemplares y actualización automática de disponibilidad.
* **⚠️ Sistema de Multas:** Generación de penalizaciones por entregas tardías y gestión de pagos.

---

## 🛠️ Tecnologías

* **Frontend:** HTML5, CSS3 (Diseño responsivo moderno), JavaScript Vanilla (SPA / Fetch API).
* **Backend:** Python (Flask REST API).
* **Base de Datos:** Supabase (PostgreSQL) en Producción / Compatible con MySQL.
* **Hosting & Cloud:** Vercel (Despliegue continuo serverless).

---

## 📁 Estructura del Proyecto

```text
biblioteca/
├── app.py                  # Servidor Flask y API RESTful
├── database.py             # Conexión agnóstica a base de datos (PostgreSQL / MySQL)
├── schema_supabase.sql     # Script SQL para Supabase (PostgreSQL)
├── schema.sql              # Script SQL para MySQL
├── vercel.json             # Configuración de despliegue en Vercel
├── requirements.txt        # Dependencias de Python
├── index.html              # Interfaz de usuario (SPA)
└── static/                 # Hojas de estilo (CSS) y scripts (JS)
```

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Milton421/Biblioteca---BiblioSys.git
   cd Biblioteca---BiblioSys
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el servidor local:**
   ```bash
   python app.py
   ```
   Abre `http://127.0.0.1:5050` en tu navegador.

---

