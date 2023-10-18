import pandas as pd
from typing import List, Tuple
import os

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    # Crea el nombre del archivo Parquet reemplazando la extensión .json por .parquet
    archivo_parquet = file_path.replace('.json', '.parquet')
    
    # Verifica si existe el archivo Parquet
    if os.path.exists(archivo_parquet):
        # Lee el archivo Parquet si existe
        df = pd.read_parquet(archivo_parquet)
    else:
        # Lee el archivo JSON si el Parquet no existe y lo guarda como Parquet
        df = pd.read_json(file_path, lines=True)
        df.to_parquet(archivo_parquet, index=False)
    
    # Encuentra menciones en el contenido de los tweets y crea una nueva columna 'mentions'
    df['menciones'] = df['content'].str.findall(r'@(\w+)')
    
    # Divide las filas del DataFrame por cada mención, creando múltiples filas duplicadas
    df = df.explode('menciones', ignore_index=True)
    
    # Calcula la frecuencia de menciones y crea un nuevo DataFrame con columnas 'nombre_de_usuario' y 'conteo'
    conteo_menciones = df['menciones'].value_counts().reset_index()
    conteo_menciones.columns = ['nombre_de_usuario', 'conteo']
    
    # Obtiene las 10 menciones más frecuentes como un iterable de tuplas sin índice
    top_menciones = conteo_menciones.head(10).itertuples(index=False, name=None)
    
    # Convierte el iterable en una lista de tuplas
    return list(top_menciones)