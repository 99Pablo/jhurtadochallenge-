import pandas as pd
import ujson as json
import emoji
import re
from collections import Counter
from typing import List, Tuple
from datetime import datetime
from collections import defaultdict

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Crear un diccionario anidado para contar usuarios por fecha
    usuarios_por_fecha = defaultdict(lambda: defaultdict(int))
    # Abrir el archivo en modo lectura
    with open(file_path, "r") as archivo:
        # Iterar sobre cada línea en el archivo
        for linea in archivo:
            # Cargar cada línea como un objeto JSON
            tweet = json.loads(linea)
            # Extraer la fecha del tweet y convertirla en un objeto de fecha
            fecha_tweet_str = tweet['date'].split("T")[0]
            fecha_tweet = datetime.strptime(fecha_tweet_str, '%Y-%m-%d').date()
            # Obtener el nombre de usuario del tweet
            nombre_usuario = tweet['user']['username']
            # Actualizar el contador de usuarios por fecha
            usuarios_por_fecha[fecha_tweet][nombre_usuario] += 1
    # Inicializar una lista vacía para almacenar las fechas y usuarios principales
    fechas_usuarios_principales = []
    # Iterar a través de las fechas y sus recuentos de usuarios
    for fecha, recuentos_usuarios in usuarios_por_fecha.items():
        # Encontrar el usuario con el recuento máximo para cada fecha
        usuario_principal = max(recuentos_usuarios, key=recuentos_usuarios.get)
        # Agregar la fecha y el usuario principal a la lista
        fechas_usuarios_principales.append((fecha, usuario_principal))
    # Ordenar la lista por recuento de usuarios en orden descendente y tomar las 10 primeras entradas
    resultado = sorted(fechas_usuarios_principales, key=lambda x: usuarios_por_fecha[x[0]][x[1]], reverse=True)[:10]

    return resultado

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