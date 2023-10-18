import pandas as pd
from typing import List, Tuple
from datetime import datetime
import os


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