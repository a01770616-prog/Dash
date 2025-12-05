import streamlit as st

# Carga de estilos CSS personalizados para dar identidad visual al dashboard.
# Este bloque controla:
# - Tipografías
# - Tamaños de headers
# - Diseño de tarjetas y contenedores
# - Animaciones hover
# - Colores corporativos tipo Airbnb
# Todo se inyecta con st.markdown porque Streamlit permite HTML seguro.
st.markdown("""
    <style>

    /* Importación de tipografía corporativa */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Todos los elementos adoptan la tipografía */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Encabezado grande para la sección */
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        color: #FF5A5F;
        margin-bottom: 1.2rem;
        text-align: center;
    }

    /* Encabezados internos para cada bloque analítico */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FF5A5F;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* Caja blanca usada como contenedor de explicación general */
    .content-box {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        border-left: 5px solid #FF5A5F;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.07);
    }

    /* Tarjeta principal para representar áreas de análisis */
    .area-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff4f4 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        border: 2px solid #ffdfe0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(255, 90, 95, 0.10);
    }

    /* Animación al pasar el cursor */
    .area-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 8px 28px rgba(255, 90, 95, 0.18);
    }

    /* Título de cada tarjeta temática */
    .area-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FF5A5F;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* Texto descriptivo de cada área temática */
    .area-description {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.7;
        text-align: justify;
    }

    /* Subcontenedor que agrupa listas internas explicativas */
    .subarea-item {
        background: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        border-left: 4px solid #FF8B8F;
    }

    /* Título de subapartado */
    .subarea-title {
        font-weight: 600;
        color: #FF5A5F;
        margin-bottom: 0.5rem;
    }

    </style>
""", unsafe_allow_html=True)



# Render del encabezado principal
# Se utiliza HTML personalizado para mantener estilo corporativo y tamaños.
st.markdown('<h1 class="main-header">Áreas de Enfoque</h1>', unsafe_allow_html=True)



# Este bloque sirve como introducción general de la vista.
# Explica contexto del análisis y alcance del estudio realizado.
st.markdown("""
    <div class="content-box">
        El estudio realizado sobre las propiedades de Airbnb involucra la
        exploración estadística, comparativa y predictiva de datos provenientes de
        <strong>Amsterdam, Barcelona, Atenas, Madrid y Milán</strong>. A través de técnicas analíticas
        se identifican patrones relevantes, diferencias entre mercados y oportunidades de inversión
        o segmentación basada en comportamiento del usuario.
    </div>
""", unsafe_allow_html=True)




# ÁREA 1 — Análisis estadístico
st.markdown(
    '<div class="area-card">'
    '<div class="area-title">Análisis Estadístico</div>'
    '<div class="area-description">Se enfoca en el estudio de variables clave como precio, amenities, capacidad, niveles de rating y tipo de propiedad. Ayuda a comprender qué factores tienen mayor influencia en la valoración del mercado hospedaje europeo.</div>'
    '<div class="subarea-item">'
    '<div class="subarea-title">Técnicas aplicadas</div>'
    '<ul>'
    '<li>Extracción de características relevantes por ciudad</li>'
    '<li>Regresión lineal para analizar relaciones entre precio y atributos</li>'
    '<li>Regresión no lineal para patrones complejos o curvilíneos</li>'
    '<li>Regresión logística para clasificación binaria/categórica</li>'
    '<li>Modelos ANOVA para comparar medias entre regiones y categorías</li>'
    '</ul>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)




# ÁREA 2 — Análisis Comparativo
st.markdown(
    '<div class="area-card">'
    '<div class="area-title">Análisis Comparativo</div>'
    '<div class="area-description">Permite contrastar la oferta disponible y esquema de consumo por ciudad. Se observan diferencias en: precios promedio, densidad de alojamientos, volumen de superhosts, disponibilidad anual y tipo de alojamiento preferido.</div>'
    '<div class="subarea-item">'
    '<div class="subarea-title">Dimensiones evaluadas</div>'
    '<ul>'
    '<li>Distribución del precio promedio por país y ciudad</li>'
    '<li>Diferencias en rating y reseñas acumuladas</li>'
    '<li>Oferta predominante por tipo de propiedad</li>'
    '<li>Variación geográfica usando mapas comparativos</li>'
    '<li>Presencia de zonas catalogadas como “premium”</li>'
    '</ul>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)




# ÁREA 3 — Clasificación y Agrupamiento (Machine Learning)
st.markdown(
    '<div class="area-card">'
    '<div class="area-title">Clasificación y Agrupamiento</div>'
    '<div class="area-description">El uso de machine learning permite segmentar propiedades con base en similitudes naturales sin intervención manual. Esto permite obtener conglomerados y perfiles claros del mercado.</div>'
    '<div class="subarea-item">'
    '<div class="subarea-title">Algoritmos utilizados</div>'
    '<ul>'
    '<li>K-Means → segmentación rápida por características de magnitud</li>'
    '<li>Jerárquico → agrupamientos según similitud progresiva</li>'
    '<li>DBSCAN → agrupación basada en densidad y detección de ruido</li>'
    '</ul>'
    '</div>'
    '<div class="subarea-item">'
    '<div class="subarea-title">Aplicaciones reales</div>'
    '<ul>'
    '<li>Identificación de clusters premium por zona</li>'
    '<li>Descubrimiento de viviendas económicas con alta demanda</li>'
    '<li>Clasificación automática basada en amenidades</li>'
    '<li>Segmentación de grupos de propiedades homogéneas</li>'
    '</ul>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)
