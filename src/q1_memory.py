import ujson as json
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