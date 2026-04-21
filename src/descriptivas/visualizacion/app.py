"""
Frontend para el Sistema de Predicción de Accidentes de Tránsito (COSEVI)
Basado en datos de COSEVI.
Ejecutar: streamlit run app.py
"""
import streamlit as st

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Predicción Accidentes CR - COSEVI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILO PERSONALIZADO (TEMA COSEVI)
st.markdown("""
<style>
:root {
    --cosevi-blue: #003366;
    --cosevi-orange: #F15A24;
    --cosevi-light-gray: #F2F2F2;
    --cosevi-dark-gray: #333333;
}

/* Fondos y Texto */
body, .stApp {
    background-color: white; 
    color: var(--cosevi-dark-gray);
}
h1, h2, h3 {
    color: var(--cosevi-blue);
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: var(--cosevi-blue);
    border-right: 5px solid var(--cosevi-orange);
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--cosevi-orange) !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--cosevi-orange);
}
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    color: var(--cosevi-blue);
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: var(--cosevi-blue);
    color: white !important;
    border-radius: 5px 5px 0 0;
}

/* Botones */
div.stButton > button:first-child {
    background-color: var(--cosevi-orange);
    color: white;
    border-radius: 5px;
    border: none;
}
div.stButton > button:first-child:hover {
    background-color: #d4491c;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("🚗 Prevención Vial")
    st.markdown("### Análisis y Predicción de Accidentes")
    st.markdown("---")

    st.markdown("### 👩‍💻 Estudiantes")
    st.info(f"Camila Jiménez y Marisol Viquez\n\n*Big Data - CUC - 2026*")

    st.markdown("---")
    st.markdown("### 📊 Fuentes de Datos")
    st.markdown("[📄 CSV COSEVI](https://datosabiertos.csv.go.cr/datasets/193472/consolidado-de-accidentes-de-transito-con-victimas/)")
    st.markdown("[📖 Archivo .JSON](https://simplemaps.com/data/cr-cities)")
    st.markdown("[📁 Repositorio GitHub](#)")

# PÁGINA PRINCIPAL
st.title("🚗 Predicción de Accidentes de Tránsito en Costa Rica")
st.markdown("---")

st.markdown("""
Esta plataforma integra datos históricos de accidentes del **COSEVI** con condiciones climáticas para analizar patrones de riesgo y predecir la ocurrencia de incidentes mediante modelos supervisados.
""")

# TABS ADAPTADOS A TU PROYECTO
tab_eda, tab_model, tab_info = st.tabs(["📊 EDA y Visualización", "🧠 Modelo Predictivo", "📝 Detalles del Proyecto"])

# TAB 1: EDA
with tab_eda:
    st.subheader("Análisis Exploratorio de Datos (EDA)")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Frecuencia de Accidentes")
        # Aquí iría tu gráfico de barras de accidentes por provincia u hora
        st.image("https://via.placeholder.com/500x300.png?text=Gráfico+de+Frecuencia+por+Provincia",
                 use_container_width=True)

    with col2:
        st.write("### Mapas de Calor por Zona")
        # Aquí iría tu mapa de calor (Folium/Plotly)
        st.image("https://via.placeholder.com/500x300.png?text=Mapa+de+Calor+Accidentes+CR", use_container_width=True)

    st.markdown("---")
    st.write("### Relación Accidentes vs Condiciones Climáticas")
    st.write("Visualización de cómo la lluvia acumulada impacta en la cantidad de accidentes registrados.")

# TAB 2: MODELO (Basado en tus variables de entrada)
with tab_model:
    st.subheader("Cálculo de Riesgo de Accidente")

    with st.form("form_prediccion"):
        c1, c2 = st.columns(2)

        with c1:
            provincia = st.selectbox("Provincia",
                                     ["San José", "Alajuela", "Cartago", "Heredia", "Guanacaste", "Puntarenas",
                                      "Limón"])
            tipo_via = st.selectbox("Tipo de Vía", ["Carretera Nacional", "Vía Local", "Autopista"])
            hora = st.slider("Hora del día", 0, 23, 12)

        with c2:
            dia_semana = st.selectbox("Día de la semana",
                                      ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            lluvia = st.number_input("Lluvia acumulada (mm)", min_value=0.0, max_value=500.0, value=0.0)

        submit = st.form_submit_button("Predecir Ocurrencia")

        if submit:
            # Aquí conectarías con tu modelo .pkl (Regresión Logística, Árbol o KNN)
            st.success(f"Análisis completado para {provincia}")
            st.metric(label="Riesgo Estimado", value="Bajo", delta="-5% respecto al promedio")
            st.info("Nota: Este es un prototipo. La predicción se basa en los algoritmos de Regresión Logística y KNN.")

# TAB 3: INFORMACIÓN DEL PROYECTO
with tab_info:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 🎯 Objetivos")
        st.markdown("""
        - **Analizar** factores climáticos y viales que influyen en los accidentes.
        - **Predecir** la probabilidad de ocurrencia (Sí/No) en zonas específicas.
        - **Visualizar** geográficamente los puntos calientes de siniestralidad.
        """)

    with col_b:
        st.markdown("### 🧠 Especificaciones Técnicas")
        st.markdown("""
        - **Algoritmos:** Regresión Logística, Árbol de Decisión, KNN.
        - **Variable Objetivo:** Ocurrencia de accidente (Binaria).
        - **Tecnologías:** Python, Pandas, Scikit-learn, SQL Server/SQLite.
        """)

    st.markdown("---")
    st.code("""
# Estructura del repositorio en GitHub
Proyecto_Accidentes_COSEVI/
├── data/              # CSV de COSEVI y clima
├── notebooks/         # EDA y entrenamiento del modelo
├── src/               # Scripts de procesamiento
├── models/            # Archivos .pkl (modelos entrenados)
└── app.py             # Este dashboard de Streamlit
    """)

# FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666666;'>© 2026 | Proyecto de Predicción de Accidentes - Colegio Universitario de Cartago</div>",
    unsafe_allow_html=True)
