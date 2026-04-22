import os
import pandas as pd
from sqlalchemy import create_engine
import urllib

class GestorBaseDatos:
    def __init__(self, server, database, use_windows_auth=True, username=None, password=None, driver='ODBC Driver 17 for SQL Server'):
        self.server = server
        self.database = database
        self.use_windows_auth = use_windows_auth
        self.username = username
        self.password = password
        self.driver = driver
        self.engine = None

    def _create_connection_string(self):
        """Construye la cadena de conexión para SQLAlchemy"""
        if self.use_windows_auth:
            params = urllib.parse.quote_plus(
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                "Trusted_Connection=yes;"
            )
            return f"mssql+pyodbc:///?odbc_connect={params}"
        else:
            return f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}?driver={self.driver}"

    def conectar(self):
        """Crea el motor de conexión"""
        try:
            conn_str = self._create_connection_string()
            self.engine = create_engine(conn_str)
            # Probar conexión
            with self.engine.connect() as conn:
                print(" Conexión exitosa a SQL Server")
        except Exception as e:
            print(f" Error de conexión: {e}")
            raise

    def ejecutar_consulta(self, query):
        """Ejecuta una consulta SQL y devuelve DataFrame"""
        if self.engine is None:
            raise Exception("No hay conexión activa. Llame a conectar() primero.")
        return pd.read_sql(query, self.engine)

    def guardar_dataframe(self, df, nombre_tabla, if_exists='replace', index=False):
        """Guarda un DataFrame en una tabla SQL"""
        if self.engine is None:
            raise Exception("No hay conexión activa. Llame a conectar() primero.")
        df.to_sql(nombre_tabla, self.engine, if_exists=if_exists, index=index)
        print(f"Datos guardados en tabla '{nombre_tabla}'")

    def cerrar(self):
        """Cierra la conexión (libera recursos)"""
        if self.engine:
            self.engine.dispose()
            print("Conexión cerrada")