import streamlit as st

# Configuración de la página
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .main .block-container {
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 0 !important;
        max-width: 100% !important;
    }
    
    .main {
        padding: 0 !important;
        background: #fafafa;
    }
    
    .logo-wrapper {
        padding: 2rem 0;
    }
    
    .banner-wrapper {
        position: relative;
        margin-bottom: 3rem;
    }
    
    .banner-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.4) 0%, transparent 100%);
        height: 80px;
        display: flex;
        align-items: flex-end;
        padding: 1.5rem 3rem;
    }
    
    .banner-text {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    .cards-container {
        display: grid;
        grid-template-columns: repeat(3, minmax(280px, 380px));
        gap: 2.5rem;
        justify-content: center;
        max-width: 1300px;
        margin: 0 auto;
        padding: 0 3rem 3rem 3rem;
    }
    
    .card {
        width: 100%;
        text-align: center;
        padding: 2rem 1.5rem;
        background: white;
        border-radius: 16px;
        border: 1px solid rgba(255, 90, 95, 0.08);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 240px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #FF5A5F 0%, #FF8B8F 100%);
        transform: scaleX(1);
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(255, 90, 95, 0.15);
        border-color: rgba(255, 90, 95, 0.2);
    }
    
    .card:hover::before {
        transform: scaleX(1);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1.2rem;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80px;
        position: relative;
    }
    
    .card-icon::before {
        content: '';
        position: absolute;
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, rgba(255, 90, 95, 0.08) 0%, rgba(255, 139, 143, 0.08) 100%);
        border-radius: 50%;
        z-index: 0;
        transition: transform 0.4s ease;
    }
    
    .card:hover .card-icon::before {
        transform: scale(1.2);
    }
    
    .card-icon svg {
        width: 55px;
        height: 55px;
        stroke: #FF5A5F;
        position: relative;
        z-index: 1;
        transition: transform 0.4s ease;
    }
    
    .card:hover .card-icon svg {
        transform: scale(1.1);
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FF5A5F;
        margin-bottom: 0.8rem;
        letter-spacing: -0.3px;
    }
    
    .card-description {
        font-size: 0.95rem;
        color: #64748b;
        line-height: 1.6;
        font-weight: 400;
    }
    
    @media (max-width: 1024px) {
        .cards-container {
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            padding: 0 2rem 3rem 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Logo superior
st.markdown("""
    <div class="logo-wrapper">
        <div style="text-align: center;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/2560px-Airbnb_Logo_B%C3%A9lo.svg.png" 
                 alt="Airbnb Logo" 
                 style="height: 50px; width: auto;">
        </div>
    </div>
""", unsafe_allow_html=True)

# Imagen del banner con overlay
st.markdown("""
    <div class="banner-wrapper">
        <div class="banner-container" style="width: 100vw; margin-left: calc(-50vw + 50%); margin-right: calc(-50vw + 50%); padding: 0; height: 240px; overflow: hidden; transition: height 0.3s ease; position: relative;">
            <img src="https://images.unsplash.com/photo-1583422409516-2895a77efded?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" 
                 style="width: 100%; height: 100%; display: block; object-fit: cover; object-position: 55% 30%;"
                 onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
            <div style="display: none; text-align: center; padding: 4rem; background: #f5f5f5;">
                <h2 style="color: #FF5A5F; margin: 0;">Dashboard Airbnb</h2>
                <p style="color: #666; margin-top: 1rem;">Descubre tu próximo hogar</p>
            </div>
        </div>
        <div class="banner-overlay">
            <div class="banner-text">Descubre tu próxima reserva</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stButton > button, .stLinkButton > a {
        color: #444 !important;
        font-weight: 500;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center !important;
    }
    .stButton > button > div, .stLinkButton > a > div {
        width: 100%;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)


# Tarjetas de información usando columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <a href="https://www.airbnb.mx/host/homes?c=.pi0.pk21187098705_167669482982&gclsrc=aw.ds&&c=.pi0.pk21187098705_167669482982&gad_source=1&gad_campaignid=21187098705&gbraid=0AAAAADz55LlVhK7QvmaZYdQjKknt_hLe7&gclid=CjwKCAiA55rJBhByEiwAFkY1QL4sLhfboqi4xmY6yaSlvdOilSAsGd-6YA8cydWqU-7ERgXAp3nP6xoCbzcQAvD_BwE" target="_blank" style="text-decoration: none; color: inherit;">
            <div class="card">
                <div class="card-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"></path>
                    </svg>
                </div>
                <div class="card-title">Haz una Reserva</div>
                <div class="card-description">Encuentra el lugar perfecto para tu próximo viaje</div>
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 0.7rem;'></div>", unsafe_allow_html=True)
    st.link_button("¡Reserva y disfruta tu próxima experiencia!", "https://www.airbnb.mx/host/homes?c=.pi0.pk21187098705_167669482982&gclsrc=aw.ds&&c=.pi0.pk21187098705_167669482982&gad_source=1&gad_campaignid=21187098705&gbraid=0AAAAADz55LlVhK7QvmaZYdQjKknt_hLe7&gclid=CjwKCAiA55rJBhByEiwAFkY1QL4sLhfboqi4xmY6yaSlvdOilSAsGd-6YA8cydWqU-7ERgXAp3nP6xoCbzcQAvD_BwE", use_container_width=True)

with col2:
    st.markdown("""
        <a href="#" onclick="return false;" style="text-decoration: none; color: inherit; cursor: pointer;">
            <div class="card">
                <div class="card-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                        <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                    </svg>
                </div>
                <div class="card-title">Acerca del Programa</div>
                <div class="card-description">Conoce más sobre nuestro sistema de análisis de propiedades</div>
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 0.7rem;'></div>", unsafe_allow_html=True)
    if st.button("¿Cómo este programa mejora tu hospedaje?", key="btn_programa", use_container_width=True):
        st.switch_page("Paginas/acerca_programa.py")

with col3:
    st.markdown("""
        <a href="#" onclick="return false;" style="text-decoration: none; color: inherit; cursor: pointer;">
            <div class="card">
                <div class="card-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                </div>
                <div class="card-title">Áreas de Enfoque</div>
                <div class="card-description">Accede a los puntos más relevantes del análisis</div>
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 0.7rem;'></div>", unsafe_allow_html=True)
    if st.button("Explora los temas y análisis clave del dashboard", key="btn_areas", use_container_width=True):
        st.switch_page("Paginas/areas_enfoque.py")




