import ujson as json

import re
from collections import Counter
from typing import List, Tuple


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # Inicializa un contador para contar menciones
    conteo_menciones = Counter()
    
    # Abre el archivo en modo lectura
    with open(file_path, 'r') as archivo:
        # Itera sobre cada línea en el archivo
        for linea in archivo:
            try:
                # Intenta cargar cada línea como un objeto JSON (puede haber excepciones JSONDecodeError)
                tweet = json.loads(linea)
                
                # Obtiene el contenido del tweet o una cadena vacía si no hay contenido
                contenido = tweet.get('content', '')
                
                # Encuentra menciones en el contenido del tweet
                menciones = re.findall(r'@(\w+)', contenido)
                
                # Actualiza el contador de menciones con las menciones encontradas
                conteo_menciones.update(menciones)
            except json.JSONDecodeError:
                # Captura excepciones JSONDecodeError en caso de líneas inválidas
                pass
    
    # Obtiene las 10 menciones más frecuentes
    top_menciones = conteo_menciones.most_common(10)
    
    return top_menciones