import requests
import pandas as pd
from datetime import datetime

class ClienteClima:
    def __init__(self, latitud=9.9281, longitud=-84.0907):
        """
        Inicializa el cliente para la API de Open-Meteo.
        Por defecto usa coordenadas del centro de San José.
        """
        self.lat = latitud
        self.lon = longitud
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"

    def obtener_lluvia_diaria(self, fecha_inicio, fecha_fin):
        """
        Obtiene la precipitación diaria para un rango de fechas.
        Args:
            fecha_inicio (str): Fecha de inicio en formato 'YYYY-MM-DD'.
            fecha_fin (str): Fecha de fin en formato 'YYYY-MM-DD'.
        Returns:
            pd.DataFrame: DataFrame con columnas 'fecha' y 'precipitacion_mm'.
        """
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'start_date': fecha_inicio,
            'end_date': fecha_fin,
            'daily': 'precipitation_sum',
            'timezone': 'America/Costa_Rica'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            daily = data['daily']
            df = pd.DataFrame({
                'fecha': pd.to_datetime(daily['time']),
                'precipitacion_mm': daily['precipitation_sum']
            })
            return df
        else:
            raise Exception(f"Error en la API de clima: {response.status_code}")