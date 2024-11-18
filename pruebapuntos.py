import folium
import math
from geopy.distance import geodesic

# Definir la ruta ideal como una lista de coordenadas (latitud, longitud)
ruta_ideal = [
    (-17.382463, -66.151018),
    (-17.382934, -66.149913),
    (-17.384204, -66.146308),
    (-17.385965, -66.147606),
    (-17.383415, -66.149462),
    (-17.383886, -66.151458),
    (-17.382678, -66.151640),
]

# Coordenadas de la ruta real tomada por el usuario (sin especificar el tercer número)
ruta_real = [
    (-17.382463, -66.151018),
    (-17.382934, -66.149913),
    (-17.382308, -66.149730),
    (-17.382613, -66.148544),
    (-17.383156, -66.148627),
    (-17.384204, -66.146308),
    (-17.385965, -66.147606),
    (-17.383415, -66.149462),
    (-17.383886, -66.151458),
    (-17.382678, -66.151640)
]

# Definir los márgenes de tolerancia en metros (5 metros alrededor de cada punto)
margen_tolerancia = 10  # margen de 5 metros para la latitud y longitud


# Función para calcular la distancia entre dos puntos utilizando geodesic de geopy
def calcular_distancia(punto1, punto2):
    """
    Calcula la distancia en metros entre dos puntos geográficos usando geopy.
    """
    return geodesic(punto1, punto2).meters


# Función para calcular el ángulo en grados entre dos puntos geográficos
def calcular_angulo(punto1, punto2):
    """
    Calcula el ángulo en grados (desde el norte) entre dos puntos geográficos.
    """
    lat1, lon1 = punto1
    lat2, lon2 = punto2

    # Convertir las coordenadas de grados a radianes
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Diferencias de longitud
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Calcular el ángulo (bearing) en radianes
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)

    # Calcular el ángulo en grados
    angulo = math.degrees(math.atan2(x, y))

    # Normalizar el ángulo para que esté entre 0 y 360 grados
    if angulo < 0:
        angulo += 360

    return angulo


# Función para calcular las coordenadas desplazadas en direcciones perpendiculares
def calcular_desplazamientos_perpendiculares(punto, angulo, margen_tolerancia):
    """
    Calcula los desplazamientos hacia la izquierda y la derecha (perpendiculares)
    a la línea que conecta los puntos, generando un rectángulo.
    """
    lat, lon = punto

    # Convertir el ángulo a radianes
    angulo_rad = math.radians(angulo)

    # Calcular los desplazamientos en las direcciones norte-sur y este-oeste
    dlat = margen_tolerancia / 111320.0  # Aproximadamente 1 metro en latitud
    dlon = margen_tolerancia / (111320.0 * abs(math.cos(math.radians(lat))))  # Aproximadamente 1 metro en longitud

    # Calcular las direcciones perpendiculares (izquierda y derecha)
    angulo_izquierda = angulo + 90  # 90 grados a la izquierda
    angulo_derecha = angulo - 90  # 90 grados a la derecha

    # Convertir esos ángulos a radianes
    angulo_izquierda_rad = math.radians(angulo_izquierda)
    angulo_derecha_rad = math.radians(angulo_derecha)

    # Desplazamientos en las direcciones perpendiculares
    izquierda = (lat + dlat * math.cos(angulo_izquierda_rad), lon + dlon * math.sin(angulo_izquierda_rad))
    derecha = (lat + dlat * math.cos(angulo_derecha_rad), lon + dlon * math.sin(angulo_derecha_rad))

    return izquierda, derecha


# Crear el mapa base centrado en el primer punto de la ruta
m = folium.Map(location=ruta_ideal[0], zoom_start=15)

# Añadir los puntos de la ruta ideal al mapa
for lat, lon in ruta_ideal:
    folium.Marker([lat, lon], popup=f"Ruta Ideal: ({lat}, {lon})", icon=folium.Icon(color='blue')).add_to(m)

# Añadir los puntos de la ruta real al mapa y calcular si están dentro o fuera de la zona de tolerancia
ruta_real_con_tolerancia = []  # Nueva lista para almacenar las coordenadas con el tercer valor

for i in range(len(ruta_real)):
    lat, lon = ruta_real[i]

    # Encontrar la coordenada más cercana de la ruta ideal para cada punto real
    distancias = [calcular_distancia((lat, lon), punto_ideal) for punto_ideal in ruta_ideal]
    distancia_minima = min(distancias)

    # Determinar si la coordenada está dentro o fuera del margen
    tercer_valor = 0 if distancia_minima <= margen_tolerancia else 1

    # Añadir el tercer valor (0 o 1) a la coordenada de la ruta real
    ruta_real_con_tolerancia.append((lat, lon, tercer_valor))

    # Determinar el color de la línea entre el punto actual y el siguiente
    if i > 0:
        lat1, lon1, _ = ruta_real_con_tolerancia[i - 1]
        lat2, lon2, _ = ruta_real_con_tolerancia[i]

        distancias1 = [calcular_distancia((lat1, lon1), punto_ideal) for punto_ideal in ruta_ideal]
        distancia_minima1 = min(distancias1)

        distancias2 = [calcular_distancia((lat2, lon2), punto_ideal) for punto_ideal in ruta_ideal]
        distancia_minima2 = min(distancias2)

        # Color de la línea: rojo si está fuera del margen, verde si está dentro
        color_linea = 'green' if distancia_minima1 <= margen_tolerancia and distancia_minima2 <= margen_tolerancia else 'red'

        # Dibujar la línea entre los puntos de la ruta real con el color correspondiente
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color=color_linea, weight=3).add_to(m)

# Añadir los puntos de la ruta real con el tercer valor
for lat, lon, tercer_valor in ruta_real_con_tolerancia:
    color_marker = 'green' if tercer_valor == 0 else 'red'
    folium.Marker([lat, lon], popup=f"Ruta Real: ({lat}, {lon}, {tercer_valor})",
                  icon=folium.Icon(color=color_marker)).add_to(m)

# También, se debe dibujar los rectángulos entre los puntos de la ruta ideal
for i in range(1, len(ruta_ideal)):
    punto_ideal1 = ruta_ideal[i - 1]
    punto_ideal2 = ruta_ideal[i]

    # Calcular el ángulo entre los dos puntos consecutivos de la ruta ideal
    angulo = calcular_angulo(punto_ideal1, punto_ideal2)

    # Calcular los desplazamientos perpendiculares (izquierda y derecha)
    izquierda1, derecha1 = calcular_desplazamientos_perpendiculares(punto_ideal1, angulo, margen_tolerancia)
    izquierda2, derecha2 = calcular_desplazamientos_perpendiculares(punto_ideal2, angulo, margen_tolerancia)

    # Crear el rectángulo utilizando los desplazamientos
    folium.Polygon(
        locations=[izquierda1, derecha1, derecha2, izquierda2],
        color='green', fill=True, fill_opacity=0.3, weight=2  # Añadir grosor con 'weight'
    ).add_to(m)

# Agregar un rectángulo entre la primera y última coordenada de la ruta ideal
punto_ideal1 = ruta_ideal[0]
punto_ideal2 = ruta_ideal[-1]

# Calcular el ángulo entre la primera y la última coordenada
angulo = calcular_angulo(punto_ideal1, punto_ideal2)

# Calcular los desplazamientos perpendiculares (izquierda y derecha)
izquierda1, derecha1 = calcular_desplazamientos_perpendiculares(punto_ideal1, angulo, margen_tolerancia)
izquierda2, derecha2 = calcular_desplazamientos_perpendiculares(punto_ideal2, angulo, margen_tolerancia)

# Crear el rectángulo entre la primera y la última coordenada
folium.Polygon(
    locations=[izquierda1, derecha1, derecha2, izquierda2],
    color='green', fill=True, fill_opacity=0.3, weight=2  # Añadir grosor con 'weight'
).add_to(m)

# Guardar el mapa como archivo HTML
m.save('mapa_ruta.html')

# Mostrar un mensaje para indicar que el mapa se ha generado
print("El mapa ha sido generado y guardado como 'mapa_ruta.html'. Puedes abrirlo en tu navegador.")
