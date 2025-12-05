import streamlit as st
import pandas as pd


# Esta función genera filtros interactivos basados en ciudad, barrios y rango de precios.
# Se diseñó para integrarse dentro de una interfaz de Streamlit y facilitar el filtrado estructurado
# de información proveniente de un DataFrame de Airbnb u otra fuente similar.
def filtros_ciudad_barrios_precios(
    df: pd.DataFrame,                  # DataFrame principal sobre el cual se realizarán los filtros
    min_barrios_default: int = 5,      # Cantidad mínima de barrios preseleccionados automáticamente
    use_sidebar: bool = True,          # Indica si los filtros se mostrarán en la barra lateral
):
    # Validación inicial: si no existe la columna "ciudad", no se puede segmentar el dataset
    if "ciudad" not in df.columns:
        st.error("No existe la columna 'ciudad' en el DataFrame.")
        return None, [], None, pd.DataFrame()

    # Obtiene todas las ciudades disponibles y las ordena alfabéticamente
    ciudades = sorted(df["ciudad"].dropna().unique().tolist())
    if not ciudades:
        st.error("No hay ciudades disponibles en 'ciudad'.")
        return None, [], None, pd.DataFrame()

    # Dependiendo de use_sidebar se decide si los filtros se despliegan en sidebar o en pantalla principal
    container = st.sidebar if use_sidebar else st

    # Encabezado visible para el usuario
    container.markdown("### Filtros")

    # Selectbox que permite elegir una ciudad de forma única
    ciudad_sel = container.selectbox("Ciudad", ciudades)

    # Se construye un subconjunto del DataFrame únicamente con los registros de la ciudad seleccionada
    df_city = df[df["ciudad"] == ciudad_sel].copy()

    barrios_sel = []
    # Validación para saber si existe la columna de barrios estandarizados
    if "barrio_std" in df_city.columns:
        # Extrae barrios ordenados por mayor frecuencia
        barrios = (
            df_city["barrio_std"]
            .dropna()
            .value_counts()
            .index
            .tolist()
        )

        # Selección por defecto de los primeros barrios más relevantes
        default_barrios = barrios[:min_barrios_default]

        # Selector múltiple para elegir uno o varios barrios
        barrios_sel = container.multiselect(
            "Barrios",
            barrios,
            default=default_barrios,
        )

        # Se filtra nuevamente el dataset si el usuario seleccionó barrios
        if barrios_sel:
            df_city = df_city[df_city["barrio_std"].isin(barrios_sel)]
    else:
        # Mensaje informativo cuando no se puede filtrar por barrio
        container.info("No existe la columna 'barrio_std' para filtrar por barrio.")

    rango_precios = None
    # Identifica valores mínimos y máximos de la variable "price" y genera un slider dinámico
    if "price" in df_city.columns and df_city["price"].notna().any():
        min_p = float(df_city["price"].min())
        max_p = float(df_city["price"].max())

        # Slider de rango dinámico para filtrar precios
        rango_precios = container.slider(
            "Rango de precio",
            min_value=round(min_p),
            max_value=round(max_p),
            value=(round(min_p), round(max_p)),
        )

        # Segmenta el dataframe de acuerdo con el rango seleccionado
        df_city = df_city[
            (df_city["price"] >= rango_precios[0]) &
            (df_city["price"] <= rango_precios[1])
        ]
    else:
        container.info("No hay datos suficientes de 'price' para filtrar por rango.")

    # La función devuelve la ciudad seleccionada, los barrios seleccionados,
    # el rango seleccionado y el DataFrame filtrado final
    return ciudad_sel, barrios_sel, rango_precios, df_city


import streamlit as st
import pandas as pd


# Esta función construye un conjunto de filtros generales para seleccionar ciudades y otras variables relevantes.
# Se utiliza normalmente en dashboards donde el usuario necesita trabajar con subconjuntos comparables del dataset.
def sidebar_filtros(df, Lista):
    # Validación para garantizar que existe una columna ciudad con valores válidos
    if "ciudad" not in df.columns or df["ciudad"].dropna().empty:
        st.warning("No hay columna 'ciudad' válida.")
        st.stop()

    # Lista ordenada de ciudades disponibles
    ciudades_disp = sorted(df["ciudad"].dropna().unique().tolist())

    # Título de sección en la barra lateral
    st.sidebar.header("Ciudades")

    # Filtro múltiple para elegir una o varias ciudades
    selected_cities = st.sidebar.multiselect(
        "Selecciona ciudades",
        ciudades_disp,
        default=ciudades_disp[:min(3, len(ciudades_disp))],  # Preselección de máximo 3 ciudades
        max_selections=5                                     # Límite máximo seleccionable
    )

    # Si el usuario no elige ninguna ciudad, se detiene la ejecución por seguridad
    if not selected_cities:
        st.info("Selecciona al menos una ciudad.")
        st.stop()

    # Filtra el DataFrame con base en las ciudades seleccionadas
    df_filtered = df[df["ciudad"].isin(selected_cities)].copy()

    # Slider para determinar un top de categorías que se utilizará posteriormente
    top_k = st.sidebar.slider("Top categorías", 5, 30, 10)

    # Check para decidir si el usuario mostrará una tabla en pantalla
    mostrar_tabla = st.sidebar.checkbox("Mostrar tabla", False)

    # Selectbox que recibe como input una lista que corresponde a variables categóricas disponibles
    Variable_Cat = st.sidebar.selectbox("Variable categórica", Lista)

    # La función retorna los filtros seleccionados para uso posterior en la visualización o cálculo
    return selected_cities, df_filtered, top_k, mostrar_tabla, Variable_Cat

