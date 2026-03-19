🌲 FireData: Análisis de Incendios Forestales en España (1968-2020)

FireData es una plataforma integral para el monitoreo y análisis del impacto de los incendios forestales en España. El proyecto abarca desde la limpieza de datos crudos con Pandas hasta la exposición de una API de alto rendimiento y la visualización en un Dashboard interactivo con Django.
📂 Estructura del Repositorio

El proyecto está organizado de forma modular para separar la lógica de datos de la interfaz de usuario:

    django_dashboard/: Aplicación principal que sirve la interfaz de usuario. Incluye gráficos dinámicos de Plotly, tablas de datos y paneles de KPIs con un diseño dark-mode profesional.

    api_fast/: Microservicio desarrollado con FastAPI para ofrecer acceso programático a las estadísticas, optimizando la velocidad de respuesta.

    pandas_sqlite/: Scripts de ingeniería de datos (ETL). Realiza la limpieza de datasets, filtrado por provincias y la migración a la base de datos relacional.

    data/: Contenedor de los archivos fuente (CSV/Excel) y la base de datos final db.sqlite3.

    .venv/: Entorno virtual con todas las dependencias aisladas del sistema.

🚀 Características Técnicas
📊 Visualización de Datos

    Dashboards de Alto Impacto: KPIs personalizados para hectáreas quemadas y número de siniestros totales.

    Interactividad Total: Gráficos de líneas y barras con Plotly que permiten filtrar información de forma dinámica.

    Interfaz Moderna: Diseño optimizado con CSS personalizado, uso de variables nativas, tipografía Inter y layouts adaptables (Flexbox/Grid).

⚙️ Stack Tecnológico

    Backend: Django (Framework principal) y FastAPI (Servicios ligeros).

    Data Science: Pandas y NumPy para el procesamiento de grandes volúmenes de datos.

    Frontend: HTML5 Semántico y CSS3 avanzado (Custom Dark Theme).

    Base de Datos: SQLite3 para una persistencia ligera y eficiente.

🛠️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

    Clonar el repositorio:
    git clone https://www.google.com/search?q=https://github.com/tu-usuario/tu-repositorio.git
    cd PROYECTO_INCENDIOS_FORESTALES_V1

    Activar el entorno virtual:
    En Windows

    .venv\Scripts\activate
    En Linux/Mac

    source .venv/bin/activate

    Instalar las dependencias:
    pip install -r requirements.txt

    Ejecutar el servidor de Django:
    cd django_dashboard
    python manage.py runserver

    Accede a https://www.google.com/search?q=http://127.0.0.1:8000 en tu navegador.

📈 Metodología de Trabajo

El flujo de datos sigue un proceso riguroso para garantizar la precisión de los análisis:

    Limpieza: Tratamiento de valores nulos y eliminación de duplicados en los registros históricos.

    Normalización: Estandarización de nombres de provincias y comunidades para evitar inconsistencias.

    Carga: Migración de datos desde archivos planos hacia una estructura relacional optimizada.

    Visualización: Traducción de datos complejos en métricas comprensibles para el usuario final.

✒️ Autor

    David Herrera Torrado - Pipeline TD & Data Analysis - (https://github.com/daher7)

© 2026 FireData Project - Análisis Medioambiental de Datos Abiertos.
