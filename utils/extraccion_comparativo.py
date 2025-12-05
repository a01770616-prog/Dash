import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from utils.extraccion_competitividad import (
    calcular_competitividad,
    calcular_competitividad_ciudades,
    render_barras_competitividad,
    render_scatter_competitividad
)

from utils.extraccion_mapas import render_mapa_comparativo


def render_tab_comparativo(
    df_filtered,
    selected_cities,
    Variable_Cat,
    Lista,
    top_k,
    mostrar_tabla,
    SCALE
):
    """
    Renderiza la sección de comparación entre ciudades dentro del dashboard.
    Esta vista busca contrastar resultados entre varias ciudades simultáneamente
    utilizando KPIs generales, proporciones categóricas, métricas de competitividad
    y una simulación de ROI aproximado.

    df_filtered         → DataFrame ya filtrado según criterios del usuario
    selected_cities     → Lista de ciudades elegidas
    Variable_Cat        → Columna categórica seleccionada
    Lista               → Lista completa de variables categóricas posibles
    top_k               → Cantidad máxima de categorías a mostrar
    mostrar_tabla       → Activa o desactiva visualización tabular
    SCALE               → Escala de colores usada en competitividad
    """

    # Se aísla únicamente la información de las ciudades seleccionadas,
    # esto evita cálculos innecesarios y mejora claridad de análisis.
    df_comp = df_filtered[df_filtered["ciudad"].isin(selected_cities)].copy()

    st.subheader("KPIs por ciudad")

    # Crear una pestaña específica para cada ciudad permite navegar por resultados
    # sin mezclar datos visualmente.
    tabs = st.tabs(selected_cities)

    for i, ciudad in enumerate(selected_cities):
        # Cada pestaña presentará KPIs de forma independiente
        with tabs[i]:
            df_city = df_comp[df_comp["ciudad"] == ciudad]

            colA, colB, colC, colD = st.columns(4)

            # Total de propiedades activas para la ciudad
            with colA:
                st.metric("Listings", len(df_city))

            # Precio promedio de una noche
            if "price" in df_city.columns:
                precio_promedio = df_city["price"].mean()
            else:
                precio_promedio = 0

            with colB:
                st.metric("Precio promedio", f"€{precio_promedio:,.0f}")

            # Se definen tasas aproximadas de ocupación por ciudad.
            # Estos valores son referenciales basados en reportes del mercado europeo.
            ocupacion_rates = {
                "Barcelona": 0.68,
                "Amsterdam": 0.62,
                "Milan": 0.65,
                "Athens": 0.70,
                "Atenas": 0.70,
                "Madrid": 0.67,
            }
            ocupacion = ocupacion_rates.get(ciudad, 0.65)

            with colC:
                st.metric("Ocupación Estimada", f"{ocupacion*100:.0f}%")

            # Revenue aproximado anual se calcula a partir de ingresos promedio diarios
            # multiplicado por días ocupados en el año.
            revenue_neto_estimado = precio_promedio * (ocupacion * 365)

            with colD:
                st.metric("Revenue Neto/Año", f"€{revenue_neto_estimado:,.0f}")

    st.markdown("---")

    # Se colocan dos enfoques de análisis en paralelo:
    # izquierda → distribución categórica,
    # derecha → competitividad por ciudad.
    col1, col2 = st.columns([2, 1])

    # ANÁLISIS DISTRIBUTIVO: muestra frecuencia relativa de categorías seleccionadas.
    with col1:
        st.subheader("Distribución barrios por ciudad")

        # Se crean categorías válidas reemplazando NaN usando una etiqueta explícita.
        df_comp["__cat__"] = df_comp[Variable_Cat].fillna("NA").astype(str)

        # Conteo agrupado para poder graficar en barras agrupadas
        frec = df_comp.groupby(["ciudad", "__cat__"]).size().reset_index(name="freq")

        # Mapeo manual permite diferenciación cromática por ciudad
        colores_ciudades = {
            "Amsterdam": "#1f77b4",
            "Atenas": "#2ca02c",
            "Barcelona": "#d62728",
            "Milan": "#ff7f0e",
            "Madrid": "#9467bd",
        }

        fig_cat = px.bar(
            frec,
            x="__cat__",
            y="freq",
            color="ciudad",
            barmode="group",
            height=450,
            color_discrete_map=colores_ciudades,
        )
        st.plotly_chart(fig_cat, use_container_width=True)

        # La tabla de frecuencias se muestra de forma opcional
        if mostrar_tabla:
            st.dataframe(frec, use_container_width=True)

    # ANÁLISIS COMPETITIVO: resume desempeño mediante función externa
    with col2:
        st.subheader("Competitividad Multi-Ciudad")

        comp_df = calcular_competitividad_ciudades(df_comp, selected_cities)

        # Se renderiza barra codificada por escala continua
        render_barras_competitividad(comp_df, SCALE)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align: center;'>Comparativo Multi-Ciudad ROI</h3>",
        unsafe_allow_html=True
    )

    # Entrada de usuario sobre costo operativo estimado
    col_empty1, col_input, col_empty2 = st.columns([1, 2, 1])
    with col_input:
        gastos_mensuales_input_comp = st.number_input(
            "Gastos operativos mensuales (€)",
            min_value=200,
            max_value=3000,
            value=800,
            step=50,
            key="gastos_comp_multi",
            help="Incluye mantenimiento, servicios e impuestos básicos."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Validación de al menos una ciudad seleccionada
    if len(selected_cities) == 0:
        st.warning("Selecciona al menos una ciudad para calcular ROI.")
        return

    st.markdown(
        "<h4 style='text-align: center;'>Ranking ROI por Ciudad</h4>",
        unsafe_allow_html=True
    )

    # Lista donde se almacenarán métricas comparativas por ciudad
    roi_ciudades_comp = []

    for ciudad in selected_cities:
        ciudad_data = df_comp[df_comp["ciudad"] == ciudad].copy()

        # Estimación de ingresos basada en precio promedio limpio
        if "price" in ciudad_data.columns:
            ciudad_data["price_clean"] = (
                ciudad_data["price"]
                .astype(str)
                .str.replace("$", "")
                .str.replace(",", "")
            )
            ciudad_data["price_clean"] = pd.to_numeric(
                ciudad_data["price_clean"], errors="coerce"
            )
            precio_promedio_ciudad = ciudad_data["price_clean"].mean()
        else:
            precio_promedio_ciudad = 0

        # Tasas aproximadas de ocupación para estimaciones de mercado
        ocupacion_rates = {
            "Barcelona": 0.68,
            "Amsterdam": 0.62,
            "Milan": 0.65,
            "Athens": 0.70,
            "Atenas": 0.70,
            "Madrid": 0.67,
        }

        ocupacion_pct_ciudad = ocupacion_rates.get(ciudad, 0.65) * 100
        dias_ocupados_ciudad = (ocupacion_pct_ciudad / 100) * 365

        revenue_bruto_ciudad = precio_promedio_ciudad * dias_ocupados_ciudad

        # Descuentos estimados por comisiones
        comision_airbnb = revenue_bruto_ciudad * 0.15
        costos_limpieza = revenue_bruto_ciudad * 0.05

        revenue_neto_ciudad = revenue_bruto_ciudad - comision_airbnb - costos_limpieza

        # Costos operativos fijos ingresados por usuario
        gastos_operativos_ciudad = gastos_mensuales_input_comp * 12

        # Utilidad neta anual resultante
        ganancia_neta_ciudad = revenue_neto_ciudad - gastos_operativos_ciudad

        # Costos iniciales estimados por ciudad (setting cost)
        setup_costs = {
            "Barcelona": 8000,
            "Amsterdam": 12000,
            "Milan": 7000,
            "Athens": 5000,
            "Atenas": 5000,
            "Madrid": 6500,
        }
        inversion_inicial = setup_costs.get(ciudad, 7000) + (gastos_mensuales_input_comp * 8)

        # Indicador comparativo de rendimiento
        # ROI = utilidad / inversión inicial
        if inversion_inicial > 0:
            roi_ciudad = ganancia_neta_ciudad / inversion_inicial * 100
        else:
            roi_ciudad = 0

        roi_ciudades_comp.append(
            {
                "Ciudad": ciudad,
                "Precio_Promedio": precio_promedio_ciudad,
                "Ocupacion_Pct": ocupacion_pct_ciudad,
                "Dias_Ocupados": dias_ocupados_ciudad,
                "Revenue_Bruto": revenue_bruto_ciudad,
                "Revenue_Neto": revenue_neto_ciudad,
                "Inversion_Inicial": inversion_inicial,
                "Ganancia_Neta": ganancia_neta_ciudad,
                "ROI": roi_ciudad,
            }
        )

    # Orden descendente de mayor a menor desempeño financiero
    roi_ciudades_comp.sort(key=lambda x: x["ROI"], reverse=True)




    # Despliegue por ciudad con layout alineado a la izquierda y ancho completo


    st.markdown("<div style='max-width:900px;margin:0 auto;'>", unsafe_allow_html=True)
    for rank, ciudad_roi in enumerate(roi_ciudades_comp):
        st.markdown("<div style='display:flex;align-items:flex-start;justify-content:center;margin-bottom:8px;width:100%;'>", unsafe_allow_html=True)
        # Centro: ranking, nombre y ROI badge
        st.markdown(f"<div style='min-width:220px;text-align:center;'>"
                    f"<div style='font-size:1.35rem;font-weight:700;margin-bottom:2px;'>#{rank+1}: {ciudad_roi['Ciudad']}</div>"
                    f"<span style='background:#e3f0ff;color:#1976d2;padding:6px 22px;border-radius:8px;font-weight:600;display:inline-block;margin-top:8px;font-size:1.08rem;'>ROI: {ciudad_roi['ROI']:.1f}%</span>"
                    f"</div>", unsafe_allow_html=True)
        # Métricas centradas
        st.markdown(f"<div style='display:flex;gap:64px;justify-content:center;margin-left:32px;'>"
                    f"<div style='text-align:center;'><div style='font-size:1.12rem;color:#888;margin-bottom:2px;'>Ganancia Neta/Año</div><div style='font-size:1.7rem;font-weight:700;'>€{ciudad_roi['Ganancia_Neta']:,.0f}</div></div>"
                    f"<div style='text-align:center;'><div style='font-size:1.12rem;color:#888;margin-bottom:2px;'>Revenue Neto</div><div style='font-size:1.7rem;font-weight:700;'>€{ciudad_roi['Revenue_Neto']:,.0f}</div></div>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        # Detalles debajo, centrados
        st.markdown(f"<div style='color:#888;font-size:0.99rem;margin:6px 0 0 0;text-align:center;'>"
                    f"Precio promedio: €{ciudad_roi['Precio_Promedio']:.0f}/noche | Ocupación: {ciudad_roi['Ocupacion_Pct']:.0f}% ({ciudad_roi['Dias_Ocupados']:.0f} días/año)"
                    f"</div>", unsafe_allow_html=True)
        # Separador horizontal
        st.markdown("<hr style='margin:18px 0 22px 0;border:0;border-top:1px solid #eee;'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

