import streamlit as st

# En este bloque se definen estilos globales mediante CSS incrustado.
# La intención es dar consistencia visual a toda la interfaz que se presenta,
# sin necesidad de repetir estilos en cada módulo. Todos los estilos aplican
# inmediatamente porque Streamlit interpreta HTML/CSS por medio de markdown
# cuando se activa unsafe_allow_html=True.
st.markdown("""
    <style>
    /* Importación de tipografía externa utilizada en todo el dashboard */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Aplicación de la fuente de forma global a todos los componentes */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Encabezado principal superior que abre la página de Acerca */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;  /* Se busca jerarquía visual fuerte */
        color: #FF5A5F;  /* Color representativo de Airbnb */
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Estilo utilizado para dividir secciones conceptuales */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FF5A5F;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #FF5A5F;  /* Línea visual para separar bloques */
        padding-bottom: 0.5rem;
    }
    
    /* Bloques grandes tipo tarjeta que funcionan como contenedor de texto explicativo */
    .content-box {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);  /* Sombras suaves */
        border-left: 4px solid #FF5A5F;
    }
    
    /* Tarjetas internas para destacar puntos importantes */
    .feature-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 3px solid #FF8B8F;  /* Variante de tono para jerarquía secundaria */
    }
    
    /* Subtítulos internos dentro de tarjetas principales */
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #FF5A5F;
        margin-bottom: 0.5rem;
    }
    
    /* Texto normal explicado dentro de tarjetas — se usa en descripciones largas */
    .feature-description {
        color: #4a5568;
        line-height: 1.6;
    }
    
    /* Contenedores aplicados a ítems numerados — listados específicos */
    .objective-item {
        background: white;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-bottom: 0.8rem;
        border: 1px solid #e2e8f0;
        display: flex;
        align-items: flex-start; /* Asegura alineación vertical */
    }
    
    /* Número/ícono del objetivo que aparece a la izquierda como marcador visual */
    .objective-icon {
        color: #FF5A5F;
        font-size: 1.5rem;
        margin-right: 1rem;
        flex-shrink: 0;
        min-width: 30px;  /* Garantiza uniformidad visual */
    }
    
    /* Si se usan métricas globales después, estas son sus características visuales */
    .stat-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* Ajuste responsivo */
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #FF5A5F 0%, #FF8B8F 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)


# Renderización del encabezado principal en la interfaz.
# Aquí se define el nombre del módulo. Al hacerlo mediante HTML es posible
# aplicar las clases creadas previamente.
st.markdown('<h1 class="main-header">Acerca del Programa</h1>', unsafe_allow_html=True)


# Texto introductorio que contextualiza al usuario respecto a
# qué trata el dashboard y cuál es su objetivo general.
# Se emplea el contenedor tipo "content-box" definido arriba para darle contraste.
st.markdown("""
    <div class="content-box">
        El <strong>Dashboard de Análisis Airbnb</strong> es una plataforma diseñada para consolidar
        y explorar información sobre propiedades disponibles en Europa. Su propósito es centralizar
        datos clave y facilitar la interpretación de tendencias relacionadas con precios, tipos de
        alojamiento, niveles de reputación de anfitriones y patrones de demanda por ciudad.
    </div>
""", unsafe_allow_html=True)


# Indicamos qué se busca resolver desde el punto de vista de negocio.
# Aquí se presenta valor estratégico para cualquier usuario analítico
# o tomador de decisiones.
st.markdown('<h2 class="section-header">Objetivos de Negocio</h2>', unsafe_allow_html=True)


st.markdown(
    '<div class="content-box">'
    '<div class="feature-title" style="font-size: 1.3rem; margin-bottom: 1rem;">Plataforma centralizada con métricas homogéneas para análisis de Airbnb</div>'
    '<ul style="line-height: 2; color: #2d3748;">'
    '<li>Comparar propiedades entre varias ciudades europeas bajo un mismo criterio de evaluación.</li>'
    '<li>Visualizar tendencias de ocupación y preferencias de alojamiento.</li>'
    '<li>Reducir la necesidad de cálculos manuales mediante indicadores automáticos.</li>'
    '<li>Detectar zonas de mayor valor comercial basadas en precio y reputación.</li>'
    '</ul>'
    '<p style="margin-top: 1rem;">Ciudades incluidas: Ámsterdam, Barcelona, Atenas, Madrid y Milán.</p>'
    '</div>',
    unsafe_allow_html=True
)


# Ahora se listan tareas técnicas que soportan los objetivos comerciales.
# Lo que está abajo representa procesos desarrollados internamente.
st.markdown('<h2 class="section-header">Objetivos de Minería de Datos</h2>', unsafe_allow_html=True)

objetivos_mineria = [
    "Estandarizar información proveniente de diversas fuentes independientes.",
    "Analizar comparativamente el precio promedio por ciudad y tipo de propiedad.",
    "Evaluar niveles de ocupación estimada y su variación anual.",
    "Ubicar concentraciones geográficas donde se localiza la mayor oferta.",
    "Modelar comportamientos del mercado mediante agrupamiento (clustering).",
    "Explorar valores atípicos basados en distribución de ratings o ingresos.",
    "Generar visualizaciones automáticas que simplifiquen la toma de decisiones."
]

# Construcción iterativa de la lista visual de objetivos,
# permitiendo un número ordenado sin usar la etiqueta estándar de lista HTML.
for i, objetivo in enumerate(objetivos_mineria, 1):
    st.markdown(f"""
        <div class="objective-item">
            <div class="objective-icon">{i}.</div>
            <div class="feature-description">{objetivo}</div>
        </div>
    """, unsafe_allow_html=True)


# Finalmente se justifican los beneficios al tener el sistema operando.
# En esta parte se explica el diferencial frente a análisis tradicionales.
st.markdown('<h2 class="section-header">Beneficios del Sistema</h2>', unsafe_allow_html=True)

st.markdown("""
    <div class="content-box">
        <ul style="line-height: 2; font-size: 1.05rem;">
            <li>Centralización de información previamente dispersa.</li>
            <li>Acceso inmediato a indicadores sin procesamiento manual.</li>
            <li>Exploración visual flexible y filtrable.</li>
            <li>Identificación de oportunidades basadas en desempeño real del mercado.</li>
            <li>Complemento ideal para análisis estadístico y predictivo.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
