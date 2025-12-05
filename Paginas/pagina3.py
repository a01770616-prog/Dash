import streamlit as st
import pandas as pd
import plotly.express as px
from utils.utils_datos import load_data
from utils.utils_filtros import filtros_ciudad_barrios_precios


# Título principal del módulo.
# Esta sección específica del dashboard tiene como objetivo permitir la exploración
# de barrios dentro de una ciudad previamente seleccionada, dando relevancia a:
# · precios
# · reputación del host
# · rating promedio
# · concentración de reseñas
# · tipo de alojamiento predominante
# · patrones geográficos
st.title('Explorador de Barrios')


# Paletas de color alineadas a la identidad visual utilizada en todo el dashboard.
# Cada color se aplicará principalmente a barras, indicadores y densidades.
# La paleta define intensidades relacionadas con desempeño o atractivo residencial.
AIRBNB_COMPETITIVENESS_SCALE = [
    "#FF7A85",  # Nivel medio de competitividad
    "#FF5A5F",  # Color principal institucional
    "#FF385C",  # Máxima intensidad llamativa
    "#FFB400",  # Colores alternos Airbnb
    "#00A699",
    "#FC642D",
]

# Paleta especial para métricas asociadas a reputación o rating.
rating = [
    "#FFB400",  # Alto y confiable
    "#00A699",  # Promedio aceptable
    "#FC642D",  # Riesgo o bajo desempeño
]


# Por defecto se aplican estilos generales a plotly para que todas sus gráficas
# mantengan coherencia visual sin tener que redefinir estilos en cada gráfico.
px.defaults.color_discrete_sequence = AIRBNB_COMPETITIVENESS_SCALE
px.defaults.template = "plotly_white"


# Función auxiliar para optimización visual de los gráficos más pequeños.
# Se reducen márgenes para permitir disposición eficiente dentro de columnas.
def compact(fig):
    fig.update_layout(
        height=260,
        margin=dict(l=0, r=0, t=25, b=0),
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig


# Carga de información ya consolidada.
# load_data:
# - lee los archivos desde carpeta /data
# - valida existencia de columnas esenciales
# - devuelve el DataFrame y advertencias (si hubo problemas)
df, warns = load_data()

# Si el sistema detectó avisos relevantes al cargar los datos,
# se muestran para mantener transparencia en el análisis.
for w in warns:
    st.warning(w)


# Validaciones críticas antes de operar sobre el dataset.
# Se realizan temprano para evitar errores posteriores.
if df.empty:
    st.error("No hay datos de Airbnb.")
    st.stop()

if "ciudad" not in df.columns:
    st.error("No existe la columna 'ciudad' en los datos.")
    st.stop()


# Se solicita al usuario:
# · ciudad
# · barrios representativos
# · umbral de precios
# La función devuelve el subconjunto filtrado listo para análisis visual.
ciudad_sel, barrios_sel, rango_precios, df_city = filtros_ciudad_barrios_precios(df)


# Distribución de la interfaz en dos secciones:
# Izquierda → tablas resumidas con indicadores comparativos
# Derecha   → gráficas reforzando hallazgos
col_left, col_right = st.columns([2, 5])


# BLOQUE IZQUIERDO
# Ranking de barrios basado en distintas variables agregadas
with col_left:

    st.markdown("#### Ranking de barrios")

    # Se agregan métricas consolidadas a nivel de barrio,
    # esto permite análisis estadístico y comparativo inmediato.
    agr = (
        df_city.groupby("barrio_std", dropna=True)
        .agg(
            listings=("id", "count"),            # mide disponibilidad y oferta
            price_mean=("price", "mean"),        # disposición a pagar
            rating_mean=("review_scores_rating", "mean"),  # reputación
            reviews_mean=("number_of_reviews_ltm", "mean"),     # relevancia histórica
            amenities_mean=("amenities_count", "mean"),      # atractivo y nivel de servicio
        )
        .reset_index()
    )

    # Solo se continúa si hay datos
    if agr.empty:
        st.info("No hay suficientes datos para calcular el ranking de barrios.")
    else:
        # El usuario puede elegir el criterio de ordenamiento:
        # · rating medio (preferencia/hospitalidad)
        # · precio (estatus económico)
        # · cantidad de alojamientos (relevancia territorial)
        criterio = st.selectbox(
            "Ordenar por",
            ["Rating medio", "Precio medio", "N.º de listings"],
            index=0,
        )

        if criterio == "Rating medio":
            agr = agr.sort_values("rating_mean", ascending=False)

        elif criterio == "Precio medio":
            agr = agr.sort_values("price_mean", ascending=False)

        else:
            agr = agr.sort_values("listings", ascending=False)

        # Se presenta tabla ordenada y redondeada para lectura rápida
        st.dataframe(
            agr.round(
                {
                    "price_mean": 2,
                    "rating_mean": 2,
                    "reviews_mean": 1,
                    "amenities_mean": 1,
                }
            ),
            use_container_width=True,
        )


# BLOQUE DERECHO
# Aquí se despliegan varios análisis visuales complementarios
with col_right:

    if not agr.empty:

        g1, g3 = st.columns([1, 1])

        # Gráfico de barras que permite identificar
        # patrones de renta por zona
        with g1:

            st.markdown("<div style='text-align:center; font-weight:bold;'>Precio medio por barrio</div>", unsafe_allow_html=True)

            top_price = agr.sort_values("price_mean", ascending=False)

            fig = px.bar(
                top_price,
                x="barrio_std",
                y="price_mean",
                height=350,
                color_discrete_sequence=AIRBNB_COMPETITIVENESS_SCALE
            )

            fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
            fig.update_xaxes(title="Barrio")
            fig.update_yaxes(title="Precio medio (€)")
            st.plotly_chart(fig, use_container_width=True)


        # Distribución por tipo de habitación
        # Útil para ver:
        # · predominancia de habitaciones privadas
        # · enfoque turístico tipo hotel-apartamento
        with g3:
            if "room_type" in df_city.columns:

                st.markdown("<div style='text-align:center; font-weight:bold;'>Room types en barrios seleccionados</div>", unsafe_allow_html=True)

                rt = df_city["room_type"].value_counts().reset_index()
                rt.columns = ["room_type", "count"]

                if not rt.empty:
                    fig = px.pie(
                        rt,
                        names="room_type",
                        values="count",
                        hole=0.4,
                        height=350,
                        color_discrete_sequence=AIRBNB_COMPETITIVENESS_SCALE
                    )

                    fig.update_traces(textinfo='percent+label')
                    fig.update_layout(legend_title_text="Tipo de habitación")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No hay room types disponibles para estos filtros.")
            else:
                st.info("No existe la columna 'room_type' en los datos.")


# Gráfico de dispersión cruzando:
# precio vs rating
# tamaño de punto = amenidades
st.caption("Relación precio vs rating por barrio (listings filtrados)")

if {"price", "review_scores_rating", "barrio_std"}.issubset(df_city.columns):

    scatter_df = df_city.dropna(subset=["price", "review_scores_rating", "barrio_std"])

    if not scatter_df.empty:
        fig = px.scatter(
            scatter_df,
            x="price",
            y="review_scores_rating",
            color="barrio_std",
            size="amenities_count"
        )
        fig = compact(fig)
        fig.update_xaxes(title="Precio (€)")
        fig.update_yaxes(title="Rating")
        st.plotly_chart(fig, use_container_width=True)


# Módulo de reputación
# Clasificación usando reglas híbridas basadas en rating + número de reseñas acumuladas
st.markdown("### Reputación en barrios seleccionados")

if {"review_scores_rating", "number_of_reviews_ltm"}.issubset(df_city.columns):

    rep_df = df_city.dropna(subset=["review_scores_rating", "number_of_reviews_ltm"]).copy()

    if not rep_df.empty:

        # Reglas:
        # Top host → rating alto y volumen mínimo
        cond_top = (rep_df["review_scores_rating"] >= 4.8) & (rep_df["number_of_reviews_ltm"] >= 30)

        # Riesgoso → rating bajo o sin historial de reseñas
        cond_risk = (rep_df["review_scores_rating"] < 4.3) | (rep_df["number_of_reviews_ltm"] < 5)

        rep_df["categoria_reputacion"] = "Normal"
        rep_df.loc[cond_top, "categoria_reputacion"] = "Top host"
        rep_df.loc[cond_risk, "categoria_reputacion"] = "Riesgoso"

        c1, c2 = st.columns([1, 1])

        with c1:
            cat_counts = (
                rep_df["categoria_reputacion"]
                .value_counts(normalize=True)
                .mul(100)
                .round(1)
                .reset_index()
            )
            cat_counts.columns = ["categoria", "porcentaje"]

            fig = px.bar(
                cat_counts,
                x="categoria",
                y="porcentaje",
                text="porcentaje",
                color="categoria",
                height=350
            )
            fig.update_traces(texttemplate="%{text}%")
            st.plotly_chart(fig, use_container_width=True)


        with c2:
            fig = px.scatter(
                rep_df,
                x="number_of_reviews_ltm",
                y="review_scores_rating",
                color="categoria_reputacion",
                size="amenities_count",
                size_max=10,
                color_discrete_sequence=rating,
                height=350
            )
            fig.update_xaxes(title="Número de reviews")
            fig.update_yaxes(title="Rating")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay puntos suficientes para evaluación de reputación.")
else:
    st.info("Faltan columnas para generar reputación.")
