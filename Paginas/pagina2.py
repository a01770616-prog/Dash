import streamlit as st
import pandas as pd
import plotly.express as px
from utils.utils_datos import load_data
import plotly.express as px


st.title('KPIs Por Ciudades')

AIRBNB_COMPETITIVENESS_SCALE = [ 
    "#FF7A85",  # Medio
    "#FF5A5F",  # Medio alto (brand_alt)
    "#FF385C"   # Alto (brand principal)
]

px.defaults.color_discrete_sequence = AIRBNB_COMPETITIVENESS_SCALE
px.defaults.template = "plotly_white"

df, warns = load_data()
for w in warns:
    st.warning(w)

if df.empty:
    st.error("No hay datos de Airbnb. Revisa los archivos CSV en la carpeta 'data'.")
    st.stop()

if "ciudad" not in df.columns:
    st.error("No existe la columna 'ciudad' en los datos.")
    st.stop()

ciudades_originales = sorted(df["ciudad"].dropna().unique().tolist())
ciudades_labels = [c.replace("Amsterdam", "Ámsterdam").replace("Milan", "Milán") for c in ciudades_originales]
if not ciudades_labels:
    st.warning("No se encontraron ciudades.")
    st.stop()

def compact(fig):
    fig.update_layout(
        height=260,
        margin=dict(l=0, r=0, t=25, b=0),
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig

tabs = st.tabs(ciudades_labels)

for i, (tab, ciudad_label, ciudad_original) in enumerate(zip(tabs, ciudades_labels, ciudades_originales)):
    with tab:
        df_city = df[df["ciudad"] == ciudad_original].copy()
        if df_city.empty:
            st.info(f"Sin datos para {ciudad_label}.")
            st.stop()
        # KPIs por ciudad en fila horizontal (como antes)
        # Título eliminado, solo KPIs centrados
        # KPIs y gráficas juntos en la parte superior
        # KPIs y gráficas principales en la misma fila
        col_kpi, col_graficas = st.columns([2, 6], gap="large")
        with col_kpi:
            st.markdown('<div class="kpi-col">', unsafe_allow_html=True)
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
            kpi_labels = [
                ("Listings", len(df_city)),
                ("€Precio medio", f"{df_city['price'].mean():.2f}" if "price" in df_city.columns else "N/A"),
                ("Rating medio", f"{df_city['review_scores_rating'].mean():.2f}" if "review_scores_rating" in df_city.columns else "N/A"),
                ("€ por persona", f"{df_city['price_per_person'].mean():.2f}" if "price_per_person" in df_city.columns else "N/A"),
            ]
            if "host_is_superhost" in df_city.columns:
                pct_superhost = 100 * df_city["host_is_superhost"].astype(str).str.lower().str.strip().eq('t').mean()
                kpi_labels.append(("% Superhosts", f"{pct_superhost:.1f}%"))
            else:
                kpi_labels.append(("% Superhosts", "N/A"))
            for label, value in kpi_labels:
                with st.container(border=True):
                    st.metric(label, value)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_graficas:
            st.markdown("#### Análisis de capacidad y rating")
            # Gráficas principales alineadas a la derecha de los KPIs
            col1, col2, col3 = st.columns(3)
            # 1. Precio medio por capacidad
            with col1:
                if "accommodates" in df_city.columns and "price" in df_city.columns:
                    all_caps = pd.Series(range(int(df_city["accommodates"].min()), int(df_city["accommodates"].max())+1))
                    precio_cap = df_city.groupby("accommodates")["price"].mean().reindex(all_caps).reset_index()
                    precio_cap.columns = ["accommodates", "price"]
                    if ciudad_original.lower() == "amsterdam":
                        precio_cap["price"] = precio_cap["price"].interpolate(method="linear")
                    fig_precio_cap = px.line(precio_cap, x="accommodates", y="price", markers=True, title="Precio medio según capacidad")
                    fig_precio_cap.update_traces(line_color="#FF5A5F")
                    fig_precio_cap.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
                    fig_precio_cap.update_xaxes(title="Capacidad")
                    fig_precio_cap.update_yaxes(title="Precio medio (€)")
                    st.plotly_chart(fig_precio_cap, use_container_width=True, key=f"precio_cap_{ciudad_original}_top")
                else:
                    st.info("No hay datos suficientes para precio por capacidad.")
            # 2. Rating medio por capacidad
            with col2:
                if "accommodates" in df_city.columns and "review_scores_rating" in df_city.columns:
                    rating_cap = df_city.groupby("accommodates")["review_scores_rating"].mean().reset_index()
                    fig_rating_cap = px.line(rating_cap, x="accommodates", y="review_scores_rating", markers=True, title="Rating medio según capacidad")
                    fig_rating_cap.update_traces(line_color="#FF7A85")
                    fig_rating_cap.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
                    fig_rating_cap.update_xaxes(title="Capacidad")
                    fig_rating_cap.update_yaxes(title="Rating medio")
                    st.plotly_chart(fig_rating_cap, use_container_width=True, key=f"rating_cap_{ciudad_original}_top")
                else:
                    st.info("No hay datos suficientes para rating por capacidad.")
            # 3. Relación precio vs rating
            with col3:
                if "price" in df_city.columns and "review_scores_rating" in df_city.columns:
                    fig_precio_rating = px.scatter(df_city, x="price", y="review_scores_rating", opacity=0.5, color_discrete_sequence=["#FF385C"])
                    fig_precio_rating.update_traces(marker=dict(size=6))
                    fig_precio_rating.update_layout(title="Relación precio vs rating", height=250, margin=dict(l=10, r=10, t=40, b=10))
                    fig_precio_rating.update_xaxes(title="Precio (€)")
                    fig_precio_rating.update_yaxes(title="Rating")
                    st.plotly_chart(fig_precio_rating, use_container_width=True, key=f"precio_rating_{ciudad_original}_top")
                else:
                    st.info("No hay datos suficientes para relación precio-rating.")
            # Gráficas adicionales debajo de las principales
            g1, g2 = st.columns(2)
            chart_height = 350
            # 1) Precio medio por barrio
            with g1:
                st.markdown("<div style='text-align:center; font-weight:bold;'>Precio medio por barrio</div>", unsafe_allow_html=True)
                agr = df_city.groupby("barrio_std", dropna=True).agg(
                    listings=("id", "count"),
                    price_mean=("price", "mean"),
                    rating_mean=("review_scores_rating", "mean"),
                    reviews_mean=("number_of_reviews_ltm", "mean"),
                    amenities_mean=("amenities_count", "mean"),
                ).reset_index()
                top_price = agr.sort_values("price_mean", ascending=False)
                fig = px.bar(top_price, x="barrio_std", y="price_mean", height=chart_height)
                fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
                fig.update_xaxes(title="Barrio")
                fig.update_yaxes(title="Precio medio (€)")
                st.plotly_chart(fig, use_container_width=True, key=f"barrios_{ciudad_original}")
            # 2) Room types en barrios seleccionados
            with g2:
                if "room_type" in df_city.columns:
                    st.markdown("<div style='text-align:center; font-weight:bold;'>Room types en barrios seleccionados</div>", unsafe_allow_html=True)
                    rt = df_city["room_type"].value_counts().reset_index()
                    rt.columns = ["room_type", "count"]
                    if not rt.empty:
                        fig = px.pie(rt, names="room_type", values="count", hole=0.4, height=chart_height, color_discrete_sequence=["#FF7A85", "#FF5A5F", "#FF385C", "#FFB400", "#00A699", "#FC642D"])
                        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), legend=dict(font=dict(size=14), orientation="h", y=-0.2))
                        fig.update_traces(textinfo='percent+label')
                        fig.update_layout(legend_title_text="Tipo de habitación")
                        st.plotly_chart(fig, use_container_width=True, key=f"roomtypes_{ciudad_original}")
                    else:
                        st.info("No hay room types disponibles para estos filtros.")
                else:
                    st.info("No existe la columna 'room_type' en los datos.")



        # --- MAPA DE SUPERHOSTS (al final) ---
        st.markdown("---")
        superhost_container = st.container()
        with superhost_container:
            if {"latitude", "longitude", "host_is_superhost"}.issubset(df_city.columns):
                df_geo_superhost = df_city[df_city["host_is_superhost"].astype(str).str.lower().str.strip() == 't'].copy()
                # Filtrar valores nulos en lat/lon
                df_geo_superhost = df_geo_superhost.dropna(subset=["latitude", "longitude"])
                # Rango específico por ciudad para evitar filtrar todo por error
                if ciudad_original.lower() == "amsterdam":
                    df_geo_superhost = df_geo_superhost[(df_geo_superhost["latitude"].between(52.2, 52.5)) & (df_geo_superhost["longitude"].between(4.7, 5.1))]
                elif ciudad_original.lower() == "milan":
                    df_geo_superhost = df_geo_superhost[(df_geo_superhost["latitude"].between(45.3, 45.6)) & (df_geo_superhost["longitude"].between(9.0, 9.4))]
                # Para otras ciudades, solo filtrar nulos
                if len(df_geo_superhost) == 0:
                    st.warning("No hay superhosts para mostrar en el mapa.")
                else:
                    hover_superhost = {}
                    if "barrio_std" in df_geo_superhost.columns:
                        hover_superhost["barrio_std"] = True
                    if "price" in df_geo_superhost.columns:
                        hover_superhost["price"] = True
                    fig_map = px.scatter_mapbox(
                        df_geo_superhost, lat="latitude", lon="longitude",
                        color="host_is_superhost",
                        hover_name="barrio_std" if "barrio_std" in df_geo_superhost.columns else None,
                        hover_data=hover_superhost,
                        mapbox_style="carto-positron",
                        title=f"Distribución Geográfica de Superhosts - {ciudad_label} ({len(df_geo_superhost):,} puntos)",
                        height=500
                    )
                    # Forzar centro y zoom si hay datos
                    if not df_geo_superhost.empty:
                        lat_center = df_geo_superhost["latitude"].mean()
                        lon_center = df_geo_superhost["longitude"].mean()
                        fig_map.update_layout(mapbox_center={"lat": lat_center, "lon": lon_center}, mapbox_zoom=12)
                        fig_map.update_traces(marker=dict(size=9, opacity=0.7))
                    st.plotly_chart(fig_map, use_container_width=True, key=f"tab{i}_map_{ciudad_label}_main")
            else:
                st.info("No hay información de superhosts para mostrar en el mapa.")

        # División para contenido adicional
        st.markdown("<div id='extra-content'></div>", unsafe_allow_html=True)




        






