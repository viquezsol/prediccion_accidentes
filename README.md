Este proyecto analiza datos historicos de accidentes de transito con victimas en Costa Rica, obtenidos del COSEVI. Se realiza un analisis exploratorio (EDA), se almacenan los datos en SQL Server, se consulta una API de clima (Open-Meteo) para enriquecer los registros con precipitacion, y se despliega un dashboard interactivo con Streamlit.


## Requisitos

- Python 
- SQL Server (opcional, puede funcionar solo con CSV)


## Instalacion

1. Clonar el repositorio
2. Crear un entorno virtual (recomendado)
3. Instalar dependencias:

pandas
numpy
matplotlib
seaborn
plotly
streamlit
requests
sqlalchemy
pyodbc

## Uso

### 1. Preparacion de datos

Colocar el archivo CSV del COSEVI en data/raw/BD.csv (con separador ; y codificacion UTF-8).

Ejecutar el orquestador principal:

python src/main.py

Este script:
- Carga y limpia el CSV.
- Guarda una copia limpia en data/processed/.
- Opcionalmente guarda los datos en SQL Server (configurar credenciales en el script).

### 2. Dashboard interactivo

Para lanzar la aplicacion web:

streamlit run app.py

El dashboard permite:
- Visualizar estadisticas de accidentes por provincia, ano, dia, hora.
- Consultar la API de Open-Meteo para obtener precipitacion historica en San Jose.
- Explorar mapas de concentracion de accidentes.

## API de clima

Se utiliza la API gratuita Open-Meteo (sin autenticacion). El usuario puede seleccionar un rango de fechas y obtener la precipitacion diaria acumulada.



## Autoria

Camila Jimenez y Marisol Viquez
Big Data - Colegio Universitario de Cartago
2026
