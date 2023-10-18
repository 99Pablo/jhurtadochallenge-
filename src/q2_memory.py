import ujson as json
import emoji
from collections import Counter
from typing import List, Tuple


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    # Inicializa un contador para contar emojis
    conteo_emojis = Counter()
    
    # Abre el archivo en modo lectura
    with open(file_path, 'r') as archivo:
        # Itera sobre cada línea en el archivo
        for linea in archivo:
            # Carga cada línea como un objeto JSON
            tweet = json.loads(linea)
            
            # Obtiene el contenido del tweet o una cadena vacía si no hay contenido
            contenido = tweet.get('content', '')
            
            # Extrae los emojis del contenido del tweet y actualiza el contador de emojis
            emojis_en_contenido = [entrada['emoji'] for entrada in emoji.emoji_list(contenido)]
            conteo_emojis.update(emojis_en_contenido)
    
    # Encuentra los 10 emojis más comunes
    top_emojis = conteo_emojis.most_common(10)
    
    return top_emojis