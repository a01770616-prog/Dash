import streamlit as st

# Configuración inicial de la aplicación. Este ajuste debe ejecutarse antes de mostrar cualquier componente en pantalla.
st.set_page_config(
    page_title='Dashboard multi-pagina',     # Define el título que aparecerá en la pestaña del navegador.
    layout='wide',                           # Asigna un diseño expandido que aprovecha el ancho de la pantalla.
    initial_sidebar_state='expanded'         # Hace que la barra lateral aparezca expandida desde el inicio.
)

# Definición de cada página que formará parte del dashboard. Cada página corresponde a un archivo dentro de la carpeta "Paginas".

# Página principal o de bienvenida. Generalmente muestra información inicial del dashboard.
homepage = st.Page(
    'Paginas/homepage.py',                   # Ruta al archivo Python responsable del contenido dentro de esta sección.
    title='Home',                            # Título que aparecerá en la navegación lateral.
    icon=':material/home:'                   # Icono que representa visualmente a la página.
)

# Página con información sobre el programa o proyecto. Útil para contexto general.
acerca_programa_page = st.Page(
    'Paginas/acerca_programa.py',
    title='Acerca del Programa',
    icon=':material/menu_book:'              # Icono alusivo a documentación o contenido informativo.
)

# Página donde se describen áreas o módulos clave del proyecto o análisis.
areas_enfoque_page = st.Page(
    'Paginas/areas_enfoque.py',
    title='Áreas de Enfoque',
    icon=':material/home:'                   # Icono genérico relacionado a navegación principal.
)

# Página donde se visualizan indicadores generales de Airbnb calculados a nivel global.
kpis_airbnb_page = st.Page(
    'Paginas/pagina1.py',
    title='KPIs Globales',
    icon=':material/analytics:'              # Icono que representa métricas o resultados cuantitativos.
)

# Página donde se muestra el análisis desglosado por ciudad (comparación y estadísticas específicas).
detalle_airbnb_page = st.Page(
    'Paginas/pagina2.py',
    title='KPIS por Ciudades',
    icon=':material/location_city:'          # Icono que representa el contexto urbano o geográfico.
)

# Página de análisis detallado de barrios dentro de cada ciudad del dataset.
explorador_barrios_page = st.Page(
    "Paginas/pagina3.py",
    title="Explorador de Barrios",
    icon=":material/map:"                    # Icono adecuado para visualizaciones por zona geográfica.
)

# Página utilizada para extraer características relevantes dentro del dataset (limpieza, cómputo, ingeniería).
extraccion_caracteristicas= st.Page(
    "Paginas/pagina4.py",
    title="Extracción de Características",
    icon=":material/insert_chart:"           # Icono orientado a análisis e interpretación de datos.
)

# Página relacionada con el entrenamiento de modelos. Aquí se cargan algoritmos y resultados de clasificación.
entrenamiento= st.Page(
    "Paginas/pagina5.py",
    title="Clasificación",
    icon=":material/insert_chart:"           # Icono representativo de aprendizaje automático.
)

# Configuración del menú de navegación lateral. Se organiza en grupos temáticos.
# Cada llave corresponde al título mostrado como sección principal
# y cada valor es una lista con las páginas que pertenecen a dicha sección.
pg = st.navigation({
    'Home':        [homepage],                               # Grupo principal con acceso directo.
    'Airbnb':      [kpis_airbnb_page, detalle_airbnb_page, explorador_barrios_page],  # Métricas y análisis de Airbnb.
    'Estadisticas':[extraccion_caracteristicas],             # Procesos relacionados con estadística avanzada.
    'Clasificación':[entrenamiento],                         # Modelado supervisado y análisis de resultados.
    'Información': [acerca_programa_page, areas_enfoque_page], # Información adicional y documentación de referencia.
})

# Ejecución final del sistema de navegación para habilitar el flujo entre páginas.
pg.run()
