import streamlit as st

from utils.utils_datos import load_data
from utils.utils_filtros import sidebar_filtros
from utils.extraccion_ciudad import render_tab_ciudad
from utils.extraccion_comparativo import render_tab_comparativo


# Título principal de la página que indica la naturaleza del módulo
# En esta sección se explorarán atributos relevantes de la base de datos
st.title("Extracción de Características")

# Carga del DataFrame principal utilizando la función modularizada load_data()
# Esta función regresa:
# df        → datos combinados de todas las ciudades
# warnings  → mensajes informativos relacionados con la carga
df, warnings = load_data()

# Si hay advertencias, se despliegan dentro de un contenedor expandible
if warnings:
    with st.expander("Avisos al cargar datos"):
        for w in warnings:
            st.warning(w)

# En caso de fallar la lectura de los archivos, se detiene la ejecución
if df.empty:
    st.error("No se pudo cargar ningún dataset. Revisa la carpeta data/.")
    st.stop()


# Identificación de variables categóricas
# Se seleccionan únicamente columnas tipo 'object', excluyendo ciudad e id
# Estas variables servirán como filtros y parámetros para análisis comparativos
candidatos_cat = df.select_dtypes(include=["object"]).columns.tolist()
Lista = sorted([c for c in candidatos_cat if c not in ["ciudad", "id"]])


# Paleta base de colores utilizada en visualizaciones específicas
# Se asocia al look & feel corporativo de Airbnb
PALETTE = {
    "brand": "#FF385C",
    "accent": "#FF5A5F",
    "muted": "#E2E8F0",
}

# Escala extendida utilizada para gradientes o intensidad en gráficas comparativas
AIRBNB_COMPETITIVENESS_SCALE = [
    "#FFF5F5",
    "#FFE3E6",
    "#FFB3BA",
    "#FF7A85",
    "#FF5A5F",
    "#FF385C",
]


# Se envían los datos al menú lateral, donde se definen filtros interactivos
# Esta función retorna:
# selected_cities → ciudades elegidas por el usuario
# df_filtered     → dataset filtrado según criterios activos
# top_k           → cantidad máxima de elementos a mostrar
# mostrar_tabla   → indicador de visualización tabular
# Variable_Cat    → variable categórica seleccionada
selected_cities, df_filtered, top_k, mostrar_tabla, Variable_Cat = sidebar_filtros(
    df, Lista
)


# Configuración de navegación interna mediante pestañas
# Primera pestaña: análisis individual por ciudad
# Segunda pestaña: comparativo entre múltiples ciudades
tab_ciudad, tab_comparativo = st.tabs(["Por ciudad", "Comparativo multi-ciudad"])


# Renderizado de contenido específico para cada tab
# El contenido se delega a funciones especializadas modularizadas
with tab_ciudad:
    render_tab_ciudad(
        df_filtered,
        selected_cities,
        Lista,
        Variable_Cat,
        top_k,
        mostrar_tabla,
        PALETTE
    )

with tab_comparativo:
    render_tab_comparativo(
        df_filtered,
        selected_cities,
        Variable_Cat,
        Lista,
        top_k,
        mostrar_tabla,
        AIRBNB_COMPETITIVENESS_SCALE
    )

