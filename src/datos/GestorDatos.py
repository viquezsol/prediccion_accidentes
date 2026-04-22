import os
import pandas as pd
import numpy as np

class GestorDatos:
    def __init__(self, file_path, sep=';', encoding='utf-8', sheet_name=0):

        self.file_path = file_path
        self.sep = sep
        self.encoding = encoding
        self.sheet_name = sheet_name
        self.df = None
        self.original_columns = None

    def cargar(self):

        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == '.csv':
            self.df = pd.read_csv(self.file_path, sep=self.sep, encoding=self.encoding)
        elif ext in ['.xlsx', '.xls']:
            self.df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        else:
            raise ValueError("Formato no soportado. Use .csv, .xlsx o .xls")
        self.original_columns = self.df.columns.tolist()
        print(f"Archivo cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        return self.df

    def limpiar_columnas(self):
        """Elimina espacios en nombres de columnas y en datos de tipo texto"""
        self.df.columns = self.df.columns.str.strip()
        texto_cols = self.df.select_dtypes(include=['object']).columns
        for col in texto_cols:
            self.df[col] = self.df[col].astype(str).str.strip()
        print("Columnas y texto limpiados.")

    def manejar_nulos(self, fill_text='Desconocido', fill_num=0):
        """Rellena nulos: texto con fill_text, numéricos con fill_num"""
        texto_cols = self.df.select_dtypes(include=['object']).columns
        self.df[texto_cols] = self.df[texto_cols].fillna(fill_text)
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[num_cols] = self.df[num_cols].fillna(fill_num)
        print("Nulos manejados.")

    def estandarizar_tiempo(self, dia_col='Día', mes_col='Mes'):
        """Limpia prefijos en columnas de día y mes (si existen)"""
        if dia_col in self.df.columns:
            self.df[dia_col] = self.df[dia_col].astype(str).str.replace(r'^\d+\.', '', regex=True)
        if mes_col in self.df.columns:
            self.df[mes_col] = self.df[mes_col].astype(str).str.replace(r'^[A-Z]\.\s?', '', regex=True)
        print("Día/Mes estandarizados.")

    def pipeline(self):
        """Ejecuta toda la limpieza y devuelve el DataFrame limpio"""
        self.cargar()
        self.limpiar_columnas()
        self.manejar_nulos()
        self.estandarizar_tiempo()
        return self.df

    def exportar_csv(self, ruta_salida, sep=';', encoding='utf-8', index=False):


        if self.df is None:
            raise ValueError("No hay datos cargados. Ejecute pipeline() primero.")
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        self.df.to_csv(ruta_salida, sep=sep, encoding=encoding, index=index)
        print(f"CSV exportado a: {ruta_salida}")

    def exportar_excel(self, ruta_salida, sheet_name='Datos', index=False):

        if self.df is None:
            raise ValueError("No hay datos cargados. Ejecute pipeline() primero.")
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        self.df.to_excel(ruta_salida, sheet_name=sheet_name, index=index)
        print(f"Excel exportado a: {ruta_salida}")