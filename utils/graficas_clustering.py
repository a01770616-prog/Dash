import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


# Paleta de colores basada en branding institucional de Airbnb.
# Se utiliza en gradientes y asignación por categorías.
AIRBNB_COLORS = [
    "#FFE6EA",
    "#FFB6C1",
    "#FF8FA3",
    "#FF5A5F",
    "#E0004D",
    "#B0003A"
]


def heatmap_clusters_airbnb(data_dict):
    """
    Construye un heatmap que evidencia la distribución porcentual de cada clúster en cada ciudad.
    El objetivo es visualizar de forma matricial qué clúster predomina en cada región.

    Parámetro
    data_dict: diccionario estructurado como:
        {
            "Económico": {"Ciudad1": %, "Ciudad2": %, ...},
            "Premium": {...},
            "Estándar": {...}
        }

    La función transforma dicha estructura en un DataFrame y posteriormente
    reorganiza sus dimensiones para construir la matriz utilizada por px.imshow.
    """

    filas = []

    # Transformación del diccionario a formato tabular compatible con DataFrame.
    # Se genera una fila por cada combinación ciudad–clúster.
    for cluster_name, valores in data_dict.items():
        for ciudad, porcentaje in valores.items():
            filas.append({
                "Cluster": cluster_name,
                "Ciudad": ciudad,
                "Porcentaje (%)": porcentaje
            })

    df = pd.DataFrame(filas)

    # Se definen categorías ordenadas para asegurar consistencia visual.
    ciudades_orden = ["Amsterdam", "Atenas", "Barcelona", "Madrid", "Milán"]
    clusters_orden = ["Económico", "Premium", "Estándar"]

    df["Ciudad"] = pd.Categorical(df["Ciudad"], ciudades_orden)
    df["Cluster"] = pd.Categorical(df["Cluster"], clusters_orden)

    # Reagrupamiento a formato matriz para mapa de calor.
    matriz = df.pivot(index="Ciudad", columns="Cluster", values="Porcentaje (%)")

    # Visualización tipo mapa de calor con anotaciones de porcentaje dentro de cada celda.
    fig = px.imshow(
        matriz,
        text_auto=".1f",  # Representación numérica con un decimal
        aspect="auto",
        color_continuous_scale=AIRBNB_COLORS,
        title="Distribución por Ciudad y Clúster"
    )

    # Ajustes visuales: márgenes, ocultamiento de fondos, escalas y estilo general.
    fig.update_layout(
        height=560,
        margin=dict(t=80, l=60, r=60, b=60),
        font=dict(size=14),
        coloraxis_colorbar=dict(title="%"),
        paper_bgcolor="rgba(0,0,0,0)",   # Transparencia para compatibilidad con modo dark
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)



def grafica_ocupacion_stack(data_dict):
    """
    Construye una representación horizontal apilada que permite observar los niveles
    de ocupación predominantes (alta, media o baja) dentro de cada clúster.

    Ejemplo de entrada:
        {
            "Cluster 0": {"Alta": 52, "Media": 16, "Baja": 32},
            ...
        }

    El agrupamiento por densidad refleja situaciones de demanda diferenciada,
    tendencia de reservas y comportamiento de temporalidad.
    """

    categorias = ["Alta", "Media", "Baja"]

    # Se asignan colores específicos para destacar por nivel de ocupación.
    colores_airbnb = {
        "Alta": "#FF385C",
        "Media": "#FFB3BA",
        "Baja": "#E2E8F0"
    }

    fig = go.Figure()

    # Cada trace representa una categoría de ocupación dentro
    # de todos los clústeres disponibles.
    for cat in categorias:
        fig.add_trace(go.Bar(
            x=[data_dict[c][cat] for c in data_dict.keys()],
            y=list(data_dict.keys()),
            name=cat,
            orientation='h',
            text=[f"{data_dict[c][cat]}%" for c in data_dict.keys()],
            textposition="inside",
            marker_color=colores_airbnb[cat],
        ))

    fig.update_layout(
        barmode='stack',  # Define apilamiento horizontal
        title="Distribución de Ocupación por Clúster",
        height=320,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2  # Ubica la leyenda debajo de la gráfica
        ),
        xaxis=dict(title="Porcentaje (%)"),
        yaxis=dict(title="Cluster"),
        font=dict(size=14)
    )

    st.plotly_chart(fig, use_container_width=True)



def stacked_bars_ocupacion(data_dict):
    """
    Variante compacta para representar ocupación por clúster.
    Cada clúster se muestra individualmente, orientado a formato de resumen.

    La visualización es útil cuando se desea mostrar resultados en tarjetas
    o espacios con poca área disponible, favoreciendo síntesis visual inmediata.
    """

    categorias = ["Alta", "Media", "Baja"]
    colores = ["#FF385C", "#FF9AA2", "#A7C7E7"]

    # Se itera por cada clúster de manera independiente.
    for cluster, valores in data_dict.items():

        fig = go.Figure()

        # Dentro de cada gráfico se apilan los tres niveles de ocupación.
        for cat, color in zip(categorias, colores):
            porcentaje = valores.get(cat, 0)

            fig.add_trace(go.Bar(
                x=[porcentaje],
                y=[cluster],
                name=cat,
                orientation='h',
                marker=dict(color=color),
                text=[f"{porcentaje}% {cat}"],
                textposition="inside",
                insidetextanchor="middle",
            ))

        fig.update_layout(
            barmode='stack',
            height=120,  # Compacto para uso en dashboards
            margin=dict(l=40, r=40, t=10, b=10),
            showlegend=False,
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=False)
        )

        st.plotly_chart(fig, use_container_width=True)



def grafica_ranking_ciudades(data_dict):
    """
    Construye un ranking descendente de ciudades con base en el porcentaje de ruido 
    detectado durante la ejecución de DBSCAN.

    El ruido representa instancias aisladas no pertenecientes a un grupo principal,
    lo cual sugiere mercados más dispares en precio o amenities.
    """

    df = pd.DataFrame({
        "Ciudad": list(data_dict.keys()),
        "Valor (%)": list(data_dict.values())
    })

    # Orden descendente para identificar la ciudad con mayor dispersión.
    df = df.sort_values("Valor (%)", ascending=False)

    fig = px.bar(
        df,
        x="Valor (%)",
        y="Ciudad",
        orientation="h",
        text="Valor (%)",
        color="Valor (%)",
        color_continuous_scale=AIRBNB_COLORS,
    )

    fig.update_traces(
        texttemplate="%{x:.2f}%",   # Valores representados con dos decimales
        textposition="outside"
    )

    fig.update_layout(
        title="Ruido por ciudad",
        height=380,
        margin=dict(l=30, r=30, t=60, b=30),
        xaxis=dict(title="Ruido (%)"),
        yaxis=dict(title="Ciudad"),
        paper_bgcolor="rgba(0,0,0,0)",  # Facilita integración con temas personalizados
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)



def graficas_experimento_2(df):
    """
    Comparación visual del comportamiento del clustering en el experimento más relevante:
    price vs amenities_count.

    El análisis contrasta:
    - Agrupamiento segmentado bajo centroides (KMeans)
    - Agrupamiento basado en densidad con detección de ruido (DBSCAN)

    Requisitos del DataFrame:
        df["price"]
        df["amenities_count"]
        df["kmeans_cluster"]
        df["dbscan_cluster"]
    """

    st.subheader("Experimento 2: KMeans vs DBSCAN (price vs amenities_count)")

    # Estructura: título de identificación y nombre de columna con etiquetas de clúster.
    modelos = [
        ("KMeans   k = 3, (Sil = 0.39)", "kmeans_cluster"),
        ("DBSCAN   eps = 0.5, min = 10, Sil = 0.00, Ruido = 36", "dbscan_cluster")
    ]

    # División de interfaz en dos columnas para comparación simultánea.
    col1, col2 = st.columns(2)

    for (titulo, col_cluster), destino_visual in zip(modelos, [col1, col2]):

        with destino_visual:
            df_m = df.copy()
            clusters = df_m[col_cluster].unique()

            fig = go.Figure()

            # Paleta discreta asignada a cada clúster detectado.
            colores = ["#B0003A", "#FFB6C1", "#E2E8F0"]

            for i, cl in enumerate(clusters):
                subset = df_m[df_m[col_cluster] == cl]

                fig.add_trace(go.Scatter(
                    x=subset["price"],
                    y=subset["amenities_count"],
                    mode="markers",
                    name=f"Clúster {cl}",
                    marker=dict(
                        color=colores[i % len(colores)],
                        size=5,
                        opacity=0.7
                    )
                ))

            fig.update_layout(
                title=titulo,
                xaxis_title="price (std)",            # Valores estandarizados previamente
                yaxis_title="amenities_count (std)",
                height=420,
                margin=dict(t=60, l=40, r=40, b=40),
                plot_bgcolor="rgba(0,0,0,0)",         # Fondo transparente útil en dashboards
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)

