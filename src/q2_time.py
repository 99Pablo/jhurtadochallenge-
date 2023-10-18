import pandas as pd
import emoji
import os
from collections import Counter
from typing import List, Tuple


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