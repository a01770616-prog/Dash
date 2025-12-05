import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def calcular_competitividad(df):
    """
    Calcula un conjunto de métricas asociadas a competitividad
    tomando como referencia cuatro dimensiones clave:

    1) Profesionalismo → asociado al porcentaje de superhosts.
    2) Flexibilidad → porcentaje de propiedades con reserva inmediata.
    3) Calidad del servicio → aproximado mediante promedio de amenidades.
    4) Variabilidad del precio → medida mediante coeficiente de variación.

    El resultado es un diccionario con valores individuales
    y un índice consolidado ponderado.
    """

    m = {}  # Diccionario acumulador de métricas

    # Porcentaje de superhosts (si hay columna disponible)
    # reflects mayor profesionalización del anfitrión
    if "host_is_superhost" in df.columns:
        m["prof"] = (df["host_is_superhost"] == "t").mean() * 100
    else:
        m["prof"] = 0

    # Porcentaje de alojamientos con instant booking disponible
    # indica facilidad de reservar sin validación manual
    if "instant_bookable" in df.columns:
        m["flex"] = (df["instant_bookable"] == "t").mean() * 100
    else:
        m["flex"] = 0

    # Amenidades promedio escaladas a porcentaje
    # la división entre 15 es una base de ajuste uniforme y limitante hasta 100%
    if "amenities_count" in df.columns:
        m["amen"] = min(df["amenities_count"].mean() / 15 * 100, 100)
    else:
        m["amen"] = 0

    # Variabilidad relativa del precio usando coeficiente de variación
    # valores altos representan mercados heterogéneos y dispersos
    if "price" in df.columns:
        cv = df["price"].std() / df["price"].mean() * 100
        m["precio"] = min(cv / 50 * 100, 100)
    else:
        m["precio"] = 0

    # Índice final ponderado
    # Pesos definidos metodológicamente según relevancia analítica
    m["index"] = (
        m["prof"] * 0.4 +
        m["flex"] * 0.3 +
        m["amen"] * 0.2 +
        m["precio"] * 0.1
    )

    return m



def render_radar_competitividad(m, ciudad, PALETTE):
    """
    Representa las métricas de competitividad en formato de gráfico polar tipo radar.

    Cada dimensión ocupa un eje radial y permite visualizar fácilmente
    fortalezas relativas de la ciudad frente a cada componente evaluado.
    """

    fig = go.Figure()

    # La repetición del primer valor al final cierra la figura de forma circular.
    fig.add_trace(go.Scatterpolar(
        r=[
            m["prof"],
            m["flex"],
            m["amen"],
            m["precio"],
            m["prof"]
        ],
        theta=[
            "Profesionalismo",
            "Flexibilidad",
            "Servicios",
            "Precios",
            "Profesionalismo"
        ],
        fill="toself",
        line_color=PALETTE["brand"],
        name=ciudad
    ))

    # Escala fija 0–100 para todas las métricas,
    # permitiendo comparar ciudades con referencia común
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100]))
    )

    st.plotly_chart(fig, use_container_width=True)



def render_vecindarios_profesionalismo(df):
    """
    Genera una gráfica de barras que muestra el porcentaje
    de superhosts por vecindario.

    Esta representación permite identificar concentraciones geográficas
    asociadas a calidad del anfitrión.
    """

    # Condición mínima para poder calcular métricas por vecindario
    if "barrio_std" not in df.columns or "host_is_superhost" not in df.columns:
        st.info("No hay datos suficientes para analizar vecindarios.")
        return

    # Se agrupa por barrio y se calcula el porcentaje de superhosts
    t = (
        df.groupby("barrio_std")["host_is_superhost"]
        .apply(lambda x: (x == "t").mean() * 100)
        .reset_index(name="superhost_pct")
    )

    # Se muestran solo barrios con valores positivos
    t = t[t["superhost_pct"] > 0]

    fig = go.Figure()
    fig.add_bar(
        x=t["barrio_std"],
        y=t["superhost_pct"]
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)



def calcular_competitividad_ciudades(df, ciudades):
    """
    Ejecuta el cálculo de competitividad para cada ciudad seleccionada.

    El retorno es un DataFrame con una fila por ciudad,
    facilitando posteriormente comparaciones o gráficas.
    """

    rows = []

    for c in ciudades:
        sub_df = df[df["ciudad"] == c]  # se filtra por ciudad
        m = calcular_competitividad(sub_df)
        m["Ciudad"] = c  # etiqueta de identificación
        rows.append(m)

    return pd.DataFrame(rows)



def render_barras_competitividad(df, SCALE):
    """
    Representa el índice competitivo final en barras,
    usando un gradiente de color asociado al nivel competitivo.

    DF esperado:
        columnas → Ciudad, index
    """

    import plotly.express as px

    fig = px.bar(
        df,
        x="Ciudad",
        y="index",
        color="index",
        color_continuous_scale=SCALE
    )

    st.plotly_chart(fig, use_container_width=True)



def render_scatter_competitividad(df):
    """
    Crea un gráfico de dispersión que relaciona:
        X = amenidades promedio,
        Y = índice competitivo,
        tamaño del marcador = profesionalismo promedio,
        color = ciudad.

    Esta visualización permite interpretar si la competitividad
    está explicada por consistencia en servicios y calidad.
    """

    import plotly.express as px

    fig = px.scatter(
        df,
        x="amen",
        y="index",
        size="prof",
        color="Ciudad"
    )

    st.plotly_chart(fig, use_container_width=True)
