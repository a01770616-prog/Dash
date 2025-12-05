import streamlit as st

from utils.utils_filtros import sidebar_filtros                     # Función para crear filtros dinámicos
from utils.extraccion_ciudad import render_tab_ciudad              # Módulo encargado del análisis por ciudad
from utils.extraccion_comparativo import render_tab_comparativo    # Módulo encargado de análisis comparativo entre ciudades


# Esta función construye la página de análisis de extracción de características.
# No realiza cálculos directamente, sino que organiza componentes visuales y
# delega el procesamiento y visualización a funciones de módulos externos.
def render_pagina_extraccion(df, Lista, PALETTE, AIRBNB_COMPETITIVENESS_SCALE):
    """
    Parámetros
    ----------
    df: DataFrame con información consolidada.
    Lista: Lista con variables categóricas disponibles para análisis.
    PALETTE: Diccionario o estructura de colores asignados para visualizaciones.
    AIRBNB_COMPETITIVENESS_SCALE: Vector o escala utilizada para categorizar competitividad.

    Su propósito principal es construir una interfaz que incluya:
        - Filtros de selección
        - División de la vista mediante tabs
        - Envío de los filtros a funciones especializadas
    """

    # Se obtienen los filtros seleccionados por el usuario desde un panel lateral.
    # La función sidebar_filtros retorna los componentes necesarios para estructurar
    # vistas dinámicas: ciudades filtradas, subconjunto de datos filtrado, cantidad
    # de categorías (top_k), indicador para visualizar tabla y la variable categórica seleccionada.
    selected_cities, df_filtered, top_k, mostrar_tabla, Variable_Cat = sidebar_filtros(
        df, Lista
    )

    # Se dividen las vistas utilizando pestañas. Cada pestaña contendrá un análisis distinto.
    # Esto permite cambiar entre análisis por ciudad o uno comparativo sin recargar la aplicación.
    tab_ciudad, tab_comparativo = st.tabs(
        ["Por ciudad", "Comparativo multi-ciudad"]
    )

    # Procesamiento y visualización orientado a análisis individual por ciudad.
    # En esta sección se envían únicamente los parámetros necesarios para dicho análisis.
    with tab_ciudad:
        render_tab_ciudad(
            df_filtered=df_filtered,        # Subconjunto de datos filtrados
            selected_cities=selected_cities,# Ciudades seleccionadas por el usuario
            Lista=Lista,                    # Lista de variables categóricas disponibles
            Variable_Cat=Variable_Cat,      # Variable categórica elegida
            top_k=top_k,                    # Número máximo de categorías a mostrar
            mostrar_tabla=mostrar_tabla,    # Boolean para controlar visualización tabular
            PALETTE=PALETTE,                # Paleta de colores homogénea
        )

    # Procesamiento orientado a la comparación simultánea de múltiples ciudades.
    # Aquí se envían parámetros específicos al módulo encargado de análisis comparativo.
    with tab_comparativo:
        render_tab_comparativo(
            df_filtered=df_filtered,         # DataFrame filtrado
            selected_cities=selected_cities, # Ciudades elegidas
            Variable_Cat=Variable_Cat,       # Categoría activa
            Lista=Lista,                     # Listado disponible
            top_k=top_k,                     # Nivel de detalle categórico
            mostrar_tabla=mostrar_tabla,     # Indicador de despliegue tabular
            SCALE=AIRBNB_COMPETITIVENESS_SCALE, # Escala utilizada para métricas derivadas
        )
