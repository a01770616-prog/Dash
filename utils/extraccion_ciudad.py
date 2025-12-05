import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Estas funciones encapsulan cálculos y visualizaciones avanzadas
# relacionadas al profesionalismo, competitividad y estructura de la ciudad.
from utils.extraccion_competitividad import (
    calcular_competitividad,
    render_radar_competitividad,
    render_vecindarios_profesionalismo,
)

# Función que permite presentar distribuciones geográficas sobre el mapa
from utils.extraccion_mapas import render_mapa_ciudad

# Paleta aplicada en gráficas de identificación visual asociadas a la marca Airbnb
AIRBNB_COLORS = [
    "#FFF5F5",
    "#FFE3E6",
    "#FFB3BA",
    "#FF7A85",
    "#FF5A5F",
    "#FF385C"
]


def render_tab_ciudad(
    df_filtered,         
    selected_cities,
    Lista,
    Variable_Cat,
    top_k,
    mostrar_tabla,
    PALETTE
):
    """
    Renderiza vistas individuales por ciudad, permitiendo que el usuario seleccione
    una ciudad y visualice gráficas comparativas con mayor nivel de detalle.

    df_filtered  → información ya filtrada globalmente por el usuario
    selected_cities → ciudades activas en análisis
    Variable_Cat → columna categórica elegida para desglose
    Mostrar_tabla → habilita tabla complementaria
    PALETTE → paleta general usada en componentes visuales
    """

    # Selección controlada de una sola ciudad a analizar en detalle
    ciudad_sel = st.selectbox("Ciudad para gráficas individuales", selected_cities)

    # Subconjunto con solo la ciudad elegida para evitar ruido visual
    df_city = df_filtered[df_filtered["ciudad"] == ciudad_sel].copy()

    st.markdown("## Análisis detallado por ciudad")


    # PRIMER BLOQUE VISUAL: Distribución de categoría + Boxplot comparativo
    col1, col2 = st.columns(2)

    # Se analiza la variable categórica principal elegida por el usuario
    with col1:
        st.subheader("Top Barrios")

        # Conteo de frecuencia por categorías ordenadas descendentemente
        Tabla_frec = (
            df_city[Variable_Cat]
            .astype(str)
            .fillna("NA")
            .value_counts()
            .head(top_k)
            .reset_index()
        )

        # Asignación de nombres formales a columnas
        Tabla_frec.columns = ["categoría", "frecuencia"]

        # Visualización en barras representa jerarquización de zonas o atributos
        fig = px.bar(
            Tabla_frec,
            x="categoría",
            y="frecuencia",
            color="categoría",
            color_discrete_sequence=[PALETTE["brand"], PALETTE["accent"]],
        )
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

        if mostrar_tabla:
            st.dataframe(Tabla_frec, use_container_width=True)


    with col2:
        st.subheader("Boxplot — Precio por categoría")

        # Para generar análisis de variabilidad, debe existir una columna válida de price
        if "price" in df_city.columns and df_city["price"].notna().any():

            # Selección libre de columna categórica para análisis transversal del precio
            cat_box = st.selectbox(
                "Categoría",
                options=[c for c in Lista if c in df_city.columns],
                key="boxcat_ciudad",
            )

            df_box = df_city[[cat_box, "price"]].dropna()

            # Se reducen categorías a las más frecuentes para evitar esquemas saturados visualmente
            top_cats = (
                df_box[cat_box]
                .astype(str)
                .value_counts()
                .head(min(top_k, 15))
                .index
            )

            df_box = df_box[df_box[cat_box].astype(str).isin(top_cats)]

            # Boxplot permite observar mediana, dispersión e outliers
            fig_box = px.box(
                df_box,
                x=cat_box,
                y="price",
                color=cat_box,
                color_discrete_sequence=[PALETTE["brand"], PALETTE["accent"]],
                points=False,
            )
            fig_box.update_layout(height=380)
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("No existe columna 'price' válida para boxplot.")

    st.markdown("---")


    # SEGUNDO BLOQUE VISUAL: Coocurrencias de categorías + profesionalismo de host
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Heatmap de coocurrencias")

        # Extraemos solo variables categóricas disponibles
        cats_heat = [c for c in Lista if c in df_city.columns]

        # Para cruzar categorías se necesitan mínimo dos variables
        if len(cats_heat) >= 2:

            cat_x = st.selectbox("Eje X", cats_heat, key="heat_x_ciudad")
            cat_y = st.selectbox(
                "Eje Y",
                [c for c in cats_heat if c != cat_x],
                key="heat_y_ciudad",
            )

            # Se genera tabla de conteos
            df_hm = df_city[[cat_x, cat_y]].astype(str)
            t = df_hm.value_counts().reset_index(name="freq")

            # Heatmap para observar coincidencias entre categorías
            fig_hm = px.density_heatmap(
                t,
                x=cat_x,
                y=cat_y,
                z="freq",
                color_continuous_scale=["#E0F7FA", PALETTE["accent"], "#004D40"],
                height=390
            )

            st.plotly_chart(fig_hm, use_container_width=True)

        else:
            st.info("Se requieren al menos 2 variables categóricas para el heatmap.")


    with col4:
        st.subheader("Profesionalismo por vecindario")

        # Esta función mide qué porcentaje del inventario es gestionado por Superhosts
        # Lo cual sirve como indicador de madurez del mercado en cada barrio
        render_vecindarios_profesionalismo(df_city)

    st.markdown("---")


    # TERCER BLOQUE VISUAL: Índice competitivo + Geolocalización
    col_radar, col_mapa = st.columns(2)

    with col_radar:
        st.subheader("Índice de Competitividad")

        # Se calcula una métrica global ponderada con varios factores
        comp = calcular_competitividad(df_city)

        # Radar permite comparar simultáneamente las dimensiones competitivas
        render_radar_competitividad(comp, ciudad_sel, PALETTE)


    with col_mapa:
        st.subheader("Mapa Geoespacial")

        # Mapa con puntos georreferenciados de Airbnb visibles según ciudad
        # Permite ver concentración de inventario (centro, playa, periferias)
        render_mapa_ciudad(df_city)


