import streamlit as st

def resumen_variables():
    """
    Muestra un resumen descriptivo de las variables empleadas en los diferentes
    experimentos de clustering dentro de la aplicación.

    Objetivo
    ---------
    Documentar al usuario cuáles variables fueron utilizadas, su significado
    y su relevancia analítica dentro del proceso de agrupamiento.

    Alcance
    --------
    Esta sección se muestra colapsada mediante st.expander para mantener
    orden visual dentro del dashboard y facilitar la consulta únicamente
    cuando el usuario lo requiera.
    """

    with st.expander("Variables utilizadas en el Clustering"):
        st.markdown("""
        Las principales variables empleadas en los experimentos fueron:

        - price → precio por noche de cada alojamiento
        - amenities_count → cantidad total de amenidades declaradas
        - number_of_reviews_ltm → número de reseñas recibidas en los últimos 12 meses
        - host_listings_count → cantidad de propiedades administradas por el anfitrión
        - estimated_occupancy_l365d → porcentaje estimado de ocupación durante el último año
        - estimated_revenue_l365d → estimación del ingreso generado en 365 días

        Justificación analítica
        -----------------------
        Estas variables permiten caracterizar a los listings desde diferentes perspectivas:

        - Dimensión económica: price, estimated_revenue_l365d
        - Dimensión de calidad percibida: amenities_count
        - Dimensión de demanda real: number_of_reviews_ltm y estimated_occupancy_l365d
        - Dimensión de profesionalización: host_listings_count

        Su combinación permite segmentar el mercado, identificar perfiles de host,
        detectar niveles de competitividad y analizar desempeño económico dentro
        del contexto del mercado Airbnb.
        """)

