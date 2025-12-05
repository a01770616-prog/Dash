import streamlit as st
import pandas as pd
from utils.graficas_clustering import heatmap_clusters_airbnb
from utils.info_clustering import resumen_variables
from utils.graficas_clustering import grafica_ocupacion_stack
from utils.graficas_clustering import grafica_ranking_ciudades
from utils.graficas_clustering import graficas_experimento_2
import plotly.express as px

# Lectura del dataset completo correspondiente al experimento 2
# Se asume que este archivo contiene resultados de clustering ya procesados
df_exp2 = pd.read_csv("data/df_exp2_completo.csv")

# Normalización de variables (Z-score)
# Resta de la media y división por el estándar para escalar correctamente
df_exp2["price"] = (df_exp2["price"] - df_exp2["price"].mean()) / df_exp2["price"].std()
df_exp2["amenities_count"] = (df_exp2["amenities_count"] - df_exp2["amenities_count"].mean()) / df_exp2["amenities_count"].std()

# Renderizado de gráficas principales del experimento mediante función modular
graficas_experimento_2(df_exp2)

# Bloque superior de KPIs por clúster presentados en formato de tarjetas
st.subheader("Precios promedio por Clúster")

# Se define un layout de tres columnas
col6, col7, col8 = st.columns(3)

# Plantilla de estilo HTML reutilizable para métricas
# Se formatea con valores insertados dinámicamente
card_style = """
<div style="
    background-color: white;
    border-radius: 12px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #f1f1f1;
">
    <div style="font-size: 14px; color: #6c757d; margin-bottom: 6px;">
        {titulo}
    </div>
    <div style="font-size: 32px; font-weight: 700; color: #333;">
        {valor}
    </div>
</div>
"""

# Despliegue de las tarjetas asociadas a cada clúster
with col6:
    st.markdown(card_style.format(titulo="Ecónomico", valor="€92"), unsafe_allow_html=True)

with col7:
    st.markdown(card_style.format(titulo="Estándar", valor="€105"), unsafe_allow_html=True)

with col8:
    st.markdown(card_style.format(titulo="Premium", valor="€321"), unsafe_allow_html=True)

# Diccionarios que representan porcentajes de participación por ciudad en cada clúster
# Estructuras utilizadas para generar el heatmap comparativo
cluster_0 = {
    "Atenas": 27.8,
    "Milán": 24.1,
    "Madrid": 18.7,
    "Barcelona": 15.5,
    "Amsterdam": 13.9
}

cluster_1 = {
    "Amsterdam": 46.1,
    "Barcelona": 27.7,
    "Milán": 10.6,
    "Madrid": 8.7,
    "Atenas": 6.8
}

cluster_2 = {
    "Madrid": 25.7,
    "Barcelona": 21.4,
    "Milán": 19.7,
    "Atenas": 17.6,
    "Amsterdam": 15.6
}

data_dict = {
    "Económico": cluster_0,
    "Premium": cluster_1,
    "Estándar": cluster_2
}

# Datos de ocupación asociados a cada clúster para graficar barras apiladas
ocupacion_dict = {
    "Económico": {"Alta": 52, "Media": 16, "Baja": 32},
    "Premium": {"Alta": 37, "Media": 17, "Baja": 46},
    "Estándar": {"Alta": 42, "Media": 18, "Baja": 41},
}

# División de pantalla para visualizar heatmap y ocupación
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Heatmap")
    heatmap_clusters_airbnb(data_dict)

with col2:
    st.subheader("Barras Apiladas")
    grafica_ocupacion_stack(ocupacion_dict)

    # Panel adjunto con insights sintetizados
    col3, col4, col5 = st.columns([1, 1, 1], border=True)

    with col3:
        st.markdown('🏠Dominio del Tipo de Host')
        st.caption('Los anfitriones individuales lideran en los tres clústeres.')

    with col4:
        st.markdown('🛎️Dominio de Amenidades')
        st.caption('Clusters ecónomico y premium lideran en amenidades altas.')

    with col5:
        st.markdown('💬Mercado por Reseñas')
        st.caption('Clúster ecónomico domina en volumen de reseñas.')

# Sección para mostrar niveles de ruido (outliers detectados por DBSCAN)
st.subheader('Ruido del DBSCAN')

# Ranking de ruido agrupado por ciudad
ranking_dict = {
    "Amsterdam": 61.11,
    "Barcelona": 16.67,
    "Milán": 13.88,
    "Madrid": 5.56,
    "Atenas": 2.78
}

# Columna principal con gráfica de ranking
col9, col10 = st.columns([1.2, 1])

with col9:
    grafica_ranking_ciudades(ranking_dict)

with col10:
    colA, colB = st.columns(2, border=True)
    with colA:
        st.caption("Ámsterdam tiene más propiedades premium (**€600–€800**).")
    with colB:
        st.caption(
            'Lujo Extremo Concentrado (**100%**) Ámsterdam, Barcelona y Madrid Precios muy altos'
        )

    colC, colD = st.columns(2, border=True)
    with colC:
        st.caption('Homogeneidad en Atenas, sin rangos muy altos')
    with colD:
        st.caption('Ruido mixto en Milán: mayoría muy altos, resto altos')
    
    colE = st.columns(1, border=True)[0]
    with colE:
        st.caption('La mayoría de las propiedades premium lo son por nivel excepcional de amenidades')

# Despliegue del checklist de amenidades
st.markdown("<h4 style='margin-top: 2em;'>Checklist de Amenidades por Clúster</h4>", unsafe_allow_html=True)

# Listado de amenidades relevantes extraídas manualmente
amenidades = [
    "Wifi", "Cocina", "Calefacción", "Alarma de humo", "Secador", "Utensilios básicos de cocina",
    "Microondas", "TV", "Self check-in", "Lavavajillas", "Jacuzzi/Hot Tub",
    "Patio / Balcón", "Muebles exteriores", "Sistema de sonido"
]

# Matrices booleanas asociadas a disponibilidad por clúster
economico = [True, True, True, True, True, True, False, False, False, False, False, False, False, False]
estandar  = [True, True, True, True, True, True, True, True, True, False, False, False, False, False]
premium   = [True, True, True, True, True, True, True, True, True, True, True, True, True, True]

# Alineación visual del checklist mediante CSS
st.markdown("""
    <style>
    .centered-col-header {text-align:center !important;}
    .stCheckbox {display: flex; justify-content: center;}
    </style>
""", unsafe_allow_html=True)

# Encabezados del checklist
cols = st.columns([2, 1, 1, 1])
cols[0].markdown("<div class='centered-col-header'><b>Amenidad</b></div>", unsafe_allow_html=True)
cols[1].markdown("<div class='centered-col-header'><b>Económico</b></div>", unsafe_allow_html=True)
cols[2].markdown("<div class='centered-col-header'><b>Estándar</b></div>", unsafe_allow_html=True)
cols[3].markdown("<div class='centered-col-header'><b>Premium</b></div>", unsafe_allow_html=True)

# Renderizado dinámico del checklist fila por fila
for i, amenidad in enumerate(amenidades):
    cols = st.columns([2, 1, 1, 1])
    cols[0].markdown(f"<div style='text-align:center'>{amenidad}</div>", unsafe_allow_html=True)
    with cols[1]:
        st.checkbox("", value=economico[i], key=f"eco_{i}", disabled=True, label_visibility="collapsed")
    with cols[2]:
        st.checkbox("", value=estandar[i], key=f"est_{i}", disabled=True, label_visibility="collapsed")
    with cols[3]:
        st.checkbox("", value=premium[i], key=f"pre_{i}", disabled=True, label_visibility="collapsed")

# Separador visual previo a gráficas analíticas finales
st.markdown("---")
st.subheader("Resultados del Clustering (Price vs Amenities Count)")

# Paleta reductiva basada en colores institucionales
AIRBNB_RED = "#FF5A5F"
AIRBNB_DEEP_RED = "#FF385C"
AIRBNB_TEAL = "#00A699"

# Datos precargados equivalentes a curvas de inercia y silhouette
k_vals = list(range(2, 11))
inertia_vals = [95000, 68000, 54000, 46000, 40000, 36000, 33000, 30000, 28000]
silhouette_vals = [0.36, 0.42, 0.28, 0.34, 0.36, 0.37, 0.35, 0.32, 0.31]

df_elbow = pd.DataFrame({"k": k_vals, "inertia": inertia_vals})
df_sil = pd.DataFrame({"k": k_vals, "silhouette": silhouette_vals})

# Vista comparativa de las métricas mediante columnas
col1, col2 = st.columns(2)

# Plot de codo (curva de inercia)
with col1:
    fig_elbow = px.line(
        df_elbow,
        x="k",
        y="inertia",
        markers=True,
        title="Codo: price vs amenities_count",
        color_discrete_sequence=[AIRBNB_RED]
    )
    fig_elbow.update_traces(marker=dict(size=9, color=AIRBNB_DEEP_RED))
    fig_elbow.update_layout(
        xaxis_title="k",
        yaxis_title="Inercia",
        height=400,
        title_font=dict(size=16),
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_elbow, use_container_width=True)

# Plot silhouette comparativo
with col2:
    fig_sil = px.line(
        df_sil,
        x="k",
        y="silhouette",
        markers=True,
        title="Silhouette: price vs amenities_count",
        color_discrete_sequence=[AIRBNB_RED]
    )
    fig_sil.update_traces(marker=dict(size=9, color=AIRBNB_RED))
    fig_sil.update_layout(
        xaxis_title="k",
        yaxis_title="Silhouette",
        height=400,
        title_font=dict(size=16),
        plot_bgcolor="white"
    )
    st.plotly_chart(fig_sil, use_container_width=True)
resumen_variables()
