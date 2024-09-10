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
        Data_frame = pd.DataFrame.from_records(resultados)  # Convertir resultados en DataFrame

        if Data_frame.empty:
            logging.warning("No se encontraron datos para calcular la mediana.")
            return {}

        # Verificar que las columnas existen antes de continuar
        required_columns = ['ph_agua_suelo_2_5_1_0', 'f_sforo_p_bray_ii_mg_kg', 'potasio_k_intercambiable_cmol_kg']
        missing_columns = [col for col in required_columns if col not in Data_frame.columns]

        if missing_columns:
            logging.error(f"Faltan las siguientes columnas para calcular medianas: {missing_columns}")
            return {}
        
        # Extraer valores especiales (como "<3.87")
        valor_especial_ph = Data_frame['ph_agua_suelo_2_5_1_0'].apply(lambda valor_columna: valor_columna if isinstance(valor_columna, str) and '<' in valor_columna else None).dropna().unique()
        valor_especial_fosforo = Data_frame['f_sforo_p_bray_ii_mg_kg'].apply(lambda valor_columna: valor_columna if isinstance(valor_columna, str) and '<' in valor_columna else None).dropna().unique()
        valor_especial_potasio = Data_frame['potasio_k_intercambiable_cmol_kg'].apply(lambda valor_columna: valor_columna if isinstance(valor_columna, str) and '<' in valor_columna else None).dropna().unique()


        # Convertir columnas a numerico, solo las que no sean cadenas especiales para calcular la mediana
        Data_frame['ph_agua_suelo_2_5_1_0'] = pd.to_numeric(Data_frame['ph_agua_suelo_2_5_1_0'].where(Data_frame['ph_agua_suelo_2_5_1_0'].apply(lambda valor_columna: not isinstance(valor_columna, str) or '<' not in valor_columna)), errors='coerce')
        Data_frame['f_sforo_p_bray_ii_mg_kg'] = pd.to_numeric(Data_frame['f_sforo_p_bray_ii_mg_kg'].where(Data_frame['f_sforo_p_bray_ii_mg_kg'].apply(lambda valor_columna: not isinstance(valor_columna, str) or '<' not in valor_columna)), errors='coerce')
        Data_frame['potasio_k_intercambiable_cmol_kg'] = pd.to_numeric(Data_frame['potasio_k_intercambiable_cmol_kg'].where(Data_frame['potasio_k_intercambiable_cmol_kg'].apply(lambda valor_columna: not isinstance(valor_columna, str) or '<' not in valor_columna)), errors='coerce')

        
        # Calcular medianas ignorando NaN (que se descartan automáticamente)
        mediana_ph = valor_especial_ph[0] if len(valor_especial_ph) > 0 else Data_frame['ph_agua_suelo_2_5_1_0'].median()
        mediana_fosforo = valor_especial_fosforo[0] if len(valor_especial_fosforo) > 0 else Data_frame['f_sforo_p_bray_ii_mg_kg'].median()
        mediana_potasio = valor_especial_potasio[0] if len(valor_especial_potasio) > 0 else Data_frame['potasio_k_intercambiable_cmol_kg'].median()

        medianas = {
            'pH': mediana_ph,
            'Fósforo': mediana_fosforo,
            'Potasio': mediana_potasio
        }
        return medianas
