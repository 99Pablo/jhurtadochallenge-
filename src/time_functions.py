import os
import pandas as pd
import ujson as json
import emoji
import re
import cProfile
import pstats
from collections import Counter
from typing import List, Tuple
from datetime import datetime
from collections import defaultdict

def q1_time(archivo_json: str) -> List[Tuple[datetime.date, str]]:
    # Separar el nombre del archivo y su extensión
    nombre_archivo, _ = os.path.splitext(archivo_json)
    archivo_parquet = f"{nombre_archivo}.parquet"
    
    # Verificar si existe un archivo parquet más reciente que el JSON
    if os.path.exists(archivo_parquet) and os.path.getmtime(archivo_parquet) >= os.path.getmtime(archivo_json):
        # Si existe y es más reciente, cargar datos desde el archivo parquet
        df = pd.read_parquet(archivo_parquet)
    else:
        # Si no existe un archivo parquet o es más antiguo, cargar datos desde el JSON
        df = pd.read_json(archivo_json, lines=True)
        # Optimizar la conversión de fecha y extracción de nombre de usuario
        df['date'] = pd.to_datetime(df['date']).dt.date
        df['username'] = df['user'].apply(lambda x: x.get('username'))
        df.drop(columns=['user'], inplace=True)
        # Guardar los datos procesados en formato parquet
        df.to_parquet(archivo_parquet, index=False)

    # Obtener el usuario con más tweets para cada fecha de manera eficiente
    top_users_df = df.groupby(['date', 'username']).size().reset_index(name='count')
    top_users_df = top_users_df.loc[top_users_df.groupby('date')['count'].idxmax()]
    
    # Encontrar las 10 fechas con más tweets y los usuarios correspondientes de manera eficiente
    top_dates_df = df['date'].value_counts().nlargest(10).reset_index()
    result = [(fecha, top_users_df[top_users_df['date'] == fecha]['username'].values[0]) for fecha in top_dates_df['index']]
    
    return result

def q2_time(file_path: str) -> List[Tuple[str, int]]:
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
    
    # Inicializa una lista vacía para almacenar todos los emojis en el contenido de los tweets
    todos_emojis = []
    
    # Itera a través de la columna 'content' del DataFrame
    for contenido in df['content']:
        # Extrae los emojis de cada contenido y los agrega a la lista de todos los emojis
        emojis_en_contenido = [entrada['emoji'] for entrada in emoji.emoji_list(contenido)]
        todos_emojis.extend(emojis_en_contenido)
    
    # Cuenta la frecuencia de cada emoji
    conteo_emojis = Counter(todos_emojis)
    
    # Encuentra los 10 emojis más comunes
    top_emojis = conteo_emojis.most_common(10)
    
    return top_emojis

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