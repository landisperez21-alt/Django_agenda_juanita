# 📅 Django Agenda - Juanita

Sistema web de gestión de agenda y citas desarrollado con **Django 6.0** y **MariaDB 10.4 (XAMPP)**.

## 👨‍💻 Autor y Desarrollor
* **Autor:** Landis Sanchez

## 🚀 Tecnologías y Entorno
* **Python 3.12+**
* **Django 6.0.10**
* **MariaDB 10.4 (XAMPP)**
* **PyMySQL** (Conector de base de datos adaptado)

## 🛠️ Solución de Compatibilidad (Django 6.x & MariaDB 10.4)
Este proyecto incluye un parche global en `config/__init__.py` para desactivar las consultas `RETURNING` incompatibles con MariaDB 10.4:
python
from django.db.backends.mysql.features import DatabaseFeatures
DatabaseFeatures.can_return_rows_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False
DatabaseFeatures.can_return_generated_columns = False
DatabaseFeatures.can_return_columns_from_insert = False


## ⚙️ Instalación y Configuración Local

Sigue estos pasos para clonar y poner en marcha el proyecto:

1. **Clonar el repositorio:**

git clone https://github.com/landisperez21-alt/Django_agenda_juanita.git
cd Django_agenda_juanita/Django_agenda_juanita_26-2


2. **Crear y activar el entorno virtual:**

python -m venv .venv
.venv\Scripts\Activate  # En Windows (PowerShell)


3. **Instalar dependencias:**

pip install django pymysql


4. **Configurar la base de datos en XAMPP:**
* Inicia **Apache** y **MySQL** en XAMPP.
* Crea una base de datos vacía llamada `agenda_juanita_26_2_db`.

5. **Aplicar las migraciones:**

python manage.py migrate


6. **Crear el superusuario (Administrador):**

python manage.py createsuperuser


7. **Ejecutar el servidor de desarrollo:**

python manage.py runserver

Abre tu navegador y entra a: `http://127.0.0.1:8000/`
