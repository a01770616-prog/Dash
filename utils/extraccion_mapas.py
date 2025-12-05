import streamlit as st
import plotly.express as px
import pandas as pd


def render_mapa_ciudad(df_city):
    """
    Renderiza un mapa para una sola ciudad utilizando coordenadas geográficas.
    La finalidad es mostrar la distribución espacial de las propiedades filtradas
    en una vista geográfica. Esta visualización permite identificar zonas de mayor
    concentración de anuncios y variaciones en precios dentro de la misma ciudad.
    """

    # Validación previa: si no están disponibles las coordenadas, el mapa no puede construirse.
    if "latitude" not in df_city or "longitude" not in df_city:
        st.info("No hay datos de ubicación disponibles.")
        return

    # Se elimina cualquier registro que no tenga coordenadas válidas para evitar fallos en el renderizado.
    df_geo = df_city.dropna(subset=["latitude", "longitude"])

    # Mapa geográfico de puntos donde cada punto representa una propiedad.
    # Si existe la variable price, se utiliza para colorear los puntos y generar un gradiente visual por costo.
    fig = px.scatter_mapbox(
        df_geo,
        lat="latitude",
        lon="longitude",
        color="price" if "price" in df_geo else None,
        mapbox_style="open-street-map",
        height=500,
        color_continuous_scale=[
            "#FFE3E6", "#FFB3BA", "#FF7A85", "#FF5A5F", "#FF385C"
        ]
    )

    # Se deshabilita la barra de escala para mantener el diseño limpio y centrado en los puntos.
    fig.update_coloraxes(showscale=False)

    # Despliegue dentro de Streamlit ajustando el grafico al ancho disponible.
    st.plotly_chart(fig, use_container_width=True)



def render_mapa_comparativo(df):
    """
    Muestra un mapa con propiedades provenientes de múltiples ciudades simultáneamente.
    Esta visualización es útil para comparar espacialmente mercados urbanos distintos,
    permitiendo identificar diferencias en densidad, zonas comerciales y patrones geográficos.
    """

    # Validación: si no existen coordenadas, no es posible dibujar el mapa.
    if "latitude" not in df or "longitude" not in df:
        st.info("No hay datos suficientes para generar un mapa comparativo.")
        return

    # Se eliminan filas con valores faltantes de latitud y longitud para evitar errores en el mapa.
    df_geo = df.dropna(subset=["latitude", "longitude"])

    # Construcción del mapa donde cada punto está asociado a una ciudad específica.
    # El color permite distinguir visualmente la procedencia urbana de cada registro.
    fig = px.scatter_mapbox(
        df_geo,
        lat="latitude",
        lon="longitude",
        color="ciudad",
        mapbox_style="open-street-map",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)



def render_mapa_turismo_transporte():
    """
    Renderiza dos mapas temáticos basados en información complementaria
    que contiene sitios turísticos y hubs de transporte.

    Su uso principal es contextualizar decisiones de alojamiento analizando
    factores como:
        - accesibilidad urbana,
        - cercanía a puntos turísticos de interés,
        - potencial atractivo del entorno.
    """

    import os

    # Se obtiene la ruta del archivo externo que contiene ubicaciones turísticas y de transporte.
    csv_path = os.path.join(os.path.dirname(__file__), '../data/tourism_transport_map_data_full.csv')
    df_map = pd.read_csv(csv_path)

    # Filtrado de filas clasificadas como sitios turísticos.
    df_tourist = df_map[df_map['Type'] == 'Tourist Spot']

    # Si existen registros turísticos, se construye un mapa específico.
    if not df_tourist.empty:
        st.markdown("#### Mapa de Sitios Turísticos")

        # Cada punto en el mapa representa un punto turístico identificado con su nombre.
        fig_tourist = px.scatter_mapbox(
            df_tourist,
            lat="Latitude",
            lon="Longitude",
            hover_name="Name",
            color="City",
            mapbox_style="carto-positron",
            height=400,
            zoom=3
        )

        st.plotly_chart(fig_tourist, use_container_width=True)
    else:
        st.info("No existen registros turísticos disponibles.")

    # Filtrado de filas clasificadas como puntos o nodos de transporte.
    df_transport = df_map[df_map['Type'] == 'Transport Hub']

    # Si existen registros, se construye un mapa con ellos.
    if not df_transport.empty:
        st.markdown("#### Mapa de Rutas y Hubs de Transporte")

        # Esta vista permite reconocer conectividad urbana y proximidad a zonas relevantes.
        fig_transport = px.scatter_mapbox(
            df_transport,
            lat="Latitude",
            lon="Longitude",
            hover_name="Name",
            color="City",
            mapbox_style="carto-positron",
            height=400,
            zoom=3
        )

        st.plotly_chart(fig_transport, use_container_width=True)
    else:
        st.info("No existen datos sobre infraestructura de transporte.")


