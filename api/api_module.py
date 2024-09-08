import pandas as pd
from sodapy import Socrata
import logging

class APIClient:
    def __init__(self, token=None):
        self.client = Socrata("www.datos.gov.co", token)

    def consultar_datos(self, departamento, municipio, cultivo, limit=1000):
        if not departamento or not municipio or not cultivo:
            logging.error("Los parámetros departamento, municipio y cultivo son obligatorios.")
            return pd.DataFrame()  # Retorna un DataFrame vacío en lugar de lista vacía
        
        query = f"departamento='{departamento}' AND municipio='{municipio}' AND cultivo='{cultivo}'"
        logging.info(f"Consulta realizada: {query}")
        try:
            results = self.client.get("ch4u-f3i5", where=query, limit=limit)
            return pd.DataFrame.from_records(results)
        except Exception as e:
            logging.error(f"Error al consultar datos: {e}")
            return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

    def calcular_mediana(self, resultados):
        df = pd.DataFrame.from_records(resultados)  # Convertir resultados en DataFrame

        if df.empty:
            logging.warning("No se encontraron datos para calcular la mediana.")
            return {}

        # Verificar que las columnas existen antes de continuar
        required_columns = ['ph_agua_suelo_2_5_1_0', 'f_sforo_p_bray_ii_mg_kg', 'potasio_k_intercambiable_cmol_kg']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            logging.error(f"Faltan las siguientes columnas para calcular medianas: {missing_columns}")
            return {}

        # Convertir columnas a numérico (forzando errores a NaN) para calcular la mediana
        df['ph_agua_suelo_2_5_1_0'] = pd.to_numeric(df['ph_agua_suelo_2_5_1_0'], errors='coerce')
        df['f_sforo_p_bray_ii_mg_kg'] = pd.to_numeric(df['f_sforo_p_bray_ii_mg_kg'], errors='coerce')
        df['potasio_k_intercambiable_cmol_kg'] = pd.to_numeric(df['potasio_k_intercambiable_cmol_kg'], errors='coerce')

        # Calcular medianas ignorando NaN (que se descartan automáticamente)
        mediana_ph = df['ph_agua_suelo_2_5_1_0'].median()
        mediana_fosforo = df['f_sforo_p_bray_ii_mg_kg'].median()
        mediana_potasio = df['potasio_k_intercambiable_cmol_kg'].median()

        medianas = {
            'pH': mediana_ph,
            'Fósforo': mediana_fosforo,
            'Potasio': mediana_potasio
        }
        return medianas
