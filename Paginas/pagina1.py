import streamlit as st
import pandas as pd

import plotly.express as px
from utils.utils_datos import load_data


# Título principal de la página
# Indica que se mostrarán indicadores globales del dataset completo
st.title('KPIs Globales')


# Función auxiliar que ajusta las figuras para ocupar menos espacio vertical
# Ideal para filas de 3 gráficos lado a lado
def compact(fig):
    fig.update_layout(
        height=260,                     # altura reducida
        margin=dict(l=0, r=0, t=25, b=0)  # márgenes más pequeños
    )
    fig.update_xaxes(title=None)        # oculta etiquetas del eje X
    fig.update_yaxes(title=None)        # oculta etiquetas del eje Y
    return fig


# Paleta de color corporativa adaptada del branding de Airbnb
AIRBNB_COMPETITIVENESS_SCALE = [
    "#FF7A85",  # intensidad media
    "#FF5A5F",  # color institucional fuerte
    "#FF385C"   # variante protagonista
]

# Configuración de colores por defecto para todas las gráficas
px.defaults.color_discrete_sequence = AIRBNB_COMPETITIVENESS_SCALE
px.defaults.template = "plotly_white"


# Importación del DataFrame principal y posibles advertencias generadas en la carga
df, warns = load_data()
# Solo mostrar advertencias si existen y no están vacías
for w in warns:
    if w:
        st.warning(w)

# Si no hay datos válidos, la ejecución se detiene
if df.empty:
    st.error("No hay datos de Airbnb disponible.")
    st.stop()


# División de la interfaz en dos secciones:
# columna izquierda → métricas
# columna derecha → gráficos comparativos
col_left, col_right = st.columns([1, 5])


# Ajustes visuales adicionales vía CSS para mejorar orden y alineación
st.markdown("""
    <style>
    .kpi-col {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 100%;
    }
    .charts-col {
        margin-top: 2.5rem;
    }
    </style>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 5], gap="large")


# Panel izquierdo con KPIs principales del dataset
with col_left:
    st.markdown('<div class="kpi-col">', unsafe_allow_html=True)

    st.markdown("#### Resumen")

    # Ajuste para centrar los KPIs visualmente
    st.markdown("""
        <style>
        div[data-testid='stMetric'] {
            text-align: center !important;
        }
        div[data-testid='stMetric'] > label, div[data-testid='stMetric'] > div {
            width: 100%;
            justify-content: center;
            text-align: center !important;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Lista de métricas calculadas en todo el dataset
    kpi_labels = [
        ("Listings", len(df)),  # número total de propiedades en el dataset
        ("€Precio medio", f"{df['price'].mean():.2f}" if "price" in df else "N/A"),
        ("Rating medio", f"{df['review_scores_rating'].mean():.2f}" if "review_scores_rating" in df else "N/A"),
        ("€ por persona", f"{df['price_per_person'].mean():.2f}" if "price_per_person" in df else "N/A"),
    ]

    # Cálculo de porcentaje de superhosts solo si existe dicha columna
    if "host_is_superhost" in df.columns:
        pct_superhost = (
            100 *
            df["host_is_superhost"]
            .astype(str)
            .str.lower()
            .str.strip()
            .eq('t')
            .mean()
        )
        kpi_labels.append(("% Superhosts", f"{pct_superhost:.1f}%"))
    else:
        kpi_labels.append(("% Superhosts", "N/A"))

    # Renderizado individual de los KPIs
    for label, value in kpi_labels:
        with st.container(border=True):
            st.metric(label, value)

    st.markdown('</div>', unsafe_allow_html=True)


# Panel derecho con visualizaciones de distribución y comportamiento global
with col_right:
    st.markdown('<div class="charts-col">', unsafe_allow_html=True)

    chart_height = 260  # tamaño estándar de gráficas

    # Primera fila de visualizaciones comparativas por ciudad
    c11, c12, c13 = st.columns([1, 1, 1])

    # Gráfico 1: Precio promedio por ciudad
    with c11:
        if {"ciudad", "price"}.issubset(df.columns):
            st.markdown(
                "<div style='text-align:center; font-weight:bold;'>Precio medio por ciudad</div>",
                unsafe_allow_html=True
            )
            precio_ciudad = (
                df.groupby("ciudad")["price"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
            )
            precio_ciudad["ciudad"] = precio_ciudad["ciudad"].replace({
                "Amsterdam": "Ámsterdam",
                "Milan": "Milán"
            })

            fig = px.bar(precio_ciudad, x="ciudad", y="price", height=chart_height)
            fig = compact(fig)
            fig.update_xaxes(title="Ciudad")
            fig.update_yaxes(title="Precio medio (€)")
            st.plotly_chart(fig, use_container_width=True, key="precio_ciudad")

    # Gráfico 2: Participación porcentual de listings por ciudad
    with c12:
        if "ciudad" in df.columns:
            st.markdown(
                "<div style='text-align:center; font-weight:bold;'>Participación de listings por ciudad</div>",
                unsafe_allow_html=True
            )
            counts_ciudad = (
                df["ciudad"]
                .replace({"Amsterdam": "Ámsterdam", "Milan": "Milán"})
                .value_counts()
                .reset_index()
            )
            counts_ciudad.columns = ["ciudad", "count"]

            fig = px.pie(
                counts_ciudad,
                names="ciudad",
                values="count",
                hole=0.5,
                height=chart_height,
                color_discrete_sequence=[
                    "#FF7A85", "#FF5A5F", "#FF385C",
                    "#FFB400", "#00A699", "#FC642D"
                ]
            )
            fig = compact(fig)
            fig.update_traces(textinfo='percent+label')
            fig.update_layout(legend_title_text="Ciudad")
            st.plotly_chart(fig, use_container_width=True, key="participacion_ciudad")

    # Gráfico 3: Rating promedio por ciudad
    with c13:
        if {"ciudad", "review_scores_rating"}.issubset(df.columns):
            st.markdown(
                "<div style='text-align:center; font-weight:bold;'>Rating medio por ciudad</div>",
                unsafe_allow_html=True
            )
            rat_ciudad = (
                df.dropna(subset=["review_scores_rating"])
                .groupby("ciudad")["review_scores_rating"]
                .mean()
                .sort_values()
                .reset_index()
            )
            rat_ciudad["ciudad"] = rat_ciudad["ciudad"].replace({
                "Amsterdam": "Ámsterdam",
                "Milan": "Milán"
            })

            fig = px.bar(
                rat_ciudad, x="review_scores_rating", y="ciudad",
                orientation="h", height=chart_height
            )
            fig = compact(fig)
            fig.update_xaxes(title="Rating medio")
            fig.update_yaxes(title="Ciudad")
            st.plotly_chart(fig, use_container_width=True, key="rating_ciudad")

    # Segunda fila: relación de métricas con capacidad de hospedaje
    c21, c22, c23 = st.columns(3)

    # Gráfico 4: Precio promedio según capacidad
    with c21:
        if {"accommodates", "price"}.issubset(df.columns):
            st.markdown(
                "<div style='text-align:center; font-weight:bold;'>Precio medio según capacidad</div>",
                unsafe_allow_html=True
            )
            grp_p = (
                df.groupby("accommodates")["price"]
                .mean()
                .sort_index()
                .reset_index()
            )
            grp_p = grp_p[grp_p["accommodates"] <= 8]

            fig = compact(px.line(grp_p, x="accommodates", y="price"))
            fig.update_xaxes(title="Capacidad (personas)")
            fig.update_yaxes(title="Precio medio (€)")
            st.plotly_chart(fig, use_container_width=True, key="precio_capacidad")

    # Gráfico 5: Rating promedio por capacidad
    with c22:
        if {"accommodates", "review_scores_rating"}.issubset(df.columns):
            st.markdown(
                "<div style='text-align:center; font-weight:bold;'>Rating medio según capacidad</div>",
                unsafe_allow_html=True
            )
            grp_r = (
                df.dropna(subset=["review_scores_rating"])
                .groupby("accommodates")["review_scores_rating"]
                .mean()
                .sort_index()
                .reset_index()
            )
            grp_r = grp_r[grp_r["accommodates"] <= 8]

            fig = compact(px.line(grp_r, x="accommodates", y="review_scores_rating"))
            fig.update_xaxes(title="Capacidad (personas)")
            fig.update_yaxes(title="Rating medio")
            st.plotly_chart(fig, use_container_width=True, key="rating_capacidad")

    # Gráfico 6: Distribución global de tipos de habitación
    with c23:
        if "room_type" in df.columns:
            st.markdown(
                "<div style='text-align:center; font-weight:bold;'>Room types (global)</div>",
                unsafe_allow_html=True
            )
            rt = df["room_type"].value_counts().reset_index()
            rt.columns = ["room_type", "count"]

            fig = compact(px.bar(rt, x="room_type", y="count"))
            fig.update_xaxes(title="Tipo de habitación")
            fig.update_yaxes(title="Cantidad de listings")
            st.plotly_chart(fig, use_container_width=True, key="room_types_global")

    st.markdown('</div>', unsafe_allow_html=True)



