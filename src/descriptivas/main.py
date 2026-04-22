
import os
import sys
import pandas as pd
from sqlalchemy import create_engine
import urllib

from src.base_datos.GestorBaseDatos import GestorDatos
from src.eda.ProcesadorEDA import ProcesadorEDA
from src.descriptivas.visualizacion.Visualizador import Visualizador
from src.datos.GestorDatos import GestorDatos

DATA_RAW = r"C:\prediccion_accidentes\data\raw\BD.csv"
DATA_PROCESSED = r"C:\prediccion_accidentes\data\processed\accidentes_limpio.csv"

if not os.path.exists(DATA_RAW):
    print(f"ERROR: No se encuentra el archivo en: {DATA_RAW}")
    print("Por favor, verifica la ruta o coloca el archivo en esa ubicación.")
    sys.exit(1)

SERVER = 'localhost\\SQLEXPRESS'
DATABASE = 'AccidentesDB'
DRIVER = '{ODBC Driver 17 for SQL Server}'
USE_WINDOWS_AUTH = True


def cargar_y_limpiar_datos():
    print("=" * 60)
    print("1. Cargando y limpiando datos...")
    gestor = GestorDatos(DATA_RAW)
    df = gestor.pipeline()
    print(f"Datos cargados y limpios. Shape: {df.shape}")
    return df


def guardar_csv_limpio(df):

    print("\n2. Guardando CSV limpio...")
    os.makedirs(os.path.dirname(DATA_PROCESSED), exist_ok=True)
    df.to_csv(DATA_PROCESSED, index=False, encoding='utf-8-sig')
    print(f"CSV guardado en: {DATA_PROCESSED}")


def guardar_en_sql_server(df):
    print("\n3. Guardando datos en SQL Server...")
    try:
        if USE_WINDOWS_AUTH:
            params = urllib.parse.quote_plus(
                f"DRIVER={DRIVER};"
                f"SERVER={SERVER};"
                f"DATABASE={DATABASE};"
                "Trusted_Connection=yes;"
            )
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        else:
            raise NotImplementedError("Autenticación SQL no configurada aún")

        df.to_sql('accidentes', engine, if_exists='replace', index=False)
        print(" Datos guardados correctamente en SQL Server")
        engine.dispose()
    except Exception as e:
        print(f"Error al guardar en SQL Server: {e}")
        print("Continuando sin guardar en SQL Server...")


def ejecutar_eda(df):
    print("\n4. Ejecutando análisis EDA...")
    eda = ProcesadorEDA(df)
    eda.tendencia_anual()
    eda.top_provincias()
    eda.tipo_accidentes_top10()
    eda.distribucion_semana()


def ejecutar_visualizaciones(df):
    print("\n5. Generando visualizaciones avanzadas...")
    viz = Visualizador(df)
    viz.mapa_calor_provincia_hora()
    viz.mapa_calor_canton_zona()
    viz.comparar_accidente_clima()

    def agregar_clima(df, cliente_clima):
        if 'fecha' not in df.columns:
            raise ValueError("El DataFrame de accidentes no tiene una columna 'fecha'.")

        fecha_min = df['fecha'].min().date()
        fecha_max = df['fecha'].max().date()
        print(f"Consultando clima desde {fecha_min} hasta {fecha_max}...")

        df_clima = cliente_clima.obtener_lluvia_diaria(str(fecha_min), str(fecha_max))
        return pd.merge(df, df_clima, on='fecha', how='left')


def main():
    print(" SISTEMA DE PREDICCIÓN DE ACCIDENTES DE TRÁNSITO - COSTA RICA")

    # 1. Cargar y limpiar datos
    df = cargar_y_limpiar_datos()

    # 2. Guardar CSV limpio
    guardar_csv_limpio(df)

    # 3. Guardar en SQL Server
    guardar_en_sql_server(df)

    # 4. Análisis EDA
    ejecutar_eda(df)

    # 5. Visualizaciones avanzadas
    ejecutar_visualizaciones(df)

    print("\n Proceso completado exitosamente.")


if __name__ == "__main__":
    main()