
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from datetime import datetime, timedelta
import os

# =====================================================
# CONFIGURACIÓN DE PÁGINA
# =====================================================
st.set_page_config(
    page_title="Análisis Accidentes CR - COSEVI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# ESTILO PERSONALIZADO (TEMA COSEVI)
# =====================================================
st.markdown("""
<style>
:root {
    --cosevi-blue: #003366;
    --cosevi-orange: #F15A24;
    --cosevi-light-gray: #F2F2F2;
    --cosevi-dark-gray: #333333;
}
body, .stApp {
    background-color: white; 
    color: var(--cosevi-dark-gray);
}
h1, h2, h3 {
    color: var(--cosevi-blue);
}
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


# =====================================================
# FUNCIONES DE CARGA DE DATOS Y API
# =====================================================
@st.cache_data
def cargar_datos():
    """Carga el DataFrame limpio desde CSV procesado, SQL Server o genera datos de ejemplo."""
    # Intenta desde CSV procesado
    csv_path = r"C:\prediccion_accidentes\data\processed\accidentes_limpio.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            st.success(f"Datos cargados desde CSV: {df.shape[0]} registros")
            return df
        except Exception as e:
            st.warning(f"Error al leer CSV: {e}")

    # Intenta desde SQL Server (si tienes conexión)
    try:
        from sqlalchemy import create_engine
        import urllib
        server = 'localhost\\SQLEXPRESS'
        database = 'AccidentesDB'
        driver = '{ODBC Driver 17 for SQL Server}'
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
        )
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        df = pd.read_sql("SELECT * FROM accidentes", engine)
        engine.dispose()
        st.success(f"Datos cargados desde SQL Server: {df.shape[0]} registros")
        return df
    except Exception as e:
        st.warning(f"Error al conectar a SQL Server: {e}")

    # Fallback: generar datos de ejemplo
    st.info("No se encontraron datos reales. Cargando datos de ejemplo para visualización.")
    np.random.seed(42)
    n = 5000
    fechas = pd.date_range('2018-01-01', '2024-12-31', periods=n)
    provincias = ['San José', 'Alajuela', 'Cartago', 'Heredia', 'Guanacaste', 'Puntarenas', 'Limón']
    tipos_accidente = ['Colisión entre vehículos', 'Colisión con motocicleta', 'Salió de la vía', 'Vuelco',
                       'Colisión con bicicleta']
    climas = ['Buen tiempo', 'Lluvia', 'Nublado']
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    horas = ['06:00-11:59', '12:00-17:59', '18:00-23:59', '00:00-05:59']

    df = pd.DataFrame({
        'fecha': fechas,
        'Año': fechas.year,
        'Provincia': np.random.choice(provincias, n),
        'Tipo de accidente': np.random.choice(tipos_accidente, n),
        'Día': np.random.choice(dias, n),
        'Hora recodificada': np.random.choice(horas, n),
        'Estado del tiempo': np.random.choice(climas, n, p=[0.7, 0.2, 0.1]),
        'Tipo ruta': np.random.choice(['Nacional', 'Cantonal', 'Local'], n),
        'Cantón': np.random.choice(['San José', 'Alajuela', 'Cartago', 'Heredia', 'Liberia', 'Puntarenas', 'Limón'], n)
    })
    return df


@st.cache_data
def obtener_lluvia_api(fecha_inicio, fecha_fin, lat=9.9281, lon=-84.0907):
    """Obtiene precipitación diaria desde Open-Meteo API."""
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': fecha_inicio.strftime('%Y-%m-%d'),
        'end_date': fecha_fin.strftime('%Y-%m-%d'),
        'daily': 'precipitation_sum',
        'timezone': 'America/Costa_Rica'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            daily = data['daily']
            df_clima = pd.DataFrame({
                'fecha': pd.to_datetime(daily['time']),
                'precipitacion_mm': daily['precipitation_sum']
            })
            return df_clima
        else:
            st.error(f"Error en API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error de conexión con API de clima: {e}")
        return None


@st.cache_data
def cargar_coordenadas_provincias():
    """Devuelve un DataFrame con coordenadas aproximadas de las capitales de provincia."""
    coords = {
        'Provincia': ['San José', 'Alajuela', 'Cartago', 'Heredia', 'Guanacaste', 'Puntarenas', 'Limón'],
        'lat': [9.9333, 10.0167, 9.8667, 10.0000, 10.5000, 9.9764, 9.9900],
        'lon': [-84.0833, -84.2167, -83.9167, -84.1167, -85.2500, -84.8333, -83.0333]
    }
    return pd.DataFrame(coords)


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.title("🚗 Prevención Vial")
    st.markdown("### Análisis y Visualización de Accidentes")
    st.markdown("---")
    st.markdown("### 👩‍💻 Estudiantes")
    st.info(f"Camila Jiménez y Marisol Viquez\n\n*Big Data - CUC - 2026*")
    st.markdown("---")
    st.markdown("### 📊 Fuentes de Datos")
    st.markdown(
        "[📄 CSV COSEVI](https://datosabiertos.csv.go.cr/datasets/193472/consolidado-de-accidentes-de-transito-con-victimas/)")
    st.markdown("🌦️ [API Open-Meteo](https://open-meteo.com/)")

# =====================================================
# PÁGINA PRINCIPAL
# =====================================================
st.title("🚗 Análisis de Accidentes de Tránsito en Costa Rica")
st.markdown("---")
st.markdown("""
Esta plataforma integra datos históricos de accidentes del **COSEVI** con condiciones climáticas obtenidas de la API de Open-Meteo.
""")

# Cargar datos
df = cargar_datos()

if df is None:
    st.stop()

# =====================================================
# TABS
# =====================================================
tab_eda, tab_clima, tab_mapas, tab_info = st.tabs(
    ["📊 EDA y Visualización", "🌦️ Relación con Clima (API)", "🗺️ Mapas", "📝 Detalles del Proyecto"])

# -----------------------------------------------------
# TAB 1: EDA
# -----------------------------------------------------
with tab_eda:
    st.subheader("Análisis Exploratorio de Datos (EDA)")

    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)

    col1, col2 = st.columns(2)
    with col1:
        st.write("#### Evolución Anual")
        if 'Año' in df.columns:
            fig, ax = plt.subplots()
            trend = df.groupby('Año').size()
            sns.lineplot(x=trend.index, y=trend.values, marker='o', color='teal', ax=ax)
            ax.set_title('Accidentes por Año')
            ax.set_xlabel('Año')
            ax.set_ylabel('Cantidad')
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Columna 'Año' no disponible.")

    with col2:
        st.write("#### Accidentes por Provincia")
        if 'Provincia' in df.columns:
            fig, ax = plt.subplots()
            order = df['Provincia'].value_counts().index
            sns.countplot(data=df, y='Provincia', order=order, palette='viridis', ax=ax)
            ax.set_title('Distribución por Provincia')
            ax.set_xlabel('Cantidad')
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Columna 'Provincia' no disponible.")

    st.write("#### Top 10 Tipos de Accidente")
    if 'Tipo de accidente' in df.columns:
        fig, ax = plt.subplots()
        top10 = df['Tipo de accidente'].value_counts().head(10)
        sns.barplot(x=top10.values, y=top10.index, palette='magma', ax=ax)
        ax.set_title('Tipos más frecuentes')
        ax.set_xlabel('Número de Casos')
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Columna 'Tipo de accidente' no disponible.")

    st.write("#### Accidentes por Día de la Semana")
    if 'Día' in df.columns:
        fig, ax = plt.subplots()
        orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        sns.countplot(data=df, x='Día', order=orden_dias, palette='coolwarm', ax=ax)
        ax.set_title('Frecuencia por Día')
        ax.set_ylabel('Cantidad')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Columna 'Día' no disponible.")

    st.write("#### Mapa de Calor: Provincia vs Rango Horario")
    if 'Provincia' in df.columns and 'Hora recodificada' in df.columns:
        ct = pd.crosstab(df['Provincia'], df['Hora recodificada'])
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(ct, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
        ax.set_title('Provincia vs Hora')
        ax.set_ylabel('Provincia')
        ax.set_xlabel('Rango Horario')
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Columnas 'Provincia' o 'Hora recodificada' no disponibles.")

# -----------------------------------------------------
# TAB 2: CLIMA (API)
# -----------------------------------------------------
with tab_clima:
    st.subheader("🌦️ Consulta de Lluvia Histórica desde Open-Meteo")

    # Selección de fechas
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio", datetime(2023, 1, 1))
    with col2:
        fecha_fin = st.date_input("Fecha de fin", datetime(2023, 12, 31))

    if st.button("Consultar lluvia en San José"):
        df_lluvia = obtener_lluvia_api(fecha_inicio, fecha_fin)
        if df_lluvia is not None:
            st.success(f"Datos obtenidos desde {fecha_inicio} hasta {fecha_fin}")
            st.dataframe(df_lluvia.head(10))

            # Gráfico de precipitación
            fig = px.line(df_lluvia, x='fecha', y='precipitacion_mm',
                          title='Precipitación diaria (mm)',
                          labels={'fecha': 'Fecha', 'precipitacion_mm': 'Lluvia (mm)'})
            st.plotly_chart(fig, use_container_width=True)

            # Si el dataframe de accidentes tiene columna 'fecha', fusionar y mostrar correlación
            if 'fecha' in df.columns:
                df_acc = df.copy()
                df_acc['fecha'] = pd.to_datetime(df_acc['fecha']).dt.date
                df_lluvia['fecha'] = pd.to_datetime(df_lluvia['fecha']).dt.date
                df_merged = pd.merge(df_acc, df_lluvia, on='fecha', how='left')
                st.subheader("Accidentes y lluvia (datos fusionados)")
                st.write(f"Registros con datos de lluvia: {df_merged['precipitacion_mm'].notna().sum()}")
                # Gráfico de accidentes por día con lluvia
                if 'precipitacion_mm' in df_merged.columns:
                    fig2 = px.scatter(df_merged, x='precipitacion_mm', y='Año',
                                      title='Accidentes vs Precipitación',
                                      labels={'precipitacion_mm': 'Lluvia (mm)'})
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("El DataFrame de accidentes no tiene columna 'fecha' para fusionar con datos climáticos.")
        else:
            st.error("No se pudo obtener datos de la API.")

# -----------------------------------------------------
# TAB 3: MAPAS
# -----------------------------------------------------
with tab_mapas:
    st.subheader("🗺️ Visualización Geográfica de Accidentes")

    # Mapa de concentración por provincia
    st.write("#### Concentración de accidentes por provincia")
    if 'Provincia' in df.columns:
        df_coords = cargar_coordenadas_provincias()
        prov_counts = df['Provincia'].value_counts().reset_index()
        prov_counts.columns = ['Provincia', 'cantidad']
        df_map = prov_counts.merge(df_coords, on='Provincia')
        fig_map = px.scatter_mapbox(df_map, lat='lat', lon='lon', size='cantidad',
                                    hover_name='Provincia', zoom=6,
                                    mapbox_style="stamen-terrain",
                                    title="Accidentes por provincia (tamaño proporcional)")
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Columna 'Provincia' no disponible.")

    # Mapa de calor por cantón (si hay coordenadas)
    st.write("#### Cantones con más accidentes")
    if 'Cantón' in df.columns:
        top_cantones = df['Cantón'].value_counts().head(20).reset_index()
        top_cantones.columns = ['Cantón', 'accidentes']
        st.dataframe(top_cantones)
    else:
        st.info("Columna 'Cantón' no disponible.")

# -----------------------------------------------------
# TAB 4: INFORMACIÓN
# -----------------------------------------------------
with tab_info:
    st.markdown("### 🎯 Objetivos del Proyecto")
    st.markdown("""
    - **Analizar** factores climáticos y viales que influyen en los accidentes.
    - **Visualizar** geográficamente los puntos calientes de siniestralidad.
    - **Explorar** patrones temporales (año, día, hora) y geográficos (provincia, cantón).
    - **Integrar** datos de lluvia desde API abierta para correlacionar con accidentes.
    """)

    st.markdown("### 🧠 Especificaciones Técnicas")
    st.markdown("""
    - **Tecnologías:** Python, Pandas, Streamlit, Plotly, Matplotlib, Seaborn, Requests.
    - **API de Clima:** Open-Meteo (gratuita, sin autenticación).
    - **Base de datos:** SQL Server (opcional).
    - **Visualizaciones:** Gráficos interactivos y mapas.
    """)

    st.markdown("---")
    st.markdown("#### 📊 Resumen de los datos cargados")
    st.write(f"**Registros:** {df.shape[0]:,}")
    st.write(f"**Columnas:** {df.shape[1]}")
    st.dataframe(df.head(10))

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666666;'>© 2026 | Proyecto de Análisis de Accidentes - Colegio Universitario de Cartago</div>",
    unsafe_allow_html=True)