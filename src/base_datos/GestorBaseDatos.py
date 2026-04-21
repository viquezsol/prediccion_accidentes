import os
import pandas as pd
import numpy as np

class GestorDatos:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def cargar_csv(self, sep=';', encoding='utf-8'):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {self.file_path}")
        self.df = pd.read_csv(self.file_path, sep=sep, encoding=encoding)
        print(f"Cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        return self.df

    def limpiar_columnas(self):
        self.df.columns = self.df.columns.str.strip()
        texto_cols = self.df.select_dtypes(include=['object']).columns
        for col in texto_cols:
            self.df[col] = self.df[col].str.strip()
        print("Columnas limpias.")

    def manejar_nulos(self):
        texto_cols = self.df.select_dtypes(include=['object']).columns
        self.df[texto_cols] = self.df[texto_cols].fillna('Desconocido')
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[num_cols] = self.df[num_cols].fillna(0)
        print("Nulos manejados.")

    def estandarizar_tiempo(self):
        if 'Día' in self.df.columns:
            self.df['Día'] = self.df['Día'].str.replace(r'^\d+\.', '', regex=True)
        if 'Mes' in self.df.columns:
            self.df['Mes'] = self.df['Mes'].str.replace(r'^[A-Z]\.\s?', '', regex=True)
        print("Día/Mes estandarizados.")

    def pipeline(self):
        self.cargar_csv()
        self.limpiar_columnas()
        self.manejar_nulos()
        self.estandarizar_tiempo()
        return self.df